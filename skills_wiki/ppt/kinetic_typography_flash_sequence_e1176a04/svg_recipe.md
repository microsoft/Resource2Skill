# SVG Recipe — Kinetic Typography Flash Sequence

## Visual mechanism
A single word or short phrase dominates the entire slide, cut hard against a high-contrast background. The “motion” is created by duplicating this SVG as separate slides, changing the word per slide, and setting each PowerPoint slide to auto-advance in milliseconds.

## SVG primitives needed
- 1× `<rect>` for the full-canvas mustard flash background
- 1× `<linearGradient>` for a very subtle premium background lift while preserving the flat poster look
- 8× `<path>` for jagged edge slashes / impact shards that imply speed without using animation
- 2× large background `<text>` elements for cropped ghost typography texture
- 1× offset `<text>` element for a tiny vibration imprint behind the main word
- 1× primary centered `<text>` element for the active flash word
- 1× small `<text>` production cue showing the frame duration; remove it for final export if a perfectly clean lyric-video frame is desired

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="mustardFlash" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#F8DF6B"/>
      <stop offset="0.52" stop-color="#F6D757"/>
      <stop offset="1" stop-color="#EFCB43"/>
    </linearGradient>
  </defs>

  <!-- Full-frame flash color -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#mustardFlash)"/>

  <!-- Cropped background typography: gives the frame kinetic density while staying editable -->
  <text x="-76" y="158" width="1500"
        font-family="Impact, Arial Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="172" font-weight="900" letter-spacing="-5"
        fill="#D7AC22" opacity="0.26">TROUBLE</text>

  <text x="448" y="694" width="1050"
        font-family="Impact, Arial Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="190" font-weight="900" letter-spacing="-7"
        fill="#D7AC22" opacity="0.22">TROUBLE.</text>

  <!-- Impact shards: static visual accents for a one-frame flash -->
  <path d="M0,0 L184,0 L122,48 L0,70 Z" fill="#101010" opacity="0.10"/>
  <path d="M1280,0 L1280,92 L1114,50 L1186,0 Z" fill="#101010" opacity="0.12"/>
  <path d="M0,720 L0,610 L154,666 L105,720 Z" fill="#101010" opacity="0.13"/>
  <path d="M1280,720 L1080,720 L1168,665 L1280,626 Z" fill="#101010" opacity="0.11"/>

  <path d="M74,250 L254,228 L232,252 L82,278 Z" fill="#101010" opacity="0.16"/>
  <path d="M1014,220 L1228,238 L1212,267 L994,249 Z" fill="#101010" opacity="0.15"/>
  <path d="M116,494 L310,468 L292,498 L98,524 Z" fill="#101010" opacity="0.13"/>
  <path d="M968,510 L1194,470 L1210,496 L986,540 Z" fill="#101010" opacity="0.14"/>

  <!-- Micro-offset imprint: suggests the previous/next frame without using animation -->
  <text x="646" y="390" width="1160" text-anchor="middle"
        font-family="Impact, Arial Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="156" font-weight="900" letter-spacing="-4"
        fill="#A7790E" opacity="0.42">TROUBLE.</text>

  <!-- Main flash word -->
  <text x="640" y="384" width="1160" text-anchor="middle"
        font-family="Impact, Arial Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="156" font-weight="900" letter-spacing="-4"
        fill="#0F0F0F">
    <tspan>TROUBLE</tspan><tspan>.</tspan>
  </text>

  <!-- Optional editor cue: delete or recolor to background before final playback -->
  <text x="1134" y="676" width="110" text-anchor="end"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" letter-spacing="1.6"
        fill="#0F0F0F" opacity="0.34">1500MS</text>
</svg>
```

## Avoid in this skill
- ❌ SVG `<animate>` or `<animateTransform>`; the effect should come from PowerPoint slide cuts, not SVG animation.
- ❌ Object-by-object PowerPoint motion paths; they reduce the hard-cut lyric-video feel.
- ❌ Gradual slide transitions such as dissolve, push, or morph unless intentionally breaking the rhythm.
- ❌ Long paragraphs or multi-line copy; this technique works best with one word or one short phrase per slide.
- ❌ Text without a `width` attribute; PowerPoint may reflow or clip it unpredictably after translation.

## Composition notes
- Keep the active word centered and enormous, usually spanning 75–95% of the slide width.
- Use one background color per sequence section; reserve color swaps or inverted frames for major beats.
- Build the sequence as many separate SVG/PPT slides: one word per slide, instant transition, auto-advance after 50–1500 ms.
- Edge shards and ghost typography should remain secondary; the viewer must read the main word instantly.