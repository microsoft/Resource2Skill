# SVG Recipe — Hexagonal Portrait Spotlight

## Visual mechanism
A centered portrait is cropped into a pointy-topped hexagon and wrapped in a thick cyan geometric frame, creating a sharp modern “spotlight” focal point. Radiating white tick lines and bold centered typography turn a standard employee headshot into a premium speaker or team-introduction slide.

## SVG primitives needed
- 1× `<rect>` for the full-slide slate blue background
- 2× `<radialGradient>` / `<linearGradient>` for subtle background depth and portrait-frame sheen
- 1× `<clipPath>` with a hexagonal `<path>` applied to the portrait `<image>`
- 1× `<image>` for the professional portrait photo, clipped to the inner hexagon
- 2× `<path>` for the outer cyan hexagon frame and inner dark rim
- 18× `<line>` for subtle radiating spotlight accents around the portrait
- 2× `<filter>` with blur/offset for soft glow and dimensional shadow on the hex frame
- 4× `<text>` elements for eyebrow, name, title, and small descriptor; each with explicit `width`

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgSpot" cx="50%" cy="34%" r="62%">
      <stop offset="0%" stop-color="#7898B7"/>
      <stop offset="48%" stop-color="#5B83A6"/>
      <stop offset="100%" stop-color="#416B8F"/>
    </radialGradient>

    <linearGradient id="cyanFrame" x1="480" y1="80" x2="820" y2="440" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#8AF2FF"/>
      <stop offset="55%" stop-color="#6FD4E4"/>
      <stop offset="100%" stop-color="#42AFC4"/>
    </linearGradient>

    <filter id="hexShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="12" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="8"/>
    </filter>

    <clipPath id="portraitHex">
      <path d="M 640 96 L 782 178 L 782 342 L 640 424 L 498 342 L 498 178 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgSpot)"/>

  <path d="M 80 660 C 230 585 320 610 470 676 C 620 742 770 710 940 636 C 1085 573 1180 585 1280 630 L 1280 720 L 80 720 Z"
        fill="#FFFFFF" opacity="0.055"/>
  <path d="M 0 92 C 170 38 300 58 420 112 C 570 180 710 170 880 96 C 1040 26 1160 34 1280 82 L 1280 0 L 0 0 Z"
        fill="#123B5D" opacity="0.12"/>

  <circle cx="640" cy="260" r="238" fill="#6FD4E4" opacity="0.18" filter="url(#softGlow)"/>

  <g stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" opacity="0.42">
    <line x1="640" y1="34" x2="640" y2="4"/>
    <line x1="640" y1="486" x2="640" y2="516"/>
    <line x1="448" y1="145" x2="414" y2="126"/>
    <line x1="832" y1="145" x2="866" y2="126"/>
    <line x1="448" y1="375" x2="414" y2="394"/>
    <line x1="832" y1="375" x2="866" y2="394"/>
    <line x1="430" y1="260" x2="388" y2="260"/>
    <line x1="850" y1="260" x2="892" y2="260"/>
    <line x1="512" y1="72" x2="492" y2="42"/>
    <line x1="768" y1="72" x2="788" y2="42"/>
    <line x1="512" y1="448" x2="492" y2="478"/>
    <line x1="768" y1="448" x2="788" y2="478"/>
  </g>

  <g stroke="#FFFFFF" stroke-width="1.5" stroke-linecap="round" opacity="0.25">
    <line x1="380" y1="198" x2="338" y2="188"/>
    <line x1="900" y1="198" x2="942" y2="188"/>
    <line x1="380" y1="322" x2="338" y2="332"/>
    <line x1="900" y1="322" x2="942" y2="332"/>
    <line x1="570" y1="28" x2="562" y2="0"/>
    <line x1="710" y1="28" x2="718" y2="0"/>
  </g>

  <path d="M 640 58 L 815 159 L 815 361 L 640 462 L 465 361 L 465 159 Z"
        fill="url(#cyanFrame)" filter="url(#hexShadow)"/>
  <path d="M 640 82 L 794 171 L 794 349 L 640 438 L 486 349 L 486 171 Z"
        fill="#2F5E83" opacity="0.85"/>

  <image href="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=900&q=85"
         x="456" y="72" width="368" height="430"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#portraitHex)"/>

  <path d="M 640 96 L 782 178 L 782 342 L 640 424 L 498 342 L 498 178 Z"
        fill="none" stroke="#B7F7FF" stroke-width="3" opacity="0.75"/>

  <text x="390" y="530" width="500"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="19" font-weight="700" letter-spacing="4"
        text-anchor="middle" fill="#7BE3F2">
    <tspan x="640">EMPLOYEE SPOTLIGHT</tspan>
  </text>

  <text x="290" y="590" width="700"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="58" font-weight="800" letter-spacing="2"
        text-anchor="middle" fill="#FFFFFF">
    <tspan x="640">CASEY SADLER</tspan>
  </text>

  <text x="350" y="634" width="580"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="400" letter-spacing="1.6"
        text-anchor="middle" fill="#FFFFFF" opacity="0.95">
    <tspan x="640">SENIOR MANAGER OF</tspan>
    <tspan x="640" dy="30">PROFESSIONAL DEVELOPMENT</tspan>
  </text>

  <text x="440" y="696" width="400"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="600" letter-spacing="2"
        text-anchor="middle" fill="#D9F7FF" opacity="0.65">
    <tspan x="640">LEADERSHIP ENABLEMENT TEAM</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Applying `clip-path` to a `<path>` or `<rect>` for the frame; use the clip only on the portrait `<image>`
- ❌ Using `<mask>` to crop the photo; the translator may hard-fail or ignore it
- ❌ Using `<use>` to repeat the radiating lines; duplicate `<line>` elements directly
- ❌ Putting `filter` on the radiating `<line>` elements; line filters are dropped
- ❌ Using `marker-end` for decorative rays or arrows; this design should rely on plain lines

## Composition notes
- Keep the hex portrait centered and slightly above the vertical midpoint; it should occupy roughly the upper 60% of the slide.
- Reserve the lower third for centered typography: small cyan eyebrow, large white name, then smaller white role/title.
- Use a solid or softly radial slate-blue background so the cyan frame and white text remain dominant.
- Radiating lines should be subtle and symmetrical; they add energy without competing with the face.