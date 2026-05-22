def create_component(
    output_dir: str,
    title_text: str = "Discover Our Collection",
    body_text: str = "A fluid bento grid demonstrating native CSS Grid wrapping and stacking without media queries.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#6366f1",     # CSS hex color for accent (e.g., Indigo)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Bento Grid & Grid Stacking Card effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_color = "#f8fafc"
        card_bg = "#1e293b"
        border_color = "rgba(255,255,255,0.1)"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        card_bg = "#ffffff"
        border_color = "rgba(0,0,0,0.1)"

    css = f"""/* Bento Grid & Card Stacking — Generated Component */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --card-bg: {card_bg};
    --accent-color: {accent_color};
    --border-color: {border_color};
    --container-width: {width_px}px;
    --min-col-width: 300px;
    --gap-size: 1.5rem;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    display: grid;
    place-items: center;
    padding: 2rem;
}}

.page-wrapper {{
    width: 100%;
    max-width: var(--container-width);
    display: flex;
    flex-direction: column;
    gap: 2rem;
}}

.header {{
    text-align: center;
    margin-bottom: 1rem;
}}

.header h1 {{
    font-size: clamp(2rem, 4vw, 3.5rem);
    font-weight: 700;
    letter-spacing: -0.02em;
    margin-bottom: 0.5rem;
}}

.header p {{
    color: var(--text-color);
    opacity: 0.7;
    font-size: 1.1rem;
    max-width: 600px;
    margin: 0 auto;
}}

/* == GRID WRAPPING: The Bento Gallery Macro-Layout == */
.bento-grid {{
    display: grid;
    /* The magic formula for responsive grids without media queries */
    grid-template-columns: repeat(auto-fit, minmax(min(100%, var(--min-col-width)), 1fr));
    gap: var(--gap-size);
    width: 100%;
}}

/* == GRID STACKING: The Individual Card Micro-Layout == */
.bento-card {{
    display: grid;
    /* Create a single named grid area that everything will share */
    grid-template-areas: "stack";
    background-color: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 1.25rem;
    overflow: hidden;
    aspect-ratio: 4 / 5;
    cursor: pointer;
    box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.2);
    transition: box-shadow 0.3s ease, transform 0.3s ease;
}}

.bento-card:hover {{
    box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.4);
    transform: translateY(-4px);
}}

/* Place the image in the 'stack' area */
.bento-card img {{
    grid-area: stack;
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}}

.bento-card:hover img {{
    transform: scale(1.08);
}}

/* Place the content in the exact same 'stack' area, layering it on top */
.bento-content {{
    grid-area: stack;
    z-index: 1; /* Ensure it stays above the image */
    display: grid;
    /* Align content to the bottom (end) of the card */
    place-content: end start;
    padding: 1.5rem;
    /* Linear gradient ensures text contrast regardless of the image */
    background: linear-gradient(
        to top, 
        rgba(0, 0, 0, 0.9) 0%, 
        rgba(0, 0, 0, 0.4) 50%, 
        transparent 100%
    );
    color: white; /* Force white text over images for contrast */
}}

.card-tag {{
    background-color: var(--accent-color);
    color: #fff;
    padding: 0.25rem 0.75rem;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.75rem;
    width: max-content;
}}

.bento-content h3 {{
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    line-height: 1.2;
    transform: translateY(10px);
    transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}}

.bento-content p {{
    font-size: 0.95rem;
    opacity: 0.8;
    line-height: 1.4;
    transform: translateY(10px);
    transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}}

.bento-card:hover .bento-content h3,
.bento-card:hover .bento-content p {{
    transform: translateY(0);
}}

/* Allow spanning across columns if there's enough space (optional flair) */
@media (min-width: 650px) {{
    .bento-card.wide {{
        grid-column: span 2;
        aspect-ratio: 16 / 9;
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="page-wrapper">
        <header class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>

        <!-- Bento Grid Container -->
        <main class="bento-grid" id="grid-container">
            <!-- Cards will be populated by JavaScript -->
        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Bento Grid - Content Generation
document.addEventListener('DOMContentLoaded', () => {{
    const gridContainer = document.getElementById('grid-container');
    
    // Sample data to populate the grid
    const cardsData = [
        {{
            title: "Dynamic Layouts",
            desc: "Grid wrapping effortlessly recalculates columns as the viewport scales.",
            tag: "CSS Grid",
            img: "https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=800&q=80",
            wide: true
        }},
        {{
            title: "Layered Depth",
            desc: "No more position absolute. Stack elements in the same grid cell.",
            tag: "Architecture",
            img: "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=600&q=80",
            wide: false
        }},
        {{
            title: "Performance First",
            desc: "Hardware accelerated transitions keep interactions silky smooth.",
            tag: "Optimization",
            img: "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=600&q=80",
            wide: false
        }},
        {{
            title: "Visual Stability",
            desc: "Using 'min(100%, width)' prevents horizontal scrolling on small devices.",
            tag: "Mobile",
            img: "https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?auto=format&fit=crop&w=600&q=80",
            wide: false
        }},
        {{
            title: "Implicit Flow",
            desc: "Add as many items as you want; the grid automatically generates rows.",
            tag: "Scalable",
            img: "https://images.unsplash.com/photo-1558655146-d09347e92766?auto=format&fit=crop&w=600&q=80",
            wide: false
        }}
    ];

    // Generate cards
    cardsData.forEach(card => {{
        const article = document.createElement('article');
        article.className = `bento-card ${{card.wide ? 'wide' : ''}}`;
        
        article.innerHTML = `
            <img src="${{card.img}}" alt="${{card.title}}" loading="lazy">
            <div class="bento-content">
                <span class="card-tag">${{card.tag}}</span>
                <h3>${{card.title}}</h3>
                <p>${{card.desc}}</p>
            </div>
        `;
        
        gridContainer.appendChild(article);
    }});
}});
"""

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
