# SVG Recipe — Infographic Table of Contents with Fading Bars

## Visual mechanism
A left-side thematic emblem anchors the slide, while the right side presents agenda items as numbered color badges attached to long rounded bars that fade from soft gray into the background. The fade keeps the list structured without becoming visually heavy, creating a premium, airy table-of-contents slide.

## SVG primitives needed
- 1× `<rect>` for the off-white slide background
- 2× `<circle>` with thick strokes for the concentric gray emblem rings
- 4× `<path>` for decorative colored arcs and the central brain/lightbulb-style icon
- 1× `<circle>` for the white central icon plate
- 1× `<filter id="softShadow">` applied to the emblem plate and agenda badges
- 1× `<filter id="badgeGlow">` applied subtly to colored number circles
- 1× `<linearGradient id="barFade">` for gray content bars fading left-to-right into transparency
- 6× `<linearGradient>` fills for colored number badges
- 6× `<rect>` for the fading rounded agenda bars
- 6× `<circle>` for numbered agenda badges
- 6× `<text>` for white numbers inside the badges
- 6× `<text>` for agenda item labels
- 1× `<text>` for the slide title
- 1× `<line>` and 5× `<circle>` for the decorative title underline and color dots

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#fbfbf8"/>
      <stop offset="100%" stop-color="#f1f3f4"/>
    </linearGradient>

    <linearGradient id="barFade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#d9d9d9" stop-opacity="0.92"/>
      <stop offset="58%" stop-color="#d9d9d9" stop-opacity="0.34"/>
      <stop offset="100%" stop-color="#d9d9d9" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="redBadge" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ff7a66"/>
      <stop offset="100%" stop-color="#e74c3c"/>
    </linearGradient>
    <linearGradient id="purpleBadge" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#c69be0"/>
      <stop offset="100%" stop-color="#9b59b6"/>
    </linearGradient>
    <linearGradient id="blueBadge" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#74c7f5"/>
      <stop offset="100%" stop-color="#3498db"/>
    </linearGradient>
    <linearGradient id="greenBadge" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#78e6a4"/>
      <stop offset="100%" stop-color="#2ecc71"/>
    </linearGradient>
    <linearGradient id="yellowBadge" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffe16a"/>
      <stop offset="100%" stop-color="#f1c40f"/>
    </linearGradient>
    <linearGradient id="orangeBadge" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffb066"/>
      <stop offset="100%" stop-color="#e67e22"/>
    </linearGradient>

    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="12"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="badgeGlow" x="-35%" y="-35%" width="170%" height="170%">
      <feGaussianBlur stdDeviation="3"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <!-- Title -->
  <text x="650" y="82" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="700" fill="#30343b">
    Table of content
  </text>
  <line x1="652" y1="108" x2="880" y2="108" stroke="#c9ced3" stroke-width="3"/>
  <circle cx="910" cy="108" r="6" fill="#e74c3c"/>
  <circle cx="932" cy="108" r="6" fill="#9b59b6"/>
  <circle cx="954" cy="108" r="6" fill="#3498db"/>
  <circle cx="976" cy="108" r="6" fill="#2ecc71"/>
  <circle cx="998" cy="108" r="6" fill="#f1c40f"/>

  <!-- Left thematic emblem -->
  <circle cx="270" cy="378" r="172" fill="none" stroke="#dddddd" stroke-width="34"/>
  <circle cx="270" cy="378" r="120" fill="none" stroke="#eeeeee" stroke-width="28"/>
  <path d="M130 378 A140 140 0 0 1 270 238" fill="none" stroke="#00b0f0" stroke-width="16" stroke-linecap="round"/>
  <path d="M270 518 A140 140 0 0 1 410 378" fill="none" stroke="#ffc000" stroke-width="16" stroke-linecap="round"/>
  <circle cx="270" cy="378" r="92" fill="#ffffff" filter="url(#softShadow)"/>

  <!-- Brain / idea icon built from editable paths -->
  <path d="M237 349
           C222 348 210 360 210 375
           C210 386 216 395 225 399
           C222 414 234 427 249 424
           C256 438 277 438 284 424
           C298 428 312 418 312 403
           C327 399 336 386 333 371
           C330 354 314 345 299 351
           C290 333 260 333 250 351
           C246 350 242 349 237 349 Z"
        fill="#00b0f0" opacity="0.95"/>
  <path d="M263 344
           C275 336 294 340 301 355
           C315 352 328 362 329 376
           C330 391 319 402 305 402
           C308 415 297 427 283 423
           C275 436 254 433 251 418
           C236 422 224 408 229 394
           C217 388 215 371 226 361
           C235 352 249 354 257 363"
        fill="none" stroke="#ffffff" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M270 423 L270 448 M246 448 H294 M254 463 H286"
        fill="none" stroke="#ffc000" stroke-width="8" stroke-linecap="round"/>
  <circle cx="168" cy="260" r="8" fill="#e74c3c"/>
  <circle cx="388" cy="286" r="7" fill="#3498db"/>
  <circle cx="142" cy="492" r="6" fill="#2ecc71"/>
  <circle cx="415" cy="468" r="9" fill="#f1c40f"/>

  <!-- Agenda fading bars -->
  <g font-family="Segoe UI, Microsoft YaHei">
    <rect x="678" y="157" width="486" height="58" rx="29" fill="url(#barFade)"/>
    <circle cx="670" cy="186" r="34" fill="url(#redBadge)" filter="url(#badgeGlow)"/>
    <text x="651" y="198" width="38" font-size="31" font-weight="700" fill="#ffffff">1</text>
    <text x="725" y="194" width="420" font-size="25" font-weight="600" fill="#30343b">Executive summary</text>

    <rect x="678" y="235" width="486" height="58" rx="29" fill="url(#barFade)"/>
    <circle cx="670" cy="264" r="34" fill="url(#purpleBadge)" filter="url(#badgeGlow)"/>
    <text x="651" y="276" width="38" font-size="31" font-weight="700" fill="#ffffff">2</text>
    <text x="725" y="272" width="420" font-size="25" font-weight="600" fill="#30343b">Market landscape</text>

    <rect x="678" y="313" width="486" height="58" rx="29" fill="url(#barFade)"/>
    <circle cx="670" cy="342" r="34" fill="url(#blueBadge)" filter="url(#badgeGlow)"/>
    <text x="651" y="354" width="38" font-size="31" font-weight="700" fill="#ffffff">3</text>
    <text x="725" y="350" width="420" font-size="25" font-weight="600" fill="#30343b">Customer insights</text>

    <rect x="678" y="391" width="486" height="58" rx="29" fill="url(#barFade)"/>
    <circle cx="670" cy="420" r="34" fill="url(#greenBadge)" filter="url(#badgeGlow)"/>
    <text x="651" y="432" width="38" font-size="31" font-weight="700" fill="#ffffff">4</text>
    <text x="725" y="428" width="420" font-size="25" font-weight="600" fill="#30343b">Strategic priorities</text>

    <rect x="678" y="469" width="486" height="58" rx="29" fill="url(#barFade)"/>
    <circle cx="670" cy="498" r="34" fill="url(#yellowBadge)" filter="url(#badgeGlow)"/>
    <text x="651" y="510" width="38" font-size="31" font-weight="700" fill="#ffffff">5</text>
    <text x="725" y="506" width="420" font-size="25" font-weight="600" fill="#30343b">Roadmap and milestones</text>

    <rect x="678" y="547" width="486" height="58" rx="29" fill="url(#barFade)"/>
    <circle cx="670" cy="576" r="34" fill="url(#orangeBadge)" filter="url(#badgeGlow)"/>
    <text x="651" y="588" width="38" font-size="31" font-weight="700" fill="#ffffff">6</text>
    <text x="725" y="584" width="420" font-size="25" font-weight="600" fill="#30343b">Next steps</text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to create the fading bars; use a native `<linearGradient>` with `stop-opacity` instead.
- ❌ Do not place `clip-path` on rectangles or paths for the emblem rings; use stroked circles or editable paths.
- ❌ Do not use `<use>` to duplicate agenda rows; write each row explicitly so every item remains editable after translation.
- ❌ Do not use `marker-end` arrows for list connectors; this design does not need arrows, and path markers may disappear.
- ❌ Do not omit `width` on text elements; agenda labels can reflow or clip incorrectly in PowerPoint without explicit widths.

## Composition notes
- Keep the left emblem within roughly the left 40% of the slide and vertically centered; it should feel like a visual anchor, not a competing title.
- Place the agenda stack in the right 55–60% of the slide, with consistent vertical rhythm and all badge centers aligned on one x-coordinate.
- Let each fading bar extend far enough to support the text, but fade before the right margin to preserve negative space.
- Use one vivid badge color per row, while keeping bars neutral gray so the color rhythm comes from the numbered circles.