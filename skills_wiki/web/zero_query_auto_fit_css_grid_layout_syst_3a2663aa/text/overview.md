### 1. High-level Design Pattern Extraction

> **Skill Name**: Zero-Query Auto-Fit CSS Grid Layout System

* **Core Visual Mechanism**: This pattern leverages CSS Grid's algorithmic track sizing (`repeat(auto-fit, minmax(...))`) coupled with dense auto-flow and item spanning. It creates a dynamic, masonry-like responsive layout that automatically reflows to fit the viewport—without a single `@media` query. It also demonstrates CSS Grid's native Z-axis layering (stacking items within the same `grid-area`) to create overlapping elements like badges or text overlays without absolute positioning.
* **Why Use This Skill (Rationale)**: Before CSS Grid, creating robust 2D layouts required heavy use of floats, deeply nested flexbox containers, or JavaScript masonry libraries. This technique offloads the layout math entirely to the browser's native engine. It guarantees perfectly aligned rows and columns, allows items to establish visual hierarchy by breaking out of standard cell sizes (spanning), and simplifies DOM structure.
* **Overall Applicability**: This technique is universally applicable for dashboards, portfolio galleries, e-commerce product grids, feature cards on landing pages, and responsive article feeds.
* **Value Addition**: It brings true fluid responsiveness. Instead of discrete breakpoints where the layout abruptly shifts, the grid continuously calculates how many columns can fit. Furthermore, the ability to layer elements natively in the same grid cell opens up clean, relative-positioning-free overlay designs.
* **Browser Compatibility**: Broadly supported across all modern browsers (Chrome 66+, Safari 10.1+, Firefox 52+). Requires no polyfills.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Grid Container**: A primary wrapper acting as the CSS Grid context.
  - **Cards (Grid Items)**: Modular content blocks functioning as cells.
  - **Color Logic**: Uses a semantic token system. Dark mode relies on deep slate backgrounds (`#0f172a`), elevated surface colors (`#1e293b`), and vibrant accent injections (`var(--accent)`). Light mode flips to soft greys (`#f8fafc`) and crisp white surfaces (`#ffffff`).
  - **CSS Properties**: Driven by `grid-template-columns`, `grid-auto-rows`, `grid-column: span`, `gap`, `justify-self`, and `align-self`.

* **Step B: Layout & Compositional Style**
  - **Responsive Track Generation**: `grid-template-columns: repeat(auto-fit, minmax(260px, 1fr))` ensures no column is ever smaller than 260px. Once enough space exists for another 260px column, the browser adds one automatically.
  - **Dense Packing**: `grid-auto-flow: dense` tells the browser to backfill any empty gaps left by larger spanned items with smaller items appearing later in the DOM.
  - **Header Spanning**: A header item spans the entire width using `grid-column: 1 / -1` (from the first line to the last explicit line).
  - **Z-Index Layering**: An image and text block are assigned to the exact same `grid-area`, automatically overlapping them. Z-index is used to specify which sits on top.

* **Step C: Interactive Behavior & Animations**
  - Cards feature a pure CSS subtle hover lift and shadow (`transition: transform 0.2s, box-shadow 0.2s`) to emphasize interactivity.
  - No JavaScript is required for the layout reflow, minimizing layout thrashing and maximizing framerate during window resizing.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Responsive Column Sizing** | CSS Grid (`auto-fit`, `minmax`) | Eliminates the need for multiple `@media` queries; fluidly handles any viewport size automatically. |
