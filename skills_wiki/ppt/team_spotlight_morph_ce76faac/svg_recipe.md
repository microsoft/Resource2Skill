# SVG Recipe — Team Spotlight Morph

## Visual mechanism
A full-bleed row of vertical photo panels morphs between an equal-width gallery state and a spotlight state where one panel expands dramatically while the others contract into contextual slivers. The selected item receives a cinematic gradient scrim and bold name/title overlay, preserving group context while focusing attention.

## SVG primitives needed
- 4× `<image>` for the team/product/project photos, one per panel
- 4× `<clipPath>` with `<rect>` for cropping each image to its current panel bounds
- 4× transparent/dark `<rect>` overlays for dimming non-selected preview panels
- 1× `<linearGradient>` for the spotlight bottom scrim behind the text
- 1× `<linearGradient>` for subtle edge shine between panels
- 1× `<radialGradient>` for a soft focal glow on the expanded panel
- 1× `<filter id="textShadow">` applied to spotlight text
- 1× `<filter id="softShadow">` applied to the spotlight label card
- 2–4× `<text>` elements for name, role, small section label, and optional preview labels
- 3× `<line>` elements for thin separators between panels

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="clipA"><rect x="0" y="0" width="174" height="720"/></clipPath>
    <clipPath id="clipB"><rect x="174" y="0" width="704" height="720"/></clipPath>
    <clipPath id="clipC"><rect x="878" y="0" width="201" height="720"/></clipPath>
    <clipPath id="clipD"><rect x="1079" y="0" width="201" height="720"/></clipPath>

    <linearGradient id="bottomScrim" x1="0" y1="430" x2="0" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#000000" stop-opacity="0"/>
      <stop offset="0.45" stop-color="#000000" stop-opacity="0.45"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0.86"/>
    </linearGradient>

    <linearGradient id="edgeShine" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.0"/>
      <stop offset="0.5" stop-color="#ffffff" stop-opacity="0.45"/>
      <stop offset="1" stop-color="#ffffff" stop-opacity="0.0"/>
    </linearGradient>

    <radialGradient id="spotGlow" cx="50%" cy="42%" r="62%">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.13"/>
      <stop offset="0.55" stop-color="#ffffff" stop-opacity="0.02"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0.22"/>
    </radialGradient>

    <filter id="textShadow" x="-20%" y="-20%" width="140%" height="160%">
      <feOffset dx="0" dy="4" result="off"/>
      <feGaussianBlur in="off" stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="160%">
      <feOffset dx="0" dy="12" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#090B12"/>

  <!-- Spotlight state: second member expanded. Use the same image order on every Morph slide. -->
  <image href="https://images.example.com/team-portrait-ana-vertical.jpg"
         x="0" y="0" width="174" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipA)"/>
  <image href="https://images.example.com/team-portrait-marcus-vertical.jpg"
         x="174" y="0" width="704" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipB)"/>
  <image href="https://images.example.com/team-portrait-leila-vertical.jpg"
         x="878" y="0" width="201" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipC)"/>
  <image href="https://images.example.com/team-portrait-david-vertical.jpg"
         x="1079" y="0" width="201" height="720" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipD)"/>

  <!-- Dim contextual preview panels. -->
  <rect x="0" y="0" width="174" height="720" fill="#02030A" opacity="0.48"/>
  <rect x="878" y="0" width="201" height="720" fill="#02030A" opacity="0.44"/>
  <rect x="1079" y="0" width="201" height="720" fill="#02030A" opacity="0.50"/>

  <!-- Expanded panel treatment. -->
  <rect x="174" y="0" width="704" height="720" fill="url(#spotGlow)" opacity="0.9"/>
  <rect x="174" y="410" width="704" height="310" fill="url(#bottomScrim)"/>

  <!-- Panel separators / premium glass edges. -->
  <line x1="174" y1="0" x2="174" y2="720" stroke="#FFFFFF" stroke-opacity="0.28" stroke-width="1"/>
  <line x1="878" y1="0" x2="878" y2="720" stroke="#FFFFFF" stroke-opacity="0.28" stroke-width="1"/>
  <line x1="1079" y1="0" x2="1079" y2="720" stroke="#FFFFFF" stroke-opacity="0.18" stroke-width="1"/>
  <rect x="172" y="0" width="4" height="720" fill="url(#edgeShine)" opacity="0.65"/>
  <rect x="876" y="0" width="4" height="720" fill="url(#edgeShine)" opacity="0.65"/>

  <!-- Spotlight metadata card. -->
  <rect x="226" y="514" width="420" height="118" rx="22" fill="#0B1020" opacity="0.42" filter="url(#softShadow)"/>
  <text x="226" y="490" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" letter-spacing="3" fill="#B7D7FF" opacity="0.96">
    LEADERSHIP SPOTLIGHT
  </text>
  <text x="226" y="568" width="560" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="58" font-weight="800" fill="#FFFFFF" filter="url(#textShadow)">
    Marcus Chen
  </text>
  <text x="230" y="608" width="500" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="500" fill="#D8E4F8" opacity="0.95">
    Chief Product Officer
  </text>

  <!-- Preview labels stay small; they give context without stealing focus. -->
  <text x="28" y="654" width="130" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="19" font-weight="700" fill="#FFFFFF" opacity="0.78">
    Ana
  </text>
  <text x="914" y="654" width="130" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="19" font-weight="700" fill="#FFFFFF" opacity="0.78">
    Leila
  </text>
  <text x="1114" y="654" width="130" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="19" font-weight="700" fill="#FFFFFF" opacity="0.72">
    David
  </text>

  <!-- Optional slide cue: small progress capsules. -->
  <rect x="548" y="36" width="34" height="5" rx="2.5" fill="#FFFFFF" opacity="0.35"/>
  <rect x="590" y="36" width="54" height="5" rx="2.5" fill="#FFFFFF" opacity="0.95"/>
  <rect x="652" y="36" width="34" height="5" rx="2.5" fill="#FFFFFF" opacity="0.35"/>
  <rect x="694" y="36" width="34" height="5" rx="2.5" fill="#FFFFFF" opacity="0.35"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<animate>` or `<animateTransform>` for the morph; create separate static slide states and apply PowerPoint Morph manually.
- ❌ Do not use `<mask>` for image fading; use editable gradient `<rect>` overlays instead.
- ❌ Do not apply `clip-path` to overlay rectangles or text; clipping is reliable here only on `<image>`.
- ❌ Do not use `<use>` to duplicate panel components; duplicate the actual image/overlay elements so PowerPoint can morph them predictably.
- ❌ Do not rely on `marker-end` arrows or line filters; this layout should feel photographic and cinematic, not diagrammatic.

## Composition notes
- Build one SVG per state: an equal four-panel gallery, then one spotlight slide per member. Keep photo order, element order, and image URLs consistent across slides so Morph has stable objects to interpolate.
- The expanded panel should occupy roughly 50–60% of the canvas width; the remaining panels become narrow but still recognizable previews.
- Put the main label in the lower third of the expanded panel over a dark gradient scrim; leave faces and key photo detail unobstructed.
- Use dim overlays on preview panels and a soft glow/scrim on the selected panel to create focus without fully hiding the group context.