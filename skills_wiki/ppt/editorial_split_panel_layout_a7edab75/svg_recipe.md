# SVG Recipe — Editorial Split-Panel Layout

## Visual mechanism
Divide the slide into one wide editorial text panel and three full-height vertical pillars, alternating white, photographic, white, and dark backgrounds. The premium feel comes from strict column alignment, oversized tracked typography, centered pillar content, a tinted image overlay, and tiny bottom numbering anchors.

## SVG primitives needed
- 4× `<rect>` for the full-bleed panel backgrounds and narrow accent bars
- 1× `<image>` for the full-height editorial photo pillar
- 1× `<clipPath>` with `<rect>` applied to the image so the photo remains confined to its pillar
- 1× `<linearGradient>` for the dark-to-gold transparent image overlay
- 1× `<filter id="softShadow">` applied to a small floating metric card
- 8× `<text>` blocks with explicit `width` for title, labels, pillar headlines, body copy, metrics, and bottom numbers
- 3× `<circle>` for centered icon medallions in the pillar columns
- 4× `<path>` for simple editable line-chart strokes and icon glyph accents
- 3× `<line>` for subtle column dividers and decorative rules

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="photoPillarClip">
      <rect x="416" y="0" width="288" height="720"/>
    </clipPath>

    <linearGradient id="photoOverlay" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#323232" stop-opacity="0.78"/>
      <stop offset="52%" stop-color="#5a4939" stop-opacity="0.62"/>
      <stop offset="100%" stop-color="#d28c46" stop-opacity="0.82"/>
    </linearGradient>

    <linearGradient id="goldRule" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#d28c46"/>
      <stop offset="100%" stop-color="#f0c080"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="8" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#ffffff"/>

  <!-- Left editorial panel -->
  <rect x="0" y="0" width="416" height="720" fill="#ffffff"/>
  <rect x="64" y="76" width="72" height="5" fill="url(#goldRule)"/>
  <text x="64" y="118" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" letter-spacing="3" fill="#d28c46">
    MARKET INTELLIGENCE
  </text>
  <text x="62" y="194" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="48" font-weight="300" letter-spacing="5" fill="#262626">
    <tspan x="62" dy="0">Q3</tspan>
    <tspan x="62" dy="58">SIGNALS</tspan>
    <tspan x="62" dy="58">IN THREE</tspan>
    <tspan x="62" dy="58">MOVES</tspan>
  </text>
  <text x="66" y="472" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="17" line-height="1.35" fill="#6b6b6b">
    A concise editorial frame for turning dense business updates into three sharp, memorable evidence pillars.
  </text>
  <line x1="64" y1="624" x2="328" y2="624" stroke="#e8e1d8" stroke-width="1"/>
  <text x="64" y="660" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="12" letter-spacing="2" fill="#9a9a9a">
    BOARD REVIEW / EXECUTIVE SUMMARY
  </text>

  <!-- Photo pillar -->
  <image x="416" y="0" width="288" height="720" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#photoPillarClip)"
         href="https://images.example.com/editorial-split-panel-modern-architecture-column.jpg"/>
  <rect x="416" y="0" width="288" height="720" fill="url(#photoOverlay)"/>
  <circle cx="560" cy="154" r="42" fill="#ffffff" fill-opacity="0.18" stroke="#ffffff" stroke-opacity="0.65" stroke-width="1.5"/>
  <text x="524" y="168" width="72" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="38" fill="#ffffff">✦</text>
  <text x="452" y="292" width="216" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="23" font-weight="700" letter-spacing="2" fill="#ffffff">
    DEMAND
  </text>
  <text x="455" y="333" width="210" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" line-height="1.45" fill="#f6efe6">
    Search velocity and inbound interest widened across premium segments, creating a stronger top-of-funnel signal.
  </text>
  <text x="448" y="635" width="224" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="72" font-weight="200" fill="#ffffff" fill-opacity="0.28">
    01
  </text>

  <!-- White data pillar -->
  <rect x="704" y="0" width="288" height="720" fill="#fbfaf8"/>
  <line x1="704" y1="0" x2="704" y2="720" stroke="#ebe6df" stroke-width="1"/>
  <circle cx="848" cy="154" r="42" fill="#f4eadf" stroke="#d28c46" stroke-opacity="0.45" stroke-width="1.5"/>
  <path d="M825 166 C833 144, 846 174, 856 150 C863 134, 872 150, 877 139" fill="none" stroke="#d28c46" stroke-width="4" stroke-linecap="round"/>
  <text x="740" y="292" width="216" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="23" font-weight="700" letter-spacing="2" fill="#323232">
    CONVERSION
  </text>
  <text x="743" y="333" width="210" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" line-height="1.45" fill="#666666">
    Trial cohorts are now advancing faster, with fewer approval stalls and a cleaner handoff from pilot to procurement.
  </text>

  <rect x="748" y="454" width="200" height="92" rx="18" fill="#ffffff" filter="url(#softShadow)"/>
  <text x="772" y="491" width="152" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" letter-spacing="2" fill="#a48a70">
    PIPELINE LIFT
  </text>
  <text x="772" y="526" width="152" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#323232">
    +18%
  </text>
  <path d="M774 566 L806 552 L836 559 L866 534 L920 520" fill="none" stroke="#d28c46" stroke-width="3" stroke-linecap="round"/>
  <text x="736" y="635" width="224" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="72" font-weight="200" fill="#d8d2cb">
    02
  </text>

  <!-- Dark pillar -->
  <rect x="992" y="0" width="288" height="720" fill="#323232"/>
  <line x1="992" y1="0" x2="992" y2="720" stroke="#272727" stroke-width="1"/>
  <circle cx="1136" cy="154" r="42" fill="#d28c46" fill-opacity="0.18" stroke="#d28c46" stroke-opacity="0.9" stroke-width="1.5"/>
  <path d="M1114 158 C1125 139, 1146 139, 1158 158 C1150 178, 1124 178, 1114 158 Z" fill="none" stroke="#f0c080" stroke-width="3"/>
  <path d="M1136 143 L1136 174" stroke="#f0c080" stroke-width="3" stroke-linecap="round"/>
  <text x="1028" y="292" width="216" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="23" font-weight="700" letter-spacing="2" fill="#ffffff">
    RETENTION
  </text>
  <text x="1031" y="333" width="210" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" line-height="1.45" fill="#d7d7d7">
    Expansion intent is strongest where service teams pair automation with high-touch strategic guidance.
  </text>
  <rect x="1056" y="472" width="160" height="4" fill="#4b4b4b"/>
  <rect x="1056" y="472" width="116" height="4" fill="#d28c46"/>
  <text x="1056" y="510" width="160" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" letter-spacing="2" fill="#f0c080">
    72% HEALTHY
  </text>
  <text x="1024" y="635" width="224" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="72" font-weight="200" fill="#ffffff" fill-opacity="0.16">
    03
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using equal-width panels across the whole slide; the technique depends on a wider editorial lead panel and narrower support pillars.
- ❌ Applying `clip-path` to overlay rectangles or text; keep clipping only on the `<image>` and size overlays exactly to the pillar bounds.
- ❌ Using `<pattern>` fills for the photo pillar; use a real `<image>` plus a translucent gradient overlay for a more editorial result.
- ❌ Relying on PowerPoint letter-spacing support alone for the main title; if tracking is critical, manually space short uppercase words or use `letter-spacing` only as a visual enhancement.
- ❌ Adding heavy borders around every column; seams should feel architectural and full-bleed, not like table cells.

## Composition notes
- Keep the left column mostly white with generous margins; it should read like a magazine cover title area, not a dense content block.
- Center all pillar content on a shared vertical rhythm: icon near the top, headline and body in the middle, large pale number at the bottom.
- Use the image pillar as the emotional focal point, then repeat the gold accent in small details across the other columns.
- Let the dark final pillar provide visual closure; it should balance the white lead panel and make the slide feel intentionally framed.