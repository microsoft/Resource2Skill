# SVG Recipe — Centered Statement

## Visual mechanism
A single decisive statement is centered in a quiet, high-whitespace canvas, with subtle atmospheric gradients and a few restrained editorial accents to make the quote feel premium rather than empty. The layout relies on scale, alignment, and soft contrast: the statement is the hero, while background blobs, quote marks, and a blinking-cursor accent imply a modern “typewriter reveal” mood.

## SVG primitives needed
- 1× full-slide `<rect>` for the warm off-white background
- 2× large `<ellipse>` shapes for soft blurred atmospheric color fields
- 2× `<path>` shapes for abstract editorial corner flourishes
- 1× rounded `<rect>` for the translucent highlight behind the key phrase
- 1× narrow rounded `<rect>` for the typewriter cursor accent
- 3× `<text>` elements for quote mark, eyebrow label, and centered statement
- 1× `<linearGradient>` for the background wash
- 2× `<radialGradient>` fills for soft color blooms
- 1× `<filter id="softBlur">` using `feGaussianBlur` for background haze
- 1× `<filter id="statementShadow">` using offset blur merge for subtle text lift
- 1× `<filter id="accentGlow">` using `feGaussianBlur` for the cursor glow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFF9EF"/>
      <stop offset="0.48" stop-color="#F8F4ED"/>
      <stop offset="1" stop-color="#EEF6FA"/>
    </linearGradient>

    <radialGradient id="coralBloom" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#FF8A65" stop-opacity="0.35"/>
      <stop offset="0.55" stop-color="#FFB199" stop-opacity="0.16"/>
      <stop offset="1" stop-color="#FFB199" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="aquaBloom" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#5ED9D1" stop-opacity="0.34"/>
      <stop offset="0.58" stop-color="#8DEBE4" stop-opacity="0.13"/>
      <stop offset="1" stop-color="#8DEBE4" stop-opacity="0"/>
    </radialGradient>

    <filter id="softBlur" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="34"/>
    </filter>

    <filter id="statementShadow" x="-10%" y="-20%" width="120%" height="150%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="accentGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="5"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <ellipse cx="200" cy="155" rx="270" ry="150" fill="url(#coralBloom)" filter="url(#softBlur)"/>
  <ellipse cx="1115" cy="585" rx="330" ry="185" fill="url(#aquaBloom)" filter="url(#softBlur)"/>

  <path d="M87 114 C132 80, 202 84, 236 125 C268 164, 248 215, 190 228 C140 239, 77 214, 61 171 C52 146, 62 128, 87 114 Z"
        fill="#FFB199" opacity="0.16"/>
  <path d="M1045 112 C1092 64, 1182 74, 1211 141 C1239 204, 1196 265, 1123 260 C1056 255, 1012 199, 1027 151 C1031 137, 1037 123, 1045 112 Z"
        fill="#64D8CB" opacity="0.14"/>

  <path d="M178 536 C210 508, 252 503, 289 522"
        fill="none" stroke="#151A21" stroke-opacity="0.12" stroke-width="3" stroke-linecap="round"/>
  <path d="M1001 189 C1035 207, 1072 202, 1105 171"
        fill="none" stroke="#151A21" stroke-opacity="0.12" stroke-width="3" stroke-linecap="round"/>

  <text x="640" y="150" width="360"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14"
        font-weight="700"
        letter-spacing="4"
        fill="#6F7782">
    CENTERED STATEMENT
  </text>

  <text x="640" y="258" width="160"
        text-anchor="middle"
        font-family="Georgia, 'Times New Roman', serif"
        font-size="108"
        fill="#151A21"
        opacity="0.10">
    “
  </text>

  <rect x="436" y="386" width="408" height="56" rx="28"
        fill="#FFFFFF" opacity="0.68"/>

  <text x="640" y="318" width="900"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="54"
        font-weight="650"
        line-height="1.12"
        fill="#151A21"
        filter="url(#statementShadow)">
    <tspan x="640" dy="0">The future belongs</tspan>
    <tspan x="640" dy="64">to teams who turn</tspan>
    <tspan x="640" dy="64" font-weight="800" fill="#0E766E">clarity into momentum</tspan>
  </text>

  <rect x="864" y="401" width="5" height="46" rx="2.5"
        fill="#0E766E" filter="url(#accentGlow)"/>

  <circle cx="370" cy="304" r="4" fill="#FF8A65" opacity="0.55"/>
  <circle cx="914" cy="336" r="5" fill="#0E766E" opacity="0.42"/>
  <circle cx="406" cy="482" r="3" fill="#151A21" opacity="0.18"/>
  <circle cx="895" cy="246" r="3" fill="#151A21" opacity="0.16"/>

  <path d="M379 253 L386 267 L401 270 L390 281 L392 296 L379 289 L365 296 L368 281 L356 270 L372 267 Z"
        fill="#FF8A65" opacity="0.34"/>
  <path d="M907 475 L913 487 L926 490 L916 499 L918 512 L907 506 L895 512 L897 499 L887 490 L901 487 Z"
        fill="#64D8CB" opacity="0.38"/>

  <text x="640" y="596" width="620"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17"
        font-weight="500"
        fill="#6F7782">
    Minimal composition for a quote, principle, or keynote thesis
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not add multiple body paragraphs or bullet lists; the technique collapses if the centered statement is no longer singular.
- ❌ Do not rely on automatic text wrapping; manually split the statement into `<tspan>` lines and give every `<text>` a clear `width`.
- ❌ Do not use heavy borders, tables, dashboards, or dense icon rows; they compete with the statement.
- ❌ Do not use `<textPath>`, `<foreignObject>`, masks, or patterned fills for decorative typography; keep the quote editable as native text.
- ❌ Do not apply filters to `<line>` elements; use filtered `<rect>`, `<path>`, `<ellipse>`, or `<text>` only.

## Composition notes
- Keep the statement centered both optically and spatially; reserve roughly the middle 55–60% of the slide width for the main words.
- Use large negative space above and below the statement so the slide feels intentional, not underfilled.
- Let accent color appear only in one phrase, cursor, and tiny decorative marks to create rhythm without visual noise.
- Background gradients and blurred blooms should stay low-contrast; they are atmosphere, not content.