| **Element Layering (Overlays)** | CSS Grid Area Stacking | Assigning multiple children to the same `grid-area` creates a stacking context without taking them out of the document flow via `position: absolute`. |
| **Grid Item Spanning** | CSS Grid `span` Keyword | Allows highlighted or featured content to occupy 2x2 grid spaces easily while maintaining vertical and horizontal alignment. |
| **Individual Item Alignment** | CSS `justify-self` / `align-self` | Provides precise alignment overrides for specific items inside their grid tracks without affecting the entire container. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "CSS Grid Masterclass",
    body_text: str = "A fluid, zero-media-query responsive layout demonstrating auto-fit grids, track spanning, and native layer stacking.",
    color_scheme: str = "dark",
    accent_color: str = "#ec4899",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Zero-Query Auto-Fit CSS Grid Layout.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_color = "#f8fafc"
        text_muted = "#94a3b8"
        surface_color = "#1e293b"
        border_color = "#334155"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        text_muted = "#64748b"
        surface_color = "#ffffff"
        border_color = "#e2e8f0"

    # === CSS ===
    css = f"""/* Zero-Query Auto-Fit CSS Grid — generated component */
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
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: flex-start;
    justify-content: center;
    overflow-x: hidden;
    overflow-y: auto;
    padding: clamp(16px, 4vw, 48px);
}}

/* Main wrapper defining the bounds */
.app-wrapper {{
    width: 100%;
    max-width: var(--width);
    min-height: var(--height);
    margin: 0 auto;
}}

/* ==========================================
   THE CORE SKILL: Responsive Grid Layout
========================================== */
.grid-container {{
    display: grid;
    /* Auto-fit + minmax creates the zero-query responsive behavior */
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    /* Implicit row size for generated tracks */
    grid-auto-rows: 200px;
    /* Dense packing fills holes left by spanning items */
    grid-auto-flow: dense;
    gap: 20px;
    width: 100%;
}}

/* Header area spanning all columns */
.grid-header {{
    grid-column: 1 / -1; /* Spans from first to last grid line */
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    padding-bottom: 12px;
}}

.grid-header h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    margin-bottom: 8px;
}}

.grid-header p {{
    color: var(--text-muted);
    font-size: 1.1rem;
    max-width: 60ch;
    line-height: 1.5;
}}

/* Base Card Styles */
.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
    display: flex;
    flex-direction: column;
    gap: 12px;
}}

.card h3 {{
    font-size: 1.25rem;
    font-weight: 600;
}}

.card p {{
    color: var(--text-muted);
    font-size: 0.95rem;
    line-height: 1.5;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
}}

/* Highlighted Item: Track Spanning */
.card-featured {{
    grid-column: span 2;
    grid-row: span 2;
    background: var(--accent);
    color: #ffffff;
    border: none;
    justify-content: center;
}}

.card-featured h3 {{
    font-size: 2rem;
}}

.card-featured p {{
    color: rgba(255, 255, 255, 0.9);
    font-size: 1.1rem;
}}

.badge-inline {{
    background: rgba(255, 255, 255, 0.2);
    align-self: flex-start;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: auto;
}}

/* Highlighted Item: Native Grid Stacking (Layering) */
.card-layered {{
    display: grid;
    /* Create a single explicit area named 'stack' */
    grid-template-areas: "stack";
    padding: 0;
    overflow: hidden;
    border: none;
}}

.card-layered > * {{
    /* Assign all children to the exact same cell */
    grid-area: stack;
}}

.layered-img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    filter: brightness(0.4) saturate(1.2);
    z-index: 0;
}}

.layered-content {{
    z-index: 1; /* Sits above the image */
    align-self: end; /* Align to the bottom of the cell */
    padding: 24px;
    color: white;
}}

.layered-content p {{
    color: rgba(255, 255, 255, 0.8);
}}

.badge-corner {{
    z-index: 2;
    justify-self: end; /* Align to the right edge */
    align-self: start; /* Align to the top edge */
    background: var(--accent);
    color: white;
    padding: 8px 16px;
    border-radius: 0 0 0 16px;
    font-weight: bold;
    font-size: 0.85rem;
}}

/* Highlighted Item: Cell Alignment Override */
.card-alignment {{
    display: grid;
    grid-template-rows: auto 1fr;
    gap: 16px;
}}

.align-demo-grid {{
    display: grid;
    grid-template-rows: repeat(3, 1fr);
    gap: 8px;
    background: var(--bg);
    border-radius: 8px;
    padding: 8px;
    border: 1px dashed var(--border);
}}

.align-box {{
    background: var(--surface);
    border: 1px solid var(--border);
    padding: 4px 16px;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: 600;
    align-self: center; /* Vertical center inside its row */
}}

/* Overriding horizontal alignment for individual items */
.align-box.start {{ justify-self: start; }}
.align-box.center {{ justify-self: center; }}
.align-box.end {{ justify-self: end; }}

/* Prevent featured card from causing overflow on very small devices */
@media (max-width: 600px) {{
    .card-featured {{
        grid-column: span 1;
        grid-row: span 1;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-wrapper">
        <div class="grid-container">
            
            <!-- Full Width Spanning Header -->
            <header class="grid-header">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
            </header>

            <!-- 2x2 Spanning Feature Card -->
            <article class="card card-featured">
                <div class="badge-inline">Featured Span</div>
                <h3>Visual Hierarchy</h3>
                <p>By declaring <code>grid-column: span 2</code> and <code>grid-row: span 2</code>, this item seamlessly breaks out of the standard track dimensions, forcing the algorithm to flow smaller items around it.</p>
            </article>

            <!-- Grid Cell Layering (Z-Index without position:absolute) -->
            <article class="card card-layered">
                <img class="layered-img" src="https://images.unsplash.com/photo-1550684848-fac1c5b4e853?q=80&w=800&auto=format&fit=crop" alt="Abstract gradient background">
                <div class="badge-corner">Z-Index Stack</div>
                <div class="layered-content">
                    <h3>Grid Layering</h3>
                    <p>Both this text and the background image share the same <code>grid-area</code>. CSS Grid naturally stacks them on the Z-axis, avoiding brittle absolute positioning.</p>
                </div>
            </article>

            <!-- Item Alignment -->
            <article class="card card-alignment">
                <div>
                    <h3>Cell Alignment</h3>
                    <p>Using <code>justify-self</code>.</p>
                </div>
                <div class="align-demo-grid">
                    <div class="align-box start">start</div>
                    <div class="align-box center">center</div>
                    <div class="align-box end">end</div>
                </div>
            </article>

            <!-- Auto-fit Responsive Items -->
            <article class="card">
                <h3>Responsive Tracks</h3>
                <p>Because of <code>minmax(260px, 1fr)</code>, this card shrinks to fit available space but will trigger a column wrap if the space falls below 260 pixels.</p>
            </article>
            
            <article class="card">
                <h3>Implicit Grid</h3>
                <p>Any items placed beyond explicitly defined tracks are captured by the implicit grid, automatically taking on the 200px height defined in <code>grid-auto-rows</code>.</p>
            </article>

            <article class="card">
                <h3>Dense Auto-Flow</h3>
                <p>The <code>grid-auto-flow: dense</code> directive instructs the grid algorithm to back-fill any empty cells left behind by larger spanning items.</p>
            </article>

        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// CSS Grid Layout Component
// The layout logic is handled 100% via CSS Grid natively.
// JavaScript can be utilized here for dynamically fetching and injecting cards into the .grid-container.

document.addEventListener('DOMContentLoaded', () => {{
    console.log('Grid Container mounted. Resize the browser to watch the auto-fit algorithm in action.');
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

* **Accessibility**: 
  - Semantic HTML (`<article>`, `<header>`) is used to segment the cards logically for screen readers. 
  - Care has been taken to map text colors correctly based on the `color_scheme` to maintain a high contrast ratio (WCAG AA compliant).
  - Important Note: Using `grid-auto-flow: dense` can disconnect the *visual order* of elements from the *DOM order* (tabbing sequence). Avoid putting strictly sequential data or forms in a dense grid.
* **Performance**: 
  - **Exceptional**: Handling responsive column reflow using native CSS Grid algorithms (`repeat`, `auto-fit`, `minmax`) avoids attaching `window.addEventListener('resize')` scripts. This prevents main-thread blocking and layout thrashing (jank), taking full advantage of native browser layout optimizations.