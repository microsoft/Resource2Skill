# SVG Recipe — Seamless Multi-State Interactive Product Showcase

## Visual mechanism
A stable, minimalist product-configurator slide where static typography and controls remain locked in place while only the hero product color/image and the active swatch state change between slides. Duplicate the same SVG layout for each variant, change the product asset/color and active swatch shadow/offset, then use PowerPoint hyperlinks plus Fade transitions for an app-like multi-state experience.

## SVG primitives needed
- 2× `<rect>` for the off-white background and subtle UI information pill
- 1× diagonal `<path>` for an energetic “interactive / must match” corner ribbon accent
- 8× `<text>` for eyebrow label, title, body copy, active variant label, swatch labels, and ribbon text
- 6× `<circle>` for color swatches and active-state halo
- 4× `<ellipse>` for soft product floor shadows and earbud speaker details
- 10× `<path>` for editable stylized earbuds, stems, highlights, and product contours
- 4× `<linearGradient>` for background depth, product body shading, metallic caps, and ribbon color
- 1× `<radialGradient>` for active swatch glow
- 2× `<filter>` using `feGaussianBlur` / `feOffset+feGaussianBlur+feMerge` for soft floor shadows and active control shadow
- Optional in production: 1× `<image>` per state for a transparent PNG product render, replacing the editable SVG earbud illustration while keeping the same position and size

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7F7F5"/>
      <stop offset="100%" stop-color="#ECEDEB"/>
    </linearGradient>

    <linearGradient id="ribbonGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#D8FF22"/>
      <stop offset="100%" stop-color="#BDF000"/>
    </linearGradient>

    <linearGradient id="roseBody" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FF8A9B"/>
      <stop offset="42%" stop-color="#D9405C"/>
      <stop offset="100%" stop-color="#8F1E34"/>
    </linearGradient>

    <linearGradient id="roseDark" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#B5253F"/>
      <stop offset="100%" stop-color="#47101B"/>
    </linearGradient>

    <linearGradient id="metalCap" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#F1F1F1"/>
      <stop offset="45%" stop-color="#777777"/>
      <stop offset="100%" stop-color="#2A2A2A"/>
    </linearGradient>

    <radialGradient id="activeGlow" cx="50%" cy="45%" r="60%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.95"/>
      <stop offset="65%" stop-color="#D9405C" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#D9405C" stop-opacity="0"/>
    </radialGradient>

    <filter id="floorBlur" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="12"/>
    </filter>

    <filter id="swatchShadow" x="-80%" y="-80%" width="260%" height="260%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="8"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <path d="M0 0 L310 0 L0 310 Z" fill="url(#ribbonGrad)"/>
  <text x="48" y="166" width="260" transform="rotate(-45 48 166)"
        font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="900"
        letter-spacing="1" fill="#050505">TAP TO SWITCH</text>

  <text x="92" y="118" width="440" font-family="Segoe UI, Microsoft YaHei"
        font-size="17" font-weight="700" letter-spacing="4" fill="#D24635">
    PRODUCT CONFIGURATOR
  </text>

  <text x="88" y="198" width="500" font-family="Segoe UI, Microsoft YaHei"
        font-size="62" font-weight="900" letter-spacing="-2" fill="#111111">
    EarPods
  </text>

  <text x="92" y="252" width="520" font-family="Segoe UI, Microsoft YaHei"
        font-size="25" font-weight="700" fill="#292929">
    Immersive sound in every colour.
  </text>

  <text x="92" y="300" width="470" font-family="Segoe UI, Microsoft YaHei"
        font-size="17" font-weight="400" fill="#666666">
    Duplicate this exact slide for each product state. Keep every element fixed, then swap only the product colour and the active swatch.
  </text>

  <rect x="92" y="382" width="318" height="52" rx="26" fill="#FFFFFF" opacity="0.82"/>
  <text x="118" y="415" width="260" font-family="Segoe UI, Microsoft YaHei"
        font-size="16" font-weight="700" fill="#333333">
    Active variant: <tspan fill="#D9405C">Rosy Red</tspan>
  </text>

  <circle cx="120" cy="500" r="20" fill="#F1F1F1" stroke="#D6D6D6" stroke-width="2"/>
  <circle cx="186" cy="500" r="20" fill="#1E1E1E" stroke="#000000" stroke-width="2"/>
  <circle cx="252" cy="500" r="20" fill="#3CB371" stroke="#2C8A58" stroke-width="2"/>
  <circle cx="318" cy="493" r="34" fill="url(#activeGlow)" filter="url(#swatchShadow)"/>
  <circle cx="318" cy="493" r="22" fill="#DC143C" stroke="#FFFFFF" stroke-width="5"/>

  <text x="90" y="552" width="88" font-family="Segoe UI, Microsoft YaHei"
        font-size="12" font-weight="600" fill="#777777">Heaven</text>
  <text x="160" y="552" width="80" font-family="Segoe UI, Microsoft YaHei"
        font-size="12" font-weight="600" fill="#777777">Black</text>
  <text x="226" y="552" width="90" font-family="Segoe UI, Microsoft YaHei"
        font-size="12" font-weight="600" fill="#777777">Mint</text>
  <text x="292" y="552" width="100" font-family="Segoe UI, Microsoft YaHei"
        font-size="12" font-weight="800" fill="#D9405C">Rosy</text>

  <ellipse cx="908" cy="604" rx="210" ry="24" fill="#111111" opacity="0.18" filter="url(#floorBlur)"/>
  <ellipse cx="752" cy="604" rx="86" ry="15" fill="#111111" opacity="0.10" filter="url(#floorBlur)"/>

  <g transform="translate(760 128) rotate(-10 120 210)">
    <path d="M145 214 C174 202 202 218 206 250 L222 440 C225 475 204 493 178 486
             C160 481 153 464 156 437 L174 282 C177 258 164 244 140 251 Z"
          fill="url(#roseBody)"/>
    <path d="M179 272 C194 283 198 304 200 334 L209 436 C211 458 201 472 184 475
             C196 455 195 398 188 336 C185 306 184 287 179 272 Z"
          fill="#FFFFFF" opacity="0.28"/>
    <path d="M156 438 C176 448 197 448 218 438 L220 457 C203 471 176 470 157 457 Z"
          fill="url(#metalCap)"/>

    <path d="M70 100 C122 67 202 84 229 136 C252 181 224 230 166 241
             C111 252 50 229 37 184 C26 146 39 119 70 100 Z"
          fill="url(#roseBody)"/>
    <path d="M183 97 C219 112 235 140 231 172 C210 148 185 136 146 133
             C117 131 95 119 88 101 C114 88 151 86 183 97 Z"
          fill="#FFFFFF" opacity="0.20"/>
    <ellipse cx="66" cy="156" rx="18" ry="28" transform="rotate(9 66 156)" fill="url(#roseDark)"/>
    <ellipse cx="68" cy="155" rx="7" ry="13" transform="rotate(9 68 155)" fill="#0C0C0C"/>
    <circle cx="130" cy="112" r="6" fill="#181818"/>
    <circle cx="154" cy="105" r="4" fill="#181818"/>
  </g>

  <g transform="translate(650 162) rotate(-14 120 210) scale(0.86)">
    <path d="M145 214 C174 202 202 218 206 250 L222 440 C225 475 204 493 178 486
             C160 481 153 464 156 437 L174 282 C177 258 164 244 140 251 Z"
          fill="url(#roseBody)" opacity="0.95"/>
    <path d="M156 438 C176 448 197 448 218 438 L220 457 C203 471 176 470 157 457 Z"
          fill="url(#metalCap)"/>
    <path d="M70 100 C122 67 202 84 229 136 C252 181 224 230 166 241
             C111 252 50 229 37 184 C26 146 39 119 70 100 Z"
          fill="url(#roseBody)" opacity="0.95"/>
    <ellipse cx="66" cy="156" rx="18" ry="28" transform="rotate(9 66 156)" fill="url(#roseDark)"/>
    <circle cx="130" cy="112" r="6" fill="#181818"/>
  </g>

  <text x="792" y="103" width="290" font-family="Segoe UI, Microsoft YaHei"
        font-size="15" font-weight="800" letter-spacing="3" fill="#777777">
    STATE 04 / 04
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not animate the swatches or product inside SVG; use duplicated PowerPoint slides with Fade transitions for stable state changes.
- ❌ Do not use SVG `<animate>`, `<animateTransform>`, `<foreignObject>`, `<use>`, or masks for interactivity; they will not translate reliably.
- ❌ Do not place `filter` on `<line>` elements; use shadows on circles, paths, ellipses, or text instead.
- ❌ Do not let swatch positions drift between states. Only the active swatch should move slightly upward and receive the shadow/glow.
- ❌ Do not rebuild the whole composition for each variant; the seamless illusion depends on identical geometry across slides.

## Composition notes
- Keep the layout split roughly 45/55: copy and swatches on the left, large floating product render on the right.
- The product should dominate the right half with generous negative space and one soft blurred floor shadow to make it feel premium.
- Use one accent color per state: product fill, active swatch, and one small text accent should all match.
- For the final deck, create one slide per color variant, assign each swatch a hyperlink to its matching slide, and apply the same medium Fade transition to every state slide.