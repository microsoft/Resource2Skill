# SVG Recipe — Geometric Offset Underlay Accent

## Visual mechanism
Crop a hero image into a strong geometric polygon, then place an identical solid-color polygon behind it, shifted down and right. The offset underlay creates a crisp editorial “flat shadow” that breaks the grid while keeping the image and text layout clean and executive-ready.

## SVG primitives needed
- 1× `<rect>` for the clean slide background
- 1× `<linearGradient>` for a very subtle background wash
- 1× `<clipPath>` with a `<path>` defining the polygon crop shape
- 1× `<image>` clipped to the polygon for the hero visual
- 1× `<path>` for the offset accent underlay
- 1× `<path>` for the white foreground image outline
- 1× `<filter id="softShadow">` applied to the accent underlay for slight dimensionality
- 3× small `<rect>` elements for accent rules and label chips
- 2× `<circle>` elements for decorative data markers
- 5× `<text>` elements with explicit `width` for title, body, label, and metrics

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="72%" stop-color="#F7FBFA"/>
      <stop offset="100%" stop-color="#EEF7F5"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="10" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="hexClip" clipPathUnits="userSpaceOnUse">
      <path d="M154 360 L254 187 L454 187 L554 360 L454 533 L254 533 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <!-- Offset underlay: same geometry as image crop, shifted down and right -->
  <path d="M154 360 L254 187 L454 187 L554 360 L454 533 L254 533 Z"
        transform="translate(42 38)"
        fill="#009688"
        filter="url(#softShadow)"/>

  <!-- Secondary offset sliver for richer brand layering -->
  <path d="M154 360 L254 187 L454 187 L554 360 L454 533 L254 533 Z"
        transform="translate(70 64)"
        fill="#CDEEEA"/>

  <!-- Cropped hero image: clip-path is applied only to the image -->
  <image x="120" y="150" width="470" height="470"
         href="https://images.unsplash.com/photo-1551836022-d5d88e9218df?q=80&amp;w=900&amp;auto=format&amp;fit=crop"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#hexClip)"/>

  <!-- White outline separates photo from accent underlay -->
  <path d="M154 360 L254 187 L454 187 L554 360 L454 533 L254 533 Z"
        fill="none"
        stroke="#FFFFFF"
        stroke-width="9"
        stroke-linejoin="round"/>

  <!-- Decorative data markers near the visual asset -->
  <circle cx="586" cy="214" r="8" fill="#009688"/>
  <circle cx="610" cy="214" r="8" fill="#B2DFDB"/>
  <rect x="102" y="548" width="154" height="42" rx="21" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="126" y="575" width="110" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="700" fill="#009688">+34% QoQ</text>

  <!-- Text column -->
  <rect x="710" y="168" width="86" height="6" rx="3" fill="#009688"/>
  <text x="710" y="218" width="430" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="54" font-weight="800" fill="#1E1E1E" letter-spacing="-1">
    <tspan x="710" dy="0">Geometric</tspan>
    <tspan x="710" dy="62">Image Accent</tspan>
  </text>

  <text x="713" y="365" width="430" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="400" fill="#666666">
    <tspan x="713" dy="0">Use a cropped polygon image with an</tspan>
    <tspan x="713" dy="34">offset brand-color underlay to create</tspan>
    <tspan x="713" dy="34">depth, motion, and editorial polish.</tspan>
  </text>

  <!-- Supporting metric card -->
  <rect x="710" y="490" width="360" height="96" rx="24" fill="#FFFFFF" filter="url(#softShadow)"/>
  <rect x="736" y="518" width="6" height="42" rx="3" fill="#009688"/>
  <text x="762" y="536" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="700" fill="#009688" letter-spacing="1.2">VISUAL PRIORITY</text>
  <text x="762" y="566" width="270" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="750" fill="#222222">Hero image leads the story</text>

  <!-- Fine baseline accent -->
  <rect x="710" y="624" width="310" height="2" rx="1" fill="#DDEDEA"/>
  <rect x="710" y="624" width="112" height="2" rx="1" fill="#009688"/>
</svg>
```

## Avoid in this skill
- ❌ Applying `clip-path` to the underlay or outline shape; only the `<image>` should be clipped.
- ❌ Using `<mask>` to create the polygon crop; masks are not reliable for editable PPT output.
- ❌ Using `<use href="#hex">` to duplicate the polygon; repeat the path data directly instead.
- ❌ Adding a filter to `<line>` elements; use thin rounded `<rect>` accents instead.
- ❌ Letting the image stretch without `preserveAspectRatio="xMidYMid slice"`; it weakens the premium crop effect.

## Composition notes
- Keep the polygon image on one side, occupying roughly 38–45% of slide width; the text column should breathe on the opposite side.
- Offset the underlay by about 35–55 px down and right so it reads as a deliberate brand accent, not a misalignment.
- Use a crisp white stroke around the clipped image to separate the photo from the colored underlay.
- Repeat the underlay color in small rules, chips, or metric highlights to make the accent feel integrated rather than decorative.