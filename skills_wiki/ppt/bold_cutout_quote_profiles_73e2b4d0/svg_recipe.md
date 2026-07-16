# SVG Recipe — Bold Cutout Quote Profiles

## Visual mechanism
A dark, cinematic background is interrupted by oversized quote typography and tilted editorial quote cards. Each card pairs bold white quote text with a single accent-color keyword and a high-contrast black-and-white portrait cut into or placed over a bright geometric backing shape.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark gradient background
- 1× `<radialGradient>` for the moody blue/charcoal vignette
- 3× `<linearGradient>` for subtle card and title depth
- 4× `<filter>` definitions for card shadows, text shadow, soft glow, and arrow shadow
- 5× `<rect>` for tilted dark quote cards and accent quote panels
- 4× `<path>` for curved arrow, arrowhead, slanted accent portrait backings, and decorative quote marks
- 3× `<circle>` / `<ellipse>` for the main cutout portrait disk, outline ring, and glow accents
- 3× `<clipPath>` definitions applied only to `<image>` for circular and rounded portrait/photo crops
- 3× `<image>` for preprocessed black-and-white or transparent-cutout portrait assets
- 9× `<text>` elements with explicit `width` attributes for headline, quote copy, authors, and oversized quotation marks
- 2× `<line>` for fine editorial dividers / accent ticks

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgRadial" cx="50%" cy="43%" r="75%">
      <stop offset="0%" stop-color="#374A9B"/>
      <stop offset="55%" stop-color="#28377D"/>
      <stop offset="100%" stop-color="#10131F"/>
    </radialGradient>

    <linearGradient id="cardGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#252A31"/>
      <stop offset="100%" stop-color="#15191F"/>
    </linearGradient>
    <linearGradient id="quoteGold" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFD64D"/>
      <stop offset="100%" stop-color="#FFB400"/>
    </linearGradient>
    <linearGradient id="pptOrange" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FF7C45"/>
      <stop offset="100%" stop-color="#EF321C"/>
    </linearGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="150%" height="160%">
      <feOffset dx="0" dy="22"/>
      <feGaussianBlur stdDeviation="20"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="titleShadow" x="-10%" y="-10%" width="130%" height="140%">
      <feOffset dx="5" dy="8"/>
      <feGaussianBlur stdDeviation="5"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
    <filter id="arrowShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="7"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="mainPortraitClip">
      <circle cx="0" cy="0" r="82"/>
    </clipPath>
    <clipPath id="smallPortraitClip">
      <rect x="0" y="0" width="130" height="170" rx="16"/>
    </clipPath>
    <clipPath id="roundPanelClip">
      <rect x="0" y="0" width="172" height="118" rx="10"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgRadial)"/>
  <ellipse cx="1035" cy="565" rx="300" ry="95" fill="#05070B" opacity="0.45" filter="url(#softGlow)"/>

  <text x="70" y="132" width="560" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="78" font-weight="900" fill="#FFFFFF" letter-spacing="1" filter="url(#titleShadow)">HOW TO DESIGN</text>
  <text x="60" y="326" width="610" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="165" font-weight="900" fill="url(#quoteGold)" letter-spacing="-4" filter="url(#titleShadow)">QUOTES</text>

  <path d="M630 97 C710 72 776 104 800 181" fill="none" stroke="#FFFFFF" stroke-width="15" stroke-linecap="round" filter="url(#arrowShadow)"/>
  <path d="M762 178 L844 174 C852 174 857 183 852 190 L804 258 C799 265 789 264 785 257 L752 190 C749 184 755 178 762 178Z" fill="#FFFFFF" filter="url(#arrowShadow)"/>

  <g transform="translate(872 36) rotate(10)">
    <rect x="0" y="0" width="390" height="180" rx="2" fill="url(#cardGrad)" filter="url(#cardShadow)"/>
    <line x1="72" y1="74" x2="72" y2="150" stroke="#E8F7F5" stroke-width="1" opacity="0.65"/>
    <rect x="84" y="62" width="285" height="74" fill="#7EF4F0"/>
    <text x="106" y="47" width="60" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="58" font-weight="900" fill="#FFFFFF">“</text>
    <text x="110" y="97" width="185" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="900" fill="#1B252A">A WINNER IS A</text>
    <text x="110" y="120" width="200" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="900" fill="#1B252A">DREAMER WHO</text>
    <text x="110" y="143" width="205" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="900" fill="#1B252A">NEVER GIVES UP.</text>
    <image x="300" y="38" width="105" height="136" clip-path="url(#smallPortraitClip)" href="https://images.example.com/bw-transparent-executive-portrait-waving.png"/>
  </g>

  <g transform="translate(575 164) rotate(10)">
    <rect x="0" y="0" width="565" height="365" rx="2" fill="url(#cardGrad)" filter="url(#cardShadow)"/>
    <text x="68" y="137" width="80" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="80" font-weight="900" fill="#FFFFFF">“</text>
    <text x="90" y="170" width="330" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="27" font-weight="900" fill="#FFFFFF">
      <tspan x="90" dy="0">BE THE </tspan><tspan fill="#FFC400">CHANGE</tspan>
      <tspan x="90" dy="34">THAT YOU WISH TO</tspan>
      <tspan x="90" dy="34">SEE IN </tspan><tspan fill="#FFC400">THE WORLD.</tspan>
    </text>
    <circle cx="420" cy="178" r="99" fill="#FFC400"/>
    <circle cx="420" cy="178" r="111" fill="none" stroke="#FFFFFF" stroke-width="1.2" opacity="0.55"/>
    <circle cx="420" cy="178" r="82" fill="#EFEFEF"/>
    <image x="338" y="96" width="164" height="164" clip-path="url(#mainPortraitClip)" transform="translate(420 178)" href="https://images.example.com/black-white-circular-leader-portrait.png"/>
  </g>

  <g transform="translate(315 345) rotate(12)">
    <rect x="0" y="0" width="520" height="305" rx="2" fill="url(#cardGrad)" filter="url(#cardShadow)"/>
    <text x="53" y="108" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="76" font-weight="900" fill="#FFFFFF">“</text>
    <text x="78" y="154" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="26" font-weight="900" fill="#FFFFFF">
      <tspan fill="#84E5B9">PRICE</tspan><tspan> IS WHAT YOU</tspan>
      <tspan x="78" dy="32">PAY, </tspan><tspan fill="#84E5B9">VALUE</tspan><tspan> IS WHAT</tspan>
      <tspan x="78" dy="32">YOU GET.</tspan>
    </text>
    <text x="195" y="236" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#FFFFFF">- Warren Buffett</text>
    <path d="M358 80 L502 58 L472 252 L328 268 Z" fill="#84E5B9"/>
    <image x="344" y="60" width="145" height="205" clip-path="url(#smallPortraitClip)" href="https://images.example.com/bw-transparent-business-profile-cutout.png"/>
  </g>

  <circle cx="176" cy="574" r="168" fill="#FF9D63" opacity="0.95"/>
  <path d="M176 406 A168 168 0 0 1 344 574 L176 574 Z" fill="#FFA56B" opacity="0.85"/>
  <path d="M176 574 L344 574 A168 168 0 0 1 176 742 Z" fill="#FF5B32" opacity="0.9"/>
  <rect x="-35" y="479" width="205" height="181" rx="16" fill="url(#pptOrange)" filter="url(#cardShadow)"/>
  <text x="31" y="620" width="115" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="138" font-weight="800" fill="#FFFFFF">P</text>
</svg>
```

## Avoid in this skill
- ❌ Applying `clip-path` to rectangles or paths for card crops; use clip paths only on `<image>` elements.
- ❌ SVG grayscale filters such as `feColorMatrix`; instead use preprocessed black-and-white portrait assets.
- ❌ `marker-end` arrows; draw the arrowhead as a filled `<path>` so it remains editable.
- ❌ Overly thin typography for quotes; this style depends on heavy, poster-like sans-serif weight.
- ❌ Busy full-color portraits that fight the accent color; keep the portrait monochrome or transparent-cutout.

## Composition notes
- Keep the quote cards on the right 55–65% of the canvas, overlapping and slightly rotated for a keynote-thumbnail feel.
- Use one dominant accent color per quote card; repeat it in both the portrait backing shape and one or two key words.
- Preserve a very dark card surface so white text and bright accents have maximum contrast.
- Let the oversized headline or quotation marks bleed visually behind the cards; negative space can be dark, but not empty.