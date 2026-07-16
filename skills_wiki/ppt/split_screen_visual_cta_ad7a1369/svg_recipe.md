# SVG Recipe — Split-Screen Visual CTA

## Visual mechanism
A decisive vertical split pairs an emotional full-bleed image pane with a calm text pane containing a bold promise, concise proof copy, and a high-contrast CTA. The eye lands on the photo first, then moves left-to-right or right-to-left into a structured action area with generous whitespace.

## SVG primitives needed
- 1× `<rect>` for the full-slide white base
- 1× `<rect>` for the right-side image backing color
- 1× `<image>` clipped to the right pane for the hero visual
- 1× `<clipPath>` with `<rect>` for the full-height image crop
- 2× `<linearGradient>` for photo tint and CTA button depth
- 1× `<filter id="softShadow">` applied to the CTA button and floating proof card
- 2× translucent `<rect>` overlays on the image for premium contrast and color wash
- 2× decorative `<path>` shapes for soft visual energy and directional flow
- 4× `<text>` blocks for eyebrow, headline, body copy, and CTA labels
- 1× `<rect>` rounded primary CTA button
- 1× `<rect>` subtle secondary CTA outline/button surface
- 1× `<rect>` floating proof card over the image
- 2× `<circle>` status/avatar accents inside the proof card
- 2× `<line>` or `<path>` strokes for small check/metric accents

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="rightPaneClip">
      <rect x="704" y="0" width="576" height="720" rx="0"/>
    </clipPath>

    <linearGradient id="photoWash" x1="704" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#111827" stop-opacity="0.12"/>
      <stop offset="55%" stop-color="#5B5FE0" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#050816" stop-opacity="0.45"/>
    </linearGradient>

    <linearGradient id="ctaGradient" x1="120" y1="516" x2="330" y2="592" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#7377FF"/>
      <stop offset="100%" stop-color="#4F46E5"/>
    </linearGradient>

    <linearGradient id="softLilac" x1="0" y1="0" x2="640" y2="540" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#F4F2FF" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-30%" width="140%" height="180%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="16"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>
  <rect x="704" y="0" width="576" height="720" fill="#111827"/>

  <image
    href="https://images.example.com/hero-photo-modern-team-using-product-in-bright-studio.jpg"
    x="704" y="0" width="576" height="720"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#rightPaneClip)"/>

  <rect x="704" y="0" width="576" height="720" fill="url(#photoWash)" opacity="0.95"/>
  <rect x="704" y="0" width="120" height="720" fill="#FFFFFF" opacity="0.08"/>

  <path d="M-80,96 C70,12 206,18 326,110 C450,204 560,194 668,122 L668,0 L0,0 Z"
        fill="url(#softLilac)"/>
  <path d="M666,0 C728,132 728,245 688,360 C644,488 660,608 734,720 L688,720 C618,594 612,480 650,352 C688,224 684,116 628,0 Z"
        fill="#EEF2FF"/>

  <text x="120" y="140" width="450"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" letter-spacing="2.5"
        fill="#5B5FE0">LIMITED LAUNCH OFFER</text>

  <text x="120" y="226" width="510"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="58" font-weight="800" fill="#171717">
    <tspan x="120" dy="0">Design faster</tspan>
    <tspan x="120" dy="66">than ever.</tspan>
  </text>

  <text x="120" y="360" width="500"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" font-weight="400" fill="#555B66">
    <tspan x="120" dy="0">Launch polished campaigns, client decks, and</tspan>
    <tspan x="120" dy="31">product stories with a workflow built for teams</tspan>
    <tspan x="120" dy="31">that move from idea to approval in hours.</tspan>
  </text>

  <rect x="120" y="506" width="214" height="62" rx="31"
        fill="url(#ctaGradient)" filter="url(#softShadow)"/>
  <text x="156" y="545" width="150"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" fill="#FFFFFF">Buy Now — $64</text>

  <rect x="360" y="506" width="190" height="62" rx="31"
        fill="#FFFFFF" stroke="#D8DCE8" stroke-width="1.5"/>
  <text x="395" y="545" width="130"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="650" fill="#6B7280">Try free first</text>

  <rect x="804" y="484" width="326" height="116" rx="24"
        fill="#FFFFFF" opacity="0.94" filter="url(#softShadow)"/>
  <circle cx="850" cy="542" r="27" fill="#EEF2FF"/>
  <path d="M839,542 L848,551 L864,531"
        fill="none" stroke="#5B5FE0" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="892" y="529" width="190"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="700" fill="#111827">4.9/5 customer rating</text>
  <text x="892" y="558" width="210"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="400" fill="#6B7280">Trusted by 12,000+ creative teams</text>
  <circle cx="1088" cy="546" r="6" fill="#22C55E"/>

  <path d="M118,628 C180,646 252,646 314,626"
        fill="none" stroke="#CBD5E1" stroke-width="2.5" stroke-linecap="round" stroke-dasharray="1 10"/>
</svg>
```

## Avoid in this skill
- ❌ Using a plain rectangle placeholder instead of a real or clearly indicated hero photo; the split-screen pattern depends on emotional visual contrast.
- ❌ Applying `clip-path` to decorative shapes or text; use clipping only on the `<image>` crop.
- ❌ Making both panes equally busy; the text pane should remain calm and readable.
- ❌ Low-contrast CTA colors or multiple competing primary buttons.
- ❌ Center-aligning all content; the premium version relies on a strong left-aligned text axis.

## Composition notes
- Keep the image pane around 40–50% of slide width; the content pane needs enough room for a two-line headline and button row.
- Place the headline in the upper-middle of the text pane, not at the very top; CTA buttons should sit below the body copy with clear breathing room.
- Use one vivid accent color repeatedly: eyebrow, CTA, and small proof-card icon are enough.
- Add a subtle image wash or overlay so the photo feels integrated rather than pasted on.