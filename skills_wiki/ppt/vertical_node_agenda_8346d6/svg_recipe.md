# SVG Recipe — Vertical Node Agenda

## Visual mechanism
A bold split-layout agenda: a dark title slab anchors the left third while a vertical “rail” on the right connects numbered circular nodes to staggered agenda cards. The visual hierarchy comes from high-contrast typography, glowing accent nodes, and generous negative space around the agenda path.

## SVG primitives needed
- 2× <rect> for full-slide background and the left title panel
- 1× <rect> for the vertical agenda connector rail
- 4× <rect> for agenda item cards
- 4× <circle> glow halos behind the nodes
- 8× <circle> for numbered node outer/inner disks
- 4× <path> for short curved connector strokes from nodes to cards
- 2× <path> for decorative abstract background shapes and the angled panel edge
- 15× <text> blocks for section label, main title, node numbers, item labels, headings, body copy, and footer note
- 3× <linearGradient> for background, dark panel, and accent rail/node fills
- 1× <radialGradient> for node glow
- 2× <filter> definitions for card shadows and soft decorative glow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0" stop-color="#F7F1E8"/>
      <stop offset="0.58" stop-color="#FBF8F2"/>
      <stop offset="1" stop-color="#EEF4F8"/>
    </linearGradient>
    <linearGradient id="navyPanel" x1="0" y1="0" x2="470" y2="720">
      <stop offset="0" stop-color="#102A46"/>
      <stop offset="0.55" stop-color="#071A2E"/>
      <stop offset="1" stop-color="#031120"/>
    </linearGradient>
    <linearGradient id="accentGrad" x1="0" y1="150" x2="0" y2="590">
      <stop offset="0" stop-color="#FFCF69"/>
      <stop offset="0.48" stop-color="#F59E2E"/>
      <stop offset="1" stop-color="#E66B2D"/>
    </linearGradient>
    <radialGradient id="nodeGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#FFD978" stop-opacity="0.75"/>
      <stop offset="0.55" stop-color="#F4A12C" stop-opacity="0.28"/>
      <stop offset="1" stop-color="#F4A12C" stop-opacity="0"/>
    </radialGradient>
    <filter id="cardShadow" x="-20%" y="-30%" width="150%" height="170%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>
  <path d="M920,64 C1080,18 1225,74 1280,176 L1280,0 L855,0 C874,30 895,50 920,64 Z" fill="#DDECF3" opacity="0.72"/>
  <path d="M1040,600 C1130,548 1215,578 1280,640 L1280,720 L960,720 C970,670 996,626 1040,600 Z" fill="#F8DDAE" opacity="0.46" filter="url(#softGlow)"/>

  <rect x="0" y="0" width="472" height="720" fill="url(#navyPanel)"/>
  <path d="M382,0 C450,120 434,246 497,360 C440,472 458,604 392,720 L472,720 L472,0 Z" fill="#0D2741" opacity="0.96"/>
  <circle cx="94" cy="86" r="118" fill="#1D4D73" opacity="0.24"/>
  <circle cx="392" cy="608" r="158" fill="#F59E2E" opacity="0.12" filter="url(#softGlow)"/>
  <path d="M58,548 C96,500 154,514 181,456 C210,393 283,404 310,459 C340,519 297,587 229,600 C156,615 102,602 58,548 Z" fill="#FFFFFF" opacity="0.045"/>

  <text x="68" y="92" width="270" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" letter-spacing="3" fill="#F5B640">EXECUTIVE WORKSHOP</text>
  <text x="66" y="206" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="62" font-weight="800" fill="#FFFFFF">
    <tspan x="66" dy="0">Q4</tspan>
    <tspan x="66" dy="72">LAUNCH</tspan>
    <tspan x="66" dy="72">AGENDA</tspan>
  </text>
  <text x="70" y="454" width="315" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" fill="#B8C8D8">Four connected decisions to align market entry, operating model, and leadership commitments.</text>
  <text x="72" y="642" width="300" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600" letter-spacing="2" fill="#7FA0BC">STRATEGY SESSION · 90 MIN</text>
  <text x="82" y="680" width="460" transform="rotate(-90 82 680)" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="84" font-weight="800" fill="#FFFFFF" opacity="0.035">AGENDA</text>

  <text x="570" y="82" width="540" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="34" font-weight="800" fill="#102A46">Connected decision path</text>
  <text x="572" y="116" width="520" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#667789">Follow the numbered nodes from context to commitment.</text>

  <rect x="602" y="160" width="7" height="420" rx="3.5" fill="url(#accentGrad)" opacity="0.92"/>
  <rect x="590" y="158" width="31" height="424" rx="15.5" fill="#FFFFFF" opacity="0.32"/>

  <path d="M638,180 C654,180 660,180 674,180" fill="none" stroke="#F3A536" stroke-width="4" stroke-linecap="round"/>
  <circle cx="606" cy="180" r="49" fill="url(#nodeGlow)" filter="url(#softGlow)"/>
  <circle cx="606" cy="180" r="32" fill="url(#accentGrad)"/>
  <circle cx="606" cy="180" r="23" fill="#FFFFFF"/>
  <text x="581" y="188" width="50" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="800" fill="#E87B2E">01</text>
  <rect x="674" y="142" width="500" height="78" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="704" y="169" width="80" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="800" letter-spacing="2" fill="#F39A2E">CONTEXT</text>
  <text x="704" y="193" width="430" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="21" font-weight="800" fill="#132A43">Market signal review</text>
  <text x="704" y="213" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#6C7885">Align on customer demand, competitor movement, and launch constraints.</text>

  <path d="M638,300 C660,300 678,300 698,300" fill="none" stroke="#F3A536" stroke-width="4" stroke-linecap="round"/>
  <circle cx="606" cy="300" r="49" fill="url(#nodeGlow)" filter="url(#softGlow)"/>
  <circle cx="606" cy="300" r="32" fill="url(#accentGrad)"/>
  <circle cx="606" cy="300" r="23" fill="#FFFFFF"/>
  <text x="581" y="308" width="50" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="800" fill="#E87B2E">02</text>
  <rect x="698" y="262" width="500" height="78" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="728" y="289" width="80" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="800" letter-spacing="2" fill="#F39A2E">MODEL</text>
  <text x="728" y="313" width="430" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="21" font-weight="800" fill="#132A43">Operating choices</text>
  <text x="728" y="333" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#6C7885">Decide channel mix, launch sequencing, service levels, and ownership.</text>

  <path d="M638,420 C654,420 660,420 674,420" fill="none" stroke="#F3A536" stroke-width="4" stroke-linecap="round"/>
  <circle cx="606" cy="420" r="49" fill="url(#nodeGlow)" filter="url(#softGlow)"/>
  <circle cx="606" cy="420" r="32" fill="url(#accentGrad)"/>
  <circle cx="606" cy="420" r="23" fill="#FFFFFF"/>
  <text x="581" y="428" width="50" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="800" fill="#E87B2E">03</text>
  <rect x="674" y="382" width="500" height="78" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="704" y="409" width="80" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="800" letter-spacing="2" fill="#F39A2E">RISKS</text>
  <text x="704" y="433" width="430" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="21" font-weight="800" fill="#132A43">Critical dependency map</text>
  <text x="704" y="453" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#6C7885">Surface blockers, mitigation owners, decision gates, and timing pressure.</text>

  <path d="M638,540 C660,540 678,540 698,540" fill="none" stroke="#F3A536" stroke-width="4" stroke-linecap="round"/>
  <circle cx="606" cy="540" r="49" fill="url(#nodeGlow)" filter="url(#softGlow)"/>
  <circle cx="606" cy="540" r="32" fill="url(#accentGrad)"/>
  <circle cx="606" cy="540" r="23" fill="#FFFFFF"/>
  <text x="581" y="548" width="50" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="800" fill="#E87B2E">04</text>
  <rect x="698" y="502" width="500" height="78" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="728" y="529" width="110" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="800" letter-spacing="2" fill="#F39A2E">COMMIT</text>
  <text x="728" y="553" width="430" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="21" font-weight="800" fill="#132A43">Actions and accountability</text>
  <text x="728" y="573" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#6C7885">Lock owners, next milestones, escalation paths, and success measures.</text>
</svg>
```

## Avoid in this skill
- ❌ Using `marker-end` arrowheads on agenda connectors; they may disappear. Use short stroked paths or editable lines without markers.
- ❌ Applying a blur/shadow filter to `<line>` elements for the vertical rail; use a skinny rounded `<rect>` instead.
- ❌ Creating node repetition with `<use href="#node">`; duplicate the editable circles and text directly.
- ❌ Omitting `width` on agenda text boxes; PowerPoint will not size text predictably.
- ❌ Overfilling the slide with long agenda copy; this layout works best with four to five compact nodes.

## Composition notes
- Keep the left panel around 35–38% of the slide width; it should feel like a strong editorial title block, not a sidebar.
- Place the vertical rail just right of center, leaving enough room for 480–540 px wide agenda cards.
- Stagger cards subtly left/right by 20–30 px to create motion while preserving a clean vertical reading path.
- Use one warm accent color for rail, nodes, and labels; reserve dark navy and white for structure and legibility.