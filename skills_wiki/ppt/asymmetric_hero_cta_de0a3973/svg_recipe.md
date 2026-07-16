# SVG Recipe — Asymmetric Hero CTA

## Visual mechanism
A full-height hero photograph occupies the larger side of the slide while a clean, vertically centered offer stack occupies the other side. A curved asymmetric seam, premium typography, feature proof points, and a high-contrast CTA button guide the eye from emotion to action.

## SVG primitives needed
- 2× `<rect>` for the white slide base and translucent image color overlay
- 1× `<image>` clipped to the hero column for the full-height emotional visual
- 1× `<clipPath>` with a `<rect>` to crop the image column cleanly
- 2× `<path>` for the curved white seam and subtle decorative hero-side highlight
- 1× `<linearGradient>` for the photographic color wash
- 1× `<linearGradient>` for the CTA button fill
- 1× `<radialGradient>` for a soft accent glow behind the text panel
- 1× `<filter id="softShadow">` applied to the CTA button
- 1× `<filter id="textGlow">` applied to small accent elements
- 8× `<text>` blocks for eyebrow, headline, product name, body copy, feature labels, and CTA label
- 5× `<circle>` elements for numbered feature icons
- 1× `<line>` for the small accent divider

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="heroClip">
      <rect x="520" y="0" width="760" height="720"/>
    </clipPath>

    <linearGradient id="photoWash" x1="520" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#18224A" stop-opacity="0.10"/>
      <stop offset="0.55" stop-color="#4454A4" stop-opacity="0.16"/>
      <stop offset="1" stop-color="#050814" stop-opacity="0.42"/>
    </linearGradient>

    <linearGradient id="buttonGrad" x1="86" y1="574" x2="330" y2="640" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#596DFF"/>
      <stop offset="0.52" stop-color="#4454A4"/>
      <stop offset="1" stop-color="#27347E"/>
    </linearGradient>

    <radialGradient id="panelGlow" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse"
      gradientTransform="translate(110 150) rotate(42) scale(420 250)">
      <stop offset="0" stop-color="#EEF1FF" stop-opacity="0.95"/>
      <stop offset="0.62" stop-color="#F8F9FF" stop-opacity="0.45"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-30%" width="150%" height="180%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="12"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.12  0 0 0 0 0.16  0 0 0 0 0.36  0 0 0 0.24 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="textGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>
  <rect x="0" y="0" width="520" height="720" fill="url(#panelGlow)"/>

  <image x="520" y="0" width="760" height="720"
    href="https://images.example.com/vertical-hero-photo-confident-founder-with-laptop.jpg"
    xlink:href="https://images.example.com/vertical-hero-photo-confident-founder-with-laptop.jpg"
    preserveAspectRatio="xMidYMid slice" clip-path="url(#heroClip)"/>

  <rect x="520" y="0" width="760" height="720" fill="url(#photoWash)"/>

  <path d="M520 0 L622 0 C584 118 573 230 598 350 C621 463 596 588 548 720 L0 720 L0 0 Z"
    fill="#FFFFFF"/>

  <path d="M1060 68 C1135 96 1187 165 1192 248 C1198 345 1134 410 1064 446 C1005 476 980 542 1006 611 C947 569 919 504 936 439 C950 384 1001 355 1039 325 C1093 282 1092 195 1060 68 Z"
    fill="#FFFFFF" opacity="0.14"/>

  <text x="88" y="92" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="16" font-weight="700" letter-spacing="2.4" fill="#4454A4">
    LIMITED LAUNCH OFFER
  </text>

  <line x1="88" y1="118" x2="164" y2="118" stroke="#4454A4" stroke-width="4" stroke-linecap="round"/>

  <text x="84" y="190" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="58" font-weight="800" fill="#1E1E1E">
    <tspan x="84" dy="0">Scale your</tspan>
    <tspan x="84" dy="62">sales engine</tspan>
    <tspan x="84" dy="70" fill="#4454A4">$320.00</tspan>
  </text>

  <text x="88" y="373" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="24" font-weight="700" fill="#1E1E1E">
    eBook Sales Booster
  </text>

  <text x="88" y="414" width="390" font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="17" fill="#595959">
    <tspan x="88" dy="0">A compact growth playbook for founders and sales</tspan>
    <tspan x="88" dy="25">teams who need sharper positioning, cleaner</tspan>
    <tspan x="88" dy="25">funnels, and conversion-ready launch assets.</tspan>
  </text>

  <circle cx="104" cy="508" r="15" fill="#EEF1FF" stroke="#4454A4" stroke-width="2"/>
  <text x="98" y="514" width="18" font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="13" font-weight="800" fill="#4454A4">1</text>
  <text x="132" y="514" width="310" font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="16" font-weight="600" fill="#303030">2,000+ core slide frameworks</text>

  <circle cx="104" cy="548" r="15" fill="#EEF1FF" stroke="#4454A4" stroke-width="2"/>
  <text x="98" y="554" width="18" font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="13" font-weight="800" fill="#4454A4">2</text>
  <text x="132" y="554" width="310" font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="16" font-weight="600" fill="#303030">Lifetime updates and support</text>

  <circle cx="104" cy="588" r="15" fill="#EEF1FF" stroke="#4454A4" stroke-width="2"/>
  <text x="98" y="594" width="18" font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="13" font-weight="800" fill="#4454A4">3</text>
  <text x="132" y="594" width="310" font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="16" font-weight="600" fill="#303030">28,000+ icons and vector assets</text>

  <rect x="88" y="630" width="250" height="58" rx="29" fill="url(#buttonGrad)" filter="url(#softShadow)"/>
  <text x="126" y="666" width="180" font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="18" font-weight="800" fill="#FFFFFF">Purchase Today!</text>

  <circle cx="445" cy="646" r="7" fill="#4454A4" opacity="0.25" filter="url(#textGlow)"/>
  <circle cx="468" cy="646" r="7" fill="#4454A4" opacity="0.16"/>
  <circle cx="491" cy="646" r="7" fill="#4454A4" opacity="0.10"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use a `<mask>` to fade the photo edge; use a white curved `<path>` seam or a normal overlay `<rect>` instead.
- ❌ Do not apply `clip-path` to text, paths, or rectangles; reserve clipping for the hero `<image>`.
- ❌ Do not create the CTA arrow with `marker-end` on a `<path>`; if an arrow is needed, use a `<line>` with marker directly on the line or draw the arrowhead as a small path.
- ❌ Do not overcrowd the offer side with many equal-weight bullets; the CTA needs a clear visual runway.
- ❌ Do not place low-contrast text directly on the photo unless it sits on a deliberate overlay panel.

## Composition notes
- Keep the hero image at roughly 55–60% of the slide width; the text panel should feel calm, spacious, and vertically centered.
- Use the curved white seam to soften the split and make the layout feel editorial rather than like two rigid rectangles.
- The visual path should read: eyebrow → headline/price → product promise → three proof points → button.
- Choose one dominant accent color and repeat it in the price, feature circles, divider, and CTA button for a premium, controlled rhythm.