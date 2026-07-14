# SVG Recipe — Vintage Newspaper Layout

## Visual mechanism
A faux broadsheet front page: aged cream paper, double black rules, a dramatic masthead, dense three-column editorial text, and high-contrast monochrome imagery. The visual authority comes from strict grid discipline, serif hierarchy, tight rules, and small “newsprint” details like captions, edition labels, and miniature data graphics.

## SVG primitives needed
- 2× `<rect>` for the full-slide background and raised newspaper sheet
- 2× `<rect>` with strokes for the double page border
- 1× `<radialGradient>` for darkened paper edges / vignette
- 1× `<linearGradient>` for uneven aged-paper warmth
- 1× `<filter id="paperShadow">` using `feOffset`, `feGaussianBlur`, `feMerge` for the lifted paper shadow
- 5–8× low-opacity `<path>` / `<ellipse>` for editable stains, creases, and ink smudges
- 12–18× `<line>` for masthead rules, dateline rules, article separators, and column dividers
- 1× `<clipPath>` with rounded `<rect>` applied to the newspaper photo
- 1× `<image>` for a grayscale or already desaturated editorial photo
- 1× `<path>` for a small black line-chart inset
- Many `<text>` blocks with explicit `width` attributes for masthead, dateline, headlines, captions, pull-quotes, and column copy
- Nested `<tspan>` elements for line-broken newspaper paragraphs and inline emphasis

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="paperBase" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f4eee3"/>
      <stop offset="48%" stop-color="#efe4cf"/>
      <stop offset="100%" stop-color="#dfcfad"/>
    </linearGradient>

    <radialGradient id="edgeVignette" cx="50%" cy="45%" r="72%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0"/>
      <stop offset="62%" stop-color="#c8b9a0" stop-opacity="0.05"/>
      <stop offset="100%" stop-color="#8f7759" stop-opacity="0.36"/>
    </radialGradient>

    <filter id="paperShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feOffset dx="0" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softInk" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="5"/>
    </filter>

    <clipPath id="photoCrop">
      <rect x="465" y="288" width="330" height="166" rx="4" ry="4"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#2a241e"/>
  <rect x="58" y="34" width="1164" height="652" rx="2" fill="url(#paperBase)" filter="url(#paperShadow)"/>
  <rect x="58" y="34" width="1164" height="652" rx="2" fill="url(#edgeVignette)"/>

  <path d="M118 102 C210 74, 286 102, 372 83 C450 66, 546 77, 626 102" fill="none" stroke="#8a7354" stroke-width="3" opacity="0.08" filter="url(#softInk)"/>
  <path d="M892 86 C952 132, 1042 96, 1130 138 C1178 161, 1185 224, 1148 257" fill="none" stroke="#6f5a42" stroke-width="5" opacity="0.07" filter="url(#softInk)"/>
  <ellipse cx="222" cy="612" rx="94" ry="25" fill="#6f5a42" opacity="0.045" filter="url(#softInk)"/>
  <ellipse cx="1045" cy="558" rx="128" ry="34" fill="#6f5a42" opacity="0.04" filter="url(#softInk)"/>

  <rect x="82" y="58" width="1116" height="604" fill="none" stroke="#000000" stroke-width="2"/>
  <rect x="95" y="71" width="1090" height="578" fill="none" stroke="#000000" stroke-width="0.8"/>

  <line x1="110" y1="112" x2="1170" y2="112" stroke="#000000" stroke-width="1.4"/>
  <text x="110" y="99" width="210" font-family="Georgia, 'Times New Roman', serif" font-size="13" font-weight="700" fill="#000000" letter-spacing="1.4">
    VOL. XLVII
  </text>
  <text x="970" y="99" width="200" font-family="Georgia, 'Times New Roman', serif" font-size="13" font-weight="700" fill="#000000" text-anchor="end" letter-spacing="1.4">
    PRICE 5¢
  </text>

  <text x="640" y="168" width="1040" font-family="'Times New Roman', Georgia, serif" font-size="68" font-weight="700" fill="#000000" text-anchor="middle" letter-spacing="-1.5">
    THE DAILY CHRONICLE
  </text>

  <line x1="110" y1="190" x2="1170" y2="190" stroke="#000000" stroke-width="3"/>
  <line x1="110" y1="199" x2="1170" y2="199" stroke="#000000" stroke-width="0.9"/>

  <text x="110" y="222" width="1060" font-family="Georgia, 'Times New Roman', serif" font-size="14" font-weight="700" fill="#000000" text-anchor="middle" letter-spacing="1.8">
    SPECIAL MARKET EDITION  •  MONDAY, OCTOBER 21  •  INDUSTRY BRIEFING FOR EXECUTIVE READERS
  </text>
  <line x1="110" y1="238" x2="1170" y2="238" stroke="#000000" stroke-width="1"/>

  <text x="110" y="282" width="330" font-family="Georgia, 'Times New Roman', serif" font-size="31" font-weight="700" fill="#000000">
    Quarter Opens With Record Demand
  </text>
  <line x1="110" y1="308" x2="440" y2="308" stroke="#000000" stroke-width="0.8"/>

  <text x="110" y="332" width="330" font-family="Georgia, 'Times New Roman', serif" font-size="13.5" fill="#000000">
    <tspan x="110" dy="0">Executives reported a sharp rise in customer</tspan>
    <tspan x="110" dy="18">activity as orders advanced across priority</tspan>
    <tspan x="110" dy="18">accounts. The commercial desk described the</tspan>
    <tspan x="110" dy="18">movement as broad based, resilient, and more</tspan>
    <tspan x="110" dy="18">balanced than earlier forecasts had suggested.</tspan>
    <tspan x="110" dy="18">Analysts point to pricing discipline, faster</tspan>
    <tspan x="110" dy="18">cycle times, and improved retention as the</tspan>
    <tspan x="110" dy="18">principal engines of this week’s performance.</tspan>
    <tspan x="110" dy="18">The figures strengthen confidence in the</tspan>
    <tspan x="110" dy="18">annual plan while leaving room for careful</tspan>
    <tspan x="110" dy="18">investment in the next wave of expansion.</tspan>
  </text>

  <line x1="455" y1="258" x2="455" y2="626" stroke="#000000" stroke-width="0.8"/>
  <line x1="810" y1="258" x2="810" y2="626" stroke="#000000" stroke-width="0.8"/>

  <image x="465" y="288" width="330" height="166" clip-path="url(#photoCrop)"
         href="https://images.unsplash.com/photo-1504711434969-e33886168f5c?auto=format&amp;fit=crop&amp;w=900&amp;q=80"/>
  <rect x="465" y="288" width="330" height="166" fill="none" stroke="#000000" stroke-width="1.2"/>
  <text x="465" y="474" width="330" font-family="Georgia, 'Times New Roman', serif" font-size="11" font-style="italic" fill="#000000">
    Archive desk photograph, printed in high-contrast grayscale for a newsprint effect.
  </text>

  <text x="465" y="522" width="330" font-family="Georgia, 'Times New Roman', serif" font-size="25" font-weight="700" fill="#000000">
    Signals Strengthen Across Three Regions
  </text>
  <text x="465" y="555" width="330" font-family="Georgia, 'Times New Roman', serif" font-size="13.2" fill="#000000">
    <tspan x="465" dy="0">Regional teams posted synchronized gains,</tspan>
    <tspan x="465" dy="17">with the northern portfolio leading margin</tspan>
    <tspan x="465" dy="17">recovery. Leaders credited disciplined account</tspan>
    <tspan x="465" dy="17">planning and reduced operational friction.</tspan>
  </text>

  <text x="835" y="282" width="320" font-family="Georgia, 'Times New Roman', serif" font-size="28" font-weight="700" fill="#000000">
    Data Desk
  </text>
  <line x1="835" y1="300" x2="1155" y2="300" stroke="#000000" stroke-width="0.8"/>

  <rect x="835" y="318" width="320" height="132" fill="#eadfc9" stroke="#000000" stroke-width="1"/>
  <line x1="855" y1="420" x2="1138" y2="420" stroke="#000000" stroke-width="0.7"/>
  <line x1="855" y1="390" x2="1138" y2="390" stroke="#000000" stroke-width="0.4" stroke-dasharray="4 4"/>
  <line x1="855" y1="360" x2="1138" y2="360" stroke="#000000" stroke-width="0.4" stroke-dasharray="4 4"/>
  <path d="M858 412 L900 398 L940 402 L982 370 L1024 381 L1068 344 L1112 332 L1138 326"
        fill="none" stroke="#000000" stroke-width="3"/>
  <text x="850" y="342" width="280" font-family="Georgia, 'Times New Roman', serif" font-size="14" font-weight="700" fill="#000000">
    WEEKLY ORDER INDEX
  </text>
  <text x="850" y="470" width="305" font-family="Georgia, 'Times New Roman', serif" font-size="12.5" fill="#000000">
    <tspan x="850" dy="0">Index closes up 18 points after a late surge</tspan>
    <tspan x="850" dy="16">in enterprise renewals and new bookings.</tspan>
  </text>

  <line x1="835" y1="502" x2="1155" y2="502" stroke="#000000" stroke-width="1"/>
  <text x="835" y="532" width="320" font-family="Georgia, 'Times New Roman', serif" font-size="18" font-weight="700" fill="#000000">
    “The front page format makes dense updates feel consequential.”
  </text>
  <text x="835" y="582" width="320" font-family="Georgia, 'Times New Roman', serif" font-size="13.2" fill="#000000">
    <tspan x="835" dy="0">Use short paragraphs, hard rules, and compact</tspan>
    <tspan x="835" dy="17">headlines to create the impression of a</tspan>
    <tspan x="835" dy="17">credible printed record rather than a slide.</tspan>
  </text>

  <line x1="110" y1="636" x2="1170" y2="636" stroke="#000000" stroke-width="1.1"/>
  <text x="110" y="655" width="1060" font-family="Georgia, 'Times New Roman', serif" font-size="11" font-weight="700" fill="#000000" text-anchor="middle" letter-spacing="1.2">
    INSIDE: PRODUCT NOTES  •  OPERATIONS WATCH  •  CUSTOMER LEDGER  •  BOARDROOM BRIEFING
  </text>
</svg>
```

## Avoid in this skill
- ❌ `<pattern>` fills for paper grain; they may not translate reliably. Use gradients plus editable low-opacity stains instead.
- ❌ True SVG/CSS multi-column text flow; PowerPoint will not preserve it as editable text. Manually place each column as its own `<text>` block.
- ❌ `mask` for the vignette or distressed edges. Use a radial gradient overlay instead.
- ❌ `filter` on `<line>` elements for blurred ink rules; line filters are dropped. Apply blur only to editable `<path>`, `<rect>`, `<ellipse>`, or `<text>`.
- ❌ Relying on a rare Old English font for the masthead. Use Times New Roman or Georgia-style serif typography for safer PowerPoint editing.

## Composition notes
- Keep the masthead and dateline in the top 25–30% of the slide; the “newspaper” effect depends on a strong ceremonial header.
- Use a strict three-column grid below the masthead, with thin vertical dividers and narrow gutters.
- Reserve one column-width area for a grayscale photo or data inset so the slide does not become an unreadable wall of text.
- Foreground should remain almost entirely black; the visual richness comes from paper warmth, typography, rules, and density rather than color.