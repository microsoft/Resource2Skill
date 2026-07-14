# SVG Recipe — AI-Powered Declarative Infographic Generation

## Visual mechanism
Show a left-to-right “prompt/spec → AI layout compiler → polished infographic” pipeline: a dark declarative code panel feeds a glowing AI engine, which outputs multiple ready-made chart templates on a presentation canvas. The premium feel comes from glass cards, neon connector accents, miniature infographic modules, and clear typographic hierarchy.

## SVG primitives needed
- 6× <rect> for background panels, glass cards, code blocks, and output infographic modules
- 8× <rect> for code-line tokens and generated chart labels
- 5× <circle> for the AI engine core, neural nodes, and timeline milestones
- 8× <line> for connectors, circuit links, and timeline axes
- 8× <path> for arrowheads, decorative brackets, pyramid/funnel levels, spark accents, and AI circuit glyphs
- 12× <text> for slide title, subtitles, code/spec content, AI labels, and infographic annotations
- 2× <linearGradient> for background and card surfaces
- 1× <radialGradient> for the AI glow core
- 2× <filter> with blur/shadow applied to panels and the AI core
- stroke-dasharray for the “declarative input” and “rendered output” guide rails

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#07111F"/>
      <stop offset="55%" stop-color="#111A35"/>
      <stop offset="100%" stop-color="#071827"/>
    </linearGradient>
    <linearGradient id="glassGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.05"/>
    </linearGradient>
    <linearGradient id="bluePink" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#35D5FF"/>
      <stop offset="55%" stop-color="#7A5CFF"/>
      <stop offset="100%" stop-color="#FF5CC8"/>
    </linearGradient>
    <radialGradient id="aiCore" cx="50%" cy="45%" r="60%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="30%" stop-color="#66F6FF"/>
      <stop offset="72%" stop-color="#5C4DFF"/>
      <stop offset="100%" stop-color="#231A68"/>
    </radialGradient>
    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="16"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="glow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="12" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <path d="M1010 40 C1120 15 1195 72 1228 155 C1265 248 1195 330 1080 308 C986 290 930 224 944 145 C953 91 972 58 1010 40 Z" fill="#35D5FF" opacity="0.08"/>
  <path d="M60 640 C170 590 245 610 324 664 C222 704 126 704 60 640 Z" fill="#FF5CC8" opacity="0.07"/>

  <text x="60" y="58" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#FFFFFF">AI-Powered Declarative Infographic Generation</text>
  <text x="62" y="88" width="780" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#AEB8D6">Natural language and structured data become editable, theme-consistent executive infographics.</text>

  <rect x="60" y="125" width="350" height="485" rx="28" fill="url(#glassGrad)" stroke="#31405F" stroke-width="1.2" filter="url(#softShadow)"/>
  <text x="88" y="166" width="290" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#FFFFFF">1. Declarative intent</text>
  <text x="88" y="192" width="285" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#9FB0D0">Compact text syntax describes chart type, data, hierarchy, and tone.</text>

  <rect x="88" y="224" width="294" height="310" rx="18" fill="#07101E" stroke="#35D5FF" stroke-opacity="0.35"/>
  <text x="108" y="256" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#66F6FF">chart-roadmap</text>
  <text x="108" y="285" width="245" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#DCE7FF">theme: executive-dark</text>
  <text x="108" y="313" width="245" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#DCE7FF">title: AI Platform Launch</text>
  <text x="108" y="341" width="245" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#DCE7FF">milestones:</text>
  <rect x="126" y="360" width="190" height="18" rx="9" fill="#1D2B48"/>
  <text x="137" y="374" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#A7F3FF">Q1 · data foundation</text>
  <rect x="126" y="389" width="214" height="18" rx="9" fill="#1D2B48"/>
  <text x="137" y="403" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#D7D0FF">Q2 · model orchestration</text>
  <rect x="126" y="418" width="182" height="18" rx="9" fill="#1D2B48"/>
  <text x="137" y="432" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#FFD6F1">Q3 · agent pilots</text>
  <rect x="126" y="447" width="230" height="18" rx="9" fill="#1D2B48"/>
  <text x="137" y="461" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#C9FFD8">Q4 · scaled deployment</text>
  <path d="M104 500 L356 500" stroke="#35D5FF" stroke-width="1.5" stroke-dasharray="5 7" fill="none"/>
  <text x="108" y="520" width="245" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7F8DAE">editable SVG primitives, not screenshots</text>

  <line x1="420" y1="365" x2="530" y2="365" stroke="#35D5FF" stroke-width="2.5" stroke-dasharray="8 8"/>
  <path d="M530 365 L511 354 L511 376 Z" fill="#35D5FF"/>

  <circle cx="620" cy="365" r="92" fill="#111936" stroke="#435379" stroke-width="1.2" filter="url(#softShadow)"/>
  <circle cx="620" cy="365" r="64" fill="url(#aiCore)" filter="url(#glow)"/>
  <circle cx="590" cy="338" r="7" fill="#FFFFFF"/>
  <circle cx="651" cy="337" r="7" fill="#FFFFFF"/>
  <circle cx="620" cy="390" r="7" fill="#FFFFFF"/>
  <line x1="590" y1="338" x2="651" y2="337" stroke="#FFFFFF" stroke-width="2"/>
  <line x1="590" y1="338" x2="620" y2="390" stroke="#FFFFFF" stroke-width="2"/>
  <line x1="651" y1="337" x2="620" y2="390" stroke="#FFFFFF" stroke-width="2"/>
  <path d="M571 411 C600 441 642 444 672 411" stroke="#FFFFFF" stroke-width="3" fill="none" stroke-linecap="round"/>
  <text x="552" y="500" width="145" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF" text-anchor="middle">AI Layout Compiler</text>
  <text x="540" y="525" width="165" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#AEB8D6" text-anchor="middle">maps intent to templates, spacing, color, and hierarchy</text>

  <line x1="710" y1="365" x2="760" y2="365" stroke="#FF5CC8" stroke-width="2.5"/>
  <path d="M760 365 L741 354 L741 376 Z" fill="#FF5CC8"/>

  <rect x="780" y="125" width="440" height="485" rx="28" fill="url(#glassGrad)" stroke="#405174" stroke-width="1.2" filter="url(#softShadow)"/>
  <text x="810" y="166" width="340" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#FFFFFF">2. Generated infographic canvas</text>
  <text x="810" y="192" width="355" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#9FB0D0">Template-driven modules render as editable PowerPoint shapes.</text>

  <rect x="815" y="225" width="360" height="115" rx="20" fill="#0B1224" stroke="#35D5FF" stroke-opacity="0.35"/>
  <text x="840" y="255" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">Roadmap template</text>
  <line x1="850" y1="296" x2="1135" y2="296" stroke="#50607F" stroke-width="3"/>
  <circle cx="875" cy="296" r="13" fill="#35D5FF"/>
  <circle cx="960" cy="296" r="13" fill="#7A5CFF"/>
  <circle cx="1045" cy="296" r="13" fill="#FF5CC8"/>
  <circle cx="1130" cy="296" r="13" fill="#5CF28D"/>
  <text x="845" y="325" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#AEB8D6">Q1 Data</text>
  <text x="930" y="325" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#AEB8D6">Q2 Models</text>
  <text x="1015" y="325" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#AEB8D6">Q3 Agents</text>
  <text x="1095" y="325" width="85" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#AEB8D6">Q4 Scale</text>

  <rect x="815" y="365" width="165" height="175" rx="20" fill="#0B1224" stroke="#7A5CFF" stroke-opacity="0.35"/>
  <text x="838" y="395" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">Pyramid</text>
  <path d="M898 420 L948 505 L848 505 Z" fill="#35D5FF" opacity="0.85"/>
  <path d="M872 465 L924 465 L948 505 L848 505 Z" fill="#7A5CFF" opacity="0.9"/>
  <path d="M888 438 L908 438 L924 465 L872 465 Z" fill="#FF5CC8" opacity="0.9"/>
  <text x="856" y="525" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#AEB8D6" text-anchor="middle">strategy layers</text>

  <rect x="1005" y="365" width="170" height="175" rx="20" fill="#0B1224" stroke="#FF5CC8" stroke-opacity="0.35"/>
  <text x="1028" y="395" width="125" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">Comparison</text>
  <rect x="1032" y="425" width="48" height="78" rx="10" fill="#35D5FF"/>
  <rect x="1098" y="445" width="48" height="58" rx="10" fill="#FF5CC8"/>
  <line x1="1027" y1="510" x2="1150" y2="510" stroke="#50607F" stroke-width="2"/>
  <text x="1030" y="530" width="55" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#AEB8D6">Now</text>
  <text x="1092" y="530" width="65" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#AEB8D6">Target</text>

  <path d="M1135 128 L1194 128 L1194 187" stroke="#35D5FF" stroke-width="2" fill="none" opacity="0.7"/>
  <path d="M817 585 L875 585 L875 610" stroke="#FF5CC8" stroke-width="2" fill="none" opacity="0.7"/>
</svg>
```

## Avoid in this skill
- ❌ Treating the generated infographic as one flat screenshot; preserve editable SVG primitives for each chart component.
- ❌ Using `<foreignObject>` to embed HTML/code blocks; recreate the spec panel with native `<rect>` and `<text>`.
- ❌ Using `<pattern>` fills for template backgrounds; use gradients, translucent rectangles, and strokes instead.
- ❌ Applying `filter` to `<line>` connectors; use unfiltered lines and glow on nearby circles/paths if needed.
- ❌ Using `marker-end` on `<path>` arrows; draw arrowheads as small filled `<path>` triangles.

## Composition notes
- Keep the pipeline readable: input panel on the left, AI translation engine centered, generated infographic canvas on the right.
- Use dark executive backgrounds with cyan/purple/magenta accents to imply AI automation and template intelligence.
- Make the output area the largest visual mass; it should look like a mini gallery of infographic templates.
- Leave generous negative space around the center AI engine so the transformation moment feels important, not crowded.