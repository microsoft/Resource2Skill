# Auto-Responsive Fluid Grid Gallery

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Auto-Responsive Fluid Grid Gallery

* **Core Visual Mechanism**: A responsive grid of card elements that automatically calculates the number of columns based on the available container width, entirely eliminating the need for CSS media queries. It uses the `repeat(auto-fit, minmax(min(100%, var(--min-size)), 1fr))` CSS Grid formula to ensure cards stretch to fill available space (`auto-fit`), wrap gracefully, and never cause horizontal overflow on extremely narrow screens.

* **Why Use This Skill (Rationale)**: Traditional responsive design relies on arbitrary "magic number" breakpoints (e.g., `@media (max-width: 768px)`), which are tedious to maintain and often break when the component is placed inside a smaller container rather than the full page width. This technique allows components to be completely self-governing and intrinsically responsive, reacting to their immediate environment rather than the viewport.

* **Overall Applicability**: Perfect for product catalogs, blog post layouts, dashboard widgets, portfolio galleries, and any scenario where dynamic, card-based content is fetched and displayed.

* **Value Addition**: It drastically reduces CSS payload, simplifies maintenance, and provides the flexibility to toggle between `auto-fit` (stretching to fill empty space) and `auto-fill` (leaving empty grid tracks for alignment), depending on how filtered or sparse data should be displayed.

* **Browser Compatibility**: Broadly supported in all modern browsers. CSS Grid (`auto-fit`, `auto-fill`, `minmax()`) has excellent support (>96%). The `min()` function used to prevent overflow on ultra-small screens is also fully supported in modern environments (Chrome 79+, Safari 11.1+, Firefox 75+).


### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Cards**: Soft-cornered (`border-radius: 12px`), distinct background color to stand out from the canvas.
  - **Color Logic**: Deep, high-contrast dark mode (e.g., Background `#111111`, Card `#222222`, Text `#f0f0f0`, Accent tags `#4caf50` / `#f44336`).
  - **Typography**: Clean, modern sans-serif (`Inter`). Clear hierarchy with bold titles and smaller, muted secondary text.
  - **CSS Drivers**: `display: grid`, `gap`, `minmax()`, and CSS Custom Properties for reusable configuration.

* **Step B: Layout & Compositional Style**
  - **Layout System**: Pure CSS Grid.
  - **Spatial Feel**: Uniform spacing using `gap: 1.5rem`.
  - **Proportions**: The minimum card size is defined via a custom property (e.g., `--grid-min-col-size: 275px`).
  - **The Overflow Hack**: Using `minmax(min(100%, 275px), 1fr)`. Without `min(100%, ...)`, a screen narrower than 275px would force horizontal scrolling. `min(100%, 275px)` tells the browser: "use 275px, unless the screen itself is smaller than 275px, then just use 100% of the screen."

* **Step C: Interactive Behavior & Animations**
  - **Filtering**: When items are hidden via JavaScript filtering, the grid automatically recalculates.
  - **Fit vs Fill**:
    - `auto-fit`: If there are only two cards, they will stretch to take up 50% of the row each.
    - `auto-fill`: If there are only two cards, they will remain 275px wide, leaving an empty "ghost" column next to them.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Auto-Responsive Grid | CSS Grid `auto-fit` / `auto-fill` | Native, performant, completely eliminates the need for media queries. |
