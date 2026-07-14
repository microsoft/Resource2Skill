# SVG Recipe — Fragmented Tech Glitch Bar

## Visual mechanism
A compact divider is built from many sharp-edged, horizontally aligned rectangles with varied widths, offsets, and colors, creating the sensation of corrupted data packets moving across the slide. The fragmented bar works best as a kinetic underline or section divider beneath bold tech typography.

## SVG primitives needed
- 1× `<rect>` for the clean slide background
- 3× `<linearGradient>` for subtle background wash, title accent, and faint bar glow
- 2× `<filter>` definitions for soft glow and premium drop shadow
- 2× `<text>` blocks for the main title and spaced subtitle
- 1× `<rect>` behind the bar as a low-opacity luminous base rail
- 50–70× small `<rect>` fragments for the main glitch/data-stream bar
- 8–12× ultra-thin `<rect>` fragments for high-speed scanline accents
- 6–10× tiny `<rect>` pixels around the bar edges for digital debris

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="58%" stop-color="#FAFAFF"/>
      <stop offset="100%" stop-color="#F2F0FA"/>
    </linearGradient>

    <linearGradient id="titleGrad" x1="360" y1="0" x2="920" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#33165F"/>
      <stop offset="55%" stop-color="#512378"/>
      <stop offset="100%" stop-color="#1A237E"/>
    </linearGradient>

    <linearGradient id="barGlow" x1="250" y1="0" x2="1040" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#512378" stop-opacity="0"/>
      <stop offset="22%" stop-color="#D81B60" stop-opacity="0.28"/>
      <stop offset="56%" stop-color="#FF9800" stop-opacity="0.22"/>
      <stop offset="88%" stop-color="#1A237E" stop-opacity="0.24"/>
      <stop offset="100%" stop-color="#512378" stop-opacity="0"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-30%" width="140%" height="180%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="hotGlow" x="-25%" y="-80%" width="150%" height="260%">
      <feGaussianBlur stdDeviation="5"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <text x="640" y="220" width="760" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="96" font-weight="800" letter-spacing="-3"
        fill="url(#titleGrad)">DATAFORGE 2026</text>

  <text x="640" y="278" width="720" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="700" letter-spacing="5"
        fill="#66636D">BUILD. SCALE. DISRUPT.</text>

  <rect x="245" y="354" width="790" height="88" rx="2" fill="url(#barGlow)" filter="url(#hotGlow)" opacity="0.85"/>

  <!-- high-speed scanline fragments above and below the main band -->
  <rect x="306" y="336" width="82" height="4" fill="#512378" opacity="0.70"/>
  <rect x="405" y="336" width="31" height="4" fill="#D81B60" opacity="0.90"/>
  <rect x="471" y="336" width="148" height="4" fill="#FF9800" opacity="0.65"/>
  <rect x="691" y="336" width="55" height="4" fill="#1A237E" opacity="0.75"/>
  <rect x="801" y="336" width="169" height="4" fill="#512378" opacity="0.45"/>
  <rect x="263" y="463" width="132" height="5" fill="#1A237E" opacity="0.55"/>
  <rect x="431" y="463" width="70" height="5" fill="#FF9800" opacity="0.80"/>
  <rect x="554" y="463" width="184" height="5" fill="#D81B60" opacity="0.55"/>
  <rect x="785" y="463" width="92" height="5" fill="#512378" opacity="0.75"/>
  <rect x="918" y="463" width="105" height="5" fill="#1A237E" opacity="0.60"/>

  <!-- row 1 -->
  <rect x="260" y="360" width="108" height="13" fill="#512378" filter="url(#softShadow)"/>
  <rect x="379" y="360" width="44" height="13" fill="#D81B60"/>
  <rect x="430" y="360" width="164" height="13" fill="#FF9800"/>
  <rect x="608" y="360" width="74" height="13" fill="#1A237E"/>
  <rect x="696" y="360" width="205" height="13" fill="#512378"/>
  <rect x="918" y="360" width="91" height="13" fill="#9E9E9E" opacity="0.78"/>

  <!-- row 2 -->
  <rect x="226" y="379" width="64" height="14" fill="#D81B60"/>
  <rect x="304" y="379" width="157" height="14" fill="#1A237E"/>
  <rect x="470" y="379" width="96" height="14" fill="#512378"/>
  <rect x="584" y="379" width="36" height="14" fill="#FF9800"/>
  <rect x="636" y="379" width="188" height="14" fill="#D81B60"/>
  <rect x="841" y="379" width="126" height="14" fill="#1A237E"/>
  <rect x="982" y="379" width="47" height="14" fill="#FF9800"/>

  <!-- row 3 -->
  <rect x="282" y="399" width="185" height="15" fill="#1A237E"/>
  <rect x="481" y="399" width="58" height="15" fill="#9E9E9E" opacity="0.72"/>
  <rect x="552" y="399" width="137" height="15" fill="#512378"/>
  <rect x="701" y="399" width="66" height="15" fill="#FF9800"/>
  <rect x="779" y="399" width="232" height="15" fill="#D81B60" filter="url(#softShadow)"/>

  <!-- row 4, densest core -->
  <rect x="250" y="421" width="38" height="17" fill="#FF9800"/>
  <rect x="296" y="421" width="112" height="17" fill="#512378"/>
  <rect x="418" y="421" width="71" height="17" fill="#D81B60"/>
  <rect x="501" y="421" width="206" height="17" fill="#1A237E"/>
  <rect x="719" y="421" width="33" height="17" fill="#9E9E9E" opacity="0.70"/>
  <rect x="766" y="421" width="119" height="17" fill="#FF9800"/>
  <rect x="896" y="421" width="157" height="17" fill="#512378"/>

  <!-- row 5 -->
  <rect x="321" y="445" width="76" height="13" fill="#512378"/>
  <rect x="409" y="445" width="171" height="13" fill="#FF9800"/>
  <rect x="592" y="445" width="49" height="13" fill="#D81B60"/>
  <rect x="656" y="445" width="128" height="13" fill="#1A237E"/>
  <rect x="802" y="445" width="64" height="13" fill="#512378"/>
  <rect x="884" y="445" width="121" height="13" fill="#D81B60"/>

  <!-- offset micro fragments and digital debris -->
  <rect x="214" y="366" width="18" height="8" fill="#512378" opacity="0.55"/>
  <rect x="238" y="392" width="12" height="12" fill="#FF9800" opacity="0.80"/>
  <rect x="1039" y="366" width="24" height="8" fill="#D81B60" opacity="0.60"/>
  <rect x="1069" y="392" width="15" height="15" fill="#1A237E" opacity="0.75"/>
  <rect x="221" y="441" width="30" height="7" fill="#1A237E" opacity="0.42"/>
  <rect x="1023" y="438" width="56" height="7" fill="#FF9800" opacity="0.58"/>
  <rect x="498" y="350" width="14" height="7" fill="#D81B60" opacity="0.65"/>
  <rect x="742" y="348" width="22" height="6" fill="#1A237E" opacity="0.48"/>

  <text x="640" y="525" width="640" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="600" letter-spacing="2"
        fill="#8A8492">FRAGMENTED DATA STREAM DIVIDER</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use one continuous rectangle as the underline; the effect depends on visible packet-like fragmentation.
- ❌ Do not randomize the vertical alignment too much; keep fragments locked to clear horizontal tracks so it reads as a deliberate tech bar.
- ❌ Do not use rounded corners on the fragments; sharp 90° edges create the digital/glitch aesthetic.
- ❌ Do not rely on `<pattern>`, `<mask>`, or clipped non-image shapes for the fragmentation; use individual editable rectangles.
- ❌ Do not make every fragment the same width or color; variation is what creates motion and energy.

## Composition notes
- Keep the top 45–55% of the slide calm and spacious so the fragmented bar feels like a deliberate anchor, not visual noise.
- Place the glitch bar directly under a title, between title/subtitle groups, or as a section divider near the lower third.
- Use 4–5 saturated brand colors plus one neutral gray; repeat colors irregularly to avoid a rainbow-strip look.
- Let the left and right edges of the bar be jagged with small debris fragments, while the center remains denser and more confident.