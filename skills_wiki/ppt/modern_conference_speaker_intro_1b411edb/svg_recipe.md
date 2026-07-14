# SVG Recipe — Modern Conference Speaker Intro

## Visual mechanism
A crisp asymmetrical speaker-intro slide: the left 40% acts as a stable conference branding panel, while the right 60% is a large speaker/session photo card with a translucent lower information band. A bold rotated accent diamond bridges the panels, breaking the grid and adding keynote-style depth.

## SVG primitives needed
- 1× `<rect>` for the white slide background
- 1× `<rect>` for the subtle left branding panel tint
- 1× `<image>` clipped into a rounded photo card for the speaker/event image
- 1× `<clipPath>` with rounded `<rect>` for the photo crop
- 2× `<path>` for rotated diamond accent shapes
- 1× `<rect>` for the translucent session-info overlay on top of the photo
- 2× `<linearGradient>` for soft background and overlay depth
- 1× `<radialGradient>` for a faint spotlight behind the branding panel
- 2× `<filter>` definitions: one soft drop shadow for the photo card, one glow for the accent diamond
- 1× `<line>` for the slim vertical divider/accent rule
- Multiple `<text>` elements with explicit `width` attributes for conference branding, section title, session title, and speaker details
- Nested `<tspan>` elements for inline color and hierarchy inside title text

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="leftWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="62%" stop-color="#FFF8F7"/>
      <stop offset="100%" stop-color="#FDECEA"/>
    </linearGradient>

    <linearGradient id="overlayPeach" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFF4F2" stop-opacity="0.88"/>
      <stop offset="100%" stop-color="#F8D8D4" stop-opacity="0.92"/>
    </linearGradient>

    <radialGradient id="softSpot" cx="28%" cy="34%" r="62%">
      <stop offset="0%" stop-color="#EB5757" stop-opacity="0.12"/>
      <stop offset="55%" stop-color="#EB5757" stop-opacity="0.04"/>
      <stop offset="100%" stop-color="#EB5757" stop-opacity="0"/>
    </radialGradient>

    <filter id="photoShadow" x="-12%" y="-12%" width="124%" height="130%">
      <feOffset dx="0" dy="16"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="accentGlow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>

    <clipPath id="photoClip">
      <rect x="662" y="86" width="526" height="548" rx="26" ry="26"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>
  <rect x="0" y="0" width="520" height="720" fill="url(#leftWash)"/>
  <rect x="0" y="0" width="520" height="720" fill="url(#softSpot)"/>

  <path d="M76 54 L142 120 L76 186 L10 120 Z" fill="#EB5757"/>
  <path d="M555 455 L692 592 L555 729 L418 592 Z" fill="#EB5757" opacity="0.18" filter="url(#accentGlow)"/>
  <path d="M548 466 L676 594 L548 722 L420 594 Z" fill="#EB5757"/>

  <line x1="514" y1="96" x2="514" y2="624" stroke="#EB5757" stroke-width="4" opacity="0.28"/>

  <rect x="662" y="86" width="526" height="548" rx="26" ry="26" fill="#FFFFFF" filter="url(#photoShadow)"/>

  <image
    href="https://images.unsplash.com/photo-1543269865-cbf427effbad?w=1200&amp;auto=format&amp;fit=crop"
    x="662" y="86" width="526" height="548"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#photoClip)"/>

  <rect x="662" y="492" width="526" height="142" rx="0" ry="0" fill="url(#overlayPeach)" opacity="0.96"/>

  <text x="92" y="136" width="360"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="48" font-weight="800" fill="#111111">
    Laravel<tspan fill="#EB5757">Conf</tspan>
  </text>

  <text x="94" y="176" width="300"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="700" letter-spacing="1.8" fill="#EB5757">
    TAIWAN 2026
  </text>

  <text x="94" y="213" width="370"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" fill="#777777">
    from {{$idea}} to {{$production}}
  </text>

  <text x="92" y="342" width="370"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="54" font-weight="800" fill="#111111">
    議程介紹
  </text>

  <text x="96" y="388" width="340"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" fill="#888888">
    KEYNOTE SPEAKER INTRODUCTION
  </text>

  <text x="96" y="590" width="350"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="700" letter-spacing="2.2" fill="#EB5757">
    MAIN STAGE · 09:30 AM
  </text>

  <text x="704" y="540" width="420"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="30" font-weight="800" fill="#111111">
    開源之路：從解決問題到
  </text>

  <text x="704" y="578" width="420"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="30" font-weight="800" fill="#111111">
    解決大家的問題
  </text>

  <text x="704" y="615" width="300"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" font-weight="700" fill="#EB5757">
    周建毅 (Miles)
  </text>

  <text x="905" y="615" width="240"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" fill="#666666">
    一零四資訊科技 資深工程師
  </text>

  <text x="1130" y="122" width="80"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="700" letter-spacing="2" fill="#FFFFFF" opacity="0.86">
    LIVE
  </text>
</svg>
```

## Avoid in this skill
- ❌ Applying `clip-path` to the translucent overlay rectangle; keep clipping only on the `<image>` for reliable translation.
- ❌ Using `<mask>` to fade the photo or overlay; use semi-transparent fills and gradients instead.
- ❌ Building the diamond accents with `<use>` or `<symbol>`; draw each diamond as its own editable `<path>`.
- ❌ Relying on a background-only photo without the overlay band; speaker/session text will become illegible on busy images.
- ❌ Center-aligning all content; the technique depends on strong left alignment and asymmetric tension.

## Composition notes
- Keep the left branding panel to roughly 38–42% of slide width; it should feel calm, editorial, and reusable across a conference deck.
- Place the photo card on the right with generous top/bottom margins, then anchor the speaker/session overlay to the card’s bottom quarter.
- Let one large accent diamond cross the panel boundary near the lower middle; it visually ties branding and speaker content together.
- Use a minimal palette: white/near-white, charcoal text, muted gray secondary text, and one saturated conference accent color.