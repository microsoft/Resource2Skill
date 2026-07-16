# SVG Recipe — Formal Document Template with Simulated Form Fields

## Visual mechanism
A polished slide is made to look like a formal fillable document: centered title, disciplined label/value rows, subtle paper styling, and input-like gray fields that simulate dynamic date and dropdown controls. The form-field illusion comes from light fills, thin borders, placeholder text, and small chevron icons inside the fields.

## SVG primitives needed
- 2× `<rect>` for the slide background and main paper sheet
- 1× `<linearGradient>` for the cool executive background
- 1× `<linearGradient>` for the soft paper fill
- 1× `<linearGradient>` for simulated input-field fills
- 1× `<filter id="paperShadow">` applied to the document sheet
- 1× `<filter id="fieldShadow">` applied to the active form controls
- 10× `<rect>` for section bands, form fields, dropdown fields, and subtle status chips
- 2× `<circle>` for the official-looking approval seal
- 8× `<line>` for separator rules, signature lines, and fill-in blanks
- 7× `<path>` for the folded-corner paper detail, dropdown chevrons, and decorative watermark strokes
- 20+× `<text>` for title, labels, field content, placeholders, and inline-styled document metadata
- Nested `<tspan>` inside selected `<text>` for mixed emphasis in the document header

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f3f6fb"/>
      <stop offset="55%" stop-color="#edf2f8"/>
      <stop offset="100%" stop-color="#dfe8f3"/>
    </linearGradient>
    <linearGradient id="paperGrad" x1="0" y1="45" x2="0" y2="675" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#fbfcfe"/>
    </linearGradient>
    <linearGradient id="fieldGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#f7f9fc"/>
      <stop offset="100%" stop-color="#edf1f6"/>
    </linearGradient>
    <filter id="paperShadow" x="-10%" y="-10%" width="120%" height="125%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="fieldShadow" x="-15%" y="-30%" width="130%" height="170%">
      <feOffset dx="0" dy="2"/>
      <feGaussianBlur stdDeviation="2"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <path d="M1040 95 C1115 135 1138 224 1080 284 C1027 340 934 306 927 232 C920 158 977 62 1040 95Z" fill="#dfe8f4" opacity="0.65"/>
  <path d="M204 605 C260 548 347 544 397 602 C432 643 399 684 333 680 C265 676 168 646 204 605Z" fill="#e7eef7" opacity="0.75"/>

  <rect x="150" y="45" width="980" height="630" rx="14" fill="url(#paperGrad)" filter="url(#paperShadow)"/>
  <path d="M1082 45 L1130 93 L1082 93 Z" fill="#edf1f6"/>
  <path d="M1082 45 L1130 93" stroke="#cfd8e3" stroke-width="1.2" fill="none"/>
  <rect x="150" y="45" width="980" height="8" rx="4" fill="#1f4e79"/>
  <rect x="190" y="83" width="900" height="1.5" fill="#d6dde7"/>

  <text x="640" y="127" width="900" text-anchor="middle" font-family="Microsoft YaHei, Segoe UI" font-size="38" font-weight="700" fill="#172033">會議記錄</text>
  <text x="640" y="165" width="900" text-anchor="middle" font-family="Microsoft YaHei, Segoe UI" font-size="22" fill="#303a4a">「年度策略例會」</text>
  <text x="194" y="198" width="360" font-family="Microsoft YaHei, Segoe UI" font-size="13" fill="#7c8795">
    <tspan font-weight="700" fill="#516070">文件編號：</tspan><tspan>MTG-2024-0528</tspan>
  </text>
  <text x="930" y="198" width="170" text-anchor="end" font-family="Microsoft YaHei, Segoe UI" font-size="13" fill="#7c8795">版本：v1.0</text>

  <rect x="190" y="220" width="900" height="54" rx="8" fill="#f7f9fc" stroke="#e1e7ef"/>
  <text x="222" y="254" width="210" font-family="Microsoft YaHei, Segoe UI" font-size="20" font-weight="700" fill="#111827">壹、時　　間：</text>
  <rect x="430" y="231" width="374" height="32" rx="5" fill="url(#fieldGrad)" stroke="#aeb9c6" filter="url(#fieldShadow)"/>
  <text x="448" y="253" width="320" font-family="Microsoft YaHei, Segoe UI" font-size="17" fill="#1f2937">113年5月28日（星期二）</text>
  <rect x="814" y="231" width="36" height="32" rx="5" fill="#e6ebf2" stroke="#aeb9c6"/>
  <path d="M826 243 L838 255 L850 243" fill="none" stroke="#465264" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>

  <line x1="190" y1="292" x2="1090" y2="292" stroke="#dbe2eb" stroke-width="1"/>
  <text x="222" y="326" width="210" font-family="Microsoft YaHei, Segoe UI" font-size="20" font-weight="700" fill="#111827">貳、開會地點：</text>
  <text x="430" y="326" width="350" font-family="Microsoft YaHei, Segoe UI" font-size="19" fill="#1f2937">501 會議室</text>
  <text x="780" y="326" width="130" font-family="Microsoft YaHei, Segoe UI" font-size="20" font-weight="700" fill="#111827">記錄：</text>
  <rect x="850" y="303" width="190" height="32" rx="5" fill="url(#fieldGrad)" stroke="#aeb9c6" filter="url(#fieldShadow)"/>
  <text x="866" y="325" width="135" font-family="Microsoft YaHei, Segoe UI" font-size="16" fill="#687386">請點擊選取</text>
  <path d="M1014 315 L1024 325 L1034 315" fill="none" stroke="#465264" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>

  <line x1="190" y1="353" x2="1090" y2="353" stroke="#dbe2eb" stroke-width="1"/>
  <text x="222" y="387" width="210" font-family="Microsoft YaHei, Segoe UI" font-size="20" font-weight="700" fill="#111827">參、主　　席：</text>
  <text x="430" y="387" width="250" font-family="Microsoft YaHei, Segoe UI" font-size="19" fill="#1f2937">王志明</text>
  <text x="690" y="387" width="150" font-family="Microsoft YaHei, Segoe UI" font-size="20" font-weight="700" fill="#111827">列席單位：</text>
  <line x1="820" y1="392" x2="1050" y2="392" stroke="#9aa6b5" stroke-width="1.4" stroke-dasharray="5 5"/>

  <line x1="190" y1="414" x2="1090" y2="414" stroke="#dbe2eb" stroke-width="1"/>
  <text x="222" y="448" width="210" font-family="Microsoft YaHei, Segoe UI" font-size="20" font-weight="700" fill="#111827">肆、出席人員：</text>
  <text x="430" y="448" width="280" font-family="Microsoft YaHei, Segoe UI" font-size="19" fill="#1f2937">（詳簽到單）</text>
  <line x1="662" y1="453" x2="1050" y2="453" stroke="#9aa6b5" stroke-width="1.4" stroke-dasharray="5 5"/>

  <rect x="190" y="476" width="900" height="124" rx="8" fill="#ffffff" stroke="#dbe2eb"/>
  <rect x="190" y="476" width="900" height="34" rx="8" fill="#f3f6fa"/>
  <text x="222" y="500" width="210" font-family="Microsoft YaHei, Segoe UI" font-size="19" font-weight="700" fill="#111827">伍、主席致詞：</text>
  <text x="222" y="545" width="830" font-family="Microsoft YaHei, Segoe UI" font-size="18" fill="#9aa3af">○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○</text>
  <line x1="222" y1="568" x2="1050" y2="568" stroke="#cbd5e1" stroke-width="1"/>
  <text x="222" y="588" width="830" font-family="Microsoft YaHei, Segoe UI" font-size="18" fill="#c0c7d1">○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○</text>

  <rect x="190" y="616" width="430" height="34" rx="6" fill="#f7f9fc" stroke="#e1e7ef"/>
  <text x="212" y="639" width="115" font-family="Microsoft YaHei, Segoe UI" font-size="17" font-weight="700" fill="#111827">審核狀態：</text>
  <rect x="330" y="623" width="92" height="20" rx="10" fill="#e8f3ed" stroke="#b9d9c6"/>
  <text x="376" y="638" width="82" text-anchor="middle" font-family="Microsoft YaHei, Segoe UI" font-size="12" font-weight="700" fill="#247146">待確認</text>
  <text x="450" y="639" width="150" font-family="Microsoft YaHei, Segoe UI" font-size="14" fill="#6b7280">可於會後補登</text>

  <circle cx="1008" cy="586" r="48" fill="none" stroke="#b91c1c" stroke-width="3" opacity="0.72"/>
  <circle cx="1008" cy="586" r="35" fill="none" stroke="#b91c1c" stroke-width="1.6" opacity="0.55"/>
  <text x="1008" y="580" width="80" text-anchor="middle" font-family="Microsoft YaHei, Segoe UI" font-size="14" font-weight="700" fill="#b91c1c" opacity="0.72">正式</text>
  <text x="1008" y="602" width="88" text-anchor="middle" font-family="Microsoft YaHei, Segoe UI" font-size="13" fill="#b91c1c" opacity="0.72">紀錄格式</text>
</svg>
```

## Avoid in this skill
- ❌ Real interactive form controls; PowerPoint output will be static, so simulate dropdowns and date fields visually with editable shapes.
- ❌ `<foreignObject>` for HTML inputs or tables; it will hard-fail and is not editable as PowerPoint content.
- ❌ `<textPath>` for seal text; use normal `<text>` and circles instead.
- ❌ Applying `clip-path` to rectangles or text for field effects; clipping is only reliable on `<image>`.
- ❌ Relying only on plain text rows; without field fills, borders, chevrons, and rules, the form metaphor becomes weak.

## Composition notes
- Keep the document sheet centered with generous margins; the slide background should feel secondary and quiet.
- Use strict x-alignment: labels share one left column, values start on a consistent vertical axis, and dropdown controls align to the right.
- Reserve light gray-blue fills for simulated editable fields only, so viewers immediately understand what is “fillable.”
- Add one premium detail, such as a paper fold, approval seal, or status chip, but keep it subtle to preserve the formal document tone.