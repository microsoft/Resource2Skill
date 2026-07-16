# SVG Recipe — Apple-Style Cinematic Minimalist Keynote (高对比度苹果风极简大字报)

## Visual mechanism
A near-black cinematic vignette creates a premium “stage” while one oversized, dead-centered phrase or number carries the entire message. Sparse gray microcopy and subtle blurred light blooms add depth without competing with the main words.

## SVG primitives needed
- 1× `<rect>` for the full-slide black base background
- 1× `<rect>` filled with `<radialGradient>` for the centered cinematic vignette
- 2× `<ellipse>` with blur filters for very subtle stage-light blooms
- 1× `<path>` for a soft abstract horizon/shadow shape behind the title
- 3× `<text>` blocks for eyebrow, massive keynote statement, and supporting subtitle
- 1× `<text>` with nested `<tspan>` for inline emphasis inside the hero statement
- 1× `<linearGradient>` for the hero text silver-white finish
- 1× `<radialGradient>` for the background spotlight
- 2× `<filter>` using `feGaussianBlur` / `feOffset+feGaussianBlur+feMerge` for glow and soft text shadow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="cinematicVignette" cx="50%" cy="45%" r="72%">
      <stop offset="0%" stop-color="#2B3036"/>
      <stop offset="38%" stop-color="#15181C"/>
      <stop offset="72%" stop-color="#050506"/>
      <stop offset="100%" stop-color="#000000"/>
    </radialGradient>

    <linearGradient id="heroSilver" x1="0" y1="250" x2="0" y2="455" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="52%" stop-color="#F1F2F4"/>
      <stop offset="100%" stop-color="#B9BDC4"/>
    </linearGradient>

    <linearGradient id="subtleHorizon" x1="240" y1="420" x2="1040" y2="520" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="50%" stop-color="#9AA4B2" stop-opacity="0.13"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>

    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="42"/>
    </filter>

    <filter id="heroShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10" result="offset"/>
      <feGaussianBlur in="offset" stdDeviation="16" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Pure black foundation -->
  <rect x="0" y="0" width="1280" height="720" fill="#000000"/>

  <!-- Premium dark radial stage -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#cinematicVignette)"/>

  <!-- Nearly invisible cinematic light blooms -->
  <ellipse cx="640" cy="350" rx="330" ry="155" fill="#5D6A78" opacity="0.14" filter="url(#softGlow)"/>
  <ellipse cx="640" cy="690" rx="520" ry="76" fill="#1D2834" opacity="0.45" filter="url(#softGlow)"/>

  <!-- Soft horizon / stage reflection behind the words -->
  <path d="M235 454 C380 419, 508 412, 640 423 C783 435, 895 418, 1045 452 C920 474, 776 489, 640 483 C500 477, 373 475, 235 454 Z"
        fill="url(#subtleHorizon)" opacity="0.8"/>

  <!-- Small keynote eyebrow -->
  <text x="640" y="190" width="760"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24"
        font-weight="600"
        fill="#8D939B"
        opacity="0.9">
    2026 STRATEGY KEYNOTE
  </text>

  <!-- Massive centered message -->
  <text x="640" y="382" width="1080"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="142"
        font-weight="800"
        fill="url(#heroSilver)"
        filter="url(#heroShadow)">
    <tspan>Less</tspan><tspan fill="#FFFFFF"> is </tspan><tspan>More.</tspan>
  </text>

  <!-- Minimal support line -->
  <text x="640" y="462" width="880"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="30"
        font-weight="400"
        fill="#A7ADB5">
    让观点更有力量，而不是让页面更拥挤
  </text>

  <!-- Tiny footer datum, optional executive restraint -->
  <text x="640" y="638" width="520"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18"
        font-weight="400"
        fill="#5F6670"
        opacity="0.82">
    One idea. One slide. Full attention.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Bullet lists, dense labels, table grids, axes, legends, or decorative infographic furniture
- ❌ Bright multicolor palettes; this style depends on black, charcoal, white, silver, and restrained gray
- ❌ Placing the headline off-center unless there is a deliberate hero photo/product object balancing it
- ❌ Drop shadows that look like UI cards; use only broad, cinematic softness
- ❌ Overusing glows, gradients, or background texture until the slide stops feeling minimal

## Composition notes
- Keep the main statement mathematically centered; it should occupy roughly 30–40% of the slide width/height and dominate instantly.
- Leave the edges almost empty and nearly black; the negative space is the premium signal.
- Use one tiny eyebrow above and one muted support line below only if they clarify the spoken point.
- Prefer white/silver typography on a charcoal vignette; any accent color should be rare, small, and intentional.