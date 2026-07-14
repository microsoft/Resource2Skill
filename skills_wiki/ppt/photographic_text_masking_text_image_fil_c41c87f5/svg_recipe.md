# SVG Recipe — Photographic Text Masking

## Visual mechanism
Bold display words are converted into vector letter-outline paths and used as a `clipPath` for vibrant photography. The image is visible only through the thick letterforms, making the typography feel like an editorial photo window rather than ordinary text.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 2× decorative `<ellipse>` elements for soft color atmosphere behind the headline
- 2× `<clipPath>` definitions containing compound `<path>` letter outlines, one for each photo-filled word group
- 2× `<image>` elements clipped to the letter-outline paths for the photographic text fill
- 4× duplicate `<path>` elements for editable drop shadows and subtle highlight overlays on the masked typography
- 1× `<filter id="softShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` for dimensional letter shadows
- 1× `<filter id="blobBlur">` using `feGaussianBlur` for soft background glow
- 2× `<linearGradient>` fills for background and accent shapes
- 3× `<text>` elements with explicit `width` attributes for supporting editorial labels

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#07111f"/>
      <stop offset="52%" stop-color="#0d1728"/>
      <stop offset="100%" stop-color="#101826"/>
    </linearGradient>

    <linearGradient id="goldChip" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffd35a"/>
      <stop offset="100%" stop-color="#ff8e24"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="12" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="blobBlur" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="42"/>
    </filter>

    <clipPath id="maskWordClip" clipPathUnits="userSpaceOnUse">
      <path fill-rule="evenodd" clip-rule="evenodd"
        d="M120 330 L120 190 L166 190 L221 275 L276 190 L322 190 L322 330 L272 330 L272 262 L236 330 L206 330 L170 262 L170 330 Z
           M350 330 L410 190 L482 190 L542 330 L486 330 L476 300 L416 300 L406 330 Z M431 266 L462 266 L446 224 Z
           M684 240 C660 222 626 214 606 224 C588 232 591 246 610 250 L653 260 C704 272 718 322 682 351 C638 386 560 382 515 354 L540 310 C567 328 610 338 635 326 C652 318 648 302 630 298 L595 290 C552 281 532 254 550 228 C570 200 632 205 665 226 Z
           M720 330 L720 190 L776 190 L776 250 L835 190 L902 190 L826 265 L908 330 L836 330 L776 280 L776 330 Z"/>
    </clipPath>

    <clipPath id="textWordClip" clipPathUnits="userSpaceOnUse">
      <path
        d="M170 360 L332 360 L332 406 L281 406 L281 520 L221 520 L221 406 L170 406 Z
           M354 360 L518 360 L518 405 L410 405 L410 421 L506 421 L506 462 L410 462 L410 475 L524 475 L524 520 L354 520 Z
           M538 360 L604 360 L638 405 L674 360 L741 360 L672 441 L747 520 L678 520 L638 470 L598 520 L529 520 L604 441 Z
           M765 360 L927 360 L927 406 L876 406 L876 520 L816 520 L816 406 L765 406 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <ellipse cx="250" cy="165" rx="250" ry="130" fill="#21c7ff" opacity="0.18" filter="url(#blobBlur)"/>
  <ellipse cx="980" cy="555" rx="330" ry="150" fill="#ff9a35" opacity="0.16" filter="url(#blobBlur)"/>

  <text x="88" y="86" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#8fdfff" letter-spacing="3">
    PHOTOGRAPHIC TEXT MASK
  </text>
  <text x="88" y="122" width="460" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" fill="#aab6c8">
    Bold vector letterforms become windows into high-contrast editorial imagery.
  </text>

  <rect x="86" y="600" width="350" height="46" rx="23" fill="url(#goldChip)" opacity="0.95"/>
  <text x="116" y="630" width="310" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" font-weight="800" fill="#111827" letter-spacing="1">
    IMAGE-FILLED TYPE EFFECT
  </text>

  <path fill-rule="evenodd" clip-rule="evenodd" fill="#000817" opacity="0.72" filter="url(#softShadow)"
    d="M120 330 L120 190 L166 190 L221 275 L276 190 L322 190 L322 330 L272 330 L272 262 L236 330 L206 330 L170 262 L170 330 Z
       M350 330 L410 190 L482 190 L542 330 L486 330 L476 300 L416 300 L406 330 Z M431 266 L462 266 L446 224 Z
       M684 240 C660 222 626 214 606 224 C588 232 591 246 610 250 L653 260 C704 272 718 322 682 351 C638 386 560 382 515 354 L540 310 C567 328 610 338 635 326 C652 318 648 302 630 298 L595 290 C552 281 532 254 550 228 C570 200 632 205 665 226 Z
       M720 330 L720 190 L776 190 L776 250 L835 190 L902 190 L826 265 L908 330 L836 330 L776 280 L776 330 Z"/>

  <path fill="#000817" opacity="0.70" filter="url(#softShadow)"
    d="M170 360 L332 360 L332 406 L281 406 L281 520 L221 520 L221 406 L170 406 Z
       M354 360 L518 360 L518 405 L410 405 L410 421 L506 421 L506 462 L410 462 L410 475 L524 475 L524 520 L354 520 Z
       M538 360 L604 360 L638 405 L674 360 L741 360 L672 441 L747 520 L678 520 L638 470 L598 520 L529 520 L604 441 Z
       M765 360 L927 360 L927 406 L876 406 L876 520 L816 520 L816 406 L765 406 Z"/>

  <image x="70" y="120" width="930" height="280" preserveAspectRatio="xMidYMid slice"
    href="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&amp;fit=crop&amp;w=1400&amp;q=80"
    clip-path="url(#maskWordClip)"/>

  <image x="130" y="300" width="900" height="280" preserveAspectRatio="xMidYMid slice"
    href="https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&amp;fit=crop&amp;w=1400&amp;q=80"
    clip-path="url(#textWordClip)"/>

  <path fill-rule="evenodd" clip-rule="evenodd" fill="#ffffff" opacity="0.12"
    d="M120 330 L120 190 L166 190 L221 275 L276 190 L322 190 L322 330 L272 330 L272 262 L236 330 L206 330 L170 262 L170 330 Z
       M350 330 L410 190 L482 190 L542 330 L486 330 L476 300 L416 300 L406 330 Z M431 266 L462 266 L446 224 Z
       M684 240 C660 222 626 214 606 224 C588 232 591 246 610 250 L653 260 C704 272 718 322 682 351 C638 386 560 382 515 354 L540 310 C567 328 610 338 635 326 C652 318 648 302 630 298 L595 290 C552 281 532 254 550 228 C570 200 632 205 665 226 Z
       M720 330 L720 190 L776 190 L776 250 L835 190 L902 190 L826 265 L908 330 L836 330 L776 280 L776 330 Z"/>

  <path fill="#ffffff" opacity="0.10"
    d="M170 360 L332 360 L332 406 L281 406 L281 520 L221 520 L221 406 L170 406 Z
       M354 360 L518 360 L518 405 L410 405 L410 421 L506 421 L506 462 L410 462 L410 475 L524 475 L524 520 L354 520 Z
       M538 360 L604 360 L638 405 L674 360 L741 360 L672 441 L747 520 L678 520 L638 470 L598 520 L529 520 L604 441 Z
       M765 360 L927 360 L927 406 L876 406 L876 520 L816 520 L816 406 L765 406 Z"/>

  <line x1="1030" y1="206" x2="1150" y2="206" stroke="#ffbe37" stroke-width="5" stroke-linecap="round"/>
  <line x1="1030" y1="231" x2="1110" y2="231" stroke="#38d3ff" stroke-width="5" stroke-linecap="round"/>
</svg>
```

## Avoid in this skill
- ❌ Do not put live `<text>` directly inside a `clipPath`; convert the headline to compound `<path>` outlines for reliable PowerPoint translation.
- ❌ Do not use SVG `<mask>` or CSS `background-clip:text`; those will not become editable PowerPoint shapes.
- ❌ Do not use thin or condensed type outlines; the photograph needs thick letter interiors to remain recognizable.
- ❌ Do not clip a `<rect>` or `<path>` to the text shape expecting an image-fill effect; clipping should be applied to the `<image>` element.
- ❌ Do not rely on `<pattern>` image fills for the letters; pattern fills are not preserved reliably.

## Composition notes
- Keep the masked headline enormous: 70–85% of slide width and roughly half the slide height.
- Use a quiet background so the photograph inside the letterforms provides the main color energy.
- Choose high-contrast photos with large recognizable regions; tiny detailed imagery becomes muddy inside letters.
- Add a soft duplicate-path shadow behind the clipped image to keep the photographic text readable on both dark and light backgrounds.