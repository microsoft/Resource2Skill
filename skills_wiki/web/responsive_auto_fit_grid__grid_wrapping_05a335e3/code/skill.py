import os

def create_component(
    output_dir: str,
    title_text: str = "Online Shop",
    product_items: list = None,
    color_scheme: str = "light",        # "dark" or "light"
    accent_color: str = "#4a148c",     # CSS hex color for accent
    width_px: int = 1200,              # Max width for the entire product list
    height_px: int = 800,              # Not directly used for grid item height, but for overall context (container min-height)
    min_column_width_px: int = 300,    # Minimum width for grid columns before wrapping
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the "Grid Wrapping" visual effect from the tutorial.

    Generates a responsive product grid that automatically adjusts column count based on viewport size.
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    os.makedirs(output_dir, exist_ok=True)

    if product_items is None:
        # Default product items with placeholder images
        product_items = [
            {"image": "https://via.placeholder.com/300x200/4070FF/ffffff?text=Blue+Shoes", "name": "Duramo SL 2.0", "price": "$56.00"},
            {"image": "https://via.placeholder.com/300x200/ffffff/000000?text=White+Nike", "name": "Air Force 1 '07", "price": "$119.00"},
            {"image": "https://via.placeholder.com/300x200/1a1a1a/ffffff?text=Black+Nike", "name": "Air Force 1 '07", "price": "$99.00"},
            {"image": "https://via.placeholder.com/300x200/f8f9fa/1a1a1a?text=White+Adidas", "name": "Advantage Base Court Lifestyle", "price": "$80.00"},
            {"image": "https://via.placeholder.com/300x200/ffffff/000000?text=White+Nike", "name": "Air Force 1 '07", "price": "$119.00"},
            {"image": "https://via.placeholder.com/300x200/1a1a1a/ffffff?text=Black+Nike", "name": "Air Force 1 '07", "price": "$99.00"},
            {"image": "https://via.placeholder.com/300x200/a0a0a0/ffffff?text=Grey+Nike", "name": "Air Max 97", "price": "$170.00"},
            {"image": "https://via.placeholder.com/300x200/1a1a1a/ffffff?text=Black+Nike", "name": "Air Max DN", "price": "$200.00"},
            {"image": "https://via.placeholder.com/300x200/4070FF/ffffff?text=Blue+Adidas", "name": "Duramo SL 2.0", "price": "$56.00"},
            {"image": "https://via.placeholder.com/300x200/ffffff/000000?text=White+Nike", "name": "Air Force 1 '07", "price": "$119.00"},
            {"image": "https://via.placeholder.com/300x200/1a1a1a/ffffff?text=Black+Nike", "name": "Air Force 1 '07", "price": "$99.00"},
            {"image": "https://via.placeholder.com/300x200/f8f9fa/1a1a1a?text=White+Adidas", "name": "Advantage Base Court Lifestyle", "price": "$80.00"},
        ]

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#1a1a1a"
        text_color = "#f0f0f0"
        header_bg = "#2a2a2a"
        card_bg = "#3a3a3a"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        header_bg = "#ffffff"
        card_bg = "#ffffff"

    # === CSS ===
    css = f"""
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

body {{
    font-family: 'Poppins', sans-serif;
    margin: 0;
    background-color: {bg_color};
    color: {text_color};
    min-height: {height_px}px; /* Added for general container sizing context */
}}

.online-shop-header {{
    background-color: {header_bg};
    padding: 1em 2em;
    border-bottom: 1px solid #eee;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}}

.online-shop-header h1 {{
    margin: 0;
    font-size: 1.5em;
    color: {text_color};
}}

.online-shop-nav ul {{
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    gap: 1.5em;
}}

.online-shop-nav a {{
    text-decoration: none;
    color: {text_color};
    font-weight: 500;
    transition: color 0.2s ease-in-out;
}}

.online-shop-nav a:hover {{
    color: {accent_color};
}}

.products-list {{
    display: grid;
    /* Core responsive grid wrapping: auto-fit as many columns as possible, 
       each column between min_column_width_px and 1 fraction of available space */
    grid-template-columns: repeat(auto-fit, minmax({min_column_width_px}px, 1fr));
    gap: 1.5em; /* Spacing between grid items */
    justify-content: center; /* Centers the entire grid if total column width is less than max-width */
    padding: 2em;
    max-width: {width_px}px; /* Constrains the overall width of the grid */
    margin: 0 auto; /* Centers the grid container on the page */
}}

.product {{
    background-color: {card_bg};
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    padding: 1em;
    display: flex;
    flex-direction: column;
    align-items: center; /* Centers items horizontally within the flex container */
    text-align: center; /* Centers text content */
    overflow: hidden; /* Ensures content respects border-radius */
    transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}}

.product:hover {{
    transform: translateY(-5px);
    box-shadow: 0 8px 16px rgba(0,0,0,0.1);
}}

.product img {{
    max-width: 100%;
    height: auto; /* Maintain aspect ratio */
    border-radius: 8px;
    margin-bottom: 1em;
}}

.product p {{
    font-weight: 600;
    margin: 0 0 0.5em 0;
    color: {text_color};
}}

.product span {{
    font-size: 1.1em;
    color: {accent_color};
    font-weight: 500;
}}
"""

    # Generate product HTML
    products_html = ""
    for product in product_items:
        products_html += f"""
        <div class="product">
            <img src="{product['image']}" alt="{product['name']}">
            <p>{product['name']}</p>
            <span>{product['price']}</span>
        </div>
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
    <header class="online-shop-header">
        <h1>{title_text}</h1>
        <nav class="online-shop-nav">
            <ul>
                <li><a href="#">Shoes</a></li>
                <li><a href="#">About</a></li>
                <li><a href="#">Login</a></li>
            </ul>
        </nav>
    </header>
    <main>
        <section class="products-list">
            {products_html}
        </section>
    </main>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript (empty for this specific effect) ===
    js = f"""// No JavaScript needed for this core responsive grid wrapping effect."""

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

