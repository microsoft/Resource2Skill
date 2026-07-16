# SVG Recipe — Cosmic Quiz Layout (Sequential Reveal Staging)

## Visual mechanism
A deep navy starfield creates an immersive “game show in space” stage, with a giant moon bleeding off the right edge as the visual anchor. The question occupies the left side in oversized white type, while a gold-framed answer panel sits below it as the object intended for sequential reveal or fade-in.

## SVG primitives needed
- 1× `<rect>` for the full-slide deep-space background
- 30–60× `<circle>` for deterministic editable stars with varied opacity and size
- 1× `<circle>` for the oversized moon/planet anchor bleeding off the right edge
- 8× `<ellipse>` / `<circle>` for moon craters and surface details
- 2× `<path>` for subtle orbital arcs crossing the slide
- 3× `<rect>` for question label, answer reveal panel, and small metadata chips
- 6× `<text>` for category label, question, reveal cue, answer, and quiz-progress microcopy
- 1× `<linearGradient>` for the space background
- 1× `<radialGradient>` for the moon surface
- 1× `<filter id="softShadow">` for elevated answer panel shadow
- 1× `<filter id="goldGlow">` for the answer-panel accent glow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="spaceBg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#070A14"/>
      <stop offset="45%" stop-color="#0D111C"/>
      <stop offset="100%" stop-color="#151B31"/>
    </linearGradient>

    <radialGradient id="moonGrad" cx="38%" cy="35%" r="70%">
      <stop offset="0%" stop-color="#F4F1E8"/>
      <stop offset="45%" stop-color="#D8D8D8"/>
      <stop offset="100%" stop-color="#9EA2AA"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-30%" width="150%" height="170%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="goldGlow" x="-30%" y="-40%" width="160%" height="180%">
      <feGaussianBlur stdDeviation="5"/>
    </filter>
  </defs>

  <!-- Deep space base -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#spaceBg)"/>

  <!-- Subtle nebula wash -->
  <ellipse cx="210" cy="150" rx="360" ry="210" fill="#20345F" opacity="0.18"/>
  <ellipse cx="690" cy="640" rx="520" ry="190" fill="#2E1D5E" opacity="0.20"/>
  <ellipse cx="1120" cy="95" rx="270" ry="170" fill="#123A53" opacity="0.22"/>

  <!-- Editable starfield -->
  <circle cx="54" cy="58" r="1.4" fill="#FFFFFF" opacity="0.80"/>
  <circle cx="146" cy="112" r="1.1" fill="#FFFFFF" opacity="0.55"/>
  <circle cx="238" cy="42" r="2.1" fill="#FFFFFF" opacity="0.85"/>
  <circle cx="328" cy="96" r="1.2" fill="#FFFFFF" opacity="0.45"/>
  <circle cx="436" cy="54" r="1.8" fill="#FFFFFF" opacity="0.65"/>
  <circle cx="610" cy="92" r="1.2" fill="#FFFFFF" opacity="0.55"/>
  <circle cx="762" cy="48" r="2.4" fill="#FFF7C2" opacity="0.80"/>
  <circle cx="928" cy="86" r="1.2" fill="#FFFFFF" opacity="0.50"/>
  <circle cx="1162" cy="52" r="1.7" fill="#FFFFFF" opacity="0.72"/>
  <circle cx="84" cy="220" r="2.3" fill="#FFFFFF" opacity="0.78"/>
  <circle cx="190" cy="286" r="1.1" fill="#FFFFFF" opacity="0.45"/>
  <circle cx="366" cy="226" r="1.6" fill="#FFFFFF" opacity="0.66"/>
  <circle cx="518" cy="262" r="1.1" fill="#FFFFFF" opacity="0.52"/>
  <circle cx="682" cy="212" r="2.0" fill="#FFFFFF" opacity="0.70"/>
  <circle cx="820" cy="286" r="1.2" fill="#FFFFFF" opacity="0.45"/>
  <circle cx="1014" cy="248" r="1.5" fill="#FFFFFF" opacity="0.60"/>
  <circle cx="1218" cy="224" r="2.0" fill="#FFF7C2" opacity="0.76"/>
  <circle cx="72" cy="414" r="1.3" fill="#FFFFFF" opacity="0.50"/>
  <circle cx="244" cy="384" r="2.7" fill="#FFFFFF" opacity="0.90"/>
  <circle cx="394" cy="452" r="1.0" fill="#FFFFFF" opacity="0.45"/>
  <circle cx="566" cy="398" r="1.8" fill="#FFFFFF" opacity="0.62"/>
  <circle cx="724" cy="458" r="1.2" fill="#FFFFFF" opacity="0.50"/>
  <circle cx="876" cy="402" r="2.2" fill="#FFFFFF" opacity="0.78"/>
  <circle cx="1110" cy="438" r="1.2" fill="#FFFFFF" opacity="0.46"/>
  <circle cx="1242" cy="382" r="1.6" fill="#FFFFFF" opacity="0.64"/>
  <circle cx="126" cy="612" r="1.7" fill="#FFFFFF" opacity="0.70"/>
  <circle cx="306" cy="646" r="1.2" fill="#FFFFFF" opacity="0.48"/>
  <circle cx="492" cy="594" r="2.5" fill="#FFF7C2" opacity="0.80"/>
  <circle cx="674" cy="642" r="1.4" fill="#FFFFFF" opacity="0.58"/>
  <circle cx="846" cy="612" r="1.1" fill="#FFFFFF" opacity="0.45"/>
  <circle cx="1036" cy="658" r="2.0" fill="#FFFFFF" opacity="0.70"/>
  <circle cx="1198" cy="598" r="1.3" fill="#FFFFFF" opacity="0.56"/>

  <!-- Orbital guide arcs -->
  <path d="M-80 610 C260 470 545 396 846 385 C1035 378 1160 400 1340 458"
        fill="none" stroke="#FFFFFF" stroke-width="1.4" opacity="0.13"/>
  <path d="M-120 180 C220 305 470 340 780 302 C980 278 1130 222 1320 118"
        fill="none" stroke="#FFD75A" stroke-width="1.2" opacity="0.18" stroke-dasharray="8 14"/>

  <!-- Oversized moon anchor -->
  <circle cx="1062" cy="368" r="310" fill="url(#moonGrad)" opacity="0.98"/>
  <circle cx="1062" cy="368" r="310" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.16"/>
  <ellipse cx="940" cy="218" rx="54" ry="38" fill="#AEB2B8" opacity="0.55"/>
  <ellipse cx="1130" cy="180" rx="38" ry="30" fill="#B9BCC1" opacity="0.55"/>
  <ellipse cx="996" cy="402" rx="82" ry="58" fill="#A4A8AE" opacity="0.48"/>
  <ellipse cx="1194" cy="430" rx="50" ry="40" fill="#A8ACB2" opacity="0.50"/>
  <ellipse cx="1094" cy="586" rx="76" ry="44" fill="#B3B6BC" opacity="0.42"/>
  <circle cx="875" cy="526" r="31" fill="#9FA3AA" opacity="0.45"/>
  <circle cx="1230" cy="278" r="24" fill="#9FA3AA" opacity="0.45"/>
  <ellipse cx="1018" cy="278" rx="20" ry="15" fill="#F4F1E8" opacity="0.35"/>

  <!-- Left content stage -->
  <rect x="72" y="78" width="154" height="34" rx="17" fill="#FFD75A" opacity="0.96"/>
  <text x="98" y="101" width="110" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" fill="#101522" letter-spacing="1.8">MOONSHOT QUIZ</text>

  <text x="72" y="182" width="660" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="54" font-weight="750" fill="#FFFFFF">
    <tspan x="72" dy="0">Who was the first</tspan>
    <tspan x="72" dy="66">person to walk</tspan>
    <tspan x="72" dy="66">on the moon?</tspan>
  </text>

  <text x="76" y="405" width="430" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="19" fill="#AAB4CF">Tap, fade, or fly in the answer panel when the audience is ready.</text>

  <!-- Reveal target: select this group in PowerPoint and apply Fade / Fly In -->
  <rect x="72" y="478" width="548" height="118" rx="22" fill="#060914" opacity="0.72" filter="url(#softShadow)"/>
  <rect x="72" y="478" width="548" height="118" rx="22" fill="none" stroke="#FFD75A" stroke-width="3" filter="url(#goldGlow)" opacity="0.95"/>
  <rect x="92" y="498" width="102" height="28" rx="14" fill="#FFD75A"/>
  <text x="116" y="518" width="58" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="800" fill="#0D111C" letter-spacing="1.4">REVEAL</text>
  <text x="96" y="567" width="470" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="34" font-weight="700" fill="#FFFFFF">
    <tspan fill="#FFD75A">Answer:</tspan><tspan> Neil Armstrong</tspan>
  </text>

  <!-- Progress chip -->
  <rect x="72" y="632" width="184" height="34" rx="17" fill="#FFFFFF" opacity="0.10" stroke="#FFFFFF" stroke-width="1" stroke-dasharray="3 7"/>
  <text x="96" y="655" width="140" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" fill="#D7DDF2" letter-spacing="1.2">QUESTION 01 / 05</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<animate>` or `<animateTransform>` for the reveal; stage the answer panel as a separate editable object and apply PowerPoint Fade/Fly In after translation.
- ❌ Do not create the starfield as a raster background if editability matters; use many small editable `<circle>` stars instead.
- ❌ Do not use `<mask>` to shade the moon; use radial gradients, crater ellipses, and translucent overlays.
- ❌ Do not place `clip-path` on shapes for moon cropping; simply position the moon circle so it bleeds beyond the slide edge.
- ❌ Do not use `marker-end` on curved paths for orbit arrows; if arrows are needed, draw them with separate editable `<line>` elements.

## Composition notes
- Keep the left 55–60% as the “quiz stage”: label at top, large question in the middle, answer reveal panel below.
- Let the moon dominate the right 40% and bleed off-canvas to create scale without competing with the question text.
- Use white for the question, gold only for reveal-state accents, and muted blue-gray for secondary instructions.
- The answer box should be isolated enough that it can be selected and animated independently in PowerPoint.