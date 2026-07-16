# SVG Recipe — Symmetrical Node Flow Infographic (Stylized Barbell)

## Visual mechanism
A premium “barbell” infographic: two mirrored teardrop nodes taper into a dominant central white circle, while thick semicircular arrows orbit the center to imply bidirectional flow. A deep radial purple background, translucent world-map texture, and soft shadows create keynote-style depth.

## SVG primitives needed
- 1× `<rect>` for the full-slide radial gradient background.
- 6× `<path>` for translucent world-map silhouettes behind the diagram.
- 2× `<path>` for the left and right flared teardrop/barbell node shapes.
- 2× `<path>` for thick curved orbit arrows around the central node.
- 2× `<path>` for manual triangular arrowheads, because `marker-end` on paths will not translate reliably.
- 1× `<circle>` for the large central focal node.
- 2× `<circle>` for subtle side-node highlight overlays.
- 8× `<text>` blocks with explicit `width` attributes for node labels and body copy.
- 6× small `<rect>` / `<path>` icon elements for editable phone/device glyphs.
- 1× `<radialGradient>` for the background.
- 3× `<linearGradient>` definitions for node fills, arrow strokes, and central sheen.
- 2× `<filter>` definitions using blur/offset/merge for soft shadows and glows.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgRadial" cx="50%" cy="50%" r="72%">
      <stop offset="0%" stop-color="#6f38a5"/>
      <stop offset="48%" stop-color="#4f237d"/>
      <stop offset="100%" stop-color="#1e0a36"/>
    </radialGradient>
    <linearGradient id="nodeGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#8f52c7"/>
      <stop offset="55%" stop-color="#4b1d73"/>
      <stop offset="100%" stop-color="#261038"/>
    </linearGradient>
    <linearGradient id="arrowGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#c67cff"/>
      <stop offset="100%" stop-color="#7130b6"/>
    </linearGradient>
    <linearGradient id="circleSheen" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="72%" stop-color="#f4f1f8"/>
      <stop offset="100%" stop-color="#ded7e8"/>
    </linearGradient>
    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="170%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="8" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="violetGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="6" result="glow"/>
      <feMerge><feMergeNode in="glow"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgRadial)"/>

  <g opacity="0.22" fill="#c7a3e9">
    <path d="M166 216 C210 169 283 155 348 170 C390 179 412 151 452 140 C500 128 535 145 552 176 C511 188 482 198 460 232 C427 222 394 224 360 246 C300 225 244 224 166 216 Z"/>
    <path d="M585 162 C662 132 764 139 824 174 C875 203 920 183 966 194 C1008 203 1038 228 1064 260 C988 256 941 278 890 300 C835 276 781 278 738 315 C682 284 639 262 585 270 Z"/>
    <path d="M334 333 C374 319 414 338 437 375 C461 415 457 474 426 517 C391 489 370 447 351 405 C331 363 307 348 334 333 Z"/>
    <path d="M710 375 C752 351 810 362 850 401 C890 439 918 483 966 507 C904 529 841 518 794 482 C752 450 725 421 710 375 Z"/>
    <path d="M972 455 C1016 433 1066 441 1104 478 C1071 510 1018 514 978 490 C958 478 952 466 972 455 Z"/>
    <path d="M510 233 C552 221 596 235 625 268 C591 280 560 295 532 321 C510 296 498 264 510 233 Z"/>
  </g>

  <text x="22" y="92" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="64" font-weight="800" fill="#ffffff" letter-spacing="1">SYMMETRIC</text>
  <text x="24" y="151" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="55" font-weight="800" fill="#b7b1bd" letter-spacing="1">NODE FLOW</text>

  <path d="M185 297 C125 297 91 327 91 360 C91 394 125 423 185 423 C254 423 279 374 350 371 C420 368 483 382 565 389 C529 371 529 349 565 331 C483 338 420 352 350 349 C279 346 254 297 185 297 Z"
        fill="url(#nodeGrad)" filter="url(#softShadow)"/>
  <path d="M1095 297 C1155 297 1189 327 1189 360 C1189 394 1155 423 1095 423 C1026 423 1001 374 930 371 C860 368 797 382 715 389 C751 371 751 349 715 331 C797 338 860 352 930 349 C1001 346 1026 297 1095 297 Z"
        fill="url(#nodeGrad)" filter="url(#softShadow)"/>

  <circle cx="190" cy="360" r="62" fill="#a660d5" opacity="0.45"/>
  <circle cx="1090" cy="360" r="62" fill="#a660d5" opacity="0.45"/>

  <path d="M493 298 C514 220 577 177 651 181 C700 184 739 201 773 233"
        fill="none" stroke="url(#arrowGrad)" stroke-width="19" stroke-linecap="round" filter="url(#violetGlow)"/>
  <path d="M773 233 L720 235 L754 196 Z" fill="#9f56e9" filter="url(#softShadow)"/>

  <path d="M787 422 C756 505 688 546 613 536 C565 530 526 508 496 473"
        fill="none" stroke="url(#arrowGrad)" stroke-width="19" stroke-linecap="round" filter="url(#violetGlow)"/>
  <path d="M496 473 L549 475 L512 513 Z" fill="#7d37bf" filter="url(#softShadow)"/>

  <circle cx="640" cy="360" r="132" fill="#2a113e" opacity="0.85" filter="url(#softShadow)"/>
  <circle cx="640" cy="360" r="124" fill="url(#circleSheen)" stroke="#35134f" stroke-width="6"/>

  <g opacity="0.35" fill="#7f7a86">
    <path d="M548 318 C587 296 642 292 681 315 C642 323 606 321 548 318 Z"/>
    <path d="M705 333 C737 346 748 371 729 394 C705 380 693 358 705 333 Z"/>
    <path d="M569 376 C600 354 640 352 672 373 C635 387 600 390 569 376 Z"/>
  </g>

  <g fill="none" stroke="#3c4a5d" stroke-width="6" stroke-linecap="round" stroke-linejoin="round">
    <rect x="631" y="263" width="29" height="54" rx="4" fill="#e8edf4"/>
    <path d="M661 272 L672 272 M661 285 L669 285 M632 309 L604 328 L597 352 L626 345 L646 316"/>
  </g>

  <text x="548" y="367" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="800" fill="#3b1559" text-anchor="middle" letter-spacing="1">INFOGRAPHIC</text>
  <text x="565" y="393" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6f6876" text-anchor="middle">Core platform connecting both strategic motions</text>

  <text x="151" y="335" width="85" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="800" fill="#ffffff" text-anchor="middle">OPTION A</text>
  <text x="148" y="356" width="88" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#f2e9ff" text-anchor="middle">Acquisition channel</text>
  <text x="149" y="372" width="88" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#f2e9ff" text-anchor="middle">that feeds demand</text>

  <text x="1045" y="335" width="95" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="800" fill="#ffffff" text-anchor="middle">OPTION B</text>
  <text x="1044" y="356" width="98" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#f2e9ff" text-anchor="middle">Retention loop</text>
  <text x="1044" y="372" width="98" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#f2e9ff" text-anchor="middle">that expands value</text>

  <g fill="none" stroke="#ffffff" stroke-width="2.2" stroke-linecap="round" opacity="0.9">
    <rect x="181" y="382" width="19" height="26" rx="3"/>
    <circle cx="190.5" cy="401" r="3" fill="#ffffff"/>
    <path d="M176 388 C169 393 169 399 176 404 M205 388 C212 393 212 399 205 404"/>
    <rect x="1080" y="382" width="20" height="29" rx="3"/>
    <path d="M1074 388 C1067 395 1067 402 1074 409 M1106 388 C1113 395 1113 402 1106 409"/>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to carve the node shapes around the center; simply layer the white central circle above the tapered node paths.
- ❌ Do not use `marker-end` on curved `<path>` arrows; draw arrowheads as separate filled triangular `<path>` shapes.
- ❌ Do not apply filters to `<line>` elements; use curved `<path>` strokes for the orbit arrows if glow or shadow is needed.
- ❌ Do not rely on `<textPath>` for circular arrow labels; place normal editable `<text>` blocks around the nodes instead.
- ❌ Do not clip vector node shapes with `clip-path`; clip paths should be reserved for images only.

## Composition notes
- Keep the central circle large, approximately 240–270 px in diameter, so it visibly hides the tapered inner points of both side nodes.
- Place side labels inside the circular lobes, not in the tapered bridge, to preserve legibility.
- Use a dark-to-bright rhythm: dark background, darker node bridge, bright violet arrows, white center.
- Leave generous negative space above and below the barbell; the design works best as a single strong horizontal visual axis.