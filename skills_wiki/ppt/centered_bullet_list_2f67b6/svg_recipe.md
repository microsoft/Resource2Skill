# SVG Recipe — Centered Bullet List

## Visual mechanism
A low-density bullet list is placed inside a large, centered “focus card” with generous padding, soft shadows, and symmetrical decorative accents. Each bullet uses a polished icon pill and a short label, making the list feel intentional rather than like default PowerPoint bullets.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background
- 2× `<path>` for large abstract decorative background ribbons/blobs
- 3× `<circle>` for blurred atmospheric color glows
- 1× `<rect>` for the main centered rounded content card
- 1× `<rect>` for the small section label chip
- 1× `<text>` for the label chip
- 1× `<text>` for the main centered title
- 1× `<text>` for the centered subtitle
- 5× `<rect>` for subtle bullet row panels
- 5× `<circle>` for bullet icon pills
- 5× `<path>` for editable checkmark icons
- 5× `<text>` for bullet copy
- 4× `<line>` for thin separators between bullet rows
- 2× `<linearGradient>` for premium background/card accents
- 1× `<radialGradient>` for glow coloring
- 2× `<filter>` definitions for soft shadow and blur/glow effects

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#F7FAFF"/>
      <stop offset="48%" stop-color="#EEF4FF"/>
      <stop offset="100%" stop-color="#F8FBFF"/>
    </linearGradient>

    <linearGradient id="cardGrad" x1="260" y1="96" x2="1020" y2="624">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F8FBFF"/>
    </linearGradient>

    <linearGradient id="pillGrad" x1="0" y1="0" x2="52" y2="52">
      <stop offset="0%" stop-color="#3B82F6"/>
      <stop offset="100%" stop-color="#14B8A6"/>
    </linearGradient>

    <radialGradient id="glowGrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#60A5FA" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="#60A5FA" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="16"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="blurGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="28"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <circle cx="190" cy="150" r="150" fill="url(#glowGrad)" filter="url(#blurGlow)"/>
  <circle cx="1110" cy="560" r="190" fill="#99F6E4" opacity="0.28" filter="url(#blurGlow)"/>
  <circle cx="1050" cy="110" r="110" fill="#C4B5FD" opacity="0.22" filter="url(#blurGlow)"/>

  <path d="M-40,500 C170,420 260,600 450,520 C610,452 690,412 850,466 C1010,520 1130,456 1320,382 L1320,720 L-40,720 Z"
        fill="#DBEAFE" opacity="0.36"/>
  <path d="M930,58 C1010,18 1118,24 1178,92 C1238,160 1218,258 1138,286 C1058,314 1010,254 944,286 C878,318 810,262 826,188 C842,114 874,86 930,58 Z"
        fill="#E0F2FE" opacity="0.75"/>

  <rect x="260" y="86" width="760" height="548" rx="34"
        fill="url(#cardGrad)" stroke="#DDE8F8" stroke-width="1.5" filter="url(#softShadow)"/>

  <rect x="548" y="126" width="184" height="34" rx="17" fill="#EAF3FF" stroke="#CFE2FF"/>
  <text x="640" y="148" width="184" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700"
        fill="#2563EB" letter-spacing="1.7">KEY TAKEAWAYS</text>

  <text x="640" y="218" width="690" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="40" font-weight="700"
        fill="#0F172A">A concise plan everyone can follow</text>

  <text x="640" y="254" width="620" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17"
        fill="#64748B">Use this centered list when the message is short, important, and needs a calm executive rhythm.</text>

  <g transform="translate(0 0)">
    <rect x="335" y="302" width="610" height="58" rx="18" fill="#FFFFFF" opacity="0.78"/>
    <circle cx="382" cy="331" r="21" fill="url(#pillGrad)"/>
    <path d="M372,331 L380,339 L394,320" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
    <text x="425" y="337" width="470"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="600"
          fill="#1E293B">Clarify the decision before adding detail</text>
  </g>

  <line x1="374" y1="374" x2="906" y2="374" stroke="#E5EDF7" stroke-width="1"/>

  <g transform="translate(0 0)">
    <rect x="335" y="388" width="610" height="58" rx="18" fill="#FFFFFF" opacity="0.62"/>
    <circle cx="382" cy="417" r="21" fill="url(#pillGrad)"/>
    <path d="M372,417 L380,425 L394,406" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
    <text x="425" y="423" width="470"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="600"
          fill="#1E293B">Keep each bullet to one clean thought</text>
  </g>

  <line x1="374" y1="460" x2="906" y2="460" stroke="#E5EDF7" stroke-width="1"/>

  <g transform="translate(0 0)">
    <rect x="335" y="474" width="610" height="58" rx="18" fill="#FFFFFF" opacity="0.78"/>
    <circle cx="382" cy="503" r="21" fill="url(#pillGrad)"/>
    <path d="M372,503 L380,511 L394,492" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
    <text x="425" y="509" width="470"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="600"
          fill="#1E293B">Use strong verbs to create momentum</text>
  </g>

  <line x1="374" y1="546" x2="906" y2="546" stroke="#E5EDF7" stroke-width="1"/>

  <g transform="translate(0 0)">
    <rect x="335" y="560" width="610" height="58" rx="18" fill="#FFFFFF" opacity="0.62"/>
    <circle cx="382" cy="589" r="21" fill="url(#pillGrad)"/>
    <path d="M372,589 L380,597 L394,578" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
    <text x="425" y="595" width="470"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="600"
          fill="#1E293B">Center the list, not the paragraph text</text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Default SVG bullet characters as the only visual device; use editable icon pills or custom paths instead.
- ❌ Overfilling the center card with long wrapped paragraphs; the technique depends on concise, low-density points.
- ❌ Using `<marker-end>` for decorative arrows or bullets; if arrows are needed, use explicit `<line>` elements with direct styling.
- ❌ Applying `filter` effects to separator `<line>` elements; shadows/glows should be on cards, circles, or paths only.
- ❌ Relying on `text-anchor="middle"` for multi-line bullet bodies; keep bullet text left-aligned inside a centered list column.

## Composition notes
- Keep the content card centered and occupying roughly 55–65% of slide width, leaving visible negative space around it.
- Use a centered title/subtitle above the list, then switch to left-aligned bullet copy for readability.
- Let the bullet column feel centered as a whole: icon, text, and row panel should share a consistent vertical rhythm.
- Use one restrained accent gradient for the icons and a very pale background glow so the list remains calm and corporate.