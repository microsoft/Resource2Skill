# SVG Recipe — Dual Call-to-Action (CTA) Closure

## Visual mechanism
A closing slide with two large, symmetrical downward block arrows that act as visual funnels toward two explicit next-step actions. The brand/title and URL sit in the calm center channel, creating a final, directive composition that converts attention into action.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background
- 2× `<ellipse>` for soft ambient spotlight glows behind the CTA zones
- 2× `<path>` for the large left/right downward block arrows
- 2× `<path>` for subtle arrow highlight overlays
- 2× `<rect>` for rounded CTA label cards below the arrows
- 1× `<rect>` for the central URL pill
- 2× `<circle>` for small CTA icon badges
- 4× `<path>` for simple editable icon glyphs inside the badges
- 1× `<line>` for the URL underline accent
- 6× `<text>` elements for title, subtitle, URL, and CTA copy
- 2× `<linearGradient>` for background and arrow fills
- 1× `<radialGradient>` for ambient blue glows
- 1× `<filter id="softShadow">` applied to arrows and CTA cards
- 1× `<filter id="titleGlow">` applied lightly to the title text

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="720">
      <stop offset="0%" stop-color="#FAFBFD"/>
      <stop offset="58%" stop-color="#F0F3F7"/>
      <stop offset="100%" stop-color="#E3E8EE"/>
    </linearGradient>

    <linearGradient id="arrowGrad" x1="0" y1="200" x2="0" y2="585">
      <stop offset="0%" stop-color="#2A6DA8"/>
      <stop offset="52%" stop-color="#1F4E79"/>
      <stop offset="100%" stop-color="#153957"/>
    </linearGradient>

    <radialGradient id="blueGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#5EA4E4" stop-opacity="0.28"/>
      <stop offset="65%" stop-color="#5EA4E4" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#5EA4E4" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="12"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="titleGlow" x="-8%" y="-30%" width="116%" height="160%">
      <feGaussianBlur stdDeviation="1.2"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <ellipse cx="305" cy="525" rx="245" ry="150" fill="url(#blueGlow)"/>
  <ellipse cx="975" cy="525" rx="245" ry="150" fill="url(#blueGlow)"/>

  <text x="640" y="92" width="900" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="54" font-weight="800"
        fill="#111827" filter="url(#titleGlow)">Ready to keep momentum?</text>

  <text x="640" y="136" width="760" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="500"
        fill="#64748B">Choose your next step and stay connected after today’s session.</text>

  <path d="M255 205 H355 V428 H422 L305 575 L188 428 H255 Z"
        fill="url(#arrowGrad)" filter="url(#softShadow)"/>
  <path d="M925 205 H1025 V428 H1092 L975 575 L858 428 H925 Z"
        fill="url(#arrowGrad)" filter="url(#softShadow)"/>

  <path d="M274 224 H310 V437 H354 L305 501 L256 437 H292 V224 Z"
        fill="#FFFFFF" opacity="0.13"/>
  <path d="M944 224 H980 V437 H1024 L975 501 L926 437 H962 V224 Z"
        fill="#FFFFFF" opacity="0.13"/>

  <rect x="456" y="298" width="368" height="72" rx="36"
        fill="#FFFFFF" stroke="#D7E2EE" stroke-width="2" filter="url(#softShadow)"/>
  <text x="640" y="343" width="340" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="30" font-weight="800"
        fill="#1F4E79">www.expertacademy.be</text>
  <line x1="505" y1="358" x2="775" y2="358" stroke="#1F4E79" stroke-width="3" opacity="0.55"/>

  <rect x="150" y="594" width="310" height="78" rx="24"
        fill="#FFFFFF" stroke="#CFE0F2" stroke-width="2" filter="url(#softShadow)"/>
  <rect x="820" y="594" width="310" height="78" rx="24"
        fill="#FFFFFF" stroke="#CFE0F2" stroke-width="2" filter="url(#softShadow)"/>

  <circle cx="194" cy="633" r="24" fill="#1F4E79"/>
  <path d="M183 634 C191 626, 198 626, 207 634" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
  <path d="M194 619 V648" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>

  <circle cx="864" cy="633" r="24" fill="#1F4E79"/>
  <path d="M855 633 H873" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
  <path d="M865 623 L875 633 L865 643" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>

  <text x="305" y="625" width="220" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="21" font-weight="800"
        fill="#1F4E79">
    <tspan x="305" y="625">FOLLOW US</tspan>
    <tspan x="305" y="652" font-size="17" font-weight="700" fill="#315F8B">CLICK HERE</tspan>
  </text>

  <text x="975" y="625" width="220" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="21" font-weight="800"
        fill="#1F4E79">
    <tspan x="975" y="625">MORE INFO</tspan>
    <tspan x="975" y="652" font-size="17" font-weight="700" fill="#315F8B">CLICK HERE</tspan>
  </text>

  <text x="640" y="642" width="280" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="600"
        fill="#94A3B8">Thank you for joining us</text>
</svg>
```

## Avoid in this skill
- ❌ Using `marker-end` on paths for the arrows; create the block arrows as editable `<path>` shapes instead.
- ❌ Applying `filter` to `<line>` elements such as the URL underline; shadows/glows should be on rectangles, paths, or text.
- ❌ Omitting `width` on `<text>` elements; PowerPoint translation relies on explicit text box widths.
- ❌ Making the CTAs too small or too close to the slide edge; this technique depends on obvious, low-friction next actions.
- ❌ Using masks or clip paths on non-image elements for arrow effects; use layered editable paths with opacity instead.

## Composition notes
- Keep the slide highly symmetrical: arrows sit around 24% and 76% of the slide width, leaving a calm central corridor for the URL.
- Reserve the top 20% for the closing headline and one short explanatory line; avoid cluttering this area.
- Place CTA cards directly below the arrow tips so the visual flow resolves into actionable text.
- Use one dominant accent color for arrows, URL, icons, and CTA text; the background should stay quiet and neutral.