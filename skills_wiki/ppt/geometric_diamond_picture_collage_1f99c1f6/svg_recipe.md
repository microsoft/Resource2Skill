# SVG Recipe — Geometric Diamond Picture Collage

## Visual mechanism
A premium editorial collage built from four identical image-filled diamonds, arranged around a shared center with precise white gutters. The diagonal geometry turns ordinary product or lifestyle photos into a dynamic rhombus mosaic, balanced by minimal typography and generous negative space.

## SVG primitives needed
- 1× `<rect>` for the clean off-white slide background
- 1× `<linearGradient>` for a subtle side accent panel
- 1× `<filter id="softShadow">` applied to backing diamond `<path>` shapes
- 5× `<clipPath>`: four diamond image masks plus one rounded-rectangle portrait mask
- 5× `<image>`: four square-cropped collage photos and one optional vertical supporting portrait
- 4× backing `<path>` diamonds with shadow to give the collage depth
- 4× outline `<path>` diamonds with white stroke to create crisp, uniform gutters
- 1× accent `<rect>` for a vertical navy brand block
- 2× `<line>` for thin editorial separator rules
- 5× `<text>` blocks for company name, issue label, title, caption, and footer details
- 2× small decorative `<path>` diamonds for branded geometric rhythm

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="sideWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#293556"/>
      <stop offset="100%" stop-color="#151B2E"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="14" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="portraitClip">
      <rect x="88" y="154" width="218" height="338" rx="22"/>
    </clipPath>

    <clipPath id="clipTop">
      <path d="M840 136 L965 261 L840 386 L715 261 Z"/>
    </clipPath>
    <clipPath id="clipLeft">
      <path d="M701 275 L826 400 L701 525 L576 400 Z"/>
    </clipPath>
    <clipPath id="clipRight">
      <path d="M979 275 L1104 400 L979 525 L854 400 Z"/>
    </clipPath>
    <clipPath id="clipBottom">
      <path d="M840 414 L965 539 L840 664 L715 539 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F8F7F3"/>
  <rect x="0" y="0" width="38" height="720" fill="url(#sideWash)"/>

  <image x="58" y="134" width="278" height="378"
         href="https://images.unsplash.com/photo-1550614000-4b95d4ed7963?w=900&amp;q=80"
         preserveAspectRatio="xMidYMid slice" clip-path="url(#portraitClip)"/>
  <rect x="88" y="154" width="218" height="338" rx="22" fill="none" stroke="#FFFFFF" stroke-width="6"/>

  <text x="88" y="78" width="270" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="600" letter-spacing="3" fill="#293556">ATELIER NORD</text>
  <line x1="88" y1="98" x2="306" y2="98" stroke="#293556" stroke-width="1.5"/>
  <text x="88" y="555" width="310" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="40" font-weight="300" fill="#212121">Summer Edit</text>
  <text x="91" y="590" width="310" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" letter-spacing="2" fill="#8A7762">LOOKBOOK / COLLECTION 2026</text>
  <text x="88" y="646" width="340" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" fill="#626262">Four image stories arranged as one geometric hero mark.</text>

  <path d="M840 136 L965 261 L840 386 L715 261 Z" fill="#FFFFFF" filter="url(#softShadow)"/>
  <path d="M701 275 L826 400 L701 525 L576 400 Z" fill="#FFFFFF" filter="url(#softShadow)"/>
  <path d="M979 275 L1104 400 L979 525 L854 400 Z" fill="#FFFFFF" filter="url(#softShadow)"/>
  <path d="M840 414 L965 539 L840 664 L715 539 Z" fill="#FFFFFF" filter="url(#softShadow)"/>

  <image x="715" y="136" width="250" height="250"
         href="https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=900&amp;q=80"
         preserveAspectRatio="xMidYMid slice" clip-path="url(#clipTop)"/>
  <image x="576" y="275" width="250" height="250"
         href="https://images.unsplash.com/photo-1483985988355-763728e1935b?w=900&amp;q=80"
         preserveAspectRatio="xMidYMid slice" clip-path="url(#clipLeft)"/>
  <image x="854" y="275" width="250" height="250"
         href="https://images.unsplash.com/photo-1520006403909-838d6b92c22e?w=900&amp;q=80"
         preserveAspectRatio="xMidYMid slice" clip-path="url(#clipRight)"/>
  <image x="715" y="414" width="250" height="250"
         href="https://images.unsplash.com/photo-1434389678369-182cb11b6510?w=900&amp;q=80"
         preserveAspectRatio="xMidYMid slice" clip-path="url(#clipBottom)"/>

  <path d="M840 136 L965 261 L840 386 L715 261 Z" fill="none" stroke="#FFFFFF" stroke-width="10"/>
  <path d="M701 275 L826 400 L701 525 L576 400 Z" fill="none" stroke="#FFFFFF" stroke-width="10"/>
  <path d="M979 275 L1104 400 L979 525 L854 400 Z" fill="none" stroke="#FFFFFF" stroke-width="10"/>
  <path d="M840 414 L965 539 L840 664 L715 539 Z" fill="none" stroke="#FFFFFF" stroke-width="10"/>

  <path d="M840 382 L858 400 L840 418 L822 400 Z" fill="#F8F7F3"/>
  <path d="M438 154 L452 168 L438 182 L424 168 Z" fill="#B08A54"/>
  <path d="M468 154 L482 168 L468 182 L454 168 Z" fill="#293556"/>
  <line x1="424" y1="208" x2="522" y2="208" stroke="#B08A54" stroke-width="2"/>
  <text x="424" y="246" width="205" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" line-height="1.4" fill="#5A5A5A">Use equal diamond sizes and identical spacing so the collage reads as one intentional master shape.</text>
</svg>
```

## Avoid in this skill
- ❌ Applying `clip-path` to ordinary `<path>` or `<rect>` shapes; use clip paths only on `<image>` elements for reliable PPT translation.
- ❌ Using `<use>` to duplicate the diamond masks or outlines; repeat the paths explicitly.
- ❌ Rotating rectangular image elements instead of clipping them; rotated images are harder to crop predictably and may expose corners.
- ❌ Using `<mask>` to create gutters; use real white strokes or physical spacing between diamond paths.
- ❌ Adding arrow markers or complex connector paths; the visual language should stay editorial and geometric.

## Composition notes
- Keep the diamond cluster slightly right of center, occupying roughly 45–55% of slide width; this creates a strong hero object without crowding the text.
- Preserve uniform gutters by using identical diamond coordinates and a consistent white stroke width, usually 8–12 px on a 1280×720 canvas.
- Use the left third for brand typography, a supporting portrait crop, or quiet negative space; avoid filling every corner.
- Choose four photos with related color temperature, then let one accent color, such as navy or muted gold, repeat in lines, labels, and small diamond motifs.