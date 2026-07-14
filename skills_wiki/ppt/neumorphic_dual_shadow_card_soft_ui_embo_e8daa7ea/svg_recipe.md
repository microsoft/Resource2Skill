# SVG Recipe — Neumorphic Dual-Shadow Card (Soft UI Emboss)

## Visual mechanism
A rounded card appears physically raised from the slide by stacking two identical shapes: one casts a dark blurred shadow down-right, the other casts a bright blurred shadow up-left. The card uses no hard outline; separation comes entirely from soft opposing light.

## SVG primitives needed
- 1× `<rect>` for the full-slide mid-tone background that makes both white and dark shadows visible
- 2× `<rect>` for the duplicated main rounded card, each with a different shadow filter
- 2× `<filter>` using `feOffset + feGaussianBlur + feMerge` for the dark bottom-right shadow and light top-left shadow
- 1× `<linearGradient>` for a subtle background wash
- 1× `<radialGradient>` for a soft ambient glow behind the card
- 1× `<ellipse>` for the ambient glow field
- 3× `<circle>` for raised KPI/icon dots on the card
- 4× `<path>` for soft decorative interface/icon marks inside the card
- 1× `<rect>` for a raised mini-pill accent on the card
- Multiple `<text>` elements with explicit `width` attributes for title, subtitle, metrics, and label copy

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#21B493"/>
      <stop offset="0.52" stop-color="#19A082"/>
      <stop offset="1" stop-color="#128369"/>
    </linearGradient>

    <radialGradient id="ambientGlow" cx="50%" cy="42%" r="58%">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.22"/>
      <stop offset="0.58" stop-color="#FFFFFF" stop-opacity="0.06"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="cardFill" x1="360" y1="190" x2="920" y2="520" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF"/>
      <stop offset="1" stop-color="#F1FBF7"/>
    </linearGradient>

    <filter id="shadowDarkBR" x="-18%" y="-18%" width="140%" height="145%">
      <feOffset dx="18" dy="18" in="SourceAlpha" result="offset"/>
      <feGaussianBlur in="offset" stdDeviation="15" result="blur"/>
      <feFlood flood-color="#000000" flood-opacity="0.34" result="color"/>
      <feComposite in="color" in2="blur" operator="in" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="shadowLightTL" x="-20%" y="-20%" width="145%" height="145%">
      <feOffset dx="-16" dy="-16" in="SourceAlpha" result="offset"/>
      <feGaussianBlur in="offset" stdDeviation="15" result="blur"/>
      <feFlood flood-color="#FFFFFF" flood-opacity="0.42" result="color"/>
      <feComposite in="color" in2="blur" operator="in" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="microShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="7" dy="7" in="SourceAlpha" result="offset"/>
      <feGaussianBlur in="offset" stdDeviation="8" result="blur"/>
      <feFlood flood-color="#05745F" flood-opacity="0.22" result="color"/>
      <feComposite in="color" in2="blur" operator="in" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>
  <ellipse cx="640" cy="330" rx="520" ry="330" fill="url(#ambientGlow)"/>

  <text x="70" y="78" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#D9FFF4" opacity="0.78" letter-spacing="2">
    SOFT UI COMPONENT
  </text>
  <text x="70" y="124" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="700" fill="#FFFFFF">
    Neumorphic card
  </text>
  <text x="70" y="162" width="470" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#D9FFF4" opacity="0.82">
    Dual shadows create a tactile raised surface without borders.
  </text>

  <g id="float-in-card">
    <rect x="340" y="210" width="600" height="310" rx="44" ry="44" fill="url(#cardFill)" filter="url(#shadowDarkBR)"/>
    <rect x="340" y="210" width="600" height="310" rx="44" ry="44" fill="url(#cardFill)" filter="url(#shadowLightTL)"/>

    <rect x="390" y="252" width="154" height="42" rx="21" ry="21" fill="#F8FFFC" filter="url(#microShadow)"/>
    <circle cx="414" cy="273" r="7" fill="#19A082"/>
    <text x="432" y="279" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#158169">
      RAISED
    </text>

    <path d="M728 270 C756 244, 806 244, 834 270 C862 296, 862 344, 834 370 C806 396, 756 396, 728 370 C700 344, 700 296, 728 270 Z"
          fill="#E9F8F3" filter="url(#microShadow)"/>
    <path d="M752 319 L776 343 L815 295" fill="none" stroke="#19A082" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/>

    <text x="390" y="356" width="335" font-family="Segoe UI, Microsoft YaHei" font-size="35" font-weight="800" fill="#173F37">
      Premium depth
    </text>
    <text x="390" y="395" width="355" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#5E7F77">
      A clean executive card built from two soft opposing shadows.
    </text>

    <g transform="translate(390 438)">
      <circle cx="24" cy="24" r="24" fill="#F5FFFB" filter="url(#microShadow)"/>
      <path d="M15 25 L23 33 L36 16" fill="none" stroke="#19A082" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
      <text x="64" y="18" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#7A9991">
        BLUR
      </text>
      <text x="64" y="43" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="800" fill="#173F37">
        24pt
      </text>
    </g>

    <g transform="translate(560 438)">
      <circle cx="24" cy="24" r="24" fill="#F5FFFB" filter="url(#microShadow)"/>
      <path d="M16 31 C20 18, 29 15, 38 19" fill="none" stroke="#19A082" stroke-width="5" stroke-linecap="round"/>
      <text x="64" y="18" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#7A9991">
        DISTANCE
      </text>
      <text x="64" y="43" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="800" fill="#173F37">
        11pt
      </text>
    </g>

    <g transform="translate(740 438)">
      <circle cx="24" cy="24" r="24" fill="#F5FFFB" filter="url(#microShadow)"/>
      <path d="M15 33 L33 15 M33 15 L33 29 M33 15 L19 15" fill="none" stroke="#19A082" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
      <text x="64" y="18" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#7A9991">
        LIGHT
      </text>
      <text x="64" y="43" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="800" fill="#173F37">
        225°
      </text>
    </g>
  </g>

  <text x="850" y="650" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#D9FFF4" opacity="0.78" text-anchor="end">
    Apply PowerPoint “Float In” to the grouped card for motion.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<animate>` or `<animateTransform>` for the “Float In” behavior; keep the card as a group and apply the animation in PowerPoint after translation.
- ❌ Do not use a hard stroke outline around the card; it destroys the soft embossed illusion.
- ❌ Do not use only one shadow; neumorphism depends on the paired dark bottom-right and light top-left shadows.
- ❌ Do not apply `filter` to `<line>` elements; use paths or shapes if a shadowed decorative mark is needed.
- ❌ Do not use `clip-path` on rectangles or paths for this effect; clipping is only reliable on `<image>` elements.

## Composition notes
- Keep the main card large but isolated, occupying roughly 45–60% of the slide width with generous negative space so the blurred shadows have room to breathe.
- Use a mid-tone background; if the background is too white, the top-left highlight disappears, and if it is too dark, the soft UI effect becomes heavy.
- Place the brightest shadow toward the light source, usually top-left, and the darkest shadow toward bottom-right for a natural raised surface.
- For animation decks, group the duplicated card rectangles and all card contents, then apply one PowerPoint “Float In” or “Fade + Up” animation to the group so the shadows travel with the surface.