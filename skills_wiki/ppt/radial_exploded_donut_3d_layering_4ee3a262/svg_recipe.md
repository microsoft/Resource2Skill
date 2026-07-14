# SVG Recipe — Radial Exploded Donut & 3D Layering

## Visual mechanism
An exploded donut is split into separate radial arc segments, each nudged outward from the center and lifted with shadows. A darker inner lip overlay and central hub create the illusion of a layered 3D control dial, while numbered nodes and side text turn the dial into a premium process-flow infographic.

## SVG primitives needed
- 1× `<rect>` for the dark slate slide background
- 6× main `<path>` donut segments using arc commands for the exploded ring slices
- 6× inner-lip `<path>` overlays for the transparent dark 3D depth band
- 6× `<circle>` outer node pins, 6× `<circle>` inner node fills, and 6× `<text>` numbers for step markers
- 6× `<line>` connectors from nodes to side text blocks
- 12× `<text>` elements for step titles and descriptions
- 3× central `<circle>` elements for the hub, highlight, and inner recess
- 1× decorative `<path>` gear-like icon inside the hub
- Multiple `<linearGradient>` fills for premium segment color depth
- 1× `<radialGradient>` for the background vignette
- 1× `<filter id="softShadow">` applied directly to donut paths and node circles
- 1× `<filter id="hubShadow">` applied directly to central hub circles

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgGrad" cx="50%" cy="44%" r="70%">
      <stop offset="0%" stop-color="#40515C"/>
      <stop offset="70%" stop-color="#34424B"/>
      <stop offset="100%" stop-color="#26323A"/>
    </radialGradient>

    <linearGradient id="segOrange" x1="430" y1="500" x2="610" y2="320">
      <stop offset="0%" stop-color="#D94E2F"/>
      <stop offset="100%" stop-color="#F78A45"/>
    </linearGradient>
    <linearGradient id="segAmber" x1="430" y1="360" x2="610" y2="180">
      <stop offset="0%" stop-color="#DD8732"/>
      <stop offset="100%" stop-color="#F5B94A"/>
    </linearGradient>
    <linearGradient id="segYellow" x1="520" y1="150" x2="650" y2="330">
      <stop offset="0%" stop-color="#FFE06A"/>
      <stop offset="100%" stop-color="#EFB735"/>
    </linearGradient>
    <linearGradient id="segLime" x1="650" y1="150" x2="790" y2="330">
      <stop offset="0%" stop-color="#BBD860"/>
      <stop offset="100%" stop-color="#779F3B"/>
    </linearGradient>
    <linearGradient id="segGreen" x1="700" y1="200" x2="860" y2="360">
      <stop offset="0%" stop-color="#39A874"/>
      <stop offset="100%" stop-color="#1F7654"/>
    </linearGradient>
    <linearGradient id="segTeal" x1="700" y1="350" x2="850" y2="520">
      <stop offset="0%" stop-color="#25A2A8"/>
      <stop offset="100%" stop-color="#156E82"/>
    </linearGradient>

    <linearGradient id="hubGrad" x1="570" y1="280" x2="705" y2="450">
      <stop offset="0%" stop-color="#F7FAFC"/>
      <stop offset="58%" stop-color="#D8E0E5"/>
      <stop offset="100%" stop-color="#AEBBC3"/>
    </linearGradient>

    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="7" dy="9"/>
      <feGaussianBlur stdDeviation="8"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .36 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="hubShadow" x="-35%" y="-35%" width="170%" height="170%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .45 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <text x="640" y="62" width="520" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#F4F7F8" letter-spacing="2">RADIAL OPERATING LOOP</text>
  <text x="640" y="94" width="560" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#AFC0C8">six interlocking stages with exploded 3D depth</text>

  <!-- Exploded donut segments -->
  <path d="M492.8 499.8 A190 190 0 0 1 437.1 365.4 L545.1 365.4 A82 82 0 0 0 569.1 423.4 Z" fill="url(#segOrange)" stroke="#FFFFFF" stroke-opacity=".18" stroke-width="2" filter="url(#softShadow)"/>
  <path d="M437.1 354.6 A190 190 0 0 1 492.8 220.2 L569.1 296.6 A82 82 0 0 0 545.1 354.6 Z" fill="url(#segAmber)" stroke="#FFFFFF" stroke-opacity=".18" stroke-width="2" filter="url(#softShadow)"/>
  <path d="M500.2 212.8 A190 190 0 0 1 634.6 157.1 L634.6 265.1 A82 82 0 0 0 576.6 289.1 Z" fill="url(#segYellow)" stroke="#FFFFFF" stroke-opacity=".18" stroke-width="2" filter="url(#softShadow)"/>
  <path d="M645.4 157.1 A190 190 0 0 1 779.8 212.8 L703.4 289.1 A82 82 0 0 0 645.4 265.1 Z" fill="url(#segLime)" stroke="#FFFFFF" stroke-opacity=".18" stroke-width="2" filter="url(#softShadow)"/>
  <path d="M787.2 220.2 A190 190 0 0 1 842.9 354.6 L734.9 354.6 A82 82 0 0 0 710.9 296.6 Z" fill="url(#segGreen)" stroke="#FFFFFF" stroke-opacity=".18" stroke-width="2" filter="url(#softShadow)"/>
  <path d="M842.9 365.4 A190 190 0 0 1 787.2 499.8 L710.9 423.4 A82 82 0 0 0 734.9 365.4 Z" fill="url(#segTeal)" stroke="#FFFFFF" stroke-opacity=".18" stroke-width="2" filter="url(#softShadow)"/>

  <!-- Inner transparent depth lip -->
  <path d="M545.1 447.4 A116 116 0 0 1 511.1 365.4 L545.1 365.4 A82 82 0 0 0 569.1 423.4 Z" fill="#000000" opacity=".30"/>
  <path d="M511.1 354.6 A116 116 0 0 1 545.1 272.6 L569.1 296.6 A82 82 0 0 0 545.1 354.6 Z" fill="#000000" opacity=".30"/>
  <path d="M552.6 265.1 A116 116 0 0 1 634.6 231.1 L634.6 265.1 A82 82 0 0 0 576.6 289.1 Z" fill="#000000" opacity=".30"/>
  <path d="M645.4 231.1 A116 116 0 0 1 727.4 265.1 L703.4 289.1 A82 82 0 0 0 645.4 265.1 Z" fill="#000000" opacity=".30"/>
  <path d="M734.9 272.6 A116 116 0 0 1 768.9 354.6 L734.9 354.6 A82 82 0 0 0 710.9 296.6 Z" fill="#000000" opacity=".30"/>
  <path d="M768.9 365.4 A116 116 0 0 1 734.9 447.4 L710.9 423.4 A82 82 0 0 0 734.9 365.4 Z" fill="#000000" opacity=".30"/>

  <!-- Central hub -->
  <circle cx="640" cy="360" r="86" fill="#1F2B32" opacity=".35" filter="url(#hubShadow)"/>
  <circle cx="640" cy="360" r="74" fill="url(#hubGrad)" filter="url(#hubShadow)"/>
  <circle cx="640" cy="360" r="48" fill="#34424B"/>
  <path d="M640 296 L653 302 L656 317 L671 320 L680 332 L674 346 L684 360 L674 374 L680 388 L671 400 L656 403 L653 418 L640 424 L627 418 L624 403 L609 400 L600 388 L606 374 L596 360 L606 346 L600 332 L609 320 L624 317 L627 302 Z" fill="#FFFFFF" opacity=".92"/>
  <circle cx="640" cy="360" r="23" fill="#34424B"/>
  <text x="640" y="356" width="110" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">SIX</text>
  <text x="640" y="376" width="110" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">STEPS</text>

  <!-- Connectors -->
  <line x1="404" y1="458" x2="238" y2="534" stroke="#91A2AA" stroke-width="2" stroke-opacity=".5"/>
  <line x1="404" y1="262" x2="238" y2="216" stroke="#91A2AA" stroke-width="2" stroke-opacity=".5"/>
  <line x1="542" y1="124" x2="315" y2="128" stroke="#91A2AA" stroke-width="2" stroke-opacity=".5"/>
  <line x1="738" y1="124" x2="965" y2="128" stroke="#91A2AA" stroke-width="2" stroke-opacity=".5"/>
  <line x1="876" y1="262" x2="1042" y2="216" stroke="#91A2AA" stroke-width="2" stroke-opacity=".5"/>
  <line x1="876" y1="458" x2="1042" y2="534" stroke="#91A2AA" stroke-width="2" stroke-opacity=".5"/>

  <!-- Number nodes -->
  <circle cx="404" cy="458" r="27" fill="#F26B38" filter="url(#softShadow)"/>
  <circle cx="404" cy="458" r="18" fill="#34424B"/>
  <text x="404" y="466" width="40" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#FFFFFF">1</text>

  <circle cx="404" cy="262" r="27" fill="#F2A638" filter="url(#softShadow)"/>
  <circle cx="404" cy="262" r="18" fill="#34424B"/>
  <text x="404" y="270" width="40" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#FFFFFF">2</text>

  <circle cx="542" cy="124" r="27" fill="#F2CB38" filter="url(#softShadow)"/>
  <circle cx="542" cy="124" r="18" fill="#34424B"/>
  <text x="542" y="132" width="40" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#FFFFFF">3</text>

  <circle cx="738" cy="124" r="27" fill="#9BBF40" filter="url(#softShadow)"/>
  <circle cx="738" cy="124" r="18" fill="#34424B"/>
  <text x="738" y="132" width="40" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#FFFFFF">4</text>

  <circle cx="876" cy="262" r="27" fill="#268C60" filter="url(#softShadow)"/>
  <circle cx="876" cy="262" r="18" fill="#34424B"/>
  <text x="876" y="270" width="40" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#FFFFFF">5</text>

  <circle cx="876" cy="458" r="27" fill="#197E8C" filter="url(#softShadow)"/>
  <circle cx="876" cy="458" r="18" fill="#34424B"/>
  <text x="876" y="466" width="40" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#FFFFFF">6</text>

  <!-- Side labels -->
  <text x="86" y="522" width="190" text-anchor="start" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF">DISCOVER</text>
  <text x="86" y="547" width="245" text-anchor="start" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#B9C7CD">Map current signals, identify friction, and frame the opportunity.</text>

  <text x="86" y="203" width="190" text-anchor="start" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF">DEFINE</text>
  <text x="86" y="228" width="245" text-anchor="start" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#B9C7CD">Translate insights into clear principles, owners, and measurable targets.</text>

  <text x="86" y="117" width="235" text-anchor="start" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF">DESIGN</text>
  <text x="86" y="142" width="260" text-anchor="start" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#B9C7CD">Prototype the workflow and pressure-test the highest-risk assumptions.</text>

  <text x="965" y="117" width="235" text-anchor="start" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF">BUILD</text>
  <text x="965" y="142" width="260" text-anchor="start" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#B9C7CD">Assemble the operating model, assets, governance, and launch cadence.</text>

  <text x="965" y="203" width="190" text-anchor="start" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF">DEPLOY</text>
  <text x="965" y="228" width="245" text-anchor="start" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#B9C7CD">Roll out the system with adoption support and executive visibility.</text>

  <text x="965" y="522" width="190" text-anchor="start" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF">OPTIMIZE</text>
  <text x="965" y="547" width="245" text-anchor="start" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#B9C7CD">Feed performance data back into the loop for continuous improvement.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use a bitmap screenshot of the donut; the point is to keep each arc, node, and label editable in PowerPoint.
- ❌ Do not apply `clip-path` to the donut segments; use native `<path>` arc geometry instead.
- ❌ Do not use `<mask>` for the inner cutout or lip shading; masks can break translation, while compound-looking arc paths remain editable.
- ❌ Do not put `filter` on connector `<line>` elements; if connectors need depth, use subtle color/opacity instead.
- ❌ Do not rely on PowerPoint chart objects for this look; native charts will not reproduce exploded spacing, custom lips, or per-slice shadowing reliably.

## Composition notes
- Keep the exploded donut centered and occupying roughly 45–55% of slide height; the side labels need generous breathing room.
- Use a dark slate background so saturated segment colors feel luminous and executive-grade.
- Put steps 1–3 on the left and 4–6 on the right for mirrored visual balance.
- The 3D effect comes from three layers: soft shadow below, bright gradient segment fill, and semi-transparent black inner lip above.