# Perfect-Fit CSS Scroll Snapping

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Perfect-Fit CSS Scroll Snapping

* **Core Visual Mechanism**: Snapping the viewport (or a container) to discrete sections as the user scrolls, creating a slide-show or presentation-like feel. This is achieved natively using `scroll-snap-type` on the container and `scroll-snap-align` on the child elements. A critical secondary mechanism is accounting for sticky/fixed navigation bars using `scroll-padding-top` so that snapped content perfectly aligns just *below* the header rather than being obscured by it.
* **Why Use This Skill (Rationale)**: Standard scrolling allows users to stop halfway between sections, which can break layout composition and storytelling rhythm. Scroll snapping enforces a "perfect frame," ensuring the user always lands on a precisely composed view. This heavily reduces cognitive load and directs focus to one discrete piece of information at a time.
* **Overall Applicability**: Ideal for landing page hero sections, immersive storytelling pages, digital portfolios, web-based presentations, and full-screen product showcases where pacing and framing are critical.
* **Browser Compatibility**: Excellent. `scroll-snap-type`, `scroll-snap-align`, and `scroll-padding-top` are supported in all modern browsers (Edge 79+, Firefox 68+, Chrome 69+, Safari 11+).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Containers**: A parent scrollable container (`div` or `html`) and multiple full-viewport child sections (`section`).
  - **Fixed Navigation**: A sticky header that overlays the content.
  - **Color Logic**: Uses alternating background opacities (e.g., `rgba(255,255,255,0.05)`) on consecutive sections to visually distinguish the snapping boundary.
  - **CSS Properties**: 
    - `scroll-snap-type: y mandatory` (forces snapping on the Y axis).
    - `scroll-padding-top` (offsets the snap position to accommodate the sticky nav).
    - `scroll-snap-align: start` (aligns the top of the element to the offset snapport).
    - `scroll-snap-stop: always` (prevents fast scrolling from skipping past sections).

* **Step B: Layout & Compositional Style**
  - **Layout System**: The scroll container uses `overflow-y: scroll`. Each section inside relies on Flexbox (`display: flex`, `align-items: center`) to center content perfectly within the snapped frame.
  - **Spatial Proportions**: The sticky navigation is a fixed height (e.g., `70px`). The first section is automatically offset by document flow, while subsequent sections explicitly fill the remaining vertical space using `height: calc(100% - 70px)`.
  - **Z-index Layering**: The navigation bar must sit above the scrolling content (`z-index: 10`) with an opaque or blurred background so text passing underneath is legible.

* **Step C: Interactive Behavior & Animations**
  - **Scrolling**: Smooth snapping handled entirely by the browser's CSS engine.
  - **JS Enhancement**: An `IntersectionObserver` watches which section is currently centered in the viewport and dynamically highlights the corresponding navigation link.
  - **Transitions**: Native smooth scrolling enabled via `scroll-behavior: smooth` so clicking navigation links glides to the target section before snapping.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Mandatory Snapping | CSS `scroll-snap-type` | Native, GPU-accelerated browser API; avoids heavy JavaScript scroll event listeners which often cause jank. |
