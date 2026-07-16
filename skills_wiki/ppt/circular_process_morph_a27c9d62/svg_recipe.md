# SVG Recipe — Circular Process Morph

## Visual mechanism
A large circular process ring anchors the slide while a contrasting donut-wedge highlight rotates between four icon nodes. On duplicated Morph slides, keep the same shapes and IDs, then rotate the wedge and update the matching list card to create a polished “guided focus” sequence.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 1× decorative `<path>` blob for subtle background depth
- 1× donut `<path>` for the base circular process ring
- 1× donut-wedge `<path id="morph_wedge">` for the rotating Morph highlight
- 4× `<circle>` for icon stations around the ring
- 4× small icon groups made from editable `<path>`, `<circle>`, `<ellipse>`, and `<line>` primitives
- 4× connector `<path>` curves from ring nodes toward the list
- 4× `<circle>` for numbered list badges
- 8× rounded `<rect>` for list title pills and description panels
- 12× `<text>` elements with explicit `width` attributes for numbers, titles, and descriptions
- 2× `<linearGradient>` for premium maroon/navy fills
- 1× `<radialGradient>` for soft ring depth
- 2× `<filter>` definitions for shadow and active glow, applied only to shapes/text-safe primitives

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#f7eef0"/>
    </linearGradient>
    <linearGradient id="maroonGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#a23848"/>
      <stop offset="100%" stop-color="#6f1727"/>
    </linearGradient>
    <linearGradient id="navyGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#3c5397"/>
      <stop offset="100%" stop-color="#1f2d5a"/>
    </linearGradient>
    <radialGradient id="ringDepth" cx="50%" cy="42%" r="62%">
      <stop offset="0%" stop-color="#b94b5d"/>
      <stop offset="100%" stop-color="#842333"/>
    </radialGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="activeGlow" x="-35%" y="-35%" width="170%" height="170%">
      <feGaussianBlur stdDeviation="8" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>
  <path d="M-40,665 C160,565 275,675 455,600 C610,536 705,635 850,586 C1010,532 1115,592 1325,480 L1325,760 L-40,760 Z"
        fill="#8f2433" opacity="0.06"/>

  <text x="650" y="58" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#27212a">
    Four-Phase Growth System
  </text>
  <text x="650" y="92" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#7b6970">
    The rotating wedge becomes the Morph focus cue; the active card changes with it.
  </text>

  <!-- Base circular process ring -->
  <path id="base_ring" fill="url(#ringDepth)" fill-rule="evenodd" filter="url(#softShadow)"
        d="M370,140
           A220,220 0 1,1 369.9,140
           M370,228
           A132,132 0 1,0 370.1,228 Z"/>

  <!-- Morph object: duplicate the slide and rotate this same wedge by 90/180/270 degrees around 370 360 -->
  <path id="morph_wedge" transform="rotate(0 370 360)" fill="url(#navyGrad)" fill-rule="evenodd" filter="url(#activeGlow)"
        d="M214.4,204.4
           A220,220 0 0,1 525.6,204.4
           L463.3,266.7
           A132,132 0 0,0 276.7,266.7 Z"/>

  <circle cx="370" cy="360" r="88" fill="#ffffff" opacity="0.96" filter="url(#softShadow)"/>
  <text x="292" y="338" width="156" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#8f2433">
    PROCESS
  </text>
  <text x="292" y="366" width="156" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" letter-spacing="2" fill="#8f2433">
    MORPH
  </text>

  <!-- Curved connectors -->
  <path d="M370,173 C465,148 546,126 622,130" fill="none" stroke="#8f2433" stroke-width="3" opacity="0.35" stroke-dasharray="8 8"/>
  <path d="M557,360 C590,329 610,283 622,265" fill="none" stroke="#8f2433" stroke-width="3" opacity="0.25" stroke-dasharray="8 8"/>
  <path d="M370,547 C480,548 555,505 622,400" fill="none" stroke="#8f2433" stroke-width="3" opacity="0.25" stroke-dasharray="8 8"/>
  <path d="M183,360 C385,420 515,520 622,535" fill="none" stroke="#8f2433" stroke-width="3" opacity="0.20" stroke-dasharray="8 8"/>

  <!-- Ring nodes and icons -->
  <circle cx="370" cy="173" r="43" fill="url(#navyGrad)" filter="url(#activeGlow)"/>
  <ellipse cx="370" cy="166" rx="20" ry="8" fill="none" stroke="#ffffff" stroke-width="5"/>
  <path d="M350,166 L350,185 C350,190 390,190 390,185 L390,166" fill="none" stroke="#ffffff" stroke-width="5"/>
  <path d="M350,177 C350,183 390,183 390,177" fill="none" stroke="#ffffff" stroke-width="5"/>

  <circle cx="557" cy="360" r="38" fill="url(#maroonGrad)"/>
  <circle cx="557" cy="360" r="22" fill="none" stroke="#ffffff" stroke-width="5"/>
  <circle cx="557" cy="360" r="8" fill="#ffffff"/>
  <line x1="557" y1="334" x2="557" y2="346" stroke="#ffffff" stroke-width="4"/>
  <line x1="557" y1="374" x2="557" y2="386" stroke="#ffffff" stroke-width="4"/>

  <circle cx="370" cy="547" r="38" fill="url(#maroonGrad)"/>
  <path d="M349,548 L363,563 L393,529" fill="none" stroke="#ffffff" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="370" cy="547" r="24" fill="none" stroke="#ffffff" stroke-width="4" opacity="0.7"/>

  <circle cx="183" cy="360" r="38" fill="url(#maroonGrad)"/>
  <path d="M166,345 C175,339 188,340 196,348 L186,358 L195,367 C187,375 173,376 164,368 C157,361 158,351 166,345 Z"
        fill="none" stroke="#ffffff" stroke-width="5" stroke-linejoin="round"/>
  <line x1="190" y1="365" x2="204" y2="379" stroke="#ffffff" stroke-width="6" stroke-linecap="round"/>

  <!-- Step 1 active card -->
  <circle cx="650" cy="130" r="30" fill="url(#navyGrad)" filter="url(#activeGlow)"/>
  <text x="634" y="143" width="32" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#ffffff">1</text>
  <rect x="696" y="105" width="382" height="48" rx="24" fill="url(#navyGrad)" filter="url(#softShadow)"/>
  <text x="722" y="137" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="23" font-weight="700" fill="#ffffff">Earn Your Money</text>
  <rect x="696" y="162" width="470" height="58" rx="18" fill="#8f2433" opacity="0.55"/>
  <text x="722" y="185" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#ffffff">
    Build financial stability through disciplined earning, saving, and reinvestment.
  </text>

  <!-- Step 2 -->
  <circle cx="650" cy="265" r="28" fill="url(#maroonGrad)"/>
  <text x="634" y="278" width="32" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#ffffff">2</text>
  <rect x="696" y="242" width="345" height="44" rx="22" fill="url(#maroonGrad)"/>
  <text x="722" y="272" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" fill="#ffffff">Solve Your Problem</text>
  <rect x="696" y="294" width="430" height="52" rx="16" fill="#8f2433" opacity="0.32"/>
  <text x="722" y="316" width="380" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#ffffff">Clarify the issue, remove friction, and choose the highest-leverage action.</text>

  <!-- Step 3 -->
  <circle cx="650" cy="400" r="28" fill="url(#maroonGrad)"/>
  <text x="634" y="413" width="32" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#ffffff">3</text>
  <rect x="696" y="377" width="330" height="44" rx="22" fill="url(#maroonGrad)"/>
  <text x="722" y="407" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" fill="#ffffff">Aim Your Target</text>
  <rect x="696" y="429" width="430" height="52" rx="16" fill="#8f2433" opacity="0.32"/>
  <text x="722" y="451" width="380" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#ffffff">Translate strategy into daily targets that keep momentum visible.</text>

  <!-- Step 4 -->
  <circle cx="650" cy="535" r="28" fill="url(#maroonGrad)"/>
  <text x="634" y="548" width="32" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#ffffff">4</text>
  <rect x="696" y="512" width="345" height="44" rx="22" fill="url(#maroonGrad)"/>
  <text x="722" y="542" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" fill="#ffffff">Get Your Success</text>
  <rect x="696" y="564" width="430" height="52" rx="16" fill="#8f2433" opacity="0.32"/>
  <text x="722" y="586" width="380" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#ffffff">Compound consistent execution into measurable wins and lasting progress.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<animate>` or `<animateTransform>` for the rotation; create duplicate PPT slides and rely on PowerPoint Morph instead.
- ❌ Do not build the ring with `<mask>` or clipped non-image shapes; use editable donut-style `<path>` geometry.
- ❌ Do not use `marker-end` for arrows on connector paths; simple dashed curves are safer and remain editable.
- ❌ Do not omit `width` on `<text>` elements; PowerPoint needs fixed text box widths for clean rendering.
- ❌ Do not use `<use>` to duplicate icons or nodes; repeat the editable shapes directly.

## Composition notes
- Keep the circular mechanism in the left 40–45% of the slide and reserve the right side for the synchronized list.
- For Morph, duplicate the slide four times; rotate `morph_wedge` by `0`, `90`, `180`, and `270` degrees around the ring center, then swap the navy active styling to the corresponding node and card.
- The active state should be visibly stronger: navy fill, glow, slightly larger badge/card, and higher opacity connector.
- Maintain generous white space around the ring so the rotating wedge feels premium rather than crowded.