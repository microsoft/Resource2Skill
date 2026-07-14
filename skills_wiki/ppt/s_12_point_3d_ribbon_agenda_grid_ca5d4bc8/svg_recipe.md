# SVG Recipe — 12-Point 3D Ribbon Agenda Grid

## Visual mechanism
A dense 12-item agenda is split into a balanced 2-column × 6-row grid of short white cards, each anchored by a vivid left ribbon and circular numbered badge. Depth comes from separate soft shadow shapes behind each card plus a darker offset “fold” sliver that makes the ribbon feel layered.

## SVG primitives needed
- 1× `<rect>` for the full-slide cool gray background.
- 2–3× blurred decorative `<ellipse>` elements for soft frosted background variation.
- 12× blurred shadow `<rect>` elements behind the cards.
- 12× white rounded `<rect>` elements for the agenda card bodies.
- 12× dark accent `<rect>` elements for the faux ribbon fold/back layer.
- 12× colored ribbon `<rect>` elements plus 12× colored `<circle>` elements to create a straight-left, rounded-right tab shape without `<path>`.
- 12× gradient-filled `<circle>` elements for the numbered badges.
- 48× `<text>` elements for STEP labels, numbers, titles/body copy, and simple right-side icon glyphs.

## Safe-subset SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="softBlur"><feGaussianBlur stdDeviation="10"/></filter>
    <linearGradient id="g1" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#ff4b7a"/><stop offset="100%" stop-color="#9b0037"/></linearGradient>
    <linearGradient id="g2" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#ffdf23"/><stop offset="100%" stop-color="#d96000"/></linearGradient>
    <linearGradient id="g3" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#ff8a1a"/><stop offset="100%" stop-color="#c12a16"/></linearGradient>
    <linearGradient id="g4" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#ff3b9a"/><stop offset="100%" stop-color="#7f005f"/></linearGradient>
    <linearGradient id="g5" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#6550e6"/><stop offset="100%" stop-color="#20156f"/></linearGradient>
    <linearGradient id="g6" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#008bea"/><stop offset="100%" stop-color="#003d94"/></linearGradient>
    <linearGradient id="g7" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#39c7f4"/><stop offset="100%" stop-color="#006fa9"/></linearGradient>
    <linearGradient id="g8" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#60d7c9"/><stop offset="100%" stop-color="#00757d"/></linearGradient>
    <linearGradient id="g9" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#5fe13b"/><stop offset="100%" stop-color="#087327"/></linearGradient>
    <linearGradient id="g10" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#c6ef26"/><stop offset="100%" stop-color="#3c9a16"/></linearGradient>
    <linearGradient id="g11" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#ff4b4b"/><stop offset="100%" stop-color="#b50014"/></linearGradient>
    <linearGradient id="g12" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#d24a13"/><stop offset="100%" stop-color="#4a1c00"/></linearGradient>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#eef2f5"/>
  <g filter="url(#softBlur)" opacity="0.35">
    <ellipse cx="260" cy="115" rx="250" ry="90" fill="#ffffff"/>
    <ellipse cx="1020" cy="640" rx="310" ry="120" fill="#d8e5ec"/>
    <ellipse cx="665" cy="365" rx="420" ry="155" fill="#ffffff"/>
  </g>

  <g transform="translate(64 54)">
    <rect x="28" y="17" width="535" height="84" rx="9" fill="#60717a" opacity="0.28" filter="url(#softBlur)"/><rect x="18" y="0" width="54" height="22" rx="3" fill="#9b0037"/><rect x="18" y="13" width="92" height="68" fill="#dd1f54"/><circle cx="110" cy="47" r="34" fill="#dd1f54"/><circle cx="103" cy="47" r="27" fill="url(#g1)"/>
    <text x="38" y="53" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#ffffff">STEP</text><text x="83" y="57" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="800" fill="#ffffff">01</text><rect x="38" y="0" width="535" height="84" rx="9" fill="#ffffff"/><text x="152" y="28" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#3a3a3a">Kickoff · Align objectives and scope</text><text x="515" y="55" width="40" font-family="Segoe UI Symbol, Segoe UI" font-size="30" fill="#c01849">☼</text>
  </g>

  <g transform="translate(64 161)">
    <rect x="28" y="17" width="535" height="84" rx="9" fill="#60717a" opacity="0.26" filter="url(#softBlur)"/><rect x="18" y="0" width="54" height="22" rx="3" fill="#c96a00"/><rect x="18" y="13" width="92" height="68" fill="#ffda16"/><circle cx="110" cy="47" r="34" fill="#ffda16"/><circle cx="103" cy="47" r="27" fill="url(#g2)"/>
    <text x="38" y="53" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#ffffff">STEP</text><text x="83" y="57" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="800" fill="#ffffff">02</text><rect x="38" y="0" width="535" height="84" rx="9" fill="#ffffff"/><text x="152" y="28" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#3a3a3a">Research · Map customer insights</text><text x="515" y="55" width="42" font-family="Segoe UI Symbol, Segoe UI" font-size="30" fill="#d77a15">⌂</text>
  </g>

  <g transform="translate(64 268)">
    <rect x="28" y="17" width="535" height="84" rx="9" fill="#60717a" opacity="0.26" filter="url(#softBlur)"/><rect x="18" y="0" width="54" height="22" rx="3" fill="#bb3214"/><rect x="18" y="13" width="92" height="68" fill="#ff6517"/><circle cx="110" cy="47" r="34" fill="#ff6517"/><circle cx="103" cy="47" r="27" fill="url(#g3)"/>
    <text x="38" y="53" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#ffffff">STEP</text><text x="83" y="57" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="800" fill="#ffffff">03</text><rect x="38" y="0" width="535" height="84" rx="9" fill="#ffffff"/><text x="152" y="28" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#3a3a3a">Prioritize · Select top initiatives</text><text x="515" y="55" width="42" font-family="Segoe UI Symbol, Segoe UI" font-size="30" fill="#dd5b2b">□</text>
  </g>

  <g transform="translate(64 375)">
    <rect x="28" y="17" width="535" height="84" rx="9" fill="#60717a" opacity="0.26" filter="url(#softBlur)"/><rect x="18" y="0" width="54" height="22" rx="3" fill="#7f005f"/><rect x="18" y="13" width="92" height="68" fill="#db228a"/><circle cx="110" cy="47" r="34" fill="#db228a"/><circle cx="103" cy="47" r="27" fill="url(#g4)"/>
    <text x="38" y="53" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#ffffff">STEP</text><text x="83" y="57" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="800" fill="#ffffff">04</text><rect x="38" y="0" width="535" height="84" rx="9" fill="#ffffff"/><text x="152" y="28" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#3a3a3a">Design · Build the solution model</text><text x="515" y="55" width="42" font-family="Segoe UI Symbol, Segoe UI" font-size="30" fill="#bd2b8a">▤</text>
  </g>

  <g transform="translate(64 482)">
    <rect x="28" y="17" width="535" height="84" rx="9" fill="#60717a" opacity="0.26" filter="url(#softBlur)"/><rect x="18" y="0" width="54" height="22" rx="3" fill="#2c227d"/><rect x="18" y="13" width="92" height="68" fill="#5146cf"/><circle cx="110" cy="47" r="34" fill="#5146cf"/><circle cx="103" cy="47" r="27" fill="url(#g5)"/>
    <text x="38" y="53" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#ffffff">STEP</text><text x="83" y="57" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="800" fill="#ffffff">05</text><rect x="38" y="0" width="535" height="84" rx="9" fill="#ffffff"/><text x="152" y="28" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#3a3a3a">Configure · Prepare resources</text><text x="515" y="55" width="42" font-family="Segoe UI Symbol, Segoe UI" font-size="30" fill="#453aa8">⚙</text>
  </g>

  <g transform="translate(64 589)">
    <rect x="28" y="17" width="535" height="84" rx="9" fill="#60717a" opacity="0.26" filter="url(#softBlur)"/><rect x="18" y="0" width="54" height="22" rx="3" fill="#00407f"/><rect x="18" y="13" width="92" height="68" fill="#007ad4"/><circle cx="110" cy="47" r="34" fill="#007ad4"/><circle cx="103" cy="47" r="27" fill="url(#g6)"/>
    <text x="38" y="53" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#ffffff">STEP</text><text x="83" y="57" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="800" fill="#ffffff">06</text><rect x="38" y="0" width="535" height="84" rx="9" fill="#ffffff"/><text x="152" y="28" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#3a3a3a">Validate · Review early metrics</text><text x="515" y="55" width="42" font-family="Segoe UI Symbol, Segoe UI" font-size="30" fill="#126bb0">▥</text>
  </g>

  <g transform="translate(668 54)">
    <rect x="28" y="17" width="535" height="84" rx="9" fill="#60717a" opacity="0.28" filter="url(#softBlur)"/><rect x="18" y="0" width="54" height="22" rx="3" fill="#006fa9"/><rect x="18" y="13" width="92" height="68" fill="#29aee3"/><circle cx="110" cy="47" r="34" fill="#29aee3"/><circle cx="103" cy="47" r="27" fill="url(#g7)"/>
    <text x="38" y="53" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#ffffff">STEP</text><text x="83" y="57" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="800" fill="#ffffff">07</text><rect x="38" y="0" width="535" height="84" rx="9" fill="#ffffff"/><text x="152" y="28" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#3a3a3a">Partner · Confirm handoffs</text><text x="515" y="55" width="42" font-family="Segoe UI Symbol, Segoe UI" font-size="30" fill="#1fa8d7">◇</text>
  </g>

  <g transform="translate(668 161)">
    <rect x="28" y="17" width="535" height="84" rx="9" fill="#60717a" opacity="0.26" filter="url(#softBlur)"/><rect x="18" y="0" width="54" height="22" rx="3" fill="#00757d"/><rect x="18" y="13" width="92" height="68" fill="#55c7bd"/><circle cx="110" cy="47" r="34" fill="#55c7bd"/><circle cx="103" cy="47" r="27" fill="url(#g8)"/>
    <text x="38" y="53" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#ffffff">STEP</text><text x="83" y="57" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="800" fill="#ffffff">08</text><rect x="38" y="0" width="535" height="84" rx="9" fill="#ffffff"/><text x="152" y="28" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#3a3a3a">Benchmark · Compare performance</text><text x="515" y="55" width="42" font-family="Segoe UI Symbol, Segoe UI" font-size="30" fill="#43aeb3">♕</text>
  </g>

  <g transform="translate(668 268)">
    <rect x="28" y="17" width="535" height="84" rx="9" fill="#60717a" opacity="0.26" filter="url(#softBlur)"/><rect x="18" y="0" width="54" height="22" rx="3" fill="#0a7c22"/><rect x="18" y="13" width="92" height="68" fill="#38c929"/><circle cx="110" cy="47" r="34" fill="#38c929"/><circle cx="103" cy="47" r="27" fill="url(#g9)"/>
    <text x="38" y="53" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#ffffff">STEP</text><text x="83" y="57" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="800" fill="#ffffff">09</text><rect x="38" y="0" width="535" height="84" rx="9" fill="#ffffff"/><text x="152" y="28" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#3a3a3a">Budget · Lock investment plan</text><text x="515" y="55" width="42" font-family="Segoe UI Symbol, Segoe UI" font-size="30" fill="#27a83d">▭</text>
  </g>

  <g transform="translate(668 375)">
    <rect x="28" y="17" width="535" height="84" rx="9" fill="#60717a" opacity="0.26" filter="url(#softBlur)"/><rect x="18" y="0" width="54" height="22" rx="3" fill="#4a970f"/><rect x="18" y="13" width="92" height="68" fill="#9bdc18"/><circle cx="110" cy="47" r="34" fill="#9bdc18"/><circle cx="103" cy="47" r="27" fill="url(#g10)"/>
    <text x="38" y="53" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#ffffff">STEP</text><text x="83" y="57" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="800" fill="#ffffff">10</text><rect x="38" y="0" width="535" height="84" rx="9" fill="#ffffff"/><text x="152" y="28" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#3a3a3a">Approve · Finalize decisions</text><text x="515" y="55" width="42" font-family="Segoe UI Symbol, Segoe UI" font-size="30" fill="#72b62c">✉</text>
  </g>

  <g transform="translate(668 482)">
    <rect x="28" y="17" width="535" height="84" rx="9" fill="#60717a" opacity="0.26" filter="url(#softBlur)"/><rect x="18" y="0" width="54" height="22" rx="3" fill="#9a0010"/><rect x="18" y="13" width="92" height="68" fill="#ff353a"/><circle cx="110" cy="47" r="34" fill="#ff353a"/><circle cx="103" cy="47" r="27" fill="url(#g11)"/>
    <text x="38" y="53" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#ffffff">STEP</text><text x="83" y="57" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="800" fill="#ffffff">11</text><rect x="38" y="0" width="535" height="84" rx="9" fill="#ffffff"/><text x="152" y="28" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#3a3a3a">Launch · Communicate rollout</text><text x="515" y="55" width="42" font-family="Segoe UI Symbol, Segoe UI" font-size="30" fill="#e2252f">≋</text>
  </g>

  <g transform="translate(668 589)">
    <rect x="28" y="17" width="535" height="84" rx="9" fill="#60717a" opacity="0.26" filter="url(#softBlur)"/><rect x="18" y="0" width="54" height="22" rx="3" fill="#5a2100"/><rect x="18" y="13" width="92" height="68" fill="#c2410c"/><circle cx="110" cy="47" r="34" fill="#c2410c"/><circle cx="103" cy="47" r="27" fill="url(#g12)"/>
    <text x="38" y="53" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#ffffff">STEP</text><text x="83" y="57" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="800" fill="#ffffff">12</text><rect x="38" y="0" width="535" height="84" rx="9" fill="#ffffff"/><text x="152" y="28" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#3a3a3a">Track · Measure next actions</text><text x="515" y="55" width="42" font-family="Segoe UI Symbol, Segoe UI" font-size="30" fill="#6a2b07">⌖</text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<path>` or `<polygon>` for the ribbon fold triangle; in this safe subset, approximate the fold with a small dark offset rectangle behind the tab.
- ❌ Do not apply blur/filter to groups containing text; keep shadows as separate decorative rectangles so text remains editable in PowerPoint.
- ❌ Do not place a single marker or style on a parent group for arrows; this layout does not need arrows, but if added, every `<line>` must carry its own `marker-end`.
- ❌ Do not rely on auto-sized text frames; every `<text>` element needs an explicit `width` attribute to prevent PowerPoint reflow drift.
- ❌ Do not overfill the cards with paragraph text; the card height is intentionally shallow.

## Composition notes
- Keep the grid symmetrical: two columns with six evenly spaced rows, leaving a narrow central gutter and generous outer margins.
- The strongest visual focus should be the colored tab and numbered badge; keep the white card body clean and low-contrast.
- Use one unique hue per item, but keep all cards identical in size so the palette feels systematic rather than chaotic.
- Shadows should sit behind the white cards, not over the ribbons or text, to preserve the premium paper-layer effect.