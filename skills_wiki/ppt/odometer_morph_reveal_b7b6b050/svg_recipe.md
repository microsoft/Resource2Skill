# SVG Recipe — Odometer Morph Reveal

## Visual mechanism
A huge number is built from separate vertical digit-strip images, each clipped by a fixed rounded “window” so only one numeral is visible. Duplicate the slide, keep the clipping windows in the same place, change each strip’s vertical offset from the starting digit to the ending digit, then use PowerPoint Morph to create the rolling odometer reveal.

## SVG primitives needed
- 1× `<rect>` for a dark-to-blue gradient fallback background
- 1× `<image>` for the cinematic hero photo background
- 2× `<rect>` gradient overlays for vignette/readability over the photo
- 4× `<clipPath>` with rounded `<rect>` windows for the digit apertures
- 4× `<image>` digit strips, one per number column, clipped to the windows
- 2× `<rect>` translucent fade bands over the digit area to imply slot-machine glass depth
- 1× `<text>` for the static unit suffix
- 1× `<text>` for the spaced location/title label
- 2× `<filter>` definitions for soft shadows on text and small foreground objects
- Several `<rect>`, `<path>`, and `<circle>` primitives for the small China/Nepal flags and decorative mountain silhouettes

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="skyFallback" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#6fb8f5"/>
      <stop offset="48%" stop-color="#9fd3ff"/>
      <stop offset="100%" stop-color="#06111f"/>
    </linearGradient>

    <linearGradient id="vignette" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.05"/>
      <stop offset="52%" stop-color="#000000" stop-opacity="0.02"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.68"/>
    </linearGradient>

    <linearGradient id="topDigitFade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#8cc9ff" stop-opacity="0.32"/>
      <stop offset="100%" stop-color="#8cc9ff" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="bottomDigitFade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.20"/>
    </linearGradient>

    <filter id="softTextShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="4" dy="8" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="flagShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="5" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <!-- Each clipPath is the fixed viewport. Move the image y-position between Morph slides. -->
    <clipPath id="winDigit1"><rect x="198" y="82" width="170" height="278" rx="18"/></clipPath>
    <clipPath id="winDigit2"><rect x="438" y="82" width="170" height="278" rx="18"/></clipPath>
    <clipPath id="winDigit3"><rect x="660" y="82" width="170" height="278" rx="18"/></clipPath>
    <clipPath id="winDigit4"><rect x="868" y="82" width="170" height="278" rx="18"/></clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#skyFallback)"/>
  <image href="https://images.example.com/hero-photo-mount-everest-sunrise-wide-16x9.jpg"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#vignette)"/>

  <!-- Optional painted ridge accents keep the composition readable if the photo is very bright. -->
  <path d="M0 544 L104 484 L184 520 L294 440 L392 505 L516 365 L640 470 L744 402 L900 520 L1020 472 L1280 548 L1280 720 L0 720 Z"
        fill="#07101d" opacity="0.34"/>
  <path d="M280 526 L512 352 L598 480 L672 452 L736 542 Z"
        fill="#f8fbff" opacity="0.20"/>
  <path d="M424 500 L520 360 L566 462 L620 492 Z"
        fill="#f7a449" opacity="0.25"/>

  <!-- Final frame: 8848. For the first Morph slide, use y=82 for all four strips to show 0000. -->
  <image id="digit_1_strip"
         href="https://images.example.com/odometer-strip-white-bold-digits-0-to-9-transparent-shadow.png"
         x="198" y="-1998" width="170" height="2780" preserveAspectRatio="none" clip-path="url(#winDigit1)"/>
  <image id="digit_2_strip"
         href="https://images.example.com/odometer-strip-white-bold-digits-0-to-9-transparent-shadow.png"
         x="438" y="-1998" width="170" height="2780" preserveAspectRatio="none" clip-path="url(#winDigit2)"/>
  <image id="digit_3_strip"
         href="https://images.example.com/odometer-strip-white-bold-digits-0-to-9-transparent-shadow.png"
         x="660" y="-1030" width="170" height="2780" preserveAspectRatio="none" clip-path="url(#winDigit3)"/>
  <image id="digit_4_strip"
         href="https://images.example.com/odometer-strip-white-bold-digits-0-to-9-transparent-shadow.png"
         x="868" y="-1998" width="170" height="2780" preserveAspectRatio="none" clip-path="url(#winDigit4)"/>

  <!-- Slot-window sheen: overlays, not masks, so they remain PPT-editable. -->
  <rect x="180" y="78" width="880" height="64" fill="url(#topDigitFade)" opacity="0.55"/>
  <rect x="180" y="296" width="880" height="70" fill="url(#bottomDigitFade)" opacity="0.42"/>

  <text x="1072" y="352" width="150"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="104" font-weight="300"
        fill="#ffffff" filter="url(#softTextShadow)">m</text>

  <text x="54" y="650" width="460"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="26" font-weight="400"
        letter-spacing="11" fill="#ffffff" opacity="0.78">MOUNT EVEREST</text>

  <!-- China flag -->
  <g filter="url(#flagShadow)">
    <rect x="1018" y="596" width="78" height="49" fill="#e60012"/>
    <path d="M1031 604 L1034 611 L1042 611 L1036 616 L1038 624 L1031 619 L1024 624 L1026 616 L1020 611 L1028 611 Z"
          fill="#ffde00"/>
    <circle cx="1048" cy="608" r="2.2" fill="#ffde00"/>
    <circle cx="1058" cy="616" r="2.2" fill="#ffde00"/>
    <circle cx="1058" cy="629" r="2.2" fill="#ffde00"/>
    <circle cx="1048" cy="637" r="2.2" fill="#ffde00"/>
  </g>

  <!-- Nepal flag simplified as native editable paths -->
  <g filter="url(#flagShadow)">
    <path d="M1124 596 L1200 596 L1154 622 L1200 645 L1124 645 Z" fill="#ffffff"/>
    <path d="M1128 600 L1186 600 L1148 621 L1188 641 L1128 641 Z" fill="#003893"/>
    <path d="M1133 606 L1166 618 L1133 618 Z" fill="#dc143c"/>
    <path d="M1133 623 L1172 638 L1133 638 Z" fill="#dc143c"/>
    <circle cx="1145" cy="614" r="5" fill="#ffffff"/>
    <path d="M1145 629 L1148 635 L1155 635 L1150 639 L1152 645 L1145 641 L1138 645 L1140 639 L1135 635 L1142 635 Z"
          fill="#ffffff"/>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<animate>` or `<animateTransform>` for the roll; create two PPT slides and let PowerPoint Morph interpolate the strip positions.
- ❌ Do not try to clip live `<text>` digits or a `<g>` of text; PPT-Master only preserves clipping reliably on `<image>`, so pre-render the 0–9 digit strip as a transparent PNG.
- ❌ Do not use SVG `<mask>` to fade the top/bottom of the number window; use semi-transparent gradient `<rect>` overlays instead.
- ❌ Do not make the entire number one image if the digits must roll independently; each digit needs its own strip object and fixed crop window.
- ❌ Do not change object sizes between the start and end slide unless intentional; Morph is cleanest when only the digit-strip y-offset changes.

## Composition notes
- Keep the rolling number in the upper-middle third, spanning roughly 65–75% of slide width; the background photo should support the drama without competing with the digits.
- The digit windows stay fixed across both Morph slides. Only the vertical `y` position of each clipped digit-strip image changes.
- Use white digits with pre-baked black shadow in the strip image; this preserves readability over complex photography.
- Static context labels, units, and flags should be small and peripheral so the odometer reveal remains the hero moment.