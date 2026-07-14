# SVG Recipe — Consultant-Style Focused Data Chart

## Visual mechanism
A clean business chart uses one saturated accent series to prove the headline, while all other series are rendered as pale context. The chart removes legends and visual noise, replacing them with direct end labels and a takeaway title that states the conclusion before the viewer studies the data.

## SVG primitives needed
- 1× `<rect>` for the white slide background.
- 1× `<rect>` for a subtle insight callout card.
- 5× `<line>` for horizontal gridlines and the understated x-axis baseline.
- 4× `<path>` for editable line-chart data series.
- 8× `<circle>` for selected endpoint markers on the highlighted series and muted context endpoints.
- 1× `<filter id="softShadow">` applied to the callout card.
- 1× `<filter id="accentGlow">` applied to the highlighted data path.
- Multiple `<text>` elements with explicit `width` for the action title, subtitle, axis labels, direct series labels, callout text, and source note.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="accentGlow" x="-5%" y="-20%" width="110%" height="140%">
      <feGaussianBlur stdDeviation="2.2" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <text x="84" y="62" width="930" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="29" font-weight="700" fill="#1E1E1E">
    <tspan x="84" dy="0">Kwanzaan Cherry is the only species with sustained sales growth,</tspan>
    <tspan x="84" dy="38">more than doubling volume since 2020</tspan>
  </text>
  <text x="84" y="146" width="720" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#777777">
    Trees sold by species, Aspira Nursery, 2020–2023
  </text>

  <!-- Plot area: x 150–885, y 230–560. Direct labels occupy right gutter. -->
  <line x1="150" y1="277" x2="945" y2="277" stroke="#ECEFF2" stroke-width="1"/>
  <line x1="150" y1="371" x2="945" y2="371" stroke="#ECEFF2" stroke-width="1"/>
  <line x1="150" y1="466" x2="945" y2="466" stroke="#ECEFF2" stroke-width="1"/>
  <line x1="150" y1="560" x2="945" y2="560" stroke="#D5D8DC" stroke-width="1.2"/>
  <line x1="150" y1="230" x2="945" y2="230" stroke="#F5F6F7" stroke-width="1"/>

  <text x="94" y="282" width="44" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#9A9A9A" text-anchor="end">100</text>
  <text x="94" y="376" width="44" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#9A9A9A" text-anchor="end">80</text>
  <text x="94" y="471" width="44" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#9A9A9A" text-anchor="end">60</text>
  <text x="94" y="565" width="44" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#9A9A9A" text-anchor="end">40</text>

  <text x="150" y="604" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#333333" text-anchor="middle">2020</text>
  <text x="395" y="604" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#333333" text-anchor="middle">2021</text>
  <text x="640" y="604" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#333333" text-anchor="middle">2022</text>
  <text x="885" y="604" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#333333" text-anchor="middle">2023</text>

  <!-- Muted contextual series -->
  <path d="M150 357 L395 367 L640 371 L885 385" fill="none" stroke="#C9CDD2" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M150 414 L395 395 L640 423 L885 428" fill="none" stroke="#C9CDD2" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M150 381 L395 414 L640 437 L885 489" fill="none" stroke="#C9CDD2" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>

  <circle cx="885" cy="385" r="4" fill="#C9CDD2"/>
  <circle cx="885" cy="428" r="4" fill="#C9CDD2"/>
  <circle cx="885" cy="489" r="4" fill="#C9CDD2"/>

  <!-- Highlighted series -->
  <path d="M150 536 L395 508 L640 395 L885 263" fill="none" stroke="#2F80ED" stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round" filter="url(#accentGlow)"/>
  <circle cx="150" cy="536" r="5.5" fill="#FFFFFF" stroke="#2F80ED" stroke-width="3"/>
  <circle cx="395" cy="508" r="5.5" fill="#FFFFFF" stroke="#2F80ED" stroke-width="3"/>
  <circle cx="640" cy="395" r="5.5" fill="#FFFFFF" stroke="#2F80ED" stroke-width="3"/>
  <circle cx="885" cy="263" r="7.5" fill="#2F80ED" stroke="#FFFFFF" stroke-width="3"/>

  <!-- Direct labels instead of legend -->
  <text x="966" y="268" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700" fill="#2F80ED">Kwanzaan Cherry</text>
  <text x="966" y="390" width="230" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13.5" fill="#8F969E">Thundercloud Plum</text>
  <text x="966" y="433" width="230" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13.5" fill="#8F969E">Golden Rain Tree</text>
  <text x="966" y="494" width="250" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13.5" fill="#8F969E">Tina Sargent Crabapple</text>

  <!-- Executive-style insight card -->
  <rect x="905" y="109" width="260" height="92" rx="16" fill="#FFFFFF" stroke="#E7ECF2" stroke-width="1" filter="url(#softShadow)"/>
  <text x="928" y="144" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" fill="#6B7280">KEY PROOF POINT</text>
  <text x="928" y="176" width="220" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="700" fill="#2F80ED">+129%</text>
  <text x="1015" y="176" width="130" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13.5" fill="#4B5563">growth vs. 2020</text>

  <text x="84" y="665" width="680" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12.5" fill="#8C8C8C">
    Source: internal sales ledger; units indexed to trees sold. Highlighting applied to the series relevant to the recommendation.
  </text>
</svg>
```

## Avoid in this skill
- ❌ A separate legend box; it forces the audience to look back and forth. Use direct labels at the line ends.
- ❌ Equal visual weight for every data series; the focused series must dominate through color, stroke weight, and labeling.
- ❌ Heavy chart borders, vertical gridlines, dense tick marks, or decorative axes that compete with the message.
- ❌ Labeling every data point unless the story requires it; endpoint labels and one concise callout are usually enough.
- ❌ `marker-end` arrowheads on paths for annotations; if an arrow is needed, use a direct `<line>` with its own supported arrow treatment or a simple drawn path shape.

## Composition notes
- Reserve the top 20–25% of the slide for the action title and subtitle; the title should state the finding, not describe the chart type.
- Keep the plot area wide and low, with a generous right gutter for direct labels so no legend is needed.
- Use one accent color only for the hero series; repeat it in the endpoint label and key proof-point card.
- Let muted gray series provide context but not competition: thin strokes, pale labels, and no data-point clutter.