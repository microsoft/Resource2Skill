# SVG Recipe — Cinematic Dark Mode Product Reveal

## Visual mechanism
A pure-black stage removes all visual noise, leaving a single glowing product mockup suspended in the center like a keynote reveal. The phone screen carries a saturated warm-to-cool blur, while a thin white frame and spaced white title typography add cinematic restraint.

## SVG primitives needed
- 1× `<rect>` for the pitch-black full-slide background
- 1× `<rect>` for the thin inset white cinematic border
- 2× `<ellipse>` for extremely subtle ambient glow behind the product
- 3× `<filter>` definitions for soft product shadow, screen bloom, and faint text glow
- 1× `<linearGradient>` for the phone bezel highlight
- 1× `<linearGradient>` for the glass reflection sheen
- 1× `<radialGradient>` for background vignette glow
- 1× `<clipPath>` with rounded phone-screen path applied to the wallpaper image
- 1× `<image>` for the blurred colorful product wallpaper inside the phone
- 4× `<rect>` for phone outer body, inner screen, side buttons, and glass reflection panel
- 2× `<path>` for the notch and bottom speaker / logo accent shapes
- 4× `<text>` elements for the reveal title and compact product-studio branding

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="stageGlow" cx="50%" cy="50%" r="55%">
      <stop offset="0%" stop-color="#111827" stop-opacity="0.34"/>
      <stop offset="55%" stop-color="#030303" stop-opacity="0.72"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="1"/>
    </radialGradient>

    <linearGradient id="bezelGradient" x1="475" y1="40" x2="805" y2="650" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#15233d"/>
      <stop offset="18%" stop-color="#0b0e15"/>
      <stop offset="55%" stop-color="#050507"/>
      <stop offset="100%" stop-color="#171717"/>
    </linearGradient>

    <linearGradient id="glassSheen" x1="520" y1="100" x2="770" y2="620" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.16"/>
      <stop offset="34%" stop-color="#ffffff" stop-opacity="0.02"/>
      <stop offset="70%" stop-color="#ffffff" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="edgeLight" x1="512" y1="55" x2="794" y2="636" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#4878ff" stop-opacity="0.55"/>
      <stop offset="35%" stop-color="#111111" stop-opacity="0"/>
      <stop offset="100%" stop-color="#ff315f" stop-opacity="0.32"/>
    </linearGradient>

    <filter id="phoneShadow" x="-30%" y="-20%" width="160%" height="150%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="screenBloom" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="5"/>
    </filter>

    <filter id="titleGlow" x="-20%" y="-40%" width="140%" height="180%">
      <feGaussianBlur stdDeviation="1.2"/>
    </filter>

    <clipPath id="screenClip">
      <path d="M526 68
               L754 68
               Q780 68 780 98
               L780 602
               Q780 632 748 632
               L532 632
               Q500 632 500 602
               L500 98
               Q500 68 526 68 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#000000"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#stageGlow)"/>

  <ellipse cx="640" cy="340" rx="210" ry="315" fill="#0b1020" opacity="0.28" filter="url(#screenBloom)"/>
  <ellipse cx="640" cy="355" rx="140" ry="250" fill="#091b2a" opacity="0.20" filter="url(#screenBloom)"/>

  <rect x="27" y="18" width="1226" height="669" fill="none" stroke="#ffffff" stroke-width="4" opacity="0.94"/>

  <g filter="url(#phoneShadow)">
    <rect x="493" y="51" width="300" height="590" rx="47" fill="url(#bezelGradient)" stroke="#273247" stroke-width="3"/>
    <rect x="499" y="58" width="288" height="576" rx="41" fill="#050505"/>
    <rect x="512" y="68" width="256" height="564" rx="31" fill="#111111"/>

    <image
      x="500"
      y="68"
      width="280"
      height="564"
      clip-path="url(#screenClip)"
      href="https://images.example.com/abstract-phone-wallpaper-red-pink-cyan-soft-blur.jpg"
      preserveAspectRatio="xMidYMid slice"/>

    <rect x="500" y="68" width="280" height="564" rx="32" fill="url(#edgeLight)" opacity="0.55"/>
    <rect x="500" y="68" width="280" height="564" rx="32" fill="url(#glassSheen)" opacity="0.72"/>

    <path d="M571 68
             Q574 89 592 90
             L690 90
             Q708 90 712 68
             Z"
          fill="#050507"/>

    <rect x="491" y="128" width="4" height="28" rx="2" fill="#151923"/>
    <rect x="491" y="180" width="4" height="68" rx="2" fill="#151923"/>
    <rect x="789" y="193" width="4" height="78" rx="2" fill="#151923"/>

    <path d="M594 576
             C611 587 635 590 658 584
             C684 578 704 566 718 546"
          fill="none" stroke="#ffffff" stroke-width="3" opacity="0.82"/>
  </g>

  <text x="640" y="352"
        width="520"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="38"
        font-weight="300"
        letter-spacing="14"
        fill="#ffffff"
        filter="url(#titleGlow)">Hello,Future</text>

  <text x="640" y="575"
        width="210"
        text-anchor="middle"
        font-family="Microsoft YaHei, Segoe UI, sans-serif"
        font-size="42"
        font-weight="800"
        letter-spacing="-3"
        fill="#ffffff"
        transform="rotate(-8 640 575)">瞬视</text>

  <text x="640" y="606"
        width="150"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="8"
        font-weight="500"
        letter-spacing="2"
        fill="#ffffff"
        opacity="0.82">JBS · PPT STUDIO</text>

  <text x="705" y="603"
        width="22"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16"
        font-weight="700"
        fill="#ffffff">f</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use a medium-gray background; the effect depends on true black surrounding the illuminated product.
- ❌ Do not overcrowd the slide with feature bullets, icons, or charts; this is a reveal moment, not an information layout.
- ❌ Do not use `<mask>` for phone cutouts or screen reflections; use native rounded rectangles, paths, and image clipping instead.
- ❌ Do not apply filters to `<line>` elements for the border; use a plain stroked `<rect>` for reliable PowerPoint translation.
- ❌ Do not make the title bold or oversized; the hero is the product silhouette, while the text should feel airy and cinematic.

## Composition notes
- Keep the phone almost perfectly centered, occupying roughly 80% of slide height, with heavy black negative space on both sides.
- Use one crisp white inset frame to create a film-still feeling without competing with the product.
- Place the main title across the center of the phone, not above it; this creates depth and makes the device feel like the stage.
- Use saturated red, pink, cyan, and blue only inside the product screen so color feels precious and controlled.