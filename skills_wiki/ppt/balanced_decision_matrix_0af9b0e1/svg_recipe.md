# SVG Recipe — Balanced Decision Matrix

## Visual mechanism
A symmetrical two-column decision board gives equal visual weight to benefits and risks, using green/red color coding, mirrored icon medallions, and structured evidence rows. Soft cards, subtle shadows, and small priority chips make the analysis feel executive-ready while remaining fully scannable.

## SVG primitives needed
- 1× `<rect>` for the full-slide pale background
- 2× large `<rect>` for the Pros and Cons content cards
- 2× rounded `<rect>` for colored header bands
- 2× thin `<rect>` for vertical accent rails inside each card
- 10× small rounded `<rect>` for priority / impact chips
- 2× footer `<rect>` elements for the balanced recommendation bar
- 2× `<circle>` for icon medallions
- 10× small `<circle>` elements for list bullets
- 4× decorative `<path>` elements for soft background blobs and custom thumbs icons
- 1× `<line>` for the dashed center divider
- 1× `<filter id="cardShadow">` applied to card rectangles
- 1× `<filter id="softGlow">` applied to icon medallions
- 3× `<linearGradient>` fills for headers, background, and footer accents
- Multiple `<text>` elements with explicit `width` attributes for title, headers, list items, chips, and verdict labels

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7FAFC"/>
      <stop offset="55%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F3F6F9"/>
    </linearGradient>
    <linearGradient id="prosGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#7ED957"/>
      <stop offset="100%" stop-color="#31A65A"/>
    </linearGradient>
    <linearGradient id="consGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FF6B7A"/>
      <stop offset="100%" stop-color="#D93B4C"/>
    </linearGradient>
    <linearGradient id="verdictGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#31A65A"/>
      <stop offset="49%" stop-color="#B8C2CC"/>
      <stop offset="51%" stop-color="#B8C2CC"/>
      <stop offset="100%" stop-color="#D93B4C"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="14"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.08 0 0 0 0 0.11 0 0 0 0 0.15 0 0 0 0.18 0"/>
      <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="softGlow" x="-70%" y="-70%" width="240%" height="240%">
      <feGaussianBlur stdDeviation="7" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <path d="M-40 120 C120 30 250 60 330 150 C390 220 285 285 160 250 C50 220 -35 220 -40 120Z" fill="#DFF5E5" opacity="0.55"/>
  <path d="M1300 86 C1160 18 1040 48 960 142 C900 212 980 286 1115 252 C1220 226 1305 204 1300 86Z" fill="#FFE3E7" opacity="0.62"/>

  <text x="80" y="58" width="1120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#263238">Analysis of the Proposed Initiative</text>
  <text x="220" y="90" width="840" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#66737F">A balanced view of strategic upside and implementation risk before committing resources</text>

  <line x1="640" y1="138" x2="640" y2="604" stroke="#CBD3DA" stroke-width="2" stroke-dasharray="7 9"/>
  <rect x="552" y="610" width="176" height="34" rx="17" fill="url(#verdictGrad)" opacity="0.92"/>
  <text x="640" y="632" width="176" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">BALANCED CALL</text>

  <rect x="72" y="132" width="536" height="468" rx="24" fill="#FFFFFF" stroke="#E3E8EE" stroke-width="1.4" filter="url(#cardShadow)"/>
  <rect x="672" y="132" width="536" height="468" rx="24" fill="#FFFFFF" stroke="#E3E8EE" stroke-width="1.4" filter="url(#cardShadow)"/>

  <rect x="104" y="156" width="472" height="78" rx="20" fill="url(#prosGrad)"/>
  <rect x="704" y="156" width="472" height="78" rx="20" fill="url(#consGrad)"/>

  <circle cx="150" cy="195" r="31" fill="#FFFFFF" opacity="0.24" filter="url(#softGlow)"/>
  <circle cx="750" cy="195" r="31" fill="#FFFFFF" opacity="0.24" filter="url(#softGlow)"/>
  <path d="M129 191 h15 v32 h-15 z M149 220 h36 c5 0 8-3 9-8 l5-24 c1-5-2-9-7-9 h-18 l3-13 c1-7-3-13-9-13 l-15 28 h-4 z" fill="#FFFFFF"/>
  <path d="M729 199 h15 v32 h-15 z M749 202 h36 c5 0 8 3 9 8 l5 24 c1 5-2 9-7 9 h-18 l3 13 c1 7-3 13-9 13 l-15-28 h-4 z" fill="#FFFFFF" transform="rotate(180 764 226)"/>

  <text x="194" y="188" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="700" fill="#FFFFFF">Pros</text>
  <text x="194" y="213" width="340" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#EFFFF2">Value drivers and positive outcomes</text>
  <text x="794" y="188" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="700" fill="#FFFFFF">Cons</text>
  <text x="794" y="213" width="340" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#FFF1F3">Risks, constraints, and trade-offs</text>

  <rect x="104" y="268" width="7" height="284" rx="3.5" fill="#49B968"/>
  <rect x="704" y="268" width="7" height="284" rx="3.5" fill="#E04C5D"/>

  <circle cx="134" cy="286" r="7" fill="#49B968"/>
  <text x="154" y="292" width="325" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="600" fill="#263238">Focuses investment on what matters most</text>
  <rect x="494" y="272" width="70" height="25" rx="12.5" fill="#E7F7EB"/>
  <text x="529" y="290" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#258B49">HIGH</text>

  <circle cx="134" cy="340" r="7" fill="#49B968"/>
  <text x="154" y="336" width="318" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="600" fill="#263238">Creates a shared operating vision</text>
  <text x="154" y="357" width="318" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#697782">Leadership message is easier to repeat across teams.</text>
  <rect x="494" y="326" width="70" height="25" rx="12.5" fill="#E7F7EB"/>
  <text x="529" y="344" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#258B49">HIGH</text>

  <circle cx="134" cy="406" r="7" fill="#49B968"/>
  <text x="154" y="412" width="325" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="600" fill="#263238">Engages the organization early</text>
  <rect x="494" y="392" width="70" height="25" rx="12.5" fill="#EEF4F0"/>
  <text x="529" y="410" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#4D7F60">MED</text>

  <circle cx="134" cy="460" r="7" fill="#49B968"/>
  <text x="154" y="466" width="325" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="600" fill="#263238">Progress can be monitored with clear KPIs</text>
  <rect x="494" y="446" width="70" height="25" rx="12.5" fill="#E7F7EB"/>
  <text x="529" y="464" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#258B49">HIGH</text>

  <circle cx="134" cy="514" r="7" fill="#49B968"/>
  <text x="154" y="520" width="325" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="600" fill="#263238">Improves accountability across workstreams</text>
  <rect x="494" y="500" width="70" height="25" rx="12.5" fill="#EEF4F0"/>
  <text x="529" y="518" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#4D7F60">MED</text>

  <circle cx="734" cy="286" r="7" fill="#E04C5D"/>
  <text x="754" y="292" width="325" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="600" fill="#263238">Rigid implementation model may slow pivots</text>
  <rect x="1094" y="272" width="70" height="25" rx="12.5" fill="#FCE7EA"/>
  <text x="1129" y="290" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#C33445">HIGH</text>

  <circle cx="734" cy="340" r="7" fill="#E04C5D"/>
  <text x="754" y="346" width="325" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="600" fill="#263238">Requires sustained executive commitment</text>
  <rect x="1094" y="326" width="70" height="25" rx="12.5" fill="#FCE7EA"/>
  <text x="1129" y="344" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#C33445">HIGH</text>

  <circle cx="734" cy="406" r="7" fill="#E04C5D"/>
  <text x="754" y="402" width="318" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="600" fill="#263238">Objectives must remain stable for 3–5 years</text>
  <text x="754" y="423" width="318" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#697782">Volatile markets could make targets obsolete.</text>
  <rect x="1094" y="392" width="70" height="25" rx="12.5" fill="#F6ECEE"/>
  <text x="1129" y="410" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#9A4D58">MED</text>

  <circle cx="734" cy="472" r="7" fill="#E04C5D"/>
  <text x="754" y="478" width="325" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="600" fill="#263238">Potential resistance to process change</text>
  <rect x="1094" y="458" width="70" height="25" rx="12.5" fill="#FCE7EA"/>
  <text x="1129" y="476" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#C33445">HIGH</text>

  <circle cx="734" cy="526" r="7" fill="#E04C5D"/>
  <text x="754" y="532" width="325" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="600" fill="#263238">Benefits may lag initial transformation costs</text>
  <rect x="1094" y="512" width="70" height="25" rx="12.5" fill="#F6ECEE"/>
  <text x="1129" y="530" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#9A4D58">MED</text>
</svg>
```

## Avoid in this skill
- ❌ Using only plain bullet text without cards, icons, or color-coded structure; it loses the “balanced decision” signal.
- ❌ Making one column visually heavier than the other unless the conclusion is intentionally biased.
- ❌ Relying on emoji thumbs icons if the deck must be brand-consistent; custom `<path>` icons translate more predictably.
- ❌ Applying `filter` to the dashed center `<line>`; line filters are dropped by the translator.
- ❌ Clipping or masking shape cards; keep clips only for `<image>` elements if you add photography.

## Composition notes
- Keep the two columns equal width with a clear central gutter; the symmetry is the main credibility cue.
- Use green and red as accents, not full-card fills, so body text remains readable and executive.
- Reserve the top 15–18% of the slide for title and context; place the decision evidence in the central 65%.
- Add small impact chips to convert a basic pros/cons list into a lightweight decision matrix without overcrowding.