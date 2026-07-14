# SVG Recipe — Modern Geometric Introduction Slide

## Visual mechanism
A pristine white title slide is split into a calm typography column on the left and a layered abstract geometry cluster on the right. The premium look comes from overlapping rotated square cards, diagonal gradients, dot-grid textures, soft shadows, and restrained accent marks.

## SVG primitives needed
- 1× `<rect>` for the full-slide white background
- 4× `<rect>` for the main geometric square cards: two pale texture cards, one gradient hero card, one small accent tile
- 2× `<rect>` for the kicker underline and tiny brand mark
- 40–70× `<circle>` for editable dot-grid textures and a few floating accent particles
- 3× `<path>` for diagonal/triangular decorative shards that make the geometry feel custom rather than grid-like
- 3× `<text>` blocks for kicker, oversized headline, and body copy; every text element must include `width`
- 2× `<linearGradient>` definitions for the vivid square and small accent elements
- 1× `<filter id="softShadow">` applied to card rectangles and decorative paths for depth

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="violetPink" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F25BEA"/>
      <stop offset="48%" stop-color="#B64FE4"/>
      <stop offset="100%" stop-color="#6C4BFF"/>
    </linearGradient>
    <linearGradient id="warmAccent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FF6BD6"/>
      <stop offset="100%" stop-color="#7A5CFF"/>
    </linearGradient>
    <filter id="softShadow" x="-25%" y="-25%" width="150%" height="150%">
      <feOffset dx="0" dy="18" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="tinyGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="8"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <text x="90" y="142" width="330" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" letter-spacing="3" fill="#6B6B74">ABOUT US</text>
  <rect x="90" y="162" width="58" height="5" rx="2.5" fill="url(#warmAccent)"/>
  <rect x="158" y="162" width="10" height="5" rx="2.5" fill="#E8E8EF"/>

  <text x="86" y="260" width="570" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="76" font-weight="800" fill="#1E1E24">
    <tspan x="86" dy="0">Awesome</tspan>
    <tspan x="86" dy="82">Presentation</tspan>
  </text>

  <text x="92" y="482" width="500" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" fill="#7B7B86">
    <tspan x="92" dy="0">A modern introduction layout built for pitch decks,</tspan>
    <tspan x="92" dy="28">agency portfolios, and high-stakes brand storytelling.</tspan>
    <tspan x="92" dy="28">Clean typography meets bold abstract geometry.</tspan>
  </text>

  <text x="96" y="650" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" letter-spacing="2" fill="#B7B7C2">2026 BRAND SYSTEM</text>

  <path d="M686 115 L1178 42 L1088 158 L738 207 Z" fill="#F7F7FB"/>
  <path d="M1048 586 L1215 448 L1242 682 Z" fill="#F2F0FF"/>
  <path d="M682 565 L766 548 L742 642 Z" fill="#F9EAFE"/>

  <g transform="rotate(-8 870 276)">
    <rect x="735" y="135" width="286" height="286" rx="8" fill="#FAFAFC" filter="url(#softShadow)"/>
    <circle cx="772" cy="176" r="2.2" fill="#C9C9D2"/>
    <circle cx="812" cy="176" r="2.2" fill="#C9C9D2"/>
    <circle cx="852" cy="176" r="2.2" fill="#C9C9D2"/>
    <circle cx="892" cy="176" r="2.2" fill="#C9C9D2"/>
    <circle cx="932" cy="176" r="2.2" fill="#C9C9D2"/>
    <circle cx="972" cy="176" r="2.2" fill="#C9C9D2"/>
    <circle cx="772" cy="216" r="2.2" fill="#C9C9D2"/>
    <circle cx="812" cy="216" r="2.2" fill="#C9C9D2"/>
    <circle cx="852" cy="216" r="2.2" fill="#C9C9D2"/>
    <circle cx="892" cy="216" r="2.2" fill="#C9C9D2"/>
    <circle cx="932" cy="216" r="2.2" fill="#C9C9D2"/>
    <circle cx="972" cy="216" r="2.2" fill="#C9C9D2"/>
    <circle cx="772" cy="256" r="2.2" fill="#C9C9D2"/>
    <circle cx="812" cy="256" r="2.2" fill="#C9C9D2"/>
    <circle cx="852" cy="256" r="2.2" fill="#C9C9D2"/>
    <circle cx="892" cy="256" r="2.2" fill="#C9C9D2"/>
    <circle cx="932" cy="256" r="2.2" fill="#C9C9D2"/>
    <circle cx="972" cy="256" r="2.2" fill="#C9C9D2"/>
    <circle cx="772" cy="296" r="2.2" fill="#C9C9D2"/>
    <circle cx="812" cy="296" r="2.2" fill="#C9C9D2"/>
    <circle cx="852" cy="296" r="2.2" fill="#C9C9D2"/>
    <circle cx="892" cy="296" r="2.2" fill="#C9C9D2"/>
    <circle cx="932" cy="296" r="2.2" fill="#C9C9D2"/>
    <circle cx="972" cy="296" r="2.2" fill="#C9C9D2"/>
  </g>

  <g transform="rotate(6 925 395)">
    <rect x="770" y="240" width="310" height="310" rx="10" fill="url(#violetPink)" filter="url(#softShadow)"/>
    <path d="M770 240 L1080 240 L1080 344 C992 322 894 352 770 314 Z" fill="#FFFFFF" opacity="0.13"/>
    <path d="M826 550 L1080 298 L1080 550 Z" fill="#351567" opacity="0.16"/>
  </g>

  <g transform="rotate(-5 1068 430)">
    <rect x="958" y="320" width="220" height="220" rx="8" fill="#FBFBFD" filter="url(#softShadow)"/>
    <circle cx="992" cy="354" r="2" fill="#CBCBD5"/>
    <circle cx="1032" cy="354" r="2" fill="#CBCBD5"/>
    <circle cx="1072" cy="354" r="2" fill="#CBCBD5"/>
    <circle cx="1112" cy="354" r="2" fill="#CBCBD5"/>
    <circle cx="1152" cy="354" r="2" fill="#CBCBD5"/>
    <circle cx="992" cy="394" r="2" fill="#CBCBD5"/>
    <circle cx="1032" cy="394" r="2" fill="#CBCBD5"/>
    <circle cx="1072" cy="394" r="2" fill="#CBCBD5"/>
    <circle cx="1112" cy="394" r="2" fill="#CBCBD5"/>
    <circle cx="1152" cy="394" r="2" fill="#CBCBD5"/>
    <circle cx="992" cy="434" r="2" fill="#CBCBD5"/>
    <circle cx="1032" cy="434" r="2" fill="#CBCBD5"/>
    <circle cx="1072" cy="434" r="2" fill="#CBCBD5"/>
    <circle cx="1112" cy="434" r="2" fill="#CBCBD5"/>
    <circle cx="1152" cy="434" r="2" fill="#CBCBD5"/>
    <circle cx="992" cy="474" r="2" fill="#CBCBD5"/>
    <circle cx="1032" cy="474" r="2" fill="#CBCBD5"/>
    <circle cx="1072" cy="474" r="2" fill="#CBCBD5"/>
    <circle cx="1112" cy="474" r="2" fill="#CBCBD5"/>
    <circle cx="1152" cy="474" r="2" fill="#CBCBD5"/>
  </g>

  <rect x="1076" y="214" width="74" height="74" rx="7" fill="url(#warmAccent)" transform="rotate(12 1113 251)" filter="url(#softShadow)"/>
  <circle cx="704" cy="204" r="9" fill="#F25BEA" filter="url(#tinyGlow)"/>
  <circle cx="1168" cy="168" r="6" fill="#7A5CFF"/>
  <circle cx="722" cy="505" r="5" fill="#FF7ADD"/>
</svg>
```

## Avoid in this skill
- ❌ `<pattern>` for the dot grid; create dots as editable `<circle>` elements instead
- ❌ Masking or clipping non-image geometry; the card texture can be built directly inside each rotated group
- ❌ Overcrowding the right-side cluster with too many shapes, which weakens the premium minimalist feel
- ❌ Pure black text; use deep charcoal so the slide feels softer and more editorial
- ❌ Skew or matrix transforms; use only `rotate(...)`, `translate(...)`, and simple scale if needed

## Composition notes
- Keep the left 45–50% of the slide mostly empty except for the kicker, large title, and short body copy.
- Let the right geometric cluster occupy the vertical center and bleed visually toward the upper-right edge for energy.
- Use one dominant gradient card, then support it with quieter off-white dot-texture cards.
- Maintain a restrained color rhythm: charcoal text, pale gray textures, and one vivid pink-purple accent system.