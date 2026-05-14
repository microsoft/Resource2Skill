### 1. High-level Design Pattern Extraction

> **Skill Name**: Aligned Card Layout using CSS Subgrid

* **Core Visual Mechanism**: Horizontally aligned internal elements (headers, content blocks, buttons) across a row of multiple standalone card components. This is achieved by nesting a grid (`.card`) inside a parent grid (`.wrapper`) and inheriting the parent's row tracks via `grid-template-rows: subgrid`. 
* **Why Use This Skill (Rationale)**: One of the most common UI annoyances is "ragged" layouts, where cards in a row have different heights due to varying paragraph lengths, causing their bottom buttons to misalign. Traditionally, this required complex Flexbox hacks (`margin-top: auto`), fixed heights, or JavaScript calculations. CSS Subgrid solves this natively, ensuring complete horizontal harmony while remaining content-aware and flexible.
* **Overall Applicability**: Perfect for pricing tables, feature comparison charts, product listings, blog post grids, and team member profile cards where structural rhythm is critical.
* **Value Addition**: Delivers a clean, uniform, professional appearance without brittle CSS hacks. It makes the UI feel deliberate and engineered, significantly improving readability and visual trust.
* **Browser Compatibility**: `subgrid` is part of CSS Grid Layout Level 2 and is fully supported in all major modern browsers (Baseline 2023: Chrome 117+, Safari 16+, Firefox 71+).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Wrapper Grid**: The outer container that dictates the overarching layout and implicitly generates the row tracks.
  - **Card Containers**: The nested grids that hook into the parent's rows.
  - **Color Logic**: Deep interface palette. Dark background (`#0b0f19`), slightly elevated surface color for cards (`#1e293b`), subtle borders (`#334155`), and a striking purple/cyan accent color (`#8a2be2`) for interactive elements.
  - **Typographic Hierarchy**: High-contrast, clean sans-serif (`Inter`). Headers are bold and prominent (`700` weight, `1.5rem`), while descriptions are muted (`#94a3b8`) with a readable line-height (`1.6`).

* **Step B: Layout & Compositional Style**
  - **Responsive Parent Grid**: `grid-template-columns: repeat(auto-fit, minmax(320px, 1fr))` ensures cards wrap fluidly without media queries.
  - **Subgrid Hook**: The `.card` elements use `grid-template-rows: subgrid` and `grid-row: span 3`. Because the browser auto-places the cards side-by-side, they all span the *same* three implicit rows (Row 1 for headers, Row 2 for paragraphs, Row 3 for buttons).
  - **Spacing**: The parent's `gap: 2rem` spaces the cards apart. Inside the subgrid, we use `gap: 0` to explicitly override inherited gaps, managing vertical rhythm via standard `margin-bottom` on the text elements instead.

* **Step C: Interactive Behavior & Animations**
  - Purely structural CSS technique—no JavaScript required.
  - Enhanced with CSS transitions: a subtle `transform: translateY(-4px)` and border highlight on card hover provides satisfying tactile feedback.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Cross-card alignment | CSS `subgrid` | Native, declarative layout feature designed exactly for this use case. Avoids JS calculation overhead. |
