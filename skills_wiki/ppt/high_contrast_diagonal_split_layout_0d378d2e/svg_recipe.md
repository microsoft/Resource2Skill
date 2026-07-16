# SVG Recipe — High-Contrast Diagonal Split Layout

## Visual mechanism
A sharp diagonal split divides the slide into a dark brand zone and a bright information zone, with a saturated accent band emphasizing the slant. The layout feels dynamic because every major element aligns to, echoes, or counterbalances the diagonal boundary.

## SVG primitives needed
- 1× `<rect>` for the full white slide background
- 2× `<path>` for the dark left trapezoid and red diagonal accent band
- 3× `<path>` for decorative diagonal red/black slivers that reinforce motion
- 1× `<path>` for a large accent hexagon with thick white stroke
- 4× `<rect>` for red icon tiles on the right-side information list
- 4× `<path>` for simple white line icons inside the icon tiles
- 8× `<text>` for brand title, subtitle, section label, and contact detail rows
- 5× `<line>` for dividers and subtle diagonal rhythm marks
- 1× `<linearGradient id="accentGrad">` for richer red accent fills
- 1× `<filter id="softShadow">` applied to the hexagon and icon tiles
- 1× `<filter id="redGlow">` applied to the diagonal accent band for premium depth

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="accentGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ff3b45"/>
      <stop offset="55%" stop-color="#dc1428"/>
      <stop offset="100%" stop-color="#a90018"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="redGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="8" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Clean white information field -->
  <rect x="0" y="0" width="1280" height="720" fill="#ffffff"/>

  <!-- Left high-contrast diagonal field -->
  <path d="M 0 0 L 560 0 L 390 720 L 0 720 Z" fill="#141414"/>
  <path d="M 558 0 L 674 0 L 504 720 L 390 720 Z" fill="url(#accentGrad)" filter="url(#redGlow)"/>

  <!-- Secondary diagonal accents -->
  <path d="M 615 0 L 638 0 L 468 720 L 445 720 Z" fill="#ffffff" opacity="0.18"/>
  <path d="M 1060 0 L 1280 0 L 1280 34 L 1048 34 Z" fill="#141414"/>
  <path d="M 1114 34 L 1280 34 L 1280 58 L 1108 58 Z" fill="#dc1428"/>
  <line x1="705" y1="625" x2="960" y2="625" stroke="#e7e7e7" stroke-width="3"/>
  <line x1="745" y1="646" x2="1040" y2="646" stroke="#f0f0f0" stroke-width="2"/>

  <!-- Brand-side geometric anchor -->
  <path d="M 280 110 L 355 153 L 355 239 L 280 282 L 205 239 L 205 153 Z"
        fill="url(#accentGrad)" stroke="#ffffff" stroke-width="8" filter="url(#softShadow)"/>
  <path d="M 280 145 L 323 170 L 323 220 L 280 245 L 237 220 L 237 170 Z"
        fill="none" stroke="#ffffff" stroke-width="4" opacity="0.72"/>
  <line x1="230" y1="196" x2="330" y2="196" stroke="#ffffff" stroke-width="4" opacity="0.65"/>
  <line x1="280" y1="146" x2="280" y2="246" stroke="#ffffff" stroke-width="4" opacity="0.65"/>

  <!-- Left text block -->
  <text x="80" y="382" width="390" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="56" font-weight="800" fill="#ffffff" letter-spacing="1.5">
    NOVA
  </text>
  <text x="80" y="438" width="390" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="50" font-weight="800" fill="#ffffff" letter-spacing="1.5">
    SYSTEMS
  </text>
  <text x="82" y="486" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="25" font-weight="400" fill="#d7d7d7">
    Strategic Technology Studio
  </text>
  <line x1="82" y1="526" x2="350" y2="526" stroke="#dc1428" stroke-width="8"/>

  <!-- Right-side header -->
  <text x="755" y="138" width="400" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="46" font-weight="800" fill="#141414" letter-spacing="1">
    CONTACT US
  </text>
  <text x="758" y="176" width="410" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="500" fill="#777777">
    Fast response for enterprise partnerships
  </text>

  <!-- Contact row 1 -->
  <rect x="745" y="226" width="62" height="62" rx="12" fill="url(#accentGrad)" filter="url(#softShadow)"/>
  <path d="M 769 247 C 774 240 785 241 790 248 C 794 254 791 262 783 266 C 789 276 797 282 807 286 C 805 295 798 300 790 297 C 773 291 761 279 755 262 C 752 255 755 250 769 247 Z"
        fill="#ffffff"/>
  <text x="832" y="254" width="320" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" fill="#141414">Phone</text>
  <text x="832" y="281" width="340" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="600" fill="#333333">+1 415 908 2234</text>

  <!-- Contact row 2 -->
  <rect x="745" y="324" width="62" height="62" rx="12" fill="url(#accentGrad)" filter="url(#softShadow)"/>
  <path d="M 760 342 L 792 342 C 799 342 804 347 804 354 L 804 369 C 804 376 799 381 792 381 L 760 381 C 753 381 748 376 748 369 L 748 354 C 748 347 753 342 760 342 Z M 754 350 L 776 365 L 798 350"
        fill="none" stroke="#ffffff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="832" y="352" width="320" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" fill="#141414">Email</text>
  <text x="832" y="379" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="600" fill="#333333">hello@novasystems.co</text>

  <!-- Contact row 3 -->
  <rect x="745" y="422" width="62" height="62" rx="12" fill="url(#accentGrad)" filter="url(#softShadow)"/>
  <path d="M 776 438 C 762 438 751 449 751 463 C 751 481 776 496 776 496 C 776 496 801 481 801 463 C 801 449 790 438 776 438 Z M 776 453 C 782 453 786 457 786 463 C 786 469 782 473 776 473 C 770 473 766 469 766 463 C 766 457 770 453 776 453 Z"
        fill="#ffffff"/>
  <text x="832" y="450" width="320" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" fill="#141414">Office</text>
  <text x="832" y="477" width="390" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="600" fill="#333333">88 Market Street, San Francisco</text>

  <!-- Contact row 4 -->
  <rect x="745" y="520" width="62" height="62" rx="12" fill="url(#accentGrad)" filter="url(#softShadow)"/>
  <path d="M 776 535 C 789 535 800 546 800 559 C 800 572 789 583 776 583 C 763 583 752 572 752 559 C 752 546 763 535 776 535 Z M 752 559 L 800 559 M 776 535 C 768 543 764 551 764 559 C 764 567 768 575 776 583 M 776 535 C 784 543 788 551 788 559 C 788 567 784 575 776 583"
        fill="none" stroke="#ffffff" stroke-width="4" stroke-linecap="round"/>
  <text x="832" y="548" width="320" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" fill="#141414">Website</text>
  <text x="832" y="575" width="340" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="600" fill="#333333">www.novasystems.co</text>
</svg>
```

## Avoid in this skill
- ❌ Using only two rectangles for the background; the diagonal split must be real vector geometry made from `<path>` shapes.
- ❌ Applying `clip-path` to the dark or accent polygons; clipping non-image shapes will not translate reliably.
- ❌ Using `marker-end` for decorative arrows along the diagonal; use explicit `<line>` or `<path>` geometry instead.
- ❌ Placing right-side text too close to the red band; the information zone needs clean white breathing room.
- ❌ Low-contrast accent colors such as muted orange or gray-red; this layout depends on a bold, high-saturation accent.

## Composition notes
- Keep the dark brand zone around 40–45% of the slide width, with the red diagonal band acting as a visual hinge between brand and details.
- Place the largest brand text low-left, not centered vertically; this makes the upper-left hexagon feel like a deliberate anchor instead of decoration.
- Align right-side icon tiles in a strict vertical column, with labels and values sharing one consistent x-position.
- Use red sparingly outside the main band: icon tiles, one divider, and small diagonal accents are enough to create rhythm without clutter.