def create_component(
    output_dir: str,
    title_text: str = "Explore Our Collection",
    body_text: str = "A fully responsive, auto-wrapping grid utilizing CSS Grid stacking for perfect layer alignment.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#8b5cf6",     # CSS hex color for accent (e.g., Indigo)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Auto-Wrapping Bento Grid.
    """
    import os
    import json

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0f172a"          # Slate 900
        text_color = "#f8fafc"        # Slate 50
        text_muted = "#94a3b8"        # Slate 400
        card_bg = "#1e293b"           # Slate 800
        overlay_color = "rgba(15, 23, 42, 0.85)"
    else:
        bg_color = "#f8fafc"          # Slate 50
        text_color = "#0f172a"        # Slate 900
        text_muted = "#64748b"        # Slate 500
        card_bg = "#ffffff"           # White
        overlay_color = "rgba(0, 0, 0, 0.75)" # Dark overlay is still needed for white text over images

    # Card data to populate the grid
    cards = [
        {"title": "Air Max Pro", "price": "$120.00", "tag": "New", "img": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&q=80&w=800"},
        {"title": "Urban Classic", "price": "$95.00", "tag": "Bestseller", "img": "https://images.unsplash.com/photo-1507464098880-e367bc5d2c08?auto=format&fit=crop&q=80&w=800"},
        {"title": "Trail Runner", "price": "$140.00", "tag": "Outdoor", "img": "https://images.unsplash.com/photo-1511556532299-8f662fc26c06?auto=format&fit=crop&q=80&w=800"},
        {"title": "Minimalist V2", "price": "$85.00", "tag": "Sale", "img": "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?auto=format&fit=crop&q=80&w=800"},
        {"title": "Retro High", "price": "$110.00", "tag": "Limited", "img": "https://images.unsplash.com/photo-1551107696-a4b0c5a0d9a2?auto=format&fit=crop&q=80&w=800"},
        {"title": "Aero Glide", "price": "$135.00", "tag": "Performance", "img": "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?auto=format&fit=crop&q=80&w=800"}
    ]

    # Generate HTML for cards
    cards_html = ""
    for card in cards:
        cards_html += f"""
            <article class="grid-card hidden-initial">
                <img src="{card['img']}" alt="{card['title']}" class="card-img" loading="lazy">
                <div class="card-overlay"></div>
                <div class="card-content">
                    <span class="card-tag">{card['tag']}</span>
                    <div>
                        <h2 class="card-title">{card['title']}</h2>
                        <p class="card-price">{card['price']}</p>
                    </div>
                </div>
            </article>
        """

    # === CSS ===
    css = f"""/* Responsive Auto-Wrapping Grid generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --card-bg: {card_bg};
    --accent: {accent_color};
    --overlay: {overlay_color};
    --card-min-width: 300px;
    --card-height: 420px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    padding: 4rem 2rem;
    line-height: 1.5;
}}

.main-container {{
    width: 100%;
    max-width: {width_px}px;
}}

.header {{
    margin-bottom: 3rem;
    text-align: center;
}}

.header-title {{
    font-size: clamp(2rem, 4vw, 3rem);
    font-weight: 700;
    letter-spacing: -0.02em;
    margin-bottom: 1rem;
}}

.header-desc {{
    color: var(--text-muted);
    font-size: 1.125rem;
    max-width: 600px;
    margin: 0 auto;
}}

/* MACRO LAYOUT: The Auto-wrapping Grid */
.product-grid {{
    display: grid;
    /* Core Skill: Auto-wrapping layout without media queries */
    grid-template-columns: repeat(auto-fit, minmax(var(--card-min-width), 1fr));
    /* Core Skill: Keep generated rows a consistent height */
    grid-auto-rows: var(--card-height);
    gap: 2rem;
}}

/* MICRO LAYOUT: Individual Card Stacking */
.grid-card {{
    background: var(--card-bg);
    border-radius: 1.25rem;
    overflow: hidden;
    position: relative;
    cursor: pointer;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
    
    /* Core Skill: CSS Grid Stacking Context */
    display: grid;
    grid-template-areas: "stack";
}}

/* Assign ALL children to the exact same grid cell to stack them */
.grid-card > * {{
    grid-area: stack;
}}

/* 1. Base Layer: Image */
.card-img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}}

/* 2. Middle Layer: Gradient Overlay (for text readability) */
.card-overlay {{
    background: linear-gradient(to top, var(--overlay) 0%, transparent 60%);
    opacity: 0.8;
    transition: opacity 0.3s ease;
}}

/* 3. Top Layer: Text Content */
.card-content {{
    padding: 2rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    color: #ffffff; /* Always white over the dark overlay */
    z-index: 10;
}}

.card-tag {{
    align-self: flex-start;
    background: var(--accent);
    color: #ffffff;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 0.5rem 1rem;
    border-radius: 9999px;
    box-shadow: 0 4px 14px 0 rgba(0,0,0,0.2);
}}

.card-title {{
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 0.25rem;
    transform: translateY(10px);
    transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}}

.card-price {{
    font-size: 1.125rem;
    font-weight: 500;
    color: #cbd5e1;
    transform: translateY(10px);
    transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    transition-delay: 0.05s;
}}

/* Hover Dynamics */
.grid-card:hover .card-img {{
    transform: scale(1.08);
}}

.grid-card:hover .card-overlay {{
    opacity: 1;
}}

.grid-card:hover .card-title,
.grid-card:hover .card-price {{
    transform: translateY(0);
}}

/* JS Animation States */
.hidden-initial {{
    opacity: 0;
    transform: translateY(30px);
}}

.reveal-animate {{
    opacity: 1;
    transform: translateY(0);
    transition: opacity 0.8s ease, transform 0.8s cubic-bezier(0.16, 1, 0.3, 1);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="main-container">
        <header class="header">
            <h1 class="header-title">{title_text}</h1>
            <p class="header-desc">{body_text}</p>
        </header>
        
        <section class="product-grid" aria-label="Product Showcase">
            {cards_html}
        </section>
    </main>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Intersection Observer for Staggered Load Animation
document.addEventListener('DOMContentLoaded', () => {{
    const cards = document.querySelectorAll('.grid-card');
    
    // Observer options
    const observerOptions = {{
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    }};

    // Observer callback
    const observerCallback = (entries, observer) => {{
        entries.forEach((entry, index) => {{
            if (entry.isIntersecting) {{
                // Stagger the animations based on index
                setTimeout(() => {{
                    entry.target.classList.remove('hidden-initial');
                    entry.target.classList.add('reveal-animate');
                }}, index * 100); // 100ms stagger between cards
                
                // Unobserve after revealing
                observer.unobserve(entry.target);
            }}
        }});
    }};

    const observer = new IntersectionObserver(observerCallback, observerOptions);

    // Observe all cards
    cards.forEach(card => {{
        observer.observe(card);
    }});
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
