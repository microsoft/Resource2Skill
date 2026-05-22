def create_component(
    output_dir: str,
    title_text: str = "Online Shop",
    body_text: str = "", # Not directly used in this specific component's main layout
    color_scheme: str = "light",        # "dark" or "light"
    accent_color: str = "#4f46e5",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800, # Not directly used for grid height, grid height adapts to content
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Grid Wrapping visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#1a1a2e"
        text_color = "#f0f0f0"
        card_bg_color = "#2a2a4a"
        border_color = "rgba(255, 255, 255, 0.1)"
    else: # light theme as shown in the online shop example in the video
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        card_bg_color = "#ffffff"
        border_color = "rgba(0, 0, 0, 0.1)"

    # Product data for demonstration (images are placeholders)
    products = [
        {"image": "https://via.placeholder.com/300x200/4f46e5/ffffff?text=Product+1", "name": "Duramo SL 2.0", "price": "$56.00"},
        {"image": "https://via.placeholder.com/300x200/ffffff/000000?text=Product+2", "name": "Air Force 1 '07", "price": "$110.00"},
        {"image": "https://via.placeholder.com/300x200/1a1a2e/ffffff?text=Product+3", "name": "Air Force 1 '07", "price": "$99.00"},
        {"image": "https://via.placeholder.com/300x200/ffffff/000000?text=Product+4", "name": "Advantage Base Court Lifestyle", "price": "$80.00"},
        {"image": "https://via.placeholder.com/300x200/ffffff/000000?text=Product+5", "name": "Air Force 1 '07", "price": "$99.00"},
        {"image": "https://via.placeholder.com/300x200/1a1a2e/ffffff?text=Product+6", "name": "Air Force 1 '07", "price": "$99.00"},
        {"image": "https://via.placeholder.com/300x200/4f46e5/ffffff?text=Product+7", "name": "Air Max DN", "price": "$170.00"},
        {"image": "https://via.placeholder.com/300x200/1a1a2e/ffffff?text=Product+8", "name": "Air Max Plus 3", "price": "$200.00"},
        {"image": "https://via.placeholder.com/300x200/4f46e5/ffffff?text=Product+9", "name": "Air Max 97", "price": "$180.00"},
        {"image": "https://via.placeholder.com/300x200/ffffff/000000?text=Product+10", "name": "Air Max Plus", "price": "$190.00"},
        {"image": "https://via.placeholder.com/300x200/1a1a2e/ffffff?text=Product+11", "name": "Campus 00s", "price": "$95.00"},
        {"image": "https://via.placeholder.com/300x200/4f46e5/ffffff?text=Product+12", "name": "Air Max Plus Utility", "price": "$185.00"},
    ]

    product_html_items = ""
    for product in products:
        product_html_items += f"""
            <div class="product">
                <img src="{product['image']}" alt="{product['name']}" height="200">
                <p class="product-name">{product['name']}</p>
                <span class="product-price">{product['price']}</span>
            </div>
        """

    # === CSS ===
    css = f"""/* Responsive Grid Wrapping for Dynamic Content — generated component */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --card-bg: {card_bg_color};
    --border-color: {border_color};
    --container-width: {width_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    padding: 20px;
}}

.online-shop-wrapper {{
    width: min(var(--container-width), 100%); /* Max width for the whole shop content */
    background: var(--bg);
    padding: 20px 0;
    display: flex;
    flex-direction: column;
    align-items: center;
}}

.header-nav {{
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 20px;
    border-bottom: 1px solid var(--border-color);
    margin-bottom: 20px;
}}

.header-nav h1 {{
    font-size: 1.5rem;
    font-weight: 600;
}}

.nav-links a {{
    color: var(--text);
    text-decoration: none;
    margin-left: 20px;
    font-weight: 500;
}}

.products-list {{
    display: grid;
    /* Core responsive wrapping grid logic */
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px; /* Gap between grid items */
    justify-content: center; /* Center the grid within its container if items don't fill full width */
    width: 100%;
}}

.product {{
    background: var(--card-bg);
    border-radius: 10px;
    padding: 16px;
    display: flex;
    flex-direction: column;
    align-items: center; /* Center content within product card */
    text-align: center;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
    transition: transform 0.2s ease-in-out;
}}

.product:hover {{
    transform: translateY(-5px);
}}

.product img {{
    max-width: 100%;
    height: auto; /* Allow image height to adapt while maintaining aspect ratio */
    border-radius: 8px;
    margin-bottom: 10px;
}}

.product-name {{
    font-weight: 600;
    margin-bottom: 5px;
    font-size: 1rem;
    color: var(--text);
}}

.product-price {{
    font-weight: 500;
    font-size: 0.9rem;
    color: var(--accent);
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
    <div class="online-shop-wrapper">
        <header class="header-nav">
            <h1>{title_text}</h1>
            <nav class="nav-links">
                <a href="#">Shoes</a>
                <a href="#">About</a>
                <a href="#">Login</a>
            </nav>
        </header>
        <div class="products-list">
            {product_html_items}
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Grid Wrapping for Dynamic Content — no explicit JS interaction for this component
document.addEventListener('DOMContentLoaded', () => {{
    // No specific JavaScript needed for the core responsive grid wrapping effect.
    // CSS handles all the layout and responsiveness.
    console.log("Responsive Grid Wrapping component loaded.");
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

