# SVG Recipe — Hero Metric Overlay

## Visual mechanism
A full-bleed editorial image is darkened with cinematic gradient scrims so one oversized metric can sit directly on top with high contrast. Supporting copy is minimal: a small label, a hairline accent, and subtle glow/shadow effects make the number feel like the hero object rather than just text.

## SVG primitives needed
- 1× `<image>` for the full-bleed background photo
- 4× `<rect>` for darkening overlays, bottom scrim, label capsule, and accent bar
- 2× `<ellipse>` for soft colored light leaks behind the metric
- 3× `<path>` for subtle editorial contour / motion-line decoration
- 3× `<text>` for the giant metric, short label, and tiny context line
- 2× `<linearGradient>` for image scrims and label capsule
- 1× `<radialGradient>` for the metric-area glow
- 2× `<filter>` definitions: one soft glow for light leaks / metric, one drop shadow for text and label card

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="leftScrim" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#030712" stop-opacity="0.88"/>
      <stop offset="45%" stop-color="#030712" stop-opacity="0.52"/>
      <stop offset="100%" stop-color="#030712" stop-opacity="0.12"/>
    </linearGradient>

    <linearGradient id="bottomScrim" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#030712" stop-opacity="0"/>
      <stop offset="65%" stop-color="#030712" stop-opacity="0.58"/>
      <stop offset="100%" stop-color="#030712" stop-opacity="0.86"/>
    </linearGradient>

    <radialGradient id="cyanAura" cx="38%" cy="54%" r="42%">
      <stop offset="0%" stop-color="#22D3EE" stop-opacity="0.38"/>
      <stop offset="45%" stop-color="#2563EB" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="#030712" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="capsuleFill" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.06"/>
    </linearGradient>

    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="textShadow" x="-20%" y="-20%" width="150%" height="150%">
      <feOffset dx="0" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <image
    href="https://images.example.com/full-bleed-night-city-logistics-hero.jpg"
    x="0" y="0" width="1280" height="720"
    preserveAspectRatio="xMidYMid slice"/>

  <rect x="0" y="0" width="1280" height="720" fill="url(#leftScrim)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#bottomScrim)"/>

  <ellipse cx="395" cy="390" rx="390" ry="250" fill="url(#cyanAura)" filter="url(#softGlow)"/>
  <ellipse cx="1140" cy="110" rx="180" ry="130" fill="#F97316" opacity="0.16" filter="url(#softGlow)"/>

  <path d="M815 92 C930 70 1040 92 1160 50" fill="none" stroke="#FFFFFF" stroke-width="1.3" opacity="0.18"/>
  <path d="M810 132 C930 105 1045 136 1195 86" fill="none" stroke="#67E8F9" stroke-width="1.2" opacity="0.20"/>
  <path d="M855 612 C960 568 1085 628 1225 570" fill="none" stroke="#FFFFFF" stroke-width="1.1" opacity="0.14"/>

  <rect x="72" y="112" width="214" height="42" rx="21" fill="url(#capsuleFill)" stroke="#FFFFFF" stroke-opacity="0.22"/>
  <rect x="72" y="183" width="7" height="298" rx="3.5" fill="#22D3EE"/>

  <text x="98" y="140"
        width="180"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16"
        font-weight="700"
        letter-spacing="2.8"
        fill="#E0F2FE"
        opacity="0.96">FY2026 SIGNAL</text>

  <text x="96" y="425"
        width="760"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="228"
        font-weight="800"
        letter-spacing="-12"
        fill="#FFFFFF"
        filter="url(#textShadow)">73%</text>

  <text x="105" y="505"
        width="560"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="34"
        font-weight="650"
        letter-spacing="-0.8"
        fill="#E5E7EB"
        filter="url(#textShadow)">
    <tspan fill="#67E8F9">Retention lift</tspan>
    <tspan fill="#E5E7EB"> after the new onboarding flow</tspan>
  </text>

  <text x="105" y="640"
        width="520"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16"
        font-weight="500"
        letter-spacing="0.4"
        fill="#CBD5E1"
        opacity="0.78">Source: Q4 cohort analysis · enterprise accounts only</text>
</svg>
```

## Avoid in this skill
- ❌ Do not place the giant metric over the busiest or brightest part of the photo; add a scrim or reposition the image crop instead.
- ❌ Do not use SVG masks for the vignette; use transparent gradient `<rect>` overlays so the result remains editable.
- ❌ Do not omit `width` on `<text>` elements; the metric and label may reflow or clip in PowerPoint.
- ❌ Do not overpopulate the slide with chart furniture, legends, or multiple KPIs; this technique is built around one dramatic number.

## Composition notes
- Keep the metric in the left or lower-left 55–65% of the slide, leaving the photo subject or atmospheric detail visible on the right.
- Use heavy contrast: dark gradient overlays behind white type, with one accent color repeated in the bar, glow, and label emphasis.
- The label should be short and editorial, not explanatory; reserve long sourcing or caveats for small footer text.
- The background photo should feel cinematic and directional, with enough negative space to make the metric readable at presentation distance.