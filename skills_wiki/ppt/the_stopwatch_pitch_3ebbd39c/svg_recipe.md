# SVG Recipe — The Stopwatch Pitch

## Visual mechanism
A dramatic dark slide uses an oversized editable vector stopwatch as a scarcity cue, balanced by one concise, high-authority message on the right. The stopwatch is symbolic, polished with gradients and soft shadow, while the typography stays stark, bold, and minimal.

## SVG primitives needed
- 1× `<rect>` for the full-slide charcoal background
- 2× `<radialGradient>` / `<linearGradient>` for metallic stopwatch body and face depth
- 1× `<filter id="softShadow">` applied to the stopwatch body group elements
- 1× `<filter id="textGlow">` applied subtly to the countdown display
- 4× `<circle>` for stopwatch body, inner rim, face, and center pivot
- 3× `<rect>` for top plunger, stem, and side button blocks
- 3× `<path>` for rounded top crown, angled side crown, and translucent face highlight
- 24× `<line>` for minute ticks around the stopwatch face
- 2× `<line>` for stopwatch hands
- 4× `<text>` elements with explicit `width` for timer display, headline, subtitle, and small urgency label
- 1× `<line>` as a thin accent rule beside the headline

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bodyMetal" cx="38%" cy="28%" r="70%">
      <stop offset="0%" stop-color="#B8B8B8"/>
      <stop offset="45%" stop-color="#7F7F7F"/>
      <stop offset="100%" stop-color="#4E4E4E"/>
    </radialGradient>
    <radialGradient id="facePaper" cx="42%" cy="30%" r="72%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="70%" stop-color="#F2F2F0"/>
      <stop offset="100%" stop-color="#D8D8D4"/>
    </radialGradient>
    <linearGradient id="crownMetal" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#C9C9C9"/>
      <stop offset="55%" stop-color="#808080"/>
      <stop offset="100%" stop-color="#565656"/>
    </linearGradient>
    <linearGradient id="redAccent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FF4B4B"/>
      <stop offset="100%" stop-color="#FFB000"/>
    </linearGradient>
    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="16"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="textGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2.5"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#282828"/>

  <g transform="translate(105 104)">
    <rect x="190" y="0" width="58" height="58" rx="13" fill="url(#crownMetal)"/>
    <path d="M158 42 C158 25 174 17 199 17 L239 17 C264 17 280 25 280 42 L280 76 L158 76 Z" fill="url(#crownMetal)"/>
    <path d="M372 121 L430 156 C441 163 444 178 437 190 L420 218 C413 230 398 234 386 226 L330 192 Z" fill="url(#crownMetal)"/>

    <circle cx="220" cy="300" r="213" fill="url(#bodyMetal)" filter="url(#softShadow)"/>
    <circle cx="220" cy="300" r="186" fill="#6F6F6F"/>
    <circle cx="220" cy="300" r="169" fill="url(#facePaper)"/>

    <path d="M91 221 C130 145 239 112 318 157 C256 146 171 162 111 250 Z" fill="#FFFFFF" opacity="0.42"/>

    <g stroke="#686868" stroke-linecap="round">
      <line x1="220" y1="143" x2="220" y2="160" stroke-width="5"/>
      <line x1="220" y1="143" x2="220" y2="155" stroke-width="3" transform="rotate(15 220 300)"/>
      <line x1="220" y1="143" x2="220" y2="155" stroke-width="3" transform="rotate(30 220 300)"/>
      <line x1="220" y1="143" x2="220" y2="160" stroke-width="5" transform="rotate(45 220 300)"/>
      <line x1="220" y1="143" x2="220" y2="155" stroke-width="3" transform="rotate(60 220 300)"/>
      <line x1="220" y1="143" x2="220" y2="155" stroke-width="3" transform="rotate(75 220 300)"/>
      <line x1="220" y1="143" x2="220" y2="160" stroke-width="5" transform="rotate(90 220 300)"/>
      <line x1="220" y1="143" x2="220" y2="155" stroke-width="3" transform="rotate(105 220 300)"/>
      <line x1="220" y1="143" x2="220" y2="155" stroke-width="3" transform="rotate(120 220 300)"/>
      <line x1="220" y1="143" x2="220" y2="160" stroke-width="5" transform="rotate(135 220 300)"/>
      <line x1="220" y1="143" x2="220" y2="155" stroke-width="3" transform="rotate(150 220 300)"/>
      <line x1="220" y1="143" x2="220" y2="155" stroke-width="3" transform="rotate(165 220 300)"/>
      <line x1="220" y1="143" x2="220" y2="160" stroke-width="5" transform="rotate(180 220 300)"/>
      <line x1="220" y1="143" x2="220" y2="155" stroke-width="3" transform="rotate(195 220 300)"/>
      <line x1="220" y1="143" x2="220" y2="155" stroke-width="3" transform="rotate(210 220 300)"/>
      <line x1="220" y1="143" x2="220" y2="160" stroke-width="5" transform="rotate(225 220 300)"/>
      <line x1="220" y1="143" x2="220" y2="155" stroke-width="3" transform="rotate(240 220 300)"/>
      <line x1="220" y1="143" x2="220" y2="155" stroke-width="3" transform="rotate(255 220 300)"/>
      <line x1="220" y1="143" x2="220" y2="160" stroke-width="5" transform="rotate(270 220 300)"/>
      <line x1="220" y1="143" x2="220" y2="155" stroke-width="3" transform="rotate(285 220 300)"/>
      <line x1="220" y1="143" x2="220" y2="155" stroke-width="3" transform="rotate(300 220 300)"/>
      <line x1="220" y1="143" x2="220" y2="160" stroke-width="5" transform="rotate(315 220 300)"/>
      <line x1="220" y1="143" x2="220" y2="155" stroke-width="3" transform="rotate(330 220 300)"/>
      <line x1="220" y1="143" x2="220" y2="155" stroke-width="3" transform="rotate(345 220 300)"/>
    </g>

    <line x1="220" y1="300" x2="220" y2="205" stroke="#242424" stroke-width="9" stroke-linecap="round" transform="rotate(38 220 300)"/>
    <line x1="220" y1="300" x2="318" y2="300" stroke="#E03232" stroke-width="7" stroke-linecap="round" transform="rotate(-18 220 300)"/>
    <circle cx="220" cy="300" r="15" fill="#242424"/>
    <circle cx="220" cy="300" r="7" fill="#E03232"/>

    <text x="101" y="388" width="238" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="50" font-weight="800" letter-spacing="1" fill="#2B2B2B" text-anchor="middle" filter="url(#textGlow)">00:20</text>
  </g>

  <line x1="610" y1="178" x2="610" y2="540" stroke="url(#redAccent)" stroke-width="5" stroke-linecap="round"/>

  <text x="650" y="185" width="470" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" letter-spacing="4" fill="#FFB000">THE 20-SECOND PITCH</text>

  <text x="650" y="258" width="525" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="58" font-weight="800" fill="#FFFFFF">
    <tspan x="650" dy="0">Success is</tspan>
    <tspan x="650" dy="68">temporary.</tspan>
    <tspan x="650" dy="82" fill="#DADADA">So is failure.</tspan>
  </text>

  <text x="652" y="535" width="455" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="400" fill="#BDBDBD">
    Make the next twenty seconds decide what the room remembers.
  </text>

  <text x="1045" y="650" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" letter-spacing="3" fill="#777777" text-anchor="end">NO FLUFF</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use a photo-realistic stopwatch unless it is intentionally clipped as an image; the core metaphor should remain editable vector shapes.
- ❌ Do not fill the slide with multiple claims or bullet lists; the scarcity cue only works when the message feels distilled.
- ❌ Do not apply filters to the tick `<line>` elements; line filters may be dropped by the PowerPoint translator.
- ❌ Do not use `marker-end` for any pointer or hand; create clock hands with plain `<line>` elements.
- ❌ Do not rely on `<textPath>` for curved dial labels; use simple ticks and centered text instead.

## Composition notes
- Keep the stopwatch on the left 35–40% of the slide; it should feel large enough to create urgency but not compete with the headline.
- Place the headline in the right 55–60% with generous line spacing and a hard left edge for executive authority.
- Use a mostly monochrome charcoal/white/metal palette, then reserve one warm accent color for urgency.
- Let negative space do the work: one stopwatch, one divider rule, one message, one supporting sentence.