# SVG Recipe — Glassmorphism Reveal Panel

## Visual mechanism
A full-bleed or framed hero photo is duplicated: the sharp photo remains visible, while a second copy is clipped to a rounded rectangle and heavily blurred/tinted to mimic frosted glass. Semi-transparent gradients, a white edge stroke, and crisp typography make the panel feel like a floating premium UI card over the image.

## SVG primitives needed
- 2× `<image>` for the same hero photograph: one sharp visible photo, one blurred duplicate clipped to the glass panel
- 1× `<image>` for a full-slide blurred/dimmed ambient background behind the framed photo
- 1× `<clipPath>` with rounded `<rect>` for the main photo crop
- 1× `<clipPath>` with rounded `<rect>` for the glass panel crop
- 3× `<rect>` for the outer black device/photo frame, subtle inner photo dark overlay, and glass tint layers
- 2× `<linearGradient>` for the glass shine and edge/tint depth
- 2× `<filter>`: one Gaussian blur for the duplicate image, one soft shadow for the floating panel/frame
- 1× `<line>` or narrow `<rect>` for the bold divider rule inside the panel
- 3× `<text>` blocks with explicit `width` for the title, body copy, and optional eyebrow/accent label

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="photoClip">
      <rect x="148" y="78" width="984" height="564" rx="16" ry="16"/>
    </clipPath>

    <clipPath id="glassClip">
      <rect x="822" y="180" width="286" height="360" rx="46" ry="46"/>
    </clipPath>

    <linearGradient id="glassTint" x1="822" y1="180" x2="1108" y2="540" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.34"/>
      <stop offset="0.42" stop-color="#FFFFFF" stop-opacity="0.13"/>
      <stop offset="1" stop-color="#1B2430" stop-opacity="0.34"/>
    </linearGradient>

    <linearGradient id="glassEdge" x1="822" y1="180" x2="1108" y2="540" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.88"/>
      <stop offset="0.48" stop-color="#FFFFFF" stop-opacity="0.28"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0.58"/>
    </linearGradient>

    <linearGradient id="photoVignette" x1="148" y1="78" x2="1132" y2="642" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#000000" stop-opacity="0.08"/>
      <stop offset="0.55" stop-color="#000000" stop-opacity="0"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0.52"/>
    </linearGradient>

    <filter id="heavyBlur" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="20"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Ambient full-slide backdrop: same image enlarged, blurred, and darkened -->
  <image x="-40" y="-30" width="1360" height="780"
         href="https://source.unsplash.com/1600x900/?steam-train,forest,dark"
         preserveAspectRatio="xMidYMid slice"
         opacity="0.72"
         filter="url(#heavyBlur)"/>
  <rect x="0" y="0" width="1280" height="720" fill="#111820" opacity="0.62"/>

  <!-- Floating black photo frame -->
  <rect x="140" y="76" width="1000" height="568" rx="24" ry="24"
        fill="#050607" filter="url(#softShadow)"/>
  <rect x="148" y="84" width="984" height="548" rx="16" ry="16"
        fill="#0A0B0D"/>

  <!-- Main sharp hero image -->
  <image x="148" y="84" width="984" height="548"
         href="https://source.unsplash.com/1600x900/?steam-train,forest,dark"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#photoClip)"/>
  <rect x="148" y="84" width="984" height="548" rx="16" ry="16"
        fill="url(#photoVignette)" opacity="0.72"/>

  <!-- Small camera/notch detail to echo the premium device-frame look -->
  <path d="M570 84 L710 84 C704 99 700 102 684 102 L596 102 C580 102 576 99 570 84 Z"
        fill="#050607"/>
  <rect x="622" y="87" width="32" height="4" rx="2" fill="#1E2428" opacity="0.8"/>
  <circle cx="670" cy="89" r="3" fill="#10171D"/>

  <!-- Frosted glass: duplicate of same photo, clipped to panel and blurred -->
  <image x="148" y="84" width="984" height="548"
         href="https://source.unsplash.com/1600x900/?steam-train,forest,dark"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#glassClip)"
         filter="url(#heavyBlur)"
         opacity="0.96"/>

  <!-- Glass tint, shine, and edge -->
  <rect x="822" y="180" width="286" height="360" rx="46" ry="46"
        fill="#18202A" opacity="0.28"/>
  <rect x="822" y="180" width="286" height="360" rx="46" ry="46"
        fill="url(#glassTint)"/>
  <path d="M846 185 C930 178 1042 184 1088 238 C1052 208 985 205 913 220 C873 228 846 230 830 216 C834 202 839 192 846 185 Z"
        fill="#FFFFFF" opacity="0.13"/>
  <rect x="822" y="180" width="286" height="360" rx="46" ry="46"
        fill="none" stroke="url(#glassEdge)" stroke-width="1.4"/>

  <!-- Text hierarchy inside glass panel -->
  <text x="840" y="228" width="236"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="38" font-weight="700" letter-spacing="2.2"
        fill="#FFFFFF">
    <tspan x="840" dy="0">JOURNEY</tspan>
    <tspan x="840" dy="45">THROUGH</tspan>
    <tspan x="840" dy="45">WOODS</tspan>
  </text>

  <rect x="838" y="365" width="142" height="11" rx="1" fill="#FFFFFF"/>

  <text x="840" y="423" width="230"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="21" font-weight="700"
        fill="#FFFFFF">
    <tspan x="840" dy="0">Embracing Nature in</tspan>
    <tspan x="840" dy="24">its glory, a train</tspan>
    <tspan x="840" dy="24">whistled to alert the</tspan>
    <tspan x="840" dy="24">forest's life!</tspan>
  </text>

  <text x="840" y="506" width="220"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" font-weight="600" letter-spacing="2"
        fill="#B9F4FF" opacity="0.72">
    FROSTED REVEAL PANEL
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use CSS `backdrop-filter`; PowerPoint will not recreate it as editable objects.
- ❌ Do not apply `clip-path` to the glass tint rectangles; clip only the duplicated `<image>` and use rounded `<rect>` shapes for overlays.
- ❌ Do not rely on `<mask>` to carve the panel or vignette; use rounded rectangles, gradients, and clipped images instead.
- ❌ Do not place text directly over the busy photo without the frosted layer; the whole value of the technique is smoothing visual noise.
- ❌ Do not forget explicit `width` on every `<text>` element; otherwise the PowerPoint text boxes may render unpredictably.

## Composition notes
- Place the glass panel off-center, usually on the right third, so the main subject of the photo remains visible on the left or center.
- Keep generous inner padding inside the panel: roughly 18–28 px from the panel edge to the text block.
- Use a bright white title and divider rule for contrast, but let the panel itself stay translucent so background color still bleeds through.
- The effect works best with dark, moody, high-detail photography because the blur/tint creates a dramatic premium contrast.