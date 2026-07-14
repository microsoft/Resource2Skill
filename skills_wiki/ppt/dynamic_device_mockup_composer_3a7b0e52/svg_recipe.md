# SVG Recipe — Dynamic Device Mockup Composer

## Visual mechanism
A premium phone mockup is built from a clipped vertical screenshot, a layered vector bezel, and a small notch/camera assembly, then placed dead-center as the focal point. Symmetrical icon-and-copy blocks on both sides use opposing alignments to visually funnel attention toward the device.

## SVG primitives needed
- 1× `<image>` for the app screenshot, clipped to a rounded phone-screen shape
- 1× `<clipPath>` with rounded `<rect>` for the precise screen crop
- 3× `<rect>` for the phone outer hardware, inner screen edge, and notch
- 2× `<circle>` for camera/sensor details
- 1× `<filter id="phoneShadow">` for the deep floating device shadow
- 1× `<filter id="softGlow">` for subtle premium icon glows
- 1× `<linearGradient>` for the slide background
- 1× `<linearGradient>` for the phone bezel highlight
- 1× `<radialGradient>` for soft ambient background accents
- 4× icon clusters made from `<circle>`, `<path>`, and `<line>`
- 9× `<text>` elements with explicit `width` attributes for title, subtitle, feature headings, and descriptions
- 2× `<line>` elements for subtle connector accents pointing toward the device

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="55%" stop-color="#F7F9FC"/>
      <stop offset="100%" stop-color="#EEF3FA"/>
    </linearGradient>

    <radialGradient id="aura" cx="50%" cy="48%" r="46%">
      <stop offset="0%" stop-color="#DCEBFF" stop-opacity="0.95"/>
      <stop offset="55%" stop-color="#F1F7FF" stop-opacity="0.42"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="bezelGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#3B3B3D"/>
      <stop offset="42%" stop-color="#151517"/>
      <stop offset="100%" stop-color="#050506"/>
    </linearGradient>

    <linearGradient id="iconGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#3D7CFF"/>
      <stop offset="100%" stop-color="#8A4DFF"/>
    </linearGradient>

    <filter id="phoneShadow" x="-30%" y="-20%" width="160%" height="150%">
      <feOffset dx="0" dy="22"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="7"/>
    </filter>

    <clipPath id="screenClip">
      <rect x="526" y="114" width="228" height="494" rx="34" ry="34"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <ellipse cx="640" cy="362" rx="360" ry="250" fill="url(#aura)"/>
  <circle cx="224" cy="142" r="88" fill="#EEF5FF"/>
  <circle cx="1064" cy="594" r="120" fill="#F1F2FF"/>

  <text x="640" y="58" width="620" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#111111">
    Product experience, composed for launch
  </text>
  <text x="640" y="88" width="560" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#747B86">
    Drop a raw screenshot into a polished, editable device frame with keynote-grade balance.
  </text>

  <rect x="503" y="88" width="274" height="552" rx="46" ry="46"
        fill="url(#bezelGrad)" filter="url(#phoneShadow)"/>
  <rect x="517" y="102" width="246" height="524" rx="39" ry="39"
        fill="#050506"/>
  <image x="526" y="114" width="228" height="494" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#screenClip)"
         href="https://images.example.com/mobile-finance-app-dashboard-screenshot-tall.png"/>
  <rect x="526" y="114" width="228" height="494" rx="34" ry="34"
        fill="none" stroke="#202124" stroke-width="2"/>
  <rect x="596" y="119" width="88" height="23" rx="11.5" ry="11.5" fill="#080809"/>
  <circle cx="696" cy="130.5" r="4.4" fill="#1A1F28"/>
  <circle cx="696" cy="130.5" r="1.7" fill="#415B77"/>

  <rect x="548" y="524" width="184" height="56" rx="18" ry="18" fill="#FFFFFF" opacity="0.92"/>
  <circle cx="577" cy="552" r="16" fill="#1F7AFF"/>
  <path d="M570 552 L576 558 L586 545" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="604" y="548" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#111111">
    Live portfolio
  </text>
  <text x="604" y="566" width="118" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#6B7280">
    +18.4% this month
  </text>

  <line x1="416" y1="218" x2="500" y2="246" stroke="#D5DCE8" stroke-width="2" stroke-dasharray="5 8"/>
  <line x1="864" y1="218" x2="780" y2="246" stroke="#D5DCE8" stroke-width="2" stroke-dasharray="5 8"/>

  <circle cx="388" cy="202" r="24" fill="#FFFFFF" filter="url(#softGlow)" opacity="0.9"/>
  <circle cx="388" cy="202" r="24" fill="url(#iconGrad)"/>
  <path d="M379 205 C379 198 384 193 391 193 C398 193 403 198 403 205 C403 211 398 216 391 216 L380 216 L380 211 L391 211 C395 211 398 208 398 205 C398 201 395 198 391 198 C387 198 384 201 384 205 Z"
        fill="#FFFFFF"/>
  <text x="356" y="194" width="220" text-anchor="end"
        font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#111111">
    Frictionless onboarding
  </text>
  <text x="356" y="222" width="230" text-anchor="end"
        font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#777E89">
    Show the first-run flow inside a realistic mobile context.
  </text>

  <circle cx="892" cy="202" r="24" fill="#FFFFFF" filter="url(#softGlow)" opacity="0.9"/>
  <circle cx="892" cy="202" r="24" fill="url(#iconGrad)"/>
  <path d="M881 210 L881 194 L886 194 L886 210 Z M890 210 L890 188 L895 188 L895 210 Z M899 210 L899 199 L904 199 L904 210 Z"
        fill="#FFFFFF"/>
  <text x="924" y="194" width="230"
        font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#111111">
    Real-time analytics
  </text>
  <text x="924" y="222" width="240"
        font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#777E89">
    Feature callouts stay editable while the screenshot remains photo-real.
  </text>

  <circle cx="388" cy="432" r="24" fill="#FFFFFF" filter="url(#softGlow)" opacity="0.9"/>
  <circle cx="388" cy="432" r="24" fill="url(#iconGrad)"/>
  <path d="M376 432 C382 420 394 420 400 432 C394 444 382 444 376 432 Z"
        fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linejoin="round"/>
  <circle cx="388" cy="432" r="4" fill="#FFFFFF"/>
  <text x="356" y="424" width="230" text-anchor="end"
        font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#111111">
    Focused visual proof
  </text>
  <text x="356" y="452" width="230" text-anchor="end"
        font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#777E89">
    The bezel masks messy screenshot edges and creates instant product credibility.
  </text>

  <circle cx="892" cy="432" r="24" fill="#FFFFFF" filter="url(#softGlow)" opacity="0.9"/>
  <circle cx="892" cy="432" r="24" fill="url(#iconGrad)"/>
  <path d="M881 424 L903 424 L903 439 L881 439 Z M886 419 L898 419 L898 424 L886 424 Z"
        fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linejoin="round"/>
  <text x="924" y="424" width="230"
        font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#111111">
    Editable slide system
  </text>
  <text x="924" y="452" width="240"
        font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#777E89">
    Swap the screenshot, recolor icons, and rewrite labels directly in PowerPoint.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Applying `clip-path` to a group of screenshot-like vector UI shapes; only clip the `<image>` itself.
- ❌ Using `<mask>` to punch the phone screen out of the bezel; use layered rounded rectangles or a path instead.
- ❌ Using `marker-end` for connector arrows; if arrows are needed, build arrowheads manually with small `<path>` triangles.
- ❌ Relying on raster-only phone frame PNGs; the bezel, notch, and sensor details should remain native editable shapes.
- ❌ Leaving text boxes without `width`; PowerPoint will not reliably preserve wrapping or alignment.

## Composition notes
- Keep the phone centered and tall: about 20–22% of slide width and 75–80% of slide height creates a strong keynote-style focal object.
- Left-side text should be right-aligned; right-side text should be left-aligned, with icons closest to the phone.
- Use a very light background with soft radial accents so the dark device silhouette has maximum contrast.
- Make the screenshot slightly inset beneath the bezel so rounded corners look intentional, not like a raw rectangle pasted on top.