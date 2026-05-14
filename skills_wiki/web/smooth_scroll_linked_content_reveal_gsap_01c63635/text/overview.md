# Smooth Scroll-Linked Content Reveal (GSAP + Lenis)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Smooth Scroll-Linked Content Reveal (GSAP + Lenis)

*   **Core Visual Mechanism**: The defining characteristic of this technique is tying the physical position or state of DOM elements (like translation, opacity, or scale) directly to the user's scroll progress, augmented by a smooth-scrolling wrapper. Specifically, it uses a "scrubbing" mechanic where an off-screen card smoothly slides into the center of the viewport exactly as the user scrolls through a specific vertical zone (e.g., from the moment the element's container hits the center of the screen until its bottom hits the center).
*   **Why Use This Skill (Rationale)**: Native browser scrolling can feel disjointed or "chunky," making scroll-triggered animations feel abrupt. By combining a smooth scroll interpolation library (Lenis) with a robust animation timeline (GSAP ScrollTrigger), the website creates a tactile, premium feel. Users feel as though they are physically pulling the content into view via their scroll wheel or trackpad, which increases engagement and time-on-site.
*   **Overall Applicability**: Ideal for storytelling landing pages, product feature showcases (where hardware or UI elements slide into view as text appears), portfolio case studies, and editorial articles where pacing the delivery of information is crucial.
*   **Value Addition**: Compared to standard CSS `:hover` states or simple Intersection Observers that just play a one-off animation, this pattern creates a two-way relationship between user input (scrolling) and UI output. The user can scrub back and forth, reversing the animation naturally.
*   **Browser Compatibility**: Broadly compatible with modern browsers. GSAP and Lenis handle cross-browser calculation discrepancies. Requires `requestAnimationFrame` and `IntersectionObserver` support (available in all modern browsers: Chrome 51+, Safari 12.1+, Firefox 55+, Edge 55+).

### 2. Visual & Technical Breakdown

*   **Step A: Core Visual Elements**
    *   **Animated Target**: A primary content card.
    *   **Color Logic**:
        *   Background: Needs deep contrast to make the card pop. (e.g., `#0d111c`).
        *   Card Surface: A slightly elevated surface color, often frosted or solid with a subtle border/shadow (e.g., `rgba(255,255,255,0.06)`).
        *   Accent: High-visibility brand color applied to the card border or a decorative element (e.g., `#00bfff`).
    *   **Typography**: Clean, sans-serif hierarchy (e.g., 'Inter') to keep the focus on the motion.
    *   **CSS Properties driving the effect**: `transform: translateX()`, `opacity`, and hardware-accelerated rendering (`will-change: transform`). *Note: While the tutorial used `left: -400px`, using `transform` is significantly better for performance and frame rates.*

*   **Step B: Layout & Compositional Style**
    *   **Layout System**: Flexbox for centering within sections.
    *   **Scroll Spacing**: The pattern relies on vertical whitespace (`100vh` sections) to give the user enough scroll track to actually perform the animation.
    *   **Visual Anchors**: A background pattern (like a subtle grid or dots) is highly recommended when using smooth scroll, as it gives the human eye a frame of reference to perceive the smoothness of the scroll velocity.

*   **Step C: Interactive Behavior & Animations**
    *   **Smooth Scrolling**: Lenis hijack's the native scroll events, applying a dampening mathematical function (linear interpolation) to create a buttery glide, passing these smoothed values to the window scroll.
    *   **GSAP ScrollTrigger**:
        *   `trigger`: The DOM element that acts as the starting line.
        *   `start: "top center"`: Animation begins when the **top** of the trigger element hits the **center** of the viewport.
        *   `end: "bottom center"`: Animation ends when the **bottom** of the trigger hits the **center** of the viewport.
        *   `scrub: true`: Links the animation playhead to the scrollbar, allowing forward and reverse playback bound exactly to scroll pixels.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
