# SVG Recipe — Cinematic Hero Metric Layout

## Visual mechanism
A full-bleed thematic photograph is darkened with layered navy overlays and vignette gradients, turning the slide into a cinematic backdrop. One oversized metric dominates the left-center, supported by compact uppercase context text and a sharp gold accent rule that creates a premium keynote “billboard” effect.

## SVG primitives needed
- 1× `<image>` for the full-bleed hero background photograph.
- 3× `<rect>` for dark overlay, left contrast panel, and gold metric accent bar.
- 2× `<linearGradient>` for cinematic left-to-right darkening and gold accent sheen.
- 1× `<radialGradient>` for a subtle vignette that focuses attention toward the metric.
- 1× `<filter id="heroShadow">` with `feOffset`, `feGaussianBlur`, and `feMerge` applied to the giant metric text.
- 1× `<filter id="softGlow">` with `feGaussianBlur` applied to the gold accent shape.
- 3× `<path>` for decorative diagonal light leaks / cinematic geometry.
- 6× `<text>` for eyebrow label, giant metric, contextual phrase, subcaption, small proof-point, and right-side ghost annotation.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="darkSweep" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#020617" stop-opacity="0.96"/>
      <stop offset="42%" stop-color="#0F172A" stop-opacity="0.82"/>
      <stop offset="73%" stop-color="#111827" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#020617" stop-opacity="0.72"/>
    </linearGradient>

    <linearGradient id="goldSheen" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#D97706"/>
      <stop offset="45%" stop-color="#FBBF24"/>
      <stop offset="100%" stop-color="#F59E0B"/>
    </linearGradient>

    <radialGradient id="vignette" cx="70%" cy="42%" r="78%">
      <stop offset="0%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="64%" stop-color="#000000" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.62"/>
    </radialGradient>

    <filter id="heroShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="5"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#020617"/>

  <image
    href="https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&amp;fit=crop&amp;w=1920&amp;q=85"
    x="0" y="0" width="1280" height="720"
    preserveAspectRatio="xMidYMid slice"/>

  <rect x="0" y="0" width="1280" height="720" fill="url(#darkSweep)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#vignette)"/>

  <path d="M760 0 L1280 0 L1280 150 C1110 118 970 88 760 0 Z"
        fill="#38BDF8" opacity="0.08"/>
  <path d="M900 720 L1280 720 L1280 465 C1150 560 1035 640 900 720 Z"
        fill="#FBBF24" opacity="0.075"/>
  <path d="M650 105 C810 135 970 130 1160 82"
        fill="none" stroke="#FFFFFF" stroke-width="1.2" stroke-opacity="0.18"
        stroke-dasharray="10 14"/>

  <rect x="82" y="116" width="560" height="492" rx="26"
        fill="#020617" opacity="0.34"/>
  <rect x="104" y="178" width="8" height="318" rx="4"
        fill="url(#goldSheen)" filter="url(#softGlow)" opacity="0.95"/>

  <text x="132" y="190" width="520"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="27" font-weight="700" letter-spacing="5"
        fill="#E5E7EB">
    MORE THAN
  </text>

  <rect x="132" y="216" width="320" height="7" rx="3.5"
        fill="url(#goldSheen)"/>
  <rect x="466" y="216" width="48" height="7" rx="3.5"
        fill="#FFFFFF" opacity="0.42"/>

  <text x="126" y="438" width="560"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="244" font-weight="800"
        fill="#FFFFFF" filter="url(#heroShadow)">
    35
  </text>

  <text x="144" y="502" width="690"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="36" font-weight="800" letter-spacing="1.5"
        fill="#FFFFFF">
    YEARS OF EXPERIENCE
  </text>

  <text x="146" y="548" width="575"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="400"
        fill="#CBD5E1">
    Engineering resilient technology platforms for mission-critical operations.
  </text>

  <rect x="146" y="582" width="178" height="38" rx="19"
        fill="#FFFFFF" opacity="0.11"/>
  <text x="168" y="607" width="260"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" letter-spacing="1.1"
        fill="#FDE68A">
    GLOBAL DELIVERY
  </text>

  <rect x="910" y="472" width="224" height="1.5"
        fill="#FFFFFF" opacity="0.28"/>
  <text x="910" y="452" width="270"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" letter-spacing="2.2"
        fill="#FFFFFF" opacity="0.54">
    EST. 1989
  </text>

  <text x="910" y="508" width="270"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="400"
        fill="#CBD5E1" opacity="0.54">
    Proven scale, stable execution, and long-cycle customer trust.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using a plain solid background only; the cinematic effect depends on a real photographic backdrop plus controlled darkening.
- ❌ Placing many competing KPIs on the slide; this layout is built around one heroic number.
- ❌ Applying `filter` to `<line>` elements for glow effects; use thin `<rect>` accents instead.
- ❌ Using `<mask>` to darken the image; use translucent `<rect>` overlays and gradients.
- ❌ Relying on tiny body text over detailed photo areas; keep supporting copy short and place it inside the darker left zone.

## Composition notes
- Keep the metric block left-aligned, usually starting around 10% from the left edge and centered vertically between 40–60% slide height.
- Reserve the right half for atmospheric image detail and negative space; only add faint secondary annotations there.
- Use one accent color, typically gold or red, repeated in the vertical rule, underline, and small pill label.
- The main number should feel poster-scale: roughly one-third of slide height, with strong shadow for readability over photography.