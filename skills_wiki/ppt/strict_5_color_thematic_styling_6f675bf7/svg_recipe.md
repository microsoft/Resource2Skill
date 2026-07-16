# SVG Recipe — Strict 5-Color Thematic Styling

## Visual mechanism
Build the entire slide from one locked 5-color palette and assign each color a fixed semantic role: ambient background, structural mid-tone, dark contrast, primary accent, and highlight accent. The premium look comes from disciplined repetition of the same five colors across illustration, typography, shadows, and callouts—never introducing “almost matching” extras.

## SVG primitives needed
- 1× `<rect>` for the full-slide background in the light palette color
- 20× `<line>` for window mullions, chair ribs, laptop details, and icon bars using only palette strokes
- 12× `<rect>` for window panes, laptop screen, logo panel, corner tag, and palette swatches
- 14× `<path>` for the conference table, chairs, laptop base, folded corner, PowerPoint-style icon, and translucent echo cards
- 2× `<ellipse>` for subtle tabletop and laptop shadows
- 5× `<text>` for the large episode number, corner letter, palette label, and logo letter
- 2× `<filter>` using `feOffset`, `feGaussianBlur`, and `feMerge` for editable soft shadows on shapes/text
- 2× `<linearGradient>` using palette colors only for controlled depth without breaking color harmony

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <!-- Locked 5-color palette:
      mintLight #9ADCCB, mintMid #5ABEA7, deepTeal #0B5F4E,
      powerRed #D84324, lemonYellow #FFD84D
    -->
    <linearGradient id="mintDepth" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#9ADCCB"/>
      <stop offset="1" stop-color="#5ABEA7"/>
    </linearGradient>
    <linearGradient id="foldDepth" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#FFD84D"/>
      <stop offset="1" stop-color="#D84324"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="8" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="7" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="smallShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="4" dy="5" result="off"/>
      <feGaussianBlur in="off" stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Ambient conference-room background: all colors come from the 5-color system -->
  <rect x="0" y="0" width="1280" height="720" fill="#9ADCCB"/>
  <rect x="0" y="0" width="1280" height="720" fill="#5ABEA7" opacity="0.22"/>

  <!-- Tall window grid -->
  <g opacity="0.55">
    <rect x="-28" y="24" width="330" height="490" fill="none" stroke="#5ABEA7" stroke-width="10"/>
    <line x1="42" y1="24" x2="42" y2="514" stroke="#5ABEA7" stroke-width="8"/>
    <line x1="-28" y1="148" x2="302" y2="148" stroke="#5ABEA7" stroke-width="8"/>
    <line x1="-28" y1="273" x2="302" y2="273" stroke="#5ABEA7" stroke-width="8"/>
    <line x1="-28" y1="406" x2="302" y2="406" stroke="#5ABEA7" stroke-width="8"/>

    <rect x="362" y="8" width="558" height="506" fill="none" stroke="#5ABEA7" stroke-width="10"/>
    <line x1="644" y1="24" x2="644" y2="514" stroke="#5ABEA7" stroke-width="10"/>
    <line x1="386" y1="148" x2="902" y2="148" stroke="#5ABEA7" stroke-width="8"/>
    <line x1="386" y1="273" x2="902" y2="273" stroke="#5ABEA7" stroke-width="8"/>
    <line x1="386" y1="406" x2="902" y2="406" stroke="#5ABEA7" stroke-width="8"/>

    <rect x="980" y="24" width="330" height="490" fill="none" stroke="#5ABEA7" stroke-width="10"/>
    <line x1="1244" y1="24" x2="1244" y2="514" stroke="#5ABEA7" stroke-width="8"/>
    <line x1="980" y1="148" x2="1310" y2="148" stroke="#5ABEA7" stroke-width="8"/>
    <line x1="980" y1="273" x2="1310" y2="273" stroke="#5ABEA7" stroke-width="8"/>
    <line x1="980" y1="406" x2="1310" y2="406" stroke="#5ABEA7" stroke-width="8"/>
  </g>

  <!-- Chairs and table, kept monochrome teal to reserve accents for the message -->
  <path d="M78 502 C84 420 89 354 96 348 L207 351 C216 352 225 424 250 506 Z" fill="#0B5F4E" opacity="0.72" filter="url(#smallShadow)"/>
  <path d="M1030 506 C1054 421 1063 354 1074 352 L1184 347 C1190 348 1196 419 1205 502 Z" fill="#0B5F4E" opacity="0.72" filter="url(#smallShadow)"/>
  <g opacity="0.46">
    <line x1="84" y1="376" x2="219" y2="378" stroke="#9ADCCB" stroke-width="5"/>
    <line x1="82" y1="401" x2="226" y2="403" stroke="#9ADCCB" stroke-width="5"/>
    <line x1="83" y1="427" x2="235" y2="430" stroke="#9ADCCB" stroke-width="5"/>
    <line x1="91" y1="454" x2="244" y2="456" stroke="#9ADCCB" stroke-width="5"/>
    <line x1="1063" y1="380" x2="1192" y2="376" stroke="#9ADCCB" stroke-width="5"/>
    <line x1="1056" y1="405" x2="1197" y2="401" stroke="#9ADCCB" stroke-width="5"/>
    <line x1="1049" y1="431" x2="1200" y2="427" stroke="#9ADCCB" stroke-width="5"/>
    <line x1="1042" y1="458" x2="1195" y2="454" stroke="#9ADCCB" stroke-width="5"/>
  </g>
  <path d="M0 548 C230 486 410 462 640 462 C870 462 1035 486 1280 548 L1280 720 L0 720 Z" fill="url(#mintDepth)" opacity="0.88"/>
  <ellipse cx="640" cy="674" rx="300" ry="32" fill="#0B5F4E" opacity="0.20"/>

  <!-- Laptop silhouette -->
  <rect x="438" y="328" width="420" height="280" rx="14" fill="#9ADCCB" stroke="#0B5F4E" stroke-width="2" opacity="0.72"/>
  <rect x="458" y="350" width="380" height="232" fill="#9ADCCB" stroke="#5ABEA7" stroke-width="8" opacity="0.95"/>
  <path d="M438 608 L842 608 L895 670 L386 670 Z" fill="#5ABEA7" opacity="0.82" filter="url(#smallShadow)"/>
  <path d="M492 612 L788 612 L824 645 L454 645 Z" fill="#0B5F4E" opacity="0.68"/>
  <rect x="559" y="648" width="166" height="20" rx="3" fill="#0B5F4E" opacity="0.28"/>

  <!-- PowerPoint-like focal icon with echo cards -->
  <g opacity="0.34" filter="url(#smallShadow)">
    <path d="M454 264 L586 238 L586 422 L454 389 Z" fill="#FFD84D"/>
    <rect x="570" y="268" width="250" height="138" rx="6" fill="none" stroke="#D84324" stroke-width="5"/>
    <text x="484" y="373" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="72" font-weight="700" fill="#9ADCCB">P</text>
  </g>
  <g opacity="0.32">
    <path d="M418 286 L552 260 L552 414 L418 389 Z" fill="#FFD84D"/>
    <rect x="698" y="292" width="190" height="92" rx="4" fill="none" stroke="#D84324" stroke-width="4"/>
  </g>
  <g filter="url(#softShadow)">
    <rect x="650" y="238" width="128" height="190" rx="7" fill="#9ADCCB" stroke="#D84324" stroke-width="6"/>
    <path d="M520 232 L660 208 L660 462 L520 435 Z" fill="#D84324"/>
    <text x="566" y="381" width="78" font-family="Segoe UI, Microsoft YaHei" font-size="130" font-weight="800" fill="#9ADCCB">P</text>
    <path d="M694 263 C718 266 734 282 738 306 L694 306 Z" fill="#D84324"/>
    <path d="M739 315 C736 337 719 354 694 357 L694 315 Z" fill="#D84324"/>
    <line x1="674" y1="366" x2="744" y2="366" stroke="#D84324" stroke-width="9"/>
    <line x1="674" y1="389" x2="744" y2="389" stroke="#D84324" stroke-width="9"/>
  </g>

  <!-- Episode number / highlight accent -->
  <text x="48" y="674" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="198" font-weight="900" fill="#FFD84D" filter="url(#softShadow)">#4</text>

  <!-- Folded-corner brand tag -->
  <path d="M1146 0 L1280 0 L1280 132 C1252 86 1201 38 1146 0 Z" fill="url(#foldDepth)"/>
  <path d="M1184 91 L1280 132 C1255 86 1208 39 1146 0 C1176 30 1189 58 1184 91 Z" fill="#9ADCCB" filter="url(#smallShadow)"/>
  <text x="1234" y="58" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="900" fill="#0B5F4E">L</text>

  <!-- Palette audit strip: demonstrates the strict five-color source -->
  <g transform="translate(912 642)">
    <rect x="0" y="0" width="238" height="42" rx="21" fill="#9ADCCB" stroke="#0B5F4E" stroke-width="2" opacity="0.72"/>
    <rect x="12" y="10" width="24" height="22" rx="4" fill="#9ADCCB" stroke="#0B5F4E" stroke-width="1"/>
    <rect x="42" y="10" width="24" height="22" rx="4" fill="#5ABEA7"/>
    <rect x="72" y="10" width="24" height="22" rx="4" fill="#0B5F4E"/>
    <rect x="102" y="10" width="24" height="22" rx="4" fill="#D84324"/>
    <rect x="132" y="10" width="24" height="22" rx="4" fill="#FFD84D"/>
    <text x="166" y="27" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#0B5F4E">5-COLOR</text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Introducing a sixth “convenient” color for shadows, outlines, white fills, or labels; use opacity of an existing palette color instead.
- ❌ Random gradients with off-palette stop colors; if using gradients, both stops should be from the locked palette.
- ❌ Full-color photos unless they are intentionally tinted or visually dominated by the selected palette.
- ❌ Mixing multiple accent colors at equal strength; reserve the brightest palette color for one or two focal moments only.
- ❌ Using default black text when the palette already contains a dark contrast color.

## Composition notes
- Keep 70–80% of the slide in the light/medium palette colors so vivid accents feel intentional rather than noisy.
- Use the darkest color for legibility, depth, and structural anchors; do not scatter it randomly.
- Let one accent own the focal object and one accent own the callout/number—this creates hierarchy while staying harmonious.
- Add a small swatch audit strip when teaching or systematizing the theme; it signals that every visible element belongs to the same palette.