| Fixed Header Offset | CSS `scroll-padding-top` | Perfectly offsets the CSS snap target area so content isn't hidden behind the sticky navigation. |
| Section Framing | CSS `calc()` | Subtracts the nav height from the total container height, ensuring the snapped section exactly fills the visible space perfectly. |
| Nav Highlighting | JS `IntersectionObserver` | The most performant way to detect which section is actively in view without attaching costly `scroll` event listeners. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "CSS Scroll Snapping",
    body_text: str = "A pure CSS solution for perfectly framed, full-page scrolling experiences without JavaScript jank.",
    color_scheme: str = "dark",
    accent_color: str = "#3b82f6",
    width_px: int = 1000,
    height_px: int = 700,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Perfect-Fit CSS Scroll Snapping effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        body_bg = "#020617"       # Very dark page background
        bg_color = "#0f172a"      # Component background
        text_color = "#f8fafc"
        surface_color = "rgba(255, 255, 255, 0.04)"
        surface_alt = "rgba(255, 255, 255, 0.02)"
    else:
        body_bg = "#f1f5f9"
        bg_color = "#ffffff"
        text_color = "#0f172a"
        surface_color = "rgba(0, 0, 0, 0.04)"
        surface_alt = "rgba(0, 0, 0, 0.02)"

    # === CSS ===
    css = f"""/* Perfect-Fit CSS Scroll Snapping */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --surface-alt: {surface_alt};
    --width: {width_px}px;
    --height: {height_px}px;
    --nav-height: 70px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: {body_bg};
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

/* The Core Mechanism Container */
.scroll-container {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    background: var(--bg);
    border: 1px solid var(--surface);
    border-radius: 16px;
    box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);
    overflow-y: scroll;
    position: relative;
    
    /* Scroll Snapping Properties */
    scroll-snap-type: y mandatory;
    scroll-padding-top: var(--nav-height); /* Crucial for sticky header */
    scroll-behavior: smooth;
}}

/* Custom scrollbar to keep it clean */
.scroll-container::-webkit-scrollbar {{
    width: 6px;
}}
.scroll-container::-webkit-scrollbar-track {{
    background: transparent;
}}
.scroll-container::-webkit-scrollbar-thumb {{
    background: var(--surface);
    border-radius: 3px;
}}

.sticky-nav {{
    position: sticky;
    top: 0;
    height: var(--nav-height);
    background: var(--bg);
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 40px;
    border-bottom: 1px solid var(--surface);
    z-index: 10;
}}

.nav-brand {{
    font-weight: 700;
    font-size: 1.2rem;
    color: var(--text);
    letter-spacing: -0.5px;
}}

.nav-links {{
    display: flex;
    gap: 24px;
}}

.nav-links a {{
    color: var(--text);
    text-decoration: none;
    font-size: 0.9rem;
    font-weight: 500;
    opacity: 0.4;
    transition: all 0.3s ease;
}}

.nav-links a:hover,
.nav-links a.active {{
    opacity: 1;
    color: var(--accent);
}}

/* The Snap Targets */
.snap-page {{
    /* Height subtracts nav to perfectly fill remaining container space */
    height: calc(100% - var(--nav-height));
    
    /* Child Snapping Properties */
    scroll-snap-align: start;
    scroll-snap-stop: always; /* Prevents skipping past sections on fast scrolls */
    
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px;
    text-align: center;
}}

.snap-page:nth-child(even) {{
    background: var(--surface-alt);
}}

.snap-page:nth-child(odd) {{
    background: transparent;
}}

.title {{
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 24px;
    letter-spacing: -1px;
    line-height: 1.1;
}}

.body-text {{
    font-size: 1.125rem;
    max-width: 600px;
    line-height: 1.6;
    opacity: 0.7;
}}

.scroll-indicator {{
    margin-top: 48px;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--accent);
    font-weight: 600;
    animation: bounce 2s infinite;
}}

@keyframes bounce {{
    0%, 20%, 50%, 80%, 100% {{ transform: translateY(0); }}
    40% {{ transform: translateY(-8px); }}
    60% {{ transform: translateY(-4px); }}
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="scroll-container">
        <!-- Sticky Header -->
        <nav class="sticky-nav">
            <div class="nav-brand">SnapFlow.</div>
            <div class="nav-links">
                <a href="#page1" class="active">01</a>
                <a href="#page2">02</a>
                <a href="#page3">03</a>
                <a href="#page4">04</a>
            </div>
        </nav>

        <!-- Snapping Sections -->
        <section class="snap-page" id="page1">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
            <div class="scroll-indicator">↓ Scroll to Snap</div>
        </section>

        <section class="snap-page" id="page2">
            <h2 class="title">Perfectly Framed</h2>
            <p class="body-text">By using <code>scroll-snap-align: start</code>, the browser physically pulls the container to ensure this section perfectly aligns at the top edge of the offset area.</p>
        </section>

        <section class="snap-page" id="page3">
            <h2 class="title">Accounting for Headers</h2>
            <p class="body-text">The parent container uses <code>scroll-padding-top: 70px</code>. This ensures the snapping calculates its "top" 70px down, preventing content from hiding under the sticky nav.</p>
        </section>

        <section class="snap-page" id="page4">
            <h2 class="title">No JavaScript Layouts</h2>
            <p class="body-text">The layout physics are 100% CSS. The only JavaScript included is a tiny Intersection Observer to highlight the navigation dots as you scroll.</p>
        </section>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Intersection Observer to update navigation links based on visible section
document.addEventListener('DOMContentLoaded', () => {{
    const sections = document.querySelectorAll('.snap-page');
    const navLinks = document.querySelectorAll('.nav-links a');
    const container = document.querySelector('.scroll-container');

    const observer = new IntersectionObserver((entries) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                const id = entry.target.getAttribute('id');
                
                // Update active class on nav links
                navLinks.forEach(link => {{
                    if (link.getAttribute('href') === `#${{id}}`) {{
                        link.classList.add('active');
                    }} else {{
                        link.classList.remove('active');
                    }}
                }});
            }}
        }});
    }}, {{
        root: container,
        // The negative top margin matches the sticky nav height so the 
        // intersection trigger line starts below the nav
        rootMargin: '-70px 0px 0px 0px', 
        threshold: 0.5 // Trigger when a section is 50% visible
    }});

    sections.forEach(section => observer.observe(section));
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
  - Standard scrolling interactions remain fully intact for mouse-wheel, touch, and keyboard (Arrow keys, Page Down/Up).
  - The `scroll-behavior: smooth` is generally safe, but for a fully production-ready environment, it's recommended to wrap it in `@media (prefers-reduced-motion: no-preference)` to respect users who suffer from vestibular motion sickness.
* **Performance**: 
  - Using CSS for scroll snapping is vastly superior to older JavaScript implementations (like fullPage.js) because it taps directly into the browser's native compositing and scrolling thread. It will not cause main-thread jank.
  - The included JavaScript relies on the `IntersectionObserver` API rather than a `scroll` event listener. This ensures the navigation state logic only fires when necessary (section boundaries) rather than hundreds of times a second, saving battery life and keeping the UI buttery smooth.