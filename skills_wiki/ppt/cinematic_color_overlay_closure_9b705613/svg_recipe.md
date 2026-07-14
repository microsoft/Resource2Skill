# SVG Recipe — Cinematic Color-Overlay Closure

## Visual mechanism
A full-bleed cinematic photograph is subdued by a strong translucent brand-color overlay, turning the image into atmospheric texture while preserving perfect white-text legibility. Centered oversized typography, a thin geometric halo, and restrained accent lines create a calm, premium closing-slide moment.

## SVG primitives needed
- 1× `<image>` for the full-bleed thematic background photo
- 4× `<rect>` for fallback color, full-slide color overlay, subtle vignette wash, and top/bottom cinematic letterbox bands
- 1× `<radialGradient>` for edge darkening / vignette depth
- 2× `<linearGradient>` for fallback background and brand overlay toning
- 1× `<ellipse>` for the delicate centered geometric accent
- 2× `<line>` for minimal horizontal divider accents around the subtitle
- 3× `<text>` for main title, bilingual subtitle, and small closing metadata
- 2× `<filter>` using blur/offset/merge for soft text shadow and subtle halo glow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="fallbackSkyline" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0B1E3A"/>
      <stop offset="45%" stop-color="#184C95"/>
      <stop offset="100%" stop-color="#06111F"/>
    </linearGradient>

    <linearGradient id="brandWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1D77D4" stop-opacity="0.78"/>
      <stop offset="52%" stop-color="#1856AB" stop-opacity="0.72"/>
      <stop offset="100%" stop-color="#102D66" stop-opacity="0.84"/>
    </linearGradient>

    <radialGradient id="edgeVignette" cx="50%" cy="46%" r="76%">
      <stop offset="0%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="62%" stop-color="#000000" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.42"/>
    </radialGradient>

    <filter id="softTextShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="haloGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="7"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#fallbackSkyline)"/>

  <image
    x="0" y="0" width="1280" height="720"
    preserveAspectRatio="xMidYMid slice"
    href="https://images.example.com/cinematic-blue-glass-skyscraper-night-city-full-bleed.jpg"
    xlink:href="https://images.example.com/cinematic-blue-glass-skyscraper-night-city-full-bleed.jpg"/>

  <rect x="0" y="0" width="1280" height="720" fill="url(#brandWash)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#edgeVignette)"/>

  <rect x="0" y="0" width="1280" height="58" fill="#020A14" opacity="0.22"/>
  <rect x="0" y="662" width="1280" height="58" fill="#020A14" opacity="0.22"/>

  <ellipse
    cx="640" cy="342" rx="225" ry="225"
    fill="none"
    stroke="#FFFFFF"
    stroke-width="1.4"
    stroke-opacity="0.72"/>

  <ellipse
    cx="640" cy="342" rx="226" ry="226"
    fill="none"
    stroke="#FFFFFF"
    stroke-width="3"
    stroke-opacity="0.16"
    filter="url(#haloGlow)"/>

  <line x1="472" y1="466" x2="548" y2="466" stroke="#FFFFFF" stroke-width="1.2" stroke-opacity="0.62"/>
  <line x1="732" y1="466" x2="808" y2="466" stroke="#FFFFFF" stroke-width="1.2" stroke-opacity="0.62"/>

  <text
    x="640" y="360"
    width="760"
    text-anchor="middle"
    font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif"
    font-size="92"
    font-weight="700"
    letter-spacing="7"
    fill="#FFFFFF"
    filter="url(#softTextShadow)">THANKS</text>

  <text
    x="640" y="475"
    width="620"
    text-anchor="middle"
    font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif"
    font-size="25"
    font-weight="300"
    letter-spacing="2.5"
    fill="#FFFFFF"
    opacity="0.88">欢迎指正 · Q &amp; A</text>

  <text
    x="640" y="618"
    width="760"
    text-anchor="middle"
    font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif"
    font-size="15"
    font-weight="400"
    letter-spacing="1.8"
    fill="#FFFFFF"
    opacity="0.54">STRATEGY REVIEW 2026  ·  BUILDING THE NEXT GROWTH CURVE</text>
</svg>
```

## Avoid in this skill
- ❌ Using a bright, high-contrast photo without a strong overlay; it will compete with the closing message.
- ❌ Placing text over detailed faces, signage, or busy architecture without additional darkening.
- ❌ Overdecorating the center with icons, charts, or multiple shapes; the closing slide should feel still and resolved.
- ❌ Applying `clip-path` or masks to non-image elements for the overlay; use simple full-slide rectangles instead.

## Composition notes
- Keep the main title locked to the exact center or slightly above center; the slide should feel symmetrical and conclusive.
- Let the photo occupy the whole canvas, but reduce it to texture with a 65–85% brand-color wash.
- Use one thin circle or ellipse as the only geometric accent; it should frame the message, not dominate it.
- Reserve the lower 15% for small closing metadata, contact line, or event name in low-opacity white.