# SVG Recipe — Diagonal Duotone Split (Magazine Cover Style)

## Visual mechanism
A full-bleed photograph is split by a bold diagonal geometric slice; the uncovered side stays photographic while the diagonal zone receives a dark navy duotone wash that preserves image texture and creates a high-contrast editorial text field. Large masthead typography and a highlighted accent word/year make the slide feel like a premium magazine cover.

## SVG primitives needed
- 1× `<image>` for the full-bleed hero photograph.
- 1× `<rect>` for a subtle full-slide dark vignette to improve overall contrast.
- 1× `<path>` for the main diagonal navy duotone overlay.
- 1× `<path>` for a darker secondary diagonal depth band near the bottom.
- 1× `<line>` for a crisp diagonal separator highlight along the split.
- 1× `<linearGradient>` for the tinted overlay, letting the duotone region feel less flat.
- 1× `<filter id="textShadow">` using `feOffset + feGaussianBlur + feMerge` for readable premium typography.
- 1× `<filter id="softGlow">` using `feGaussianBlur` for a subtle accent glow behind the year badge.
- 8× `<text>` elements for masthead, issue metadata, main title, highlighted year, subtitle, and small cover lines.
- 1× `<rect>` for the small yellow accent rule beside the feature text.
- 1× `<circle>` for a glowing editorial badge behind the highlighted year.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="navyDuotone" x1="0" y1="190" x2="980" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#071427" stop-opacity="0.92"/>
      <stop offset="0.55" stop-color="#0F2748" stop-opacity="0.84"/>
      <stop offset="1" stop-color="#163A64" stop-opacity="0.76"/>
    </linearGradient>

    <linearGradient id="vignette" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#000000" stop-opacity="0.20"/>
      <stop offset="0.55" stop-color="#000000" stop-opacity="0.02"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0.34"/>
    </linearGradient>

    <filter id="textShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="4" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="16"/>
    </filter>
  </defs>

  <image
    href="https://images.example.com/full-bleed-modern-office-in-forest-hero-photo.jpg"
    x="0" y="0" width="1280" height="720"
    preserveAspectRatio="xMidYMid slice"/>

  <rect x="0" y="0" width="1280" height="720" fill="url(#vignette)"/>

  <!-- Main diagonal duotone field: edit the points to change the split angle -->
  <path d="M 0 205 L 0 720 L 1280 720 L 1280 560 Z" fill="url(#navyDuotone)"/>

  <!-- Darker base band adds magazine-cover weight at the bottom -->
  <path d="M 0 520 L 0 720 L 1280 720 L 1280 640 Z" fill="#03101F" opacity="0.42"/>

  <!-- Crisp diagonal highlight separating photo and tinted zone -->
  <line x1="0" y1="205" x2="1280" y2="560" stroke="#FFFFFF" stroke-opacity="0.34" stroke-width="2"/>

  <!-- Masthead -->
  <text x="640" y="92" width="1120"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="66" font-weight="800"
        letter-spacing="5"
        fill="#FFFFFF"
        filter="url(#textShadow)">PHOTO MAGZ</text>

  <text x="640" y="126" width="620"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="600"
        letter-spacing="4"
        fill="#FFFFFF" opacity="0.82">ARCHITECTURE · WORKSPACE · FUTURE LIVING</text>

  <!-- Small cover metadata -->
  <text x="70" y="70" width="230"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="700"
        letter-spacing="2"
        fill="#FFFFFF" opacity="0.88">SPECIAL ISSUE</text>

  <text x="1045" y="70" width="170"
        text-anchor="end"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="700"
        letter-spacing="2"
        fill="#FFFFFF" opacity="0.88">VOL. 08 / 2024</text>

  <!-- Editorial feature block in the tinted diagonal zone -->
  <rect x="72" y="452" width="7" height="126" rx="3.5" fill="#FFCC00"/>

  <text x="96" y="474" width="620"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="58" font-weight="800"
        line-height="1.05"
        fill="#FFFFFF"
        filter="url(#textShadow)">
    <tspan x="96" dy="0">OFFICE</tspan>
    <tspan x="96" dy="62">IN NATURE</tspan>
  </text>

  <circle cx="545" cy="555" r="48" fill="#FFCC00" opacity="0.36" filter="url(#softGlow)"/>
  <text x="506" y="571" width="145"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="42" font-weight="900"
        letter-spacing="-1"
        fill="#FFCC00"
        filter="url(#textShadow)">2024</text>

  <text x="96" y="626" width="590"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="500"
        fill="#FFFFFF" opacity="0.88">
    Biophilic workplaces, regenerative materials, and the new language of focused collaboration.
  </text>

  <text x="1035" y="646" width="180"
        text-anchor="end"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="700"
        letter-spacing="1.5"
        fill="#FFFFFF" opacity="0.78">
    DESIGN INDEX
  </text>

  <text x="1035" y="674" width="180"
        text-anchor="end"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="800"
        fill="#FFCC00">
    42 IDEAS
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG blend modes or CSS `mix-blend-mode` to create the duotone; PowerPoint translation may not preserve it. Use a semi-transparent dark polygon/gradient over the photo instead.
- ❌ Do not use `<mask>` to cut the diagonal tint; use an editable `<path>` polygon for the overlay.
- ❌ Do not apply `clip-path` to the navy overlay path; clipping non-image elements is ignored by the translator.
- ❌ Do not rely on `filter` effects on the diagonal separator `<line>`; line filters are dropped. Keep the separator simple.
- ❌ Do not omit `width` on any `<text>` element; PowerPoint needs explicit text box width for stable rendering.

## Composition notes
- Keep the diagonal tinted zone large enough for real typography: roughly the lower 35–45% of the slide, rising slightly from left to right.
- Use the clean photo area for the masthead and atmosphere; place the main title fully inside the dark duotone field.
- Use one bright accent color, typically yellow or warm orange, for a year, rule, or key word.
- The diagonal should feel intentional: align the feature block to a vertical grid while letting the angled edge create motion and editorial energy.