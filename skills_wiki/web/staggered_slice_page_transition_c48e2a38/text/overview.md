# Staggered Slice Page Transition

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Staggered Slice Page Transition

* **Core Visual Mechanism**: A transition effect where the screen is masked by multiple vertical "slices" (HTML list elements) that animate into view sequentially from the bottom to the top. Once the screen is fully obscured, the underlying content swaps, and the slices cascade away by shrinking towards the top. This is paired with an expanding `clip-path` reveal on hero images for a highly polished, cinematic sequence.
* **Why Use This Skill (Rationale)**: Native browser page reloads feel abrupt and break the user's immersion. Implementing a coordinated, staggered overlay creates a "Single Page Application" (SPA) feel, keeping the user engaged while content is fetched or swapped. The staggering mechanism adds a rhythmic, organic momentum compared to a flat, single-div fade.
* **Overall Applicability**: Ideal for high-end digital agency portfolios, luxury e-commerce sites, photography galleries, and SaaS landing pages where brand perception heavily relies on smooth, premium motion design. 
* **Browser Compatibility**: Excellent across all modern browsers. Relies on CSS Flexbox, standard CSS transforms (`scaleY`, `transform-origin`), and `clip-path`. The GSAP library smoothly polyfills animation timings and easing.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **The Slices**: An unordered list (`<ul class="transition">`) positioned absolutely over the container. It contains 5 empty `<li>` elements.
  - **Color Logic**: The transition slices use a bold accent color (e.g., `#00bfff` or crisp white `#ffffff` depending on the theme) to create high contrast against the content.
  - **The Content Area**: Two separate page wrappers (`.page`) that toggle `display: flex/none` under the cover of the transition slices.
  - **Image Reveals**: Hero images hidden initially using `clip-path: polygon(0 100%, 100% 100%, 100% 100%, 0 100%)`.

* **Step B: Layout & Compositional Style**
  - **Slice Layout**: The `<ul>` uses `display: flex`, and each `<li>` uses `flex: 1` to perfectly divide the container's width into equal columns without hardcoding percentages.
  - **Z-Index Layering**: Content sits at base `z-index`, while the transition list sits at a very high `z-index: 9999` with `pointer-events: none` to ensure it never traps clicks when hidden.

* **Step C: Interactive Behavior & Animations**
  - **Phase 1 (Cover)**: Slices animate `scaleY` from `0` to `1` with `transform-origin: bottom left`. GSAP's `stagger` property delays each slice by `0.1s`, creating a wave effect.
  - **Phase 2 (Swap)**: Triggered via GSAP's `.call()` when the timeline peaks. The DOM updates to show the new page.
  - **Phase 3 (Reveal)**: Slices animate `scaleY` from `1` to `0`. Crucially, `transform-origin` is swapped to `top left` so the slices pull *upwards* and away, continuing the directional momentum.
  - **Phase 4 (Image Unfurl)**: The new page's image animates its `clip-path` up to `100% 0%`, slightly overlapping with Phase 3 to make the reveal feel cohesive.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Staggered Animations** | GSAP (via CDN) | GSAP's `.timeline()` and `stagger` properties make orchestrating complex multi-element sequences trivial compared to writing dozens of native CSS `@keyframes` with manually calculated `animation-delay` offsets. |
| **Virtual Page Swap** | JavaScript DOM manipulation | The tutorial uses Barba.js, which requires fetching URLs from an active local server (violating `file://` protocol execution). To make this component 100% self-contained and reproducible offline, the SPA logic is simulated by toggling CSS classes on virtual "pages" within the same file. |
| **Slice Grid** | CSS Flexbox | `flex: 1` on the list items dynamically calculates their width, making the effect completely responsive to any container dimension. |
| **Image Reveal** | CSS `clip-path` | Performant, GPU-accelerated masking technique that animates smoothly. |

