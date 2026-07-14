# SVG Recipe — Engineering Drafting & Orthographic Development

## Visual mechanism
Create a technical drawing slide that combines orthographic front/top projections with a radial surface development diagram, using strict line-weight hierarchy, faint construction geometry, and precise vertex labels. The style should feel like a clean executive “blueprint on drafting paper”: analytical, geometric, and deliberately sparse.

## SVG primitives needed
- 1× `<rect>` for the matte drafting-paper background
- 1× `<rect>` for a subtle problem-statement panel
- 35+× `<line>` for XY reference lines, projection guides, axes, pyramid edges, fold lines, and construction rays
- 12+× `<path>` for square outlines, pyramid outlines, radial development panels, base arcs, and highlighted truncation/cut edges
- 1× `<linearGradient>` for a very subtle paper-tone background
- 1× `<filter id="softShadow">` applied to the problem-statement panel
- 40+× `<text>` for title, problem statement, view captions, and engineering point labels

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="paper" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#fbfbf8"/>
      <stop offset="55%" stop-color="#f3f1ea"/>
      <stop offset="100%" stop-color="#ebe7dc"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="3"/>
      <feGaussianBlur stdDeviation="5"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#paper)"/>
  <rect x="42" y="28" width="1196" height="92" rx="18" fill="#ffffff" opacity="0.72" filter="url(#softShadow)"/>

  <text x="64" y="58" width="1120" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="600" fill="#202020">
    Engineering Drafting: Orthographic Projection + Lateral Surface Development
  </text>
  <text x="64" y="90" width="1140" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#444444">
    A square pyramid is cut by an inclined plane. Construct the front view, top view, and true development of the truncated lateral surfaces.
  </text>

  <text x="88" y="158" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#333333">ORTHOGRAPHIC VIEWS</text>
  <text x="520" y="158" width="450" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#333333">RADIAL DEVELOPMENT OF LATERAL SURFACES</text>

  <!-- left-side drafting reference and projection frame -->
  <line x1="70" y1="438" x2="455" y2="438" stroke="#222222" stroke-width="2"/>
  <text x="54" y="432" width="24" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-style="italic" fill="#555555">X</text>
  <text x="462" y="432" width="24" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-style="italic" fill="#555555">Y</text>

  <line x1="280" y1="210" x2="280" y2="438" stroke="#aeb2b4" stroke-width="1.2" stroke-dasharray="8 7"/>
  <line x1="118" y1="438" x2="150" y2="495" stroke="#b8b8b8" stroke-width="1"/>
  <line x1="442" y1="438" x2="360" y2="495" stroke="#b8b8b8" stroke-width="1"/>
  <line x1="150" y1="495" x2="150" y2="684" stroke="#b8b8b8" stroke-width="1"/>
  <line x1="360" y1="495" x2="360" y2="684" stroke="#b8b8b8" stroke-width="1"/>

  <!-- front elevation -->
  <path d="M118 438 L280 210 L442 438 Z" fill="none" stroke="#242424" stroke-width="3" stroke-linejoin="round"/>
  <line x1="118" y1="438" x2="280" y2="438" stroke="#242424" stroke-width="2"/>
  <line x1="280" y1="438" x2="442" y2="438" stroke="#242424" stroke-width="2"/>
  <line x1="198" y1="438" x2="280" y2="210" stroke="#777777" stroke-width="1.3"/>
  <line x1="362" y1="438" x2="280" y2="210" stroke="#777777" stroke-width="1.3"/>
  <path d="M165 390 L235 350 L317 332 L398 305" fill="none" stroke="#00a8e8" stroke-width="3.2" stroke-linecap="round"/>
  <line x1="235" y1="350" x2="235" y2="438" stroke="#b8b8b8" stroke-width="1" stroke-dasharray="5 6"/>
  <line x1="317" y1="332" x2="317" y2="438" stroke="#b8b8b8" stroke-width="1" stroke-dasharray="5 6"/>
  <line x1="398" y1="305" x2="398" y2="438" stroke="#b8b8b8" stroke-width="1" stroke-dasharray="5 6"/>

  <text x="271" y="202" width="36" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-style="italic" fill="#555555">o′</text>
  <text x="105" y="431" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-style="italic" fill="#555555">a′</text>
  <text x="430" y="431" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-style="italic" fill="#555555">b′</text>
  <text x="226" y="344" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-style="italic" fill="#0078b8">p′</text>
  <text x="309" y="327" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-style="italic" fill="#0078b8">q′</text>
  <text x="394" y="298" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-style="italic" fill="#0078b8">s′</text>

  <!-- top view square -->
  <path d="M150 495 L360 495 L360 684 L150 684 Z" fill="none" stroke="#242424" stroke-width="2.5"/>
  <line x1="150" y1="495" x2="360" y2="684" stroke="#7a7a7a" stroke-width="1.2"/>
  <line x1="150" y1="684" x2="360" y2="495" stroke="#7a7a7a" stroke-width="1.2"/>
  <circle cx="255" cy="589.5" r="3.8" fill="#242424"/>
  <path d="M178 525 C216 564, 246 598, 303 654" fill="none" stroke="#00a8e8" stroke-width="2.4" stroke-linecap="round"/>
  <text x="143" y="490" width="26" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-style="italic" fill="#555555">d</text>
  <text x="362" y="490" width="26" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-style="italic" fill="#555555">c</text>
  <text x="143" y="707" width="26" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-style="italic" fill="#555555">a</text>
  <text x="362" y="707" width="26" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-style="italic" fill="#555555">b</text>
  <text x="264" y="596" width="24" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-style="italic" fill="#555555">o</text>
  <text x="190" y="528" width="26" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-style="italic" fill="#0078b8">p</text>

  <!-- development construction arcs -->
  <path d="M505 528 C625 640, 800 625, 922 520 C1002 450, 1010 275, 955 88" fill="none" stroke="#b9b9b9" stroke-width="1.2"/>
  <path d="M555 405 C665 468, 798 455, 888 360 C936 309, 935 218, 790 175" fill="none" stroke="#c9c9c9" stroke-width="1" stroke-dasharray="7 7"/>
  <path d="M500 528 C560 515, 642 496, 700 458" fill="none" stroke="#c9c9c9" stroke-width="1" stroke-dasharray="6 8"/>
  <path d="M700 604 C773 597, 844 568, 922 520" fill="none" stroke="#c9c9c9" stroke-width="1" stroke-dasharray="6 8"/>
  <path d="M922 520 C978 442, 995 350, 955 88" fill="none" stroke="#c9c9c9" stroke-width="1" stroke-dasharray="6 8"/>

  <!-- radial development main fan -->
  <line x1="650" y1="235" x2="505" y2="528" stroke="#242424" stroke-width="3"/>
  <line x1="650" y1="235" x2="700" y2="604" stroke="#242424" stroke-width="2.5"/>
  <line x1="650" y1="235" x2="922" y2="520" stroke="#242424" stroke-width="2.5"/>
  <line x1="650" y1="235" x2="955" y2="88" stroke="#242424" stroke-width="2.5"/>
  <line x1="650" y1="235" x2="990" y2="360" stroke="#777777" stroke-width="1.4"/>

  <path d="M505 528 L700 604 L922 520 L990 360 L955 88" fill="none" stroke="#242424" stroke-width="3" stroke-linejoin="round"/>
  <path d="M505 528 L650 235 L700 604 Z" fill="#ffffff" opacity="0.10" stroke="#242424" stroke-width="1.1"/>
  <path d="M700 604 L650 235 L922 520 Z" fill="#ffffff" opacity="0.08" stroke="#242424" stroke-width="1.1"/>
  <path d="M922 520 L650 235 L990 360 Z" fill="#ffffff" opacity="0.08" stroke="#242424" stroke-width="1.1"/>
  <path d="M990 360 L650 235 L955 88 Z" fill="#ffffff" opacity="0.08" stroke="#242424" stroke-width="1.1"/>

  <!-- highlighted cut profile across development -->
  <path d="M555 405 L655 356 L742 330 L835 305 L790 175" fill="none" stroke="#00a8e8" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <line x1="655" y1="356" x2="700" y2="604" stroke="#777777" stroke-width="1.2"/>
  <line x1="742" y1="330" x2="922" y2="520" stroke="#777777" stroke-width="1.2"/>
  <line x1="835" y1="305" x2="990" y2="360" stroke="#777777" stroke-width="1.2"/>
  <line x1="790" y1="175" x2="955" y2="88" stroke="#777777" stroke-width="1.2"/>

  <!-- development labels -->
  <text x="638" y="228" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-style="italic" fill="#333333">O</text>
  <text x="490" y="548" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-style="italic" fill="#333333">A</text>
  <text x="692" y="627" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-style="italic" fill="#333333">B</text>
  <text x="918" y="543" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-style="italic" fill="#333333">C</text>
  <text x="996" y="365" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-style="italic" fill="#333333">D</text>
  <text x="960" y="82" width="36" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-style="italic" fill="#333333">A′</text>
  <text x="538" y="401" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-style="italic" fill="#0078b8">P</text>
  <text x="655" y="350" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-style="italic" fill="#0078b8">Q</text>
  <text x="742" y="322" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-style="italic" fill="#0078b8">R</text>
  <text x="842" y="300" width="32" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-style="italic" fill="#0078b8">S</text>
  <text x="790" y="166" width="36" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-style="italic" fill="#0078b8">P′</text>

  <text x="520" y="675" width="660" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#666666">
    Thin gray lines show construction geometry; dark strokes define true edges; cyan strokes identify the cutting plane and transferred truncation profile.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using `<marker-end>` arrowheads for projection arrows; if arrows are required, draw them manually with short `<line>` segments.
- ❌ Applying blur or shadow filters to `<line>` elements; filters on lines may be dropped.
- ❌ Using `<pattern>` fills for graph paper; use faint individual lines or a subtle gradient instead.
- ❌ Clipping or masking non-image elements; drafting geometry should remain editable paths and lines.
- ❌ Over-filling the panels with solid colors; the technique depends on precise line hierarchy and negative space.

## Composition notes
- Reserve the top 15–20% for the problem statement; keep it quiet so the geometry remains the hero.
- Place orthographic views on the left, anchored to a strong horizontal XY reference line; use projection guides to connect elevation and plan.
- Give the radial development on the right more space than the orthographic views; it should feel like the “answer” derived from the construction.
- Use three line classes consistently: dark thick object edges, pale thin construction lines, and one vivid accent color for cut/development transfer lines.