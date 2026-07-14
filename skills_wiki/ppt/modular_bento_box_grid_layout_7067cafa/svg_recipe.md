# SVG Recipe — Modular Bento Box Grid Layout

## Visual mechanism
A strict rounded-rectangle grid becomes dynamic by rotating the entire bento cluster, letting varied card spans feel editorial rather than dashboard-like. The left side holds a bold title lockup on a dark technical grid background, while the right side stacks image, accent, and text cards with identical gutters and radii.

## SVG primitives needed
- 1× `<rect>` for the full dark background
- 2× `<path>` for fine and major background grid overlays
- 1× `<radialGradient>` for a subtle vignette glow behind the bento cluster
- 1× `<linearGradient>` for the neon green title label
- 1× `<filter id="cardShadow">` applied to card rectangles for elevation
- 1× `<filter id="softGlow">` applied to the green title label
- 10× `<rect>` for rounded bento cards, title label, and image card bases
- 3× `<clipPath>` with rounded `<rect>` crops for image cards
- 3× `<image>` for editorial photo/product modules inside the bento grid
- 8× `<path>` for decorative waveform, radial ray, and texture details inside cards
- 18× `<text>` elements for title typography, card labels, captions, and arrow glyphs

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="clusterGlow" cx="74%" cy="48%" r="55%">
      <stop offset="0%" stop-color="#33384a" stop-opacity="0.52"/>
      <stop offset="55%" stop-color="#111827" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#07090f" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="limeLabel" x1="88" y1="370" x2="443" y2="532" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#d7ff36"/>
      <stop offset="100%" stop-color="#b7f52c"/>
    </linearGradient>
    <filter id="cardShadow" x="-15%" y="-15%" width="130%" height="130%">
      <feOffset dx="0" dy="16"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="5"/>
    </filter>
    <clipPath id="clipSpeaker" clipPathUnits="userSpaceOnUse">
      <rect x="590" y="190" width="255" height="420" rx="28" ry="28"/>
    </clipPath>
    <clipPath id="clipDevice" clipPathUnits="userSpaceOnUse">
      <rect x="850" y="160" width="278" height="216" rx="28" ry="28"/>
    </clipPath>
    <clipPath id="clipFamily" clipPathUnits="userSpaceOnUse">
      <rect x="1125" y="92" width="260" height="430" rx="28" ry="28"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#080a0f"/>
  <path d="M0 40H1280 M0 80H1280 M0 120H1280 M0 160H1280 M0 200H1280 M0 240H1280 M0 280H1280 M0 320H1280 M0 360H1280 M0 400H1280 M0 440H1280 M0 480H1280 M0 520H1280 M0 560H1280 M0 600H1280 M0 640H1280 M0 680H1280 M40 0V720 M80 0V720 M120 0V720 M160 0V720 M200 0V720 M240 0V720 M280 0V720 M320 0V720 M360 0V720 M400 0V720 M440 0V720 M480 0V720 M520 0V720 M560 0V720 M600 0V720 M640 0V720 M680 0V720 M720 0V720 M760 0V720 M800 0V720 M840 0V720 M880 0V720 M920 0V720 M960 0V720 M1000 0V720 M1040 0V720 M1080 0V720 M1120 0V720 M1160 0V720 M1200 0V720 M1240 0V720" stroke="#ffffff" stroke-opacity="0.08" stroke-width="1"/>
  <path d="M0 160H1280 M0 320H1280 M0 480H1280 M0 640H1280 M160 0V720 M320 0V720 M480 0V720 M640 0V720 M800 0V720 M960 0V720 M1120 0V720" stroke="#ffffff" stroke-opacity="0.13" stroke-width="1.2"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#clusterGlow)"/>

  <text x="92" y="338" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="138" font-weight="900" letter-spacing="8" fill="#f5f5f2">BENTO</text>
  <rect x="88" y="370" width="355" height="162" rx="6" fill="url(#limeLabel)" filter="url(#softGlow)"/>
  <text x="151" y="506" width="250" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="116" font-weight="900" letter-spacing="3" fill="#020202">GRIDS</text>

  <g transform="rotate(-13 900 360)">
    <rect x="540" y="20" width="390" height="130" rx="28" fill="#f5f3ef" filter="url(#cardShadow)"/>
    <text x="570" y="62" width="250" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="700" fill="#08080a">We will watch</text>
    <text x="570" y="92" width="250" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="700" fill="#08080a">and listen</text>
    <text x="570" y="132" width="125" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#111">Multimedia</text>
    <path d="M704 135 C712 102 719 96 726 135 S741 168 748 122 S763 58 770 136 S785 175 792 82 S807 44 814 135 S829 172 836 70 S851 28 858 134" fill="none" stroke="#d8d8d8" stroke-width="2" stroke-opacity="0.8"/>
    <text x="888" y="102" width="30" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" fill="#111">→</text>

    <rect x="945" y="-6" width="300" height="112" rx="26" fill="#1b2b21" filter="url(#cardShadow)"/>
    <image href="https://images.example.com/smart-home-reminder-green-desk-photo.jpg" x="945" y="-6" width="300" height="112" preserveAspectRatio="xMidYMid slice" opacity="0.72"/>
    <text x="972" y="73" width="140" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#ffffff">Reminders</text>

    <rect x="590" y="190" width="255" height="420" rx="28" fill="#07111f" filter="url(#cardShadow)"/>
    <image href="https://images.example.com/orange-smart-speaker-glowing-on-table.jpg" x="590" y="190" width="255" height="420" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipSpeaker)"/>
    <rect x="590" y="190" width="255" height="420" rx="28" fill="#00111f" opacity="0.28"/>
    <text x="620" y="248" width="205" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#ffffff">Help you stay</text>
    <text x="620" y="277" width="205" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#ffffff">connected</text>
    <text x="620" y="306" width="205" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#ffffff">with loved ones</text>
    <text x="650" y="586" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#ffffff">Call and messages</text>
    <text x="810" y="560" width="30" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="23" fill="#ffffff">→</text>

    <rect x="850" y="160" width="278" height="216" rx="28" fill="#e8ded0" filter="url(#cardShadow)"/>
    <image href="https://images.example.com/black-round-smart-speaker-minimal-table.jpg" x="850" y="160" width="278" height="216" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipDevice)"/>
    <rect x="850" y="160" width="278" height="216" rx="28" fill="#fff4e5" opacity="0.24"/>
    <text x="880" y="215" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#15110e">I’ll tune in at your</text>
    <text x="880" y="244" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#15110e">convenience</text>
    <text x="882" y="342" width="90" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#15110e">Настройки</text>
    <text x="1088" y="312" width="30" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="21" fill="#15110e">→</text>

    <rect x="1125" y="92" width="260" height="430" rx="28" fill="#3a2b27" filter="url(#cardShadow)"/>
    <image href="https://images.example.com/family-cooking-together-kitchen-no-identifiable-faces.jpg" x="1125" y="92" width="260" height="430" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipFamily)"/>
    <rect x="1125" y="92" width="260" height="430" rx="28" fill="#000000" opacity="0.22"/>
    <text x="1155" y="155" width="190" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#ffffff">I’ll be your family</text>
    <text x="1155" y="184" width="190" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#ffffff">best friend</text>
    <text x="1160" y="488" width="170" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#ffffff">Children and parents</text>

    <rect x="880" y="392" width="280" height="195" rx="28" fill="#ff4937" filter="url(#cardShadow)"/>
    <text x="910" y="446" width="200" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="23" font-weight="700" fill="#ffffff">Let’s surf</text>
    <text x="910" y="475" width="200" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="23" font-weight="700" fill="#ffffff">the internet</text>
    <text x="918" y="558" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#ffffff">Search the internet</text>
    <text x="1122" y="518" width="30" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="23" fill="#ffffff">→</text>

    <rect x="735" y="620" width="330" height="160" rx="28" fill="#55505e" filter="url(#cardShadow)"/>
    <text x="765" y="682" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#ffffff">I’ll think of</text>
    <text x="765" y="711" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#ffffff">what you ask</text>
    <path d="M915 638 L998 606 M920 650 L1022 640 M923 662 L1015 682 M920 674 L990 719 M905 645 L945 595 M900 664 L928 738 M940 636 L1060 585 M945 652 L1078 662 M946 671 L1048 735" stroke="#ffffff" stroke-opacity="0.65" stroke-width="1.4" stroke-dasharray="2 7" fill="none"/>

    <rect x="1070" y="565" width="300" height="165" rx="28" fill="#7431f6" filter="url(#cardShadow)"/>
    <text x="1100" y="625" width="245" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#ffffff">Let’s manage</text>
    <text x="1100" y="654" width="245" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#ffffff">a smart home together</text>
    <text x="1110" y="706" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#ffffff">Smart House</text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Irregular gutters; the rotated composition can be playful, but the cards themselves must still snap to a consistent grid.
- ❌ Sharp-corner rectangles; the bento language depends on generous, consistent radii.
- ❌ Clipping text or vector decorations with `clip-path`; use clipping only on `<image>` elements for reliable PowerPoint translation.
- ❌ A flat grid with all cards the same size; use at least one hero card, one wide card, and several smaller modules.
- ❌ Heavy outlines around every card; rely on contrast, color blocks, and soft shadows instead.

## Composition notes
- Keep the left 35–40% of the slide as title territory; the bento grid should visually “enter” from the right.
- Use one high-energy accent card or label, then balance it with dark, white, neutral, and photo-based cards.
- Maintain a single gutter value between cards before rotation; the tilt should not disturb the underlying modular math.
- Let some cards crop off the canvas edge to create keynote-style motion and scale rather than a static dashboard.