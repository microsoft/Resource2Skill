# SVG Recipe — Dark Mode Arc Diagram (Node-Link Sequence)

## Visual mechanism
A dark technical slide uses a horizontal node sequence as the anchor, then maps non-linear relationships with nested semicircular arcs above and below the baseline. Thin glowing strokes, apex labels, and small “traveling” particles make the static SVG feel like a captured frame from an animated data-flow sequence.

## SVG primitives needed
- 1× `<rect>` for the pitch-black background.
- 1× `<line>` for the subtle horizontal sequence axis.
- 7× `<circle>` for filled node checkpoints, plus 7× `<circle>` for faint node halos.
- 7× `<path>` for cubic Bézier arc links, alternating above and below the axis.
- 7× `<text>` for node labels beneath the axis.
- 7× `<text>` for percentage / weight labels positioned near each arc apex.
- 10× `<circle>` for small glowing “packet” dots placed along selected arcs to imply motion without using SVG animation.
- 2× decorative `<path>` elements for low-opacity corner HUD accents.
- 2× `<linearGradient>` definitions for cool arc strokes and node highlights.
- 2× `<filter>` definitions: one soft glow for arcs/particles, one subtle title glow.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="arcTop" x1="160" y1="160" x2="1120" y2="450" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#6EE7FF" stop-opacity="0.15"/>
      <stop offset="48%" stop-color="#C7D2FE" stop-opacity="0.88"/>
      <stop offset="100%" stop-color="#6EE7FF" stop-opacity="0.18"/>
    </linearGradient>
    <linearGradient id="arcBottom" x1="160" y1="450" x2="1120" y2="610" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#A78BFA" stop-opacity="0.18"/>
      <stop offset="50%" stop-color="#F0ABFC" stop-opacity="0.78"/>
      <stop offset="100%" stop-color="#A78BFA" stop-opacity="0.16"/>
    </linearGradient>
    <linearGradient id="nodeFill" x1="0" y1="438" x2="0" y2="464" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#A7F3D0"/>
    </linearGradient>
    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="titleGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2.4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#030406"/>

  <path d="M72 88 H230 M72 88 V132 M1050 88 H1208 M1208 88 V132"
        fill="none" stroke="#38BDF8" stroke-width="1.2" opacity="0.35"/>
  <path d="M82 628 H230 M82 628 V586 M1050 628 H1198 M1198 628 V586"
        fill="none" stroke="#A78BFA" stroke-width="1.2" opacity="0.28"/>

  <text x="0" y="82" width="1280" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700"
        letter-spacing="5" fill="#FFFFFF" filter="url(#titleGlow)">
    DATA FLOW DIAGRAM
  </text>
  <text x="0" y="118" width="1280" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="13" letter-spacing="2.5"
        fill="#94A3B8">
    NODE-LINK SEQUENCE / NON-LINEAR TRANSITIONS
  </text>

  <line x1="180" y1="450" x2="1100" y2="450"
        stroke="#64748B" stroke-width="1.5" opacity="0.62"/>

  <path d="M180 450 C180 300 486 300 486 450" fill="none"
        stroke="url(#arcTop)" stroke-width="2.1" stroke-linecap="round" filter="url(#softGlow)"/>
  <path d="M333 450 C333 132 946 132 946 450" fill="none"
        stroke="url(#arcTop)" stroke-width="2.1" stroke-linecap="round" opacity="0.88" filter="url(#softGlow)"/>
  <path d="M486 450 C486 320 793 320 793 450" fill="none"
        stroke="url(#arcTop)" stroke-width="1.8" stroke-linecap="round" opacity="0.72"/>
  <path d="M640 450 C640 348 946 348 946 450" fill="none"
        stroke="url(#arcTop)" stroke-width="1.8" stroke-linecap="round" opacity="0.68"/>
  <path d="M180 450 C180 594 640 594 640 450" fill="none"
        stroke="url(#arcBottom)" stroke-width="2" stroke-linecap="round" filter="url(#softGlow)"/>
  <path d="M486 450 C486 566 946 566 946 450" fill="none"
        stroke="url(#arcBottom)" stroke-width="1.9" stroke-linecap="round" opacity="0.78"/>
  <path d="M793 450 C793 526 1100 526 1100 450" fill="none"
        stroke="url(#arcBottom)" stroke-width="1.9" stroke-linecap="round" opacity="0.74"/>

  <text x="293" y="290" width="80" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#E0F2FE">10%</text>
  <text x="640" y="122" width="80" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">20%</text>
  <text x="640" y="310" width="80" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#CBD5E1">25%</text>
  <text x="793" y="340" width="80" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#CBD5E1">18%</text>
  <text x="410" y="622" width="80" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#F5D0FE">75%</text>
  <text x="716" y="594" width="80" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#F5D0FE">60%</text>
  <text x="946" y="554" width="80" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#F5D0FE">40%</text>

  <circle cx="257" cy="342" r="4" fill="#E0F2FE" filter="url(#softGlow)"/>
  <circle cx="394" cy="302" r="3" fill="#E0F2FE" opacity="0.7"/>
  <circle cx="470" cy="206" r="4" fill="#FFFFFF" filter="url(#softGlow)"/>
  <circle cx="650" cy="132" r="3.5" fill="#FFFFFF" filter="url(#softGlow)"/>
  <circle cx="810" cy="216" r="3" fill="#C7D2FE" opacity="0.76"/>
  <circle cx="340" cy="556" r="4" fill="#F0ABFC" filter="url(#softGlow)"/>
  <circle cx="535" cy="592" r="3" fill="#F0ABFC" opacity="0.72"/>
  <circle cx="670" cy="562" r="3.5" fill="#F0ABFC" filter="url(#softGlow)"/>
  <circle cx="865" cy="548" r="3" fill="#F0ABFC" opacity="0.72"/>
  <circle cx="1008" cy="508" r="3.5" fill="#F0ABFC" filter="url(#softGlow)"/>

  <circle cx="180" cy="450" r="15" fill="#38BDF8" opacity="0.12"/>
  <circle cx="333" cy="450" r="15" fill="#38BDF8" opacity="0.12"/>
  <circle cx="486" cy="450" r="15" fill="#38BDF8" opacity="0.12"/>
  <circle cx="640" cy="450" r="15" fill="#38BDF8" opacity="0.12"/>
  <circle cx="793" cy="450" r="15" fill="#38BDF8" opacity="0.12"/>
  <circle cx="946" cy="450" r="15" fill="#38BDF8" opacity="0.12"/>
  <circle cx="1100" cy="450" r="15" fill="#38BDF8" opacity="0.12"/>

  <circle cx="180" cy="450" r="7" fill="url(#nodeFill)" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="333" cy="450" r="7" fill="url(#nodeFill)" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="486" cy="450" r="7" fill="url(#nodeFill)" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="640" cy="450" r="7" fill="url(#nodeFill)" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="793" cy="450" r="7" fill="url(#nodeFill)" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="946" cy="450" r="7" fill="url(#nodeFill)" stroke="#FFFFFF" stroke-width="1.5"/>
  <circle cx="1100" cy="450" r="7" fill="url(#nodeFill)" stroke="#FFFFFF" stroke-width="1.5"/>

  <text x="140" y="492" width="80" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#E5E7EB">Data 1</text>
  <text x="293" y="492" width="80" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#E5E7EB">Data 2</text>
  <text x="446" y="492" width="80" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#E5E7EB">Data 3</text>
  <text x="600" y="492" width="80" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#E5E7EB">Data 4</text>
  <text x="753" y="492" width="80" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#E5E7EB">Data 5</text>
  <text x="906" y="492" width="80" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#E5E7EB">Data 6</text>
  <text x="1060" y="492" width="80" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#E5E7EB">Data 7</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<animate>` or `<animateMotion>` for the moving dots; represent motion as static glow particles, then add PowerPoint motion paths manually if needed.
- ❌ Do not use `marker-end` arrowheads on arc paths; PowerPoint translation may drop path markers.
- ❌ Do not apply `filter` to the baseline `<line>`; use filters only on paths, circles, or text.
- ❌ Do not use `<textPath>` to curve labels along arcs; place percentage labels as normal `<text>` at the arc apex.
- ❌ Do not clip or mask arc strokes; keep the links as directly editable `<path>` elements.

## Composition notes
- Place the baseline around 60–65% down the slide so tall upper arcs have enough room to nest cleanly.
- Use the strongest glow only on one or two “hero” arcs; the remaining links should stay thin and semi-transparent to avoid clutter.
- Keep node labels below the axis and percentage labels near arc apices, never directly on the baseline.
- The dark background needs generous negative space; resist filling the top area with annotations unless they align to arc peaks.