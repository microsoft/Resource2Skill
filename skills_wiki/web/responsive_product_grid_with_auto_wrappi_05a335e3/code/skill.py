import os

def create_component(
    output_dir: str,
    title_text: str = "Online Shop",
    body_text: str = "", # Not directly used in the product list, but kept for consistency
    color_scheme: str = "light",        # "dark" or "light"
    accent_color: str = "#0071ff",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800, # This height is primarily for the viewport in testing
    min_item_width_px: int = 280,
    grid_gap_rem: float = 1.0,
    num_products: int = 12,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Product Grid with Auto-Wrapping Columns visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#121212"
        text_color = "#e0e0e0"
        product_bg_color = "#1e1e1e"
        border_color = "rgba(255, 255, 255, 0.1)"
        box_shadow_color = "rgba(0, 0, 0, 0.3)"
    else:
        bg_color = "#f8f8f8"
        text_color = "#333333"
        product_bg_color = "#ffffff"
        border_color = "rgba(0, 0, 0, 0.1)"
        box_shadow_color = "rgba(0, 0, 0, 0.05)"

    # === Product Data (Examples) ===
    products_data = [
        {"name": "Duramo SL 2.0", "price": "$56.00", "image_url": "https://images.unsplash.com/photo-1595341888075-ef0cdb1a6462?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNTY3MHwwfDF8c2VhcmNofDh8fHNuZWFrZXJzJTIwbmlrZXxlbnwwfHx8fDE2OTk3Nzc5Nzd8MA&ixlib=rb-4.0.3&q=80&w=400"},
        {"name": "Air Force 1 '07", "price": "$110.00", "image_url": "https://images.unsplash.com/photo-1595950653106-aa11b846f17d?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNTY3MHwwfDF8c2VhcmNofDV8fHNuZWFrZXJzJTIwbmlrZXxlbnwwfHx8fDE2OTk3Nzc5Nzd8MA&ixlib=rb-4.0.3&q=80&w=400"},
        {"name": "Air Force 1 '07", "price": "$99.00", "image_url": "https://images.unsplash.com/photo-1595341888075-ef0cdb1a6462?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNTY3MHwwfDF8c2VhcmNofDh8fHNuZWFrZXJzJTIwbmlrZXxlbnwwfHx8fDE2OTk3Nzc5Nzd8MA&ixlib=rb-4.0.3&q=80&w=400"},
        {"name": "Advantage Base Court Lifestyle", "price": "$80.00", "image_url": "https://images.unsplash.com/photo-1628310892010-85f61765c71d?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNTY3MHwwfDF8c2VhcmNofDF8fHNuZWFrZXJzJTIwYWRpZGFzJTIwd2hpdGV8ZW58MHx8fHwxNjk5Nzc5OTI1fDA&ixlib=rb-4.0.3&q=80&w=400"},
        {"name": "Air Force 1 '07", "price": "$89.00", "image_url": "https://images.unsplash.com/photo-1595341888075-ef0cdb1a6462?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNTY3MHwwfDF8c2VhcmNofDh8fHNuZWFrZXJzJTIwbmlrZXxlbnwwfHx8fDE2OTk3Nzc5Nzd8MA&ixlib=rb-4.0.3&q=80&w=400"},
        {"name": "Air Max DN", "price": "$170.00", "image_url": "https://images.unsplash.com/photo-1698263177726-3023f03b87d2?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNTY3MHwwfDF8c2VhcmNofDEzfHJuZHQlMjBzbmVha2Vyc3xlbnwwfHx8fDE3MDYyMjk0MjN8MA&ixlib=rb-4.0.3&q=80&w=400"},
        {"name": "Air Max Plus 3", "price": "$200.00", "image_url": "https://images.unsplash.com/photo-1606526131484-9c5950d26859?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNTY3MHwwfDF8c2VhcmNofDE5fHJuZHQlMjBzbmVha2Vyc3xlbnwwfHx8fDE3MDYyMjk0MjN8MA&ixlib=rb-4.0.3&q=80&w=400"},
        {"name": "Air Max Plus", "price": "$190.00", "image_url": "https://images.unsplash.com/photo-1600185365483-26d7a4cc7519?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNTY3MHwwfDF8c2VhcmNofDEyfHJuZHQlMjBzbmVha2Vyc3xlbnwwfHx8fDE3MDYyMjk0MjN8MA&ixlib=rb-4.0.3&q=80&w=400"},
        {"name": "Air Force 1 '07", "price": "$99.00", "image_url": "https://images.unsplash.com/photo-1595341888075-ef0cdb1a6462?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNTY3MHwwfDF8c2VhcmNofDh8fHNuZWFrZXJzJTIwbmlrZXxlbnwwfHx8fDE2OTk3Nzc5Nzd8MA&ixlib=rb-4.0.3&q=80&w=400"},
        {"name": "Air Max 97", "price": "$180.00", "image_url": "https://images.unsplash.com/photo-1600185365483-26d7a4cc7519?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNTY3MHwwfDF8c2VhcmNofDEyfHJuZHQlMjBzbmVha2Vyc3xlbnwwfHx8fDE3MDYyMjk0MjN8MA&ixlib=rb-4.0.3&q=80&w=400"},
        {"name": "Campus 00s", "price": "$95.00", "image_url": "https://images.unsplash.com/photo-1632289657518-e37452d3ff30?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNTY3MHwwfDF8c2VhcmNofDIyfHNuZWFrZXJzJTIwYWRpZGFzfGVufDB8fHx8MTY5OTc3OTkyNXww&ixlib=rb-4.0.3&q=80&w=400"},
        {"name": "Air Force 1 '07", "price": "$110.00", "image_url": "https://images.unsplash.com/photo-1595950653106-aa11b846f17d?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNTY3MHwwfDF8c2VhcmNofDV8fHNuZWFrZXJzJTIwbmlrZXxlbnwwfHx8fDE2OTk3Nzc5Nzd8MA&ixlib=rb-4.0.3&q=80&w=400"},
    ]
    
    # Trim products_data to num_products
    products_data = products_data[:num_products]

    products_html = ""
    for product in products_data:
        products_html += f"""
        <div class="product">
            <img src="{product['image_url']}" alt="{product['name']}" height="300">
            <p>{product['name']}</p>
            <span>{product['price']}</span>
        </div>
        """

    # === CSS ===
    css = f"""
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --product-bg: {product_bg_color};
    --border-color: {border_color};
    --box-shadow-color: {box_shadow_color};
    --accent: {accent_color};
    --min-item-width: {min_item_width_px}px;
    --grid-gap: {grid_gap_rem}rem;
}}

body {{
    font-family: 'Inter', sans-serif;
    background-color: var(--bg);
    color: var(--text);
    margin: 0;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    padding: 20px; /* Add some padding around the entire shop */
}}

.online-shop-wrapper {{
    max-width: {width_px}px; /* Constrain overall width */
    margin: 0 auto;
    padding: 20px;
    border-radius: 8px;
    background-color: var(--product-bg); /* Use product bg for main wrapper to match tutorial */
}}

.products-list {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(var(--min-item-width), 1fr));
    gap: var(--grid-gap);
    justify-content: center; /* Centers the grid if it doesn't fill the entire width */
    padding: var(--grid-gap); /* Padding around the grid items */
}}

.product {{
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: var(--product-bg);
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid var(--border-color);
    box-shadow: 0 2px 4px var(--box-shadow-color);
    text-align: center;
    transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}}

.product:hover {{
    transform: translateY(-5px);
    box-shadow: 0 4px 8px var(--box-shadow-color);
}}

.product img {{
    max-width: 100%;
    height: 200px; /* Fixed height for image area */
    object-fit: contain; /* Ensure entire image is visible */
    border-radius: 4px;
    margin-bottom: 0.8rem;
}}

.product p {{
    font-weight: 600;
    font-size: 1.1em;
    margin-bottom: 0.4rem;
    line-height: 1.3;
}}

.product span {{
    font-weight: 500;
    font-size: 1em;
    color: var(--text);
}}

/* Top navigation/header */
.header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 1.5rem;
    background-color: var(--product-bg);
    border-bottom: 1px solid var(--border-color);
    margin-bottom: var(--grid-gap);
    border-radius: 8px;
    box-shadow: 0 1px 3px var(--box-shadow-color);
}}

.shop-title {{
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text);
}}

.nav-links a {{
    color: var(--text);
    text-decoration: none;
    margin-left: 1.5rem;
    font-weight: 500;
    transition: color 0.2s ease-in-out;
}}

.nav-links a:hover {{
    color: var(--accent);
}}

/* Basic search bar styling */
.search-bar {{
    width: 80%;
    max-width: 600px;
    margin: 1rem auto 2rem auto;
    padding: 0.8rem;
    border: 1px solid var(--border-color);
    border-radius: 25px;
    font-size: 1rem;
    color: var(--text);
    background-color: var(--product-bg);
    box-shadow: 0 1px 3px var(--box-shadow-color);
    outline: none;
    transition: border-color 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}}

.search-bar:focus {{
    border-color: var(--accent);
    box-shadow: 0 0 0 3px rgba(var(--accent-rgb, 0, 113, 255), 0.2);
}}

/* Set accent-rgb for rgba conversion in JS if needed */
:root {{
    --accent-rgb: {int(accent_color[1:3], 16)}, {int(accent_color[3:5], 16)}, {int(accent_color[5:7], 16)};
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
        <header class="header">
            <div class="shop-title">{title_text}</div>
            <nav class="nav-links">
                <a href="#">Shoes</a>
                <a href="#">About</a>
                <a href="#">Login</a>
            </nav>
        </header>

        <input type="text" class="search-bar" placeholder="Search for products...">

        <div class="products-list">
            {products_html}
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript (empty for this pattern, as responsiveness is CSS-driven) ===
    js = """// This pattern is primarily driven by CSS for its responsive layout.
// No specific JavaScript is required for the auto-wrapping grid itself.
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
