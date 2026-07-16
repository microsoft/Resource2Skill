# SVG Recipe — Corporate Dual-Tone Node Diagram (Slide Science Style)

## Visual mechanism
A premium corporate process diagram built from strict radial geometry: a dominant deep-purple central hub, vibrant magenta satellite nodes, and crisp white separator strokes. The style feels proprietary by combining flat dual-tone branding with subtle gradients, soft shadows, thick borders, and symmetrical connector logic.

## SVG primitives needed
- 1× `<rect>` for the off-white slide background
- 1× `<rect>` for a small magenta title accent bar
- 2× `<rect>` for compact legend/status chips
- 4× `<line>` thick white connector underlays to create clean separation
- 4× `<line>` purple connector strokes radiating from the hub
- 1× `<circle>` for the faint dashed orbital guide
- 1× `<circle>` for the central purple hub
- 1× `<circle>` for the central white separator ring
- 4× `<circle>` for magenta satellite nodes
- 4× `<circle>` for small purple number badges on satellite nodes
- 4× `<path>` for small directional chevrons along each connector
- 3× `<path>` for faint abstract corporate background geometry
- 1× `<linearGradient>` for the central hub fill
- 1× `<linearGradient>` for magenta node fills
- 1× `<radialGradient>` for the background spotlight
- 1× `<filter id="softShadow">` applied to circles and cards
- 1× `<filter id="glow">` applied to the central hub ring
- Multiple `<text>` elements with explicit `width` attributes for editable titles, labels, badges, and legend text

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgSpot" cx="50%" cy="50%" r="70%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="65%" stop-color="#F8F8FA"/>
      <stop offset="100%" stop-color="#ECECF2"/>
    </radialGradient>

    <linearGradient id="purpleGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#3E2388"/>
      <stop offset="55%" stop-color="#2B1672"/>
      <stop offset="100%" stop-color="#1A0B4F"/>
    </linearGradient>

    <linearGradient id="magentaGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F0448A"/>
      <stop offset="55%" stop-color="#D81B60"/>
      <stop offset="100%" stop-color="#A90F4B"/>
    </linearGradient>

    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="12"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="8"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgSpot)"/>

  <path d="M1020 78 C1104 48 1191 84 1228 154 C1258 213 1241 283 1181 314 C1113 350 1032 310 1000 242 C966 169 962 100 1020 78 Z"
        fill="#2B1672" opacity="0.05"/>
  <path d="M44 565 C118 514 204 520 250 578 C292 632 268 687 196 706 C113 728 37 690 20 632 C12 603 21 581 44 565 Z"
        fill="#D81B60" opacity="0.06"/>
  <path d="M1010 612 L1218 516 L1252 588 L1044 684 Z"
        fill="#2B1672" opacity="0.045"/>

  <rect x="78" y="72" width="9" height="62" rx="4.5" fill="#D81B60"/>
  <text x="104" y="98" width="640" font-family="Segoe UI, Microsoft YaHei" font-size="35" font-weight="700" fill="#2B1672">
    Process Architecture
  </text>
  <text x="106" y="130" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="500" fill="#6F6A82">
    Dual-tone node system for executive strategy, transformation roadmaps, and operating-model flows
  </text>

  <rect x="928" y="80" width="196" height="42" rx="21" fill="#FFFFFF" stroke="#E3E1EA" stroke-width="1.5" filter="url(#softShadow)"/>
  <circle cx="954" cy="101" r="7" fill="#2B1672"/>
  <text x="971" y="107" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#2B1672">
    CORE SYSTEM
  </text>

  <rect x="928" y="136" width="196" height="42" rx="21" fill="#FFFFFF" stroke="#E3E1EA" stroke-width="1.5" filter="url(#softShadow)"/>
  <circle cx="954" cy="157" r="7" fill="#D81B60"/>
  <text x="971" y="163" width="132" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#D81B60">
    ACTION NODES
  </text>

  <circle cx="640" cy="402" r="238" fill="none" stroke="#2B1672" stroke-width="2" stroke-dasharray="8 12" opacity="0.16"/>

  <line x1="640" y1="402" x2="878" y2="402" stroke="#FFFFFF" stroke-width="16" stroke-linecap="round"/>
  <line x1="640" y1="402" x2="640" y2="164" stroke="#FFFFFF" stroke-width="16" stroke-linecap="round"/>
  <line x1="640" y1="402" x2="402" y2="402" stroke="#FFFFFF" stroke-width="16" stroke-linecap="round"/>
  <line x1="640" y1="402" x2="640" y2="640" stroke="#FFFFFF" stroke-width="16" stroke-linecap="round"/>

  <line x1="640" y1="402" x2="878" y2="402" stroke="#2B1672" stroke-width="5" stroke-linecap="round"/>
  <line x1="640" y1="402" x2="640" y2="164" stroke="#2B1672" stroke-width="5" stroke-linecap="round"/>
  <line x1="640" y1="402" x2="402" y2="402" stroke="#2B1672" stroke-width="5" stroke-linecap="round"/>
  <line x1="640" y1="402" x2="640" y2="640" stroke="#2B1672" stroke-width="5" stroke-linecap="round"/>

  <path d="M762 392 L784 402 L762 412 Z" fill="#D81B60" stroke="#FFFFFF" stroke-width="3"/>
  <path d="M630 280 L640 258 L650 280 Z" fill="#D81B60" stroke="#FFFFFF" stroke-width="3"/>
  <path d="M518 392 L496 402 L518 412 Z" fill="#D81B60" stroke="#FFFFFF" stroke-width="3"/>
  <path d="M630 524 L640 546 L650 524 Z" fill="#D81B60" stroke="#FFFFFF" stroke-width="3"/>

  <circle cx="640" cy="402" r="118" fill="#FFFFFF" opacity="0.85" filter="url(#glow)"/>
  <circle cx="640" cy="402" r="112" fill="url(#purpleGrad)" stroke="#FFFFFF" stroke-width="8" filter="url(#softShadow)"/>
  <circle cx="640" cy="402" r="77" fill="none" stroke="#FFFFFF" stroke-width="2.5" opacity="0.3"/>
  <text x="570" y="386" width="140" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="800" fill="#FFFFFF">
    <tspan x="640" dy="0">CORE</tspan>
    <tspan x="640" dy="27">SYSTEM</tspan>
  </text>
  <text x="578" y="442" width="124" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#E7DFFF">
    <tspan x="640">governance layer</tspan>
  </text>

  <circle cx="878" cy="402" r="78" fill="url(#magentaGrad)" stroke="#FFFFFF" stroke-width="7" filter="url(#softShadow)"/>
  <circle cx="928" cy="352" r="22" fill="#2B1672" stroke="#FFFFFF" stroke-width="4"/>
  <text x="916" y="360" width="24" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="800" fill="#FFFFFF">01</text>
  <text x="818" y="391" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" fill="#FFFFFF">
    <tspan x="878">PLAN</tspan>
    <tspan x="878" dy="22" font-size="12" font-weight="600">prioritize</tspan>
  </text>

  <circle cx="640" cy="164" r="78" fill="url(#magentaGrad)" stroke="#FFFFFF" stroke-width="7" filter="url(#softShadow)"/>
  <circle cx="690" cy="114" r="22" fill="#2B1672" stroke="#FFFFFF" stroke-width="4"/>
  <text x="678" y="122" width="24" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="800" fill="#FFFFFF">02</text>
  <text x="580" y="153" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" fill="#FFFFFF">
    <tspan x="640">DESIGN</tspan>
    <tspan x="640" dy="22" font-size="12" font-weight="600">blueprint</tspan>
  </text>

  <circle cx="402" cy="402" r="78" fill="url(#magentaGrad)" stroke="#FFFFFF" stroke-width="7" filter="url(#softShadow)"/>
  <circle cx="452" cy="352" r="22" fill="#2B1672" stroke="#FFFFFF" stroke-width="4"/>
  <text x="440" y="360" width="24" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="800" fill="#FFFFFF">03</text>
  <text x="342" y="391" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" fill="#FFFFFF">
    <tspan x="402">BUILD</tspan>
    <tspan x="402" dy="22" font-size="12" font-weight="600">execute</tspan>
  </text>

  <circle cx="640" cy="640" r="78" fill="url(#magentaGrad)" stroke="#FFFFFF" stroke-width="7" filter="url(#softShadow)"/>
  <circle cx="690" cy="590" r="22" fill="#2B1672" stroke="#FFFFFF" stroke-width="4"/>
  <text x="678" y="598" width="24" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="800" fill="#FFFFFF">04</text>
  <text x="580" y="629" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" fill="#FFFFFF">
    <tspan x="640">SCALE</tspan>
    <tspan x="640" dy="22" font-size="12" font-weight="600">optimize</tspan>
  </text>

  <text x="80" y="670" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#8A8498">
    Use white strokes as separators whenever nodes touch or visually overlap.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use plain default SmartArt-style circles without thick white strokes; the white separators are a key part of the Slide Science look.
- ❌ Do not add too many colors. This technique depends on a disciplined purple + magenta palette with only neutral grays for support.
- ❌ Do not place satellite nodes irregularly unless the business meaning requires it; symmetry is what makes the diagram feel structured and executive-ready.
- ❌ Do not use `marker-end` on `<path>` connectors. If arrowheads are needed, draw them as separate editable `<path>` chevrons.
- ❌ Do not rely on filters on `<line>` elements; create connector depth with white underlay lines instead.

## Composition notes
- Keep the main diagram centered slightly below the title zone, with generous negative space around the orbit so the slide stays premium rather than crowded.
- Use the central hub at roughly 1.4× the diameter of each satellite node to create a clear hierarchy.
- Put purple on structural elements: hub, connector lines, number badges, and primary title. Use magenta only for action/process nodes and small accents.
- The strongest visual focus should be the central hub and the four magenta nodes; background geometry should stay very low-opacity.