# SVG Recipe — Kinetic Cinematic Film Strip Overlay

## Visual mechanism
A stark white film strip cuts across a pitch-black poster background, dividing the slide into sequential cinematic frames. Oversized dark typography creates atmospheric texture behind the strip, while bright foreground words sit inside each frame like story beats in motion.

## SVG primitives needed
- 1× `<rect>` for the full-slide black background.
- 1× `<linearGradient>` for a barely visible noir background sheen.
- 2× giant `<text>` elements for low-contrast background texture typography.
- 3× `<clipPath>` definitions with rounded `<rect>` crops for cinematic frame imagery.
- 3× `<image>` elements clipped into the film frames.
- 3× translucent `<rect>` overlays to darken the photos and improve text contrast.
- 2× wide white `<rect>` elements for the film strip’s top and bottom bands.
- 4× vertical white `<rect>` elements for the strip edges and frame separators.
- 2× black multi-subpath `<path>` elements for the repeating sprocket holes.
- 3× foreground `<text>` elements with nested `<tspan>` for step labels and hero words.
- 3× small accent `<path>` slashes for kinetic editorial energy.
- 2× `<filter>` definitions: one drop shadow for film-strip depth, one glow/shadow for foreground typography.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="noirBg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#050505"/>
      <stop offset="55%" stop-color="#000000"/>
      <stop offset="100%" stop-color="#111318"/>
    </linearGradient>

    <filter id="stripShadow" x="-10%" y="-20%" width="120%" height="150%">
      <feOffset dx="0" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="typeGlow" x="-20%" y="-40%" width="140%" height="180%">
      <feOffset dx="0" dy="4" result="off"/>
      <feGaussianBlur in="off" stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="frameOne">
      <rect x="92" y="278" width="316" height="162" rx="2"/>
    </clipPath>
    <clipPath id="frameTwo">
      <rect x="462" y="278" width="316" height="162" rx="2"/>
    </clipPath>
    <clipPath id="frameThree">
      <rect x="832" y="278" width="316" height="162" rx="2"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#noirBg)"/>

  <text x="640" y="162" width="1280" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="132" font-weight="900"
        letter-spacing="-6" fill="#1a1a1a">KINETIC</text>
  <text x="640" y="654" width="1280" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="116" font-weight="900"
        letter-spacing="-5" fill="#171717">STORYBOARD</text>

  <g transform="rotate(-2 640 360)">
    <rect x="-80" y="216" width="1440" height="286" fill="#050505"/>

    <image href="https://images.unsplash.com/photo-1492691527719-9d1e07e534b4?auto=format&amp;fit=crop&amp;w=800&amp;q=80"
           x="92" y="250" width="316" height="220" preserveAspectRatio="xMidYMid slice"
           clip-path="url(#frameOne)"/>
    <image href="https://images.unsplash.com/photo-1516280440614-37939bbacd81?auto=format&amp;fit=crop&amp;w=800&amp;q=80"
           x="462" y="250" width="316" height="220" preserveAspectRatio="xMidYMid slice"
           clip-path="url(#frameTwo)"/>
    <image href="https://images.unsplash.com/photo-1485846234645-a62644f84728?auto=format&amp;fit=crop&amp;w=800&amp;q=80"
           x="832" y="250" width="316" height="220" preserveAspectRatio="xMidYMid slice"
           clip-path="url(#frameThree)"/>

    <rect x="92" y="278" width="316" height="162" fill="#000000" opacity="0.58"/>
    <rect x="462" y="278" width="316" height="162" fill="#000000" opacity="0.58"/>
    <rect x="832" y="278" width="316" height="162" fill="#000000" opacity="0.58"/>

    <rect x="-80" y="216" width="1440" height="60" fill="#ffffff" filter="url(#stripShadow)"/>
    <rect x="-80" y="442" width="1440" height="60" fill="#ffffff" filter="url(#stripShadow)"/>
    <rect x="50" y="216" width="42" height="286" fill="#ffffff"/>
    <rect x="420" y="216" width="42" height="286" fill="#ffffff"/>
    <rect x="790" y="216" width="42" height="286" fill="#ffffff"/>
    <rect x="1160" y="216" width="42" height="286" fill="#ffffff"/>

    <path fill="#000000" d="M-38 234h34v24h-34z M32 234h34v24h-34z M102 234h34v24h-34z M172 234h34v24h-34z M242 234h34v24h-34z M312 234h34v24h-34z M382 234h34v24h-34z M452 234h34v24h-34z M522 234h34v24h-34z M592 234h34v24h-34z M662 234h34v24h-34z M732 234h34v24h-34z M802 234h34v24h-34z M872 234h34v24h-34z M942 234h34v24h-34z M1012 234h34v24h-34z M1082 234h34v24h-34z M1152 234h34v24h-34z M1222 234h34v24h-34z M1292 234h34v24h-34z"/>
    <path fill="#000000" d="M-38 460h34v24h-34z M32 460h34v24h-34z M102 460h34v24h-34z M172 460h34v24h-34z M242 460h34v24h-34z M312 460h34v24h-34z M382 460h34v24h-34z M452 460h34v24h-34z M522 460h34v24h-34z M592 460h34v24h-34z M662 460h34v24h-34z M732 460h34v24h-34z M802 460h34v24h-34z M872 460h34v24h-34z M942 460h34v24h-34z M1012 460h34v24h-34z M1082 460h34v24h-34z M1152 460h34v24h-34z M1222 460h34v24h-34z M1292 460h34v24h-34z"/>

    <path d="M116 306 L148 292 L140 322 Z" fill="#ffcc33"/>
    <path d="M486 306 L518 292 L510 322 Z" fill="#ffcc33"/>
    <path d="M856 306 L888 292 L880 322 Z" fill="#ffcc33"/>

    <text x="250" y="336" width="260" text-anchor="middle" filter="url(#typeGlow)"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" fill="#ffffff">
      <tspan x="250" font-size="18" font-weight="700" letter-spacing="4" fill="#ffcc33">STEP 01</tspan>
      <tspan x="250" dy="54" font-size="46" font-weight="900" letter-spacing="-1">DISCOVER</tspan>
    </text>

    <text x="620" y="336" width="260" text-anchor="middle" filter="url(#typeGlow)"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" fill="#ffffff">
      <tspan x="620" font-size="18" font-weight="700" letter-spacing="4" fill="#ffcc33">STEP 02</tspan>
      <tspan x="620" dy="54" font-size="46" font-weight="900" letter-spacing="-1">FRAME</tspan>
    </text>

    <text x="990" y="336" width="260" text-anchor="middle" filter="url(#typeGlow)"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" fill="#ffffff">
      <tspan x="990" font-size="18" font-weight="700" letter-spacing="4" fill="#ffcc33">STEP 03</tspan>
      <tspan x="990" dy="54" font-size="46" font-weight="900" letter-spacing="-1">REVEAL</tspan>
    </text>
  </g>

  <text x="74" y="74" width="460" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" letter-spacing="5" fill="#f5f5f5" opacity="0.72">
    CINEMATIC PROCESS SEQUENCE
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not build the sprocket holes with `<mask>`; place black rectangles or black multi-subpath `<path>` shapes over the white bands instead.
- ❌ Do not use `<use>` to repeat sprocket holes; it hard-fails translation. Use explicit rects or one combined editable path.
- ❌ Do not rely on `clip-path` for non-image shapes; only clip the frame photos, then place normal dark overlay rectangles above them.
- ❌ Do not use `marker-end` on paths for motion arrows; if arrows are needed, use editable `<line>` elements with marker attributes directly on each line.
- ❌ Avoid making the strip perfectly horizontal if the goal is “kinetic”; a subtle `rotate(-1.5 to -3)` gives the poster energy without harming readability.

## Composition notes
- Keep the film strip in the middle 35–45% of the canvas; it should dominate the slide but leave black negative space above and below.
- Use huge low-contrast background type as texture, not as content: dark grey on black, partially hidden behind the strip.
- Divide the strip into three equal story windows for process slides; the white separators should feel like physical film stock.
- Use one warm accent color, such as yellow or red, sparingly for step labels and small slashes so the white typography remains the hero.