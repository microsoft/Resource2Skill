# SVG Recipe — Metric Split with Image

## Visual mechanism
A restrained editorial split pairs one oversized KPI on the left with a rounded, clipped contextual image on the right. Thin horizontal rules, generous whitespace, and a small accent color make the metric feel like the headline of an executive dashboard rather than a dense chart.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 2× `<line>` for top title-section divider rules
- 1× `<line>` for the subtle vertical split between metric and image
- 2× `<rect>` for accent chips behind the eyebrow label and metric footnote
- 1× `<rect>` for the rounded image card shadow receiver
- 1× `<image>` clipped to a rounded rectangle for the 4:3 visual context
- 1× `<rect>` for the rounded image border
- 2× `<path>` for soft editorial accent shapes behind the metric and image
- 5× `<text>` blocks for title, section label, metric label, metric value, and explanatory footnote
- 1× `<linearGradient>` for the background wash
- 1× `<linearGradient>` for the metric accent shape
- 1× `<filter id="cardShadow">` applied to the image card receiver
- 1× `<clipPath>` with rounded `<rect>` applied to the `<image>`

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8FAFC"/>
      <stop offset="62%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#EEF4F8"/>
    </linearGradient>

    <linearGradient id="metricGlow" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#D7F4EA" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="#DDEBFF" stop-opacity="0.55"/>
    </linearGradient>

    <filter id="cardShadow" x="-15%" y="-15%" width="130%" height="130%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="imageRoundClip">
      <rect x="736" y="228" width="420" height="315" rx="28" ry="28"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <path d="M-45 558 C98 498 210 493 316 542 C414 588 480 580 560 520 L560 720 L-45 720 Z"
        fill="url(#metricGlow)" opacity="0.68"/>
  <path d="M930 95 C1034 49 1148 60 1237 130 C1293 174 1314 238 1296 310 C1251 259 1183 247 1110 275 C1018 310 948 288 906 218 C880 174 887 125 930 95 Z"
        fill="#EAF1FF" opacity="0.65"/>

  <line x1="80" y1="94" x2="1200" y2="94" stroke="#CBD5E1" stroke-width="1.2"/>
  <line x1="80" y1="166" x2="1200" y2="166" stroke="#CBD5E1" stroke-width="1.2"/>

  <text x="80" y="140" width="820"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="34" font-weight="650" fill="#111827" letter-spacing="-0.5">
    Revenue momentum after premium launch
  </text>

  <rect x="80" y="226" width="118" height="34" rx="17" fill="#ECFDF5"/>
  <text x="100" y="249" width="180"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="700" fill="#047857" letter-spacing="1.4">
    Q4 KPI
  </text>

  <text x="80" y="313" width="430"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="28" font-weight="600" fill="#334155">
    Net recurring revenue
  </text>

  <text x="76" y="428" width="520"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="104" font-weight="750" fill="#0F172A" letter-spacing="-5">
    $48.2M
  </text>

  <rect x="84" y="475" width="364" height="48" rx="24" fill="#F1F5F9"/>
  <text x="110" y="506" width="330"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="600" fill="#475569">
    +18.6% year over year · 92% gross retention
  </text>

  <text x="82" y="585" width="450"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" font-weight="400" fill="#64748B">
    Premium accounts expanded faster than forecast, offsetting slower mid-market bookings.
  </text>

  <line x1="640" y1="218" x2="640" y2="592" stroke="#D6DEE8" stroke-width="1.4"/>

  <rect x="736" y="228" width="420" height="315" rx="28" ry="28"
        fill="#FFFFFF" filter="url(#cardShadow)"/>
  <image x="736" y="228" width="420" height="315"
         href="https://images.example.com/premium-retail-team-reviewing-dashboard-4x3.jpg"
         clip-path="url(#imageRoundClip)" preserveAspectRatio="xMidYMid slice"/>
  <rect x="736" y="228" width="420" height="315" rx="28" ry="28"
        fill="none" stroke="#FFFFFF" stroke-width="5"/>

  <rect x="770" y="494" width="230" height="34" rx="17" fill="#0F172A" opacity="0.86"/>
  <text x="790" y="517" width="210"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="650" fill="#FFFFFF">
    Visual context: enterprise adoption
  </text>
</svg>
```

## Avoid in this skill
- ❌ Dense multi-metric dashboards; this shell is for one hero number only.
- ❌ Placing the KPI over the photo; keep the metric and image in clearly separated zones for executive readability.
- ❌ Unclipped rectangular photos with hard corners; the rounded 4:3 card is part of the premium editorial feel.
- ❌ Applying shadows or filters to divider `<line>` elements; use shadows only on rectangles, paths, text, ellipses, or circles.
- ❌ Image crops using masks; use `<clipPath>` on the `<image>` only.

## Composition notes
- Keep the title band shallow, roughly the top 25% of the slide, with thin rules to create a report-like editorial header.
- Reserve the left 45% for the KPI stack: small eyebrow, metric label, oversized number, then a short evidence note.
- Place the photo card in the right 35–40% with ample breathing room; it should support the metric, not compete with it.
- Use one accent color sparingly for the KPI chip and soft background shape; keep the rest neutral with slate text and pale dividers.