# SVG Recipe — Dynamic Split-Diagonal End Card

## Visual mechanism
A high-energy closing card built from oversized diagonal geometric pillars that funnel attention toward a central circular CTA. Heavy charcoal content panels sit on top of flat crimson offset shadows, creating a punchy layered outro frame for “next steps,” links, videos, or contact actions.

## SVG primitives needed
- 1× `<rect>` for the full-slide cool gray background
- 2× `<path>` for the oversized inward-leaning crimson diagonal pillars
- 2× `<rect>` for flat crimson offset shadows behind the dark content panels
- 2× `<rect>` for large charcoal video/link placeholder panels
- 2× `<path>` for subtle diagonal shine overlays inside the dark panels
- 1× `<circle>` for the central floating CTA / logo medallion
- 3× `<path>` for the simple central play/arrow brand icon
- 1× `<rect>` for the top rounded title banner
- 8× `<text>` for title, rotated banner labels, panel labels, CTA, and footer metadata
- 1× `<linearGradient>` for panel sheen
- 1× `<radialGradient>` for the central medallion
- 2× `<filter>` definitions: one soft shadow for cards, one stronger glow/shadow for the central circle

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="panelSheen" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#2f3035" stop-opacity="1"/>
      <stop offset="48%" stop-color="#161618" stop-opacity="1"/>
      <stop offset="100%" stop-color="#050506" stop-opacity="1"/>
    </linearGradient>

    <radialGradient id="centerMedallion" cx="45%" cy="35%" r="70%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="64%" stop-color="#f6f6f7"/>
      <stop offset="100%" stop-color="#d8d8dc"/>
    </radialGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="16"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="medallionGlow" x="-60%" y="-60%" width="220%" height="220%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="12"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#f5f5f7"/>

  <!-- diagonal structural pillars -->
  <path d="M118 0 L262 0 L420 720 L276 720 Z" fill="#a30f23"/>
  <path d="M1018 0 L1162 0 L1004 720 L860 720 Z" fill="#a30f23"/>

  <!-- faint extra diagonal energy strokes -->
  <path d="M315 0 L350 0 L510 720 L475 720 Z" fill="#c31934" opacity="0.18"/>
  <path d="M930 0 L965 0 L805 720 L770 720 Z" fill="#c31934" opacity="0.18"/>

  <!-- top title banner -->
  <rect x="205" y="28" width="870" height="74" rx="25" fill="#080809" filter="url(#cardShadow)"/>
  <text x="640" y="77" width="820" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="800"
        font-style="italic" fill="#ffffff" letter-spacing="1.5">
    WHAT SHOULD WE DO NEXT?
  </text>

  <!-- flat offset shadows behind panels -->
  <rect x="132" y="238" width="358" height="214" rx="8" fill="#a30f23"/>
  <rect x="790" y="238" width="358" height="214" rx="8" fill="#a30f23"/>

  <!-- dark foreground panels -->
  <rect x="104" y="210" width="358" height="214" rx="8" fill="url(#panelSheen)" filter="url(#cardShadow)"/>
  <rect x="818" y="210" width="358" height="214" rx="8" fill="url(#panelSheen)" filter="url(#cardShadow)"/>

  <!-- angular sheen inside panels -->
  <path d="M104 210 L462 210 L340 424 L104 424 Z" fill="#ffffff" opacity="0.05"/>
  <path d="M818 210 L1176 210 L1176 424 L940 424 Z" fill="#ffffff" opacity="0.05"/>

  <!-- left panel icon: report card -->
  <rect x="214" y="262" width="138" height="96" rx="12" fill="#ffffff" opacity="0.96"/>
  <rect x="238" y="285" width="90" height="10" rx="5" fill="#a30f23"/>
  <rect x="238" y="309" width="72" height="8" rx="4" fill="#7d7f87"/>
  <rect x="238" y="330" width="96" height="8" rx="4" fill="#7d7f87"/>

  <!-- right panel icon: demo screen -->
  <rect x="920" y="260" width="156" height="98" rx="10" fill="#ffffff" opacity="0.96"/>
  <path d="M982 288 L982 330 L1020 309 Z" fill="#a30f23"/>
  <rect x="948" y="373" width="100" height="10" rx="5" fill="#ffffff" opacity="0.82"/>

  <!-- center medallion -->
  <circle cx="640" cy="350" r="66" fill="url(#centerMedallion)" filter="url(#medallionGlow)"/>
  <circle cx="640" cy="350" r="61" fill="none" stroke="#ffffff" stroke-width="5"/>
  <path d="M613 318 L613 382 L670 350 Z" fill="#a30f23"/>
  <path d="M686 321 L705 321 L670 382 L651 382 Z" fill="#161618" opacity="0.18"/>
  <path d="M585 350 C585 320 607 295 640 295 C673 295 695 320 695 350"
        fill="none" stroke="#a30f23" stroke-width="7" stroke-linecap="round" opacity="0.22"/>

  <!-- rotated banner labels -->
  <text x="264" y="383" width="360" transform="rotate(78 264 383)"
        text-anchor="middle" font-family="Segoe UI, Microsoft YaHei"
        font-size="24" font-weight="800" fill="#ffffff" letter-spacing="9">
    LATEST
  </text>
  <text x="1016" y="383" width="360" transform="rotate(-78 1016 383)"
        text-anchor="middle" font-family="Segoe UI, Microsoft YaHei"
        font-size="24" font-weight="800" fill="#ffffff" letter-spacing="9">
    POPULAR
  </text>

  <!-- panel captions -->
  <text x="284" y="505" width="430" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="40" font-weight="900"
        font-style="italic" fill="#161618" letter-spacing="0.5">
    READ THE REPORT
  </text>
  <text x="996" y="505" width="430" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="40" font-weight="900"
        font-style="italic" fill="#161618" letter-spacing="0.5">
    WATCH THE DEMO
  </text>

  <!-- central CTA and footer -->
  <text x="640" y="466" width="260" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800"
        fill="#a30f23" letter-spacing="2">
    CHOOSE ONE
  </text>
  <text x="640" y="646" width="720" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="600"
        fill="#4b4d55">
    company.com/next · @company · hello@company.com
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using rotated `<rect>` elements for the diagonal pillars; off-canvas corners can become awkward. Use explicit `<path>` polygons instead.
- ❌ Applying `filter` effects to `<line>` elements for separators or arrows; filters on lines may be dropped.
- ❌ Using `<mask>` to cut diagonal panels; define the diagonal geometry directly as editable paths.
- ❌ Putting `clip-path` on text or shape elements; clipping is only safe for images in this workflow.
- ❌ Relying on CSS letter-spacing alone without enough text width; every `<text>` needs an explicit `width`.

## Composition notes
- Keep the center 25–30% of the slide visually breathable so the medallion has enough contrast between the two heavy side panels.
- Let the diagonal crimson pillars run fully off the top and bottom edges; this makes the slide feel engineered and cinematic rather than like rotated stickers.
- Use the dark content panels as the primary actionable zones, with captions directly beneath them for instant scanning.
- Maintain a strict tri-tone rhythm: pale background, crimson structure/accent, and charcoal panels; reserve white for text, icon interiors, and the central CTA circle.