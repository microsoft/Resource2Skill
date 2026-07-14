# SVG Recipe — Editorial Magazine Cutout Profile

## Visual mechanism
Create depth by placing a transparent cutout portrait over the edge of a clean editorial text card, so the subject breaks the geometric frame. High-contrast typography, small magazine metadata, and an accent color pulled from the subject make the slide feel like a premium sports/profile feature.

## SVG primitives needed
- 7× `<rect>` for the neutral canvas, main white editorial card, top accent stripe, and stat panels
- 4× `<path>` for dynamic red editorial slashes, corner accents, and the soft contact shadow behind the cutout
- 1× `<circle>` for a subtle radial halo behind the subject
- 1× `<image>` for the transparent PNG cutout subject overlapping the card
- 2× `<line>` for thin magazine divider rules
- 10× `<text>` with explicit `width` for headline, subhead, body copy, metadata, vertical label, and stats
- 2× `<linearGradient>` for background wash and red accent treatment
- 1× `<radialGradient>` for the subject halo
- 2× `<filter>` using blur/offset/merge for the card shadow and subject contact shadow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f7f7f9"/>
      <stop offset="100%" stop-color="#ececf0"/>
    </linearGradient>

    <linearGradient id="redGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ff4b3e"/>
      <stop offset="100%" stop-color="#c91521"/>
    </linearGradient>

    <radialGradient id="halo" cx="50%" cy="45%" r="60%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.95"/>
      <stop offset="55%" stop-color="#f14a4a" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#f14a4a" stop-opacity="0"/>
    </radialGradient>

    <filter id="cardShadow" x="-10%" y="-10%" width="125%" height="125%">
      <feOffset dx="0" dy="18" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feColorMatrix in="blur" type="matrix"
        values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .16 0" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softContact" x="-20%" y="-20%" width="150%" height="150%">
      <feGaussianBlur stdDeviation="16"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>
  <circle cx="270" cy="355" r="285" fill="url(#halo)"/>

  <text x="450" y="176" width="760"
        font-family="Segoe UI, Microsoft YaHei" font-size="124" font-weight="900"
        fill="#e2e2e7" opacity="0.72" letter-spacing="-5">SPRINT</text>

  <path d="M70 630 L214 95 L278 95 L132 630 Z" fill="url(#redGrad)" opacity="0.92"/>
  <path d="M250 680 L388 145 L420 145 L286 680 Z" fill="#111111" opacity="0.08"/>

  <rect x="410" y="70" width="795" height="580" rx="26" fill="#ffffff" filter="url(#cardShadow)"/>
  <rect x="410" y="70" width="795" height="9" rx="4.5" fill="url(#redGrad)"/>
  <path d="M1110 70 L1205 70 L1205 220 C1176 174 1140 128 1110 70 Z" fill="#dc2626" opacity="0.13"/>

  <line x1="642" y1="296" x2="1136" y2="296" stroke="#1f1f24" stroke-width="1.2" opacity="0.18"/>
  <line x1="642" y1="492" x2="1136" y2="492" stroke="#1f1f24" stroke-width="1.2" opacity="0.14"/>

  <path d="M92 646 C160 606 300 594 442 626 C510 642 542 666 510 686 C396 710 190 706 82 676 C52 666 56 658 92 646 Z"
        fill="#000000" opacity="0.24" filter="url(#softContact)"/>

  <image href="https://images.example.com/transparent-cutout-sprinter-red-track-suit.png"
         x="24" y="26" width="585" height="676" preserveAspectRatio="xMidYMax meet"/>

  <text x="118" y="642" width="230" transform="rotate(-90 118 642)"
        font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700"
        fill="#202024" letter-spacing="3">PROFILE  /  NO LIMITS</text>

  <text x="642" y="125" width="520"
        font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="800"
        fill="#dc2626" letter-spacing="3">EDITORIAL ATHLETE PROFILE</text>

  <text x="640" y="214" width="520"
        font-family="Segoe UI, Microsoft YaHei" font-size="78" font-weight="900"
        fill="#17171b" letter-spacing="-2">飞人归来</text>

  <text x="644" y="263" width="560"
        font-family="Segoe UI, Microsoft YaHei" font-size="31" font-weight="800"
        fill="#dc2626">苏炳添 晋级百米半决赛</text>

  <text x="642" y="340" width="500"
        font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700"
        fill="#232327">
    <tspan x="642" dy="0">亚洲纪录保持者，以强韧节奏冲破预赛压力。</tspan>
  </text>

  <text x="642" y="386" width="510"
        font-family="Segoe UI, Microsoft YaHei" font-size="16"
        fill="#5b5b63" line-height="1.45">
    <tspan x="642" dy="0">北京时间16日上午，俄勒冈田径世锦赛展开男子100米预赛。</tspan>
    <tspan x="642" dy="27">他跑出10秒15，凭借递补成绩惊险晋级半决赛。</tspan>
    <tspan x="642" dy="27">这不是一张普通人物介绍页，而是一张拥有层次、速度与焦点的杂志封面。</tspan>
  </text>

  <rect x="642" y="522" width="144" height="84" rx="18" fill="#f6f6f8" stroke="#e6e6ea"/>
  <rect x="814" y="522" width="144" height="84" rx="18" fill="#f6f6f8" stroke="#e6e6ea"/>
  <rect x="986" y="522" width="144" height="84" rx="18" fill="#f6f6f8" stroke="#e6e6ea"/>

  <text x="664" y="554" width="104"
        font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="900"
        fill="#17171b">10.15</text>
  <text x="665" y="582" width="104"
        font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700"
        fill="#7a7a82" letter-spacing="1.5">SECONDS</text>

  <text x="836" y="554" width="104"
        font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="900"
        fill="#17171b">100M</text>
  <text x="837" y="582" width="104"
        font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700"
        fill="#7a7a82" letter-spacing="1.5">EVENT</text>

  <text x="1008" y="554" width="104"
        font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="900"
        fill="#dc2626">Q</text>
  <text x="1009" y="582" width="104"
        font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700"
        fill="#7a7a82" letter-spacing="1.5">QUALIFIED</text>

  <text x="642" y="632" width="500"
        font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700"
        fill="#9a9aa2" letter-spacing="2.2">ID: CHN-100M-2022  ·  POWER &amp; PRECISION  ·  ISSUE 05</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use a full-bleed busy background photo behind the text; it destroys the clean magazine-card contrast.
- ❌ Do not use `<mask>` for the cutout. Use a real transparent PNG subject instead.
- ❌ Do not clip the person image into a rectangle; the whole point is the freeform silhouette breaking the card edge.
- ❌ Do not place the cutout behind the white card; it must visibly overlap the card boundary.
- ❌ Do not put filter shadows on `<line>` elements; use filters only on the card `<rect>` or shadow `<path>`.

## Composition notes
- Put the white editorial card on the right 60–65% of the slide, with the subject occupying the left 40–45% and overlapping the card by roughly 80–160 px.
- Reserve the card’s left edge for overlap; keep all important text starting farther right so the cutout does not cover it.
- Use one strong accent color from the clothing or brand palette, repeated in the stripe, subtitle, slash shape, and one statistic.
- Keep the canvas pale gray, not pure white, so the white card reads as a physical paper layer with depth.