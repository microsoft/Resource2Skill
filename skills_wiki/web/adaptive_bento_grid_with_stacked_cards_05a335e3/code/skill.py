def create_component(
    output_dir: str,
    title_text: str = "Discover Our Collection",
    body_text: str = "Explore our responsive bento gallery built entirely with modern CSS Grid.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#6366f1",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Adaptive Bento Grid with Stacked Cards visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Theme Configuration ===
    if color_scheme == "dark":
        bg_color = "#0f111a"
        text_color = "#f8f9fa"
        surface_color = "rgba(255, 255, 255, 0.05)"
        border_color = "rgba(255, 255, 255, 0.1)"
    else:
        bg_color = "#f4f5f7"
        text_color = "#111827"
        surface_color = "#ffffff"
        border_color = "rgba(0, 0, 0, 0.1)"

    # === CSS ===
    css = f"""/* Adaptive Bento Grid Component */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --accent-color: {accent_color};
    --surface-color: {surface_color};
    --border-color: {border_color};
    --container-width: {width_px}px;
    --container-height: {height_px}px;
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
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 3rem 1.5rem;
}}

header {{
    text-align: center;
    max-width: 800px;
    margin-bottom: 3rem;
}}

h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    letter-spacing: -0.02em;
}}

p.subtitle {{
    font-size: 1.125rem;
    opacity: 0.8;
    line-height: 1.6;
}}

/* Outer Grid System: Fluid Auto-fitting */
.bento-grid {{
    display: grid;
    /* The magic formula for responsive grids without media queries */
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    grid-auto-rows: 320px;
    gap: 1.5rem;
    width: 100%;
    max-width: var(--container-width);
}}

/* Inner Grid System: Grid Stacking */
.bento-card {{
    display: grid;
    grid-template-areas: "stack";
    border-radius: 16px;
    overflow: hidden;
    background-color: var(--surface-color);
    border: 1px solid var(--border-color);
    text-decoration: none;
    cursor: pointer;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
    transition: box-shadow 0.3s ease, transform 0.3s ease;
}}

.bento-card:hover {{
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
    transform: translateY(-4px);
}}

/* Assign all direct children to the same grid cell */
.bento-card > * {{
    grid-area: stack;
}}

.bento-card .card-bg {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    z-index: 1;
    transition: transform 0.5s cubic-bezier(0.33, 1, 0.68, 1);
}}

.bento-card:hover .card-bg {{
    transform: scale(1.08);
}}

.bento-card .card-overlay {{
    z-index: 2;
    background: linear-gradient(to top, rgba(0, 0, 0, 0.85) 0%, rgba(0, 0, 0, 0.3) 50%, transparent 100%);
    opacity: 0.8;
    transition: opacity 0.3s ease;
}}

.bento-card:hover .card-overlay {{
    opacity: 1;
}}

.bento-card .card-content {{
    z-index: 3;
    /* Push content to the bottom of the cell */
    align-self: end; 
    padding: 1.5rem;
    color: #ffffff; /* Always light to contrast with dark overlay */
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}}

.card-tag {{
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--accent-color);
}}

.card-title {{
    font-size: 1.25rem;
    font-weight: 600;
    margin: 0;
}}

.card-price {{
    font-size: 1rem;
    font-weight: 400;
    opacity: 0.9;
}}

/* Feature the first item to create a Bento look on larger screens */
@media (min-width: 650px) {{
    .bento-card.featured {{
        grid-column: span 2;
        grid-row: span 2;
    }}
    
    .bento-card.featured .card-title {{
        font-size: 2rem;
    }}
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
    <header>
        <h1>{title_text}</h1>
        <p class="subtitle">{body_text}</p>
    </header>

    <main class="bento-grid" id="grid-container">
        <!-- Grid items will be injected by JavaScript -->
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Bento Grid Data and Generation
document.addEventListener('DOMContentLoaded', () => {
    const gridContainer = document.getElementById('grid-container');

    // Sample data to populate the grid
    const products = [
        {
            title: "Air Max Infinity",
            tag: "New Arrival",
            price: "$150.00",
            img: "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=800&q=80",
            featured: true
        },
        {
            title: "Urban Runner",
            tag: "Bestseller",
            price: "$120.00",
            img: "https://images.unsplash.com/photo-1511556532299-8f662fc26c06?auto=format&fit=crop&w=600&q=80",
            featured: false
        },
        {
            title: "Trail Blazer X",
            tag: "Outdoor",
            price: "$180.00",
            img: "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?auto=format&fit=crop&w=600&q=80",
            featured: false
        },
        {
            title: "Street Classic",
            tag: "Lifestyle",
            price: "$95.00",
            img: "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?auto=format&fit=crop&w=600&q=80",
            featured: false
        },
        {
            title: "Velocity Zoom",
            tag: "Running",
            price: "$140.00",
            img: "https://images.unsplash.com/photo-1491553895911-0055eca6402d?auto=format&fit=crop&w=600&q=80",
            featured: false
        }
    ];

    // Function to generate the HTML for a single stacked grid card
    const createCard = (product, index) => {
        const isFeatured = product.featured ? 'featured' : '';
        
        // The card acts as the stack wrapper.
        // Elements inside it automatically overlap via 'grid-area: stack' in CSS.
        return `
            <a href="#" class="bento-card ${isFeatured}" style="animation: fadeUp 0.5s ease backwards ${(index * 0.1)}s;">
                <img src="${product.img}" alt="${product.title}" class="card-bg">
                <div class="card-overlay"></div>
                <div class="card-content">
                    <span class="card-tag">${product.tag}</span>
                    <h2 class="card-title">${product.title}</h2>
                    <span class="card-price">${product.price}</span>
                </div>
            </a>
        `;
    };

    // Inject cards into the container
    gridContainer.innerHTML = products.map(createCard).join('');
});

// Add simple CSS animation for entry
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
`;
document.head.appendChild(style);
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
