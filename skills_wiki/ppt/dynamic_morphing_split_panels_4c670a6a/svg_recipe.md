# SVG Recipe — Dynamic Morphing Split-Panels

## Visual mechanism
Three edge-to-edge vertical panels behave like elastic spatial zones: in the overview slide they are equal width, and in the focus slide one panel expands while the others compress. The same SVG object stack is reused across slides so PowerPoint Morph animates panel widths, product mockups, titles, and detail copy into a fluid hierarchy shift.

## SVG primitives needed
- 3× `<rect>` for the full-height vertical background panels
- 3× `<g>` panel content groups, each containing title text, compact labels, and product mockup geometry
- 9× `<rect>` for phone bodies, screens, camera pills, and UI cards
- 6× `<path>` for premium decorative wave overlays and app interface accents
- 1× `<image>` for a clipped product screenshot/photo in the expanded focus panel
- 1× `<clipPath>` with rounded `<rect>` applied only to the screenshot `<image>`
- 3× `<linearGradient>` for phone screens and expanded-panel lighting
- 1× `<radialGradient>` for a soft spotlight behind the focused mockup
- 2× `<filter>` definitions: one shadow for cards/devices, one blur glow for the focus halo
- Multiple `<text>` elements with explicit `width` attributes for master title, panel headings, captions, and focus-state detail text

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="midPanelWash" x1="300" y1="0" x2="1030" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#A8B0C0"/>
      <stop offset="0.55" stop-color="#79849A"/>
      <stop offset="1" stop-color="#465269"/>
    </linearGradient>
    <linearGradient id="screenBlue" x1="0" y1="165" x2="0" y2="520" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#52D7FF"/>
      <stop offset="1" stop-color="#5F4BFF"/>
    </linearGradient>
    <linearGradient id="screenGreen" x1="0" y1="150" x2="0" y2="560" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#8DFFB3"/>
      <stop offset="1" stop-color="#006D67"/>
    </linearGradient>
    <linearGradient id="screenAmber" x1="0" y1="160" x2="0" y2="520" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFE18A"/>
      <stop offset="1" stop-color="#FF6A5E"/>
    </linearGradient>
    <radialGradient id="focusGlow" cx="50%" cy="50%" r="55%">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.38"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>
    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="170%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="blurGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="24"/>
    </filter>
    <clipPath id="screenshotClip">
      <rect x="560" y="210" width="260" height="230" rx="26"/>
    </clipPath>
  </defs>

  <!-- Focus-state geometry: left compressed, center expanded, right compressed. For overview, change widths to 426/427/427 while preserving object order. -->
  <rect x="0" y="0" width="250" height="720" fill="#29303F"/>
  <rect x="250" y="0" width="780" height="720" fill="url(#midPanelWash)"/>
  <rect x="1030" y="0" width="250" height="720" fill="#C6CBD4"/>

  <path d="M250,0 C390,110 418,248 340,388 C300,460 300,610 390,720 L250,720 Z" fill="#FFFFFF" opacity="0.08"/>
  <path d="M1030,0 C918,96 898,242 960,360 C1018,470 1000,604 920,720 L1030,720 Z" fill="#1E2635" opacity="0.10"/>
  <ellipse cx="640" cy="365" rx="255" ry="255" fill="url(#focusGlow)" filter="url(#blurGlow)"/>

  <text x="56" y="62" width="1168" font-family="Segoe UI, Microsoft YaHei" font-size="46" font-weight="800" letter-spacing="2" fill="#FFFFFF">
    CHOOSING THE BEST
  </text>
  <text x="56" y="102" width="350" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#DDE5F2" opacity="0.75">
    Morph-ready split panels: overview → focused comparison
  </text>

  <!-- Left compressed option -->
  <g id="panelA">
    <text x="42" y="188" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="700" fill="#FFFFFF">BASIC</text>
    <text x="42" y="218" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#9FA8BA">fast start</text>
    <g transform="translate(66 285) scale(0.52)" filter="url(#softShadow)">
      <rect x="0" y="0" width="220" height="390" rx="34" fill="#DADDE4"/>
      <rect x="22" y="28" width="176" height="334" rx="24" fill="url(#screenBlue)"/>
      <ellipse cx="110" cy="48" rx="15" ry="8" fill="#1F2430"/>
      <rect x="47" y="92" width="126" height="16" rx="8" fill="#FFFFFF" opacity="0.82"/>
      <rect x="47" y="130" width="92" height="10" rx="5" fill="#FFFFFF" opacity="0.45"/>
      <path d="M50,258 C82,220 116,302 170,238 L170,326 L50,326 Z" fill="#FFFFFF" opacity="0.22"/>
    </g>
    <text x="42" y="650" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">$19 / mo</text>
  </g>

  <!-- Center focused option -->
  <g id="panelB">
    <text x="330" y="166" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="54" font-weight="800" fill="#FFFFFF">PRO</text>
    <text x="333" y="214" width="450" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" fill="#F0F4FF" opacity="0.86">recommended for scaling teams</text>
    <g transform="translate(365 245)" filter="url(#softShadow)">
      <rect x="0" y="0" width="245" height="405" rx="38" fill="#2B3039"/>
      <rect x="24" y="30" width="197" height="345" rx="27" fill="url(#screenGreen)"/>
      <ellipse cx="122" cy="50" rx="16" ry="8" fill="#15181E"/>
      <rect x="55" y="92" width="136" height="18" rx="9" fill="#FFFFFF" opacity="0.88"/>
      <rect x="55" y="135" width="88" height="10" rx="5" fill="#FFFFFF" opacity="0.45"/>
      <rect x="55" y="164" width="132" height="72" rx="18" fill="#FFFFFF" opacity="0.18"/>
      <path d="M56,312 C92,260 126,350 188,282 L188,345 L56,345 Z" fill="#FFFFFF" opacity="0.24"/>
    </g>
    <image x="560" y="210" width="260" height="230" clip-path="url(#screenshotClip)"
           href="https://images.example.com/product-dashboard-screenshot-with-charts.jpg"/>
    <rect x="560" y="210" width="260" height="230" rx="26" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.55"/>
    <text x="560" y="485" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#FFFFFF">Why it wins</text>
    <text x="560" y="525" width="385" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#FFFFFF" opacity="0.92">
      Advanced automations, live analytics, priority support, and flexible seats without enterprise overhead.
    </text>
    <text x="560" y="625" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="800" fill="#FFFFFF">$49 / mo</text>
  </g>

  <!-- Right compressed option -->
  <g id="panelC">
    <text x="1072" y="188" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="700" fill="#29303F">ELITE</text>
    <text x="1072" y="218" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#647086">enterprise</text>
    <g transform="translate(1102 285) scale(0.52)" filter="url(#softShadow)">
      <rect x="0" y="0" width="220" height="390" rx="34" fill="#F8F9FC"/>
      <rect x="22" y="28" width="176" height="334" rx="24" fill="url(#screenAmber)"/>
      <ellipse cx="110" cy="48" rx="15" ry="8" fill="#252B36"/>
      <rect x="47" y="92" width="126" height="16" rx="8" fill="#FFFFFF" opacity="0.82"/>
      <rect x="47" y="130" width="92" height="10" rx="5" fill="#FFFFFF" opacity="0.5"/>
      <path d="M48,265 C82,205 116,318 172,245 L172,326 L48,326 Z" fill="#FFFFFF" opacity="0.24"/>
    </g>
    <text x="1072" y="650" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="800" fill="#29303F">Custom</text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ SVG animation tags such as `<animate>` or `<animateTransform>`; create two static slides and let PowerPoint Morph do the motion.
- ❌ Rebuilding the second slide with a different object order; Morph works best when every panel, text box, image, and mockup appears in the same sequence on both slides.
- ❌ Using clipping on text or shape groups; only clip `<image>` elements, such as the focused screenshot crop.
- ❌ Hiding detail content by deleting it between slides; keep it present and change fill color/opacity so it can fade in during Morph.
- ❌ Putting shadows on `<line>` elements or relying on marker arrowheads; this layout should use rectangles, paths, images, and text only.

## Composition notes
- Build two slides from the same SVG template: overview uses three equal columns, while the focus slide expands the selected panel to roughly 55–60% of the width.
- Keep compressed panels legible but sparse: title, small subtitle, product silhouette, and price are enough.
- Place detail copy and screenshots only inside the expanded panel; on the overview slide, keep those objects in the same positions but make them invisible by matching the panel background or using very low opacity.
- Use one strong dark-to-light color rhythm across the panels so the expanding panel feels like the narrative spotlight rather than a disconnected new slide.