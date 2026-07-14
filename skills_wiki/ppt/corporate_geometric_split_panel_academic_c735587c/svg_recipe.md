# SVG Recipe — Geometric Split-Panel Layout

## Visual mechanism
A dark geometric anchor panel occupies the left quarter of the slide and carries the main topic in white, while the right side remains a crisp white structured workspace for dense academic or consulting content. Subtle cards, rule lines, and hanging-indented references convert text-heavy material into a disciplined executive layout.

## SVG primitives needed
- 1× full-slide `<rect>` for the white background
- 1× large `<rect>` for the left split-panel anchor
- 2× `<path>` for angled geometric overlays inside the anchor panel
- 1× `<linearGradient>` for the navy anchor depth
- 1× `<filter id="softShadow">` applied to right-side content cards
- 4× rounded `<rect>` for structured content cards and section headers
- 8× `<line>` for grid rules, dividers, and bullet guide strokes
- 10× `<circle>` for premium bullet dots and numbered section markers
- Multiple `<text>` elements with explicit `width` for title, section labels, bullets, metadata, and hanging-indent references
- Nested `<tspan>` elements for multiline labels and inline emphasis

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="navyDepth" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#16395f"/>
      <stop offset="58%" stop-color="#1f497d"/>
      <stop offset="100%" stop-color="#102a46"/>
    </linearGradient>
    <filter id="softShadow" x="-10%" y="-10%" width="130%" height="130%">
      <feOffset dx="0" dy="6"/>
      <feGaussianBlur stdDeviation="8"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#ffffff"/>

  <!-- left geometric anchor -->
  <rect x="0" y="0" width="360" height="720" fill="url(#navyDepth)"/>
  <path d="M230 0 L360 0 L360 720 L120 720 C210 585 252 435 248 285 C245 170 222 82 230 0 Z" fill="#2f5f97" opacity="0.34"/>
  <path d="M0 545 L360 400 L360 720 L0 720 Z" fill="#0b2138" opacity="0.28"/>
  <line x1="360" y1="0" x2="360" y2="720" stroke="#d9e2ef" stroke-width="2"/>

  <text x="48" y="78" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600" fill="#c9d8ea" letter-spacing="2">
    RESEARCH BRIEF
  </text>
  <line x1="48" y1="104" x2="168" y2="104" stroke="#c9d8ea" stroke-width="3"/>
  <text x="48" y="178" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="44" font-weight="700" fill="#ffffff">
    <tspan x="48" dy="0">Company</tspan>
    <tspan x="48" dy="52">History</tspan>
    <tspan x="48" dy="52">&amp; Strategic</tspan>
    <tspan x="48" dy="52">Position</tspan>
  </text>
  <text x="48" y="484" width="238" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#e7eef7">
    <tspan x="48" dy="0">Prepared for STM 252</tspan>
    <tspan x="48" dy="26">Strategic Management</tspan>
    <tspan x="48" dy="26">Chelsea Seburn · 2026</tspan>
  </text>
  <circle cx="54" cy="650" r="4" fill="#ffffff"/>
  <circle cx="74" cy="650" r="4" fill="#9fb8d7"/>
  <circle cx="94" cy="650" r="4" fill="#9fb8d7"/>

  <!-- right content workspace -->
  <text x="424" y="76" width="730" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#242a31">
    Evidence-based summary
  </text>
  <text x="424" y="108" width="650" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#6b7280">
    Dense academic content arranged on a strict grid with clear typographic hierarchy.
  </text>
  <line x1="424" y1="134" x2="1184" y2="134" stroke="#d6dde7" stroke-width="1.5"/>

  <rect x="424" y="166" width="340" height="196" rx="14" fill="#ffffff" stroke="#e1e7ef" stroke-width="1.2" filter="url(#softShadow)"/>
  <rect x="446" y="188" width="48" height="48" rx="12" fill="#1f497d"/>
  <text x="463" y="220" width="20" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#ffffff">1</text>
  <text x="512" y="206" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#27313d">
    Foundational context
  </text>
  <line x1="512" y1="226" x2="722" y2="226" stroke="#d6dde7" stroke-width="1"/>
  <circle cx="462" cy="260" r="4.5" fill="#1f497d"/>
  <text x="480" y="266" width="238" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#3c3c3c">
    Expansion through service-line specialization
  </text>
  <circle cx="462" cy="296" r="4.5" fill="#1f497d"/>
  <text x="480" y="302" width="238" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#3c3c3c">
    Governance model emphasizes partner accountability
  </text>
  <circle cx="462" cy="332" r="4.5" fill="#1f497d"/>
  <text x="480" y="338" width="238" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#3c3c3c">
    Reputation anchored in long-cycle advisory work
  </text>

  <rect x="804" y="166" width="340" height="196" rx="14" fill="#ffffff" stroke="#e1e7ef" stroke-width="1.2" filter="url(#softShadow)"/>
  <rect x="826" y="188" width="48" height="48" rx="12" fill="#1f497d"/>
  <text x="843" y="220" width="20" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#ffffff">2</text>
  <text x="892" y="206" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#27313d">
    Competitive posture
  </text>
  <line x1="892" y1="226" x2="1102" y2="226" stroke="#d6dde7" stroke-width="1"/>
  <circle cx="842" cy="260" r="4.5" fill="#1f497d"/>
  <text x="860" y="266" width="238" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#3c3c3c">
    Differentiated by analytical rigor and trust
  </text>
  <circle cx="842" cy="296" r="4.5" fill="#1f497d"/>
  <text x="860" y="302" width="238" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#3c3c3c">
    Premium pricing sustained by senior expertise
  </text>
  <circle cx="842" cy="332" r="4.5" fill="#1f497d"/>
  <text x="860" y="338" width="238" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#3c3c3c">
    Risk: digital entrants compress baseline analysis
  </text>

  <rect x="424" y="402" width="720" height="190" rx="14" fill="#f8fafc" stroke="#dbe3ee" stroke-width="1.2"/>
  <rect x="448" y="428" width="160" height="28" rx="14" fill="#e8eef7"/>
  <text x="468" y="448" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#1f497d" letter-spacing="1">
    APA REFERENCES
  </text>
  <text x="448" y="490" width="650" font-family="Segoe UI, Microsoft YaHei" font-size="13.5" fill="#3c3c3c">
    <tspan x="448" dy="0">Porter, M. E. (1985). </tspan><tspan font-style="italic">Competitive advantage.</tspan><tspan> Free Press.</tspan>
  </text>
  <text x="448" y="528" width="650" font-family="Segoe UI, Microsoft YaHei" font-size="13.5" fill="#3c3c3c">
    <tspan x="448" dy="0">Rumelt, R. P. (2011). </tspan><tspan font-style="italic">Good strategy/bad strategy.</tspan>
    <tspan x="488" dy="20">Crown Business.</tspan>
  </text>
  <text x="448" y="580" width="650" font-family="Segoe UI, Microsoft YaHei" font-size="13.5" fill="#3c3c3c">
    <tspan x="448" dy="0">Teece, D. J. (2018). Dynamic capabilities as workable systems theory.</tspan>
    <tspan x="488" dy="20">Journal of Management &amp; Organization, 24(3), 359–368.</tspan>
  </text>

  <line x1="424" y1="636" x2="1144" y2="636" stroke="#d6dde7" stroke-width="1"/>
  <text x="424" y="666" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6b7280">
    Slide rule: 30% anchor panel · 70% structured evidence field
  </text>
  <text x="1080" y="666" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#1f497d">
    02 / 08
  </text>
</svg>
```

## Avoid in this skill
- ❌ Decorative photos or icons that compete with the text-first academic structure
- ❌ Centered body paragraphs; this style depends on strong left alignment and grid discipline
- ❌ Overly narrow right content columns that create excessive wrapping
- ❌ Low-contrast anchor colors; the split-panel must clearly separate “topic” from “evidence”
- ❌ Using `<textPath>`, `<foreignObject>`, or HTML-like text boxes for hanging indents; build them with native `<text>` and `<tspan>`

## Composition notes
- Keep the anchor panel at roughly 25–30% of slide width; the right field should feel spacious enough for dense text.
- Use the left panel only for metadata: topic title, course/client label, date, or section number.
- Align all right-side content to one vertical axis, with cards and reference blocks sharing the same left edge.
- Limit color rhythm to navy, charcoal, white, and pale blue-gray so the slide feels authoritative rather than decorative.