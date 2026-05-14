import os

def create_component(
    output_dir: str,
    main_title: str = "Online Shop",
    item_prefix: str = "Shoe",
    item_count: int = 12,
    color_scheme: str = "light",        # "dark" or "light"
    accent_color: str = "#0071ff",     # CSS hex color for accent (for buttons/highlights)
    grid_min_item_width_px: int = 250, # Minimum width for responsive grid items
    grid_gap_em: float = 1.0,         # Gap between grid items in em
    bento_layout_base_color: str = "#0071ff", # Base color for bento boxes
    stacking_image_url: str = "https://via.placeholder.com/600x400/9966cc/ffffff?text=Mountain+City", # Image for stacking example
    stacking_text_content: str = "Explore the peaks, find tranquility, and discover breathtaking vistas. Our mountain city offers the perfect escape for nature lovers and adventurers alike.",
    **kwargs,
) -> dict:
    """
    Create a web component reproducing various CSS Grid layout visual effects from the tutorial.

    Includes a responsive product grid, a Bento layout, and a grid stacking example.
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#1a1a1a"
        text_color = "#f0f0f0"
        card_bg_color = "#2a2a2a"
        border_color = "#3a3a3a"
    else: # light theme
        bg_color = "#f8f9fa"
        text_color = "#212529"
        card_bg_color = "#ffffff"
        border_color = "#e9ecef"

    # --- HTML content for Responsive Product Grid ---
    products_html = ""
    for i in range(1, item_count + 1):
        products_html += f"""
        <div class="product-card">
            <img src="https://via.placeholder.com/300x200/{bento_layout_base_color.replace('#','')}/ffffff?text={item_prefix}+{i}" alt="{item_prefix} {i}">
            <p>{item_prefix} {i}</p>
            <span>${(i * 10) + 50}.00</span>
        </div>
        """

    # --- HTML content for Bento Grid example ---
    bento_boxes_html = ""
    bento_box_names = ["one", "two", "three", "four", "five"]
    for i, name in enumerate(bento_box_names):
        bento_boxes_html += f"""
        <div class="bento-box bento-box-{name}">Box {i+1}</div>
        """

    # --- HTML content for Grid Stacking example ---
    stacking_html = f"""
    <div class="stack-wrapper">
        <img class="stack-image" src="{stacking_image_url}" alt="Background Image">
        <div class="stack-text-container">
            <h3>Image Text Card</h3>
            <p>{stacking_text_content}</p>
        </div>
    </div>
    """

    # === CSS ===
    css = f"""
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

body {{
    font-family: 'Inter', sans-serif;
    background-color: {bg_color};
    color: {text_color};
    margin: 0;
    padding: 20px;
    line-height: 1.6;
}}

h1, h2, h3 {{
    color: {text_color};
    margin-bottom: 15px;
}}

.section {{
    margin-bottom: 60px;
    padding-bottom: 30px;
    border-bottom: 1px solid {border_color};
}}

/* --- Responsive Product Grid --- */
.products-list {{
    display: grid;
    /* This creates responsive columns: min {grid_min_item_width_px}px, max 1fr, auto-fit as many as possible */
    grid-template-columns: repeat(auto-fit, minmax({grid_min_item_width_px}px, 1fr));
    gap: {grid_gap_em}em;
    justify-content: center; /* Center the grid when items don't fill the row */
    padding: 20px 0;
}}

.product-card {{
    background-color: {card_bg_color};
    border: 1px solid {border_color};
    border-radius: 8px;
    padding: 15px;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: transform 0.2s ease-in-out;
}}

.product-card:hover {{
    transform: translateY(-5px);
}}

.product-card img {{
    max-width: 100%;
    height: auto;
    border-radius: 4px;
    margin-bottom: 10px;
}}

.product-card p {{
    font-weight: 600;
    margin: 5px 0;
}}

.product-card span {{
    color: {accent_color};
    font-weight: 700;
    font-size: 1.1em;
}}

