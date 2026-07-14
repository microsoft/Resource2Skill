# SVG Recipe — Cinematic Spotlight & Blur Extract

## Visual mechanism
A single photo is split into two visual states: a blurred grayscale full-slide background and sharp full-color cropped “extract” cards from the same source image. The color extracts are shifted downward so they overlap a dark lower-third banner, creating a cinematic depth-of-field reveal.

## SVG primitives needed
- 1× `<image>` for the preprocessed blurred grayscale full-slide background
- 4× `<image>` for full-color crop extracts from the original photo, each clipped to a card window
- 4× `<clipPath>` with rounded `<rect>` for sharp floating image-card crops
- 4× shadow `<rect>` behind the extract cards using a shared drop-shadow filter
- 4× outline `<rect>` for subtle white card borders/highlights
- 1× dark lower-third `<rect>` banner for the text anchor plane
- 2× gradient overlay `<rect>` elements for vignette and cinematic contrast
- 1× `<linearGradient>` for top/bottom atmospheric darkening
- 1× `<filter id="cardShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge`
- Multiple `<text>` elements with explicit `width` for title, names, roles, and caption metadata

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="cinemaVignette" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#05070A" stop-opacity="0.58"/>
      <stop offset="38%" stop-color="#05070A" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#05070A" stop-opacity="0.78"/>
    </linearGradient>

    <linearGradient id="bannerSheen" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#11151C"/>
      <stop offset="48%" stop-color="#1A1F28"/>
      <stop offset="100%" stop-color="#0D1016"/>
    </linearGradient>

    <filter id="cardShadow" x="-25%" y="-25%" width="150%" height="160%">
      <feOffset dx="0" dy="18" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="16" result="blur"/>
      <feColorMatrix in="blur" type="matrix"
        values="0 0 0 0 0
                0 0 0 0 0
                0 0 0 0 0
                0 0 0 .42 0" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="cropAlex"><rect x="121" y="205" width="210" height="310" rx="18"/></clipPath>
    <clipPath id="cropJordan"><rect x="386" y="178" width="210" height="310" rx="18"/></clipPath>
    <clipPath id="cropTaylor"><rect x="651" y="198" width="210" height="310" rx="18"/></clipPath>
    <clipPath id="cropCasey"><rect x="916" y="170" width="210" height="310" rx="18"/></clipPath>
  </defs>

  <!-- Pre-render this asset from the same source photo: grayscale + heavy Gaussian blur. -->
  <image x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/team-photo-grayscale-blur-20px-16x9.png"/>

  <!-- Cinematic darkening over the blurred background. -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#cinemaVignette)"/>
  <rect x="0" y="0" width="1280" height="720" fill="#111827" opacity="0.18"/>

  <!-- Lower-third anchor plane. -->
  <rect x="0" y="475" width="1280" height="245" fill="url(#bannerSheen)"/>
  <rect x="0" y="474" width="1280" height="1.5" fill="#FFFFFF" opacity="0.10"/>

  <!-- Editorial label. -->
  <text x="64" y="530" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="18"
        font-weight="700" letter-spacing="3" fill="#7F8A9A">MEET OUR TEAM</text>
  <text x="64" y="586" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="40"
        font-weight="800" fill="#FFFFFF">The people behind the work</text>
  <text x="66" y="622" width="450" font-family="Segoe UI, Microsoft YaHei" font-size="16"
        fill="#AAB4C3">Sharp color extracts pull the key subjects out of a softened cinematic field.</text>

  <!-- Card 1: shadow plate, clipped sharp image, glass edge, caption. -->
  <rect x="121" y="205" width="210" height="310" rx="18" fill="#000000" opacity="0.35" filter="url(#cardShadow)"/>
  <image x="-18" y="-56" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#cropAlex)"
         href="https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&amp;fit=crop&amp;w=1920&amp;q=80"/>
  <rect x="121" y="205" width="210" height="310" rx="18" fill="none" stroke="#FFFFFF" stroke-opacity="0.24" stroke-width="1.5"/>
  <text x="121" y="560" width="210" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei"
        font-size="18" font-weight="800" fill="#FFFFFF">ALEX RIVERA</text>
  <text x="121" y="585" width="210" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei"
        font-size="13" fill="#93A4B8">Creative Director</text>

  <!-- Card 2 -->
  <rect x="386" y="178" width="210" height="310" rx="18" fill="#000000" opacity="0.35" filter="url(#cardShadow)"/>
  <image x="-270" y="-70" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#cropJordan)"
         href="https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&amp;fit=crop&amp;w=1920&amp;q=80"/>
  <rect x="386" y="178" width="210" height="310" rx="18" fill="none" stroke="#FFFFFF" stroke-opacity="0.25" stroke-width="1.5"/>
  <text x="386" y="560" width="210" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei"
        font-size="18" font-weight="800" fill="#FFFFFF">JORDAN LEE</text>
  <text x="386" y="585" width="210" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei"
        font-size="13" fill="#93A4B8">Lead Engineer</text>

  <!-- Card 3 -->
  <rect x="651" y="198" width="210" height="310" rx="18" fill="#000000" opacity="0.35" filter="url(#cardShadow)"/>
  <image x="-530" y="-60" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#cropTaylor)"
         href="https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&amp;fit=crop&amp;w=1920&amp;q=80"/>
  <rect x="651" y="198" width="210" height="310" rx="18" fill="none" stroke="#FFFFFF" stroke-opacity="0.24" stroke-width="1.5"/>
  <text x="651" y="560" width="210" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei"
        font-size="18" font-weight="800" fill="#FFFFFF">TAYLOR SMITH</text>
  <text x="651" y="585" width="210" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei"
        font-size="13" fill="#93A4B8">Product Manager</text>

  <!-- Card 4 -->
  <rect x="916" y="170" width="210" height="310" rx="18" fill="#000000" opacity="0.35" filter="url(#cardShadow)"/>
  <image x="-790" y="-64" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#cropCasey)"
         href="https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&amp;fit=crop&amp;w=1920&amp;q=80"/>
  <rect x="916" y="170" width="210" height="310" rx="18" fill="none" stroke="#FFFFFF" stroke-opacity="0.24" stroke-width="1.5"/>
  <text x="916" y="560" width="210" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei"
        font-size="18" font-weight="800" fill="#FFFFFF">CASEY CHEN</text>
  <text x="916" y="585" width="210" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei"
        font-size="13" fill="#93A4B8">Head of Sales</text>

  <!-- Small cinematic footer detail. -->
  <line x1="1060" y1="640" x2="1190" y2="640" stroke="#FFFFFF" stroke-opacity="0.22" stroke-width="1"/>
  <text x="1028" y="668" width="190" text-anchor="end" font-family="Segoe UI, Microsoft YaHei"
        font-size="12" letter-spacing="2" fill="#6F7B8B">SPOTLIGHT EXTRACT</text>
</svg>
```

## Avoid in this skill
- ❌ Do not rely on SVG/CSS `filter: grayscale()` or blur filters on `<image>`; preprocess the full-slide background image into a blurred grayscale PNG/JPEG before inserting it.
- ❌ Do not apply `clip-path` to groups or rectangles for the cards; apply the clip directly to each `<image>`.
- ❌ Do not use `<mask>` to fade the image background; use translucent rectangles and gradients instead.
- ❌ Do not use `<use>` to duplicate the card image; insert each clipped `<image>` separately.
- ❌ Do not use animated SVG elements for the “extract” movement; create separate slides and use PowerPoint Morph if animation is required.

## Composition notes
- Keep the blurred grayscale photo full-bleed so it reads as atmosphere, not content; all important recognition should happen in the sharp extract cards.
- Place the lower banner in the bottom third and let the cards cross its top edge by 30–70 px to create the floating depth illusion.
- Use symmetrical card spacing, but vary the vertical offsets slightly so the layout feels cinematic rather than like a static grid.
- Keep text restrained and low-contrast except for the main headline and names; the color cards should remain the visual focus.