def create_component(
    output_dir: str,
    title_text: str = "Explore Our Collection",
    body_text: str = "A responsive Bento grid demonstrating auto-fit wrapping and pure CSS grid stacking.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#6366f1",     # CSS hex color for accent (e.g., Indigo)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Bento Grid and Grid Stacking visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#0b0f19"
        text_color = "#f3f4f6"
        text_muted = "#9ca3af"
        surface_color = "#1f2937"
        overlay_gradient = "linear-gradient(to top, rgba(11, 15, 25, 0.95) 0%, rgba(11, 15, 25, 0.4) 50%, rgba(11, 15, 25, 0) 100%)"
        shadow = "0 20px 25px -5px rgba(0, 0, 0, 0.5), 0 10px 10px -5px rgba(0, 0, 0, 0.2)"
        shadow_hover = "0 25px 50px -12px rgba(0, 0, 0, 0.7)"
    else:
        bg_color = "#f9fafb"
        text_color = "#111827"
        text_muted = "#4b5563"
        surface_color = "#ffffff"
        overlay_gradient = "linear-gradient(to top, rgba(255, 255, 255, 0.95) 0%, rgba(255, 255, 255, 0.6) 50%, rgba(255, 255, 255, 0) 100%)"
        shadow = "0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.025)"
        shadow_hover = "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)"

    # === CSS ===
    css = f"""/* Responsive Bento Grid & Grid Stacking */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --surface: {surface_color};
    --overlay: {overlay_gradient};
    --shadow: {shadow};
    --shadow-hover: {shadow_hover};
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    padding: 2rem;
    line-height: 1.5;
}}

/* Bounding wrapper for the demo environment */
.main-wrapper {{
    width: 100%;
    max-width: {width_px}px;
    /* Height is dynamic based on content, but min-height ensures it fills the requested area */
    min-height: {height_px}px;
    display: flex;
    flex-direction: column;
    gap: 3rem;
}}

.header-section {{
    text-align: center;
    max-width: 600px;
    margin: 0 auto;
}}

.header-section h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -0.025em;
    margin-bottom: 1rem;
}}

.header-section p {{
    color: var(--text-muted);
    font-size: 1.125rem;
}}

/* 
  === THE MAGIC: GRID WRAPPING ===
  auto-fit: Creates as many columns as will fit.
  minmax(300px, 1fr): Each column must be at least 300px. If there's extra space, they grow equally.
*/
.bento-grid {{
    display: grid;
    gap: 1.5rem;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    width: 100%;
}}

/* 
  === THE MAGIC: GRID STACKING ===
  The card is a grid. All direct children are placed in row 1, column 1.
  This stacks them like layers in Photoshop without using position: absolute.
*/
.bento-card {{
    display: grid;
    border-radius: 1rem;
    overflow: hidden;
    background: var(--surface);
    box-shadow: var(--shadow);
    text-decoration: none;
    color: var(--text);
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s ease;
    cursor: pointer;
    opacity: 0;
    transform: translateY(20px);
    
    /* Give cards a baseline height, but allow them to grow if text is long */
    min-height: 380px; 
}}

/* Assign all children to the same grid cell */
.bento-card > * {{
    grid-area: 1 / 1 / -1 / -1;
}}

.bento-card:hover {{
    transform: translateY(-8px);
    box-shadow: var(--shadow-hover);
}}

/* Layer 1: Background Image */
.card-img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    z-index: 1;
    transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}}

.bento-card:hover .card-img {{
    transform: scale(1.08);
}}

/* Layer 2: Gradient Overlay (for text readability) */
.card-overlay {{
    z-index: 2;
    background: var(--overlay);
    width: 100%;
    height: 100%;
}}

/* Layer 3: Text Content */
.card-content {{
    z-index: 3;
    padding: 1.5rem;
    /* Pushes content to the bottom of the grid cell */
    align-self: end; 
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}}

.card-tag {{
    align-self: flex-start;
    background: var(--accent);
    color: #ffffff;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    margin-bottom: 0.5rem;
}}

.card-title {{
    font-size: 1.5rem;
    font-weight: 700;
    line-height: 1.2;
}}

.card-desc {{
    color: var(--text-muted);
    font-size: 0.95rem;
    line-height: 1.4;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}}

/* JS Animation Class */
.bento-card.is-visible {{
    opacity: 1;
    transform: translateY(0);
}}
"""

    # Generate Card HTML dynamically
    cards_html = ""
    placeholders = [
        {"tag": "New", "title": "Nike Air Max Pro", "desc": "Lightweight mesh upper with responsive cushioning for all-day comfort."},
        {"tag": "Trending", "title": "Ultra Boost Lifestyle", "desc": "Sleek, modern design meeting everyday utility and supreme energy return."},
        {"tag": "Limited", "title": "Phantom Run V2", "desc": "Laceless flyknit architecture providing a secure, sock-like fit."},
        {"tag": "Essential", "title": "Canvas Classic", "desc": "The timeless silhouette updated with eco-friendly, sustainable materials."},
        {"tag": "Sport", "title": "Zoom Strike Track", "desc": "Aerodynamic construction built specifically for high-intensity interval training."},
        {"tag": "Premium", "title": "Heritage Leather", "desc": "Hand-stitched premium leather delivering unmatched durability and style."}
    ]

    for i, data in enumerate(placeholders):
        # Use picsum for reliable placeholder imagery
        img_url = f"https://picsum.photos/seed/{i+150}/600/800"
        cards_html += f"""
            <article class="bento-card" tabindex="0">
                <img src="{img_url}" alt="{data['title']}" class="card-img" loading="lazy">
                <div class="card-overlay"></div>
                <div class="card-content">
                    <span class="card-tag">{data['tag']}</span>
                    <h2 class="card-title">{data['title']}</h2>
                    <p class="card-desc">{data['desc']}</p>
                </div>
            </article>"""

    # === HTML ===
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
    <main class="main-wrapper">
        <header class="header-section">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>

        <section class="bento-grid" aria-label="Product Gallery">
            {cards_html}
        </section>
    </main>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Scroll Reveal Animation for Bento Cards
document.addEventListener('DOMContentLoaded', () => {{
    const cards = document.querySelectorAll('.bento-card');

    // Setup Intersection Observer
    const observerOptions = {{
        root: null,
        rootMargin: '0px',
        threshold: 0.1 // Trigger when 10% of card is visible
    }};

    const observer = new IntersectionObserver((entries, observer) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                // Add visible class
                entry.target.classList.add('is-visible');
                // Unobserve after animating to only animate once
                observer.unobserve(entry.target);
            }}
        }});
    }}, observerOptions);

    // Add staggered delay to cards and observe them
    cards.forEach((card, index) => {{
        // Apply a slight transition delay based on grid order for a cascading effect
        card.style.transitionDelay = `${{(index % 3) * 100}}ms`;
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
