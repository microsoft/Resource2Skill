# SVG Recipe — Blank Canvas

## Visual mechanism
A premium “blank” slide is not merely empty: it uses a calm field of negative space with barely perceptible tonal gradients, soft edge glows, and an optional centered statement. The result feels intentional enough for a section divider or closing slide while remaining visually quiet.

## SVG primitives needed
- 1× `<rect>` for the full-slide background wash
- 2× `<rect>` for subtle vignette / tonal overlay bands
- 3× `<ellipse>` for very soft atmospheric glows near the canvas edges
- 2× `<line>` for optional ultra-faint alignment/horizon accents
- 1× `<text>` with nested `<tspan>` for the optional centered message
- 1× `<linearGradient id="bgWash">` for the base background
- 2× `<radialGradient>` for soft peripheral light blooms
- 1× `<filter id="softBlur">` using `feGaussianBlur` for blurred glow shapes

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#F8FAFC"/>
      <stop offset="42%" stop-color="#F4F7FB"/>
      <stop offset="100%" stop-color="#EEF2F7"/>
    </linearGradient>

    <linearGradient id="topVeil" x1="0" y1="0" x2="0" y2="360" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.72"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="bottomVeil" x1="0" y1="720" x2="0" y2="360" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#DDE6F1" stop-opacity="0.42"/>
      <stop offset="100%" stop-color="#DDE6F1" stop-opacity="0"/>
    </linearGradient>

    <radialGradient id="leftGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#BFD7FF" stop-opacity="0.42"/>
      <stop offset="70%" stop-color="#BFD7FF" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#BFD7FF" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="rightGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#D7C7FF" stop-opacity="0.28"/>
      <stop offset="72%" stop-color="#D7C7FF" stop-opacity="0.07"/>
      <stop offset="100%" stop-color="#D7C7FF" stop-opacity="0"/>
    </radialGradient>

    <filter id="softBlur" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="34"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <ellipse cx="20" cy="145" rx="310" ry="260" fill="url(#leftGlow)" filter="url(#softBlur)"/>
  <ellipse cx="1210" cy="610" rx="330" ry="230" fill="url(#rightGlow)" filter="url(#softBlur)"/>
  <ellipse cx="735" cy="-40" rx="480" ry="140" fill="#FFFFFF" opacity="0.38" filter="url(#softBlur)"/>

  <rect x="0" y="0" width="1280" height="360" fill="url(#topVeil)"/>
  <rect x="0" y="360" width="1280" height="360" fill="url(#bottomVeil)"/>

  <line x1="160" y1="361" x2="1120" y2="361" stroke="#8FA2B8" stroke-opacity="0.10" stroke-width="1"/>
  <line x1="520" y1="525" x2="760" y2="525" stroke="#8FA2B8" stroke-opacity="0.16" stroke-width="1"/>

  <text
    x="640"
    y="337"
    width="760"
    text-anchor="middle"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="46"
    font-weight="600"
    letter-spacing="-0.8"
    fill="#182233">
    <tspan x="640">Begin with clarity</tspan>
  </text>

  <text
    x="640"
    y="382"
    width="620"
    text-anchor="middle"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="17"
    font-weight="400"
    letter-spacing="2.2"
    fill="#5C6B7A"
    opacity="0.72">
    <tspan x="640">A QUIET SPACE FOR THE NEXT IDEA</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Dense decorative grids, cards, icons, or chart furniture; this layout depends on restraint.
- ❌ `<pattern>` fills for texture; they may be dropped and can make the blank canvas feel noisy.
- ❌ Large borders or heavy shadows that frame the slide too aggressively.
- ❌ Text without an explicit `width` attribute; centered statements can clip or reflow unexpectedly in PowerPoint.
- ❌ Applying blur filters to `<line>` elements; use blurred ellipses or paths for atmosphere instead.

## Composition notes
- Keep the center 50–60% of the slide mostly empty; the optional message should feel suspended in open space.
- Use atmosphere at the edges, not behind the text: soft glows belong in corners or beyond the canvas boundary.
- The message should be short, ideally 2–6 words; remove the subtitle for a purer divider.
- For a truly blank transition slide, delete both `<text>` elements while keeping the background gradients and faint glows.