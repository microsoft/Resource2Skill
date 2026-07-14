# SVG Recipe — Blueprint Grid & Brand Accent Framework

## Visual mechanism
A white executive canvas is turned into a precise “architectural blueprint” surface with pale dashed grid lines, then locked down by bold brand-color anchor bars at the top and bottom. Content, photos, data cards, and offset L-shaped corner marks snap to the grid, creating a technical, structured, premium presentation frame.

## SVG primitives needed
- 1× `<rect>` for the white slide background
- 2× `<path>` for the dashed blueprint grid: one minor grid layer and one slightly stronger major grid layer
- 2× `<rect>` for full-width top and bottom brand anchor bars
- 1× `<linearGradient>` for a richer orange brand accent fill
- 1× `<filter id="softShadow">` applied to photo/card backing rectangles
- 1× `<clipPath>` with a rounded `<rect>` applied to the hero/profile `<image>`
- 1× `<image>` for the clipped portrait, product, architecture, or technical workspace photo
- 4× `<path>` for offset L-shaped orange corner accents around the image
- 4× `<rect>` for white content/data cards and accent strips
- 1× `<path>` for a small editable trend/chart line
- Multiple `<text>` elements with explicit `width` attributes for title, metadata, body copy, and KPI labels

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="brandOrange" x1="0" y1="0" x2="1280" y2="0">
      <stop offset="0%" stop-color="#F05A00"/>
      <stop offset="55%" stop-color="#FF7A18"/>
      <stop offset="100%" stop-color="#F05A00"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="12"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="photoClip" clipPathUnits="userSpaceOnUse">
      <rect x="118" y="128" width="424" height="302" rx="4"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <!-- blueprint grid: minor lines -->
  <path d="M40 0 V720 M80 0 V720 M120 0 V720 M160 0 V720 M200 0 V720 M240 0 V720 M280 0 V720 M320 0 V720 M360 0 V720 M400 0 V720 M440 0 V720 M480 0 V720 M520 0 V720 M560 0 V720 M600 0 V720 M640 0 V720 M680 0 V720 M720 0 V720 M760 0 V720 M800 0 V720 M840 0 V720 M880 0 V720 M920 0 V720 M960 0 V720 M1000 0 V720 M1040 0 V720 M1080 0 V720 M1120 0 V720 M1160 0 V720 M1200 0 V720 M1240 0 V720"
        fill="none" stroke="#E9E9E9" stroke-width="1" stroke-dasharray="5 8"/>
  <path d="M0 40 H1280 M0 80 H1280 M0 120 H1280 M0 160 H1280 M0 200 H1280 M0 240 H1280 M0 280 H1280 M0 320 H1280 M0 360 H1280 M0 400 H1280 M0 440 H1280 M0 480 H1280 M0 520 H1280 M0 560 H1280 M0 600 H1280 M0 640 H1280 M0 680 H1280"
        fill="none" stroke="#E9E9E9" stroke-width="1" stroke-dasharray="5 8"/>

  <!-- blueprint grid: stronger 160px structural lines -->
  <path d="M160 0 V720 M320 0 V720 M480 0 V720 M640 0 V720 M800 0 V720 M960 0 V720 M1120 0 V720"
        fill="none" stroke="#DADADA" stroke-width="1.2" stroke-dasharray="8 10"/>
  <path d="M0 160 H1280 M0 320 H1280 M0 480 H1280 M0 640 H1280"
        fill="none" stroke="#DADADA" stroke-width="1.2" stroke-dasharray="8 10"/>

  <!-- brand anchors -->
  <rect x="0" y="0" width="1280" height="42" fill="url(#brandOrange)"/>
  <rect x="0" y="700" width="1280" height="20" fill="url(#brandOrange)"/>

  <!-- photo block -->
  <rect x="118" y="128" width="424" height="302" rx="4" fill="#FFFFFF" filter="url(#softShadow)" opacity="0.92"/>
  <image x="118" y="128" width="424" height="302"
         href="https://images.example.com/portrait-engineer-in-modern-technical-studio.jpg"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#photoClip)"/>

  <!-- offset drafting-style corner marks -->
  <path d="M94 112 H178 M94 112 V196" fill="none" stroke="#F05A00" stroke-width="8" stroke-linecap="square"/>
  <path d="M566 112 H482 M566 112 V196" fill="none" stroke="#F05A00" stroke-width="8" stroke-linecap="square"/>
  <path d="M94 446 H178 M94 446 V362" fill="none" stroke="#F05A00" stroke-width="8" stroke-linecap="square"/>
  <path d="M566 446 H482 M566 446 V362" fill="none" stroke="#F05A00" stroke-width="8" stroke-linecap="square"/>

  <!-- title and metadata -->
  <text x="620" y="150" width="500" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="58" font-weight="700" fill="#282828">Andrew Doe</text>
  <text x="624" y="195" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" letter-spacing="2.5" fill="#F05A00" font-weight="700">SYSTEMS ARCHITECT · TECHNICAL PORTFOLIO</text>

  <text x="624" y="238" width="470" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="19" fill="#646464">
    <tspan fill="#F05A00" font-weight="700">Age:</tspan>
    <tspan> 34</tspan>
    <tspan dx="32" fill="#F05A00" font-weight="700">Nationality:</tspan>
    <tspan> Canadian</tspan>
  </text>
  <text x="624" y="272" width="470" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="19" fill="#646464">
    <tspan fill="#F05A00" font-weight="700">Focus:</tspan>
    <tspan> infrastructure, product systems, delivery governance</tspan>
  </text>

  <text x="624" y="326" width="500" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#282828">Blueprint for scalable execution</text>
  <text x="624" y="365" width="500" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" fill="#666666">
    <tspan x="624" dy="0">A rigorous planning framework for translating complex</tspan>
    <tspan x="624" dy="28">technical objectives into measurable workstreams, clear</tspan>
    <tspan x="624" dy="28">ownership, and board-ready operating cadence.</tspan>
  </text>

  <!-- aligned KPI cards -->
  <rect x="620" y="468" width="158" height="104" rx="3" fill="#FFFFFF" filter="url(#softShadow)"/>
  <rect x="620" y="468" width="8" height="104" fill="#F05A00"/>
  <text x="644" y="505" width="110" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#F05A00" font-weight="700">READINESS</text>
  <text x="644" y="548" width="110" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="40" fill="#282828" font-weight="700">92%</text>

  <rect x="810" y="468" width="158" height="104" rx="3" fill="#FFFFFF" filter="url(#softShadow)"/>
  <rect x="810" y="468" width="8" height="104" fill="#F05A00"/>
  <text x="834" y="505" width="110" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#F05A00" font-weight="700">MILESTONES</text>
  <text x="834" y="548" width="110" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="40" fill="#282828" font-weight="700">18</text>

  <rect x="1000" y="468" width="158" height="104" rx="3" fill="#FFFFFF" filter="url(#softShadow)"/>
  <rect x="1000" y="468" width="8" height="104" fill="#F05A00"/>
  <text x="1024" y="505" width="116" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#F05A00" font-weight="700">RISK DELTA</text>
  <text x="1024" y="548" width="116" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="40" fill="#282828" font-weight="700">−24</text>

  <!-- small editable trend strip beneath photo -->
  <rect x="118" y="504" width="424" height="84" rx="3" fill="#FFFFFF" opacity="0.84"/>
  <text x="138" y="535" width="220" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#F05A00" font-weight="700" letter-spacing="1.5">DELIVERY CONFIDENCE</text>
  <path d="M138 566 C178 548 214 558 252 532 S334 520 376 498 S448 508 522 486"
        fill="none" stroke="#F05A00" stroke-width="4" stroke-linecap="round"/>
  <path d="M138 566 H522" fill="none" stroke="#BDBDBD" stroke-width="1" stroke-dasharray="6 7"/>
</svg>
```

## Avoid in this skill
- ❌ SVG `<pattern>` fills for the grid; use editable dashed `<path>` or `<line>` strokes instead.
- ❌ Applying `clip-path` to decorative rectangles or groups; only apply clipping to the `<image>`.
- ❌ Do not place `filter` on grid `<line>` or `<path>` strokes; keep shadows on card/photo backing `<rect>` elements.
- ❌ Avoid dense hundreds-of-line SVG grids if the slide needs to stay easy to edit; use multi-segment paths for grid layers.
- ❌ Avoid centered/free-floating content that ignores the grid; the whole aesthetic depends on strict alignment.

## Composition notes
- Keep top and bottom brand bars full-bleed; make the top bar visibly thicker than the bottom bar to create a strong executive frame.
- Place the hero image on one side and the title/body/data stack on the other, with both snapped to the same grid rhythm.
- Use orange sparingly but decisively: anchor bars, labels, image corner marks, KPI strips, and chart highlight strokes.
- Let the pale grid fill the negative space; avoid overfilling the canvas so the “blueprint” precision remains visible.