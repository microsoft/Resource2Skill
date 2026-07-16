# SVG Recipe — Sweet Isometric 3D Data Blocks

## Visual mechanism
Build “3D” data out of editable SVG paths: each block is three rhombus/quadrilateral faces with candy gradients, stacked in an isometric camera angle. A blurred, elongated purple shadow and a faint isometric platform make the blocks feel like floating executive-keynote data objects rather than flat chart bars.

## SVG primitives needed
- 1× `<rect>` for the clean slide background
- 4× `<rect>` for rounded label pills behind callout text
- 14× `<path>` for the soft shadow, platform, and three editable faces per isometric data block
- 8× `<line>` for platform guide lines and callout connectors
- 8× `<circle>` for decorative background bubbles and connector anchor dots
- 11× `<text>` for title, subtitle, top-face percentages, and callout labels; every text element includes explicit `width`
- 15× `<linearGradient>` for background, shadow fade, platform sheen, and candy-colored block faces
- 1× `<filter id="softShadow">` using blur/offset/merge for the long floating shadow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F7F4FF"/>
    </linearGradient>
    <linearGradient id="shadowFade" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#6F44FF" stop-opacity="0.28"/>
      <stop offset="70%" stop-color="#6F44FF" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#6F44FF" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="platformGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.92"/>
      <stop offset="100%" stop-color="#EDE7FF" stop-opacity="0.35"/>
    </linearGradient>

    <linearGradient id="purpleTop" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#8C63FF"/><stop offset="100%" stop-color="#5B2BFF"/></linearGradient>
    <linearGradient id="purpleL" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#7047F4"/><stop offset="100%" stop-color="#3F1AB8"/></linearGradient>
    <linearGradient id="purpleR" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#5930D8"/><stop offset="100%" stop-color="#2D127E"/></linearGradient>

    <linearGradient id="orangeTop" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#FF9B61"/><stop offset="100%" stop-color="#FD7535"/></linearGradient>
    <linearGradient id="orangeL" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#F06B34"/><stop offset="100%" stop-color="#B93B15"/></linearGradient>
    <linearGradient id="orangeR" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#D64E22"/><stop offset="100%" stop-color="#8C270D"/></linearGradient>

    <linearGradient id="yellowTop" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#FFE078"/><stop offset="100%" stop-color="#FFC107"/></linearGradient>
    <linearGradient id="yellowL" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#F2B91D"/><stop offset="100%" stop-color="#BF7E00"/></linearGradient>
    <linearGradient id="yellowR" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#D99A00"/><stop offset="100%" stop-color="#8A5B00"/></linearGradient>

    <linearGradient id="cyanTop" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#6FF2FF"/><stop offset="100%" stop-color="#22C7E8"/></linearGradient>
    <linearGradient id="cyanL" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#1EBAD6"/><stop offset="100%" stop-color="#08768F"/></linearGradient>
    <linearGradient id="cyanR" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#1597BC"/><stop offset="100%" stop-color="#05546F"/></linearGradient>

    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="180%">
      <feOffset dx="24" dy="34"/>
      <feGaussianBlur stdDeviation="22"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>
  <circle cx="1110" cy="102" r="72" fill="#6F44FF" opacity="0.08"/>
  <circle cx="1010" cy="618" r="44" fill="#FD7535" opacity="0.10"/>
  <circle cx="190" cy="585" r="58" fill="#22C7E8" opacity="0.10"/>
  <circle cx="78" cy="128" r="26" fill="#FFC107" opacity="0.16"/>

  <text x="82" y="86" width="700" font-family="Segoe UI, Microsoft YaHei" font-size="46" font-weight="800" fill="#28233A">
    Sweet Isometric <tspan fill="#6F44FF">Data Blocks</tspan>
  </text>
  <text x="86" y="126" width="550" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#77718A">
    Candy-colored 3D blocks turn summary metrics into tangible, memorable data objects.
  </text>

  <path d="M352 510 L674 338 L982 493 L660 664 Z" fill="url(#shadowFade)" filter="url(#softShadow)"/>
  <path d="M352 488 L672 322 L958 464 L638 630 Z" fill="url(#platformGrad)" stroke="#E7DFFF" stroke-width="1.5"/>
  <line x1="430" y1="449" x2="716" y2="591" stroke="#D9CDFD" stroke-width="1" stroke-dasharray="6 8"/>
  <line x1="512" y1="407" x2="798" y2="549" stroke="#D9CDFD" stroke-width="1" stroke-dasharray="6 8"/>
  <line x1="594" y1="365" x2="880" y2="507" stroke="#D9CDFD" stroke-width="1" stroke-dasharray="6 8"/>
  <line x1="478" y1="552" x2="798" y2="386" stroke="#D9CDFD" stroke-width="1" stroke-dasharray="6 8"/>

  <!-- orange block, 52% -->
  <path d="M399 323 L475 361 L475 505 L399 467 Z" fill="url(#orangeL)"/>
  <path d="M551 323 L475 361 L475 505 L551 467 Z" fill="url(#orangeR)"/>
  <path d="M475 285 L551 323 L475 361 L399 323 Z" fill="url(#orangeTop)" stroke="#FFB18A" stroke-width="1.2"/>
  <text x="441" y="328" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#FFFFFF" transform="rotate(26 475 326)">52%</text>

  <!-- yellow block, 39% -->
  <path d="M759 354 L835 392 L835 500 L759 462 Z" fill="url(#yellowL)"/>
  <path d="M911 354 L835 392 L835 500 L911 462 Z" fill="url(#yellowR)"/>
  <path d="M835 316 L911 354 L835 392 L759 354 Z" fill="url(#yellowTop)" stroke="#FFE59A" stroke-width="1.2"/>
  <text x="802" y="359" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#563A00" transform="rotate(26 835 357)">39%</text>

  <!-- cyan block, 24% -->
  <path d="M548 388 L624 426 L624 506 L548 468 Z" fill="url(#cyanL)"/>
  <path d="M700 388 L624 426 L624 506 L700 468 Z" fill="url(#cyanR)"/>
  <path d="M624 350 L700 388 L624 426 L548 388 Z" fill="url(#cyanTop)" stroke="#A3F8FF" stroke-width="1.2"/>
  <text x="590" y="393" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#FFFFFF" transform="rotate(26 624 391)">24%</text>

  <!-- hero purple block, 68% -->
  <path d="M534 243 L610 281 L610 507 L534 469 Z" fill="url(#purpleL)"/>
  <path d="M686 243 L610 281 L610 507 L686 469 Z" fill="url(#purpleR)"/>
  <path d="M610 205 L686 243 L610 281 L534 243 Z" fill="url(#purpleTop)" stroke="#A48BFF" stroke-width="1.4"/>
  <text x="576" y="249" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="800" fill="#FFFFFF" transform="rotate(26 610 247)">68%</text>

  <line x1="535" y1="244" x2="332" y2="242" stroke="#A69BBE" stroke-width="1.4"/>
  <circle cx="535" cy="244" r="5" fill="#FFFFFF" stroke="#6F44FF" stroke-width="3"/>
  <rect x="116" y="208" width="210" height="64" rx="18" fill="#FFFFFF" stroke="#E9E3F8"/>
  <text x="136" y="233" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#28233A">
    <tspan font-size="22" font-weight="800" fill="#6F44FF">68%</tspan><tspan x="136" dy="21">Core growth engine</tspan>
  </text>

  <line x1="552" y1="323" x2="300" y2="360" stroke="#A69BBE" stroke-width="1.4"/>
  <circle cx="552" cy="323" r="5" fill="#FFFFFF" stroke="#FD7535" stroke-width="3"/>
  <rect x="94" y="328" width="198" height="62" rx="18" fill="#FFFFFF" stroke="#E9E3F8"/>
  <text x="114" y="353" width="158" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#28233A">
    <tspan font-size="21" font-weight="800" fill="#FD7535">52%</tspan><tspan x="114" dy="20">Adoption layer</tspan>
  </text>

  <line x1="910" y1="354" x2="1018" y2="310" stroke="#A69BBE" stroke-width="1.4"/>
  <circle cx="910" cy="354" r="5" fill="#FFFFFF" stroke="#FFC107" stroke-width="3"/>
  <rect x="1028" y="274" width="178" height="62" rx="18" fill="#FFFFFF" stroke="#E9E3F8"/>
  <text x="1048" y="299" width="138" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#28233A">
    <tspan font-size="21" font-weight="800" fill="#E0A000">39%</tspan><tspan x="1048" dy="20">Upside pool</tspan>
  </text>

  <line x1="700" y1="388" x2="989" y2="438" stroke="#A69BBE" stroke-width="1.4"/>
  <circle cx="700" cy="388" r="5" fill="#FFFFFF" stroke="#22C7E8" stroke-width="3"/>
  <rect x="1000" y="406" width="180" height="62" rx="18" fill="#FFFFFF" stroke="#E9E3F8"/>
  <text x="1020" y="431" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#28233A">
    <tspan font-size="21" font-weight="800" fill="#11AFCF">24%</tspan><tspan x="1020" dy="20">Emerging signal</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Relying on real PowerPoint 3D extrusion from SVG; instead, draw separate editable top/side faces as paths.
- ❌ Using `<use>` to duplicate block faces; repeat the path geometry explicitly so PPT-Master keeps each face editable.
- ❌ Applying `filter` to connector `<line>` elements; keep shadows on block/platform paths only.
- ❌ Using `marker-end` arrowheads on connectors; use plain lines plus small circles for reliable editable callouts.
- ❌ Using skew or matrix transforms to fake isometric projection; hard-code the rhombus coordinates or use simple rotate transforms on text only.

## Composition notes
- Keep the isometric data object in the central 50–60% of the slide; labels can sit in the left and right margins.
- Draw shadow first, then platform, then blocks from rear to front so overlaps feel physically correct.
- Use bright top faces and darker side faces: the candy palette should feel playful, but the side gradients provide premium depth.
- Preserve generous white space around the blocks; the floating shadow and platform need room to breathe.