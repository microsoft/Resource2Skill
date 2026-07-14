# SVG Recipe — Minimalist Typographic Grid Bio

## Visual mechanism
A highly disciplined editorial bio slide built from an invisible two-column grid: a large accent-colored name and generous paragraph column on the left, with compact aligned personal details on the right. The premium feel comes from restraint—deep grey text, hairline rules, ample whitespace, and consistent typographic rhythm.

## SVG primitives needed
- 1× `<rect>` for the soft off-white slide background
- 1× `<linearGradient>` for a barely perceptible paper-like background tint
- 6× `<line>` for editorial hairlines, column boundaries, and baseline rhythm accents
- 1× `<rect>` for a small accent color block anchoring the profile label
- 12× `<text>` blocks for name, role, section labels, paragraph copy, stat labels, stat values, and footer details
- Nested `<tspan>` elements inside paragraph and stat text for controlled multiline wrapping and inline hierarchy

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="paperTint" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="62%" stop-color="#FAFBFD"/>
      <stop offset="100%" stop-color="#F4F7FB"/>
    </linearGradient>
  </defs>

  <!-- Background -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#paperTint)"/>

  <!-- Editorial grid hairlines -->
  <line x1="112" y1="96" x2="112" y2="624" stroke="#E4E8EF" stroke-width="1"/>
  <line x1="808" y1="96" x2="808" y2="624" stroke="#E4E8EF" stroke-width="1"/>
  <line x1="112" y1="624" x2="1168" y2="624" stroke="#E4E8EF" stroke-width="1"/>
  <line x1="112" y1="248" x2="736" y2="248" stroke="#D7DDE8" stroke-width="1"/>
  <line x1="872" y1="248" x2="1168" y2="248" stroke="#D7DDE8" stroke-width="1"/>
  <line x1="872" y1="504" x2="1168" y2="504" stroke="#D7DDE8" stroke-width="1"/>

  <!-- Small accent anchor -->
  <rect x="112" y="108" width="42" height="6" rx="3" fill="#4472C4"/>

  <!-- Left column: identity -->
  <text x="112" y="152" width="620"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="700" letter-spacing="3"
        fill="#4472C4">
    PROFILE
  </text>

  <text x="112" y="224" width="660"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="58" font-weight="700"
        fill="#4472C4">
    工藤新一
  </text>

  <text x="116" y="268" width="620"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" font-weight="400"
        fill="#737373">
    High School Detective · Strategic Reasoning Specialist
  </text>

  <!-- Left column: biography paragraph with deliberate line rhythm -->
  <text x="112" y="332" width="650"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="400"
        fill="#595959">
    <tspan x="112" dy="0">高中生侦探，原先就读于帝丹高中二年B班，</tspan>
    <tspan x="112" dy="38">是毛利兰的青梅竹马、工藤优作和工藤有希子</tspan>
    <tspan x="112" dy="38">之独子。因拥有一流的推理能力，而被称为</tspan>
    <tspan x="112" dy="38">“日本警察的救世主”、“平成年代的福尔摩斯”。</tspan>
    <tspan x="112" dy="38">他以冷静观察、快速归纳与严密逻辑著称，</tspan>
    <tspan x="112" dy="38">常在复杂局势中提炼关键线索并推动决策。</tspan>
  </text>

  <!-- Right column: compact stat block -->
  <text x="872" y="152" width="296"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="700" letter-spacing="3"
        fill="#4472C4">
    DETAILS
  </text>

  <text x="872" y="290" width="96"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="700"
        fill="#4472C4">
    <tspan x="872" dy="0">年龄</tspan>
    <tspan x="872" dy="42">性别</tspan>
    <tspan x="872" dy="42">身高</tspan>
    <tspan x="872" dy="42">体重</tspan>
    <tspan x="872" dy="42">出生</tspan>
    <tspan x="872" dy="42">国籍</tspan>
  </text>

  <text x="1000" y="290" width="168"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="400"
        fill="#595959">
    <tspan x="1000" dy="0">17岁</tspan>
    <tspan x="1000" dy="42">男</tspan>
    <tspan x="1000" dy="42">174公分</tspan>
    <tspan x="1000" dy="42">58公斤</tspan>
    <tspan x="1000" dy="42">5月4日</tspan>
    <tspan x="1000" dy="42">日本</tspan>
  </text>

  <!-- Right column: short professional summary -->
  <text x="872" y="548" width="296"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="700" letter-spacing="2.4"
        fill="#4472C4">
    CORE STRENGTH
  </text>

  <text x="872" y="586" width="296"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="400"
        fill="#595959">
    <tspan x="872" dy="0">Observation-led problem solving,</tspan>
    <tspan x="872" dy="30">deductive analysis, and calm</tspan>
    <tspan x="872" dy="30">communication under pressure.</tspan>
  </text>

  <!-- Footer metadata -->
  <text x="112" y="660" width="420"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="400"
        fill="#9A9A9A">
    Internal biography profile · Executive introduction format
  </text>

  <text x="872" y="660" width="296"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="600"
        fill="#9A9A9A">
    CONFIDENTIAL / TEAM BRIEF
  </text>
</svg>
```

## Avoid in this skill
- ❌ Photo placeholders, avatars, or decorative icons; this technique is strongest when it proves professionalism through typography alone
- ❌ Pure black body copy on white; use deep grey such as `#595959` to reduce visual fatigue
- ❌ Center-aligned paragraphs; the design depends on strict left alignment and column discipline
- ❌ Dense bullet lists; convert bullets into either a flowing biography paragraph or a clean label/value stat grid
- ❌ Too many accent colors; one corporate accent color should carry the name, labels, and small anchors

## Composition notes
- Keep the left column dominant: roughly 60% of the slide width for name, role, and biography; reserve the right 25–30% for factual details.
- Align the top of the bio paragraph and the top of the stats block to the same horizontal guide for a polished grid feel.
- Use generous line spacing in paragraph copy—about 1.35× to 1.5× the font size—so the slide feels editorial rather than document-like.
- Add only a few hairline rules or tiny accent blocks; they should reveal the grid without becoming decorative clutter.