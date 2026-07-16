# SVG Recipe — Trifold Panoramic Gradient Blend

## Visual mechanism
A strict three-column brochure grid is softened by a single panoramic photograph clipped into a broad bottom arch. Three column-colored vertical gradients wash over the photo from above, making the image fade naturally into the trifold background instead of appearing as a hard-edged picture strip.

## SVG primitives needed
- 3× `<rect>` for the white / mustard / white trifold background panels
- 1× `<image>` for the panoramic cityscape or landscape photo spanning the full slide
- 1× `<clipPath>` with 1× `<path>` for the sweeping arched photo crop
- 3× `<rect>` with vertical `<linearGradient>` fills for the per-column fade overlays
- 2× `<circle>` for dark green circular corner-sector accents
- 2× `<line>` for subtle column dividers
- 6× `<circle>` for left-column bullet anchors
- 1× `<filter>` with offset blur shadow for the small center KPI card
- 1× `<rect>` for the KPI card
- Multiple `<text>` elements with explicit `width` attributes for headings, body copy, numbers, and labels

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="archClip" clipPathUnits="userSpaceOnUse">
      <path d="M0,720 L1280,720 L1280,455
               C1115,305 900,245 640,245
               C380,245 165,305 0,455 Z"/>
    </clipPath>

    <linearGradient id="fadeWhite" x1="0" y1="230" x2="0" y2="590" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="1"/>
      <stop offset="42%" stop-color="#FFFFFF" stop-opacity="0.78"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="fadeYellow" x1="0" y1="230" x2="0" y2="590" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#F4B41A" stop-opacity="1"/>
      <stop offset="45%" stop-color="#F4B41A" stop-opacity="0.76"/>
      <stop offset="100%" stop-color="#F4B41A" stop-opacity="0"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Trifold base panels -->
  <rect x="0" y="0" width="426.67" height="720" fill="#FFFFFF"/>
  <rect x="426.67" y="0" width="426.66" height="720" fill="#F4B41A"/>
  <rect x="853.33" y="0" width="426.67" height="720" fill="#FFFFFF"/>

  <!-- Subtle fold lines -->
  <line x1="426.67" y1="0" x2="426.67" y2="720" stroke="#1E6B52" stroke-opacity="0.14" stroke-width="1"/>
  <line x1="853.33" y1="0" x2="853.33" y2="720" stroke="#1E6B52" stroke-opacity="0.14" stroke-width="1"/>

  <!-- Panoramic arched image -->
  <image href="https://images.example.com/panoramic-modern-city-skyline-at-golden-hour.jpg"
         x="0" y="210" width="1280" height="560"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#archClip)"/>

  <!-- Column-colored gradient washes that create the photo-to-background blend -->
  <rect x="0" y="220" width="426.67" height="390" fill="url(#fadeWhite)"/>
  <rect x="426.67" y="220" width="426.66" height="390" fill="url(#fadeYellow)"/>
  <rect x="853.33" y="220" width="426.67" height="390" fill="url(#fadeWhite)"/>

  <!-- Dark green circular sector accents -->
  <circle cx="-28" cy="742" r="230" fill="#1E6B52"/>
  <circle cx="1308" cy="742" r="230" fill="#1E6B52"/>

  <!-- Left column copy -->
  <text x="70" y="72" width="290" font-family="Segoe UI, Microsoft YaHei" font-size="16" letter-spacing="3" fill="#1E6B52" font-weight="700">
    MARKET VIEW
  </text>
  <text x="70" y="118" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="34" fill="#333333" font-weight="700">
    <tspan x="70" dy="0">Urban Growth</tspan>
    <tspan x="70" dy="40">Snapshot</tspan>
  </text>

  <circle cx="78" cy="214" r="8" fill="#1E6B52"/>
  <text x="100" y="220" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#333333">
    Mixed-use districts are driving a higher share of premium leasing demand.
  </text>

  <circle cx="78" cy="290" r="8" fill="#1E6B52"/>
  <text x="100" y="296" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#333333">
    Transit-oriented hubs continue to outperform suburban office inventory.
  </text>

  <circle cx="78" cy="366" r="8" fill="#1E6B52"/>
  <text x="100" y="372" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#333333">
    Hospitality, retail, and civic spaces are converging into one experience layer.
  </text>

  <!-- Center column headline and KPI card -->
  <text x="640" y="78" width="330" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" letter-spacing="3" fill="#1E6B52" font-weight="700">
    2026 OUTLOOK
  </text>
  <text x="640" y="137" width="330" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="42" fill="#FFFFFF" font-weight="800">
    <tspan x="640" dy="0">TRIFOLD</tspan>
    <tspan x="640" dy="46">PORTFOLIO</tspan>
  </text>

  <rect x="520" y="244" width="240" height="96" rx="24" fill="#FFFFFF" fill-opacity="0.92" filter="url(#softShadow)"/>
  <text x="640" y="282" width="220" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="38" fill="#1E6B52" font-weight="800">
    +18%
  </text>
  <text x="640" y="314" width="220" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" letter-spacing="1.5" fill="#333333" font-weight="700">
    YOY VALUE UPLIFT
  </text>

  <!-- Right column copy -->
  <text x="1210" y="72" width="300" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="16" letter-spacing="3" fill="#1E6B52" font-weight="700">
    PRIORITIES
  </text>
  <text x="1210" y="122" width="310" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="32" fill="#333333" font-weight="700">
    <tspan x="1210" dy="0">Three Moves</tspan>
    <tspan x="1210" dy="38">to Scale</tspan>
  </text>

  <text x="1210" y="214" width="310" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#333333" font-weight="700">
    01  Reposition core assets
  </text>
  <text x="1210" y="255" width="310" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#555555">
    Upgrade amenities and public-facing ground floors to increase dwell time.
  </text>

  <text x="1210" y="326" width="310" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#333333" font-weight="700">
    02  Connect mobility nodes
  </text>
  <text x="1210" y="367" width="310" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#555555">
    Prioritize sites with high-frequency transit and walkable catchments.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<mask>` or `mask="url(...)"` to create the photo fade; masks are not reliable in the target PowerPoint translation.
- ❌ Do not apply `clip-path` to gradient rectangles or vector shapes; keep clipping only on the `<image>`.
- ❌ Do not split the arched photo into three unrelated images; the panoramic continuity is the signature of the technique.
- ❌ Do not place text underneath the fade overlays; all typography should sit above the photo/fade stack for clean readability.
- ❌ Do not use `<pattern>` fills for the background panels; use solid rectangles and gradients instead.

## Composition notes
- Keep the three columns exact: left `0–426.67`, center `426.67–853.33`, right `853.33–1280`.
- The photo should begin visually around the vertical midpoint, with the arch crest near `y=245` and the strongest image visibility below `y=520`.
- Use the mustard center panel as the energetic focal zone; balance it with dark green accents and mostly neutral text in the white side panels.
- Leave generous upper whitespace in each column so the bottom panoramic arch feels like an integrated editorial image, not a background wallpaper.