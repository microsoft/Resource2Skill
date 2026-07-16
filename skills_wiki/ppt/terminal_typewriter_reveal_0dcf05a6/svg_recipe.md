# SVG Recipe — Terminal Typewriter Reveal

## Visual mechanism
A high-contrast software splash or terminal window frames a monospace headline as if it is being typed live, with a visible caret and status prompt to imply sequential reveal. The slide should feel like a technical launch screen: sparse, cinematic, and focused on one phrase forming in the center.

## SVG primitives needed
- 8× `<rect>` for the letterbox background, red application panel, subtle overlays, title/status areas, and blinking caret placeholder.
- 7× `<path>` for the simplified Office/app logo, window controls, and faint terminal/circuit decoration.
- 5× `<text>` for the brand label, product title, typewriter headline lines, and status prompt; every text element must include `width`.
- 1× `<linearGradient>` for the rich PowerPoint-red / terminal-launch background.
- 1× `<radialGradient>` for the soft center highlight behind the typed text.
- 2× `<filter>` definitions: one soft drop shadow for the main panel and one glow for the typed monospace text.
- Optional animation after SVG-to-PPT conversion: apply PowerPoint “Appear / By letter” to the monospace headline text and a repeated blink to the caret shape.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="pptRed" x1="0" y1="60" x2="1280" y2="620" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#E9552B"/>
      <stop offset="0.52" stop-color="#D83E20"/>
      <stop offset="1" stop-color="#B92718"/>
    </linearGradient>

    <radialGradient id="centerHeat" cx="50%" cy="48%" r="58%">
      <stop offset="0" stop-color="#FF7A4C" stop-opacity="0.38"/>
      <stop offset="0.55" stop-color="#E04624" stop-opacity="0.16"/>
      <stop offset="1" stop-color="#8E160F" stop-opacity="0"/>
    </radialGradient>

    <filter id="panelShadow" x="-10%" y="-15%" width="120%" height="140%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="22"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="textGlow" x="-10%" y="-30%" width="120%" height="160%">
      <feGaussianBlur stdDeviation="2.6" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- black letterbox canvas -->
  <rect x="0" y="0" width="1280" height="720" fill="#050506"/>
  <rect x="0" y="72" width="1280" height="548" fill="url(#pptRed)" filter="url(#panelShadow)"/>
  <rect x="0" y="72" width="1280" height="548" fill="url(#centerHeat)"/>

  <!-- subtle angular application-splash texture -->
  <path d="M900 72 L1280 72 L1280 250 C1170 230 1050 188 900 72 Z" fill="#FF8B5E" opacity="0.11"/>
  <path d="M0 620 L355 620 C245 558 120 520 0 494 Z" fill="#7A120C" opacity="0.16"/>
  <path d="M1020 620 C1115 540 1210 465 1280 332 L1280 620 Z" fill="#6C100B" opacity="0.17"/>

  <!-- faint terminal/circuit accents -->
  <path d="M134 512 H284 V548 H384" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.12" stroke-dasharray="10 10"/>
  <path d="M896 185 H1026 V222 H1138" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.10" stroke-dasharray="8 12"/>
  <path d="M742 566 H806 V538 H872" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.10" stroke-dasharray="7 9"/>

  <!-- top-left simplified Office mark -->
  <path d="M44 117 L73 104 L103 116 L103 157 L73 170 L44 158 Z" fill="#FFFFFF" opacity="0.97"/>
  <path d="M61 124 L77 117 L77 157 L61 150 Z" fill="#D64222"/>
  <path d="M77 117 L96 124 L96 150 L77 157 Z" fill="#FFFFFF" opacity="0.72"/>
  <text x="112" y="146" width="180" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="34" fill="#FFFFFF" opacity="0.96">Office</text>

  <!-- window controls -->
  <path d="M1138 132 H1164" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.95"/>
  <path d="M1226 120 L1250 144 M1250 120 L1226 144" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.95"/>

  <!-- main product title -->
  <text x="170" y="275" width="940" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="94" font-weight="300" fill="#FFFFFF" opacity="0.98">PowerPoint</text>

  <!-- typewriter-reveal headline: keep monospace and animate by-letter in PowerPoint -->
  <text x="354" y="364" width="580" font-family="Consolas, Courier New, monospace" font-size="50" font-weight="700" letter-spacing="5" fill="#FFFFFF" filter="url(#textGlow)">TYPE-WRITER</text>
  <text x="206" y="446" width="870" font-family="Consolas, Courier New, monospace" font-size="52" font-weight="700" letter-spacing="5" fill="#FFFFFF" filter="url(#textGlow)">ANIMATION EFFECT</text>

  <!-- underscored typing baseline and active caret -->
  <rect x="349" y="385" width="582" height="3" fill="#FFFFFF" opacity="0.15"/>
  <rect x="205" y="468" width="872" height="3" fill="#FFFFFF" opacity="0.15"/>
  <rect x="1078" y="401" width="13" height="54" rx="2" fill="#FFFFFF" opacity="0.92"/>

  <!-- bottom command/status prompt -->
  <rect x="0" y="582" width="1280" height="38" fill="#4D120D" opacity="0.16"/>
  <text x="34" y="610" width="260" font-family="Consolas, Courier New, monospace" font-size="24" fill="#FFD8C9" opacity="0.92">Starting...</text>
  <rect x="154" y="590" width="10" height="24" rx="1" fill="#FFD8C9" opacity="0.88"/>

  <!-- small launch diagnostics, intentionally low contrast -->
  <text x="870" y="606" width="350" font-family="Consolas, Courier New, monospace" font-size="15" fill="#FFFFFF" opacity="0.24">boot: text_reveal --mode=by-letter</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<animate>` or `<animateTransform>` for the typing effect; create the static final frame in SVG, then apply PowerPoint “Appear / By letter” after translation if animation is needed.
- ❌ Do not use `<textPath>` for curved command text; it will not translate reliably.
- ❌ Do not use a `<mask>` to reveal the text; masks outside defs or mask attributes on shapes can hard-fail or be ignored.
- ❌ Do not put `filter` on `<line>` elements for glowing terminal strokes; use `<path>` or `<rect>` instead.
- ❌ Do not split every character into a separate SVG text object unless you need manual frame-by-frame control; it makes the PPT hard to edit.

## Composition notes
- Center the typed phrase vertically and give it at least 40% of the slide width; this technique works best when there is only one sentence or launch phrase to watch.
- Use a large humanist sans title for product context and a monospace font for the “typed” words so the reveal reads instantly as terminal/typewriter behavior.
- Keep the caret slightly brighter than the text and place it immediately after the final character or prompt to imply live input.
- Preserve generous negative space around the headline; peripheral UI details should stay low-contrast so they support, not compete with, the reveal.