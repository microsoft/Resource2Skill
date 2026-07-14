# SVG Recipe — Interlocking Alternating Milestones

## Visual mechanism
A premium horizontal timeline is built from thick connector strokes that pass underneath open donut-arc nodes. Each milestone alternates its annotation above and below the track, with a perpendicular branch line emerging through the arc gap to create an interlocking, engineered rhythm.

## SVG primitives needed
- 1× `<rect>` for the soft radial-gradient slide background
- 1× `<rect>` for a small title accent bar
- 4× `<line>` for the thick segmented horizontal timeline connectors
- 10× `<line>` for vertical milestone stems and short horizontal annotation rules
- 5× `<path>` for incomplete circular outer arcs with top/bottom gaps
- 5× `<circle>` for colored inner milestone cores
- 5× `<circle>` for small terminal dots at the text branches
- 5× `<circle>` for subtle white highlight glints on the cores
- 16× `<text>` blocks for title, deck kicker, milestone numbers, years, subtitles, and descriptions
- 1× `<radialGradient>` for the washed executive background
- 1× `<filter id="coreShadow">` applied to milestone cores for soft depth
- 1× `<filter id="softGlow">` applied to outer arcs for a light premium lift

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgWash" cx="50%" cy="45%" r="72%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="62%" stop-color="#F8FAFC"/>
      <stop offset="100%" stop-color="#EEF2F6"/>
    </radialGradient>
    <filter id="coreShadow" x="-40%" y="-40%" width="180%" height="180%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="7" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="1.2"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>
  <rect x="88" y="92" width="70" height="6" rx="3" fill="#3DB2D3"/>
  <text x="88" y="72" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="700" fill="#343A40">Strategic Roadmap Timeline</text>
  <text x="90" y="118" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#7A838D">Five interlocking milestones with alternating evidence blocks</text>

  <!-- timeline connectors drawn first so nodes visually cap the seams -->
  <line x1="180" y1="360" x2="410" y2="360" stroke="#2A4B7C" stroke-width="9" stroke-linecap="round"/>
  <line x1="410" y1="360" x2="640" y2="360" stroke="#3DB2D3" stroke-width="9" stroke-linecap="round"/>
  <line x1="640" y1="360" x2="870" y2="360" stroke="#F29C38" stroke-width="9" stroke-linecap="round"/>
  <line x1="870" y1="360" x2="1100" y2="360" stroke="#D94E34" stroke-width="9" stroke-linecap="round"/>

  <!-- branch stems and annotation rules -->
  <line x1="180" y1="360" x2="180" y2="242" stroke="#2A4B7C" stroke-width="3" stroke-linecap="round"/>
  <line x1="112" y1="242" x2="248" y2="242" stroke="#2A4B7C" stroke-width="2"/>
  <circle cx="180" cy="242" r="6" fill="#2A4B7C"/>

  <line x1="410" y1="360" x2="410" y2="478" stroke="#3DB2D3" stroke-width="3" stroke-linecap="round"/>
  <line x1="342" y1="478" x2="478" y2="478" stroke="#3DB2D3" stroke-width="2"/>
  <circle cx="410" cy="478" r="6" fill="#3DB2D3"/>

  <line x1="640" y1="360" x2="640" y2="242" stroke="#F29C38" stroke-width="3" stroke-linecap="round"/>
  <line x1="572" y1="242" x2="708" y2="242" stroke="#F29C38" stroke-width="2"/>
  <circle cx="640" cy="242" r="6" fill="#F29C38"/>

  <line x1="870" y1="360" x2="870" y2="478" stroke="#D94E34" stroke-width="3" stroke-linecap="round"/>
  <line x1="802" y1="478" x2="938" y2="478" stroke="#D94E34" stroke-width="2"/>
  <circle cx="870" cy="478" r="6" fill="#D94E34"/>

  <line x1="1100" y1="360" x2="1100" y2="242" stroke="#8BA84B" stroke-width="3" stroke-linecap="round"/>
  <line x1="1032" y1="242" x2="1168" y2="242" stroke="#8BA84B" stroke-width="2"/>
  <circle cx="1100" cy="242" r="6" fill="#8BA84B"/>

  <!-- open circular arcs: top milestones have top gaps; lower milestones have bottom gaps -->
  <path d="M198.5 309.2 A54 54 0 1 1 161.5 309.2" fill="none" stroke="#2A4B7C" stroke-width="9" stroke-linecap="round" filter="url(#softGlow)"/>
  <path d="M391.5 410.8 A54 54 0 1 1 428.5 410.8" fill="none" stroke="#3DB2D3" stroke-width="9" stroke-linecap="round" filter="url(#softGlow)"/>
  <path d="M658.5 309.2 A54 54 0 1 1 621.5 309.2" fill="none" stroke="#F29C38" stroke-width="9" stroke-linecap="round" filter="url(#softGlow)"/>
  <path d="M851.5 410.8 A54 54 0 1 1 888.5 410.8" fill="none" stroke="#D94E34" stroke-width="9" stroke-linecap="round" filter="url(#softGlow)"/>
  <path d="M1118.5 309.2 A54 54 0 1 1 1081.5 309.2" fill="none" stroke="#8BA84B" stroke-width="9" stroke-linecap="round" filter="url(#softGlow)"/>

  <!-- inner cores cover connector seams and hide the branch line through the center -->
  <circle cx="180" cy="360" r="38" fill="#2A4B7C" filter="url(#coreShadow)"/>
  <circle cx="410" cy="360" r="38" fill="#3DB2D3" filter="url(#coreShadow)"/>
  <circle cx="640" cy="360" r="38" fill="#F29C38" filter="url(#coreShadow)"/>
  <circle cx="870" cy="360" r="38" fill="#D94E34" filter="url(#coreShadow)"/>
  <circle cx="1100" cy="360" r="38" fill="#8BA84B" filter="url(#coreShadow)"/>

  <circle cx="166" cy="345" r="8" fill="#FFFFFF" opacity="0.22"/>
  <circle cx="396" cy="345" r="8" fill="#FFFFFF" opacity="0.22"/>
  <circle cx="626" cy="345" r="8" fill="#FFFFFF" opacity="0.22"/>
  <circle cx="856" cy="345" r="8" fill="#FFFFFF" opacity="0.22"/>
  <circle cx="1086" cy="345" r="8" fill="#FFFFFF" opacity="0.22"/>

  <text x="180" y="371" width="76" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="700" fill="#FFFFFF">01</text>
  <text x="410" y="371" width="76" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="700" fill="#FFFFFF">02</text>
  <text x="640" y="371" width="76" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="700" fill="#FFFFFF">03</text>
  <text x="870" y="371" width="76" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="700" fill="#FFFFFF">04</text>
  <text x="1100" y="371" width="76" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="700" fill="#FFFFFF">05</text>

  <text x="105" y="150" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="33" font-weight="700" fill="#606A74">2024</text>
  <text x="105" y="180" width="185" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#2A4B7C">Market Foundation</text>
  <text x="105" y="207" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6E7781">Define the launch thesis, validate buyer segments, and align operating teams.</text>

  <text x="335" y="530" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="33" font-weight="700" fill="#606A74">2025</text>
  <text x="335" y="560" width="185" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#3DB2D3">Scaled Platform</text>
  <text x="335" y="587" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6E7781">Expand the product core, harden data workflows, and move pilots into repeatable motion.</text>

  <text x="565" y="150" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="33" font-weight="700" fill="#606A74">2026</text>
  <text x="565" y="180" width="185" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#F29C38">Regional Growth</text>
  <text x="565" y="207" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6E7781">Open priority markets through channel partners and localized commercial playbooks.</text>

  <text x="795" y="530" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="33" font-weight="700" fill="#606A74">2027</text>
  <text x="795" y="560" width="185" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#D94E34">Portfolio Integration</text>
  <text x="795" y="587" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6E7781">Unify adjacent offerings, reduce duplicated effort, and consolidate customer insight loops.</text>

  <text x="1025" y="150" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="33" font-weight="700" fill="#606A74">2028</text>
  <text x="1025" y="180" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#8BA84B">Category Leadership</text>
  <text x="1025" y="207" width="195" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6E7781">Convert operating scale into brand authority, margin lift, and durable ecosystem advantage.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<circle stroke-dasharray>` as the primary arc method if the gap must align precisely with the branch; explicit `<path>` arcs are easier to control.
- ❌ Do not place connector lines above the nodes; the interlocking illusion depends on the arcs and inner cores capping the horizontal track.
- ❌ Do not apply `<filter>` to `<line>` elements; use shadows/glows on circles or arc paths instead.
- ❌ Do not use `marker-end` arrows on the timeline; arrowheads on paths may disappear, and this technique reads better as a continuous roadmap.
- ❌ Do not use `clip-path` or masks on non-image shapes to fake ring gaps; use real open arc paths.

## Composition notes
- Keep the timeline track centered around the vertical midpoint, with roughly 80–86% of slide width used for the five nodes.
- Alternate text blocks above and below the track to preserve whitespace and make dense milestone copy readable.
- Use saturated node colors against a pale background; repeat each node color on its arc, stem, terminal dot, and subtitle.
- Draw order matters: background → connectors → stems/rules/dots → outer arcs → inner cores → milestone numbers/text.