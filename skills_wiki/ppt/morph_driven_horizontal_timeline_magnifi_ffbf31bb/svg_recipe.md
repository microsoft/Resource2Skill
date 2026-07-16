# SVG Recipe — Morph-Driven Horizontal Timeline Magnifier

## Visual mechanism
A long horizontal timeline stays quiet until one event reaches the center focal point: inactive milestones are small solid white dots with white-on-white labels, while the active milestone becomes a transparent outlined “magnifier” that reveals its year and detail text against the dark background. The hero asset above the active node scales up and glows, creating the impression that the timeline is sliding underneath a fixed lens during PowerPoint Morph.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark navy background
- 1× `<linearGradient>` for the background depth wash
- 2× `<radialGradient>` for the focal glow and hero accent halo
- 2× `<filter>` definitions for soft glow and lifted hero shadow
- 1× `<line>` for the full horizontal timeline axis
- 1× `<circle>` behind the active node to break the axis line cleanly
- 5× `<circle>` for timeline nodes: 4 inactive filled nodes and 1 active outlined magnifier node
- 5× `<text>` year labels, all white, with inactive labels hidden by white fills
- 1× `<image>` clipped into a rounded hero card above the active node
- 1× `<clipPath>` with rounded `<rect>` for the hero image crop
- 4× `<rect>` and 2× `<path>` for the active floating device/card illustration and decorative highlight shapes
- 3× `<path>` for cinematic background arcs, glints, and morph-motion trails
- 2× `<text>` blocks for active event title and explanatory copy

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0B1020"/>
      <stop offset="55%" stop-color="#10172B"/>
      <stop offset="100%" stop-color="#070A14"/>
    </linearGradient>

    <radialGradient id="focalGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#7C5CFF" stop-opacity="0.46"/>
      <stop offset="55%" stop-color="#3E8BFF" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#3E8BFF" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="heroHalo" cx="50%" cy="45%" r="55%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.36"/>
      <stop offset="45%" stop-color="#67D7FF" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#67D7FF" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="deviceGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFB347"/>
      <stop offset="50%" stop-color="#FF5F7E"/>
      <stop offset="100%" stop-color="#8257FF"/>
    </linearGradient>

    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>

    <filter id="heroShadow" x="-30%" y="-30%" width="160%" height="170%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="20"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="heroPhotoClip">
      <rect x="505" y="96" width="270" height="174" rx="32" ry="32"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <path d="M94 122 C242 48, 360 54, 480 132 S735 226, 918 118 S1195 72, 1268 154"
        fill="none" stroke="#FFFFFF" stroke-opacity="0.08" stroke-width="2"/>
  <path d="M190 640 C355 570, 525 612, 690 548 S1035 464, 1208 548"
        fill="none" stroke="#67D7FF" stroke-opacity="0.10" stroke-width="3"/>
  <path d="M835 172 C902 142, 964 160, 1015 214 C942 197, 892 214, 835 172"
        fill="#FFFFFF" fill-opacity="0.05"/>

  <ellipse cx="640" cy="324" rx="260" ry="190" fill="url(#focalGlow)" filter="url(#softGlow)"/>
  <ellipse cx="640" cy="210" rx="210" ry="145" fill="url(#heroHalo)" filter="url(#softGlow)"/>

  <image x="505" y="96" width="270" height="174"
         href="https://images.example.com/product-roadmap-2010-touchscreen-launch.jpg"
         clip-path="url(#heroPhotoClip)" opacity="0.92"/>

  <g id="heroAsset_2010" filter="url(#heroShadow)" transform="translate(0 0)">
    <rect x="536" y="124" width="208" height="302" rx="38" fill="#070A14" opacity="0.55"/>
    <rect x="548" y="108" width="184" height="300" rx="34" fill="url(#deviceGrad)"/>
    <rect x="569" y="150" width="142" height="196" rx="18" fill="#FFFFFF" opacity="0.88"/>
    <rect x="602" y="366" width="76" height="9" rx="4.5" fill="#FFFFFF" opacity="0.76"/>
    <path d="M586 181 C616 156, 663 160, 697 194 C668 190, 633 205, 609 229 C604 207, 596 192, 586 181"
          fill="#10172B" opacity="0.20"/>
    <path d="M584 260 C628 231, 682 244, 704 291 C664 276, 625 286, 596 316 C596 292, 592 275, 584 260"
          fill="#7C5CFF" opacity="0.20"/>
  </g>

  <text x="78" y="92" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="600" fill="#FFFFFF" opacity="0.92">
    Product evolution timeline
  </text>
  <text x="78" y="128" width="470" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#AAB5D1">
    The center event expands into a readable lens while surrounding milestones stay visually compressed.
  </text>

  <line x1="0" y1="504" x2="1280" y2="504" stroke="#FFFFFF" stroke-opacity="0.28" stroke-width="2"/>

  <circle cx="640" cy="504" r="88" fill="#10172B"/>
  <circle cx="420" cy="504" r="7" fill="#FFFFFF" opacity="0.36"/>
  <circle cx="860" cy="504" r="7" fill="#FFFFFF" opacity="0.36"/>
  <path d="M500 504 C545 494, 590 494, 628 504" fill="none" stroke="#FFFFFF" stroke-opacity="0.10" stroke-width="10" stroke-linecap="round"/>
  <path d="M652 504 C690 494, 735 494, 780 504" fill="none" stroke="#FFFFFF" stroke-opacity="0.10" stroke-width="10" stroke-linecap="round"/>

  <g id="timelineNodes">
    <circle id="node_1980" cx="200" cy="504" r="38" fill="#FFFFFF"/>
    <text x="162" y="514" width="76" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#FFFFFF">1980</text>

    <circle id="node_1990" cx="420" cy="504" r="38" fill="#FFFFFF"/>
    <text x="382" y="514" width="76" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#FFFFFF">1990</text>

    <circle id="node_2000" cx="640" cy="504" r="78" fill="none" stroke="#FFFFFF" stroke-width="4"/>
    <text x="562" y="496" width="156" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#FFFFFF">2010</text>
    <text x="558" y="528" width="164" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#DDE6FF">Touch-first platform</text>

    <circle id="node_2020" cx="860" cy="504" r="38" fill="#FFFFFF"/>
    <text x="822" y="514" width="76" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#FFFFFF">2020</text>

    <circle id="node_2030" cx="1080" cy="504" r="38" fill="#FFFFFF"/>
    <text x="1042" y="514" width="76" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#FFFFFF">2030</text>
  </g>

  <text x="460" y="615" width="360" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" fill="#FFFFFF">
    Active milestone becomes the story frame
  </text>
  <text x="400" y="646" width="480" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#AAB5D1">
    Duplicate this slide, shift every node group left by one interval, then change which circle has transparent fill and the enlarged hero asset.
  </text>
</svg>
```

## Avoid in this skill
- ❌ SVG animation elements such as `<animate>` or `<animateTransform>`; use PowerPoint Morph between duplicated slides instead.
- ❌ `<mask>` to hide the timeline under the active circle; use a background-colored `<circle>` behind the magnifier.
- ❌ `clip-path` on circles, paths, or groups; only clip the `<image>` hero card.
- ❌ `marker-end` arrows on timeline paths; this technique should read as a continuous axis, not a flowchart.
- ❌ Changing object IDs/names between Morph states; if PPT object names are not stable, the timeline will fade instead of sliding smoothly.

## Composition notes
- Place the timeline on the lower third, around `y=500`, leaving the upper half for the enlarged hero asset and focal glow.
- Keep the active node centered; create Morph states by sliding the entire timeline horizontally while swapping the active styling.
- Use fill inversion deliberately: inactive nodes are white circles with white text, while the active node is `fill="none"` with a white stroke.
- For a premium keynote feel, pair the simple axis with cinematic depth: dark gradient background, subtle motion trails, glow behind the lens, and a lifted hero card above the active event.