| Responsive Columns | CSS Grid `auto-fit` | Fluidly wraps cards based on container width without hardcoded media queries. |
| Inner spacing control | `gap: 0` + `margin` | Subgrids inherit parent gaps; overriding it prevents huge vertical spaces inside the cards. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Aligned Cards with CSS Subgrid",
    body_text: str = "Notice how the elements align perfectly horizontally across all cards, no matter the length of the paragraph content.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#8a2be2",     # Purple accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the CSS Subgrid alignment layout.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#0b0f19"
        text_color = "#ffffff"
        text_muted = "#94a3b8"
        surface_color = "#1e293b"
        surface_border = "#334155"
        btn_text = "#ffffff"
    else:
        bg_color = "#f8f9fa"
        text_color = "#0f172a"
        text_muted = "#475569"
        surface_color = "#ffffff"
        surface_border = "#e2e8f0"
        btn_text = "#ffffff"

    # === CSS ===
    css = f"""/* CSS Subgrid Alignment — generated component */
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
    --surface-border: {surface_border};
    --btn-text: {btn_text};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

.page-container {{
    width: 100%;
    max-width: var(--width);
    display: flex;
    flex-direction: column;
    gap: 3rem;
}}

.header {{
    text-align: center;
}}

.header h1 {{
    font-size: 2.5rem;
    margin-bottom: 1rem;
    font-weight: 700;
}}

.header p {{
    color: var(--text-muted);
    font-size: 1.125rem;
    max-width: 600px;
    margin: 0 auto;
    line-height: 1.6;
}}

/* --- Core Subgrid Layout --- */

.wrapper {{
    display: grid;
    /* Responsive auto-wrapping columns */
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 2rem; 
}}

.card {{
    display: grid;
    /* Subgrid inherits row tracks from .wrapper implicitly */
    grid-template-rows: subgrid;
    /* Span exactly 3 rows for title, desc, and button */
    grid-row: span 3;
    
    /* Override inherited parent gap to control inner spacing manually */
    gap: 0;
    
    background: var(--surface);
    border: 1px solid var(--surface-border);
    border-radius: 16px;
    padding: 2.5rem 2rem;
    box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
}}

.card:hover {{
    transform: translateY(-4px);
    border-color: var(--accent);
    box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.2);
}}

.card-title {{
    font-size: 1.5rem;
    font-weight: 700;
    margin: 0 0 1rem 0;
    /* Keep title pinned to top of its row track */
    align-self: start; 
}}

.card-desc {{
    font-size: 1rem;
    line-height: 1.6;
    color: var(--text-muted);
    margin: 0 0 2.5rem 0;
    /* Keep text pinned to top of its row track if another card stretches it */
    align-self: start; 
}}

.card-btn {{
    /* Pin button to the bottom of the card */
    align-self: end;
    justify-self: start;
    padding: 0.875rem 1.75rem;
    background: var(--accent);
    color: var(--btn-text);
    border: none;
    border-radius: 8px;
    font-weight: 600;
    font-size: 1rem;
    cursor: pointer;
    transition: filter 0.2s ease, transform 0.2s ease;
}}

.card-btn:hover {{
    filter: brightness(1.15);
    transform: scale(1.02);
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
    <main class="page-container">
        <header class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>
        
        <div class="wrapper">
            <article class="card">
                <h2 class="card-title">Custom Websites</h2>
                <p class="card-desc">We design fast, modern, and responsive websites that help your business look professional on every device. From clean landing pages to full company sites.</p>
                <button class="card-btn">Learn More</button>
            </article>
            
            <article class="card">
                <h2 class="card-title">Full-Service Web Development</h2>
                <p class="card-desc">Need a more complex solution? We develop complete web applications with solid architecture, clean code, and a focus on long-term maintainability. Whether it's booking systems, dashboards, or custom APIs — we've got it covered.</p>
                <button class="card-btn">Discover</button>
            </article>
            
            <article class="card">
                <h2 class="card-title">SEO & Performance</h2>
                <p class="card-desc">Slow site? Dropping rankings? We audit, optimize, and rebuild the technical foundation of your website to improve loading speed, search visibility, and overall user experience.</p>
                <button class="card-btn">Optimize</button>
            </article>
        </div>
    </main>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// CSS Subgrid Layout
document.addEventListener('DOMContentLoaded', () => {{
    // This layout is powered entirely by native CSS Grid and Subgrid.
    // No JavaScript is required to maintain the horizontal alignment logic!
    console.log("Subgrid layout initialized natively via CSS.");
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

* **Accessibility (a11y)**: 
  - The layout uses `<article>` elements for the cards, providing correct semantic meaning to screen readers identifying standalone content blocks. 
  - Standard DOM ordering is preserved. Unlike some masonry or positioning hacks, CSS Subgrid respects the exact tab order (Header -> Text -> Button).
  - Hover states utilize high-contrast visual cues (border highlight and transform), improving discoverability without sacrificing baseline readability.
* **Performance**: 
  - Native CSS Subgrid is extremely performant because the browser's layout engine resolves the grid dependencies concurrently during the paint cycle. 
  - Zero Layout Thrashing: Unlike JS `ResizeObserver` techniques that measure DOM heights and artificially apply fixed pixel heights (causing costly forced reflows), Subgrid runs purely on the GPU/Render thread.