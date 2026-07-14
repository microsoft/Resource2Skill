# SVG Recipe — Central UI Wireframe

## Visual mechanism
A single oversized soft-UI card sits in the center of a dark, cool-toned canvas, using layered blurred shadows, subtle bevel strokes, and low-contrast gradients to create a neumorphic mockup. Inside the card, a large media/content placeholder, progress slider, and compact labels suggest a featured product UI without requiring detailed data.

## SVG primitives needed
- 18× `<rect>` for the background, central shell, inset media area, placeholder blocks, slider track, label pill, and small UI modules
- 7× `<circle>` for traffic-light controls, play button, slider handle, and small status dots
- 4× `<path>` for ambient background blobs, a play glyph, and simplified chart/content strokes
- 8× `<line>` for wireframe text rows and slider/progress strokes
- 7× `<text>` with explicit `width` attributes for headline, metadata, timestamps, and action label
- 4× `<linearGradient>` for dark background, card surface, media inset, and progress color
- 1× `<radialGradient>` for a soft cyan ambient glow
- 3× `<filter>` definitions using `feOffset`, `feGaussianBlur`, and `feMerge` for soft neumorphic shadows and glows

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0" stop-color="#101823"/>
      <stop offset="0.55" stop-color="#182334"/>
      <stop offset="1" stop-color="#0b1018"/>
    </linearGradient>
    <linearGradient id="cardGrad" x1="360" y1="120" x2="920" y2="610">
      <stop offset="0" stop-color="#253244"/>
      <stop offset="0.52" stop-color="#1b2636"/>
      <stop offset="1" stop-color="#121a27"/>
    </linearGradient>
    <linearGradient id="screenGrad" x1="410" y1="190" x2="870" y2="430">
      <stop offset="0" stop-color="#111926"/>
      <stop offset="0.65" stop-color="#172335"/>
      <stop offset="1" stop-color="#0c121b"/>
    </linearGradient>
    <linearGradient id="progressGrad" x1="430" y1="508" x2="850" y2="508">
      <stop offset="0" stop-color="#44f0ff"/>
      <stop offset="0.55" stop-color="#5f8cff"/>
      <stop offset="1" stop-color="#9b6bff"/>
    </linearGradient>
    <radialGradient id="cyanGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#3deaff" stop-opacity="0.34"/>
      <stop offset="0.65" stop-color="#3deaff" stop-opacity="0.08"/>
      <stop offset="1" stop-color="#3deaff" stop-opacity="0"/>
    </radialGradient>
    <filter id="deepShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="18" dy="24" result="off"/>
      <feGaussianBlur in="off" stdDeviation="22" result="blur"/>
      <feFlood flood-color="#050912" flood-opacity="0.72" result="color"/>
      <feComposite in="color" in2="blur" operator="in" result="shadow"/>
      <feMerge><feMergeNode in="shadow"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="topHighlight" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="-10" dy="-12" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feFlood flood-color="#6b89ad" flood-opacity="0.22" result="color"/>
      <feComposite in="color" in2="blur" operator="in" result="light"/>
      <feMerge><feMergeNode in="light"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="18" result="glow"/>
      <feMerge><feMergeNode in="glow"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <ellipse cx="300" cy="155" rx="260" ry="115" fill="url(#cyanGlow)" opacity="0.62"/>
  <ellipse cx="960" cy="590" rx="300" ry="145" fill="url(#cyanGlow)" opacity="0.36"/>
  <path d="M980 105 C1075 80 1160 115 1190 185 C1220 255 1165 315 1076 300 C990 285 930 230 940 170 C945 138 956 114 980 105 Z" fill="#243b56" opacity="0.22" filter="url(#softGlow)"/>
  <path d="M92 520 C165 470 260 470 310 535 C355 596 300 655 208 650 C120 645 48 588 92 520 Z" fill="#2d4260" opacity="0.18" filter="url(#softGlow)"/>

  <text x="110" y="98" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#eaf4ff">Central UI Wireframe</text>
  <text x="110" y="132" width="470" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#8fa4bb">Soft neumorphic media module for feature reveals and metric previews</text>

  <rect x="342" y="114" width="596" height="492" rx="44" fill="#09101a" opacity="0.52" filter="url(#deepShadow)"/>
  <rect x="342" y="114" width="596" height="492" rx="44" fill="url(#cardGrad)" stroke="#314056" stroke-width="1.5" filter="url(#topHighlight)"/>
  <rect x="365" y="137" width="550" height="446" rx="34" fill="none" stroke="#647892" stroke-opacity="0.20" stroke-width="1"/>

  <circle cx="410" cy="165" r="7" fill="#ff6c7a" opacity="0.88"/>
  <circle cx="434" cy="165" r="7" fill="#ffd166" opacity="0.84"/>
  <circle cx="458" cy="165" r="7" fill="#4de0a7" opacity="0.84"/>
  <text x="682" y="171" width="185" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#9fb1c7" text-anchor="end">FEATURED PREVIEW</text>

  <rect x="405" y="196" width="470" height="238" rx="28" fill="#080d14" opacity="0.55"/>
  <rect x="405" y="196" width="470" height="238" rx="28" fill="url(#screenGrad)" stroke="#3b4d67" stroke-opacity="0.65" stroke-width="1.2"/>
  <rect x="429" y="220" width="212" height="148" rx="18" fill="#202e40" stroke="#50647d" stroke-opacity="0.42"/>
  <rect x="449" y="242" width="92" height="12" rx="6" fill="#7086a1" opacity="0.38"/>
  <rect x="449" y="267" width="150" height="9" rx="4.5" fill="#4f627b" opacity="0.30"/>
  <rect x="449" y="288" width="126" height="9" rx="4.5" fill="#4f627b" opacity="0.22"/>
  <path d="M459 340 C490 302 523 310 546 332 C567 352 592 323 621 346 L621 368 L459 368 Z" fill="#44f0ff" opacity="0.20"/>

  <rect x="674" y="222" width="162" height="42" rx="14" fill="#202d3e" stroke="#52647a" stroke-opacity="0.28"/>
  <circle cx="700" cy="243" r="8" fill="#44f0ff" opacity="0.85"/>
  <line x1="722" y1="238" x2="808" y2="238" stroke="#8aa0b8" stroke-width="5" stroke-linecap="round" opacity="0.42"/>
  <line x1="722" y1="250" x2="782" y2="250" stroke="#647890" stroke-width="4" stroke-linecap="round" opacity="0.28"/>
  <rect x="674" y="286" width="162" height="102" rx="18" fill="#1c293a" stroke="#52647a" stroke-opacity="0.25"/>
  <path d="M694 358 L718 330 L742 344 L768 310 L794 337 L816 318" fill="none" stroke="#6f8cff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" opacity="0.72"/>
  <line x1="694" y1="371" x2="816" y2="371" stroke="#63758a" stroke-width="4" stroke-linecap="round" opacity="0.28"/>

  <circle cx="640" cy="315" r="42" fill="#111925" filter="url(#deepShadow)"/>
  <circle cx="640" cy="315" r="39" fill="#223044" stroke="#536981" stroke-opacity="0.55"/>
  <path d="M628 294 L628 336 L662 315 Z" fill="#eaf8ff" opacity="0.94"/>

  <text x="405" y="468" width="310" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#e7f0fa">Product demo interface</text>
  <text x="405" y="494" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#8fa4bb">Wireframe state · synced preview</text>
  <text x="807" y="492" width="68" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#9cafc4" text-anchor="end">03:24</text>

  <line x1="430" y1="523" x2="850" y2="523" stroke="#0b111b" stroke-width="13" stroke-linecap="round"/>
  <line x1="430" y1="523" x2="666" y2="523" stroke="url(#progressGrad)" stroke-width="9" stroke-linecap="round"/>
  <circle cx="666" cy="523" r="13" fill="#26384f" stroke="#7df3ff" stroke-width="3" filter="url(#topHighlight)"/>

  <rect x="405" y="548" width="132" height="34" rx="17" fill="#223147" stroke="#61738a" stroke-opacity="0.28"/>
  <circle cx="426" cy="565" r="5" fill="#4de0a7"/>
  <text x="441" y="571" width="82" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#cfe0f2">Live Sync</text>
  <rect x="724" y="548" width="151" height="34" rx="17" fill="#1b2636" stroke="#44f0ff" stroke-opacity="0.35"/>
  <text x="747" y="571" width="106" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#dffbff">Launch View</text>
</svg>
```

## Avoid in this skill
- ❌ Real CSS `box-shadow` or CSS neumorphism; build the soft shadows with duplicated shapes and SVG filters instead
- ❌ Applying filters to `<line>` elements for the slider; use thick rounded lines without filters, then add a filtered circle handle
- ❌ Using `<mask>` to create inset shadows; fake inset depth with dark inner rectangles, gradient fills, and low-opacity strokes
- ❌ Overloading the wireframe with dense charts or tables; this technique depends on a calm, central hero UI

## Composition notes
- Keep the main card centered and large, occupying roughly 45–50% of slide width and 65–70% of slide height.
- Preserve generous negative space around the mockup so the soft shadows and ambient glows remain visible.
- Use cool blue-gray surfaces with cyan/purple accents only on the active progress, status dot, or primary action.
- Put optional headline text in the upper-left or upper-center; do not compete with the central UI module.