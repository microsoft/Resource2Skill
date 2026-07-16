# SVG Recipe — Product Hero Split

## Visual mechanism
A split-screen hero composition pairs a large left-aligned value proposition with a visually dominant product image on the right. The energy comes from an asymmetric diagonal color field, layered shadows, clipped product imagery, and a single high-contrast CTA that anchors the marketing message.

## SVG primitives needed
- 3× <linearGradient> for the right hero field, CTA button, and subtle product-card surface
- 1× <radialGradient> for a soft atmospheric glow behind the product visual
- 2× <filter> definitions for product-card shadow and colored glow
- 1× <clipPath> with rounded <rect> for clipping the product screenshot / hero image
- 2× large <path> shapes for the diagonal split background and organic accent blob
- 4× <circle> / <ellipse> shapes for premium launch-style decorative accents
- 4× <rect> shapes for CTA button, product card, mini floating metric chips, and brand badge
- 1× <image> for the main product screenshot or product photography
- 7× <text> elements with explicit width attributes for brand, eyebrow, headline, subhead, CTA, and supporting product annotations

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="heroGrad" x1="690" y1="70" x2="1250" y2="650" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#7C3AED"/>
      <stop offset="0.45" stop-color="#2563EB"/>
      <stop offset="1" stop-color="#06B6D4"/>
    </linearGradient>

    <linearGradient id="ctaGrad" x1="92" y1="530" x2="280" y2="530" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#111827"/>
      <stop offset="1" stop-color="#334155"/>
    </linearGradient>

    <linearGradient id="cardGrad" x1="760" y1="180" x2="1130" y2="550" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF"/>
      <stop offset="1" stop-color="#EEF4FF"/>
    </linearGradient>

    <radialGradient id="aura" cx="50%" cy="50%" r="60%">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.62"/>
      <stop offset="0.55" stop-color="#93C5FD" stop-opacity="0.28"/>
      <stop offset="1" stop-color="#2563EB" stop-opacity="0"/>
    </radialGradient>

    <filter id="shadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="24" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="24" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>

    <clipPath id="productClip">
      <rect x="760" y="184" width="420" height="315" rx="30" ry="30"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F8FAFC"/>

  <path d="M665,0 C790,72 792,171 753,265 C717,354 730,434 817,505 C918,589 1048,605 1280,540 L1280,0 Z"
        fill="url(#heroGrad)"/>

  <path d="M1010,46 C1104,15 1197,71 1217,154 C1244,262 1139,297 1052,263 C957,225 913,78 1010,46 Z"
        fill="#FFFFFF" opacity="0.16" filter="url(#softGlow)"/>

  <circle cx="1080" cy="360" r="238" fill="url(#aura)" opacity="0.85"/>
  <circle cx="1198" cy="114" r="7" fill="#FFFFFF" opacity="0.9"/>
  <circle cx="695" cy="596" r="10" fill="#22D3EE" opacity="0.75"/>
  <ellipse cx="1185" cy="610" rx="64" ry="18" fill="#0F172A" opacity="0.16"/>

  <rect x="88" y="56" width="132" height="38" rx="19" fill="#FFFFFF" stroke="#E2E8F0"/>
  <circle cx="112" cy="75" r="10" fill="#2563EB"/>
  <text x="132" y="81" width="80" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#0F172A">
    NOVA
  </text>

  <text x="92" y="168" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" letter-spacing="2.8" fill="#2563EB">
    PRODUCT LAUNCH 2026
  </text>

  <text x="88" y="252" width="545" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="60" font-weight="800" fill="#0F172A">
    <tspan x="88" dy="0">Turn every</tspan>
    <tspan x="88" dy="70">customer signal</tspan>
    <tspan x="88" dy="70">into action.</tspan>
  </text>

  <text x="92" y="465" width="482" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="400" fill="#475569">
    Launch-ready product intelligence for teams that need faster decisions, cleaner workflows, and measurable growth.
  </text>

  <rect x="92" y="532" width="188" height="58" rx="29" fill="url(#ctaGrad)" filter="url(#shadow)"/>
  <text x="123" y="569" width="132" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#FFFFFF">
    Request demo
  </text>

  <text x="310" y="568" width="190" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" font-weight="600" fill="#64748B">
    Watch 90-sec tour
  </text>

  <g transform="rotate(-4 970 360)">
    <rect x="728" y="154" width="484" height="375" rx="38" fill="#1E293B" opacity="0.18" filter="url(#shadow)"/>
    <rect x="742" y="168" width="456" height="347" rx="34" fill="url(#cardGrad)" filter="url(#shadow)"/>

    <image x="760" y="184" width="420" height="315"
           href="https://images.example.com/product-dashboard-analytics-interface-4x3.png"
           clip-path="url(#productClip)" preserveAspectRatio="xMidYMid slice"/>

    <rect x="780" y="204" width="142" height="34" rx="17" fill="#FFFFFF" opacity="0.92"/>
    <circle cx="803" cy="221" r="6" fill="#22C55E"/>
    <text x="817" y="226" width="92" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" fill="#0F172A">
      Live insights
    </text>
  </g>

  <g transform="rotate(5 1090 480)">
    <rect x="1020" y="438" width="174" height="86" rx="24" fill="#FFFFFF" filter="url(#shadow)"/>
    <text x="1046" y="472" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#64748B">
      Conversion lift
    </text>
    <text x="1046" y="506" width="128" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="34" font-weight="800" fill="#2563EB">
      +38%
    </text>
  </g>

  <g transform="rotate(-8 760 218)">
    <rect x="676" y="184" width="162" height="76" rx="22" fill="#0F172A" opacity="0.94" filter="url(#shadow)"/>
    <text x="701" y="215" width="116" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" fill="#CBD5E1">
      Automations
    </text>
    <text x="701" y="244" width="110" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="28" font-weight="800" fill="#FFFFFF">
      12.4k
    </text>
  </g>

  <path d="M117,655 C158,628 216,632 252,658 C286,682 333,680 372,650"
        fill="none" stroke="#CBD5E1" stroke-width="4" stroke-linecap="round" stroke-dasharray="1 13"/>
</svg>
```

## Avoid in this skill
- ❌ Applying clip-path to decorative blobs, cards, or text; use clipping only on the hero <image>.
- ❌ Building the right-side product visual from dozens of tiny dashboard rectangles; a real clipped image or screenshot gives the hero slide premium impact.
- ❌ Centering all content symmetrically; the technique depends on a strong left/right imbalance.
- ❌ Using marker arrows or animated UI callouts; keep emphasis static and editable with cards, paths, and text.

## Composition notes
- Keep the left 45–50% of the slide calm and text-led: headline, subhead, CTA, and minimal brand furniture.
- Let the right 50–55% carry visual weight with a diagonal gradient field, oversized product card, and floating metric chips.
- Use one dominant accent family across the background, CTA support, and product annotations so the split feels intentional.
- Preserve generous negative space around the headline; the product visual can overlap the split boundary to create depth and launch energy.