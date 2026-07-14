# SVG Recipe — Interlocking Chevron Agenda

## Visual mechanism
A vertical agenda is built from repeated, forward-flowing ribbon rows: each colored body has a sharp left chevron point and a rounded right end, while a detached gray chevron tip sits just to the left with a crisp white gap. Large step numbers anchor the sequence, and compact white icons at the far right reinforce each agenda topic.

## SVG primitives needed
- 1× `<rect>` for the white slide background
- 4× `<path>` for the colored main ribbon bodies with pointed left edges and rounded right corners
- 4× `<path>` for the detached light-gray interlocking chevron tips
- 1× `<filter id="softShadow">` applied to ribbon and chevron paths for subtle keynote depth
- 1× `<linearGradient>` for the decorative PowerPoint-style circle
- 2× `<circle>` and 2× `<rect>` for the small decorative app badge in the upper-left corner
- 10× `<text>` for title, subtitle, step numbers, and agenda descriptions
- Multiple `<path>`, `<line>`, and `<rect>` primitives for native editable white line icons at row ends
- Optional `<defs>` colors/filters only; no symbols or reusable `<use>` instances

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="pptGlow" x1="35" y1="20" x2="135" y2="110" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#ff8a65"/>
      <stop offset="1" stop-color="#c83b21"/>
    </linearGradient>
    <filter id="softShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feOffset dx="0" dy="5"/>
      <feGaussianBlur stdDeviation="5"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .16 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#ffffff"/>

  <!-- small decorative PowerPoint-style badge -->
  <circle cx="91" cy="60" r="43" fill="url(#pptGlow)" opacity="0.96"/>
  <path d="M91 17 A43 43 0 0 1 134 60 L91 60 Z" fill="#ff9f7f" opacity="0.8"/>
  <rect x="36" y="35" width="54" height="50" rx="5" fill="#b4321f" filter="url(#softShadow)"/>
  <rect x="44" y="42" width="37" height="36" rx="3" fill="#cf4a2f"/>
  <text x="52" y="69" width="32" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="30" font-weight="800" fill="#ffffff">P</text>

  <!-- left title block -->
  <text x="82" y="342" width="430" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="66" font-weight="900" fill="#1f5a86" letter-spacing="-3">AGENDA SLIDE</text>
  <text x="88" y="382" width="430" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" fill="#111111">
    <tspan x="88" dy="0">The quick brown fox jumps over the lazy</tspan>
    <tspan x="88" dy="29">dog. The quick brown fox jumps over the</tspan>
    <tspan x="88" dy="29">lazy dog.</tspan>
  </text>

  <!-- Row 01 -->
  <path d="M632 42 L558 109 L632 176 L716 176 L649 109 L716 42 Z" fill="#d7d7d7"/>
  <path d="M732 42 H1200 Q1222 42 1222 64 V154 Q1222 176 1200 176 H732 L664 109 Z" fill="#3434cc" filter="url(#softShadow)"/>
  <text x="728" y="131" width="85" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="64" font-weight="900" fill="#ffffff">01</text>
  <text x="816" y="84" width="310" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" fill="#ffffff">
    <tspan x="816" dy="0">The quick brown fox jumps over the</tspan>
    <tspan x="816" dy="25">lazy dog. The quick brown fox jumps</tspan>
    <tspan x="816" dy="25">over the lazy dog.</tspan>
  </text>
  <path d="M1134 130 L1158 105 L1168 116 L1194 91" fill="none" stroke="#ffffff" stroke-width="6"/>
  <path d="M1181 91 H1194 V104" fill="none" stroke="#ffffff" stroke-width="6"/>
  <circle cx="1140" cy="87" r="6" fill="#ffffff"/><circle cx="1155" cy="83" r="6" fill="#ffffff"/><circle cx="1170" cy="87" r="6" fill="#ffffff"/>
  <path d="M1130 112 C1135 98 1145 98 1150 112 M1147 113 C1153 98 1162 98 1167 113 M1164 114 C1170 99 1180 99 1185 114" fill="none" stroke="#ffffff" stroke-width="4"/>

  <!-- Row 02 -->
  <path d="M632 204 L558 271 L632 338 L716 338 L649 271 L716 204 Z" fill="#d7d7d7"/>
  <path d="M732 204 H1200 Q1222 204 1222 226 V316 Q1222 338 1200 338 H732 L664 271 Z" fill="#790038" filter="url(#softShadow)"/>
  <text x="728" y="293" width="85" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="64" font-weight="900" fill="#ffffff">02</text>
  <text x="824" y="248" width="312" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" fill="#ffffff">
    <tspan x="824" dy="0">The quick brown fox jumps over the</tspan>
    <tspan x="824" dy="25">lazy dog. The quick brown fox jumps</tspan>
    <tspan x="824" dy="25">over the lazy dog.</tspan>
  </text>
  <circle cx="1160" cy="272" r="25" fill="none" stroke="#ffffff" stroke-width="5"/>
  <circle cx="1160" cy="272" r="13" fill="none" stroke="#ffffff" stroke-width="5"/>
  <path d="M1160 272 L1187 245" fill="none" stroke="#ffffff" stroke-width="5"/>
  <path d="M1180 246 L1198 242 L1191 260" fill="#ffffff"/>

  <!-- Row 03 -->
  <path d="M632 366 L558 433 L632 500 L716 500 L649 433 L716 366 Z" fill="#d7d7d7"/>
  <path d="M732 366 H1200 Q1222 366 1222 388 V478 Q1222 500 1200 500 H732 L664 433 Z" fill="#2f982f" filter="url(#softShadow)"/>
  <text x="728" y="455" width="85" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="64" font-weight="900" fill="#ffffff">03</text>
  <text x="834" y="412" width="300" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" fill="#ffffff">
    <tspan x="834" dy="0">The quick brown fox jumps over the</tspan>
    <tspan x="834" dy="25">lazy dog. The quick brown fox jumps</tspan>
    <tspan x="834" dy="25">over the lazy dog.</tspan>
  </text>
  <line x1="1144" y1="456" x2="1192" y2="456" stroke="#ffffff" stroke-width="5"/>
  <line x1="1148" y1="456" x2="1148" y2="410" stroke="#ffffff" stroke-width="5"/>
  <rect x="1156" y="424" width="8" height="28" fill="#ffffff"/>
  <rect x="1172" y="436" width="8" height="16" fill="#ffffff"/>
  <rect x="1188" y="416" width="8" height="36" fill="#ffffff"/>
  <path d="M1156 414 L1172 427 L1181 418 L1192 431" fill="none" stroke="#ffffff" stroke-width="4"/>

  <!-- Row 04 -->
  <path d="M632 528 L558 595 L632 662 L716 662 L649 595 L716 528 Z" fill="#d7d7d7"/>
  <path d="M732 528 H1200 Q1222 528 1222 550 V640 Q1222 662 1200 662 H732 L664 595 Z" fill="#7200d8" filter="url(#softShadow)"/>
  <text x="728" y="617" width="85" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="64" font-weight="900" fill="#ffffff">04</text>
  <text x="844" y="574" width="300" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" fill="#ffffff">
    <tspan x="844" dy="0">The quick brown fox jumps over the</tspan>
    <tspan x="844" dy="25">lazy dog. The quick brown fox jumps</tspan>
    <tspan x="844" dy="25">over the lazy dog.</tspan>
  </text>
  <path d="M1150 583 L1177 574 L1203 583 L1177 594 Z" fill="none" stroke="#ffffff" stroke-width="5" stroke-linejoin="round"/>
  <path d="M1150 595 L1177 606 L1203 595" fill="none" stroke="#ffffff" stroke-width="5" stroke-linejoin="round"/>
  <path d="M1150 607 L1177 619 L1203 607" fill="none" stroke="#ffffff" stroke-width="5" stroke-linejoin="round"/>
</svg>
```

## Avoid in this skill
- ❌ Using `<use>` or `<symbol>` to duplicate the chevrons; duplicate the path geometry explicitly so PowerPoint keeps every row editable.
- ❌ Relying on `marker-end` for icon arrows; draw arrowheads as small paths or use direct `<line>`/`<path>` geometry.
- ❌ Applying `clip-path` to the ribbon paths; only images should receive clip paths in this translator.
- ❌ Building the main ribbon from overlapping rectangles only; the chevron point and rounded right edge need a custom `<path>` for the premium interlocking look.
- ❌ Making all rows the same color with only text changes; the technique depends on strong row-level color coding.

## Composition notes
- Reserve the left third of the slide for the title and short explanatory copy; keep it sparse so the chevron agenda dominates the right side.
- Align all gray tips vertically and keep a consistent white gap between the gray chevron and the colored ribbon point.
- Use large, bold white numbers near the left of each colored body; place descriptive text in the middle and icons at the far right.
- Keep row heights generous and vertical spacing even; the rhythm of repeated interlocking shapes is what makes the slide feel structured and executive.