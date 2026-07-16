# SVG Recipe — Centered Closing

## Visual mechanism
A single oversized centered message sits in a calm cinematic field, with subtle folded-paper planes and a soft central glow pulling all attention to the final statement. The slide should feel almost empty, but not plain: depth comes from gradients, translucent geometric folds, and a restrained accent underline.

## SVG primitives needed
- 1× `<rect>` for the full-bleed gradient background
- 2× `<ellipse>` for large blurred ambient light auras behind the headline
- 5× `<path>` for folded-paper side planes, central highlight wedge, and accent swoosh underline
- 4× `<line>` for faint fold seams and quiet horizontal framing rules
- 2× `<text>` for the centered closing headline and small closing note
- 3× `<linearGradient>` for the background, folded panels, and accent text/underline
- 2× `<radialGradient>` for soft background auras
- 2× `<filter>` with `feGaussianBlur` / `feOffset+feGaussianBlur+feMerge` for glow and soft shadow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGradient" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#08111F"/>
      <stop offset="0.48" stop-color="#10192A"/>
      <stop offset="1" stop-color="#050814"/>
    </linearGradient>

    <linearGradient id="leftFold" x1="0" y1="0" x2="560" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#24324A" stop-opacity="0.54"/>
      <stop offset="0.52" stop-color="#0D1525" stop-opacity="0.12"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0.34"/>
    </linearGradient>

    <linearGradient id="rightFold" x1="1280" y1="0" x2="710" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#1F3153" stop-opacity="0.48"/>
      <stop offset="0.58" stop-color="#0B1220" stop-opacity="0.08"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0.36"/>
    </linearGradient>

    <linearGradient id="accentGradient" x1="400" y1="0" x2="880" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#68E1FD"/>
      <stop offset="0.45" stop-color="#B38CFF"/>
      <stop offset="1" stop-color="#FFB86B"/>
    </linearGradient>

    <radialGradient id="centerAura" cx="50%" cy="48%" r="48%">
      <stop offset="0" stop-color="#7BA7FF" stop-opacity="0.34"/>
      <stop offset="0.48" stop-color="#5A6DFF" stop-opacity="0.12"/>
      <stop offset="1" stop-color="#5A6DFF" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="warmAura" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#FFB86B" stop-opacity="0.18"/>
      <stop offset="0.55" stop-color="#FFB86B" stop-opacity="0.06"/>
      <stop offset="1" stop-color="#FFB86B" stop-opacity="0"/>
    </radialGradient>

    <filter id="blurGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="28"/>
    </filter>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="16"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGradient)"/>

  <ellipse cx="640" cy="348" rx="390" ry="225" fill="url(#centerAura)" filter="url(#blurGlow)"/>
  <ellipse cx="668" cy="386" rx="260" ry="118" fill="url(#warmAura)" filter="url(#blurGlow)"/>

  <path d="M0 0 L418 0 C455 162 486 329 536 720 L0 720 Z"
        fill="url(#leftFold)"/>
  <path d="M1280 0 L858 0 C823 175 788 356 742 720 L1280 720 Z"
        fill="url(#rightFold)"/>
  <path d="M420 0 C508 146 565 266 640 360 C716 263 775 144 860 0 L420 0 Z"
        fill="#FFFFFF" opacity="0.045"/>
  <path d="M536 720 C582 520 611 430 640 360 C670 430 700 520 742 720 Z"
        fill="#FFFFFF" opacity="0.035"/>
  <path d="M438 425 C525 456 752 459 842 425"
        fill="none" stroke="url(#accentGradient)" stroke-width="7" stroke-linecap="round"
        opacity="0.86" filter="url(#softShadow)"/>

  <line x1="418" y1="0" x2="536" y2="720" stroke="#FFFFFF" stroke-width="1.2" opacity="0.11"/>
  <line x1="858" y1="0" x2="742" y2="720" stroke="#FFFFFF" stroke-width="1.2" opacity="0.10"/>
  <line x1="502" y1="220" x2="778" y2="220" stroke="#FFFFFF" stroke-width="1" opacity="0.10"/>
  <line x1="488" y1="500" x2="792" y2="500" stroke="#FFFFFF" stroke-width="1" opacity="0.08"/>

  <text x="640" y="324" width="920"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="76" font-weight="700" letter-spacing="-2.2"
        text-anchor="middle" fill="#F7FAFF" filter="url(#softShadow)">
    <tspan x="640" dy="0">Let’s build</tspan>
    <tspan x="640" dy="86" fill="url(#accentGradient)">what’s next.</tspan>
  </text>

  <text x="640" y="485" width="680"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="500" letter-spacing="3.5"
        text-anchor="middle" fill="#AEB9CC" opacity="0.78">
    THANK YOU
  </text>
</svg>
```

## Avoid in this skill
- ❌ Adding multiple content blocks, charts, icons, or callout cards; this skill works because the message is alone.
- ❌ Using a flat white background with only centered text; add subtle depth through gradients, folds, or glow.
- ❌ Applying `filter` to `<line>` elements for glowing rules; use opacity-only lines or put glow on a nearby `<path>`.
- ❌ Relying on auto-wrapped text without `width`; every `<text>` needs an explicit `width` for reliable PowerPoint rendering.
- ❌ Using masks or clip paths on non-image shapes for the vignette; build the atmosphere with gradients and translucent paths instead.

## Composition notes
- Keep the headline optically centered around the middle of the slide, with the full text block occupying roughly 45–55% of the canvas width.
- Use large negative space above and below; the background effects should support the message, not compete with it.
- Let the brightest glow sit directly behind the headline, while darker folded planes frame the left and right edges.
- Use one accent gradient only, preferably on the key word, punctuation, or a single underline stroke.