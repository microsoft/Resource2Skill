# SVG Recipe — Dark Navy & Coral SaaS Pitch Slide (Lovable Minimalist Aesthetic)

## Visual mechanism
A premium dark-mode SaaS slide built from oversized white typography, coral attention blocks, and a floating product/app mockup on a deep navy radial spotlight background. The layout borrows from high-conversion landing pages and product-demo thumbnails: bold claim first, product proof second, with coral used only for urgency and focal guidance.

## SVG primitives needed
- 1× full-slide `<rect>` for the deep navy background
- 2× large translucent `<ellipse>` elements for radial ambient spotlight/glow
- 1× `<linearGradient>` for the coral-to-indigo “MASTER” label banner
- 2× `<radialGradient>` / `<linearGradient>` definitions for app-icon and background effects
- 3× `<filter>` definitions for soft shadow, text lift, and coral glow
- 1× rounded `<rect>` gradient banner behind the headline keyword
- 1× coral `<rect>` banner behind the urgency line
- 6× large `<text>` elements for hero typography, subtitle, and feature captions
- 1× clipped `<image>` for a dashboard/product screenshot mockup
- 1× `<clipPath>` with rounded rectangle for the screenshot crop
- 8–12× small `<rect>` and `<circle>` elements for editable faux SaaS UI details
- 1× rounded white `<rect>` for the floating app tile
- 2× gradient `<path>` shapes for the Lovable-style heart/cloud app mark
- 1× curved `<path>` plus 1× triangular `<path>` for a hand-drawn arrow cue
- 3× coral accent dots/checks using `<circle>` and `<path>`

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#111827"/>
      <stop offset="48%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#050816"/>
    </linearGradient>

    <radialGradient id="blueSpot" cx="42%" cy="28%" r="62%">
      <stop offset="0%" stop-color="#3157ff" stop-opacity="0.62"/>
      <stop offset="45%" stop-color="#172554" stop-opacity="0.30"/>
      <stop offset="100%" stop-color="#020617" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="coralSpot" cx="58%" cy="46%" r="55%">
      <stop offset="0%" stop-color="#ff6b6b" stop-opacity="0.42"/>
      <stop offset="55%" stop-color="#7c3aed" stop-opacity="0.20"/>
      <stop offset="100%" stop-color="#020617" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="masterGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#f97316"/>
      <stop offset="45%" stop-color="#ff4f8b"/>
      <stop offset="100%" stop-color="#4f46e5"/>
    </linearGradient>

    <linearGradient id="appGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ff8a00"/>
      <stop offset="36%" stop-color="#ff3d81"/>
      <stop offset="72%" stop-color="#7c3aed"/>
      <stop offset="100%" stop-color="#2563eb"/>
    </linearGradient>

    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="170%">
      <feOffset dx="0" dy="22"/>
      <feGaussianBlur stdDeviation="24"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="textLift" x="-10%" y="-10%" width="130%" height="140%">
      <feOffset dx="0" dy="5"/>
      <feGaussianBlur stdDeviation="4"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="coralGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>

    <clipPath id="dashClip">
      <rect x="754" y="104" width="432" height="292" rx="26"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <ellipse cx="760" cy="200" rx="520" ry="360" fill="url(#blueSpot)"/>
  <ellipse cx="930" cy="360" rx="390" ry="310" fill="url(#coralSpot)"/>
  <rect x="0" y="0" width="1280" height="720" fill="#000000" opacity="0.22"/>

  <rect x="36" y="32" width="604" height="186" rx="0" fill="url(#masterGrad)" filter="url(#textLift)"/>
  <text x="58" y="196" width="560" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="194" font-weight="900" letter-spacing="-10" fill="#ffffff" filter="url(#textLift)">MASTER</text>

  <text x="42" y="362" width="620" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="126" font-weight="900" letter-spacing="-6" fill="#ffffff" filter="url(#textLift)">Lovable</text>

  <rect x="36" y="392" width="360" height="88" rx="0" fill="#ef1d2d"/>
  <text x="48" y="465" width="330" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="66" font-weight="900" letter-spacing="-3" fill="#ffffff" filter="url(#textLift)">IN 15 MINS</text>

  <text x="44" y="546" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="600" fill="#cbd5e1">Build, launch, and pitch your SaaS idea with one clean dark-mode story.</text>

  <path d="M280 488 C322 566, 415 590, 492 542" fill="none" stroke="#fff7f7" stroke-width="12" stroke-linecap="round"/>
  <path d="M486 540 L438 531 L462 575 Z" fill="#fff7f7"/>

  <rect x="728" y="80" width="486" height="342" rx="32" fill="#020617" opacity="0.72" filter="url(#softShadow)"/>
  <image x="754" y="104" width="432" height="292" clip-path="url(#dashClip)" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/dark-saas-dashboard-no-people-product-analytics.png"/>

  <rect x="754" y="104" width="432" height="292" rx="26" fill="#0f172a" opacity="0.68"/>
  <rect x="782" y="130" width="104" height="14" rx="7" fill="#ffffff" opacity="0.92"/>
  <circle cx="1138" cy="137" r="7" fill="#ff6b6b"/>
  <circle cx="1160" cy="137" r="7" fill="#fbbf24"/>
  <circle cx="1182" cy="137" r="7" fill="#34d399"/>

  <rect x="782" y="170" width="142" height="72" rx="16" fill="#111827" stroke="#334155" stroke-width="1.5"/>
  <rect x="946" y="170" width="212" height="72" rx="16" fill="#111827" stroke="#334155" stroke-width="1.5"/>
  <text x="802" y="201" width="110" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#f8fafc">ARR</text>
  <text x="802" y="227" width="110" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="28" font-weight="800" fill="#ff6b6b">$42k</text>
  <text x="970" y="201" width="160" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#f8fafc">Launch velocity</text>
  <rect x="970" y="218" width="154" height="9" rx="5" fill="#334155"/>
  <rect x="970" y="218" width="116" height="9" rx="5" fill="#ff6b6b"/>

  <rect x="782" y="264" width="376" height="100" rx="18" fill="#0b1120" stroke="#334155" stroke-width="1.5"/>
  <path d="M806 334 C842 284, 882 322, 916 292 C950 262, 996 306, 1034 276 C1072 246, 1114 274, 1134 238" fill="none" stroke="#ff6b6b" stroke-width="5" stroke-linecap="round"/>
  <circle cx="806" cy="334" r="5" fill="#ff6b6b"/>
  <circle cx="916" cy="292" r="5" fill="#ff6b6b"/>
  <circle cx="1034" cy="276" r="5" fill="#ff6b6b"/>
  <circle cx="1134" cy="238" r="5" fill="#ff6b6b"/>

  <rect x="596" y="348" width="238" height="238" rx="34" fill="#ffffff" filter="url(#softShadow)" transform="rotate(-9 715 467)"/>
  <rect x="614" y="366" width="202" height="202" rx="28" fill="#f8fafc" opacity="0.96" transform="rotate(-9 715 467)"/>
  <path d="M677 468 C639 430, 655 384, 700 394 C719 398, 730 414, 734 430 C748 412, 775 407, 795 423 C824 447, 811 492, 772 522 L686 540 Z"
        fill="url(#appGrad)" filter="url(#coralGlow)" transform="rotate(-9 735 466)"/>
  <path d="M677 468 C639 430, 655 384, 700 394 C719 398, 730 414, 734 430 C748 412, 775 407, 795 423 C824 447, 811 492, 772 522 L686 540 Z"
        fill="url(#appGrad)" transform="rotate(-9 735 466)"/>

  <rect x="850" y="466" width="318" height="154" rx="26" fill="#0f172a" opacity="0.88" stroke="#1e293b" stroke-width="1.5"/>
  <circle cx="886" cy="506" r="9" fill="#ff6b6b"/>
  <text x="908" y="513" width="220" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="800" fill="#ffffff">AI-generated UI</text>
  <text x="886" y="548" width="250" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="500" fill="#94a3b8">Turn a single prompt into production-ready screens, flows, and CRM logic.</text>
  <path d="M884 589 L894 599 L914 576" fill="none" stroke="#ff6b6b" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="926" y="599" width="190" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700" fill="#e2e8f0">Pitch-ready in minutes</text>

  <text x="42" y="672" width="620" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="600" fill="#64748b">Dark navy · white type · coral focus · floating SaaS proof</text>
</svg>
```

## Avoid in this skill
- ❌ Using a flat black background only; the Lovable-style dark aesthetic needs subtle navy/blue/coral depth.
- ❌ Overusing coral for every element; reserve it for the urgency banner, key metric, CTA, or app highlight.
- ❌ Building the product area as a plain grid of rectangles with no elevation; the mockup should feel like a premium floating object.
- ❌ Applying `clip-path` to regular shapes; use it only on the screenshot `<image>` so the crop remains reliable.
- ❌ Using SVG animation for the “floating” mockup; represent drift through rotation, shadow, and offset layering instead.

## Composition notes
- Keep the left side typographic and loud: 45–55% of the slide can be dominated by oversized white title text and coral label blocks.
- Place the product proof on the right or lower-right, elevated with a soft shadow and slight rotation so it feels tactile rather than dashboard-flat.
- Use coral in a strict rhythm: one major coral banner, one metric/accent line, and one app/logo gradient.
- Leave dark negative space around the main objects; the premium feel comes from contrast, not from filling every corner.