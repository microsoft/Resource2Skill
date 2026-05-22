def create_component(
    output_dir: str,
    title_text: str = "CSS Grid Demo",
    body_text: str = "Explore the power of CSS Grid with responsive layouts, flexible item placement, and easy alignment.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Dynamic CSS Grid Layout with Responsive Item Placement and Overlays.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#1a1a2e"
        text_color = "#f0f0f0"
        item_bg_base = "#3a3a5e"
        item_border = "#5a5a8e"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        item_bg_base = "#e0e0f0"
        item_border = "#c0c0d0"

    # === CSS ===
    css = f"""/* Dynamic CSS Grid Layout with Responsive Item Placement and Overlays — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --item-bg-base: {item_bg_base};
    --item-border: {item_border};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 20px;
    gap: 20px;
    overflow-x: hidden; /* Prevent horizontal scroll for responsive demo */
}}

h1, p {{
    text-align: center;
    margin-bottom: 10px;
}}

.container {{
    display: grid;
    /* Explicitly define rows (4 rows, each 100px tall) */
    grid-template-rows: repeat(4, 100px);
    /* Responsive columns: auto-fit as many 100px columns as possible,
       remaining space distributed equally with 1fr.
       This is the 'responsive without media queries' trick. */
    grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
    
    /* Gaps between grid cells */
    grid-gap: 1em; /* 16px */

    /* Implicit rows will be 100px tall */
    grid-auto-rows: 100px;
    /* Implicit columns will be 1fr wide (not used with auto-fit) */
    /* grid-auto-columns: 1fr; */ 
    
    /* Overall grid alignment within the container if space is available */
    /* justify-content: center; */ /* Uncomment to see grid centered horizontally */
    /* align-content: center; */ /* Uncomment to see grid centered vertically */

    width: 100%; /* Take full width of parent */
    max-width: var(--width); /* Limit max width for demonstration */
    height: auto; /* Allow height to adjust */
    border: 2px solid var(--item-border);
    padding: 10px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    border-radius: 8px;
}}

.item {{
    background-color: var(--item-bg-base);
    border: 1px solid var(--item-border);
    border-radius: 5px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5em;
    font-weight: 600;
    color: var(--text);
    /* Default item alignment within its cell (stretch is default) */
    justify-self: stretch; 
    align-self: stretch;
}}

/* Item 1: Span 2 rows and 2 columns */
.item-1 {{
    grid-row: 1 / span 2;
    grid-column: 1 / span 2;
    background-color: {accent_color};
}}

/* Item 2: Explicitly placed, spanning columns */
.item-2 {{
    grid-row: 1; /* Starts on row line 1 */
    grid-column: 3 / span 2; /* Starts on column line 3, spans 2 columns */
    background-color: #ff6b6b;
}}

/* Item 3: Uses grid-area shorthand for placement, spans rows and columns, with layering */
.item-3 {{
    grid-area: 3 / 1 / span 2 / span 2; /* Row start 3, Col start 1, spans 2 rows, spans 2 cols */
    background-color: #a051ff;
    z-index: 1; /* Layered below item 4 */
}}

/* Item 4: Layered on top of item 3, occupying a specific cell and spanning */
.item-4 {{
    grid-row: 3; /* Starts on row line 3 */
    grid-column: 2 / span 2; /* Starts on column line 2, spans 2 columns */
    background-color: #36a2eb;
    z-index: 2; /* Layered above item 3 */
}}

/* Item 5: Demonstrates individual item alignment (justify-self & align-self) */
.item-5 {{
    grid-row: 1;
    grid-column: 5;
    background-color: #ffdd57;
    justify-self: start; /* Overrides default justify-items: stretch */
    align-self: end;    /* Overrides default align-items: stretch */
    width: 60px; /* Give it a size to show alignment */
    height: 60px;
}}

/* Item 6: Another example of individual item alignment */
.item-6 {{
    grid-row: 2;
    grid-column: 5;
    background-color: #f7b731;
    justify-self: end;   /* Overrides default justify-items: stretch */
    align-self: start;   /* Overrides default align-items: stretch */
    width: 60px;
    height: 60px;
}}

/* Item 7 & 8: Implicitly added items, demonstrating grid-auto-rows */
.item-7 {{
    background-color: #83d475;
}}
.item-8 {{
    background-color: #6a0572;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1>{title_text}</h1>
    <p>{body_text}</p>
    <div class="container">
        <div class="item item-1">1</div>
        <div class="item item-2">2</div>
        <div class="item item-3">3</div>
        <div class="item item-4">4</div>
        <div class="item item-5">5</div>
        <div class="item item-6">6</div>
        <!-- Items 7 & 8 are outside the explicit 4x columns defined by items 1-6 above,
             demonstrating grid-auto-rows and auto-placement -->
        <div class="item item-7">7</div>
        <div class="item item-8">8</div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    # No JavaScript required for the core CSS Grid demonstration
    js = f"""// Dynamic CSS Grid Layout with Responsive Item Placement and Overlays — no JS needed for core functionality.
document.addEventListener('DOMContentLoaded', () => {{
    console.log('CSS Grid Demo Loaded');
    // You can inspect the grid using browser developer tools.
    // In Chrome/Firefox, select the .container element and click the 'grid' icon in the inspector to visualize the grid lines and areas.
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

