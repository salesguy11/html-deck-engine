#!/usr/bin/env python3
"""빌드된 HTML 검증: 3개 해상도에서 가로 스크롤, 쪽 밖으로 나간 요소, 본문 오버플로, 콘솔 오류를 검사하고
발표 모드로 끝까지 넘겨 본다. 사용: ver.py OUT.html [--shots DIR]  (playwright 필요)
"""
import asyncio, os, sys
from playwright.async_api import async_playwright
AUDIT = """()=>{const out=[];document.querySelectorAll('.tile').forEach((t,i)=>{
 const tr=t.getBoundingClientRect();const sc=tr.width/1920;
 t.querySelectorAll('.body *,.tsrc,.tfoot,.cv-t,.cv-s,.cv-a,.cv-o,.cv-eb').forEach(e=>{
  if(e.children.length&&e.tagName!=='LI'&&e.tagName!=='H3'&&e.tagName!=='P')return;
  const r=e.getBoundingClientRect();
  if(r.width&&(r.right>tr.right+1||r.bottom>tr.bottom+1||r.left<tr.left-1))out.push([i+1,'outside',e.className||e.tagName]);});
 const b=t.querySelector('.body');if(b){const br=b.getBoundingClientRect();
  b.querySelectorAll('*').forEach(e=>{const r=e.getBoundingClientRect();if(r.width&&r.bottom>br.bottom+2)out.push([i+1,'overflow-body',e.className||e.tagName,Math.round((r.bottom-br.bottom)/sc)])});}
 });return out}"""
async def main(path, shots):
    bad = 0
    async with async_playwright() as p:
        br = await p.chromium.launch()
        for (w, h) in [(1366, 768), (1920, 1080), (2560, 1440)]:
            pg = await br.new_page(viewport={'width': w, 'height': h})
            errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else 0)
            await pg.goto('file://' + os.path.abspath(path) + '#static'); await pg.wait_for_timeout(500)
            hs = await pg.evaluate("document.documentElement.scrollWidth-document.documentElement.clientWidth")
            a = await pg.evaluate(AUDIT)
            n = await pg.evaluate("document.querySelectorAll('.tile').length")
            verr = await pg.evaluate("document.querySelector('.errbox')?document.querySelector('.errbox').innerText:''")
            print(w, h, 'pages', n, 'hscroll', hs, 'audit', a, 'err', errs, 'schema', verr or 'ok')
            bad += (hs > 0) + len(a) + len(errs) + (1 if verr else 0)
            await pg.evaluate("__deck.enterPres(0)"); await pg.wait_for_timeout(300)
            for i in range(n):
                if i: await pg.keyboard.press('ArrowRight')
                await pg.wait_for_timeout(700)
                if shots and w == 1920:
                    os.makedirs(shots, exist_ok=True); await pg.screenshot(path=os.path.join(shots, 'p%02d.png' % (i + 1)))
            a2 = await pg.evaluate(AUDIT); bad += len(a2)
            print('  presentation audit', a2)
            await pg.close()
        await br.close()
    print('RESULT', 'PASS' if bad == 0 else 'FAIL (%d)' % bad)
    sys.exit(1 if bad else 0)
if __name__ == '__main__':
    asyncio.run(main(sys.argv[1], sys.argv[sys.argv.index('--shots') + 1] if '--shots' in sys.argv else None))