| :--- | :--- | :--- |
| **Scroll Velocity Smoothing** | Lenis CDN | Provides a lightweight, highly performant smooth scroll without locking the native scrollbar, which is crucial for accessibility. |
| **Scroll-linked Animation** | GSAP + ScrollTrigger CDN | The industry standard for complex scroll timelines. Handles the complex math of viewport intersections and scrubbed easing perfectly. |
| **Element Movement** | CSS `transform: translateX` | Modifying `transform` avoids triggering browser layout recalculations (reflows), ensuring the animation runs at a smooth 60/120fps. |
| **Visual Framing** | CSS Background Gradient/Grid | Allows the user to actually *see* the smooth scroll effect, which is lost on a blank solid background. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Discover The Details",
    body_text: str = "This card's position is physically bound to your scroll position. Scroll up and down to scrub the timeline.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#8a2be2",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the GSAP ScrollTrigger + Lenis smooth scroll reveal.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os
    import html

    os.makedirs(output_dir, exist_ok=True)
    
    safe_title = html.escape(title_text)
    safe_body = html.escape(body_text)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#0f1016"
        grid_color = "rgba(255, 255, 255, 0.05)"
        text_color = "#f0f0f0"
        text_muted = "#a0a0b0"
        surface_color = "rgba(255, 255, 255, 0.03)"
        border_color = "rgba(255, 255, 255, 0.1)"
        shadow = "0 20px 40px rgba(0,0,0,0.4)"
    else:
        bg_color = "#f4f6f8"
        grid_color = "rgba(0, 0, 0, 0.05)"
        text_color = "#111111"
        text_muted = "#555566"
        surface_color = "#ffffff"
        border_color = "rgba(0, 0, 0, 0.1)"
        shadow = "0 20px 40px rgba(0,0,0,0.08)"

    # === CSS ===
    css = f"""/* Smooth Scroll-Linked Content Reveal — generated component */
:root {{
    --bg: {bg_color};
    --grid: {grid_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --surface: {surface_color};
    --border: {border_color};
    --shadow: {shadow};
    --max-width: {width_px}px;
}}

/* Lenis recommended base styles */
html.lenis {{ height: auto; }}
.lenis.lenis-smooth {{ scroll-behavior: auto !important; }}
.lenis.lenis-smooth [data-lenis-prevent] {{ overscroll-behavior: contain; }}
.lenis.lenis-stopped {{ overflow: hidden; }}
.lenis.lenis-scrolling iframe {{ pointer-events: none; }}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    /* Subtle grid to make smooth scrolling visually apparent */
    background-image: 
        linear-gradient(to right, var(--grid) 1px, transparent 1px),
        linear-gradient(to bottom, var(--grid) 1px, transparent 1px);
    background-size: 40px 40px;
    overflow-x: hidden;
}}

.spacer {{
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    text-align: center;
    padding: 2rem;
}}

.spacer-text {{
    font-size: 1rem;
    color: var(--text-muted);
    letter-spacing: 2px;
    text-transform: uppercase;
    animation: pulse 2s infinite;
}}

@keyframes pulse {{
    0%, 100% {{ opacity: 0.5; transform: translateY(0); }}
    50% {{ opacity: 1; transform: translateY(5px); }}
}}

.trigger-section {{
    height: 150vh; /* Extra height to allow a long scroll track for the animation */
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    border-top: 1px dashed var(--border);
    border-bottom: 1px dashed var(--border);
    background: radial-gradient(circle at center, var(--surface) 0%, transparent 70%);
}}

.animated-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 4px solid var(--accent);
    padding: 3rem;
    border-radius: 12px;
    width: 90%;
    max-width: 450px;
    box-shadow: var(--shadow);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    
    /* Performance optimization */
    will-change: transform, opacity;
    
    /* Initial state (hidden and pushed left) */
    opacity: 0;
    transform: translateX(-150px);
}}

.card-title {{
    font-size: 1.75rem;
    font-weight: 700;
    margin-bottom: 1rem;
    line-height: 1.2;
}}

.card-title span {{
    color: var(--accent);
}}

.card-body {{
    font-size: 1rem;
    line-height: 1.6;
    color: var(--text-muted);
}}
"""

    # === HTML ===
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scroll-Linked Animation</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <section class="spacer">
        <h2 style="font-size: 3rem; margin-bottom: 1rem;">Keep Scrolling</h2>
        <div class="spacer-text">↓ Scroll Down ↓</div>
    </section>

    <!-- The trigger section dictates the start and end of the timeline -->
    <section class="trigger-section">
        
        <!-- The element that actually animates -->
        <div class="animated-card">
            <h3 class="card-title"><span>#</span> {safe_title}</h3>
            <p class="card-body">{safe_body}</p>
        </div>

    </section>

    <section class="spacer">
        <h2 style="font-size: 2rem;">End of Timeline</h2>
        <div class="spacer-text" style="margin-top: 1rem; animation: none;">Scroll back up to reverse</div>
    </section>

    <!-- Lenis Smooth Scroll -->
    <script src="https://cdn.jsdelivr.net/gh/studio-freight/lenis@1.0.29/bundled/lenis.min.js"></script>
    
    <!-- GSAP Core & ScrollTrigger -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""document.addEventListener('DOMContentLoaded', () => {{
    
    // 1. Initialize Lenis for Smooth Scrolling
    const lenis = new Lenis({{
        duration: 1.2, // smoothness modifier
        easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)), 
        direction: 'vertical', 
        gestureDirection: 'vertical',
        smooth: true,
        mouseMultiplier: 1,
        smoothTouch: false,
        touchMultiplier: 2,
    }});

    // Tie Lenis rAF to GSAP ticker so they stay perfectly in sync
    lenis.on('scroll', ScrollTrigger.update);

    gsap.ticker.add((time) => {{
        lenis.raf(time * 1000);
    }});
    gsap.ticker.lagSmoothing(0);

    // 2. Register GSAP ScrollTrigger
    gsap.registerPlugin(ScrollTrigger);

    // 3. Create the Scroll Animation
    // We animate from the CSS default (-150px, opacity 0) TO (0px, opacity 1)
    gsap.to('.animated-card', {{
        x: 0,
        opacity: 1,
        ease: "none", // Avoid adding ease to scrubbed animations for 1:1 scroll feel
        scrollTrigger: {{
            trigger: '.trigger-section',
            
            // "top center" -> Start animation when the TOP of the trigger-section hits the CENTER of viewport
            start: 'top center',
            
            // "bottom center" -> End animation when the BOTTOM of the trigger-section hits the CENTER of viewport
            end: 'bottom center',
            
            // Link animation progress directly to scrollbar (scrubbing)
            scrub: true,
            
            // Uncomment to see the visual markers debugging tools
            // markers: true 
        }}
    }});
}});
"""

    # === Write files ===
    files = []
    for fname, content in [("index.html", html_content), ("style.css", css), ("script.js", js)]:
        path = os.path.join(output_dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        files.append(path)

    return {
        "html": html_content,
        "css": css,
        "js": js,
        "files": files,
    }
```

#### 3c. Verification Checklist

*   [x] Does the code produce valid HTML5 that passes basic validation?
*   [x] Does `index.html` work when opened directly in a browser (`file://` protocol)?
*   [x] Are all color values explicit hex or rgba (not referencing undefined CSS variables from external systems)?
*   [x] Are all external resources loaded from CDN URLs (not local `node_modules` paths)?
*   [x] Does the component respect the parameters?
*   [x] Does `color_scheme="dark"` produce a dark theme and `"light"` a light theme?
*   [x] Does `accent_color` propagate to all accent elements (buttons, highlights, borders)?
*   [x] Are `title_text` and `body_text` properly escaped for HTML (no XSS from special characters)?
*   [x] Does the JavaScript run without console errors?
*   [x] Does it produce a visually recognizable reproduction of the tutorial's effect?

### 4. Accessibility & Performance Notes

*   **Accessibility (a11y)**: 
    *   *Motion Sensitivity*: Scroll-linked animations can trigger vestibular disorders. In a production environment, you should wrap the GSAP execution in a `window.matchMedia('(prefers-reduced-motion: no-preference)').matches` check. If the user prefers reduced motion, set the card to `opacity: 1; transform: none;` via CSS and do not initialize ScrollTrigger.
    *   *Scroll Hijacking*: Lenis is technically a "scroll hijacker," but unlike older libraries, it utilizes native scrolling APIs and doesn't trap the user, making it much more accessible.
*   **Performance**:
    *   We animate `transform` (specifically `translateX`) and `opacity`. Animating properties like `left`, `margin`, or `padding` forces the browser to recalculate the layout on every single pixel of scroll, which causes severe frame drops (jank).
    *   `will-change: transform, opacity` gives the browser a hint to push this element to the GPU layer before the scroll begins.
    *   Tying the `Lenis.raf` to `gsap.ticker` ensures that the visual DOM updates happen in the exact same render frame, eliminating stuttering between the scroll library and the animation library.