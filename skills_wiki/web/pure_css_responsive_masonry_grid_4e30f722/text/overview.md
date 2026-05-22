# Pure CSS Responsive Masonry Grid

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Pure CSS Responsive Masonry Grid

*   **Core Visual Mechanism**: A Pinterest-style, variable-height grid layout achieved entirely with CSS without requiring JavaScript calculations. It relies on the CSS Multi-column Layout module (`column-count`, `column-gap`) combined with `break-inside: avoid` on the items. It features two card styles: standard stacked content (image on top, text below) and immersive overlay content (text positioned over the image with a gradient fade for legibility).
*   **Why Use This Skill (Rationale)**: Traditional grid layouts force rows to align, leaving awkward white space if content varies in length or images vary in aspect ratio. A masonry layout tightly packs items vertically, maximizing screen real estate and creating a visually engaging, dynamic rhythm. Doing it in pure CSS is vastly more performant and easier to maintain than older JavaScript-based solutions (like Masonry.js).
*   **Overall Applicability**: Ideal for photography portfolios, blog post feeds, product catalogs, user-generated content feeds, and dashboard widget layouts where items have unpredictable heights.
*   **Value Addition**: Transforms a basic linear list into a highly space-efficient, visually interesting mosaic. It natively adapts to screen sizes, seamlessly reflowing from a single column on mobile to multi-column on desktop.
*   **Browser Compatibility**: Excellent. The CSS Multi-column Layout module has been supported in all major browsers for many years. The `break-inside: avoid` property is also widely supported to prevent items from splitting across columns.

### 2. Visual & Technical Breakdown

*   **Step A: Core Visual Elements**
    *   **Markup**: A simple nesting structure: `.grid` container > `.grid-item` wrapper > `.card` component.
    *   **Cards**: Feature rounded corners (`5px`), hidden overflow (to clip images), and a subtle 1px solid border.
    *   **Color Logic (Dark Theme default)**:
        *   Background: Deep gray (`#222222`)
        *   Card Background: Lighter gray (`#333333`)
        *   Borders: Medium gray (`#545454`)
        *   Text: White (`#ffffff`) and off-white (`#9b9b9b` for body text)
    *   **Card Variants**:
        *   *Standard*: Flow layout. Image takes full width, text sits below with padding.
        *   *Overlay (`.card-v2`)*: Uses `position: relative` on the card. A `::before` pseudo-element creates a dark `linear-gradient` from bottom to top to ensure text contrast. Text is `position: absolute` at the bottom.

*   **Step B: Layout & Compositional Style**
    *   **Grid System**: Driven by CSS `column-count`. Unlike CSS Grid (`display: grid`), which creates rigid rows and columns, `column-count` flows content vertically down one column before wrapping to the next.
    *   **Item Integrity**: The critical CSS rule is `break-inside: avoid;` applied to the `.grid-item`. This tells the browser not to split a card in half at the bottom of a column, forcing it to the top of the next column instead.
    *   **Spacing**: Consistent padding (`1.5em`) inside cards and consistent gaps between columns (`column-gap`).

*   **Step C: Interactive Behavior & Animations**
    *   The tutorial focuses on the static layout and responsiveness. The layout reflows automatically as the viewport resizes based on `@media` queries altering the `column-count`. (I will add a subtle CSS hover scale effect in the reproduction for polish, as is standard practice for card grids).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
