# SVG Recipe — Picture-in-Picture Video Narration Layout (Testimonial Style)

## Visual mechanism
A full-slide screen capture or report mockup becomes the primary evidence layer, while a rounded Picture-in-Picture webcam tile floats in the lower-right corner to add human narration without interrupting the data flow. The composition should feel like a polished recorded walkthrough: clean application/document UI, subtle cursor cue, and a high-contrast video card with border, shadow, name tag, and recording indicator.

## SVG primitives needed
- 1× `<rect>` for the white slide/app background
- 1× `<rect>` for the left PowerPoint-style navigation rail
- Multiple `<rect>` elements for menu highlights, template thumbnails, search bar, file rows, dividers, and the PiP frame
- Multiple `<text>` elements with explicit `width` for navigation labels, app labels, template captions, recent-file rows, and webcam name tag
- Multiple `<line>` elements for thin UI separators and row dividers
- Several `<circle>` elements for small app icons, status dots, profile/utility icons, and recording indicator
- Several `<path>` elements for simple navigation icons, cursor pointer, tiny chevrons, file icons, and decorative UI marks
- 1× `<image>` for the webcam/presenter feed, clipped to a rounded rectangle
- 1× `<clipPath>` with rounded `<rect>` applied to the webcam `<image>`
- 1× `<linearGradient>` for a subtle video-card tint overlay/background
- 1× `<filter id="softShadow">` applied to the PiP card and selected content panels
- 1× `<filter id="glow">` applied to the recording dot or video focus accent

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="pipTint" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#111827"/>
      <stop offset="100%" stop-color="#374151"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="12"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="glow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="4"/>
    </filter>
    <clipPath id="webcamClip">
      <rect x="978" y="502" width="264" height="164" rx="22" ry="22"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#f6f7f4"/>

  <!-- Left navigation rail, like a recorded PowerPoint backstage screen -->
  <rect x="0" y="0" width="108" height="720" fill="#bd3f24"/>
  <rect x="0" y="72" width="108" height="30" fill="#6f1520"/>
  <circle cx="19" cy="54" r="8" fill="none" stroke="#f9d7cb" stroke-width="1.6"/>
  <path d="M22 54 L16 54 M16 54 L19 51 M16 54 L19 57" fill="none" stroke="#f9d7cb" stroke-width="1.4"/>
  <text x="30" y="91" width="62" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#ffffff">Home</text>
  <text x="30" y="119" width="62" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#ffffff">New</text>
  <text x="30" y="149" width="62" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#ffffff">Open</text>
  <line x1="13" y1="168" x2="94" y2="168" stroke="#d7816c" stroke-width="1"/>
  <text x="30" y="190" width="62" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#ffffff">Info</text>
  <text x="30" y="220" width="62" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#ffffff">Save</text>
  <text x="30" y="250" width="62" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#ffffff">Save As</text>
  <text x="30" y="280" width="62" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#ffffff">Print</text>
  <text x="30" y="310" width="62" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#ffffff">Share</text>
  <text x="30" y="340" width="62" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#ffffff">Export</text>
  <text x="30" y="370" width="62" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#ffffff">Close</text>
  <line x1="13" y1="616" x2="94" y2="616" stroke="#d7816c" stroke-width="1"/>
  <text x="30" y="639" width="62" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#ffffff">Account</text>
  <text x="30" y="669" width="62" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#ffffff">Feedback</text>
  <text x="30" y="699" width="62" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#ffffff">Options</text>

  <!-- Main app chrome -->
  <rect x="108" y="0" width="1172" height="72" fill="#ffffff"/>
  <text x="600" y="25" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#555">Presentation3  -  PowerPoint</text>
  <text x="1045" y="24" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#333">Nigel Booth</text>
  <circle cx="1138" cy="20" r="7" fill="none" stroke="#777" stroke-width="1"/>
  <circle cx="1165" cy="20" r="7" fill="none" stroke="#777" stroke-width="1"/>
  <circle cx="1192" cy="20" r="7" fill="none" stroke="#777" stroke-width="1"/>
  <line x1="108" y1="72" x2="1280" y2="72" stroke="#deded8" stroke-width="1"/>

  <!-- Main content region -->
  <text x="140" y="61" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" fill="#252525">Good morning</text>
  <path d="M124 92 L128 97 L132 92" fill="none" stroke="#333" stroke-width="1.4"/>
  <text x="146" y="98" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#222">New</text>

  <!-- Template thumbnails -->
  <rect x="156" y="139" width="110" height="64" fill="#ffffff" stroke="#deded8"/>
  <text x="171" y="227" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#1f1f1f">Blank Presentation</text>
  <rect x="322" y="139" width="110" height="64" fill="#ffffff" stroke="#d7d7d7"/>
  <rect x="325" y="142" width="104" height="4" fill="#78b7d8"/>
  <path d="M325 190 C350 178, 375 202, 405 184 S425 186, 430 176" fill="none" stroke="#111" stroke-width="1"/>
  <text x="343" y="227" width="95" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#1f1f1f">Future Forward</text>
  <rect x="489" y="139" width="110" height="64" fill="#d74424"/>
  <text x="498" y="163" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="9" fill="#ffe7df">Welcome to PowerPoint</text>
  <text x="491" y="227" width="122" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#1f1f1f">Welcome to PowerPoint</text>
  <rect x="655" y="139" width="110" height="64" fill="#c94728"/>
  <text x="665" y="154" width="86" font-family="Segoe UI, Microsoft YaHei" font-size="7.5" fill="#ffd4c8">Bring Your Presentations to Life with 3D</text>
  <text x="659" y="227" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#1f1f1f">Bring your presentations to...</text>
  <rect x="820" y="139" width="110" height="64" fill="#1f2937"/>
  <path d="M822 166 C842 132, 872 174, 892 143 S925 176, 930 150" fill="none" stroke="#e95656" stroke-width="5"/>
  <text x="849" y="170" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="7" fill="#ffffff">TITLE LOREM IPSUM</text>
  <text x="845" y="227" width="88" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#1f1f1f">Floral flourish</text>
  <rect x="984" y="139" width="110" height="64" fill="#f9fafb" stroke="#deded8"/>
  <path d="M1002 190 L1021 171 L1036 181 L1064 147" fill="none" stroke="#2d3748" stroke-width="2"/>
  <text x="1025" y="227" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#1f1f1f">Urban monochrome</text>
  <rect x="1149" y="139" width="110" height="64" fill="#1a1615"/>
  <circle cx="1208" cy="166" r="31" fill="#5b3a32" opacity="0.55"/>
  <text x="1174" y="170" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="8" fill="#ffffff">Title Lorem Ipsum</text>
  <text x="1168" y="227" width="95" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#1f1f1f">Earthy inspiration</text>
  <line x1="140" y1="259" x2="1274" y2="259" stroke="#deded8" stroke-width="1"/>
  <text x="1198" y="280" width="72" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#bd3f24">More themes →</text>

  <!-- Search and recent files -->
  <rect x="140" y="305" width="368" height="24" fill="#ffffff" stroke="#d4d4cf"/>
  <circle cx="170" cy="315" r="4" fill="none" stroke="#b25748" stroke-width="1.2"/>
  <line x1="167" y1="319" x2="162" y2="324" stroke="#b25748" stroke-width="1.2"/>
  <text x="192" y="322" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#777">Search</text>
  <text x="140" y="359" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#333">Recent</text>
  <line x1="140" y1="364" x2="180" y2="364" stroke="#bd3f24" stroke-width="2"/>
  <text x="195" y="359" width="55" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#333">Pinned</text>
  <text x="253" y="359" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#333">Shared with Me</text>
  <line x1="140" y1="400" x2="1274" y2="400" stroke="#ddddda" stroke-width="1"/>
  <text x="180" y="392" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#777">Name</text>
  <text x="932" y="392" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#777">Date modified</text>

  <g fill="#ffffff" stroke="#ddd">
    <rect x="148" y="413" width="19" height="21" rx="2"/>
    <rect x="148" y="457" width="19" height="21" rx="2"/>
    <rect x="148" y="501" width="19" height="21" rx="2"/>
    <rect x="148" y="545" width="19" height="21" rx="2"/>
    <rect x="148" y="589" width="19" height="21" rx="2"/>
    <rect x="148" y="633" width="19" height="21" rx="2"/>
    <rect x="148" y="677" width="19" height="21" rx="2"/>
  </g>
  <g fill="#d74424">
    <rect x="151" y="418" width="9" height="9"/>
    <rect x="151" y="462" width="9" height="9"/>
    <rect x="151" y="506" width="9" height="9"/>
    <rect x="151" y="550" width="9" height="9"/>
    <rect x="151" y="594" width="9" height="9"/>
    <rect x="151" y="638" width="9" height="9"/>
    <rect x="151" y="682" width="9" height="9"/>
  </g>
  <text x="181" y="420" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#333">BUSINESS UPDATED PRESENTATION.pptx</text>
  <text x="181" y="436" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="9" fill="#777">OneDrive - Personal » Documents » Company_1 » Powerpoint » ZINZINO » Business Presentation</text>
  <text x="932" y="426" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#777">Yesterday at 15:02</text>
  <text x="181" y="464" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#333">UK ZINZINO LAUNCH JAN 21st 2020 NB v2.pptx</text>
  <text x="181" y="480" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="9" fill="#777">OneDrive - Personal » Documents » Company_1 » Powerpoint » ZINZINO</text>
  <text x="932" y="470" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#777">Mon at 10:39</text>
  <text x="181" y="508" width="460" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#333">partner training working with a new distributor no pictures.pptx</text>
  <text x="181" y="524" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="9" fill="#777">Nigel Booth's OneDrive (Personal) » Documents » Company_1 » Powerpoint » ZINZINO</text>
  <text x="932" y="514" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#777">Mon at 10:39</text>
  <text x="181" y="552" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#333">Steps of a Customer.pptx</text>
  <text x="181" y="568" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="9" fill="#777">Nigel Booth's OneDrive (Personal) » Documents » Company_1 » Powerpoint » ZINZINO</text>
  <text x="932" y="558" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#777">Sat at 10:05</text>
  <line x1="140" y1="444" x2="1274" y2="444" stroke="#e5e5e1" stroke-width="1"/>
  <line x1="140" y1="488" x2="1274" y2="488" stroke="#e5e5e1" stroke-width="1"/>
  <line x1="140" y1="532" x2="1274" y2="532" stroke="#e5e5e1" stroke-width="1"/>
  <line x1="140" y1="576" x2="1274" y2="576" stroke="#e5e5e1" stroke-width="1"/>
  <line x1="140" y1="620" x2="1274" y2="620" stroke="#e5e5e1" stroke-width="1"/>
  <line x1="140" y1="664" x2="1274" y2="664" stroke="#e5e5e1" stroke-width="1"/>

  <!-- Cursor cue from the screen recording -->
  <path d="M87 315 L100 331 L93 332 L97 343 L92 345 L88 334 L83 339 Z" fill="#2a96c7" stroke="#1e5f78" stroke-width="1"/>

  <!-- Picture-in-picture webcam overlay -->
  <rect x="970" y="494" width="280" height="180" rx="26" fill="#111827" opacity="0.28" filter="url(#softShadow)"/>
  <rect x="978" y="502" width="264" height="164" rx="22" fill="url(#pipTint)"/>
  <image x="978" y="502" width="264" height="164" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/webcam-presenter-smiling-in-home-office.jpg"
         clip-path="url(#webcamClip)"/>
  <rect x="978" y="502" width="264" height="164" rx="22" fill="none" stroke="#ffffff" stroke-width="4"/>
  <rect x="992" y="618" width="178" height="34" rx="17" fill="#111827" opacity="0.76"/>
  <circle cx="1012" cy="635" r="5" fill="#ff3b30" filter="url(#glow)"/>
  <circle cx="1012" cy="635" r="3.5" fill="#ff3b30"/>
  <text x="1024" y="640" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#ffffff">Nigel Booth · Live</text>
  <rect x="1178" y="618" width="48" height="34" rx="17" fill="#111827" opacity="0.76"/>
  <path d="M1191 637 C1198 628, 1206 628, 1213 637" fill="none" stroke="#ffffff" stroke-width="2"/>
  <circle cx="1196" cy="634" r="2" fill="#ffffff"/>
  <circle cx="1208" cy="634" r="2" fill="#ffffff"/>

  <!-- Recording progress accent -->
  <rect x="0" y="697" width="1280" height="7" fill="#0d5f26"/>
</svg>
```

## Avoid in this skill
- ❌ Do not try to embed an actual video stream or animation in SVG; represent the webcam as a clipped image/card and let PowerPoint recording handle live narration.
- ❌ Do not use `<mask>` to crop the webcam tile; use `<clipPath>` applied directly to the `<image>`.
- ❌ Do not place `clip-path` on a `<g>` or `<rect>` expecting it to crop multiple elements; PowerPoint translation only preserves clipping reliably on images.
- ❌ Do not use `marker-end` for cursor arrows or callouts; draw arrowheads/cursors as standalone `<path>` shapes.
- ❌ Do not omit `width` on any `<text>` element; the editable PPT text boxes need explicit widths.

## Composition notes
- Keep the main content nearly full-frame, as if it is a screen recording or shared document; the slide itself should not add much decorative typography.
- Anchor the PiP tile to the bottom-right with a 30–45 px margin, sized around 20–25% of slide width and 20–24% of slide height.
- Use a white stroke and soft shadow on the webcam tile so it remains legible over busy documents or application screens.
- Reserve the bottom edge for a subtle recording/progress accent if desired; avoid placing important report content under the PiP area.