> **Feasibility Assessment**: 100% visual reproduction of the tutorial's core animation pattern. The only difference is the architectural choice to use an internal state swap instead of Barba.js XHR fetching, ensuring it works perfectly as a standalone component.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Explore our Services",
    body_text: str = "An Ongoing Experience",
    color_scheme: str = "light",        
    accent_color: str = "#111111",     
    width_px: int = 1000,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Staggered Slice Page Transition.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
        card_bg = "#1a2235"
        alt_accent = "#ffffff"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        card_bg = "#ffffff"
        alt_accent = "#000000"

    # === CSS ===
    css = f"""/* Staggered Slice Page Transition — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --card-bg: {card_bg};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #000; /* Outer background */
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

/* Component constraints */
.wrapper {{
    width: var(--width);
    height: var(--height);
    background: var(--bg);
    color: var(--text);
    position: relative;
    overflow: hidden;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    border-radius: 8px;
}}

/* Transition Slice Overlay */
.transition {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 9999;
    display: flex;
    pointer-events: none;
    list-style: none;
}}

.transition li {{
    flex: 1;
    background: var(--accent);
    transform: scaleY(0);
    transform-origin: bottom left;
    will-change: transform;
}}

/* Page Layouts */
.page {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: none; /* Hidden by default */
    padding: 40px;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
}}

.page.active {{
    display: flex; /* Only active page is shown */
}}

.content-left {{
    flex: 1;
    padding-right: 40px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}}

h1 {{
    font-size: 3.5rem;
    line-height: 1.1;
    font-weight: 700;
    margin-bottom: 16px;
    letter-spacing: -0.03em;
}}

p {{
    font-size: 1.25rem;
    opacity: 0.8;
    margin-bottom: 40px;
}}

.btn {{
    align-self: flex-start;
    padding: 16px 32px;
    background: var(--card-bg);
    color: var(--text);
    border: 2px solid var(--text);
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    text-transform: uppercase;
    letter-spacing: 1px;
}}

.btn:hover {{
    background: var(--text);
    color: var(--bg);
}}

/* Image Reveal Element */
.image-wrapper {{
    width: 45%;
    height: 80%;
    position: relative;
    border-radius: 4px;
    overflow: hidden;
}}

.hero-image {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    /* Hidden state for animation */
    clip-path: polygon(0% 100%, 100% 100%, 100% 100%, 0% 100%);
    will-change: clip-path;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
    <!-- GSAP Core -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
</head>
<body>

    <div class="wrapper">
        
        <!-- Slices Overlay -->
        <ul class="transition">
            <li></li><li></li><li></li><li></li><li></li>
        </ul>

        <!-- Virtual Page 1 -->
        <div id="home-page" class="page active">
            <div class="content-left">
                <h1>{body_text}</h1>
                <p>Welcome to our digital space. We craft seamless transitions.</p>
                <button class="btn" onclick="transitionTo('services-page')">Take me there</button>
            </div>
            <div class="image-wrapper">
                <!-- Initial image is visible without clip-path reset on first load -->
                <img class="hero-image" src="https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?auto=format&fit=crop&w=800&q=80" alt="Interior Architecture" style="clip-path: polygon(0% 0%, 100% 0%, 100% 100%, 0% 100%);">
            </div>
        </div>

        <!-- Virtual Page 2 -->
        <div id="services-page" class="page">
            <div class="content-left">
                <h1>{title_text}</h1>
                <p>Discover a new dimension of web interactivity.</p>
                <button class="btn" onclick="transitionTo('home-page')">Take me home</button>
            </div>
            <div class="image-wrapper">
                <img class="hero-image" src="https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=800&q=80" alt="Modern Living Space">
            </div>
        </div>

    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Staggered Slice Page Transition Logic
let isAnimating = false;

function transitionTo(targetPageId) {{
    // Prevent overlapping transitions
    if (isAnimating) return;
    isAnimating = true;

    // Create a GSAP Timeline
    const tl = gsap.timeline({{
        onComplete: () => {{
            isAnimating = false;
        }}
    }});

    // Phase 1: Slices slide UP to cover the screen
    tl.set('.transition li', {{ transformOrigin: "bottom left" }})
      .to('.transition li', {{
          duration: 0.5,
          scaleY: 1,
          stagger: 0.1,
          ease: "power2.inOut"
      }})
      
      // Phase 2: Swap the content while the screen is completely covered
      .call(() => {{
          // Hide all pages
          document.querySelectorAll('.page').forEach(page => {{
              page.classList.remove('active');
          }});
          
          // Show the target page
          document.getElementById(targetPageId).classList.add('active');

          // Reset the clip-path of the image on the newly active page so it can be animated in
          const newImg = document.querySelector('#' + targetPageId + ' .hero-image');
          if(newImg) {{
              gsap.set(newImg, {{ clipPath: "polygon(0% 100%, 100% 100%, 100% 100%, 0% 100%)" }});
          }}
      }})
      
      // Phase 3: Slices slide UP to reveal the new screen
      .set('.transition li', {{ transformOrigin: "top left" }})
      .to('.transition li', {{
          duration: 0.5,
          scaleY: 0,
          stagger: 0.1,
          ease: "power2.inOut",
          delay: 0.1
      }});

    // Phase 4: Secondary animations on the new page (Image Unfurl)
    const activeImg = document.querySelector('#' + targetPageId + ' .hero-image');
    if (activeImg) {{
        tl.to(activeImg, {{
            clipPath: "polygon(0% 0%, 100% 0%, 100% 100%, 0% 100%)",
            duration: 1.2,
            ease: "power3.out"
        }}, "-=0.4"); // Offset to start slightly before the slices finish leaving
    }}
}}
"""

    # === Write files ===
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

* **Accessibility**: 
  - Rapid, full-screen sweeping animations can trigger vertigo or motion sickness in susceptible users. A production implementation should include a `prefers-reduced-motion: reduce` media query that disables the slice animation and instantly toggles the `.active` state classes.
  - The `ul.transition` is marked with `pointer-events: none` and is semantically empty, but adding `aria-hidden="true"` to the `<ul>` would further ensure screen readers ignore the transition masking elements entirely.
* **Performance**: 
  - We exclusively animate `transform: scaleY()` and `clip-path`. These properties are heavily optimized by browsers and trigger compositor-only repaints, meaning the animation avoids layout thrashing and easily runs at 60fps.
  - The `will-change: transform` and `will-change: clip-path` properties are applied to proactively hint to the browser to assign GPU layers to the animated elements.