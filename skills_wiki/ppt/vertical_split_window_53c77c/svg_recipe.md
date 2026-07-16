# SVG Recipe — Vertical Split Window

## Visual mechanism
A single oversized “window” card anchors the slide, split into two stacked panes that compare two states, priorities, or phases. A thick frame, subtle glass gradients, and a crisp horizontal divider make the split feel architectural rather than like a simple table.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background
- 1× `<path>` for a soft decorative ambient blob behind the window
- 1× `<rect>` for the main rounded outer window frame
- 2× `<rect>` for top and bottom pane fills
- 1× `<rect>` for the central horizontal divider bar
- 2× `<image>` clipped into rounded preview tiles inside each pane
- 2× `<clipPath>` using rounded `<rect>` crops for pane images
- 4× `<circle>` for status dots and small emphasis accents
- 4× `<line>` for subtle window frame details
- 6× `<text>` elements with explicit `width` attributes for headline, pane titles, body copy, and labels
- 3× `<linearGradient>` for background, frame, and pane depth
- 1× `<radialGradient>` for ambient glow
- 2× `<filter>` definitions for card shadow and soft glow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#08111F"/>
      <stop offset="0.55" stop-color="#101B31"/>
      <stop offset="1" stop-color="#17233B"/>
    </linearGradient>

    <radialGradient id="ambientGlow" cx="50%" cy="45%" r="65%">
      <stop offset="0" stop-color="#2F8CFF" stop-opacity="0.42"/>
      <stop offset="0.48" stop-color="#675CFF" stop-opacity="0.18"/>
      <stop offset="1" stop-color="#101B31" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="frameGrad" x1="350" y1="80" x2="930" y2="650" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#F5F8FF" stop-opacity="0.98"/>
      <stop offset="0.45" stop-color="#B7C7E8" stop-opacity="0.88"/>
      <stop offset="1" stop-color="#6F7FA2" stop-opacity="0.92"/>
    </linearGradient>

    <linearGradient id="topPaneGrad" x1="410" y1="140" x2="870" y2="345" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#F7FAFF"/>
      <stop offset="1" stop-color="#DCEBFF"/>
    </linearGradient>

    <linearGradient id="bottomPaneGrad" x1="410" y1="375" x2="870" y2="585" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#111C32"/>
      <stop offset="1" stop-color="#1E3154"/>
    </linearGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="20"/>
      <feGaussianBlur stdDeviation="22"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>

    <clipPath id="topImageClip">
      <rect x="678" y="166" width="188" height="134" rx="24"/>
    </clipPath>

    <clipPath id="bottomImageClip">
      <rect x="678" y="420" width="188" height="134" rx="24"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <circle cx="640" cy="365" r="390" fill="url(#ambientGlow)" filter="url(#softGlow)"/>

  <path d="M165 585 C250 492 332 604 421 514 C527 406 645 570 770 456 C895 341 987 412 1104 316 C1134 292 1178 287 1210 302 L1210 720 L165 720 Z"
        fill="#263D66" opacity="0.28"/>

  <text x="88" y="82" width="480" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" fill="#8EA3C7" letter-spacing="2">
    OPERATING MODEL
  </text>
  <text x="88" y="128" width="570" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="44" font-weight="700" fill="#F7FAFF">
    Vertical Split Window
  </text>
  <text x="88" y="174" width="510" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" fill="#B8C7E3">
    Use one architectural frame to contrast what is visible now with what is changing next.
  </text>

  <rect x="374" y="105" width="532" height="520" rx="38" fill="url(#frameGrad)" filter="url(#cardShadow)"/>
  <rect x="392" y="123" width="496" height="484" rx="28" fill="#091425" opacity="0.92"/>

  <rect x="410" y="141" width="460" height="204" rx="24" fill="url(#topPaneGrad)"/>
  <rect x="410" y="375" width="460" height="214" rx="24" fill="url(#bottomPaneGrad)"/>

  <rect x="410" y="338" width="460" height="44" rx="16" fill="#0B1323"/>
  <line x1="438" y1="360" x2="842" y2="360" stroke="#8FA8D4" stroke-width="1.2" opacity="0.35"/>
  <line x1="438" y1="148" x2="842" y2="148" stroke="#FFFFFF" stroke-width="1.2" opacity="0.42"/>
  <line x1="438" y1="584" x2="842" y2="584" stroke="#6F86B0" stroke-width="1.2" opacity="0.32"/>
  <line x1="640" y1="123" x2="640" y2="607" stroke="#FFFFFF" stroke-width="1" opacity="0.10"/>

  <circle cx="448" cy="178" r="7" fill="#34D399"/>
  <circle cx="470" cy="178" r="7" fill="#60A5FA"/>
  <circle cx="492" cy="178" r="7" fill="#FBBF24"/>

  <text x="442" y="224" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="30" font-weight="700" fill="#0F1C31">
    Current State
  </text>
  <text x="442" y="262" width="205" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" fill="#31445F">
    Stable demand, fragmented workflows, and clear opportunities for automation.
  </text>

  <image x="678" y="166" width="188" height="134"
         href="https://images.example.com/abstract-blue-operations-dashboard.jpg"
         clip-path="url(#topImageClip)" preserveAspectRatio="xMidYMid slice"/>
  <rect x="690" y="286" width="96" height="8" rx="4" fill="#2F80ED" opacity="0.75"/>
  <rect x="690" y="270" width="142" height="8" rx="4" fill="#7BA7EF" opacity="0.55"/>

  <text x="565" y="367" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" fill="#BFD0EE" text-anchor="middle">
    TRANSITION LAYER
  </text>

  <circle cx="448" cy="416" r="9" fill="#7C3AED"/>
  <text x="442" y="464" width="220" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="30" font-weight="700" fill="#F7FAFF">
    Future State
  </text>
  <text x="442" y="502" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" fill="#BAC9E4">
    Integrated planning window, fewer handoffs, and faster executive decision cycles.
  </text>

  <image x="678" y="420" width="188" height="134"
         href="https://images.example.com/futuristic-enterprise-control-room.jpg"
         clip-path="url(#bottomImageClip)" preserveAspectRatio="xMidYMid slice"/>
  <rect x="694" y="438" width="54" height="54" rx="14" fill="#FFFFFF" opacity="0.18"/>
  <path d="M709 466 L724 481 L747 451" fill="none" stroke="#A7F3D0" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>

  <path d="M920 178 C982 184 1036 225 1056 285 C1079 354 1041 419 975 430 C925 438 891 399 901 351 C910 308 947 294 972 310"
        fill="none" stroke="#4EA1FF" stroke-width="3" stroke-dasharray="9 12" opacity="0.55"/>
  <text x="938" y="494" width="230" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" fill="#D7E4FF">
    The frame keeps the story unified while each pane carries a distinct message.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Building the split as a table grid; it should feel like one premium framed object, not a spreadsheet.
- ❌ Applying `clip-path` to pane rectangles for rounded corners; use rounded `<rect>` directly, and reserve clipping for `<image>`.
- ❌ Using `<mask>` to create glass effects; layer translucent gradients and soft shadows instead.
- ❌ Overloading both panes with dense bullets; the split window works best with short titles and 1–2 lines of body copy.

## Composition notes
- Keep the window centered and large, occupying roughly 40–45% of slide width and 70% of slide height.
- Place the headline and framing copy in the upper-left negative space; do not compete with the central card.
- Use strong contrast between panes: light top / dark bottom, or warm top / cool bottom, so the split is instantly legible.
- Add only one or two decorative elements outside the frame; the main focus should remain the split architectural window.