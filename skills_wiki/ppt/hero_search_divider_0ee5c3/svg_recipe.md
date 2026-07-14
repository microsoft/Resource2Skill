# SVG Recipe — Hero Search Divider

## Visual mechanism
A calm full-slide shell places an oversized strategic question above a glossy, oversized search bar, making the slide feel like a live query or a tutorial prompt. Soft gradient background shapes, a magnifying-glass icon, cursor hint, and small suggestion chips add premium depth without competing with the central headline.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background
- 3× `<path>` for large soft decorative blobs / diagonal atmosphere shapes
- 1× `<filter id="barShadow">` applied to the search bar card
- 1× `<filter id="softGlow">` applied to background accent paths
- 1× `<linearGradient>` for the background wash
- 2× `<linearGradient>` for the search bar and accent pill fills
- 1× `<radialGradient>` for a subtle spotlight behind the hero content
- 1× `<rect>` for the main rounded search bar
- 3× `<rect>` for small suggestion chips below the search bar
- 1× `<circle>` and 1× `<line>` for the magnifying glass icon
- 1× `<line>` for the search cursor
- 5× `<text>` for headline, search query, section eyebrow, and chip labels
- 2× `<circle>` for small decorative status dots

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#F8FBFF"/>
      <stop offset="0.48" stop-color="#EEF5FF"/>
      <stop offset="1" stop-color="#FFF7EC"/>
    </linearGradient>

    <radialGradient id="spotlight" cx="50%" cy="43%" r="48%">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.95"/>
      <stop offset="0.62" stop-color="#FFFFFF" stop-opacity="0.34"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="blobBlue" x1="80" y1="120" x2="420" y2="460" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#7DC8FF" stop-opacity="0.45"/>
      <stop offset="1" stop-color="#3C6DF0" stop-opacity="0.08"/>
    </linearGradient>

    <linearGradient id="blobCoral" x1="880" y1="40" x2="1230" y2="360" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFB15E" stop-opacity="0.42"/>
      <stop offset="1" stop-color="#FF6F91" stop-opacity="0.08"/>
    </linearGradient>

    <linearGradient id="searchFill" x1="308" y1="371" x2="972" y2="455" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF"/>
      <stop offset="0.64" stop-color="#FBFDFF"/>
      <stop offset="1" stop-color="#F4F8FF"/>
    </linearGradient>

    <linearGradient id="chipFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.92"/>
      <stop offset="1" stop-color="#EEF4FF" stop-opacity="0.88"/>
    </linearGradient>

    <filter id="barShadow" x="-20%" y="-40%" width="140%" height="190%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#spotlight)"/>

  <path d="M-90,174 C40,52 185,52 286,148 C388,244 356,386 230,444 C105,502 -48,445 -92,325 C-128,229 -114,197 -90,174 Z"
        fill="url(#blobBlue)" filter="url(#softGlow)"/>
  <path d="M1006,42 C1128,-12 1280,34 1348,145 C1417,258 1375,406 1241,450 C1107,494 962,408 931,283 C900,159 926,78 1006,42 Z"
        fill="url(#blobCoral)" filter="url(#softGlow)"/>
  <path d="M836,690 C953,594 1138,578 1292,626 L1292,730 L790,730 C794,715 811,706 836,690 Z"
        fill="#DDEBFF" opacity="0.5"/>

  <circle cx="226" cy="180" r="6" fill="#2F6BFF" opacity="0.65"/>
  <circle cx="1034" cy="526" r="8" fill="#FF9A3C" opacity="0.6"/>

  <text x="0" y="132" width="1280" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700"
        letter-spacing="3.5" fill="#4770A8">
    SECTION 03 · STRATEGIC QUESTION
  </text>

  <text x="160" y="255" width="960" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="58" font-weight="800"
        fill="#17233C">
    <tspan x="640" dy="0">What are customers</tspan>
    <tspan x="640" dy="68">really searching for?</tspan>
  </text>

  <rect x="308" y="369" width="664" height="88" rx="44"
        fill="url(#searchFill)" stroke="#D7E3F7" stroke-width="1.5" filter="url(#barShadow)"/>

  <circle cx="365" cy="413" r="17" fill="none" stroke="#2864E8" stroke-width="5"/>
  <line x1="378" y1="426" x2="394" y2="442" stroke="#2864E8" stroke-width="5" stroke-linecap="round"/>

  <text x="421" y="425" width="420"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="27" font-weight="600"
        fill="#23314F">
    how to reduce churn
  </text>

  <line x1="842" y1="393" x2="842" y2="433" stroke="#2864E8" stroke-width="3" stroke-linecap="round"/>

  <rect x="842" y="390" width="92" height="46" rx="23" fill="#EAF1FF" stroke="#CFE0FF"/>
  <text x="842" y="421" width="92" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700"
        fill="#2864E8">
    ENTER
  </text>

  <rect x="394" y="492" width="142" height="38" rx="19" fill="url(#chipFill)" stroke="#DCE7F7"/>
  <text x="394" y="517" width="142" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="600"
        fill="#5D6B84">
    customer signals
  </text>

  <rect x="556" y="492" width="158" height="38" rx="19" fill="url(#chipFill)" stroke="#DCE7F7"/>
  <text x="556" y="517" width="158" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="600"
        fill="#5D6B84">
    onboarding friction
  </text>

  <rect x="734" y="492" width="152" height="38" rx="19" fill="url(#chipFill)" stroke="#DCE7F7"/>
  <text x="734" y="517" width="152" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="600"
        fill="#5D6B84">
    activation moments
  </text>

  <text x="360" y="612" width="560" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" font-weight="500"
        fill="#70809A">
    Use this divider to frame the next section as a focused search, investigation, or tutorial step.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use real HTML input fields or `<foreignObject>`; build the search bar from editable SVG shapes and text.
- ❌ Do not use `<textPath>` for curved decorative labels; it will not translate reliably.
- ❌ Do not place the cursor or magnifier inside a grouped filter; apply filters only to supported shapes such as the search bar rectangle.
- ❌ Do not use `marker-end` for the magnifier handle or action hints; use explicit `<line>` elements instead.
- ❌ Do not rely on animation for the blinking cursor; represent it as a static editable line.

## Composition notes
- Keep the headline and search bar centered vertically, with the search bar occupying roughly 50–55% of slide width for strong “hero object” presence.
- Reserve the top third for the section label and headline; keep supporting chips small and low-contrast so they read as optional prompts.
- Use a soft, mostly white background with two off-canvas color blobs to create depth without reducing legibility.
- The search query should be concise and concrete; the visual works best when the query feels like a real prompt rather than a generic subtitle.