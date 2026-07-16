# SVG Recipe — Windowed Slide Show Configurator (Split-Screen Optimized)

## Visual mechanism
Create a premium desktop mockup showing a single monitor split into two snapped windows: meeting app on the left, PowerPoint slide show on the right. The slide visually explains the workflow while the actual deck-generation pipeline should also set PowerPoint’s file-level “Browsed by an individual / windowed” presentation property.

## SVG primitives needed
- 1× full-canvas `<rect>` for the Windows-style desktop gradient background
- 1× bottom `<rect>` for the translucent taskbar
- 2× large rounded `<rect>` shapes for the left and right application windows
- 2× title-bar `<rect>` shapes for meeting app and PowerPoint window chrome
- Multiple small `<circle>` controls for window buttons, avatars, status dots, and UI indicators
- Multiple `<rect>` shapes for video tiles, chat panels, slide thumbnails, and instruction cards
- Several `<path>` icons for camera, microphone, presentation, arrowheads, snap-highlight brackets, and decorative desktop glows
- 3× `<line>` shapes for snap divider and instructional callouts
- Multiple `<text width="...">` blocks for title, app labels, workflow steps, and annotations
- 2× `<linearGradient>` fills for desktop background and PowerPoint slide surface
- 1× `<radialGradient>` for subtle center glow behind the split-screen area
- 1× `<filter id="windowShadow">` using feOffset + feGaussianBlur + feMerge for elevated app windows
- 1× `<filter id="softGlow">` using feGaussianBlur for snap-edge glow and emphasis shapes

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="desktopGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0476D9"/>
      <stop offset="52%" stop-color="#0067B8"/>
      <stop offset="100%" stop-color="#003E7E"/>
    </linearGradient>
    <radialGradient id="centerGlow" cx="50%" cy="45%" r="58%">
      <stop offset="0%" stop-color="#6BD6FF" stop-opacity="0.28"/>
      <stop offset="65%" stop-color="#0078D7" stop-opacity="0.06"/>
      <stop offset="100%" stop-color="#003E7E" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="slideGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFF4EE"/>
      <stop offset="45%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#FFE0D4"/>
    </linearGradient>
    <filter id="windowShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="12" result="off"/>
      <feGaussianBlur in="off" stdDeviation="16" result="blur"/>
      <feColorMatrix in="blur" type="matrix" values="0 0 0 0 0  0 0 0 0 0.1  0 0 0 0 0.22  0 0 0 .30 0" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#desktopGrad)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#centerGlow)"/>
  <path d="M83 92 C150 42, 230 48, 286 110 C205 102, 146 123, 83 92 Z" fill="#70D7FF" opacity="0.18" filter="url(#softGlow)"/>
  <path d="M1030 92 C1112 30, 1200 54, 1238 126 C1168 108, 1095 118, 1030 92 Z" fill="#B7E9FF" opacity="0.14" filter="url(#softGlow)"/>

  <text x="64" y="58" width="760" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="30" font-weight="700" fill="#FFFFFF">Split-screen presentation setup</text>
  <text x="64" y="89" width="780" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#DDF3FF">Windowed slide show mode keeps PowerPoint resizable so your meeting app stays visible.</text>

  <line x1="640" y1="118" x2="640" y2="642" stroke="#B9EAFF" stroke-width="2" stroke-dasharray="10 10" opacity="0.75"/>
  <rect x="624" y="310" width="32" height="100" rx="16" fill="#B9EAFF" opacity="0.22" filter="url(#softGlow)"/>
  <text x="604" y="288" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="700" fill="#DDF3FF" text-anchor="middle">Snap edge</text>

  <!-- Left: meeting app window -->
  <rect x="58" y="126" width="548" height="484" rx="22" fill="#FFFFFF" stroke="#C7D8E8" stroke-width="1.2" filter="url(#windowShadow)"/>
  <rect x="58" y="126" width="548" height="46" rx="22" fill="#F4F7FA"/>
  <rect x="58" y="154" width="548" height="22" fill="#F4F7FA"/>
  <circle cx="88" cy="149" r="6" fill="#FF5F57"/>
  <circle cx="108" cy="149" r="6" fill="#FFBD2E"/>
  <circle cx="128" cy="149" r="6" fill="#28C840"/>
  <path d="M170 141 h18 a4 4 0 0 1 4 4 v10 a4 4 0 0 1 -4 4 h-18 a4 4 0 0 1 -4 -4 v-10 a4 4 0 0 1 4 -4 Z M193 147 l13 -7 v20 l-13 -7 Z" fill="#2F80ED"/>
  <text x="216" y="155" width="250" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#263238">Meeting app</text>

  <rect x="84" y="196" width="230" height="154" rx="16" fill="#17202B"/>
  <circle cx="164" cy="250" r="34" fill="#35A7FF"/>
  <text x="151" y="263" width="40" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="30" font-weight="700" fill="#FFFFFF">A</text>
  <rect x="100" y="314" width="80" height="16" rx="8" fill="#FFFFFF" opacity="0.18"/>
  <circle cx="286" cy="322" r="8" fill="#00D26A"/>

  <rect x="330" y="196" width="230" height="154" rx="16" fill="#22313F"/>
  <circle cx="410" cy="250" r="34" fill="#9B7CFF"/>
  <text x="397" y="263" width="40" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="30" font-weight="700" fill="#FFFFFF">M</text>
  <rect x="346" y="314" width="94" height="16" rx="8" fill="#FFFFFF" opacity="0.18"/>
  <circle cx="532" cy="322" r="8" fill="#00D26A"/>

  <rect x="84" y="366" width="230" height="134" rx="16" fill="#EEF4F8"/>
  <path d="M168 410 h62 a12 12 0 0 1 12 12 v26 a12 12 0 0 1 -12 12 h-62 a12 12 0 0 1 -12 -12 v-26 a12 12 0 0 1 12 -12 Z M245 426 l28 -16 v58 l-28 -16 Z" fill="#A9BAC8"/>
  <text x="142" y="482" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="600" fill="#78909C" text-anchor="middle">Screen share preview</text>

  <rect x="330" y="366" width="230" height="134" rx="16" fill="#F7FAFC"/>
  <text x="354" y="398" width="160" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#263238">Chat + audience</text>
  <rect x="354" y="418" width="152" height="12" rx="6" fill="#DDE7EF"/>
  <rect x="354" y="442" width="112" height="12" rx="6" fill="#DDE7EF"/>
  <rect x="354" y="466" width="178" height="12" rx="6" fill="#DDE7EF"/>

  <rect x="108" y="530" width="390" height="44" rx="22" fill="#111820" opacity="0.94"/>
  <path d="M150 542 h26 a8 8 0 0 1 8 8 v6 a8 8 0 0 1 -8 8 h-26 a8 8 0 0 1 -8 -8 v-6 a8 8 0 0 1 8 -8 Z M185 548 l16 -9 v32 l-16 -9 Z" fill="#5BC7FF"/>
  <path d="M252 541 a12 12 0 0 1 24 0 v14 a12 12 0 0 1 -24 0 Z M244 556 c2 20 40 20 42 0" fill="none" stroke="#5BC7FF" stroke-width="4" stroke-linecap="round"/>
  <circle cx="358" cy="552" r="15" fill="#E53935"/>
  <text x="386" y="558" width="90" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" fill="#FFFFFF">Live meeting</text>

  <!-- Right: PowerPoint windowed slide show -->
  <rect x="674" y="126" width="548" height="484" rx="22" fill="#FFFFFF" stroke="#D2C9C4" stroke-width="1.2" filter="url(#windowShadow)"/>
  <rect x="674" y="126" width="548" height="46" rx="22" fill="#C43E1C"/>
  <rect x="674" y="154" width="548" height="22" fill="#C43E1C"/>
  <circle cx="704" cy="149" r="6" fill="#FFD4C8" opacity="0.8"/>
  <circle cx="724" cy="149" r="6" fill="#FFD4C8" opacity="0.8"/>
  <circle cx="744" cy="149" r="6" fill="#FFD4C8" opacity="0.8"/>
  <path d="M785 137 h28 a9 9 0 0 1 9 9 v14 a9 9 0 0 1 -9 9 h-28 Z M776 143 h20 v21 h-20 a8 8 0 0 1 -8 -8 v-5 a8 8 0 0 1 8 -8 Z" fill="#FFFFFF"/>
  <text x="840" y="155" width="300" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#FFFFFF">PowerPoint Slide Show — Windowed</text>

  <rect x="704" y="202" width="320" height="230" rx="18" fill="url(#slideGrad)" stroke="#F0B09B" stroke-width="1"/>
  <text x="732" y="246" width="245" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="800" fill="#B73A1B">Presenter view stays flexible</text>
  <text x="734" y="282" width="240" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#5D4037">Press F5 and the show opens inside this resizable window instead of taking over the monitor.</text>
  <rect x="734" y="320" width="92" height="68" rx="12" fill="#F26B3A" opacity="0.16"/>
  <rect x="846" y="320" width="92" height="68" rx="12" fill="#F26B3A" opacity="0.16"/>
  <rect x="958" y="320" width="36" height="68" rx="12" fill="#F26B3A" opacity="0.16"/>
  <path d="M759 346 h35 v10 h-35 Z M771 332 h12 v38 h-12 Z" fill="#C43E1C"/>
  <path d="M872 338 h40 v8 h-40 Z M872 358 h40 v8 h-40 Z M884 326 h8 v52 h-8 Z" fill="#C43E1C"/>
  <path d="M970 338 l16 16 -16 16 Z" fill="#C43E1C"/>

  <rect x="1048" y="202" width="138" height="230" rx="18" fill="#F8F3F1" stroke="#E7D1C8"/>
  <text x="1070" y="232" width="94" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" fill="#6D4C41">Slide queue</text>
  <rect x="1070" y="254" width="88" height="50" rx="7" fill="#FFFFFF" stroke="#F26B3A" stroke-width="2"/>
  <rect x="1070" y="318" width="88" height="50" rx="7" fill="#FFFFFF" stroke="#E1C6BC"/>
  <rect x="1070" y="382" width="88" height="24" rx="7" fill="#FFFFFF" stroke="#E1C6BC"/>

  <rect x="704" y="458" width="482" height="92" rx="20" fill="#FFF7F4" stroke="#F2C5B6"/>
  <circle cx="744" cy="504" r="22" fill="#C43E1C"/>
  <text x="735" y="513" width="22" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="25" font-weight="800" fill="#FFFFFF">1</text>
  <text x="780" y="492" width="370" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="800" fill="#3E2723">Drag this window to the right half</text>
  <text x="780" y="520" width="365" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#6D4C41">Keep Zoom/Teams snapped left, then present without losing chat or participant video.</text>

  <line x1="575" y1="484" x2="674" y2="484" stroke="#DDF3FF" stroke-width="3" stroke-linecap="round"/>
  <path d="M674 484 l-18 -10 v20 Z" fill="#DDF3FF"/>
  <text x="548" y="464" width="180" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="700" fill="#FFFFFF">Side-by-side workflow</text>

  <rect x="0" y="660" width="1280" height="60" fill="#071B2E" opacity="0.62"/>
  <circle cx="42" cy="690" r="13" fill="#20C997"/>
  <rect x="78" y="678" width="138" height="24" rx="12" fill="#FFFFFF" opacity="0.15"/>
  <rect x="234" y="678" width="138" height="24" rx="12" fill="#FFFFFF" opacity="0.15"/>
  <rect x="1044" y="678" width="164" height="24" rx="12" fill="#FFFFFF" opacity="0.15"/>
  <text x="82" y="695" width="130" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#E7F7FF">Meeting app</text>
  <text x="238" y="695" width="130" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#E7F7FF">PowerPoint</text>
  <text x="1048" y="695" width="155" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#E7F7FF">Windowed show ready</text>
