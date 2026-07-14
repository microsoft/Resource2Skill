# SVG Recipe — Interactive Accordion Morph (水平手风琴平滑展开交互)

## Visual mechanism
A horizontal accordion is built from narrow vertical color pillars; the “active” chapter expands into a wide image reveal while the other pillars compress to the sides. In PowerPoint, create one SVG-derived slide per state and apply Morph so matching object IDs interpolate their X positions and widths.

## SVG primitives needed
- 1× full-slide `<rect>` for the premium dark gradient background
- 1× decorative `<path>` glow/blob for atmospheric depth
- 1× `<rect>` behind the accordion for a soft floating shadow plane
- 5× `<image>` elements for chapter photos, each clipped to its current reveal area
- 5× `<clipPath>` definitions with `<rect rx>` for photo crops; resize/reposition these per Morph state
- 5× main colored `<rect>` pillars/tabs, with stable `id` values across states
- 1× translucent `<rect>` overlay on the active image for legible text
- 1× `<filter id="softShadow">` applied to the accordion base and active tab
- 1× `<radialGradient>` and 2× `<linearGradient>` definitions for background and image shading
- Multiple `<text>` elements with explicit `width` for title, labels, vertical Chinese chapter names, rotated English captions, numbers, and active-state copy
- 1× `<line>` for a thin header rule

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#111722"/>
      <stop offset="55%" stop-color="#1d2735"/>
      <stop offset="100%" stop-color="#080b10"/>
    </linearGradient>
    <radialGradient id="blueGlow" cx="50%" cy="50%" r="65%">
      <stop offset="0%" stop-color="#6f8eaa" stop-opacity="0.42"/>
      <stop offset="100%" stop-color="#6f8eaa" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="photoShade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#000000" stop-opacity="0.05"/>
      <stop offset="62%" stop-color="#000000" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.62"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="16"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <!-- In a Morph deck, keep these IDs and change x/width per slide state. -->
    <clipPath id="clip_photo_01"><rect x="150" y="145" width="92" height="500" rx="26"/></clipPath>
    <clipPath id="clip_photo_02"><rect x="242" y="145" width="92" height="500" rx="26"/></clipPath>
    <clipPath id="clip_photo_03"><rect x="334" y="145" width="500" height="500" rx="26"/></clipPath>
    <clipPath id="clip_photo_04"><rect x="942" y="145" width="92" height="500" rx="26"/></clipPath>
    <clipPath id="clip_photo_05"><rect x="1034" y="145" width="92" height="500" rx="26"/></clipPath>
  </defs>

  <rect id="slide_background" x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <path id="ambient_glow" d="M900,40 C1085,12 1240,110 1266,260 C1294,420 1160,560 980,540 C820,522 740,410 770,270 C792,170 810,70 900,40 Z" fill="url(#blueGlow)"/>

  <text id="deck_title" x="74" y="70" width="650" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#F3EFE8">Future Mobility Strategy</text>
  <text id="deck_subtitle" x="76" y="104" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="13" letter-spacing="2.2" fill="#AAB5C2">MORPH ACCORDION NAVIGATION / 平滑展开目录</text>
  <line id="header_rule" x1="76" y1="122" x2="430" y2="122" stroke="#AAB5C2" stroke-opacity="0.45" stroke-width="1"/>

  <rect id="accordion_shadow_plate" x="140" y="150" width="996" height="500" rx="30" fill="#000000" opacity="0.24" filter="url(#softShadow)"/>

  <image id="photo_01" href="https://images.unsplash.com/photo-1503376760367-111c1d763321?auto=format&amp;fit=crop&amp;w=1200&amp;q=80" x="150" y="145" width="500" height="500" preserveAspectRatio="xMidYMid slice" clip-path="url(#clip_photo_01)"/>
  <image id="photo_02" href="https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?auto=format&amp;fit=crop&amp;w=1200&amp;q=80" x="242" y="145" width="500" height="500" preserveAspectRatio="xMidYMid slice" clip-path="url(#clip_photo_02)"/>
  <image id="photo_03" href="https://images.unsplash.com/photo-1494976388531-d1058494cdd8?auto=format&amp;fit=crop&amp;w=1200&amp;q=80" x="334" y="145" width="500" height="500" preserveAspectRatio="xMidYMid slice" clip-path="url(#clip_photo_03)"/>
  <image id="photo_04" href="https://images.unsplash.com/photo-1511919884226-fd3cad34687c?auto=format&amp;fit=crop&amp;w=1200&amp;q=80" x="942" y="145" width="500" height="500" preserveAspectRatio="xMidYMid slice" clip-path="url(#clip_photo_04)"/>
  <image id="photo_05" href="https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?auto=format&amp;fit=crop&amp;w=1200&amp;q=80" x="1034" y="145" width="500" height="500" preserveAspectRatio="xMidYMid slice" clip-path="url(#clip_photo_05)"/>

  <rect id="active_photo_shade" x="334" y="145" width="500" height="500" rx="26" fill="url(#photoShade)"/>

  <rect id="panel_01_bar" x="150" y="145" width="92" height="500" rx="26" fill="#E6E0D8"/>
  <rect id="panel_02_bar" x="242" y="145" width="92" height="500" rx="26" fill="#D5C4B3"/>
  <rect id="panel_03_bar" x="834" y="145" width="108" height="500" rx="26" fill="#768EA6" filter="url(#softShadow)"/>
  <rect id="panel_04_bar" x="942" y="145" width="92" height="500" rx="26" fill="#445D73"/>
  <rect id="panel_05_bar" x="1034" y="145" width="92" height="500" rx="26" fill="#222E3D"/>

  <text id="active_kicker" x="372" y="228" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="12" letter-spacing="2.4" fill="#FFFFFF" opacity="0.82">ACTIVE CHAPTER</text>
  <text id="active_number" x="370" y="324" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="82" font-weight="800" fill="#FFFFFF">03</text>
  <text id="active_title" x="374" y="374" width="320" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#FFFFFF">产品创新理念</text>
  <text id="active_desc" x="376" y="414" width="350" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#FFFFFF" opacity="0.86">Use Morph to make the selected pillar glide open, exposing a cinematic image field behind the menu.</text>

  <text id="num_01" x="176" y="226" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#1E1E1E">壹</text>
  <text id="title_01_vertical" x="184" y="306" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#1E1E1E"><tspan x="184" dy="0">外</tspan><tspan x="184" dy="34">观</tspan><tspan x="184" dy="34">设</tspan><tspan x="184" dy="34">计</tspan></text>
  <text id="en_01" transform="rotate(-90 198 596)" x="198" y="596" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="11" letter-spacing="1.5" fill="#1E1E1E" opacity="0.72">AUTOMOTIVE EXTERIOR</text>

  <text id="num_02" x="268" y="226" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#1E1E1E">贰</text>
  <text id="title_02_vertical" x="276" y="306" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#1E1E1E"><tspan x="276" dy="0">功</tspan><tspan x="276" dy="34">能</tspan><tspan x="276" dy="34">特</tspan><tspan x="276" dy="34">点</tspan></text>
  <text id="en_02" transform="rotate(-90 290 596)" x="290" y="596" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="11" letter-spacing="1.5" fill="#1E1E1E" opacity="0.72">CAR FEATURES</text>

  <text id="num_03" x="866" y="226" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#F5F7FA">叁</text>
  <text id="title_03_vertical" x="874" y="306" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#F5F7FA"><tspan x="874" dy="0">创</tspan><tspan x="874" dy="34">新</tspan><tspan x="874" dy="34">理</tspan><tspan x="874" dy="34">念</tspan></text>
  <text id="en_03" transform="rotate(-90 892 596)" x="892" y="596" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="11" letter-spacing="1.5" fill="#F5F7FA" opacity="0.75">PRODUCT INNOVATION</text>

  <text id="num_04" x="968" y="226" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#F5F7FA">肆</text>
  <text id="title_04_vertical" x="976" y="306" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#F5F7FA"><tspan x="976" dy="0">宣</tspan><tspan x="976" dy="34">传</tspan><tspan x="976" dy="34">渠</tspan><tspan x="976" dy="34">道</tspan></text>
  <text id="en_04" transform="rotate(-90 990 596)" x="990" y="596" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="11" letter-spacing="1.5" fill="#F5F7FA" opacity="0.72">COMMUNICATION CHANNELS</text>

  <text id="num_05" x="1060" y="226" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#F5F7FA">伍</text>
  <text id="title_05_vertical" x="1068" y="306" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#F5F7FA"><tspan x="1068" dy="0">售</tspan><tspan x="1068" dy="34">后</tspan><tspan x="1068" dy="34">保</tspan><tspan x="1068" dy="34">障</tspan></text>
  <text id="en_05" transform="rotate(-90 1082 596)" x="1082" y="596" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="11" letter-spacing="1.5" fill="#F5F7FA" opacity="0.72">AFTER-SALES GUARANTEE</text>

  <text id="state_caption" x="956" y="690" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#AAB5C2" opacity="0.75">Slide state: Chapter 03 expanded</text>
</svg>
```

## Avoid in this skill
- ❌ SVG `<animate>` / `<animateTransform>`; the motion should come from PowerPoint Morph between separate slides, not SVG animation.
- ❌ `<use>` or `<symbol>` to repeat panels; duplicate real editable shapes so each panel can keep its own stable ID.
- ❌ `writing-mode: vertical-rl` for vertical Chinese labels; use stacked `<tspan>` lines or separate text objects for more reliable PPT editability.
- ❌ `clip-path` on colored panel rectangles or overlays; clipping is only reliable on `<image>` elements.
- ❌ `marker-end` on paths for navigation arrows; if arrows are needed, use editable `<line>` arrows with marker applied directly to each line.

## Composition notes
- Keep the accordion centered vertically, roughly from `y=145` to `y=645`, leaving the top 120 px for a calm executive title zone.
- Use one expanded photo region of about 40% of slide width; all other chapters compress into 90–110 px pillars.
- Maintain the same object IDs across all slide states: only change `x`, `width`, and matching clip rectangles to make Morph feel physical.
- Color rhythm should move from warm light panels on the left to deep navy panels on the right, with the active state receiving the strongest shadow and image contrast.