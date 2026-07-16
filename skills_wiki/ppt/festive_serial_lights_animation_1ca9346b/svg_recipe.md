# SVG Recipe — Festive Serial Lights Animation

## Visual mechanism
Frame the slide with two loose, wavy strings of festive bulbs: each bulb is a crisp white circle layered over a larger colored radial glow, creating the illusion of serial lights blinking in staggered phases. The center remains dark and spacious so celebratory script typography becomes the hero.

## SVG primitives needed
- 1× `<rect>` for the dark navy/charcoal full-slide background
- 2× `<path>` for organic draped light wires across the top and bottom
- 36× `<circle>` for large colored glow halos behind bulbs
- 36× `<circle>` for small white bulb cores
- 4× `<radialGradient>` for red, green, blue, and gold light blooms
- 1× `<filter id="softBloom">` with `feGaussianBlur` applied to glow circles
- 1× `<filter id="textLift">` with offset blur shadow applied to central text
- 3× `<text>` elements with explicit `width` attributes for headline, subtitle, and small footer
- Optional `<tspan>` inside text for varied emphasis if the message needs inline styling

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="720">
      <stop offset="0%" stop-color="#202329"/>
      <stop offset="55%" stop-color="#17191f"/>
      <stop offset="100%" stop-color="#202329"/>
    </linearGradient>

    <radialGradient id="glowRed" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ff3c32" stop-opacity="0.92"/>
      <stop offset="32%" stop-color="#ff3c32" stop-opacity="0.42"/>
      <stop offset="100%" stop-color="#ff3c32" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glowGreen" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#5cff95" stop-opacity="0.90"/>
      <stop offset="34%" stop-color="#36e977" stop-opacity="0.40"/>
      <stop offset="100%" stop-color="#36e977" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glowBlue" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#4cc8ff" stop-opacity="0.88"/>
      <stop offset="35%" stop-color="#2ca8ff" stop-opacity="0.38"/>
      <stop offset="100%" stop-color="#2ca8ff" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glowGold" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#fff04a" stop-opacity="0.95"/>
      <stop offset="35%" stop-color="#ffd21f" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="#ffd21f" stop-opacity="0"/>
    </radialGradient>

    <filter id="softBloom" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="7"/>
    </filter>
    <filter id="textLift" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="4" result="off"/>
      <feGaussianBlur in="off" stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <path d="M -30 112 C 70 178, 175 184, 280 145 S 480 72, 610 130 S 815 191, 940 86 S 1130 33, 1310 116"
        fill="none" stroke="#d8d8d8" stroke-width="2.2" stroke-linecap="round" opacity="0.82"/>
  <path d="M -35 596 C 105 676, 220 676, 340 618 S 510 560, 650 636 S 845 678, 975 570 S 1145 516, 1310 606"
        fill="none" stroke="#d8d8d8" stroke-width="2.2" stroke-linecap="round" opacity="0.82"/>

  <g filter="url(#softBloom)">
    <circle cx="96" cy="141" r="42" fill="url(#glowGold)" opacity="0.92"/>
    <circle cx="126" cy="186" r="36" fill="url(#glowGreen)" opacity="0.78"/>
    <circle cx="185" cy="162" r="39" fill="url(#glowBlue)" opacity="0.86"/>
    <circle cx="239" cy="185" r="37" fill="url(#glowGreen)" opacity="0.72"/>
    <circle cx="276" cy="149" r="35" fill="url(#glowBlue)" opacity="0.80"/>
    <circle cx="327" cy="163" r="34" fill="url(#glowRed)" opacity="0.42"/>
    <circle cx="357" cy="123" r="39" fill="url(#glowBlue)" opacity="0.86"/>
    <circle cx="402" cy="142" r="34" fill="url(#glowGreen)" opacity="0.70"/>
    <circle cx="442" cy="103" r="36" fill="url(#glowRed)" opacity="0.55"/>
    <circle cx="477" cy="125" r="41" fill="url(#glowGold)" opacity="0.92"/>
    <circle cx="514" cy="103" r="36" fill="url(#glowGreen)" opacity="0.78"/>
    <circle cx="548" cy="132" r="39" fill="url(#glowGold)" opacity="0.86"/>
    <circle cx="607" cy="121" r="40" fill="url(#glowBlue)" opacity="0.80"/>
    <circle cx="646" cy="158" r="34" fill="url(#glowGreen)" opacity="0.70"/>
    <circle cx="699" cy="152" r="40" fill="url(#glowGold)" opacity="0.90"/>
    <circle cx="735" cy="181" r="37" fill="url(#glowBlue)" opacity="0.74"/>
    <circle cx="777" cy="156" r="36" fill="url(#glowGreen)" opacity="0.76"/>
    <circle cx="822" cy="168" r="34" fill="url(#glowRed)" opacity="0.45"/>
    <circle cx="846" cy="132" r="38" fill="url(#glowBlue)" opacity="0.82"/>
    <circle cx="887" cy="140" r="38" fill="url(#glowGold)" opacity="0.90"/>
    <circle cx="906" cy="100" r="36" fill="url(#glowGreen)" opacity="0.78"/>
    <circle cx="944" cy="103" r="37" fill="url(#glowBlue)" opacity="0.78"/>
    <circle cx="972" cy="58" r="41" fill="url(#glowGreen)" opacity="0.88"/>
    <circle cx="1012" cy="70" r="38" fill="url(#glowBlue)" opacity="0.82"/>
    <circle cx="1044" cy="41" r="40" fill="url(#glowBlue)" opacity="0.78"/>
    <circle cx="1078" cy="65" r="38" fill="url(#glowGreen)" opacity="0.76"/>
    <circle cx="1124" cy="52" r="42" fill="url(#glowGold)" opacity="0.96"/>
    <circle cx="1156" cy="80" r="36" fill="url(#glowRed)" opacity="0.48"/>
    <circle cx="1206" cy="72" r="41" fill="url(#glowGold)" opacity="0.94"/>
    <circle cx="1232" cy="106" r="38" fill="url(#glowGreen)" opacity="0.78"/>

    <circle cx="100" cy="624" r="42" fill="url(#glowRed)" opacity="0.90"/>
    <circle cx="128" cy="670" r="36" fill="url(#glowGreen)" opacity="0.76"/>
    <circle cx="189" cy="646" r="37" fill="url(#glowRed)" opacity="0.82"/>
    <circle cx="244" cy="672" r="38" fill="url(#glowGold)" opacity="0.92"/>
    <circle cx="282" cy="631" r="36" fill="url(#glowBlue)" opacity="0.78"/>
    <circle cx="330" cy="648" r="34" fill="url(#glowRed)" opacity="0.76"/>
    <circle cx="362" cy="607" r="36" fill="url(#glowGreen)" opacity="0.74"/>
    <circle cx="407" cy="620" r="38" fill="url(#glowGold)" opacity="0.88"/>
    <circle cx="445" cy="585" r="42" fill="url(#glowRed)" opacity="0.96"/>
    <circle cx="481" cy="607" r="34" fill="url(#glowGreen)" opacity="0.72"/>
    <circle cx="516" cy="585" r="38" fill="url(#glowBlue)" opacity="0.82"/>
    <circle cx="551" cy="616" r="36" fill="url(#glowRed)" opacity="0.80"/>
    <circle cx="612" cy="604" r="37" fill="url(#glowGreen)" opacity="0.72"/>
    <circle cx="650" cy="641" r="39" fill="url(#glowBlue)" opacity="0.78"/>
    <circle cx="703" cy="633" r="40" fill="url(#glowRed)" opacity="0.84"/>
    <circle cx="738" cy="664" r="41" fill="url(#glowGold)" opacity="0.92"/>
    <circle cx="780" cy="640" r="36" fill="url(#glowBlue)" opacity="0.74"/>
    <circle cx="823" cy="656" r="39" fill="url(#glowGold)" opacity="0.86"/>
    <circle cx="850" cy="619" r="38" fill="url(#glowGold)" opacity="0.82"/>
    <circle cx="889" cy="622" r="36" fill="url(#glowRed)" opacity="0.84"/>
    <circle cx="909" cy="584" r="36" fill="url(#glowGreen)" opacity="0.76"/>
    <circle cx="947" cy="587" r="40" fill="url(#glowGold)" opacity="0.90"/>
    <circle cx="976" cy="541" r="39" fill="url(#glowGreen)" opacity="0.78"/>
    <circle cx="1017" cy="554" r="37" fill="url(#glowBlue)" opacity="0.78"/>
    <circle cx="1048" cy="524" r="42" fill="url(#glowRed)" opacity="0.96"/>
    <circle cx="1085" cy="550" r="38" fill="url(#glowGreen)" opacity="0.74"/>
    <circle cx="1128" cy="535" r="40" fill="url(#glowGold)" opacity="0.92"/>
    <circle cx="1160" cy="564" r="36" fill="url(#glowGreen)" opacity="0.74"/>
    <circle cx="1211" cy="555" r="39" fill="url(#glowBlue)" opacity="0.78"/>
    <circle cx="1236" cy="588" r="39" fill="url(#glowRed)" opacity="0.88"/>
  </g>

  <g fill="#ffffff">
    <circle cx="96" cy="141" r="11"/><circle cx="126" cy="186" r="11"/><circle cx="185" cy="162" r="11"/><circle cx="239" cy="185" r="11"/><circle cx="276" cy="149" r="11"/>
    <circle cx="327" cy="163" r="10"/><circle cx="357" cy="123" r="11"/><circle cx="402" cy="142" r="10"/><circle cx="442" cy="103" r="11"/><circle cx="477" cy="125" r="11"/>
    <circle cx="514" cy="103" r="10"/><circle cx="548" cy="132" r="11"/><circle cx="607" cy="121" r="11"/><circle cx="646" cy="158" r="10"/><circle cx="699" cy="152" r="11"/>
    <circle cx="735" cy="181" r="10"/><circle cx="777" cy="156" r="10"/><circle cx="822" cy="168" r="10"/><circle cx="846" cy="132" r="10"/><circle cx="887" cy="140" r="10"/>
    <circle cx="906" cy="100" r="10"/><circle cx="944" cy="103" r="10"/><circle cx="972" cy="58" r="11"/><circle cx="1012" cy="70" r="11"/><circle cx="1044" cy="41" r="11"/>
    <circle cx="1078" cy="65" r="11"/><circle cx="1124" cy="52" r="11"/><circle cx="1156" cy="80" r="10"/><circle cx="1206" cy="72" r="11"/><circle cx="1232" cy="106" r="11"/>

    <circle cx="100" cy="624" r="11"/><circle cx="128" cy="670" r="11"/><circle cx="189" cy="646" r="11"/><circle cx="244" cy="672" r="11"/><circle cx="282" cy="631" r="10"/>
    <circle cx="330" cy="648" r="10"/><circle cx="362" cy="607" r="10"/><circle cx="407" cy="620" r="10"/><circle cx="445" cy="585" r="11"/><circle cx="481" cy="607" r="10"/>
    <circle cx="516" cy="585" r="10"/><circle cx="551" cy="616" r="10"/><circle cx="612" cy="604" r="10"/><circle cx="650" cy="641" r="11"/><circle cx="703" cy="633" r="11"/>
    <circle cx="738" cy="664" r="11"/><circle cx="780" cy="640" r="10"/><circle cx="823" cy="656" r="10"/><circle cx="850" cy="619" r="10"/><circle cx="889" cy="622" r="10"/>
    <circle cx="909" cy="584" r="10"/><circle cx="947" cy="587" r="10"/><circle cx="976" cy="541" r="11"/><circle cx="1017" cy="554" r="10"/><circle cx="1048" cy="524" r="11"/>
    <circle cx="1085" cy="550" r="10"/><circle cx="1128" cy="535" r="11"/><circle cx="1160" cy="564" r="10"/><circle cx="1211" cy="555" r="10"/><circle cx="1236" cy="588" r="11"/>
  </g>

  <text x="640" y="316" width="1000" text-anchor="middle"
        font-family="Segoe Script, Brush Script MT, Segoe UI, Microsoft YaHei" font-size="106"
        font-weight="600" fill="#ffffff" filter="url(#textLift)">Season’s Greetings</text>
  <text x="640" y="432" width="980" text-anchor="middle"
        font-family="Segoe Script, Brush Script MT, Segoe UI, Microsoft YaHei" font-size="82"
        font-weight="600" fill="#ffffff" filter="url(#textLift)">from the whole team</text>
  <text x="1035" y="694" width="390" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="26" fill="#ffffff" opacity="0.86">Milestone Celebration 2026</text>
</svg>
```

## Avoid in this skill
- ❌ SVG `<animate>` or `<animateTransform>` for blinking; these hard-fail translation. Use staggered glow sizes/opacities in SVG, then add native PowerPoint pulse animations after import if motion is required.
- ❌ `<use href="#bulb">` to duplicate bulbs; it is not supported. Duplicate the actual `<circle>` elements instead.
- ❌ Applying `filter` to a `<line>` for glowing wires; filters on lines are dropped. Use filtered circles for the glow and a simple stroked `<path>` for the wire.
- ❌ `marker-end` arrowheads or inherited markers; this is a decorative lighting border, not a connector diagram.
- ❌ Masks or clipping on glow shapes; clip-path is only reliable on `<image>` elements.

## Composition notes
- Keep the top string in the upper 0–190 px band and the bottom string in the lower 520–690 px band, leaving a clean central stage for text.
- The wire should feel slack and organic: use long cubic Bézier waves, not straight segments or perfect sine precision.
- Alternate red, green, blue, and gold glows irregularly; vary radius and opacity to imply different blink phases in a static SVG.
- Use a very dark background and white bulb cores so the colored halos read as luminous rather than flat decoration.