/* --- Bento Grid Example --- */
.bento-grid-container {{
    display: grid;
    grid-template-columns: repeat(4, 1fr); /* Default 4 columns for large screens */
    grid-template-rows: repeat(2, 200px); /* Two rows, fixed height */
    gap: {grid_gap_em}em;
    grid-template-areas:
        "bento-one bento-two bento-two bento-three"
        "bento-one bento-four bento-five bento-five";
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px 0;
}}

.bento-box {{
    background-color: {bento_layout_base_color};
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    color: #ffffff;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}}

.bento-box-one {{ grid-area: bento-one; }}
.bento-box-two {{ grid-area: bento-two; }}
.bento-box-three {{ grid-area: bento-three; }}
.bento-box-four {{ grid-area: bento-four; }}
.bento-box-five {{ grid-area: bento-five; }}

/* Tablet Layout for Bento Grid (e.g., max-width 992px) */
@media (max-width: 992px) {{
    .bento-grid-container {{
        grid-template-columns: repeat(3, 1fr); /* 3 columns */
        grid-template-rows: repeat(3, 180px); /* 3 rows */
        grid-template-areas:
            "bento-one bento-one bento-two"
            "bento-four bento-five bento-two"
            "bento-four bento-five bento-three";
    }}
}}

/* Mobile Layout for Bento Grid (e.g., max-width 576px) */
@media (max-width: 576px) {{
    .bento-grid-container {{
        grid-template-columns: 1fr; /* Single column */
        grid-template-rows: auto; /* Auto height for rows */
        grid-template-areas:
            "bento-one"
            "bento-two"
            "bento-three"
            "bento-four"
            "bento-five";
    }}
    .bento-box {{
        padding: 20px;
        height: auto; /* Allow height to adjust */
    }}
}}

/* --- Grid Stacking Example --- */
.stack-wrapper {{
    display: grid;
    max-width: 600px;
    margin: 0 auto;
    border-radius: 10px;
    overflow: hidden; /* Ensure content stays within rounded corners */
    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    /* No explicit position relative needed on wrapper as grid handles child positioning */
}}

.stack-image {{
    grid-column: 1 / -1; /* Span full width */
    grid-row: 1 / -1;    /* Span full height */
    width: 100%;
    height: 100%;
    object-fit: cover;
    z-index: 1; /* Image is behind text */
}}

.stack-text-container {{
    grid-column: 1 / -1; /* Span full width */
    grid-row: 1 / -1;    /* Span full height */
    z-index: 2; /* Text is on top */
    display: flex;
    flex-direction: column;
    justify-content: flex-end; /* Align text to bottom */
    padding: 20px;
    background: linear-gradient(to top, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0) 100%);
    color: white;
}}

.stack-text-container h3 {{
    margin-bottom: 5px;
    font-size: 1.5em;
    color: white;
}}

.stack-text-container p {{
    font-size: 0.9em;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{main_title}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="section">
        <h1>{main_title} - Responsive Product Grid</h1>
        <p>This grid automatically adjusts the number of columns and resizes items based on the screen width, using <code>repeat(auto-fit, minmax({grid_min_item_width_px}px, 1fr))</code>.</p>
        <div class="products-list">
            {products_html}
        </div>
    </div>

    <div class="section">
        <h2>Bento Grid Example</h2>
        <p>Demonstrates <code>grid-template-areas</code> for complex layouts and responsive adjustments via media queries.</p>
        <div class="bento-grid-container">
            {bento_boxes_html}
        </div>
    </div>

    <div class="section">
        <h2>Grid Stacking Example</h2>
        <p>Demonstrates stacking elements on top of each other using CSS Grid properties (<code>grid-column</code>, <code>grid-row</code>, <code>z-index</code>).</p>
        {stacking_html}
    </div>

</body>
</html>"""

    # === JavaScript ===
    # No dynamic JS needed for these static layout examples.
    # The responsive behavior and visual effects are purely CSS-driven.
    js = """// No JavaScript required for these CSS Grid layout examples."""

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

