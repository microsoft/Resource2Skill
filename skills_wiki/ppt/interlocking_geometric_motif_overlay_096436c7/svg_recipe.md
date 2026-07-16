# SVG Recipe — Geometric Motif Title Overlay

## Visual mechanism
A full-bleed photo is anchored by an open, interlocking diamond motif drawn with thick luminous strokes, allowing the image to remain visible through the geometry. A translucent lower-third panel creates a calm reading zone while the upper field carries the bold title and decorative outline structure.

## SVG primitives needed
- 1× `<image>` for the full-bleed contextual background photo.
- 2× `<rect>` overlays for darkening the image and creating the semi-transparent frosted lower-third panel.
- 6× rotated `<rect>` elements for the interlocking diamond/rhombus motif outlines.
- 6× `<line>` elements for horizontal connector strokes extending the motif toward the slide edges.
- 3× `<path>` elements for subtle angular accent shards behind the main motif.
- 2× `<linearGradient>` definitions for image tinting and lower-panel polish.
- 1× `<filter id="titleShadow">` applied to the large title text.
- 1× `<filter id="panelShadow">` applied to the lower-third panel.
- 3× `<text>` elements for title, subtitle, and body copy; each includes an explicit `width`.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="photoVignette" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#07111f" stop-opacity="0.72"/>
      <stop offset="48%" stop-color="#0b1422" stop-opacity="0.34"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.68"/>
    </linearGradient>

    <linearGradient id="panelFill" x1="0" y1="470" x2="0" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.88"/>
      <stop offset="100%" stop-color="#f4f7fb" stop-opacity="0.82"/>
    </linearGradient>

    <linearGradient id="goldStroke" x1="230" y1="120" x2="1050" y2="450" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#ffde66"/>
      <stop offset="42%" stop-color="#ffc000"/>
      <stop offset="100%" stop-color="#ff9f1c"/>
    </linearGradient>

    <filter id="titleShadow" x="-20%" y="-40%" width="140%" height="180%">
      <feOffset dx="0" dy="5" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="panelShadow" x="-5%" y="-25%" width="110%" height="140%">
      <feOffset dx="0" dy="-8" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="12" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <image href="https://images.example.com/full-bleed-modern-business-workspace-at-night.jpg"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#photoVignette)"/>

  <path d="M95 165 L210 104 L306 188 L188 250 Z" fill="#ffffff" opacity="0.045"/>
  <path d="M1030 118 L1190 188 L1110 296 L965 225 Z" fill="#ffc000" opacity="0.075"/>
  <path d="M342 392 L455 316 L528 401 L409 470 Z" fill="#ffffff" opacity="0.055"/>

  <line x1="0" y1="310" x2="395" y2="310" stroke="url(#goldStroke)" stroke-width="7" opacity="0.96"/>
  <line x1="885" y1="310" x2="1280" y2="310" stroke="url(#goldStroke)" stroke-width="7" opacity="0.96"/>
  <line x1="78" y1="352" x2="356" y2="352" stroke="#ffffff" stroke-width="2.5" opacity="0.42"/>
  <line x1="924" y1="352" x2="1202" y2="352" stroke="#ffffff" stroke-width="2.5" opacity="0.42"/>
  <line x1="154" y1="270" x2="372" y2="270" stroke="#ffc000" stroke-width="3" opacity="0.55"/>
  <line x1="908" y1="270" x2="1126" y2="270" stroke="#ffc000" stroke-width="3" opacity="0.55"/>

  <rect x="545" y="205" width="190" height="190"
        transform="rotate(45 640 300)"
        fill="none" stroke="url(#goldStroke)" stroke-width="9"/>

  <rect x="450" y="232" width="132" height="132"
        transform="rotate(45 516 298)"
        fill="none" stroke="url(#goldStroke)" stroke-width="7" opacity="0.95"/>

  <rect x="698" y="232" width="132" height="132"
        transform="rotate(45 764 298)"
        fill="none" stroke="url(#goldStroke)" stroke-width="7" opacity="0.95"/>

  <rect x="366" y="249" width="96" height="96"
        transform="rotate(45 414 297)"
        fill="none" stroke="#ffffff" stroke-width="3" opacity="0.48"/>

  <rect x="818" y="249" width="96" height="96"
        transform="rotate(45 866 297)"
        fill="none" stroke="#ffffff" stroke-width="3" opacity="0.48"/>

  <rect x="581" y="241" width="118" height="118"
        transform="rotate(45 640 300)"
        fill="none" stroke="#ffffff" stroke-width="2.5" opacity="0.34"/>

  <text x="640" y="315" width="560"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="58" font-weight="800"
        letter-spacing="4"
        fill="#ffffff"
        filter="url(#titleShadow)">THANK YOU</text>

  <text x="640" y="365" width="500"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="600"
        letter-spacing="3"
        fill="#ffcf3a"
        opacity="0.95">FOR YOUR TIME AND PARTNERSHIP</text>

  <rect x="0" y="468" width="1280" height="252"
        fill="url(#panelFill)"
        filter="url(#panelShadow)"/>

  <line x1="410" y1="510" x2="870" y2="510" stroke="#ffc000" stroke-width="4"/>
  <line x1="510" y1="525" x2="770" y2="525" stroke="#202a38" stroke-width="1.5" opacity="0.22"/>

  <text x="250" y="570" width="780"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="700"
        fill="#273142">Let’s build the next phase with clarity, speed, and confidence.</text>

  <text x="250" y="620" width="780"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17"
        fill="#3f4650">Use the lower panel for a concise closing message, executive summary, contact cue, or section-divider statement. Keep the copy centered and brief so the geometric motif remains the visual anchor.</text>
</svg>
```

## Avoid in this skill
- ❌ Applying `clip-path` or masking to the diamond outlines; keep the motif as transparent stroked geometry so it remains editable.
- ❌ Using `<pattern>` fills for the frosted panel; use translucent gradients or solid fills instead.
- ❌ Putting a filter on the connector `<line>` elements; line filters are dropped by the translator.
- ❌ Overcrowding the lower-third panel with multiple columns or dense bullets; this technique relies on a calm, premium closing-slide feel.
- ❌ Using filled diamonds behind the title; the core effect depends on open, image-revealing geometry.

## Composition notes
- Place the motif center around the upper-middle of the slide, roughly `y=290–320`, leaving the lower third reserved for readable copy.
- Keep the title inside the central diamond and use a darkened photo vignette so white text stays legible.
- Let the gold connector lines extend horizontally beyond the diamonds to create a strong stage-like axis.
- Use the lower-third panel at about 32–36% slide height with generous side margins and centered text for a polished keynote look.