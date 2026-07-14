# SVG Recipe — Asymmetric Color-Block Overlap Layout

## Visual mechanism
Layer a large saturated rectangular color block, an offset cropped photograph, and a smaller dark accent square so their corners overlap asymmetrically. Keep the opposite side of the slide mostly white, with disciplined typography and small data callouts aligned to a clean vertical grid.

## SVG primitives needed
- 1× `<rect>` for the white slide background
- 1× large `<rect>` for the primary saturated color block anchoring the composition
- 1× `<image>` clipped by a rectangular `<clipPath>` for the overlapping editorial photo crop
- 1× dark `<rect>` for the secondary accent square overlapping the lower-right corner
- 2× small `<rect>` elements for thin editorial color tabs and alignment accents
- 3× `<line>` elements for typographic separators and right-side structure
- 3× `<path>` elements for small geometric arrow/corner decorations
- 8× `<text>` elements with explicit `width` for title, subtitle, watermark, section labels, metrics, and body copy
- 3× small `<rect>` bars for simple editable chart/data accents on the text side

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="photoCrop">
      <rect x="70" y="82" width="510" height="360"/>
    </clipPath>
  </defs>

  <!-- white breathing-space background -->
  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <!-- asymmetric graphic cluster: base color block -->
  <rect x="150" y="200" width="455" height="405" fill="#D80032"/>

  <!-- thin editorial tab peeking out behind the photo -->
  <rect x="92" y="58" width="118" height="24" fill="#002B5B"/>

  <!-- cropped hero image overlapping top-left of primary block -->
  <image
    href="https://images.unsplash.com/photo-1441986300917-64674bd600d8?auto=format&amp;fit=crop&amp;q=85&amp;w=1200&amp;h=850"
    x="70" y="82" width="510" height="360"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#photoCrop)"/>

  <!-- white registration corner to emphasize flat layered edges -->
  <path d="M70 82 L132 82 L132 94 L82 94 L82 144 L70 144 Z" fill="#FFFFFF"/>

  <!-- primary block decorative watermark text -->
  <text x="174" y="552" width="330"
        font-family="Georgia, 'Times New Roman', serif"
        font-size="28" font-style="italic" fill="#FFFFFF" opacity="0.92">
    Company Identity
  </text>

  <!-- secondary accent block overlapping bottom-right -->
  <rect x="545" y="555" width="145" height="145" fill="#002B5B"/>

  <!-- small glyph inside accent block -->
  <path d="M585 611 L622 611 L622 596 L652 628 L622 660 L622 644 L585 644 Z" fill="#FFFFFF"/>
  <text x="575" y="684" width="88"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" fill="#FFFFFF">
    SINCE 2012
  </text>

  <!-- right-side typography field -->
  <text x="735" y="126" width="425"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="62" font-weight="800" fill="#111111">
    ABOUT US
  </text>

  <line x1="735" y1="162" x2="1035" y2="162" stroke="#D80032" stroke-width="8"/>
  <line x1="735" y1="181" x2="1160" y2="181" stroke="#D9DEE8" stroke-width="1"/>

  <text x="735" y="228" width="420"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="700" fill="#002B5B">
    BUILDING BRANDS THROUGH STRUCTURE, COLOR, AND CLEAR COMMERCIAL THINKING
  </text>

  <text x="735" y="278" width="420"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" fill="#5E6673">
    <tspan x="735" dy="0">We combine strategic research, visual systems, and</tspan>
    <tspan x="735" dy="28">operational design to help teams communicate with</tspan>
    <tspan x="735" dy="28">confidence across markets, launches, and investor moments.</tspan>
  </text>

  <!-- compact data callouts aligned to the text grid -->
  <text x="735" y="408" width="120"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="42" font-weight="800" fill="#111111">
    48
  </text>
  <text x="790" y="408" width="190"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="700" fill="#002B5B">
    MARKETS SERVED
  </text>
  <rect x="735" y="428" width="210" height="8" fill="#EDF0F5"/>
  <rect x="735" y="428" width="162" height="8" fill="#D80032"/>

  <text x="735" y="500" width="120"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="42" font-weight="800" fill="#111111">
    92%
  </text>
  <text x="840" y="500" width="230"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="700" fill="#002B5B">
    RETENTION ACROSS KEY ACCOUNTS
  </text>
  <rect x="735" y="520" width="300" height="8" fill="#EDF0F5"/>
  <rect x="735" y="520" width="276" height="8" fill="#002B5B"/>

  <line x1="735" y1="585" x2="1138" y2="585" stroke="#D9DEE8" stroke-width="1"/>

  <text x="735" y="630" width="360"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" fill="#747C89">
    <tspan x="735" dy="0">Use this layout as a section opener, company profile,</tspan>
    <tspan x="735" dy="24">or executive story slide where a strong editorial image</tspan>
    <tspan x="735" dy="24">must coexist with concise performance evidence.</tspan>
  </text>

  <!-- small color rhythm detail on far right -->
  <rect x="1172" y="112" width="18" height="72" fill="#002B5B"/>
  <rect x="1197" y="112" width="18" height="42" fill="#D80032"/>
  <path d="M1152 612 L1180 612 L1180 640 L1152 640 Z M1188 612 L1216 612 L1216 640 L1188 640 Z" fill="#D80032"/>
</svg>
```

## Avoid in this skill
- ❌ Drop shadows or heavy glow filters; this technique depends on flat, confident overlap rather than soft depth.
- ❌ Centering the photo exactly on the color block; the layout should feel intentionally offset and editorial.
- ❌ Clipping color blocks or text with `clip-path`; keep clipping only on the `<image>` for reliable PowerPoint translation.
- ❌ Using many equally sized blocks; one dominant block, one photo, and one accent square should carry the hierarchy.
- ❌ Distorting the photo to fit the rectangle; use `preserveAspectRatio="xMidYMid slice"` with an image clip.

## Composition notes
- Keep the layered graphic cluster on the left 45–50% of the slide, with the photo shifted up and left from the primary block.
- Reserve the right 40% as clean white space for title, short narrative, and compact data callouts.
- Let the primary color block remain visibly exposed on the bottom and right edges to frame the image.
- Repeat the primary and secondary colors sparingly in rules, bars, and small tabs so the text side echoes the visual cluster without becoming busy.