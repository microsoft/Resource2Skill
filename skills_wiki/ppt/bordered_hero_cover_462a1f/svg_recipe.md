# SVG Recipe — Bordered Hero Cover

## Visual mechanism
A single cinematic image dominates the slide, held inside a thick editable border frame so it reads like a premium poster or framed keynote opener. A subtle gradient veil and compact headline block sit over the image, while oversized background glows and corner accents add depth without competing with the hero visual.

## SVG primitives needed
- 1× `<image>` for the full-slide hero photograph, cropped with `preserveAspectRatio="xMidYMid slice"`
- 1× `<clipPath>` with rounded `<rect>` to crop the hero image cleanly
- 5× `<rect>` for background, outer frame, inner image rim, headline plate, and small label pill
- 4× `<path>` for decorative corner brackets and energetic accent strokes
- 2× `<radialGradient>` for ambient background glow
- 2× `<linearGradient>` for the border treatment and image readability overlay
- 2× `<filter>` using blur / offset shadow for lifted frame and headline panel
- 3× `<text>` elements with explicit `width` attributes for eyebrow, headline, and subtitle metadata

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgGlowA" cx="18%" cy="18%" r="72%">
      <stop offset="0%" stop-color="#7C3AED" stop-opacity="0.55"/>
      <stop offset="45%" stop-color="#24115F" stop-opacity="0.28"/>
      <stop offset="100%" stop-color="#080B14" stop-opacity="1"/>
    </radialGradient>

    <radialGradient id="bgGlowB" cx="86%" cy="82%" r="65%">
      <stop offset="0%" stop-color="#06B6D4" stop-opacity="0.38"/>
      <stop offset="55%" stop-color="#0F172A" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="#080B14" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="frameGradient" x1="78" y1="46" x2="1210" y2="684" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="28%" stop-color="#FDE68A"/>
      <stop offset="62%" stop-color="#67E8F9"/>
      <stop offset="100%" stop-color="#FFFFFF"/>
    </linearGradient>

    <linearGradient id="imageVeil" x1="112" y1="72" x2="1168" y2="657" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#020617" stop-opacity="0.18"/>
      <stop offset="50%" stop-color="#020617" stop-opacity="0"/>
      <stop offset="100%" stop-color="#020617" stop-opacity="0.74"/>
    </linearGradient>

    <filter id="frameShadow" x="-8%" y="-8%" width="116%" height="116%">
      <feOffset dx="0" dy="20"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>

    <clipPath id="heroClip">
      <rect x="112" y="70" width="1056" height="587" rx="24" ry="24"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#080B14"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGlowA)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGlowB)"/>

  <path d="M70 96 C132 42, 204 35, 284 78 C228 88, 166 117, 109 169 C92 145, 79 121, 70 96 Z"
        fill="#A78BFA" opacity="0.28" filter="url(#softGlow)"/>
  <path d="M1045 640 C1104 572, 1172 558, 1226 604 C1197 641, 1156 674, 1084 690 C1068 678, 1055 661, 1045 640 Z"
        fill="#22D3EE" opacity="0.22" filter="url(#softGlow)"/>

  <rect x="82" y="40" width="1116" height="647" rx="38" ry="38"
        fill="#050816" opacity="0.72" filter="url(#frameShadow)"/>

  <rect x="88" y="46" width="1104" height="635" rx="36" ry="36"
        fill="none" stroke="url(#frameGradient)" stroke-width="16"/>

  <rect x="104" y="62" width="1072" height="603" rx="28" ry="28"
        fill="#0F172A" stroke="#FFFFFF" stroke-opacity="0.18" stroke-width="2"/>

  <image x="112" y="70" width="1056" height="587"
         href="https://images.example.com/hero-cover/cinematic-futuristic-aircraft-over-neon-city.jpg"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#heroClip)"/>

  <rect x="112" y="70" width="1056" height="587" rx="24" ry="24"
        fill="url(#imageVeil)"/>

  <path d="M92 140 L92 74 L158 74" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" opacity="0.9"/>
  <path d="M1188 580 L1188 665 L1103 665" fill="none" stroke="#FDE68A" stroke-width="4" stroke-linecap="round" opacity="0.9"/>
  <path d="M1015 89 C1065 112, 1105 113, 1152 92" fill="none" stroke="#67E8F9" stroke-width="5" stroke-linecap="round" opacity="0.75"/>
  <path d="M130 646 C188 618, 233 622, 284 654" fill="none" stroke="#FDE68A" stroke-width="5" stroke-linecap="round" opacity="0.72"/>

  <rect x="154" y="466" width="624" height="152" rx="24" ry="24"
        fill="#020617" opacity="0.62" filter="url(#frameShadow)"/>

  <rect x="178" y="489" width="178" height="34" rx="17" ry="17"
        fill="#FFFFFF" opacity="0.92"/>

  <text x="199" y="512" width="140"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" letter-spacing="2.2"
        fill="#111827">SECTION 01</text>

  <text x="176" y="569" width="570"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="54" font-weight="800"
        fill="#FFFFFF">
    <tspan x="176" dy="0">Bordered Hero</tspan>
    <tspan x="176" dy="55" fill="#FDE68A">Cover System</tspan>
  </text>

  <text x="178" y="646" width="520"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="500"
        fill="#E5E7EB" opacity="0.9">A cinematic frame for bold section openers and keynote title slides.</text>
</svg>
```

## Avoid in this skill
- ❌ Applying `clip-path` to a `<g>` or `<rect>` to crop the whole frame; only the `<image>` crop is reliably preserved as editable PowerPoint content.
- ❌ Using `<mask>` for the dark image fade; use a semi-transparent rounded `<rect>` with a gradient fill instead.
- ❌ Making the border part of the raster image; keep the frame as editable SVG strokes/rectangles so theme colors and thickness can be adjusted in PowerPoint.
- ❌ Placing text too close to the frame edge; PowerPoint text boxes need breathing room and explicit `width`.

## Composition notes
- Keep the hero frame large: about 86–92% of slide width and 82–90% of slide height for a true cover-page feel.
- Use a thick outer border plus a faint inner rim; this creates the “framed poster” effect even when the hero image is visually busy.
- Place headline content in the lower-left or lower-right over a translucent plate, leaving the image subject unobstructed.
- Use 1–2 accent colors from the image in the border gradient and corner marks to make the layout feel intentionally art-directed.