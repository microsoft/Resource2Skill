# SVG Recipe — One-Page Executive Project Status Dashboard

## Visual mechanism
A polished executive status slide uses a strict grid of cards, tables, and RAG indicators, with the most important project-health signal centered in a high-contrast banner. Subtle gradients, shadows, status pills, and progress bars make the page feel like a premium command center while remaining fully scannable.

## SVG primitives needed
- 1× full-slide `<rect>` for the off-white dashboard background
- 1× top `<rect>` with gradient fill for the title banner
- 2× decorative `<path>` accents in the header for executive-keynote polish
- 5× rounded `<rect>` cards for Project Summary, Priority Matrix, Overall Status, Key Risks, and Deliverables
- 1× `<filter id="cardShadow">` applied to major cards
- 1× `<linearGradient id="headerGrad">` for the top banner
- 1× `<linearGradient id="statusGrad">` for the overall-status banner
- Multiple `<rect>` rows/cells for table headers, row striping, RAG pills, and progress bars
- Multiple `<circle>` status dots for Green / Amber / Red health indicators
- Multiple `<line>` elements for editable table grid lines
- Multiple `<text>` elements with explicit `width` for headings, body copy, labels, table cells, and inline RAG emphasis

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="headerGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#123B4A"/>
      <stop offset="55%" stop-color="#215968"/>
      <stop offset="100%" stop-color="#2F5597"/>
    </linearGradient>
    <linearGradient id="statusGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#EAF8F1"/>
      <stop offset="100%" stop-color="#FFF7E1"/>
    </linearGradient>
    <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feOffset dx="0" dy="5"/>
      <feGaussianBlur stdDeviation="6"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F4F6F8"/>
  <rect x="0" y="0" width="1280" height="86" fill="url(#headerGrad)"/>
  <path d="M940,0 C1045,4 1100,38 1170,86 L1280,86 L1280,0 Z" fill="#FFFFFF" opacity="0.10"/>
  <path d="M760,0 L930,0 C885,26 850,52 830,86 L690,86 C710,47 732,20 760,0 Z" fill="#00B0F0" opacity="0.14"/>

  <text x="48" y="36" width="780" font-family="Segoe UI, Microsoft YaHei" font-size="27" font-weight="700" fill="#FFFFFF">Project Butterfly Monthly Status Update</text>
  <text x="48" y="66" width="600" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#CDE8EF">Steering committee summary · August 2 · Prepared for Executive Sponsors</text>
  <text x="1080" y="37" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#D6EEF5" text-anchor="end">CONFIDENTIAL</text>
  <text x="1080" y="63" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF" text-anchor="end">Q4 Launch</text>

  <rect x="48" y="112" width="540" height="150" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="76" y="148" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#1E1E1E">Project Summary</text>
  <rect x="76" y="166" width="70" height="5" rx="2.5" fill="#215968"/>
  <text x="76" y="198" width="470" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#2E2E2E">Implement the future-state security center, streamlining people activities and deploying technology to support new ways of working by end of Q4.</text>
  <rect x="76" y="224" width="132" height="24" rx="12" fill="#E8F3F6"/>
  <text x="92" y="241" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#215968">Scope locked</text>
  <rect x="224" y="224" width="132" height="24" rx="12" fill="#F7EBC7"/>
  <text x="242" y="241" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#8A6500">Vendor risk</text>
  <rect x="372" y="224" width="134" height="24" rx="12" fill="#EAF7EE"/>
  <text x="392" y="241" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#008A3D">Exec aligned</text>

  <rect x="616" y="112" width="616" height="150" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="644" y="148" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#1E1E1E">Project Priority Matrix</text>
  <rect x="644" y="166" width="540" height="64" rx="12" fill="#F7F9FA"/>
  <line x1="824" y1="166" x2="824" y2="230" stroke="#D8DEE3" stroke-width="1"/>
  <line x1="1004" y1="166" x2="1004" y2="230" stroke="#D8DEE3" stroke-width="1"/>
  <text x="674" y="190" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#66717A">SCOPE</text>
  <text x="854" y="190" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#66717A">TIME</text>
  <text x="1034" y="190" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#66717A">BUDGET</text>
  <circle cx="690" cy="212" r="8" fill="#00B050"/>
  <circle cx="870" cy="212" r="8" fill="#FFC000"/>
  <circle cx="1050" cy="212" r="8" fill="#00B050"/>
  <text x="706" y="217" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#1E1E1E">Maintain</text>
  <text x="886" y="217" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#1E1E1E">Watch</text>
  <text x="1066" y="217" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#1E1E1E">Healthy</text>
  <text x="644" y="248" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#66717A">Decision rule: protect launch date first, then scope quality; absorb moderate cost variance if it prevents operational disruption.</text>

  <rect x="48" y="286" width="1184" height="112" rx="20" fill="url(#statusGrad)" stroke="#D8DEE3" stroke-width="1" filter="url(#cardShadow)"/>
  <circle cx="106" cy="342" r="31" fill="#00B050"/>
  <circle cx="106" cy="342" r="19" fill="#FFFFFF" opacity="0.28"/>
  <text x="156" y="326" width="370" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#1E1E1E">Overall Project Health</text>
  <text x="156" y="357" width="480" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="800" fill="#00A34A">GREEN</text>
  <text x="300" y="357" width="480" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" fill="#1E1E1E">— on track, with schedule watch items</text>
  <rect x="760" y="318" width="410" height="18" rx="9" fill="#DDE4EA"/>
  <rect x="760" y="318" width="311" height="18" rx="9" fill="#00B050"/>
  <text x="760" y="358" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#46515A">Milestone completion</text>
  <text x="1116" y="358" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="800" fill="#1E1E1E" text-anchor="end">76%</text>

  <rect x="48" y="424" width="740" height="248" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="76" y="458" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#1E1E1E">Deliverables Status</text>
  <rect x="76" y="478" width="684" height="32" rx="6" fill="#215968"/>
  <text x="94" y="499" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">Deliverable</text>
  <text x="370" y="499" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">Owner</text>
  <text x="500" y="499" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">Due</text>
  <text x="622" y="499" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">Status</text>

  <rect x="76" y="510" width="684" height="31" fill="#FFFFFF"/>
  <rect x="76" y="541" width="684" height="31" fill="#F7F9FA"/>
  <rect x="76" y="572" width="684" height="31" fill="#FFFFFF"/>
  <rect x="76" y="603" width="684" height="31" fill="#F7F9FA"/>
  <line x1="350" y1="478" x2="350" y2="634" stroke="#D8DEE3" stroke-width="1"/>
  <line x1="484" y1="478" x2="484" y2="634" stroke="#D8DEE3" stroke-width="1"/>
  <line x1="604" y1="478" x2="604" y2="634" stroke="#D8DEE3" stroke-width="1"/>
  <line x1="76" y1="541" x2="760" y2="541" stroke="#D8DEE3" stroke-width="1"/>
  <line x1="76" y1="572" x2="760" y2="572" stroke="#D8DEE3" stroke-width="1"/>
  <line x1="76" y1="603" x2="760" y2="603" stroke="#D8DEE3" stroke-width="1"/>
  <line x1="76" y1="634" x2="760" y2="634" stroke="#D8DEE3" stroke-width="1"/>
  <text x="94" y="531" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#1E1E1E">Operating model signed off</text>
  <text x="370" y="531" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#1E1E1E">Chen</text>
  <text x="500" y="531" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#1E1E1E">Aug 12</text>
  <circle cx="634" cy="526" r="8" fill="#00B050"/><text x="650" y="531" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#008A3D">Green</text>
  <text x="94" y="562" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#1E1E1E">Vendor integration testing</text>
  <text x="370" y="562" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#1E1E1E">Patel</text>
  <text x="500" y="562" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#1E1E1E">Aug 29</text>
  <circle cx="634" cy="557" r="8" fill="#FFC000"/><text x="650" y="562" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#9A7100">Amber</text>
  <text x="94" y="593" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#1E1E1E">Training curriculum ready</text>
  <text x="370" y="593" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#1E1E1E">Morgan</text>
  <text x="500" y="593" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#1E1E1E">Sep 06</text>
  <circle cx="634" cy="588" r="8" fill="#00B050"/><text x="650" y="593" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#008A3D">Green</text>
  <text x="94" y="624" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#1E1E1E">Legacy data migration</text>
  <text x="370" y="624" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#1E1E1E">Garcia</text>
  <text x="500" y="624" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#1E1E1E">Sep 18</text>
  <circle cx="634" cy="619" r="8" fill="#FF0000"/><text x="650" y="624" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#C00000">Red</text>

  <rect x="816" y="424" width="416" height="248" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="844" y="458" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#1E1E1E">Key Risks &amp; Executive Asks</text>
  <rect x="844" y="482" width="360" height="46" rx="10" fill="#FFF3CC"/>
  <circle cx="866" cy="505" r="8" fill="#FFC000"/>
  <text x="884" y="501" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#1E1E1E">Vendor test environment delay</text>
  <text x="884" y="519" width="290" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#5B6570">Ask: sponsor escalation by Friday.</text>
  <rect x="844" y="540" width="360" height="46" rx="10" fill="#FDE9E7"/>
  <circle cx="866" cy="563" r="8" fill="#FF0000"/>
  <text x="884" y="559" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#1E1E1E">Data migration defect backlog</text>
  <text x="884" y="577" width="290" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#5B6570">Ask: approve two-week tiger team.</text>
  <rect x="844" y="598" width="360" height="46" rx="10" fill="#EAF7EE"/>
  <circle cx="866" cy="621" r="8" fill="#00B050"/>
  <text x="884" y="617" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#1E1E1E">Change network mobilized</text>
  <text x="884" y="635" width="290" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#5B6570">No decision needed; maintain cadence.</text>
</svg>
```

## Avoid in this skill
- ❌ A single dense table filling the whole slide; executives need a fast hierarchy before details.
- ❌ Using only red/yellow/green text without shape-based indicators; color-blind users and printed copies need circles, pills, or labels.
- ❌ Tiny table copy below 10–11 pt; the slide must remain readable in a conference room.
- ❌ Applying filters to table grid `<line>` elements; keep shadows on card rectangles only.
- ❌ Overusing gradients inside data cells; reserve gradients for header/status areas so RAG colors stay unambiguous.

## Composition notes
- Keep the top 10–12% of the slide as a strong context banner with project name, reporting date, and confidentiality/status metadata.
- Put the “overall health” band near the center so the eye lands there after reading the summary and matrix.
- Reserve the bottom half for proof: deliverables on the left, key risks and asks on the right.
- Use dark teal/navy for structure, white cards for content, and RAG colors only for status meaning so the color rhythm stays disciplined.