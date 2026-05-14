# Cinematic Shutter Page Transition

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Cinematic Shutter Page Transition

* **Core Visual Mechanism**: A simulated, seamless page transition using a CSS flexbox grid and GSAP timelines. When a user navigates, an overlay composed of two rows of blocks closes like a mechanical shutter (scaling vertically from opposite ends). The new content is loaded seamlessly behind the scenes, and then the shutter pulls back to reveal it.
* **Why Use This Skill (Rationale)**: Native browser reloads introduce a harsh, uncontrollable white flash between pages. This technique intercepts the navigation event to construct a continuous, fluid narrative. It bridges the gap between disconnected web pages and app-like single-page applications, significantly elevating perceived site quality.
* **Overall Applicability**: Ideal for highly visual contexts such as creative agency sites, high-end portfolios, premium e-commerce experiences, and SaaS product tours where maintaining a polished aesthetic during state changes is critical. 
* **Value Addition**: Transforms a passive loading delay into an engaging, branded motion experience. 
* **Browser Compatibility**: Fully compatible with modern browsers. Relies on standard CSS Flexbox and `transform-origin` scaling, wrapped in GSAP (GreenSock) for reliable easing and staggered animation.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **HTML Structure**: A full-screen `.transition-container` containing two `.transition-row` divs. Each row holds five empty `.block` elements.
  - **Color Logic**: Minimalist high-contrast. The shutter blocks typically use the inverse of the background color or a bold accent color (e.g., `#ffffff` shutters against a `#111111` background).
  - **Typography**: Employs heavily contrasted fonts—a brutalist, massive geometric sans-serif (Inter) for the page titles, and a technical monospace (IBM Plex Mono) for navigation to give a raw, wireframe aesthetic.
  
* **Step B: Layout & Compositional Style**
  - The shutter overlay is pinned using absolute positioning (`top: 0; left: 0; width: 100%; height: 100%; z-index: 1000`).
  - Flexbox is used to auto-distribute the blocks: `.transition-row` gets `flex: 1` (taking exactly 50% of the height), and each `.block` gets `flex: 1` (taking exactly 20% of the width).
  - **CSS Transforms**: The magic happens via `transform-origin`. Top row blocks are bound to the `top`, bottom row blocks to the `bottom`.

* **Step C: Interactive Behavior & Animations**
  - **Entrance (Reveal)**: Top and bottom blocks scale their Y-axis from `1` down to `0`. The animation staggers outward from the `center` blocks to the edges.
  - **Exit (Animate)**: Top blocks scale from `0` to `1` staggered from the `end` (right to left). Bottom blocks scale from `0` to `1` staggered from the `start` (left to right). This creates a striking diagonal crossing motion.
  - **Timing**: Animations utilize GSAP's `expo.inOut` over `1s` duration with `0.1s` staggers.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Shutter Layout | CSS Flexbox | Naturally handles percentage-based grid subdivision without math |
| Transition States | CSS `transform: scaleY()` | GPU-accelerated property; avoids expensive layout reflows |
| Animation Sequencing | JS + GSAP CDN | Provides advanced staggering (`from: "center"`), precise `expo.inOut` easing, and promise-based timelines impossible with raw CSS |
| Single-Page Simulation | Vanilla JS Event Listeners | Prevents default link navigation and coordinates the DOM text updates to simulate loading a new page |

