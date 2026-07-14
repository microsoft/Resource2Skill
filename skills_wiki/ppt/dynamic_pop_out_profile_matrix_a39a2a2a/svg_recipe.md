# SVG Recipe — Dynamic Pop-out Profile Matrix

## Visual mechanism
A row of profile cards is built from layered, curved geometric bases, with transparent-background portraits placed above the card tops so heads and shoulders break the frame. Large sweeping blue background waves unify the matrix and make the white cards feel like they are floating in a premium keynote layout.

## SVG primitives needed
- 1× `<rect>` for the clean slide background
- 2× large `<path>` shapes for the top-left and bottom-right sweeping blue background waves
- 4× teal `<path>` pedestal shapes behind each portrait, shaped like rounded “D” blocks
- 4× white `<path>` card bodies with angled lower-right corners
- 4× teal `<path>` header ribbons with a curved diagonal cut
- 4× transparent-background `<image>` portraits placed out-of-bounds above the cards
- 1× `<filter id="softShadow">` applied to card bodies and portrait pedestals
- 1× `<filter id="portraitLift">` applied to portraits for subtle depth
- 2× `<linearGradient>` definitions for the background and teal accent depth
- Multiple `<text>` elements with explicit `width` attributes for names, roles, and descriptions

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgFade" x1="0" y1="0" x2="0" y2="720">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F3FBFE"/>
    </linearGradient>
    <linearGradient id="tealDepth" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#11A6CF"/>
      <stop offset="100%" stop-color="#048DB7"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="9" result="off"/>
      <feGaussianBlur in="off" stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="portraitLift" x="-15%" y="-15%" width="130%" height="130%">
      <feOffset dx="0" dy="5" result="poff"/>
      <feGaussianBlur in="poff" stdDeviation="4" result="pblur"/>
      <feMerge>
        <feMergeNode in="pblur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgFade)"/>

  <path d="M0,0 L255,0 C160,25 67,61 0,111 Z" fill="#0B9BC1"/>
  <path d="M0,582 C230,630 505,625 760,558 C955,507 1112,421 1280,249 L1280,720 L0,720 Z" fill="#0799C3"/>
  <path d="M870,603 C1025,560 1160,495 1280,388 L1280,720 L870,720 Z" fill="#088EB8" opacity="0.55"/>

  <text x="78" y="70" width="510" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#243746">Core Project Leadership</text>
  <text x="80" y="105" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#6B7C86">Dynamic pop-out profile matrix for executive team introductions</text>

  <!-- Profile 1 -->
  <path d="M119,211 L319,211 L319,319 C319,354 291,376 254,376 L119,376 Z" fill="url(#tealDepth)" filter="url(#softShadow)"/>
  <image href="https://images.example.com/transparent-cutout-businesswoman-arms-crossed.png" x="105" y="78" width="230" height="305" preserveAspectRatio="xMidYMax meet" filter="url(#portraitLift)"/>
  <path d="M119,418 L319,386 L319,645 L281,677 L119,677 Z" fill="#FFFFFF" filter="url(#softShadow)"/>
  <path d="M119,386 L319,386 L319,403 C265,428 203,448 119,452 Z" fill="url(#tealDepth)"/>
  <text x="148" y="424" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#FFFFFF">高雅琪</text>
  <text x="153" y="485" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#1F2E36">
    <tspan x="153" dy="0">对团队管理和领导力有着</tspan>
    <tspan x="153" dy="22">独到的见解。作为一名企</tspan>
    <tspan x="153" dy="22">业执行总监，她领导团队</tspan>
    <tspan x="153" dy="22">实现了多个重要项目的成</tspan>
    <tspan x="153" dy="22">功交付，并在行业内树立</tspan>
    <tspan x="153" dy="22">了良好的声誉。</tspan>
  </text>
  <text x="153" y="655" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#078DB4">Gao Ya Qi</text>

  <!-- Profile 2 -->
  <path d="M405,211 L605,211 L605,319 C605,354 577,376 540,376 L405,376 Z" fill="url(#tealDepth)" filter="url(#softShadow)"/>
  <image href="https://images.example.com/transparent-cutout-businesswoman-pointing-white-shirt.png" x="383" y="76" width="245" height="305" preserveAspectRatio="xMidYMax meet" filter="url(#portraitLift)"/>
  <path d="M405,418 L605,386 L605,645 L567,677 L405,677 Z" fill="#FFFFFF" filter="url(#softShadow)"/>
  <path d="M405,386 L605,386 L605,403 C551,428 489,448 405,452 Z" fill="url(#tealDepth)"/>
  <text x="435" y="424" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#FFFFFF">张梦婷</text>
  <text x="439" y="485" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#1F2E36">
    <tspan x="439" dy="0">擅长在商务圈建立广泛的</tspan>
    <tspan x="439" dy="22">社交网络。她拥有卓越的</tspan>
    <tspan x="439" dy="22">沟通技巧，能够与不同背</tspan>
    <tspan x="439" dy="22">景和文化的人建立紧密的</tspan>
    <tspan x="439" dy="22">合作关系。她曾在国际商</tspan>
    <tspan x="439" dy="22">务展会上成功促成项目。</tspan>
  </text>
  <text x="439" y="655" width="145" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#078DB4">Zhang Meng Ting</text>

  <!-- Profile 3 -->
  <path d="M691,211 L891,211 L891,319 C891,354 863,376 826,376 L691,376 Z" fill="url(#tealDepth)" filter="url(#softShadow)"/>
  <image href="https://images.example.com/transparent-cutout-businessman-arms-crossed-blue-shirt.png" x="684" y="80" width="220" height="303" preserveAspectRatio="xMidYMax meet" filter="url(#portraitLift)"/>
  <path d="M691,418 L891,386 L891,645 L853,677 L691,677 Z" fill="#FFFFFF" filter="url(#softShadow)"/>
  <path d="M691,386 L891,386 L891,403 C837,428 775,448 691,452 Z" fill="url(#tealDepth)"/>
  <text x="721" y="424" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#FFFFFF">林宇航</text>
  <text x="725" y="485" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#1F2E36">
    <tspan x="725" dy="0">对企业战略和财务管理有</tspan>
    <tspan x="725" dy="22">着深刻的见解。作为一名</tspan>
    <tspan x="725" dy="22">资深顾问，他曾为多家公</tspan>
    <tspan x="725" dy="22">司提供战略规划和风险管</tspan>
    <tspan x="725" dy="22">理方面的咨询服务，帮助</tspan>
    <tspan x="725" dy="22">客户在竞争中取得成功。</tspan>
  </text>
  <text x="725" y="655" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#078DB4">Lin Yu Hang</text>

  <!-- Profile 4 -->
  <path d="M977,211 L1177,211 L1177,319 C1177,354 1149,376 1112,376 L977,376 Z" fill="url(#tealDepth)" filter="url(#softShadow)"/>
  <image href="https://images.example.com/transparent-cutout-businesswoman-holding-clipboard.png" x="952" y="82" width="245" height="302" preserveAspectRatio="xMidYMax meet" filter="url(#portraitLift)"/>
  <path d="M977,418 L1177,386 L1177,645 L1139,677 L977,677 Z" fill="#FFFFFF" filter="url(#softShadow)"/>
  <path d="M977,386 L1177,386 L1177,403 C1123,428 1061,448 977,452 Z" fill="url(#tealDepth)"/>
  <text x="1007" y="424" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#FFFFFF">陈雅婷</text>
  <text x="1011" y="485" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#1F2E36">
    <tspan x="1011" dy="0">拥有丰富的市场营销经验。</tspan>
    <tspan x="1011" dy="22">她在国际知名公司担任高级</tspan>
    <tspan x="1011" dy="22">市场营销经理，曾策划并成</tspan>
    <tspan x="1011" dy="22">功推出多个备受瞩目的产品。</tspan>
    <tspan x="1011" dy="22">她善于捕捉市场趋势，通过</tspan>
    <tspan x="1011" dy="22">精准策略打造市场领导者。</tspan>
  </text>
  <text x="1011" y="655" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#078DB4">Chen Ya Ting</text>
</svg>
```

## Avoid in this skill
- ❌ Do not clip the portrait into the card; the signature effect depends on the image breaking outside the geometric frame.
- ❌ Do not use `<mask>` or clip paths on card shapes to fake cutouts; draw the curved card geometry directly with `<path>`.
- ❌ Do not flatten the whole card into a single bitmap; keep card bodies, ribbons, text, and background waves editable.
- ❌ Avoid plain rectangular photo grids; the visual premium comes from asymmetric paths, overlap, shadows, and generous white space.
- ❌ Do not place the portrait behind the teal pedestal, or the pop-out illusion will disappear.

## Composition notes
- Keep portraits in the upper-middle band, extending well above the card tops; the card body begins around the lower half of the slide.
- Use four evenly spaced columns with consistent x positions, but vary portrait silhouettes slightly for a natural team-gallery rhythm.
- Reserve the top-left for a compact title/subtitle; the matrix itself should remain the dominant visual focus.
- Maintain a restrained palette: white cards, dark charcoal copy, and one strong teal/blue accent repeated in waves, pedestals, headers, and name highlights.