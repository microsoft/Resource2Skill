# SVG Recipe — Neon Ambient Glow & Interactive Glassmorphism Menu

## Visual mechanism
A dark-mode slide is anchored by a large, blurred neon orb that behaves like an ambient light source. A semi-transparent rounded “glass” navigation pill floats above it, with crisp line icons, active-state highlights, and restrained white typography to create an app-like interactive keynote interface.

## SVG primitives needed
- 1× `<rect>` for the full dark background.
- 6–10× low-opacity `<line>` elements for subtle sci-fi background alignment guides.
- 3× blurred `<circle>` elements for layered neon ambient glow.
- 1× `<circle>` for the brighter inner neon core.
- 2× `<rect>` elements for the glassmorphic top menu shell and inner highlight layer.
- 1× `<rect>` for the active navigation indicator / selected tab glow.
- 12–18× `<path>` elements for editable minimalist navigation icons and decorative angular accents.
- 4–6× `<text>` elements with explicit `width` attributes for title, subtitle, labels, and microcopy.
- 1× `<linearGradient>` for glass fill.
- 1× `<radialGradient>` for the glow core.
- 2× `<filter>` elements: one heavy Gaussian blur for ambient neon, one offset blur merge for soft glass shadows.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="neonCore" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#B9FFF2" stop-opacity="1"/>
      <stop offset="35%" stop-color="#00FFB3" stop-opacity="0.85"/>
      <stop offset="70%" stop-color="#00A7FF" stop-opacity="0.36"/>
      <stop offset="100%" stop-color="#00A7FF" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="glassFill" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.16"/>
      <stop offset="52%" stop-color="#FFFFFF" stop-opacity="0.055"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.025"/>
    </linearGradient>

    <linearGradient id="activeFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#00FFB3" stop-opacity="0.36"/>
      <stop offset="100%" stop-color="#7F45FF" stop-opacity="0.18"/>
    </linearGradient>

    <filter id="ambientBlur" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="58"/>
    </filter>

    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="180%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="24"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="smallGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="8"/>
    </filter>
  </defs>

  <!-- Deep void background -->
  <rect x="0" y="0" width="1280" height="720" fill="#140B12"/>

  <!-- Subtle background structure -->
  <line x1="160" y1="170" x2="1120" y2="170" stroke="#FFFFFF" stroke-opacity="0.035" stroke-width="1"/>
  <line x1="160" y1="552" x2="1120" y2="552" stroke="#FFFFFF" stroke-opacity="0.035" stroke-width="1"/>
  <line x1="286" y1="120" x2="286" y2="620" stroke="#FFFFFF" stroke-opacity="0.028" stroke-width="1"/>
  <line x1="994" y1="120" x2="994" y2="620" stroke="#FFFFFF" stroke-opacity="0.028" stroke-width="1"/>
  <line x1="392" y1="600" x2="888" y2="120" stroke="#00FFB3" stroke-opacity="0.04" stroke-width="1"/>
  <line x1="888" y1="600" x2="392" y2="120" stroke="#7F45FF" stroke-opacity="0.04" stroke-width="1"/>

  <!-- Ambient neon light stack -->
  <circle cx="640" cy="374" r="190" fill="#00FFB3" fill-opacity="0.55" filter="url(#ambientBlur)"/>
  <circle cx="590" cy="394" r="142" fill="#00A7FF" fill-opacity="0.36" filter="url(#ambientBlur)"/>
  <circle cx="704" cy="326" r="118" fill="#8730EA" fill-opacity="0.30" filter="url(#ambientBlur)"/>
  <circle cx="640" cy="370" r="168" fill="url(#neonCore)" opacity="0.72"/>

  <!-- Decorative angular orbit accents -->
  <path d="M397 351 C431 250 523 198 640 198 C760 198 853 253 886 356" fill="none" stroke="#FFFFFF" stroke-opacity="0.13" stroke-width="1.4" stroke-dasharray="6 14"/>
  <path d="M430 448 C480 515 552 548 640 548 C731 548 806 512 850 442" fill="none" stroke="#00FFB3" stroke-opacity="0.18" stroke-width="1.5" stroke-dasharray="2 12"/>
  <path d="M496 268 L520 244 L548 251" fill="none" stroke="#FFFFFF" stroke-opacity="0.30" stroke-width="2"/>
  <path d="M787 490 L816 498 L835 474" fill="none" stroke="#FFFFFF" stroke-opacity="0.22" stroke-width="2"/>
  <path d="M830 272 L858 248 L893 260" fill="none" stroke="#00FFB3" stroke-opacity="0.25" stroke-width="2"/>

  <!-- Glassmorphism navigation menu -->
  <rect x="290" y="34" width="700" height="78" rx="39" fill="#000000" fill-opacity="0.22" filter="url(#softShadow)"/>
  <rect x="290" y="34" width="700" height="78" rx="39" fill="url(#glassFill)" stroke="#FFFFFF" stroke-opacity="0.20" stroke-width="1.4"/>
  <rect x="306" y="44" width="668" height="22" rx="11" fill="#FFFFFF" fill-opacity="0.055"/>
  <rect x="332" y="51" width="112" height="44" rx="22" fill="url(#activeFill)" stroke="#00FFB3" stroke-opacity="0.42" stroke-width="1"/>
  <rect x="366" y="101" width="44" height="4" rx="2" fill="#00FFB3" opacity="0.95" filter="url(#smallGlow)"/>

  <!-- Menu icon 1: active hypothesis / delta -->
  <g transform="translate(368 62)" stroke="#FFFFFF" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round" fill="none">
    <path d="M18 0 L34 28 L2 28 Z"/>
    <path d="M18 9 L18 20"/>
  </g>
  <text x="332" y="126" width="112" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#FFFFFF" fill-opacity="0.80" text-anchor="middle">
    <tspan x="388">Hypothesis</tspan>
  </text>

  <!-- Menu icon 2: target -->
  <g transform="translate(506 61)" stroke="#FFFFFF" stroke-opacity="0.48" stroke-width="2.2" stroke-linecap="round" fill="none">
    <circle cx="18" cy="18" r="15"/>
    <circle cx="18" cy="18" r="7"/>
    <path d="M18 3 L18 9 M18 27 L18 33 M3 18 L9 18 M27 18 L33 18"/>
  </g>

  <!-- Menu icon 3: nodes -->
  <g transform="translate(636 62)" stroke="#FFFFFF" stroke-opacity="0.42" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" fill="none">
    <circle cx="7" cy="9" r="4"/>
    <circle cx="29" cy="7" r="4"/>
    <circle cx="20" cy="29" r="4"/>
    <path d="M11 10 L25 8 M9 13 L18 25 M27 11 L21 25"/>
  </g>

  <!-- Menu icon 4: interface card -->
  <g transform="translate(766 62)" stroke="#FFFFFF" stroke-opacity="0.42" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" fill="none">
    <path d="M3 6 Q3 3 6 3 L32 3 Q35 3 35 6 L35 30 Q35 33 32 33 L6 33 Q3 33 3 30 Z"/>
    <path d="M9 11 L24 11 M9 19 L29 19 M9 27 L18 27"/>
  </g>

  <!-- Menu icon 5: settings -->
  <g transform="translate(898 62)" stroke="#FFFFFF" stroke-opacity="0.42" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" fill="none">
    <circle cx="18" cy="18" r="5"/>
    <path d="M18 2 L18 7 M18 29 L18 34 M2 18 L7 18 M29 18 L34 18"/>
    <path d="M6.5 6.5 L10 10 M26 26 L29.5 29.5 M29.5 6.5 L26 10 M10 26 L6.5 29.5"/>
  </g>

  <!-- Central content -->
  <text x="240" y="327" width="800" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="78" font-weight="700" fill="#FFFFFF" text-anchor="middle" letter-spacing="-2">
    <tspan x="640">Hypothesis</tspan>
  </text>
  <text x="365" y="374" width="550" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="19" fill="#FFFFFF" fill-opacity="0.76" text-anchor="middle">
    <tspan x="640">Navigate a research story like a luminous product interface</tspan>
  </text>

  <!-- Frosted status card -->
  <rect x="456" y="428" width="368" height="86" rx="26" fill="#FFFFFF" fill-opacity="0.075" stroke="#FFFFFF" stroke-opacity="0.17" stroke-width="1"/>
  <rect x="475" y="448" width="46" height="46" rx="23" fill="#00FFB3" fill-opacity="0.16" stroke="#00FFB3" stroke-opacity="0.55"/>
  <path d="M489 471 L499 481 L510 458" fill="none" stroke="#DFFFF8" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="540" y="464" width="250" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#FFFFFF" fill-opacity="0.58">
    <tspan x="540">ACTIVE SECTION</tspan>
  </text>
  <text x="540" y="490" width="250" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="600" fill="#FFFFFF">
    <tspan x="540">Evidence model ready</tspan>
  </text>

  <!-- Bottom micro navigation cue -->
  <text x="480" y="652" width="320" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#FFFFFF" fill-opacity="0.46" text-anchor="middle">
    <tspan x="640">Duplicate this slide and move the active pill for Morph-style navigation</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<animate>` or `<animateTransform>` for the “interactive” feel; create separate slide states and use PowerPoint Morph instead.
- ❌ Do not use `<mask>` to fake frosted glass; use translucent rounded rectangles, gradients, strokes, and shadows.
- ❌ Do not apply blur filters to `<line>` elements; use blurred circles or rounded rectangles for glow.
- ❌ Do not rely on emoji icons inside the menu; draw icons with editable `<path>` and `<circle>` primitives for consistent PowerPoint rendering.
- ❌ Do not place clip paths on glass rectangles; clipping should only be used on `<image>` elements when needed.

## Composition notes
- Keep the top menu within the upper 15–18% of the slide so the center remains a dramatic content stage.
- Place the neon glow slightly behind the main title; the glow should be large enough to bleed beyond the title but not touch the slide edges.
- Use one saturated accent color as the active state, then desaturate inactive icons with opacity rather than changing hue.
- Preserve generous negative space around the orb; the premium effect comes from contrast between dark emptiness, soft neon, and crisp glass UI.