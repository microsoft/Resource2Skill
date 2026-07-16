# SVG Recipe — Text-Driven Grid Profile

## Visual mechanism
A dense profile narrative is decomposed into a magazine-like two-column grid: a wide editorial bio column on the left and a compact key-value data column on the right. The visual interest comes almost entirely from typographic hierarchy, generous line spacing, accent-colored labels, and disciplined alignment rather than imagery or icons.

## SVG primitives needed
- 1× `<rect>` for the white slide background
- 1× `<rect>` for a pale blue right-column data panel
- 1× `<rect>` for a slim vertical accent bar beside the profile name
- 1× `<rect>` for a soft horizontal title underline
- 6× `<line>` for subtle row separators in the structured data column
- 1× `<text>` for the small eyebrow/category label
- 1× `<text>` for the large profile name
- 1× `<text>` for the role/subtitle line
- 1× `<text>` for the narrative section label
- 1× `<text>` with multiple `<tspan>` lines for the biography block
- 1× `<text>` for the facts section label
- 6× `<text>` with nested `<tspan>` for inline key-value data rows
- 1× `<linearGradient>` for the subtle right-panel background wash

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="panelWash" x1="820" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#F4FAFF"/>
      <stop offset="100%" stop-color="#FFFFFF"/>
    </linearGradient>
  </defs>

  <!-- clean editorial background -->
  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <!-- right data panel, intentionally quiet -->
  <rect x="810" y="72" width="350" height="560" rx="28" fill="url(#panelWash)" stroke="#E4EEF8" stroke-width="1"/>

  <!-- left title anchor -->
  <rect x="118" y="86" width="8" height="92" rx="4" fill="#5D9CE3"/>
  <rect x="146" y="174" width="220" height="4" rx="2" fill="#D5E8FA"/>

  <text x="146" y="92" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="700" letter-spacing="2.2" fill="#8EA8C4">
    TEAM PROFILE / INVESTIGATION LEAD
  </text>

  <text x="146" y="152" width="610" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="50" font-weight="800" fill="#5D9CE3">
    Shinichi Kudo
  </text>

  <text x="146" y="204" width="560" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" font-weight="400" fill="#777777">
    Deductive strategist · metropolitan case consultant
  </text>

  <!-- narrative column -->
  <text x="146" y="284" width="240" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="800" letter-spacing="1.8" fill="#5D9CE3">
    BIOGRAPHICAL SUMMARY
  </text>

  <text x="146" y="328" width="585" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="21" font-weight="400" fill="#595959">
    <tspan x="146" dy="0">High school detective originally studying in Class B,</tspan>
    <tspan x="146" dy="34">Year 2 at Teitan High School. He is the childhood</tspan>
    <tspan x="146" dy="34">friend of Ran Mouri, and the only son of Yusaku</tspan>
    <tspan x="146" dy="34">Kudo and Yukiko Kudo.</tspan>

    <tspan x="146" dy="52">Possessing first-class deductive reasoning skills,</tspan>
    <tspan x="146" dy="34">he is known as the “Savior of the Japanese Police”</tspan>
    <tspan x="146" dy="34">and the “Sherlock Holmes of the Heisei Era.”</tspan>

    <tspan x="146" dy="52">He frequently assists Inspector Megure from the</tspan>
    <tspan x="146" dy="34">Tokyo Metropolitan Police Department, where his</tspan>
    <tspan x="146" dy="34">analytical precision is highly regarded.</tspan>
  </text>

  <!-- structured data column -->
  <text x="862" y="136" width="230" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="800" letter-spacing="1.8" fill="#5D9CE3">
    PROFILE DATA
  </text>

  <line x1="862" y1="170" x2="1110" y2="170" stroke="#DCEAF7" stroke-width="1.5"/>
  <line x1="862" y1="244" x2="1110" y2="244" stroke="#DCEAF7" stroke-width="1"/>
  <line x1="862" y1="318" x2="1110" y2="318" stroke="#DCEAF7" stroke-width="1"/>
  <line x1="862" y1="392" x2="1110" y2="392" stroke="#DCEAF7" stroke-width="1"/>
  <line x1="862" y1="466" x2="1110" y2="466" stroke="#DCEAF7" stroke-width="1"/>
  <line x1="862" y1="540" x2="1110" y2="540" stroke="#DCEAF7" stroke-width="1"/>

  <text x="862" y="214" width="270" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" fill="#595959">
    <tspan font-weight="800" fill="#5D9CE3">Age</tspan><tspan dx="70">17</tspan>
  </text>

  <text x="862" y="288" width="270" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" fill="#595959">
    <tspan font-weight="800" fill="#5D9CE3">Gender</tspan><tspan dx="40">Male</tspan>
  </text>

  <text x="862" y="362" width="270" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" fill="#595959">
    <tspan font-weight="800" fill="#5D9CE3">Height</tspan><tspan dx="42">174 cm</tspan>
  </text>

  <text x="862" y="436" width="270" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" fill="#595959">
    <tspan font-weight="800" fill="#5D9CE3">Weight</tspan><tspan dx="36">58 kg</tspan>
  </text>

  <text x="862" y="510" width="270" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" fill="#595959">
    <tspan font-weight="800" fill="#5D9CE3">DOB</tspan><tspan dx="70">May 4th</tspan>
  </text>

  <text x="862" y="584" width="270" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" fill="#595959">
    <tspan font-weight="800" fill="#5D9CE3">Nationality</tspan><tspan dx="22">Japan</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Relying on one giant text box for everything; it destroys hierarchy and makes alignment harder to control.
- ❌ Pure black body copy; use dark grey so dense paragraphs feel premium rather than heavy.
- ❌ Center-aligning long narrative text; it creates ragged edges and makes reading slower.
- ❌ Overdecorating with icons, portraits, or chart elements; the technique is strongest when typography carries the slide.
- ❌ Missing `width` attributes on `<text>` elements; PowerPoint text boxes need explicit widths for predictable rendering.

## Composition notes
- Keep the left column around 55–60% of the canvas width for the narrative block, with the right column around 25–30% for structured facts.
- Align the top of the biography block and the stats panel content so the slide reads as one coordinated grid.
- Use blue only for identity anchors and data labels; keep body text neutral grey to preserve a calm executive tone.
- Leave generous margins on all sides, especially above the name and around the right panel, so the dense text still feels breathable.