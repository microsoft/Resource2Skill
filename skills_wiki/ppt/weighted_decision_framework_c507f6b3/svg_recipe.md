# SVG Recipe — Weighted Decision Framework

## Visual mechanism
A balance scale acts as the central metaphor for evaluating trade-offs: weighted “Pros” and “Cons” cards sit on opposite trays, with a subtle tilt showing which side currently carries more influence. Supporting data pods beneath the scale quantify the decision and add executive-summary context.

## SVG primitives needed
- 1× `<rect>` full-slide background with a pale executive gradient
- 2× `<linearGradient>` for premium blue/teal cards and subtle background shading
- 1× `<filter id="softShadow">` applied to cards, data pods, and tray bowls
- 1× `<filter id="glow">` applied to the central pivot accent
- 4× `<line>` for the scale beam and suspension cables
- 6× `<rect>` for the base, stand, weighted cards, and data pods
- 5× `<path>` for the fulcrum, tray bowls, and editable thumbs up/down icons
- 5× `<circle>` / `<ellipse>` for pivot details and weight tokens
- Multiple `<text>` elements with explicit `width` attributes for labels, percentages, and summaries

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7FAFD"/>
      <stop offset="58%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#EEF5F8"/>
    </linearGradient>
    <linearGradient id="proGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0078D4"/>
      <stop offset="100%" stop-color="#005A9E"/>
    </linearGradient>
    <linearGradient id="conGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#2F8480"/>
      <stop offset="100%" stop-color="#226966"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="9"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .22 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="glow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <text x="80" y="58" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#202124">
    Weighted Decision Framework
  </text>
  <text x="82" y="92" width="690" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#667085">
    Compare strategic upside against implementation risk using a visual balance model.
  </text>

  <!-- scale base and stand -->
  <rect x="520" y="515" width="240" height="20" rx="10" fill="#202124"/>
  <path d="M560 555 L720 555 L755 588 L525 588 Z" fill="#202124"/>
  <rect x="626" y="300" width="28" height="222" rx="14" fill="#202124"/>
  <path d="M640 250 L700 330 L580 330 Z" fill="#202124"/>
  <circle cx="640" cy="284" r="28" fill="#FFFFFF" filter="url(#glow)" opacity="0.9"/>
  <circle cx="640" cy="284" r="17" fill="#202124"/>

  <!-- tilted beam and cables -->
  <line x1="294" y1="318" x2="986" y2="258" stroke="#202124" stroke-width="14" stroke-linecap="round"/>
  <line x1="334" y1="314" x2="334" y2="430" stroke="#202124" stroke-width="4" stroke-linecap="round"/>
  <line x1="474" y1="302" x2="474" y2="430" stroke="#202124" stroke-width="4" stroke-linecap="round"/>
  <line x1="806" y1="274" x2="806" y2="398" stroke="#202124" stroke-width="4" stroke-linecap="round"/>
  <line x1="946" y1="262" x2="946" y2="398" stroke="#202124" stroke-width="4" stroke-linecap="round"/>

  <!-- tray bowls -->
  <path d="M262 430 C292 470, 520 470, 548 430 Z" fill="#FFFFFF" stroke="#202124" stroke-width="6" filter="url(#softShadow)"/>
  <path d="M734 398 C764 438, 992 438, 1020 398 Z" fill="#FFFFFF" stroke="#202124" stroke-width="6" filter="url(#softShadow)"/>

  <!-- pro card -->
  <rect x="154" y="284" width="400" height="126" rx="24" fill="url(#proGrad)" filter="url(#softShadow)"/>
  <circle cx="210" cy="347" r="34" fill="#FFFFFF" opacity="0.18"/>
  <path d="M198 362 L198 337 L211 337 L226 312 C231 304, 243 309, 240 319 L235 337 L258 337 C266 337, 270 344, 266 350 C270 355, 268 363, 261 366 C263 374, 257 381, 248 381 L224 381 C216 381, 211 377, 207 371 L203 362 Z" fill="#FFFFFF"/>
  <text x="270" y="333" width="235" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF" letter-spacing="1.5">
    PROS
  </text>
  <text x="270" y="366" width="245" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#FFFFFF">
    Revenue expansion
  </text>
  <text x="270" y="390" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#DDEEFF">
    Higher retention and cross-sell potential
  </text>

  <!-- con card -->
  <rect x="728" y="252" width="400" height="126" rx="24" fill="url(#conGrad)" filter="url(#softShadow)"/>
  <circle cx="784" cy="315" r="34" fill="#FFFFFF" opacity="0.18"/>
  <path d="M773 299 L773 324 L786 324 L801 349 C806 357, 818 352, 815 342 L810 324 L833 324 C841 324, 845 317, 841 311 C845 306, 843 298, 836 295 C838 287, 832 280, 823 280 L799 280 C791 280, 786 284, 782 290 L778 299 Z" fill="#FFFFFF"/>
  <text x="844" y="301" width="235" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF" letter-spacing="1.5">
    CONS
  </text>
  <text x="844" y="334" width="245" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#FFFFFF">
    Delivery complexity
  </text>
  <text x="844" y="358" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#DDF2F0">
    Integration cost and adoption risk
  </text>

  <!-- visual weight tokens -->
  <ellipse cx="318" cy="428" rx="28" ry="10" fill="#0078D4" opacity="0.95"/>
  <ellipse cx="388" cy="428" rx="28" ry="10" fill="#0078D4" opacity="0.75"/>
  <ellipse cx="458" cy="428" rx="28" ry="10" fill="#0078D4" opacity="0.55"/>
  <ellipse cx="850" cy="396" rx="28" ry="10" fill="#2F8480" opacity="0.85"/>
  <ellipse cx="920" cy="396" rx="28" ry="10" fill="#2F8480" opacity="0.55"/>

  <!-- data pods -->
  <rect x="126" y="578" width="460" height="86" rx="22" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="160" y="612" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#0078D4">
    62%
  </text>
  <text x="280" y="604" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#404040">
    Weighted upside score
  </text>
  <text x="280" y="630" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#667085">
    Strong customer impact and measurable growth contribution.
  </text>

  <rect x="694" y="578" width="460" height="86" rx="22" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="728" y="612" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#2F8480">
    38%
  </text>
  <text x="848" y="604" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#404040">
    Weighted risk score
  </text>
  <text x="848" y="630" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#667085">
    Main concerns are sequencing, migration effort, and enablement.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<marker>` arrowheads for scale indicators; if you need arrows, draw them as editable `<line>` plus triangle `<path>` shapes.
- ❌ Do not use `<mask>` to create tray shadows or cutouts; use editable paths, gradients, and supported blur/offset filters instead.
- ❌ Do not place `filter` on `<line>` elements for the beam or cables; apply shadows only to rects, paths, circles, ellipses, or text.
- ❌ Do not make the comparison a plain two-column table; the scale metaphor is the visual mechanism and should remain dominant.

## Composition notes
- Keep the scale centered and large, occupying roughly 70–80% of the slide width; the metaphor should read instantly from the back of a room.
- Place the heavier side slightly lower and reinforce weight with extra tokens, stronger color, or a larger score.
- Use saturated but corporate colors for the cards, while keeping the scale itself near-black for high contrast.
- Reserve the lower third for compact data pods; these should summarize evidence, not compete with the main scale.