</svg>
```

## Avoid in this skill
- ❌ Do not try to express the PowerPoint `presProps.xml` / `<p:browse>` setting inside SVG; SVG can only render the instructional mockup, not alter deck package properties.
- ❌ Avoid `<foreignObject>` for embedding HTML-like desktop UI; build the mock operating-system interface with editable SVG rectangles, paths, circles, and text.
- ❌ Avoid `clip-path` on rectangles or groups for rounded windows; use native `<rect rx="...">` instead so PowerPoint keeps shapes editable.
- ❌ Avoid arrow markers on `<path>` callouts; draw callout shafts with `<line>` and arrowheads with small filled `<path>` triangles.
- ❌ Avoid relying on emoji icons for Zoom, Teams, or PowerPoint; use simple vector paths so the result is consistent across Windows and PowerPoint versions.

## Composition notes
- Keep the layout a true 50/50 split: meeting controls and audience context on the left, PowerPoint windowed slide show on the right.
- Use a strong central dashed divider and soft glow to communicate Windows Snap Assist without adding clutter.
- Preserve generous desktop margins around both app windows; the negative space makes the mockup feel like an OS-level workflow rather than a flat chart.
- Use blue/cyan for the desktop and meeting side, then PowerPoint orange for the presentation side to create an immediate color-coded workflow.