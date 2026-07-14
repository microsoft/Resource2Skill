# SVG Recipe — Segmented Ring Comparison

## Visual mechanism
A central topic sits inside a neutral circle, surrounded by a thick ring split into two opposing color-coded halves. Each half owns a radial set of bullet nodes that connect outward to concise comparison points, creating a balanced pros/cons or for/against infographic.

## SVG primitives needed
- 1× `<rect>` for the full-slide background with subtle gradient
- 2× `<path>` for the left and right annular ring segments
- 1× `<circle>` for the central topic disk
- 20× `<circle>` for hollow bullet nodes on the ring, using outer white disks plus smaller colored centers
- 10× `<line>` for connector rules from bullet nodes to text labels
- 10× `<circle>` for small endpoint dots near label text
- 13× `<text>` blocks for title, side headers, center topic, and comparison labels
- 3× `<linearGradient>` for premium background and segmented ring fills
- 1× `<filter id="softShadow">` applied to ring paths and central circle
- 1× `<filter id="textGlow">` applied to the main title for subtle keynote polish
- 2× decorative `<path>` strokes for faint background arcs that reinforce the circular theme

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#fbfbf7"/>
      <stop offset="55%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#f1f3ef"/>
    </linearGradient>
    <linearGradient id="greenGrad" x1="490" y1="240" x2="640" y2="540">
      <stop offset="0%" stop-color="#6f823e"/>
      <stop offset="100%" stop-color="#344628"/>
    </linearGradient>
    <linearGradient id="orangeGrad" x1="640" y1="240" x2="790" y2="540">
      <stop offset="0%" stop-color="#e37a2d"/>
      <stop offset="100%" stop-color="#a74718"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="textGlow" x="-10%" y="-50%" width="120%" height="200%">
      <feGaussianBlur stdDeviation="1.2" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <path d="M155 115 C310 40 430 65 505 150" fill="none" stroke="#d9ddd2" stroke-width="2" stroke-dasharray="8 12" opacity="0.7"/>
  <path d="M775 615 C920 690 1115 650 1195 520" fill="none" stroke="#e6d5c6" stroke-width="2" stroke-dasharray="8 12" opacity="0.75"/>

  <text x="0" y="58" width="1280" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="36" font-weight="700" fill="#171717" filter="url(#textGlow)">
    Two Sides of a Strategic Decision
  </text>
  <text x="0" y="92" width="1280" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#6a6a6a">
    Use the split ring to show an issue as one complete topic with two clearly opposed perspectives
  </text>

  <line x1="567" y1="286" x2="353" y2="172" stroke="#bebebe" stroke-width="2"/>
  <line x1="525" y1="336" x2="310" y2="272" stroke="#bebebe" stroke-width="2"/>
  <line x1="513" y1="390" x2="290" y2="390" stroke="#bebebe" stroke-width="2"/>
  <line x1="525" y1="444" x2="310" y2="508" stroke="#bebebe" stroke-width="2"/>
  <line x1="567" y1="494" x2="353" y2="608" stroke="#bebebe" stroke-width="2"/>

  <line x1="713" y1="286" x2="927" y2="172" stroke="#bebebe" stroke-width="2"/>
  <line x1="755" y1="336" x2="970" y2="272" stroke="#bebebe" stroke-width="2"/>
  <line x1="767" y1="390" x2="990" y2="390" stroke="#bebebe" stroke-width="2"/>
  <line x1="755" y1="444" x2="970" y2="508" stroke="#bebebe" stroke-width="2"/>
  <line x1="713" y1="494" x2="927" y2="608" stroke="#bebebe" stroke-width="2"/>

  <circle cx="353" cy="172" r="4" fill="#435529"/>
  <circle cx="310" cy="272" r="4" fill="#435529"/>
  <circle cx="290" cy="390" r="4" fill="#435529"/>
  <circle cx="310" cy="508" r="4" fill="#435529"/>
  <circle cx="353" cy="608" r="4" fill="#435529"/>
  <circle cx="927" cy="172" r="4" fill="#c8591b"/>
  <circle cx="970" cy="272" r="4" fill="#c8591b"/>
  <circle cx="990" cy="390" r="4" fill="#c8591b"/>
  <circle cx="970" cy="508" r="4" fill="#c8591b"/>
  <circle cx="927" cy="608" r="4" fill="#c8591b"/>

  <path d="M640 240 A150 150 0 0 0 640 540 L640 494 A104 104 0 0 1 640 286 Z" fill="url(#greenGrad)" filter="url(#softShadow)"/>
  <path d="M640 240 A150 150 0 0 1 640 540 L640 494 A104 104 0 0 0 640 286 Z" fill="url(#orangeGrad)" filter="url(#softShadow)"/>
  <rect x="636" y="238" width="8" height="304" rx="4" fill="#ffffff" opacity="0.95"/>

  <circle cx="640" cy="390" r="108" fill="#e7e7e2" filter="url(#softShadow)"/>
  <circle cx="640" cy="390" r="93" fill="#f3f3ef"/>
  <text x="560" y="355" width="160" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#252525">
    CENTRAL ISSUE
  </text>
  <text x="555" y="388" width="170" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#555555">
    <tspan x="640" dy="0">Should we enter</tspan>
    <tspan x="640" dy="22">the new market</tspan>
    <tspan x="640" dy="22">this year?</tspan>
  </text>

  <circle cx="567" cy="286" r="16" fill="#ffffff"/>
  <circle cx="567" cy="286" r="7" fill="#435529"/>
  <circle cx="525" cy="336" r="16" fill="#ffffff"/>
  <circle cx="525" cy="336" r="7" fill="#435529"/>
  <circle cx="513" cy="390" r="16" fill="#ffffff"/>
  <circle cx="513" cy="390" r="7" fill="#435529"/>
  <circle cx="525" cy="444" r="16" fill="#ffffff"/>
  <circle cx="525" cy="444" r="7" fill="#435529"/>
  <circle cx="567" cy="494" r="16" fill="#ffffff"/>
  <circle cx="567" cy="494" r="7" fill="#435529"/>

  <circle cx="713" cy="286" r="16" fill="#ffffff"/>
  <circle cx="713" cy="286" r="7" fill="#c8591b"/>
  <circle cx="755" cy="336" r="16" fill="#ffffff"/>
  <circle cx="755" cy="336" r="7" fill="#c8591b"/>
  <circle cx="767" cy="390" r="16" fill="#ffffff"/>
  <circle cx="767" cy="390" r="7" fill="#c8591b"/>
  <circle cx="755" cy="444" r="16" fill="#ffffff"/>
  <circle cx="755" cy="444" r="7" fill="#c8591b"/>
  <circle cx="713" cy="494" r="16" fill="#ffffff"/>
  <circle cx="713" cy="494" r="7" fill="#c8591b"/>

  <text x="96" y="146" width="250" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#435529">FOR / UPSIDE</text>
  <text x="96" y="178" width="250" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" fill="#222222">Early mover advantage</text>
  <text x="78" y="278" width="225" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" fill="#222222">Access to premium buyers</text>
  <text x="66" y="396" width="215" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" fill="#222222">Diversifies revenue mix</text>
  <text x="78" y="514" width="225" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" fill="#222222">Strengthens brand reach</text>
  <text x="96" y="614" width="250" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" fill="#222222">Creates learning curve lead</text>

  <text x="934" y="146" width="250" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#c8591b">AGAINST / RISK</text>
  <text x="934" y="178" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" fill="#222222">Higher launch investment</text>
  <text x="980" y="278" width="230" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" fill="#222222">Regulatory uncertainty</text>
  <text x="1000" y="396" width="230" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" fill="#222222">Operational complexity</text>
  <text x="980" y="514" width="230" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" fill="#222222">Possible margin pressure</text>
  <text x="934" y="614" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" fill="#222222">Distracts from core market</text>
</svg>
```

## Avoid in this skill
- ❌ Building the split ring with `<mask>` or `mask="url(#...)"`; use two editable annular `<path>` shapes instead.
- ❌ Using `<use>` to duplicate bullet nodes; repeat the circles directly so PowerPoint receives editable shapes.
- ❌ Applying filters to connector `<line>` elements; shadows on lines are dropped, so keep connectors flat and clean.
- ❌ Using `marker-end` arrowheads for connector lines; this comparison style works better with simple endpoint dots.
- ❌ Letting text auto-size implicitly; every `<text>` needs an explicit `width` to render predictably in PowerPoint.

## Composition notes
- Keep the segmented ring centered, slightly below the title, occupying roughly the middle third of the slide width.
- Place left-side arguments in the left margin and right-side arguments in the right margin; use connector lines to preserve association without crowding the ring.
- Use a warm/cool or green/orange color pair with the neutral center disk to make the dichotomy immediate.
- Leave generous white space around the text labels; the circular graphic should feel like the organizing anchor, not a dense chart.