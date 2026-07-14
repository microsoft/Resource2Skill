# SVG Recipe — Morphing Tabbed Navigation

## Visual mechanism
A persistent vertical stack of colored binder tabs anchors the slide, with the active tab shifted outward and layered above a large rounded content page. To create the “morphing” effect in PowerPoint, generate one slide per section with identical object structure, changing only the active tab position/color emphasis and sliding the page content from off-canvas/right to its final position.

## SVG primitives needed
- 1× `<rect>` full-slide background for the light gray canvas
- 8–12× rotated translucent `<rect>` for subtle background stripe texture
- 6× custom `<path>` tab shapes with squared left edges and rounded right edges
- 1× `<path>` active tab duplicate drawn above the page for foreground layering
- 1× large `<rect>` for the main rounded content page with gradient fill
- 1× `<image>` clipped by a rounded `<clipPath>` for a premium visual content card
- 3× small `<rect>` metric cards inside the page
- 2–3× decorative `<path>` blobs/curves for page depth and section identity
- 1× `<linearGradient>` for the content page fill
- 1× `<linearGradient>` for active-tab gloss
- 1× `<filter id="tabShadow">` applied to tab paths
- 1× `<filter id="pageShadow">` applied to the main page/card shapes
- Multiple `<text>` elements with explicit `width` attributes for tab labels, page title, body copy, and metrics

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="pageGrad" x1="180" y1="80" x2="1220" y2="650" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="60%" stop-color="#F7FBFC"/>
      <stop offset="100%" stop-color="#EAF4F6"/>
    </linearGradient>
    <linearGradient id="activeGloss" x1="58" y1="142" x2="224" y2="142" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#3CC1B9"/>
      <stop offset="100%" stop-color="#58D8D0"/>
    </linearGradient>
    <filter id="tabShadow" x="-20%" y="-20%" width="150%" height="150%">
      <feOffset dx="5" dy="5" result="off"/>
      <feGaussianBlur in="off" stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="pageShadow" x="-10%" y="-10%" width="130%" height="130%">
      <feOffset dx="0" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <clipPath id="photoClip">
      <rect x="742" y="136" width="390" height="250" rx="28" ry="28"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F0F1F3"/>
  <rect x="210" y="-80" width="72" height="880" fill="#DCDDE1" opacity="0.22" transform="rotate(15 246 360)"/>
  <rect x="370" y="-80" width="72" height="880" fill="#DCDDE1" opacity="0.18" transform="rotate(15 406 360)"/>
  <rect x="530" y="-80" width="72" height="880" fill="#DCDDE1" opacity="0.18" transform="rotate(15 566 360)"/>
  <rect x="690" y="-80" width="72" height="880" fill="#DCDDE1" opacity="0.16" transform="rotate(15 726 360)"/>
  <rect x="850" y="-80" width="72" height="880" fill="#DCDDE1" opacity="0.14" transform="rotate(15 886 360)"/>
  <rect x="1010" y="-80" width="72" height="880" fill="#DCDDE1" opacity="0.14" transform="rotate(15 1046 360)"/>

  <!-- inactive tabs: keep these objects in the same order on every Morph slide -->
  <path d="M28 62 L150 62 Q182 62 182 94 L182 142 Q182 174 150 174 L28 174 Z" fill="#ED5559" filter="url(#tabShadow)"/>
  <path d="M28 302 L150 302 Q182 302 182 334 L182 382 Q182 414 150 414 L28 414 Z" fill="#FFC000" filter="url(#tabShadow)"/>
  <path d="M28 422 L150 422 Q182 422 182 454 L182 502 Q182 534 150 534 L28 534 Z" fill="#595959" filter="url(#tabShadow)"/>
  <path d="M28 542 L150 542 Q182 542 182 574 L182 622 Q182 654 150 654 L28 654 Z" fill="#92D050" filter="url(#tabShadow)"/>
  <path d="M18 660 L140 660 Q172 660 172 692 L172 740 L18 740 Z" fill="#00B0B9" filter="url(#tabShadow)"/>

  <rect x="174" y="44" width="1016" height="626" rx="34" ry="34" fill="url(#pageGrad)" filter="url(#pageShadow)"/>
  <path d="M1065 470 C1120 420 1200 440 1230 505 C1268 586 1180 650 1094 632 C1018 616 1008 523 1065 470 Z" fill="#3CC1B9" opacity="0.12"/>
  <path d="M240 594 C320 552 420 568 470 626 C394 660 305 666 232 642 Z" fill="#3CC1B9" opacity="0.10"/>

  <!-- active tab drawn after the page so it appears physically on top -->
  <path d="M58 182 L182 182 Q214 182 214 214 L214 262 Q214 294 182 294 L58 294 Z" fill="url(#activeGloss)" filter="url(#tabShadow)"/>
  <rect x="195" y="191" width="20" height="94" fill="#58D8D0" opacity="0.45"/>

  <text x="104" y="131" width="90" font-family="Microsoft YaHei, Segoe UI" font-size="24" font-weight="700" fill="#FFFFFF" text-anchor="middle" transform="rotate(-90 104 118)">平台</text>
  <text x="136" y="251" width="90" font-family="Microsoft YaHei, Segoe UI" font-size="26" font-weight="800" fill="#FFFFFF" text-anchor="middle" transform="rotate(-90 136 238)">课程</text>
  <text x="104" y="371" width="90" font-family="Microsoft YaHei, Segoe UI" font-size="24" font-weight="700" fill="#FFFFFF" text-anchor="middle" transform="rotate(-90 104 358)">类别</text>
  <text x="104" y="491" width="90" font-family="Microsoft YaHei, Segoe UI" font-size="24" font-weight="700" fill="#FFFFFF" text-anchor="middle" transform="rotate(-90 104 478)">内容</text>
  <text x="104" y="611" width="90" font-family="Microsoft YaHei, Segoe UI" font-size="24" font-weight="700" fill="#FFFFFF" text-anchor="middle" transform="rotate(-90 104 598)">定位</text>
  <text x="96" y="714" width="80" font-family="Microsoft YaHei, Segoe UI" font-size="22" font-weight="700" fill="#FFFFFF" text-anchor="middle" transform="rotate(-90 96 696)">简介</text>

  <text x="258" y="150" width="420" font-family="Microsoft YaHei, Segoe UI" font-size="22" font-weight="700" fill="#3CC1B9" letter-spacing="3">SECTION 02</text>
  <text x="258" y="205" width="470" font-family="Microsoft YaHei, Segoe UI" font-size="52" font-weight="800" fill="#263238">课程体系设计</text>
  <text x="260" y="260" width="430" font-family="Microsoft YaHei, Segoe UI" font-size="22" fill="#68747A">
    用清晰的模块路径组织学习内容，让受众始终知道当前位置、下一步行动与整体进度。
  </text>

  <image x="742" y="136" width="390" height="250" href="https://images.example.com/premium-training-workshop-team-collaboration.jpg" clip-path="url(#photoClip)"/>
  <rect x="742" y="136" width="390" height="250" rx="28" ry="28" fill="none" stroke="#FFFFFF" stroke-width="8"/>

  <rect x="260" y="338" width="138" height="126" rx="22" fill="#FFFFFF" filter="url(#pageShadow)"/>
  <rect x="428" y="338" width="138" height="126" rx="22" fill="#FFFFFF" filter="url(#pageShadow)"/>
  <rect x="596" y="338" width="138" height="126" rx="22" fill="#FFFFFF" filter="url(#pageShadow)"/>
  <text x="292" y="386" width="82" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#3CC1B9" text-anchor="middle">06</text>
  <text x="292" y="426" width="92" font-family="Microsoft YaHei, Segoe UI" font-size="18" fill="#68747A" text-anchor="middle">核心模块</text>
  <text x="460" y="386" width="82" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#3CC1B9" text-anchor="middle">24</text>
  <text x="460" y="426" width="92" font-family="Microsoft YaHei, Segoe UI" font-size="18" fill="#68747A" text-anchor="middle">实践任务</text>
  <text x="628" y="386" width="82" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#3CC1B9" text-anchor="middle">88%</text>
  <text x="628" y="426" width="92" font-family="Microsoft YaHei, Segoe UI" font-size="18" fill="#68747A" text-anchor="middle">完成率</text>

  <path d="M790 455 L1080 455" stroke="#DCE7EA" stroke-width="3" stroke-dasharray="8 10"/>
  <circle cx="805" cy="455" r="9" fill="#3CC1B9"/>
  <circle cx="930" cy="455" r="9" fill="#3CC1B9"/>
  <circle cx="1060" cy="455" r="9" fill="#3CC1B9"/>
  <text x="775" y="500" width="330" font-family="Microsoft YaHei, Segoe UI" font-size="22" font-weight="700" fill="#263238">从导航到内容的连续运动</text>
  <text x="775" y="538" width="350" font-family="Microsoft YaHei, Segoe UI" font-size="18" fill="#68747A">复制本页作为下一章节，将活动标签右移、页面内容横向替换，然后在 PowerPoint 中应用 Morph。</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<animate>` or `<animateTransform>`; the motion should be produced by PowerPoint Morph between duplicated editable slides.
- ❌ Do not use `<use>` for repeated tabs; duplicate each tab path so PowerPoint receives independent editable shapes.
- ❌ Do not put `clip-path` on groups or shapes; use it only on the `<image>` for the photo crop.
- ❌ Do not use `marker-end` arrows for section flow; if arrows are needed, use editable `<line>` elements and simple triangle `<path>` arrowheads.
- ❌ Do not apply filters to `<line>` elements; shadows should be on tab paths, cards, and page rectangles only.
- ❌ Do not change object count/order between Morph states; disappearing/reappearing objects break the illusion.

## Composition notes
- Keep the tab rail within the left 15–17% of the canvas; inactive tabs start near x=25–30, while the active tab shifts right by 25–40 px and is drawn above the content page.
- The main page should occupy roughly x=170–1190 and y=45–670, leaving a visible gray border so the page feels like a movable sheet.
- For Morph slides, preserve identical geometry names/order conceptually: same number of tabs, same page container, same content groups; only shift active tab positions and slide content/card/photo blocks horizontally.
- Use one strong accent color per section, echoed in the active tab, small blobs, metric numbers, and timeline dots; keep the page mostly white to maintain executive clarity.