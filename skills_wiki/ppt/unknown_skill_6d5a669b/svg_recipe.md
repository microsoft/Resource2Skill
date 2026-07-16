# SVG Recipe — Dynamic Geometric Gradient Typography

## Visual mechanism
Huge extra-bold italic text is filled with a shared left-to-right hot gradient, making the words feel like fast-moving vector artwork while remaining editable text. Matching slanted parallelogram ribbons behind smaller labels reinforce the same forward angle and create a premium “motion title” lockup.

## SVG primitives needed
- 1× `<rect>` for the warm off-white slide background.
- 3× subtle background `<path>` parallelograms for oversized geometric motion slashes.
- 2× foreground `<path>` parallelogram ribbons behind the small white words.
- 5× `<text>` elements for the editable typography: large number, two main title lines, and two ribbon labels.
- 4× `<linearGradient>` definitions for global text gradients, ribbon gradients, and soft background slashes.
- 1× `<filter id="softShadow">` applied to the ribbon paths for a very light premium lift.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="heroTextGradient" gradientUnits="userSpaceOnUse" x1="70" y1="360" x2="1210" y2="360">
      <stop offset="0%" stop-color="#F2353D"/>
      <stop offset="44%" stop-color="#E94057"/>
      <stop offset="100%" stop-color="#B500B9"/>
    </linearGradient>

    <linearGradient id="numberGradient" gradientUnits="userSpaceOnUse" x1="70" y1="360" x2="330" y2="360">
      <stop offset="0%" stop-color="#F3334F"/>
      <stop offset="52%" stop-color="#F5442D"/>
      <stop offset="100%" stop-color="#D91F87"/>
    </linearGradient>

    <linearGradient id="ribbonGradient" gradientUnits="userSpaceOnUse" x1="60" y1="520" x2="760" y2="195">
      <stop offset="0%" stop-color="#F2384A"/>
      <stop offset="55%" stop-color="#E31369"/>
      <stop offset="100%" stop-color="#B600B8"/>
    </linearGradient>

    <linearGradient id="quietSlashGradient" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.92"/>
      <stop offset="100%" stop-color="#EEF1F6" stop-opacity="0.35"/>
    </linearGradient>

    <filter id="softShadow" x="-15%" y="-25%" width="130%" height="150%">
      <feOffset dx="0" dy="8" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F7F8FB"/>

  <!-- oversized quiet slashes: same forward angle as the italic typography -->
  <path d="M130 -70 L330 -70 L210 780 L10 780 Z" fill="url(#quietSlashGradient)" opacity="0.58"/>
  <path d="M880 -40 L1060 -40 L900 760 L720 760 Z" fill="#FFFFFF" opacity="0.52"/>
  <path d="M1030 250 L1230 250 L1125 735 L925 735 Z" fill="#EDF0F5" opacity="0.42"/>

  <!-- top ribbon -->
  <path d="M392 176 L760 176 L742 249 L374 249 Z"
        fill="url(#ribbonGradient)"
        filter="url(#softShadow)"/>
  <text x="400" y="230"
        width="350"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="54"
        font-weight="900"
        font-style="italic"
        letter-spacing="-1"
        fill="#FFFFFF">PROJECTS</text>

  <!-- primary numeric anchor -->
  <text x="82" y="445"
        width="260"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="214"
        font-weight="900"
        font-style="italic"
        letter-spacing="-8"
        fill="url(#numberGradient)">10</text>

  <!-- main stacked headline -->
  <text x="350" y="353"
        width="870"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="118"
        font-weight="900"
        font-style="italic"
        letter-spacing="-6"
        fill="url(#heroTextGradient)">POWERPOINT</text>

  <text x="344" y="456"
        width="650"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="112"
        font-weight="900"
        font-style="italic"
        letter-spacing="-5"
        fill="url(#heroTextGradient)">MOTIONS</text>

  <!-- lower ribbon, visually locking to the left edge of the number -->
  <path d="M84 480 L462 480 L443 554 L65 554 Z"
        fill="url(#ribbonGradient)"
        filter="url(#softShadow)"/>
  <text x="94" y="535"
        width="350"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="54"
        font-weight="900"
        font-style="italic"
        letter-spacing="-2"
        fill="#FFFFFF">ANIMATED</text>
</svg>
```

## Avoid in this skill
- ❌ Do not convert the main words into outlined `<path>` letters; the technique depends on editable gradient-filled `<text>`.
- ❌ Do not use `transform="skewX(...)"` to fake italics; use `font-style="italic"` and draw the parallelogram ribbons manually with `<path>`.
- ❌ Do not use masks or clip paths on text for the ribbon reveal effect; those will not translate reliably. Use visible slanted paths layered behind the text instead.
- ❌ Do not add thin outlines around the gradient words; the premium look comes from clean, heavy typography and strong color flow.

## Composition notes
- Keep the main lockup slightly left of center, with the number acting as a heavy visual anchor and the stacked title extending to the right.
- Use a mostly empty off-white background; the energy should come from the gradient typography and slanted geometry, not from clutter.
- Match all ribbon angles to the italic text slant so the slide feels like one coherent motion system.
- Let the gradient run horizontally across the full title area: warm red/orange on the left, magenta/purple on the right.