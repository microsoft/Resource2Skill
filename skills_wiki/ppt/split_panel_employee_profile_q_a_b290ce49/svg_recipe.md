# SVG Recipe — Split-Panel Profile with Q&A

## Visual mechanism
A magazine-like split panel pairs a strong employee portrait and identity block on the left with a structured Q&A column on the right. The accent color from the profile panel repeats in numbered circular nodes, creating a clear reading path and cohesive brand rhythm.

## SVG primitives needed
- 4× `<rect>` for slide background, left photo panel, name banner, and right-side color strip
- 1× `<image>` for the employee/profile photo, clipped to the upper-left panel
- 1× `<clipPath>` with `<rect>` for the photo crop
- 1× `<linearGradient>` for the teal profile/accent background
- 1× `<radialGradient>` for dimensional numbered circles
- 1× `<filter id="softShadow">` applied to number nodes and name banner
- 5× `<circle>` for Q&A number nodes
- 12× `<text>` groups for logo, name/title/quote, numbered labels, questions, and answers
- Optional decorative `<path>` for a subtle curved highlight over the portrait panel

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="tealPanel" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#6FAFC1"/>
      <stop offset="58%" stop-color="#5EA3B7"/>
      <stop offset="100%" stop-color="#4F95A9"/>
    </linearGradient>

    <linearGradient id="photoTint" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#7BB6C7" stop-opacity="0.48"/>
      <stop offset="100%" stop-color="#3F879D" stop-opacity="0.25"/>
    </linearGradient>

    <radialGradient id="nodeFill" cx="35%" cy="28%" r="75%">
      <stop offset="0%" stop-color="#6FB0C2"/>
      <stop offset="72%" stop-color="#3F819A"/>
      <stop offset="100%" stop-color="#2E607A"/>
    </radialGradient>

    <filter id="softShadow" x="-25%" y="-25%" width="150%" height="150%">
      <feOffset dx="0" dy="3" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="photoCrop">
      <rect x="0" y="0" width="452" height="426"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>
  <rect x="0" y="0" width="452" height="720" fill="url(#tealPanel)"/>
  <rect x="1242" y="0" width="38" height="720" fill="#5D9FB1"/>

  <image x="0" y="0" width="452" height="426"
         href="https://images.example.com/profile-photo-warehouse-team-member-on-blue-background.jpg"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#photoCrop)"/>
  <rect x="0" y="0" width="452" height="426" fill="url(#photoTint)"/>

  <path d="M-30,372 C92,330 246,343 482,274 L482,426 L-30,426 Z"
        fill="#2E7288" opacity="0.18"/>

  <text x="17" y="54" width="96" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="35" font-weight="800" fill="#FFFFFF" letter-spacing="-2">POS</text>
  <text x="17" y="112" width="112" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="700" fill="#FFFFFF" letter-spacing="7">PORTAL</text>
  <rect x="16" y="28" width="86" height="24" fill="#FFFFFF" opacity="0.95"/>

  <rect x="0" y="426" width="452" height="61" fill="#48536E" filter="url(#softShadow)"/>
  <text x="17" y="468" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="39" font-weight="400" fill="#FFFFFF" letter-spacing="1">RAFAELA GUTIERREZ</text>

  <text x="52" y="535" width="348" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="27" font-weight="700" fill="#FFFFFF">
    <tspan x="226">Receiving Clerk</tspan>
  </text>

  <text x="40" y="578" width="372" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="27" font-style="italic" fill="#EAF6F8">
    <tspan x="226">“I am responsible for the</tspan>
    <tspan x="226" dy="31">receipt, verification and recording</tspan>
    <tspan x="226" dy="31">of products that come into</tspan>
    <tspan x="226" dy="31">the warehouse.”</tspan>
  </text>

  <circle cx="520" cy="88" r="36" fill="url(#nodeFill)" filter="url(#softShadow)"/>
  <text x="504" y="101" width="32" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="34" fill="#FFFFFF" text-anchor="middle">1</text>
  <text x="582" y="78" width="610" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="26" fill="#2F8196">
    <tspan x="582">List five hashtags that describe your personality.</tspan>
  </text>
  <text x="582" y="111" width="610" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="26" fill="#4A4A4A">
    <tspan x="582">#friendly #lovemyfamily #ontime #honest</tspan>
    <tspan x="582" dy="32">#TakingcaremyNieces</tspan>
  </text>

  <circle cx="520" cy="226" r="36" fill="url(#nodeFill)" filter="url(#softShadow)"/>
  <text x="504" y="239" width="32" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="34" fill="#FFFFFF" text-anchor="middle">2</text>
  <text x="582" y="217" width="620" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="26" fill="#2F8196">
    <tspan x="582">If you could vacation anywhere in the world, where</tspan>
    <tspan x="582" dy="31">would you go?</tspan>
  </text>
  <text x="582" y="283" width="610" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="26" fill="#4A4A4A">Rome, Italia, or Spain</text>

  <circle cx="520" cy="358" r="36" fill="url(#nodeFill)" filter="url(#softShadow)"/>
  <text x="504" y="371" width="32" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="34" fill="#FFFFFF" text-anchor="middle">3</text>
  <text x="582" y="345" width="620" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="26" fill="#2F8196">
    <tspan x="582">What is your favorite part about working at POS</tspan>
    <tspan x="582" dy="31">Portal?</tspan>
  </text>
  <text x="582" y="414" width="620" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="26" fill="#4A4A4A">I really enjoy assisting and helping others.</text>

  <circle cx="520" cy="490" r="36" fill="url(#nodeFill)" filter="url(#softShadow)"/>
  <text x="504" y="503" width="32" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="34" fill="#FFFFFF" text-anchor="middle">4</text>
  <text x="582" y="480" width="630" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="26" fill="#2F8196">Outside of work, what activity can we find you doing?</text>
  <text x="582" y="514" width="630" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="26" fill="#4A4A4A">
    <tspan x="582">Camping, watching movies at the theater, going to the</tspan>
    <tspan x="582" dy="32">casino, and attending my nephews sports games.</tspan>
  </text>

  <circle cx="520" cy="624" r="36" fill="url(#nodeFill)" filter="url(#softShadow)"/>
  <text x="504" y="637" width="32" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="34" fill="#FFFFFF" text-anchor="middle">5</text>
  <text x="582" y="613" width="610" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="26" fill="#2F8196">Apple or Android?</text>
  <text x="582" y="648" width="610" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="26" fill="#4A4A4A">Apple</text>
</svg>
```

## Avoid in this skill
- ❌ Using a `<mask>` to crop the profile photo; use `<clipPath>` directly on the `<image>` instead.
- ❌ Putting all Q&A content into one giant text box; separate question and answer text elements preserve editability and spacing control.
- ❌ Applying `filter` to connector lines or decorative rules; use filters only on rectangles, circles, paths, and text.
- ❌ Overcrowding the right column with more than five Q&A items unless font size and spacing are deliberately reduced.

## Composition notes
- Keep the left panel at roughly one-third of the slide width; it should feel like a visual identity card, not a sidebar.
- Align all numbered circles on one vertical axis, with question text starting consistently to the right.
- Repeat the left-panel accent color in the number nodes and right-edge strip for a branded editorial feel.
- Use generous white space on the right; the layout works because the dense profile image is balanced by a clean reading field.