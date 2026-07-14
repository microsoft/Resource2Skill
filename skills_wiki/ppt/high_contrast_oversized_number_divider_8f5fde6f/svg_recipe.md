# SVG Recipe — High-Contrast Oversized Number Divider

## Visual mechanism
A hard vertical accent panel occupies the left quarter of the slide and contains an oversized, ultra-bold number in the background color. The remaining dark field carries a concise statement in large two-tone typography, using the same accent color to create rhythm and hierarchy.

## SVG primitives needed
- 2× `<rect>` for the full-slide dark background and the bright left number panel
- 1× `<path>` for a small angled accent bite at the panel edge, adding executive keynote polish while preserving the flat aesthetic
- 1× `<line>` for a crisp vertical divider seam between panel and content field
- 1× `<text>` for the oversized anchor number
- 1× `<text>` for a rotated section label inside the accent panel
- 1× `<text>` for the small eyebrow label above the headline
- 3× `<text>` for the large multi-line two-tone headline
- 1× `<text>` for a short supporting caption
- 2× `<rect>` for minimalist decorative rules under the headline

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <!-- Palette:
       Deep navy: #172B3D
       Canary yellow: #FDD127
       White: #FFFFFF
       Muted blue-gray: #9FB0BF
  -->

  <!-- Base background -->
  <rect x="0" y="0" width="1280" height="720" fill="#172B3D"/>

  <!-- Left accent number panel -->
  <rect x="0" y="0" width="350" height="720" fill="#FDD127"/>

  <!-- Small angular bite to give the divider a designed, keynote-like edge -->
  <path d="M350 0 L392 0 L350 86 Z" fill="#FDD127"/>
  <path d="M350 634 L392 720 L350 720 Z" fill="#FDD127"/>

  <!-- Clean seam line -->
  <line x1="350" y1="0" x2="350" y2="720" stroke="#172B3D" stroke-width="2"/>

  <!-- Rotated metadata label in the number column -->
  <text
    x="-628"
    y="56"
    width="560"
    transform="rotate(-90)"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="15"
    font-weight="700"
    letter-spacing="4"
    fill="#172B3D"
    opacity="0.72">
    STRATEGIC PRINCIPLE
  </text>

  <!-- Oversized anchor number -->
  <text
    x="175"
    y="382"
    width="350"
    text-anchor="middle"
    dominant-baseline="middle"
    font-family="Arial Black, Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif"
    font-size="285"
    font-weight="900"
    fill="#172B3D">
    5
  </text>

  <!-- Small counter mark -->
  <text
    x="84"
    y="626"
    width="200"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="18"
    font-weight="800"
    letter-spacing="2"
    fill="#172B3D">
    / TOP TEN
  </text>

  <!-- Right content area -->
  <text
    x="455"
    y="164"
    width="690"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="18"
    font-weight="800"
    letter-spacing="3"
    fill="#FDD127">
    PRODUCTIVITY PLAYBOOK
  </text>

  <!-- Headline, separated into editable text blocks for reliable PPT rendering -->
  <text
    x="455"
    y="276"
    width="760"
    font-family="Arial Black, Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif"
    font-size="66"
    font-weight="900"
    fill="#FDD127">
    Give every team
  </text>

  <text
    x="455"
    y="354"
    width="760"
    font-family="Arial Black, Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif"
    font-size="66"
    font-weight="900"
    fill="#FFFFFF">
    access to better
  </text>

  <text
    x="455"
    y="432"
    width="760"
    font-family="Arial Black, Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif"
    font-size="66"
    font-weight="900"
    fill="#FFFFFF">
    reusable templates
  </text>

  <!-- Decorative underline rules echoing the accent panel -->
  <rect x="455" y="482" width="132" height="9" rx="4.5" fill="#FDD127"/>
  <rect x="600" y="482" width="54" height="9" rx="4.5" fill="#FFFFFF" opacity="0.28"/>

  <!-- Supporting caption -->
  <text
    x="455"
    y="552"
    width="630"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="25"
    font-weight="500"
    fill="#9FB0BF">
    Replace long bullet lists with one memorable, numbered statement per slide.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Gradients, glows, or shadows; the power of this pattern comes from flat, hard contrast.
- ❌ Centering the headline in the dark field; keep it left-aligned to contrast with the centered number.
- ❌ Making the side panel too narrow; the number must feel oversized, not like a sidebar label.
- ❌ Using many bullets or small annotations; this is a divider / takeaway slide, not a dense dashboard.

## Composition notes
- Reserve roughly 25–30% of the slide width for the accent panel; the number should nearly fill its height and width.
- Place the main statement in the right field with generous left padding, usually starting around x=440–480 on a 1280px canvas.
- Use only two dominant colors plus white: dark background, bright accent, and white text for hierarchy.
- Keep the headline to 2–3 short lines; the oversized number and large typography should be the only visual focus.