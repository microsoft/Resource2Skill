# SVG Recipe — Three Circle Focus

## Visual mechanism
Three large, evenly spaced concentric circles create a bold “focus row” for three features, steps, or pillars. Each circle combines a glowing outer aura, nested rings, a small numbered badge, an icon-like center mark, and a label, with a concise footer description anchoring the whole slide.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark gradient background
- 3× blurred `<ellipse>` / `<circle>` shapes for atmospheric colored glows behind each focus circle
- 1× `<line>` for the subtle dashed connector running through the three circles
- 9× `<circle>` for the three concentric focus modules: outer ring, middle translucent fill, inner core
- 3× small `<circle>` badges for step numbers
- 6–9× `<path>` for simple editable center icons and decorative accents inside the circles
- 1× `<rect>` for the translucent footer description panel
- Multiple `<text>` elements with explicit `width` attributes for headline, circle labels, badge numbers, and footer text
- 3× `<radialGradient>` for colored circle fills and glows
- 1× `<linearGradient>` for the slide background
- 2× `<filter>` definitions: one soft glow filter for circles, one shadow filter for the footer card and major discs

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#071323"/>
      <stop offset="52%" stop-color="#0B1B33"/>
      <stop offset="100%" stop-color="#101827"/>
    </linearGradient>

    <radialGradient id="blueDisc" cx="50%" cy="42%" r="62%">
      <stop offset="0%" stop-color="#D7F5FF" stop-opacity="0.95"/>
      <stop offset="38%" stop-color="#39BDF8" stop-opacity="0.88"/>
      <stop offset="100%" stop-color="#1454D9" stop-opacity="0.78"/>
    </radialGradient>

    <radialGradient id="violetDisc" cx="50%" cy="42%" r="62%">
      <stop offset="0%" stop-color="#F3E8FF" stop-opacity="0.95"/>
      <stop offset="40%" stop-color="#A855F7" stop-opacity="0.88"/>
      <stop offset="100%" stop-color="#5B21B6" stop-opacity="0.78"/>
    </radialGradient>

    <radialGradient id="tealDisc" cx="50%" cy="42%" r="62%">
      <stop offset="0%" stop-color="#E6FFFA" stop-opacity="0.95"/>
      <stop offset="40%" stop-color="#2DD4BF" stop-opacity="0.88"/>
      <stop offset="100%" stop-color="#047C7A" stop-opacity="0.78"/>
    </radialGradient>

    <linearGradient id="badgeGold" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFF7B8"/>
      <stop offset="50%" stop-color="#F8C84E"/>
      <stop offset="100%" stop-color="#E18A16"/>
    </linearGradient>

    <filter id="softGlow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="cardShadow" x="-40%" y="-40%" width="180%" height="180%">
      <feOffset dx="0" dy="12" result="off"/>
      <feGaussianBlur in="off" stdDeviation="16" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <circle cx="180" cy="110" r="180" fill="#1D4ED8" opacity="0.14" filter="url(#softGlow)"/>
  <circle cx="1100" cy="130" r="210" fill="#7C3AED" opacity="0.12" filter="url(#softGlow)"/>
  <ellipse cx="650" cy="660" rx="430" ry="90" fill="#14B8A6" opacity="0.10" filter="url(#softGlow)"/>

  <text x="90" y="74" width="1100" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="38" font-weight="700" fill="#F8FAFC">
    Three moments that concentrate execution
  </text>
  <text x="92" y="112" width="920" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#9FB3C8">
    Use this shell when three capabilities, stages, or choices need equal visual weight with a premium keynote feel.
  </text>

  <line x1="300" y1="330" x2="980" y2="330" stroke="#7DD3FC" stroke-width="2.5" stroke-opacity="0.38" stroke-dasharray="10 14"/>

  <circle cx="290" cy="330" r="145" fill="#1D4ED8" opacity="0.16" filter="url(#softGlow)"/>
  <circle cx="290" cy="330" r="122" fill="#071323" opacity="0.75" stroke="#7DD3FC" stroke-width="2.5"/>
  <circle cx="290" cy="330" r="98" fill="url(#blueDisc)" opacity="0.93" filter="url(#cardShadow)"/>
  <circle cx="290" cy="330" r="64" fill="#071323" opacity="0.32" stroke="#FFFFFF" stroke-opacity="0.32" stroke-width="1.5"/>
  <circle cx="206" cy="236" r="28" fill="url(#badgeGold)" stroke="#FFF3B0" stroke-width="2"/>
  <text x="194" y="245" width="24" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="800" fill="#172033">1</text>
  <path d="M258 326 C258 304 274 290 294 290 C318 290 333 307 333 329 C333 352 317 369 293 369 C274 369 258 352 258 326 Z" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round"/>
  <path d="M292 303 L292 330 L316 344" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="190" y="503" width="200" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="700" text-anchor="middle" fill="#F8FAFC">
    Discover Signal
  </text>
  <text x="190" y="532" width="200" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" text-anchor="middle" fill="#AFC2D6">
    Separate weak noise from the few inputs that matter.
  </text>

  <circle cx="640" cy="330" r="150" fill="#7C3AED" opacity="0.17" filter="url(#softGlow)"/>
  <circle cx="640" cy="330" r="126" fill="#071323" opacity="0.78" stroke="#C084FC" stroke-width="2.5"/>
  <circle cx="640" cy="330" r="101" fill="url(#violetDisc)" opacity="0.94" filter="url(#cardShadow)"/>
  <circle cx="640" cy="330" r="66" fill="#071323" opacity="0.30" stroke="#FFFFFF" stroke-opacity="0.34" stroke-width="1.5"/>
  <circle cx="556" cy="236" r="28" fill="url(#badgeGold)" stroke="#FFF3B0" stroke-width="2"/>
  <text x="544" y="245" width="24" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="800" fill="#172033">2</text>
  <path d="M600 346 L640 296 L680 346 Z" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linejoin="round"/>
  <path d="M613 346 L613 365 L667 365 L667 346" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M640 309 L640 347" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round"/>
  <text x="540" y="503" width="200" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="700" text-anchor="middle" fill="#F8FAFC">
    Align Teams
  </text>
  <text x="540" y="532" width="200" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" text-anchor="middle" fill="#AFC2D6">
    Convert the signal into a shared operating direction.
  </text>

  <circle cx="990" cy="330" r="145" fill="#14B8A6" opacity="0.16" filter="url(#softGlow)"/>
  <circle cx="990" cy="330" r="122" fill="#071323" opacity="0.75" stroke="#5EEAD4" stroke-width="2.5"/>
  <circle cx="990" cy="330" r="98" fill="url(#tealDisc)" opacity="0.93" filter="url(#cardShadow)"/>
  <circle cx="990" cy="330" r="64" fill="#071323" opacity="0.32" stroke="#FFFFFF" stroke-opacity="0.32" stroke-width="1.5"/>
  <circle cx="906" cy="236" r="28" fill="url(#badgeGold)" stroke="#FFF3B0" stroke-width="2"/>
  <text x="894" y="245" width="24" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="800" fill="#172033">3</text>
  <path d="M948 352 C965 318 991 300 1028 300" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round"/>
  <path d="M1010 286 L1032 300 L1016 322" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M955 370 L1025 370" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round"/>
  <text x="890" y="503" width="200" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="700" text-anchor="middle" fill="#F8FAFC">
    Scale Outcome
  </text>
  <text x="890" y="532" width="200" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" text-anchor="middle" fill="#AFC2D6">
    Turn the aligned motion into measurable market impact.
  </text>

  <rect x="180" y="590" width="920" height="74" rx="22" fill="#0F2742" opacity="0.82" stroke="#2B6A8F" stroke-opacity="0.65" filter="url(#cardShadow)"/>
  <text x="230" y="624" width="820" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="600" fill="#E2F4FF">
    Best used as a feature-grid or three-step narrative: one short label per circle, then a single sentence that explains why the trio matters together.
  </text>
  <text x="230" y="650" width="820" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#9FB3C8">
    Keep copy tight; the circles carry the emphasis, while the footer provides executive-level interpretation.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Adding long paragraphs inside the circles; the circular modules work best with icon + short label only.
- ❌ Using `marker-end` on curved connector paths; if arrows are needed, draw arrowheads manually with small `<path>` shapes.
- ❌ Applying filters to `<line>` connectors; use opacity and dash styling instead.
- ❌ Clipping non-image elements into circles; build the rings directly with `<circle>` primitives.
- ❌ Overcrowding with more than three focus nodes, which weakens the “three pillars” visual rhythm.

## Composition notes
- Place the three circles across the horizontal centerline, with generous spacing so each module feels like a standalone focal object.
- Keep the headline in the top-left or top-center, leaving the circle row as the dominant visual mass.
- Use one accent hue per circle, but repeat the same gold badge treatment to unify the set.
- Reserve the bottom 15–20% of the slide for a single translucent description panel or takeaway sentence.