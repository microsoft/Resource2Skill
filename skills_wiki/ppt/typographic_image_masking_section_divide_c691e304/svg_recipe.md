# SVG Recipe — Typographic Image Masking (Section Divider)

## Visual mechanism
A huge, heavy “01” is converted into vector outline paths and used as a `clipPath` for a thematic photograph, creating the illusion that the image lives inside the typography. The masked number sits on a dark keynote-style background, balanced by a slim accent divider and crisp editorial copy on the right.

## SVG primitives needed
- 1× `<rect>` for the full-slide charcoal background.
- 1× `<image>` for the thematic photograph clipped into the oversized number.
- 1× `<clipPath>` containing custom `<path>` outlines for the “0” and “1” digit shapes.
- 3× duplicated `<path>` digit outlines for soft shadow, subtle rim highlight, and optional dark edge definition.
- 1× `<filter id="softShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` for the masked-number depth.
- 1× `<linearGradient>` for the thin vertical divider accent.
- 1× `<rect>` for the vertical divider line.
- 3× `<text>` blocks for eyebrow label, section title, and explanatory body copy.
- 3× small `<rect>` elements for a lower accent rhythm bar / animation cue.
- 1× `<line>` for a fine horizontal rule under the title.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="12" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <linearGradient id="dividerGrad" x1="0" y1="120" x2="0" y2="600" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#B7E44B"/>
      <stop offset="0.55" stop-color="#8BB32D"/>
      <stop offset="1" stop-color="#F03A16"/>
    </linearGradient>

    <!-- Convert the target number to editable vector outlines.
         The “0” is a compound evenodd path; the “1” is a heavy angular sans shape. -->
    <clipPath id="number01Clip" clipPathUnits="userSpaceOnUse">
      <path fill-rule="evenodd" d="
        M250 106
        C352 106 414 190 414 360
        C414 530 352 614 250 614
        C148 614 86 530 86 360
        C86 190 148 106 250 106
        Z
        M250 184
        C199 184 173 239 173 360
        C173 481 199 536 250 536
        C301 536 327 481 327 360
        C327 239 301 184 250 184
        Z"/>
      <path d="
        M520 600
        L520 206
        C496 229 462 244 421 250
        L421 171
        C466 164 506 142 543 106
        L614 106
        L614 600
        Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#1A1B20"/>

  <!-- Large typographic silhouette shadow behind the clipped photograph -->
  <path fill-rule="evenodd" filter="url(#softShadow)" fill="#07080A" opacity="0.72" d="
    M250 106 C352 106 414 190 414 360 C414 530 352 614 250 614
    C148 614 86 530 86 360 C86 190 148 106 250 106 Z
    M250 184 C199 184 173 239 173 360 C173 481 199 536 250 536
    C301 536 327 481 327 360 C327 239 301 184 250 184 Z
    M520 600 L520 206 C496 229 462 244 421 250 L421 171
    C466 164 506 142 543 106 L614 106 L614 600 Z"/>

  <!-- The photograph is clipped directly to the digit outlines. -->
  <image
    href="https://images.unsplash.com/photo-1533038590840-1cbea976a55e?auto=format&fit=crop&w=1200&q=90"
    x="40" y="70" width="620" height="580"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#number01Clip)"/>

  <!-- Subtle editable vector rim to make the clipped text feel intentional on dark background -->
  <path fill-rule="evenodd" fill="none" stroke="#FFFFFF" stroke-opacity="0.16" stroke-width="3" d="
    M250 106 C352 106 414 190 414 360 C414 530 352 614 250 614
    C148 614 86 530 86 360 C86 190 148 106 250 106 Z
    M250 184 C199 184 173 239 173 360 C173 481 199 536 250 536
    C301 536 327 481 327 360 C327 239 301 184 250 184 Z
    M520 600 L520 206 C496 229 462 244 421 250 L421 171
    C466 164 506 142 543 106 L614 106 L614 600 Z"/>

  <!-- Fine dark edge gives contrast where the photo is very bright -->
  <path fill-rule="evenodd" fill="none" stroke="#111318" stroke-opacity="0.42" stroke-width="8" d="
    M250 106 C352 106 414 190 414 360 C414 530 352 614 250 614
    C148 614 86 530 86 360 C86 190 148 106 250 106 Z
    M250 184 C199 184 173 239 173 360 C173 481 199 536 250 536
    C301 536 327 481 327 360 C327 239 301 184 250 184 Z
    M520 600 L520 206 C496 229 462 244 421 250 L421 171
    C466 164 506 142 543 106 L614 106 L614 600 Z"/>

  <!-- Accent divider and editorial text column -->
  <rect x="698" y="136" width="6" height="446" rx="3" fill="url(#dividerGrad)"/>

  <text x="742" y="164" width="410" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="700" letter-spacing="4" fill="#8BB32D">
    + CHAPTER 01
  </text>

  <text x="742" y="258" width="450" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="62" font-weight="800" letter-spacing="-1" fill="#F2F4F7">
    ORGANIC
    <tspan x="742" dy="66" fill="#F03A16">GROWTH</tspan>
  </text>

  <line x1="742" y1="365" x2="1118" y2="365" stroke="#FFFFFF" stroke-opacity="0.18" stroke-width="1.5"/>

  <text x="742" y="412" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" line-height="1.45" fill="#C8CCD2">
    Transform a simple section number into a cinematic hero graphic by clipping a rich photograph into oversized type outlines.
  </text>

  <!-- Lower accent rhythm, echoing an animation-strip or progress cue -->
  <rect x="742" y="570" width="164" height="16" rx="8" fill="#F03A16"/>
  <rect x="922" y="570" width="42" height="16" rx="8" fill="#F03A16" opacity="0.72"/>
  <rect x="978" y="570" width="24" height="16" rx="8" fill="#F03A16" opacity="0.38"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<text>` itself as the clipping shape; convert the number to `<path>` outlines first so the photo crop survives translation.
- ❌ Do not use `<mask>` or `mask="url(#...)"` for the typographic reveal; use `clipPath` applied directly to the `<image>`.
- ❌ Do not use `<pattern>` fills inside text to fake the image fill; pattern fills are not reliable in this pipeline.
- ❌ Do not apply `clip-path` to a `<g>`, `<path>`, or `<text>` element; for this workflow, apply it directly to the `<image>`.
- ❌ Avoid thin fonts for the number; the effect needs ultra-bold geometry with enough interior area for the photo to be legible.

## Composition notes
- Keep the masked number oversized and left-weighted, occupying roughly 45–50% of the slide width; it should feel like the hero object, not a label.
- Use a dark, flat background so the clipped image and accent color carry the visual energy.
- Place the divider just right of the number, then align all text to that divider for a clean editorial grid.
- Repeat the accent color sparingly: one vertical divider, one title highlight, and one small lower rhythm bar are enough.