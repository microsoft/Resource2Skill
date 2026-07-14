# SVG Recipe — Modular Color-Block Infographic

## Visual mechanism
A large neutral header introduces the story, then the information is divided into high-contrast, self-contained color modules that can be scanned independently. Each block uses a consistent internal system—icon, uppercase title, concise bullets, and subtle decorative overlap—to make dense business content feel editorial and organized.

## SVG primitives needed
- 1× full-canvas `<rect>` for the soft neutral background
- 1× large rounded `<rect>` for the white header card
- 4× rounded `<rect>` for the modular color blocks
- 4× darker translucent `<rect>` strips for block label contrast
- 1× `<image>` clipped by a circular `<clipPath>` for the avatar/profile photo
- 2× `<circle>` for avatar ring and small accent dots
- 8× decorative rotated rounded `<rect>` elements for paperclip/tape accents
- 8× `<path>` elements for simple editable icons and decorative swooshes
- 1× `<linearGradient>` for the header sheen
- 4× `<linearGradient>` fills for the colored information blocks
- 1× `<filter id="softShadow">` applied to cards and blocks for premium depth
- Multiple `<text>` elements with explicit `width` attributes for title, subtitle, block headings, bullets, and metadata

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="headerSheen" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#EEF2F6"/>
    </linearGradient>
    <linearGradient id="blueBlock" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#88BCEB"/>
      <stop offset="100%" stop-color="#5F9FD8"/>
    </linearGradient>
    <linearGradient id="magentaBlock" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#EA6E9B"/>
      <stop offset="100%" stop-color="#D94B7F"/>
    </linearGradient>
    <linearGradient id="yellowBlock" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8D76C"/>
      <stop offset="100%" stop-color="#EDB93E"/>
    </linearGradient>
    <linearGradient id="redBlock" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#E86C67"/>
      <stop offset="100%" stop-color="#CF4E4B"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <clipPath id="avatarClip">
      <circle cx="142" cy="116" r="54"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F4F5F7"/>
  <path d="M1050,34 C1134,18 1226,52 1270,118 L1270,0 L1050,0 Z" fill="#E7ECF2"/>
  <path d="M-10,610 C94,570 180,612 235,720 L-10,720 Z" fill="#E8EDF3"/>

  <rect x="72" y="46" width="1136" height="150" rx="28" fill="url(#headerSheen)" filter="url(#softShadow)"/>
  <circle cx="142" cy="116" r="62" fill="none" stroke="#FFFFFF" stroke-width="10"/>
  <image href="https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=400" x="88" y="62" width="108" height="108" clip-path="url(#avatarClip)"/>
  <circle cx="204" cy="66" r="9" fill="#F4C958"/>
  <circle cx="196" cy="166" r="6" fill="#E6668F"/>

  <text x="232" y="92" width="720" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#6A7480" letter-spacing="2">EXECUTIVE SNAPSHOT</text>
  <text x="232" y="135" width="760" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="36" font-weight="800" fill="#2F343A">SWOT Analysis for a Creator-Led Brand</text>
  <text x="234" y="166" width="720" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#66717D">Four modular evidence blocks summarize the strategic posture at a glance.</text>
  <rect x="1012" y="82" width="142" height="50" rx="25" fill="#2F343A"/>
  <text x="1038" y="114" width="96" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#FFFFFF" text-anchor="middle">Q3 REVIEW</text>

  <rect x="72" y="232" width="544" height="190" rx="26" fill="url(#blueBlock)" filter="url(#softShadow)"/>
  <rect x="96" y="256" width="104" height="104" rx="24" fill="#FFFFFF" opacity="0.22"/>
  <path d="M131,318 L151,338 L180,291" fill="none" stroke="#FFFFFF" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/>
  <rect x="228" y="254" width="344" height="38" rx="19" fill="#387DBB" opacity="0.32"/>
  <text x="250" y="280" width="290" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="800" fill="#FFFFFF" letter-spacing="1">STRENGTHS</text>
  <text x="228" y="326" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#FFFFFF">
    <tspan x="228" dy="0">• Loyal audience with high repeat viewing</tspan>
    <tspan x="228" dy="25">• Recognizable editing and thumbnail style</tspan>
    <tspan x="228" dy="25">• Consistent weekly publishing cadence</tspan>
  </text>
  <rect x="548" y="214" width="26" height="62" rx="13" fill="#FFFFFF" opacity="0.5" transform="rotate(32 561 245)"/>

  <rect x="664" y="232" width="544" height="190" rx="26" fill="url(#magentaBlock)" filter="url(#softShadow)"/>
  <rect x="688" y="256" width="104" height="104" rx="24" fill="#FFFFFF" opacity="0.20"/>
  <path d="M721,291 C751,282 770,303 755,326 C742,347 711,343 704,319 C700,306 708,296 721,291 Z" fill="none" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round"/>
  <path d="M758,340 L775,356" fill="none" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round"/>
  <rect x="820" y="254" width="344" height="38" rx="19" fill="#B63566" opacity="0.34"/>
  <text x="842" y="280" width="290" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="800" fill="#FFFFFF" letter-spacing="1">WEAKNESSES</text>
  <text x="820" y="326" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#FFFFFF">
    <tspan x="820" dy="0">• Production cost rises with each launch</tspan>
    <tspan x="820" dy="25">• Revenue concentrated on one platform</tspan>
    <tspan x="820" dy="25">• Founder burnout risk during peak cycles</tspan>
  </text>
  <rect x="1140" y="213" width="26" height="62" rx="13" fill="#FFFFFF" opacity="0.46" transform="rotate(-31 1153 244)"/>

  <rect x="72" y="462" width="544" height="190" rx="26" fill="url(#yellowBlock)" filter="url(#softShadow)"/>
  <rect x="96" y="486" width="104" height="104" rx="24" fill="#FFFFFF" opacity="0.24"/>
  <path d="M126,552 C126,526 147,510 169,522 C190,533 190,565 166,576 L166,590 L137,590 L137,576 C130,572 126,563 126,552 Z" fill="none" stroke="#FFFFFF" stroke-width="9" stroke-linejoin="round"/>
  <path d="M139,604 L164,604" stroke="#FFFFFF" stroke-width="9" stroke-linecap="round"/>
  <rect x="228" y="484" width="344" height="38" rx="19" fill="#D99D21" opacity="0.33"/>
  <text x="250" y="510" width="290" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="800" fill="#FFFFFF" letter-spacing="1">OPPORTUNITIES</text>
  <text x="228" y="556" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#FFFFFF">
    <tspan x="228" dy="0">• Launch a premium resource library</tspan>
    <tspan x="228" dy="25">• Co-create episodes with adjacent experts</tspan>
    <tspan x="228" dy="25">• Package content into live workshops</tspan>
  </text>
  <rect x="548" y="444" width="26" height="62" rx="13" fill="#FFFFFF" opacity="0.48" transform="rotate(-28 561 475)"/>

  <rect x="664" y="462" width="544" height="190" rx="26" fill="url(#redBlock)" filter="url(#softShadow)"/>
  <rect x="688" y="486" width="104" height="104" rx="24" fill="#FFFFFF" opacity="0.20"/>
  <path d="M741,512 L780,580 L702,580 Z" fill="none" stroke="#FFFFFF" stroke-width="10" stroke-linejoin="round"/>
  <path d="M741,537 L741,558" stroke="#FFFFFF" stroke-width="9" stroke-linecap="round"/>
  <circle cx="741" cy="571" r="5" fill="#FFFFFF"/>
  <rect x="820" y="484" width="344" height="38" rx="19" fill="#A93D3B" opacity="0.34"/>
  <text x="842" y="510" width="290" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="800" fill="#FFFFFF" letter-spacing="1">THREATS</text>
  <text x="820" y="556" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#FFFFFF">
    <tspan x="820" dy="0">• Algorithm shifts could reduce discovery</tspan>
    <tspan x="820" dy="25">• Competitors copying the visual format</tspan>
    <tspan x="820" dy="25">• Audience fatigue from category saturation</tspan>
  </text>
  <rect x="1140" y="444" width="26" height="62" rx="13" fill="#FFFFFF" opacity="0.45" transform="rotate(30 1153 475)"/>

  <text x="72" y="690" width="540" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#8A929C">Design system: color modules, shared rhythm, icon-led scan path</text>
  <text x="935" y="690" width="270" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#8A929C" text-anchor="end">Prepared for leadership discussion</text>
</svg>
```

## Avoid in this skill
- ❌ Using `<mask>` to create the circular avatar; use `<clipPath>` applied directly to the `<image>` instead.
- ❌ Building repeated icons with `<use href="#id">`; duplicate the editable paths directly so PowerPoint can preserve them.
- ❌ Applying `clip-path` to colored rectangles or text; clipping is reliable for images only in this workflow.
- ❌ Overloading the modules with long paragraphs; the technique depends on short, scannable bullets.
- ❌ Low-contrast color blocks with dark text; the executive infographic look works best with bold color fields and white typography.

## Composition notes
- Keep the header to roughly the top quarter of the canvas; it should introduce the story without competing with the four modules.
- Use a strict 2×2 grid with generous gutters so each color block feels like an independent card.
- Put icons on the left side of each module and text on the right to create a repeated scan pattern.
- Reserve small decorative overlaps, such as paperclip tabs or accent dots, for warmth and depth without breaking the clean modular system.