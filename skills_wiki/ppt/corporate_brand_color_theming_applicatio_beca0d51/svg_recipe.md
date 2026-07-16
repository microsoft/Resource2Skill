# SVG Recipe — Branded Color Palette Application

## Visual mechanism
Apply a strict 4-color brand palette everywhere: dark color for authority text and contrast panels, medium/light colors for data graphics and accents, and grey for secondary UI/rules. The slide becomes a branded keynote thumbnail by combining a vivid palette environment, a mock PowerPoint workspace, color-wheel evidence, swatches, and oversized high-contrast headline typography.

## SVG primitives needed
- 8× <rect> for background, laptop body/screen, ribbon bars, headline blocks, palette swatches, and UI panels
- 18× <path> for purple burst rays, color-wheel wedges, PowerPoint icon geometry, and annotation accents
- 6× <circle> for color wheels, icon badge, KPI dots, and decorative palette marks
- 7× <line> for slide UI dividers, axis/grid lines, and connector accents
- 16× <text> for title banner, labels, ribbon text, swatch labels, and dashboard copy
- 2× <linearGradient> for branded background and PowerPoint icon depth
- 1× <radialGradient> for glow behind the hero mockup
- 2× <filter> for soft shadow and color glow on major elements

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgPurple" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#9B4DFF"/>
      <stop offset="0.45" stop-color="#5A1FD6"/>
      <stop offset="1" stop-color="#12002E"/>
    </linearGradient>
    <radialGradient id="heroGlow" cx="45%" cy="28%" r="64%">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.45"/>
      <stop offset="0.45" stop-color="#8A5CFF" stop-opacity="0.18"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="pptGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#FF8A00"/>
      <stop offset="0.55" stop-color="#F04B16"/>
      <stop offset="1" stop-color="#B82412"/>
    </linearGradient>
    <linearGradient id="screenWhite" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FFFFFF"/>
      <stop offset="1" stop-color="#ECECF2"/>
    </linearGradient>
    <filter id="shadow">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="12"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="glow">
      <feGaussianBlur stdDeviation="7"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgPurple)"/>
  <circle cx="510" cy="245" r="430" fill="url(#heroGlow)"/>
  <path d="M0 0 L150 0 L610 720 L0 720 Z" fill="#FFFFFF" opacity="0.12"/>
  <path d="M210 0 L300 0 L760 720 L660 720 Z" fill="#FFFFFF" opacity="0.14"/>
  <path d="M455 0 L520 0 L930 720 L850 720 Z" fill="#FFFFFF" opacity="0.12"/>
  <path d="M710 0 L780 0 L1040 720 L940 720 Z" fill="#FFFFFF" opacity="0.10"/>
  <path d="M980 0 L1280 0 L1280 720 L1130 720 Z" fill="#000000" opacity="0.16"/>
  <rect x="0" y="552" width="1280" height="168" fill="#000000" opacity="0.55"/>

  <rect x="58" y="42" width="838" height="525" rx="28" fill="#1A0E12" filter="url(#shadow)"/>
  <rect x="76" y="58" width="802" height="476" rx="12" fill="url(#screenWhite)"/>
  <rect x="76" y="58" width="802" height="38" rx="10" fill="#E72710"/>
  <rect x="428" y="58" width="98" height="16" rx="4" fill="#15151D"/>
  <text x="104" y="81" width="110" font-family="Segoe UI" font-size="10" font-weight="700" fill="#FFFFFF">AutoSave</text>
  <text x="90" y="116" width="520" font-family="Segoe UI" font-size="10" fill="#333333">File      Home      Insert      Draw      Design      Transitions      Animations      Slide Show      Review</text>
  <line x1="88" y1="130" x2="866" y2="130" stroke="#D6D5D7" stroke-width="1"/>
  <rect x="89" y="138" width="86" height="48" rx="4" fill="#FFFFFF" stroke="#D6D5D7"/>
  <rect x="190" y="138" width="150" height="48" rx="4" fill="#FFFFFF" stroke="#D6D5D7"/>
  <rect x="354" y="138" width="144" height="48" rx="4" fill="#FFFFFF" stroke="#D6D5D7"/>
  <text x="242" y="213" width="150" font-family="Segoe UI" font-size="9" font-weight="700" fill="#02094D">PRIMARY COLOURS</text>

  <circle cx="370" cy="352" r="132" fill="#F8F8FB" stroke="#D6D5D7"/>
  <path d="M370 352 L335 224 A132 132 0 0 1 370 220 Z" fill="#FFF200"/>
  <path d="M370 352 L370 220 A132 132 0 0 1 463 259 Z" fill="#BDE94A"/>
  <path d="M370 352 L463 259 A132 132 0 0 1 499 321 Z" fill="#26B86C"/>
  <path d="M370 352 L499 321 A132 132 0 0 1 496 386 Z" fill="#31C2D8"/>
  <path d="M370 352 L496 386 A132 132 0 0 1 441 462 Z" fill="#3E89FF"/>
  <path d="M370 352 L441 462 A132 132 0 0 1 350 482 Z" fill="#6D48B8"/>
  <path d="M370 352 L350 482 A132 132 0 0 1 272 440 Z" fill="#D43F7C"/>
  <path d="M370 352 L272 440 A132 132 0 0 1 241 321 Z" fill="#FF6E1A"/>
  <path d="M370 352 L241 321 A132 132 0 0 1 335 224 Z" fill="#FFC425"/>
  <text x="353" y="235" width="70" font-family="Segoe UI" font-size="10" font-weight="700" fill="#02094D">YELLOW</text>
  <text x="470" y="405" width="50" font-family="Segoe UI" font-size="10" font-weight="700" fill="#02094D">BLUE</text>
  <text x="273" y="407" width="50" font-family="Segoe UI" font-size="10" font-weight="700" fill="#02094D">RED</text>

  <circle cx="668" cy="354" r="132" fill="#FFFFFF" stroke="#D6D5D7"/>
  <path d="M668 354 L633 226 A132 132 0 0 1 740 244 Z" fill="#FFF200"/>
  <path d="M668 354 L740 244 A132 132 0 0 1 794 333 Z" fill="#FF8A00"/>
  <path d="M668 354 L794 333 A132 132 0 0 1 752 452 Z" fill="#E72710"/>
  <path d="M668 354 L752 452 A132 132 0 0 1 621 477 Z" fill="#02094D"/>
  <path d="M668 354 L621 477 A132 132 0 0 1 542 390 Z" fill="#008C78"/>
  <path d="M668 354 L542 390 A132 132 0 0 1 633 226 Z" fill="#49D600"/>
  <circle cx="668" cy="354" r="76" fill="#FFFFFF"/>
  <line x1="668" y1="275" x2="668" y2="433" stroke="#4B3A16" stroke-width="1.4"/>
  <line x1="590" y1="354" x2="746" y2="354" stroke="#4B3A16" stroke-width="1.4"/>
  <line x1="610" y1="298" x2="727" y2="411" stroke="#4B3A16" stroke-width="1.4"/>
  <line x1="727" y1="298" x2="610" y2="411" stroke="#4B3A16" stroke-width="1.4"/>
  <text x="646" y="250" width="80" font-family="Segoe UI" font-size="20" font-weight="800" fill="#241100">Yellow</text>
  <text x="556" y="303" width="70" font-family="Segoe UI" font-size="13" font-weight="700" fill="#FFFFFF">Green</text>
  <text x="553" y="413" width="70" font-family="Segoe UI" font-size="15" font-weight="800" fill="#FFFFFF">Blue</text>
  <text x="748" y="302" width="70" font-family="Segoe UI" font-size="13" font-weight="700" fill="#FFFFFF">Orange</text>
  <text x="755" y="407" width="60" font-family="Segoe UI" font-size="16" font-weight="800" fill="#FFFFFF">Red</text>

  <rect x="725" y="14" width="190" height="190" rx="36" fill="#FFFFFF" filter="url(#shadow)"/>
  <circle cx="824" cy="110" r="70" fill="url(#pptGrad)"/>
  <path d="M824 40 A70 70 0 0 1 894 110 L824 110 Z" fill="#FF9B3A" opacity="0.85"/>
  <path d="M824 110 L894 110 A70 70 0 0 1 824 180 Z" fill="#E84016" opacity="0.9"/>
  <rect x="742" y="72" width="82" height="78" rx="8" fill="#E94713" filter="url(#shadow)"/>
  <text x="763" y="129" width="60" font-family="Segoe UI" font-size="54" font-weight="900" fill="#FFFFFF">P</text>

  <rect x="948" y="62" width="294" height="398" rx="2" fill="#02094D" opacity="0.94" filter="url(#shadow)"/>
  <text x="982" y="111" width="230" font-family="Segoe UI" font-size="24" font-weight="800" fill="#FFFFFF">Brand palette</text>
  <text x="982" y="143" width="220" font-family="Segoe UI" font-size="13" fill="#D6D5D7">Logo-derived colors applied consistently</text>
  <rect x="982" y="176" width="226" height="46" rx="8" fill="#02094D" stroke="#FFFFFF" stroke-opacity="0.25"/>
  <rect x="982" y="236" width="226" height="46" rx="8" fill="#3E89FF"/>
  <rect x="982" y="296" width="226" height="46" rx="8" fill="#ADCDFF"/>
  <rect x="982" y="356" width="226" height="46" rx="8" fill="#D6D5D7"/>
  <text x="1000" y="206" width="170" font-family="Segoe UI" font-size="16" font-weight="800" fill="#FFFFFF">Dark / Headlines</text>
  <text x="1000" y="266" width="170" font-family="Segoe UI" font-size="16" font-weight="800" fill="#FFFFFF">Medium / Data</text>
  <text x="1000" y="326" width="170" font-family="Segoe UI" font-size="16" font-weight="800" fill="#02094D">Light / Support</text>
  <text x="1000" y="386" width="170" font-family="Segoe UI" font-size="16" font-weight="800" fill="#02094D">Grey / Rules</text>

  <rect x="38" y="429" width="722" height="119" fill="#FFF200" filter="url(#shadow)"/>
  <text x="60" y="528" width="670" font-family="Segoe UI" font-size="112" font-weight="900" fill="#000000">BRAND PPT</text>
  <rect x="38" y="548" width="654" height="120" fill="#000000"/>
  <text x="60" y="648" width="600" font-family="Segoe UI" font-size="92" font-weight="900" fill="#FFFFFF">LIKE A PRO</text>
</svg>
```

## Avoid in this skill
- ❌ Using default Office-like rainbow colors without a visible hierarchy; the point is disciplined palette ownership.
- ❌ Applying all brand colors equally; reserve the darkest color for text/authority, medium for active data, light for support, and grey for UI structure.
- ❌ Clipping or masking non-image shapes for the color wheels; use explicit editable <path> wedges instead.
- ❌ Overcrowding the composition with too many unrelated colors, gradients, or decorative icons that dilute the brand palette.

## Composition notes
- Keep the main brand statement oversized and high contrast, anchored in the bottom-left third for instant thumbnail readability.
- Use the laptop/workspace mockup as “proof of design process,” while the palette card on the right explains the applied system.
- Let the four brand colors repeat across text, swatches, chart-like graphics, and UI accents so the deck feels intentionally themed.
- Balance bright accent blocks with dark navy/black panels; the restrained palette should feel premium, not playful by accident.