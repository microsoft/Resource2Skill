# Skill Strategy Document

## 1. High-level Design Pattern Extraction

> **Skill Name**: Auto-Responsive CSS Grid with Overflow Protection

* **Core Visual Mechanism**: A fluid card grid that automatically calculates the optimal number of columns based on available container width, requiring zero media queries. It uses the highly robust CSS Grid formula: `repeat(auto-fill, minmax(min(275px, 100%), 1fr))`. This specific pattern ensures cards never shrink below 275px, never cause horizontal scrolling on tiny screens (thanks to the `min()` function), and don't stretch awkwardly when the grid is partially empty (thanks to `auto-fill`).
* **Why Use This Skill (Rationale)**: Traditional responsive grids rely on breakpoints (e.g., 1 column on mobile, 2 on tablet, 3 on desktop), leading to "magic numbers" and jumpy layout shifts. This mathematical CSS approach allows the browser to dynamically calculate tracks. Furthermore, choosing `auto-fill` over `auto-fit` preserves the intended column width even if content is filtered down to a single item, preventing the lonely item from grotesantly stretching across the entire screen.
* **Overall Applicability**: Essential for dynamic content galleries, portfolio pages, e-commerce product listings, and dashboard widgets where the number of items is unknown or actively filtered by the user.
* **Value Addition**: Drastically reduces CSS complexity by eliminating media queries. It provides a more resilient layout component that natively adapts to any container it is placed in, making it a perfect drop-in modular component.
* **Browser Compatibility**: Excellent. The CSS Grid `minmax()`, `repeat()`, `auto-fill`, and CSS math function `min()` are supported in all modern browsers (Edge, Chrome, Firefox, Safari 11.1+).

## 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **HTML Structure**: A parent grid container holding multiple semantic card elements. A control header containing filter buttons and a layout toggle.
  - **Color Logic**: Uses a CSS-variable-driven theme. In dark mode: Background `#121212`, surface `#1e1e1e`, subtle borders `#333333`, and an accent color (e.g., `#4caf50`) applied using `color-mix()` to generate soft translucent backgrounds for tags.
  - **Typographic Hierarchy**: Driven by the `Inter` sans-serif font. `1.5rem` bold titles, `0.75rem` uppercase tracking tags, and `0.9rem` muted body text with `1.5` line-height for readability.
  - **Core CSS Properties**: `display: grid`, `grid-template-columns`, `gap`.

* **Step B: Layout & Compositional Style**
  - **Grid System**: The grid dictates a gap of `1.5rem` (24px).
  - **Proportions**: The minimum column size is defined via `--grid-min-col-size: 275px`. If the screen is narrower than 275px, the `min(275px, 100%)` fallback kicks in, setting the column to `100%` and preventing horizontal scrollbars.
  - **Card Layout**: Each card uses `display: flex; flex-direction: column;` to push footer elements to the bottom or stack content vertically.

* **Step C: Interactive Behavior & Animations**
  - **Card Hover**: Cards lift slightly `transform: translateY(-4px)` with an enhanced `box-shadow` on a `0.2s ease` transition.
  - **Filtering Logic**: A JavaScript event listener filters cards by setting `display: none`. Because CSS Grid ignores elements with `display: none`, the grid automatically closes the gaps.
  - **Educational Interaction**: A select dropdown allows toggling between `auto-fill` and `auto-fit`. When filtered to 1 or 2 items, `auto-fit` will aggressively stretch them to fill the space, demonstrating exactly why `auto-fill` is the superior choice for dynamic content.

