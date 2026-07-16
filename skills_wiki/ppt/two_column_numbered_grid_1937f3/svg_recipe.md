# SVG Recipe — Two-Column Numbered Grid

## Visual mechanism
A premium two-column list where each item sits in a soft glass card, anchored by an oversized translucent number and a compact accent stripe. The grid reads like a structured executive checklist: bold numerical rhythm, strong alignment, and enough negative space for up to ten concise points.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background.
- 2× `<path>` for soft abstract background ribbons/blobs that add depth without distracting from the list.
- 2× `<rect>` for faint column backplates behind the grid.
- 10× `<rect>` for rounded item cards with shadow.
- 10× `<rect>` for vertical accent strips inside the cards.
- 10× `<text>` for large translucent item numbers.
- 10× `<text>` for item titles.
- 10× `<text>` for short supporting descriptions.
- 1× `<text>` for the headline.
- 1× `<text>` for the eyebrow/kicker.
- 1× `<text>` for a small section label.
- 3× `<linearGradient>` for background, card fill, and accent coloring.
- 1× `<radialGradient>` for atmospheric glow.
- 2× `<filter>` using blur/offset/merge for editable soft glow and card shadow.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#07111F"/>
      <stop offset="54%" stop-color="#0B1730"/>
      <stop offset="100%" stop-color="#111827"/>
    </linearGradient>
    <linearGradient id="cardGrad" x1="0" y1="0" x2="520" y2="90">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.13"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.055"/>
    </linearGradient>
    <linearGradient id="accentGrad" x1="0" y1="0" x2="0" y2="88">
      <stop offset="0%" stop-color="#5EEAD4"/>
      <stop offset="52%" stop-color="#38BDF8"/>
      <stop offset="100%" stop-color="#818CF8"/>
    </linearGradient>
    <radialGradient id="glowGrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#22D3EE" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#22D3EE" stop-opacity="0"/>
    </radialGradient>
    <filter id="shadow" x="-20%" y="-30%" width="140%" height="170%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="28"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <path d="M-40 610 C170 500 265 520 410 425 C548 335 664 312 780 365 C908 423 990 405 1115 300 C1195 232 1285 224 1350 250 L1350 760 L-40 760 Z" fill="#0EA5E9" opacity="0.10" filter="url(#softGlow)"/>
  <path d="M760 -70 C880 44 986 54 1110 32 C1218 12 1285 67 1328 160 L1328 -70 Z" fill="url(#glowGrad)" opacity="0.9" filter="url(#softGlow)"/>

  <text x="78" y="63" width="280" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" letter-spacing="2.2" fill="#67E8F9">OPERATING PLAN</text>
  <text x="78" y="114" width="760" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="42" font-weight="750" fill="#F8FAFC">Ten priorities, organized for action</text>
  <text x="1010" y="82" width="190" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="600" text-anchor="end" fill="#94A3B8">Two-column numbered grid</text>

  <rect x="66" y="148" width="548" height="520" rx="28" fill="#FFFFFF" opacity="0.035"/>
  <rect x="666" y="148" width="548" height="520" rx="28" fill="#FFFFFF" opacity="0.035"/>

  <rect x="86" y="170" width="520" height="88" rx="20" fill="url(#cardGrad)" stroke="#FFFFFF" stroke-opacity="0.11" filter="url(#shadow)"/>
  <rect x="86" y="188" width="5" height="52" rx="2.5" fill="url(#accentGrad)"/>
  <text x="112" y="238" width="92" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="72" font-weight="800" fill="#FFFFFF" opacity="0.16">01</text>
  <text x="205" y="205" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="19" font-weight="700" fill="#F8FAFC">Clarify the north-star outcome</text>
  <text x="205" y="232" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13.5" fill="#CBD5E1">Translate strategy into one measurable target.</text>

  <rect x="86" y="268" width="520" height="88" rx="20" fill="url(#cardGrad)" stroke="#FFFFFF" stroke-opacity="0.11" filter="url(#shadow)"/>
  <rect x="86" y="286" width="5" height="52" rx="2.5" fill="url(#accentGrad)"/>
  <text x="112" y="336" width="92" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="72" font-weight="800" fill="#FFFFFF" opacity="0.16">02</text>
  <text x="205" y="303" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="19" font-weight="700" fill="#F8FAFC">Map the decision owners</text>
  <text x="205" y="330" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13.5" fill="#CBD5E1">Name accountable leads before work begins.</text>

  <rect x="86" y="366" width="520" height="88" rx="20" fill="url(#cardGrad)" stroke="#FFFFFF" stroke-opacity="0.11" filter="url(#shadow)"/>
  <rect x="86" y="384" width="5" height="52" rx="2.5" fill="url(#accentGrad)"/>
  <text x="112" y="434" width="92" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="72" font-weight="800" fill="#FFFFFF" opacity="0.16">03</text>
  <text x="205" y="401" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="19" font-weight="700" fill="#F8FAFC">Sequence the critical path</text>
  <text x="205" y="428" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13.5" fill="#CBD5E1">Expose dependencies, gates, and release moments.</text>

  <rect x="86" y="464" width="520" height="88" rx="20" fill="url(#cardGrad)" stroke="#FFFFFF" stroke-opacity="0.11" filter="url(#shadow)"/>
  <rect x="86" y="482" width="5" height="52" rx="2.5" fill="url(#accentGrad)"/>
  <text x="112" y="532" width="92" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="72" font-weight="800" fill="#FFFFFF" opacity="0.16">04</text>
  <text x="205" y="499" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="19" font-weight="700" fill="#F8FAFC">Allocate scarce capacity</text>
  <text x="205" y="526" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13.5" fill="#CBD5E1">Protect expert time and remove low-value demand.</text>

  <rect x="86" y="562" width="520" height="88" rx="20" fill="url(#cardGrad)" stroke="#FFFFFF" stroke-opacity="0.11" filter="url(#shadow)"/>
  <rect x="86" y="580" width="5" height="52" rx="2.5" fill="url(#accentGrad)"/>
  <text x="112" y="630" width="92" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="72" font-weight="800" fill="#FFFFFF" opacity="0.16">05</text>
  <text x="205" y="597" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="19" font-weight="700" fill="#F8FAFC">Instrument the progress signals</text>
  <text x="205" y="624" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13.5" fill="#CBD5E1">Use weekly evidence, not status theater.</text>

  <rect x="686" y="170" width="520" height="88" rx="20" fill="url(#cardGrad)" stroke="#FFFFFF" stroke-opacity="0.11" filter="url(#shadow)"/>
  <rect x="686" y="188" width="5" height="52" rx="2.5" fill="url(#accentGrad)"/>
  <text x="712" y="238" width="92" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="72" font-weight="800" fill="#FFFFFF" opacity="0.16">06</text>
  <text x="805" y="205" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="19" font-weight="700" fill="#F8FAFC">Codify repeatable playbooks</text>
  <text x="805" y="232" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13.5" fill="#CBD5E1">Turn best practices into usable operating assets.</text>

  <rect x="686" y="268" width="520" height="88" rx="20" fill="url(#cardGrad)" stroke="#FFFFFF" stroke-opacity="0.11" filter="url(#shadow)"/>
  <rect x="686" y="286" width="5" height="52" rx="2.5" fill="url(#accentGrad)"/>
  <text x="712" y="336" width="92" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="72" font-weight="800" fill="#FFFFFF" opacity="0.16">07</text>
  <text x="805" y="303" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="19" font-weight="700" fill="#F8FAFC">Reduce handoff friction</text>
  <text x="805" y="330" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13.5" fill="#CBD5E1">Standardize inputs, outputs, and escalation routes.</text>

  <rect x="686" y="366" width="520" height="88" rx="20" fill="url(#cardGrad)" stroke="#FFFFFF" stroke-opacity="0.11" filter="url(#shadow)"/>
  <rect x="686" y="384" width="5" height="52" rx="2.5" fill="url(#accentGrad)"/>
  <text x="712" y="434" width="92" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="72" font-weight="800" fill="#FFFFFF" opacity="0.16">08</text>
  <text x="805" y="401" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="19" font-weight="700" fill="#F8FAFC">Run executive review cadence</text>
  <text x="805" y="428" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13.5" fill="#CBD5E1">Focus discussion on decisions and risk retirement.</text>

  <rect x="686" y="464" width="520" height="88" rx="20" fill="url(#cardGrad)" stroke="#FFFFFF" stroke-opacity="0.11" filter="url(#shadow)"/>
  <rect x="686" y="482" width="5" height="52" rx="2.5" fill="url(#accentGrad)"/>
  <text x="712" y="532" width="92" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="72" font-weight="800" fill="#FFFFFF" opacity="0.16">09</text>
  <text x="805" y="499" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="19" font-weight="700" fill="#F8FAFC">Document change decisions</text>
  <text x="805" y="526" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13.5" fill="#CBD5E1">Create a durable trail of tradeoffs and rationale.</text>

  <rect x="686" y="562" width="520" height="88" rx="20" fill="url(#cardGrad)" stroke="#FFFFFF" stroke-opacity="0.11" filter="url(#shadow)"/>
  <rect x="686" y="580" width="5" height="52" rx="2.5" fill="url(#accentGrad)"/>
  <text x="712" y="630" width="92" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="72" font-weight="800" fill="#FFFFFF" opacity="0.16">10</text>
  <text x="805" y="597" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="19" font-weight="700" fill="#F8FAFC">Close the loop with learning</text>
  <text x="805" y="624" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13.5" fill="#CBD5E1">Feed lessons into the next planning cycle.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<foreignObject>` for wrapping list text; every list label should be native `<text width="...">`.
- ❌ Do not place `filter` on a parent `<g>` expecting all cards to inherit it; apply the shadow filter directly to each card `<rect>`.
- ❌ Do not use `<use>` to repeat cards; duplicate the editable SVG primitives so each item remains editable in PowerPoint.
- ❌ Do not rely on tiny dense body copy. This layout works best with one short title line and one supporting line per item.
- ❌ Do not add arrow markers between numbers; this is a grid/checklist pattern, not a flowchart.

## Composition notes
- Keep the two columns symmetrical: five cards on the left, five on the right, with a generous center gutter of roughly 60–80 px.
- Reserve the top 140–155 px for headline and context; the numbered grid should start below it and fill the remaining slide height.
- Use oversized low-opacity numbers as rhythm, not as the main reading target; item titles should carry the informational hierarchy.
- Use one accent gradient consistently across all cards to unify the grid while the dark background and glass cards provide executive polish.