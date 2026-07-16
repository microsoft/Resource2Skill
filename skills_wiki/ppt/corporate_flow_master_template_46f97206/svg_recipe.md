# SVG Recipe — Professional Corporate Master Template

## Visual mechanism
A polished corporate master slide uses a calm blue gradient header, a crisp dividing rule, and translucent organic wave paths sweeping from the left edge to add motion without compromising whitespace. Subtle glossy gradient content modules sit in the safe area, creating a unified executive-template look that remains fully editable in PowerPoint.

## SVG primitives needed
- 1× full-slide `<rect>` for the white canvas background
- 1× `<rect>` with vertical `<linearGradient>` for the structural header banner
- 1× `<line>` for the header’s darker bottom rule
- 8× `<path>` for layered abstract blue wave/swoosh accents
- 1× `<filter id="waveBlur">` with `feGaussianBlur` applied to background wave paths
- 1× `<filter id="softShadow">` with offset blur and merge applied to glossy content cards
- 4× rounded `<rect>` for glossy content modules
- 4× small `<circle>` for numbered/semantic card badges
- 8× `<text>` elements with explicit `width` for master title, subtitle, section title, and card labels
- Multiple `<linearGradient>` definitions for header, cards, highlights, and blue wave strokes

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="headerGrad" x1="0" y1="0" x2="0" y2="120">
      <stop offset="0%" stop-color="#F2F8FD"/>
      <stop offset="45%" stop-color="#D8EAF8"/>
      <stop offset="100%" stop-color="#8DBDE2"/>
    </linearGradient>

    <linearGradient id="waveStroke1" x1="0" y1="110" x2="520" y2="640">
      <stop offset="0%" stop-color="#0C4EA2" stop-opacity="0.72"/>
      <stop offset="50%" stop-color="#3F8CD6" stop-opacity="0.40"/>
      <stop offset="100%" stop-color="#BBDCF4" stop-opacity="0.05"/>
    </linearGradient>
    <linearGradient id="waveStroke2" x1="0" y1="420" x2="760" y2="540">
      <stop offset="0%" stop-color="#6EB3E8" stop-opacity="0.55"/>
      <stop offset="55%" stop-color="#1662B4" stop-opacity="0.48"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="cardBlue" x1="0" y1="220" x2="0" y2="405">
      <stop offset="0%" stop-color="#5CC8FF"/>
      <stop offset="48%" stop-color="#1597DA"/>
      <stop offset="100%" stop-color="#0269B8"/>
    </linearGradient>
    <linearGradient id="cardTeal" x1="0" y1="220" x2="0" y2="405">
      <stop offset="0%" stop-color="#5BE8D7"/>
      <stop offset="52%" stop-color="#16B8B6"/>
      <stop offset="100%" stop-color="#047E8A"/>
    </linearGradient>
    <linearGradient id="cardIndigo" x1="0" y1="440" x2="0" y2="625">
      <stop offset="0%" stop-color="#8CA7FF"/>
      <stop offset="50%" stop-color="#4B69D8"/>
      <stop offset="100%" stop-color="#263B9D"/>
    </linearGradient>
    <linearGradient id="cardSlate" x1="0" y1="440" x2="0" y2="625">
      <stop offset="0%" stop-color="#B9D1E9"/>
      <stop offset="48%" stop-color="#6E94BA"/>
      <stop offset="100%" stop-color="#385A7A"/>
    </linearGradient>
    <linearGradient id="cardGloss" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.55"/>
      <stop offset="42%" stop-color="#FFFFFF" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>

    <filter id="waveBlur" x="-20%" y="-20%" width="150%" height="150%">
      <feGaussianBlur stdDeviation="3.2"/>
    </filter>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <rect x="0" y="0" width="1280" height="116" fill="url(#headerGrad)"/>
  <line x1="0" y1="116" x2="1280" y2="116" stroke="#5D95C8" stroke-width="4"/>

  <path d="M -80 145 C 30 235, 240 195, 248 342 C 256 490, 90 502, 28 430 C -55 333, 168 308, 305 398 C 425 477, 502 419, 610 340"
        fill="none" stroke="url(#waveStroke1)" stroke-width="13" stroke-linecap="round" opacity="0.86" filter="url(#waveBlur)"/>
  <path d="M -70 136 C 20 270, 244 158, 304 298 C 372 458, 155 556, 54 451 C -14 381, 96 326, 235 374 C 390 427, 438 402, 558 350"
        fill="none" stroke="#145AA8" stroke-width="4.5" stroke-linecap="round" opacity="0.72"/>
  <path d="M -120 535 C 35 358, 180 366, 330 489 C 405 550, 512 560, 725 527"
        fill="none" stroke="url(#waveStroke2)" stroke-width="19" stroke-linecap="round" opacity="0.62" filter="url(#waveBlur)"/>
  <path d="M -140 522 C 92 314, 178 410, 300 514 C 382 584, 497 579, 760 542"
        fill="none" stroke="#0B4D9F" stroke-width="4" stroke-linecap="round" opacity="0.54"/>
  <path d="M -40 86 C 32 178, 20 270, 48 354 C 92 486, 243 550, 355 604"
        fill="none" stroke="#2B7DCA" stroke-width="20" stroke-linecap="round" opacity="0.20" filter="url(#waveBlur)"/>
  <path d="M -6 84 C 52 190, 34 282, 68 369 C 119 500, 248 548, 354 610"
        fill="none" stroke="#0A4C9A" stroke-width="5" stroke-linecap="round" opacity="0.45"/>
  <path d="M 760 695 C 930 558, 1080 565, 1375 425"
        fill="none" stroke="#6FB5E7" stroke-width="30" stroke-linecap="round" opacity="0.12" filter="url(#waveBlur)"/>
  <path d="M 805 706 C 955 578, 1128 574, 1368 456"
        fill="none" stroke="#1E73BE" stroke-width="5" stroke-linecap="round" opacity="0.24"/>

  <text x="720" y="74" width="500" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="38" font-weight="700" fill="#1F4F80" text-anchor="middle">
    PowerPoint Templates
  </text>
  <text x="1035" y="680" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#A7A7A7" text-anchor="middle">
    DigitalOfficePro.com
  </text>

  <text x="360" y="188" width="560" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="30" font-weight="700" fill="#1A365D">
    Quarterly Business Overview
  </text>
  <text x="360" y="222" width="660" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" fill="#66809A">
    A clean master layout with reusable branded modules and generous whitespace
  </text>

  <g filter="url(#softShadow)">
    <rect x="360" y="270" width="205" height="118" rx="16" fill="url(#cardBlue)"/>
    <rect x="380" y="286" width="165" height="38" rx="12" fill="url(#cardGloss)"/>
    <circle cx="397" cy="352" r="18" fill="#FFFFFF" opacity="0.92"/>
    <text x="427" y="348" width="115" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" fill="#FFFFFF">Strategy</text>
    <text x="427" y="372" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#DDF4FF">market direction</text>

    <rect x="590" y="270" width="205" height="118" rx="16" fill="url(#cardTeal)"/>
    <rect x="610" y="286" width="165" height="38" rx="12" fill="url(#cardGloss)"/>
    <circle cx="627" cy="352" r="18" fill="#FFFFFF" opacity="0.92"/>
    <text x="657" y="348" width="115" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" fill="#FFFFFF">Growth</text>
    <text x="657" y="372" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#E3FFFB">pipeline health</text>

    <rect x="360" y="420" width="205" height="118" rx="16" fill="url(#cardIndigo)"/>
    <rect x="380" y="436" width="165" height="38" rx="12" fill="url(#cardGloss)"/>
    <circle cx="397" cy="502" r="18" fill="#FFFFFF" opacity="0.92"/>
    <text x="427" y="498" width="115" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" fill="#FFFFFF">People</text>
    <text x="427" y="522" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#EEF1FF">capability plan</text>

    <rect x="590" y="420" width="205" height="118" rx="16" fill="url(#cardSlate)"/>
    <rect x="610" y="436" width="165" height="38" rx="12" fill="url(#cardGloss)"/>
    <circle cx="627" cy="502" r="18" fill="#FFFFFF" opacity="0.92"/>
    <text x="657" y="498" width="115" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" fill="#FFFFFF">Finance</text>
    <text x="657" y="522" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#EDF6FF">margin focus</text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Do not use a single flattened background image for the header and waves if the template needs editable brand colors; keep the waves as SVG paths with gradients and blur.
- ❌ Do not apply `filter` to the header divider `<line>`; line filters are dropped, so keep the rule crisp and unfiltered.
- ❌ Do not use `<mask>` or clipping on non-image shapes for the glossy card highlights; use translucent rounded `<rect>` overlays instead.
- ❌ Do not create wave accents with `<use>` clones; duplicate the editable paths directly and vary stroke, opacity, and blur.
- ❌ Do not overcrowd the left wave area with dense content; the organic accent should remain decorative, not compete with text.

## Composition notes
- Keep the header at roughly 15–17% of slide height, with primary title text right-weighted or centered-right for the classic corporate-template feel.
- Reserve the left third for abstract waves and the center/right safe area for content; this preserves motion while maintaining readability.
- Use blue as the dominant rhythm: pale header, darker divider, semi-transparent wave strokes, and saturated glossy module fills.
- Leave generous white space between the header, wave cluster, and content cards so the slide reads as a master template rather than a dashboard.