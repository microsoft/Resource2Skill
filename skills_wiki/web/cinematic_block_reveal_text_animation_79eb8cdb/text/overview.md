# Cinematic Block Reveal Text Animation

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Cinematic Block Reveal Text Animation

* **Core Visual Mechanism**: This pattern hides typography initially, revealing it progressively as the user scrolls. A solid-colored block "wipes" across each individual line of text from left to right. Once the block fully covers the line, the text underneath becomes visible, and the block immediately shrinks away to the right, leaving the revealed text in its wake. This relies heavily on manipulating CSS `transform-origin` alongside dynamic text-splitting.
* **Why Use This Skill (Rationale)**: The block reveal adds dramatic tension and a highly polished, editorial feel to typography. It forces the user to digest the text linearly (line by line) pacing the delivery of information and aligning perfectly with the momentum of their scroll. 
* **Overall Applicability**: This technique is exceptional for portfolio sites, digital magazines, agency landing pages, and dramatic hero/intro sections where you want to make a bold, cinematic statement.
* **Value Addition**: Compared to standard fade-ins or translates, a block reveal adds a physical "weight" to the animation. It introduces a secondary visual element (the colored block) that can carry the brand's accent color, drawing the eye precisely where the designer wants it.
* **Browser Compatibility**: This technique uses standard CSS transforms (`scaleX`, `transform-origin`), `opacity`, and JS Intersection Observers (via GSAP ScrollTrigger). It is fully compatible with all modern browsers (Chrome 60+, Firefox 55+, Safari 11+).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Typography**: Heavily relies on tight, bold, uppercase typography to ensure the blocks form satisfying rectangular shapes when covering the text.
  - **Color Logic**: Usually employs a stark, high-contrast palette. E.g., Dark mode uses a pitch-black background (`#0d111c`) with stark white text (`#f0f0f0`) and a vibrant, aggressive accent color for the reveal block (e.g., Blood Red `#ff0100` or Cyan `#00bfff`).
  - **CSS Properties**: The heavy lifting is done via absolute positioned overlay elements using `transform: scaleX(0)` and dynamically shifting `transform-origin` from `left center` to `right center`.

* **Step B: Layout & Compositional Style**
  - Text must be split into distinct line-level wrappers. If the text reflows, the wrappers must reflow with it.
  - Line height is kept intentionally tight (e.g., `0.9` to `1.1`) so the revealing blocks sit flush against each other, creating a dense, masonry-like feel when multiple lines animate at once.

* **Step C: Interactive Behavior & Animations**
  - **Smooth Scrolling**: Momentum-based smooth scrolling (via Lenis) is paired with the animation so that the scroll triggers feel fluid and continuous, rather than jerky native scroll steps.
  - **Staggering**: Multiple lines of text are staggered (e.g., `0.1s` to `0.15s` delay between each line) to create a cascading wipe effect rather than a monolithic block.
  - **Animation Arc**: 
    1. `scaleX(0)` to `scaleX(1)` with `transform-origin: left`.
    2. Snap text `opacity` to `1`.
    3. Snap `transform-origin` to `right`.
    4. `scaleX(1)` to `scaleX(0)`.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Text Splitting | SplitType (JS Library) | The tutorial uses GSAP's premium `SplitText`, which requires a paid license. `SplitType` is a robust, free, open-source alternative that does the exact same thing natively. |
