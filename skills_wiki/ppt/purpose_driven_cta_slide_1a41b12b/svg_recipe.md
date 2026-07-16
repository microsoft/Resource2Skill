# SVG Recipe — Purpose-Driven CTA Slide

## Visual mechanism
A purpose-driven CTA slide pairs a direct contact action with a human-impact story, so the audience leaves with both a practical next step and an emotional reason to engage. Use a confident full-bleed brand color, one warm beneficiary photo, a large contact icon, and a clear “business action → social outcome” narrative.

## SVG primitives needed
- 1× full-canvas `<rect>` for the deep brand background
- 2× `<linearGradient>` for premium blue background depth and CTA card sheen
- 1× `<radialGradient>` for a soft emotional glow behind the impact story
- 2× `<filter>` for editable soft shadows/glows on cards and emphasis shapes
- 1× `<clipPath>` with rounded `<rect>` applied to the beneficiary `<image>`
- 1× `<image>` for the human-impact / beneficiary photograph
- 5× `<rect>` for photo frame, CTA card, impact story card, impact badge, and small label pills
- 4× decorative `<path>` elements for organic purpose shapes, heart/leaf icon, and brand flourishes
- 3× `<line>` elements for subtle divider / connector strokes
- Multiple `<text>` elements with explicit `width` for title, company name, tagline, email, narrative, metrics, and labels
- 3× `<circle>` / `<ellipse>` elements for icon backgrounds, glow accents, and small connector dots

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgBlue" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#123B96"/>
      <stop offset="55%" stop-color="#1D4EB9"/>
      <stop offset="100%" stop-color="#082B72"/>
    </linearGradient>

    <linearGradient id="ctaCard" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.19"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.07"/>
    </linearGradient>

    <linearGradient id="impactAccent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#9ED4FF"/>
      <stop offset="100%" stop-color="#D6E5FF"/>
    </linearGradient>

    <radialGradient id="warmGlow" cx="50%" cy="50%" r="65%">
      <stop offset="0%" stop-color="#FFE7A8" stop-opacity="0.44"/>
      <stop offset="70%" stop-color="#FFE7A8" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#FFE7A8" stop-opacity="0"/>
    </radialGradient>

    <filter id="shadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-35%" y="-35%" width="170%" height="170%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>

    <clipPath id="photoClip">
      <rect x="78" y="188" width="378" height="378" rx="34" ry="34"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgBlue)"/>

  <path d="M1038,-40 C1130,8 1194,74 1280,54 L1280,0 L1038,0 Z" fill="#6EA8FF" opacity="0.18"/>
  <path d="M-70,638 C88,590 182,652 290,718 L0,720 Z" fill="#FFFFFF" opacity="0.07"/>
  <path d="M1114,585 C1178,556 1234,579 1290,630 L1290,720 L1070,720 C1054,674 1064,609 1114,585 Z" fill="#9ED4FF" opacity="0.12"/>

  <text x="70" y="80" width="440" font-family="Segoe UI, Microsoft YaHei" font-size="52" font-weight="300" fill="#CCDAF9">Virtual CFO</text>
  <text x="74" y="116" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="600" letter-spacing="1.2" fill="#FFFFFF" opacity="0.88">BY DECISIONS PLUS STRATEGIC</text>

  <text x="704" y="78" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="31" font-weight="400" text-anchor="end" fill="#C7C7C7">
    Connect with us and make a difference
  </text>

  <rect x="60" y="170" width="414" height="430" rx="42" fill="#08265F" opacity="0.36" filter="url(#shadow)"/>
  <image x="78" y="188" width="378" height="378" preserveAspectRatio="xMidYMid slice"
         href="https://images.unsplash.com/photo-1605786184133-2558509a55a8?auto=format&amp;fit=crop&amp;w=900&amp;q=80"
         clip-path="url(#photoClip)"/>

  <rect x="102" y="514" width="316" height="68" rx="22" fill="#071C4B" opacity="0.78"/>
  <text x="128" y="541" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#9ED4FF" letter-spacing="0.8">PURPOSE PARTNER</text>
  <text x="128" y="565" width="282" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" fill="#FFFFFF">Micro-business training in Malawi</text>

  <ellipse cx="760" cy="432" rx="280" ry="170" fill="url(#warmGlow)" filter="url(#softGlow)" opacity="0.72"/>

  <rect x="538" y="184" width="642" height="164" rx="38" fill="url(#ctaCard)" stroke="#FFFFFF" stroke-opacity="0.20" stroke-width="1.2" filter="url(#shadow)"/>
  <circle cx="623" cy="266" r="48" fill="#D6E5FF" opacity="0.18"/>
  <text x="589" y="286" width="78" font-family="Segoe UI, Microsoft YaHei" font-size="72" font-weight="700" fill="#FFFFFF">@</text>

  <text x="700" y="245" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" letter-spacing="1.4" fill="#9ED4FF">START THE CONVERSATION</text>
  <text x="698" y="292" width="460" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#FFFFFF">hello@decisionsplusstrategic.com</text>
  <line x1="700" y1="314" x2="1110" y2="314" stroke="#FFFFFF" stroke-opacity="0.28" stroke-width="2"/>

  <rect x="538" y="390" width="642" height="214" rx="36" fill="#FFFFFF" opacity="0.10" stroke="#D6E5FF" stroke-opacity="0.20" stroke-width="1.2"/>
  <rect x="570" y="416" width="128" height="34" rx="17" fill="url(#impactAccent)" opacity="0.96"/>
  <text x="592" y="439" width="86" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" fill="#123B96" letter-spacing="0.9">IMPACT</text>

  <path d="M1060 426 C1060 407 1088 402 1098 421 C1108 402 1136 407 1136 426 C1136 456 1098 476 1098 476 C1098 476 1060 456 1060 426 Z" fill="#FFE7A8" opacity="0.92"/>
  <path d="M1098 476 C1112 462 1124 452 1146 452 C1129 470 1112 481 1098 476 Z" fill="#9ED4FF" opacity="0.88"/>

  <text x="570" y="492" width="470" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#FFFFFF">
    Every engagement funds practical business skills.
  </text>
  <text x="570" y="532" width="548" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="400" fill="#EAF1FF" opacity="0.94">
    Each time we collaborate in a Virtual CFO engagement, 500 women in Malawi receive start-up and bookkeeping training to grow micro-businesses and lift families out of poverty.
  </text>

  <line x1="488" y1="380" x2="536" y2="380" stroke="#9ED4FF" stroke-width="2" stroke-dasharray="6 8" opacity="0.72"/>
  <circle cx="488" cy="380" r="5" fill="#9ED4FF"/>
  <circle cx="536" cy="380" r="5" fill="#D6E5FF"/>

  <rect x="74" y="626" width="310" height="38" rx="19" fill="#FFFFFF" opacity="0.12"/>
  <text x="99" y="651" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#D6E5FF">Business partnership with measurable good</text>

  <text x="570" y="658" width="148" font-family="Segoe UI, Microsoft YaHei" font-size="56" font-weight="800" fill="#FFE7A8">500</text>
  <text x="715" y="642" width="310" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF">women trained per engagement</text>
  <text x="715" y="667" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="400" fill="#C7D8FF">through B1G1 and MicroLoan Australia</text>

  <line x1="70" y1="136" x2="272" y2="136" stroke="#9ED4FF" stroke-width="3" opacity="0.82"/>
</svg>
```

## Avoid in this skill
- ❌ A plain “Thank you / Contact us” slide with no impact story; the technique depends on connecting action to purpose.
- ❌ Overcrowding the story area with too many CSR statistics; one emotional metric is stronger than a dashboard.
- ❌ Applying `clip-path` to decorative rectangles or paths; only clip the photo `<image>`.
- ❌ Using `marker-end` arrowheads for the business-to-impact connector; use simple `<line>` strokes and small circles instead.
- ❌ Low-contrast gray text on blue for the email; the CTA must remain immediately readable.

## Composition notes
- Keep the left 30–35% as the human anchor: photo, impact label, and a small purpose caption.
- Reserve the right 60–65% for the CTA card and story card, with the email placed near the visual center.
- Use one warm accent, such as pale gold, only for the impact metric or heart mark so it feels meaningful.
- Maintain generous blue negative space around the title and top tagline; the final slide should feel confident, not crowded.