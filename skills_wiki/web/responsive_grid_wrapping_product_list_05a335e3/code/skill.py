import os

def create_component(
    output_dir: str,
    title_text: str = "Online Shop",
    num_products: int = 12,
    product_min_width_px: int = 250, # Minimum width for grid columns, matches video example
    grid_gap_em: float = 1.0,        # Gap between grid items
    color_scheme: str = "light",     # "dark" or "light"
    accent_color: str = "#0071ff",   # CSS hex color for elements like button or hover
    width_px: int = 1200,            # Outer container width for main content
    height_px: int = 800,            # Outer container height (min-height generally better for main content)
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Grid Wrapping Product List visual effect.

    Utilizes CSS Grid's repeat(auto-fit, minmax(min_size, 1fr)) to create flexible and adaptive columns.
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#1a1a1a"
        text_color = "#f0f0f0"
        surface_color = "#2a2a2a" # Used for generic surfaces or background of items
        item_bg = "#4a4a4a"
        header_bg = "#333333"
    else: # light theme
        bg_color = "#f0f0f0"
        text_color = "#1a1a1a"
        surface_color = "#ffffff"
        item_bg = "#ffffff"
        header_bg = "#eeeeee"

    # === HTML for product items ===
    product_items_html = ""
    for i in range(1, num_products + 1):
        # Placeholder image URL uses item_bg and text_color for theme consistency
        img_placeholder_color = item_bg.lstrip('#')
        img_text_color = text_color.lstrip('#')
        product_items_html += f"""
        <div class="product">
            <img src="https://via.placeholder.com/{product_min_width_px}x200/{img_placeholder_color}/{img_text_color}?text=Item+{i}" alt="Item {i}">
            <p>Item {i}</p>
            <span>$ {i * 10}.00</span>
        </div>"""

    # === CSS ===
    css = f"""
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', sans-serif;
    background-color: {bg_color};
    color: {text_color};
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center; /* Center content horizontally if main is narrower than body */
}}

header {{
    width: 100%;
    background-color: {header_bg};
    padding: 1em 2em;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(0,0,0,0.05);
}}

header h1 {{
    font-size: 1.8em;
    margin: 0;
    color: {accent_color};
    font-weight: 700;
}}

nav ul {{
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
}}

nav ul li {{
    margin-left: 1.5em;
}}

nav ul li a {{
    text-decoration: none;
    color: {text_color};
    font-weight: 600;
    transition: color 0.3s ease;
}}

nav ul li a:hover {{
    color: {accent_color};
}}

main {{
    padding: 2em;
    width: 100%;
    max-width: {width_px}px; /* Constrain main content width for larger screens */
}}

.products-list {{
    display: grid;
    /* Core Grid Wrapping logic:
       auto-fit: automatically creates columns to fill space
       minmax(product_min_width_px, 1fr): columns are at least product_min_width_px and grow proportionally
    */
    grid-template-columns: repeat(auto-fit, minmax({product_min_width_px}px, 1fr));
    gap: {grid_gap_em}em;
    justify-content: center; /* Centers grid items within the tracks, if they don't fill completely */
    margin: 0 auto; /* Centers the grid itself within the main element if it's narrower */
}}

.product {{
    background-color: {item_bg};
    border-radius: 8px;
    padding: 1.5em;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}

.product:hover {{
    transform: translateY(-5px);
    box-shadow: 0 6px 12px rgba(0,0,0,0.15);
}}

.product img {{
    max-width: 100%;
    height: auto; /* Maintain aspect ratio */
    border-radius: 4px;
    margin-bottom: 1em;
}}

.product p {{
    font-weight: 600;
    font-size: 1.1em;
    margin-bottom: 0.5em;
}}

.product span {{
    font-size: 1em;
    font-weight: 600;
    color: {accent_color};
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>{title_text}</h1>
        <nav>
            <ul>
                <li><a href="#">Shoes</a></li>
                <li><a href="#">About</a></li>
                <li><a href="#">Login</a></li>
            </ul>
        </nav>
    </header>
    <main>
        <div class="products-list">
            {product_items_html}
        </div>
    </main>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript (empty for this example, as responsiveness is CSS-driven) ===
    js = """// No JavaScript needed for the core responsive grid wrapping effect in this example."""

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

