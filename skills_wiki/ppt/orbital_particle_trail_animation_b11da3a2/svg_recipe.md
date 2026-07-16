# SVG Recipe — Orbital Particle Trail Animation

## Visual mechanism
Create the impression of animated orbital motion by layering glowing particle dots along several tilted elliptical paths around a central circular photo. Since SVG-to-PPT does not preserve SVG animation, render a premium static “motion moment” with fading dot sizes, dashed orbit guides, glow filters, and staggered trail positions that can later receive native PowerPoint motion paths if needed.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark radial-gradient space background
- 3× decorative `<path>` blobs for subtle nebula depth and asymmetrical energy
- 3× `<ellipse>` for thin dashed orbital guide rings
- 1× `<image>` clipped by 1× circular `<clipPath>` for the central hero image
- 2× `<circle>` for the image border and luminous halo
- 30–45× `<circle>` for particle dots with varying size, opacity, and glow
- 1× `<linearGradient>` for accent strokes and title emphasis
- 1× `<radialGradient>` for the background
- 2× `<filter>` definitions: one soft glow for particles/halo, one shadow for the photo medallion
- 3× `<text>` elements with explicit `width` attributes for title, subtitle, and small label

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="spaceBg" cx="64%" cy="50%" r="78%">
      <stop offset="0%" stop-color="#073A78"/>
      <stop offset="42%" stop-color="#061A3D"/>
      <stop offset="100%" stop-color="#150816"/>
    </radialGradient>

    <linearGradient id="goldStroke" x1="660" y1="190" x2="1000" y2="540" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFF2A8"/>
      <stop offset="48%" stop-color="#FFC000"/>
      <stop offset="100%" stop-color="#FF7A18"/>
    </linearGradient>

    <linearGradient id="cyanAccent" x1="120" y1="0" x2="500" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#7DEBFF"/>
      <stop offset="100%" stop-color="#FFFFFF"/>
    </linearGradient>

    <filter id="softGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="photoShadow" x="-35%" y="-35%" width="170%" height="170%">
      <feOffset dx="0" dy="16" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="photoClip">
      <circle cx="840" cy="360" r="118"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#spaceBg)"/>

  <path d="M880 70 C1040 40 1160 105 1210 235 C1260 365 1175 500 1020 485 C910 474 875 385 905 295 C930 220 800 130 880 70 Z"
        fill="#2B0E49" opacity="0.38"/>
  <path d="M-40 525 C105 445 245 482 300 600 C342 691 235 750 80 730 C-20 718 -105 612 -40 525 Z"
        fill="#094F78" opacity="0.32"/>
  <path d="M575 135 C660 88 740 118 770 178 C804 246 748 307 661 290 C580 274 512 172 575 135 Z"
        fill="#0B8FB0" opacity="0.13"/>

  <text x="96" y="172" width="470" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="600" fill="#7DEBFF" letter-spacing="3">
    DATA ORBIT SYSTEM
  </text>

  <text x="92" y="286" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="68" font-weight="800" fill="#FFFFFF">
    Orbital
    <tspan x="92" dy="76" fill="url(#cyanAccent)">Particle Trails</tspan>
  </text>

  <text x="98" y="468" width="470" font-family="Segoe UI, Microsoft YaHei" font-size="24" fill="#C9D9F2" opacity="0.9">
    Continuous motion, layered focus, and a high-tech keynote atmosphere.
  </text>

  <line x1="100" y1="520" x2="292" y2="520" stroke="#FFC000" stroke-width="4" stroke-linecap="round"/>
  <circle cx="320" cy="520" r="5" fill="#FFFFFF" opacity="0.85" filter="url(#softGlow)"/>

  <ellipse cx="840" cy="360" rx="250" ry="110" fill="none" stroke="#FFFFFF" stroke-width="1.4"
           stroke-opacity="0.23" stroke-dasharray="7 14" transform="rotate(-18 840 360)"/>
  <ellipse cx="840" cy="360" rx="295" ry="136" fill="none" stroke="#7DEBFF" stroke-width="1.2"
           stroke-opacity="0.18" stroke-dasharray="4 18" transform="rotate(18 840 360)"/>
  <ellipse cx="840" cy="360" rx="210" ry="88" fill="none" stroke="#FFC000" stroke-width="1.1"
           stroke-opacity="0.22" stroke-dasharray="2 13" transform="rotate(42 840 360)"/>

  <circle cx="840" cy="360" r="144" fill="#FFC000" opacity="0.22" filter="url(#softGlow)"/>
  <circle cx="840" cy="360" r="129" fill="#07152D" filter="url(#photoShadow)"/>
  <image href="https://images.unsplash.com/photo-1549492423-400259a565b3?w=900"
         x="700" y="220" width="280" height="280" clip-path="url(#photoClip)" preserveAspectRatio="xMidYMid slice"/>
  <circle cx="840" cy="360" r="122" fill="none" stroke="url(#goldStroke)" stroke-width="8"/>
  <circle cx="840" cy="360" r="137" fill="none" stroke="#FFFFFF" stroke-width="1.5" stroke-opacity="0.3"/>

  <circle cx="1062" cy="275" r="8" fill="#FFFFFF" opacity="1" filter="url(#softGlow)"/>
  <circle cx="1040" cy="296" r="6.8" fill="#FFFFFF" opacity="0.82" filter="url(#softGlow)"/>
  <circle cx="1012" cy="313" r="5.8" fill="#FFFFFF" opacity="0.64" filter="url(#softGlow)"/>
  <circle cx="978" cy="329" r="4.8" fill="#FFFFFF" opacity="0.46" filter="url(#softGlow)"/>
  <circle cx="938" cy="342" r="3.8" fill="#FFFFFF" opacity="0.3" filter="url(#softGlow)"/>
  <circle cx="894" cy="352" r="3" fill="#FFFFFF" opacity="0.18"/>

  <circle cx="590" cy="400" r="7.5" fill="#7DEBFF" opacity="0.95" filter="url(#softGlow)"/>
  <circle cx="620" cy="379" r="6.2" fill="#7DEBFF" opacity="0.75" filter="url(#softGlow)"/>
  <circle cx="656" cy="359" r="5.2" fill="#7DEBFF" opacity="0.56" filter="url(#softGlow)"/>
  <circle cx="695" cy="343" r="4.2" fill="#7DEBFF" opacity="0.38" filter="url(#softGlow)"/>
  <circle cx="737" cy="332" r="3.3" fill="#7DEBFF" opacity="0.24"/>

  <circle cx="998" cy="478" r="7" fill="#FFC000" opacity="0.95" filter="url(#softGlow)"/>
  <circle cx="970" cy="462" r="5.8" fill="#FFC000" opacity="0.74" filter="url(#softGlow)"/>
  <circle cx="938" cy="446" r="4.8" fill="#FFC000" opacity="0.53" filter="url(#softGlow)"/>
  <circle cx="902" cy="429" r="3.9" fill="#FFC000" opacity="0.34"/>
  <circle cx="864" cy="410" r="3" fill="#FFC000" opacity="0.2"/>

  <circle cx="716" cy="219" r="5.8" fill="#FFFFFF" opacity="0.82" filter="url(#softGlow)"/>
  <circle cx="748" cy="203" r="4.8" fill="#FFFFFF" opacity="0.58" filter="url(#softGlow)"/>
  <circle cx="783" cy="196" r="3.8" fill="#FFFFFF" opacity="0.36"/>
  <circle cx="818" cy="198" r="3" fill="#FFFFFF" opacity="0.2"/>

  <circle cx="1080" cy="397" r="5.5" fill="#7DEBFF" opacity="0.75" filter="url(#softGlow)"/>
  <circle cx="1112" cy="370" r="4.3" fill="#7DEBFF" opacity="0.48"/>
  <circle cx="1132" cy="338" r="3.3" fill="#7DEBFF" opacity="0.28"/>

  <text x="730" y="640" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#FFFFFF" opacity="0.68" text-anchor="middle">
    editable SVG particles · add PPT motion paths for live orbit
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<animate>` or `<animateTransform>`; they hard-fail and will not become PowerPoint animations.
- ❌ Do not use `<textPath>` to place bullets around an orbit; it is not preserved reliably.
- ❌ Do not rely on `marker-end` for orbit direction arrows; use plain dots or separate `<line>` arrows only if needed.
- ❌ Do not apply `filter` to `<line>` orbit guides; use filtered circles/ellipses/paths instead.
- ❌ Do not clip particles or decorative paths with `clip-path`; clipping is only dependable on `<image>` elements.

## Composition notes
- Keep the visual engine on the right 55–60% of the slide and reserve the left side for a large keynote title with generous negative space.
- Use three orbital radii with different rotations, colors, and dot sizes so the trails feel layered rather than like a flat target.
- The brightest particle should sit at the “head” of each trail; fade opacity and size backward to imply motion blur.
- Use a warm accent border around the circular image to contrast with the cold blue/cyan particle system.