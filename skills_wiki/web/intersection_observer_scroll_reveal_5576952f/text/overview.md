# Intersection Observer Scroll Reveal

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Intersection Observer Scroll Reveal

* **Core Visual Mechanism**: Elements on the page are initially hidden (transparent and slightly translated downwards). As the user scrolls and these elements enter the browser's viewport, a JavaScript `IntersectionObserver` detects their presence and appends a CSS class. This class triggers a CSS `@keyframes` animation (or transition) that smoothly fades the element in and translates it back to its natural resting position.
* **Why Use This Skill (Rationale)**: This pattern prevents the user from being overwhelmed by a massive wall of content upon initial load. By animating elements into view just as they are needed, it creates a sense of narrative flow, rewards the user's scroll interaction, and makes the webpage feel modern, dynamic, and responsive to user input.
* **Overall Applicability**: Perfect for landing pages, portfolio galleries, product feature lists, and long-form articles. It is widely used for "features grids" where individual cards pop into place as you scroll down.
* **Value Addition**: Transforms a static HTML document into an interactive experience. It directs user attention to newly revealed content and provides a polished, professional aesthetic with minimal performance overhead.
* **Browser Compatibility**: The `IntersectionObserver` API is fully supported in all modern browsers (Chrome 51+, Firefox 55+, Safari 12.1+, Edge 15+). For older browsers, a polyfill would be required, or the elements should simply default to visible.

---

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **HTML Structure**: Standard semantic blocks (e.g., `<section>`, `<article>`, or `<div>` cards). They require a specific class (like `.scroll-reveal`) to be targeted by JavaScript.
  - **Color Logic**: Flexible, but works best when the revealing elements (cards/images) have a defined background surface or border that contrasts with the page background. (e.g., Dark background `#0d111c` with frosted surface cards `rgba(255, 255, 255, 0.06)`).
  - **CSS Properties**: The heavy lifting is done by `opacity`, `transform: translateY()`, and `animation`.

* **Step B: Layout & Compositional Style**
  - **Layout System**: Independent of the structural layout (works with Grid, Flexbox, or block flow). However, vertical spacing (margins/padding) is crucial to ensure elements actually reside *below* the fold on initial load, necessitating a scroll action.
  - **Z-index**: Standard stacking order; elements don't typically overlap during this specific entrance animation.

* **Step C: Interactive Behavior & Animations**
  - **Initial State**: Elements are styled with `opacity: 0` to hide them before they enter the viewport.
  - **JavaScript Logic**: An `IntersectionObserver` is instantiated with a callback that filters for `isIntersecting`. When true, it adds a `.scrolled` class and `unobserves` the element so the animation only happens once.
  - **Animation State**: The `.scrolled` class applies an `animation: scroll-in forwards`.
  - **Keyframes**: 
    - `0% { opacity: 0; transform: translateY(30px); }`
    - `100% { opacity: 1; transform: translateY(0); }`

---

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Initial Hiding | CSS `opacity` & `transform` | Hardware-accelerated properties, easily manipulated via classes. |
| Scroll Detection | JS `IntersectionObserver` | Highly performant native API. It runs asynchronously off the main thread, completely avoiding the jank and layout thrashing associated with traditional `window.addEventListener('scroll')`. |
| Entrance Animation | CSS `@keyframes` | Native CSS animations are performant and allow the use of `forwards` to maintain the final state. |

