# SVG Recipe — Interactive "Click-to-Reveal" Scenario/Quiz Board

## Visual mechanism
A high-contrast quiz board uses oversized instructional headline text, glossy circular choice buttons, and visually paired reveal cards that are initially hidden in PowerPoint and triggered by clicking each button. The slide feels like a YouTube-style interactive prompt: bold typography, saturated blue glow background, red answer buttons, a large cursor cue, and answer outcomes staged as editable reveal objects.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark blue gradient background
- 2× `<radialGradient>` for the vivid blue spotlight and glossy red button shine
- 1× `<linearGradient>` for metallic button rims
- 2× `<filter>` for soft shadows and button glow
- 1× `<clipPath>` for an optional right-side presenter/photo crop with the face excluded or covered
- 1× `<image>` for an optional cropped presenter/participant photo on the right edge
- 1× `<rect>` overlay panel to exclude/cover the face area if a presenter image is used
- 6× `<text>` blocks for the title, subtitle, large keyword, prompt, and option labels
- 3× button assemblies made from `<circle>` + `<text>` for clickable triggers
- 3× reveal card assemblies made from `<rect>`, `<circle>`, and `<text>` for correct/incorrect feedback
- 1× `<path>` cursor pointer to visually suggest “click here”
- Several decorative `<circle>` / `<path>` accents for game-show polish and depth

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgGlow" cx="48%" cy="42%" r="72%">
      <stop offset="0%" stop-color="#18a7e8"/>
      <stop offset="48%" stop-color="#057fc2"/>
      <stop offset="100%" stop-color="#063b74"/>
    </radialGradient>

    <radialGradient id="buttonRed" cx="35%" cy="24%" r="75%">
      <stop offset="0%" stop-color="#ff5a4d"/>
      <stop offset="45%" stop-color="#e00000"/>
      <stop offset="100%" stop-color="#850000"/>
    </radialGradient>

    <linearGradient id="metalRim" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="28%" stop-color="#bfc5cc"/>
      <stop offset="54%" stop-color="#2b2f34"/>
      <stop offset="78%" stop-color="#f7f7f7"/>
      <stop offset="100%" stop-color="#6b7280"/>
    </linearGradient>

    <linearGradient id="whitePanel" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#edf6ff"/>
    </linearGradient>

    <filter id="deepShadow" x="-30%" y="-30%" width="160%" height="170%">
      <feOffset dx="8" dy="10"/>
      <feGaussianBlur stdDeviation="7"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="buttonGlow" x="-55%" y="-55%" width="210%" height="210%">
      <feGaussianBlur stdDeviation="9" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="rightPortraitCrop">
      <rect x="890" y="0" width="390" height="720" rx="0"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGlow)"/>
  <circle cx="190" cy="632" r="98" fill="#ff7a45" opacity="0.85"/>
  <path d="M190 534 A98 98 0 0 1 288 632 L190 632 Z" fill="#ffb088" opacity="0.8"/>
  <path d="M190 632 L288 632 A98 98 0 0 1 190 730 Z" fill="#d93618" opacity="0.7"/>

  <image id="Optional_Right_Presenter_Crop_No_Face"
         href="https://images.example.com/cropped-presenter-shoulders-hair-no-face.png"
         x="850" y="-10" width="455" height="760"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#rightPortraitCrop)"
         opacity="0.78"/>
  <rect x="970" y="105" width="250" height="380" fill="#1e293b" opacity="0.94"/>

  <text id="Title_How_To" x="120" y="154" width="710"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="118" font-weight="900" letter-spacing="18"
        fill="#ffffff" filter="url(#deepShadow)">HOW TO</text>

  <text id="Title_Make_Things" x="132" y="258" width="700"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="76" font-weight="900" letter-spacing="12"
        fill="#ffffff" filter="url(#deepShadow)">MAKE THINGS</text>

  <rect id="Keyword_Panel" x="115" y="278" width="715" height="160" fill="#ffffff" filter="url(#deepShadow)"/>
  <text id="Keyword_Appear" x="145" y="419" width="650"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="132" font-weight="900" letter-spacing="10"
        fill="#006ca9">APPEAR</text>

  <text id="Scenario_Prompt" x="392" y="612" width="390"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="76" font-weight="900"
        fill="#d64a2a" text-anchor="middle" filter="url(#deepShadow)">???</text>
  <circle cx="470" cy="672" r="110" fill="#ffffff" opacity="0.96" filter="url(#deepShadow)"/>

  <g id="Trigger_A_Click_Target">
    <circle cx="280" cy="514" r="59" fill="#ffffff" opacity="0.92" filter="url(#buttonGlow)"/>
    <circle cx="280" cy="514" r="53" fill="url(#metalRim)"/>
    <circle cx="280" cy="514" r="43" fill="url(#buttonRed)" stroke="#720000" stroke-width="3"/>
    <text x="280" y="531" width="80"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="64" font-weight="900"
          fill="#ffffff" text-anchor="middle">A</text>
  </g>

  <g id="Trigger_B_Click_Target">
    <circle cx="482" cy="514" r="59" fill="#ffffff" opacity="0.92" filter="url(#buttonGlow)"/>
    <circle cx="482" cy="514" r="53" fill="url(#metalRim)"/>
    <circle cx="482" cy="514" r="43" fill="url(#buttonRed)" stroke="#720000" stroke-width="3"/>
    <text x="482" y="531" width="80"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="64" font-weight="900"
          fill="#ffffff" text-anchor="middle">B</text>
  </g>

  <g id="Trigger_C_Click_Target">
    <circle cx="676" cy="514" r="59" fill="#ffffff" opacity="0.92" filter="url(#buttonGlow)"/>
    <circle cx="676" cy="514" r="53" fill="url(#metalRim)"/>
    <circle cx="676" cy="514" r="43" fill="url(#buttonRed)" stroke="#720000" stroke-width="3"/>
    <text x="676" y="531" width="80"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="64" font-weight="900"
          fill="#ffffff" text-anchor="middle">C</text>
  </g>

  <path id="Cursor_Click_Cue"
        d="M520 506 L594 580 L560 584 L580 630 L552 642 L532 595 L508 620 Z"
        fill="#ffffff" stroke="#0f172a" stroke-width="5" filter="url(#deepShadow)"/>

  <g id="Reveal_A_Incorrect" opacity="0.18">
    <rect x="130" y="594" width="260" height="86" rx="22" fill="url(#whitePanel)" filter="url(#deepShadow)"/>
    <circle cx="176" cy="637" r="27" fill="#ef4444"/>
    <text x="176" y="649" width="50" font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="34" font-weight="900" fill="#ffffff" text-anchor="middle">✕</text>
    <text x="218" y="645" width="160" font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="24" font-weight="700" fill="#0f172a">Not quite</text>
  </g>

  <g id="Reveal_B_Correct" opacity="0.18">
    <rect x="425" y="594" width="275" height="86" rx="22" fill="url(#whitePanel)" filter="url(#deepShadow)"/>
    <circle cx="471" cy="637" r="27" fill="#22c55e"/>
    <text x="471" y="649" width="50" font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="34" font-weight="900" fill="#ffffff" text-anchor="middle">✓</text>
    <text x="513" y="645" width="170" font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="24" font-weight="800" fill="#0f172a">Correct: 260</text>
  </g>

  <g id="Reveal_C_Incorrect" opacity="0.18">
    <rect x="730" y="594" width="280" height="86" rx="22" fill="url(#whitePanel)" filter="url(#deepShadow)"/>
    <circle cx="776" cy="637" r="27" fill="#ef4444"/>
    <text x="776" y="649" width="50" font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="34" font-weight="900" fill="#ffffff" text-anchor="middle">✕</text>
    <text x="818" y="645" width="170" font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="24" font-weight="700" fill="#0f172a">Try again</text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Do not rely on SVG animation; PowerPoint click-to-reveal behavior should be added with PPT “Appear” animations triggered by the named button shapes.
- ❌ Do not use `<use>` to duplicate the answer buttons; duplicate the actual circles/text so each trigger is separately editable and selectable.
- ❌ Do not put `clip-path` on groups or shapes; use it only on the optional presenter `<image>`.
- ❌ Do not use `marker-end` for cursor arrows or callouts; draw the cursor/callout as editable paths.
- ❌ Do not make reveal states only by raster image; keep reveal cards as editable text, circles, and rounded rectangles.

## Composition notes
- Keep the top-left 65% of the slide for oversized headline typography; it should feel like a dramatic prompt, not a form.
- Place clickable answer buttons in a horizontal row beneath the headline, with generous spacing so each can be selected easily in PowerPoint.
- Put reveal cards close to their corresponding buttons and name them clearly, e.g. `Reveal_B_Correct`, so manual trigger setup is fast.
- Use a strong blue background, white headline, and red glossy buttons for a game-show rhythm; reserve green only for the correct reveal.