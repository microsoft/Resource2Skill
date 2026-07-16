# SVG Recipe — automated_image_to_palette_harmony_7d8c4144

## Visual mechanism
A dominant hero photograph owns one side of the slide, while the opposite panel borrows its darkest extracted color for the background and its lightest extracted color for typography. Small accent chips and subtle gradients echo secondary extracted tones so the whole composition feels algorithmically matched to the image.

## SVG primitives needed
- 1× `<image>` for the full-height hero photo, cropped to the left panel
- 1× `<clipPath>` with `<rect>` for the hero image crop
- 2× `<linearGradient>` for the image-edge darkening and content-panel color depth
- 1× `<filter id="softShadow">` applied to accent cards/chips for premium depth
- 1× `<filter id="titleGlow">` applied to the large title for subtle contrast polish
- 3× `<rect>` for the main content panel, the translucent seam overlay, and the small eyebrow label
- 4× `<circle>` for extracted palette swatches
- 2× `<path>` for organic decorative color echoes behind the copy
- 4× `<text>` blocks with explicit `width` for eyebrow, title, subtitle, and palette labels
- 1× `<line>` for a thin divider/accent rule

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="heroCrop">
      <rect x="0" y="0" width="545" height="720" rx="0"/>
    </clipPath>

    <!-- Colors represent values extracted from the hero image:
         deep navy #29394E, dusk teal #4B6874, flower coral #D98574, warm cream #F7F0E8 -->
    <linearGradient id="panelDepth" x1="545" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#29394E"/>
      <stop offset="58%" stop-color="#243246"/>
      <stop offset="100%" stop-color="#172335"/>
    </linearGradient>

    <linearGradient id="imageFade" x1="350" y1="0" x2="560" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#172335" stop-opacity="0.55"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10" result="offset"/>
      <feGaussianBlur in="offset" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="titleGlow" x="-5%" y="-10%" width="110%" height="130%">
      <feGaussianBlur stdDeviation="1.2" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Hero photo: choose an image with visible darks, lights, and one memorable accent hue -->
  <image
    href="https://images.unsplash.com/photo-1563212896-185585b14144?auto=format&amp;fit=crop&amp;w=1200&amp;q=85"
    xlink:href="https://images.unsplash.com/photo-1563212896-185585b14144?auto=format&amp;fit=crop&amp;w=1200&amp;q=85"
    x="0" y="0" width="545" height="720"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#heroCrop)"/>

  <!-- Dark edge overlay unifies the image with the extracted-color panel -->
  <rect x="340" y="0" width="220" height="720" fill="url(#imageFade)"/>

  <!-- Main text panel: darkest extracted image color -->
  <rect x="545" y="0" width="735" height="720" fill="url(#panelDepth)"/>

  <!-- Organic color echoes from secondary image tones -->
  <path d="M1124 74 C1208 93 1262 152 1252 228 C1241 309 1152 336 1082 303 C1018 273 988 210 1013 150 C1035 98 1074 62 1124 74 Z"
        fill="#4B6874" opacity="0.26"/>
  <path d="M1067 555 C1156 510 1231 539 1253 600 C1276 663 1214 711 1138 715 C1064 719 1004 684 1008 631 C1010 598 1034 571 1067 555 Z"
        fill="#D98574" opacity="0.16"/>

  <!-- Eyebrow pill -->
  <rect x="640" y="106" width="226" height="36" rx="18" fill="#F7F0E8" opacity="0.12"/>
  <text x="664" y="130" width="190"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="700"
        letter-spacing="2.5" fill="#F7F0E8">
    IMAGE-LED PALETTE
  </text>

  <!-- Main typography: lightest extracted image color -->
  <text x="638" y="236" width="520"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="66" font-weight="800"
        letter-spacing="-1.8" fill="#F7F0E8"
        filter="url(#titleGlow)">
    <tspan x="638" dy="0">LIFE IS LIKE</tspan>
    <tspan x="638" dy="76">SUMMER</tspan>
    <tspan x="638" dy="76" fill="#F2C6B8">FLOWERS</tspan>
  </text>

  <line x1="642" y1="438" x2="760" y2="438" stroke="#D98574" stroke-width="4" stroke-linecap="round"/>

  <text x="640" y="488" width="505"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="26" font-weight="400"
        line-height="1.35" fill="#F7F0E8" opacity="0.88">
    <tspan x="640" dy="0">Let life be beautiful like summer flowers</tspan>
    <tspan x="640" dy="36">and death like autumn leaves.</tspan>
  </text>

  <!-- Extracted palette strip -->
  <rect x="640" y="590" width="390" height="70" rx="22" fill="#0F1A2A" opacity="0.28" filter="url(#softShadow)"/>
  <circle cx="686" cy="625" r="18" fill="#29394E" stroke="#F7F0E8" stroke-opacity="0.25" stroke-width="1"/>
  <circle cx="739" cy="625" r="18" fill="#4B6874" stroke="#F7F0E8" stroke-opacity="0.25" stroke-width="1"/>
  <circle cx="792" cy="625" r="18" fill="#D98574" stroke="#F7F0E8" stroke-opacity="0.25" stroke-width="1"/>
  <circle cx="845" cy="625" r="18" fill="#F7F0E8" stroke="#F7F0E8" stroke-opacity="0.25" stroke-width="1"/>

  <text x="890" y="618" width="120"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="700"
        letter-spacing="1.4" fill="#F7F0E8" opacity="0.68">
    EXTRACTED
    <tspan x="890" dy="18">FROM IMAGE</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Expecting SVG to calculate the palette at render time; extract or choose the colors before generating the SVG, then write them as literal hex values.
- ❌ Using arbitrary brand colors that do not appear in the image; the effect depends on visible repetition between photo, panel, type, and accents.
- ❌ Placing `clip-path` on decorative rectangles or paths; use clipping only on the `<image>` crop.
- ❌ Low-contrast text colors selected only because they are “dominant”; always choose a light/dark pair with strong luminance separation.
- ❌ Overloading the text panel with many colors; use one dark panel color, one light text color, and one restrained accent.

## Composition notes
- Keep the hero image at roughly 40–45% slide width and let the text panel occupy the remaining 55–60% for an executive title-slide feel.
- Use the darkest extracted color as the panel base; add a very subtle gradient with a neighboring dark tone so the panel does not look flat.
- Reserve the brightest extracted color for the main text, and use one warmer or more saturated extracted color for emphasis words, dividers, or palette chips.
- Maintain generous left padding inside the text panel, around 90–110 px from the image seam, so the composition feels calm rather than crowded.