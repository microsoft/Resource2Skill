# SVG Recipe — Media Showcase with Caption

## Visual mechanism
A cinematic 16:9 media panel dominates the slide, treated like a premium poster frame with rounded-corner clipping, depth shadow, and a subtle play affordance. A small brand pill anchors the top-left while a translucent caption card overlays the media near the lower edge without competing with the image.

## SVG primitives needed
- 1× `<rect>` full-slide background with gradient fill
- 2× decorative `<path>` blobs for ambient brand color and visual depth
- 1× `<clipPath>` with rounded `<rect>` to crop the media image
- 1× `<image>` for the central photo/video poster/screenshot
- 2× `<rect>` for the media frame base and hairline border
- 1× `<rect>` translucent caption card over the media
- 1× `<circle>` plus 1× `<path>` for an optional video play button
- 1× `<rect>` brand label pill
- 4× `<text>` elements for brand, eyebrow, caption headline, and caption detail
- 2× `<linearGradient>` fills for background and glass caption
- 1× `<radialGradient>` for soft color bloom
- 2× `<filter>` definitions for card shadow and soft glow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#07111F"/>
      <stop offset="0.52" stop-color="#0E1B2E"/>
      <stop offset="1" stop-color="#111827"/>
    </linearGradient>

    <linearGradient id="captionGlass" x1="350" y1="470" x2="930" y2="620" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.92"/>
      <stop offset="1" stop-color="#EAF2FF" stop-opacity="0.76"/>
    </linearGradient>

    <radialGradient id="blueBloom" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#4CC9F0" stop-opacity="0.48"/>
      <stop offset="1" stop-color="#4CC9F0" stop-opacity="0"/>
    </radialGradient>

    <filter id="frameShadow" x="-12%" y="-12%" width="124%" height="130%">
      <feOffset dx="0" dy="24" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="24" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-35%" y="-35%" width="170%" height="170%">
      <feGaussianBlur stdDeviation="28"/>
    </filter>

    <clipPath id="mediaClip">
      <rect x="166" y="118" width="948" height="533" rx="34" ry="34"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <path d="M-90,95 C40,10 178,34 260,126 C342,218 303,347 176,374 C45,402 -80,311 -122,202 C-149,134 -132,121 -90,95 Z"
        fill="url(#blueBloom)" filter="url(#softGlow)" opacity="0.8"/>
  <path d="M1110,34 C1228,4 1334,76 1362,184 C1390,292 1315,402 1199,398 C1082,394 1018,300 1038,195 C1051,121 1069,51 1110,34 Z"
        fill="#7C3AED" opacity="0.18" filter="url(#softGlow)"/>

  <rect x="56" y="42" width="186" height="42" rx="21" fill="#FFFFFF" opacity="0.09" stroke="#FFFFFF" stroke-opacity="0.18"/>
  <circle cx="78" cy="63" r="8" fill="#4CC9F0"/>
  <text x="96" y="69" width="128" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="600" fill="#F8FAFC" letter-spacing="1.4">ACME LABS</text>

  <rect x="146" y="98" width="988" height="573" rx="42" fill="#030712" opacity="0.85" filter="url(#frameShadow)"/>
  <image x="166" y="118" width="948" height="533"
         href="https://images.example.com/premium-product-video-poster-dark-device-interface.jpg"
         preserveAspectRatio="xMidYMid slice" clip-path="url(#mediaClip)"/>
  <rect x="166" y="118" width="948" height="533" rx="34" fill="none" stroke="#FFFFFF" stroke-opacity="0.22" stroke-width="1.5"/>

  <path d="M166,478 L166,617 C166,636 181,651 200,651 L1080,651 C1099,651 1114,636 1114,617 L1114,520 C958,566 775,590 566,579 C398,570 263,532 166,478 Z"
        fill="#020617" opacity="0.44"/>

  <circle cx="640" cy="365" r="43" fill="#FFFFFF" opacity="0.22" stroke="#FFFFFF" stroke-opacity="0.42" stroke-width="1.4"/>
  <circle cx="640" cy="365" r="31" fill="#FFFFFF" opacity="0.86"/>
  <path d="M633,349 L633,381 L660,365 Z" fill="#0F172A"/>

  <rect x="226" y="505" width="610" height="104" rx="24" fill="url(#captionGlass)" filter="url(#frameShadow)"/>
  <rect x="246" y="525" width="78" height="24" rx="12" fill="#0F172A" opacity="0.9"/>
  <text x="262" y="542" width="48" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="11" font-weight="700" fill="#FFFFFF" letter-spacing="1.2">VIDEO</text>

  <text x="346" y="548" width="430" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="23" font-weight="700" fill="#0F172A">Seamless device mockup integration</text>
  <text x="346" y="579" width="430" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="400" fill="#475569">A short walkthrough showing how the new workflow connects product screens, motion assets, and launch storytelling.</text>

  <text x="1000" y="84" width="170" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="600" fill="#CBD5E1" text-anchor="end" letter-spacing="1.6">SECTION 03</text>
</svg>
```

## Avoid in this skill
- ❌ Using `<mask>` to create the video fade or glass overlay; use normal translucent shapes and gradients instead.
- ❌ Applying `clip-path` to caption cards, scrims, or decorative shapes; clipping is reliable here only on the `<image>`.
- ❌ Building the caption as `<foreignObject>` HTML; use native SVG `<text>` with explicit `width`.
- ❌ Using `marker-end` or path markers for play controls; draw the play triangle as a simple filled `<path>`.
- ❌ Relying on an actual embedded video object; represent video with a poster image plus editable play-button geometry.

## Composition notes
- Keep the media panel large, around 74–80% of slide width, centered horizontally with generous dark margins.
- Place the brand identifier in the top-left safe area; keep it small so it reads as provenance, not a title.
- Put the caption card over the lower-left or lower-center of the image, covering less than one quarter of the media height.
- Use a restrained palette: dark cinematic background, white/glass caption, and one vivid brand accent for the pill or glow.