| Scroll Triggers | GSAP + ScrollTrigger | Industry standard for highly-sequenced scroll animations. Allows precise timeline control for the complex block-in/text-show/block-out sequence. |
| Smooth Scroll | Lenis (CDN) | Reproduces the high-end, buttery-smooth scroll momentum from the tutorial, significantly improving the feel of ScrollTrigger animations. |
| DOM Manipulation | Vanilla JS | The tutorial uses Next.js/React components. To ensure this skill is universally reproducible without a Node environment, we programmatically wrap the text lines with the block overlays using Vanilla JS. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "FRAMED IN TUNGSTEN",
    body_text: str = "This is cinematography in its raw form. The camera settles into long takes and patient movement. Colors stay unrefined and shadows turn into texture.",
    color_scheme: str = "dark",
    accent_color: str = "#ff0100",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#0a0a0a"
        text_color = "#f4f4f4"
        secondary_bg = "#111111"
    else:
        bg_color = "#f4f4f4"
        text_color = "#0a0a0a"
        secondary_bg = "#e0e0e0"

    css = f"""/* Cinematic Block Reveal — generated component */
@import url('https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@400;600&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --secondary-bg: {secondary_bg};
}}

html.lenis {{
  height: auto;
}}
.lenis.lenis-smooth {{
  scroll-behavior: auto;
}}
.lenis.lenis-smooth [data-lenis-prevent] {{
  overscroll-behavior: contain;
}}
.lenis.lenis-stopped {{
  overflow: hidden;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 200vh; /* Allow scrolling */
    overflow-x: hidden;
    -webkit-font-smoothing: antialiased;
}}

/* Navigation mock */
nav {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    padding: 2rem 4rem;
    display: flex;
    justify-content: space-between;
    z-index: 100;
    mix-blend-mode: difference;
    color: #fff;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    pointer-events: none;
}}

/* Layout */
.section {{
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 4rem;
    position: relative;
}}

.section.intro {{
    align-items: center;
    text-align: center;
    background: var(--secondary-bg);
}}

.section.content {{
    align-items: flex-start;
    max-width: {width_px}px;
    margin: 0 auto;
}}

/* Typography */
.reveal-heading {{
    font-family: 'Anton', sans-serif;
    text-transform: uppercase;
    font-size: clamp(4rem, 8vw, 8rem);
    line-height: 1.05;
    letter-spacing: 0.02em;
    margin-bottom: 2rem;
    max-width: 900px;
}}

.reveal-body {{
    font-family: 'Inter', sans-serif;
    text-transform: uppercase;
    font-weight: 600;
    font-size: clamp(1.5rem, 3vw, 2.5rem);
    line-height: 1.3;
    max-width: 800px;
}}

/* Utility for the generated structure */
.line {{
    position: relative;
    display: inline-block;
    vertical-align: top;
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cinematic Block Reveal</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <nav>
        <span>Index</span>
        <span>Menu</span>
    </nav>

    <!-- First section pushes content down to demo scroll trigger -->
    <section class="section intro">
        <p style="font-family: 'Anton', sans-serif; font-size: 2rem; letter-spacing: 2px; color: var(--accent);">
            Scroll Down
        </p>
    </section>

    <!-- Content section with reveal elements -->
    <section class="section content">
        <h1 class="reveal-heading" data-block-color="var(--accent)">{title_text}</h1>
        <p class="reveal-body" data-block-color="var(--text)">{body_text}</p>
    </section>
    
    <section class="section intro">
        <p style="font-family: 'Anton', sans-serif; font-size: 2rem; letter-spacing: 2px;">
            End of Reel
        </p>
    </section>

    <!-- Dependencies -->
    <script src="https://unpkg.com/@studio-freight/lenis@1.0.42/dist/lenis.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
    <script src="https://unpkg.com/split-type"></script>
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Cinematic Block Reveal — interactive behavior

document.addEventListener('DOMContentLoaded', () => {{
    // 1. Initialize Lenis Smooth Scroll
    const lenis = new Lenis({{
        duration: 1.2,
        easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
        orientation: 'vertical',
        gestureOrientation: 'vertical',
        smoothWheel: true,
    }});

    lenis.on('scroll', ScrollTrigger.update);

    gsap.ticker.add((time) => {{
        lenis.raf(time * 1000);
    }});
    gsap.ticker.lagSmoothing(0);

    // 2. Setup Reveal Animations
    const revealElements = document.querySelectorAll('.reveal-heading, .reveal-body');

    revealElements.forEach(el => {{
        // Split text into lines
        const splitText = new SplitType(el, {{ types: 'lines' }});
        const blockColor = el.getAttribute('data-block-color') || 'var(--accent)';

        // Setup GSAP ScrollTrigger timeline for this block of text
        const tl = gsap.timeline({{
            scrollTrigger: {{
                trigger: el,
                start: "top 85%", // Trigger when top of element hits 85% of viewport height
                toggleActions: "play none none none" 
            }}
        }});

        // Process each line to create the overlay block and text span
        splitText.lines.forEach((line, index) => {{
            // Ensure line container acts as a positioning context
            line.style.position = 'relative';

            // Wrap original text in a span so we can hide/show it independently
            const originalHTML = line.innerHTML;
            line.innerHTML = ''; // Clear line

            const textSpan = document.createElement('span');
            textSpan.innerHTML = originalHTML;
            textSpan.style.opacity = '0'; // Hide initially
            textSpan.style.position = 'relative';
            textSpan.style.zIndex = '0';
            line.appendChild(textSpan);

            // Create the wiping block overlay
            const block = document.createElement('div');
            block.style.position = 'absolute';
            block.style.top = '0';
            block.style.left = '0';
            block.style.width = '100%';
            block.style.height = '100%';
            block.style.backgroundColor = blockColor;
            block.style.transformOrigin = 'left center';
            block.style.transform = 'scaleX(0)';
            block.style.zIndex = '1';
            block.style.pointerEvents = 'none';
            line.appendChild(block);

            // Calculate staggered timing
            const staggerDelay = index * 0.15;
            const animDuration = 0.45;

            // Step 1: Block scales in from the left
            tl.to(block, {{
                scaleX: 1,
                duration: animDuration,
                ease: "power3.inOut"
            }}, staggerDelay)
            
            // Step 2: Make text visible exactly when block is fully covering it
            .set(textSpan, {{
                opacity: 1
            }}, staggerDelay + animDuration)
            
            // Step 3: Shift block's transform origin to the right
            .set(block, {{
                transformOrigin: "right center"
            }}, staggerDelay + animDuration)
            
            // Step 4: Block scales out to the right, revealing text
            .to(block, {{
                scaleX: 0,
                duration: animDuration,
                ease: "power3.inOut"
            }}, staggerDelay + animDuration);
        }});
    }});
}});
"""

    files = []
    for fname, content in [("index.html", html), ("style.css", css), ("script.js", js)]:
        path = os.path.join(output_dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        files.append(path)

    return {
        "html": html,
        "css": css,
        "js": js,
        "files": files,
    }
```

### 4. Accessibility & Performance Notes

* **Accessibility**: Dynamically splitting text creates deep nesting (`div.line > div.word > div.char`) which can sometimes confuse standard screen readers, causing them to read out individual letters or words out of order. To mitigate this in a production build, add `aria-label` to the parent `.reveal-heading` containing the full unsplit string, and set `aria-hidden="true"` on the split nodes.
* **Performance**: 
  - GSAP animations utilizing `scaleX` and `opacity` are highly performant as they are offloaded to the GPU and do not trigger layout reflows or repaints.
  - Using `IntersectionObserver` internally within GSAP's ScrollTrigger avoids expensive, un-throttled native `scroll` event listeners.
  - Ensure you clear or revert the SplitType instances if your web application utilizes client-side routing (e.g., Next.js, React Router) to prevent memory leaks.