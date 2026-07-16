# SVG Recipe — Horizontal Morphing Node Carousel

## Visual mechanism
A thin horizontal track anchors evenly spaced nodes, while one “active” node expands into a large circular avatar and a floating detail card. Duplicate the slide and move the same active avatar/card group to the next node position; PowerPoint Morph creates the carousel-like horizontal glide.

## SVG primitives needed
- 1× `<rect>` for the soft background wash
- 1× `<linearGradient>` for the premium warm-to-cool background
- 1× `<radialGradient>` for the active-node glow
- 1× `<filter id="softShadow">` for the active card and avatar backing shadow
- 1× `<filter id="cardGlow">` for the active card accent glow
- 1× `<clipPath>` with `<circle>` for the circular active avatar crop
- 1× `<image>` for the active client/profile photo
- 1× `<rect>` for the horizontal track
- 4× `<circle>` for inactive/active node dots on the track
- 2× `<circle>` for active node pulse rings
- 1× `<path>` for the active detail card with a pointer notch
- 1× `<path>` for an organic decorative blob behind the active avatar
- 1× `<line>` for the vertical connector between avatar and node
- Multiple `<text>` elements with explicit `width` for title, subtitle, labels, rating, testimonial, and metadata
- Nested `<tspan>` inside `<text>` for inline emphasis and colored star ratings

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#F8FBFF"/>
      <stop offset="0.55" stop-color="#FFFFFF"/>
      <stop offset="1" stop-color="#EEF7FF"/>
    </linearGradient>

    <radialGradient id="activeGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#25B7FF" stop-opacity="0.34"/>
      <stop offset="0.58" stop-color="#25B7FF" stop-opacity="0.12"/>
      <stop offset="1" stop-color="#25B7FF" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="cardGrad" x1="340" y1="440" x2="660" y2="650" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF"/>
      <stop offset="1" stop-color="#F4FAFF"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="cardGlow" x="-20%" y="-20%" width="140%" height="150%">
      <feGaussianBlur stdDeviation="4"/>
    </filter>

    <clipPath id="avatarClip">
      <circle cx="500" cy="278" r="72"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <text x="120" y="82" width="700" font-family="Segoe UI, Microsoft YaHei" font-size="44" font-weight="700" fill="#162033">
    Few words from our clients
  </text>
  <text x="122" y="126" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#6D7788">
    A morphing carousel keeps all testimonials in context while spotlighting one story at a time.
  </text>

  <path d="M408 196 C455 130, 568 139, 611 202 C653 264, 622 345, 545 371 C465 398, 381 357, 371 282 C365 242, 383 217, 408 196 Z"
        fill="#DFF4FF" opacity="0.72"/>

  <circle cx="500" cy="278" r="118" fill="url(#activeGlow)"/>
  <circle cx="500" cy="278" r="82" fill="#FFFFFF" filter="url(#softShadow)"/>
  <image href="https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&amp;fit=crop&amp;w=500&amp;q=80"
         x="428" y="206" width="144" height="144" clip-path="url(#avatarClip)"/>
  <circle cx="500" cy="278" r="73" fill="none" stroke="#FFFFFF" stroke-width="6"/>
  <circle cx="500" cy="278" r="80" fill="none" stroke="#25B7FF" stroke-width="3"/>

  <rect x="190" y="428" width="900" height="4" rx="2" fill="#D7DEE8"/>
  <circle cx="220" cy="430" r="10" fill="#AAB3C0"/>
  <circle cx="500" cy="430" r="24" fill="#25B7FF" opacity="0.14"/>
  <circle cx="500" cy="430" r="15" fill="#25B7FF"/>
  <circle cx="780" cy="430" r="10" fill="#AAB3C0"/>
  <circle cx="1060" cy="430" r="10" fill="#AAB3C0"/>

  <line x1="500" y1="360" x2="500" y2="414" stroke="#25B7FF" stroke-width="3" stroke-dasharray="6 7"/>

  <path d="M344 466
           Q344 448 362 448
           L466 448
           L500 420
           L534 448
           L638 448
           Q656 448 656 466
           L656 616
           Q656 638 634 638
           L366 638
           Q344 638 344 616
           Z"
        fill="url(#cardGrad)" stroke="#E4EEF8" stroke-width="1.5" filter="url(#softShadow)"/>

  <path d="M367 455 L470 455 L500 430 L530 455 L633 455" fill="none" stroke="#25B7FF" stroke-width="3" filter="url(#cardGlow)"/>

  <text x="374" y="493" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#172033">
    Mrs. Client Y
  </text>
  <text x="374" y="520" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#7A8494">
    Chief Growth Officer, Northstar Labs
  </text>

  <text x="374" y="552" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="22" fill="#FFBE00" letter-spacing="2">
    ★★★★★
  </text>

  <text x="374" y="588" width="252" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#334155">
    <tspan font-weight="700" fill="#172033">“Outstanding service.</tspan>
    <tspan> They went above and beyond expectations, translating complexity into a clear executive story.”</tspan>
  </text>

  <text x="180" y="466" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="13" text-anchor="middle" fill="#8B95A5">
    Discovery
  </text>
  <text x="460" y="466" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="13" text-anchor="middle" fill="#25B7FF" font-weight="700">
    Delivery
  </text>
  <text x="740" y="466" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="13" text-anchor="middle" fill="#8B95A5">
    Scale-up
  </text>
  <text x="1020" y="466" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="13" text-anchor="middle" fill="#8B95A5">
    Renewal
  </text>

  <text x="890" y="108" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#7A8494">
    Duplicate this slide and move the avatar/card group from x=500 to x=780, then x=1060. Apply PowerPoint Morph between slides.
  </text>
</svg>
```

## Avoid in this skill
- ❌ SVG `<animate>` or `<animateTransform>`; the motion must come from PowerPoint Morph across duplicated slides.
- ❌ `marker-end` arrowheads on paths; if you need direction cues, use simple `<line>` or drawn arrowhead paths.
- ❌ Applying `clip-path` to the avatar backing circles or card; use clipping only on the `<image>` for the circular photo crop.
- ❌ Rebuilding the active card as different objects on each slide; Morph works best when the same SVG/PPT objects are duplicated and only moved/resized.
- ❌ Dense text on every node; inactive nodes should remain context markers, not competing content blocks.

## Composition notes
- Place the track slightly below vertical center, around y=430 on a 1280×720 canvas, leaving generous upper whitespace for the active avatar.
- Keep inactive nodes small, grey, and evenly distributed; make the active node 3–4× larger with glow or ring accents.
- The detail card should sit below the track and align horizontally with the active node, using a notch or pointer to visually attach it.
- For Morph slides, duplicate the whole layout, move only the active avatar/card/connector/glow group to the next node’s x-position, and swap the text/photo content while preserving the object structure.