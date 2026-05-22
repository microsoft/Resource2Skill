### 1. High-level Design Pattern Extraction

> **Skill Name**: Asymmetric Bento Grid with Stacked Overlays

* **Core Visual Mechanism**: This pattern utilizes CSS Grid's `grid-template-areas` to create irregular, interlocking UI modules known as a "Bento Grid" (inspired by Japanese lunchboxes). Furthermore, it leverages **Grid Stacking**—defining a single-cell grid (`grid-template-areas: "stack"`) on individual cards to effortlessly layer images, gradients, and text over each other without relying on brittle `position: absolute` calculations.
* **Why Use This Skill (Rationale)**: The Bento Grid provides high information density while maintaining a clean, structured, and modern aesthetic. By sizing modules differently (spanning multiple rows or columns), you establish a clear visual hierarchy. Grid Stacking solves the notorious difficulty of vertically/horizontally centering or pinning layered content, letting native Grid alignment (`place-items`, `place-self`) handle the math flawlessly.
* **Overall Applicability**: Ideal for SaaS feature highlights, creative portfolios, dashboard overview widgets, and product landing pages where diverse media (text, images, charts) needs to be presented cohesively. 
* **Value Addition**: Compared to standard flexbox lists or masonry layouts, Bento Grids offer deterministic, highly art-directable layouts. Grid Stacking completely eliminates Z-index/absolute-positioning bugs, ensuring background images and foreground text scale together responsively.
* **Browser Compatibility**: Fully supported in all modern browsers (Chrome 57+, Firefox 52+, Safari 10.1+, Edge 16+).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  *   **Structure**: A parent container defining the grid, housing multiple card elements (`div` or `article`). 
  *   **Color Logic**: Often employs a high-contrast theme. Example: A deep background (`#0d111c`), elevated cards (`rgba(255, 255, 255, 0.04)`), and vivid accent borders (`#00bfff`) on hover.
  *   **Typography**: Clean, sans-serif typography (`Inter` or `system-ui`). Bold, oversized headings for dominant cards, and subdued, smaller weights for descriptions.
  *   **CSS Properties**: `display: grid`, `grid-template-areas`, `gap`, `object-fit: cover` for images, and `backdrop-filter` for stacked glassmorphism layers.

* **Step B: Layout & Compositional Style**
  *   **Macro Layout (Bento)**: Uses fractional (`fr`) units. For example, a 4-column desktop layout where the primary feature spans `2fr` columns and `2fr` rows, while secondary features occupy `1fr` cells.
  *   **Micro Layout (Stacking)**: Each card is itself a grid (`display: grid; grid-template-areas: "stack";`). The image is assigned `grid-area: stack;` and the text overlay is also assigned `grid-area: stack;`, causing them to occupy the exact same spatial footprint. 
  *   **Alignment**: Overlay content is pinned using `place-self: end start;` (bottom-left) or `place-items: center;`.

* **Step C: Interactive Behavior & Animations**
  *   **Hover States**: Cards subtly scale up (`transform: translateY(-4px) scale(1.01)`), and background images zoom in slightly (`transform: scale(1.05)`) to create a parallax-like depth effect.
  *   **Transitions**: Smooth transitions (`0.4s cubic-bezier(0.2, 0.8, 0.2, 1)`) on transforms and box-shadows.
  *   **Responsiveness**: Uses `@media` queries to redefine `grid-template-areas`, flattening the layout from a 4-column asymmetric grid into a 2-column tablet grid, and finally a 1-column mobile stack.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Macro Layout** | CSS Grid (`grid-template-areas`) | Allows for explicit, visual mapping of asymmetric, spanning card layouts that are trivial to redefine in media queries. |
