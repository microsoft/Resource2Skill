# SVG Recipe — Modern Pitch Deck 'Rule of Three' Layout

## Visual mechanism
An asymmetric editorial slide: a dominant edge-to-edge hero photo anchors the left 40%, while a spacious white content field on the right carries one large focused headline and three memorable feature columns. The “rule of three” is reinforced with numbered micro-cards, crisp grid alignment, restrained accent color, and generous negative space.

## SVG primitives needed
- 1× `<rect>` for the full white slide background
- 1× `<image>` for the left-side hero photograph
- 1× `<clipPath>` with `<rect>` for keeping the hero image locked to the left panel
- 2× `<rect>` overlays on the photo for premium contrast and caption legibility
- 1× `<path>` for a subtle organic accent blob behind the headline
- 3× `<rect>` for the rule-of-three content cards
- 3× `<rect>` for small accent bars at the top of each card
- 3× `<circle>` for numbered feature badges
- 2× `<line>` for delicate vertical separators between columns
- Multiple `<text>` elements with explicit `width` attributes for headline, subtitle, labels, numbers, and body copy
- 3× `<linearGradient>` definitions for photo shading, accent treatment, and soft card fill
- 2× `<filter>` definitions for soft card shadow and faint accent glow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="heroClip">
      <rect x="0" y="0" width="512" height="720" rx="0"/>
    </clipPath>

    <linearGradient id="photoShade" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0F172A" stop-opacity="0.10"/>
      <stop offset="58%" stop-color="#0F172A" stop-opacity="0.06"/>
      <stop offset="100%" stop-color="#0F172A" stop-opacity="0.46"/>
    </linearGradient>

    <linearGradient id="accentGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FF6B6B"/>
      <stop offset="100%" stop-color="#7C3AED"/>
    </linearGradient>

    <linearGradient id="cardFill" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F8FAFC"/>
    </linearGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="12"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <image x="0" y="0" width="512" height="720"
         href="https://images.example.com/premium-startup-team-strategy-room-vertical.jpg"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#heroClip)"/>
  <rect x="0" y="0" width="512" height="720" fill="url(#photoShade)"/>
  <rect x="44" y="568" width="330" height="84" rx="20" fill="#0F172A" opacity="0.54"/>

  <text x="70" y="604" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF" letter-spacing="1.6">
    PRODUCT MOMENTUM
  </text>
  <text x="70" y="631" width="285" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#CBD5E1">
    Built for teams moving from insight to execution.
  </text>

  <path d="M965 52 C1036 22 1144 53 1177 118 C1211 184 1164 253 1086 259 C1008 265 944 232 924 170 C906 114 913 74 965 52 Z"
        fill="#FF6B6B" opacity="0.10" filter="url(#softGlow)"/>

  <text x="604" y="92" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FF6B6B" letter-spacing="2.4">
    THE OPERATING MODEL
  </text>

  <text x="604" y="169" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="800" fill="#1E293B">
    <tspan x="604" dy="0">A Single Focused</tspan>
    <tspan x="604" dy="64">Message.</tspan>
  </text>

  <text x="606" y="265" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="19" fill="#64748B">
    <tspan x="606" dy="0">Clarity drives action. Our framework reduces noise,</tspan>
    <tspan x="606" dy="29">aligns teams, and turns strategy into measurable growth.</tspan>
  </text>

  <rect x="604" y="334" width="72" height="5" rx="2.5" fill="url(#accentGrad)"/>

  <line x1="812" y1="392" x2="812" y2="642" stroke="#E2E8F0" stroke-width="1"/>
  <line x1="1019" y1="392" x2="1019" y2="642" stroke="#E2E8F0" stroke-width="1"/>

  <rect x="604" y="386" width="180" height="258" rx="24" fill="url(#cardFill)" stroke="#E5E7EB" stroke-width="1" filter="url(#cardShadow)"/>
  <rect x="632" y="414" width="44" height="5" rx="2.5" fill="#FF6B6B"/>
  <circle cx="656" cy="462" r="25" fill="#FFF1F2" stroke="#FF6B6B" stroke-width="1.5"/>
  <text x="642" y="471" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#FF6B6B">01</text>
  <text x="632" y="522" width="124" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#1E293B">
    Discovery
  </text>
  <text x="632" y="557" width="124" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#64748B">
    <tspan x="632" dy="0">Uncover hidden</tspan>
    <tspan x="632" dy="22">value by mapping</tspan>
    <tspan x="632" dy="22">market behavior.</tspan>
  </text>

  <rect x="831" y="386" width="180" height="258" rx="24" fill="url(#cardFill)" stroke="#E5E7EB" stroke-width="1" filter="url(#cardShadow)"/>
  <rect x="859" y="414" width="44" height="5" rx="2.5" fill="#7C3AED"/>
  <circle cx="883" cy="462" r="25" fill="#F5F3FF" stroke="#7C3AED" stroke-width="1.5"/>
  <text x="869" y="471" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#7C3AED">02</text>
  <text x="859" y="522" width="124" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#1E293B">
    Strategy
  </text>
  <text x="859" y="557" width="124" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#64748B">
    <tspan x="859" dy="0">Build resilient</tspan>
    <tspan x="859" dy="22">systems that scale</tspan>
    <tspan x="859" dy="22">with the market.</tspan>
  </text>

  <rect x="1058" y="386" width="180" height="258" rx="24" fill="url(#cardFill)" stroke="#E5E7EB" stroke-width="1" filter="url(#cardShadow)"/>
  <rect x="1086" y="414" width="44" height="5" rx="2.5" fill="#0EA5E9"/>
  <circle cx="1110" cy="462" r="25" fill="#E0F2FE" stroke="#0EA5E9" stroke-width="1.5"/>
  <text x="1096" y="471" width="30" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#0EA5E9">03</text>
  <text x="1086" y="522" width="124" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#1E293B">
    Execution
  </text>
  <text x="1086" y="557" width="124" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#64748B">
    <tspan x="1086" dy="0">Launch precise</tspan>
    <tspan x="1086" dy="22">solutions with speed,</tspan>
    <tspan x="1086" dy="22">quality, and focus.</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Filling the slide with six or more bullets; the technique depends on one message plus exactly three supporting ideas.
- ❌ Centering everything symmetrically; the premium look comes from the asymmetric 40/60 split.
- ❌ Low-contrast photo backgrounds behind body text; keep the image on one side and text on a clean white field.
- ❌ Decorative animations, arrows, or connector-heavy diagrams; this layout should feel editorial and static.
- ❌ Applying `clip-path` to cards or text; only clip the `<image>` if the hero needs a controlled crop.

## Composition notes
- Keep the hero image flush to the left edge, roughly 40% of the canvas width; let it act as the emotional anchor.
- Reserve the upper-right quadrant for the large headline and subtitle, with at least 70–90 px of breathing room from the image boundary.
- Place the three columns in the lower-right half, aligned to a consistent baseline and separated by subtle gutters.
- Use one vivid accent family sparingly: small bars, number badges, and one short headline label are enough.