# SVG Recipe — Dynamic Mosaic Profile Morph

## Visual mechanism
A large rounded hero portrait anchors the current profile while smaller portraits orbit around it as context; on the next slide, keep the same element IDs and swap their positions/sizes so PowerPoint Morph animates the selected person into the hero slot. The left-side biography and accent color update to match the active portrait, while a pale oversized team watermark gives the right side depth.

## SVG primitives needed
- 1× `<rect>` for the off-white slide background
- 1× `<rect>` for the large floating white content card
- 9× `<image>` for rounded portrait tiles: one hero, eight supporting mosaic portraits
- 9× `<clipPath>` with rounded `<rect>` crops applied only to portrait images
- 1× `<filter id="cardShadow">` for the floating card shadow
- 1× `<filter id="photoShadow">` for hero/supporting portrait lift
- 1× `<linearGradient>` for a subtle card surface highlight
- 1× `<path>` for a small abstract agency mark
- 1× `<line>` for the biography accent rule
- Multiple `<text>` elements with explicit `width` for agency label, hero name, description, tile captions, and watermark

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="cardSheen" x1="120" y1="110" x2="1160" y2="650" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#ffffff"/>
      <stop offset="0.72" stop-color="#fbfbf8"/>
      <stop offset="1" stop-color="#f2f4ef"/>
    </linearGradient>

    <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="photoShadow" x="-15%" y="-15%" width="130%" height="140%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="8"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="clipHero"><rect x="796" y="258" width="196" height="250" rx="14"/></clipPath>
    <clipPath id="clipP2"><rect x="640" y="319" width="152" height="102" rx="9"/></clipPath>
    <clipPath id="clipP3"><rect x="750" y="190" width="110" height="74" rx="7"/></clipPath>
    <clipPath id="clipP4"><rect x="1015" y="257" width="82" height="102" rx="8"/></clipPath>
    <clipPath id="clipP5"><rect x="895" y="205" width="88" height="60" rx="6"/></clipPath>
    <clipPath id="clipP6"><rect x="680" y="448" width="110" height="72" rx="7"/></clipPath>
    <clipPath id="clipP7"><rect x="1020" y="426" width="86" height="94" rx="8"/></clipPath>
    <clipPath id="clipP8"><rect x="708" y="276" width="82" height="54" rx="6"/></clipPath>
    <clipPath id="clipP9"><rect x="1018" y="365" width="62" height="54" rx="6"/></clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#f4f5ef"/>
  <text x="-12" y="164" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="70" font-weight="800" fill="#dbe2d5" opacity="0.62">Sophia</text>
  <text x="-12" y="244" width="540" font-family="Segoe UI, Microsoft YaHei" font-size="70" font-weight="800" fill="#dbe2d5" opacity="0.62">White</text>

  <rect x="126" y="116" width="1028" height="536" rx="14" fill="url(#cardSheen)" filter="url(#cardShadow)"/>

  <path d="M210 184 C216 174 226 174 230 184 C224 194 217 201 210 210 C204 204 203 194 210 184 Z
           M236 184 C242 174 252 174 256 184 C250 194 243 201 236 210 C230 204 229 194 236 184 Z"
        fill="#d8d8d5"/>
  <text x="204" y="246" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="800" letter-spacing="4" fill="#191919">SOME COOL AGENCY</text>

  <text x="204" y="332" width="310" font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="800" fill="#80a967">
    <tspan x="204" dy="0">Sophia</tspan>
    <tspan x="204" dy="68">White</tspan>
  </text>
  <line x1="206" y1="435" x2="484" y2="435" stroke="#80a967" stroke-width="4"/>
  <text x="206" y="494" width="340" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#232323">
    <tspan x="206" dy="0">Brand strategist with a golden</tspan>
    <tspan x="206" dy="34">touch. Transforms startups into</tspan>
    <tspan x="206" dy="34">household names.</tspan>
  </text>

  <text x="716" y="637" width="390" font-family="Segoe UI, Microsoft YaHei" font-size="52" font-weight="800" letter-spacing="6" fill="none" stroke="#dfe3dd" stroke-width="1.5" opacity="0.7">OUR TEAM</text>
  <text x="1080" y="570" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="210" font-weight="900" fill="#e8ebe5" opacity="0.72" transform="rotate(-90 1080 570)">TEAM</text>

  <image id="Photo_2" x="640" y="319" width="152" height="102" clip-path="url(#clipP2)" filter="url(#photoShadow)"
         href="https://images.example.com/profile-mosaic/blonde-strategist-yellow-background.jpg"/>
  <image id="Photo_3" x="750" y="190" width="110" height="74" clip-path="url(#clipP3)" filter="url(#photoShadow)"
         href="https://images.example.com/profile-mosaic/designer-red-sweater-pink-background.jpg"/>
  <image id="Photo_5" x="895" y="205" width="88" height="60" clip-path="url(#clipP5)" filter="url(#photoShadow)"
         href="https://images.example.com/profile-mosaic/producer-yellow-jacket-violet-background.jpg"/>
  <image id="Photo_8" x="708" y="276" width="82" height="54" clip-path="url(#clipP8)" filter="url(#photoShadow)"
         href="https://images.example.com/profile-mosaic/copywriter-orange-sweater-lavender-background.jpg"/>

  <image id="Photo_1" x="796" y="258" width="196" height="250" clip-path="url(#clipHero)" filter="url(#photoShadow)"
         href="https://images.example.com/profile-mosaic/sophia-white-orange-top-green-background.jpg"/>
  <rect x="796" y="258" width="196" height="250" rx="14" fill="none" stroke="#ffffff" stroke-width="2" opacity="0.75"/>

  <image id="Photo_4" x="1015" y="257" width="82" height="102" clip-path="url(#clipP4)" filter="url(#photoShadow)"
         href="https://images.example.com/profile-mosaic/engineer-purple-sweater-neutral-background.jpg"/>
  <image id="Photo_9" x="1018" y="365" width="62" height="54" clip-path="url(#clipP9)" filter="url(#photoShadow)"
         href="https://images.example.com/profile-mosaic/pr-lead-orange-jacket-cyan-background.jpg"/>
  <image id="Photo_6" x="680" y="448" width="110" height="72" clip-path="url(#clipP6)" filter="url(#photoShadow)"
         href="https://images.example.com/profile-mosaic/art-director-orange-dress-blue-background.jpg"/>
  <image id="Photo_7" x="1020" y="426" width="86" height="94" clip-path="url(#clipP7)" filter="url(#photoShadow)"
         href="https://images.example.com/profile-mosaic/analyst-yellow-shirt-magenta-background.jpg"/>

  <circle cx="1125" cy="270" r="39" fill="#f1f2ee"/>
  <circle cx="1125" cy="270" r="21" fill="#ffffff"/>
  <text x="744" y="544" width="350" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" letter-spacing="2" fill="#9aa39a">DUPLICATE SLIDE • MOVE SAME PHOTO IDS • APPLY MORPH</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to round portraits; use `<clipPath>` on each `<image>` instead.
- ❌ Do not convert portraits into flat colored rectangles only; the technique depends on photographic mosaic energy.
- ❌ Do not rename or delete profile image objects between Morph states; keep stable IDs such as `Photo_1`, `Photo_2`, etc.
- ❌ Do not apply clip paths to `<rect>` or `<g>` wrappers; PPT-Master only preserves clipping reliably on `<image>`.
- ❌ Do not use `<use>` to duplicate portrait cards; duplicate the explicit `<image>` and clip definitions.

## Composition notes
- Reserve the left 40% of the card for biography text; keep it clean, left-aligned, and color-matched to the active hero portrait.
- Use the right 60% as an organic mosaic field: one dominant portrait near center-right, with smaller rounded portraits staggered above, below, and to the far right.
- Keep the background watermark very pale and partially behind the mosaic so it adds depth without competing with faces.
- For the Morph sequence, duplicate the slide, promote a different `Photo_*` into the hero clip size/position, demote the previous hero into a small slot, and update the name/accent color.