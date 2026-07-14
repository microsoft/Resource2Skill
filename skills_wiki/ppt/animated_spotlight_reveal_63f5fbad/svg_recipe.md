# SVG Recipe — Animated Spotlight Reveal

## Visual mechanism
A rich background scene is covered by a dark compound-path overlay with a circular cutout, creating a “spotlight” that exposes only one area at a time. In PowerPoint, animate this overlay with a custom motion path so the hole travels between focal points, then make the overlay disappear for the full reveal.

## SVG primitives needed
- 1× `<image>` for the full-slide background content being revealed
- 1× `<clipPath>` with rounded `<rect>` for an optional inset product/UI image crop
- 1× compound `<path>` for the dark overlay: slide-sized rectangle plus circular subpath using `fill-rule="evenodd"`
- 1× `<circle>` for the luminous rim around the spotlight hole
- 1× `<circle>` with radial gradient for subtle spotlight bloom
- 1× dashed `<path>` for the visible custom motion-path guide
- 4× small `<circle>` markers for key reveal stops
- 3× `<rect>` translucent annotation cards
- Multiple `<text>` elements with explicit `width` for title, labels, and animation instructions
- 2× `<filter>` definitions: soft shadow for cards and glow for the spotlight rim
- 2× `<linearGradient>` definitions for cinematic background tint and callout cards
- 1× `<radialGradient>` for the warm light bloom inside the spotlight

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="sceneTint" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#10203A" stop-opacity="0.15"/>
      <stop offset="55%" stop-color="#0C1220" stop-opacity="0.05"/>
      <stop offset="100%" stop-color="#111827" stop-opacity="0.32"/>
    </linearGradient>

    <linearGradient id="cardFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.92"/>
      <stop offset="100%" stop-color="#DCEBFF" stop-opacity="0.84"/>
    </linearGradient>

    <radialGradient id="spotBloom" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.28"/>
      <stop offset="45%" stop-color="#FFE8A3" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="#FFE8A3" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="spotGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>

    <clipPath id="roundedScreenshot">
      <rect x="735" y="175" width="390" height="250" rx="28" ry="28"/>
    </clipPath>
  </defs>

  <!-- Revealed background scene -->
  <image href="https://images.example.com/hero-photo-modern-product-demo-control-room-dashboard.jpg"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#sceneTint)"/>

  <!-- Underlying content details that the spotlight will reveal in sequence -->
  <rect x="86" y="92" width="430" height="190" rx="30" fill="#FFFFFF" opacity="0.88" filter="url(#softShadow)"/>
  <text x="124" y="146" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#0F172A">1. Hidden insight</text>
  <text x="124" y="185" width="345" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#334155">Revenue acceleration appears first, before the audience sees the full operating context.</text>
  <path d="M124 239 C172 205, 220 265, 270 226 S365 210, 450 248" fill="none" stroke="#2563EB" stroke-width="5" stroke-linecap="round"/>

  <rect x="650" y="118" width="535" height="365" rx="36" fill="#0B1220" opacity="0.88" filter="url(#softShadow)"/>
  <image href="https://images.example.com/ui-screenshot-saas-analytics-dashboard-dark-mode.jpg"
         x="735" y="175" width="390" height="250" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#roundedScreenshot)"/>
  <text x="700" y="150" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#E0F2FE">2. Product capability</text>
  <rect x="706" y="444" width="140" height="16" rx="8" fill="#38BDF8"/>
  <rect x="866" y="444" width="190" height="16" rx="8" fill="#4ADE80"/>
  <rect x="1076" y="444" width="70" height="16" rx="8" fill="#FBBF24"/>

  <rect x="170" y="448" width="430" height="150" rx="30" fill="#111827" opacity="0.86" filter="url(#softShadow)"/>
  <text x="210" y="503" width="350" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#FFFFFF">3. Final implication</text>
  <text x="210" y="542" width="335" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#CBD5E1">The reveal ends here, then the overlay exits so the complete story lands at once.</text>

  <!-- Optional visible motion guide; hide or delete before final export if desired -->
  <path d="M285 200 C470 85, 670 125, 850 260 S1015 470, 430 520"
        fill="none" stroke="#FDE68A" stroke-width="4" stroke-linecap="round"
        stroke-dasharray="12 14" opacity="0.72"/>
  <circle cx="285" cy="200" r="10" fill="#FDE68A"/>
  <circle cx="850" cy="260" r="10" fill="#FDE68A"/>
  <circle cx="1030" cy="390" r="10" fill="#FDE68A"/>
  <circle cx="430" cy="520" r="10" fill="#FDE68A"/>

  <!-- Dark spotlight overlay: animate this single compound path in PowerPoint -->
  <path fill="#020617" opacity="0.82" fill-rule="evenodd"
        d="
        M0 0 H1280 V720 H0 Z
        M966 390
        A126 126 0 1 0 714 390
        A126 126 0 1 0 966 390
        Z"/>

  <!-- Spotlight bloom and rim aligned to the current circular hole -->
  <circle cx="840" cy="390" r="166" fill="url(#spotBloom)"/>
  <circle cx="840" cy="390" r="126" fill="none" stroke="#FFF7CC" stroke-width="4" opacity="0.82" filter="url(#spotGlow)"/>
  <circle cx="840" cy="390" r="128" fill="none" stroke="#FFFFFF" stroke-width="1.5" opacity="0.78"/>

  <!-- Presenter-facing instruction card placed above the overlay -->
  <rect x="58" y="42" width="415" height="118" rx="24" fill="url(#cardFill)" filter="url(#softShadow)"/>
  <text x="86" y="83" width="350" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="800" fill="#0F172A">Animated Spotlight Reveal</text>
  <text x="86" y="119" width="350" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#334155">Move the dark overlay along the dashed path; the transparent hole guides attention.</text>

  <rect x="830" y="560" width="360" height="96" rx="22" fill="#0F172A" opacity="0.92" filter="url(#softShadow)"/>
  <text x="858" y="598" width="305" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FDE68A">PowerPoint animation cue</text>
  <text x="858" y="628" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#E5E7EB">Apply Custom Motion Path to the overlay, then add Disappear after previous.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<mask>` or `mask="url(#...)"` to cut the spotlight hole; use a compound `<path>` with `fill-rule="evenodd"` instead.
- ❌ Do not use `<animate>` or `<animateTransform>` for the moving spotlight; create the editable overlay in SVG, then apply the motion path animation inside PowerPoint.
- ❌ Do not apply `clip-path` to the dark overlay or other non-image shapes; clipping is reliable only for `<image>` crops.
- ❌ Do not put a filter on a `<line>` for the motion path; use a dashed `<path>` or plain line without filter.
- ❌ Do not use `marker-end` on a `<path>` for arrows; if an arrow is needed, draw a small triangle `<path>` manually.

## Composition notes
- Keep the background visually rich enough to reward the reveal: product UI, map, photograph, technical diagram, or dense infographic.
- The spotlight radius should expose one narrative unit at a time, usually 18–24% of slide height.
- Place the starting spotlight over a high-curiosity detail, then travel through 2–4 focal points before the full reveal.
- Use the dashed path and yellow stop dots only as authoring guides; remove or hide them for the final cinematic version.