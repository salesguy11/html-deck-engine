#!/usr/bin/env python3
"""deck.json -> 단일 HTML (오프라인, 외부 리소스 없음).
사용: build.py DECK.json OUT.html [--theme apple|tech|editorial]
deck.json: {"meta":{title,brand,lang,theme,logos?},"assets":{"key":"img/file.webp"},"pages":[...]}
이미지는 base64 로 내장한다. 스키마 검증은 엔진(engine.js CATALOG)이 열 때 수행하고 오류는 화면에 표시한다.
"""
import argparse, base64, json, mimetypes, os

HERE = os.path.dirname(os.path.abspath(__file__))
ASSET = os.path.join(HERE, '..', 'assets')

def rd(name):
    with open(os.path.join(ASSET, name), encoding='utf-8') as f:
        return f.read()

def jdump(o):
    return json.dumps(o, ensure_ascii=False, indent=2).replace('<', '\\u003c')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('deck'); ap.add_argument('out')
    ap.add_argument('--theme', choices=['apple', 'tech', 'editorial'], help='deck.json meta.theme 을 덮어씀')
    a = ap.parse_args()
    base = os.path.dirname(os.path.abspath(a.deck))
    deck = json.load(open(a.deck, encoding='utf-8'))
    if a.theme: deck.setdefault('meta', {})['theme'] = a.theme
    assets = {}
    for k, rel in (deck.pop('assets', {}) or {}).items():
        p = os.path.join(base, rel)
        mt = mimetypes.guess_type(p)[0] or 'image/webp'
        if p.endswith('.webp'): mt = 'image/webp'
        assets[k] = 'data:%s;base64,%s' % (mt, base64.b64encode(open(p, 'rb').read()).decode())
    html = rd('shell.html')
    for ph, val in [('__TITLE__', deck['meta']['title'].replace('<', '')), ('/*FONTS*/', rd('fonts.css')), ('/*STYLE*/', rd('style.css')),
                    ('/*DATA*/', jdump(deck)), ('/*ASSETS*/', json.dumps(assets)), ('/*ENGINE*/', rd('engine.js'))]:
        html = html.replace(ph, val, 1)
    with open(a.out, 'w', encoding='utf-8') as f: f.write(html)
    print('OK %s  %.2f MB  pages=%d  theme=%s' % (a.out, len(html.encode()) / 1e6, len(deck['pages']), deck['meta'].get('theme', 'apple')))

if __name__ == '__main__':
    main()
