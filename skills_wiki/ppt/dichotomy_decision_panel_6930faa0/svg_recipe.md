# SVG Recipe — Dichotomy Decision Panel

## Visual mechanism
A decisive 50/50 vertical split uses green versus red panels to create an instant “yes/no” or “opportunity/risk” frame. Large symbolic icons, translucent content cards, and a bright central divider make the opposition feel structured, executive, and decision-ready.

## SVG primitives needed
- 2× `<rect>` for the full-height left/right color panels
- 2× `<linearGradient>` for premium green/red panel depth
- 2× `<path>` for large semi-transparent decorative background waves
- 1× `<rect>` for the central vertical decision spine
- 2× `<circle>` for icon medallions behind the check and X
- 3× `<path>` for the check icon and two crossing strokes of the X icon
- 2× `<rect>` for frosted-glass content cards
- 6× `<circle>` for bullet dots inside the cards
- 10× `<text>` blocks for titles, subtitles, bullet text, and footer labels
- 1× `<filter id="cardShadow">` applied to content cards and icon medallions
- 1× `<filter id="softGlow">` applied to the central divider and icon strokes

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="greenPanel" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#34C76F"/>
      <stop offset="55%" stop-color="#24A85A"/>
      <stop offset="100%" stop-color="#137A43"/>
    </linearGradient>
    <linearGradient id="redPanel" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F04B45"/>
      <stop offset="55%" stop-color="#D91E18"/>
      <stop offset="100%" stop-color="#9F1515"/>
    </linearGradient>
    <linearGradient id="dividerGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.15"/>
      <stop offset="45%" stop-color="#FFFFFF" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.15"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="16"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="5"/>
    </filter>
  </defs>

  <!-- Split-screen panels -->
  <rect x="0" y="0" width="640" height="720" fill="url(#greenPanel)"/>
  <rect x="640" y="0" width="640" height="720" fill="url(#redPanel)"/>

  <!-- Decorative depth waves -->
  <path d="M0,520 C130,445 250,510 360,420 C465,335 540,365 640,285 L640,720 L0,720 Z"
        fill="#FFFFFF" opacity="0.08"/>
  <path d="M1280,120 C1140,205 1015,145 915,250 C810,360 720,330 640,430 L640,0 L1280,0 Z"
        fill="#FFFFFF" opacity="0.08"/>

  <!-- Central decision spine -->
  <rect x="636" y="0" width="8" height="720" fill="url(#dividerGrad)" filter="url(#softGlow)"/>
  <circle cx="640" cy="360" r="34" fill="#FFFFFF" opacity="0.18"/>
  <circle cx="640" cy="360" r="18" fill="#FFFFFF" opacity="0.88"/>

  <!-- Left header -->
  <text x="320" y="82" width="520" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="50" font-weight="800"
        letter-spacing="4" fill="#FFFFFF">OPPORTUNITIES</text>
  <text x="320" y="122" width="480" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="500"
        fill="#DDFBE9" opacity="0.95">What we gain by moving forward</text>

  <!-- Right header -->
  <text x="960" y="82" width="520" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="50" font-weight="800"
        letter-spacing="4" fill="#FFFFFF">RISKS</text>
  <text x="960" y="122" width="480" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="500"
        fill="#FFE0DE" opacity="0.95">What could derail the decision</text>

  <!-- Icon medallions -->
  <circle cx="320" cy="225" r="72" fill="#FFFFFF" opacity="0.14" filter="url(#cardShadow)"/>
  <circle cx="960" cy="225" r="72" fill="#FFFFFF" opacity="0.14" filter="url(#cardShadow)"/>

  <!-- Check icon -->
  <path d="M278,225 L311,258 L369,188"
        fill="none" stroke="#FFFFFF" stroke-width="22" stroke-linecap="round" stroke-linejoin="round"
        filter="url(#softGlow)"/>

  <!-- X icon -->
  <path d="M918,183 L1002,267"
        fill="none" stroke="#FFFFFF" stroke-width="22" stroke-linecap="round" filter="url(#softGlow)"/>
  <path d="M1002,183 L918,267"
        fill="none" stroke="#FFFFFF" stroke-width="22" stroke-linecap="round" filter="url(#softGlow)"/>

  <!-- Content cards -->
  <rect x="82" y="348" width="476" height="248" rx="28" fill="#FFFFFF" opacity="0.16"
        stroke="#FFFFFF" stroke-opacity="0.22" stroke-width="1.5" filter="url(#cardShadow)"/>
  <rect x="722" y="348" width="476" height="248" rx="28" fill="#FFFFFF" opacity="0.16"
        stroke="#FFFFFF" stroke-opacity="0.22" stroke-width="1.5" filter="url(#cardShadow)"/>

  <!-- Left bullets -->
  <circle cx="126" cy="404" r="6" fill="#FFFFFF"/>
  <text x="148" y="411" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="600" fill="#FFFFFF">Accelerates executive alignment</text>
  <circle cx="126" cy="474" r="6" fill="#FFFFFF"/>
  <text x="148" y="481" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="600" fill="#FFFFFF">Creates a sharper market position</text>
  <circle cx="126" cy="544" r="6" fill="#FFFFFF"/>
  <text x="148" y="551" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="600" fill="#FFFFFF">Unlocks measurable operating leverage</text>

  <!-- Right bullets -->
  <circle cx="766" cy="404" r="6" fill="#FFFFFF"/>
  <text x="788" y="411" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="600" fill="#FFFFFF">Requires disciplined change adoption</text>
  <circle cx="766" cy="474" r="6" fill="#FFFFFF"/>
  <text x="788" y="481" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="600" fill="#FFFFFF">May expose legacy process gaps</text>
  <circle cx="766" cy="544" r="6" fill="#FFFFFF"/>
  <text x="788" y="551" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="600" fill="#FFFFFF">Benefits depend on execution quality</text>

  <!-- Bottom decision cue -->
  <text x="320" y="660" width="500" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700"
        letter-spacing="2" fill="#FFFFFF" opacity="0.82">RECOMMEND IF UPSIDE IS STRATEGIC</text>
  <text x="960" y="660" width="500" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700"
        letter-spacing="2" fill="#FFFFFF" opacity="0.82">MITIGATE BEFORE COMMITMENT</text>
</svg>
```

## Avoid in this skill
- ❌ Using low-contrast pastel panels; the dichotomy depends on immediate green/red recognition.
- ❌ Making one panel visually heavier than the other unless the slide is intentionally advocating a decision.
- ❌ Long paragraph text inside each side; this pattern works best with short, parallel bullet statements.
- ❌ Putting clip paths or masks on non-image elements for fancy panel reveals; use simple rects, paths, gradients, and opacity instead.

## Composition notes
- Keep the split exact or near-exact 50/50; the center line is the visual argument.
- Place icons in the upper third and content cards in the lower half so the audience reads “meaning” before “details.”
- Use white typography throughout for maximum contrast, with subtle translucent overlays to add depth without harming readability.
- Maintain parallel wording and similar bullet counts on both sides to preserve the feeling of a fair decision panel.