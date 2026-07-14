# SVG Recipe — Continuous Blurred-Background Aesthetic (Apple Presentation Style)

## Visual mechanism
Use a full-slide, photo-like abstract background made from large soft color fields, then heavily blur and dim only the decorative background layer so the slide feels cinematic while white typography stays crisp. Place concise, center-weighted text and small translucent “glass” UI pills over the blurred canvas to create a premium Apple-style keynote look.

## SVG primitives needed
- 1× `<rect>` for the full-canvas base color
- 1× filtered `<g>` containing decorative background color fields
- 4–6× `<ellipse>` for blurred photographic light/color blobs
- 2× `<linearGradient>` for atmospheric background and glass/pill fills
- 1× `<filter>` with Gaussian blur applied only to the decorative background group
- 1× semi-transparent `<rect>` overlay for dimming and legibility
- 1× translucent rounded `<rect>` for the central glass content panel
- 3–5× small rounded `<rect>` pills for navigation/status tabs
- 4–6× `<text>` elements for title, subtitle, navigation labels, and compact body copy
- Optional 1–2× `<line>` elements for subtle dividers, without arrows

## Safe-subset SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="baseAtmosphere" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#071426"/>
      <stop offset="42%" stop-color="#17213f"/>
      <stop offset="100%" stop-color="#2b1630"/>
    </linearGradient>

    <linearGradient id="glassFill" x1="360" y1="170" x2="920" y2="540">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.20"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0.07"/>
    </linearGradient>

    <linearGradient id="pillFill" x1="0" y1="0" x2="160" y2="44">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.26"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0.10"/>
    </linearGradient>

    <filter id="backgroundBlur" x="-120" y="-120" width="1520" height="960">
      <feGaussianBlur stdDeviation="34"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#baseAtmosphere)"/>

  <g filter="url(#backgroundBlur)" opacity="0.95">
    <ellipse cx="180" cy="130" rx="310" ry="210" fill="#5cc8ff" opacity="0.55"/>
    <ellipse cx="1030" cy="95" rx="360" ry="250" fill="#ff8ad8" opacity="0.42"/>
    <ellipse cx="690" cy="350" rx="420" ry="260" fill="#6b7cff" opacity="0.45"/>
    <ellipse cx="310" cy="650" rx="390" ry="230" fill="#ffb35c" opacity="0.28"/>
    <ellipse cx="1080" cy="610" rx="320" ry="210" fill="#40f0c8" opacity="0.25"/>
    <ellipse cx="650" cy="80" rx="260" ry="150" fill="#ffffff" opacity="0.13"/>
  </g>

  <rect x="0" y="0" width="1280" height="720" fill="#080812" opacity="0.36"/>

  <g>
    <rect x="486" y="48" width="308" height="44" rx="22" fill="url(#pillFill)" stroke="#ffffff" stroke-opacity="0.24"/>
    <text x="532" y="76" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600" fill="#ffffff" opacity="0.94">Team</text>
    <text x="628" y="76" width="78" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="400" fill="#ffffff" opacity="0.62">Timing</text>
    <text x="722" y="76" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="400" fill="#ffffff" opacity="0.62">Budget</text>
  </g>

  <rect x="330" y="164" width="620" height="384" rx="34" fill="url(#glassFill)" stroke="#ffffff" stroke-opacity="0.26"/>

  <text x="390" y="266" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="68" font-weight="700" fill="#ffffff" text-anchor="middle">
    Launch clarity
  </text>
  <text x="390" y="313" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="400" fill="#ffffff" opacity="0.78" text-anchor="middle">
    A calm, cinematic canvas for executive stories.
  </text>

  <line x1="452" y1="356" x2="828" y2="356" stroke="#ffffff" stroke-opacity="0.28" stroke-width="1"/>

  <text x="435" y="405" width="410" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="400" fill="#ffffff" opacity="0.82">
    Keep the message concise. Let the softened background carry depth while the foreground remains minimal, centered, and highly legible.
  </text>

  <g transform="translate(508 462)">
    <rect x="0" y="0" width="264" height="48" rx="24" fill="#ffffff" opacity="0.92"/>
    <text x="42" y="31" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#10131f">
      Continue the story
    </text>
  </g>

  <g transform="translate(100 622)">
    <circle cx="18" cy="18" r="18" fill="#ffffff" opacity="0.18"/>
    <circle cx="58" cy="18" r="18" fill="#ffffff" opacity="0.10"/>
    <circle cx="98" cy="18" r="18" fill="#ffffff" opacity="0.10"/>
    <text x="132" y="24" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#ffffff" opacity="0.58">
      Continuous background system
    </text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Applying blur filters to text, buttons, arrows, or foreground panels; PPT-Master may rasterize that subtree and make text uneditable.
- ❌ Using `<image>` inside the SVG recipe; instead, represent the look with editable gradient/ellipse fields or handle real photography as a separate full-slide background asset.
- ❌ Overloading the slide with paragraphs or dense bullet lists; the style depends on short, keynote-like copy.
- ❌ Hard opaque panels that cover most of the background; the premium effect comes from visible blurred color around the content.
- ❌ Complex transforms, masks, clipping, or paths for glass shapes; use rounded `<rect>` and simple circles/ellipses only.

## Composition notes
- Keep the visual focus in the middle 45–55% of the canvas; leave large blurred margins visible on all sides.
- Use white typography with opacity variation for hierarchy: title near 100%, subtitle around 70–80%, metadata around 50–65%.
- Navigation pills belong near the top center, small enough to feel like UI chrome rather than main content.
- The background should have slow color rhythm: 3–5 large blurred blobs, dark overlay, and no sharp decorative details competing with text.