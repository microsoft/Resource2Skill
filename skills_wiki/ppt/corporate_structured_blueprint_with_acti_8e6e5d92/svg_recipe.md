# SVG Recipe — Corporate Blueprint with Progress Navigator

## Visual mechanism
A disciplined corporate master layout uses a persistent top navigation sequence to orient the audience, with the current section highlighted in a vivid accent while inactive sections remain muted. The rest of the slide follows a strict grid: logo top-right, title and accent rule below, structured content canvas, and unobtrusive footer metadata.

## SVG primitives needed
- 1× `<rect>` for the white slide background
- 1× `<rect>` for a faint header band / master-slide zone
- 1× `<text>` with nested `<tspan>` for the active progress navigator
- 1× `<rect>` for the active navigator highlight capsule
- 1× `<rect>` + 1× `<text>` for the corporate logo mark
- 1× `<text>` for the slide title
- 1× `<rect>` for the title accent rule
- 3× `<rect>` for structured content cards
- 3× `<text>` for card headings
- 3× `<text>` blocks with nested `<tspan>` for body copy / bullets
- Multiple `<line>` elements for grid guides, column dividers, footer rules, and fine blueprint structure
- 2× `<path>` for subtle decorative blueprint brackets / progress-routing accents
- 1× `<linearGradient>` for the active accent rule
- 1× `<filter id="softShadow">` applied to content cards and logo block
- 1× `<filter id="magentaGlow">` applied to the active navigator capsule

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="accentGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#D500F9"/>
      <stop offset="100%" stop-color="#7C4DFF"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="magentaGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="5" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Master background -->
  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>
  <rect x="0" y="0" width="1280" height="96" fill="#FAFAFC"/>
  <line x1="64" y1="96" x2="1216" y2="96" stroke="#E8E8EE" stroke-width="1"/>

  <!-- Active navigator -->
  <line x1="64" y1="48" x2="372" y2="48" stroke="#D9D9DF" stroke-width="2"/>
  <rect x="232" y="28" width="42" height="40" rx="20" fill="#D500F9" filter="url(#magentaGlow)"/>
  <text x="64" y="55" width="340" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#969696">
    <tspan>1</tspan><tspan dx="18">|</tspan>
    <tspan dx="18">2</tspan><tspan dx="18">|</tspan>
    <tspan dx="18">3</tspan><tspan dx="18">|</tspan>
    <tspan dx="18" fill="#FFFFFF" font-weight="700">4</tspan><tspan dx="18">|</tspan>
    <tspan dx="18">5</tspan><tspan dx="18">|</tspan>
    <tspan dx="18">6</tspan><tspan dx="18">|</tspan>
    <tspan dx="18">7</tspan>
  </text>
  <text x="64" y="78" width="340" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="10" fill="#A8A8B0" letter-spacing="1.6">
    STRATEGIC OPERATING REVIEW
  </text>

  <!-- Logo block -->
  <rect x="1148" y="28" width="68" height="48" rx="6" fill="#1A1A1A" filter="url(#softShadow)"/>
  <text x="1165" y="60" width="40" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="21" font-weight="700" fill="#D500F9">
    PM
  </text>

  <!-- Title zone -->
  <text x="64" y="154" width="920" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="42" font-weight="700" fill="#1A1A1A">
    Q3 Operating Review
  </text>
  <text x="66" y="188" width="760" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#6B6B72">
    Section 04 · Execution cadence, risk posture, and next-quarter commitments
  </text>
  <rect x="64" y="216" width="172" height="5" rx="2.5" fill="url(#accentGrad)"/>

  <!-- Subtle blueprint guides -->
  <line x1="64" y1="258" x2="1216" y2="258" stroke="#EFEFF4" stroke-width="1"/>
  <line x1="64" y1="604" x2="1216" y2="604" stroke="#EFEFF4" stroke-width="1"/>
  <line x1="440" y1="258" x2="440" y2="604" stroke="#F0F0F5" stroke-width="1"/>
  <line x1="816" y1="258" x2="816" y2="604" stroke="#F0F0F5" stroke-width="1"/>
  <path d="M64 252 L64 232 L92 232" fill="none" stroke="#D500F9" stroke-width="2"/>
  <path d="M1216 610 L1216 630 L1188 630" fill="none" stroke="#D500F9" stroke-width="2"/>

  <!-- Content card 1 -->
  <rect x="64" y="286" width="336" height="264" rx="14" fill="#FFFFFF" stroke="#E7E7EE" stroke-width="1" filter="url(#softShadow)"/>
  <text x="92" y="330" width="280" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#1A1A1A">
    Core Principles
  </text>
  <rect x="92" y="350" width="52" height="4" rx="2" fill="#D500F9"/>
  <text x="92" y="392" width="270" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#333333">
    <tspan x="92" dy="0">• Maintain one strategic narrative</tspan>
    <tspan x="92" dy="32">• Use section numbers as wayfinding</tspan>
    <tspan x="92" dy="32">• Reserve accent color for progress</tspan>
    <tspan x="92" dy="32">• Keep footer metadata consistent</tspan>
  </text>

  <!-- Content card 2 -->
  <rect x="472" y="286" width="336" height="264" rx="14" fill="#FFFFFF" stroke="#E7E7EE" stroke-width="1" filter="url(#softShadow)"/>
  <text x="500" y="330" width="280" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#1A1A1A">
    Operating Rhythm
  </text>
  <rect x="500" y="350" width="52" height="4" rx="2" fill="#D500F9"/>
  <text x="500" y="392" width="270" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#333333">
    <tspan x="500" dy="0">• Quarterly performance snapshot</tspan>
    <tspan x="500" dy="32">• Function-level dependency review</tspan>
    <tspan x="500" dy="32">• Decision log with accountable owners</tspan>
    <tspan x="500" dy="32">• Next-step commitments by date</tspan>
  </text>

  <!-- Content card 3 -->
  <rect x="880" y="286" width="336" height="264" rx="14" fill="#FFFFFF" stroke="#E7E7EE" stroke-width="1" filter="url(#softShadow)"/>
  <text x="908" y="330" width="280" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#1A1A1A">
    Executive Signal
  </text>
  <rect x="908" y="350" width="52" height="4" rx="2" fill="#D500F9"/>
  <text x="908" y="392" width="270" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#333333">
    <tspan x="908" dy="0">• Audience always knows location</tspan>
    <tspan x="908" dy="32">• Document feels governed and complete</tspan>
    <tspan x="908" dy="32">• Reusable across long-form decks</tspan>
    <tspan x="908" dy="32">• Brand discipline without clutter</tspan>
  </text>

  <!-- Footer -->
  <line x1="64" y1="650" x2="1216" y2="650" stroke="#E8E8EE" stroke-width="1"/>
  <text x="64" y="678" width="640" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#969696">
    Source: Internal operating cadence review · Confidential
  </text>
  <text x="1138" y="678" width="78" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#969696">
    04 / 27
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using `<marker-end>` for navigator arrows; if directional cues are needed, draw them with plain `<line>` or `<path>` geometry.
- ❌ Applying filters to `<line>` elements; shadows/glows should sit on rectangles, circles, paths, or text.
- ❌ Building the navigator with `<use>` or `<symbol>` reuse; duplicate simple shapes directly for reliable PowerPoint editability.
- ❌ Omitting `width` on `<text>` elements; the PowerPoint translator relies on explicit text box widths.
- ❌ Over-decorating the header; the navigator must remain a quiet master element, not compete with the slide title.

## Composition notes
- Keep the top 12–15% of the slide reserved for persistent wayfinding: navigator left, logo right, no body content.
- Use the accent color sparingly: active step, title rule, and small structural cues only.
- Preserve generous whitespace between the title zone and content canvas so the slide feels executive rather than crowded.
- Footer should be low-contrast and consistent across the deck: source left, page/section count right.