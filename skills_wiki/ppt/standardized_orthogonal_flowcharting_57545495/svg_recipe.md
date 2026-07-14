# SVG Recipe — Standardized Orthogonal Flowcharting

## Visual mechanism
A flowchart becomes executive-clean by locking every node to a grid, using standard symbols, and routing every connector as a 90-degree orthogonal elbow. The visual rhythm comes from equal node widths, consistent vertical spacing, crisp arrowheads, and concise centered labels.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 2× translucent `<rect>` lane panels for main path and exception path zones
- 6× node `<rect>` shapes for terminators and process steps
- 1× `<path>` diamond for the decision node
- 1× mini legend `<path>` diamond and 2× mini legend `<rect>` symbols
- Multiple `<line>` elements for orthogonal connector segments; keep them horizontal or vertical only
- Multiple small filled `<path>` triangles for arrowheads instead of relying on path markers
- Multiple `<text>` elements with explicit `width` for title, subtitles, node labels, branch labels, and legend labels
- 3× `<linearGradient>` fills for premium blue, amber rework, and green completion states
- 1× `<filter id="nodeShadow">` applied only to rect/path nodes for subtle elevation

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8FBFF"/>
      <stop offset="100%" stop-color="#EAF1FA"/>
    </linearGradient>
    <linearGradient id="blueNode" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#5D8CE6"/>
      <stop offset="100%" stop-color="#2F5597"/>
    </linearGradient>
    <linearGradient id="amberNode" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#F3B64A"/>
      <stop offset="100%" stop-color="#D88416"/>
    </linearGradient>
    <linearGradient id="greenNode" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#42C586"/>
      <stop offset="100%" stop-color="#19835A"/>
    </linearGradient>
    <filter id="nodeShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="8"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>

  <line x1="160" y1="120" x2="1120" y2="120" stroke="#D6E0EF" stroke-width="1"/>
  <line x1="160" y1="220" x2="1120" y2="220" stroke="#D6E0EF" stroke-width="1"/>
  <line x1="160" y1="320" x2="1120" y2="320" stroke="#D6E0EF" stroke-width="1"/>
  <line x1="160" y1="420" x2="1120" y2="420" stroke="#D6E0EF" stroke-width="1"/>
  <line x1="160" y1="520" x2="1120" y2="520" stroke="#D6E0EF" stroke-width="1"/>
  <line x1="160" y1="620" x2="1120" y2="620" stroke="#D6E0EF" stroke-width="1"/>
  <line x1="400" y1="80" x2="400" y2="670" stroke="#DDE6F2" stroke-width="1"/>
  <line x1="640" y1="80" x2="640" y2="670" stroke="#DDE6F2" stroke-width="1"/>
  <line x1="880" y1="80" x2="880" y2="670" stroke="#DDE6F2" stroke-width="1"/>

  <text x="64" y="48" width="700" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#1F3763">Hiring SOP — standardized orthogonal flow</text>
  <text x="66" y="78" width="680" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#61738A">Universal symbols, equal spacing, and right-angle routing make the decision logic instantly scannable.</text>

  <rect x="480" y="86" width="320" height="594" rx="22" fill="#FFFFFF" fill-opacity="0.55" stroke="#B9C8DC" stroke-width="1.5" stroke-dasharray="8 8"/>
  <rect x="840" y="250" width="300" height="180" rx="22" fill="#FFF7E8" fill-opacity="0.70" stroke="#E7B45F" stroke-width="1.5" stroke-dasharray="8 8"/>
  <text x="640" y="108" width="240" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" letter-spacing="2" fill="#6E7F95">MAIN PATH</text>
  <text x="990" y="272" width="220" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" letter-spacing="2" fill="#B06B12">EXCEPTION PATH</text>

  <g stroke="#334A68" stroke-width="3" stroke-linecap="round">
    <line x1="640" y1="158" x2="640" y2="178"/>
    <line x1="640" y1="254" x2="640" y2="263"/>
    <line x1="640" y1="395" x2="640" y2="418"/>
    <line x1="640" y1="494" x2="640" y2="513"/>
    <line x1="640" y1="589" x2="640" y2="613"/>
    <line x1="770" y1="335" x2="868" y2="335"/>
    <line x1="990" y1="302" x2="990" y2="222"/>
    <line x1="990" y1="222" x2="762" y2="222"/>
  </g>

  <path d="M640 190 L632 178 L648 178 Z" fill="#334A68"/>
  <path d="M640 275 L632 263 L648 263 Z" fill="#334A68"/>
  <path d="M640 430 L632 418 L648 418 Z" fill="#334A68"/>
  <path d="M640 525 L632 513 L648 513 Z" fill="#334A68"/>
  <path d="M640 625 L632 613 L648 613 Z" fill="#334A68"/>
  <path d="M880 335 L868 327 L868 343 Z" fill="#334A68"/>
  <path d="M750 222 L762 214 L762 230 Z" fill="#334A68"/>

  <rect x="530" y="100" width="220" height="58" rx="29" fill="url(#blueNode)" stroke="#24477F" stroke-width="1.5" filter="url(#nodeShadow)"/>
  <text x="640" y="126" width="190" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">
    <tspan x="640" dy="0">Trigger request</tspan>
    <tspan x="640" dy="20" font-size="12" font-weight="600" fill="#DCE8FF">Start</tspan>
  </text>

  <rect x="530" y="190" width="220" height="64" rx="8" fill="url(#blueNode)" stroke="#24477F" stroke-width="1.5" filter="url(#nodeShadow)"/>
  <text x="640" y="216" width="190" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF">
    <tspan x="640" dy="0">Draft requisition</tspan>
    <tspan x="640" dy="20" font-size="12" font-weight="600" fill="#DCE8FF">Owner: hiring manager</tspan>
  </text>

  <path d="M640 275 L770 335 L640 395 L510 335 Z" fill="url(#blueNode)" stroke="#24477F" stroke-width="1.5" filter="url(#nodeShadow)"/>
  <text x="640" y="323" width="190" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF">
    <tspan x="640" dy="0">Budget</tspan>
    <tspan x="640" dy="20">approved?</tspan>
  </text>

  <rect x="530" y="430" width="220" height="64" rx="8" fill="url(#blueNode)" stroke="#24477F" stroke-width="1.5" filter="url(#nodeShadow)"/>
  <text x="640" y="457" width="190" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF">
    <tspan x="640" dy="0">Publish role</tspan>
    <tspan x="640" dy="20" font-size="12" font-weight="600" fill="#DCE8FF">Careers + referrals</tspan>
  </text>

  <rect x="530" y="525" width="220" height="64" rx="8" fill="url(#blueNode)" stroke="#24477F" stroke-width="1.5" filter="url(#nodeShadow)"/>
  <text x="640" y="552" width="190" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF">
    <tspan x="640" dy="0">Screen candidates</tspan>
    <tspan x="640" dy="20" font-size="12" font-weight="600" fill="#DCE8FF">Recruiter review</tspan>
  </text>

  <rect x="530" y="625" width="220" height="54" rx="27" fill="url(#greenNode)" stroke="#166B4B" stroke-width="1.5" filter="url(#nodeShadow)"/>
  <text x="640" y="658" width="190" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF">Advance to Stage 2</text>

  <rect x="880" y="302" width="220" height="66" rx="8" fill="url(#amberNode)" stroke="#B96E10" stroke-width="1.5" filter="url(#nodeShadow)"/>
  <text x="990" y="329" width="190" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF">
    <tspan x="990" dy="0">Revise scope</tspan>
    <tspan x="990" dy="20" font-size="12" font-weight="600" fill="#FFF4D8">Loop back to draft</tspan>
  </text>

  <text x="672" y="414" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#19835A">YES</text>
  <text x="820" y="324" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#B06B12">NO</text>

  <rect x="72" y="582" width="235" height="78" rx="16" fill="#FFFFFF" fill-opacity="0.75" stroke="#CAD6E6"/>
  <rect x="94" y="602" width="42" height="22" rx="11" fill="#5D8CE6"/>
  <rect x="94" y="632" width="42" height="22" rx="4" fill="#5D8CE6"/>
  <path d="M201 602 L224 613 L201 624 L178 613 Z" fill="#5D8CE6"/>
  <text x="146" y="618" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#3A4B61">Terminator</text>
  <text x="146" y="648" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#3A4B61">Process</text>
  <text x="235" y="618" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#3A4B61">Decision</text>
</svg>
```

## Avoid in this skill
- ❌ Curved or diagonal connector paths; the technique depends on orthogonal horizontal/vertical routing.
- ❌ `marker-end` on `<path>` connectors; use `<line>` segments plus small triangle `<path>` arrowheads.
- ❌ Unequal node widths or inconsistent vertical spacing, which breaks the standardized SOP rhythm.
- ❌ Long paragraphs inside nodes; keep each label to 1–4 words plus an optional small owner/status line.
- ❌ Text without explicit `width` attributes; PowerPoint translation needs fixed text boxes.

## Composition notes
- Keep the primary path on the vertical centerline; use side branches only for exceptions, rework, or termination paths.
- Reserve generous whitespace around the decision diamond so branch labels and elbows remain readable.
- Use one dominant node color for the canonical flow, then one accent color for exception/rework paths.
- Align node centers, arrowheads, and connector endpoints mathematically; small misalignments make flowcharts feel amateur.