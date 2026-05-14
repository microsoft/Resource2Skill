# Scroll-Triggered Clip-Path Reveal & Image Zoom

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Scroll-Triggered Clip-Path Reveal & Image Zoom

* **Core Visual Mechanism**: This pattern relies on synchronizing a directional wipe-in effect (using CSS `clip-path: inset()`) with a subtle scale-down transition on images. As elements enter the viewport, text elements slide their visibility open from one side, while image containers wipe open to reveal an image that is simultaneously zooming out to its natural scale. 
* **Why Use This Skill (Rationale)**: This technique transforms a standard static grid into an editorial, storytelling experience. The directional wipe guides the user's eye across the content, establishing a reading rhythm. The image zoom adds a subtle parallax-like depth, making the content feel dynamic rather than flat. Re-hiding elements when they leave the viewport encourages users to scroll back and forth to re-experience the motion.
* **Overall Applicability**: Perfect for editorial layouts, portfolio showcases, product feature grids, and high-end landing pages (like coffee roasters, fashion brands, or architectural firms). It works best in checkerboard (alternating) grid layouts.
* **Value Addition**: It elevates basic HTML structure into a modern, cinematic experience using purely native CSS and a lightweight Intersection Observer, avoiding the need for heavy animation libraries.
* **Browser Compatibility**: Fully supported in all modern browsers. `clip-path`, `transform`, and `IntersectionObserver` are universally supported across current versions of Chrome, Safari, Firefox, and Edge.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **HTML Structure**: Semantic alternating blocks of `.image-box` (containing an `img`) and `.content-box` (containing headings and text). Specific target elements receive a `data-reveal="left"` or `data-reveal="right"` attribute.
  - **Typography**: Clean, geometric sans-serif (like Inter) with strong contrast between heading sizes (`4em`) and body text, utilizing generous line height (`2.25`) for readability.
  - **CSS Properties**: The heavy lifting is done by `clip-path: inset()`, `transform: scale()`, and `animation` with custom `cubic-bezier` timing functions.

* **Step B: Layout & Compositional Style**
  - **Layout System**: A simple CSS Grid (`grid-template-columns: 1fr 1fr`).
  - **Flow**: A "checkerboard" pattern achieved by manually ordering the HTML elements (Image/Text, then Text/Image).
  - **Dimensions**: Image boxes are fixed to a substantial height (e.g., `800px` or `80vh`) with `overflow: hidden`, acting as massive atmospheric windows. Content boxes use deep horizontal padding (`padding-inline: 5em`) to create elegant whitespace.

* **Step C: Interactive Behavior & Animations**
  - **Trigger Mechanism**: JavaScript monitors scroll position. When an element enters the viewport, a `.revealed` class is appended.
  - **The Wipe (Clip-Path)**: Elements start with `clip-path: inset(0 100% 0 0)` (fully clipped/hidden on the right). The `.revealed` class triggers a keyframe animation that animates the inset to `0 0 0 0` (fully visible) over `1.2s` with a `300ms` delay.
  - **The Zoom**: Images start at `scale(1.5)`. When the parent `.image-box` gets the `.revealed` class, the image transitions to `scale(1)` over `1.2s`. The easing `cubic-bezier(0.17, 0.97, 0.38, 1)` provides a snappy start that smoothly decelerates.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Directional Wipe In** | CSS `clip-path: inset()` + `@keyframes` | Provides crisp, performant directional masking without requiring wrapper divs or extra absolute layers. |
