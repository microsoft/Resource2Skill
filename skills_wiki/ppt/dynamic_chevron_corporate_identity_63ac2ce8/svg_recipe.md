# SVG Recipe — Dynamic Chevron Corporate Identity

## Visual mechanism
A large corporate photo is clipped into a sharp right-pointing pentagon, then extended by parallel chevron bands that echo the same diagonal angle. The bottom fifth of the slide remains calm and white, creating an executive title zone that contrasts with the energetic geometry above.

## SVG primitives needed
- 2× `<rect>` for the white background and subtle footer separator band
- 1× `<image>` for the hero photo, clipped into a right-pointing pentagon
- 1× `<clipPath>` with a `<polygon>` for the custom photo crop
- 1× `<path>` for the transparent teal overlay on top of the photo
- 4× `<path>` for the editable colored chevron bands
- 3× `<path>` for crisp white diagonal separators and highlight strokes
- 1× `<line>` for the horizontal title rule
- 4× `<text>` elements for kicker, title, subtitle, and right-side section label
- 4× `<linearGradient>` definitions for refined corporate band fills
- 1× `<filter id="softShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` applied to chevron paths

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="heroChevronClip">
      <polygon points="0,0 480,0 672,288 480,576 0,576"/>
    </clipPath>

    <linearGradient id="photoTint" x1="0" y1="0" x2="672" y2="576" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#1F4F55" stop-opacity="0.10"/>
      <stop offset="0.58" stop-color="#498E8D" stop-opacity="0.28"/>
      <stop offset="1" stop-color="#152F34" stop-opacity="0.42"/>
    </linearGradient>

    <linearGradient id="goldBand" x1="510" y1="0" x2="830" y2="576" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#D6C38A"/>
      <stop offset="1" stop-color="#BAA36E"/>
    </linearGradient>

    <linearGradient id="coralBand" x1="658" y1="0" x2="970" y2="576" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#D89292"/>
      <stop offset="1" stop-color="#C17D7D"/>
    </linearGradient>

    <linearGradient id="sageBand" x1="806" y1="0" x2="1120" y2="576" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#A7CFA1"/>
      <stop offset="1" stop-color="#8EBA8D"/>
    </linearGradient>

    <linearGradient id="tealBand" x1="954" y1="0" x2="1280" y2="576" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#5EA5A2"/>
      <stop offset="1" stop-color="#498E8D"/>
    </linearGradient>

    <filter id="softShadow" x="-10%" y="-10%" width="130%" height="130%">
      <feOffset dx="0" dy="8" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>
  <rect x="0" y="576" width="1280" height="144" fill="#FFFFFF"/>

  <image
    href="https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&amp;fit=crop&amp;w=1800&amp;q=80"
    xlink:href="https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&amp;fit=crop&amp;w=1800&amp;q=80"
    x="0" y="0" width="672" height="576"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#heroChevronClip)"/>

  <path d="M0 0 L480 0 L672 288 L480 576 L0 576 Z" fill="url(#photoTint)"/>
  <path d="M480 0 L672 288 L480 576" fill="none" stroke="#FFFFFF" stroke-width="14" stroke-opacity="0.96"/>

  <path d="M510 0 L630 0 L822 288 L630 576 L510 576 L702 288 Z"
        fill="url(#goldBand)" filter="url(#softShadow)"/>
  <path d="M658 0 L778 0 L970 288 L778 576 L658 576 L850 288 Z"
        fill="url(#coralBand)" filter="url(#softShadow)"/>
  <path d="M806 0 L926 0 L1118 288 L926 576 L806 576 L998 288 Z"
        fill="url(#sageBand)" filter="url(#softShadow)"/>
  <path d="M954 0 L1074 0 L1266 288 L1074 576 L954 576 L1146 288 Z"
        fill="url(#tealBand)" filter="url(#softShadow)"/>

  <path d="M510 0 L702 288 L510 576" fill="none" stroke="#FFFFFF" stroke-width="10" stroke-opacity="0.90"/>
  <path d="M658 0 L850 288 L658 576" fill="none" stroke="#FFFFFF" stroke-width="10" stroke-opacity="0.88"/>
  <path d="M806 0 L998 288 L806 576" fill="none" stroke="#FFFFFF" stroke-width="10" stroke-opacity="0.84"/>

  <line x1="64" y1="604" x2="286" y2="604" stroke="#BAA36E" stroke-width="8"/>
  <text x="64" y="636" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700"
        letter-spacing="2" fill="#498E8D">FY2026 EXECUTIVE REVIEW</text>
  <text x="64" y="674" width="820" font-family="Segoe UI, Microsoft YaHei" font-size="48" font-weight="700"
        fill="#498E8D">Customer Service Review</text>
  <text x="66" y="704" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="400"
        fill="#687878">Annual Performance &amp; Strategic Roadmap</text>

  <text x="1188" y="690" width="360" transform="rotate(-90 1188 690)"
        font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700"
        letter-spacing="3" fill="#9AA7A7">STRATEGIC GOALS / CUSTOMER EXPERIENCE</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<mask>` for the hero image; use `<clipPath>` applied directly to the `<image>`.
- ❌ Do not build the chevrons from rotated rectangles with `skewX`, `skewY`, or `matrix()` transforms; draw each band as a native editable `<path>`.
- ❌ Do not apply `clip-path` to the colored chevron vector shapes; PPT-Master only preserves clipping reliably on `<image>`.
- ❌ Do not use marker arrows on paths for the chevron points; the arrowhead will disappear. The arrow geometry must be part of the path itself.
- ❌ Do not crowd the footer with icons or cards; the clean typography zone is what makes the top geometry feel premium.

## Composition notes
- Keep the chevron system in the top 80% of the slide, ending around y=576 on a 1280×720 canvas.
- Let the hero photo occupy the left half visually, with its point reaching toward the slide center; the colored bands should continue the same diagonal rhythm to the right edge.
- Use white gaps and separator strokes between chevrons to make the geometry feel precise and intentional.
- Reserve the bottom 120–145 px for title hierarchy: short rule, small uppercase kicker, large teal title, and subdued subtitle.