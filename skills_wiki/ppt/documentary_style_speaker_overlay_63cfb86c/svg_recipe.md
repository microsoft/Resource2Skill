# SVG Recipe — Documentary-Style Speaker Overlay

## Visual mechanism
A full-bleed interview image is grounded by a dark, cinematic left-side matte that creates a premium typography zone while leaving the speaker/photo dominant on the right. The hierarchy relies on oversized serif name text, tracked all-caps branding, subtle shadows, and generous vertical spacing.

## SVG primitives needed
- 1× `<image>` for the full-bleed documentary/interview background photo
- 1× `<rect>` for a full-slide dark translucent wash that improves text contrast over the photo
- 1× `<rect>` for the solid left navy editorial overlay panel
- 1× `<linearGradient>` for a soft feathered edge from the panel into the image
- 1× `<rect>` filled with the gradient for the panel-to-photo transition
- 1× `<filter id="textShadow">` using `feOffset+feGaussianBlur+feMerge` for broadcast-style text depth
- 1× `<filter id="panelShadow">` for a subtle separation shadow at the panel edge
- 4× `<text>` blocks for brand, speaker name, contextual italic phrase, and partner/topic
- Several `<tspan>` elements for multi-line name layout and mixed footer styling
- 3× small decorative `<line>` elements for minimal editorial separators/accent rules

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="panelFeather" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#101522" stop-opacity="0.98"/>
      <stop offset="58%" stop-color="#101522" stop-opacity="0.82"/>
      <stop offset="100%" stop-color="#101522" stop-opacity="0"/>
    </linearGradient>

    <filter id="textShadow" x="-20%" y="-20%" width="150%" height="150%">
      <feOffset dx="3" dy="4" result="off"/>
      <feGaussianBlur in="off" stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="panelShadow" x="-10%" y="0" width="130%" height="100%">
      <feOffset dx="8" dy="0" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Full-bleed documentary / webinar feed background -->
  <image
    href="https://images.example.com/full-bleed-documentary-interview-speaker-by-window.jpg"
    x="0" y="0" width="1280" height="720"
    preserveAspectRatio="xMidYMid slice"/>

  <!-- Overall cinematic dim so white type stays readable -->
  <rect x="0" y="0" width="1280" height="720" fill="#05070B" opacity="0.30"/>

  <!-- Solid editorial matte on the left third -->
  <rect x="0" y="0" width="430" height="720" fill="#101522" opacity="0.96" filter="url(#panelShadow)"/>

  <!-- Feathered blend so the panel feels integrated with the photo -->
  <rect x="360" y="0" width="230" height="720" fill="url(#panelFeather)"/>

  <!-- Minimal editorial accent rules -->
  <line x1="72" y1="158" x2="174" y2="158" stroke="#FFFFFF" stroke-width="2" opacity="0.34"/>
  <line x1="72" y1="545" x2="132" y2="545" stroke="#AAB4BE" stroke-width="2" opacity="0.45"/>
  <line x1="430" y1="0" x2="430" y2="720" stroke="#FFFFFF" stroke-width="1" opacity="0.08"/>

  <!-- Top brand: all caps, heavily tracked -->
  <text
    x="70" y="112" width="360"
    fill="#FFFFFF"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="31"
    font-weight="700"
    letter-spacing="9"
    filter="url(#textShadow)">
    SEQUOIA
  </text>

  <!-- Small geometric brand mark echo; editable paths instead of logo image -->
  <path d="M350 72 L350 128 L359 128 L359 72 Z" fill="#FFFFFF" opacity="0.92"/>
  <path d="M365 72 L365 128 L374 128 L374 72 Z" fill="#FFFFFF" opacity="0.92"/>
  <path d="M380 72 L380 100 L410 72 L421 72 L389 103 L422 128 L408 128 L380 106 L380 128 L389 128 L389 112 L400 121 L400 128 L380 128 Z" fill="#FFFFFF" opacity="0.92"/>

  <!-- Speaker name: large classic serif, documentary title-card scale -->
  <text
    x="68" y="300" width="470"
    fill="#FFFFFF"
    font-family="Georgia, 'Times New Roman', serif"
    font-size="78"
    font-weight="400"
    letter-spacing="-1"
    filter="url(#textShadow)">
    <tspan x="68" dy="0">Mike</tspan>
    <tspan x="68" dy="92">Vernal</tspan>
  </text>

  <!-- Footer context: italic serif connector -->
  <text
    x="70" y="622" width="180"
    fill="#FFFFFF"
    font-family="Georgia, 'Times New Roman', serif"
    font-size="50"
    font-style="italic"
    filter="url(#textShadow)">
    on
  </text>

  <!-- Footer topic / partner: serif italic phrase with wide breathing room -->
  <text
    x="176" y="622" width="420"
    fill="#FFFFFF"
    font-family="Georgia, 'Times New Roman', serif"
    font-size="50"
    font-style="italic"
    letter-spacing="1"
    filter="url(#textShadow)">
    Pitch Decks
  </text>

  <!-- Optional lower-left metadata, kept subdued -->
  <text
    x="72" y="680" width="330"
    fill="#AAB4BE"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="13"
    font-weight="600"
    letter-spacing="4">
    EXECUTIVE INTERVIEW
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to create the panel fade; use a native `<linearGradient>` fill on a rectangle instead.
- ❌ Do not place text without a `width` attribute; the PowerPoint translation needs fixed text boxes.
- ❌ Do not rely on CSS `text-shadow`; use an SVG `filter` with offset and blur on each text element.
- ❌ Do not use `<foreignObject>` for custom typography blocks; keep all typography as native `<text>` and `<tspan>`.
- ❌ Do not cover the speaker/photo area with too much opaque shape; the layout should preserve the documentary subject.

## Composition notes
- Keep the left matte around one third of the slide width; let the photo breathe across the remaining two thirds.
- Anchor brand at the upper-left, the speaker name near the vertical center, and the topic/footer near the lower-left.
- Use white text with subtle shadows for a broadcast look; reserve slate gray for metadata or secondary labels.
- The panel can be fully solid for maximum contrast or slightly feathered on the right edge for a more cinematic video-overlay feel.