# SVG Recipe — Split-Pane Employee Spotlight

## Visual mechanism
A premium editorial profile slide built from a strict asymmetrical vertical split: the left third anchors identity with a portrait, nameplate, title, and quote, while the right two-thirds carry structured Q&A content. Bright circular number badges create a strong vertical reading rhythm across the data-heavy pane.

## SVG primitives needed
- 2× <rect> for the left slate pane and white right content pane
- 1× <image> for the employee portrait, cropped inside the left pane
- 1× <clipPath> with rounded <rect> for the portrait crop
- 1× <linearGradient> for a soft portrait-to-background fade overlay
- 1× <rect> using the fade gradient to blend the bottom of the portrait into the left pane
- 1× <rect> for the dark navy nameplate banner
- 1× <filter id="cardShadow"> with feOffset + feGaussianBlur + feMerge for subtle elevation
- 5× <circle> for numbered Q&A badges
- 5× <line> for light dividers between Q&A items
- 14× <text> for name, role, quote, section label, badge numbers, questions, and answers
- 2× <path> for decorative editorial accent shapes in the left pane

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="portraitFade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#E3E8EC" stop-opacity="0"/>
      <stop offset="55%" stop-color="#E3E8EC" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#E3E8EC" stop-opacity="1"/>
    </linearGradient>

    <linearGradient id="leftGlow" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F4F7F9"/>
      <stop offset="100%" stop-color="#D8E0E6"/>
    </linearGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="6" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="portraitClip">
      <rect x="52" y="34" width="340" height="430" rx="28" ry="28"/>
    </clipPath>
  </defs>

  <!-- Split background -->
  <rect x="0" y="0" width="440" height="720" fill="url(#leftGlow)"/>
  <rect x="440" y="0" width="840" height="720" fill="#FFFFFF"/>

  <!-- Editorial accents in the left pane -->
  <path d="M-80,138 C60,56 160,68 250,122 C344,178 398,126 466,64 L466,0 L-80,0 Z"
        fill="#CAD5DD" opacity="0.45"/>
  <path d="M52,616 C132,572 214,594 278,640 C338,684 390,690 440,660 L440,720 L52,720 Z"
        fill="#5C9EAD" opacity="0.13"/>

  <!-- Portrait -->
  <image href="https://images.example.com/employee-portrait-confident-procurement-manager.jpg"
         x="52" y="34" width="340" height="430"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#portraitClip)"/>
  <rect x="52" y="318" width="340" height="146" fill="url(#portraitFade)"/>

  <!-- Nameplate -->
  <rect x="0" y="464" width="440" height="104" fill="#2C3E50" filter="url(#cardShadow)"/>
  <text x="36" y="520" width="368"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="39" font-weight="800" letter-spacing="2.5"
        fill="#FFFFFF">MEL STEAD</text>

  <!-- Role and quote -->
  <text x="36" y="606" width="368"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="25" font-weight="700"
        fill="#2C3E50">Procurement Manager</text>
  <text x="36" y="650" width="354"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-style="italic"
        fill="#3B4C5C">
    <tspan x="36" dy="0">“I innovate on walking the fine line</tspan>
    <tspan x="36" dy="24">between lean inventory and never</tspan>
    <tspan x="36" dy="24">stocking out.”</tspan>
  </text>

  <!-- Right pane header -->
  <text x="505" y="76" width="620"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="800" letter-spacing="2"
        fill="#5C9EAD">EMPLOYEE SPOTLIGHT</text>
  <text x="505" y="116" width="640"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="31" font-weight="700"
        fill="#2C3E50">Five things to know about Mel</text>

  <!-- Q&A item 1 -->
  <circle cx="530" cy="184" r="27" fill="#5C9EAD"/>
  <text x="516" y="194" width="28"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="25" font-weight="800" text-anchor="middle"
        fill="#FFFFFF">1</text>
  <text x="585" y="169" width="610"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="21" font-weight="800"
        fill="#5C9EAD">List five hashtags that describe your personality.</text>
  <text x="585" y="203" width="610"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18"
        fill="#333333">#bakingsnob  #ancienthistory  #dryhumor  #supplychainnerd  #curious</text>
  <line x1="585" y1="238" x2="1194" y2="238" stroke="#E4E9ED" stroke-width="2"/>

  <!-- Q&A item 2 -->
  <circle cx="530" cy="286" r="27" fill="#5C9EAD"/>
  <text x="516" y="296" width="28"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="25" font-weight="800" text-anchor="middle"
        fill="#FFFFFF">2</text>
  <text x="585" y="271" width="610"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="21" font-weight="800"
        fill="#5C9EAD">If you could vacation anywhere, where would you go?</text>
  <text x="585" y="305" width="610"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18"
        fill="#333333">Norway — fjords, cold air, long hikes, and zero email.</text>
  <line x1="585" y1="340" x2="1194" y2="340" stroke="#E4E9ED" stroke-width="2"/>

  <!-- Q&A item 3 -->
  <circle cx="530" cy="388" r="27" fill="#5C9EAD"/>
  <text x="516" y="398" width="28"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="25" font-weight="800" text-anchor="middle"
        fill="#FFFFFF">3</text>
  <text x="585" y="373" width="610"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="21" font-weight="800"
        fill="#5C9EAD">What is your favorite part about working here?</text>
  <text x="585" y="407" width="610"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18"
        fill="#333333">Working with smart, generous people who can solve hard problems and still laugh.</text>
  <line x1="585" y1="442" x2="1194" y2="442" stroke="#E4E9ED" stroke-width="2"/>

  <!-- Q&A item 4 -->
  <circle cx="530" cy="490" r="27" fill="#5C9EAD"/>
  <text x="516" y="500" width="28"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="25" font-weight="800" text-anchor="middle"
        fill="#FFFFFF">4</text>
  <text x="585" y="475" width="610"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="21" font-weight="800"
        fill="#5C9EAD">Outside of work, what activity can we find you doing?</text>
  <text x="585" y="509" width="610"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18"
        fill="#333333">Baking, reading about baking, and testing oddly specific kitchen gadgets.</text>
  <line x1="585" y1="544" x2="1194" y2="544" stroke="#E4E9ED" stroke-width="2"/>

  <!-- Q&A item 5 -->
  <circle cx="530" cy="592" r="27" fill="#5C9EAD"/>
  <text x="516" y="602" width="28"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="25" font-weight="800" text-anchor="middle"
        fill="#FFFFFF">5</text>
  <text x="585" y="577" width="610"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="21" font-weight="800"
        fill="#5C9EAD">Apple or Android?</text>
  <text x="585" y="611" width="610"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18"
        fill="#333333">Apple — unless the music app breaks the Sonos setup again.</text>
</svg>
```

## Avoid in this skill
- ❌ Using <mask> to fade the portrait; instead place a transparent-to-background gradient rectangle above the photo.
- ❌ Cropping the portrait by applying clip-path to a <g> or <rect>; apply clip-path directly to the <image>.
- ❌ Letting the right pane become a generic bullet list; the numbered circular badges are the core visual rhythm.
- ❌ Omitting width attributes on <text>; PowerPoint translation needs explicit text widths for stable wrapping.
- ❌ Over-centering the layout; the left pane should stay visually heavy and the right pane should feel spacious and editorial.

## Composition notes
- Keep the split near 34% / 66%: left pane around 430–450 px wide on a 1280 px canvas, with the right pane starting cleanly at that boundary.
- Use the portrait and navy nameplate as the left-side focal stack; the nameplate should span the full pane width to create a decisive editorial break.
- Align all Q&A text to one vertical column, with badges slightly offset to the left; this creates scanability even when the answers are long.
- Limit the palette to slate, navy, teal, white, and dark gray; repeat teal in both badges and question text for cohesion.