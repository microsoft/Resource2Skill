# SVG Recipe — Centered Title & Bullets

## Visual mechanism
A large centered headline anchors the slide, while a polished rounded “bullet card” below creates a calm reading zone for 3–5 concise takeaways. Subtle gradient washes, blurred decorative blobs, and a luminous accent line keep the minimal layout feeling premium rather than plain.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background
- 2× `<path>` for soft organic background blobs
- 1× `<rect>` for a small centered eyebrow pill
- 1× `<text>` for the eyebrow label
- 1× `<text>` with nested `<tspan>` for the main centered headline
- 1× `<rect>` for the large rounded bullet card
- 1× `<rect>` for the glowing accent divider inside the card
- 5× `<circle>` for numbered/check bullet markers
- 5× `<path>` for check marks inside bullet markers
- 5× `<text>` for bullet copy, each with explicit `width`
- 3× `<linearGradient>` for background, card, and accent fills
- 1× `<radialGradient>` for bullet marker glow
- 2× `<filter>` for soft shadow and background glow effects

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#F8FBFF"/>
      <stop offset="0.48" stop-color="#F3F6FF"/>
      <stop offset="1" stop-color="#FFF7F0"/>
    </linearGradient>

    <linearGradient id="cardGrad" x1="255" y1="300" x2="1025" y2="620" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF"/>
      <stop offset="1" stop-color="#F8FAFF"/>
    </linearGradient>

    <linearGradient id="accentGrad" x1="314" y1="0" x2="966" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#6A5CFF"/>
      <stop offset="0.45" stop-color="#27D3C3"/>
      <stop offset="1" stop-color="#FFB457"/>
    </linearGradient>

    <radialGradient id="dotGrad" cx="35%" cy="25%" r="75%">
      <stop offset="0" stop-color="#FFFFFF"/>
      <stop offset="0.3" stop-color="#62E0D1"/>
      <stop offset="1" stop-color="#5B55F4"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="blobGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="28"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <path d="M-80 132 C80 28 206 14 294 86 C385 160 308 270 416 338 C296 372 164 334 72 266 C-6 208 -58 190 -80 132 Z"
        fill="#7B61FF" opacity="0.12" filter="url(#blobGlow)"/>
  <path d="M1046 478 C1136 392 1282 406 1362 512 C1438 612 1354 738 1210 748 C1098 756 1008 706 988 622 C974 562 1000 520 1046 478 Z"
        fill="#FFB457" opacity="0.18" filter="url(#blobGlow)"/>

  <rect x="531" y="82" width="218" height="38" rx="19" fill="#FFFFFF" opacity="0.82"/>
  <text x="640" y="107" width="218" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700"
        letter-spacing="1.8" fill="#5B55F4">KEY TAKEAWAYS</text>

  <text x="640" y="173" width="900" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="58" font-weight="800"
        fill="#151A2D">
    <tspan x="640" dy="0">Three moves that make</tspan>
    <tspan x="640" dy="66" fill="#5B55F4">strategy stick</tspan>
  </text>

  <rect x="255" y="306" width="770" height="304" rx="38"
        fill="url(#cardGrad)" filter="url(#softShadow)"/>
  <rect x="314" y="340" width="652" height="7" rx="3.5" fill="url(#accentGrad)"/>

  <circle cx="338" cy="386" r="17" fill="url(#dotGrad)"/>
  <path d="M330 386 L336 392 L347 379" fill="none" stroke="#FFFFFF" stroke-width="4"
        stroke-linecap="round" stroke-linejoin="round"/>
  <text x="374" y="395" width="560"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="25" font-weight="600"
        fill="#22283A">Align the team around one clear outcome</text>

  <circle cx="338" cy="432" r="17" fill="url(#dotGrad)"/>
  <path d="M330 432 L336 438 L347 425" fill="none" stroke="#FFFFFF" stroke-width="4"
        stroke-linecap="round" stroke-linejoin="round"/>
  <text x="374" y="441" width="590"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="25" font-weight="600"
        fill="#22283A">Turn insights into visible operating choices</text>

  <circle cx="338" cy="478" r="17" fill="url(#dotGrad)"/>
  <path d="M330 478 L336 484 L347 471" fill="none" stroke="#FFFFFF" stroke-width="4"
        stroke-linecap="round" stroke-linejoin="round"/>
  <text x="374" y="487" width="610"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="25" font-weight="600"
        fill="#22283A">Cut low-value work before adding initiatives</text>

  <circle cx="338" cy="524" r="17" fill="url(#dotGrad)"/>
  <path d="M330 524 L336 530 L347 517" fill="none" stroke="#FFFFFF" stroke-width="4"
        stroke-linecap="round" stroke-linejoin="round"/>
  <text x="374" y="533" width="570"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="25" font-weight="600"
        fill="#22283A">Review progress in a cadence people trust</text>

  <circle cx="338" cy="570" r="17" fill="url(#dotGrad)"/>
  <path d="M330 570 L336 576 L347 563" fill="none" stroke="#FFFFFF" stroke-width="4"
        stroke-linecap="round" stroke-linejoin="round"/>
  <text x="374" y="579" width="570"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="25" font-weight="600"
        fill="#22283A">Celebrate proof, then scale what works</text>
</svg>
```

## Avoid in this skill
- ❌ Dense bullet paragraphs; this layout works best when each bullet fits on one line or a very short wrap.
- ❌ Left-heavy title placement; the visual promise of this shell is centered hierarchy.
- ❌ Tiny default bullet symbols; use custom circles, checks, or numbered markers so the list feels intentional.
- ❌ Excessive decorative shapes behind the bullet text; keep the reading zone clean and high-contrast.

## Composition notes
- Keep the headline in the upper-middle third, with generous negative space above and around it.
- Place the bullet card below the title, centered horizontally; aim for a card width around 60–65% of the slide.
- Use 3–5 bullets maximum, with large type and consistent vertical rhythm.
- Let color appear as accents—marker dots, divider line, and subtle background glow—while the main text remains dark and readable.