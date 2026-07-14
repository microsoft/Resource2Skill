# SVG Recipe — Neon Cyberpunk Holographic Callout

## Visual mechanism
A dark HUD-style canvas uses faint constellation geometry and a glowing cyan wireframe subject to create spatial context, then a hot magenta scan reticle isolates one region and routes attention to a floating data label. The effect depends on layered duplicate strokes: blurred neon glows underneath crisp editable geometry.

## SVG primitives needed
- 1× `<rect>` for the full-slide deep navy / vignette background
- 20–35× `<line>` for faint constellation network links and segmented connector lines
- 20–35× `<circle>` for constellation nodes, anatomical joints, endpoint dots, and scan pips
- 2× `<ellipse>` for holographic head glow and crisp head outline
- 8–12× `<path>` for wireframe anatomy, torso mesh, reticle hexagon, arrow chevron, micro UI accents, and decorative scan arcs
- 2–4× `<rect>` for right-side translucent callout cards and tiny metric bars
- 5–8× `<text>` elements with explicit `width` attributes for editable labels, price, title, and HUD metadata
- 2× `<linearGradient>` for neon strokes and translucent panel fills
- 1× `<radialGradient>` for the dark cyberpunk background vignette
- 2× `<filter>` using `feGaussianBlur` for cyan and magenta neon glow on paths/circles/ellipses
- 1× `<filter>` using `feOffset + feGaussianBlur + feMerge` for soft panel shadow on rectangles

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgVignette" cx="42%" cy="45%" r="78%">
      <stop offset="0%" stop-color="#102238"/>
      <stop offset="55%" stop-color="#0A0E19"/>
      <stop offset="100%" stop-color="#050711"/>
    </radialGradient>

    <linearGradient id="cyanStroke" x1="260" y1="90" x2="560" y2="640" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#C8FBFF"/>
      <stop offset="45%" stop-color="#00BFFF"/>
      <stop offset="100%" stop-color="#316BFF"/>
    </linearGradient>

    <linearGradient id="panelFill" x1="770" y1="190" x2="1175" y2="500" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#0B2438" stop-opacity="0.88"/>
      <stop offset="100%" stop-color="#080B18" stop-opacity="0.55"/>
    </linearGradient>

    <filter id="cyanGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="7" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="magentaGlow" x="-90%" y="-90%" width="280%" height="280%">
      <feGaussianBlur stdDeviation="6" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="panelShadow" x="-40%" y="-40%" width="180%" height="180%">
      <feOffset dx="0" dy="12" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- deep cyberpunk field -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#bgVignette)"/>

  <!-- faint constellation network -->
  <line x1="70" y1="88" x2="158" y2="124" stroke="#00BFFF" stroke-opacity="0.16" stroke-width="1"/>
  <line x1="158" y1="124" x2="245" y2="86" stroke="#00BFFF" stroke-opacity="0.13" stroke-width="1"/>
  <line x1="245" y1="86" x2="335" y2="142" stroke="#00BFFF" stroke-opacity="0.12" stroke-width="1"/>
  <line x1="82" y1="326" x2="188" y2="274" stroke="#00BFFF" stroke-opacity="0.12" stroke-width="1"/>
  <line x1="188" y1="274" x2="296" y2="332" stroke="#00BFFF" stroke-opacity="0.16" stroke-width="1"/>
  <line x1="296" y1="332" x2="398" y2="286" stroke="#00BFFF" stroke-opacity="0.10" stroke-width="1"/>
  <line x1="538" y1="72" x2="650" y2="126" stroke="#00BFFF" stroke-opacity="0.11" stroke-width="1"/>
  <line x1="650" y1="126" x2="734" y2="86" stroke="#00BFFF" stroke-opacity="0.13" stroke-width="1"/>
  <line x1="1044" y1="96" x2="1156" y2="142" stroke="#00BFFF" stroke-opacity="0.11" stroke-width="1"/>
  <line x1="962" y1="596" x2="1080" y2="552" stroke="#00BFFF" stroke-opacity="0.10" stroke-width="1"/>
  <line x1="1080" y1="552" x2="1194" y2="610" stroke="#00BFFF" stroke-opacity="0.13" stroke-width="1"/>

  <circle cx="70" cy="88" r="2.2" fill="#00BFFF" fill-opacity="0.45"/>
  <circle cx="158" cy="124" r="2.5" fill="#00BFFF" fill-opacity="0.5"/>
  <circle cx="245" cy="86" r="1.8" fill="#00BFFF" fill-opacity="0.38"/>
  <circle cx="335" cy="142" r="2.2" fill="#00BFFF" fill-opacity="0.42"/>
  <circle cx="82" cy="326" r="2" fill="#00BFFF" fill-opacity="0.34"/>
  <circle cx="188" cy="274" r="2.4" fill="#00BFFF" fill-opacity="0.42"/>
  <circle cx="296" cy="332" r="2.1" fill="#00BFFF" fill-opacity="0.40"/>
  <circle cx="398" cy="286" r="1.8" fill="#00BFFF" fill-opacity="0.32"/>
  <circle cx="538" cy="72" r="2" fill="#00BFFF" fill-opacity="0.34"/>
  <circle cx="650" cy="126" r="2.5" fill="#00BFFF" fill-opacity="0.45"/>
  <circle cx="734" cy="86" r="2" fill="#00BFFF" fill-opacity="0.34"/>
  <circle cx="1044" cy="96" r="2.2" fill="#00BFFF" fill-opacity="0.35"/>
  <circle cx="1156" cy="142" r="2.4" fill="#00BFFF" fill-opacity="0.38"/>
  <circle cx="962" cy="596" r="2" fill="#00BFFF" fill-opacity="0.28"/>
  <circle cx="1080" cy="552" r="2.4" fill="#00BFFF" fill-opacity="0.36"/>
  <circle cx="1194" cy="610" r="2" fill="#00BFFF" fill-opacity="0.32"/>

  <!-- wireframe subject: glow layer -->
  <ellipse cx="405" cy="122" rx="44" ry="52" fill="none" stroke="#00BFFF" stroke-opacity="0.62" stroke-width="10" filter="url(#cyanGlow)"/>
  <path d="M405 174 L405 218 L405 292 L405 405
           M345 205 L465 205
           M345 205 L405 405 L465 205
           M365 397 L445 397
           M345 205 L320 320 L330 445
           M465 205 L500 320 L488 445
           M365 397 L350 540 L342 662
           M445 397 L462 540 L472 662"
        fill="none" stroke="#00BFFF" stroke-opacity="0.60" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" filter="url(#cyanGlow)"/>
  <path d="M360 250 C390 230 422 230 455 250
           M354 286 C390 268 425 268 460 286
           M372 350 C392 362 420 362 440 350"
        fill="none" stroke="#00BFFF" stroke-opacity="0.42" stroke-width="7" stroke-linecap="round" filter="url(#cyanGlow)"/>

  <!-- wireframe subject: crisp layer -->
  <ellipse cx="405" cy="122" rx="44" ry="52" fill="none" stroke="url(#cyanStroke)" stroke-width="2.2"/>
  <path d="M405 174 L405 218 L405 292 L405 405
           M345 205 L465 205
           M345 205 L405 405 L465 205
           M365 397 L445 397
           M345 205 L320 320 L330 445
           M465 205 L500 320 L488 445
           M365 397 L350 540 L342 662
           M445 397 L462 540 L472 662"
        fill="none" stroke="url(#cyanStroke)" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M360 250 C390 230 422 230 455 250
           M354 286 C390 268 425 268 460 286
           M372 350 C392 362 420 362 440 350"
        fill="none" stroke="#9EF6FF" stroke-opacity="0.82" stroke-width="1.4" stroke-linecap="round"/>

  <!-- glowing anatomical joints -->
  <circle cx="405" cy="174" r="4" fill="#C8FBFF" filter="url(#cyanGlow)"/>
  <circle cx="345" cy="205" r="4" fill="#C8FBFF" filter="url(#cyanGlow)"/>
  <circle cx="465" cy="205" r="4" fill="#C8FBFF" filter="url(#cyanGlow)"/>
  <circle cx="405" cy="292" r="4" fill="#C8FBFF" filter="url(#cyanGlow)"/>
  <circle cx="330" cy="445" r="3.5" fill="#C8FBFF" filter="url(#cyanGlow)"/>
  <circle cx="488" cy="445" r="3.5" fill="#C8FBFF" filter="url(#cyanGlow)"/>
  <circle cx="350" cy="540" r="3.5" fill="#C8FBFF" filter="url(#cyanGlow)"/>
  <circle cx="462" cy="540" r="3.5" fill="#C8FBFF" filter="url(#cyanGlow)"/>

  <!-- active scan reticle on head -->
  <path d="M405 48 L462 82 L462 148 L405 184 L348 148 L348 82 Z"
        fill="none" stroke="#FF2864" stroke-width="4" stroke-linejoin="round" filter="url(#magentaGlow)"/>
  <path d="M405 68 L444 91 L444 139 L405 164 L366 139 L366 91 Z"
        fill="none" stroke="#FF6B9B" stroke-width="1.6" stroke-dasharray="8 7"/>
  <circle cx="405" cy="122" r="14" fill="none" stroke="#FF2864" stroke-width="2.6" filter="url(#magentaGlow)"/>
  <line x1="352" y1="122" x2="374" y2="122" stroke="#FF2864" stroke-width="2"/>
  <line x1="436" y1="122" x2="458" y2="122" stroke="#FF2864" stroke-width="2"/>
  <line x1="405" y1="70" x2="405" y2="94" stroke="#FF2864" stroke-width="2"/>
  <line x1="405" y1="150" x2="405" y2="174" stroke="#FF2864" stroke-width="2"/>

  <!-- segmented neon connector -->
  <circle cx="462" cy="122" r="5" fill="#FF2864" filter="url(#magentaGlow)"/>
  <line x1="462" y1="122" x2="590" y2="122" stroke="#FF2864" stroke-width="2.5"/>
  <line x1="590" y1="122" x2="666" y2="205" stroke="#FF2864" stroke-width="2.5"/>
  <line x1="666" y1="205" x2="780" y2="205" stroke="#FF2864" stroke-width="2.5"/>
  <path d="M780 205 L765 197 L765 213 Z" fill="#FF2864" filter="url(#magentaGlow)"/>
  <circle cx="590" cy="122" r="3" fill="#FF6B9B"/>
  <circle cx="666" cy="205" r="3" fill="#FF6B9B"/>

  <!-- floating data label -->
  <rect x="790" y="164" width="360" height="236" rx="24" fill="url(#panelFill)" stroke="#00BFFF" stroke-opacity="0.55" stroke-width="1.4" filter="url(#panelShadow)"/>
  <rect x="814" y="188" width="92" height="24" rx="12" fill="#FF2864" fill-opacity="0.20" stroke="#FF2864" stroke-opacity="0.9"/>
  <text x="832" y="205" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FF8AAD" letter-spacing="2">ACTIVE SCAN</text>

  <text x="814" y="258" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="40" font-weight="700" fill="#FFFFFF">Cataracts</text>
  <text x="814" y="306" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#9EF6FF">Estimated treatment cost</text>
  <text x="814" y="362" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="48" font-weight="800" fill="#00BFFF" filter="url(#cyanGlow)">£2,300</text>

  <line x1="814" y1="384" x2="1118" y2="384" stroke="#00BFFF" stroke-opacity="0.28" stroke-width="1"/>
  <rect x="814" y="414" width="220" height="6" rx="3" fill="#00BFFF" fill-opacity="0.18"/>
  <rect x="814" y="414" width="146" height="6" rx="3" fill="#FF2864"/>
  <text x="814" y="446" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#B7D7E8" letter-spacing="0.6">REGION: OCULAR · PRIORITY: HIGH</text>

  <!-- title / HUD footer -->
  <text x="72" y="642" width="480" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#00BFFF" fill-opacity="0.75" letter-spacing="3">HOLOGRAPHIC MEDICAL COST MAP</text>
  <text x="72" y="674" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="700" fill="#FFFFFF">Spatial callout for diagnostic pricing</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG animation for pulsing scans; build the final static frame and animate in PowerPoint if needed.
- ❌ Do not apply `filter` to `<line>` elements; duplicate important connector segments with bright strokes instead, or use glowing endpoint circles/paths.
- ❌ Do not use `marker-end` on `<path>` connectors; use `<line>` segments and draw the arrowhead as a small editable `<path>`.
- ❌ Do not use `<mask>` or clip non-image geometry to create the HUD glow; use duplicate blurred shapes with `feGaussianBlur`.
- ❌ Do not make the background too busy behind the label area; constellation lines should stay faint and decorative.

## Composition notes
- Keep the holographic subject on the left/center 55–60% of the slide; the right 35–40% should remain clean enough for the floating data card.
- Use cyan as the ambient system color and magenta/red only for the active region, connector, and priority label so the eye has a single dominant path.
- Layer order matters: dark field → faint network → blurred hologram → crisp wireframe → magenta reticle → connector → text panel.
- Use generous negative space around the callout card; the premium HUD look comes from contrast and restraint, not from filling every area with UI elements.