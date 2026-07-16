# SVG Recipe — Wavy Image Panel Divider

## Visual mechanism
A full-height photo panel is cropped into a custom wavy shape on the right side of the slide, replacing the standard straight vertical divider with a premium editorial curve. Two offset copies of the same wave sit behind the photo as branded blue and gold accent ribbons, creating depth and motion while leaving a clean white content area for title text.

## SVG primitives needed
- 1× `<rect>` for the white slide background
- 3× large `<path>` shapes for the layered wavy panel silhouettes: rear blue accent, middle gold accent, and subtle shadow
- 1× `<clipPath>` with a `<path>` for cropping the photo into the front wavy panel
- 1× `<image>` clipped to the wavy panel shape for the upright hero photo
- 1× front `<path>` overlay with a translucent gradient to darken the photo edge and improve contrast
- 2× `<linearGradient>` fills for premium blue/gold accent depth and photo vignette overlay
- 1× `<filter>` with `feOffset`, `feGaussianBlur`, and `feMerge` for a soft panel shadow
- Multiple `<text>` elements with explicit `width` attributes for title, subtitle, metadata, and small metric labels
- 2× small `<circle>` / `<rect>` elements for minimal executive-slide UI accents

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="blueAccent" x1="720" y1="0" x2="1040" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#0B4EA2"/>
      <stop offset="0.55" stop-color="#1C75CF"/>
      <stop offset="1" stop-color="#39A3FF"/>
    </linearGradient>

    <linearGradient id="goldAccent" x1="780" y1="0" x2="980" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFE17A"/>
      <stop offset="0.48" stop-color="#FFC000"/>
      <stop offset="1" stop-color="#F29A00"/>
    </linearGradient>

    <linearGradient id="photoEdgeShade" x1="760" y1="360" x2="1280" y2="360" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#061B33" stop-opacity="0.38"/>
      <stop offset="0.38" stop-color="#061B33" stop-opacity="0.10"/>
      <stop offset="1" stop-color="#061B33" stop-opacity="0.00"/>
    </linearGradient>

    <filter id="panelShadow" x="-20%" y="-10%" width="140%" height="120%">
      <feOffset dx="-12" dy="0" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="wavePhotoClip">
      <path d="M858 0 L1280 0 L1280 720 L806 720
               C870 645 872 570 820 494
               C761 407 768 318 842 256
               C915 195 905 74 858 0 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <!-- Rear accent ribbon -->
  <path d="M760 0 L1280 0 L1280 720 L708 720
           C778 648 786 574 738 500
           C681 414 692 322 770 254
           C847 188 824 72 760 0 Z"
        fill="url(#blueAccent)"/>

  <!-- Middle accent ribbon -->
  <path d="M812 0 L1280 0 L1280 720 L758 720
           C826 642 832 574 784 498
           C728 410 735 320 812 256
           C890 191 872 76 812 0 Z"
        fill="url(#goldAccent)"/>

  <!-- Soft shadow cast by the front photo panel -->
  <path d="M858 0 L1280 0 L1280 720 L806 720
           C870 645 872 570 820 494
           C761 407 768 318 842 256
           C915 195 905 74 858 0 Z"
        fill="#000000" opacity="0.16" filter="url(#panelShadow)"/>

  <!-- Upright image, cropped by the wavy divider -->
  <image x="650" y="0" width="700" height="720"
         href="https://images.unsplash.com/photo-1497366754035-f200968a6e72?w=1400&amp;auto=format&amp;fit=crop"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#wavePhotoClip)"/>

  <!-- Editable gradient wash over the photo shape for contrast and polish -->
  <path d="M858 0 L1280 0 L1280 720 L806 720
           C870 645 872 570 820 494
           C761 407 768 318 842 256
           C915 195 905 74 858 0 Z"
        fill="url(#photoEdgeShade)"/>

  <!-- Left content block -->
  <text x="92" y="122" width="520"
        font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600"
        letter-spacing="3" fill="#1C75CF">BUSINESS SERVICE</text>

  <text x="88" y="220" width="640"
        font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="700"
        fill="#2B2F33">
    <tspan x="88" dy="0">商务服务</tspan>
    <tspan x="88" dy="72">对接方案</tspan>
  </text>

  <rect x="92" y="324" width="92" height="6" rx="3" fill="#FFC000"/>
  <rect x="194" y="324" width="220" height="6" rx="3" fill="#E8EEF5"/>

  <text x="92" y="382" width="560"
        font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="400"
        fill="#4B5563">可行性报告 · 2026</text>

  <text x="92" y="438" width="590"
        font-family="Segoe UI, Microsoft YaHei" font-size="18"
        fill="#6B7280">
    <tspan x="92" dy="0">以流程协同、资源整合与客户体验为核心，</tspan>
    <tspan x="92" dy="30">构建可复制、可量化、可持续的服务增长模型。</tspan>
  </text>

  <!-- Small data-card accents to connect the divider with chart/data usage -->
  <rect x="92" y="535" width="164" height="72" rx="18" fill="#F5F8FC"/>
  <circle cx="122" cy="571" r="14" fill="#1C75CF"/>
  <text x="150" y="563" width="90"
        font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600"
        fill="#6B7280">效率提升</text>
  <text x="150" y="590" width="90"
        font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700"
        fill="#2B2F33">32%</text>

  <rect x="278" y="535" width="164" height="72" rx="18" fill="#F5F8FC"/>
  <circle cx="308" cy="571" r="14" fill="#FFC000"/>
  <text x="336" y="563" width="90"
        font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600"
        fill="#6B7280">周期缩短</text>
  <text x="336" y="590" width="90"
        font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700"
        fill="#2B2F33">18天</text>

  <text x="92" y="664" width="360"
        font-family="Segoe UI, Microsoft YaHei" font-size="14"
        fill="#9CA3AF">Prepared for Executive Review</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to create the wavy photo edge; use `<clipPath>` applied directly to the `<image>`.
- ❌ Do not apply `clip-path` to accent `<path>` or `<rect>` elements; only the photo needs clipping.
- ❌ Do not rely on rotated image fills as in PowerPoint preset shapes; in SVG, keep the image upright and crop it with a custom path.
- ❌ Do not make the divider a simple vertical rectangle; the premium effect depends on the S-like wave and layered offsets.
- ❌ Do not use `<use>` to duplicate the wavy path; repeat the path data explicitly for PowerPoint-safe editability.

## Composition notes
- Keep the left 55–65% of the slide mostly white for title, subtitle, and executive summary text.
- The photo panel should occupy the right 35–45% of the canvas and run full height for maximum contrast against the clean content area.
- Offset the blue and gold paths slightly left of the photo path so they appear as layered ribbons along the wavy boundary.
- Use strong corporate colors sparingly: one dominant blue ribbon, one warm gold accent, and neutral dark-gray typography.