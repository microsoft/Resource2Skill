# SVG Recipe — Organic-Geometric Contrast Layout

## Visual mechanism
A hard-edged, dark geometric text panel anchors the slide while a large, soft-edged organic image crop creates expressive contrast on the opposite side. The result feels structured enough for executive content but visually distinctive through the custom blob photo frame.

## SVG primitives needed
- 1× `<rect>` for the full-slide atmospheric background
- 1× `<rect>` for the dark geometric text panel
- 1× `<rect>` for a subtle panel edge highlight
- 1× `<path>` for the organic photo shadow
- 1× `<path>` for the offset teal organic accent shape
- 1× `<image>` clipped into the organic blob photo shape
- 1× `<clipPath>` with a `<path>` defining the organic image crop
- 2× `<linearGradient>` for background depth and panel sheen
- 1× `<filter id="softShadow">` for the organic blob shadow
- 1× `<filter id="panelShadow">` for light depth on the text panel
- 6× `<text>` for eyebrow, title, subtitle, metadata, and small supporting labels
- 3× `<line>` for minimal geometric accent rules

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#F6FAFA"/>
      <stop offset="0.55" stop-color="#EAF1F1"/>
      <stop offset="1" stop-color="#DDE8E8"/>
    </linearGradient>

    <linearGradient id="panelSheen" x1="0" y1="0" x2="455" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#40545D"/>
      <stop offset="0.55" stop-color="#34474F"/>
      <stop offset="1" stop-color="#26363D"/>
    </linearGradient>

    <filter id="softShadow" x="-80" y="-80" width="980" height="860" filterUnits="userSpaceOnUse">
      <feOffset dx="18" dy="22"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="panelShadow" x="-20" y="-20" width="530" height="780" filterUnits="userSpaceOnUse">
      <feOffset dx="10" dy="0"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="organicPhotoClip" clipPathUnits="userSpaceOnUse">
      <path d="M835 92
               C1000 38 1218 88 1240 268
               C1266 478 1104 654 888 662
               C705 669 546 558 560 396
               C570 284 655 232 704 172
               C742 126 774 112 835 92 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <path d="M835 92
           C1000 38 1218 88 1240 268
           C1266 478 1104 654 888 662
           C705 669 546 558 560 396
           C570 284 655 232 704 172
           C742 126 774 112 835 92 Z"
        fill="#1B2D33" opacity="0.22" filter="url(#softShadow)"/>

  <path d="M790 128
           C945 54 1160 116 1188 285
           C1215 451 1054 610 872 617
           C707 624 604 532 603 400
           C602 296 676 244 721 190
           C747 159 760 143 790 128 Z"
        fill="#75B6B4" opacity="0.95"/>

  <image x="500" y="38" width="790" height="650"
         href="https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&amp;fit=crop&amp;w=1600&amp;q=85"
         clip-path="url(#organicPhotoClip)"
         preserveAspectRatio="xMidYMid slice"/>

  <rect x="0" y="0" width="455" height="720" fill="url(#panelSheen)" filter="url(#panelShadow)"/>
  <rect x="451" y="0" width="4" height="720" fill="#75B6B4" opacity="0.9"/>

  <line x1="78" y1="92" x2="166" y2="92" stroke="#75B6B4" stroke-width="4"/>
  <line x1="78" y1="604" x2="156" y2="604" stroke="#75B6B4" stroke-width="3" opacity="0.75"/>
  <line x1="78" y1="626" x2="205" y2="626" stroke="#FFFFFF" stroke-width="1.5" opacity="0.28"/>

  <text x="78" y="132" width="300"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" letter-spacing="2.8"
        fill="#75B6B4">EXECUTIVE OVERVIEW</text>

  <text x="76" y="238" width="330"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="56" font-weight="800"
        fill="#FFFFFF">
    <tspan x="76" dy="0">Production</tspan>
    <tspan x="76" dy="66">Plant</tspan>
  </text>

  <text x="80" y="356" width="315"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="19" font-weight="400"
        fill="#DCE8E8">
    <tspan x="80" dy="0">Collection of 10+ premium</tspan>
    <tspan x="80" dy="30">PowerPoint templates for</tspan>
    <tspan x="80" dy="30">industrial transformation.</tspan>
  </text>

  <text x="80" y="500" width="280"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="600" letter-spacing="1.4"
        fill="#FFFFFF" opacity="0.72">2026 STRATEGIC ROADMAP</text>

  <text x="80" y="642" width="260"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13"
        fill="#B9C9C9">Designed for board-ready narratives</text>

  <text x="970" y="665" width="220"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="600"
        fill="#40545D" opacity="0.72">Organic image crop + geometric panel</text>
</svg>
```

## Avoid in this skill
- ❌ Applying `clip-path` to a `<path>` or `<rect>` for the blob effect; use `clipPath` only on the `<image>`.
- ❌ Using `<mask>` to fade the photo into the background; masks can hard-fail translation.
- ❌ Building the organic crop from many circles or rectangles; use one smooth Bézier `<path>` for a premium freeform silhouette.
- ❌ Letting the photo and panel compete equally; the panel should be stable and geometric, while the organic image should be the expressive focal point.
- ❌ Omitting `width` on text elements; PowerPoint text conversion needs explicit widths.

## Composition notes
- Keep the text panel at roughly 32–38% of slide width so it feels architectural without crowding the image.
- Let the organic photo occupy most of the right side and slightly overlap the implied centerline for dynamic asymmetry.
- Use one accent color, such as muted teal, both as a panel divider and as an offset blob behind the image.
- Preserve generous margins inside the panel; the contrast works best when the typography feels calm against the expressive image crop.