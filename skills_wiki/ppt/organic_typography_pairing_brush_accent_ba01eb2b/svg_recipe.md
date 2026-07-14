# SVG Recipe — Organic Typography Pairing & Brush Accent

## Visual mechanism
A rough, hand-painted charcoal brush stroke breaks the clean slide grid and becomes a dramatic anchor for oversized serif typography. The contrast between messy organic texture and crisp type pairing creates a premium editorial/keynote feel.

## SVG primitives needed
- 1× `<rect>` for the warm off-white slide background
- 1× `<linearGradient>` for subtle ink variation across the brush stroke
- 1× `<filter id="brushShadow">` applied to the main brush path for a soft lifted ink shadow
- 1× large `<path>` for the main organic brush body
- 10–16× smaller `<path>` strokes for bristle streaks, jagged extensions, dry-brush edges, and internal texture
- 5–8× background-colored `<path>` overlays to simulate scraped paint gaps without using masks
- 3× `<text>` blocks for the small kicker, large serif headline, and sans-serif body copy
- Optional 2–4× tiny `<circle>` or `<ellipse>` marks for ink flecks around the brush

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="inkGradient" x1="180" y1="0" x2="1100" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#11161c"/>
      <stop offset="42%" stop-color="#1b2028"/>
      <stop offset="72%" stop-color="#101419"/>
      <stop offset="100%" stop-color="#222832"/>
    </linearGradient>

    <filter id="brushShadow" x="-10%" y="-20%" width="120%" height="150%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Warm editorial background -->
  <rect x="0" y="0" width="1280" height="720" fill="#f6f3ee"/>

  <!-- Small ink flecks, kept subtle and editable -->
  <circle cx="198" cy="250" r="4" fill="#1a1f27" opacity="0.45"/>
  <circle cx="1048" cy="423" r="5" fill="#1a1f27" opacity="0.35"/>
  <ellipse cx="1092" cy="284" rx="8" ry="3" fill="#1a1f27" opacity="0.28" transform="rotate(-14 1092 284)"/>
  <ellipse cx="235" cy="430" rx="12" ry="4" fill="#1a1f27" opacity="0.22" transform="rotate(9 235 430)"/>

  <!-- Organic brush stroke: main body -->
  <path filter="url(#brushShadow)" fill="url(#inkGradient)" opacity="0.98"
        d="M174 292
           C234 240, 328 256, 416 247
           C512 236, 596 216, 714 238
           C812 256, 906 231, 1014 255
           C1081 270, 1127 295, 1100 332
           C1078 363, 1001 356, 936 374
           C828 402, 728 384, 612 397
           C501 409, 407 395, 302 407
           C226 415, 153 386, 179 343
           C190 325, 137 318, 174 292 Z"/>

  <!-- Left and right rough bristle extensions -->
  <path d="M142 304 C196 279, 232 282, 286 294" fill="none" stroke="#151a21" stroke-width="34" stroke-linecap="round" opacity="0.88"/>
  <path d="M158 360 C220 382, 270 375, 344 365" fill="none" stroke="#222832" stroke-width="28" stroke-linecap="round" opacity="0.72"/>
  <path d="M980 285 C1042 262, 1094 269, 1146 288" fill="none" stroke="#171c23" stroke-width="32" stroke-linecap="round" opacity="0.78"/>
  <path d="M910 377 C996 392, 1058 388, 1128 358" fill="none" stroke="#202630" stroke-width="25" stroke-linecap="round" opacity="0.64"/>

  <!-- Layered dry-brush texture lines -->
  <path d="M232 281 C354 265, 464 276, 575 259 C704 240, 810 273, 963 262" fill="none" stroke="#2d3440" stroke-width="17" stroke-linecap="round" opacity="0.46"/>
  <path d="M212 324 C337 308, 482 328, 623 312 C750 297, 872 319, 1034 304" fill="none" stroke="#0d1116" stroke-width="22" stroke-linecap="round" opacity="0.38"/>
  <path d="M251 366 C396 386, 511 359, 653 370 C779 380, 909 356, 1056 366" fill="none" stroke="#303743" stroke-width="14" stroke-linecap="round" opacity="0.34"/>
  <path d="M278 248 C390 236, 465 250, 540 240" fill="none" stroke="#38404d" stroke-width="10" stroke-linecap="round" opacity="0.30"/>
  <path d="M739 397 C823 414, 914 398, 990 386" fill="none" stroke="#090c10" stroke-width="13" stroke-linecap="round" opacity="0.24"/>

  <!-- Background-colored scrapes simulate unpainted gaps without masks -->
  <path d="M308 304 C381 293, 446 298, 516 289" fill="none" stroke="#f6f3ee" stroke-width="7" stroke-linecap="round" opacity="0.42"/>
  <path d="M610 279 C676 267, 739 278, 812 271" fill="none" stroke="#f6f3ee" stroke-width="6" stroke-linecap="round" opacity="0.35"/>
  <path d="M421 352 C505 342, 604 352, 700 344" fill="none" stroke="#f6f3ee" stroke-width="5" stroke-linecap="round" opacity="0.34"/>
  <path d="M775 333 C852 325, 915 334, 1004 322" fill="none" stroke="#f6f3ee" stroke-width="8" stroke-linecap="round" opacity="0.30"/>
  <path d="M238 382 C292 391, 350 389, 414 381" fill="none" stroke="#f6f3ee" stroke-width="5" stroke-linecap="round" opacity="0.28"/>

  <!-- Kicker above the brush: clean sans-serif -->
  <text x="640" y="176" width="620" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" letter-spacing="4"
        fill="#6f675d">
    CREATIVE STRATEGY
  </text>

  <!-- Serif headline on the brush -->
  <text x="640" y="338" width="850" text-anchor="middle"
        font-family="Georgia, 'Times New Roman', serif"
        font-size="66" font-weight="700"
        fill="#ffffff">
    Bold Ideas
  </text>

  <text x="640" y="400" width="900" text-anchor="middle"
        font-family="Georgia, 'Times New Roman', serif"
        font-size="42" font-style="italic"
        fill="#ffffff" opacity="0.96">
    need human texture
  </text>

  <!-- Body copy in negative space, sans-serif contrast -->
  <text x="640" y="520" width="760" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" fill="#33302c">
    <tspan x="640" dy="0">Pair a classic serif headline with a calm sans-serif body.</tspan>
    <tspan x="640" dy="36">The brush creates energy; the typography creates trust.</tspan>
  </text>

  <!-- Small grounding rule -->
  <path d="M500 608 C580 600, 710 600, 780 608" fill="none" stroke="#c8beb2" stroke-width="3" stroke-linecap="round"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to cut holes into the brush; simulate dry-brush gaps with off-white overlay paths instead.
- ❌ Do not rely on one flat rectangle behind text; the technique depends on irregular, layered, hand-painted edges.
- ❌ Do not use `<pattern>` fills for texture because they will not translate reliably.
- ❌ Do not use `<animate>` to mimic a brush wipe; create the static brush in SVG and apply any wipe transition later in PowerPoint.
- ❌ Do not omit `width` on text elements; PowerPoint translation needs explicit text widths for predictable layout.

## Composition notes
- Place the brush across the upper-middle third of the slide, roughly 70–80% of the canvas width and 25–30% of the canvas height.
- Keep the headline centered on the darkest part of the brush for maximum contrast; use a large serif face to make the slide feel editorial.
- Put body copy in the clean negative space below, using a restrained sans-serif font and generous line spacing.
- Use a warm off-white background so the black brush feels tactile rather than harsh, and repeat small ink flecks sparingly for rhythm.