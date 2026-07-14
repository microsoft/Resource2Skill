# SVG Recipe — Minimal Central Card

## Visual mechanism
A single large rounded card is centered on a quiet full-slide background, using soft dual shadows, a subtle gradient surface, and sparse typography to make one message feel deliberate and premium. Tiny accent geometry and low-contrast decorative blobs add depth without competing with the central content.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 2× `<path>` for oversized blurred ambient background blobs
- 1× `<rect>` for the central rounded card body
- 1× `<rect>` for the card’s inner top highlight stroke/sheen
- 1× `<rect>` for a small eyebrow pill label
- 1× `<rect>` for a thin accent rule under the headline
- 1× `<path>` for a decorative abstract quote mark / brand glyph
- 3× `<text>` for eyebrow, headline, and subhead content
- 3× `<linearGradient>` for background, card fill, and accent color
- 1× `<radialGradient>` for the ambient glow
- 3× `<filter>` using `feGaussianBlur` and/or `feOffset+feGaussianBlur+feMerge` for soft background blur, card shadow, and subtle glyph glow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#F8FAFC"/>
      <stop offset="48%" stop-color="#EEF3F8"/>
      <stop offset="100%" stop-color="#E8EEF5"/>
    </linearGradient>

    <linearGradient id="cardGrad" x1="290" y1="170" x2="990" y2="550">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="58%" stop-color="#F8FAFD"/>
      <stop offset="100%" stop-color="#F1F5FA"/>
    </linearGradient>

    <linearGradient id="accentGrad" x1="504" y1="0" x2="776" y2="0">
      <stop offset="0%" stop-color="#5B8CFF"/>
      <stop offset="55%" stop-color="#7C5CFF"/>
      <stop offset="100%" stop-color="#B45CFF"/>
    </linearGradient>

    <radialGradient id="blobGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#8EA7FF" stop-opacity="0.34"/>
      <stop offset="70%" stop-color="#8EA7FF" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#8EA7FF" stop-opacity="0"/>
    </radialGradient>

    <filter id="ambientBlur" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="34"/>
    </filter>

    <filter id="cardShadow" x="-12%" y="-16%" width="124%" height="136%">
      <feOffset dx="0" dy="22" result="offDark"/>
      <feGaussianBlur in="offDark" stdDeviation="24" result="blurDark"/>
      <feOffset dx="0" dy="-10" result="offLight"/>
      <feGaussianBlur in="offLight" stdDeviation="16" result="blurLight"/>
      <feMerge>
        <feMergeNode in="blurDark"/>
        <feMergeNode in="blurLight"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="glyphGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="7" result="softGlow"/>
      <feMerge>
        <feMergeNode in="softGlow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <path d="M154 106 C250 20 392 32 448 138 C503 241 428 340 296 348 C158 357 52 250 78 174 C90 139 120 126 154 106 Z"
        fill="url(#blobGlow)" filter="url(#ambientBlur)" opacity="0.85"/>
  <path d="M1018 455 C1124 390 1230 426 1250 516 C1274 622 1158 690 1042 660 C932 632 872 534 930 484 C952 466 982 468 1018 455 Z"
        fill="#B9F0E6" opacity="0.22" filter="url(#ambientBlur)"/>

  <rect x="290" y="170" width="700" height="380" rx="38" ry="38"
        fill="url(#cardGrad)" filter="url(#cardShadow)"/>

  <rect x="307" y="187" width="666" height="346" rx="28" ry="28"
        fill="none" stroke="#FFFFFF" stroke-opacity="0.78" stroke-width="2"/>

  <path d="M867 244 C890 244 908 262 908 285 C908 308 890 326 867 326 C844 326 826 308 826 285 C826 262 844 244 867 244 Z
           M875 275 C875 268 881 262 888 262 C895 262 901 268 901 275 C901 282 895 288 888 288 C881 288 875 282 875 275 Z
           M824 303 C837 325 856 337 883 338 C857 354 823 342 807 316 C790 288 798 254 821 236 C812 257 812 282 824 303 Z"
        fill="url(#accentGrad)" opacity="0.16" filter="url(#glyphGlow)"/>

  <rect x="512" y="236" width="256" height="34" rx="17" ry="17"
        fill="#EEF3FF" stroke="#FFFFFF" stroke-width="1.2"/>
  <text x="640" y="258" width="230" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13"
        font-weight="700" letter-spacing="2.4" fill="#5B6F9B">EXECUTIVE SUMMARY</text>

  <text x="640" y="344" width="560" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="44"
        font-weight="700" fill="#172033">
    <tspan x="640" dy="0">Focus creates momentum.</tspan>
  </text>

  <rect x="504" y="379" width="272" height="4" rx="2" ry="2" fill="url(#accentGrad)"/>

  <text x="640" y="430" width="520" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="21"
        font-weight="400" line-height="1.35" fill="#5B667A">
    <tspan x="640" dy="0">A clean centered card gives one idea the room</tspan>
    <tspan x="640" dy="30">to land before the next section begins.</tspan>
  </text>

  <circle cx="640" cy="506" r="4" fill="#7C5CFF" opacity="0.55"/>
  <circle cx="662" cy="506" r="4" fill="#7C5CFF" opacity="0.24"/>
  <circle cx="618" cy="506" r="4" fill="#7C5CFF" opacity="0.24"/>
</svg>
```

## Avoid in this skill
- ❌ Busy multi-card grids; the visual power comes from one centered object and generous negative space
- ❌ Hard black shadows; use soft, low-opacity neumorphic shadows so the card feels elevated but quiet
- ❌ Edge-to-edge text blocks; keep all copy inside a narrow centered column within the card
- ❌ Placing filters on `<line>` elements; use filtered rects/paths for glows and shadows instead
- ❌ Text without explicit `width`; every `<text>` needs a width for predictable PowerPoint rendering

## Composition notes
- Keep the card around 52–58% of slide width and 48–55% of slide height, centered both horizontally and vertically.
- Reserve the upper third of the card for a small label or section cue, the middle for the main takeaway, and the lower third for supporting copy.
- Use a pale background and only one saturated accent gradient so the layout feels premium, not decorative.
- Background blobs should sit near corners and remain very low contrast; the card and headline must be the only true focal points.