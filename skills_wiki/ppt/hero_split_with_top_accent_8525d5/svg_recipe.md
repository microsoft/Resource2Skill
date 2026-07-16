# SVG Recipe — Hero Split with Top Accent

## Visual mechanism
A bold editorial split layout: the left half stays mostly open for an oversized headline anchored low, while the right half is dominated by a clipped hero image. A saturated block running along the top edge creates the distinctive accent and makes the slide feel like a designed cover, not a generic two-column page.

## SVG primitives needed
- 1× `<rect>` for the warm full-slide background
- 2× `<linearGradient>` for subtle background and accent depth
- 1× `<filter id="softShadow">` applied to the hero-image backing card and small accent cards
- 1× `<clipPath>` with rounded `<rect>` applied to the hero `<image>`
- 1× `<image>` for the right-side hero visual
- 2× `<rect>` for the hero image shadow card and editable border frame
- 2× `<path>` for the top accent block and lower-left organic decorative shape
- 4× `<rect>` for top tabs, label pills, and small color rhythm blocks
- 3× `<circle>` for playful editorial dots near the image and headline
- 4× `<text>` elements with explicit `width` attributes for kicker, headline, metadata, and accent label

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWarm" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFF8EA"/>
      <stop offset="58%" stop-color="#FFF2D8"/>
      <stop offset="100%" stop-color="#FFE8C2"/>
    </linearGradient>

    <linearGradient id="accentSunset" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FF4D6D"/>
      <stop offset="58%" stop-color="#FF9F1C"/>
      <stop offset="100%" stop-color="#FFD166"/>
    </linearGradient>

    <linearGradient id="blobTint" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFE45E" stop-opacity="0.72"/>
      <stop offset="100%" stop-color="#FF4D6D" stop-opacity="0.15"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="16" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="heroClip">
      <rect x="704" y="96" width="500" height="540" rx="34" ry="34"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWarm)"/>

  <path d="M0 0 H706 C670 21 650 50 660 82 H0 Z" fill="url(#accentSunset)"/>
  <rect x="706" y="0" width="132" height="82" fill="#161616"/>
  <rect x="838" y="0" width="78" height="82" fill="#06D6A0"/>
  <circle cx="956" cy="40" r="12" fill="#161616"/>
  <circle cx="992" cy="40" r="12" fill="#FF4D6D"/>

  <text x="44" y="52" width="280" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" letter-spacing="2.6" fill="#161616">
    SECTION DIVIDER
  </text>

  <text x="725" y="52" width="100" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="800" letter-spacing="1.8" fill="#FFFFFF">
    2026
  </text>

  <path d="M82 455 C146 402 237 424 286 493 C330 555 293 632 212 657 C132 681 57 646 42 577 C32 527 42 488 82 455 Z"
        fill="url(#blobTint)"/>

  <rect x="690" y="112" width="500" height="540" rx="34" ry="34" fill="#1D1D1D" opacity="0.23" filter="url(#softShadow)"/>
  <image href="https://images.example.com/hero-photo-playful-cosmic-quiz-audience.jpg"
         x="704" y="96" width="500" height="540"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#heroClip)"/>
  <rect x="704" y="96" width="500" height="540" rx="34" ry="34"
        fill="none" stroke="#161616" stroke-width="4"/>

  <rect x="650" y="148" width="126" height="44" rx="22" ry="22"
        fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="674" y="177" width="86" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="800" letter-spacing="1.4" fill="#161616">
    LIVE
  </text>

  <circle cx="674" cy="530" r="14" fill="#FFD166"/>
  <circle cx="646" cy="569" r="8" fill="#06D6A0"/>
  <rect x="610" y="600" width="66" height="16" rx="8" ry="8" fill="#FF4D6D"/>

  <rect x="78" y="300" width="108" height="10" rx="5" ry="5" fill="#161616"/>
  <text x="78" y="360" width="550" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="78" font-weight="800" fill="#161616">
    <tspan x="78" dy="0">Cosmic</tspan>
    <tspan x="78" dy="86">Quiz Night</tspan>
  </text>

  <text x="82" y="561" width="455" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="500" fill="#3A3025">
    A playful launch session for teams who think faster than light.
  </text>

  <line x1="82" y1="612" x2="206" y2="612" stroke="#FF4D6D" stroke-width="5" stroke-linecap="round"/>
  <text x="230" y="619" width="280" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="700" letter-spacing="1.2" fill="#161616">
    MONDAY · MAIN STAGE
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use a plain 50/50 split with identical column weights; the left side should breathe and the right hero should feel dominant.
- ❌ Do not apply `clip-path` to the shadow card or decorative shapes; use clipping only on the `<image>`.
- ❌ Do not put the headline near the top accent; the shell works best when the headline is anchored in the lower-left quadrant.
- ❌ Do not use tiny body text or dense bullet lists; this is a cover / divider shell, not an information slide.
- ❌ Do not use `mask`, `<foreignObject>`, `<textPath>`, or inherited arrow markers.

## Composition notes
- Keep the top accent between 70–95 px tall so it reads as a branded edge treatment without stealing focus from the headline.
- Place the hero image on the right, roughly 38–42% of slide width, with generous top and bottom margins and a rounded editable frame.
- Anchor the headline around x=75–95 and y=340–470; leave the upper-left field mostly empty except for the top accent label.
- Repeat accent colors in small dots, pills, or bars near the image to visually tie the two columns together.