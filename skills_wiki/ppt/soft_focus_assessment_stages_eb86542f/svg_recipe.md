# SVG Recipe — Soft Focus Assessment Stages

## Visual mechanism
A lavender gradient background is softened with oversized blurred “bokeh” light circles, creating atmospheric depth behind crisp floating white stage cards. Each card uses a rounded rectangle, subtle shadow, circular icon badge, stage number, and concise bullet text to make a process feel calm, premium, and easy to scan.

## SVG primitives needed
- 1× full-slide `<rect>` for the lavender gradient background
- 10× blurred `<circle>` / `<ellipse>` for soft-focus bokeh lights
- 4× white rounded `<rect>` cards with a shadow filter
- 4× accent `<circle>` icon badges floating above the cards
- 8× decorative `<path>` icon strokes/fills for simple editable line icons
- 3× `<line>` connector segments between stage badges
- 1× `<text>` slide title
- 4× `<text>` stage numbers
- 4× `<text>` stage titles
- 4× multiline `<text>` blocks with `<tspan>` bullet lines
- 1× `<linearGradient>` for the background
- 1× `<radialGradient>` for badge fills
- 1× `<filter id="bokehBlur">` for blurred background circles
- 1× `<filter id="cardShadow">` for floating panel shadows

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="lavenderBg" x1="0" y1="0" x2="0" y2="720">
      <stop offset="0%" stop-color="#eee8ff"/>
      <stop offset="52%" stop-color="#ddd5fa"/>
      <stop offset="100%" stop-color="#c8c0eb"/>
    </linearGradient>

    <radialGradient id="badgeGlow" cx="35%" cy="25%" r="75%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="45%" stop-color="#eee9ff"/>
      <stop offset="100%" stop-color="#a28be7"/>
    </radialGradient>

    <filter id="bokehBlur" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="22"/>
    </filter>

    <filter id="cardShadow" x="-25%" y="-25%" width="150%" height="160%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#lavenderBg)"/>

  <circle cx="80" cy="86" r="92" fill="#ffffff" opacity="0.34" filter="url(#bokehBlur)"/>
  <circle cx="260" cy="150" r="70" fill="#c8d2ff" opacity="0.46" filter="url(#bokehBlur)"/>
  <circle cx="1125" cy="110" r="115" fill="#f4ecff" opacity="0.50" filter="url(#bokehBlur)"/>
  <ellipse cx="1040" cy="530" rx="165" ry="110" fill="#cbd6ff" opacity="0.28" filter="url(#bokehBlur)"/>
  <circle cx="610" cy="90" r="52" fill="#ffffff" opacity="0.30" filter="url(#bokehBlur)"/>
  <circle cx="740" cy="610" r="100" fill="#f0dcff" opacity="0.34" filter="url(#bokehBlur)"/>
  <circle cx="160" cy="590" r="130" fill="#ffffff" opacity="0.20" filter="url(#bokehBlur)"/>
  <ellipse cx="475" cy="455" rx="135" ry="82" fill="#d8ddff" opacity="0.23" filter="url(#bokehBlur)"/>
  <circle cx="1230" cy="360" r="70" fill="#ffffff" opacity="0.30" filter="url(#bokehBlur)"/>
  <circle cx="900" cy="205" r="44" fill="#f7f1ff" opacity="0.46" filter="url(#bokehBlur)"/>

  <text x="640" y="82" width="900" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="36" font-weight="700" fill="#594f77">
    Four stages of business assessment process
  </text>
  <text x="640" y="122" width="760" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#80739d">
    A calm structured journey from discovery to client-ready agreement
  </text>

  <line x1="214" y1="214" x2="463" y2="214" stroke="#ffffff" stroke-width="5" opacity="0.55" stroke-linecap="round"/>
  <line x1="499" y1="214" x2="748" y2="214" stroke="#ffffff" stroke-width="5" opacity="0.55" stroke-linecap="round"/>
  <line x1="784" y1="214" x2="1033" y2="214" stroke="#ffffff" stroke-width="5" opacity="0.55" stroke-linecap="round"/>

  <rect x="72" y="250" width="245" height="345" rx="28" fill="#ffffff" opacity="0.97" filter="url(#cardShadow)"/>
  <rect x="357" y="250" width="245" height="345" rx="28" fill="#ffffff" opacity="0.97" filter="url(#cardShadow)"/>
  <rect x="642" y="250" width="245" height="345" rx="28" fill="#ffffff" opacity="0.97" filter="url(#cardShadow)"/>
  <rect x="927" y="250" width="245" height="345" rx="28" fill="#ffffff" opacity="0.97" filter="url(#cardShadow)"/>

  <circle cx="194" cy="214" r="47" fill="url(#badgeGlow)"/>
  <circle cx="479" cy="214" r="47" fill="url(#badgeGlow)"/>
  <circle cx="764" cy="214" r="47" fill="url(#badgeGlow)"/>
  <circle cx="1049" cy="214" r="47" fill="url(#badgeGlow)"/>

  <path d="M172 214 h44 M172 198 h44 M172 230 h31" fill="none" stroke="#6d5caf" stroke-width="6" stroke-linecap="round"/>
  <path d="M455 214 c0-13 11-24 24-24 s24 11 24 24 -11 24-24 24 -24-11-24-24z M479 182 v13 M479 233 v13 M447 214 h13 M498 214 h13"
        fill="none" stroke="#6d5caf" stroke-width="5" stroke-linecap="round"/>
  <path d="M742 197 l22-12 22 12 v34 l-22 12 -22-12z" fill="none" stroke="#6d5caf" stroke-width="5" stroke-linejoin="round"/>
  <path d="M742 197 l22 13 22-13 M764 210 v33" fill="none" stroke="#6d5caf" stroke-width="4" stroke-linecap="round"/>
  <path d="M1030 187 h29 l18 18 v36 h-47z" fill="none" stroke="#6d5caf" stroke-width="5" stroke-linejoin="round"/>
  <path d="M1059 187 v19 h18 M1040 220 h27 M1040 233 h22" fill="none" stroke="#6d5caf" stroke-width="4" stroke-linecap="round"/>

  <text x="194" y="313" width="120" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#9682dc">STAGE 01</text>
  <text x="194" y="356" width="190" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#594f77">Designing</text>
  <text x="104" y="404" width="180"
        font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#786e96">
    <tspan x="104" dy="0">• Pinpoint expectations</tspan>
    <tspan x="104" dy="30">• Collect requirements</tspan>
    <tspan x="104" dy="30">• Map strategic interface</tspan>
    <tspan x="104" dy="30">• Align on assessment lens</tspan>
  </text>

  <text x="479" y="313" width="120" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#9682dc">STAGE 02</text>
  <text x="479" y="356" width="190" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#594f77">Finalizing Scope</text>
  <text x="389" y="404" width="180"
        font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#786e96">
    <tspan x="389" dy="0">• Define process areas</tspan>
    <tspan x="389" dy="30">• Target improvements</tspan>
    <tspan x="389" dy="30">• Confirm key stakeholders</tspan>
    <tspan x="389" dy="30">• Lock success criteria</tspan>
  </text>

  <text x="764" y="313" width="120" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#9682dc">STAGE 03</text>
  <text x="764" y="356" width="190" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#594f77">Building Use Case</text>
  <text x="674" y="404" width="180"
        font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#786e96">
    <tspan x="674" dy="0">• Analyze assessment data</tspan>
    <tspan x="674" dy="30">• Draft opportunity case</tspan>
    <tspan x="674" dy="30">• Evaluate POC options</tspan>
    <tspan x="674" dy="30">• Shape executive story</tspan>
  </text>

  <text x="1049" y="313" width="120" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#9682dc">STAGE 04</text>
  <text x="1049" y="348" width="195" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" fill="#594f77">
    <tspan x="1049" dy="0">Finalizing Client</tspan>
    <tspan x="1049" dy="27">Agreement</tspan>
  </text>
  <text x="959" y="404" width="180"
        font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#786e96">
    <tspan x="959" dy="0">• Review recommendations</tspan>
    <tspan x="959" dy="30">• Confirm commercial terms</tspan>
    <tspan x="959" dy="30">• Prepare agreement pack</tspan>
    <tspan x="959" dy="30">• Launch next-phase plan</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using a flat solid background only; the technique depends on layered blur and depth.
- ❌ Applying `filter` to connector `<line>` elements; shadows and blur should be on circles, ellipses, paths, rects, or text.
- ❌ Using `<mask>` to create bokeh fades; use blurred translucent circles/ellipses instead.
- ❌ Putting all stage content inside one large text box; keep each card’s title, number, and bullets separately editable.
- ❌ Over-saturating the cards with purple fills; foreground panels should remain clean white for contrast.

## Composition notes
- Keep the title in the upper 15–20% of the slide, with the stage row centered horizontally below it.
- Let the bokeh circles drift behind content asymmetrically; the cards provide the visual order while the background provides softness.
- Use white cards with generous internal padding so the purple text feels airy and premium.
- Maintain a restrained lavender palette: dark purple for hierarchy, muted purple for body text, and pale violet accents for badges and numbers.