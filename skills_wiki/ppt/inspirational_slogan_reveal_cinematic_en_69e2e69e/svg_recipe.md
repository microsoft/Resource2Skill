# SVG Recipe — Inspirational Slogan Reveal (Cinematic End Page)

## Visual mechanism
A full-bleed emotional photograph is darkened with cinematic navy overlays, then layered with a giant muted watermark word/year and a sharp white slogan in the foreground. A clean white metadata band at the bottom grounds the slide and turns the ending into a polished keynote-style closing frame.

## SVG primitives needed
- 1× `<image>` for the full-bleed cinematic background photo.
- 3× `<rect>` for the dark overlay, vignette/fade layer, and bottom metadata band.
- 1× `<ellipse>` with radial gradient for a subtle horizon glow behind the slogan.
- 3× `<path>` for atmospheric diagonal light streaks and a simple editable logo mark.
- 5× `<text>` for the watermark, kicker, main slogan, metadata, date, and logo wordmark.
- 1× `<linearGradient id="darkFade">` for top/bottom cinematic shading.
- 1× `<radialGradient id="horizonGlow">` for the soft glow behind the headline.
- 1× `<linearGradient id="accentLine">` for the thin premium accent rule above the footer.
- 1× `<filter id="sloganShadow">` applied to the main slogan text for depth.
- 1× `<filter id="softGlow">` applied to background light paths for cinematic atmosphere.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="darkFade" x1="0" y1="0" x2="0" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#050712" stop-opacity="0.72"/>
      <stop offset="45%" stop-color="#0D111C" stop-opacity="0.34"/>
      <stop offset="82%" stop-color="#050712" stop-opacity="0.78"/>
      <stop offset="100%" stop-color="#050712" stop-opacity="0.92"/>
    </linearGradient>

    <radialGradient id="horizonGlow" cx="50%" cy="54%" r="48%">
      <stop offset="0%" stop-color="#5DA8FF" stop-opacity="0.34"/>
      <stop offset="42%" stop-color="#2E5F9E" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#0D111C" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="accentLine" x1="0" y1="0" x2="1280" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="18%" stop-color="#7CC7FF" stop-opacity="0.75"/>
      <stop offset="50%" stop-color="#FFFFFF" stop-opacity="0.95"/>
      <stop offset="82%" stop-color="#7CC7FF" stop-opacity="0.75"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>

    <filter id="sloganShadow" x="-8%" y="-20%" width="116%" height="150%">
      <feOffset dx="0" dy="7" result="offset"/>
      <feGaussianBlur in="offset" stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-40%" y="-80%" width="180%" height="260%">
      <feGaussianBlur stdDeviation="8"/>
    </filter>
  </defs>

  <image
    href="https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&amp;w=1600&amp;auto=format&amp;fit=crop"
    x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>

  <rect x="0" y="0" width="1280" height="720" fill="#0D111C" opacity="0.48"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#darkFade)"/>
  <ellipse cx="640" cy="396" rx="520" ry="210" fill="url(#horizonGlow)"/>

  <path d="M-40 210 C230 145, 450 125, 760 74 C950 43, 1110 24, 1340 -38"
        fill="none" stroke="#7DC7FF" stroke-width="2.2" stroke-opacity="0.22" filter="url(#softGlow)"/>
  <path d="M-80 460 C210 380, 445 353, 700 280 C915 218, 1110 160, 1370 118"
        fill="none" stroke="#FFFFFF" stroke-width="1.4" stroke-opacity="0.18" filter="url(#softGlow)"/>
  <path d="M122 112 C330 190, 485 208, 690 180 C870 155, 1015 103, 1190 70"
        fill="none" stroke="#5DA8FF" stroke-width="1.1" stroke-opacity="0.16"/>

  <text x="640" y="332" width="1280"
        text-anchor="middle"
        font-family="Segoe UI Black, Microsoft YaHei, sans-serif"
        font-size="214"
        font-weight="900"
        letter-spacing="-8"
        fill="#344B76">
    2026
  </text>

  <text x="640" y="242" width="980"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18"
        font-weight="700"
        letter-spacing="4"
        fill="#9FCBFF">
    THE NEXT ORBIT BEGINS NOW
  </text>

  <text x="640" y="365" width="1160"
        text-anchor="middle"
        font-family="Segoe UI Black, Microsoft YaHei, sans-serif"
        font-size="66"
        font-weight="900"
        letter-spacing="-1"
        fill="#FFFFFF"
        filter="url(#sloganShadow)">
    <tspan x="640" dy="0">AIM HIGH.</tspan>
    <tspan fill="#CFE9FF"> EXECUTE FASTER.</tspan>
  </text>

  <text x="640" y="430" width="820"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22"
        font-weight="400"
        fill="#D7E7F8"
        opacity="0.92">
    Strategy is momentum made visible.
  </text>

  <rect x="0" y="606" width="1280" height="114" fill="#FFFFFF"/>
  <rect x="0" y="604" width="1280" height="3" fill="url(#accentLine)"/>

  <path d="M77 656 L101 632 L125 656 L101 680 Z"
        fill="#0D2A4D"/>
  <path d="M101 641 L116 656 L101 671 L86 656 Z"
        fill="#2E9BFF"/>

  <text x="148" y="653" width="420"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18"
        font-weight="800"
        letter-spacing="1.5"
        fill="#0D111C">
    NOVA STRATEGY GROUP
  </text>

  <text x="148" y="681" width="560"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15"
        font-weight="400"
        fill="#485466">
    Presenter: Steven Chen  ·  Department of Strategy
  </text>

  <text x="1135" y="663" width="210"
        text-anchor="end"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16"
        font-weight="700"
        fill="#0D111C">
    December 2026
  </text>

  <text x="1135" y="688" width="260"
        text-anchor="end"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13"
        font-weight="400"
        fill="#697386">
    Annual Leadership Summit
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use a plain solid background; the emotional full-bleed photo is the core of the cinematic effect.
- ❌ Do not rely on `<mask>` for the dark overlay or vignette; use editable rectangles with gradients instead.
- ❌ Do not make the watermark bright white; it should sit in the middle ground as muted blue-gray typography.
- ❌ Do not place the slogan inside the white footer; the slogan belongs in the dramatic image field.
- ❌ Do not use `<foreignObject>` for multiline text; use SVG `<text>` with explicit `width` and nested `<tspan>`.

## Composition notes
- Keep the main slogan centered slightly above the vertical midpoint, leaving the image’s depth visible around it.
- Use the watermark as a graphic mass, not as readable body copy; it should be huge, low-contrast, and partially recede.
- Reserve the bottom 15–18% of the canvas for a clean white metadata band with logo, presenter, and date.
- Maintain a restrained palette: navy/black atmosphere, white headline, cool blue accents, and a crisp white footer.