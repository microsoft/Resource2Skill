# SVG Recipe — Hero Overlap Block

## Visual mechanism
A wide, saturated horizontal block anchors the slide while a portrait hero image overlaps its right edge, creating an editorial “cover story” composition. The headline and subhead sit inside the block, with subtle shadows, gradients, and decorative geometry adding premium depth without clutter.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 1× `<rect>` for the large horizontal hero text block
- 2× `<rect>` for image backing cards / highlight frames
- 1× `<image>` for the portrait hero photo, clipped to a rounded rectangle
- 1× `<clipPath>` with rounded `<rect>` for the portrait crop
- 3× `<path>` for organic accent shapes and angular editorial decorations
- 3× `<circle>` / `<ellipse>` for soft background and block accents
- 2× `<line>` for small editorial divider rules
- 4× `<text>` elements with explicit `width` attributes for eyebrow, headline, subhead, and caption
- 2× `<linearGradient>` for premium block and image-frame fills
- 1× `<radialGradient>` for the soft background glow
- 2× `<filter>` definitions for drop shadow and soft glow applied to editable shapes

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="blockGradient" x1="80" y1="190" x2="940" y2="520" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#123C69"/>
      <stop offset="0.52" stop-color="#1E5A7A"/>
      <stop offset="1" stop-color="#0B253F"/>
    </linearGradient>

    <linearGradient id="frameGradient" x1="760" y1="90" x2="1170" y2="650" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#F8D58A"/>
      <stop offset="0.45" stop-color="#F29F4B"/>
      <stop offset="1" stop-color="#D94F3D"/>
    </linearGradient>

    <radialGradient id="bgGlow" cx="72%" cy="45%" r="58%">
      <stop offset="0" stop-color="#FFE2BA" stop-opacity="0.9"/>
      <stop offset="0.45" stop-color="#F6F1E8" stop-opacity="0.72"/>
      <stop offset="1" stop-color="#EEF2F6" stop-opacity="0"/>
    </radialGradient>

    <filter id="shadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="16"/>
    </filter>

    <clipPath id="portraitClip">
      <rect x="790" y="94" width="348" height="532" rx="34" ry="34"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F5F0E8"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGlow)"/>

  <path d="M1010 44 C1112 52 1194 118 1218 214 C1249 338 1166 444 1050 430 C950 418 889 338 900 236 C911 132 936 38 1010 44 Z"
        fill="#F7B55E" opacity="0.32" filter="url(#softGlow)"/>
  <circle cx="1020" cy="586" r="96" fill="#123C69" opacity="0.08"/>
  <ellipse cx="226" cy="122" rx="142" ry="54" fill="#D94F3D" opacity="0.10"/>

  <rect x="86" y="204" width="858" height="316" rx="30" ry="30"
        fill="url(#blockGradient)" filter="url(#shadow)"/>

  <path d="M86 204 H390 C335 260 319 349 358 520 H86 Z"
        fill="#FFFFFF" opacity="0.08"/>
  <path d="M782 204 H944 V520 H690 C740 454 762 345 782 204 Z"
        fill="#F8D58A" opacity="0.18"/>

  <circle cx="154" cy="466" r="5" fill="#F8D58A"/>
  <circle cx="178" cy="466" r="5" fill="#F8D58A" opacity="0.62"/>
  <circle cx="202" cy="466" r="5" fill="#F8D58A" opacity="0.34"/>

  <line x1="138" y1="278" x2="248" y2="278" stroke="#F8D58A" stroke-width="4"/>
  <line x1="138" y1="492" x2="420" y2="492" stroke="#FFFFFF" stroke-width="1.5" opacity="0.28"/>

  <text x="138" y="262" width="430" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" letter-spacing="3" fill="#F8D58A">
    EXECUTIVE PROFILE
  </text>

  <text x="136" y="345" width="560" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="58" font-weight="800" fill="#FFFFFF">
    <tspan x="136" dy="0">Designing the</tspan>
    <tspan x="136" dy="66">Next Growth Era</tspan>
  </text>

  <text x="140" y="425" width="520" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="400" fill="#DDEAF2">
    A bold leadership narrative for teams moving from incremental gains to category-defining momentum.
  </text>

  <rect x="766" y="78" width="396" height="568" rx="42" ry="42"
        fill="url(#frameGradient)" opacity="0.98" filter="url(#shadow)"/>
  <rect x="790" y="94" width="348" height="532" rx="34" ry="34"
        fill="#FFFFFF" opacity="0.92"/>

  <image x="790" y="94" width="348" height="532" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#portraitClip)"
         href="https://images.example.com/portrait-confident-executive-warm-studio-light.jpg"/>

  <path d="M1106 116 L1162 116 L1162 172" fill="none" stroke="#FFFFFF" stroke-width="5" opacity="0.72"/>
  <path d="M818 604 L818 550 L872 604 Z" fill="#FFFFFF" opacity="0.82"/>

  <rect x="820" y="560" width="250" height="52" rx="18" ry="18" fill="#0B253F" opacity="0.86"/>
  <text x="842" y="593" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="700" fill="#FFFFFF">
    Maya Chen · CEO
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using a simple side-by-side image and text grid; the visual impact depends on real overlap between the block and portrait.
- ❌ Applying `clip-path` to decorative shapes or text; use clipping only on the `<image>` crop for reliable PowerPoint translation.
- ❌ Letting the portrait float without a backing card or shadow; it will lose the “out-of-bounds editorial cover” effect.
- ❌ Overfilling the block with bullets; this shell works best with one strong headline and a short supporting sentence.

## Composition notes
- Keep the text block wide and low-to-mid on the slide, occupying roughly the left two-thirds of the canvas.
- Let the portrait break the right edge of the block and extend above and below it to create depth.
- Use a restrained palette: one deep corporate base color, one warm accent, and white typography.
- Preserve negative space in the upper-left and lower-right corners so the overlap remains the main visual focus.