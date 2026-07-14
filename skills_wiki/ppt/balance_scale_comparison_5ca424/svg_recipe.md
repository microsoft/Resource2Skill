# SVG Recipe — Balance Scale Comparison

## Visual mechanism
A large custom-drawn balance scale occupies the left two-thirds of the slide, with two opposing concepts placed in the pans to make the comparison instantly legible. A calm explanatory text card on the right provides interpretation, criteria, or the decision takeaway.

## SVG primitives needed
- 4× `<linearGradient>` for dark background, metallic pillar, gold beam, and side-card surface
- 2× `<radialGradient>` for subtle spotlight and pan highlights
- 2× `<filter>` for soft card/scale shadow and gentle glow accents
- 5× `<rect>` for background, top title accent, side explanation panel, concept pills, and beam
- 5× `<path>` for decorative background arcs, central pillar, weighted pans, and base
- 6× `<line>` for scale suspension wires
- 4× `<circle>` / `<ellipse>` for pivot detail, bolt, and floor shadow
- 8× `<text>` elements with explicit `width` for headline, subtitle, pan labels, side title, body, and small metadata labels

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#081421"/>
      <stop offset="58%" stop-color="#0E2135"/>
      <stop offset="100%" stop-color="#132D43"/>
    </linearGradient>

    <radialGradient id="spotlight" cx="36%" cy="48%" r="55%">
      <stop offset="0%" stop-color="#2F6F9B" stop-opacity="0.42"/>
      <stop offset="55%" stop-color="#16364F" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#081421" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="gold" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8D98A"/>
      <stop offset="45%" stop-color="#C99A3E"/>
      <stop offset="100%" stop-color="#8D6424"/>
    </linearGradient>

    <linearGradient id="steel" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#D8E6EF"/>
      <stop offset="45%" stop-color="#7F98A8"/>
      <stop offset="100%" stop-color="#465B6A"/>
    </linearGradient>

    <linearGradient id="panelGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#F7FAFC"/>
      <stop offset="100%" stop-color="#EAF0F4"/>
    </linearGradient>

    <radialGradient id="panGlow" cx="50%" cy="20%" r="80%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#B9812F" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="6"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#spotlight)"/>

  <path d="M88 612 C190 522, 302 496, 432 530 C553 562, 654 537, 768 455"
        fill="none" stroke="#6BA6C8" stroke-opacity="0.16" stroke-width="2"/>
  <path d="M80 654 C250 590, 415 604, 590 626 C680 638, 762 622, 828 578"
        fill="none" stroke="#D7B25A" stroke-opacity="0.14" stroke-width="2"/>
  <ellipse cx="455" cy="638" rx="300" ry="34" fill="#000000" opacity="0.28" filter="url(#glow)"/>

  <rect x="72" y="60" width="84" height="5" rx="2.5" fill="#D7B25A"/>
  <text x="72" y="112" width="660" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="42" font-weight="700" fill="#F7FAFC">Strategic Trade-offs</text>
  <text x="74" y="150" width="610" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" fill="#AFC4D3">Use the scale to compare the forces that pull a decision in opposite directions.</text>

  <path d="M448 320 C438 370, 427 480, 412 595 L505 595 C490 480, 479 370, 468 320 Z"
        fill="url(#steel)" filter="url(#softShadow)"/>
  <path d="M363 596 C383 570, 531 570, 553 596 L588 632 L328 632 Z"
        fill="url(#steel)" filter="url(#softShadow)"/>
  <rect x="226" y="300" width="468" height="18" rx="9"
        fill="url(#gold)" transform="rotate(-6 460 309)" filter="url(#softShadow)"/>

  <circle cx="460" cy="309" r="32" fill="#101D2A" stroke="#E6C46F" stroke-width="8"/>
  <circle cx="460" cy="309" r="9" fill="#F6D88A"/>

  <line x1="252" y1="330" x2="210" y2="430" stroke="#D7B25A" stroke-width="3"/>
  <line x1="252" y1="330" x2="252" y2="430" stroke="#D7B25A" stroke-width="3"/>
  <line x1="252" y1="330" x2="294" y2="430" stroke="#D7B25A" stroke-width="3"/>

  <line x1="668" y1="286" x2="626" y2="386" stroke="#D7B25A" stroke-width="3"/>
  <line x1="668" y1="286" x2="668" y2="386" stroke="#D7B25A" stroke-width="3"/>
  <line x1="668" y1="286" x2="710" y2="386" stroke="#D7B25A" stroke-width="3"/>

  <path d="M174 430 C196 486, 306 486, 330 430 Z"
        fill="url(#gold)" stroke="#F4D37E" stroke-width="2" filter="url(#softShadow)"/>
  <path d="M174 430 C196 452, 306 452, 330 430 C303 444, 202 444, 174 430 Z"
        fill="url(#panGlow)"/>

  <path d="M590 386 C612 442, 722 442, 746 386 Z"
        fill="url(#gold)" stroke="#F4D37E" stroke-width="2" filter="url(#softShadow)"/>
  <path d="M590 386 C612 408, 722 408, 746 386 C719 400, 618 400, 590 386 Z"
        fill="url(#panGlow)"/>

  <rect x="156" y="482" width="190" height="54" rx="27" fill="#F05C5C" filter="url(#softShadow)"/>
  <text x="176" y="517" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="19" font-weight="700" text-anchor="middle" fill="#FFFFFF" transform="translate(75 0)">Automation</text>

  <rect x="572" y="438" width="192" height="54" rx="27" fill="#4DA3FF" filter="url(#softShadow)"/>
  <text x="592" y="473" width="152" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="19" font-weight="700" text-anchor="middle" fill="#FFFFFF" transform="translate(76 0)">Human Judgment</text>

  <text x="164" y="565" width="174" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="600" letter-spacing="1.2" text-anchor="middle" fill="#BFD3DF" transform="translate(87 0)">EFFICIENCY GAIN</text>
  <text x="580" y="520" width="176" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="600" letter-spacing="1.2" text-anchor="middle" fill="#BFD3DF" transform="translate(88 0)">RISK CONTROL</text>

  <rect x="842" y="72" width="358" height="576" rx="34" fill="url(#panelGrad)" filter="url(#softShadow)"/>
  <rect x="872" y="104" width="64" height="6" rx="3" fill="#D7B25A"/>
  <text x="872" y="166" width="278" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="32" font-weight="750" fill="#112235">Decision lens</text>

  <text x="872" y="214" width="270" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" fill="#425466">
    <tspan x="872" dy="0">The balance metaphor works best</tspan>
    <tspan x="872" dy="29">when each side represents a</tspan>
    <tspan x="872" dy="29">clear force: speed versus control,</tspan>
    <tspan x="872" dy="29">cost versus quality, or autonomy</tspan>
    <tspan x="872" dy="29">versus governance.</tspan>
  </text>

  <rect x="872" y="390" width="278" height="1.5" rx="0.75" fill="#CAD6DE"/>
  <text x="872" y="438" width="278" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" letter-spacing="1.4" fill="#8D6424">TAKEAWAY</text>
  <text x="872" y="478" width="276" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="21" font-weight="700" fill="#132D43">
    <tspan x="872" dy="0">Prioritize the side that</tspan>
    <tspan x="872" dy="31">creates durable advantage,</tspan>
    <tspan x="872" dy="31">not just short-term lift.</tspan>
  </text>

  <circle cx="1126" cy="586" r="34" fill="#132D43"/>
  <text x="1104" y="594" width="44" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" font-weight="800" text-anchor="middle" fill="#F7FAFC" transform="translate(22 0)">01</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<marker>` arrowheads on the beam or suspension wires; the balance metaphor should be built from editable lines and paths.
- ❌ Do not apply filters to `<line>` suspension wires; shadows on lines are dropped, so reserve shadows for pans, cards, pillar, and beam.
- ❌ Do not use `<mask>` to fake metallic highlights; use gradients and layered paths instead.
- ❌ Do not overcrowd both pans with bullets; the visual metaphor works best with one concise label per side and explanation in the side panel.
- ❌ Do not place the right-side text card too close to the scale; the slide needs visible separation between metaphor and analysis.

## Composition notes
- Keep the balance scale as the dominant focal object, occupying roughly 60–65% of the canvas width.
- Use the right third for a quiet explanatory card with generous margins and no more than one key takeaway block.
- Tilt the beam slightly to imply comparison or trade-off, but keep the angle subtle so the graphic still feels executive and controlled.
- Use a restrained palette: dark editorial background, metallic gold for the scale, and two distinct accent colors for the opposing concepts.