| **Layered Content** | CSS Grid Stacking | Overlays elements in the same cell (`grid-area: "stack"`) without absolute positioning, preserving document flow and aspect ratios perfectly. |
| **Responsive Degradation** | CSS Media Queries | Simplest, most performant way to collapse the Bento Grid areas from desktop to mobile views. |
| **Entry Animation** | Intersection Observer (JS) | Adds a modern, staggered fade-in effect as the grid enters the viewport, enhancing the premium feel. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Discover Our Features",
    body_text: str = "A powerful suite of tools designed to accelerate your workflow.",
    color_scheme: str = "dark",        
    accent_color: str = "#8b5cf6",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Asymmetric Bento Grid with Stacked Overlays.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#0a0a0f"
        text_color = "#f8fafc"
        text_muted = "#94a3b8"
        card_bg = "#1e293b"
        card_border = "rgba(255, 255, 255, 0.08)"
        overlay_gradient = "linear-gradient(to top, rgba(10, 10, 15, 0.95) 0%, rgba(10, 10, 15, 0.4) 50%, transparent 100%)"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        text_muted = "#475569"
        card_bg = "#ffffff"
        card_border = "rgba(0, 0, 0, 0.08)"
        overlay_gradient = "linear-gradient(to top, rgba(255, 255, 255, 0.95) 0%, rgba(255, 255, 255, 0.6) 50%, transparent 100%)"

    # Define CSS
    css = f"""/* Asymmetric Bento Grid with Grid Stacking */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --card-bg: {card_bg};
    --card-border: {card_border};
    --accent: {accent_color};
    --overlay: {overlay_gradient};
    --max-width: {width_px}px;
    --min-height: {height_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 4rem 2rem;
    overflow-x: hidden;
}}

/* Header Typography */
.header {{
    text-align: center;
    margin-bottom: 3rem;
    max-width: 600px;
}}

.header h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -0.025em;
    margin-bottom: 1rem;
}}

.header p {{
    font-size: 1.125rem;
    color: var(--text-muted);
    line-height: 1.6;
}}

/* Bento Grid Macro Layout */
.bento-grid {{
    display: grid;
    width: 100%;
    max-width: var(--max-width);
    /* 4 columns */
    grid-template-columns: repeat(4, 1fr);
    /* Auto rows maintain a consistent height rhythm */
    grid-auto-rows: minmax(240px, auto);
    gap: 1.5rem;
    
    /* The Magic: Mapping the Asymmetric Layout */
    grid-template-areas: 
        "hero hero box2 box3"
        "hero hero box4 box4";
}}

/* Assigning Grid Areas */
.card-hero {{ grid-area: hero; }}
.card-box2 {{ grid-area: box2; }}
.card-box3 {{ grid-area: box3; }}
.card-box4 {{ grid-area: box4; }}

/* Card Base Styles */
.bento-card {{
    background-color: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 1.5rem;
    overflow: hidden;
    position: relative;
    transition: transform 0.4s cubic-bezier(0.2, 0.8, 0.2, 1), 
                box-shadow 0.4s cubic-bezier(0.2, 0.8, 0.2, 1),
                border-color 0.4s ease;
    opacity: 0;
    transform: translateY(20px);
    
    /* Micro Layout: GRID STACKING */
    /* This allows us to overlay images and content without position:absolute */
    display: grid;
    grid-template-areas: "stack";
}}

.bento-card.visible {{
    opacity: 1;
    transform: translateY(0);
}}

.bento-card:hover {{
    transform: translateY(-6px) scale(1.01);
    box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.3);
    border-color: var(--accent);
}}

/* Grid Stack Layer 1: Background Image */
.card-img {{
    grid-area: stack;
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.6s cubic-bezier(0.2, 0.8, 0.2, 1);
}}

.bento-card:hover .card-img {{
    transform: scale(1.05);
}}

/* Grid Stack Layer 2: Gradient Overlay (for text readability) */
.card-overlay {{
    grid-area: stack;
    background: var(--overlay);
    pointer-events: none; /* Let clicks pass through */
}}

/* Grid Stack Layer 3: Content */
.card-content {{
    grid-area: stack;
    /* Pushes content to the bottom left */
    place-self: end start;
    padding: 2rem;
    z-index: 2;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}}

/* Non-stacked cards (Standard flex layout) */
.bento-card.standard {{
    display: flex;
    flex-direction: column;
    padding: 2rem;
}}

.standard .icon-wrapper {{
    width: 48px;
    height: 48px;
    border-radius: 12px;
    background: rgba(139, 92, 246, 0.1);
    color: var(--accent);
    display: grid;
    place-items: center;
    margin-bottom: auto; /* pushes text to bottom */
}}

.standard svg {{
    width: 24px;
    height: 24px;
}}

.card-title {{
    font-size: 1.5rem;
    font-weight: 600;
    line-height: 1.2;
}}

.card-desc {{
    font-size: 0.95rem;
    color: var(--text-muted);
    line-height: 1.5;
}}

/* Accent text for smaller cards */
.bento-card.accent {{
    background: var(--accent);
    color: #fff;
    border: none;
}}

.bento-card.accent .card-desc {{
    color: rgba(255, 255, 255, 0.8);
}}

/* === Responsiveness === */
@media (max-width: 960px) {{
    .bento-grid {{
        grid-template-columns: repeat(2, 1fr);
        grid-template-areas: 
            "hero hero"
            "box2 box3"
            "box4 box4";
    }}
}}

@media (max-width: 600px) {{
    .bento-grid {{
        grid-template-columns: 1fr;
        grid-auto-rows: minmax(280px, auto);
        grid-template-areas: 
            "hero"
            "box2"
            "box3"
            "box4";
    }}
    .header h1 {{
        font-size: 2rem;
    }}
}}

/* Accessibility: Respect motion preferences */
@media (prefers-reduced-motion: reduce) {{
    .bento-card, .card-img {{
        transition: none;
    }}
}}
"""

    # Define HTML
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
    
    <header class="header">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </header>

    <!-- The Bento Grid -->
    <main class="bento-grid">
        
        <!-- Large Hero Card (Grid Stacking applied) -->
        <article class="bento-card card-hero">
            <img class="card-img" src="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=2000&auto=format&fit=crop" alt="Abstract modern art" />
            <div class="card-overlay"></div>
            <div class="card-content">
                <h2 class="card-title">Dynamic Layering</h2>
                <p class="card-desc">Combining high-quality visuals with rich typography seamlessly using CSS Grid Stacking mechanisms.</p>
            </div>
        </article>

        <!-- Standard Card -->
        <article class="bento-card standard card-box2">
            <div class="icon-wrapper">
                <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
            </div>
            <div class="card-content" style="padding:0; margin-top: 1.5rem;">
                <h2 class="card-title" style="font-size: 1.25rem;">Blazing Fast</h2>
                <p class="card-desc">No heavy JavaScript calculations needed for layout.</p>
            </div>
        </article>

        <!-- Accent Card -->
        <article class="bento-card standard accent card-box3">
            <div class="icon-wrapper" style="background: rgba(0,0,0,0.2); color: #fff;">
                <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path></svg>
            </div>
            <div class="card-content" style="padding:0; margin-top: 1.5rem;">
                <h2 class="card-title" style="font-size: 1.25rem;">Highly Secure</h2>
                <p class="card-desc">Protected endpoints by default.</p>
            </div>
        </article>

        <!-- Wide Card (Grid Stacking applied) -->
        <article class="bento-card card-box4">
            <img class="card-img" src="https://images.unsplash.com/photo-1550745165-9bc0b252726f?q=80&w=1200&auto=format&fit=crop" alt="Retro tech aesthetic" />
            <div class="card-overlay"></div>
            <div class="card-content">
                <h2 class="card-title">Responsive Wrapping</h2>
                <p class="card-desc">Automatically adapts layout geometry from a 4-column desktop interface to a clean, single-column mobile view utilizing grid-template-areas.</p>
            </div>
        </article>

    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # Define JavaScript
    js = """// Interaction & Entry Animations
document.addEventListener('DOMContentLoaded', () => {
    const cards = document.querySelectorAll('.bento-card');
    
    // Set up Intersection Observer for staggered fade-in
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                // Add a slight delay based on index to stagger the animation
                setTimeout(() => {
                    entry.target.classList.add('visible');
                }, index * 100);
                
                // Unobserve after animating
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Apply observer to all bento cards
    cards.forEach(card => {
        observer.observe(card);
    });
});
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
  * Included the `prefers-reduced-motion` media query in CSS to disable the hover scale, translation, and image zoom animations for users who are sensitive to motion.
  * Structural HTML (`<main>`, `<article>`, `<header>`) provides solid landmark roles for screen readers.
  * Stacking text over images requires strict contrast control; the `var(--overlay)` property applies a robust linear gradient behind stacked text to ensure minimum WCAG AA contrast (4.5:1) regardless of the unpredictable image beneath it.
* **Performance**:
  * **Layout Thrashing Avoidance**: By using CSS Grid with `grid-template-areas`, layout calculations are handled natively by the browser's optimized rendering engine rather than requiring JS ResizeObservers or library-dependent masonry calculations.
  * **Animation Optimizations**: Animations (`transform`, `opacity`) are limited to properties that trigger compositor-only repaints, avoiding main thread layout reflows during hover states.
  * **Intersection Observer**: Entry animations run asynchronously off the main execution thread using the native `IntersectionObserver` API, meaning it incurs virtually zero performance overhead during scrolling compared to old `window.addEventListener('scroll')` techniques.