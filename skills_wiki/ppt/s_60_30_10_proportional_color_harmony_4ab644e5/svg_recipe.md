# SVG Recipe — 60-30-10 Proportional Color Harmony

## Visual mechanism
A slide is visually “budgeted” into three colors: 60% calm primary background, 30% strong secondary structure/typography, and 10% accent used only for emphasis. The result feels deliberate because the accent is scarce and therefore visually valuable.

## SVG primitives needed
- 2× <rect> for the black letterbox frame and the 60% neutral stage background
- 1× <linearGradient> for a subtle premium neutral background wash
- 1× <image> for a clipped presenter/hero photo on the right side
- 1× <clipPath> with <path> for an organic cutout crop around the presenter image
- 2× <path> for the presenter shadow silhouette and editable outline
- 1× <filter id="softShadow"> applied to organic photo shadow and cards
- 1× <rect> accent pill for the 10% callout
- 4× <rect> for the proportional 60/30/10 palette bar and its base card
- 5× <text> elements with explicit width for title, badge, subtitle, and palette labels
- 1× <line> for a minimal secondary-color divider

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bg60" x1="0" y1="72" x2="1280" y2="648" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#F4F4F2"/>
      <stop offset="0.62" stop-color="#E7E7E4"/>
      <stop offset="1" stop-color="#DADAD7"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="5"/>
      <feGaussianBlur stdDeviation="7"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="presenterClip" clipPathUnits="userSpaceOnUse">
      <path d="M962,104
               C1038,90 1125,126 1164,202
               C1204,279 1183,352 1138,410
               C1182,451 1215,512 1196,595
               L1192,646 L642,646
               C639,597 646,542 664,493
               C633,474 604,452 581,421
               C557,389 555,355 581,337
               C606,319 637,332 663,357
               C695,389 720,381 747,356
               C776,330 809,302 847,300
               C858,233 891,130 962,104 Z"/>
    </clipPath>
  </defs>

  <!-- black frame visible in the source thumbnail -->
  <rect x="0" y="0" width="1280" height="720" fill="#000000"/>

  <!-- 60% primary color: the quiet field -->
  <rect x="0" y="72" width="1280" height="576" fill="url(#bg60)"/>

  <!-- right-side cutout photo zone -->
  <path filter="url(#softShadow)" fill="#151515" opacity="0.38"
        d="M962,104
           C1038,90 1125,126 1164,202
           C1204,279 1183,352 1138,410
           C1182,451 1215,512 1196,595
           L1192,646 L642,646
           C639,597 646,542 664,493
           C633,474 604,452 581,421
           C557,389 555,355 581,337
           C606,319 637,332 663,357
           C695,389 720,381 747,356
           C776,330 809,302 847,300
           C858,233 891,130 962,104 Z"/>

  <image x="540" y="88" width="720" height="570"
         href="https://images.example.com/presenter-cutout-thumbs-up-neutral-background.png"
         clip-path="url(#presenterClip)" preserveAspectRatio="xMidYMid slice"/>

  <path fill="none" stroke="#24435B" stroke-width="3" opacity="0.32"
        d="M962,104
           C1038,90 1125,126 1164,202
           C1204,279 1183,352 1138,410
           C1182,451 1215,512 1196,595
           L1192,646 L642,646
           C639,597 646,542 664,493
           C633,474 604,452 581,421
           C557,389 555,355 581,337
           C606,319 637,332 663,357
           C695,389 720,381 747,356
           C776,330 809,302 847,300
           C858,233 891,130 962,104 Z"/>

  <!-- 30% secondary color: large structural typography -->
  <text x="70" y="203" width="560"
        font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="126" font-weight="900" letter-spacing="4" fill="#24435B">
    <tspan x="70" dy="0">PICK</tspan>
    <tspan x="70" dy="144">AWESOME</tspan>
    <tspan x="70" dy="144">COLOR</tspan>
    <tspan x="70" dy="144">SCHEMES</tspan>
  </text>

  <!-- 10% accent: scarce, high-value callout -->
  <rect x="78" y="558" width="146" height="40" rx="20" fill="#4C9173"/>
  <text x="96" y="585" width="112"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" fill="#FFFFFF">60–30–10</text>

  <line x1="245" y1="578" x2="520" y2="578" stroke="#24435B" stroke-width="3" opacity="0.45"/>
  <text x="78" y="628" width="470"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="600" fill="#24435B" opacity="0.88">
    Let the accent color appear only where attention should land.
  </text>

  <!-- proportional proof bar -->
  <rect x="760" y="584" width="400" height="48" rx="24" fill="#FFFFFF" opacity="0.74" filter="url(#softShadow)"/>
  <rect x="770" y="596" width="228" height="24" rx="12" fill="#F2F2F2" stroke="#24435B" stroke-width="1.5"/>
  <rect x="998" y="596" width="114" height="24" fill="#24435B"/>
  <rect x="1112" y="596" width="38" height="24" rx="12" fill="#4C9173"/>

  <text x="770" y="574" width="240"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="700" fill="#24435B">60% primary field</text>
  <text x="1002" y="574" width="150"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="700" fill="#24435B">30% structure</text>
  <text x="1115" y="574" width="80"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="700" fill="#4C9173">10%</text>
</svg>
```

## Avoid in this skill
- ❌ Using the accent color on large panels, full-width headers, or multiple competing highlights; it breaks the 10% scarcity.
- ❌ Adding extra palette colors for decoration; this technique depends on disciplined three-color budgeting.
- ❌ Applying clip-path to decorative shapes; for PowerPoint translation, use clip-path only on the photo/image.
- ❌ Recreating face blurs or privacy masks as part of the design mechanism; keep the photo treatment clean and focus on color proportion.
- ❌ Pattern fills or complex masks to “add interest”; they dilute the clarity of the 60-30-10 system.

## Composition notes
- Keep the 60% color as the dominant quiet surface: background, negative space, and breathing room.
- Spend the 30% color on large readable typography, structural dividers, outlines, and major visual anchors.
- Reserve the 10% accent for one badge, one key word, one CTA, or one data point—not all of them at once.
- For a thumbnail/title-slide feel, place oversized secondary-color type on the left and a high-contrast image crop on the right.