# SVG Recipe — Image-Filled Typography

## Visual mechanism
Use the letterforms as a vector clipping path so a photo is visible only inside thick, oversized typography. Add a duplicated shadow/outline path behind the clipped image to make the image-filled word feel dimensional and premium rather than flat.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 3× `<ellipse>` for soft atmospheric glow fields behind the type
- 1× `<clipPath>` containing 1× compound `<path>` for the outlined word shape
- 1× clipped `<image>` for the photo fill inside the typography
- 3× duplicated compound `<path>` for text shadow, subtle dark base, and highlight sheen
- 1× `<path>` for the thin white letter outline
- 2× `<line>` for small editorial accent rules
- 3× `<text>` for supporting headline metadata and subtitle copy
- 2× `<linearGradient>` for the background and photo sheen
- 1× `<radialGradient>` for soft color bloom
- 2× `<filter>` using `feGaussianBlur` / `feOffset + feGaussianBlur + feMerge` for glow and shadow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#0A1020"/>
      <stop offset="0.55" stop-color="#111827"/>
      <stop offset="1" stop-color="#05070D"/>
    </linearGradient>

    <radialGradient id="bloom" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#65D6C5" stop-opacity="0.55"/>
      <stop offset="0.55" stop-color="#2F7DE1" stop-opacity="0.20"/>
      <stop offset="1" stop-color="#2F7DE1" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="letterSheen" x1="80" y1="210" x2="1200" y2="455" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.40"/>
      <stop offset="0.28" stop-color="#FFFFFF" stop-opacity="0.06"/>
      <stop offset="0.62" stop-color="#FFFFFF" stop-opacity="0.18"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>

    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="36"/>
    </filter>

    <filter id="typeShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="visionClip" clipPathUnits="userSpaceOnUse">
      <path fill-rule="evenodd" clip-rule="evenodd" d="
        M80 220 L138 220 L190 392 L242 220 L300 220 L225 462 L155 462 Z
        M326 220 H392 V462 H326 Z
        M425 220 H620 V274 H492 V312 H612 V462 H418 V408 H546 V362 H425 Z
        M648 220 H714 V462 H648 Z
        M762 220 H913 C949 220 974 245 974 281 V401 C974 437 949 462 913 462 H762 C726 462 701 437 701 401 V281 C701 245 726 220 762 220 Z
        M779 282 V400 H896 V282 Z
        M1005 220 H1067 L1180 354 V220 H1240 V462 H1179 L1065 326 V462 H1005 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <ellipse cx="250" cy="125" rx="270" ry="140" fill="url(#bloom)" filter="url(#softGlow)" opacity="0.65"/>
  <ellipse cx="1030" cy="575" rx="330" ry="165" fill="#6D5DF6" filter="url(#softGlow)" opacity="0.22"/>
  <ellipse cx="680" cy="370" rx="500" ry="115" fill="#0EA5E9" filter="url(#softGlow)" opacity="0.12"/>

  <text x="82" y="90" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" letter-spacing="4" fill="#9FB3C8" opacity="0.86">
    FUTURE GROWTH BRIEFING
  </text>
  <line x1="82" y1="112" x2="210" y2="112" stroke="#65D6C5" stroke-width="3"/>
  <line x1="218" y1="112" x2="280" y2="112" stroke="#FFFFFF" stroke-width="3" opacity="0.28"/>

  <path fill="#000000" opacity="0.36" filter="url(#typeShadow)" d="
    M80 220 L138 220 L190 392 L242 220 L300 220 L225 462 L155 462 Z
    M326 220 H392 V462 H326 Z
    M425 220 H620 V274 H492 V312 H612 V462 H418 V408 H546 V362 H425 Z
    M648 220 H714 V462 H648 Z
    M762 220 H913 C949 220 974 245 974 281 V401 C974 437 949 462 913 462 H762 C726 462 701 437 701 401 V281 C701 245 726 220 762 220 Z
    M779 282 V400 H896 V282 Z
    M1005 220 H1067 L1180 354 V220 H1240 V462 H1179 L1065 326 V462 H1005 Z" fill-rule="evenodd"/>

  <image x="65" y="190" width="1190" height="315"
         href="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee7?q=80&w=2200&auto=format&fit=crop"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#visionClip)"/>

  <path fill="#06111F" opacity="0.18" d="
    M80 220 L138 220 L190 392 L242 220 L300 220 L225 462 L155 462 Z
    M326 220 H392 V462 H326 Z
    M425 220 H620 V274 H492 V312 H612 V462 H418 V408 H546 V362 H425 Z
    M648 220 H714 V462 H648 Z
    M762 220 H913 C949 220 974 245 974 281 V401 C974 437 949 462 913 462 H762 C726 462 701 437 701 401 V281 C701 245 726 220 762 220 Z
    M779 282 V400 H896 V282 Z
    M1005 220 H1067 L1180 354 V220 H1240 V462 H1179 L1065 326 V462 H1005 Z" fill-rule="evenodd"/>

  <path fill="url(#letterSheen)" opacity="0.82" d="
    M80 220 L138 220 L190 392 L242 220 L300 220 L225 462 L155 462 Z
    M326 220 H392 V462 H326 Z
    M425 220 H620 V274 H492 V312 H612 V462 H418 V408 H546 V362 H425 Z
    M648 220 H714 V462 H648 Z
    M762 220 H913 C949 220 974 245 974 281 V401 C974 437 949 462 913 462 H762 C726 462 701 437 701 401 V281 C701 245 726 220 762 220 Z
    M779 282 V400 H896 V282 Z
    M1005 220 H1067 L1180 354 V220 H1240 V462 H1179 L1065 326 V462 H1005 Z" fill-rule="evenodd"/>

  <path fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-opacity="0.50" d="
    M80 220 L138 220 L190 392 L242 220 L300 220 L225 462 L155 462 Z
    M326 220 H392 V462 H326 Z
    M425 220 H620 V274 H492 V312 H612 V462 H418 V408 H546 V362 H425 Z
    M648 220 H714 V462 H648 Z
    M762 220 H913 C949 220 974 245 974 281 V401 C974 437 949 462 913 462 H762 C726 462 701 437 701 401 V281 C701 245 726 220 762 220 Z
    M779 282 V400 H896 V282 Z
    M1005 220 H1067 L1180 354 V220 H1240 V462 H1179 L1065 326 V462 H1005 Z" fill-rule="evenodd"/>

  <text x="84" y="555" width="780" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="28" font-weight="600" fill="#FFFFFF">
    Turning market signals into a focused strategic direction
  </text>
  <text x="84" y="596" width="710" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" fill="#A8B3C7">
    Image-filled typography works best when the word is short, bold, and paired with photography that has strong contrast and recognizable texture.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<pattern>` fills for the photo texture; pattern fills are not reliably preserved.
- ❌ Do not rely on live `<text>` as the clipping object. Convert the word to compound `<path>` outlines and apply the `clip-path` to the `<image>`.
- ❌ Do not apply `clip-path` to `<text>` or decorative `<path>` elements; for this workflow, apply the clip only to the `<image>`.
- ❌ Avoid thin, condensed, or script fonts because the photo will not have enough visible surface area.
- ❌ Avoid low-contrast images; the typography needs clear light/dark variation to read as both word and image.

## Composition notes
- Keep the image-filled word huge, occupying roughly 60–75% of slide width; this is the visual hero.
- Use a calm, low-detail background so the photo texture inside the letters remains the focal point.
- Short words perform best: 4–8 letters with heavy geometric or slab-serif outlines.
- Add only small supporting text above or below the word; leave generous negative space around the typography.