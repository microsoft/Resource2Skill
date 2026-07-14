# SVG Recipe — Corporate Geometric Split & Flow Deck

## Visual mechanism
A crisp white corporate slide is split between a full-bleed visual panel and a structured content panel, using cyan for hierarchy/flow and coral red for directional geometric accents. The lower content area becomes a clean horizontal process timeline with circular nodes, minimal iconography, and right-facing triangle cues.

## SVG primitives needed
- 1× `<rect>` for the pure white slide background.
- 1× `<image>` for the full-height hero/photo panel on the left.
- 1× `<clipPath>` with `<rect>` for controlling the hero image crop.
- 1× `<linearGradient>` for a cyan-tinted overlay on the hero photo.
- 1× `<filter id="softShadow">` applied to process cards and node circles.
- 2× `<rect>` for the right-side content frame and subtitle outline box.
- 4× `<rect>` for lightweight process description cards.
- 4× `<circle>` for timeline process nodes.
- 4× `<path>` for simple editable line icons inside the nodes.
- 6× `<path>` for coral geometric triangles and directional arrowheads.
- 4× `<line>` for structural cyan lines and the central timeline axis.
- Multiple `<text>` elements with explicit `width` attributes for title, subtitle, labels, and process copy.
- Nested `<tspan>` elements for mixed-color title styling and multiline text.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="heroClip">
      <rect x="0" y="0" width="540" height="720"/>
    </clipPath>

    <linearGradient id="cyanWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#00AEEF" stop-opacity="0.10"/>
      <stop offset="55%" stop-color="#00AEEF" stop-opacity="0.26"/>
      <stop offset="100%" stop-color="#00AEEF" stop-opacity="0.05"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="7"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <image href="https://images.example.com/corporate-packaging-studio-hero-photo.jpg"
         x="0" y="0" width="540" height="720" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#heroClip)"/>
  <rect x="0" y="0" width="540" height="720" fill="url(#cyanWash)"/>
  <path d="M420 0 L540 0 L540 720 L315 720 Z" fill="#FFFFFF" opacity="0.10"/>
  <path d="M0 620 L120 720 L0 720 Z" fill="#F05A50"/>
  <path d="M497 112 L533 132 L497 152 Z" fill="#F05A50"/>

  <rect x="600" y="46" width="622" height="628" rx="0" fill="none" stroke="#E6E6E6" stroke-width="1.4"/>
  <line x1="1194" y1="158" x2="1194" y2="302" stroke="#00AEEF" stroke-width="5"/>
  <path d="M690 151 L724 172 L690 193 Z" fill="#F05A50"/>

  <text x="1146" y="169" width="520" text-anchor="end"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="64" font-weight="700">
    <tspan x="1146" dy="0" fill="#00AEEF">Packaging</tspan>
    <tspan x="1146" dy="70" fill="#282828">Design</tspan>
  </text>

  <text x="1146" y="323" width="485" text-anchor="end"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" fill="#666666">
    <tspan x="1146" dy="0">A modular corporate flow deck for turning complex</tspan>
    <tspan x="1146" dy="24">product decisions into clear executive milestones.</tspan>
  </text>

  <rect x="802" y="369" width="344" height="42" fill="none" stroke="#F05A50" stroke-width="1.3"/>
  <text x="826" y="396" width="296"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#666666">
    Collection of process-ready presentation modules
  </text>

  <text x="636" y="464" width="360"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#00AEEF">
    FOUR-STAGE COMMERCIALIZATION FLOW
  </text>
  <line x1="646" y1="496" x2="1162" y2="496" stroke="#00AEEF" stroke-width="2.5"/>
  <line x1="646" y1="512" x2="1162" y2="512" stroke="#E9F7FC" stroke-width="1"/>

  <path d="M764 487 L784 496 L764 505 Z" fill="#F05A50"/>
  <path d="M914 487 L934 496 L914 505 Z" fill="#F05A50"/>
  <path d="M1064 487 L1084 496 L1064 505 Z" fill="#F05A50"/>

  <circle cx="684" cy="496" r="38" fill="#FFFFFF" stroke="#00AEEF" stroke-width="3" filter="url(#softShadow)"/>
  <circle cx="834" cy="496" r="38" fill="#FFFFFF" stroke="#00AEEF" stroke-width="3" filter="url(#softShadow)"/>
  <circle cx="984" cy="496" r="38" fill="#FFFFFF" stroke="#00AEEF" stroke-width="3" filter="url(#softShadow)"/>
  <circle cx="1134" cy="496" r="38" fill="#FFFFFF" stroke="#00AEEF" stroke-width="3" filter="url(#softShadow)"/>

  <path d="M674 485 A12 12 0 1 1 692 501 L704 513" fill="none" stroke="#282828" stroke-width="3" stroke-linecap="round"/>
  <path d="M825 502 C817 492 821 480 834 477 C847 480 851 492 842 502 L842 510 L826 510 Z" fill="none" stroke="#282828" stroke-width="3" stroke-linejoin="round"/>
  <path d="M966 485 L984 476 L1002 485 L1002 506 L984 516 L966 506 Z M966 485 L984 495 L1002 485" fill="none" stroke="#282828" stroke-width="3" stroke-linejoin="round"/>
  <path d="M1128 514 C1132 498 1142 485 1155 477 C1154 493 1148 505 1134 515 L1128 514 Z M1124 500 L1113 496 L1122 490 M1143 519 L1147 530 L1154 519" fill="none" stroke="#282828" stroke-width="3" stroke-linejoin="round"/>

  <rect x="624" y="558" width="120" height="82" rx="10" fill="#FFFFFF" stroke="#ECECEC" filter="url(#softShadow)"/>
  <rect x="774" y="558" width="120" height="82" rx="10" fill="#FFFFFF" stroke="#ECECEC" filter="url(#softShadow)"/>
  <rect x="924" y="558" width="120" height="82" rx="10" fill="#FFFFFF" stroke="#ECECEC" filter="url(#softShadow)"/>
  <rect x="1074" y="558" width="120" height="82" rx="10" fill="#FFFFFF" stroke="#ECECEC" filter="url(#softShadow)"/>

  <text x="684" y="584" width="104" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#282828">Market Scan</text>
  <text x="684" y="609" width="104" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" fill="#777777">Define buyer signals and category gaps.</text>

  <text x="834" y="584" width="104" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#282828">Concept</text>
  <text x="834" y="609" width="104" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" fill="#777777">Translate insight into visual territories.</text>

  <text x="984" y="584" width="104" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#282828">Prototype</text>
  <text x="984" y="609" width="104" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" fill="#777777">Build, test, and refine shelf impact.</text>

  <text x="1134" y="584" width="104" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#282828">Launch</text>
  <text x="1134" y="609" width="104" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" fill="#777777">Package the final system for rollout.</text>
</svg>
```

## Avoid in this skill
- ❌ Using `<marker>` arrowheads on `<path>` timelines; draw separate coral triangle `<path>` arrowheads instead.
- ❌ Applying `filter` to `<line>` elements for the timeline; shadows should stay on circles/cards.
- ❌ Clipping rectangles, groups, or paths; only apply `clip-path` to the hero `<image>`.
- ❌ Filling the slide with dense grids or chart junk; the look depends on large whitespace and a few disciplined accents.
- ❌ Overusing coral red; reserve it for directional triangles, small CTA frames, and anchor markers.

## Composition notes
- Keep the hero image at roughly 40–45% of slide width and let it bleed to the top, left, and bottom edges.
- Place the main title in the right panel with generous padding; align it right to reinforce the split-screen geometry.
- Use cyan for structural rhythm: title keyword, vertical accent rule, timeline axis, and node outlines.
- Use coral triangles sparingly as visual breadcrumbs between title, subtitle, and flow steps.