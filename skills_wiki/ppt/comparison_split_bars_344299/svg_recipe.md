# SVG Recipe — Comparison Split Bars

## Visual mechanism
A vertical center spine divides two products while paired horizontal bars extend outward from the center to show relative strength across shared metrics. The metric labels sit in a central “hinge” column, making the comparison symmetrical, scannable, and executive-friendly.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background
- 1× `<rect>` for the main rounded comparison card
- 2× `<path>` for large blurred decorative background glows
- 2× `<rect>` for left/right product header panels
- 10× `<rect>` for muted horizontal track rails behind each bar
- 10× `<rect>` for the actual diverging performance bars
- 5× `<rect>` for central metric label pills
- 1× `<line>` for the vertical center axis
- 10× `<line>` for subtle row separators and scale ticks
- Multiple `<text>` elements for title, product names, descriptions, scores, metric labels, and axis captions
- 3× `<linearGradient>` for background, left bars, right bars, and card highlights
- 1× `<filter id="softShadow">` applied to card and header panels
- 1× `<filter id="barGlow">` applied to high-value bars for premium emphasis
- 1× `<filter id="blurAura">` applied to decorative background paths

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#07111F"/>
      <stop offset="0.55" stop-color="#0B1730"/>
      <stop offset="1" stop-color="#111827"/>
    </linearGradient>
    <linearGradient id="cardGrad" x1="160" y1="130" x2="1120" y2="650" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#13243D"/>
      <stop offset="1" stop-color="#0D1628"/>
    </linearGradient>
    <linearGradient id="leftBar" x1="620" y1="0" x2="250" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#67E8F9"/>
      <stop offset="1" stop-color="#2563EB"/>
    </linearGradient>
    <linearGradient id="rightBar" x1="660" y1="0" x2="1030" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#A7F3D0"/>
      <stop offset="1" stop-color="#10B981"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="barGlow" x="-20%" y="-120%" width="140%" height="340%">
      <feGaussianBlur stdDeviation="5"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="blurAura" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="42"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <path d="M58 132 C178 42 322 60 398 158 C486 270 395 389 247 365 C117 344 -39 246 58 132 Z" fill="#1D4ED8" opacity="0.22" filter="url(#blurAura)"/>
  <path d="M1010 88 C1162 38 1272 146 1236 284 C1202 414 1024 438 944 326 C872 224 886 130 1010 88 Z" fill="#10B981" opacity="0.18" filter="url(#blurAura)"/>

  <text x="80" y="72" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#F8FAFC">Platform capability comparison</text>
  <text x="82" y="104" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#94A3B8">Diverging bars show relative performance across shared buying criteria</text>

  <rect x="150" y="132" width="980" height="520" rx="34" fill="url(#cardGrad)" stroke="#203453" stroke-width="1.2" filter="url(#softShadow)"/>
  <rect x="188" y="166" width="398" height="82" rx="22" fill="#0B2A4D" stroke="#235A9F" stroke-width="1" filter="url(#softShadow)"/>
  <rect x="694" y="166" width="398" height="82" rx="22" fill="#0B332B" stroke="#1E8A67" stroke-width="1" filter="url(#softShadow)"/>

  <text x="218" y="199" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#E0F2FE">Product A</text>
  <text x="218" y="225" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#93C5FD">High-control architecture for technical teams</text>
  <text x="1062" y="199" width="300" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#DCFCE7">Product B</text>
  <text x="1062" y="225" width="330" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#86EFAC">Managed experience optimized for rollout speed</text>

  <line x1="640" y1="257" x2="640" y2="596" stroke="#CBD5E1" stroke-width="2" opacity="0.55"/>
  <text x="525" y="278" width="90" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#64748B">A stronger</text>
  <text x="665" y="278" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#64748B">B stronger</text>

  <line x1="250" y1="302" x2="1030" y2="302" stroke="#334155" stroke-width="1" opacity="0.45"/>
  <line x1="250" y1="372" x2="1030" y2="372" stroke="#334155" stroke-width="1" opacity="0.45"/>
  <line x1="250" y1="442" x2="1030" y2="442" stroke="#334155" stroke-width="1" opacity="0.45"/>
  <line x1="250" y1="512" x2="1030" y2="512" stroke="#334155" stroke-width="1" opacity="0.45"/>
  <line x1="250" y1="582" x2="1030" y2="582" stroke="#334155" stroke-width="1" opacity="0.45"/>

  <line x1="320" y1="266" x2="320" y2="596" stroke="#334155" stroke-width="1" stroke-dasharray="4 8" opacity="0.35"/>
  <line x1="480" y1="266" x2="480" y2="596" stroke="#334155" stroke-width="1" stroke-dasharray="4 8" opacity="0.35"/>
  <line x1="800" y1="266" x2="800" y2="596" stroke="#334155" stroke-width="1" stroke-dasharray="4 8" opacity="0.35"/>
  <line x1="960" y1="266" x2="960" y2="596" stroke="#334155" stroke-width="1" stroke-dasharray="4 8" opacity="0.35"/>

  <rect x="280" y="294" width="340" height="18" rx="9" fill="#1E293B"/>
  <rect x="660" y="294" width="340" height="18" rx="9" fill="#1E293B"/>
  <rect x="348" y="294" width="272" height="18" rx="9" fill="url(#leftBar)" filter="url(#barGlow)"/>
  <rect x="660" y="294" width="238" height="18" rx="9" fill="url(#rightBar)"/>
  <rect x="590" y="285" width="100" height="36" rx="18" fill="#0F172A" stroke="#334155" stroke-width="1"/>
  <text x="640" y="308" width="100" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#E2E8F0">Security</text>
  <text x="334" y="309" width="50" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#BAE6FD">80</text>
  <text x="912" y="309" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#BBF7D0">70</text>

  <rect x="280" y="364" width="340" height="18" rx="9" fill="#1E293B"/>
  <rect x="660" y="364" width="340" height="18" rx="9" fill="#1E293B"/>
  <rect x="450" y="364" width="170" height="18" rx="9" fill="url(#leftBar)"/>
  <rect x="660" y="364" width="306" height="18" rx="9" fill="url(#rightBar)" filter="url(#barGlow)"/>
  <rect x="590" y="355" width="100" height="36" rx="18" fill="#0F172A" stroke="#334155" stroke-width="1"/>
  <text x="640" y="378" width="100" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#E2E8F0">Ease of use</text>
  <text x="436" y="379" width="50" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#BAE6FD">50</text>
  <text x="980" y="379" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#BBF7D0">90</text>

  <rect x="280" y="434" width="340" height="18" rx="9" fill="#1E293B"/>
  <rect x="660" y="434" width="340" height="18" rx="9" fill="#1E293B"/>
  <rect x="365" y="434" width="255" height="18" rx="9" fill="url(#leftBar)"/>
  <rect x="660" y="434" width="204" height="18" rx="9" fill="url(#rightBar)"/>
  <rect x="590" y="425" width="100" height="36" rx="18" fill="#0F172A" stroke="#334155" stroke-width="1"/>
  <text x="640" y="448" width="100" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#E2E8F0">Integration</text>
  <text x="351" y="449" width="50" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#BAE6FD">75</text>
  <text x="878" y="449" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#BBF7D0">60</text>

  <rect x="280" y="504" width="340" height="18" rx="9" fill="#1E293B"/>
  <rect x="660" y="504" width="340" height="18" rx="9" fill="#1E293B"/>
  <rect x="314" y="504" width="306" height="18" rx="9" fill="url(#leftBar)" filter="url(#barGlow)"/>
  <rect x="660" y="504" width="187" height="18" rx="9" fill="url(#rightBar)"/>
  <rect x="590" y="495" width="100" height="36" rx="18" fill="#0F172A" stroke="#334155" stroke-width="1"/>
  <text x="640" y="518" width="100" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#E2E8F0">Customization</text>
  <text x="300" y="519" width="50" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#BAE6FD">90</text>
  <text x="861" y="519" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#BBF7D0">55</text>

  <rect x="280" y="574" width="340" height="18" rx="9" fill="#1E293B"/>
  <rect x="660" y="574" width="340" height="18" rx="9" fill="#1E293B"/>
  <rect x="382" y="574" width="238" height="18" rx="9" fill="url(#leftBar)"/>
  <rect x="660" y="574" width="289" height="18" rx="9" fill="url(#rightBar)" filter="url(#barGlow)"/>
  <rect x="590" y="565" width="100" height="36" rx="18" fill="#0F172A" stroke="#334155" stroke-width="1"/>
  <text x="640" y="588" width="100" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#E2E8F0">Time to value</text>
  <text x="368" y="589" width="50" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#BAE6FD">70</text>
  <text x="963" y="589" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#BBF7D0">85</text>

  <text x="150" y="682" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#64748B">Scale: 0–100 normalized score per criterion</text>
  <text x="1130" y="682" width="420" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#64748B">Editable SVG bars: adjust widths to match real data</text>
</svg>
```

## Avoid in this skill
- ❌ Mirroring every bar to the same length; the power of the layout comes from visibly different left/right magnitudes.
- ❌ Putting long metric labels outside the center column; this breaks scanability and makes the bars feel disconnected.
- ❌ Using arrow markers on paths for direction cues; if arrows are needed, use simple `<line>` elements with explicit styling instead.
- ❌ Applying filters to `<line>` grid marks; shadows or glows on lines may be dropped by the translator.
- ❌ Relying on tiny labels only; include numeric scores near the bar ends for executive readability.

## Composition notes
- Keep the center axis around `x=640`; reserve roughly 90–120 px for metric pills so labels do not collide with bars.
- Use cool opposing palettes, such as blue/cyan versus green/emerald, to signal two competitors without implying warning/error.
- Put product names in strong header cards above their respective halves; keep descriptions short and secondary.
- Let the longest bars nearly reach the outer track edges, but leave 60–100 px of breathing room from the card boundary.