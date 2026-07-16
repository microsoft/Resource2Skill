# SVG Recipe — Actionable Personalized Closing Slide

## Visual mechanism
A premium closing slide that turns “thank you” into an actionable contact moment: a restrained dark corporate field, a large left-aligned thank-you stack, a warm rotated signature, and a high-contrast QR card anchored in the lower-right. The asymmetry keeps the slide calm during Q&A while making the next step unmistakable.

## SVG primitives needed
- 1× `<rect>` for the full-slide deep blue gradient background
- 1× `<ellipse>` for a subtle atmospheric glow behind the QR/contact area
- 1× `<path>` for a faint diagonal decorative sweep in the upper-right
- 2× `<rect>` for the minimalist logo mark
- 6× `<text>` for company name, closing title, personalized signature, email, QR CTA label, and URL hint
- 1× `<path>` for a small envelope/contact icon
- 1× `<path>` for the handwritten signature flourish underline
- 2× `<rect>` for the QR card body and small CTA header accent
- 1× `<image>` for the real scannable QR code
- 1× `<filter id="cardShadow">` applied to the QR card rectangle
- 1× `<filter id="softGlow">` applied to decorative atmosphere paths/ellipses

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgBlue" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#081A42"/>
      <stop offset="0.58" stop-color="#0D214F"/>
      <stop offset="1" stop-color="#102B66"/>
    </linearGradient>

    <radialGradient id="aura" cx="50%" cy="50%" r="55%">
      <stop offset="0" stop-color="#6EA8FF" stop-opacity="0.34"/>
      <stop offset="0.55" stop-color="#315EA8" stop-opacity="0.12"/>
      <stop offset="1" stop-color="#0D214F" stop-opacity="0"/>
    </radialGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="16"/>
    </filter>
  </defs>

  <!-- Background -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#bgBlue)"/>

  <!-- Subtle premium atmosphere -->
  <ellipse cx="1015" cy="505" rx="360" ry="250" fill="url(#aura)" opacity="0.72" filter="url(#softGlow)"/>
  <path d="M760 58 C900 22 1045 40 1198 112 C1245 134 1275 158 1305 190 L1305 0 L760 0 Z"
        fill="#FFFFFF" opacity="0.045" filter="url(#softGlow)"/>

  <!-- Minimal logo -->
  <rect x="92" y="78" width="34" height="34" rx="6" fill="#FFFFFF"/>
  <rect x="103" y="89" width="12" height="12" rx="2" fill="#0D214F"/>
  <text x="146" y="102" width="410"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" fill="#FFFFFF" letter-spacing="0.2">
    Northstar Advisory
  </text>

  <!-- Small context line -->
  <text x="92" y="210" width="600"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="600" fill="#9FB7E8" letter-spacing="2.6">
    NEXT STEPS &amp; FOLLOW-UP
  </text>

  <!-- Main closing title -->
  <text x="88" y="314" width="740"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="86" font-weight="800" fill="#FFFFFF" letter-spacing="-2.4">
    Thank you
  </text>

  <!-- Personal handwritten signature -->
  <text x="98" y="442" width="520"
        transform="rotate(-5 260 430)"
        font-family="Segoe Script, Brush Script MT, Segoe UI, cursive"
        font-size="64" fill="#FFFFFF" opacity="0.98">
    Jane Doe
  </text>

  <!-- Signature flourish -->
  <path d="M108 476 C176 493 263 493 344 472 C386 461 421 457 452 469"
        transform="rotate(-5 280 475)"
        fill="none" stroke="#FFFFFF" stroke-width="3.2" stroke-linecap="round" opacity="0.86"/>

  <!-- Contact row -->
  <path d="M98 548 L130 548 C136 548 140 552 140 558 L140 581 C140 587 136 591 130 591 L98 591 C92 591 88 587 88 581 L88 558 C88 552 92 548 98 548 Z
           M92 555 L114 572 L136 555"
        fill="none" stroke="#BFD0F4" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"/>
  <text x="158" y="576" width="520"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="25" font-weight="500" fill="#FFFFFF">
    jane.doe@example.com
  </text>

  <!-- Optional micro-copy -->
  <text x="92" y="625" width="620"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" fill="#9FB7E8">
    Scan the code or email me for the recap, benchmarks, and implementation checklist.
  </text>

  <!-- QR action card -->
  <rect x="926" y="360" width="250" height="292" rx="28"
        fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="950" y="383" width="202" height="38" rx="19"
        fill="#0D214F"/>
  <text x="970" y="408" width="170"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="800" fill="#FFFFFF" text-anchor="middle">
    SCAN TO CONNECT
  </text>

  <!-- Real QR code image; replace data URL/endpoint with the client’s target URL -->
  <image x="963" y="438" width="176" height="176"
         href="https://api.qrserver.com/v1/create-qr-code/?size=176x176&amp;margin=8&amp;data=https%3A%2F%2Fwww.linkedin.com%2Fin%2Fjane-doe"
         xlink:href="https://api.qrserver.com/v1/create-qr-code/?size=176x176&amp;margin=8&amp;data=https%3A%2F%2Fwww.linkedin.com%2Fin%2Fjane-doe"/>

  <text x="951" y="632" width="200"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="600" fill="#56657F" text-anchor="middle">
    linkedin.com/in/jane-doe
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<a>` wrappers for clickable email/QR links; add hyperlinks in PowerPoint after conversion if interactivity is required.
- ❌ Do not use `<animate>` or ink-style SVG animation to simulate handwriting; PowerPoint “Wipe” or “Ink Replay” should be applied manually after import.
- ❌ Do not use `<mask>` to reveal the signature stroke; masks can hard-fail the slide.
- ❌ Do not place the QR code too close to the slide edge; leave enough quiet margin so phone cameras can scan it.
- ❌ Do not rely on script fonts alone for critical contact details; keep the email and URL in clean Segoe UI.

## Composition notes
- Keep the left 55–60% as a disciplined text stack: logo, small context label, large “Thank you,” signature, then contact info.
- Anchor the QR card in the lower-right quadrant with generous negative space above it; it should feel intentional, not like a footer sticker.
- Use pure white for the title/signature and muted blue-gray for secondary copy to preserve hierarchy on the dark background.
- The signature rotation should be subtle, around -4° to -7°; more rotation starts to feel playful rather than executive.