# SVG Recipe — Minimalist Process Funnel

## Visual mechanism
A clean, downward-narrowing funnel is built from stacked custom trapezoid paths whose edges align perfectly, suggesting progressive filtering. Each stage connects to a right-side explanation block with thin connector lines, creating a polished Napkin-style process diagram.

## SVG primitives needed
- 1× `<rect>` for the warm off-white slide background
- 1× `<path>` for the full-funnel shadow silhouette behind the stacked stages
- 5× `<path>` for seamless pastel trapezoid funnel segments
- 5× `<text>` inside the funnel for compact stage labels
- 5× `<line>` for minimalist horizontal connector rules
- 5× `<circle>` for small connector anchor dots
- 10× `<text>` for right-side stage titles and descriptions
- 1× `<rect>` for the final outcome pill
- 1× `<path>` for a small checkmark icon inside the outcome pill
- 5× `<linearGradient>` for subtle premium pastel fills
- 1× `<filter id="softShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` applied to the funnel shadow and outcome pill

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FCFBF7"/>
      <stop offset="100%" stop-color="#F5F7FA"/>
    </linearGradient>

    <linearGradient id="stage1" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFE0C7"/>
      <stop offset="100%" stop-color="#FFCFA8"/>
    </linearGradient>
    <linearGradient id="stage2" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ECEAFF"/>
      <stop offset="100%" stop-color="#DCD8FF"/>
    </linearGradient>
    <linearGradient id="stage3" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#C9F8D7"/>
      <stop offset="100%" stop-color="#A9EFC2"/>
    </linearGradient>
    <linearGradient id="stage4" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#BDEEFF"/>
      <stop offset="100%" stop-color="#96D9F4"/>
    </linearGradient>
    <linearGradient id="stage5" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FAD7E8"/>
      <stop offset="100%" stop-color="#F3BBD6"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feColorMatrix in="blur" type="matrix"
        values="0 0 0 0 0.25  0 0 0 0 0.29  0 0 0 0 0.34  0 0 0 .18 0" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>

  <text x="88" y="74" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="700" fill="#24272D">
    Strategic Pipeline Funnel
  </text>
  <text x="90" y="109" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#6B7280">
    A minimalist five-stage view of how broad inputs narrow into focused outcomes.
  </text>

  <path d="M155 168 L625 168 L470 578 L320 578 Z" fill="#D8DEE8" opacity="0.38" filter="url(#softShadow)"/>

  <path d="M155 168 L625 168 L598 250 L192 250 Z" fill="url(#stage1)"/>
  <path d="M192 250 L598 250 L566 332 L224 332 Z" fill="url(#stage2)"/>
  <path d="M224 332 L566 332 L534 414 L256 414 Z" fill="url(#stage3)"/>
  <path d="M256 414 L534 414 L502 496 L288 496 Z" fill="url(#stage4)"/>
  <path d="M288 496 L502 496 L470 578 L320 578 Z" fill="url(#stage5)"/>

  <line x1="168" y1="250" x2="598" y2="250" stroke="#FFFFFF" stroke-width="2" opacity="0.78"/>
  <line x1="198" y1="332" x2="566" y2="332" stroke="#FFFFFF" stroke-width="2" opacity="0.78"/>
  <line x1="231" y1="414" x2="534" y2="414" stroke="#FFFFFF" stroke-width="2" opacity="0.78"/>
  <line x1="262" y1="496" x2="502" y2="496" stroke="#FFFFFF" stroke-width="2" opacity="0.78"/>

  <text x="270" y="216" width="240" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#33363D">01  Source</text>
  <text x="280" y="298" width="220" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#33363D">02  Qualify</text>
  <text x="290" y="380" width="200" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#33363D">03  Evaluate</text>
  <text x="300" y="462" width="180" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#33363D">04  Select</text>
  <text x="310" y="544" width="160" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#33363D">05  Commit</text>

  <line x1="612" y1="209" x2="718" y2="209" stroke="#B8C0CC" stroke-width="1.4"/>
  <line x1="582" y1="291" x2="718" y2="291" stroke="#B8C0CC" stroke-width="1.4"/>
  <line x1="550" y1="373" x2="718" y2="373" stroke="#B8C0CC" stroke-width="1.4"/>
  <line x1="518" y1="455" x2="718" y2="455" stroke="#B8C0CC" stroke-width="1.4"/>
  <line x1="486" y1="537" x2="718" y2="537" stroke="#B8C0CC" stroke-width="1.4"/>

  <circle cx="612" cy="209" r="4.5" fill="#FFFFFF" stroke="#B8C0CC" stroke-width="1.5"/>
  <circle cx="582" cy="291" r="4.5" fill="#FFFFFF" stroke="#B8C0CC" stroke-width="1.5"/>
  <circle cx="550" cy="373" r="4.5" fill="#FFFFFF" stroke="#B8C0CC" stroke-width="1.5"/>
  <circle cx="518" cy="455" r="4.5" fill="#FFFFFF" stroke="#B8C0CC" stroke-width="1.5"/>
  <circle cx="486" cy="537" r="4.5" fill="#FFFFFF" stroke="#B8C0CC" stroke-width="1.5"/>

  <text x="742" y="201" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" fill="#2B2F36">Broad Sourcing</text>
  <text x="742" y="228" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#687180">
    <tspan x="742" dy="0">Capture all potential opportunities, candidates,</tspan>
    <tspan x="742" dy="20">or initiatives across available channels.</tspan>
  </text>

  <text x="742" y="283" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" fill="#2B2F36">Initial Qualification</text>
  <text x="742" y="310" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#687180">
    <tspan x="742" dy="0">Apply baseline criteria and remove low-fit items</tspan>
    <tspan x="742" dy="20">before deeper review begins.</tspan>
  </text>

  <text x="742" y="365" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" fill="#2B2F36">Deep Evaluation</text>
  <text x="742" y="392" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#687180">
    <tspan x="742" dy="0">Score, compare, and validate each option using</tspan>
    <tspan x="742" dy="20">structured evidence and expert review.</tspan>
  </text>

  <text x="742" y="447" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" fill="#2B2F36">Final Selection</text>
  <text x="742" y="474" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#687180">
    <tspan x="742" dy="0">Align stakeholders around the strongest choices</tspan>
    <tspan x="742" dy="20">and prepare them for conversion.</tspan>
  </text>

  <text x="742" y="529" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" fill="#2B2F36">Decision &amp; Commitment</text>
  <text x="742" y="556" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#687180">
    <tspan x="742" dy="0">Convert the refined shortlist into an approved,</tspan>
    <tspan x="742" dy="20">actionable outcome.</tspan>
  </text>

  <rect x="319" y="608" width="152" height="42" rx="21" fill="#FFFFFF" filter="url(#softShadow)"/>
  <path d="M355 629 L375 643 L435 616" fill="none" stroke="#23A66D" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="490" y="636" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#3A3F47">Refined output ready for execution</text>
</svg>
```

## Avoid in this skill
- ❌ Using plain `<rect>` blocks for funnel stages; the funnel needs custom trapezoid `<path>` geometry so the side edges align continuously.
- ❌ Adding heavy outlines around every stage; use clean fills and only subtle white separators if needed.
- ❌ Using `marker-end` arrowheads on connector paths; if arrows are needed, draw them manually or use simple `<line>` connectors.
- ❌ Applying filters to connector `<line>` elements; shadows on lines are dropped by the translator.
- ❌ Overcrowding the funnel interior with long text; keep labels short and place details in right-side text blocks.

## Composition notes
- Keep the funnel on the left-center third, occupying roughly 35–40% of slide width, with the explanatory text column on the right.
- Align each connector to the vertical midpoint of its funnel segment for a precise, engineered look.
- Use pastel stages in a restrained sequence; the color rhythm should guide the eye downward without feeling like a rainbow.
- Preserve generous negative space around the title and right text blocks so the diagram feels executive and editorial.