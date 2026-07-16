# SVG Recipe — Interactive Morph Toggle

## Visual mechanism
A two-state comparison slide uses identical SVG object IDs across two slides so PowerPoint Morph can animate the toggle knob, panel colors, glows, and text emphasis between “left active” and “right active.” Invisible click zones sit above the toggle halves, becoming hyperlink targets in PowerPoint while the visual layer remains sleek and app-like.

## SVG primitives needed
- 1× `<rect>` full-slide black background
- 2× large rounded `<rect>` for the comparison panels, one active and one inactive
- 2× semi-transparent highlight `<rect>` overlays for active/inactive panel depth
- 4× decorative `<path>` corner arcs / accent strokes around the active panel
- 2× title `<text>` objects with glow filters, one prominent and one muted
- 6× body `<text>` objects with nested `<tspan>` for bold labels and explanatory copy
- 1× rounded `<rect>` for the toggle track
- 2× rounded `<rect>` pill segments inside the toggle track for active/inactive halves
- 1× `<circle>` for the movable toggle knob
- 6× `<path>` chevrons inside the toggle bar for directional motion cues
- 2× transparent `<rect>` hotspot overlays for future PowerPoint hyperlinks
- 2× `<filter>` definitions for soft shadows and glow
- 3× `<linearGradient>` definitions for active green, inactive dark, and toggle glass effects

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="prosPanelGrad" x1="110" y1="90" x2="610" y2="480" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#39ff14"/>
      <stop offset="0.55" stop-color="#18b60c"/>
      <stop offset="1" stop-color="#075a05"/>
    </linearGradient>
    <linearGradient id="darkPanelGrad" x1="670" y1="90" x2="1170" y2="480" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#333333"/>
      <stop offset="1" stop-color="#171717"/>
    </linearGradient>
    <linearGradient id="toggleGlass" x1="440" y1="590" x2="840" y2="670" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#303030"/>
      <stop offset="0.5" stop-color="#111111"/>
      <stop offset="1" stop-color="#2a2a2a"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="16"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="limeGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="redGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect id="bg" x="0" y="0" width="1280" height="720" fill="#000000"/>

  <rect id="panel_pros" x="110" y="90" width="500" height="390" rx="42" fill="url(#prosPanelGrad)" filter="url(#softShadow)"/>
  <rect id="panel_cons" x="670" y="90" width="500" height="390" rx="42" fill="url(#darkPanelGrad)" filter="url(#softShadow)"/>

  <rect id="pros_sheen" x="132" y="112" width="456" height="82" rx="28" fill="#ffffff" opacity="0.14"/>
  <rect id="cons_sheen" x="692" y="112" width="456" height="82" rx="28" fill="#ffffff" opacity="0.05"/>

  <path id="pros_corner_top" d="M142 172 C142 120 170 112 220 112" fill="none" stroke="#c8ffbf" stroke-width="5" stroke-linecap="round" opacity="0.9" filter="url(#limeGlow)"/>
  <path id="pros_corner_bottom" d="M578 398 C578 450 550 458 500 458" fill="none" stroke="#c8ffbf" stroke-width="5" stroke-linecap="round" opacity="0.75" filter="url(#limeGlow)"/>
  <path id="cons_corner_top" d="M702 172 C702 120 730 112 780 112" fill="none" stroke="#777777" stroke-width="4" stroke-linecap="round" opacity="0.25"/>
  <path id="cons_corner_bottom" d="M1138 398 C1138 450 1110 458 1060 458" fill="none" stroke="#777777" stroke-width="4" stroke-linecap="round" opacity="0.25"/>

  <text id="title_pros" x="160" y="180" width="400" font-family="Segoe UI, Microsoft YaHei" font-size="70" font-weight="800" fill="#ffffff" letter-spacing="2" filter="url(#limeGlow)">PROS</text>
  <text id="title_cons" x="720" y="180" width="400" font-family="Segoe UI, Microsoft YaHei" font-size="70" font-weight="800" fill="#a6a6a6" letter-spacing="2" opacity="0.75">CONS</text>

  <text id="pros_body_1" x="160" y="245" width="390" font-family="Segoe UI, Microsoft YaHei" font-size="26" fill="#ffffff">
    <tspan font-weight="800">Visual momentum:</tspan><tspan dx="6" font-weight="400">Turns a comparison into a guided choice.</tspan>
  </text>
  <text id="pros_body_2" x="160" y="315" width="390" font-family="Segoe UI, Microsoft YaHei" font-size="26" fill="#ffffff">
    <tspan font-weight="800">Low cognitive load:</tspan><tspan dx="6" font-weight="400">Only one side competes for attention.</tspan>
  </text>
  <text id="pros_body_3" x="160" y="385" width="390" font-family="Segoe UI, Microsoft YaHei" font-size="26" fill="#ffffff">
    <tspan font-weight="800">Presenter control:</tspan><tspan dx="6" font-weight="400">Click to pace the story like an app.</tspan>
  </text>

  <text id="cons_body_1" x="720" y="245" width="390" font-family="Segoe UI, Microsoft YaHei" font-size="25" fill="#a6a6a6" opacity="0.72">
    <tspan font-weight="800">Extra setup:</tspan><tspan dx="6" font-weight="400">Requires two matched Morph slides.</tspan>
  </text>
  <text id="cons_body_2" x="720" y="315" width="390" font-family="Segoe UI, Microsoft YaHei" font-size="25" fill="#a6a6a6" opacity="0.72">
    <tspan font-weight="800">Click discipline:</tspan><tspan dx="6" font-weight="400">Hotspots must remain above the switch.</tspan>
  </text>
  <text id="cons_body_3" x="720" y="385" width="390" font-family="Segoe UI, Microsoft YaHei" font-size="25" fill="#a6a6a6" opacity="0.72">
    <tspan font-weight="800">State pairing:</tspan><tspan dx="6" font-weight="400">Object IDs must stay identical.</tspan>
  </text>

  <rect id="toggle_track" x="440" y="590" width="400" height="80" rx="40" fill="url(#toggleGlass)" stroke="#444444" stroke-width="2" filter="url(#softShadow)"/>
  <rect id="toggle_left_fill" x="448" y="598" width="184" height="64" rx="32" fill="#39ff14" opacity="0.92"/>
  <rect id="toggle_right_fill" x="648" y="598" width="184" height="64" rx="32" fill="#ff0000" opacity="0.18"/>
  <circle id="toggle_knob" cx="520" cy="630" r="35" fill="#ffffff" filter="url(#softShadow)"/>

  <path id="chev_1" d="M672 612 L692 630 L672 648" fill="none" stroke="#ff4c4c" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" opacity="0.45"/>
  <path id="chev_2" d="M714 612 L734 630 L714 648" fill="none" stroke="#ff4c4c" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" opacity="0.6"/>
  <path id="chev_3" d="M756 612 L776 630 L756 648" fill="none" stroke="#ff4c4c" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" opacity="0.75"/>
  <path id="chev_4" d="M506 613 L488 630 L506 647" fill="none" stroke="#102b0c" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" opacity="0.35"/>
  <text id="toggle_label_left" x="470" y="638" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="800" fill="#0b2108">ON</text>
  <text id="toggle_label_right" x="705" y="638" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="800" fill="#ff8a8a" opacity="0.7">CONS</text>

  <text id="hint" x="0" y="535" width="1280" font-family="Segoe UI, Microsoft YaHei" font-size="20" fill="#777777" text-anchor="middle">Click the toggle halves in PowerPoint to jump between matched Morph states</text>

  <rect id="hotspot_pros" x="440" y="590" width="200" height="80" rx="40" fill="#ffffff" opacity="0.001"/>
  <rect id="hotspot_cons" x="640" y="590" width="200" height="80" rx="40" fill="#ffffff" opacity="0.001"/>
</svg>
```

## Avoid in this skill
- ❌ SVG animation tags such as `<animate>` or `<animateTransform>`; the motion should come from PowerPoint Morph between two slides.
- ❌ `<use>` or `<symbol>` for repeated chevrons; duplicate editable `<path>` elements directly so Morph and PPT editing remain predictable.
- ❌ `clip-path` on panel shapes or text; clipping only translates reliably on `<image>`, and this toggle does not require clipped non-image elements.
- ❌ `marker-end` arrows for the toggle cues; use explicit chevron `<path>` strokes instead.
- ❌ Changing object structure between states; Morph works best when the same IDs and same primitive types exist on both slides.

## Composition notes
- Build two SVG slides from the same structure: in State A, the left panel is bright green and the knob sits left; in State B, the right panel becomes red and the knob moves right.
- Keep the toggle centered below the panels with generous black space around it so the interaction reads as the slide’s control surface.
- Use strong active/inactive contrast: active panel gets saturated color, white text, glow, and accent strokes; inactive panel gets charcoal fill and grey text.
- Place invisible hotspot rectangles as the topmost objects over each toggle half, then assign PowerPoint hyperlinks/actions to jump to the opposite Morph slide.