| Overflow Prevention | CSS Math `min(100%, [size])` | Solves the specific bug where fixed minimums break on ultra-narrow viewports. |
| Fit vs Fill Demo | Vanilla JS + DOM classes | Provides an interactive way to visually understand how the grid handles empty space when items are filtered. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Mushroom Foraging Guide",
    body_text: str = "Filter the cards below and toggle the layout mode to see how CSS Grid handles dynamic content.",
    color_scheme: str = "dark",
    accent_color: str = "#4caf50",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Auto-Responsive Fluid Grid.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#121212"
        card_bg = "#1e1e1e"
        text_color = "#e0e0e0"
        text_muted = "#a0a0a0"
        border_color = "#333333"
    else:
        bg_color = "#f4f7f6"
        card_bg = "#ffffff"
        text_color = "#222222"
        text_muted = "#666666"
        border_color = "#e0e0e0"

    # === CSS ===
    css = f"""/* Auto-Responsive Fluid Grid */
:root {{
    --bg-color: {bg_color};
    --card-bg: {card_bg};
    --text-color: {text_color};
    --text-muted: {text_muted};
    --accent-color: {accent_color};
    --border-color: {border_color};
    
    /* Core Grid Variable */
    --grid-min-col-size: 280px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    line-height: 1.5;
    padding: 2rem;
    min-height: 100vh;
    display: flex;
    justify-content: center;
}}

.app-container {{
    width: 100%;
    max-width: {width_px}px;
    /* Optional constraints based on requested sizing */
    min-height: {height_px}px; 
}}

.header {{
    margin-bottom: 2rem;
}}

.header h1 {{
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}}

.header p {{
    color: var(--text-muted);
    margin-bottom: 1.5rem;
}}

/* Controls UI */
.controls {{
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    margin-bottom: 2rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--border-color);
    justify-content: space-between;
}}

.filter-group, .toggle-group {{
    display: flex;
    gap: 0.5rem;
    align-items: center;
}}

.btn {{
    background: transparent;
    border: 1px solid var(--border-color);
    color: var(--text-color);
    padding: 0.5rem 1rem;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.9rem;
    font-weight: 500;
    transition: all 0.2s ease;
}}

.btn:hover {{
    border-color: var(--accent-color);
}}

.btn.active {{
    background: var(--accent-color);
    border-color: var(--accent-color);
    color: #fff;
}}

/* =========================================
   CORE SKILL: THE FLUID GRID 
   ========================================= */
.mushroom-grid {{
    display: grid;
    gap: 1.5rem;
    /* Defaulting to auto-fit */
    grid-template-columns: repeat(
        auto-fit, 
        minmax(min(100%, var(--grid-min-col-size)), 1fr)
    );
    transition: all 0.3s ease;
}}

/* Modifier class for the auto-fill behavior */
.mushroom-grid.use-auto-fill {{
    grid-template-columns: repeat(
        auto-fill, 
        minmax(min(100%, var(--grid-min-col-size)), 1fr)
    );
}}
/* ========================================= */

.card {{
    background-color: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    transition: transform 0.2s ease, box-shadow 0.2s ease, opacity 0.3s ease;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}}

.card.hidden {{
    display: none;
}}

.card-header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1rem;
}}

.card-title {{
    font-size: 1.25rem;
    font-weight: 600;
}}

.tags {{
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-bottom: 1rem;
}}

.tag {{
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
}}

.tag.edible {{ background: rgba(76, 175, 80, 0.15); color: #4caf50; }}
.tag.toxic {{ background: rgba(244, 67, 54, 0.15); color: #f44336; }}
.tag.season {{ background: rgba(33, 150, 243, 0.15); color: #2196f3; }}

.card-desc {{
    color: var(--text-muted);
    font-size: 0.95rem;
    margin-bottom: 1.5rem;
    flex-grow: 1;
}}

.card-footer {{
    background: rgba(0, 0, 0, 0.05);
    padding: 0.75rem;
    border-radius: 6px;
    font-size: 0.85rem;
    border-left: 3px solid var(--accent-color);
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
    <div class="app-container">
        <header class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>

        <div class="controls">
            <div class="filter-group">
                <strong>Filter:</strong>
                <button class="btn active" data-filter="all">All</button>
                <button class="btn" data-filter="spring">Spring Only</button>
                <button class="btn" data-filter="edible">Edible</button>
            </div>
            <div class="toggle-group">
                <strong>Grid Mode:</strong>
                <button class="btn active" id="btn-fit">auto-fit</button>
                <button class="btn" id="btn-fill">auto-fill</button>
            </div>
        </div>

        <!-- The Responsive Grid -->
        <div class="mushroom-grid" id="main-grid">
            
            <div class="card" data-category="edible summer fall">
                <div class="card-header">
                    <h2 class="card-title">Chanterelle</h2>
                </div>
                <div class="tags">
                    <span class="tag edible">Edible</span>
                    <span class="tag season">Summer</span>
                </div>
                <p class="card-desc">Golden-yellow, funnel-shaped mushroom with false gills. Has a fruity odor like apricots.</p>
                <div class="card-footer">
                    <strong>Important:</strong> Has toxic look-alikes.
                </div>
            </div>

            <div class="card" data-category="edible spring">
                <div class="card-header">
                    <h2 class="card-title">Morel</h2>
                </div>
                <div class="tags">
                    <span class="tag edible">Edible</span>
                    <span class="tag season">Spring</span>
                </div>
                <p class="card-desc">Distinctive honeycomb-like cap structure. Found in wooded areas in early spring.</p>
                <div class="card-footer">
                    <strong>Important:</strong> Must be cooked before eating.
                </div>
            </div>

            <div class="card" data-category="toxic summer fall">
                <div class="card-header">
                    <h2 class="card-title">Death Cap</h2>
                </div>
                <div class="tags">
                    <span class="tag toxic">Toxic</span>
                    <span class="tag season">Summer</span>
                </div>
                <p class="card-desc">Pale green to white cap with white gills. Responsible for the majority of fatal mushroom poisonings.</p>
                <div class="card-footer" style="border-color: #f44336;">
                    <strong>Important:</strong> Extremely toxic.
                </div>
            </div>

            <div class="card" data-category="edible fall">
                <div class="card-header">
                    <h2 class="card-title">Lion's Mane</h2>
                </div>
                <div class="tags">
                    <span class="tag edible">Edible</span>
                    <span class="tag season">Fall</span>
                </div>
                <p class="card-desc">White, shaggy appearance like a lion's mane. Known for its lobster-like taste.</p>
                <div class="card-footer">
                    <strong>Important:</strong> No toxic look-alikes.
                </div>
            </div>

            <div class="card" data-category="toxic spring">
                <div class="card-header">
                    <h2 class="card-title">False Morel</h2>
                </div>
                <div class="tags">
                    <span class="tag toxic">Toxic</span>
                    <span class="tag season">Spring</span>
                </div>
                <p class="card-desc">Brain-like, reddish-brown cap with irregular shape. Contains the toxin gyromitrin.</p>
                <div class="card-footer" style="border-color: #f44336;">
                    <strong>Important:</strong> Highly toxic.
                </div>
            </div>

        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Interactive logic to demonstrate fit vs fill
document.addEventListener('DOMContentLoaded', () => {{
    const grid = document.getElementById('main-grid');
    const filterBtns = document.querySelectorAll('.filter-group .btn');
    const btnFit = document.getElementById('btn-fit');
    const btnFill = document.getElementById('btn-fill');
    const cards = document.querySelectorAll('.card');

    // Filtering Logic
    filterBtns.forEach(btn => {{
        btn.addEventListener('click', (e) => {{
            // Update active state
            filterBtns.forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');

            const filter = e.target.getAttribute('data-filter');

            cards.forEach(card => {{
                if (filter === 'all') {{
                    card.classList.remove('hidden');
                }} else {{
                    const categories = card.getAttribute('data-category');
                    if (categories.includes(filter)) {{
                        card.classList.remove('hidden');
                    }} else {{
                        card.classList.add('hidden');
                    }}
                }}
            }});
        }});
    }});

    // Grid Layout Toggle Logic (auto-fit vs auto-fill)
    btnFit.addEventListener('click', () => {{
        btnFit.classList.add('active');
        btnFill.classList.remove('active');
        grid.classList.remove('use-auto-fill');
    }});

    btnFill.addEventListener('click', () => {{
        btnFill.classList.add('active');
        btnFit.classList.remove('active');
        grid.classList.add('use-auto-fill');
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

* **Accessibility**: 
  - Using semantic tags where applicable.
  - Color contrast ratios in the dark mode variant meet WCAG AA standards (light gray text on dark gray backgrounds).
  - The interactive filtering uses visual hiding (`display: none`), which correctly removes the item from the screen reader's accessibility tree, ensuring they don't read hidden content.
* **Performance**: 
  - CSS Grid calculates mathematically under the hood and is exceptionally performant. Because we removed Media Queries, the browser does not need to parse CSS rule overrides as the window resizes, it simply re-flows elements naturally.
  - The `min(100%, 280px)` rule is natively evaluated by the CSS engine, completely bypassing the need for JavaScript `ResizeObserver` or `window.innerWidth` checks.