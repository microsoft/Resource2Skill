# SVG Recipe — Asymmetric Color Block Layout

## Visual mechanism
A bright, solid color block acts as an off-center visual anchor, while content sits in spacious white zones aligned to a clean grid. The asymmetry creates energy and brand presence without sacrificing readability.

## SVG primitives needed
- 1× `<rect>` for the white slide background
- 2× large `<rect>` for the cyan bottom brand block and left title rail
- 1× `<image>` clipped into an angled right-side hero-photo panel
- 1× `<clipPath>` with a `<path>` to crop the hero photo into an asymmetric wedge
- 1× translucent `<path>` for a subtle angled overlay that connects the photo to the color block
- 3× white `<rect>` cards for modular content blocks
- 3× small cyan `<rect>` accent squares paired with section labels
- 6× small `<circle>` bullets for concise supporting points
- Multiple `<text>` elements with explicit `width` for title, metadata, section labels, and body copy
- 1× `<filter id="softShadow">` applied to cards and title badge for depth
- 1× `<linearGradient>` for a premium, slightly dimensional cyan block
- 1× `<radialGradient>` for a soft background highlight

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="cyanBlock" x1="0" y1="520" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#4FE6DE"/>
      <stop offset="0.62" stop-color="#35D7D4"/>
      <stop offset="1" stop-color="#22C7D7"/>
    </linearGradient>

    <radialGradient id="quietGlow" cx="35%" cy="25%" r="70%">
      <stop offset="0" stop-color="#EFFFFE"/>
      <stop offset="0.55" stop-color="#FFFFFF"/>
      <stop offset="1" stop-color="#F8FAFB"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="12" result="blur"/>
      <feColorMatrix in="blur" type="matrix"
        values="0 0 0 0 0
                0 0 0 0 0.18
                0 0 0 0 0.20
                0 0 0 0.18 0" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="photoWedge">
      <path d="M760 0 L1280 0 L1280 515 L910 585 L760 440 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#quietGlow)"/>

  <image x="720" y="0" width="600" height="590"
    href="https://images.example.com/modern-network-server-room-with-blue-light.jpg"
    clip-path="url(#photoWedge)" preserveAspectRatio="xMidYMid slice"/>

  <path d="M820 0 L1280 0 L1280 160 C1110 178 960 210 850 280 Z"
    fill="#FFFFFF" opacity="0.22"/>

  <rect x="0" y="520" width="1280" height="200" fill="url(#cyanBlock)"/>
  <rect x="68" y="86" width="14" height="246" rx="7" fill="#4FE6DE"/>

  <rect x="94" y="86" width="170" height="42" rx="21" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="119" y="113" width="140" font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="13" font-weight="700" letter-spacing="2" fill="#2A3438">TECH BRIEF</text>

  <text x="94" y="190" width="560" font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="58" font-weight="800" letter-spacing="-1.5" fill="#071013">
    ASYMMETRIC
  </text>
  <text x="94" y="252" width="585" font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="58" font-weight="800" letter-spacing="-1.5" fill="#071013">
    COLOR BLOCK
  </text>
  <text x="98" y="306" width="520" font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="18" font-weight="500" fill="#5F6B70">
    A structured presentation layout for executive, academic, and product storytelling.
  </text>

  <text x="1020" y="608" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="13" font-weight="800" letter-spacing="2.5" fill="#083236" opacity="0.9">
    07 JULY 2026
  </text>

  <rect x="86" y="492" width="326" height="142" rx="20" fill="#FFFFFF" filter="url(#softShadow)"/>
  <rect x="112" y="520" width="18" height="18" rx="3" fill="#4FE6DE"/>
  <text x="146" y="535" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="18" font-weight="800" fill="#071013">SINGLE ANCHOR</text>
  <circle cx="120" cy="566" r="4" fill="#4FE6DE"/>
  <text x="138" y="572" width="230" font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="14" fill="#465257">One bold block controls visual hierarchy.</text>
  <circle cx="120" cy="596" r="4" fill="#4FE6DE"/>
  <text x="138" y="602" width="238" font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="14" fill="#465257">White space keeps the message crisp.</text>

  <rect x="476" y="458" width="326" height="176" rx="20" fill="#FFFFFF" filter="url(#softShadow)"/>
  <rect x="502" y="486" width="18" height="18" rx="3" fill="#4FE6DE"/>
  <text x="536" y="501" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="18" font-weight="800" fill="#071013">GRID DISCIPLINE</text>
  <circle cx="510" cy="534" r="4" fill="#4FE6DE"/>
  <text x="528" y="540" width="232" font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="14" fill="#465257">Align every heading, card, and label.</text>
  <circle cx="510" cy="566" r="4" fill="#4FE6DE"/>
  <text x="528" y="572" width="235" font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="14" fill="#465257">Use offsets to make the slide feel custom.</text>

  <rect x="866" y="492" width="326" height="142" rx="20" fill="#FFFFFF" filter="url(#softShadow)"/>
  <rect x="892" y="520" width="18" height="18" rx="3" fill="#4FE6DE"/>
  <text x="926" y="535" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="18" font-weight="800" fill="#071013">BRANDED RHYTHM</text>
  <circle cx="900" cy="566" r="4" fill="#4FE6DE"/>
  <text x="918" y="572" width="230" font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="14" fill="#465257">Repeat the accent sparingly for cohesion.</text>
  <circle cx="900" cy="596" r="4" fill="#4FE6DE"/>
  <text x="918" y="602" width="230" font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="14" fill="#465257">Let contrast do most of the work.</text>
</svg>
```

## Avoid in this skill
- ❌ Centering every major object; the technique depends on deliberate imbalance.
- ❌ Filling the entire slide with color blocks; keep one dominant accent zone and plenty of white space.
- ❌ Using more than one saturated accent color unless the brand system requires it.
- ❌ Applying `clip-path` to text or rectangles; use clipping only for the hero `<image>`.
- ❌ Dense paragraphs inside the cards; this layout works best with short labels and compact supporting lines.

## Composition notes
- Reserve the left 50–55% for headline and explanatory copy; keep it mostly white.
- Use the bottom 25–30% as the dominant color block, then let cards overlap it for depth.
- Place the photo or secondary visual on the right edge so it counterbalances the left text mass.
- Repeat the accent color in small squares, bullets, or rails to create rhythm without clutter.