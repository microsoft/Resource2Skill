# SVG Recipe — Mobile-Optimized Digital Business Card with Interactive QR

## Visual mechanism
A standard 16:9 slide contains a centered 9:16 “phone card” composition, making the slide feel like a mobile-shareable profile screen. The visual flow is strictly vertical: avatar first, identity text second, contact details third, and a high-contrast QR action block anchored at the bottom.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark background
- 2× `<path>` for oversized geometric watermark shapes behind the phone card
- 1× `<rect>` for the vertical smartphone/business-card body
- 1× `<rect>` for a subtle inner glass highlight on the card
- 1× `<image>` clipped by `clipPath` for the circular avatar photo
- 2× `<circle>` for avatar border and accent glow ring
- 7× `<text>` for name, title, contact details, QR CTA, and microcopy; every text element needs explicit `width`
- 3× small `<circle>` plus 3× `<path>` icon glyphs for email, phone, and website contact rows
- 1× `<rect>` for the QR code white container
- Multiple `<rect>` and `<path>` elements for QR finder blocks and randomized QR modules
- 1× `<linearGradient>` for the premium dark slide background
- 1× `<linearGradient>` for the vertical phone-card fill
- 1× `<linearGradient>` for the purple-blue accent strokes and pills
- 2× `<filter>` definitions: one soft drop shadow for the phone/QR card and one glow for accent rings

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#111722"/>
      <stop offset="0.55" stop-color="#1E2330"/>
      <stop offset="1" stop-color="#10131B"/>
    </linearGradient>
    <linearGradient id="phoneGrad" x1="432" y1="24" x2="848" y2="696" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#2B3142"/>
      <stop offset="0.52" stop-color="#202633"/>
      <stop offset="1" stop-color="#171C27"/>
    </linearGradient>
    <linearGradient id="accentGrad" x1="520" y1="80" x2="760" y2="640" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#A78BFA"/>
      <stop offset="0.55" stop-color="#7C3AED"/>
      <stop offset="1" stop-color="#22D3EE"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="accentGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>
    <clipPath id="avatarClip">
      <circle cx="640" cy="148" r="68"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <path d="M80 88 L182 28 L288 88 L288 210 L182 270 L80 210 Z" fill="#293144" opacity="0.38" transform="rotate(-16 184 149)"/>
  <path d="M1010 420 L1148 342 L1288 420 L1288 580 L1148 658 L1010 580 Z" fill="#293144" opacity="0.32" transform="rotate(14 1148 500)"/>
  <path d="M292 615 C360 548 428 558 480 620 C530 682 402 730 314 704 C248 684 242 664 292 615 Z" fill="#7C3AED" opacity="0.08"/>
  <path d="M820 72 C902 18 1010 36 1048 104 C1084 170 1016 236 916 218 C822 202 754 116 820 72 Z" fill="#22D3EE" opacity="0.07"/>

  <rect x="432" y="24" width="416" height="672" rx="48" fill="#06080D" filter="url(#softShadow)"/>
  <rect x="444" y="36" width="392" height="648" rx="40" fill="url(#phoneGrad)" stroke="#3D465C" stroke-width="1.2"/>
  <rect x="470" y="58" width="340" height="594" rx="30" fill="none" stroke="#FFFFFF" stroke-opacity="0.08"/>
  <rect x="588" y="50" width="104" height="8" rx="4" fill="#0D111A" opacity="0.95"/>

  <circle cx="640" cy="148" r="82" fill="url(#accentGrad)" opacity="0.34" filter="url(#accentGlow)"/>
  <circle cx="640" cy="148" r="74" fill="none" stroke="url(#accentGrad)" stroke-width="5"/>
  <image x="572" y="80" width="136" height="136" clip-path="url(#avatarClip)"
         href="https://images.unsplash.com/photo-1560250097-0b93528c311a?q=80&amp;w=500&amp;auto=format&amp;fit=crop"/>
  <circle cx="640" cy="148" r="69" fill="none" stroke="#FFFFFF" stroke-width="3"/>

  <text x="500" y="255" width="280" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="34" font-weight="700" fill="#FFFFFF">Joe Zeplin</text>
  <text x="500" y="288" width="280" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="700" letter-spacing="2.4" fill="#A78BFA">SOCIAL MEDIA MANAGER</text>
  <text x="500" y="326" width="280" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" fill="#B9C0CF">Digital strategy • Creator partnerships</text>

  <circle cx="530" cy="372" r="15" fill="#FFFFFF" opacity="0.08"/>
  <path d="M522 367 H538 V378 H522 Z M522 367 L530 373 L538 367" fill="none" stroke="#A78BFA" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="558" y="377" width="190" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" fill="#E2E6EF">joe.zeplin@example.com</text>

  <circle cx="530" cy="408" r="15" fill="#FFFFFF" opacity="0.08"/>
  <path d="M525 400 C529 411 535 416 540 417 L542 412 L536 409 L532 413 C529 411 527 407 526 404 L530 401 Z"
        fill="#22D3EE" opacity="0.92"/>
  <text x="558" y="413" width="190" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" fill="#E2E6EF">+1 415 555 0198</text>

  <circle cx="530" cy="444" r="15" fill="#FFFFFF" opacity="0.08"/>
  <path d="M522 444 H538 M530 436 C525 440 525 448 530 452 M530 436 C535 440 535 448 530 452 M523 439 C527 441 533 441 537 439 M523 449 C527 447 533 447 537 449"
        fill="none" stroke="#A78BFA" stroke-width="1.5" stroke-linecap="round"/>
  <text x="558" y="449" width="190" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" fill="#E2E6EF">linkedin.com/in/joezeplin</text>

  <rect x="528" y="478" width="224" height="176" rx="24" fill="#FFFFFF" filter="url(#softShadow)"/>
  <rect x="544" y="494" width="192" height="144" rx="10" fill="#F8FAFC"/>

  <rect x="558" y="508" width="42" height="42" fill="#0B0D12"/>
  <rect x="566" y="516" width="26" height="26" fill="#F8FAFC"/>
  <rect x="574" y="524" width="10" height="10" fill="#0B0D12"/>
  <rect x="680" y="508" width="42" height="42" fill="#0B0D12"/>
  <rect x="688" y="516" width="26" height="26" fill="#F8FAFC"/>
  <rect x="696" y="524" width="10" height="10" fill="#0B0D12"/>
  <rect x="558" y="582" width="42" height="42" fill="#0B0D12"/>
  <rect x="566" y="590" width="26" height="26" fill="#F8FAFC"/>
  <rect x="574" y="598" width="10" height="10" fill="#0B0D12"/>

  <path fill="#0B0D12" d="M612 508h8v8h-8z M628 508h8v8h-8z M644 508h8v8h-8z M660 508h8v8h-8z
    M620 524h8v8h-8z M644 524h8v8h-8z M668 524h8v8h-8z
    M612 540h8v8h-8z M636 540h8v8h-8z M652 540h8v8h-8z
    M612 558h8v8h-8z M628 558h8v8h-8z M660 558h8v8h-8z M692 558h8v8h-8z M716 558h8v8h-8z
    M612 574h8v8h-8z M636 574h8v8h-8z M668 574h8v8h-8z M700 574h8v8h-8z
    M620 590h8v8h-8z M644 590h8v8h-8z M660 590h8v8h-8z M684 590h8v8h-8z M708 590h8v8h-8z
    M612 606h8v8h-8z M636 606h8v8h-8z M652 606h8v8h-8z M676 606h8v8h-8z M700 606h8v8h-8z
    M620 622h8v8h-8z M644 622h8v8h-8z M668 622h8v8h-8z M692 622h8v8h-8z M716 622h8v8h-8z"/>

  <rect x="548" y="660" width="184" height="26" rx="13" fill="url(#accentGrad)"/>
  <text x="548" y="678" width="184" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" font-weight="700" letter-spacing="1.5" fill="#FFFFFF">SCAN TO CONNECT</text>
  <text x="500" y="708" width="280" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="11" fill="#818A9D">vCard • LinkedIn • Book a meeting</text>
</svg>
```

## Avoid in this skill
- ❌ Using a real 9:16 SVG canvas; keep `viewBox="0 0 1280 720"` and build the vertical mobile card inside it.
- ❌ Applying `clip-path` to circles or rects for avatar masking; apply the `clip-path` only to the `<image>`.
- ❌ Building the QR with `<pattern>` or `<use>`; use direct `<rect>` and `<path>` modules so the QR remains editable.
- ❌ Overloading the side margins with content; the phone card should remain the only functional object.
- ❌ Making the QR low contrast or decorative-only; it must read as a scan target with a clean white field.

## Composition notes
- Center the vertical card on the 1280×720 slide; a card around 400–430 px wide and 660–680 px tall preserves the mobile-screen illusion.
- Keep the avatar in the upper quarter, identity text immediately below, and reserve the bottom third for the QR block.
- Use a dark professional palette with one vivid accent gradient repeated in the avatar ring, title, icons, and scan CTA.
- Leave generous side negative space; subtle geometric watermarks may sit outside the phone card but should not compete with the QR.