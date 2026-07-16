# SVG Recipe — Minimalist Geometric Device Mockups

## Visual mechanism
Build recognizable tablets, laptops, and phones from layered editable SVG primitives: rounded chassis shapes, inset screen rectangles, tiny camera/button details, and simple vector UI inside each screen. Premium polish comes from restrained gradients, soft shadows, symmetrical bezels, and overlapping devices staged like a product showcase.

## SVG primitives needed
- 1× full-slide `<rect>` for the gradient background
- 3× decorative `<circle>` / `<path>` accents for subtle keynote-style depth
- 6× large `<rect>` with `rx` for device chassis and glass screens
- 1× `<path>` for the laptop base with a shallow center lip
- 8× small `<circle>` / `<rect>` for cameras, buttons, speaker slots, trackpad, and hardware details
- 20+ small `<rect>` for editable mock SaaS UI cards, charts, navigation rails, and app panels inside screens
- 5× `<text>` labels with explicit `width` attributes for headline, subtitle, and in-screen UI labels
- 3× `<linearGradient>` for background, screen glass, and metal/device highlights
- 1× `<radialGradient>` for soft background glow
- 2× `<filter>` effects: soft device shadow and screen glow, applied only to editable shapes

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0F3F33"/>
      <stop offset="48%" stop-color="#3F9D65"/>
      <stop offset="100%" stop-color="#93C75D"/>
    </linearGradient>
    <radialGradient id="halo" cx="50%" cy="50%" r="55%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.34"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="deviceWhite" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#E9EEF0"/>
    </linearGradient>
    <linearGradient id="screenGlass" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#101820"/>
      <stop offset="62%" stop-color="#17212B"/>
      <stop offset="100%" stop-color="#04070A"/>
    </linearGradient>
    <linearGradient id="accentGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#72F1C8"/>
      <stop offset="100%" stop-color="#28A7FF"/>
    </linearGradient>
    <filter id="softShadow" x="-25%" y="-25%" width="150%" height="160%">
      <feOffset dx="0" dy="18" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="screenGlow" x="-15%" y="-15%" width="130%" height="130%">
      <feGaussianBlur stdDeviation="4"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <circle cx="995" cy="110" r="230" fill="url(#halo)" opacity="0.75"/>
  <circle cx="142" cy="620" r="185" fill="#0B2D26" opacity="0.20"/>
  <path d="M1160,560 C1215,515 1260,530 1295,590 L1295,720 L1035,720 C1065,645 1110,603 1160,560 Z" fill="#FFFFFF" opacity="0.10"/>

  <text x="72" y="74" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="44" font-weight="700" fill="#FFFFFF">
    Minimal device frames
  </text>
  <text x="74" y="118" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#DFF7E8">
    Fully editable vector mockups for SaaS demos, app reviews, and portfolio showcases.
  </text>

  <!-- Tablet mockup -->
  <rect x="108" y="178" width="250" height="382" rx="32" fill="url(#deviceWhite)" filter="url(#softShadow)"/>
  <circle cx="233" cy="203" r="5" fill="#111827"/>
  <rect x="132" y="226" width="202" height="285" rx="3" fill="url(#screenGlass)"/>
  <rect x="153" y="248" width="160" height="18" rx="9" fill="#263544"/>
  <rect x="153" y="286" width="72" height="70" rx="12" fill="url(#accentGrad)"/>
  <rect x="241" y="286" width="72" height="70" rx="12" fill="#2C3B4A"/>
  <rect x="153" y="374" width="160" height="16" rx="8" fill="#405267"/>
  <rect x="153" y="404" width="110" height="16" rx="8" fill="#304152"/>
  <rect x="153" y="434" width="137" height="16" rx="8" fill="#304152"/>
  <circle cx="233" cy="535" r="16" fill="#F8FAFC" stroke="#B8C0C7" stroke-width="2"/>
  <text x="163" y="335" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF">
    App
  </text>

  <!-- Laptop monitor -->
  <rect x="438" y="164" width="564" height="342" rx="24" fill="url(#deviceWhite)" filter="url(#softShadow)"/>
  <circle cx="720" cy="183" r="4" fill="#111827"/>
  <rect x="466" y="202" width="508" height="286" rx="4" fill="url(#screenGlass)"/>
  <rect x="490" y="226" width="92" height="238" rx="12" fill="#101923"/>
  <rect x="606" y="226" width="338" height="48" rx="14" fill="#202C38"/>
  <rect x="606" y="296" width="104" height="132" rx="16" fill="#203142"/>
  <rect x="730" y="296" width="104" height="132" rx="16" fill="#203142"/>
  <rect x="854" y="296" width="90" height="132" rx="16" fill="#203142"/>
  <rect x="624" y="320" width="66" height="12" rx="6" fill="#8BE6C9"/>
  <rect x="624" y="352" width="48" height="52" rx="8" fill="url(#accentGrad)" filter="url(#screenGlow)"/>
  <rect x="748" y="320" width="66" height="12" rx="6" fill="#8BE6C9"/>
  <rect x="748" y="350" width="66" height="14" rx="7" fill="#526A7D"/>
  <rect x="748" y="378" width="44" height="14" rx="7" fill="#526A7D"/>
  <rect x="872" y="320" width="48" height="12" rx="6" fill="#8BE6C9"/>
  <circle cx="898" cy="384" r="34" fill="none" stroke="#32C7FF" stroke-width="10"/>
  <text x="624" y="258" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#FFFFFF">
    Analytics dashboard
  </text>
  <text x="510" y="260" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#AFC1CF">
    Home
  </text>
  <text x="510" y="304" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#AFC1CF">
    Metrics
  </text>
  <path d="M388,506 L1052,506 C1078,506 1099,526 1110,548 L330,548 C341,526 362,506 388,506 Z" fill="#DDE5E8" filter="url(#softShadow)"/>
  <rect x="646" y="514" width="148" height="14" rx="7" fill="#B9C4CA"/>

  <!-- Phone mockup in foreground -->
  <rect x="936" y="302" width="174" height="310" rx="36" fill="url(#deviceWhite)" filter="url(#softShadow)"/>
  <rect x="952" y="332" width="142" height="238" rx="18" fill="url(#screenGlass)"/>
  <rect x="994" y="316" width="58" height="8" rx="4" fill="#C5CDD2"/>
  <circle cx="1023" cy="592" r="13" fill="#F8FAFC" stroke="#B8C0C7" stroke-width="2"/>
  <rect x="970" y="354" width="106" height="58" rx="16" fill="url(#accentGrad)" filter="url(#screenGlow)"/>
  <rect x="970" y="431" width="106" height="18" rx="9" fill="#34485A"/>
  <rect x="970" y="464" width="72" height="18" rx="9" fill="#34485A"/>
  <rect x="970" y="498" width="92" height="18" rx="9" fill="#34485A"/>
  <circle cx="1064" cy="507" r="16" fill="#72F1C8"/>
  <text x="986" y="390" width="72" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">
    Mobile
  </text>

  <text x="74" y="652" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#FFFFFF" opacity="0.88">
    Replace dark screens with screenshots, or keep the vector UI for fully editable product storytelling.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using imported PNG device frames when the device can be built from editable rounded rectangles and simple paths
- ❌ Applying `clip-path` to screen rectangles or groups; if screenshots are added, clip only the `<image>` itself
- ❌ Over-detailing bezels with dozens of tiny ports and screws; the mockup should stay minimalist and scalable
- ❌ Using `marker-end` paths for UI arrows inside screens; use simple `<line>` elements if arrows are needed
- ❌ Forgetting explicit `width` on `<text>`, especially for labels inside screens

## Composition notes
- Stage devices with one dominant laptop, then overlap a tablet or phone in the foreground to create depth without clutter.
- Keep bezels symmetrical: equal left/right margins, slightly larger top/bottom margins for cameras and buttons.
- Use dark screen interiors so white/silver chassis shapes read crisply against bright or gradient backgrounds.
- Reserve 20–30% of the slide for headline and explanatory text; let the devices occupy the visual center and lower-right area.