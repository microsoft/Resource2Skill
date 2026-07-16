# SVG Recipe — Staggered Title with Pill

## Visual mechanism
A low-density section divider built from oversized title words that step diagonally down the slide, with a rotated rounded “pill” crossing the composition as a playful emphasis mark. The pill adds motion and contrast while the staggered typography creates a premium editorial rhythm.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background
- 2× `<path>` for soft abstract background blobs
- 1× `<rect>` with large `rx` for the rotated decorative pill
- 1× `<rect>` with dashed stroke for a subtle secondary pill outline
- 4× `<text>` for staggered headline words, pill label, and small contextual captions
- 3× `<line>` for minimal accent rules around the title
- 2× `<linearGradient>` for the background and pill color treatment
- 1× `<radialGradient>` for a soft spotlight behind the title
- 2× `<filter>` definitions for editable glow and shadow effects applied to shapes/text

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#FFF9F0"/>
      <stop offset="48%" stop-color="#F5EFE6"/>
      <stop offset="100%" stop-color="#ECE7DE"/>
    </linearGradient>

    <radialGradient id="spotlight" cx="46%" cy="46%" r="54%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.92"/>
      <stop offset="62%" stop-color="#FFFFFF" stop-opacity="0.28"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="pillGrad" x1="650" y1="215" x2="1075" y2="325">
      <stop offset="0%" stop-color="#FFB000"/>
      <stop offset="48%" stop-color="#FF6B2C"/>
      <stop offset="100%" stop-color="#E83E8C"/>
    </linearGradient>

    <linearGradient id="inkGrad" x1="90" y1="180" x2="720" y2="540">
      <stop offset="0%" stop-color="#171717"/>
      <stop offset="100%" stop-color="#34312E"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="160%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="warmGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="16"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#spotlight)"/>

  <path d="M850,72 C980,26 1130,68 1190,172 C1258,290 1164,397 1032,366 C902,335 792,201 850,72 Z"
        fill="#FFE2B8" opacity="0.46" filter="url(#warmGlow)"/>
  <path d="M-62,522 C70,452 191,492 220,606 C244,703 115,754 -18,720 C-118,695 -165,580 -62,522 Z"
        fill="#FFD6E1" opacity="0.48" filter="url(#warmGlow)"/>

  <line x1="98" y1="132" x2="274" y2="132" stroke="#191919" stroke-width="3" opacity="0.85"/>
  <line x1="316" y1="132" x2="365" y2="132" stroke="#191919" stroke-width="3" opacity="0.3"/>
  <line x1="1040" y1="592" x2="1184" y2="592" stroke="#191919" stroke-width="3" opacity="0.18"/>

  <text x="98" y="112" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" letter-spacing="3" fill="#24211F" opacity="0.78">
    STRATEGY RESET
  </text>

  <rect x="690" y="225" width="386" height="94" rx="47" fill="url(#pillGrad)"
        transform="rotate(-10 883 272)" filter="url(#softShadow)"/>
  <rect x="668" y="209" width="426" height="124" rx="62" fill="none" stroke="#1E1E1E"
        stroke-width="2.4" stroke-dasharray="10 11" opacity="0.24"
        transform="rotate(-10 881 271)"/>

  <text x="746" y="286" width="300" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="25" font-weight="800" letter-spacing="2.4" fill="#FFFFFF"
        transform="rotate(-10 896 270)">
    SECTION 03
  </text>

  <text x="96" y="252" width="560" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="124" font-weight="800" letter-spacing="-5" fill="url(#inkGrad)">
    NEXT
  </text>

  <text x="242" y="382" width="760" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="118" font-weight="800" letter-spacing="-6" fill="url(#inkGrad)">
    GROWTH
  </text>

  <text x="132" y="514" width="580" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="124" font-weight="800" letter-spacing="-5" fill="url(#inkGrad)">
    MOVE
  </text>

  <text x="866" y="465" width="300" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="500" fill="#5C554D" opacity="0.86">
    A bold divider for a new chapter, keynote transition, or campaign launch.
  </text>

  <circle cx="826" cy="472" r="6" fill="#FF6B2C"/>
  <circle cx="849" cy="472" r="6" fill="#FFB000"/>
  <circle cx="872" cy="472" r="6" fill="#E83E8C"/>
</svg>
```

## Avoid in this skill
- ❌ Building the title as one centered text block; the technique depends on staggered word positions.
- ❌ Using a non-editable screenshot of typography; keep each title word as native `<text>`.
- ❌ Applying `clip-path` or masks to decorative shapes; clipping is unnecessary here and may be ignored on non-image elements.
- ❌ Using skew or matrix transforms for the pill; use simple `rotate(angle cx cy)` so the PowerPoint shape remains editable.

## Composition notes
- Keep the title words large and left-weighted, stepping diagonally from upper-left toward lower-left.
- Let the pill overlap the title field but not obscure critical letterforms; it should feel like a label passing through the composition.
- Use warm accent colors on the pill against a quiet neutral background for a premium, playful contrast.
- Preserve generous negative space on the right for an optional subtitle, chapter note, or speaker cue.