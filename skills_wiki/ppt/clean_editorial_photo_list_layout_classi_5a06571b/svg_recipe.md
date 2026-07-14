# SVG Recipe — Clean Editorial Photo & List Layout (Classic Keynote Aesthetic)

## Visual mechanism
A spacious editorial split layout pairs a large, polished photo card with a clean typographic list, using white space, restrained color, and a soft shadow to create a premium Keynote-like slide. The photograph acts as the visual anchor while the right-side text block provides structured, highly legible information.

## SVG primitives needed
- 1× `<rect>` for the pure white slide background
- 1× `<rect>` for the subtle shadow-casting photo backing card
- 1× `<image>` for the large editorial photograph
- 1× `<clipPath>` with rounded `<rect>` to crop the photograph cleanly
- 1× `<filter id="photoShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` for the Keynote-style photo depth
- 1× `<linearGradient>` for a very subtle warm photo-edge accent
- 1× `<rect>` for the thin vertical accent bar near the text column
- 1× `<line>` for the understated title divider
- 6× `<circle>` for refined bullet markers
- Multiple `<text>` elements for eyebrow label, title, subtitle, and list copy
- 1× decorative `<path>` for a soft organic accent shape behind the text column

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <filter id="photoShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18" result="offset"/>
      <feGaussianBlur in="offset" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <linearGradient id="warmEdge" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#B56B43"/>
      <stop offset="55%" stop-color="#C7A47B"/>
      <stop offset="100%" stop-color="#EFE7DC"/>
    </linearGradient>

    <clipPath id="photoClip">
      <rect x="90" y="82" width="470" height="556" rx="8" ry="8"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <path d="M1010 58 C1115 82 1170 164 1164 264 C1158 376 1064 420 1042 526 C1028 596 1068 646 1126 682 L1280 720 L1280 0 L1118 0 C1070 10 1032 28 1010 58 Z"
        fill="#F7F3EE"/>

  <rect x="90" y="82" width="470" height="556" rx="8" ry="8"
        fill="#FFFFFF" filter="url(#photoShadow)" opacity="0.88"/>

  <image x="90" y="82" width="470" height="556"
         href="https://images.example.com/editorial-vertical-photo-classical-monument-soft-daylight.jpg"
         clip-path="url(#photoClip)" preserveAspectRatio="xMidYMid slice"/>

  <rect x="90" y="82" width="10" height="556" fill="url(#warmEdge)" opacity="0.9"/>

  <text x="650" y="104" width="430"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="600" letter-spacing="3"
        fill="#B56B43">KEYNOTE BASICS</text>

  <text x="650" y="168" width="505"
        font-family="Georgia, 'Times New Roman', serif"
        font-size="48" font-weight="700"
        fill="#2A2A2A">My Slide</text>

  <text x="650" y="214" width="510"
        font-family="Georgia, 'Times New Roman', serif"
        font-size="22"
        fill="#5E5E5E">A clean editorial layout for presenting ideas with calm authority.</text>

  <line x1="650" y1="252" x2="1110" y2="252"
        stroke="#D8D2CA" stroke-width="2"/>

  <rect x="650" y="288" width="4" height="250" rx="2" fill="#B56B43"/>

  <circle cx="684" cy="306" r="5" fill="#B56B43"/>
  <text x="704" y="314" width="430"
        font-family="Georgia, 'Times New Roman', serif"
        font-size="22" fill="#303030">One strong visual anchor</text>

  <text x="704" y="344" width="440"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" fill="#777777">Use a single photograph with enough scale to feel intentional.</text>

  <circle cx="684" cy="388" r="5" fill="#B56B43"/>
  <text x="704" y="396" width="430"
        font-family="Georgia, 'Times New Roman', serif"
        font-size="22" fill="#303030">Refined serif hierarchy</text>

  <text x="704" y="426" width="440"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" fill="#777777">Pair a large title with restrained, evenly spaced supporting copy.</text>

  <circle cx="684" cy="470" r="5" fill="#B56B43"/>
  <text x="704" y="478" width="430"
        font-family="Georgia, 'Times New Roman', serif"
        font-size="22" fill="#303030">Soft depth, never heavy</text>

  <text x="704" y="508" width="440"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" fill="#777777">A subtle shadow makes the image feel physical without adding clutter.</text>

  <circle cx="684" cy="552" r="5" fill="#B56B43"/>
  <text x="704" y="560" width="430"
        font-family="Georgia, 'Times New Roman', serif"
        font-size="22" fill="#303030">Generous negative space</text>

  <text x="704" y="590" width="440"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" fill="#777777">Let the slide breathe so the content feels premium and memorable.</text>

  <text x="650" y="650" width="420"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" letter-spacing="1.5"
        fill="#A9A39B">CLASSIC WHITE CANVAS · PHOTO LEFT · LIST RIGHT</text>
</svg>
```

## Avoid in this skill
- ❌ Heavy borders around the photograph; the shadow should provide depth, not a visible frame.
- ❌ Overcrowded bullet lists; this layout depends on breathing room and restrained copy.
- ❌ Pure black text on stark white for all typography; use charcoal and warm gray for a softer editorial feel.
- ❌ Clipping non-image elements; use the rounded `clipPath` only on the photo image.
- ❌ Decorative gradients or shapes that compete with the photograph.

## Composition notes
- Keep the photo large, usually 35–45% of slide width, with generous margins on all sides so the shadow is visible.
- Place the text column on the opposite side with a strict left alignment and a clear vertical reading rhythm.
- Use one accent color sampled from the image for bullets, divider details, or a slim vertical bar.
- Preserve white space: the slide should feel like a magazine spread, not a dense data page.