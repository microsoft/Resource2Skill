# SVG Recipe — Desktop Publishing (DTP) Grid Canvas

## Visual mechanism
A standard 16:9 slide is treated as a print-production canvas: two white “pages” sit on a neutral pasteboard, each governed by strict margins, columns, gutters, header/footer bands, figure blocks, captions, and callouts. The effect communicates precision through visible alignment, restrained typography, and repeated page furniture.

## SVG primitives needed
- 1× `<rect>` for the neutral pasteboard background
- 2× `<rect>` for editable white page surfaces with subtle shadow
- 1× `<rect>` for the center spine / fold
- 8× `<rect>` for margin boxes, column guide fills, header bands, footer rules, and editorial callout blocks
- 1× `<image>` clipped to a rounded rectangle for an editorial figure/photo block
- 1× `<clipPath>` using rounded `<rect>` for the figure crop
- 1× `<filter id="pageShadow">` using `feOffset + feGaussianBlur + feMerge` for page depth
- 1× `<linearGradient>` for the header accent band
- Multiple `<line>` elements for baseline grid, column dividers, footer rules, and crop-mark-like guide details
- Multiple `<text>` elements with explicit `width` for title, running headers, body columns, captions, callouts, folios, and grid labels
- 2× `<path>` for decorative red editorial tabs / section markers

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="headerGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#2B2F36"/>
      <stop offset="72%" stop-color="#454B55"/>
      <stop offset="100%" stop-color="#C6282D"/>
    </linearGradient>
    <filter id="pageShadow" x="-10%" y="-10%" width="120%" height="125%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <clipPath id="figureCrop">
      <rect x="688" y="188" width="448" height="178" rx="14" ry="14"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#ECEFF3"/>
  <text x="48" y="34" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#76808C" letter-spacing="1.2">DTP GRID CANVAS · 11 × 8.5 TWO-PAGE SPREAD</text>

  <rect x="96" y="40" width="544" height="640" rx="3" fill="#FFFFFF" filter="url(#pageShadow)"/>
  <rect x="640" y="40" width="544" height="640" rx="3" fill="#FFFFFF" filter="url(#pageShadow)"/>
  <rect x="635" y="58" width="10" height="604" fill="#D4D8DE"/>
  <line x1="640" y1="58" x2="640" y2="662" stroke="#AEB5BF" stroke-width="1"/>

  <rect x="144" y="88" width="448" height="42" fill="url(#headerGrad)"/>
  <rect x="688" y="88" width="448" height="42" fill="url(#headerGrad)"/>
  <path d="M120 88 L144 88 L144 156 L120 142 Z" fill="#C6282D"/>
  <path d="M1160 88 L1136 88 L1136 156 L1160 142 Z" fill="#C6282D"/>

  <text x="164" y="115" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF">04 · Advanced Multimedia</text>
  <text x="928" y="115" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF" text-anchor="end">Production Notes</text>

  <rect x="144" y="154" width="448" height="468" fill="none" stroke="#6BAED6" stroke-width="1" stroke-dasharray="5 5" opacity="0.45"/>
  <rect x="688" y="154" width="448" height="468" fill="none" stroke="#6BAED6" stroke-width="1" stroke-dasharray="5 5" opacity="0.45"/>
  <rect x="144" y="154" width="214" height="468" fill="#EAF5FB" opacity="0.22"/>
  <rect x="378" y="154" width="214" height="468" fill="#EAF5FB" opacity="0.22"/>
  <rect x="688" y="154" width="214" height="468" fill="#EAF5FB" opacity="0.22"/>
  <rect x="922" y="154" width="214" height="468" fill="#EAF5FB" opacity="0.22"/>

  <line x1="368" y1="154" x2="368" y2="622" stroke="#78AFCB" stroke-width="1" stroke-dasharray="3 6" opacity="0.55"/>
  <line x1="912" y1="154" x2="912" y2="622" stroke="#78AFCB" stroke-width="1" stroke-dasharray="3 6" opacity="0.55"/>
  <line x1="144" y1="622" x2="592" y2="622" stroke="#D0D5DB" stroke-width="1"/>
  <line x1="688" y1="622" x2="1136" y2="622" stroke="#D0D5DB" stroke-width="1"/>

  <text x="144" y="172" width="214" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800" fill="#242933">
    <tspan x="144" dy="0">Why absolute</tspan>
    <tspan x="144" dy="29">positioning wins</tspan>
  </text>
  <text x="144" y="236" width="214" font-family="Segoe UI, Microsoft YaHei" font-size="11.5" fill="#30343B">
    <tspan x="144" dy="0">PowerPoint becomes a precise page</tspan>
    <tspan x="144" dy="17">layout system when the slide is</tspan>
    <tspan x="144" dy="17">treated as a fixed print canvas.</tspan>
    <tspan x="144" dy="17">Instead of flowing content around</tspan>
    <tspan x="144" dy="17">objects, every title, caption, sidebar,</tspan>
    <tspan x="144" dy="17">and figure is locked to a deliberate</tspan>
    <tspan x="144" dy="17">column coordinate.</tspan>
  </text>

  <text x="378" y="172" width="214" font-family="Segoe UI, Microsoft YaHei" font-size="11.5" fill="#30343B">
    <tspan x="378" dy="0">This grid uses half-inch margins,</tspan>
    <tspan x="378" dy="17">two equal text columns per page,</tspan>
    <tspan x="378" dy="17">and a narrow gutter that creates</tspan>
    <tspan x="378" dy="17">repeatable rhythm. The header band</tspan>
    <tspan x="378" dy="17">acts like a magazine running head,</tspan>
    <tspan x="378" dy="17">while the footer rule reserves space</tspan>
    <tspan x="378" dy="17">for folios and section metadata.</tspan>
  </text>

  <rect x="144" y="390" width="448" height="92" rx="10" fill="#FFF5E8" stroke="#E6B56A"/>
  <text x="164" y="416" width="408" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#9B5410">GRID TIP</text>
  <text x="164" y="442" width="408" font-family="Segoe UI, Microsoft YaHei" font-size="11.5" fill="#5A3A15">
    <tspan x="164" dy="0">Keep guide rectangles visible while designing, then recolor them</tspan>
    <tspan x="164" dy="16">to white or remove them before PDF export. The layout will still</tspan>
    <tspan x="164" dy="16">feel structured because every object shares the same measurements.</tspan>
  </text>

  <image href="https://images.example.com/dtp-editorial-layout-desk-with-print-proofs.jpg" x="688" y="188" width="448" height="178" preserveAspectRatio="xMidYMid slice" clip-path="url(#figureCrop)"/>
  <rect x="688" y="374" width="448" height="42" fill="#F2F4F7"/>
  <text x="704" y="399" width="416" font-family="Segoe UI, Microsoft YaHei" font-size="10.5" fill="#59616D">Figure 4.2 — A photo or diagram can span both columns while remaining locked to the same margin grid.</text>

  <text x="688" y="456" width="214" font-family="Segoe UI, Microsoft YaHei" font-size="11.5" fill="#30343B">
    <tspan x="688" dy="0">Large assets behave like anchored</tspan>
    <tspan x="688" dy="17">editorial blocks. They may span a</tspan>
    <tspan x="688" dy="17">full page width, sit inside one column,</tspan>
    <tspan x="688" dy="17">or interrupt the reading flow with a</tspan>
    <tspan x="688" dy="17">caption directly beneath the crop.</tspan>
  </text>
  <text x="922" y="456" width="214" font-family="Segoe UI, Microsoft YaHei" font-size="11.5" fill="#30343B">
    <tspan x="922" dy="0">Because the page is absolute, callouts</tspan>
    <tspan x="922" dy="17">and figures do not drift when text is</tspan>
    <tspan x="922" dy="17">edited. Use separate text boxes for</tspan>
    <tspan x="922" dy="17">each column to simulate professional</tspan>
    <tspan x="922" dy="17">multi-column composition.</tspan>
  </text>

  <text x="144" y="648" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#7A828C">Chapter 4 · Desktop Publishing in PowerPoint</text>
  <text x="572" y="648" width="20" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#7A828C" text-anchor="end">18</text>
  <text x="688" y="648" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#7A828C">Manual Design System</text>
  <text x="1136" y="648" width="20" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#7A828C" text-anchor="end">19</text>

  <text x="100" y="702" width="1080" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#8B949E">
    Blue dashed boxes show the editable DTP grid: margins, two-column text frames, gutter, image span, header/footer furniture, and page spine.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Native text columns or automatic text flow; use separate positioned `<text>` boxes for each column so the layout remains predictable.
- ❌ Applying `clip-path` to rectangles or text for guide effects; clipping is only reliable here for the `<image>` crop.
- ❌ Overly dense body copy in one giant text object; split columns, captions, headers, and callouts into discrete editable text blocks.
- ❌ Filtered `<line>` grid guides; use simple dashed strokes because line filters are dropped.
- ❌ Decorative elements that ignore the grid; tabs, callouts, and images should snap to margin, column, gutter, or baseline coordinates.

## Composition notes
- Treat the 1280×720 slide as a pasteboard with two page rectangles centered inside it; the pages are the visual focus, not the full slide.
- Use strong page furniture: header bands, footer rules, folios, running heads, and a center spine immediately signal “publication” rather than “slide.”
- Keep guide lines faint blue/gray so they explain the structure without overpowering the document content.
- Reserve full-width blocks for figures and callouts; they should intentionally interrupt the columns while still aligning to the same margins.