## 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Responsive layout logic | **Pure CSS Grid** | `repeat(auto-fill, minmax())` natively recalculates tracks on resize, completely eliminating media query bloat. |
| Tiny screen overflow protection | **CSS `min()` function** | `min(275px, 100%)` acts as a fail-safe, clamping the width to the viewport on ultra-narrow devices. |
| Dynamic filtering | **JavaScript DOM + `display: none`** | Dynamically removes items from the DOM flow; CSS Grid natively handles the visual reflow. |
| Tag translucency | **CSS `color-mix()`** | Easily generates an alpha-transparent version of the injected Hex accent color without needing complex color conversions. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Mushroom Reference Guide",
    body_text: str = "Filter the cards below and toggle the Grid Mode. Notice how 'auto-fill' preserves card sizes when few items are visible, while 'auto-fit' awkwardly stretches them.",
    color_scheme: str = "dark",
    accent_color: str = "#4caf50",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Auto-Responsive CSS Grid effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derived theme colors
    if color_scheme == "dark":
        bg_color = "#121212"
        surface_color = "#1e1e1e"
        border_color = "#333333"
        text_color = "#f5f5f5"
        text_muted = "#a0a0a0"
    else:
        bg_color = "#f8f9fa"
        surface_color = "#ffffff"
        border_color = "#e0e0e0"
        text_color = "#1a1a2e"
        text_muted = "#666666"

    # === CSS ===
    css = f"""/* Auto-Responsive CSS Grid Component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --surface: {surface_color};
    --border: {border_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --grid-min-col-size: 275px;
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    padding: 2rem 1rem;
    line-height: 1.5;
}}

.container {{
    width: 100%;
    max-width: var(--width);
    min-height: var(--height);
    display: flex;
    flex-direction: column;
}}

header {{
    margin-bottom: 2rem;
}}

.title {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
}}

.body-text {{
    color: var(--text-muted);
    font-size: 1.1rem;
    max-width: 65ch;
}}

.controls-wrapper {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    flex-wrap: wrap;
    gap: 1.5rem;
    margin-bottom: 2.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--border);
}}

.filters {{
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
}

.filter-btn {{
    background: transparent;
    border: 1px solid var(--border);
    color: var(--text);
    padding: 0.4rem 1rem;
    border-radius: 999px;
    cursor: pointer;
    font-size: 0.9rem;
    font-weight: 500;
    transition: all 0.2s ease;
}}

.filter-btn:hover {{
    border-color: var(--accent);
    color: var(--accent);
}}

.filter-btn.active {{
    background: var(--accent);
    border-color: var(--accent);
    color: {bg_color};
}}

.grid-mode-control {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
    background: var(--surface);
    padding: 0.5rem 1rem;
    border-radius: 8px;
    border: 1px solid var(--border);
}}

.grid-mode-control label {{
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-muted);
}}

.grid-mode-control select {{
    background: transparent;
    color: var(--text);
    border: none;
    font-family: inherit;
    font-size: 0.95rem;
    cursor: pointer;
    outline: none;
}}

/* =========================================
   THE CORE TECHNIQUE
   ========================================= */
.grid-container {{
    display: grid;
    gap: 1.5rem;
    
    /* 
      1. auto-fill: Keeps column sizes rigid and creates empty tracks, preventing stretching
      2. minmax: Sets the bounds for the columns
      3. min(275px, 100%): Ensures columns don't overflow viewports smaller than 275px 
    */
    grid-template-columns: repeat(auto-fill, minmax(min(var(--grid-min-col-size), 100%), 1fr));
}}

.grid-container.mode-fit {{
    grid-template-columns: repeat(auto-fit, minmax(min(var(--grid-min-col-size), 100%), 1fr));
}}

/* Card Styling */
.card {{
    display: flex;
    flex-direction: column;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
    border-color: color-mix(in srgb, var(--accent) 50%, transparent);
}}

.card-tag {{
    align-self: flex-start;
    padding: 0.25rem 0.75rem;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    background: color-mix(in srgb, var(--accent) 15%, transparent);
    color: var(--accent);
    margin-bottom: 1.25rem;
}}

.card-title {{
    font-size: 1.25rem;
    margin-bottom: 0.5rem;
    font-weight: 600;
}}

.card-desc {{
    font-size: 0.95rem;
    color: var(--text-muted);
    flex-grow: 1;
}}
"""

    # === HTML ===
    # Generate mock card data
    categories = ["spring", "summer", "autumn"]
    labels = ["Spring", "Summer", "Autumn"]
    
    cards_html = ""
    for i in range(1, 10):
        idx = i % 3
        cat = categories[idx]
        label = labels[idx]
        cards_html += f"""
        <div class="card" data-category="{cat}">
            <span class="card-tag">{label}</span>
            <h3 class="card-title">Grid Item {i}</h3>
            <p class="card-desc">This responsive item will adapt to the grid mathematically. Try filtering down to just a few items to see how the layout reacts.</p>
        </div>"""

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
    <div class="container">
        <header>
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </header>

        <div class="controls-wrapper">
            <div class="filters">
                <button class="filter-btn active" data-filter="all">All</button>
                <button class="filter-btn" data-filter="spring">Spring</button>
                <button class="filter-btn" data-filter="summer">Summer</button>
                <button class="filter-btn" data-filter="autumn">Autumn</button>
            </div>

            <div class="grid-mode-control">
                <label for="mode-select">Behavior</label>
                <select id="mode-select">
                    <option value="auto-fill">auto-fill (Rigid Columns)</option>
                    <option value="auto-fit">auto-fit (Stretching Columns)</option>
                </select>
            </div>
        </div>

        <div class="grid-container" id="card-grid">
            {cards_html}
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """document.addEventListener('DOMContentLoaded', () => {
    const filters = document.querySelectorAll('.filter-btn');
    const cards = document.querySelectorAll('.card');
    const modeSelect = document.getElementById('mode-select');
    const grid = document.getElementById('card-grid');

    // Filter Logic
    filters.forEach(btn => {
        btn.addEventListener('click', () => {
            // Update active state
            filters.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            const filterValue = btn.dataset.filter;
            
            // Toggle visibility. CSS grid auto-collapses 'display: none' elements
            cards.forEach(card => {
                if (filterValue === 'all' || card.dataset.category === filterValue) {
                    card.style.display = 'flex';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });

    // Toggle grid behavior between auto-fill and auto-fit to demonstrate the tutorial concept
    modeSelect.addEventListener('change', (e) => {
        if (e.target.value === 'auto-fit') {
            grid.classList.add('mode-fit');
        } else {
            grid.classList.remove('mode-fit');
        }
    });
});
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

## 4. Accessibility & Performance Notes

* **Accessibility**:
  - The control header uses a `<select>` with a linked `<label>` for standard form control accessibility.
  - Buttons use explicit `cursor: pointer` and prominent visual hover/active states.
  - Contrast ratios between text (`#f5f5f5` or `#a0a0a0`) and the dark surface (`#1e1e1e`) pass WCAG AA standards.
* **Performance**:
  - **Zero Layout Thrashing**: This layout method shifts calculating responsive bounds from JavaScript (`window.resize` listeners) directly to the native C++ browser rendering engine via CSS Grid math, resulting in highly performant resizing.
  - Using `display: none` for filtering avoids heavy DOM mutation (inserting/removing nodes), though for exceptionally large lists (>500 items), virtualizing the list would be more memory efficient.