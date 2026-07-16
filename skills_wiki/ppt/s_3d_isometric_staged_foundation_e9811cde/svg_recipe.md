# SVG Recipe — 3D Isometric Staged Foundation

## Visual mechanism
A flat square “floor” is redrawn as an isometric slab: the top surface is a diamond-shaped parquet field, while darker offset side faces create extrusion and physical weight. Subtle grain strokes, staggered plank seams, rim highlights, and a soft under-shadow make the stage feel like a premium architectural object floating in deep space.

## SVG primitives needed
- 1× `<rect>` for the dark cinematic background
- 1× `<path>` for the soft cast shadow under the slab
- 2× `<path>` for the visible extruded side faces
- 1× `<path>` for the main top-surface diamond base
- 8× `<path>` for long isometric plank rows across the top surface
- 5× `<path>` for pale highlight planks that simulate varied wood boards and reflected light
- 2× `<path>` for seam lines between rows and staggered board joints
- 3× `<path>` for dense wood-grain stroke clusters
- 3× `<path>` for bevel/rim highlights on slab edges
- 1× `<filter id="softShadow">` applied to the cast-shadow path
- 5× `<linearGradient>` fills for background, wood rows, side walls, and edge lighting

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#4b5168"/>
      <stop offset="0.42" stop-color="#2f3854"/>
      <stop offset="1" stop-color="#111735"/>
    </linearGradient>

    <linearGradient id="woodWarm" x1="310" y1="360" x2="940" y2="335" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#f4d383"/>
      <stop offset="0.35" stop-color="#ffe6a8"/>
      <stop offset="0.7" stop-color="#e7b75f"/>
      <stop offset="1" stop-color="#fff0b9"/>
    </linearGradient>

    <linearGradient id="woodAlt" x1="330" y1="405" x2="900" y2="300" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#d99f48"/>
      <stop offset="0.45" stop-color="#f7d88d"/>
      <stop offset="1" stop-color="#f0bd67"/>
    </linearGradient>

    <linearGradient id="sideLeft" x1="300" y1="360" x2="645" y2="585" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#101a36"/>
      <stop offset="0.55" stop-color="#060b1d"/>
      <stop offset="1" stop-color="#020615"/>
    </linearGradient>

    <linearGradient id="sideRight" x1="980" y1="360" x2="640" y2="585" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#172342"/>
      <stop offset="0.6" stop-color="#081027"/>
      <stop offset="1" stop-color="#030715"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="160%">
      <feOffset dx="0" dy="26" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <path d="M304 398 L640 585 L978 398 L1012 414 L640 636 L268 414 Z"
        fill="#020513" opacity="0.46" filter="url(#softShadow)"/>

  <path d="M300 360 L640 500 L640 585 L304 395 Z" fill="url(#sideLeft)"/>
  <path d="M980 360 L640 500 L640 585 L980 395 Z" fill="url(#sideRight)"/>
  <path d="M300 360 L640 220 L980 360 L640 500 Z" fill="#f9d891"/>

  <path d="M300 360 L640 220 L684 238 L344 378 Z" fill="url(#woodWarm)"/>
  <path d="M344 378 L684 238 L728 256 L388 396 Z" fill="#f2c46e"/>
  <path d="M388 396 L728 256 L773 275 L433 415 Z" fill="url(#woodAlt)"/>
  <path d="M433 415 L773 275 L817 293 L477 433 Z" fill="#f8d88d"/>
  <path d="M477 433 L817 293 L861 311 L521 451 Z" fill="#e8b75f"/>
  <path d="M521 451 L861 311 L905 329 L565 469 Z" fill="#f6d486"/>
  <path d="M565 469 L905 329 L949 347 L609 487 Z" fill="#eec16a"/>
  <path d="M609 487 L949 347 L980 360 L640 500 Z" fill="#f9dd97"/>

  <path d="M565 324 L705 266 L755 287 L615 345 Z" fill="#fff3b8" opacity="0.88"/>
  <path d="M650 374 L840 296 L900 321 L710 400 Z" fill="#fff6c4" opacity="0.9"/>
  <path d="M540 417 L660 368 L710 389 L590 438 Z" fill="#fff0ad" opacity="0.75"/>
  <path d="M724 432 L932 346 L980 365 L772 452 Z" fill="#fff7c9" opacity="0.92"/>
  <path d="M605 465 L760 401 L815 424 L660 488 Z" fill="#ffedaa" opacity="0.72"/>

  <path d="M344 378 L684 238 M388 396 L728 256 M433 415 L773 275 M477 433 L817 293
           M521 451 L861 311 M565 469 L905 329 M609 487 L949 347"
        fill="none" stroke="#b8893d" stroke-width="1.6" opacity="0.55"/>

  <path d="M395 321 L439 339 M528 266 L572 284 M423 349 L467 367 M545 299 L589 317
           M660 252 L704 270 M500 350 L544 368 M625 298 L669 316 M754 278 L798 296
           M560 399 L604 417 M693 344 L737 362 M837 314 L881 332 M612 450 L656 468
           M754 391 L798 409 M894 352 L938 370"
        fill="none" stroke="#a36f2f" stroke-width="1.8" opacity="0.58"/>

  <path d="M318 356 C390 333 470 296 625 231
           M330 365 C420 334 515 286 650 232
           M358 373 C450 340 545 293 675 242
           M395 388 C480 356 595 303 715 256
           M430 405 C515 370 630 322 760 275"
        fill="none" stroke="#c98f38" stroke-width="1.1" opacity="0.48"/>

  <path d="M455 357 C555 319 650 275 770 244
           M470 371 C590 324 690 286 805 260
           M500 389 C600 351 715 300 845 282
           M530 411 C640 367 760 318 875 309
           M560 430 C690 380 805 340 910 326"
        fill="none" stroke="#fff0b0" stroke-width="1.25" opacity="0.42"/>

  <path d="M602 474 C690 438 795 390 930 345
           M620 489 C720 446 835 398 955 358
           M585 455 C705 405 815 362 920 332
           M390 363 C505 320 600 281 716 244"
        fill="none" stroke="#9d6727" stroke-width="0.95" opacity="0.34"/>

  <path d="M300 360 L640 220 L980 360" fill="none" stroke="#fff2b8" stroke-width="3" opacity="0.72"/>
  <path d="M300 360 L640 500 L980 360" fill="none" stroke="#8b5d28" stroke-width="2.2" opacity="0.6"/>
  <path d="M304 395 L640 585 L980 395" fill="none" stroke="#020616" stroke-width="3.5" opacity="0.82"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use `transform="matrix(...)"` or `skewX/skewY` to fake the isometric plane; PPT translation drops these transforms, so draw the diamond and plank quadrilaterals directly as `<path>` coordinates.
- ❌ Do not use SVG `<pattern>` fills for the wood texture; they translate poorly. Use explicit plank paths and grain strokes instead.
- ❌ Do not rely on PowerPoint-only 3D camera/extrusion settings inside SVG; reproduce the 3D look with editable side-face paths, bevel strokes, and shadow.
- ❌ Do not apply `clip-path` to the plank paths; clipping is only reliable on `<image>` elements. Keep all plank coordinates inside the diamond surface.
- ❌ Do not use filtered `<line>` elements for shadows or glows; use `<path>` shapes with filters when a soft effect is needed.

## Composition notes
- Keep the slab centered slightly below midline, occupying the lower 50–60% of the slide; this leaves premium negative space above for title typography or product callouts.
- Use a dark blue/navy background so the warm oak surface and black extrusion read as a lit physical object in a void.
- The strongest visual focus should be the front edge and top-surface texture: use bright rim strokes on the upper edges and deep side shadows below.
- For charts or timelines, place milestones, product renders, or icons on the top diamond, aligned to the same isometric axes so they appear staged on the foundation.