| **Image Depth Effect** | CSS `transform: scale()` + `overflow: hidden` | Hardware-accelerated, buttery smooth zooming that stays constrained within the parent box. |
| **Checkerboard Grid** | CSS Grid (`1fr 1fr`) | Native, robust way to enforce the 2-column layout. |
| **Scroll Detection** | JS `IntersectionObserver` | Replaces the tutorial's inefficient scroll event listener. IntersectionObserver is the modern, performant standard for triggering animations on scroll. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Artisan Roasts",
    body_text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Id laborum iste doloremque ab facere unde alias sit commodi accusamus. Eius ut molestiae nemo perspiciatis, pariatur numquam accusamus voluptatem libero sint.",
    color_scheme: str = "dark",
    accent_color: str = "#d4a373",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Scroll-Triggered Clip-Path Reveal & Image Zoom effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_gradient = "linear-gradient(178deg, #3e2723, #1b110f)"
        text_color = "#f5f5f5"
        heading_color = "#ffffff"
    else:
        bg_gradient = "linear-gradient(178deg, #f5f0e6, #e3d5c8)"
        text_color = "#4a3b32"
        heading_color = "#2d201c"

    # Images for the grid layout
    img1 = "https://images.unsplash.com/photo-1497935586351-b67a49e012bf?auto=format&fit=crop&w=1200&q=80"
    img2 = "https://images.unsplash.com/photo-1511920170033-f8396924c348?auto=format&fit=crop&w=1200&q=80"

    css = f"""/* Scroll-Triggered Clip-Path Reveal & Image Zoom */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: {bg_gradient};
    color: {text_color};
    overflow-x: hidden;
    /* Added min-height to allow scrolling to see the effect */
    min-height: 200vh; 
}}

/* Spacer to push content down so scroll is required */
.scroll-prompt {{
    height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    opacity: 0.7;
}}

.section {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    align-items: center;
    max-width: {width_px}px;
    margin: 0 auto;
}}

/* --- Image Boxes --- */
.image-box {{
    height: {height_px}px;
    overflow: hidden;
    position: relative;
}}

.image-box img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    transform: scale(1.5);
    /* Transition scale when revealed. Adding 300ms delay to sync with clip-path animation delay */
    transition: transform 1.2s cubic-bezier(0.17, 0.97, 0.38, 1) 0.3s;
}}

.image-box.revealed img {{
    transform: scale(1);
}}

/* --- Content Boxes --- */
.content-box {{
    padding-inline: 4em;
}}

.title {{
    font-size: 4em;
    color: {heading_color};
    margin-bottom: 0.25em;
    line-height: 1.1;
}}

.text {{
    font-size: 1.1em;
    line-height: 1.8;
    opacity: 0.85;
}}

/* --- Reveal Animation Mechanics --- */

/* Initial hidden states using clip-path inset */
[data-reveal="left"] {{
    clip-path: inset(0 100% 0 0);
}}

[data-reveal="right"] {{
    clip-path: inset(0 0 0 100%);
}}

/* The animation application */
[data-reveal="left"].revealed {{
    animation: reveal-left 1.2s cubic-bezier(0.17, 0.97, 0.38, 1) forwards 300ms;
}}

[data-reveal="right"].revealed {{
    animation: reveal-right 1.2s cubic-bezier(0.17, 0.97, 0.38, 1) forwards 300ms;
}}

/* Keyframes for sliding open the clip-path */
@keyframes reveal-left {{
    0% {{ clip-path: inset(0 100% 0 0); }}
    100% {{ clip-path: inset(0 0 0 0); }}
}}

@keyframes reveal-right {{
    0% {{ clip-path: inset(0 0 0 100%); }}
    100% {{ clip-path: inset(0 0 0 0); }}
}}

/* Responsive adjustments */
@media (max-width: 900px) {{
    .section {{
        grid-template-columns: 1fr;
    }}
    .image-box {{
        height: 50vh;
    }}
    .content-box {{
        padding: 3em 2em;
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    
    <div class="scroll-prompt">
        <p>Scroll Down</p>
        <p>↓</p>
    </div>

    <!-- Main Grid Section -->
    <section class="section">
        
        <!-- Row 1: Image Left, Text Right -->
        <div class="image-box" data-reveal="left">
            <img src="{img1}" alt="Coffee Beans">
        </div>
        <div class="content-box">
            <h2 class="title" data-reveal="right">{title_text}</h2>
            <p class="text" data-reveal="right">{body_text}</p>
        </div>

        <!-- Row 2: Text Left, Image Right (Checkerboard) -->
        <div class="content-box">
            <h2 class="title" data-reveal="left">Rich Aroma</h2>
            <p class="text" data-reveal="left">{body_text}</p>
        </div>
        <div class="image-box" data-reveal="right">
            <img src="{img2}" alt="Coffee Cup">
        </div>

    </section>
    
    <div class="scroll-prompt">
        <p>Scroll Up to re-trigger</p>
        <p>↑</p>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Scroll-Triggered Clip-Path Reveal Logic
document.addEventListener('DOMContentLoaded', () => {{
    
    // Select all elements that have a data-reveal attribute
    const revealElements = document.querySelectorAll('[data-reveal]');

    // Set up the Intersection Observer
    const observerOptions = {{
        root: null, // use the viewport
        rootMargin: '0px',
        threshold: 0.15 // trigger when 15% of the element is visible
    }};

    const revealCallback = (entries, observer) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                // Element has scrolled into view
                entry.target.classList.add('revealed');
            }} else {{
                // Element has scrolled out of view - remove class to allow re-animation
                // Remove this else block if you only want the animation to play once
                entry.target.classList.remove('revealed');
            }}
        }});
    }};

    const observer = new IntersectionObserver(revealCallback, observerOptions);

    // Observe each element
    revealElements.forEach(el => observer.observe(el));
}});
"""

    # Write files
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
  - `clip-path` animations can trigger motion sickness for sensitive users. In a production environment, you should wrap the `.revealed` animation assignments inside a `@media (prefers-reduced-motion: no-preference)` query. If motion is reduced, simply default `clip-path` to `inset(0)` globally.
  - The alternating DOM order (Image, Text, Text, Image) means screen readers will read the content in that exact order. Ensure the visual flow matches the logical narrative flow.
* **Performance**: 
  - The tutorial utilized a `scroll` event listener coupled with `getBoundingClientRect()`. This causes layout thrashing and is bad for scroll performance. The reproduction code rectifies this by using the `IntersectionObserver` API, which offloads viewport calculations to the browser's background threads, resulting in jank-free 60fps scrolling.
  - Both `clip-path` and `transform: scale()` are highly optimized CSS properties that trigger GPU hardware acceleration, avoiding expensive repaints during the animation lifecycle.