# SVG Recipe — Interactive Gamified Spinning Wheel ("Wheel of Fortune")

## Visual mechanism
A uniform pie chart is restyled as a physical game-show wheel: equal colorful wedges, bold slice labels, a fixed pointer, and a prominent center “SPIN!” button. The wheel itself is a grouped set of editable wedge paths so PowerPoint users can apply a native Spin emphasis animation to the wheel group and trigger it from the button.

## SVG primitives needed
- 12× `<path>` for equal pie-slice wedges, each with a different vibrant fill
- 12× `<line>` for subtle radial separators between slices
- 2× `<circle>` for the heavy outer rim and inner wheel hub
- 12× `<circle>` for decorative rim bulbs/game-show lights
- 12× `<text>` for slice labels placed near the outer edge of each wedge
- 1× `<path>` for the large fixed red pointer arrow, made from a custom editable path instead of SVG markers
- 1× `<circle>` for the central clickable spin button
- 2× `<text>` for the center button label and small instruction label
- 3× `<rect>` for the premium stage background, right-side instruction panel, and callout card
- 1× `<linearGradient>` for the diagonal presentation-stage background
- 1× `<radialGradient>` for the center spin button highlight
- 1× `<filter id="softShadow">` applied to wheel rim, pointer, button, and cards
- 1× `<filter id="textLift">` applied to large text for a game-show outlined/shadowed look

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="stageBg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#07162f"/>
      <stop offset="48%" stop-color="#123b7a"/>
      <stop offset="100%" stop-color="#081329"/>
    </linearGradient>
    <linearGradient id="redPointer" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ff1d35"/>
      <stop offset="100%" stop-color="#c9001e"/>
    </linearGradient>
    <radialGradient id="buttonGrad" cx="35%" cy="28%" r="70%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="58%" stop-color="#fff4ba"/>
      <stop offset="100%" stop-color="#ffcf33"/>
    </radialGradient>
    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="8"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="textLift" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="5"/>
      <feGaussianBlur stdDeviation="3"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#stageBg)"/>
  <path d="M0 720 L1280 720 L1280 210 C980 390 740 520 430 720 Z" fill="#2d62b7" opacity="0.55"/>
  <circle cx="135" cy="115" r="210" fill="#ffffff" opacity="0.05"/>
  <circle cx="1125" cy="610" r="260" fill="#ffffff" opacity="0.04"/>

  <text x="720" y="95" width="480" font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="900" fill="#fff06a" stroke="#173e7e" stroke-width="8" paint-order="stroke" filter="url(#textLift)">WHO'S NEXT?</text>
  <text x="724" y="145" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#d7e6ff">A clickable wheel for raffles, Q&amp;A, standups, and icebreakers.</text>

  <circle cx="440" cy="360" r="272" fill="#06101f" opacity="0.70" filter="url(#softShadow)"/>
  <circle cx="440" cy="360" r="258" fill="#111827" stroke="#f7d44a" stroke-width="8"/>

  <g id="editable-wheel-group">
    <path d="M440 360 L440 115 A245 245 0 0 1 562.5 147.8 Z" fill="#ff595e"/>
    <path d="M440 360 L562.5 147.8 A245 245 0 0 1 652.2 237.5 Z" fill="#ffca3a"/>
    <path d="M440 360 L652.2 237.5 A245 245 0 0 1 685 360 Z" fill="#8ac926"/>
    <path d="M440 360 L685 360 A245 245 0 0 1 652.2 482.5 Z" fill="#1982c4"/>
    <path d="M440 360 L652.2 482.5 A245 245 0 0 1 562.5 572.2 Z" fill="#6a4c93"/>
    <path d="M440 360 L562.5 572.2 A245 245 0 0 1 440 605 Z" fill="#ff924c"/>
    <path d="M440 360 L440 605 A245 245 0 0 1 317.5 572.2 Z" fill="#00b4d8"/>
    <path d="M440 360 L317.5 572.2 A245 245 0 0 1 227.8 482.5 Z" fill="#2ec4b6"/>
    <path d="M440 360 L227.8 482.5 A245 245 0 0 1 195 360 Z" fill="#ff9f1c"/>
    <path d="M440 360 L195 360 A245 245 0 0 1 227.8 237.5 Z" fill="#adb5bd"/>
    <path d="M440 360 L227.8 237.5 A245 245 0 0 1 317.5 147.8 Z" fill="#4cc9f0"/>
    <path d="M440 360 L317.5 147.8 A245 245 0 0 1 440 115 Z" fill="#52b788"/>

    <line x1="440" y1="360" x2="440" y2="115" stroke="#14213d" stroke-width="3" opacity="0.45"/>
    <line x1="440" y1="360" x2="562.5" y2="147.8" stroke="#14213d" stroke-width="3" opacity="0.45"/>
    <line x1="440" y1="360" x2="652.2" y2="237.5" stroke="#14213d" stroke-width="3" opacity="0.45"/>
    <line x1="440" y1="360" x2="685" y2="360" stroke="#14213d" stroke-width="3" opacity="0.45"/>
    <line x1="440" y1="360" x2="652.2" y2="482.5" stroke="#14213d" stroke-width="3" opacity="0.45"/>
    <line x1="440" y1="360" x2="562.5" y2="572.2" stroke="#14213d" stroke-width="3" opacity="0.45"/>
    <line x1="440" y1="360" x2="440" y2="605" stroke="#14213d" stroke-width="3" opacity="0.45"/>
    <line x1="440" y1="360" x2="317.5" y2="572.2" stroke="#14213d" stroke-width="3" opacity="0.45"/>
    <line x1="440" y1="360" x2="227.8" y2="482.5" stroke="#14213d" stroke-width="3" opacity="0.45"/>
    <line x1="440" y1="360" x2="195" y2="360" stroke="#14213d" stroke-width="3" opacity="0.45"/>
    <line x1="440" y1="360" x2="227.8" y2="237.5" stroke="#14213d" stroke-width="3" opacity="0.45"/>
    <line x1="440" y1="360" x2="317.5" y2="147.8" stroke="#14213d" stroke-width="3" opacity="0.45"/>

    <text x="488" y="186" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="800" fill="#ffffff">Maya</text>
    <text x="571" y="234" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="800" fill="#ffffff">Noah</text>
    <text x="619" y="317" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="800" fill="#ffffff">Ava</text>
    <text x="619" y="413" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="800" fill="#ffffff">Liam</text>
    <text x="571" y="496" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="800" fill="#ffffff">Emma</text>
    <text x="488" y="543" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="800" fill="#ffffff">Iris</text>
    <text x="392" y="543" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="800" fill="#ffffff">Leo</text>
    <text x="309" y="496" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="800" fill="#ffffff">Zoe</text>
    <text x="261" y="413" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="800" fill="#ffffff">Kai</text>
    <text x="261" y="317" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="800" fill="#ffffff">Luna</text>
    <text x="309" y="234" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="800" fill="#ffffff">Owen</text>
    <text x="392" y="186" width="90" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="800" fill="#ffffff">Nia</text>
  </g>

  <circle cx="440" cy="88" r="9" fill="#fff06a"/><circle cx="576" cy="124" r="9" fill="#fff06a"/><circle cx="676" cy="224" r="9" fill="#fff06a"/>
  <circle cx="712" cy="360" r="9" fill="#fff06a"/><circle cx="676" cy="496" r="9" fill="#fff06a"/><circle cx="576" cy="596" r="9" fill="#fff06a"/>
  <circle cx="440" cy="632" r="9" fill="#fff06a"/><circle cx="304" cy="596" r="9" fill="#fff06a"/><circle cx="204" cy="496" r="9" fill="#fff06a"/>
  <circle cx="168" cy="360" r="9" fill="#fff06a"/><circle cx="204" cy="224" r="9" fill="#fff06a"/><circle cx="304" cy="124" r="9" fill="#fff06a"/>

  <path d="M690 360 L760 306 L760 335 L986 335 Q1012 335 1012 360 Q1012 385 986 385 L760 385 L760 414 Z" fill="url(#redPointer)" stroke="#ffffff" stroke-width="5" filter="url(#softShadow)"/>
  <text x="792" y="326" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="800" fill="#ffffff">fixed winner pointer</text>

  <circle cx="440" cy="360" r="72" fill="url(#buttonGrad)" stroke="#101827" stroke-width="6" filter="url(#softShadow)"/>
  <text x="368" y="372" width="144" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="900" fill="#101827">SPIN!</text>

  <rect x="730" y="445" width="430" height="150" rx="28" fill="#ffffff" opacity="0.12" stroke="#87b9ff" stroke-width="2"/>
  <text x="760" y="500" width="370" font-family="Segoe UI, Microsoft YaHei" font-size="27" font-weight="900" fill="#ffffff">PowerPoint step:</text>
  <text x="760" y="540" width="365" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="600" fill="#dcecff">Group the wheel wedges and labels, then add a native Spin emphasis animation triggered by the SPIN button.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<animate>` or `<animateTransform>` for the spin; create the wheel visually in SVG, then apply PowerPoint’s native Spin animation after import.
- ❌ Do not use `marker-end` for the pointer arrow; marker arrowheads may disappear, so build the pointer as an editable `<path>`.
- ❌ Do not place slice labels without explicit `width` attributes; PowerPoint text boxes need fixed widths to avoid unexpected wrapping or clipping.
- ❌ Do not rely on a real SVG `<pie>` or chart object; build equal wedges as editable paths if the slide must remain shape-editable.
- ❌ Do not apply `filter` to separator `<line>` elements; use filters only on paths, circles, rects, or text.

## Composition notes
- Keep the wheel large, ideally 65–80% of slide height, with enough margin for the pointer to overlap the rim without hiding the center button.
- Use high-contrast, alternating slice colors; labels should be bold white or black depending on slice brightness.
- The pointer must remain visually fixed outside the animated wheel group so the audience understands where the final winner is read.
- Reserve one side of the slide for the title/instructions; avoid cluttering the wheel area because the labels and center button already carry high visual density.