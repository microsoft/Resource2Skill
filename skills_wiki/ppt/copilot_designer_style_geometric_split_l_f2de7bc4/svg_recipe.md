# SVG Recipe — Copilot Designer-Style Geometric Split Layout

## Visual mechanism
A high-contrast split composition pairs a large masked hero image on one side with bold keynote typography and brand-like geometric marks on the other. Offset circles, glowing gradients, plus/star accents, and translucent diagonal bands make the layout feel like a Copilot Designer-generated executive slide rather than a simple photo-and-text grid.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark gradient background.
- 2× `<radialGradient>` and 3× `<linearGradient>` for atmospheric background glow, AI lettering, orange presentation logo, and hero-image accent color.
- 2× `<filter>` for soft glow and drop shadow on editable shapes/text.
- 1× `<clipPath>` with `<circle>` applied to the hero `<image>` for a clean circular crop.
- 1× `<image>` for the right-side hero/photo subject, clipped into the circle.
- 2× `<circle>` for the offset hero backing disc and presentation-logo disc.
- 7× `<path>` for translucent background ribbons, Copilot-style ribbon mark, sparkle accents, and letter-like geometry.
- 5× `<rect>` for the presentation app tile, inner shadow tile, and plus/accent geometry.
- 4× `<text>` elements with explicit `width` attributes for the main title, subtitle, and logo text.
- 2× `<line>` for small decorative accent strokes.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0" stop-color="#26102F"/>
      <stop offset="0.45" stop-color="#090B3D"/>
      <stop offset="1" stop-color="#111A78"/>
    </linearGradient>

    <radialGradient id="blueGlow" cx="74%" cy="17%" r="50%">
      <stop offset="0" stop-color="#4CA8FF" stop-opacity="0.75"/>
      <stop offset="0.48" stop-color="#263E91" stop-opacity="0.38"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="purpleGlow" cx="50%" cy="70%" r="55%">
      <stop offset="0" stop-color="#7860FF" stop-opacity="0.48"/>
      <stop offset="0.55" stop-color="#252063" stop-opacity="0.28"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="aiGrad" x1="80" y1="60" x2="470" y2="245">
      <stop offset="0" stop-color="#12D7F7"/>
      <stop offset="0.22" stop-color="#B9E82B"/>
      <stop offset="0.45" stop-color="#FF8A00"/>
      <stop offset="0.72" stop-color="#F51BB6"/>
      <stop offset="1" stop-color="#00D7FF"/>
    </linearGradient>

    <linearGradient id="orangeGrad" x1="108" y1="475" x2="292" y2="628">
      <stop offset="0" stop-color="#FF8D66"/>
      <stop offset="1" stop-color="#D83F1E"/>
    </linearGradient>

    <linearGradient id="heroAccent" x1="730" y1="60" x2="1180" y2="610">
      <stop offset="0" stop-color="#FFE1CC"/>
      <stop offset="0.5" stop-color="#6FB2D6"/>
      <stop offset="1" stop-color="#1C5A7E"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="8"/>
    </filter>

    <clipPath id="heroCircle">
      <circle cx="980" cy="335" r="282"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#blueGlow)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#purpleGlow)"/>

  <path d="M235 300 C430 270 595 284 760 350 C900 407 1046 423 1265 382 L1280 480 C1040 534 872 501 704 430 C560 370 415 348 235 365 Z"
        fill="#FFFFFF" opacity="0.06"/>
  <path d="M610 178 C765 216 855 271 940 350 C1035 438 1144 473 1280 465 L1280 720 L610 720 Z"
        fill="#FFFFFF" opacity="0.035"/>

  <circle cx="1018" cy="328" r="292" fill="url(#heroAccent)" opacity="0.65"/>
  <circle cx="940" cy="378" r="276" fill="#111A78" opacity="0.3"/>

  <image href="https://images.example.com/hero-presenter-right-side-cropped-with-non-identifiable-face-or-shoulder-profile.jpg"
         x="698" y="53" width="564" height="564" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#heroCircle)"/>

  <circle cx="980" cy="335" r="282" fill="none" stroke="#FFFFFF" stroke-opacity="0.18" stroke-width="2"/>
  <circle cx="1112" cy="145" r="18" fill="none" stroke="#8BE7FF" stroke-width="4" opacity="0.75"/>
  <circle cx="840" cy="595" r="10" fill="#6CF15F" opacity="0.8"/>
  <line x1="756" y1="162" x2="804" y2="162" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.45"/>
  <line x1="780" y1="138" x2="780" y2="186" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.45"/>

  <path d="M86 164 C95 88 120 52 154 51 L216 51 C239 52 242 82 225 107 C206 134 197 172 174 180 L116 181 C93 181 84 178 86 164 Z"
        fill="url(#aiGrad)" filter="url(#softShadow)"/>
  <path d="M197 101 C220 65 241 51 265 51 L225 51 C205 54 193 84 183 115 C171 151 159 177 132 181 L174 181 C205 176 216 139 230 113 Z"
        fill="#060A30" opacity="0.72"/>
  <path d="M168 132 C177 100 190 99 213 99 L264 99 C288 100 301 114 296 141 L284 204 C281 221 266 230 244 230 L187 230 C161 229 151 214 158 190 Z"
        fill="url(#aiGrad)"/>
  <text x="288" y="197" width="190" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="146" font-weight="800" fill="url(#aiGrad)" letter-spacing="-6">AI</text>

  <path d="M320 38 L330 72 L362 82 L330 92 L320 126 L309 92 L277 82 L309 72 Z"
        fill="#84F047" filter="url(#glow)"/>
  <path d="M299 76 L304 91 L319 96 L304 101 L299 116 L294 101 L279 96 L294 91 Z"
        fill="#D9F84E"/>

  <circle cx="208" cy="543" r="90" fill="url(#orangeGrad)" filter="url(#softShadow)"/>
  <path d="M208 453 A90 90 0 0 1 298 543 L208 543 Z" fill="#FFAC84" opacity="0.9"/>
  <path d="M208 543 L298 543 A90 90 0 0 1 208 633 Z" fill="#C93620" opacity="0.6"/>
  <rect x="105" y="493" width="102" height="99" rx="8" fill="#C63A1E" filter="url(#softShadow)"/>
  <rect x="111" y="493" width="92" height="94" rx="7" fill="#D84A25"/>
  <text x="128" y="569" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="72" font-weight="700" fill="#FFFFFF">P</text>

  <text x="335" y="542" width="570" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="124" font-weight="800" fill="#FFFFFF" letter-spacing="1">COPILOT</text>
  <text x="340" y="631" width="690" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="86" font-weight="800" fill="#FFFFFF" letter-spacing="1">PRESENTATION</text>
  <text x="342" y="672" width="500" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="500" fill="#C9D5FF" opacity="0.72">AI-assisted storytelling layout with geometric image masking</text>

  <rect x="1038" y="606" width="92" height="8" rx="4" fill="#80F0FF" opacity="0.55"/>
  <rect x="1150" y="606" width="42" height="8" rx="4" fill="#FFFFFF" opacity="0.35"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<mask>` to create the photo crop; use `<clipPath>` on the `<image>` only.
- ❌ Do not blur or mask a face inside SVG; instead choose a non-identifiable crop, a product/scene image, or a presenter photo already approved for use.
- ❌ Do not build the layout as a plain rectangle image placeholder plus bullets; the premium effect depends on circular/rounded masking, offset geometry, and atmospheric gradients.
- ❌ Do not use `<pattern>`, `<textPath>`, `<foreignObject>`, or `<use>` for logos/accents; draw simplified editable geometry directly.

## Composition notes
- Keep the hero image cluster dominant on the right 40–45% of the canvas, with the circle slightly bleeding toward the edge for a modern thumbnail/keynote feel.
- Put the strongest text block in the lower-left/middle zone; large white uppercase typography works well over the dark gradient.
- Use one saturated accent family for the AI/brand mark and one warmer accent family for the presentation/app icon, then repeat small glow accents near the hero image.
- Leave the center-top relatively open so the split layout breathes; translucent diagonal ribbons can connect the text side to the image side without crowding the slide.