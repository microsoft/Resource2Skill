# SVG Recipe — Two Object Comparison

## Visual mechanism
Create a premium split-screen comparison by placing two equally weighted object/photo cards on the left and right, separated by a slim central “VS / transition” axis. Each object gets its own clipped image, label stack, accent color, and subtle depth so the audience reads the slide as a direct side-by-side contrast.

## SVG primitives needed
- 1× `<rect>` full-slide gradient background
- 2× `<path>` organic accent blobs behind the comparison cards
- 2× `<rect>` large rounded cards with soft shadow
- 2× `<image>` square object/photo slots clipped by rounded-corner `<clipPath>`
- 2× `<rect>` subtle image frames around the clipped photos
- 2× `<rect>` small status pills above each object
- 1× `<line>` dashed vertical divider for the comparison axis
- 1× `<circle>` central “VS” badge with glow
- 2× `<path>` chevron arrows pointing from each object toward the center
- 6× `<text>` elements for headline, labels, short descriptions, and center caption
- 3× `<linearGradient>` fills for background and card accents
- 1× `<radialGradient>` for the center badge highlight
- 2× `<filter>` definitions for card shadow and center glow
- 2× `<clipPath>` definitions using rounded `<rect>` shapes for editable image crops

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#F7FAFF"/>
      <stop offset="52%" stop-color="#EEF4FF"/>
      <stop offset="100%" stop-color="#F9F6F1"/>
    </linearGradient>

    <linearGradient id="leftAccent" x1="90" y1="130" x2="520" y2="610">
      <stop offset="0%" stop-color="#7C3AED" stop-opacity="0.34"/>
      <stop offset="100%" stop-color="#06B6D4" stop-opacity="0.12"/>
    </linearGradient>

    <linearGradient id="rightAccent" x1="760" y1="130" x2="1190" y2="610">
      <stop offset="0%" stop-color="#F97316" stop-opacity="0.32"/>
      <stop offset="100%" stop-color="#22C55E" stop-opacity="0.12"/>
    </linearGradient>

    <radialGradient id="vsRadial" cx="50%" cy="38%" r="68%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="48%" stop-color="#F4F7FF"/>
      <stop offset="100%" stop-color="#DDE7FF"/>
    </radialGradient>

    <filter id="shadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="clipLeftPhoto">
      <rect x="145" y="210" width="360" height="330" rx="34" ry="34"/>
    </clipPath>

    <clipPath id="clipRightPhoto">
      <rect x="775" y="210" width="360" height="330" rx="34" ry="34"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>

  <path d="M104 246 C135 165, 225 123, 323 137 C421 151, 519 221, 516 334 C513 446, 440 572, 304 598 C168 624, 82 556, 70 442 C58 328, 73 327, 104 246 Z"
        fill="url(#leftAccent)"/>
  <path d="M774 273 C819 160, 926 128, 1033 154 C1140 180, 1201 280, 1181 392 C1161 504, 1072 602, 947 599 C822 596, 732 508, 725 407 C718 306, 729 386, 774 273 Z"
        fill="url(#rightAccent)"/>

  <text x="640" y="72" width="780" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="34" font-weight="700" fill="#111827">
    Two-object comparison
  </text>
  <text x="640" y="108" width="620" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" fill="#6B7280">
    Contrast the current state with the target state using balanced, image-led cards
  </text>

  <rect x="110" y="165" width="430" height="465" rx="42" fill="#FFFFFF" filter="url(#shadow)"/>
  <rect x="740" y="165" width="430" height="465" rx="42" fill="#FFFFFF" filter="url(#shadow)"/>

  <rect x="145" y="210" width="360" height="330" rx="34" fill="#EEF2FF"/>
  <image x="145" y="210" width="360" height="330" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/photo-current-manual-workflow-on-desk.jpg"
         clip-path="url(#clipLeftPhoto)"/>
  <rect x="145" y="210" width="360" height="330" rx="34" fill="none" stroke="#FFFFFF" stroke-width="5"/>

  <rect x="775" y="210" width="360" height="330" rx="34" fill="#FFF7ED"/>
  <image x="775" y="210" width="360" height="330" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/photo-future-ai-automation-dashboard.jpg"
         clip-path="url(#clipRightPhoto)"/>
  <rect x="775" y="210" width="360" height="330" rx="34" fill="none" stroke="#FFFFFF" stroke-width="5"/>

  <rect x="145" y="185" width="148" height="34" rx="17" fill="#EEF2FF" stroke="#C7D2FE"/>
  <text x="219" y="207" width="130" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="700" fill="#4F46E5">
    CURRENT STATE
  </text>

  <rect x="775" y="185" width="140" height="34" rx="17" fill="#FFF7ED" stroke="#FED7AA"/>
  <text x="845" y="207" width="124" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="700" fill="#EA580C">
    TARGET STATE
  </text>

  <text x="325" y="580" width="330" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="700" fill="#111827">
    Manual operations
  </text>
  <text x="325" y="608" width="350" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#6B7280">
    Slower handoffs, scattered tools, higher coordination cost
  </text>

  <text x="955" y="580" width="330" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="700" fill="#111827">
    AI-assisted flow
  </text>
  <text x="955" y="608" width="350" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#6B7280">
    Automated routing, live insight, fewer operational delays
  </text>

  <line x1="640" y1="165" x2="640" y2="630" stroke="#CBD5E1" stroke-width="2" stroke-dasharray="8 12"/>

  <path d="M577 344 L614 318 L614 335 L633 335 L633 353 L614 353 L614 370 Z"
        fill="#EEF2FF" stroke="#A5B4FC" stroke-width="2"/>
  <path d="M703 344 L666 318 L666 335 L647 335 L647 353 L666 353 L666 370 Z"
        fill="#FFF7ED" stroke="#FDBA74" stroke-width="2"/>

  <circle cx="640" cy="344" r="54" fill="url(#vsRadial)" stroke="#FFFFFF" stroke-width="6" filter="url(#glow)"/>
  <text x="640" y="356" width="92" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="27" font-weight="800" fill="#1F2937">
    VS
  </text>
  <text x="640" y="425" width="150" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600" fill="#64748B">
    compare impact
  </text>

  <circle cx="104" cy="120" r="5" fill="#A78BFA" opacity="0.75"/>
  <circle cx="1178" cy="132" r="6" fill="#FDBA74" opacity="0.75"/>
  <circle cx="600" cy="636" r="4" fill="#94A3B8" opacity="0.55"/>
  <circle cx="680" cy="636" r="4" fill="#94A3B8" opacity="0.55"/>
</svg>
```

## Avoid in this skill
- ❌ Mirroring the two cards with `<use href="#...">`; duplicate the shapes explicitly so PowerPoint keeps them editable.
- ❌ Applying `clip-path` to decorative overlays or card rectangles; use clipping only on `<image>` elements and draw matching rounded frames separately.
- ❌ Using `marker-end` on a `<path>` for the center arrows; build chevrons as editable `<path>` shapes or use `<line>` arrows only.
- ❌ Letting labels auto-size; every `<text>` needs a clear `width` so PowerPoint does not reflow the comparison labels unexpectedly.
- ❌ Overcrowding the middle axis with detailed text; the center should clarify the contrast, not compete with the two objects.

## Composition notes
- Keep the left and right cards the same size and aligned to the same baseline; visual equality makes the comparison feel fair.
- Reserve the top 15–18% of the slide for a short headline and subtitle, then let the two object images dominate the slide.
- Use one cool accent color on the left and one warm accent color on the right to create instant separation without adding clutter.
- The central “VS” badge should be small but high-contrast; it acts as a reading hinge between the two objects.