| :--- | :--- | :--- |
| Masonry Layout | Pure CSS (`column-count`) | Most performant, native way to achieve variable-height vertical packing without JS. |
| Item integrity | CSS `break-inside: avoid` | Prevents cards from being chopped across column boundaries. |
| Text overlay contrast | CSS `linear-gradient` pseudo-element | Creates a smooth, hardware-accelerated fade without needing extra HTML elements. |
| Responsiveness | CSS Media Queries | Adjusts column count dynamically based on viewport width. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Photography Portfolio",
    body_text: str = "A pure CSS masonry grid layout showcasing variable-height content.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Pure CSS Masonry Grid.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#222222"
        card_bg = "#333333"
        border_color = "#545454"
        text_color = "#ffffff"
        text_muted = "#9b9b9b"
        overlay_gradient_start = "rgba(34, 34, 34, 1)" # Matches bg_color roughly
        overlay_gradient_end = "rgba(34, 34, 34, 0)"
    else:
        bg_color = "#f4f4f5"
        card_bg = "#ffffff"
        border_color = "#e4e4e7"
        text_color = "#18181b"
        text_muted = "#71717a"
        overlay_gradient_start = "rgba(24, 24, 27, 0.9)" # Dark overlay even in light mode for white text
        overlay_gradient_end = "rgba(24, 24, 27, 0)"

    # === CSS ===
    css = f"""/* Pure CSS Masonry Grid */
:root {{
    --bg-color: {bg_color};
    --card-bg: {card_bg};
    --border-color: {border_color};
    --text-primary: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --overlay-start: {overlay_gradient_start};
    --overlay-end: {overlay_gradient_end};
}}

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: var(--bg-color);
    color: var(--text-primary);
    line-height: 1.5;
    padding: 2rem;
    min-height: 100vh;
}}

.header {{
    text-align: center;
    margin-bottom: 3rem;
}}

.header h1 {{
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}}

.header p {{
    color: var(--text-muted);
}}

/* --- Core Masonry Layout --- */
.grid {{
    /* Limit max width and center */
    max-width: {width_px}px;
    margin: 0 auto;
    
    /* CSS Columns magic */
    column-count: 1;
    column-gap: 1.5rem;
}}

.grid-item {{
    /* Prevent items from breaking across columns */
    break-inside: avoid;
    page-break-inside: avoid; /* For older browsers */
    margin-bottom: 1.5rem;
}}

/* Responsive column adjustments */
@media screen and (min-width: 600px) {{
    .grid {{ column-count: 2; }}
}}
@media screen and (min-width: 900px) {{
    .grid {{ column-count: 3; }}
}}
@media screen and (min-width: 1300px) {{
    .grid {{ column-count: 4; }}
}}

/* --- Card Styles --- */
.card {{
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    overflow: hidden;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.15);
}}

.card img {{
    width: 100%;
    height: auto;
    display: block; /* Removes bottom space under inline images */
    object-fit: cover;
}}

.card-content {{
    padding: 1.5rem;
}}

.card-content h2 {{
    font-size: 1.25rem;
    margin-bottom: 0.75rem;
}}

.card-content p {{
    font-size: 0.95rem;
    color: var(--text-muted);
}}

/* --- Overlay Card Style (v2) --- */
.card-v2 {{
    position: relative;
    border: none; /* Often looks better without border when full image */
}}

.card-v2::before {{
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(0deg, var(--overlay-start) 0%, var(--overlay-end) 50%);
    pointer-events: none;
    z-index: 1;
}}

.card-v2 .card-content {{
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    z-index: 2;
    color: #ffffff; /* Force white text on dark overlay */
}}

.card-v2 .card-content p {{
    color: rgba(255, 255, 255, 0.8);
}}
"""

    # === HTML ===
    # Generate some dummy content with different aspect ratios
    cards_html = ""
    image_seeds = [
        (400, 600, "Portrait Photography", "A beautiful portrait capturing natural light.", "card"),
        (500, 400, "Landscape Views", "Stunning mountains and lakes reflecting the sky.", "card-v2"),
        (400, 800, "Architecture", "Towering skyscrapers reaching into the clouds above the city.", "card"),
        (600, 400, "Macro Details", "Close up shots revealing hidden textures.", "card"),
        (400, 500, "Street Life", "Candid moments from busy city streets and markets.", "card-v2"),
        (500, 700, "Wildlife", "Majestic animals in their natural habitats.", "card"),
        (800, 600, "Abstract Textures", "Patterns and colors blending together seamlessly.", "card-v2"),
        (400, 450, "Minimalism", "Finding beauty in simplicity and negative space.", "card"),
    ]

    for i, (w, h, title, desc, cls) in enumerate(image_seeds):
        img_url = f"https://picsum.photos/seed/masonry{i}/{w}/{h}"
        cards_html += f"""
        <div class="grid-item">
            <div class="{cls}">
                <img src="{img_url}" alt="{title}" loading="lazy">
                <div class="card-content">
                    <h2>{title}</h2>
                    <p>{desc}</p>
                </div>
            </div>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="header">
        <h1 style="color: var(--accent);">{title_text}</h1>
        <p>{body_text}</p>
    </div>

    <div class="grid">
        {cards_html}
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Pure CSS implementation requires no JavaScript for layout logic.
console.log('Masonry grid initialized. Layout handled entirely by CSS.');
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

*   **Accessibility**:
    *   The generated HTML includes `alt` attributes for images, which are essential since images carry significant context in a masonry layout.
    *   Semantic `<h2>` tags are used within cards to maintain a logical document outline.
    *   The overlay gradient ensures text remains readable even if the underlying image is light-colored.
*   **Performance**:
    *   **High Performance**: This technique is inherently high-performance because it delegates the heavy lifting of layout calculation entirely to the browser's native rendering engine via CSS. It avoids the layout thrashing and forced synchronous reflows common in JavaScript masonry libraries.
    *   Images include the `loading="lazy"` attribute in the HTML generation, ensuring off-screen images do not consume bandwidth or processing power until the user scrolls near them.