# SVG Recipe — Diagonal Split Agenda Layout

## Visual mechanism
A full-bleed hero photo is cut by a strong diagonal into a dynamic right-side visual field, while a crisp white polygon creates a readable left-side agenda panel. A vivid accent line rides exactly on the diagonal seam, making the split feel intentional, energetic, and premium.

## SVG primitives needed
- 1× `<image>` for the full-height architectural / thematic hero photo on the right
- 1× `<clipPath>` with a diagonal `<path>` applied to the image crop
- 1× `<path>` for the large white diagonal agenda panel
- 1× `<filter id="panelShadow">` applied to the white panel for subtle depth along the split
- 1× `<line>` for the blue diagonal accent separator
- 1× `<linearGradient>` for the accent line stroke
- 1× `<path>` for a translucent dark overlay on the photo side
- 4× `<circle>` for numbered agenda bullets
- 4× `<text>` groups for agenda item numbers, headings, and descriptions
- 1× `<text>` for the main title
- 1× `<text>` for the subtitle / section label
- 3× decorative `<line>` or `<path>` accents on the image side for a modern tech/editorial finish

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="photoDiagonalClip">
      <path d="M690 0 L1280 0 L1280 720 L545 720 Z"/>
    </clipPath>

    <linearGradient id="blueAccent" x1="690" y1="0" x2="545" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#76A7FF"/>
      <stop offset="45%" stop-color="#4285F4"/>
      <stop offset="100%" stop-color="#0B57D0"/>
    </linearGradient>

    <linearGradient id="photoShade" x1="640" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#061A33" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#061A33" stop-opacity="0.48"/>
    </linearGradient>

    <filter id="panelShadow" x="-5%" y="-5%" width="115%" height="115%">
      <feOffset dx="12" dy="0"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <image
    href="https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&amp;w=1800&amp;auto=format&amp;fit=crop"
    x="360" y="0" width="920" height="720"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#photoDiagonalClip)"/>

  <path d="M690 0 L1280 0 L1280 720 L545 720 Z" fill="url(#photoShade)" opacity="0.95"/>

  <path d="M972 90 L1170 90" stroke="#FFFFFF" stroke-opacity="0.55" stroke-width="2"/>
  <path d="M1015 123 L1232 123" stroke="#FFFFFF" stroke-opacity="0.28" stroke-width="2"/>
  <path d="M890 586 L1210 586" stroke="#4285F4" stroke-opacity="0.65" stroke-width="5"/>

  <path
    d="M0 0 L700 0 L555 720 L0 720 Z"
    fill="#FFFFFF"
    filter="url(#panelShadow)"/>

  <line x1="690" y1="0" x2="545" y2="720" stroke="url(#blueAccent)" stroke-width="7" stroke-linecap="butt"/>

  <text x="82" y="86" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="44" font-weight="700" fill="#333333" letter-spacing="1.5">
    AGENDA
  </text>

  <text x="84" y="124" width="430" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="600" fill="#4285F4" letter-spacing="2.4">
    STRATEGIC WORKSHOP / Q3 PLANNING
  </text>

  <circle cx="104" cy="207" r="18" fill="#4285F4"/>
  <text x="96" y="214" width="22" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700" fill="#FFFFFF">
    01
  </text>
  <text x="146" y="202" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="700" fill="#333333">
    Market Signals
  </text>
  <text x="146" y="229" width="390" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#777777">
    Review customer shifts, competitor movement, and category momentum.
  </text>

  <circle cx="104" cy="315" r="18" fill="#4285F4"/>
  <text x="96" y="322" width="22" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700" fill="#FFFFFF">
    02
  </text>
  <text x="146" y="310" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="700" fill="#333333">
    Product Priorities
  </text>
  <text x="146" y="337" width="390" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#777777">
    Align roadmap bets with impact, feasibility, and executive sponsorship.
  </text>

  <circle cx="104" cy="423" r="18" fill="#4285F4"/>
  <text x="96" y="430" width="22" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700" fill="#FFFFFF">
    03
  </text>
  <text x="146" y="418" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="700" fill="#333333">
    Operating Model
  </text>
  <text x="146" y="445" width="390" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#777777">
    Define governance, decision rights, delivery cadence, and escalation paths.
  </text>

  <circle cx="104" cy="531" r="18" fill="#4285F4"/>
  <text x="96" y="538" width="22" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700" fill="#FFFFFF">
    04
  </text>
  <text x="146" y="526" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="700" fill="#333333">
    Next Commitments
  </text>
  <text x="146" y="553" width="390" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#777777">
    Confirm owners, milestones, and the measurable outcomes for the quarter.
  </text>

  <text x="918" y="660" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="600" fill="#FFFFFF" opacity="0.88" text-anchor="end">
    Built for forward motion
  </text>
</svg>
```

## Avoid in this skill
- ❌ Applying `clip-path` to the white panel or overlay shapes; clipping should only be used on the `<image>` for reliable PowerPoint translation.
- ❌ Using `marker-end` for diagonal arrows; this layout only needs a clean separator line, and SVG arrow markers may disappear.
- ❌ Overcrowding the white panel with long paragraphs; the diagonal geometry reduces usable text width near the lower right.
- ❌ Making the accent line too thin or low-contrast; it should visibly bind the photo and agenda zones.
- ❌ Using skew or matrix transforms to create the diagonal; draw the panel and photo crop directly as polygonal paths.

## Composition notes
- Keep the title and agenda list aligned to a strict left guide around `x=80–150`; the diagonal edge should never dictate text alignment.
- Reserve roughly 50–55% of the slide for the white agenda panel and 45–50% for the hero image, with the diagonal running from upper mid-right to lower center.
- Use one accent color consistently for the seam line and numbered bullets to unify the split composition.
- Choose a photo with visual interest on the far right; the diagonal crop will hide or compete with anything important near the center-left.