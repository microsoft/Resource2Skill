# SVG Recipe — Segmented KPI Progress Gauge

## Visual mechanism
A percentage KPI is encoded as a 10-block circular donut, where each arc segment represents 10% and can be independently colored. A central value plus up/down arrow adds immediate quantitative and directional meaning, making several KPIs easy to compare at executive-dashboard speed.

## SVG primitives needed
- 3× `<rect>` for elevated KPI cards
- 1× `<rect>` for full-slide gradient background
- 30× `<path>` for editable annular donut segments, 10 per KPI gauge
- 3× `<circle>` for clean white center wells inside each donut
- 3× `<path>` for central trend arrows
- 13× `<text>` for slide title, card labels, central percentages, KPI names, and descriptions
- 2× `<linearGradient>` for premium background and card accent fills
- 1× `<radialGradient>` for soft dashboard glow
- 1× `<filter id="softShadow">` applied to card rectangles for depth

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#F8FAFC"/>
      <stop offset="0.55" stop-color="#EEF3F8"/>
      <stop offset="1" stop-color="#E7ECF3"/>
    </linearGradient>
    <radialGradient id="glow" cx="50%" cy="12%" r="75%">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.95"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="cardAccent" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#FFFFFF"/>
      <stop offset="1" stop-color="#F7FAFD"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <ellipse cx="640" cy="70" rx="520" ry="220" fill="url(#glow)"/>
  <text x="70" y="76" width="820" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#172033">Quarterly Performance Snapshot</text>
  <text x="72" y="112" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#667085">Segmented KPI gauges show progress magnitude, trend direction, and performance quality in one compact visual.</text>

  <rect x="56" y="152" width="360" height="500" rx="28" fill="url(#cardAccent)" filter="url(#softShadow)"/>
  <rect x="460" y="152" width="360" height="500" rx="28" fill="url(#cardAccent)" filter="url(#softShadow)"/>
  <rect x="864" y="152" width="360" height="500" rx="28" fill="url(#cardAccent)" filter="url(#softShadow)"/>

  <text x="92" y="205" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" letter-spacing="1.5" fill="#76B82B">GROWTH</text>
  <text x="496" y="205" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" letter-spacing="1.5" fill="#F94144">RISK</text>
  <text x="900" y="205" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" letter-spacing="1.5" fill="#17A673">EXECUTION</text>

  <g transform="translate(236 318)">
    <path d="M 2.4 -68 A 68 68 0 0 1 38 -56.4 L 26.8 -39.8 A 48 48 0 0 0 1.7 -48 Z" fill="#76B82B"/>
    <path d="M 2.4 -68 A 68 68 0 0 1 38 -56.4 L 26.8 -39.8 A 48 48 0 0 0 1.7 -48 Z" transform="rotate(36)" fill="#76B82B"/>
    <path d="M 2.4 -68 A 68 68 0 0 1 38 -56.4 L 26.8 -39.8 A 48 48 0 0 0 1.7 -48 Z" transform="rotate(72)" fill="#76B82B"/>
    <path d="M 2.4 -68 A 68 68 0 0 1 38 -56.4 L 26.8 -39.8 A 48 48 0 0 0 1.7 -48 Z" transform="rotate(108)" fill="#76B82B"/>
    <path d="M 2.4 -68 A 68 68 0 0 1 38 -56.4 L 26.8 -39.8 A 48 48 0 0 0 1.7 -48 Z" transform="rotate(144)" fill="#76B82B"/>
    <path d="M 2.4 -68 A 68 68 0 0 1 38 -56.4 L 26.8 -39.8 A 48 48 0 0 0 1.7 -48 Z" transform="rotate(180)" fill="#76B82B"/>
    <path d="M 2.4 -68 A 68 68 0 0 1 38 -56.4 L 26.8 -39.8 A 48 48 0 0 0 1.7 -48 Z" transform="rotate(216)" fill="#76B82B"/>
    <path d="M 2.4 -68 A 68 68 0 0 1 38 -56.4 L 26.8 -39.8 A 48 48 0 0 0 1.7 -48 Z" transform="rotate(252)" fill="#E6E9EE"/>
    <path d="M 2.4 -68 A 68 68 0 0 1 38 -56.4 L 26.8 -39.8 A 48 48 0 0 0 1.7 -48 Z" transform="rotate(288)" fill="#E6E9EE"/>
    <path d="M 2.4 -68 A 68 68 0 0 1 38 -56.4 L 26.8 -39.8 A 48 48 0 0 0 1.7 -48 Z" transform="rotate(324)" fill="#E6E9EE"/>
    <circle cx="0" cy="0" r="42" fill="#FFFFFF"/>
    <text x="0" y="-4" width="96" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="800" fill="#1E293B">72%</text>
    <path d="M 0 8 L -15 30 L 15 30 Z" fill="#76B82B"/>
  </g>

  <g transform="translate(640 318)">
    <path d="M 2.4 -68 A 68 68 0 0 1 38 -56.4 L 26.8 -39.8 A 48 48 0 0 0 1.7 -48 Z" fill="#E6E9EE"/>
    <path d="M 2.4 -68 A 68 68 0 0 1 38 -56.4 L 26.8 -39.8 A 48 48 0 0 0 1.7 -48 Z" transform="rotate(36)" fill="#E6E9EE"/>
    <path d="M 2.4 -68 A 68 68 0 0 1 38 -56.4 L 26.8 -39.8 A 48 48 0 0 0 1.7 -48 Z" transform="rotate(72)" fill="#E6E9EE"/>
    <path d="M 2.4 -68 A 68 68 0 0 1 38 -56.4 L 26.8 -39.8 A 48 48 0 0 0 1.7 -48 Z" transform="rotate(108)" fill="#E6E9EE"/>
    <path d="M 2.4 -68 A 68 68 0 0 1 38 -56.4 L 26.8 -39.8 A 48 48 0 0 0 1.7 -48 Z" transform="rotate(144)" fill="#E6E9EE"/>
    <path d="M 2.4 -68 A 68 68 0 0 1 38 -56.4 L 26.8 -39.8 A 48 48 0 0 0 1.7 -48 Z" transform="rotate(180)" fill="#E6E9EE"/>
    <path d="M 2.4 -68 A 68 68 0 0 1 38 -56.4 L 26.8 -39.8 A 48 48 0 0 0 1.7 -48 Z" transform="rotate(216)" fill="#F94144"/>
    <path d="M 2.4 -68 A 68 68 0 0 1 38 -56.4 L 26.8 -39.8 A 48 48 0 0 0 1.7 -48 Z" transform="rotate(252)" fill="#F94144"/>
    <path d="M 2.4 -68 A 68 68 0 0 1 38 -56.4 L 26.8 -39.8 A 48 48 0 0 0 1.7 -48 Z" transform="rotate(288)" fill="#F94144"/>
    <path d="M 2.4 -68 A 68 68 0 0 1 38 -56.4 L 26.8 -39.8 A 48 48 0 0 0 1.7 -48 Z" transform="rotate(324)" fill="#F94144"/>
    <circle cx="0" cy="0" r="42" fill="#FFFFFF"/>
    <text x="0" y="-4" width="96" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="800" fill="#1E293B">43%</text>
    <path d="M 0 30 L -15 8 L 15 8 Z" fill="#F94144"/>
  </g>

  <g transform="translate(1044 318)">
    <path d="M 2.4 -68 A 68 68 0 0 1 38 -56.4 L 26.8 -39.8 A 48 48 0 0 0 1.7 -48 Z" fill="#17A673"/>
    <path d="M 2.4 -68 A 68 68 0 0 1 38 -56.4 L 26.8 -39.8 A 48 48 0 0 0 1.7 -48 Z" transform="rotate(36)" fill="#17A673"/>
    <path d="M 2.4 -68 A 68 68 0 0 1 38 -56.4 L 26.8 -39.8 A 48 48 0 0 0 1.7 -48 Z" transform="rotate(72)" fill="#17A673"/>
    <path d="M 2.4 -68 A 68 68 0 0 1 38 -56.4 L 26.8 -39.8 A 48 48 0 0 0 1.7 -48 Z" transform="rotate(108)" fill="#17A673"/>
    <path d="M 2.4 -68 A 68 68 0 0 1 38 -56.4 L 26.8 -39.8 A 48 48 0 0 0 1.7 -48 Z" transform="rotate(144)" fill="#17A673"/>
    <path d="M 2.4 -68 A 68 68 0 0 1 38 -56.4 L 26.8 -39.8 A 48 48 0 0 0 1.7 -48 Z" transform="rotate(180)" fill="#17A673"/>
    <path d="M 2.4 -68 A 68 68 0 0 1 38 -56.4 L 26.8 -39.8 A 48 48 0 0 0 1.7 -48 Z" transform="rotate(216)" fill="#17A673"/>
    <path d="M 2.4 -68 A 68 68 0 0 1 38 -56.4 L 26.8 -39.8 A 48 48 0 0 0 1.7 -48 Z" transform="rotate(252)" fill="#17A673"/>
    <path d="M 2.4 -68 A 68 68 0 0 1 38 -56.4 L 26.8 -39.8 A 48 48 0 0 0 1.7 -48 Z" transform="rotate(288)" fill="#17A673"/>
    <path d="M 2.4 -68 A 68 68 0 0 1 38 -56.4 L 26.8 -39.8 A 48 48 0 0 0 1.7 -48 Z" transform="rotate(324)" fill="#E6E9EE"/>
    <circle cx="0" cy="0" r="42" fill="#FFFFFF"/>
    <text x="0" y="-4" width="96" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="800" fill="#1E293B">91%</text>
    <path d="M 0 8 L -15 30 L 15 30 Z" fill="#17A673"/>
  </g>

  <text x="92" y="455" width="290" font-family="Segoe UI, Microsoft YaHei" font-size="23" font-weight="800" fill="#172033">Annual Recurring Revenue</text>
  <text x="92" y="492" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#5B6472">Seven segments filled clockwise signals strong progress toward the quarter target.</text>
  <text x="496" y="455" width="290" font-family="Segoe UI, Microsoft YaHei" font-size="23" font-weight="800" fill="#172033">Customer Churn Exposure</text>
  <text x="496" y="492" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#5B6472">Red segments fill anti-clockwise to reinforce a negative trend requiring intervention.</text>
  <text x="900" y="455" width="290" font-family="Segoe UI, Microsoft YaHei" font-size="23" font-weight="800" fill="#172033">Roadmap Delivery</text>
  <text x="900" y="492" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#5B6472">Nine completed blocks create instant confidence while leaving visible room to finish.</text>
</svg>
```

## Avoid in this skill
- ❌ Using one dashed `<circle>` for the whole gauge when segments need independent colors and editability.
- ❌ Using `<use>` to duplicate arc segments; duplicate the `<path>` elements directly or generate them explicitly.
- ❌ Applying `marker-end` to a path for the central arrow; make the arrow as a filled triangle `<path>`.
- ❌ Relying on masks or clip paths to carve the donut hole; build true annular segment paths and place a white center circle if needed.
- ❌ Omitting `width` on KPI labels or percentages; PowerPoint text boxes need explicit widths for clean rendering.

## Composition notes
- Keep each gauge large enough to read at a glance: a 130–160 px outer diameter works well for three cards across a 16:9 slide.
- Use clockwise filled segments for positive movement and anti-clockwise filled segments for negative movement.
- Reserve the donut center for only the primary value and arrow; put KPI names and explanations outside the ring.
- Use neutral gray for unfilled blocks so the colored segments become the visual rhythm across the dashboard.