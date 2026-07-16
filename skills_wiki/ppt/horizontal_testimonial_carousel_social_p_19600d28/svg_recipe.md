# SVG Recipe — Horizontal Testimonial Carousel / Social Proof Slider

## Visual mechanism
A premium social-proof slide uses a horizontal row of rounded testimonial cards, each built around a centered avatar, name, star rating, and concise quote. Subtle shadows, partial off-canvas cards, and small navigation dots make the layout feel like a website carousel rather than a static grid.

## SVG primitives needed
- 1× `<rect>` for the full-slide warm background
- 10–14× `<path>` for distressed background texture, purple accent wedges, quote marks, and decorative carousel motion cues
- 5× `<rect>` for testimonial cards, including two partially visible side cards to imply sliding
- 3× `<image>` clipped into circles for reviewer avatars
- 3× `<clipPath>` with `<circle>` for circular avatar crops
- 3× `<circle>` for avatar rings
- 3× `<text>` groups for names, star ratings, and testimonial copy
- 2× `<text>` blocks for headline and subtitle
- 4× `<circle>` for carousel pagination dots
- 2× `<line>` for simple previous/next chevrons
- 2× `<linearGradient>` for brand accents and background depth
- 1× `<filter id="cardShadow">` applied to cards
- 1× `<filter id="softGlow">` applied to accent shapes or active dot

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7F3EE"/>
      <stop offset="100%" stop-color="#ECE7E1"/>
    </linearGradient>
    <linearGradient id="brandGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#18C7D5"/>
      <stop offset="55%" stop-color="#4768E8"/>
      <stop offset="100%" stop-color="#8434E8"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="16"/>
      <feGaussianBlur stdDeviation="18"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.16 0 0 0 0 0.13 0 0 0 0 0.11 0 0 0 0.18 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="8"/>
    </filter>
    <clipPath id="avatarA"><circle cx="250" cy="314" r="46"/></clipPath>
    <clipPath id="avatarB"><circle cx="640" cy="314" r="46"/></clipPath>
    <clipPath id="avatarC"><circle cx="1030" cy="314" r="46"/></clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <path d="M0 76 C185 35 326 92 500 58 C640 30 812 42 1010 70 C1114 85 1198 76 1280 50 L1280 0 L0 0 Z" fill="#FFFFFF" opacity="0.72"/>
  <path d="M0 672 C160 630 310 690 520 652 C740 612 925 656 1280 620 L1280 720 L0 720 Z" fill="#FFFFFF" opacity="0.62"/>
  <path d="M970 0 L1280 0 L1280 720 L1128 720 C1085 612 1055 502 1074 390 C1092 286 1015 176 970 0 Z" fill="url(#brandGrad)" opacity="0.95"/>
  <path d="M76 42 C150 34 208 48 286 39" stroke="#BDBDBD" stroke-width="10" stroke-linecap="round" opacity="0.38" fill="none"/>
  <path d="M410 38 C520 62 592 28 706 48" stroke="#C9C9C9" stroke-width="7" stroke-linecap="round" opacity="0.42" fill="none"/>
  <path d="M188 106 C306 80 394 126 500 98" stroke="#C7C7C7" stroke-width="9" stroke-linecap="round" opacity="0.32" fill="none"/>
  <path d="M720 112 C848 82 935 122 1035 94" stroke="#BBBBBB" stroke-width="8" stroke-linecap="round" opacity="0.35" fill="none"/>

  <text x="74" y="86" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="700" fill="url(#brandGrad)" letter-spacing="1.5">CLIENT VOICES</text>
  <text x="74" y="153" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="54" font-weight="800" fill="#161616">Testimonial Slider</text>
  <text x="78" y="190" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#6B625B">Three trusted customers, one clean carousel rhythm — ideal for traction, validation, or sales proof slides.</text>

  <rect x="-185" y="258" width="300" height="338" rx="30" fill="#FFFFFF" opacity="0.52" filter="url(#cardShadow)"/>
  <rect x="1165" y="258" width="300" height="338" rx="30" fill="#FFFFFF" opacity="0.42" filter="url(#cardShadow)"/>

  <rect x="100" y="238" width="300" height="370" rx="32" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="490" y="238" width="300" height="370" rx="32" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="880" y="238" width="300" height="370" rx="32" fill="#FFFFFF" filter="url(#cardShadow)"/>

  <path d="M142 286 C128 286 120 296 120 312 L120 350 L161 350 L161 312 L143 312 C144 302 151 296 164 294 L164 270 C156 272 148 277 142 286 Z" fill="#F0E9E2"/>
  <path d="M532 286 C518 286 510 296 510 312 L510 350 L551 350 L551 312 L533 312 C534 302 541 296 554 294 L554 270 C546 272 538 277 532 286 Z" fill="#F0E9E2"/>
  <path d="M922 286 C908 286 900 296 900 312 L900 350 L941 350 L941 312 L923 312 C924 302 931 296 944 294 L944 270 C936 272 928 277 922 286 Z" fill="#F0E9E2"/>

  <image href="https://images.example.com/avatar-confident-founder-warm-office.jpg" x="204" y="268" width="92" height="92" clip-path="url(#avatarA)" preserveAspectRatio="xMidYMid slice"/>
  <image href="https://images.example.com/avatar-marketing-leader-natural-light.jpg" x="594" y="268" width="92" height="92" clip-path="url(#avatarB)" preserveAspectRatio="xMidYMid slice"/>
  <image href="https://images.example.com/avatar-operations-director-studio.jpg" x="984" y="268" width="92" height="92" clip-path="url(#avatarC)" preserveAspectRatio="xMidYMid slice"/>
  <circle cx="250" cy="314" r="50" fill="none" stroke="url(#brandGrad)" stroke-width="4"/>
  <circle cx="640" cy="314" r="50" fill="none" stroke="url(#brandGrad)" stroke-width="4"/>
  <circle cx="1030" cy="314" r="50" fill="none" stroke="url(#brandGrad)" stroke-width="4"/>

  <text x="135" y="392" width="230" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#232323">Hannah Morales</text>
  <text x="135" y="424" width="230" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="20" fill="#FFB400" letter-spacing="2">★★★★★</text>
  <text x="132" y="470" width="236" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#5E5A56">
    <tspan x="250" dy="0">“The deck finally made</tspan>
    <tspan x="250" dy="25">our traction obvious.</tspan>
    <tspan x="250" dy="25">Investors understood the</tspan>
    <tspan x="250" dy="25">story in minutes.”</tspan>
  </text>

  <text x="525" y="392" width="230" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#232323">Olivia Wilson</text>
  <text x="525" y="424" width="230" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="20" fill="#FFB400" letter-spacing="2">★★★★★</text>
  <text x="522" y="470" width="236" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#5E5A56">
    <tspan x="640" dy="0">“Clean, credible, and</tspan>
    <tspan x="640" dy="25">fast to adapt. Our sales</tspan>
    <tspan x="640" dy="25">team uses this proof slide</tspan>
    <tspan x="640" dy="25">in every proposal.”</tspan>
  </text>

  <text x="915" y="392" width="230" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#232323">Morgan Maxwell</text>
  <text x="915" y="424" width="230" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="20" fill="#FFB400" letter-spacing="2">★★★★★</text>
  <text x="912" y="470" width="236" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#5E5A56">
    <tspan x="1030" dy="0">“It turned scattered</tspan>
    <tspan x="1030" dy="25">customer praise into a</tspan>
    <tspan x="1030" dy="25">visual asset our board</tspan>
    <tspan x="1030" dy="25">immediately trusted.”</tspan>
  </text>

  <line x1="54" y1="423" x2="34" y2="443" stroke="#6D625A" stroke-width="5" stroke-linecap="round"/>
  <line x1="54" y1="463" x2="34" y2="443" stroke="#6D625A" stroke-width="5" stroke-linecap="round"/>
  <line x1="1226" y1="423" x2="1246" y2="443" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>
  <line x1="1226" y1="463" x2="1246" y2="443" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>

  <circle cx="598" cy="660" r="6" fill="#B9AEA4"/>
  <circle cx="626" cy="660" r="6" fill="#B9AEA4"/>
  <circle cx="654" cy="660" r="9" fill="url(#brandGrad)" filter="url(#softGlow)"/>
  <circle cx="686" cy="660" r="6" fill="#B9AEA4"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to create avatar crops; use `<clipPath>` applied directly to each `<image>`.
- ❌ Do not build the star rating from icon symbols with `<use>`; use editable Unicode star text or individual paths.
- ❌ Do not place testimonial copy inside `<foreignObject>`; keep it as native `<text>` with explicit `width`.
- ❌ Do not rely on `marker-end` for carousel arrows; draw chevrons with simple `<line>` elements.
- ❌ Do not overcrowd cards with long paragraphs; the carousel works best with short, highly edited quotes.

## Composition notes
- Reserve the upper-left quarter for a clear headline and subtitle; keep the testimonial cards as the primary focus in the lower two-thirds.
- Use three full cards plus faint partial cards at the left and right edges to imply a horizontal slider beyond the current frame.
- Keep all card interiors center-aligned: avatar, name, stars, and quote should share a strict vertical axis.
- Use one vivid accent gradient for rings, dots, and background wedge; keep cards white and text neutral for trust and readability.