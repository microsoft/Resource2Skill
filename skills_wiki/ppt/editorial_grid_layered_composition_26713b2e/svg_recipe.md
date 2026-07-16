# SVG Recipe — Editorial Grid & Layered Composition

## Visual mechanism
A disciplined modular editorial grid gives the slide structure, while oversized typography, a clipped hero photo, and foreground labels intentionally overlap across columns to create magazine-like depth. The design feels premium because the image, display type, metadata, and accent marks share a muted palette with one high-contrast focal color.

## SVG primitives needed
- 1× `<rect>` for the warm sand slide background
- 16× `<line>` for the faint modular editorial grid
- 2× oversized `<text>` blocks for background and foreground headline typography
- 1× `<path>` shadow plate behind the hero image
- 1× `<clipPath>` with a custom `<path>` to crop the hero photo into an editorial notched card
- 1× `<image>` for the central hero photograph
- 3× `<rect>` for small metadata chips, caption panels, and CTA blocks
- 2× `<path>` organic accent shapes for layered magazine-style disruption
- 2× `<circle>` for high-contrast focal dots
- 1× `<filter id="softShadow">` applied to the hero shadow plate and foreground cards
- 1× `<linearGradient>` for the subtle coral-to-orange accent wash
- Multiple `<text>` elements with explicit `width` attributes for headline, metadata, pull quote, and body copy

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="coralWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ff4136"/>
      <stop offset="100%" stop-color="#ff9f6e"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="18" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="heroClip">
      <path d="M540 106 L952 106 Q984 106 984 138 L984 592 Q984 624 952 624 L600 624 Q568 624 568 592 L568 505 L520 505 L520 138 Q520 106 540 106 Z"/>
    </clipPath>
  </defs>

  <!-- warm editorial paper background -->
  <rect x="0" y="0" width="1280" height="720" fill="#f5f2eb"/>

  <!-- faint 12-column / 6-row modular grid -->
  <line x1="106.7" y1="0" x2="106.7" y2="720" stroke="#e4dfd8" stroke-width="1"/>
  <line x1="213.3" y1="0" x2="213.3" y2="720" stroke="#e4dfd8" stroke-width="1"/>
  <line x1="320" y1="0" x2="320" y2="720" stroke="#e4dfd8" stroke-width="1"/>
  <line x1="426.7" y1="0" x2="426.7" y2="720" stroke="#e4dfd8" stroke-width="1"/>
  <line x1="533.3" y1="0" x2="533.3" y2="720" stroke="#e4dfd8" stroke-width="1"/>
  <line x1="640" y1="0" x2="640" y2="720" stroke="#e4dfd8" stroke-width="1"/>
  <line x1="746.7" y1="0" x2="746.7" y2="720" stroke="#e4dfd8" stroke-width="1"/>
  <line x1="853.3" y1="0" x2="853.3" y2="720" stroke="#e4dfd8" stroke-width="1"/>
  <line x1="960" y1="0" x2="960" y2="720" stroke="#e4dfd8" stroke-width="1"/>
  <line x1="1066.7" y1="0" x2="1066.7" y2="720" stroke="#e4dfd8" stroke-width="1"/>
  <line x1="1173.3" y1="0" x2="1173.3" y2="720" stroke="#e4dfd8" stroke-width="1"/>
  <line x1="0" y1="120" x2="1280" y2="120" stroke="#e4dfd8" stroke-width="1"/>
  <line x1="0" y1="240" x2="1280" y2="240" stroke="#e4dfd8" stroke-width="1"/>
  <line x1="0" y1="360" x2="1280" y2="360" stroke="#e4dfd8" stroke-width="1"/>
  <line x1="0" y1="480" x2="1280" y2="480" stroke="#e4dfd8" stroke-width="1"/>
  <line x1="0" y1="600" x2="1280" y2="600" stroke="#e4dfd8" stroke-width="1"/>

  <!-- background typography layer, intentionally oversized and low-contrast -->
  <text x="54" y="160" width="680" font-family="Segoe UI, Microsoft YaHei" font-size="132" font-weight="800" letter-spacing="-8" fill="#ded8cf">
    FIELD
  </text>
  <text x="50" y="292" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="132" font-weight="800" letter-spacing="-8" fill="#ded8cf">
    NOTES
  </text>

  <!-- organic accent layer breaking the grid -->
  <path d="M1012 88 C1078 62 1156 80 1190 136 C1226 196 1178 254 1114 244 C1046 233 995 170 1012 88 Z" fill="url(#coralWash)" opacity="0.88"/>
  <path d="M100 560 C164 518 230 534 256 590 C282 646 218 682 152 660 C98 642 62 604 100 560 Z" fill="#212529" opacity="0.08"/>

  <!-- hero image shadow plate, matching the custom crop silhouette -->
  <path d="M540 106 L952 106 Q984 106 984 138 L984 592 Q984 624 952 624 L600 624 Q568 624 568 592 L568 505 L520 505 L520 138 Q520 106 540 106 Z"
        fill="#222222" opacity="0.18" filter="url(#softShadow)"/>

  <!-- central hero photo clipped into an editorial notched card -->
  <image x="500" y="86" width="520" height="560"
         href="https://images.example.com/editorial-fashion-portrait-in-muted-sand-and-slate-tones.jpg"
         clip-path="url(#heroClip)" preserveAspectRatio="xMidYMid slice"/>

  <!-- foreground headline overlapping image and left grid columns -->
  <text x="58" y="470" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="96" font-weight="800" letter-spacing="-5" fill="#212529">
    SPRING
  </text>
  <text x="58" y="558" width="650" font-family="Segoe UI, Microsoft YaHei" font-size="96" font-weight="800" letter-spacing="-5" fill="#212529">
    INDEX
  </text>

  <!-- small editorial metadata at top-left -->
  <text x="62" y="70" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" letter-spacing="2.8" fill="#212529">
    PORTFOLIO / 2026
  </text>
  <text x="62" y="96" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6d7176">
    Modular direction system
  </text>

  <!-- body copy block aligned to grid -->
  <text x="74" y="332" width="320" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#212529">
    Editorial rhythm with controlled disruption
  </text>
  <text x="74" y="365" width="340" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#666b70">
    <tspan x="74" dy="0">A strict twelve-column structure keeps the</tspan>
    <tspan x="74" dy="22">composition calm, while overlapping type,</tspan>
    <tspan x="74" dy="22">image crops, and accent marks create depth.</tspan>
  </text>

  <!-- foreground caption card crossing the photo edge -->
  <rect x="858" y="438" width="310" height="126" rx="20" fill="#ffffff" opacity="0.94" filter="url(#softShadow)"/>
  <text x="884" y="474" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="800" letter-spacing="2.4" fill="#ff4136">
    FEATURE 04
  </text>
  <text x="884" y="504" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#212529">
    Layered brand story
  </text>
  <text x="884" y="532" width="248" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6d7176">
    <tspan x="884" dy="0">Use one vivid accent to make the</tspan>
    <tspan x="884" dy="18">viewer land on the focal message.</tspan>
  </text>

  <!-- high-contrast focal marks and CTA -->
  <circle cx="1110" cy="156" r="11" fill="#212529"/>
  <circle cx="1138" cy="156" r="11" fill="#ff4136"/>
  <rect x="74" y="618" width="180" height="42" rx="21" fill="#ff4136"/>
  <text x="105" y="645" width="128" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="800" letter-spacing="1.2" fill="#ffffff">
    VIEW EDIT
  </text>

  <!-- thin measuring rules for editorial feel -->
  <line x1="1048" y1="612" x2="1196" y2="612" stroke="#212529" stroke-width="2"/>
  <text x="1048" y="642" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" letter-spacing="2.2" fill="#6d7176">
    GRID 12 × 6
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<pattern>` for the background grid; draw faint editable `<line>` elements instead.
- ❌ Do not apply `clip-path` to text or decorative shapes; use clipping only on the hero `<image>`.
- ❌ Do not use `<mask>` to hide parts of the large headline behind the image; rely on z-order layering instead.
- ❌ Do not build the layout as equal cards only; the technique depends on intentional overlap and broken grid moments.
- ❌ Do not use `skewX`, `skewY`, or matrix transforms for editorial angles; use plain paths or rotated elements if needed.

## Composition notes
- Keep the hero image near the center-right, spanning roughly four grid columns vertically; let typography cross its edge to create depth.
- Use oversized low-contrast background type first, then image, then darker foreground type and caption cards.
- Reserve one vivid accent color for focal dots, CTA, or section labels; everything else should stay muted and harmonized.
- Leave generous negative space in the upper-left or lower-right so the overlap feels intentional rather than crowded.