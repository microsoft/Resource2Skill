# SVG Recipe — Vibrant Modular Grid Pattern

## Visual mechanism
A dark tactile canvas is overlaid with a precise dashed modular grid, then interrupted by oversized editorial modules: tilted label cards, electric accent blocks, and a cropped duotone human/photo cutout. The strict grid gives structure while the skewed scale, neon outlines, and high-contrast typography create kinetic keynote energy.

## SVG primitives needed
- 1× `<rect>` for the dark textured background base
- 1× `<filter id="paperGrain">` using blur/offset-style texture simulation on background shapes
- 24× `<line>` for the visible dashed construction grid
- 2× `<rect>` for tilted editorial headline cards
- 2× `<text>` for bold numeric/time callouts
- 1× `<image>` for the cropped hero portrait/photo module
- 1× `<clipPath>` with a custom `<path>` applied to the hero image for a cutout silhouette crop
- 2× `<path>` for cyan cutout halo and organic edge behind the hero image
- 1× `<rect>` for the intentional face/data-obscuring modular block
- 1× `<filter id="softShadow">` for lifted card depth
- 1× `<filter id="glowCyan">` for neon cutout glow
- 1× `<linearGradient>` for subtle background and photo overlay color rhythm
- Several small `<circle>` elements for gritty dot texture accents

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#242424"/>
      <stop offset="55%" stop-color="#151515"/>
      <stop offset="100%" stop-color="#292929"/>
    </linearGradient>

    <linearGradient id="tealWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#7ffcff" stop-opacity="0.92"/>
      <stop offset="100%" stop-color="#1ccbd0" stop-opacity="0.72"/>
    </linearGradient>

    <filter id="softShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="glowCyan" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="7" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="paperGrain" x="-5%" y="-5%" width="110%" height="110%">
      <feOffset dx="2" dy="2" result="shift"/>
      <feGaussianBlur in="shift" stdDeviation="1.2" result="soft"/>
      <feMerge>
        <feMergeNode in="soft"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="profileCut">
      <path d="M958,108 C1006,50 1114,30 1182,84 C1236,126 1258,196 1241,265 C1228,320 1247,356 1231,414 C1219,457 1198,490 1168,511 C1145,527 1151,561 1170,594 C1191,631 1213,666 1224,720 L884,720 C890,667 912,621 935,584 C955,553 952,520 923,500 C883,473 878,420 896,378 C909,348 895,315 899,277 C904,223 925,162 958,108 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <rect x="-20" y="-20" width="1320" height="760" fill="#1a1a1a" opacity="0.42" filter="url(#paperGrain)"/>

  <g stroke="#f4f4f4" stroke-width="1.1" stroke-opacity="0.48" stroke-dasharray="4 5">
    <line x1="36" y1="0" x2="36" y2="720"/>
    <line x1="98" y1="0" x2="98" y2="720"/>
    <line x1="160" y1="0" x2="160" y2="720"/>
    <line x1="228" y1="0" x2="228" y2="720"/>
    <line x1="288" y1="0" x2="288" y2="720"/>
    <line x1="414" y1="0" x2="414" y2="720"/>
    <line x1="478" y1="0" x2="478" y2="720"/>
    <line x1="540" y1="0" x2="540" y2="720"/>
    <line x1="604" y1="0" x2="604" y2="720"/>
    <line x1="664" y1="0" x2="664" y2="720"/>
    <line x1="790" y1="0" x2="790" y2="720"/>
    <line x1="852" y1="0" x2="852" y2="720"/>
    <line x1="916" y1="0" x2="916" y2="720"/>
    <line x1="1040" y1="0" x2="1040" y2="720"/>
    <line x1="1164" y1="0" x2="1164" y2="720"/>
    <line x1="0" y1="24" x2="1280" y2="24"/>
    <line x1="0" y1="86" x2="1280" y2="86"/>
    <line x1="0" y1="150" x2="1280" y2="150"/>
    <line x1="0" y1="274" x2="1280" y2="274"/>
    <line x1="0" y1="398" x2="1280" y2="398"/>
    <line x1="0" y1="462" x2="1280" y2="462"/>
    <line x1="0" y1="524" x2="1280" y2="524"/>
    <line x1="0" y1="648" x2="1280" y2="648"/>
    <line x1="0" y1="710" x2="1280" y2="710"/>
  </g>

  <g opacity="0.18" fill="#ffffff">
    <circle cx="74" cy="51" r="1.5"/><circle cx="182" cy="244" r="1.3"/><circle cx="330" cy="88" r="1.2"/>
    <circle cx="568" cy="376" r="1.6"/><circle cx="722" cy="102" r="1.4"/><circle cx="812" cy="572" r="1.2"/>
    <circle cx="1128" cy="410" r="1.5"/><circle cx="1210" cy="154" r="1.1"/><circle cx="1004" cy="626" r="1.3"/>
  </g>

  <path d="M944,95 C1000,41 1114,22 1191,83 C1255,134 1273,223 1241,302 C1264,354 1238,450 1184,507 C1140,554 1191,612 1226,720 L862,720 C880,637 922,588 923,543 C923,509 881,501 877,441 C873,383 899,354 894,299 C890,227 909,141 944,95 Z"
        fill="#78f8fb" opacity="0.95" filter="url(#glowCyan)"/>

  <image href="https://images.example.com/editorial-profile-portrait-right-facing.jpg"
         x="856" y="24" width="430" height="720" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#profileCut)" opacity="0.82"/>

  <path d="M958,108 C1006,50 1114,30 1182,84 C1236,126 1258,196 1241,265 C1228,320 1247,356 1231,414 C1219,457 1198,490 1168,511 C1145,527 1151,561 1170,594 C1191,631 1213,666 1224,720 L884,720 C890,667 912,621 935,584 C955,553 952,520 923,500 C883,473 878,420 896,378 C909,348 895,315 899,277 C904,223 925,162 958,108 Z"
        fill="url(#tealWash)" opacity="0.55"/>

  <g transform="rotate(-3 438 248)" filter="url(#softShadow)">
    <rect x="88" y="120" width="700" height="248" rx="22" fill="#ffffff"/>
    <rect x="102" y="134" width="672" height="220" rx="15" fill="#151515"/>
    <text x="170" y="292" width="560" font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="118" font-weight="900" fill="#ffffff" letter-spacing="-6">13 Grids</text>
  </g>

  <g transform="rotate(-3 462 480)" filter="url(#softShadow)">
    <rect x="146" y="395" width="626" height="164" fill="#ffb20f"/>
    <text x="218" y="522" width="520" font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="112" font-weight="900" fill="#000000" letter-spacing="-4">8 MINS</text>
  </g>

  <rect x="940" y="130" width="248" height="372" fill="#2f7775" opacity="0.98"/>
  <rect x="940" y="130" width="248" height="372" fill="#0b403f" opacity="0.18"/>

  <g fill="none" stroke="#d9f84b" stroke-width="3" stroke-opacity="0.82">
    <line x1="146" y1="582" x2="214" y2="582"/>
    <line x1="146" y1="582" x2="146" y2="536"/>
    <line x1="744" y1="376" x2="790" y2="376"/>
    <line x1="790" y1="376" x2="790" y2="430"/>
  </g>

  <text x="72" y="675" width="410" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" fill="#d9f84b" letter-spacing="3">MODULAR VISUAL SYSTEM / GRID STUDY</text>
</svg>
```

## Avoid in this skill
- ❌ SVG `<pattern>` fills for the grid; PPT translation drops pattern fills, so draw the construction grid with explicit dashed `<line>` elements.
- ❌ `<mask>` for the portrait cutout or face/data block; use a `clipPath` only on the `<image>`, and use normal rectangles for obscuring modules.
- ❌ Applying filters to grid `<line>` elements; shadows and glows should be applied to `<rect>`, `<path>`, or `<text>` only.
- ❌ Perfectly centered, non-rotated cards everywhere; this technique needs one or two deliberate angle breaks to feel editorial rather than spreadsheet-like.

## Composition notes
- Keep the left two-thirds for oversized typographic modules; the right third can hold a cropped photo, product render, or chart specimen.
- Let the dashed grid cover the whole canvas, but keep it low-opacity so it reads as structure rather than decoration.
- Use one loud accent block, such as yellow-orange or neon lime, plus one cool accent, such as cyan/teal, to create a punchy modular rhythm.
- Leave the grid visible around the modules; negative space is what makes the layout feel mathematically locked rather than crowded.