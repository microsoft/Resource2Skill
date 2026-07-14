# SVG Recipe — Dark Neumorphism (Soft UI) Interface

## Visual mechanism
A dark Soft UI interface makes cards, buttons, sliders, and controls appear molded from the same charcoal surface by stacking two opposing blurred shadows: a cool light highlight toward the upper-left and a deep shadow toward the lower-right. Cyan accents are reserved for active controls and animated-looking equalizer bars so the tactile surface stays calm but futuristic.

## SVG primitives needed
- 1× full-slide `<rect>` for the dark charcoal canvas.
- 2× `<filter>` definitions: one blur-only filter for separated soft shadow layers, one offset blur shadow for small floating details.
- 2× `<linearGradient>` definitions for cyan active controls and subtle button sheen.
- 1× `<clipPath>` with `<circle>` for an editable circular avatar/photo crop.
- 1× `<image>` for the avatar/photo, clipped to a circle; use a non-identifying or abstract portrait/texture if privacy matters.
- Multiple layered `<rect>` elements for neumorphic cards, slider tracks, buttons, dropdown, and equalizer wells: light shadow layer, dark shadow layer, then same-color base shape.
- Multiple `<circle>` elements for circular icon buttons and slider knob.
- Multiple cyan `<rect>` elements for active equalizer bars and progress fill.
- Multiple `<text>` elements with explicit `width` attributes for labels, title, button text, initials/name, and icon glyphs.
- Optional small `<path>` elements for decorative chevrons or custom icon strokes when text glyphs are not enough.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <filter id="blurSoft" x="-35%" y="-35%" width="170%" height="170%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>
    <filter id="smallDrop" x="-40%" y="-40%" width="180%" height="180%">
      <feOffset dx="6" dy="7"/>
      <feGaussianBlur stdDeviation="7" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <linearGradient id="cyanGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#35dce2"/>
      <stop offset="100%" stop-color="#1fb2bd"/>
    </linearGradient>
    <linearGradient id="buttonSheen" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#323741"/>
      <stop offset="100%" stop-color="#252a31"/>
    </linearGradient>
    <clipPath id="avatarClip">
      <circle cx="458" cy="156" r="46"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#2e3239"/>

  <!-- Profile card: extruded from the same dark surface -->
  <rect x="318" y="58" width="270" height="294" rx="24" fill="#464b55" filter="url(#blurSoft)"/>
  <rect x="342" y="82" width="270" height="294" rx="24" fill="#141619" filter="url(#blurSoft)"/>
  <rect x="330" y="70" width="252" height="290" rx="23" fill="#2e3239"/>
  <rect x="330" y="70" width="252" height="290" rx="23" fill="none" stroke="#3a3f48" stroke-width="1.2"/>

  <image x="412" y="110" width="92" height="92"
         href="https://images.example.com/abstract-neutral-avatar-no-identifiable-face.jpg"
         clip-path="url(#avatarClip)" preserveAspectRatio="xMidYMid slice"/>
  <circle cx="458" cy="156" r="46" fill="none" stroke="#181a1e" stroke-width="3"/>
  <text x="413" y="250" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="42" fill="#32d6d9" text-anchor="middle" font-style="italic">Julie</text>

  <rect x="342" y="286" width="224" height="58" rx="29" fill="#141619" filter="url(#blurSoft)"/>
  <rect x="346" y="292" width="220" height="48" rx="24" fill="url(#cyanGrad)"/>
  <text x="346" y="321" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#ffffff" text-anchor="middle">Message</text>

  <!-- Equalizer wells and cyan active bars -->
  <rect x="680" y="110" width="42" height="245" rx="21" fill="#15171b" filter="url(#blurSoft)"/>
  <rect x="744" y="166" width="42" height="189" rx="21" fill="#15171b" filter="url(#blurSoft)"/>
  <rect x="812" y="134" width="42" height="221" rx="21" fill="#15171b" filter="url(#blurSoft)"/>
  <rect x="872" y="80" width="42" height="275" rx="21" fill="#15171b" filter="url(#blurSoft)"/>
  <rect x="936" y="190" width="42" height="165" rx="21" fill="#15171b" filter="url(#blurSoft)"/>
  <rect x="686" y="244" width="42" height="112" rx="21" fill="url(#cyanGrad)"/>
  <rect x="750" y="209" width="42" height="147" rx="21" fill="url(#cyanGrad)"/>
  <rect x="820" y="253" width="42" height="103" rx="21" fill="url(#cyanGrad)"/>
  <rect x="874" y="165" width="42" height="191" rx="21" fill="url(#cyanGrad)"/>
  <rect x="934" y="215" width="42" height="141" rx="21" fill="url(#cyanGrad)"/>

  <!-- Slider: recessed track plus active cyan fill -->
  <rect x="330" y="426" width="250" height="9" rx="5" fill="#16181c" filter="url(#blurSoft)"/>
  <rect x="332" y="427" width="176" height="8" rx="4" fill="url(#cyanGrad)"/>
  <circle cx="506" cy="432" r="12" fill="#eef2f6" filter="url(#smallDrop)"/>

  <!-- Media controls -->
  <rect x="330" y="484" width="54" height="54" rx="7" fill="#464b55" filter="url(#blurSoft)"/>
  <rect x="340" y="494" width="54" height="54" rx="7" fill="#141619" filter="url(#blurSoft)"/>
  <rect x="330" y="484" width="54" height="54" rx="7" fill="url(#buttonSheen)"/>
  <text x="330" y="520" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="40" fill="#ffffff" text-anchor="middle">‹</text>

  <rect x="430" y="484" width="54" height="54" rx="7" fill="#464b55" filter="url(#blurSoft)"/>
  <rect x="440" y="494" width="54" height="54" rx="7" fill="#141619" filter="url(#blurSoft)"/>
  <rect x="430" y="484" width="54" height="54" rx="7" fill="url(#buttonSheen)"/>
  <text x="430" y="520" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="25" fill="#ffffff" text-anchor="middle">Ⅱ</text>

  <rect x="530" y="484" width="54" height="54" rx="7" fill="#464b55" filter="url(#blurSoft)"/>
  <rect x="540" y="494" width="54" height="54" rx="7" fill="#141619" filter="url(#blurSoft)"/>
  <rect x="530" y="484" width="54" height="54" rx="7" fill="url(#buttonSheen)"/>
  <text x="530" y="520" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="40" fill="#ffffff" text-anchor="middle">›</text>

  <!-- Dropdown pill -->
  <rect x="334" y="578" width="238" height="56" rx="28" fill="#464b55" filter="url(#blurSoft)"/>
  <rect x="350" y="594" width="238" height="56" rx="28" fill="#141619" filter="url(#blurSoft)"/>
  <rect x="338" y="582" width="236" height="50" rx="25" fill="#2e3239"/>
  <text x="338" y="613" width="185" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#ffffff" text-anchor="middle">Dropdown</text>
  <path d="M522 606 L531 615 L540 606" fill="none" stroke="#ffffff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>

  <!-- Circular icon cluster -->
  <circle cx="716" cy="454" r="31" fill="#474c56" filter="url(#blurSoft)"/>
  <circle cx="728" cy="466" r="31" fill="#141619" filter="url(#blurSoft)"/>
  <circle cx="716" cy="454" r="29" fill="#2e3239"/>
  <text x="687" y="462" width="58" font-family="Segoe UI Symbol, Segoe UI" font-size="26" fill="#ffffff" text-anchor="middle">↶</text>

  <circle cx="800" cy="454" r="31" fill="#474c56" filter="url(#blurSoft)"/>
  <circle cx="812" cy="466" r="31" fill="#141619" filter="url(#blurSoft)"/>
  <circle cx="800" cy="454" r="29" fill="#2e3239"/>
  <text x="771" y="462" width="58" font-family="Segoe UI Symbol, Segoe UI" font-size="26" fill="#ffffff" text-anchor="middle">↷</text>

  <circle cx="884" cy="454" r="31" fill="#474c56" filter="url(#blurSoft)"/>
  <circle cx="896" cy="466" r="31" fill="#141619" filter="url(#blurSoft)"/>
  <circle cx="884" cy="454" r="29" fill="#2e3239"/>
  <text x="855" y="463" width="58" font-family="Segoe UI Symbol, Segoe UI" font-size="24" fill="#ffffff" text-anchor="middle">♟</text>

  <circle cx="968" cy="454" r="31" fill="#474c56" filter="url(#blurSoft)"/>
  <circle cx="980" cy="466" r="31" fill="#141619" filter="url(#blurSoft)"/>
  <circle cx="968" cy="454" r="29" fill="#2e3239"/>
  <text x="939" y="463" width="58" font-family="Segoe UI Symbol, Segoe UI" font-size="24" fill="#ffffff" text-anchor="middle">♬</text>

  <circle cx="716" cy="536" r="31" fill="#474c56" filter="url(#blurSoft)"/>
  <circle cx="728" cy="548" r="31" fill="#141619" filter="url(#blurSoft)"/>
  <circle cx="716" cy="536" r="29" fill="#2e3239"/>
  <text x="687" y="544" width="58" font-family="Segoe UI Symbol, Segoe UI" font-size="25" fill="#ffffff" text-anchor="middle">♥</text>

  <circle cx="800" cy="536" r="31" fill="#474c56" filter="url(#blurSoft)"/>
  <circle cx="812" cy="548" r="31" fill="#141619" filter="url(#blurSoft)"/>
  <circle cx="800" cy="536" r="29" fill="#2e3239"/>
  <text x="771" y="544" width="58" font-family="Segoe UI Symbol, Segoe UI" font-size="25" fill="#ffffff" text-anchor="middle">∞</text>

  <circle cx="884" cy="536" r="31" fill="#474c56" filter="url(#blurSoft)"/>
  <circle cx="896" cy="548" r="31" fill="#141619" filter="url(#blurSoft)"/>
  <circle cx="884" cy="536" r="29" fill="#2e3239"/>
  <text x="855" y="544" width="58" font-family="Segoe UI Symbol, Segoe UI" font-size="24" fill="#ffffff" text-anchor="middle">👍</text>

  <circle cx="968" cy="536" r="31" fill="#474c56" filter="url(#blurSoft)"/>
  <circle cx="980" cy="548" r="31" fill="#141619" filter="url(#blurSoft)"/>
  <circle cx="968" cy="536" r="29" fill="#2e3239"/>
  <text x="939" y="544" width="58" font-family="Segoe UI Symbol, Segoe UI" font-size="24" fill="#ffffff" text-anchor="middle">ϟ</text>

  <text x="310" y="706" width="720" font-family="Segoe UI Light, Segoe UI, Microsoft YaHei" font-size="50" letter-spacing="6" fill="#31d4d7">NEUMORPHIC TEMPLATE</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<animate>` for the equalizer bars; create the static bar heights in SVG and add PowerPoint Wipe/Stretch animations later if needed.
- ❌ Do not use masks for inner shadows; PPT translation is safer with layered blurred rectangles/circles and darker pressed fills.
- ❌ Do not use sharp-corner rectangles for primary controls; hard corners break the soft molded illusion.
- ❌ Do not apply filters to `<line>` elements; use filtered rectangles/paths/circles for glows and shadows instead.
- ❌ Do not overuse cyan; the accent should identify active elements, not become the whole interface.

## Composition notes
- Keep the background, cards, and controls the same charcoal family; depth should come from shadow direction, not from obvious color contrast.
- Leave generous negative space around every soft component so the blurred light and dark shadows can breathe without muddy overlap.
- Use cyan only on active states: CTA button, slider progress, equalizer bars, and headline accent.
- For a premium keynote slide, balance one large tactile card on the left with animated/data-like modules on the right, then anchor the composition with a wide low title.