> **Feasibility Assessment**: 100% reproduction. Since this must be a self-contained component, actual HTTP page navigation is intercepted and mocked by dynamically updating the DOM content between the shutter closing and opening. The visual timing and CSS/GSAP logic identically match the tutorial.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "HOME",
    body_text: str = "Click the navigation links to trigger the transition.",
    color_scheme: str = "dark",
    accent_color: str = "#ffffff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Cinematic Shutter Page Transition.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#111111"
        text_color = "#f4f4f5"
        shutter_color = accent_color if accent_color != "#ffffff" else "#f4f4f5"
    else:
        bg_color = "#f4f4f5"
        text_color = "#111111"
        shutter_color = accent_color if accent_color != "#ffffff" else "#111111"

    css = f"""/* Cinematic Shutter Transition */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --shutter: {shutter_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: #000;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.app-container {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    position: relative;
    overflow: hidden;
    background-color: var(--bg);
    color: var(--text);
    box-shadow: 0 20px 40px rgba(0,0,0,0.4);
}}

/* Navigation */
.nav {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    padding: 2.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 10;
}}

.logo {{
    color: var(--text);
    text-decoration: none;
    font-weight: 800;
    font-size: 1.25rem;
    letter-spacing: 0.05em;
}}

.nav-items {{
    display: flex;
    gap: 3rem;
}}

.nav-items a {{
    color: var(--text);
    text-decoration: none;
    font-family: 'IBM Plex Mono', monospace;
    text-transform: uppercase;
    font-size: 0.9rem;
    font-weight: 500;
    transition: opacity 0.2s;
}}

.nav-items a:hover {{
    opacity: 0.6;
}}

/* Content */
.content {{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    text-align: center;
}}

.title {{
    font-size: clamp(5rem, 12vw, 12rem);
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: -0.03em;
    line-height: 1;
}}

.body-text {{
    margin-top: 1.5rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1rem;
    opacity: 0.6;
}}

/* Transition Shutter Overlay */
.transition-container {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    z-index: 1000;
    pointer-events: none; /* Let clicks pass through when idle */
}}

.transition-row {{
    flex: 1;
    display: flex;
}}

.block {{
    flex: 1;
    background-color: var(--shutter);
    will-change: transform;
}}

/* Origin controls the scale direction */
.row-1 .block {{
    transform-origin: top;
}}

.row-2 .block {{
    transform-origin: bottom;
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cinematic Transition</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500&family=Inter:wght@400;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
    <!-- GSAP Core -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
</head>
<body>
    <div class="app-container">
        <nav class="nav">
            <a href="#" class="logo">LOGO</a>
            <div class="nav-items">
                <a href="#home">Home</a>
                <a href="#about">About</a>
                <a href="#contact">Contact</a>
            </div>
        </nav>
        
        <main class="content">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </main>

        <div class="transition-container">
            <div class="transition-row row-1">
                <div class="block"></div>
                <div class="block"></div>
                <div class="block"></div>
                <div class="block"></div>
                <div class="block"></div>
            </div>
            <div class="transition-row row-2">
                <div class="block"></div>
                <div class="block"></div>
                <div class="block"></div>
                <div class="block"></div>
                <div class="block"></div>
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Cinematic Shutter Page Transition Logic
document.addEventListener("DOMContentLoaded", () => {
    // Initial State: Shutters fully covering the screen
    gsap.set(".block", { scaleY: 1, visibility: "visible" });
    
    // Simulate initial page load reveal
    revealTransition();

    /**
     * Plays the opening animation (Shutters scaling away)
     */
    function revealTransition() {
        return new Promise(resolve => {
            const tl = gsap.timeline({ 
                onComplete: () => {
                    // Hide completely after animating to ensure no click-blocking artifacts
                    gsap.set(".block", { visibility: "hidden" });
                    resolve();
                }
            });
            
            // Top row collapses upward
            tl.to(".row-1 .block", {
                scaleY: 0,
                duration: 1,
                stagger: { each: 0.1, from: "center" },
                ease: "expo.inOut"
            }, 0)
            // Bottom row collapses downward
            .to(".row-2 .block", {
                scaleY: 0,
                duration: 1,
                stagger: { each: 0.1, from: "center" },
                ease: "expo.inOut"
            }, 0);
        });
    }

    /**
     * Plays the closing animation (Shutters covering the screen)
     */
    function animateTransition() {
        return new Promise(resolve => {
            gsap.set(".block", { visibility: "visible", scaleY: 0 });
            const tl = gsap.timeline({ onComplete: resolve });
            
            // Top row drops down, right to left
            tl.to(".row-1 .block", {
                scaleY: 1,
                duration: 1,
                stagger: { each: 0.1, from: "end" },
                ease: "expo.inOut"
            }, 0)
            // Bottom row grows up, left to right
            .to(".row-2 .block", {
                scaleY: 1,
                duration: 1,
                stagger: { each: 0.1, from: "start" },
                ease: "expo.inOut"
            }, 0);
        });
    }

    // Mockup Routing Logic
    let isAnimating = false;
    const links = document.querySelectorAll(".nav-items a");
    const title = document.querySelector(".title");

    links.forEach(link => {
        link.addEventListener("click", async (e) => {
            e.preventDefault();
            
            // Prevent multiple rapid clicks
            if (isAnimating) return;
            
            const targetText = e.target.textContent;
            
            // Do nothing if we are already on that "page"
            if (title.textContent.toUpperCase() === targetText.toUpperCase()) return;

            isAnimating = true;

            // 1. Play closing shutters
            await animateTransition();
            
            // 2. Load "New Page" content (Mocked via DOM manipulation)
            title.textContent = targetText.toUpperCase();
            
            // 3. Play opening shutters
            await revealTransition();
            
            isAnimating = false;
        });
    });
});
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

* **Accessibility (a11y)**: While impressive, these kinds of sweeping full-screen motions can cause nausea for users with vestibular disorders. In a production environment, wrap the GSAP trigger in a `window.matchMedia('(prefers-reduced-motion: reduce)')` check. If matched, instantly resolve the promises rather than playing the animations, falling back to instant swaps.
* **Performance**: The effect is highly performant. Utilizing `scaleY()` leverages GPU acceleration, bypassing expensive layout calculations (reflows). The `.block` elements utilize the `will-change: transform` property to further guarantee browser-level optimization. Setting `visibility: hidden` once completed ensures screen readers and pointer events are completely unobstructed when the screen is idle.