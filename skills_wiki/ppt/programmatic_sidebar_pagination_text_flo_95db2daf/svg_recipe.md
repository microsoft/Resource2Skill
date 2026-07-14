# SVG Recipe — Programmatic Sidebar Pagination & Text Flow

## Visual mechanism
A persistent left sidebar anchors every generated page while the right content pane receives the next chunk of overflowing text. The slide feels continuous because the title, divider, palette, page counter, and layout remain fixed while only the body copy advances with a “continued” cue.

## SVG primitives needed
- 3× `<rect>` for the white sidebar, peach reading pane, and coral divider band/accent blocks
- 2× `<linearGradient>` for the warm content background and coral sidebar accent
- 1× `<filter id="softShadow">` applied to cards and labels for premium depth
- 1× `<filter id="textShadow">` applied to the large sidebar title for subtle emphasis
- 1× `<path>` for a decorative page-flow ribbon behind the body text
- 4× `<circle>` for sidebar pagination dots / progress indicators
- Multiple `<text>` elements with explicit `width` attributes for the sidebar title, continuation label, body paragraphs, page counter, and footer metadata
- 1× `<line>` for a simple non-arrow connector between pagination dots

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="panePeach" x1="384" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFF5F0"/>
      <stop offset="0.58" stop-color="#FDEBE3"/>
      <stop offset="1" stop-color="#F9D8CA"/>
    </linearGradient>
    <linearGradient id="coralGrad" x1="0" y1="0" x2="0" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#F28B4B"/>
      <stop offset="1" stop-color="#D84E25"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="textShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feOffset dx="2" dy="3"/>
      <feGaussianBlur stdDeviation="2"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- fixed template background -->
  <rect x="0" y="0" width="384" height="720" fill="#FFFFFF"/>
  <rect x="384" y="0" width="896" height="720" fill="url(#panePeach)"/>
  <rect x="381" y="0" width="6" height="720" fill="#ED7D31"/>
  <rect x="0" y="0" width="384" height="72" fill="url(#coralGrad)"/>
  <rect x="0" y="648" width="384" height="72" fill="#FFF6F2"/>

  <!-- subtle flow ribbon in content area -->
  <path d="M477 122 C620 67 782 124 920 92 C1058 60 1184 66 1280 104 L1280 204 C1165 168 1062 178 933 218 C774 268 637 188 477 246 Z"
        fill="#F4A07B" opacity="0.16"/>
  <path d="M475 611 C635 560 757 618 910 586 C1070 553 1179 563 1280 602 L1280 720 L475 720 Z"
        fill="#ED7D31" opacity="0.08"/>

  <!-- sidebar title block -->
  <text x="48" y="118" width="286" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="34" font-weight="700" fill="#ED7D31" filter="url(#textShadow)">
    <tspan x="48" dy="0">AutoFit</tspan>
    <tspan x="48" dy="43">Options:</tspan>
    <tspan x="48" dy="56" font-size="46" fill="#111111">Split Text</tspan>
  </text>

  <text x="50" y="312" width="265" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="600" fill="#7A7A7A">
    <tspan x="50" dy="0">Programmatic text flow</tspan>
    <tspan x="50" dy="27">across generated slides</tspan>
  </text>

  <!-- continued badge -->
  <rect x="48" y="384" width="208" height="48" rx="24" fill="#FFF0E9" stroke="#ED7D31" stroke-width="2"/>
  <text x="72" y="415" width="160" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="19" font-weight="700" fill="#D95D27">
    <tspan x="72" dy="0">(Cont.) Page 2</tspan>
  </text>

  <!-- sidebar progress dots -->
  <line x1="70" y1="508" x2="70" y2="598" stroke="#E7B49F" stroke-width="3"/>
  <circle cx="70" cy="508" r="10" fill="#ED7D31"/>
  <circle cx="70" cy="538" r="8" fill="#ED7D31" opacity="0.9"/>
  <circle cx="70" cy="568" r="8" fill="#F5B08D"/>
  <circle cx="70" cy="598" r="8" fill="#F5B08D"/>
  <text x="95" y="514" width="190" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" fill="#8B8B8B">
    <tspan x="95" dy="0">4-slide overflow set</tspan>
    <tspan x="95" dy="25">current chunk highlighted</tspan>
  </text>

  <text x="48" y="684" width="280" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" fill="#909090">
    <tspan x="48" dy="0">Slide 2 / 4 · generated layout</tspan>
  </text>

  <!-- content card -->
  <rect x="456" y="86" width="744" height="548" rx="28" fill="#FFFFFF" opacity="0.86" filter="url(#softShadow)"/>
  <rect x="456" y="86" width="744" height="12" rx="6" fill="#ED7D31"/>

  <text x="504" y="142" width="650" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="23" font-weight="700" fill="#0F70B7">
    <tspan x="504" dy="0">Overflow text continues here</tspan>
  </text>

  <text x="504" y="195" width="632" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" fill="#0070C0">
    <tspan x="504" dy="0">5. PowerPoint creates a new slide with the same visual</tspan>
    <tspan x="504" dy="31">template, then divides the remaining text into a fresh</tspan>
    <tspan x="504" dy="31">reading area so the audience never sees compressed copy.</tspan>

    <tspan x="504" dy="58">6. The sidebar stays locked: title, divider, progress dots,</tspan>
    <tspan x="504" dy="31">and page metadata repeat in exactly the same position.</tspan>

    <tspan x="504" dy="58">7. Body paragraphs are chunked before rendering. Use a</tspan>
    <tspan x="504" dy="31">conservative character budget per slide, then split only</tspan>
    <tspan x="504" dy="31">between paragraphs or list items whenever possible.</tspan>

    <tspan x="504" dy="58">8. The result mimics native AutoFit “split text between</tspan>
    <tspan x="504" dy="31">slides” while preserving a polished executive layout.</tspan>
  </text>

  <!-- bottom continuation cue -->
  <rect x="930" y="594" width="222" height="40" rx="20" fill="#FFF3ED" stroke="#ED7D31" stroke-width="1.5"/>
  <text x="956" y="620" width="170" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" fill="#D95D27">
    <tspan x="956" dy="0">continues on next slide</tspan>
  </text>

  <!-- small page-corner accent -->
  <path d="M1152 86 L1200 86 L1200 134 Z" fill="#F7C7B3"/>
  <path d="M1152 86 L1200 134 L1152 134 Z" fill="#EFA283"/>
</svg>
```

## Avoid in this skill
- ❌ Relying on PowerPoint text autofit to solve overflow; instead, pre-chunk the text and render each chunk into the same fixed text box.
- ❌ Letting the title or sidebar shift between generated slides; tiny layout drift breaks the “continuous pagination” illusion.
- ❌ Using one giant `<text>` element without manual line planning when the content is dynamic; preserve paragraph boundaries and predictable line lengths.
- ❌ Using masks or clipped non-image shapes for the divider/pane split; simple editable rectangles are more reliable and easier to revise.

## Composition notes
- Keep the sidebar at roughly 30% of the canvas width and the content pane at 70%; this gives the title a stable anchor while leaving generous reading space.
- Use the coral divider as the visual hinge between the template and the flowing text area.
- Body copy should sit inside a soft white card with wide padding; avoid filling the peach pane edge-to-edge with text.
- Make continuation explicit with “(Cont.)”, page counters, or progress dots so automated slide splits feel intentional rather than accidental.