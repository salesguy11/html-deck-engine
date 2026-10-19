# html-deck-engine

제안서·보고서·소개서를 모션이 들어간 단일 HTML 발표 자료로 만드는 엔진입니다. 내용은 `deck.json`에만 쓰고, 빌더가 오프라인 단일 HTML로 묶습니다.

## 구성
- `engine/assets/` : engine.js(렌더링, 모션, 발표 모드, 스키마 검증), style.css(테마 3종), shell.html, fonts.css(Pretendard 내장)
- `engine/scripts/build.py` : deck.json 에서 HTML 생성
- `engine/scripts/ver.py` : 3개 해상도 오버플로 검사와 발표 모드 순회 (playwright 필요)
- `engine/scripts/prep_image.py` : 캡처 이미지를 WebP 로 변환, 영역 마스킹
- `examples/sample-report/` : 12가지 쪽 유형을 모두 쓴 샘플 (가상 데이터)

## 사용
```
python3 engine/scripts/build.py examples/sample-report/deck.json out.html --theme tech
python3 -I engine/scripts/ver.py out.html --shots shots
```
`--theme` 를 생략하면 deck.json 의 `meta.theme`(기본 apple)을 씁니다.

## 테마
- `apple` : 흰색과 회색 타일에 다크 타일을 교차, 포인트 파랑. 절제된 기본값
- `tech` : 짙은 남색 계열, 시안과 보라 포인트, 오로라 효과가 가장 도드라짐
- `editorial` : 따뜻한 종이색과 진한 갈색, 테라코타 포인트. 읽는 문서에 적합

## 쪽 유형과 글자 수 상한 (초과하면 열 때 화면에 오류 표시)
- cover: eyebrow40 title16* subtitle46* accent90 org40 image(선택)
- statement: eyebrow30 title60* lead130 badge30
- section: eyebrow30 title36* lead140 chips(0~6, 22자)
- cards: eyebrow30 title40* lead110 badge40 items(2~4: title24* body110*)
- metrics: eyebrow30 title40* lead110 items(3~12: value10* unit8 label34* badge18) foot110
- steps: eyebrow30 title40* lead110 items(3~5: title22* body100*)
- feature-shot: eyebrow30 title30* lead100 points(0~3: text60*) image* alt* side(right|left)
- rows: eyebrow30 title40* lead110 rows(2~8: label20* value110*) side(value8 unit6 caption40 notes0~3)
- timeline: eyebrow30 title46* lead110 aside(0~2: k8* title30* body100*) items(3~6: tag8* badge14 title30* body80*)
- quotes: eyebrow30 title40* columns(1~2: org40* role40 qa1~3: q60* a230*)
- gallery: eyebrow30 title40* lead110 image* alt* caption80. 가로로 긴 이미지(약 4:1) 전용
- contact: eyebrow30 title30* lead100 rows(1~6: label16* value60* href) org40 cta(text24* href*)
(* 필수) 모든 쪽 공통: bg(light|parch|dark), notes500, src120. 제목 안 `{강조}` 는 포인트 색.

## 보기 방법
문서 보기와 발표 모드 겸용입니다. 발표 모드는 방향키, O 는 쪽 목록, N 은 발표자 노트, 주소 뒤 `#pres/3` 은 3쪽 발표 모드, `#static` 은 모션 끄기(인쇄와 PDF 변환용)입니다.
