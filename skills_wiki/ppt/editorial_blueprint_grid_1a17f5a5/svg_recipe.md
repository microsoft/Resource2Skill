# SVG Recipe — Editorial Blueprint Grid

## Visual mechanism
A strict 3-column × 2-row editorial grid organizes photos, text, accent panels, and statistics into mathematically aligned modules. Subtle blueprint guide lines and generous gutters make the layout feel intentional, premium, and publication-like rather than like a loose collage.

## SVG primitives needed
- 1× `<rect>` for the full-slide sage background.
- 6–10× `<line>` for faint blueprint grid guides, margins, gutters, and alignment rules.
- 2× `<image>` clipped into editorial photo blocks.
- 2× `<clipPath>` with rounded `<rect>` crops for the images.
- 3× `<rect>` for solid content modules: title card, accent statistic block, and body text card.
- 1× `<linearGradient>` for a subtle accent-panel fill.
- 1× `<filter id="softShadow">` applied to major editorial cards and image frames.
- 1× `<filter id="glow">` applied to the oversized numeral for a soft print-like highlight.
- 2–4× `<path>` for small blueprint annotations, corner brackets, and decorative editorial marks.
- 8–12× `<text>` elements with explicit `width` attributes for kicker labels, title, body copy, captions, statistics, and coordinate labels.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="accentGrad" x1="848" y1="76" x2="1184" y2="340" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#2FB9A9"/>
      <stop offset="1" stop-color="#1F8E84"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3"/>
    </filter>

    <clipPath id="clipHero">
      <rect x="96" y="76" width="712" height="264" rx="4"/>
    </clipPath>
    <clipPath id="clipDetail">
      <rect x="472" y="380" width="336" height="264" rx="4"/>
    </clipPath>
  </defs>

  <!-- Background -->
  <rect x="0" y="0" width="1280" height="720" fill="#E2EBDE"/>

  <!-- Blueprint grid guides: margins, columns, gutters -->
  <line x1="96" y1="40" x2="96" y2="680" stroke="#8EA49A" stroke-width="1" stroke-opacity="0.28" stroke-dasharray="5 8"/>
  <line x1="432" y1="40" x2="432" y2="680" stroke="#8EA49A" stroke-width="1" stroke-opacity="0.16" stroke-dasharray="3 8"/>
  <line x1="472" y1="40" x2="472" y2="680" stroke="#8EA49A" stroke-width="1" stroke-opacity="0.28" stroke-dasharray="5 8"/>
  <line x1="808" y1="40" x2="808" y2="680" stroke="#8EA49A" stroke-width="1" stroke-opacity="0.16" stroke-dasharray="3 8"/>
  <line x1="848" y1="40" x2="848" y2="680" stroke="#8EA49A" stroke-width="1" stroke-opacity="0.28" stroke-dasharray="5 8"/>
  <line x1="1184" y1="40" x2="1184" y2="680" stroke="#8EA49A" stroke-width="1" stroke-opacity="0.28" stroke-dasharray="5 8"/>
  <line x1="56" y1="76" x2="1224" y2="76" stroke="#8EA49A" stroke-width="1" stroke-opacity="0.28" stroke-dasharray="5 8"/>
  <line x1="56" y1="340" x2="1224" y2="340" stroke="#8EA49A" stroke-width="1" stroke-opacity="0.16" stroke-dasharray="3 8"/>
  <line x1="56" y1="380" x2="1224" y2="380" stroke="#8EA49A" stroke-width="1" stroke-opacity="0.28" stroke-dasharray="5 8"/>
  <line x1="56" y1="644" x2="1224" y2="644" stroke="#8EA49A" stroke-width="1" stroke-opacity="0.28" stroke-dasharray="5 8"/>

  <!-- Top-left hero image spanning two columns -->
  <rect x="96" y="76" width="712" height="264" rx="4" fill="#D1DDD4" filter="url(#softShadow)"/>
  <image x="96" y="76" width="712" height="264"
         href="https://images.example.com/minimal-concrete-architecture-with-sage-shadows.jpg"
         preserveAspectRatio="xMidYMid slice" clip-path="url(#clipHero)"/>
  <rect x="96" y="76" width="712" height="264" rx="4" fill="none" stroke="#FFFFFF" stroke-opacity="0.55" stroke-width="1.5"/>

  <!-- Top-right accent statistic block -->
  <rect x="848" y="76" width="336" height="264" rx="4" fill="url(#accentGrad)" filter="url(#softShadow)"/>
  <text x="876" y="116" width="140" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="700" letter-spacing="2" fill="#E7FFFB">MODULE / 01</text>
  <text x="868" y="260" width="270" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="142" font-weight="700" fill="#A8EFE7" fill-opacity="0.26" filter="url(#glow)">01</text>
  <text x="876" y="288" width="240" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="26" font-weight="600" fill="#FFFFFF">Visible order</text>
  <text x="876" y="318" width="250" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#D9FFFA">Grid discipline turns varied inputs into a calm editorial system.</text>

  <!-- Bottom-left title card -->
  <rect x="96" y="380" width="336" height="264" rx="4" fill="#F7FAF4" filter="url(#softShadow)"/>
  <text x="124" y="424" width="190" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="700" letter-spacing="2.4" fill="#2FB9A9">CASE STUDY</text>
  <text x="124" y="482" width="265" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="48" font-weight="700" fill="#303A38">
    <tspan x="124" dy="0">Grid</tspan>
    <tspan x="124" dy="54">Systems</tspan>
    <tspan x="124" dy="54">In Practice</tspan>
  </text>
  <line x1="124" y1="608" x2="248" y2="608" stroke="#2FB9A9" stroke-width="4"/>
  <text x="124" y="632" width="220" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#6E7C76">Swiss-inspired layout for complex corporate narratives.</text>

  <!-- Bottom-middle detail image -->
  <rect x="472" y="380" width="336" height="264" rx="4" fill="#D1DDD4" filter="url(#softShadow)"/>
  <image x="472" y="380" width="336" height="264"
         href="https://images.example.com/editorial-material-detail-desk-grid-paper.jpg"
         preserveAspectRatio="xMidYMid slice" clip-path="url(#clipDetail)"/>
  <rect x="472" y="380" width="336" height="264" rx="4" fill="none" stroke="#FFFFFF" stroke-opacity="0.55" stroke-width="1.5"/>
  <text x="496" y="620" width="240" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" font-weight="700" letter-spacing="1.6" fill="#FFFFFF">PHOTO 02 / DETAIL CROP</text>

  <!-- Bottom-right body copy card -->
  <rect x="848" y="380" width="336" height="264" rx="4" fill="#F7FAF4" filter="url(#softShadow)"/>
  <text x="876" y="424" width="170" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="700" letter-spacing="2.4" fill="#2FB9A9">FRAMEWORK</text>
  <text x="876" y="464" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="600" fill="#303A38">A predictable reading path</text>
  <text x="876" y="500" width="265" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13.5" fill="#58645F">
    <tspan x="876" dy="0">The design is not decoration first; it is</tspan>
    <tspan x="876" dy="23">an alignment system. Images, captions,</tspan>
    <tspan x="876" dy="23">statistics, and narrative copy all lock to</tspan>
    <tspan x="876" dy="23">the same measured columns.</tspan>
    <tspan x="876" dy="34">Consistent gutters create rhythm, while</tspan>
    <tspan x="876" dy="23">contrast between dense and open modules</tspan>
    <tspan x="876" dy="23">keeps the spread from feeling cluttered.</tspan>
  </text>

  <!-- Blueprint annotations and editorial marks -->
  <path d="M96 56 L96 44 L156 44" fill="none" stroke="#2FB9A9" stroke-width="2" stroke-opacity="0.75"/>
  <path d="M1184 664 L1184 676 L1124 676" fill="none" stroke="#2FB9A9" stroke-width="2" stroke-opacity="0.75"/>
  <path d="M1116 118 C1146 126 1158 150 1150 174 C1143 196 1118 204 1096 190" fill="none" stroke="#E7FFFB" stroke-width="1.5" stroke-opacity="0.6"/>
  <path d="M384 418 L404 418 L404 398" fill="none" stroke="#2FB9A9" stroke-width="2" stroke-opacity="0.7"/>

  <!-- Small coordinate labels reinforce the blueprint feel -->
  <text x="100" y="64" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="10" fill="#6E7C76" fill-opacity="0.7">X096 / MARGIN</text>
  <text x="474" y="64" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="10" fill="#6E7C76" fill-opacity="0.7">COL 02</text>
  <text x="850" y="64" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="10" fill="#6E7C76" fill-opacity="0.7">COL 03</text>
  <text x="1092" y="668" width="110" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="10" fill="#6E7C76" fill-opacity="0.7">BASELINE 644</text>
</svg>
```

## Avoid in this skill
- ❌ Do not place elements “by eye”; the effect depends on exact shared x/y coordinates, equal gutters, and aligned baselines.
- ❌ Do not overfill every grid cell with content. The premium editorial feel comes from alternating dense modules with quieter negative space.
- ❌ Do not use `<pattern>` fills for the blueprint grid; use simple dashed `<line>` elements so the guide system remains editable.
- ❌ Do not clip text or shapes with `clip-path`; use clipping only on `<image>` elements for reliable PPT translation.
- ❌ Do not rely on long auto-wrapping SVG text. Use explicit `width` on every `<text>` and manual `<tspan>` line breaks for controlled editorial typography.

## Composition notes
- Use a 96 px left/right margin, 40 px gutters, and three equal 336 px columns; repeat the same logic vertically with two 264 px rows.
- Let one strong image span two columns to create visual weight, then balance it with a compact accent block or statistic.
- Keep body text inside a single column with generous line spacing; the grid should guide reading, not compress it.
- Use faint blueprint guide lines behind the content at low opacity, then emphasize only a few intersections with teal corner brackets or coordinate labels.