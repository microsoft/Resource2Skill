# SVG Recipe — Morphing Toggle Switch

## Visual mechanism
A two-state comparison slide where a large toggle handle visually “selects” one content panel while the opposite panel is dimmed. In PowerPoint, duplicate the slide and change the same shapes’ colors/positions for the second state, then apply Morph so the handle glides and the active highlight transfers smoothly.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark background
- 2× decorative `<path>` shapes for soft ambient light sweeps behind the content
- 2× large rounded `<rect>` panels for the compared states
- 2× subtle stroke `<rect>` overlays for panel rim highlights
- 1× rounded `<rect>` for the toggle track
- 1× rounded `<rect>` for the active toggle capsule / handle zone
- 2× `<circle>` elements for the glowing handle core and halo
- 10× small `<circle>` elements for bullet/icon backplates and toggle indicator dots
- 8× `<path>` elements for checkmarks, warning marks, and tiny UI glyphs
- Multiple `<text>` elements with explicit `width` attributes for title, labels, headers, and body copy
- 3× `<linearGradient>` definitions for background, active green panel, and inactive surfaces
- 1× `<linearGradient id="redActive">` prepared for the second Morph state
- 2× `<filter>` definitions: one soft drop shadow and one colored glow applied to shapes

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#202124"/>
      <stop offset="55%" stop-color="#2D2D2D"/>
      <stop offset="100%" stop-color="#18191B"/>
    </linearGradient>

    <linearGradient id="prosActive" x1="105" y1="150" x2="605" y2="480">
      <stop offset="0%" stop-color="#24FF86"/>
      <stop offset="60%" stop-color="#00D65A"/>
      <stop offset="100%" stop-color="#00A344"/>
    </linearGradient>

    <linearGradient id="redActive" x1="675" y1="150" x2="1175" y2="480">
      <stop offset="0%" stop-color="#FF6A78"/>
      <stop offset="58%" stop-color="#FF4556"/>
      <stop offset="100%" stop-color="#C91F32"/>
    </linearGradient>

    <linearGradient id="inactivePanel" x1="675" y1="150" x2="1175" y2="480">
      <stop offset="0%" stop-color="#55575A"/>
      <stop offset="100%" stop-color="#343638"/>
    </linearGradient>

    <linearGradient id="trackGrad" x1="260" y1="555" x2="1020" y2="643">
      <stop offset="0%" stop-color="#303235"/>
      <stop offset="50%" stop-color="#45474A"/>
      <stop offset="100%" stop-color="#303235"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="16"/>
      <feGaussianBlur stdDeviation="18"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .35 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="greenGlow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="18" result="blur"/>
      <feColorMatrix in="blur" type="matrix" values="0 0 0 0 0  0 0 0 0 1  0 0 0 0 .38  0 0 0 .85 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <path d="M-80,118 C120,34 256,82 420,38 C560,0 665,22 790,82 C560,112 350,158 160,220 C58,253 -22,260 -80,240 Z"
        fill="#00FF55" opacity="0.07"/>
  <path d="M1290,650 C1116,690 988,664 852,700 C710,738 548,730 392,675 C548,622 724,596 914,604 C1086,612 1205,574 1290,520 Z"
        fill="#FF4556" opacity="0.06"/>

  <text x="80" y="72" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="700" fill="#F4F6F8">
    Interactive comparison mode
  </text>
  <text x="80" y="104" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#A9B0B8">
    Duplicate this slide, swap the active state, then use Morph to create the toggle movement.
  </text>

  <rect x="105" y="150" width="500" height="330" rx="38" fill="url(#prosActive)" filter="url(#softShadow)"/>
  <rect x="118" y="163" width="474" height="304" rx="30" fill="none" stroke="#B8FFD2" stroke-opacity="0.45" stroke-width="2"/>

  <text x="145" y="224" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="54" font-weight="800" letter-spacing="4" fill="#FFFFFF">
    PROS
  </text>
  <text x="148" y="264" width="390" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#EFFFF5">
    Active state is bright, high-contrast, and visually closer to the audience.
  </text>

  <circle cx="164" cy="318" r="14" fill="#FFFFFF" opacity="0.25"/>
  <path d="M157,317 L163,323 L173,309" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="190" y="325" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="600" fill="#FFFFFF">
    Faster adoption curve
  </text>

  <circle cx="164" cy="374" r="14" fill="#FFFFFF" opacity="0.25"/>
  <path d="M157,373 L163,379 L173,365" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="190" y="381" width="350" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="600" fill="#FFFFFF">
    Higher strategic upside
  </text>

  <circle cx="164" cy="430" r="14" fill="#FFFFFF" opacity="0.25"/>
  <path d="M157,429 L163,435 L173,421" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="190" y="437" width="350" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="600" fill="#FFFFFF">
    Strong customer signal
  </text>

  <rect x="675" y="150" width="500" height="330" rx="38" fill="url(#inactivePanel)" filter="url(#softShadow)"/>
  <rect x="688" y="163" width="474" height="304" rx="30" fill="none" stroke="#FFFFFF" stroke-opacity="0.08" stroke-width="2"/>

  <text x="715" y="224" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="54" font-weight="800" letter-spacing="4" fill="#141414" opacity="0.9">
    CONS
  </text>
  <text x="718" y="264" width="390" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#151515" opacity="0.78">
    Inactive state remains present, but low contrast keeps attention on the selected side.
  </text>

  <circle cx="734" cy="318" r="14" fill="#202124" opacity="0.35"/>
  <path d="M728,312 L740,324 M740,312 L728,324" fill="none" stroke="#111111" stroke-width="4" stroke-linecap="round"/>
  <text x="760" y="325" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="600" fill="#151515" opacity="0.82">
    More integration risk
  </text>

  <circle cx="734" cy="374" r="14" fill="#202124" opacity="0.35"/>
  <path d="M728,368 L740,380 M740,368 L728,380" fill="none" stroke="#111111" stroke-width="4" stroke-linecap="round"/>
  <text x="760" y="381" width="350" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="600" fill="#151515" opacity="0.82">
    Requires team retraining
  </text>

  <circle cx="734" cy="430" r="14" fill="#202124" opacity="0.35"/>
  <path d="M728,424 L740,436 M740,424 L728,436" fill="none" stroke="#111111" stroke-width="4" stroke-linecap="round"/>
  <text x="760" y="437" width="350" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="600" fill="#151515" opacity="0.82">
    Near-term cost pressure
  </text>

  <rect x="260" y="555" width="760" height="88" rx="44" fill="url(#trackGrad)" filter="url(#softShadow)"/>
  <rect x="278" y="569" width="346" height="60" rx="30" fill="#00FF55" opacity="0.18"/>
  <circle cx="450" cy="599" r="72" fill="#00FF55" opacity="0.16" filter="url(#greenGlow)"/>
  <circle cx="450" cy="599" r="46" fill="#00FF55" filter="url(#greenGlow)"/>
  <circle cx="450" cy="599" r="19" fill="#FFFFFF" opacity="0.95"/>

  <text x="320" y="605" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" letter-spacing="2" fill="#FFFFFF">
    BENEFITS
  </text>
  <text x="780" y="605" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" letter-spacing="2" fill="#141414" opacity="0.75">
    RISKS
  </text>

  <circle cx="604" cy="599" r="5" fill="#FFFFFF" opacity="0.6"/>
  <circle cx="676" cy="599" r="5" fill="#FFFFFF" opacity="0.22"/>

  <text x="80" y="676" width="1120" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#747B84">
    Morph state A shown: PROS active. For state B, move the handle to the right, turn CONS red, dim PROS, and keep object order unchanged.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<animate>` or `<animateTransform>`; the motion should come from PowerPoint Morph between two slides, not from SVG animation.
- ❌ Do not delete or reorder objects between state A and state B; Morph works best when every corresponding shape exists on both slides.
- ❌ Do not use `<use>` / `<symbol>` clones for repeated icons; create separate editable circles and paths so PowerPoint can morph or recolor them reliably.
- ❌ Do not apply filters to `<line>` elements; use paths or shapes for glowing accents if needed.
- ❌ Do not use masks or clip paths on regular shapes for the toggle; rounded rectangles and circles are enough and remain fully editable.

## Composition notes
- Keep the comparison panels in the upper two-thirds of the slide and the toggle in the lower third, centered beneath both panels.
- Use one saturated active color at a time; the inactive panel should be visible but deliberately low contrast.
- For the second Morph slide, preserve the same geometry and layer order, then change: active panel fill, inactive panel fill, text colors, handle `cx`, and glow color.
- Leave generous dark negative space around the panels so the color change and handle movement feel premium rather than crowded.