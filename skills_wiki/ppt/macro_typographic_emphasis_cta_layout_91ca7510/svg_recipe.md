# SVG Recipe — Macro Typographic Emphasis & CTA Layout

## Visual mechanism
A high-impact title card built from exaggerated italic typography, a saturated accent banner, and a tightly cropped editorial photo that occupies the right half of the slide. The layout reads like a premium video thumbnail or keynote ending slide: the left side delivers the message in oversized stacked words, while the lower accent geometry provides a clear call-to-action path.

## SVG primitives needed
- 1× `<rect>` for the full-slide base background
- 1× `<linearGradient>` for the soft white-to-photo-side background transition
- 1× `<clipPath>` with `<rect>` for the right-side editorial photo crop
- 1× `<image>` for the presenter / speaker photo, clipped to the right half
- 2× translucent `<rect>` overlays for photo darkening and left-edge fade control
- 5× `<text>` blocks for the stacked macro headline
- 1× `<rect>` for the saturated blue emphasis banner
- 1× `<text>` for the white text inside the banner
- 2× `<path>` down-arrow CTA shapes
- 2× `<text>` labels inside the CTA arrows
- 1× `<text>` for the final URL / contact line
- 1× `<filter id="softShadow">` applied to the blue banner and CTA arrows
- 1× `<filter id="textLift">` applied subtly to the largest hero word

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="stageWash" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="42%" stop-color="#fbfbf8"/>
      <stop offset="58%" stop-color="#edf0f1"/>
      <stop offset="100%" stop-color="#dce2e8"/>
    </linearGradient>

    <linearGradient id="photoEdgeFade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.96"/>
      <stop offset="22%" stop-color="#ffffff" stop-opacity="0.62"/>
      <stop offset="54%" stop-color="#ffffff" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="blueBannerFill" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#075ebd"/>
      <stop offset="100%" stop-color="#0c6fd6"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="160%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="textLift" x="-10%" y="-10%" width="120%" height="130%">
      <feOffset dx="0" dy="4"/>
      <feGaussianBlur stdDeviation="4"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="rightPhotoCrop">
      <rect x="560" y="0" width="720" height="720"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#stageWash)"/>

  <image
    x="510" y="-30" width="820" height="780"
    href="https://images.example.com/editorial-presenter-office-cropped-shoulders-no-visible-face.jpg"
    clip-path="url(#rightPhotoCrop)"
    preserveAspectRatio="xMidYMid slice"/>

  <rect x="560" y="0" width="720" height="720" fill="#07111e" opacity="0.18"/>
  <rect x="470" y="0" width="310" height="720" fill="url(#photoEdgeFade)"/>

  <text x="56" y="170" width="500"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="104" font-weight="900" font-style="italic"
        letter-spacing="1" fill="#050505">HOW TO</text>

  <text x="108" y="348" width="470"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="178" font-weight="900" font-style="italic"
        letter-spacing="-5" fill="#0867c9"
        filter="url(#textLift)">END</text>

  <text x="154" y="453" width="330"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="92" font-weight="900" font-style="italic"
        letter-spacing="-1" fill="#050505">YOUR</text>

  <rect x="0" y="490" width="594" height="100" fill="url(#blueBannerFill)" filter="url(#softShadow)"/>

  <text x="46" y="568" width="520"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="64" font-weight="900" font-style="italic"
        letter-spacing="3" fill="#ffffff">PRESENTATION</text>

  <path d="M745 520 L835 520 L835 582 L868 582 L790 660 L712 582 L745 582 Z"
        fill="#0867c9" filter="url(#softShadow)"/>
  <text x="728" y="560" width="124"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="800"
        text-anchor="middle" fill="#ffffff">
    <tspan x="790" dy="0">FOLLOW</tspan>
    <tspan x="790" dy="22">US</tspan>
  </text>

  <path d="M1005 520 L1095 520 L1095 582 L1128 582 L1050 660 L972 582 L1005 582 Z"
        fill="#0867c9" filter="url(#softShadow)"/>
  <text x="988" y="560" width="124"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="800"
        text-anchor="middle" fill="#ffffff">
    <tspan x="1050" dy="0">MORE</tspan>
    <tspan x="1050" dy="22">INFO</tspan>
  </text>

  <text x="610" y="704" width="610"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="28" font-weight="700"
        text-anchor="middle" fill="#26313c"
        letter-spacing="0.5">www.expertacademy.be</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to fade the photo; use a gradient-filled `<rect>` overlay instead.
- ❌ Do not put `clip-path` on text, paths, or rectangles; only clip the `<image>` crop.
- ❌ Do not use `<textPath>` for curved emphasis text; keep the macro typography as editable `<text>`.
- ❌ Do not use `marker-end` for CTA arrows; build arrows as editable `<path>` shapes.
- ❌ Do not overfill the left side with icons or bullets; the effect depends on brutal typographic simplicity.

## Composition notes
- Keep the headline block on the left 45–50% of the canvas; the right half is reserved for the editorial photo and atmosphere.
- Make the hero word dramatically larger than all other text, ideally 1.6–2× the height of the surrounding words.
- Use one saturated accent color repeatedly: hero word, banner, and CTA arrows should all share the same blue family.
- Let the blue banner break the left edge of the slide; this creates a thumbnail-like punch and prevents the layout from feeling too polite.