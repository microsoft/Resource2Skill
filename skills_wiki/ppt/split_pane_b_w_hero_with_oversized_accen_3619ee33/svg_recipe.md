# SVG Recipe — Split-Pane B&W Hero with Oversized Accent Circle

## Visual mechanism
A monochrome architectural hero photo is cropped into an oversized left-side circle/pane, then overlaid with a large mint accent circle carrying the section title. The right half remains mostly white, using compact icon-led text rows to balance the visual weight of the photo.

## SVG primitives needed
- 1× `<rect>` for the white slide background
- 1× `<clipPath>` with `<circle>` for the oversized circular photo crop
- 1× `<image>` for the grayscale architectural/corporate hero photo
- 1× `<circle>` for the oversized mint title accent
- 3× `<circle>` for mint icon badges on the right-side list
- 6× `<path>` for simple editable charcoal icons inside the badges
- 7× `<text>` elements for title, row headers, and descriptions
- 1× `<linearGradient>` for a subtle white fade overlay at the photo/right-pane boundary
- 1× `<rect>` using the gradient to soften the transition into the white content area

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="heroPhotoCircle">
      <circle cx="392" cy="344" r="430"/>
    </clipPath>

    <linearGradient id="rightFade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="70%" stop-color="#FFFFFF" stop-opacity="0.92"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="1"/>
    </linearGradient>
  </defs>

  <!-- Clean white canvas -->
  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <!-- Oversized circular black-and-white hero image -->
  <image
    x="-40" y="-86" width="890" height="860"
    href="https://images.example.com/grayscale-modern-architecture-campus-courtyard.jpg"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#heroPhotoCircle)"/>

  <!-- Soft white fade where the image meets the content area -->
  <rect x="720" y="0" width="180" height="720" fill="url(#rightFade)"/>

  <!-- Oversized accent circle carrying the main section title -->
  <circle cx="432" cy="360" r="188" fill="#91BFAE"/>

  <text x="432" y="342" width="330"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="66"
        font-weight="700"
        fill="#050505">
    <tspan x="432" dy="0">Our</tspan>
    <tspan x="432" dy="86">Mission</tspan>
  </text>

  <!-- Right-side list item 1 -->
  <circle cx="900" cy="272" r="36" fill="#91BFAE"/>
  <path d="M879 291 L899 263 L918 291 Z" fill="#303030"/>
  <path d="M904 258 L904 246 L922 246 L922 255 L911 255 L911 258 Z" fill="#303030"/>
  <path d="M890 283 L897 274 L901 283 Z" fill="#91BFAE"/>

  <text x="955" y="267" width="250"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="28"
        font-weight="700"
        fill="#050505">Mission</text>
  <text x="955" y="297" width="285"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15"
        font-weight="400"
        fill="#8C8C8C">
    <tspan x="955" dy="0">Adapt this section to your strategic</tspan>
    <tspan x="955" dy="21">mission and operating principles.</tspan>
  </text>

  <!-- Right-side list item 2 -->
  <circle cx="900" cy="384" r="36" fill="#91BFAE"/>
  <path d="M900 356 C916 356 927 368 927 382 C927 400 900 416 900 416 C900 416 873 400 873 382 C873 368 884 356 900 356 Z" fill="#303030"/>
  <ellipse cx="900" cy="381" rx="15" ry="9" fill="#91BFAE"/>
  <circle cx="900" cy="381" r="5" fill="#303030"/>
  <circle cx="900" cy="381" r="2" fill="#91BFAE"/>

  <text x="955" y="379" width="250"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="28"
        font-weight="700"
        fill="#050505">Vision</text>
  <text x="955" y="409" width="285"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15"
        font-weight="400"
        fill="#8C8C8C">
    <tspan x="955" dy="0">Describe the future state your team</tspan>
    <tspan x="955" dy="21">is building toward over time.</tspan>
  </text>

  <!-- Right-side list item 3 -->
  <circle cx="900" cy="496" r="36" fill="#91BFAE"/>
  <path d="M878 476 L884 476 L884 522 L878 522 Z" fill="#303030"/>
  <path d="M884 480 C895 474 907 488 923 481 L923 505 C907 512 895 498 884 504 Z" fill="#303030"/>

  <text x="955" y="491" width="250"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="28"
        font-weight="700"
        fill="#050505">Goal</text>
  <text x="955" y="521" width="285"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15"
        font-weight="400"
        fill="#8C8C8C">
    <tspan x="955" dy="0">Summarize the measurable outcome</tspan>
    <tspan x="955" dy="21">that defines success this year.</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Applying SVG color filters such as `feColorMatrix` to desaturate the photo; use a pre-grayscaled image asset instead for predictable PPT translation.
- ❌ Using `<mask>` to fade the photo; use a regular white gradient rectangle overlay instead.
- ❌ Clipping vector shapes or text with `clip-path`; keep clipping only on the `<image>`.
- ❌ Letting right-side text begin too close to the accent circle or photo edge; the white pane needs generous breathing room.

## Composition notes
- Keep the photo visually dominant on the left, ideally clipped as a very large circle that bleeds off the top, left, and bottom edges.
- Place the mint title circle over the image, slightly left of center, so the title feels embedded in the hero image rather than floating in the white area.
- Reserve the right 30–35% of the slide for three concise content rows with icon badges, bold headers, and light gray descriptions.
- Use one accent color only; the grayscale image, black title text, and mint circles create the premium contrast.