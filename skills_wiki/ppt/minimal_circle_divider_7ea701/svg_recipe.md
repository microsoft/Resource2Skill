# SVG Recipe — Minimal Circle Divider

## Visual mechanism
A large, softly shaded circle is pushed off the left edge of a quiet canvas, creating a calm geometric anchor while the title stack sits in the open negative space on the right. Subtle halos, thin strokes, and tiny accent marks make the divider feel polished without adding visual noise.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 1× `<ellipse>` for the oversized off-canvas circle
- 2× `<circle>` for thin concentric divider rings
- 2× `<path>` for soft abstract highlight slivers inside the circle
- 3× `<rect>` for small editorial accent bars near the text
- 1× `<line>` for the understated kicker rule
- 4× `<text>` for faint section number, kicker, headline, and subhead
- 3× `<linearGradient>` for background, circle shading, and accent color
- 1× `<radialGradient>` for the soft halo fill
- 2× `<filter>` with `feGaussianBlur` / `feOffset` shadows applied to circles and paths

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#F8FAFC"/>
      <stop offset="0.55" stop-color="#F3F6FA"/>
      <stop offset="1" stop-color="#EEF3F8"/>
    </linearGradient>

    <linearGradient id="circleGrad" x1="-350" y1="150" x2="320" y2="600" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF"/>
      <stop offset="0.45" stop-color="#E7EEF7"/>
      <stop offset="1" stop-color="#CAD8E8"/>
    </linearGradient>

    <radialGradient id="haloGrad" cx="50%" cy="42%" r="62%">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.85"/>
      <stop offset="0.48" stop-color="#D7E5F4" stop-opacity="0.38"/>
      <stop offset="1" stop-color="#9DB6D4" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="accentGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#4F8BFF"/>
      <stop offset="1" stop-color="#77D7C8"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="16" dy="20" result="offset"/>
      <feGaussianBlur in="offset" stdDeviation="26" result="blur"/>
      <feColorMatrix in="blur" type="matrix"
        values="0 0 0 0 0.29  0 0 0 0 0.39  0 0 0 0 0.55  0 0 0 0.22 0" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="mistGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <circle cx="-18" cy="360" r="392" fill="url(#haloGrad)" opacity="0.78" filter="url(#mistGlow)"/>
  <ellipse cx="-32" cy="360" rx="338" ry="338" fill="url(#circleGrad)" filter="url(#softShadow)"/>

  <circle cx="-32" cy="360" r="276" fill="none" stroke="#FFFFFF" stroke-width="2.4" opacity="0.65"/>
  <circle cx="-32" cy="360" r="214" fill="none" stroke="#AFC1D5" stroke-width="1.2" stroke-dasharray="8 18" opacity="0.45"/>

  <path d="M118 168 C186 226 199 316 139 399 C103 449 50 481 -4 492 C78 419 84 322 42 256 C24 228 50 176 118 168 Z"
        fill="#FFFFFF" opacity="0.26"/>
  <path d="M-255 294 C-175 203 -42 171 69 219 C15 233 -43 270 -89 323 C-149 392 -211 413 -293 389 C-303 356 -292 319 -255 294 Z"
        fill="#BFD0E3" opacity="0.28"/>

  <rect x="107" y="98" width="14" height="72" rx="7" fill="url(#accentGrad)" opacity="0.85" transform="rotate(28 114 134)"/>
  <rect x="160" y="564" width="8" height="48" rx="4" fill="#FFFFFF" opacity="0.58" transform="rotate(-34 164 588)"/>
  <rect x="255" y="414" width="6" height="36" rx="3" fill="#4F8BFF" opacity="0.42" transform="rotate(18 258 432)"/>

  <text x="745" y="224" width="290"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="112" font-weight="700" letter-spacing="-5"
        fill="#D8E0EA" opacity="0.42">03</text>

  <line x1="646" y1="261" x2="706" y2="261" stroke="#4F8BFF" stroke-width="3" stroke-linecap="round"/>

  <text x="724" y="268" width="360"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="700" letter-spacing="3.5"
        fill="#4D6A86">SECTION THREE</text>

  <text x="642" y="342" width="510"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="58" font-weight="700" letter-spacing="-1.8"
        fill="#172335">
    <tspan x="642" dy="0">Strategy Reset</tspan>
  </text>

  <text x="646" y="405" width="455"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="400" line-height="1.35"
        fill="#607286">
    <tspan x="646" dy="0">A clean visual pause before the next idea:</tspan>
    <tspan x="646" dy="32">focused, modern, and intentionally quiet.</tspan>
  </text>

  <rect x="646" y="504" width="92" height="5" rx="2.5" fill="url(#accentGrad)"/>
  <rect x="752" y="504" width="28" height="5" rx="2.5" fill="#BAC8D8" opacity="0.7"/>
</svg>
```

## Avoid in this skill
- ❌ Centering the circle fully on-slide; the technique depends on the circle being cropped by the left canvas edge.
- ❌ Adding dense icon grids, charts, or multiple content columns; this is a low-density section divider.
- ❌ Heavy outlines around the main circle; use soft gradients, faint rings, and shadows instead.
- ❌ Applying filters to `<line>` elements; use filters only on circles, ellipses, paths, rects, or text.

## Composition notes
- Keep the left 40–45% of the slide dominated by the oversized circle; let it bleed off-canvas for a premium editorial feel.
- Place all meaningful text in the right-side negative space, vertically centered around the slide midpoint.
- Use one restrained accent color, repeated in the kicker rule and small bars, to avoid breaking the minimalist mood.
- The section number can sit behind the headline as a pale oversized text layer, but it should remain decorative and low-contrast.