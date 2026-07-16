# SVG Recipe — Frosted Glass & Edge-Fade Legibility Overlays

## Visual mechanism
A full-bleed photograph remains emotionally dominant while a left-side legibility zone is created with a dark edge-fade plus a frosted-glass panel made from a blurred/darkened duplicate crop of the same image. Crisp white typography sits entirely inside the protected zone, preserving readability without using a crude opaque box.

## SVG primitives needed
- 1× full-slide `<image>` for the photographic background
- 1× duplicate `<image>` for the pre-blurred/darkened left crop, clipped into the frosted panel
- 1× `<clipPath>` with rounded `<rect>` applied only to the duplicate image
- 2× `<linearGradient>` for the left-to-right dark edge fade and subtle glass sheen
- 1× `<filter id="panelShadow">` using `feOffset + feGaussianBlur + feMerge` applied to the glass panel rect
- 1× `<rect>` for the frosted glass backing plate
- 1× `<rect>` for the broad transparent edge-fade overlay
- 1× `<rect>` for a faint inner highlight line on the glass panel
- 1× decorative `<path>` for an atmospheric contour accent behind the text
- 1× `<line>` for the small title rule
- 4× `<text>` blocks with explicit `width` attributes for eyebrow, headline, body copy, and metadata

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="edgeFade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#05070B" stop-opacity="0.92"/>
      <stop offset="54%" stop-color="#05070B" stop-opacity="0.70"/>
      <stop offset="82%" stop-color="#05070B" stop-opacity="0.26"/>
      <stop offset="100%" stop-color="#05070B" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="glassTint" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.18"/>
      <stop offset="34%" stop-color="#0D1420" stop-opacity="0.42"/>
      <stop offset="100%" stop-color="#02050A" stop-opacity="0.72"/>
    </linearGradient>

    <linearGradient id="hairline" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.50"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.05"/>
    </linearGradient>

    <filter id="panelShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="16" dy="18" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>

    <clipPath id="glassClip">
      <rect x="54" y="54" width="504" height="612" rx="34" ry="34"/>
    </clipPath>
  </defs>

  <image x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/full-bleed-kyoto-night-street-with-lanterns-and-people.jpg"/>

  <rect x="0" y="0" width="760" height="720" fill="url(#edgeFade)"/>

  <rect x="54" y="54" width="504" height="612" rx="34" ry="34"
        fill="#0A1019" opacity="0.64" filter="url(#panelShadow)"/>

  <image x="54" y="54" width="504" height="612" preserveAspectRatio="xMinYMid slice"
         clip-path="url(#glassClip)"
         opacity="0.58"
         href="https://images.example.com/preblurred-dark-left-crop-kyoto-night-street.jpg"/>

  <rect x="54" y="54" width="504" height="612" rx="34" ry="34"
        fill="url(#glassTint)" opacity="0.88"/>

  <rect x="76" y="78" width="460" height="1.5" rx="0.75"
        fill="url(#hairline)" opacity="0.78"/>

  <path d="M82 540 C150 486, 210 620, 292 548 C370 480, 436 526, 530 454"
        fill="none" stroke="#F6C66F" stroke-width="2.5" stroke-opacity="0.25"
        filter="url(#softGlow)"/>

  <text x="94" y="124" width="390"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" letter-spacing="4"
        fill="#F6C66F">DESTINATION INTELLIGENCE</text>

  <line x1="94" y1="153" x2="168" y2="153"
        stroke="#F6C66F" stroke-width="3" stroke-linecap="round"/>

  <text x="92" y="235" width="410"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="78" font-weight="800" letter-spacing="-2"
        fill="#FFFFFF">
    <tspan x="92" dy="0">KYOTO</tspan>
    <tspan x="92" dy="76" fill="#DCE8F7">AFTER</tspan>
    <tspan x="92" dy="76" fill="#DCE8F7">DARK</tspan>
  </text>

  <text x="98" y="454" width="372"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" font-weight="400"
        fill="#E9EEF6" opacity="0.94">
    <tspan x="98" dy="0">Lantern-lit alleys, layered temple silhouettes,</tspan>
    <tspan x="98" dy="31">and the quiet geometry of old streets create</tspan>
    <tspan x="98" dy="31">a premium cultural backdrop for executive</tspan>
    <tspan x="98" dy="31">travel, hospitality, and place-brand stories.</tspan>
  </text>

  <text x="98" y="624" width="360"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="600" letter-spacing="1.7"
        fill="#AEBBD0">
    <tspan fill="#F6C66F">Q4 FIELD NOTES</tspan>
    <tspan dx="14">|</tspan>
    <tspan dx="14">KANSAI REGION</tspan>
  </text>

  <rect x="1180" y="92" width="38" height="536" rx="19"
        fill="#000000" opacity="0.22"/>
  <circle cx="1199" cy="150" r="6" fill="#F6C66F" opacity="0.86"/>
  <circle cx="1199" cy="196" r="4" fill="#FFFFFF" opacity="0.42"/>
  <circle cx="1199" cy="242" r="4" fill="#FFFFFF" opacity="0.42"/>
</svg>
```

## Avoid in this skill
- ❌ CSS `backdrop-filter: blur(...)`; it will not become an editable PowerPoint frosted-glass effect.
- ❌ Applying `filter="url(#blur)"` directly to an `<image>` if you need guaranteed PPT editability; instead use a pre-blurred duplicate image asset or exported crop.
- ❌ Using `<mask>` to create the fade edge; use a native `<linearGradient>` fill on a rectangle.
- ❌ Clipping gradient or shape overlays with `clip-path`; clipping is reliable here only on `<image>`.
- ❌ Letting text extend into the transparent part of the fade; keep all critical copy inside the darkest 35–45% of the slide.
- ❌ Omitting `width` on `<text>` elements; PowerPoint translation needs explicit text box widths.

## Composition notes
- Keep the readable content zone to the left 40–45% of the canvas; the remaining right side should showcase the clearest subject or highest-emotion part of the photo.
- Use two layers for legibility: a broad dark edge-fade for seamless integration, plus a narrower frosted panel for dense copy.
- Align text with generous margins inside the panel: roughly 90–105 px from the left edge and no closer than 60 px to the panel’s right edge.
- Add restrained premium accents — a thin gold rule, hairline highlight, or soft contour path — but keep them low-opacity so the photography still feels continuous.