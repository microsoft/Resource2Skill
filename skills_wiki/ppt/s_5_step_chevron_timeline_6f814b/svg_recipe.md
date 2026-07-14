# SVG Recipe — 5-Step Chevron Timeline

## Visual mechanism
A continuous row of interlocking chevrons creates a strong left-to-right process flow, with each phase occupying one arrow-shaped tab. Number badges, compact headings, and short explanatory copy sit inside each chevron while gradients and shadows make the timeline feel layered and executive-ready.

## SVG primitives needed
- 1× `<rect>` for the full-slide background.
- 5× `<path>` for the main interlocking chevron bodies.
- 5× `<circle>` for numbered step badges.
- 5× `<path>` for small decorative icon strokes or accent marks inside each step.
- 11× `<text>` elements for headline, subtitle, step numbers, step titles, and step descriptions.
- 2× decorative blurred `<path>` shapes for background energy.
- 5× `<linearGradient>` fills for the chevron color progression.
- 1× `<radialGradient>` for the subtle background glow.
- 2× `<filter>` definitions: one soft drop shadow for chevrons, one blur/glow for decorative background shapes.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgGlow" cx="50%" cy="42%" r="70%">
      <stop offset="0%" stop-color="#F7FBFF"/>
      <stop offset="58%" stop-color="#EEF4FA"/>
      <stop offset="100%" stop-color="#E5ECF4"/>
    </radialGradient>

    <linearGradient id="g1" x1="80" y1="240" x2="340" y2="480" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#1F78FF"/>
      <stop offset="100%" stop-color="#164ECA"/>
    </linearGradient>
    <linearGradient id="g2" x1="296" y1="240" x2="556" y2="480" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#00A7D8"/>
      <stop offset="100%" stop-color="#0877B9"/>
    </linearGradient>
    <linearGradient id="g3" x1="512" y1="240" x2="772" y2="480" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#22B573"/>
      <stop offset="100%" stop-color="#0C8C61"/>
    </linearGradient>
    <linearGradient id="g4" x1="728" y1="240" x2="988" y2="480" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#F4A62A"/>
      <stop offset="100%" stop-color="#E06A16"/>
    </linearGradient>
    <linearGradient id="g5" x1="944" y1="240" x2="1204" y2="480" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#F05B7F"/>
      <stop offset="100%" stop-color="#BA2E7A"/>
    </linearGradient>

    <filter id="chevronShadow" x="-10%" y="-15%" width="125%" height="140%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="12"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.07  0 0 0 0 0.12  0 0 0 0 0.20  0 0 0 0.24 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softBlur" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGlow)"/>

  <path d="M-40 92 C120 18 250 34 354 124 C232 144 148 214 52 320 C30 250 -4 168 -40 92 Z"
        fill="#D9E7FF" opacity="0.55" filter="url(#softBlur)"/>
  <path d="M1058 560 C1120 480 1248 464 1336 538 C1308 656 1186 722 1040 696 C1006 650 1014 604 1058 560 Z"
        fill="#FFE1CF" opacity="0.65" filter="url(#softBlur)"/>

  <text x="80" y="86" width="760" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="38" font-weight="700" fill="#172033">5-Step Chevron Timeline</text>
  <text x="82" y="124" width="720" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" fill="#5E6B7A">Use the connected arrow tabs to show momentum, handoffs, and phase-by-phase ownership.</text>

  <path d="M90 240 L280 240 L340 360 L280 480 L90 480 L150 360 Z"
        fill="url(#g1)" stroke="#FFFFFF" stroke-width="3" filter="url(#chevronShadow)"/>
  <path d="M306 240 L496 240 L556 360 L496 480 L306 480 L366 360 Z"
        fill="url(#g2)" stroke="#FFFFFF" stroke-width="3" filter="url(#chevronShadow)"/>
  <path d="M522 240 L712 240 L772 360 L712 480 L522 480 L582 360 Z"
        fill="url(#g3)" stroke="#FFFFFF" stroke-width="3" filter="url(#chevronShadow)"/>
  <path d="M738 240 L928 240 L988 360 L928 480 L738 480 L798 360 Z"
        fill="url(#g4)" stroke="#FFFFFF" stroke-width="3" filter="url(#chevronShadow)"/>
  <path d="M954 240 L1144 240 L1204 360 L1144 480 L954 480 L1014 360 Z"
        fill="url(#g5)" stroke="#FFFFFF" stroke-width="3" filter="url(#chevronShadow)"/>

  <circle cx="190" cy="298" r="27" fill="#FFFFFF" opacity="0.96"/>
  <circle cx="406" cy="298" r="27" fill="#FFFFFF" opacity="0.96"/>
  <circle cx="622" cy="298" r="27" fill="#FFFFFF" opacity="0.96"/>
  <circle cx="838" cy="298" r="27" fill="#FFFFFF" opacity="0.96"/>
  <circle cx="1054" cy="298" r="27" fill="#FFFFFF" opacity="0.96"/>

  <text x="174" y="309" width="32" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="26" font-weight="800" fill="#164ECA">1</text>
  <text x="390" y="309" width="32" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="26" font-weight="800" fill="#0877B9">2</text>
  <text x="606" y="309" width="32" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="26" font-weight="800" fill="#0C8C61">3</text>
  <text x="822" y="309" width="32" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="26" font-weight="800" fill="#E06A16">4</text>
  <text x="1038" y="309" width="32" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="26" font-weight="800" fill="#BA2E7A">5</text>

  <path d="M170 347 L210 347 M180 359 L200 359" stroke="#BBD7FF" stroke-width="4" stroke-linecap="round"/>
  <path d="M386 347 L426 347 M396 359 L416 359" stroke="#BFEFFF" stroke-width="4" stroke-linecap="round"/>
  <path d="M602 347 L642 347 M612 359 L632 359" stroke="#C9F3DD" stroke-width="4" stroke-linecap="round"/>
  <path d="M818 347 L858 347 M828 359 L848 359" stroke="#FFE2B1" stroke-width="4" stroke-linecap="round"/>
  <path d="M1034 347 L1074 347 M1044 359 L1064 359" stroke="#FFD0DE" stroke-width="4" stroke-linecap="round"/>

  <text x="128" y="386" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="21" font-weight="700" fill="#FFFFFF" text-anchor="middle">Discover</text>
  <text x="128" y="421" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" fill="#EAF3FF" text-anchor="middle">Frame the problem and align on decision criteria.</text>

  <text x="344" y="386" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="21" font-weight="700" fill="#FFFFFF" text-anchor="middle">Design</text>
  <text x="344" y="421" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" fill="#EAF9FF" text-anchor="middle">Map options, dependencies, and success measures.</text>

  <text x="560" y="386" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="21" font-weight="700" fill="#FFFFFF" text-anchor="middle">Build</text>
  <text x="560" y="421" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" fill="#EBFFF4" text-anchor="middle">Create the first usable version with focused scope.</text>

  <text x="776" y="386" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="21" font-weight="700" fill="#FFFFFF" text-anchor="middle">Launch</text>
  <text x="776" y="421" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" fill="#FFF4DE" text-anchor="middle">Activate teams, channels, and operating cadence.</text>

  <text x="992" y="386" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="21" font-weight="700" fill="#FFFFFF" text-anchor="middle">Scale</text>
  <text x="992" y="421" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" fill="#FFEAF1" text-anchor="middle">Measure adoption and expand what works.</text>

  <text x="86" y="574" width="1110" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" fill="#667384">Tip: keep each step title to one or two words; reserve the lower copy line for the outcome or handoff.</text>
</svg>
```

## Avoid in this skill
- ❌ Using five separate rectangles with arrow icons between them; the method should feel like one continuous interlocking timeline.
- ❌ Putting long paragraphs inside the chevrons; the angled sides reduce available text width.
- ❌ Applying `marker-end` to paths for chevron points; draw the arrow geometry directly as `<path>` shapes.
- ❌ Using clip paths on text or chevron paths; clipping is only reliable for `<image>` elements.
- ❌ Overlapping the text with the chevron notches; keep text centered in the stable rectangular middle of each tab.

## Composition notes
- Keep the chevron band centered horizontally, occupying roughly the middle third of the slide height.
- Use the upper-left or upper-center area for the headline; leave enough negative space above the timeline so the chevrons feel premium rather than crowded.
- Assign a distinct gradient to each step, but keep all colors within one coordinated palette to preserve continuity.
- Place badges near the top of each chevron and short copy near the bottom; this creates a consistent scanning rhythm from left to right.