# SVG Recipe — Horizontal Process Flow

## Visual mechanism
A left-to-right sequence is anchored by a low horizontal baseline, with each step rising on a thin vertical stem into a large alternating-color oval, a floating white information card, and a circular icon badge. The result feels like a premium corporate process timeline: structured, rhythmic, and easy to scan.

## SVG primitives needed
- 1× `<rect>` for the warm beige slide background
- 1× `<rect>` for each white floating content card
- 5× large `<ellipse>` for oversized vertical color backplates behind each step
- 5× `<line>` for vertical stems from the baseline to each process node
- 2× `<line>` for the bottom baseline and subtle top/right frame accents
- 5× small `<circle>` for baseline node dots
- 10× `<circle>` for icon badge rings and badge interiors
- Multiple `<rect>`, `<circle>`, `<line>`, and `<path>` primitives for editable mini-icons inside the badges
- Multiple `<text width="...">` blocks for slide title, subtitle, card headings, bullets, and step numbers
- 1× `<filter id="cardShadow">` using `feOffset + feGaussianBlur + feMerge` for elevated card shadows
- 1× `<filter id="badgeShadow">` using `feGaussianBlur`/offset merge for icon badge depth

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="6" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="8" result="blur"/>
      <feColorMatrix in="blur" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .16 0" result="shadow"/>
      <feMerge><feMergeNode in="shadow"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="badgeShadow" x="-25%" y="-25%" width="150%" height="150%">
      <feOffset dx="0" dy="3" in="SourceAlpha" result="bOff"/>
      <feGaussianBlur in="bOff" stdDeviation="4" result="bBlur"/>
      <feColorMatrix in="bBlur" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .18 0"/>
      <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#f1ecdf"/>
  <line x1="770" y1="15" x2="1265" y2="15" stroke="#17374a" stroke-width="1.5"/>
  <line x1="1265" y1="0" x2="1265" y2="720" stroke="#17374a" stroke-width="1.2"/>
  <circle cx="38" cy="45" r="27" fill="#ffc400"/>
  <text x="25" y="60" width="880" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="36" font-weight="800" fill="#101820" letter-spacing="1.5">Steps to develop staff performance evaluation system</text>
  <text x="27" y="88" width="980" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#6f6f68">The slide shows steps to develop an effective performance evaluation system for an organization which ensures accountability, fairness and growth.</text>

  <g transform="translate(986 39)">
    <circle cx="14" cy="18" r="17" fill="#20a7f5"/><circle cx="45" cy="16" r="19" fill="#20a7f5"/><circle cx="76" cy="18" r="17" fill="#20a7f5"/>
    <path d="M0,45 C2,28 26,28 28,45 L28,72 L0,72 Z" fill="#20a7f5"/><path d="M29,44 C31,25 59,25 61,44 L61,73 L29,73 Z" fill="#20a7f5"/><path d="M62,45 C64,28 88,28 90,45 L90,72 L62,72 Z" fill="#20a7f5"/>
    <text x="105" y="32" width="100" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="32" font-weight="800" fill="#18a5f4">Slide</text>
    <text x="105" y="72" width="100" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="31" font-weight="800" fill="#101820">Team</text>
  </g>

  <line x1="0" y1="650" x2="1280" y2="650" stroke="#ffffff" stroke-width="8"/>
  <line x1="0" y1="650" x2="1280" y2="650" stroke="#e3ddce" stroke-width="2"/>
  <line x1="145" y1="475" x2="145" y2="650" stroke="#082f45" stroke-width="1.5"/>
  <line x1="395" y1="475" x2="395" y2="650" stroke="#ffc400" stroke-width="1.5"/>
  <line x1="645" y1="475" x2="645" y2="650" stroke="#082f45" stroke-width="1.5"/>
  <line x1="895" y1="475" x2="895" y2="650" stroke="#ffc400" stroke-width="1.5"/>
  <line x1="1135" y1="475" x2="1135" y2="650" stroke="#082f45" stroke-width="1.5"/>

  <ellipse cx="145" cy="412" rx="92" ry="192" fill="#062f47"/>
  <ellipse cx="395" cy="384" rx="90" ry="188" fill="#ffc400"/>
  <ellipse cx="645" cy="386" rx="91" ry="176" fill="#062f47"/>
  <ellipse cx="895" cy="356" rx="90" ry="188" fill="#ffc400"/>
  <ellipse cx="1135" cy="334" rx="92" ry="186" fill="#062f47"/>
  <circle cx="145" cy="650" r="11" fill="#062f47" stroke="#ffffff" stroke-width="4"/>
  <circle cx="395" cy="650" r="11" fill="#ffc400" stroke="#ffffff" stroke-width="4"/>
  <circle cx="645" cy="650" r="11" fill="#062f47" stroke="#ffffff" stroke-width="4"/>
  <circle cx="895" cy="650" r="11" fill="#ffc400" stroke="#ffffff" stroke-width="4"/>
  <circle cx="1135" cy="650" r="11" fill="#062f47" stroke="#ffffff" stroke-width="4"/>

  <rect x="38" y="317" width="214" height="220" fill="#ffffff" filter="url(#cardShadow)"/>
  <rect x="290" y="286" width="210" height="220" fill="#ffffff" filter="url(#cardShadow)"/>
  <rect x="542" y="274" width="210" height="218" fill="#ffffff" filter="url(#cardShadow)"/>
  <rect x="786" y="255" width="211" height="220" fill="#ffffff" filter="url(#cardShadow)"/>
  <rect x="1031" y="234" width="210" height="252" fill="#ffffff" filter="url(#cardShadow)"/>

  <g filter="url(#badgeShadow)">
    <circle cx="145" cy="261" r="41" fill="#ffffff"/><circle cx="145" cy="261" r="31" fill="#062f47"/>
    <circle cx="395" cy="232" r="41" fill="#ffffff"/><circle cx="395" cy="232" r="31" fill="#ffc400"/>
    <circle cx="645" cy="220" r="41" fill="#ffffff"/><circle cx="645" cy="220" r="31" fill="#062f47"/>
    <circle cx="895" cy="201" r="41" fill="#ffffff"/><circle cx="895" cy="201" r="31" fill="#ffc400"/>
    <circle cx="1135" cy="180" r="41" fill="#ffffff"/><circle cx="1135" cy="180" r="31" fill="#062f47"/>
  </g>

  <g stroke="#ffffff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <rect x="126" y="245" width="38" height="32" rx="2"/><line x1="126" y1="254" x2="164" y2="254"/><line x1="134" y1="240" x2="134" y2="249"/><line x1="156" y1="240" x2="156" y2="249"/><line x1="134" y1="262" x2="157" y2="262"/><line x1="134" y1="270" x2="151" y2="270"/>
    <rect x="378" y="215" width="26" height="35" rx="2"/><path d="M404 221 L412 221 L412 244"/><line x1="384" y1="226" x2="395" y2="226"/><line x1="384" y1="235" x2="395" y2="235"/><path d="M382 244 l4 4 l8 -10"/>
    <circle cx="645" cy="225" r="12"/><path d="M626 203 h17 q4 0 4 4 v9 q0 4 -4 4 h-5 l-5 6 v-6 h-7 q-4 0 -4-4 v-9 q0-4 4-4z"/><path d="M654 204 h13 q4 0 4 4 v8 q0 4 -4 4 h-3 v6 l-5-6 h-5"/>
    <path d="M874 211 A22 22 0 0 1 916 211"/><line x1="895" y1="211" x2="909" y2="196"/><circle cx="895" cy="211" r="3"/><line x1="878" y1="211" x2="883" y2="211"/><line x1="907" y1="211" x2="912" y2="211"/>
    <rect x="1120" y="160" width="30" height="39" rx="2"/><line x1="1127" y1="170" x2="1144" y2="170"/><line x1="1127" y1="178" x2="1144" y2="178"/><line x1="1127" y1="186" x2="1138" y2="186"/><path d="M1123 194 l4 4 l7 -9"/>
  </g>

  <text x="93" y="340" width="105" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="800" fill="#3c3c3c"><tspan x="145">Set a Schedule</tspan><tspan x="145" dy="17">for Conduct</tspan></text>
  <text x="64" y="381" width="160" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#555"><tspan x="64">○  Build a</tspan><tspan x="82" dy="15">conducting schedule</tspan><tspan x="64" dy="15">○  Ensure consistency in</tspan><tspan x="82" dy="15">review process</tspan><tspan x="64" dy="15">○  Add text here</tspan></text>
  <text x="132" y="519" width="40" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="21" font-weight="800" fill="#062f47">01</text>

  <text x="320" y="309" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="800" fill="#3c3c3c"><tspan x="395">Determine Disciplinary</tspan><tspan x="395" dy="17">and Terminating Proc Policies</tspan></text>
  <text x="309" y="350" width="165" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#555"><tspan x="309">○  Prepare a structured and</tspan><tspan x="327" dy="15">descriptive conduct</tspan><tspan x="327" dy="15">and termination</tspan><tspan x="327" dy="15">procedure document</tspan><tspan x="309" dy="15">○  Provide a precis of procedure</tspan><tspan x="327" dy="15">that would be taken in-case</tspan><tspan x="327" dy="15">of wrongful conduct etc.</tspan><tspan x="309" dy="15">○  Add text here</tspan></text>
  <text x="383" y="488" width="40" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="21" font-weight="800" fill="#ffc400">02</text>

  <text x="588" y="298" width="115" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="800" fill="#3c3c3c"><tspan x="647">Establish</tspan><tspan x="647" dy="17">Feedback Instructions</tspan></text>
  <text x="562" y="337" width="160" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#555"><tspan x="562">○  Set norms and standardize</tspan><tspan x="580" dy="15">feedback process</tspan><tspan x="562" dy="15">○  Make sure to include:</tspan><tspan x="582" dy="15">›  Value feedback</tspan><tspan x="582" dy="15">›  Expectations</tspan><tspan x="582" dy="15">from employees</tspan><tspan x="582" dy="15">›  Add text here</tspan><tspan x="562" dy="15">○  Add text here</tspan></text>
  <text x="635" y="477" width="40" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="21" font-weight="800" fill="#062f47">03</text>

  <text x="850" y="278" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="800" fill="#3c3c3c"><tspan x="895">Determine</tspan><tspan x="895" dy="17">Performance Measure</tspan></text>
  <text x="808" y="319" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#555"><tspan x="808">○  Set a benchmark for</tspan><tspan x="826" dy="15">performance measurements</tspan><tspan x="826" dy="15">(metrics)</tspan><tspan x="808" dy="15">○  Qualitative and</tspan><tspan x="826" dy="15">quantifiable targets</tspan><tspan x="808" dy="15">○  Add text here</tspan></text>
  <text x="883" y="457" width="40" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="21" font-weight="800" fill="#ffc400">04</text>

  <text x="1100" y="258" width="75" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="800" fill="#3c3c3c"><tspan x="1138">Develop</tspan><tspan x="1138" dy="17">Evaluation form</tspan></text>
  <text x="1055" y="299" width="160" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#555"><tspan x="1055">○  Adopt a standard assessment</tspan><tspan x="1073" dy="15">form or procedure</tspan><tspan x="1073" dy="15">for all evaluations</tspan><tspan x="1073" dy="15">(ensures consistency)</tspan><tspan x="1055" dy="15">○  Focus area of forms should be</tspan><tspan x="1073" dy="15">on important</tspan><tspan x="1073" dy="15">aspects of job</tspan><tspan x="1055" dy="15">○  Add text here</tspan></text>
  <text x="1124" y="436" width="40" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="21" font-weight="800" fill="#062f47">05</text>

  <text x="423" y="716" width="450" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="10" fill="#8a857b">This slide is 100% editable. Adapt it to your needs and capture your audience's attention.</text>
  <text x="1257" y="716" width="18" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#4f4f4f">3</text>
</svg>
```

## Avoid in this skill
- ❌ Arrow markers on paths; this layout reads through spacing and node sequence, not arrowheads.
- ❌ `<mask>` or clipping cards with non-image elements; use plain editable ovals, rectangles, and circles instead.
- ❌ Overcrowding every card with dense paragraphs; preserve the timeline rhythm by using short bullets.
- ❌ Applying filters to `<line>` stems or baselines; shadows should go on cards and badges only.

## Composition notes
- Keep the title band in the top 15–18% of the slide; the process objects should dominate the middle and lower canvas.
- Use evenly spaced x positions for steps, but vary the oval/card vertical height slightly for a more editorial, less mechanical feel.
- Alternate a deep navy and a bright mustard accent to create strong left-to-right rhythm.
- Cards should overlap the large ovals by 50–70%, so the colored backplates feel integrated rather than decorative afterthoughts.