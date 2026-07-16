# SVG Recipe — Opinionated Brand Aesthetics (The "Anti-Slop" Manifesto)

## Visual mechanism
A premium, anti-generic cover slide built from a near-black brutalist canvas, dimmed product/UI artifacts in the background, a high-contrast monochrome hero crop, one saturated terra-cotta brand mark, and oversized typography. The “anti-slop” effect comes from strict restraint: almost no gradients, deliberate opacity, tactile grain, hard asymmetry, and one confident accent color.

## SVG primitives needed
- 1× `<rect>` for the off-black full-slide background
- 2× `<radialGradient>` overlays for subtle vignette and spotlight depth
- 1× `<image>` for a right-side monochrome portrait/hero figure, clipped by a rectangular crop
- 1× `<clipPath>` with `<rect>` for cropping the hero image to the right side
- 1× `<rect>` privacy/abstraction block over the portrait area if an anonymized editorial look is desired
- 8–12× low-opacity `<rect>` elements for ghosted dashboard cards and UI panels in the background
- 4–6× `<line>` and `<path>` elements for faint chart axes, separators, progress bars, and line-chart traces
- 1× rounded `<rect>` for the saturated terra-cotta app icon block
- 12× short rounded `<path>` strokes for the white radial burst logo inside the app icon
- 3× `<text>` blocks for eyebrow, massive display title, and accent subtitle; every text element must include `width`
- 20–40× tiny low-opacity `<circle>` or `<rect>` specks for editable faux film grain
- 1× `<filter id="softShadow">` for the app icon and selected foreground objects
- 1× `<filter id="cardShadow">` for soft separation on dark UI panels

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="warmGlow" cx="18%" cy="47%" r="62%">
      <stop offset="0%" stop-color="#2a211d" stop-opacity="0.62"/>
      <stop offset="58%" stop-color="#141413" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="rightVignette" cx="78%" cy="40%" r="62%">
      <stop offset="0%" stop-color="#242423" stop-opacity="0.40"/>
      <stop offset="100%" stop-color="#050505" stop-opacity="0.70"/>
    </radialGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="20"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="cardShadow" x="-15%" y="-15%" width="130%" height="130%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="16"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <clipPath id="heroCrop">
      <rect x="545" y="0" width="735" height="720"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#141413"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#warmGlow)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#rightVignette)"/>

  <!-- Ghosted product UI: visible enough to imply craft, dim enough to stay subordinate -->
  <rect x="306" y="36" width="430" height="244" rx="18" fill="#0f0f0e" opacity="0.74" filter="url(#cardShadow)"/>
  <rect x="332" y="68" width="120" height="9" rx="4" fill="#f5f3ed" opacity="0.09"/>
  <text x="332" y="102" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" letter-spacing="1.6" fill="#f5f3ed" opacity="0.13">NET WORTH</text>
  <text x="332" y="139" width="320" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="34" font-weight="700" fill="#f5f3ed" opacity="0.32">$187,872.47</text>
  <line x1="332" y1="256" x2="703" y2="256" stroke="#f5f3ed" stroke-width="5" stroke-linecap="round" opacity="0.20"/>
  <line x1="332" y1="256" x2="612" y2="256" stroke="#d97757" stroke-width="5" stroke-linecap="round" opacity="0.30"/>
  <rect x="749" y="44" width="538" height="244" rx="18" fill="#0d0d0c" opacity="0.66" filter="url(#cardShadow)"/>
  <text x="769" y="77" width="180" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#f5f3ed" opacity="0.14">Net liquidity</text>
  <path d="M782 195 C850 166, 900 182, 948 150 S1068 107, 1218 112" fill="none" stroke="#f5f3ed" stroke-width="2" opacity="0.48"/>
  <line x1="786" y1="248" x2="1224" y2="248" stroke="#f5f3ed" stroke-width="1" opacity="0.09"/>
  <text x="1102" y="260" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" fill="#f5f3ed" opacity="0.22">Nov 30</text>
  <text x="1203" y="260" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" fill="#f5f3ed" opacity="0.22">Dec 31</text>
  <rect x="322" y="293" width="410" height="188" rx="13" fill="#10100f" opacity="0.63"/>
  <rect x="342" y="342" width="174" height="66" rx="10" fill="#171716" opacity="0.52"/>
  <rect x="540" y="342" width="174" height="66" rx="10" fill="#171716" opacity="0.52"/>
  <text x="344" y="390" width="160" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700" fill="#f5f3ed" opacity="0.19">$6,500.00</text>
  <text x="542" y="390" width="160" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700" fill="#f5f3ed" opacity="0.19">$4,110.45</text>

  <!-- Right-side monochrome editorial hero image -->
  <image x="500" y="-8" width="790" height="750" clip-path="url(#heroCrop)" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/black-and-white-editorial-portrait-cropped-torso-dark-shirt.png" opacity="0.78"/>
  <rect x="548" y="0" width="732" height="720" fill="#000000" opacity="0.18"/>
  <rect x="780" y="115" width="263" height="370" fill="#3d3d3a" opacity="0.92"/>

  <!-- Terra-cotta brand tile -->
  <rect x="37" y="180" width="231" height="229" rx="50" fill="#d97757" filter="url(#softShadow)"/>
  <path d="M153 223 L153 364" stroke="#f8f5ee" stroke-width="14" stroke-linecap="round"/>
  <path d="M112 252 L193 335" stroke="#f8f5ee" stroke-width="14" stroke-linecap="round"/>
  <path d="M88 292 L229 311" stroke="#f8f5ee" stroke-width="10" stroke-linecap="round"/>
  <path d="M115 360 L197 225" stroke="#f8f5ee" stroke-width="13" stroke-linecap="round"/>
  <path d="M74 292 L234 282" stroke="#f8f5ee" stroke-width="10" stroke-linecap="round"/>
  <path d="M91 335 L208 233" stroke="#f8f5ee" stroke-width="12" stroke-linecap="round"/>
  <path d="M131 217 L191 356" stroke="#f8f5ee" stroke-width="13" stroke-linecap="round"/>
  <path d="M84 249 L226 313" stroke="#f8f5ee" stroke-width="12" stroke-linecap="round"/>

  <!-- Brutalist type hierarchy -->
  <text x="49" y="583" width="520" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="152" font-weight="900" letter-spacing="-8" fill="#faf9f5">Skills</text>
  <text x="48" y="670" width="610" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="66" font-weight="800" letter-spacing="-3" fill="#d97757">For Designers</text>
  <text x="52" y="703" width="470" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" font-weight="700" letter-spacing="3.2" fill="#faf9f5" opacity="0.34">01 — ANTI-SLOP BRAND SYSTEM</text>

  <!-- Editable faux grain: tiny, irregular specks instead of non-translating patterns -->
  <circle cx="92" cy="73" r="1.2" fill="#ffffff" opacity="0.10"/>
  <circle cx="182" cy="131" r="0.9" fill="#ffffff" opacity="0.08"/>
  <circle cx="267" cy="86" r="1.0" fill="#000000" opacity="0.18"/>
  <circle cx="417" cy="61" r="0.8" fill="#ffffff" opacity="0.08"/>
  <circle cx="624" cy="114" r="1.1" fill="#ffffff" opacity="0.06"/>
  <circle cx="872" cy="62" r="1.2" fill="#ffffff" opacity="0.07"/>
  <circle cx="1118" cy="87" r="0.9" fill="#ffffff" opacity="0.07"/>
  <circle cx="1191" cy="180" r="1.0" fill="#000000" opacity="0.18"/>
  <circle cx="1008" cy="511" r="0.9" fill="#ffffff" opacity="0.06"/>
  <circle cx="725" cy="625" r="1.1" fill="#ffffff" opacity="0.06"/>
  <circle cx="516" cy="684" r="0.9" fill="#ffffff" opacity="0.07"/>
  <circle cx="292" cy="635" r="1.0" fill="#000000" opacity="0.20"/>
  <rect x="33" y="40" width="1.5" height="1.5" fill="#ffffff" opacity="0.07"/>
  <rect x="213" y="508" width="1.4" height="1.4" fill="#ffffff" opacity="0.06"/>
  <rect x="1074" y="675" width="1.5" height="1.5" fill="#ffffff" opacity="0.07"/>
</svg>
```

## Avoid in this skill
- ❌ Purple-blue “AI gradient” backgrounds; this technique depends on near-black restraint and one disciplined accent
- ❌ Generic rounded-card grids as the main composition; background UI should be ghosted, not become a dashboard slide
- ❌ `<pattern>` for grain; use sparse editable specks or a raster noise image if texture is essential
- ❌ Masking or clipping non-image shapes; keep clips only on `<image>` elements for reliable PowerPoint translation
- ❌ Overusing shadows and glows; use them sparingly so the slide feels editorial, not SaaS-template glossy
- ❌ Centered symmetrical layouts; asymmetry is part of the anti-slop posture

## Composition notes
- Keep the left third dominated by the brand mark and typography; let the right side carry the dark editorial image mass.
- Use opacity aggressively: background UI should sit around 6–25% visibility so it reads as atmosphere, not content.
- Reserve the saturated terra-cotta for the app tile and subtitle only; this makes the accent feel authored and premium.
- Let massive type crop close to the bottom edge; the slight tension makes the layout feel like a designed poster rather than a default slide.