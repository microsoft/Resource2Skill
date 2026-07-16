# SVG Recipe — Frosted Glass UI Panels (Glassmorphism)

## Visual mechanism
Layer translucent rounded panels above a vibrant blurred-gradient background, using soft shadows, white edge highlights, and low-opacity fills to simulate frosted glass. The “glass” reads best when colorful blurred blobs sit behind it and the panel content is crisp white, creating a modern floating UI-dashboard feel.

## SVG primitives needed
- 1× full-slide `<rect>` for the deep gradient background
- 5× blurred `<circle>` / `<ellipse>` for colorful out-of-focus background blobs
- 3× `<rect>` shadow plates behind the glass cards
- 3× translucent rounded `<rect>` for frosted glass panel bodies
- 3× rounded `<rect>` with gradient/white strokes for glass rim highlights
- 3× subtle `<path>` highlight streaks for reflective sheen on the panels
- 1× rounded-corner `<image>` clipped into the main glass phone panel for a premium UI/photo insert
- 1× `<clipPath>` with rounded `<rect>` for the clipped image crop
- 1× `<filter id="blobBlur">` for large background blur
- 1× `<filter id="panelShadow">` for soft floating card shadows
- 1× `<filter id="softGlow">` for edge glow on selected panel highlights
- Multiple `<text>` elements with explicit `width` for title, body copy, metrics, and UI labels
- Simple `<path>`, `<circle>`, and `<line>` icons for editable UI decoration

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#efe7ff"/>
      <stop offset="38%" stop-color="#9d6cff"/>
      <stop offset="72%" stop-color="#5134c8"/>
      <stop offset="100%" stop-color="#171142"/>
    </linearGradient>

    <linearGradient id="glassFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.36"/>
      <stop offset="48%" stop-color="#ffffff" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#d8ccff" stop-opacity="0.08"/>
    </linearGradient>

    <linearGradient id="rimStroke" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.88"/>
      <stop offset="42%" stop-color="#ffffff" stop-opacity="0.26"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0.08"/>
    </linearGradient>

    <radialGradient id="metricGlow" cx="50%" cy="35%" r="70%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.42"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0.04"/>
    </radialGradient>

    <filter id="blobBlur" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="46"/>
    </filter>

    <filter id="panelShadow" x="-25%" y="-25%" width="150%" height="150%">
      <feOffset dx="0" dy="24"/>
      <feGaussianBlur stdDeviation="28"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="8"/>
    </filter>

    <clipPath id="phoneImageClip">
      <rect x="454" y="216" width="250" height="270" rx="34" ry="34"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <circle cx="176" cy="132" r="168" fill="#ff6bd6" opacity="0.62" filter="url(#blobBlur)"/>
  <circle cx="1048" cy="130" r="210" fill="#39d6ff" opacity="0.48" filter="url(#blobBlur)"/>
  <ellipse cx="918" cy="612" rx="250" ry="126" fill="#ffb84d" opacity="0.42" filter="url(#blobBlur)"/>
  <circle cx="384" cy="552" r="190" fill="#5cffc8" opacity="0.26" filter="url(#blobBlur)"/>
  <ellipse cx="650" cy="316" rx="340" ry="190" fill="#6e48ff" opacity="0.34" filter="url(#blobBlur)"/>

  <path d="M-40 520 C180 430 220 690 460 590 C720 484 766 300 1034 388 C1166 432 1232 354 1328 300 L1328 760 L-40 760 Z"
        fill="#ffffff" opacity="0.055"/>

  <rect x="92" y="105" width="326" height="510" rx="44" fill="#1d1248" opacity="0.20" filter="url(#panelShadow)"/>
  <rect x="92" y="105" width="326" height="510" rx="44" fill="url(#glassFill)"/>
  <rect x="94" y="107" width="322" height="506" rx="42" fill="none" stroke="url(#rimStroke)" stroke-width="2.2"/>
  <path d="M126 151 C188 120 268 126 356 166" fill="none" stroke="#ffffff" stroke-opacity="0.34" stroke-width="3" filter="url(#softGlow)"/>

  <circle cx="143" cy="160" r="7" fill="#ffffff" opacity="0.68"/>
  <circle cx="170" cy="160" r="7" fill="#ffffff" opacity="0.38"/>
  <circle cx="197" cy="160" r="7" fill="#ffffff" opacity="0.24"/>

  <text x="128" y="244" width="244" font-family="Segoe UI, Microsoft YaHei" font-size="46" font-weight="700" fill="#ffffff">
    Frosted
    <tspan x="128" dy="52" fill="#f4edff">Glass UI</tspan>
  </text>
  <text x="130" y="360" width="236" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#ffffff" opacity="0.78">
    Layered translucent panels with soft depth, rim highlights, and crisp editable content.
  </text>

  <rect x="130" y="447" width="232" height="74" rx="22" fill="url(#metricGlow)" stroke="#ffffff" stroke-opacity="0.26"/>
  <path d="M164 487 L186 466 L211 488 L250 451 L298 493" fill="none" stroke="#ffffff" stroke-opacity="0.82" stroke-width="4"/>
  <text x="160" y="558" width="174" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#ffffff" opacity="0.68">
    Live dashboard surface
  </text>

  <rect x="432" y="84" width="298" height="552" rx="54" fill="#191047" opacity="0.24" filter="url(#panelShadow)"/>
  <rect x="432" y="84" width="298" height="552" rx="54" fill="url(#glassFill)"/>
  <rect x="435" y="87" width="292" height="546" rx="51" fill="none" stroke="url(#rimStroke)" stroke-width="2.4"/>
  <path d="M474 126 C530 99 626 105 692 150" fill="none" stroke="#ffffff" stroke-opacity="0.42" stroke-width="3" filter="url(#softGlow)"/>

  <text x="468" y="164" width="214" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="600" fill="#ffffff" opacity="0.86">
    Product Preview
  </text>
  <image x="454" y="216" width="250" height="270"
         href="https://images.example.com/futuristic-mobile-app-purple-dashboard.jpg"
         clip-path="url(#phoneImageClip)" opacity="0.82"/>
  <rect x="454" y="216" width="250" height="270" rx="34" fill="#ffffff" opacity="0.08"/>
  <rect x="454" y="216" width="250" height="270" rx="34" fill="none" stroke="#ffffff" stroke-opacity="0.30"/>

  <rect x="488" y="524" width="178" height="48" rx="24" fill="#ffffff" opacity="0.18"/>
  <circle cx="518" cy="548" r="13" fill="#7fffe1" opacity="0.9"/>
  <text x="544" y="554" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#ffffff">
    Synced
  </text>

  <rect x="792" y="118" width="354" height="202" rx="38" fill="#201050" opacity="0.22" filter="url(#panelShadow)"/>
  <rect x="792" y="118" width="354" height="202" rx="38" fill="url(#glassFill)"/>
  <rect x="795" y="121" width="348" height="196" rx="35" fill="none" stroke="url(#rimStroke)" stroke-width="2"/>
  <path d="M826 164 C902 130 1012 136 1108 178" fill="none" stroke="#ffffff" stroke-opacity="0.30" stroke-width="3" filter="url(#softGlow)"/>

  <circle cx="858" cy="215" r="38" fill="#ffffff" opacity="0.16"/>
  <path d="M846 216 L858 228 L875 203" fill="none" stroke="#ffffff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="918" y="194" width="174" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#ffffff">
    Build records
  </text>
  <text x="918" y="232" width="184" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#ffffff" opacity="0.72">
    Organize complex status updates into calm, readable cards.
  </text>

  <rect x="824" y="386" width="294" height="188" rx="36" fill="#201050" opacity="0.20" filter="url(#panelShadow)"/>
  <rect x="824" y="386" width="294" height="188" rx="36" fill="url(#glassFill)"/>
  <rect x="827" y="389" width="288" height="182" rx="33" fill="none" stroke="url(#rimStroke)" stroke-width="2"/>
  <path d="M858 430 C920 404 1010 408 1080 440" fill="none" stroke="#ffffff" stroke-opacity="0.28" stroke-width="3" filter="url(#softGlow)"/>

  <text x="866" y="452" width="202" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#ffffff">
    Modern UI look
  </text>
  <text x="866" y="490" width="204" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#ffffff" opacity="0.74">
    Use translucent cards, bright strokes, and blurred color fields to imply depth.
  </text>
  <line x1="866" y1="536" x2="1044" y2="536" stroke="#ffffff" stroke-opacity="0.24" stroke-width="2"/>
  <circle cx="1075" cy="536" r="10" fill="#ffffff" opacity="0.68"/>
</svg>
```

## Avoid in this skill
- ❌ SVG `<animate>` or `<animateTransform>` for the entrance motion; create the motion with PowerPoint Morph between two slides instead.
- ❌ CSS `backdrop-filter: blur(...)`; it will not translate as editable PowerPoint glass.
- ❌ `<mask>`-based glass cutouts; masks are fragile in this pipeline and can hard-fail.
- ❌ Applying `clip-path` to ordinary shapes to contain blurred decorative blobs; clipping is reliable for `<image>` only.
- ❌ Filtered `<line>` elements for glow; use filtered `<path>` or `<rect>` highlights instead.
- ❌ Overly transparent panels on pale backgrounds; the frosted effect needs enough contrast and a visible white rim.

## Composition notes
- Keep the background visually active but soft: large blurred blobs should sit behind the panels, not compete with the text.
- Use 25–45 px corner radii and generous spacing so the panels feel like premium floating UI cards.
- Place the highest-density content inside the largest glass card; secondary cards should have fewer words and stronger icon/metric cues.
- For animation, duplicate the slide: position panels slightly off-canvas or lower on slide 1, then use the final SVG layout on slide 2 with PowerPoint Morph.