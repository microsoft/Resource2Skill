# SVG Recipe — Window Pane Comparison

## Visual mechanism
A two-column comparison is framed as a large architectural window: each “pane” becomes a self-contained content bay with a title pane above and supporting points below. The shared window frame creates structure and symmetry, while glass gradients, photo texture, and highlights make the comparison feel dimensional rather than like a flat table.

## SVG primitives needed
- 1× `<rect>` full-slide background with gradient fill
- 1× clipped `<image>` for subtle scenery/texture behind the window glass
- 8–12× `<rect>` for window frame rails, pane surfaces, title cards, body cards, and small labels
- 4× `<line>` for crisp pane seams and highlight strokes
- 6× `<path>` for decorative blobs, check marks, and compact pane icons
- 4× `<circle>` for bullet dots, glow accents, and small hardware details
- 8× `<text>` blocks with explicit `width` attributes for headline, pane titles, subtitles, and bullets
- 2× `<linearGradient>` for slide background and glass pane fills
- 1× `<radialGradient>` for ambient glow
- 2× `<filter>` definitions: one soft drop shadow for the window, one blur glow for atmospheric accents
- 1× `<clipPath>` using a rounded `<rect>` applied only to the background `<image>`

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#071A2F"/>
      <stop offset="55%" stop-color="#12365A"/>
      <stop offset="100%" stop-color="#07111F"/>
    </linearGradient>

    <linearGradient id="frameGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#F7FBFF"/>
      <stop offset="48%" stop-color="#D9E7F5"/>
      <stop offset="100%" stop-color="#AFC5D9"/>
    </linearGradient>

    <linearGradient id="leftGlass" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#DDF7FF" stop-opacity="0.82"/>
      <stop offset="58%" stop-color="#8BD8F1" stop-opacity="0.48"/>
      <stop offset="100%" stop-color="#255B86" stop-opacity="0.44"/>
    </linearGradient>

    <linearGradient id="rightGlass" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFF2D7" stop-opacity="0.84"/>
      <stop offset="58%" stop-color="#FFB86B" stop-opacity="0.46"/>
      <stop offset="100%" stop-color="#713B75" stop-opacity="0.42"/>
    </linearGradient>

    <radialGradient id="ambientGlow" cx="50%" cy="45%" r="65%">
      <stop offset="0%" stop-color="#7DD3FC" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#7DD3FC" stop-opacity="0"/>
    </radialGradient>

    <filter id="windowShadow" x="-15%" y="-15%" width="130%" height="140%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="16"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="24"/>
    </filter>

    <clipPath id="windowImageClip">
      <rect x="116" y="128" width="1048" height="472" rx="34"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <circle cx="1002" cy="132" r="210" fill="url(#ambientGlow)" filter="url(#softGlow)" opacity="0.82"/>
  <path d="M-30,560 C130,470 210,650 380,575 C520,510 610,565 720,680 L-30,760 Z" fill="#2DD4BF" opacity="0.12" filter="url(#softGlow)"/>
  <path d="M1000,654 C1070,565 1195,590 1298,478 L1298,760 L930,760 C930,715 958,690 1000,654 Z" fill="#F59E0B" opacity="0.13" filter="url(#softGlow)"/>

  <text x="88" y="62" width="760" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="34" font-weight="700" fill="#FFFFFF">
    Two Ways to Open the Market
  </text>
  <text x="90" y="96" width="700" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#BFD8F1">
    A window-pane comparison keeps two alternatives parallel while giving each one its own focused story space.
  </text>

  <rect x="96" y="118" width="1088" height="500" rx="42" fill="#07111F" opacity="0.34" filter="url(#windowShadow)"/>

  <image href="https://images.example.com/premium-evening-city-through-glass-window.jpg"
         x="116" y="128" width="1048" height="472" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#windowImageClip)" opacity="0.42"/>

  <rect x="130" y="148" width="490" height="440" rx="24" fill="url(#leftGlass)"/>
  <rect x="660" y="148" width="490" height="440" rx="24" fill="url(#rightGlass)"/>

  <rect x="154" y="170" width="442" height="118" rx="20" fill="#FFFFFF" opacity="0.82"/>
  <rect x="684" y="170" width="442" height="118" rx="20" fill="#FFFFFF" opacity="0.82"/>
  <rect x="154" y="332" width="442" height="220" rx="22" fill="#08233D" opacity="0.62"/>
  <rect x="684" y="332" width="442" height="220" rx="22" fill="#241635" opacity="0.62"/>

  <path d="M202,218 C210,197 232,188 252,197 C272,206 278,229 266,247 C253,268 222,268 207,250 C199,241 197,229 202,218 Z" fill="#0EA5E9" opacity="0.95"/>
  <path d="M224,235 L238,221 L260,241" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M735,199 L786,199 C796,199 804,207 804,217 L804,250 C804,260 796,268 786,268 L735,268 C725,268 717,260 717,250 L717,217 C717,207 725,199 735,199 Z" fill="#F97316" opacity="0.96"/>
  <path d="M744,236 L758,248 L780,220" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>

  <text x="292" y="214" width="270" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#0F4C81" letter-spacing="1.5">
    OPTION A
  </text>
  <text x="292" y="247" width="285" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="30" font-weight="800" fill="#08233D">
    Focused Launch
  </text>
  <text x="824" y="214" width="270" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#9A3412" letter-spacing="1.5">
    OPTION B
  </text>
  <text x="824" y="247" width="285" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="30" font-weight="800" fill="#2B1734">
    Broad Platform
  </text>

  <circle cx="184" cy="381" r="6" fill="#67E8F9"/>
  <path d="M182,381 L188,387 L199,373" fill="none" stroke="#67E8F9" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="218" y="391" width="330" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#FFFFFF">
    Faster proof of demand
  </text>
  <text x="218" y="424" width="340" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#D8F6FF">
    Concentrates budget on one buyer segment and one clear product promise.
  </text>

  <circle cx="184" cy="482" r="6" fill="#67E8F9"/>
  <path d="M182,482 L188,488 L199,474" fill="none" stroke="#67E8F9" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="218" y="492" width="330" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#FFFFFF">
    Lower operating drag
  </text>
  <text x="218" y="525" width="340" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#D8F6FF">
    Smaller offer set reduces enablement, support, and launch complexity.
  </text>

  <circle cx="714" cy="381" r="6" fill="#FDBA74"/>
  <path d="M712,381 L718,387 L729,373" fill="none" stroke="#FDBA74" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="748" y="391" width="330" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#FFFFFF">
    Larger addressable surface
  </text>
  <text x="748" y="424" width="340" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#FFE7CA">
    Multiple use cases create more entry points for enterprise conversations.
  </text>

  <circle cx="714" cy="482" r="6" fill="#FDBA74"/>
  <path d="M712,482 L718,488 L729,474" fill="none" stroke="#FDBA74" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="748" y="492" width="330" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#FFFFFF">
    Stronger ecosystem story
  </text>
  <text x="748" y="525" width="340" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#FFE7CA">
    Partners can attach services, integrations, and long-term expansion paths.
  </text>

  <rect x="96" y="118" width="1088" height="500" rx="42" fill="none" stroke="url(#frameGrad)" stroke-width="24"/>
  <rect x="620" y="128" width="40" height="472" rx="12" fill="url(#frameGrad)"/>
  <rect x="116" y="300" width="1048" height="28" rx="12" fill="url(#frameGrad)"/>
  <line x1="134" y1="144" x2="1146" y2="144" stroke="#FFFFFF" stroke-width="2" opacity="0.65"/>
  <line x1="134" y1="587" x2="1146" y2="587" stroke="#6E8CA8" stroke-width="2" opacity="0.45"/>
  <line x1="640" y1="154" x2="640" y2="286" stroke="#FFFFFF" stroke-width="2" opacity="0.55"/>
  <line x1="640" y1="342" x2="640" y2="570" stroke="#6E8CA8" stroke-width="2" opacity="0.42"/>

  <circle cx="625" cy="314" r="7" fill="#FFFFFF" opacity="0.88"/>
  <circle cx="655" cy="314" r="7" fill="#FFFFFF" opacity="0.88"/>
  <path d="M162,158 C248,132 374,138 510,158" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.28" stroke-linecap="round"/>
  <path d="M690,158 C776,132 902,138 1038,158" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.24" stroke-linecap="round"/>
</svg>
```

## Avoid in this skill
- ❌ Do not build the window frame with a `<mask>` or masked cutout; masks on shapes are not reliable for translation. Use visible frame rails layered over the panes instead.
- ❌ Do not apply `clip-path` to groups or rectangles for the glass overlay; clipping is only safe here on the `<image>`.
- ❌ Do not use `<use>` to repeat bullets, check marks, or hardware dots; duplicate the native shapes directly.
- ❌ Do not rely on semi-transparent text boxes without explicit `width`; every text element must define its own width for stable PowerPoint rendering.
- ❌ Avoid overly thin pane dividers below 2 px; they can disappear after conversion or projection.

## Composition notes
- Keep the main window between roughly `x=96–1184` and `y=118–618`, leaving a clean title band above and breathing room below.
- Treat the center divider as the strongest organizing line; align pane titles, icons, and bullet groups symmetrically on either side.
- Use cool accents on the left and warm accents on the right so the viewer can compare quickly without reading every word.
- Place decorative glow and photo texture behind the panes only; the text cards should stay high-contrast and readable.