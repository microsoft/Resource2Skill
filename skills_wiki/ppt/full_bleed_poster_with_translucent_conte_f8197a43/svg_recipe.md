# SVG Recipe — Full-Bleed Poster with Translucent Content Panel

## Visual mechanism
A saturated full-bleed hero image fills the entire slide, then a semi-transparent “glass” content panel creates a controlled legibility zone for event details. The panel should feel like it belongs inside the artwork: lightly tinted, softly shadowed, and positioned to preserve the most expressive part of the background.

## SVG primitives needed
- 1× `<image>` for the edge-to-edge illustrated/photo background.
- 2× full-canvas `<rect>` overlays for vignette/dimming gradients that tame image contrast.
- 1× large rounded `<rect>` for the translucent content panel.
- 1× narrow rounded `<rect>` for an accent color bar inside the panel.
- 1× small `<circle>` or `<ellipse>` for decorative highlight/glow.
- 1× `<path>` for an organic decorative flourish behind or near the panel.
- 4× `<text>` blocks for eyebrow, main title, subtitle, and logistics; every text element must include `width`.
- 2× `<linearGradient>` for background shading and panel sheen.
- 1× `<radialGradient>` for the warm decorative glow.
- 2× `<filter>` definitions: one soft shadow for the glass panel and one subtle glow/shadow for headline text or decorative shapes.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="posterDim" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#061428" stop-opacity="0.25"/>
      <stop offset="55%" stop-color="#061428" stop-opacity="0.05"/>
      <stop offset="100%" stop-color="#061428" stop-opacity="0.62"/>
    </linearGradient>

    <linearGradient id="panelSheen" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.92"/>
      <stop offset="52%" stop-color="#FFF4F8" stop-opacity="0.80"/>
      <stop offset="100%" stop-color="#FFE1EC" stop-opacity="0.72"/>
    </linearGradient>

    <radialGradient id="pinkGlow" cx="50%" cy="50%" r="55%">
      <stop offset="0%" stop-color="#FF3B78" stop-opacity="0.55"/>
      <stop offset="65%" stop-color="#FF3B78" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#FF3B78" stop-opacity="0"/>
    </radialGradient>

    <filter id="panelShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="textLift" x="-10%" y="-20%" width="120%" height="140%">
      <feOffset dx="0" dy="3"/>
      <feGaussianBlur stdDeviation="3"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
  </defs>

  <image
    href="https://images.example.com/full-bleed-vibrant-ai-illustration-night-garden-lanterns-musicians.jpg"
    x="0" y="0" width="1280" height="720"
    preserveAspectRatio="xMidYMid slice"/>

  <rect x="0" y="0" width="1280" height="720" fill="url(#posterDim)"/>
  <rect x="0" y="0" width="1280" height="720" fill="#020817" opacity="0.10"/>

  <ellipse cx="1038" cy="525" rx="220" ry="150" fill="url(#pinkGlow)" filter="url(#softGlow)"/>

  <path
    d="M866,452 C915,411 1002,407 1054,437 C1116,473 1111,550 1058,580 C991,618 895,591 858,542 C835,511 835,478 866,452 Z"
    fill="#FF3B78"
    opacity="0.20"/>

  <rect
    x="402" y="366" width="742" height="274" rx="34" ry="34"
    fill="url(#panelSheen)"
    stroke="#FFFFFF"
    stroke-opacity="0.62"
    stroke-width="1.5"
    filter="url(#panelShadow)"/>

  <rect
    x="436" y="405" width="8" height="188" rx="4" ry="4"
    fill="#FF3366"/>

  <text
    x="64" y="60" width="520"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="20"
    font-weight="600"
    letter-spacing="2"
    fill="#FFFFFF"
    opacity="0.92"
    filter="url(#textLift)">
    SAN DIEGO CHINESE TOASTMASTERS
  </text>

  <text
    x="64" y="92" width="420"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="15"
    font-weight="400"
    fill="#FFFFFF"
    opacity="0.76">
    26th community speaking night
  </text>

  <text
    x="474" y="440" width="610"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="26"
    font-weight="700"
    letter-spacing="1.5"
    fill="#26304A">
    APRIL 28 · 7:00 PM PDT
  </text>

  <text
    x="474" y="500" width="610"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="58"
    font-weight="800"
    fill="#FF3366"
    filter="url(#textLift)">
    Hobby &amp; Passion
  </text>

  <text
    x="476" y="542" width="604"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="21"
    font-weight="500"
    fill="#26304A"
    opacity="0.88">
    Share what lights you up — stories, projects, obsessions, and creative sparks.
  </text>

  <text
    x="476" y="590" width="604"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="18"
    font-weight="500"
    fill="#26304A">
    <tspan x="476" dy="0">Zoom Meeting: 841 135 5373</tspan>
    <tspan x="476" dy="26">Passcode: 2024 · Guests welcome</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Putting text directly on the full-bleed image without a panel or dimming layer; busy artwork will destroy legibility.
- ❌ Using `backdrop-filter`, CSS blur, or masks to fake frosted glass; instead use translucent fills, gradients, strokes, and shadows that translate reliably.
- ❌ Applying `clip-path` to the translucent panel shape; clipping is only reliable for `<image>` elements.
- ❌ Overfilling the panel with many small text boxes; this technique works best with a poster-like hierarchy and generous spacing.
- ❌ Making the panel fully opaque unless the background is extremely chaotic; the key effect is letting image color bleed through.

## Composition notes
- Keep the hero image full bleed and reserve the most visually interesting subject area outside the panel, usually top-left or center-top.
- Place the translucent panel across the lower third to lower half; in landscape slides, a wide lower-right panel often feels more premium than a centered box.
- Use a warm off-white or pale pink panel tint when the background is dark/cool; pair it with one vivid accent color for the title and side bar.
- Add a subtle full-slide dimming gradient before the panel so the background remains cinematic but does not compete with the event information.