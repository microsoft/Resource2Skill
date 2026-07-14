# SVG Recipe — Tutorial Screenshot

## Visual mechanism
A single oversized screenshot is staged like a premium product demo: centered in a rounded browser frame with soft shadow, subtle gradient background, and only a compact headline/caption so the visual example dominates the slide.

## SVG primitives needed
- 1× `<rect>` full-slide background with a restrained gradient fill
- 2× decorative `<path>` blobs for soft ambient color behind the screenshot
- 1× `<rect>` browser/window shell with rounded corners and drop shadow
- 1× `<rect>` browser chrome bar for the top toolbar area
- 3× `<circle>` browser control dots
- 1× `<rect>` address/search bar inside the browser chrome
- 1× `<clipPath>` with a `<path>` to crop the screenshot image into the browser content area
- 1× `<image>` for the dominant tutorial screenshot, clipped to the content pane
- 3× `<rect>` translucent annotation cards over the screenshot
- 2× `<line>` callout leader strokes
- 2× `<circle>` callout target rings
- 4× `<text>` elements for headline, small label, URL/chrome text, and caption; every text element includes explicit `width`
- 2× `<filter>` definitions: one shadow for the browser frame and one blur/glow for ambient decorative blobs
- 3× `<linearGradient>` definitions for background, browser chrome, and accent fills

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0" stop-color="#F7FAFF"/>
      <stop offset="0.55" stop-color="#EEF4FF"/>
      <stop offset="1" stop-color="#F8FBFF"/>
    </linearGradient>

    <linearGradient id="chromeGrad" x1="110" y1="86" x2="1170" y2="126">
      <stop offset="0" stop-color="#FFFFFF"/>
      <stop offset="1" stop-color="#F0F4FA"/>
    </linearGradient>

    <linearGradient id="accentGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#2F7CFF"/>
      <stop offset="1" stop-color="#7B61FF"/>
    </linearGradient>

    <filter id="windowShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="22"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="34"/>
    </filter>

    <clipPath id="screenshotClip">
      <path d="M110 126 H1170 V598 Q1170 624 1144 624 H136 Q110 624 110 598 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <path d="M96 192 C180 72 360 78 432 172 C506 270 394 376 230 356 C80 338 42 272 96 192 Z"
        fill="#DDEBFF" opacity="0.68" filter="url(#softGlow)"/>
  <path d="M890 546 C982 424 1168 426 1226 540 C1286 658 1112 728 958 684 C850 654 826 626 890 546 Z"
        fill="#E9DFFF" opacity="0.62" filter="url(#softGlow)"/>

  <text x="110" y="52" width="760" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="30" font-weight="700" fill="#14213D">
    Connect your workspace in under two minutes
  </text>

  <rect x="923" y="28" width="247" height="34" rx="17" fill="#FFFFFF" opacity="0.82"/>
  <rect x="931" y="36" width="86" height="18" rx="9" fill="url(#accentGrad)"/>
  <text x="1030" y="52" width="130" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="600" fill="#4A5875">
    Step 01 / Setup
  </text>

  <rect x="110" y="86" width="1060" height="538" rx="26" fill="#FFFFFF" filter="url(#windowShadow)"/>
  <rect x="110" y="86" width="1060" height="40" rx="26" fill="url(#chromeGrad)"/>
  <path d="M110 112 H1170 V126 H110 Z" fill="url(#chromeGrad)"/>

  <circle cx="137" cy="106" r="6.5" fill="#FF5F57"/>
  <circle cx="158" cy="106" r="6.5" fill="#FFBD2E"/>
  <circle cx="179" cy="106" r="6.5" fill="#28C840"/>

  <rect x="224" y="96" width="532" height="20" rx="10" fill="#E8EDF5"/>
  <text x="244" y="111" width="480" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="11" fill="#7B879C">
    app.example.com / onboarding / integrations
  </text>

  <image x="110" y="126" width="1060" height="498" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#screenshotClip)"
         href="https://images.example.com/tutorial-screenshot-product-dashboard-16x9.png"/>

  <rect x="110" y="126" width="1060" height="498" fill="none" stroke="#D7DFEC" stroke-width="1"/>

  <rect x="175" y="184" width="214" height="102" rx="16" fill="#FFFFFF" opacity="0.92"
        stroke="#DCE5F2" stroke-width="1"/>
  <rect x="197" y="208" width="116" height="12" rx="6" fill="#AFC0D8"/>
  <rect x="197" y="234" width="154" height="9" rx="4.5" fill="#D9E2EE"/>
  <rect x="197" y="254" width="92" height="9" rx="4.5" fill="#D9E2EE"/>

  <rect x="782" y="184" width="296" height="78" rx="18" fill="#14213D" opacity="0.88"/>
  <text x="808" y="217" width="238" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" fill="#FFFFFF">
    Select the integration tile
  </text>
  <text x="808" y="242" width="236" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12.5" fill="#C8D4E8">
    This callout sits directly on the screenshot.
  </text>

  <line x1="825" y1="262" x2="708" y2="340" stroke="#2F7CFF" stroke-width="3"
        stroke-linecap="round" stroke-dasharray="0 0"/>
  <circle cx="696" cy="348" r="17" fill="none" stroke="#2F7CFF" stroke-width="4"/>
  <circle cx="696" cy="348" r="6" fill="#2F7CFF"/>

  <rect x="702" y="493" width="282" height="66" rx="16" fill="#FFFFFF" opacity="0.94"
        stroke="#DCE5F2" stroke-width="1"/>
  <text x="726" y="519" width="232" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" fill="#17233C">
    Confirm permissions
  </text>
  <text x="726" y="541" width="230" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12.5" fill="#5E6B83">
    Keep overlays sparse and purposeful.
  </text>

  <line x1="800" y1="493" x2="744" y2="445" stroke="#7B61FF" stroke-width="3"
        stroke-linecap="round"/>
  <circle cx="735" cy="438" r="14" fill="none" stroke="#7B61FF" stroke-width="4"/>

  <text x="110" y="670" width="960" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" fill="#526078">
    Use this layout when the screenshot is the evidence: one large visual, one short instruction, and light annotations only where they clarify the action.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not build the screenshot from many tiny SVG rectangles; use a real `<image>` so the slide feels like an authentic tutorial capture.
- ❌ Do not place dense paragraphs beside the screenshot; this layout works because the image owns nearly the entire canvas.
- ❌ Do not use `<mask>` to fade the screenshot edges; use a clipped `<image>` inside a rounded browser frame instead.
- ❌ Do not use `marker-end` arrows on paths for callouts; if arrows are required, draw leaders with `<line>` and use circles or small paths as endpoints.
- ❌ Do not apply `clip-path` to groups or rectangles for the screenshot crop; apply the `clip-path` directly to the `<image>`.

## Composition notes
- Keep the screenshot between roughly 80–85% of slide width and 70–75% of slide height, centered slightly below the headline.
- Reserve the top 70–80 px for a short headline or step label; avoid competing title blocks.
- Use shadow and browser chrome to make the screenshot feel like a tangible object floating above the slide.
- Add only 1–2 annotation cards, ideally inside the screenshot bounds, so the tutorial remains visual rather than text-heavy.