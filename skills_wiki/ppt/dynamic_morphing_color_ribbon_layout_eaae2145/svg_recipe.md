# SVG Recipe — Dynamic Morphing Color Ribbon Layout

## Visual mechanism
A fixed sequence of vertical color ribbons acts as both navigation and progress indicator; on each section slide, one ribbon expands into a full content canvas while the others remain compressed. The expanded block carries white typography and a very transparent photo texture, creating a cinematic “morphing menu” feel when duplicated across slides with the same shape order.

## SVG primitives needed
- 5× `<rect>` for the edge-to-edge vertical ribbon bands: four compressed navigation stripes and one expanded active section
- 1× `<image>` for a low-opacity photographic texture over the active ribbon
- 1× `<clipPath>` with `<rect rx>` for constraining the photo texture to the active ribbon area
- 1× `<linearGradient>` for a subtle depth overlay on the expanded active ribbon
- 1× `<filter id="softShadow">` applied to text cards / badges for keynote-style depth
- 3× `<path>` for large translucent decorative contour curves inside the active section
- 1× `<rect>` for a translucent content panel on top of the active color field
- 5× `<text>` blocks for rotated ribbon labels, section number, headline, body copy, and CTA
- 4× `<line>` for small progress ticks / separators on the compressed ribbons

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="activeGreenDepth" x1="64" y1="0" x2="1088" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#4CAF50"/>
      <stop offset="58%" stop-color="#43A047"/>
      <stop offset="100%" stop-color="#2E7D32"/>
    </linearGradient>

    <linearGradient id="glassPanel" x1="350" y1="180" x2="930" y2="560" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.20"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.07"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="16"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .28 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="activeRibbonClip">
      <rect x="64" y="0" width="1024" height="720" rx="0"/>
    </clipPath>
  </defs>

  <!-- Section state: green ribbon is active. Keep this same z-order on all morph slides. -->
  <rect id="ribbon-01-blue" x="0" y="0" width="64" height="720" fill="#2196F3"/>
  <rect id="ribbon-02-green-active" x="64" y="0" width="1024" height="720" fill="url(#activeGreenDepth)"/>
  <rect id="ribbon-03-orange" x="1088" y="0" width="64" height="720" fill="#FF9800"/>
  <rect id="ribbon-04-red" x="1152" y="0" width="64" height="720" fill="#F44336"/>
  <rect id="ribbon-05-yellow" x="1216" y="0" width="64" height="720" fill="#FFC107"/>

  <!-- Transparent photographic texture over the active color block -->
  <image
    href="https://images.example.com/transparent-business-team-collaboration-office.jpg"
    x="64" y="0" width="1024" height="720"
    preserveAspectRatio="xMidYMid slice"
    opacity="0.16"
    clip-path="url(#activeRibbonClip)"/>

  <!-- Decorative motion curves: imply ribbon flow without using animation -->
  <path d="M146 640 C330 520, 420 510, 610 370 C760 260, 860 150, 1048 92"
        fill="none" stroke="#FFFFFF" stroke-width="3" stroke-opacity="0.18"/>
  <path d="M100 120 C260 210, 402 192, 548 124 C694 56, 855 46, 1040 138"
        fill="none" stroke="#FFFFFF" stroke-width="2" stroke-opacity="0.13"/>
  <path d="M230 690 C360 608, 526 634, 678 548 C810 474, 922 360, 1080 352"
        fill="none" stroke="#FFFFFF" stroke-width="18" stroke-opacity="0.055"/>

  <!-- Content glass panel -->
  <rect x="322" y="150" width="590" height="420" rx="28"
        fill="url(#glassPanel)" stroke="#FFFFFF" stroke-opacity="0.28" stroke-width="1.5"
        filter="url(#softShadow)"/>

  <!-- Section badge -->
  <rect x="352" y="184" width="158" height="42" rx="21"
        fill="#FFFFFF" fill-opacity="0.18" stroke="#FFFFFF" stroke-opacity="0.38"/>
  <text x="382" y="212" width="120"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="700" letter-spacing="2"
        fill="#FFFFFF">02 / SERVICES</text>

  <!-- Main content -->
  <text x="352" y="292" width="500"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="58" font-weight="800"
        fill="#FFFFFF">Modular Growth Platform</text>

  <text x="356" y="350" width="470"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="400"
        fill="#FFFFFF" opacity="0.92">
    <tspan x="356" dy="0">Strategy, operations, analytics, and enablement</tspan>
    <tspan x="356" dy="32">combine into a configurable service portfolio</tspan>
    <tspan x="356" dy="32">that scales with each market opportunity.</tspan>
  </text>

  <line x1="356" y1="462" x2="548" y2="462" stroke="#FFFFFF" stroke-width="3" stroke-opacity="0.65"/>
  <text x="356" y="512" width="430"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="19" font-weight="600"
        fill="#FFFFFF" opacity="0.95">Explore service modules →</text>

  <!-- Rotated compressed ribbon labels -->
  <text x="22" y="632" width="210"
        transform="rotate(-90 22 632)"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" letter-spacing="2"
        fill="#FFFFFF" opacity="0.92">PROFILE</text>

  <text x="1110" y="635" width="210"
        transform="rotate(-90 1110 635)"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" letter-spacing="2"
        fill="#FFFFFF" opacity="0.92">PRODUCTS</text>

  <text x="1174" y="635" width="210"
        transform="rotate(-90 1174 635)"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" letter-spacing="2"
        fill="#FFFFFF" opacity="0.92">TEAM</text>

  <text x="1238" y="635" width="210"
        transform="rotate(-90 1238 635)"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" letter-spacing="2"
        fill="#2F2F2F" opacity="0.82">ROADMAP</text>

  <!-- Progress ticks on inactive ribbons -->
  <line x1="32" y1="64" x2="32" y2="112" stroke="#FFFFFF" stroke-width="3" stroke-opacity="0.75"/>
  <line x1="1120" y1="64" x2="1120" y2="112" stroke="#FFFFFF" stroke-width="3" stroke-opacity="0.55"/>
  <line x1="1184" y1="64" x2="1184" y2="112" stroke="#FFFFFF" stroke-width="3" stroke-opacity="0.55"/>
  <line x1="1248" y1="64" x2="1248" y2="112" stroke="#2F2F2F" stroke-width="3" stroke-opacity="0.45"/>
</svg>
```

## Avoid in this skill
- ❌ SVG `<animate>` or `<animateTransform>` for the ribbon expansion; create separate slides and let PowerPoint Morph interpolate the same rectangles instead
- ❌ Reordering, deleting, or renaming ribbon shapes between slides; Morph works best when the same five ribbon shapes remain in the same z-order
- ❌ Applying `clip-path` to decorative paths or rectangles; use it only on the texture `<image>`
- ❌ Using `marker-end` on curved paths for navigation arrows; if arrows are needed, use native `<line marker-end="...">` directly or omit arrowheads
- ❌ Overloading the expanded ribbon with many panels; the effect depends on one dominant color field with confident whitespace

## Composition notes
- Keep the ribbon sequence consistent across all slides: only the active ribbon’s `x` and `width` change from slide to slide.
- Use a compressed stripe width of roughly 5% of slide width; the active section should occupy about 75–85% of the canvas.
- Place headline and body copy well inside the expanded ribbon, leaving at least 220–300 px from the nearest compressed stripe for breathing room.
- Use white typography on blue/green/orange/red active states; switch to dark slate text only when yellow becomes the active ribbon.