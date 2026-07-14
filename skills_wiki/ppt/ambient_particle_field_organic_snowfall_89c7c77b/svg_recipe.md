# SVG Recipe — Ambient Particle Field (Organic Snowfall)

## Visual mechanism
A layered winter landscape is covered by dozens of differently sized, differently opaque circular particles, creating depth like organic snowfall frozen mid-drift. The atmosphere comes from parallax scale variation, pink-white particle color shifts, soft glow, and a twilight gradient/vignette background.

## SVG primitives needed
- 1× `<rect>` for the full-slide twilight sky gradient
- 1× `<rect>` with radial gradient for dark vignette edge falloff
- 4× `<path>` for overlapping snow hill bands and foreground drifts
- 10× `<path>` for distant pine forest silhouettes
- 1× large organic `<path>` for the foreground bare tree trunk
- 10× stroked `<path>` for irregular tree branches
- 8× `<ellipse>` / `<path>` for snow clumps sitting on branches
- 8× `<rect>` / `<path>` for the cabin body, roof, chimney, door, and windows
- 7× `<line>` for the fence rails/posts
- 75–100× `<circle>` for snow particles in foreground, midground, and background layers
- 12× small `<ellipse>` for elongated drifting flakes
- 1× `<linearGradient>` for the sky
- 3× `<linearGradient>` for snow hill depth and cabin/roof shading
- 1× `<radialGradient>` for the vignette
- 2× `<filter>` for soft particle glow and warm window glow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="720">
      <stop offset="0" stop-color="#343044"/>
      <stop offset="0.48" stop-color="#b9afd0"/>
      <stop offset="1" stop-color="#f59be8"/>
    </linearGradient>
    <linearGradient id="hillA" x1="0" y1="410" x2="0" y2="720">
      <stop offset="0" stop-color="#ffd8ff"/>
      <stop offset="0.55" stop-color="#f8b7f4"/>
      <stop offset="1" stop-color="#c578d0"/>
    </linearGradient>
    <linearGradient id="hillB" x1="0" y1="470" x2="0" y2="720">
      <stop offset="0" stop-color="#fff3ff"/>
      <stop offset="0.65" stop-color="#eca7eb"/>
      <stop offset="1" stop-color="#9053a9"/>
    </linearGradient>
    <linearGradient id="roofGrad" x1="900" y1="330" x2="1190" y2="430">
      <stop offset="0" stop-color="#ff9a53"/>
      <stop offset="1" stop-color="#c9451f"/>
    </linearGradient>
    <radialGradient id="vignette" cx="50%" cy="48%" r="70%">
      <stop offset="0.45" stop-color="#000000" stop-opacity="0"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0.48"/>
    </radialGradient>
    <filter id="flakeGlow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="2.2"/>
    </filter>
    <filter id="windowGlow" x="-100%" y="-100%" width="300%" height="300%">
      <feGaussianBlur stdDeviation="7"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#sky)"/>

  <g opacity="0.46" fill="#315d65">
    <path d="M735 455 L765 350 L748 350 L776 302 L762 302 L790 246 L822 302 L808 302 L840 350 L823 350 L854 455 Z"/>
    <path d="M815 455 L850 330 L833 330 L866 280 L850 280 L884 218 L920 280 L903 280 L938 330 L918 330 L958 455 Z"/>
    <path d="M895 455 L930 320 L912 320 L946 270 L930 270 L965 210 L1000 270 L984 270 L1018 320 L1000 320 L1036 455 Z"/>
    <path d="M1010 455 L1048 295 L1028 295 L1065 240 L1048 240 L1085 118 L1124 240 L1106 240 L1146 295 L1123 295 L1166 455 Z"/>
    <path d="M1110 455 L1145 340 L1128 340 L1162 292 L1146 292 L1182 232 L1218 292 L1200 292 L1238 340 L1218 340 L1256 455 Z"/>
  </g>

  <path d="M0 462 C175 452 250 464 385 454 C540 443 690 477 830 458 C990 438 1112 472 1280 456 L1280 720 L0 720 Z" fill="url(#hillA)"/>
  <path d="M0 505 C150 530 260 518 400 502 C590 480 745 510 900 496 C1055 483 1145 494 1280 510 L1280 720 L0 720 Z" fill="url(#hillB)" opacity="0.92"/>
  <path d="M0 594 C210 575 340 605 500 588 C685 568 875 600 1030 583 C1135 570 1215 575 1280 590 L1280 720 L0 720 Z" fill="#ee9de8" opacity="0.46"/>
  <path d="M30 642 C200 632 332 645 485 634 C655 621 827 649 1004 632 C1115 622 1202 630 1260 640" fill="none" stroke="#f9d4ff" stroke-width="6" opacity="0.25" stroke-linecap="round"/>

  <g stroke="#707c61" stroke-width="7" stroke-linecap="round">
    <line x1="690" y1="450" x2="895" y2="450"/>
    <line x1="705" y1="422" x2="885" y2="422"/>
    <line x1="707" y1="430" x2="707" y2="482"/>
    <line x1="750" y1="428" x2="750" y2="482"/>
    <line x1="795" y1="428" x2="795" y2="482"/>
    <line x1="840" y1="428" x2="840" y2="482"/>
    <line x1="883" y1="430" x2="883" y2="482"/>
  </g>

  <g>
    <rect x="918" y="386" width="218" height="96" rx="4" fill="#9b7557"/>
    <rect x="1035" y="329" width="52" height="55" fill="#896340"/>
    <path d="M1004 321 L1030 306 L1093 322 L1086 332 L1014 333 Z" fill="#f25f1d"/>
    <path d="M892 385 C920 355 965 346 1018 352 C1070 358 1117 342 1150 355 C1185 368 1192 407 1169 432 L1134 425 C1112 398 1078 394 1040 400 C1000 408 955 402 917 416 Z" fill="url(#roofGrad)"/>
    <path d="M901 382 C924 350 947 354 960 376 C981 352 1005 356 1013 378 C1035 354 1054 359 1060 377 C1080 352 1105 353 1114 376 C1132 355 1152 360 1160 384 C1124 385 1087 386 1048 390 C997 395 949 397 901 382 Z" fill="#ffe7ff"/>
    <rect x="946" y="405" width="34" height="42" rx="2" fill="#ffbd39" filter="url(#windowGlow)" opacity="0.7"/>
    <rect x="1026" y="407" width="38" height="45" rx="2" fill="#ffbd39" filter="url(#windowGlow)" opacity="0.7"/>
    <rect x="948" y="407" width="30" height="38" rx="1" fill="#ffc43f" stroke="#37513d" stroke-width="4"/>
    <rect x="1028" y="409" width="34" height="41" rx="1" fill="#ffc43f" stroke="#37513d" stroke-width="4"/>
    <line x1="963" y1="407" x2="963" y2="445" stroke="#37513d" stroke-width="3"/>
    <line x1="1045" y1="409" x2="1045" y2="450" stroke="#37513d" stroke-width="3"/>
    <rect x="1091" y="405" width="36" height="76" fill="#425d38"/>
  </g>

  <g fill="none" stroke="#004a10" stroke-linecap="round">
    <path d="M180 638 C195 590 208 548 224 501 C250 432 270 395 257 343 C248 303 248 261 269 224" stroke-width="40" fill="#004a10"/>
    <path d="M255 450 C202 422 168 405 104 401 C72 400 56 367 28 365" stroke-width="5"/>
    <path d="M260 425 C316 382 338 347 355 289 C363 257 363 226 359 196" stroke-width="8"/>
    <path d="M279 391 C328 380 357 361 382 328 C402 302 405 276 421 258" stroke-width="7"/>
    <path d="M296 468 C360 465 418 480 475 445 C512 423 527 395 574 385" stroke-width="8"/>
    <path d="M305 516 C360 546 420 557 494 541 C532 533 552 512 588 509" stroke-width="7"/>
    <path d="M227 373 C199 335 184 302 188 263 C191 237 182 218 195 196" stroke-width="7"/>
    <path d="M309 360 C301 321 314 295 336 270 C358 245 360 222 371 203" stroke-width="6"/>
    <path d="M238 527 C214 550 208 575 213 604" stroke-width="6"/>
    <path d="M342 435 C384 413 414 401 458 402 C499 403 524 386 553 362" stroke-width="6"/>
  </g>

  <g fill="#ffe8ff" opacity="0.95">
    <ellipse cx="198" cy="354" rx="18" ry="7" transform="rotate(8 198 354)"/>
    <ellipse cx="258" cy="330" rx="19" ry="8" transform="rotate(-12 258 330)"/>
    <ellipse cx="313" cy="323" rx="18" ry="7" transform="rotate(22 313 323)"/>
    <ellipse cx="365" cy="266" rx="18" ry="8" transform="rotate(-15 365 266)"/>
    <ellipse cx="417" cy="322" rx="22" ry="8" transform="rotate(-22 417 322)"/>
    <ellipse cx="482" cy="388" rx="20" ry="7" transform="rotate(-8 482 388)"/>
    <ellipse cx="343" cy="402" rx="24" ry="8" transform="rotate(18 343 402)"/>
    <ellipse cx="284" cy="488" rx="21" ry="8" transform="rotate(-10 284 488)"/>
  </g>

  <g fill="#ffffff" filter="url(#flakeGlow)">
    <circle cx="110" cy="45" r="2" opacity="0.22"/><circle cx="190" cy="44" r="7" opacity="0.35"/><circle cx="255" cy="168" r="7" opacity="0.74"/><circle cx="331" cy="104" r="7" opacity="0.55"/>
    <circle cx="374" cy="75" r="7" opacity="0.62"/><circle cx="503" cy="45" r="7" opacity="0.72"/><circle cx="594" cy="75" r="8" opacity="0.85"/><circle cx="673" cy="134" r="8" opacity="0.8"/>
    <circle cx="754" cy="105" r="8" opacity="0.88"/><circle cx="865" cy="45" r="7" opacity="0.6"/><circle cx="945" cy="166" r="8" opacity="0.78"/><circle cx="1037" cy="76" r="7" opacity="0.54"/>
    <circle cx="1119" cy="209" r="7" opacity="0.78"/><circle cx="1194" cy="277" r="7" opacity="0.78"/><circle cx="117" cy="206" r="7" opacity="0.68"/><circle cx="223" cy="236" r="8" opacity="0.9"/>
    <circle cx="363" cy="264" r="8" opacity="0.92"/><circle cx="511" cy="176" r="8" opacity="0.9"/><circle cx="592" cy="287" r="7" opacity="0.82"/><circle cx="693" cy="206" r="8" opacity="0.92"/>
    <circle cx="815" cy="278" r="7" opacity="0.8"/><circle cx="931" cy="319" r="7" opacity="0.78"/><circle cx="1018" cy="493" r="7" opacity="0.6"/><circle cx="1140" cy="454" r="7" opacity="0.8"/>
    <circle cx="73" cy="366" r="2" opacity="0.3"/><circle cx="151" cy="422" r="3" opacity="0.4"/><circle cx="450" cy="629" r="7" opacity="0.33"/><circle cx="641" cy="586" r="7" opacity="0.42"/>
    <circle cx="813" cy="518" r="7" opacity="0.48"/><circle cx="1004" cy="666" r="7" opacity="0.28"/><circle cx="1124" cy="606" r="6" opacity="0.25"/><circle cx="663" cy="707" r="7" opacity="0.55"/>
  </g>

  <g fill="#ff8dff">
    <circle cx="78" cy="18" r="2" opacity="0.35"/><circle cx="222" cy="15" r="3" opacity="0.35"/><circle cx="373" cy="9" r="4" opacity="0.36"/><circle cx="715" cy="45" r="7" opacity="0.72"/>
    <circle cx="895" cy="14" r="7" opacity="0.5"/><circle cx="1057" cy="6" r="7" opacity="0.42"/><circle cx="1132" cy="196" r="7" opacity="0.85"/><circle cx="1173" cy="302" r="7" opacity="0.75"/>
    <circle cx="139" cy="207" r="7" opacity="0.72"/><circle cx="301" cy="107" r="7" opacity="0.62"/><circle cx="589" cy="4" r="2" opacity="0.34"/><circle cx="748" cy="696" r="7" opacity="0.44"/>
    <circle cx="977" cy="3" r="7" opacity="0.44"/><circle cx="1234" cy="44" r="7" opacity="0.36"/><circle cx="421" cy="696" r="7" opacity="0.38"/><circle cx="584" cy="711" r="7" opacity="0.43"/>
  </g>

  <g fill="#ffffff" opacity="0.42">
    <ellipse cx="433" cy="92" rx="6" ry="1.4" transform="rotate(-15 433 92)"/>
    <ellipse cx="523" cy="125" rx="5" ry="1.2" transform="rotate(10 523 125)"/>
    <ellipse cx="632" cy="158" rx="6" ry="1.4" transform="rotate(-20 632 158)"/>
    <ellipse cx="752" cy="61" rx="5" ry="1.1" transform="rotate(18 752 61)"/>
    <ellipse cx="894" cy="91" rx="7" ry="1.4" transform="rotate(-18 894 91)"/>
    <ellipse cx="1044" cy="171" rx="6" ry="1.4" transform="rotate(18 1044 171)"/>
    <ellipse cx="199" cy="87" rx="5" ry="1.1" transform="rotate(-12 199 87)"/>
    <ellipse cx="277" cy="296" rx="7" ry="1.5" transform="rotate(15 277 296)"/>
    <ellipse cx="365" cy="371" rx="5" ry="1.2" transform="rotate(-20 365 371)"/>
    <ellipse cx="714" cy="480" rx="9" ry="1.8" transform="rotate(4 714 480)"/>
    <ellipse cx="778" cy="16" rx="4" ry="1" transform="rotate(-18 778 16)"/>
    <ellipse cx="1190" cy="92" rx="5" ry="1.2" transform="rotate(14 1190 92)"/>
  </g>

  <rect x="0" y="0" width="1280" height="720" fill="url(#vignette)"/>
</svg>
```

## Avoid in this skill
- ❌ SVG `<animate>` or `<animateTransform>` for falling snow; PPT-Master will hard-fail them. Keep SVG as the designed snowfall state, then apply PowerPoint motion effects separately if needed.
- ❌ `<use>` for repeating particles or trees; duplicate the actual `<circle>` / `<path>` elements instead.
- ❌ `<filter>` on `<line>` fence pieces; shadows/glows on lines are dropped, so use filtered rectangles/paths if glow is required.
- ❌ `clip-path` on the hills, tree, or particles; clipping only translates reliably for `<image>` elements.
- ❌ A mathematically perfect grid of particles; organic snowfall needs irregular spacing, varied opacity, varied radius, and mixed white/pink tones.

## Composition notes
- Keep the particle field across the entire slide, including foreground hills and sky, so the snow feels like it occupies the viewer’s space rather than sitting behind objects.
- Use three depth layers: tiny faint specks for distant atmosphere, medium white flakes for the main field, and larger glowing pink/white circles for foreground parallax.
- Reserve the lower 30–40% for landscape silhouettes and snow hills; the upper 60% should remain atmospheric and uncluttered.
- Add a vignette last to make the center glow and to push edge particles into a cinematic, premium keynote look.