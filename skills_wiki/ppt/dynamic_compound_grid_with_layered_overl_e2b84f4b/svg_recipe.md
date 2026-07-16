# SVG Recipe — Dynamic Compound Grid with Layered Overlap

## Visual mechanism
A strict 12-column editorial grid anchors the composition, while a large hero image spans most of the left side and a bold color panel overlaps it from the right. The overlap breaks the grid just enough to create depth, hierarchy, and a premium magazine-spread feel.

## SVG primitives needed
- 1× `<rect>` for the off-white slide background
- 12× `<line>` for faint vertical column-grid guides
- 4× `<line>` for subtle horizontal modular-grid guides
- 1× `<image>` for the large editorial hero photo
- 1× `<clipPath>` with rounded `<rect>` to crop the hero photo cleanly
- 1× `<rect>` for the overlapping accent text panel
- 1× `<filter id="panelShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` applied to the overlap panel
- 1× `<linearGradient>` for a slight tonal shift on the accent panel
- 5× `<text>` blocks for kicker, headline, body copy, caption, and grid label
- 2× `<path>` elements for decorative editorial brackets / motion accents
- 3× small `<rect>` elements for modular-grid annotation ticks

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="accentRed" x1="0" y1="210" x2="1120" y2="650" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#F04A45"/>
      <stop offset="0.62" stop-color="#E53935"/>
      <stop offset="1" stop-color="#C8202C"/>
    </linearGradient>

    <filter id="panelShadow" x="-20%" y="-20%" width="150%" height="150%">
      <feOffset dx="0" dy="22" result="off"/>
      <feGaussianBlur in="off" stdDeviation="22" result="blur"/>
      <feColorMatrix in="blur" type="matrix"
        values="0 0 0 0 0
                0 0 0 0 0
                0 0 0 0 0
                0 0 0 .28 0" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="heroClip">
      <rect x="64" y="64" width="656" height="528" rx="6" ry="6"/>
    </clipPath>
  </defs>

  <!-- background -->
  <rect x="0" y="0" width="1280" height="720" fill="#F5F5F2"/>

  <!-- faint compound grid: 12 columns + modular rows -->
  <g opacity="0.16" stroke="#111111" stroke-width="1">
    <line x1="64" y1="40" x2="64" y2="680"/>
    <line x1="160" y1="40" x2="160" y2="680"/>
    <line x1="256" y1="40" x2="256" y2="680"/>
    <line x1="352" y1="40" x2="352" y2="680"/>
    <line x1="448" y1="40" x2="448" y2="680"/>
    <line x1="544" y1="40" x2="544" y2="680"/>
    <line x1="640" y1="40" x2="640" y2="680"/>
    <line x1="736" y1="40" x2="736" y2="680"/>
    <line x1="832" y1="40" x2="832" y2="680"/>
    <line x1="928" y1="40" x2="928" y2="680"/>
    <line x1="1024" y1="40" x2="1024" y2="680"/>
    <line x1="1120" y1="40" x2="1120" y2="680"/>
    <line x1="64" y1="168" x2="1216" y2="168"/>
    <line x1="64" y1="296" x2="1216" y2="296"/>
    <line x1="64" y1="424" x2="1216" y2="424"/>
    <line x1="64" y1="552" x2="1216" y2="552"/>
  </g>

  <!-- hero image spanning seven columns -->
  <image
    href="https://images.unsplash.com/photo-1494526585095-c41746248156?auto=format&amp;fit=crop&amp;w=1400&amp;q=80"
    x="64" y="64" width="656" height="528"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#heroClip)"/>

  <!-- dark editorial caption tucked into the image grid -->
  <rect x="96" y="520" width="210" height="38" fill="#111111" opacity="0.86"/>
  <text x="112" y="544" width="180" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="600" letter-spacing="1.8" fill="#FFFFFF">
    ARCHITECTURE / 12-COL
  </text>

  <!-- overlap panel: starts on column 7 and crosses back over hero image -->
  <rect x="640" y="210" width="480" height="432" rx="2" ry="2"
        fill="url(#accentRed)" filter="url(#panelShadow)"/>

  <!-- oversized headline inside overlap panel -->
  <text x="684" y="292" width="390" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="700" letter-spacing="3.2" fill="#FFFFFF" opacity="0.82">
    COMPOUND GRID
  </text>

  <text x="680" y="382" width="398" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="76" font-weight="800" line-height="0.9" fill="#FFFFFF">
    <tspan x="680" dy="0">DYNAMIC</tspan>
    <tspan x="680" dy="74">GRID</tspan>
    <tspan x="680" dy="74">SYSTEMS</tspan>
  </text>

  <text x="686" y="578" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="400" fill="#FFFFFF" opacity="0.9">
    <tspan x="686" dy="0">A strict column system becomes more expressive</tspan>
    <tspan x="686" dy="27">when one module deliberately overlaps another.</tspan>
  </text>

  <!-- right-side negative-space note -->
  <text x="1148" y="126" width="72" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" font-weight="700" letter-spacing="2" fill="#111111"
        transform="rotate(90 1148 126)">
    LAYERED OVERLAP
  </text>

  <!-- modular annotation ticks -->
  <rect x="64" y="616" width="92" height="6" fill="#111111"/>
  <rect x="160" y="616" width="92" height="6" fill="#111111" opacity="0.45"/>
  <rect x="256" y="616" width="92" height="6" fill="#111111" opacity="0.18"/>

  <!-- decorative paths that imply intentional grid disruption -->
  <path d="M594 186 C620 178, 642 180, 662 198" fill="none" stroke="#111111" stroke-width="4" stroke-linecap="round"/>
  <path d="M1118 642 C1160 618, 1182 584, 1172 542" fill="none" stroke="#111111" stroke-width="3" stroke-linecap="round" opacity="0.38"/>
</svg>
```

## Avoid in this skill
- ❌ A simple side-by-side image/text layout with no overlap; the whole technique depends on crossing grid modules.
- ❌ Applying `clip-path` to the red panel or other non-image shapes; use normal rectangles for editable PowerPoint panels.
- ❌ Putting shadows on grid `<line>` elements; filters on lines are dropped, so reserve shadow filters for the overlap `<rect>`.
- ❌ Using invisible grid math only; include faint visible guide lines or modular ticks so the compound-grid logic is perceptible.
- ❌ Center-aligning everything; this style needs asymmetric tension and strong editorial alignment.

## Composition notes
- Keep the hero image dominant: roughly 50–60% of slide width and 70% of slide height, anchored to the left with generous margins.
- Start the overlap panel around column 7 so it intrudes one to two columns into the image; shift it downward to avoid symmetry.
- Use a high-contrast accent panel, usually red, navy, black, or electric blue, with white oversized headline text.
- Preserve negative space on the far right/top so the dense image-panel overlap does not make the slide feel crowded.