# SVG Recipe — High-Contrast Header & Horizontal Grid Dissection (The "Anti-Word-Doc" Layout)

## Visual mechanism
A dominant high-contrast header block carries the macro message, while the lower 60–65% of the slide is dissected into evenly spaced horizontal columns for parallel details. Thin divider rules, serial tags, and repeated typography turn dense prose into a fast-scannable executive grid.

## SVG primitives needed
- 1× full-slide `<rect>` for the warm off-white background
- 1× large `<rect>` for the high-contrast header container
- 2× `<linearGradient>` for premium header depth and subtle blue accent fills
- 1× `<filter id="headerShadow">` applied to the header block for a soft separation shadow
- 3× decorative `<path>` shapes for angular header accents and a bottom transition wedge
- 1× faint `<path>` or `<rect>` band behind the grid to reinforce the horizontal reading zone
- 4× column groupings made from `<text>` blocks, `<line>` dividers, and small `<rect>` number chips
- 8–12× `<line>` elements for horizontal micro-dividers and optional vertical alignment guides
- Multiple `<text>` elements with explicit `width` attributes for title, intro, column headings, serial tags, and body copy
- Optional 4× small `<circle>` anchor dots to visually lock each column title to its divider

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="headerBlue" x1="0" y1="0" x2="1280" y2="260" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#0B1B35"/>
      <stop offset="0.55" stop-color="#173C88"/>
      <stop offset="1" stop-color="#255FD0"/>
    </linearGradient>
    <linearGradient id="accentBlue" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#63A4FF" stop-opacity="0.55"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>
    <filter id="headerShadow" x="-5%" y="-5%" width="110%" height="125%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Base canvas -->
  <rect x="0" y="0" width="1280" height="720" fill="#F6F8FC"/>

  <!-- High-contrast macro-information header -->
  <rect x="0" y="0" width="1280" height="266" fill="url(#headerBlue)" filter="url(#headerShadow)"/>
  <path d="M850 0 L1280 0 L1280 190 C1165 160 1060 120 972 78 C922 54 884 29 850 0 Z" fill="url(#accentBlue)"/>
  <path d="M0 218 C180 250 368 258 548 238 C690 222 804 198 940 222 C1078 246 1174 282 1280 258 L1280 266 L0 266 Z" fill="#061225" opacity="0.22"/>
  <path d="M76 266 L314 266 L278 290 L76 290 Z" fill="#2E6CE6" opacity="0.95"/>

  <!-- Header text -->
  <text x="76" y="76" width="820" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="42" font-weight="700" fill="#FFFFFF">
    技术部员工技能培训
  </text>
  <text x="78" y="126" width="880" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="600" letter-spacing="2.8" fill="#AFC7FF">
    TRAINING SYSTEM / FOUR CORE METHODS
  </text>
  <text x="76" y="166" width="890" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" fill="#EAF1FF">
    <tspan x="76" dy="0">员工培训是指组织为开展业务及培育人才的需要，采用系统化方式对员工进行有目的、</tspan>
    <tspan x="76" dy="30">有计划的培养和训练。将说明文字收束在顶部，让下方只呈现并列方法与关键判断。</tspan>
  </text>

  <!-- Grid reading zone -->
  <rect x="76" y="332" width="1128" height="1.5" fill="#C8D2E4"/>
  <rect x="76" y="664" width="1128" height="1" fill="#DDE4F0"/>
  <text x="76" y="314" width="380" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" letter-spacing="2.2" fill="#7A879B">
    HORIZONTAL DISSECTION GRID
  </text>

  <!-- Column 01 -->
  <rect x="76" y="356" width="64" height="24" rx="12" fill="#E7EEFF"/>
  <text x="108" y="373" width="64" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" font-weight="700" fill="#173C88">PART 01</text>
  <circle cx="76" cy="424" r="4.5" fill="#173C88"/>
  <text x="76" y="414" width="255" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="28" font-weight="700" fill="#173C88">提取技术法</text>
  <line x1="76" y1="446" x2="331" y2="446" stroke="#173C88" stroke-width="2"/>
  <line x1="76" y1="458" x2="331" y2="458" stroke="#D6DDEA" stroke-width="1"/>
  <text x="76" y="494" width="255" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" fill="#555F6F">
    <tspan x="76" dy="0">通过现代教学技术，如投影仪、</tspan>
    <tspan x="76" dy="26">录像、在线课堂与演示工具，对</tspan>
    <tspan x="76" dy="26">员工进行标准化知识传递。</tspan>
  </text>

  <!-- Column 02 -->
  <rect x="367" y="356" width="64" height="24" rx="12" fill="#E7EEFF"/>
  <text x="399" y="373" width="64" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" font-weight="700" fill="#173C88">PART 02</text>
  <line x1="349" y1="354" x2="349" y2="640" stroke="#E1E7F2" stroke-width="1"/>
  <circle cx="367" cy="424" r="4.5" fill="#173C88"/>
  <text x="367" y="414" width="255" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="28" font-weight="700" fill="#173C88">案例研讨法</text>
  <line x1="367" y1="446" x2="622" y2="446" stroke="#173C88" stroke-width="2"/>
  <line x1="367" y1="458" x2="622" y2="458" stroke="#D6DDEA" stroke-width="1"/>
  <text x="367" y="494" width="255" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" fill="#555F6F">
    <tspan x="367" dy="0">向培训对象提供真实背景材料，</tspan>
    <tspan x="367" dy="26">让其判断问题、寻找方案，并在</tspan>
    <tspan x="367" dy="26">复盘中沉淀可复制经验。</tspan>
  </text>

  <!-- Column 03 -->
  <rect x="658" y="356" width="64" height="24" rx="12" fill="#E7EEFF"/>
  <text x="690" y="373" width="64" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" font-weight="700" fill="#173C88">PART 03</text>
  <line x1="640" y1="354" x2="640" y2="640" stroke="#E1E7F2" stroke-width="1"/>
  <circle cx="658" cy="424" r="4.5" fill="#173C88"/>
  <text x="658" y="414" width="255" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="28" font-weight="700" fill="#173C88">角色扮演法</text>
  <line x1="658" y1="446" x2="913" y2="446" stroke="#173C88" stroke-width="2"/>
  <line x1="658" y1="458" x2="913" y2="458" stroke="#D6DDEA" stroke-width="1"/>
  <text x="658" y="494" width="255" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" fill="#555F6F">
    <tspan x="658" dy="0">培训对象在设定情境中扮演</tspan>
    <tspan x="658" dy="26">特定角色，借助身份视角处理</tspan>
    <tspan x="658" dy="26">沟通、服务或管理问题。</tspan>
  </text>

  <!-- Column 04 -->
  <rect x="949" y="356" width="64" height="24" rx="12" fill="#E7EEFF"/>
  <text x="981" y="373" width="64" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" font-weight="700" fill="#173C88">PART 04</text>
  <line x1="931" y1="354" x2="931" y2="640" stroke="#E1E7F2" stroke-width="1"/>
  <circle cx="949" cy="424" r="4.5" fill="#173C88"/>
  <text x="949" y="414" width="255" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="28" font-weight="700" fill="#173C88">阶梯培训法</text>
  <line x1="949" y1="446" x2="1204" y2="446" stroke="#173C88" stroke-width="2"/>
  <line x1="949" y1="458" x2="1204" y2="458" stroke="#D6DDEA" stroke-width="1"/>
  <text x="949" y="494" width="255" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" fill="#555F6F">
    <tspan x="949" dy="0">根据不同层级与职位制定路径，</tspan>
    <tspan x="949" dy="26">从基础技能到管理能力逐步提升，</tspan>
    <tspan x="949" dy="26">形成连续成长机制。</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not fill the bottom area with paragraph-heavy text boxes; the technique depends on short, horizontally comparable modules.
- ❌ Do not use equal-sized bordered cards with heavy outlines; they make the slide feel like a table instead of a premium editorial grid.
- ❌ Do not place the title in the white lower area; the macro/micro separation only works when the title is locked inside the dark header block.
- ❌ Do not apply filters to `<line>` dividers; use plain thin strokes for reliable PowerPoint translation.
- ❌ Do not rely on automatic text wrapping; use explicit `width` attributes and manual `<tspan>` line breaks where precise spacing matters.

## Composition notes
- Keep the header at roughly 35–38% of slide height; it should feel like a confident banner, not a small title strip.
- Use 4 columns with identical widths and consistent gaps; the mathematical rhythm is what makes the detail area feel organized.
- Let navy or corporate blue repeat in the header, column titles, divider rules, and number chips to unify the two zones.
- Preserve generous negative space below the dividers; body copy should be concise, gray, and visually secondary to the column headings.