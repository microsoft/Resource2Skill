# SVG Recipe — Brutalist Portfolio Hero

## Visual mechanism
A giant, cropped wordmark sits behind a thick-framed web-like viewport, creating brutal scale contrast. Inside the viewport, tiny grid-aligned metadata, a centered media card, oversized title typography, and a floating dark profile pill create a premium portfolio homepage freeze-frame.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 1× `<linearGradient>` and 1× `<radialGradient>` for the blue-black atmospheric backdrop
- 1× oversized `<text>` for the cropped rear wordmark
- 1× `<rect>` for the main off-white browser/portfolio viewport
- 1× `<filter id="panelShadow">` applied to the main viewport
- 6× `<text>` for top metadata labels and values
- 1× pill-shaped `<rect>` plus 1× `<text>` for the top CTA
- 1× clipped `<image>` for the central portfolio media card
- 1× `<clipPath>` with rounded rect for the media image crop
- 1× `<rect>` overlay card inside the media image
- Multiple small `<rect>` and `<text>` elements for miniature slide/UI details inside the media card
- 4× micro `<text>` labels around the hero title
- 1× massive `<text>` for the brutalist title
- 1× floating pill `<rect>` with shadow for the profile widget
- 1× small rounded avatar `<rect>` with abstract gradient fill, avoiding facial detail
- 1× hamburger/menu icon made from `<line>` elements

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="720" x2="1280" y2="0">
      <stop offset="0" stop-color="#020205"/>
      <stop offset="0.36" stop-color="#07162f"/>
      <stop offset="0.65" stop-color="#087fc2"/>
      <stop offset="1" stop-color="#c8f0ff"/>
    </linearGradient>
    <radialGradient id="blueBloom" cx="72%" cy="12%" r="70%">
      <stop offset="0" stop-color="#8fe5ff" stop-opacity="0.75"/>
      <stop offset="0.42" stop-color="#0877bd" stop-opacity="0.34"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="avatarGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#f4f4f5"/>
      <stop offset="0.5" stop-color="#b9a58f"/>
      <stop offset="1" stop-color="#7f6f61"/>
    </linearGradient>
    <filter id="panelShadow" x="-8%" y="-8%" width="116%" height="116%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softShadow" x="-15%" y="-25%" width="130%" height="160%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="7"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <clipPath id="mediaClip">
      <rect x="482" y="228" width="312" height="176" rx="5"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#blueBloom)"/>

  <text x="17" y="161" width="1245" font-family="Segoe UI, Arial Black, sans-serif" font-size="190" font-weight="900" fill="#ffffff" letter-spacing="-16">AWWWARDS</text>

  <rect x="168" y="114" width="944" height="560" rx="12" fill="#f4f4f5" stroke="#18181b" stroke-width="10" filter="url(#panelShadow)"/>

  <text x="195" y="145" width="160" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" font-weight="700" fill="#000000">US Based</text>
  <text x="195" y="164" width="160" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="10" fill="#7a7a82">Working globally</text>
  <text x="421" y="145" width="160" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" font-weight="700" fill="#000000">Building at</text>
  <text x="421" y="164" width="160" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="10" fill="#7a7a82">Trackstack</text>
  <text x="650" y="145" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" font-weight="700" fill="#000000">Freelance availability</text>
  <text x="650" y="164" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="10" fill="#7a7a82">July 2025</text>

  <rect x="994" y="134" width="91" height="33" rx="16.5" fill="#18181b"/>
  <text x="1011" y="155" width="58" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="10" font-weight="700" fill="#ffffff">Get in touch</text>

  <image x="482" y="228" width="312" height="176" clip-path="url(#mediaClip)" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/abstract-pastel-glass-portfolio-render.jpg"/>
  <rect x="508" y="250" width="256" height="132" rx="3" fill="#eeeeef"/>
  <rect x="562" y="307" width="18" height="18" fill="#111111"/>
  <rect x="584" y="324" width="13" height="13" fill="#e9461e"/>
  <rect x="601" y="319" width="21" height="21" fill="#f4a23a"/>
  <rect x="626" y="308" width="15" height="15" fill="#111111"/>
  <rect x="647" y="298" width="17" height="17" fill="#111111"/>
  <rect x="666" y="284" width="14" height="14" fill="#111111"/>
  <rect x="685" y="281" width="16" height="16" fill="#e9461e"/>
  <rect x="704" y="286" width="14" height="14" fill="#d9d9d9"/>
  <rect x="720" y="296" width="18" height="18" fill="#111111"/>
  <text x="735" y="379" width="30" font-family="Segoe UI, sans-serif" font-size="25" font-weight="500" fill="#111111">75</text>
  <text x="512" y="377" width="52" font-family="Segoe UI, sans-serif" font-size="4.5" fill="#111111">MINIMAL SLIDE</text>

  <text x="195" y="462" width="40" font-family="Segoe UI, sans-serif" font-size="11" font-weight="800" fill="#000000">A</text>
  <text x="610" y="462" width="80" font-family="Segoe UI, sans-serif" font-size="10" font-weight="800" fill="#000000">SERIOUSLY</text>
  <text x="1050" y="462" width="46" font-family="Segoe UI, sans-serif" font-size="10" font-weight="800" fill="#000000">GOOD</text>

  <text x="190" y="551" width="900" font-family="Segoe UI, Arial Black, Microsoft YaHei, sans-serif" font-size="104" font-weight="900" fill="#18181b" letter-spacing="-7">DESIGN ENGINEER</text>

  <rect x="439" y="599" width="405" height="57" rx="10" fill="#18181b" filter="url(#softShadow)"/>
  <rect x="452" y="607" width="37" height="43" rx="6" fill="url(#avatarGrad)"/>
  <ellipse cx="470.5" cy="622" rx="12" ry="10" fill="#d8d2ca" opacity="0.55"/>
  <rect x="458" y="629" width="25" height="13" rx="6" fill="#9b8b7b" opacity="0.45"/>
  <text x="501" y="622" width="160" font-family="Segoe UI, sans-serif" font-size="10" font-weight="800" fill="#ffffff">JASON ZUBIATE</text>
  <text x="501" y="640" width="275" font-family="Segoe UI, sans-serif" font-size="7.5" fill="#b6b6b8" letter-spacing=".9">TEXT JS ENTHUSIAST, CREATIVE DESIGN ENGINEER, AWWWARDS</text>
  <line x1="810" y1="623" x2="822" y2="623" stroke="#ffffff" stroke-width="1.4"/>
  <line x1="810" y1="627" x2="822" y2="627" stroke="#ffffff" stroke-width="1.4"/>
  <line x1="810" y1="631" x2="822" y2="631" stroke="#ffffff" stroke-width="1.4"/>

  <text x="195" y="651" width="100" font-family="Segoe UI, sans-serif" font-size="12" fill="#000000">↓ Scroll for</text>
  <text x="1025" y="651" width="75" font-family="Segoe UI, sans-serif" font-size="12" fill="#000000">cool sh*t ↓</text>
</svg>
```

## Avoid in this skill
- ❌ Using a normal title size; the technique depends on extreme typography that bleeds, crops, or collides with other layers.
- ❌ Centering every element evenly; the composition should feel like a captured web viewport with deliberate overlap and edge pressure.
- ❌ Replacing the floating profile pill with a flat footer bar; the shadowed overlap is what creates the Z-axis depth.
- ❌ Applying `clip-path` to non-image elements for rounded cards; use rounded `<rect>` shapes directly and reserve clip paths for image crops.
- ❌ Using a detailed human face avatar if privacy is a concern; use an abstract gradient avatar or non-identifying silhouette instead.

## Composition notes
- Keep the large rear wordmark partly hidden by the foreground viewport so it reads as environmental branding, not body content.
- Place the off-white viewport slightly lower than the rear wordmark, with a thick black stroke to create brutalist contrast.
- Reserve the center for a small media showcase; the scale gap between the tiny media card and huge title is intentional.
- Use black, zinc gray, and off-white for most elements, with the blue background bloom as the main atmospheric color accent.