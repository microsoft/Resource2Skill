# SVG Recipe — Comparison Split Cards

## Visual mechanism
Two oversized side-by-side cards divide the slide into “Option A / Option B” or “Before / After,” with the right card promoted through a saturated accent gradient, glow, and higher contrast typography. The layout feels executive and editorial by combining clipped imagery, pill labels, feature rows, and a subtle central divider.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 2× large `<rect>` card bodies for the left neutral card and right accent card
- 2× `<image>` elements clipped into rounded photo bands at the top of each card
- 2× `<clipPath>` definitions with rounded `<rect>` crops for the card images
- 3× `<linearGradient>` definitions for the background wash, right-card accent, and photo fade overlays
- 2× `<filter>` definitions for soft card shadow and accent glow
- 4× decorative `<path>` shapes for editorial blobs, swooshes, and accent overlays
- 1× `<line>` for the vertical split divider
- 8× small `<circle>` elements for status dots and feature icons
- 6× pill / feature-row `<rect>` elements for labels and comparison rows
- Multiple `<text>` elements with explicit `width` attributes for title, labels, headlines, subtitles, and feature copy

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#F8FAFF"/>
      <stop offset="55%" stop-color="#F2F5FB"/>
      <stop offset="100%" stop-color="#E9EEF8"/>
    </linearGradient>

    <linearGradient id="accentCard" x1="666" y1="158" x2="1206" y2="628">
      <stop offset="0%" stop-color="#2563EB"/>
      <stop offset="58%" stop-color="#1947B8"/>
      <stop offset="100%" stop-color="#0B1F5E"/>
    </linearGradient>

    <linearGradient id="photoFade" x1="0" y1="158" x2="0" y2="328">
      <stop offset="0%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.32"/>
    </linearGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="accentGlow" x="-25%" y="-25%" width="150%" height="150%">
      <feGaussianBlur stdDeviation="14"/>
    </filter>

    <clipPath id="leftPhotoClip">
      <rect x="74" y="158" width="540" height="178" rx="30"/>
    </clipPath>

    <clipPath id="rightPhotoClip">
      <rect x="666" y="158" width="540" height="178" rx="30"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <path d="M-60 150 C120 38 245 44 390 112 C536 180 602 132 695 34 L695 0 L-60 0 Z" fill="#E4EBFF" opacity="0.75"/>
  <path d="M1015 48 C1152 74 1248 160 1328 314 L1328 0 L1005 0 Z" fill="#DBEAFE" opacity="0.9"/>
  <path d="M980 666 C1088 604 1210 612 1325 690 L1325 720 L960 720 Z" fill="#C7D2FE" opacity="0.42"/>

  <text x="74" y="70" width="700" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="19" font-weight="700" letter-spacing="2.5" fill="#2563EB">COMPARISON FRAME</text>
  <text x="74" y="112" width="760" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="38" font-weight="750" fill="#111827">From fragmented workflow to guided execution</text>
  <text x="838" y="92" width="368" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" fill="#64748B" text-anchor="end">Use the accent side to signal the preferred, future, or higher-value state.</text>

  <line x1="640" y1="178" x2="640" y2="612" stroke="#CBD5E1" stroke-width="2" stroke-dasharray="7 10"/>

  <rect x="74" y="158" width="540" height="470" rx="32" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="666" y="158" width="540" height="470" rx="32" fill="#2A63F3" opacity="0.32" filter="url(#accentGlow)"/>
  <rect x="666" y="158" width="540" height="470" rx="32" fill="url(#accentCard)" filter="url(#cardShadow)"/>

  <image href="https://images.unsplash.com/photo-1497366754035-f200968a6e72?auto=format&amp;fit=crop&amp;w=1200&amp;q=80" x="74" y="158" width="540" height="178" preserveAspectRatio="xMidYMid slice" clip-path="url(#leftPhotoClip)"/>
  <rect x="74" y="158" width="540" height="178" rx="30" fill="url(#photoFade)" opacity="0.65"/>

  <image href="https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&amp;fit=crop&amp;w=1200&amp;q=80" x="666" y="158" width="540" height="178" preserveAspectRatio="xMidYMid slice" clip-path="url(#rightPhotoClip)"/>
  <rect x="666" y="158" width="540" height="178" rx="30" fill="#0B1F5E" opacity="0.22"/>
  <rect x="666" y="158" width="540" height="178" rx="30" fill="url(#photoFade)" opacity="0.75"/>

  <rect x="106" y="188" width="128" height="34" rx="17" fill="#FFFFFF" opacity="0.92"/>
  <circle cx="128" cy="205" r="5" fill="#94A3B8"/>
  <text x="142" y="211" width="82" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" fill="#475569">CURRENT</text>

  <rect x="698" y="188" width="120" height="34" rx="17" fill="#FFFFFF" opacity="0.96"/>
  <circle cx="720" cy="205" r="5" fill="#22C55E"/>
  <text x="734" y="211" width="74" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" fill="#1D4ED8">TARGET</text>

  <text x="106" y="382" width="450" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="35" font-weight="760" fill="#111827">Manual handoffs</text>
  <text x="106" y="416" width="438" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#64748B">Teams coordinate work through disconnected tools, status meetings, and repeated clarification loops.</text>

  <text x="698" y="382" width="450" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="35" font-weight="760" fill="#FFFFFF">Guided operating flow</text>
  <text x="698" y="416" width="438" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#DBEAFE">A single flow orchestrates next-best actions, approvals, and visibility across every stakeholder.</text>

  <rect x="106" y="462" width="458" height="48" rx="16" fill="#F8FAFC" stroke="#E2E8F0"/>
  <circle cx="132" cy="486" r="8" fill="#CBD5E1"/>
  <text x="154" y="492" width="375" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="650" fill="#334155">Slow escalation cycles</text>

  <rect x="106" y="522" width="458" height="48" rx="16" fill="#F8FAFC" stroke="#E2E8F0"/>
  <circle cx="132" cy="546" r="8" fill="#CBD5E1"/>
  <text x="154" y="552" width="375" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="650" fill="#334155">Hidden ownership gaps</text>

  <rect x="106" y="582" width="458" height="48" rx="16" fill="#F8FAFC" stroke="#E2E8F0"/>
  <circle cx="132" cy="606" r="8" fill="#CBD5E1"/>
  <text x="154" y="612" width="375" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="650" fill="#334155">Decisions rely on manual updates</text>

  <path d="M1112 346 C1178 370 1198 426 1166 486 C1137 540 1074 552 1018 524 C956 493 941 430 976 381 C1007 339 1056 326 1112 346 Z" fill="#60A5FA" opacity="0.18"/>
  <path d="M666 558 C758 520 825 554 886 598 C940 637 998 640 1066 604 C1114 579 1161 576 1206 594 L1206 628 L666 628 Z" fill="#FFFFFF" opacity="0.08"/>

  <rect x="698" y="462" width="458" height="48" rx="16" fill="#FFFFFF" opacity="0.14" stroke="#93C5FD"/>
  <circle cx="724" cy="486" r="8" fill="#22C55E"/>
  <text x="746" y="492" width="375" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="650" fill="#FFFFFF">Automated exception routing</text>

  <rect x="698" y="522" width="458" height="48" rx="16" fill="#FFFFFF" opacity="0.14" stroke="#93C5FD"/>
  <circle cx="724" cy="546" r="8" fill="#22C55E"/>
  <text x="746" y="552" width="375" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="650" fill="#FFFFFF">Clear accountable owner per step</text>

  <rect x="698" y="582" width="458" height="48" rx="16" fill="#FFFFFF" opacity="0.14" stroke="#93C5FD"/>
  <circle cx="724" cy="606" r="8" fill="#22C55E"/>
  <text x="746" y="612" width="375" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="650" fill="#FFFFFF">Live decision trail and progress view</text>
</svg>
```

## Avoid in this skill
- ❌ Using two plain rectangles with no hierarchy; the comparison loses its “preferred side” emphasis.
- ❌ Applying `clip-path` to decorative shapes or card rectangles; use clipping only on `<image>` elements.
- ❌ Putting shadows or filters on `<line>` dividers; use filters on cards, paths, or text instead.
- ❌ Using `marker-end` arrows between cards; if directional comparison is needed, use a plain `<line>` plus a small triangle `<path>`.
- ❌ Letting text auto-size implicitly; every `<text>` must include a `width` attribute for reliable PowerPoint rendering.

## Composition notes
- Keep the two cards large and nearly symmetrical, but give the right card stronger color, glow, or contrast when it represents the recommended option.
- Reserve the top 20–25% of each card for clipped imagery or a color block; place the comparison headline immediately below.
- Use the center divider sparingly: a dashed vertical line or slim gap is enough to imply comparison without clutter.
- Repeat feature-row spacing across both cards so viewers can scan differences horizontally, while using color rhythm to make the accent side feel more decisive.