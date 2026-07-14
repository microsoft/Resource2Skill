# SVG Recipe — Structured Narrative Framework

## Visual mechanism
A calm, high-contrast executive slide uses a clear narrative spine: title and thesis on the left, three sequenced story beats across the middle, and a discreet progress/footer system. Minimal shapes, accent lines, and generous negative space create structure without competing with the speaker.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark gradient background
- 3× translucent `<ellipse>` shapes for subtle ambient depth
- 1× `<path>` for the curved narrative arc connecting the story beats
- 3× `<circle>` for numbered narrative nodes
- 3× `<rect>` for elevated content cards
- 3× small `<rect>` label chips for section categories
- 2× `<line>` for title underline and footer separator
- 1× `<path>` for a decorative corner bracket accent
- Multiple `<text>` elements with explicit `width` for title, thesis, card labels, body copy, and footer metadata
- 3× `<linearGradient>` definitions for background, cards, and accent fills
- 1× `<radialGradient>` definition for soft background glow
- 2× `<filter>` definitions using blur/offset/merge for editable shadows and glow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#222831"/>
      <stop offset="58%" stop-color="#1B2028"/>
      <stop offset="100%" stop-color="#111820"/>
    </linearGradient>

    <linearGradient id="cardGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#303946"/>
      <stop offset="100%" stop-color="#252C36"/>
    </linearGradient>

    <linearGradient id="accentGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00ADB5"/>
      <stop offset="100%" stop-color="#36E3D6"/>
    </linearGradient>

    <radialGradient id="focusGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#00ADB5" stop-opacity="0.28"/>
      <stop offset="72%" stop-color="#00ADB5" stop-opacity="0.05"/>
      <stop offset="100%" stop-color="#00ADB5" stop-opacity="0"/>
    </radialGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feColorMatrix in="blur" type="matrix"
        values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .32 0" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <ellipse cx="1080" cy="120" rx="270" ry="190" fill="url(#focusGlow)" opacity="0.7"/>
  <ellipse cx="180" cy="650" rx="300" ry="150" fill="#00ADB5" opacity="0.035"/>
  <ellipse cx="1040" cy="660" rx="210" ry="90" fill="#EEEEEE" opacity="0.035"/>

  <path d="M88 92 L88 42 L238 42" fill="none" stroke="#00ADB5" stroke-width="4" stroke-linecap="round" opacity="0.95"/>

  <text x="88" y="120" width="560" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" font-weight="600" fill="#00ADB5" letter-spacing="2.4">
    STRUCTURED NARRATIVE
  </text>

  <text x="88" y="185" width="690" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="48" font-weight="700" fill="#EEEEEE">
    <tspan x="88" dy="0">From complexity</tspan>
    <tspan x="88" dy="58">to a clear decision</tspan>
  </text>

  <line x1="88" y1="234" x2="380" y2="234" stroke="#00ADB5" stroke-width="5" stroke-linecap="round"/>

  <text x="88" y="282" width="620" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" fill="#C9D1D9">
    <tspan x="88" dy="0">Use the slide as a disciplined speaking guide:</tspan>
    <tspan x="88" dy="34">one thesis, three story beats, one memorable close.</tspan>
  </text>

  <path d="M170 485 C335 392, 470 397, 610 470 S910 570, 1115 425"
        fill="none" stroke="#00ADB5" stroke-width="3" stroke-linecap="round"
        stroke-dasharray="2 12" opacity="0.55" filter="url(#softGlow)"/>

  <rect x="118" y="368" width="300" height="210" rx="24" fill="url(#cardGrad)" stroke="#3F4A57" stroke-width="1.2" filter="url(#cardShadow)"/>
  <rect x="490" y="368" width="300" height="210" rx="24" fill="url(#cardGrad)" stroke="#3F4A57" stroke-width="1.2" filter="url(#cardShadow)"/>
  <rect x="862" y="368" width="300" height="210" rx="24" fill="url(#cardGrad)" stroke="#3F4A57" stroke-width="1.2" filter="url(#cardShadow)"/>

  <circle cx="168" cy="404" r="23" fill="url(#accentGrad)" filter="url(#softGlow)"/>
  <circle cx="540" cy="404" r="23" fill="url(#accentGrad)" filter="url(#softGlow)"/>
  <circle cx="912" cy="404" r="23" fill="url(#accentGrad)" filter="url(#softGlow)"/>

  <text x="158" y="413" width="24" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#111820">1</text>
  <text x="530" y="413" width="24" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#111820">2</text>
  <text x="902" y="413" width="24" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700" fill="#111820">3</text>

  <rect x="207" y="389" width="94" height="28" rx="14" fill="#00ADB5" opacity="0.14"/>
  <rect x="579" y="389" width="104" height="28" rx="14" fill="#00ADB5" opacity="0.14"/>
  <rect x="951" y="389" width="98" height="28" rx="14" fill="#00ADB5" opacity="0.14"/>

  <text x="218" y="409" width="90" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" fill="#36E3D6" letter-spacing="1.1">HOOK</text>
  <text x="590" y="409" width="100" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" fill="#36E3D6" letter-spacing="1.1">PROOF</text>
  <text x="962" y="409" width="95" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" fill="#36E3D6" letter-spacing="1.1">CLOSE</text>

  <text x="148" y="462" width="240" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="25" font-weight="700" fill="#EEEEEE">
    Name the tension
  </text>
  <text x="148" y="503" width="240" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#C9D1D9">
    <tspan x="148" dy="0">Open with the question</tspan>
    <tspan x="148" dy="25">the room already feels.</tspan>
  </text>

  <text x="520" y="462" width="240" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="25" font-weight="700" fill="#EEEEEE">
    Build the case
  </text>
  <text x="520" y="503" width="240" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#C9D1D9">
    <tspan x="520" dy="0">Sequence evidence into</tspan>
    <tspan x="520" dy="25">three digestible claims.</tspan>
  </text>

  <text x="892" y="462" width="240" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="25" font-weight="700" fill="#EEEEEE">
    Land the decision
  </text>
  <text x="892" y="503" width="240" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#C9D1D9">
    <tspan x="892" dy="0">Finish with one action</tspan>
    <tspan x="892" dy="25">the audience can repeat.</tspan>
  </text>

  <line x1="88" y1="642" x2="1192" y2="642" stroke="#EEEEEE" stroke-width="1" opacity="0.14"/>

  <text x="88" y="676" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#8F9BA8">
    Narrative framework template
  </text>
  <text x="1010" y="676" width="180" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#8F9BA8" text-anchor="end">
    01 / 05
  </text>
</svg>
```

## Avoid in this skill
- ❌ Dense grids, many competing icons, or dashboard-style panels that weaken the narrative flow.
- ❌ Decorative flourishes without structural purpose; every accent should guide reading order.
- ❌ Center-aligning all content on every slide; use centered type mainly for title, hook, or closing slides.
- ❌ Unsupported SVG features such as `<foreignObject>`, `<textPath>`, `<mask>`, `<use>`, or `marker-end` on paths.

## Composition notes
- Keep the title/thesis area in the upper-left third; it should establish the message before the audience reaches the cards.
- Use the center band for the narrative sequence, with three generous cards or beats rather than many small bullets.
- Reserve the bottom 10–12% for quiet navigation, source notes, or section progress.
- Use teal sparingly as a structural signal: underline, node, chip, or key word—not as a full-slide decoration.