> **Feasibility Assessment**: 100% — This effect relies entirely on standard, modern web APIs (Intersection Observer and CSS Animations) which can be perfectly reproduced in a self-contained environment.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Scroll & Reveal",
    body_text: str = "Scroll down the container to see elements animate into view.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Intersection Observer Scroll Reveal effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
        text_muted = "#8b949e"
        surface_color = "rgba(255, 255, 255, 0.06)"
        border_color = "rgba(255, 255, 255, 0.1)"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        text_muted = "#5c5c77"
        surface_color = "#ffffff"
        border_color = "rgba(0, 0, 0, 0.1)"

    # === CSS ===
    css = f"""/* Intersection Observer Scroll Reveal — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --surface: {surface_color};
    --border: {border_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #000; /* Outer background to frame the component */
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.container {{
    width: var(--width);
    height: var(--height);
    background: var(--bg);
    color: var(--text);
    overflow-y: auto;
    overflow-x: hidden;
    position: relative;
    scroll-behavior: smooth;
    box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    border-radius: 12px;
}}

/* Hero Section (Forces scrolling) */
.hero {{
    height: 80%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
    border-bottom: 1px solid var(--border);
}}

.hero h1 {{
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 1rem;
    color: var(--accent);
}}

.hero p {{
    font-size: 1.1rem;
    color: var(--text-muted);
}}

.scroll-indicator {{
    margin-top: 3rem;
    animation: bounce 2s infinite;
    color: var(--text-muted);
}}

@keyframes bounce {{
    0%, 20%, 50%, 80%, 100% {{ transform: translateY(0); }}
    40% {{ transform: translateY(-15px); }}
    60% {{ transform: translateY(-7px); }}
}}

/* Content Section */
.content-section {{
    padding: 4rem 2rem;
    display: flex;
    flex-direction: column;
    gap: 3rem;
    max-width: 600px;
    margin: 0 auto;
}}

.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 2rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}}

.card h2 {{
    font-size: 1.5rem;
    margin-bottom: 0.75rem;
}}

.card p {{
    color: var(--text-muted);
    line-height: 1.6;
}}

/* ========================================= */
/* Core Visual Effect: Scroll Reveal Logic   */
/* ========================================= */

/* Initial hidden state */
.scroll-reveal {{
    opacity: 0;
    /* We don't strictly need transform here if it's in the 0% keyframe, 
       but setting it prevents layout jumps before JS initializes */
    transform: translateY(30px);
}}

/* The class added by IntersectionObserver */
.scroll-reveal.scrolled {{
    animation: scroll-in 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}}

/* Keyframes for the entrance */
@keyframes scroll-in {{
    0% {{
        opacity: 0;
        transform: translateY(30px);
    }}
    100% {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

/* Staggering utility (optional, if multiple items appear at once) */
.delay-1 {{ animation-delay: 0.1s; }}
.delay-2 {{ animation-delay: 0.2s; }}

/* Accessibility: Respect user motion preferences */
@media (prefers-reduced-motion: reduce) {{
    .scroll-reveal {{
        opacity: 1 !important;
        transform: translateY(0) !important;
        animation: none !important;
    }}
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
</head>
<body>
    <div class="container">
        
        <header class="hero">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <div class="scroll-indicator">
                ↓ Scroll Down
            </div>
        </header>

        <section class="content-section">
            <!-- Items configured to be revealed on scroll -->
            <article class="card scroll-reveal">
                <h2>Phase 1: Discovery</h2>
                <p>Curabitur non nulla sit amet nisl tempus convallis quis ac lectus. Nulla porttitor accumsan tincidunt. Donec rutrum congue leo eget malesuada.</p>
            </article>

            <article class="card scroll-reveal">
                <h2>Phase 2: Architecture</h2>
                <p>Pellentesque in ipsum id orci porta dapibus. Quisque velit nisi, pretium ut lacinia in, elementum id enim. Vestibulum ac diam sit amet quam vehicula.</p>
            </article>

            <article class="card scroll-reveal">
                <h2>Phase 3: Implementation</h2>
                <p>Mauris blandit aliquet elit, eget tincidunt nibh pulvinar a. Curabitur aliquet quam id dui posuere blandit. Sed porttitor lectus nibh.</p>
            </article>
            
            <article class="card scroll-reveal">
                <h2>Phase 4: Launch</h2>
                <p>Cras ultricies ligula sed magna dictum porta. Vivamus suscipit tortor eget felis porttitor volutpat. Vestibulum ante ipsum primis in faucibus.</p>
            </article>
        </section>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Intersection Observer Scroll Reveal Logic
document.addEventListener('DOMContentLoaded', () => {{
    
    // 1. Setup options for the observer
    const options = {{
        // Observe relative to the scrolling container
        root: document.querySelector('.container'), 
        // Margin around the root. '0px' means trigger exactly at the edge
        rootMargin: '0px', 
        // 0.15 means the callback fires when 15% of the element is visible
        threshold: 0.15 
    }};

    // 2. Create the Observer
    const observer = new IntersectionObserver((entries, obs) => {{
        // Filter for elements that are currently intersecting the viewport
        entries.filter(entry => entry.isIntersecting).forEach(entry => {{
            
            // Add the animation class
            entry.target.classList.add('scrolled');
            
            // Unobserve the element so it only animates once
            obs.unobserve(entry.target);
        }});
    }}, options);

    // 3. Select all target elements and instruct the observer to watch them
    const targetElements = document.querySelectorAll('.scroll-reveal');
    targetElements.forEach(el => {{
        observer.observe(el);
    }});
}});
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

* **Accessibility (`prefers-reduced-motion`)**: 
  Scroll-triggered animations can cause discomfort for users with vestibular disorders. The provided CSS includes a `@media (prefers-reduced-motion: reduce)` query that automatically overrides the initial hidden state and disables the animation, ensuring the content is immediately visible and static for those users.
* **Progressive Enhancement**: 
  If JavaScript fails to load or is disabled, elements with `opacity: 0` would remain invisible permanently. To fix this in production environments, a common practice is to apply the `.scroll-reveal` initial states inside a `.js-enabled` context (e.g., adding a `.js` class to the `<body>` on load), or use `<noscript>` tags to override the opacity back to `1`.
* **Performance**: 
  The `IntersectionObserver` is significantly more performant than binding to the `scroll` event. Scroll events fire hundreds of times a second and execute on the main thread, often causing scroll jank. The `IntersectionObserver` evaluates layout asynchronously. Additionally, animating `opacity` and `transform` delegates the rendering work to the GPU, avoiding expensive layout/paint recalulations.