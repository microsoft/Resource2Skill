# SVG Recipe — Slanted Geometric Corporate Framing

## Visual mechanism
A clean corporate slide is given momentum by large navy polygons cutting diagonally across the canvas, with thin parallel red/gold accent bands echoing the same angle. The diagonal frame anchors titles or data while a clipped photo and compact chart content remain crisp in the open white space.

## SVG primitives needed
- 1× `<rect>` for the white slide background
- 1× `<image>` for a corporate hero photo, clipped into an angled top-right geometric panel
- 1× `<clipPath>` with a `<path>` for the slanted photo crop
- 4× large `<path>` polygons for the navy corner frame, top-right wedge, and red/gold diagonal accent bands
- 1× `<linearGradient>` for the navy frame fill
- 1× `<filter id="softShadow">` for the editable content card shadow
- 1× `<rect>` for the rounded white data card
- 8× `<line>` for chart gridlines, axes, and small separators
- 6× `<rect>` for editable vertical chart bars
- 2× `<path>` for the chart trend line and small corporate chevron detail
- Multiple `<text>` elements with explicit `width` for title, subtitle, labels, metrics, and chart annotations

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="navyGrad" x1="0" y1="260" x2="760" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#21466F"/>
      <stop offset="0.55" stop-color="#1A365D"/>
      <stop offset="1" stop-color="#122841"/>
    </linearGradient>

    <linearGradient id="photoFade" x1="650" y1="0" x2="1280" y2="480" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#1A365D" stop-opacity="0.15"/>
      <stop offset="1" stop-color="#1A365D" stop-opacity="0.55"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="14"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.05  0 0 0 0 0.08  0 0 0 0 0.12  0 0 0 0.20 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="heroClip">
      <path d="M610 0 H1280 V405 L865 520 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <image
    href="https://images.unsplash.com/photo-1497366754035-f200968a6e72?q=80&w=1600&auto=format&fit=crop"
    x="560" y="0" width="760" height="540"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#heroClip)"/>

  <path d="M610 0 H1280 V405 L865 520 Z" fill="url(#photoFade)" opacity="0.92"/>

  <path d="M0 720 L0 286 L872 720 Z" fill="url(#navyGrad)"/>
  <path d="M0 270 L0 247 L916 720 L868 720 Z" fill="#9B2C2C"/>
  <path d="M0 232 L0 220 L960 720 L935 720 Z" fill="#D69E2E"/>
  <path d="M1280 0 L1095 0 L1280 128 Z" fill="#1A365D"/>
  <path d="M1188 0 L1156 0 L1280 86 L1280 108 Z" fill="#D69E2E"/>

  <path d="M73 538 L112 538 L97 560 L128 560 L83 615 L98 578 L65 578 Z" fill="#D69E2E" opacity="0.95"/>

  <text x="76" y="404" width="560" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="54" font-weight="700" fill="#FFFFFF">
    <tspan x="76" dy="0">Sales Performance</tspan>
    <tspan x="76" dy="64">Review</tspan>
  </text>
  <text x="80" y="535" width="500" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="400" fill="#DDE7F2">
    Q4 Financial Overview &amp; 2026 Strategy
  </text>
  <text x="80" y="584" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="600" letter-spacing="2" fill="#D69E2E">
    EXECUTIVE BRIEFING
  </text>

  <rect x="684" y="330" width="470" height="286" rx="22" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="724" y="378" width="300" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="25" font-weight="700" fill="#1A365D">
    Regional Revenue Mix
  </text>
  <text x="724" y="407" width="340" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#64748B">
    Quarterly performance by market, USD millions
  </text>

  <line x1="730" y1="545" x2="1095" y2="545" stroke="#CBD5E1" stroke-width="1"/>
  <line x1="730" y1="500" x2="1095" y2="500" stroke="#E2E8F0" stroke-width="1" stroke-dasharray="5 7"/>
  <line x1="730" y1="455" x2="1095" y2="455" stroke="#E2E8F0" stroke-width="1" stroke-dasharray="5 7"/>
  <line x1="730" y1="410" x2="1095" y2="410" stroke="#E2E8F0" stroke-width="1" stroke-dasharray="5 7"/>
  <line x1="730" y1="410" x2="730" y2="545" stroke="#CBD5E1" stroke-width="1"/>

  <rect x="766" y="488" width="34" height="57" rx="5" fill="#1A365D"/>
  <rect x="826" y="456" width="34" height="89" rx="5" fill="#1A365D"/>
  <rect x="886" y="474" width="34" height="71" rx="5" fill="#1A365D"/>
  <rect x="946" y="432" width="34" height="113" rx="5" fill="#9B2C2C"/>
  <rect x="1006" y="448" width="34" height="97" rx="5" fill="#1A365D"/>
  <rect x="1066" y="420" width="34" height="125" rx="5" fill="#D69E2E"/>

  <path d="M783 475 L843 442 L903 463 L963 414 L1023 432 L1083 397" fill="none" stroke="#D69E2E" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="783" cy="475" r="5" fill="#D69E2E"/>
  <circle cx="843" cy="442" r="5" fill="#D69E2E"/>
  <circle cx="903" cy="463" r="5" fill="#D69E2E"/>
  <circle cx="963" cy="414" r="5" fill="#D69E2E"/>
  <circle cx="1023" cy="432" r="5" fill="#D69E2E"/>
  <circle cx="1083" cy="397" r="5" fill="#D69E2E"/>

  <text x="754" y="572" width="58" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" text-anchor="middle" fill="#64748B">North</text>
  <text x="814" y="572" width="58" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" text-anchor="middle" fill="#64748B">West</text>
  <text x="874" y="572" width="58" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" text-anchor="middle" fill="#64748B">APAC</text>
  <text x="934" y="572" width="58" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" text-anchor="middle" fill="#64748B">EMEA</text>
  <text x="994" y="572" width="58" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" text-anchor="middle" fill="#64748B">LATAM</text>
  <text x="1054" y="572" width="58" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" text-anchor="middle" fill="#64748B">Digital</text>

  <rect x="1088" y="356" width="42" height="8" rx="4" fill="#9B2C2C"/>
  <rect x="1088" y="372" width="42" height="8" rx="4" fill="#D69E2E"/>
  <text x="724" y="598" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600" fill="#1A365D">
    +18.6% YoY growth, strongest digital contribution
  </text>
</svg>
```

## Avoid in this skill
- ❌ Rectangular frames only; the style depends on sharp custom `<path>` polygons with consistent diagonal angles.
- ❌ `clip-path` on rectangles or paths for decorative overlays; use explicit polygon paths instead, and reserve `clipPath` for the hero `<image>`.
- ❌ `marker-end` arrows on diagonal accents; if arrows are needed, build them from editable lines and small path triangles.
- ❌ Low-contrast accent bands over busy photos; keep red/gold bands on white or navy for premium corporate clarity.
- ❌ Skew transforms or matrix transforms to fake slants; draw the slanted geometry directly with path coordinates.

## Composition notes
- Keep the main navy polygon anchored to one corner and let it cover roughly 30–40% of the slide on title/section slides, or 10–20% on content slides.
- Make accent bands perfectly parallel to the main cut; small angle mismatches immediately weaken the template discipline.
- Reserve the white/top-right region for charts, KPIs, or a clipped corporate photo so the heavy navy area does not compete with data.
- Use navy as the dominant brand color, then deploy brick red and mustard gold sparingly as motion lines, highlights, or one emphasized data series.