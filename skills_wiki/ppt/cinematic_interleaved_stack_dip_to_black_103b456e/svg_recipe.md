# SVG Recipe — Cinematic Interleaved Stack (Dip-to-Black Carousel)

## Visual mechanism
A single slide contains a bottom-to-top stack of full-bleed images interleaved with pure black rectangles, with all headline text placed above the stack as a static foreground. After SVG-to-PPT conversion, apply sequential Fade Exit animations to the stacked background layers to create a cinematic dip-to-black carousel while the message remains locked in place.

## SVG primitives needed
- 3× `<image>` for full-bleed cinematic background frames
- 2× `<rect>` for full-slide pure black dip frames interleaved between images
- 3× `<rect>` with gradient fills for static vignette/readability overlays
- 1× `<filter id="headlineShadow">` applied to headline and metadata text
- 1× `<filter id="softPanelShadow">` applied to the red live tag
- 1× `<rect>` for the red live/accent brand block
- 1× `<path>` for a sharp editorial underline/accent slash
- 1× `<line>` for the thin lower ticker divider
- 5× `<text>` with explicit `width` attributes for static headline, tag, kicker, timestamp, and ticker text
- 3× `<linearGradient>` / `<radialGradient>` for cinematic darkening, left-side text contrast, and subtle bottom fade

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="leftReadability" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#000000" stop-opacity="0.78"/>
      <stop offset="42%" stop-color="#000000" stop-opacity="0.48"/>
      <stop offset="72%" stop-color="#000000" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="bottomFade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="58%" stop-color="#000000" stop-opacity="0.42"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.88"/>
    </linearGradient>

    <radialGradient id="cornerVignette" cx="50%" cy="42%" r="78%">
      <stop offset="0%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="68%" stop-color="#000000" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.58"/>
    </radialGradient>

    <filter id="headlineShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="5" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softPanelShadow" x="-30%" y="-30%" width="160%" height="180%">
      <feOffset dx="0" dy="8" in="SourceAlpha" result="tagOff"/>
      <feGaussianBlur in="tagOff" stdDeviation="8" result="tagBlur"/>
      <feMerge>
        <feMergeNode in="tagBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- BACKGROUND STACK: apply Fade Exit sequentially to these layers in PowerPoint -->
  <!-- Layer 01, bottom frame -->
  <image href="https://images.unsplash.com/photo-1494526585095-c41746248156?auto=format&amp;fit=crop&amp;w=1920&amp;q=80"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>

  <!-- Layer 02, black dip -->
  <rect x="0" y="0" width="1280" height="720" fill="#000000"/>

  <!-- Layer 03, middle frame -->
  <image href="https://images.unsplash.com/photo-1518005020951-eccb494ad742?auto=format&amp;fit=crop&amp;w=1920&amp;q=80"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>

  <!-- Layer 04, black dip -->
  <rect x="0" y="0" width="1280" height="720" fill="#000000"/>

  <!-- Layer 05, top/current frame -->
  <image href="https://images.unsplash.com/photo-1495020689067-958852a7765e?auto=format&amp;fit=crop&amp;w=1920&amp;q=80"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>

  <!-- STATIC FOREGROUND: keep these above the animated stack -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#cornerVignette)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#leftReadability)"/>
  <rect x="0" y="425" width="1280" height="295" fill="url(#bottomFade)"/>

  <path d="M86 548 L365 548 L352 562 L73 562 Z" fill="#D00000" opacity="0.95"/>

  <rect x="84" y="450" width="112" height="52" rx="0" fill="#CC0000" filter="url(#softPanelShadow)"/>
  <text x="111" y="484" width="70"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="800" letter-spacing="2"
        fill="#FFFFFF">LIVE</text>

  <text x="214" y="486" width="430"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" letter-spacing="3"
        fill="#FFFFFF" opacity="0.92" filter="url(#headlineShadow)">GLOBAL WATCH / BREAKING SEQUENCE</text>

  <text x="82" y="574" width="780"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="54" font-weight="800"
        fill="#FFFFFF" filter="url(#headlineShadow)">
    <tspan x="82" dy="0">World in motion</tspan>
    <tspan x="82" dy="62">as events unfold live</tspan>
  </text>

  <text x="86" y="655" width="570"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" font-weight="400"
        fill="#D8DDE6" filter="url(#headlineShadow)">
    A single anchored message over a rhythmic dip-to-black image carousel.
  </text>

  <line x1="84" y1="684" x2="1196" y2="684" stroke="#FFFFFF" stroke-opacity="0.28" stroke-width="1.4"/>

  <text x="86" y="706" width="760"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="600" letter-spacing="1.8"
        fill="#FFFFFF" opacity="0.72">NEXT: SELECT BACKGROUND STACK → APPLY FADE EXIT → START AFTER PREVIOUS</text>

  <text x="1010" y="706" width="190"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="700" text-anchor="end"
        fill="#FFFFFF" opacity="0.76">20:45 GMT</text>
</svg>
```

## Avoid in this skill
- ❌ SVG `<animate>` or `<animateTransform>` for the carousel; build the editable stack in SVG, then apply PowerPoint Fade Exit animations after conversion.
- ❌ Semi-transparent black interleave rectangles; the dip frames should be pure opaque black for a true cinematic blink.
- ❌ Placing headline text inside the animated layer stack; it must be added last so it remains static while backgrounds fade away.
- ❌ Using `<mask>` or clip paths on rectangles for vignettes; use editable gradient-filled rectangles instead.
- ❌ `marker-end` arrows or filter effects on `<line>` elements; use simple divider lines without filters.

## Composition notes
- Keep all background images and black dip rectangles exactly full-bleed at `0,0,1280,720`; even 1–2 px misalignment becomes visible during fades.
- Confine typography to the lower-left 30–35% of the slide, leaving the upper and right side for cinematic atmosphere.
- The foreground overlays should be static and above the background stack: left gradient for text contrast, bottom fade for headline anchoring, radial vignette for filmic depth.
- In PowerPoint, animate only the stacked background layers from top to bottom: top image fades out, black fades out, middle image fades out, black fades out, revealing the final image.