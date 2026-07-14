# SVG Recipe — Tiered Feature Comparison Grid

## Visual mechanism
A polished comparison table uses a strong left-side feature anchor, color-coded tier headers, and high-contrast availability icons so viewers can scan plan differences instantly. Premium styling comes from a soft background, rounded card container, subtle shadows, alternating row fills, and a highlighted “recommended” tier column.

## SVG primitives needed
- 1× `<rect>` full-slide background for a clean canvas.
- 2× decorative `<path>` blobs with translucent gradient fills for executive-keynote depth.
- 1× main rounded `<rect>` card with shadow filter to hold the comparison grid.
- 1× vertical `<rect>` feature rail plus rotated `<text>` for the “FEATURES” anchor.
- 4× tier header `<rect>` blocks with gradient fills.
- 8× row background `<rect>` bands for alternating feature rows.
- 4× subtle column highlight/header/badge elements to emphasize one preferred tier.
- Multiple `<line>` elements for editable table dividers and row separators.
- 8× feature-name `<text>` labels.
- 4× tier-name `<text>` labels and 4× price/positioning `<text>` labels.
- 32× circular `<circle>` icon chips paired with 32× `<text>` check/cross marks.
- 1× `<filter id="softShadow">` applied to the main card and floating badge.
- 3× `<linearGradient>` definitions for background accents and tier headers.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7FBFC"/>
      <stop offset="100%" stop-color="#EEF4F6"/>
    </linearGradient>
    <linearGradient id="tealHeader" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#376F75"/>
      <stop offset="100%" stop-color="#5A9CA1"/>
    </linearGradient>
    <linearGradient id="goldHeader" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#D99422"/>
      <stop offset="100%" stop-color="#F3BE55"/>
    </linearGradient>
    <linearGradient id="blobBlue" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#DCEFF2" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#C7E1E5" stop-opacity="0.25"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>
  <path d="M1014 34 C1135 9 1247 72 1280 164 L1280 0 L1017 0 C992 8 982 20 1014 34 Z" fill="url(#blobBlue)"/>
  <path d="M-40 618 C84 548 177 594 238 716 L0 720 Z" fill="#DCEFF2" opacity="0.65"/>

  <text x="72" y="68" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#2F3A3D">
    Product capability comparison for editing platform tiers
  </text>
  <text x="74" y="99" width="700" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#667276">
    Compare feature depth, automation access, and collaboration controls across plans.
  </text>

  <rect x="830" y="45" width="165" height="34" rx="17" fill="#FFFFFF" stroke="#D7E2E4"/>
  <text x="850" y="67" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#526165">Company: LumaPix</text>
  <rect x="1010" y="45" width="190" height="34" rx="17" fill="#FFFFFF" stroke="#D7E2E4"/>
  <text x="1030" y="67" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#526165">Service: Creator Cloud</text>

  <rect x="70" y="132" width="1140" height="510" rx="26" fill="#FFFFFF" filter="url(#softShadow)"/>
  <rect x="92" y="158" width="66" height="458" rx="20" fill="url(#tealHeader)"/>
  <text x="-566" y="134" width="410" transform="rotate(-90)" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" letter-spacing="3" fill="#FFFFFF">FEATURES</text>

  <rect x="176" y="158" width="300" height="74" rx="16" fill="#F7FAFA"/>
  <text x="202" y="204" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#344246">Capability</text>

  <rect x="496" y="158" width="160" height="74" rx="16" fill="url(#tealHeader)"/>
  <rect x="666" y="146" width="172" height="486" rx="18" fill="#FFF7E8" stroke="#F2C877" stroke-width="2"/>
  <rect x="666" y="158" width="172" height="74" rx="16" fill="url(#goldHeader)"/>
  <rect x="697" y="124" width="110" height="28" rx="14" fill="#2F3A3D" filter="url(#softShadow)"/>
  <text x="716" y="143" width="76" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">BEST VALUE</text>
  <rect x="848" y="158" width="160" height="74" rx="16" fill="url(#tealHeader)"/>
  <rect x="1018" y="158" width="160" height="74" rx="16" fill="url(#tealHeader)"/>

  <text x="526" y="190" width="100" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF">Starter</text>
  <text x="526" y="214" width="100" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#DCEFF2">$19 / mo</text>
  <text x="752" y="190" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF">Growth</text>
  <text x="752" y="214" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#FFF8E9">$49 / mo</text>
  <text x="928" y="190" width="100" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF">Pro</text>
  <text x="928" y="214" width="100" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#DCEFF2">$99 / mo</text>
  <text x="1098" y="190" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF">Enterprise</text>
  <text x="1098" y="214" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#DCEFF2">Custom</text>

  <rect x="176" y="232" width="1002" height="48" fill="#FFFFFF"/>
  <rect x="176" y="280" width="1002" height="48" fill="#F8FBFB"/>
  <rect x="176" y="328" width="1002" height="48" fill="#FFFFFF"/>
  <rect x="176" y="376" width="1002" height="48" fill="#F8FBFB"/>
  <rect x="176" y="424" width="1002" height="48" fill="#FFFFFF"/>
  <rect x="176" y="472" width="1002" height="48" fill="#F8FBFB"/>
  <rect x="176" y="520" width="1002" height="48" fill="#FFFFFF"/>
  <rect x="176" y="568" width="1002" height="48" fill="#F8FBFB"/>

  <line x1="176" y1="232" x2="1178" y2="232" stroke="#D8E2E4"/>
  <line x1="176" y1="280" x2="1178" y2="280" stroke="#E3EAEC"/>
  <line x1="176" y1="328" x2="1178" y2="328" stroke="#E3EAEC"/>
  <line x1="176" y1="376" x2="1178" y2="376" stroke="#E3EAEC"/>
  <line x1="176" y1="424" x2="1178" y2="424" stroke="#E3EAEC"/>
  <line x1="176" y1="472" x2="1178" y2="472" stroke="#E3EAEC"/>
  <line x1="176" y1="520" x2="1178" y2="520" stroke="#E3EAEC"/>
  <line x1="176" y1="568" x2="1178" y2="568" stroke="#E3EAEC"/>
  <line x1="496" y1="158" x2="496" y2="616" stroke="#D8E2E4"/>
  <line x1="666" y1="158" x2="666" y2="616" stroke="#D8E2E4"/>
  <line x1="848" y1="158" x2="848" y2="616" stroke="#D8E2E4"/>
  <line x1="1018" y1="158" x2="1018" y2="616" stroke="#D8E2E4"/>

  <text x="202" y="262" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#3B474A">Customizable branded website</text>
  <text x="202" y="310" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#3B474A">Unlimited photo and video upload</text>
  <text x="202" y="358" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#3B474A">Responsive mobile editing</text>
  <text x="202" y="406" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#3B474A">Fully hosted, unlimited traffic</text>
  <text x="202" y="454" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#3B474A">Remove ads and spam branding</text>
  <text x="202" y="502" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#3B474A">Share galleries on the go</text>
  <text x="202" y="550" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#3B474A">Team roles and approvals</text>
  <text x="202" y="598" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#3B474A">Priority support and SLA</text>

  <g font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" text-anchor="middle">
    <circle cx="576" cy="256" r="15" fill="#E5F7ED"/><text x="576" y="263" width="30" fill="#00A651">✓</text>
    <circle cx="752" cy="256" r="15" fill="#E5F7ED"/><text x="752" y="263" width="30" fill="#00A651">✓</text>
    <circle cx="928" cy="256" r="15" fill="#E5F7ED"/><text x="928" y="263" width="30" fill="#00A651">✓</text>
    <circle cx="1098" cy="256" r="15" fill="#E5F7ED"/><text x="1098" y="263" width="30" fill="#00A651">✓</text>

    <circle cx="576" cy="304" r="15" fill="#FDEAEA"/><text x="576" y="311" width="30" fill="#E23B3B">×</text>
    <circle cx="752" cy="304" r="15" fill="#E5F7ED"/><text x="752" y="311" width="30" fill="#00A651">✓</text>
    <circle cx="928" cy="304" r="15" fill="#E5F7ED"/><text x="928" y="311" width="30" fill="#00A651">✓</text>
    <circle cx="1098" cy="304" r="15" fill="#E5F7ED"/><text x="1098" y="311" width="30" fill="#00A651">✓</text>

    <circle cx="576" cy="352" r="15" fill="#E5F7ED"/><text x="576" y="359" width="30" fill="#00A651">✓</text>
    <circle cx="752" cy="352" r="15" fill="#E5F7ED"/><text x="752" y="359" width="30" fill="#00A651">✓</text>
    <circle cx="928" cy="352" r="15" fill="#E5F7ED"/><text x="928" y="359" width="30" fill="#00A651">✓</text>
    <circle cx="1098" cy="352" r="15" fill="#E5F7ED"/><text x="1098" y="359" width="30" fill="#00A651">✓</text>

    <circle cx="576" cy="400" r="15" fill="#FDEAEA"/><text x="576" y="407" width="30" fill="#E23B3B">×</text>
    <circle cx="752" cy="400" r="15" fill="#E5F7ED"/><text x="752" y="407" width="30" fill="#00A651">✓</text>
    <circle cx="928" cy="400" r="15" fill="#E5F7ED"/><text x="928" y="407" width="30" fill="#00A651">✓</text>
    <circle cx="1098" cy="400" r="15" fill="#E5F7ED"/><text x="1098" y="407" width="30" fill="#00A651">✓</text>

    <circle cx="576" cy="448" r="15" fill="#FDEAEA"/><text x="576" y="455" width="30" fill="#E23B3B">×</text>
    <circle cx="752" cy="448" r="15" fill="#E5F7ED"/><text x="752" y="455" width="30" fill="#00A651">✓</text>
    <circle cx="928" cy="448" r="15" fill="#E5F7ED"/><text x="928" y="455" width="30" fill="#00A651">✓</text>
    <circle cx="1098" cy="448" r="15" fill="#E5F7ED"/><text x="1098" y="455" width="30" fill="#00A651">✓</text>

    <circle cx="576" cy="496" r="15" fill="#FDEAEA"/><text x="576" y="503" width="30" fill="#E23B3B">×</text>
    <circle cx="752" cy="496" r="15" fill="#FDEAEA"/><text x="752" y="503" width="30" fill="#E23B3B">×</text>
    <circle cx="928" cy="496" r="15" fill="#E5F7ED"/><text x="928" y="503" width="30" fill="#00A651">✓</text>
    <circle cx="1098" cy="496" r="15" fill="#E5F7ED"/><text x="1098" y="503" width="30" fill="#00A651">✓</text>

    <circle cx="576" cy="544" r="15" fill="#FDEAEA"/><text x="576" y="551" width="30" fill="#E23B3B">×</text>
    <circle cx="752" cy="544" r="15" fill="#E5F7ED"/><text x="752" y="551" width="30" fill="#00A651">✓</text>
    <circle cx="928" cy="544" r="15" fill="#E5F7ED"/><text x="928" y="551" width="30" fill="#00A651">✓</text>
    <circle cx="1098" cy="544" r="15" fill="#E5F7ED"/><text x="1098" y="551" width="30" fill="#00A651">✓</text>

    <circle cx="576" cy="592" r="15" fill="#FDEAEA"/><text x="576" y="599" width="30" fill="#E23B3B">×</text>
    <circle cx="752" cy="592" r="15" fill="#FDEAEA"/><text x="752" y="599" width="30" fill="#E23B3B">×</text>
    <circle cx="928" cy="592" r="15" fill="#FDEAEA"/><text x="928" y="599" width="30" fill="#E23B3B">×</text>
    <circle cx="1098" cy="592" r="15" fill="#E5F7ED"/><text x="1098" y="599" width="30" fill="#00A651">✓</text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Using an actual SVG `<table>` or HTML inside `<foreignObject>`; it will not translate into editable PowerPoint objects.
- ❌ Applying `clip-path` to row bands or header rectangles; clipping is only reliable for `<image>` elements.
- ❌ Using `<use>` to duplicate check/cross icons; repeat circles/text or paths explicitly instead.
- ❌ Placing table lines inside a filtered group; filters on `<line>` are dropped, so keep shadows on card rectangles only.
- ❌ Relying on tiny text without explicit `width`; every text label needs a width so PowerPoint preserves layout.

## Composition notes
- Keep the main grid centered and dominant, occupying roughly 80–90% of slide width; reserve the top 15% for title and context.
- Use a dark vertical “FEATURES” rail on the left to anchor the row labels and make the grid feel intentional rather than spreadsheet-like.
- Highlight one recommended tier with a tinted column, warmer header, and small badge; this creates a clear decision path.
- Maintain generous row height, subtle separators, and alternating row fills so the audience can scan horizontally without losing their place.