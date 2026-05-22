def create_component(
    output_dir: str,
    title_text: str = "Bento Grid Showcase",
    body_text: str = "A modern layout utilizing grid-template-areas, grid stacking, and auto-fit wrapping.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#8b5cf6",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Bento Grid and Grid Stacking visual effects.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0f172a"
        card_bg = "#1e293b"
        text_color = "#f8fafc"
        text_muted = "#94a3b8"
        border_color = "rgba(255, 255, 255, 0.1)"
        shadow = "0 10px 25px -5px rgba(0, 0, 0, 0.5), 0 8px 10px -6px rgba(0, 0, 0, 0.3)"
    else:
        bg_color = "#f8fafc"
        card_bg = "#ffffff"
        text_color = "#0f172a"
        text_muted = "#64748b"
        border_color = "rgba(0, 0, 0, 0.05)"
        shadow = "0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01)"

    # === CSS ===
    css = f"""/* Bento Grid Showcase — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --card-bg: {card_bg};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --border: {border_color};
    --shadow: {shadow};
    --max-width: {width_px}px;
    --min-height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 3rem 1.5rem;
    line-height: 1.6;
}}

.container {{
    width: 100%;
    max-width: var(--max-width);
    min-height: var(--min-height);
    display: flex;
    flex-direction: column;
    gap: 3rem;
}}

.header {{
    text-align: center;
    margin-bottom: 1rem;
}}

.header h1 {{
    font-size: 2.5rem;
    font-weight: 800;
    letter-spacing: -0.025em;
    margin-bottom: 0.5rem;
    background: linear-gradient(135deg, var(--text), var(--accent));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

.header p {{
    color: var(--text-muted);
    font-size: 1.1rem;
    max-width: 600px;
    margin: 0 auto;
}}

/* === BENTO GRID LAYOUT === */
.bento-grid {{
    display: grid;
    /* 4 columns, dynamic rows */
    grid-template-columns: repeat(4, 1fr);
    grid-template-rows: repeat(2, minmax(220px, 1fr));
    gap: 1.5rem;
    
    /* The Magic of Bento Grid Areas */
    grid-template-areas:
        "hero hero box2 box3"
        "hero hero box4 box5";
}}

/* Responsive Bento adjustments */
@media (max-width: 1024px) {{
    .bento-grid {{
        grid-template-columns: repeat(3, 1fr);
        grid-template-areas:
            "hero hero box2"
            "hero hero box3"
            "box4 box5 box5";
    }}
}}

@media (max-width: 768px) {{
    .bento-grid {{
        grid-template-columns: 1fr;
        grid-template-areas:
            "hero"
            "box2"
            "box3"
            "box4"
            "box5";
    }}
}}

/* Grid Items */
.bento-item {{
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 1.5rem;
    padding: 1.5rem;
    box-shadow: var(--shadow);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    display: flex;
    flex-direction: column;
    position: relative;
    overflow: hidden;
}}

.bento-item:hover {{
    transform: translateY(-4px) scale(1.01);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    border-color: var(--accent);
}}

/* Assigning areas */
.item-hero {{ grid-area: hero; }}
.item-2 {{ grid-area: box2; }}
.item-3 {{ grid-area: box3; }}
.item-4 {{ grid-area: box4; }}
.item-5 {{ grid-area: box5; }}

/* === GRID STACKING (Hero Item) === */
/* Instead of position: absolute, we use CSS grid to stack items in the same cell */
.item-hero {{
    display: grid;
    padding: 0; /* Remove default padding for full bleed */
    /* Define a 1x1 grid */
    grid-template-columns: 1fr;
    grid-template-rows: 1fr;
}}

/* Both children span the exact same grid cell (1/1 to -1/-1) */
.item-hero .hero-bg,
.item-hero .hero-content {{
    grid-column: 1 / -1;
    grid-row: 1 / -1;
}}

.item-hero .hero-bg {{
    background: linear-gradient(135deg, var(--accent), #3b82f6);
    opacity: 0.85;
    width: 100%;
    height: 100%;
    object-fit: cover;
}}

.item-hero .hero-content {{
    z-index: 10;
    padding: 2.5rem;
    /* Use grid alignment to push content to bottom left */
    place-self: end start;
    color: white;
}}

.hero-content h2 {{
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}}

.hero-content p {{
    opacity: 0.9;
    font-size: 1.1rem;
}}

/* Standard Item content */
.bento-item h3 {{
    font-size: 1.25rem;
    margin-bottom: 0.5rem;
    color: var(--text);
}}

.bento-item p {{
    color: var(--text-muted);
    font-size: 0.95rem;
}}

.bento-icon {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 3rem;
    height: 3rem;
    border-radius: 0.75rem;
    background: rgba(139, 92, 246, 0.1);
    color: var(--accent);
    margin-bottom: auto; /* Pushes text to the bottom if container grows */
}}


/* === AUTO-FIT WRAPPING GRID === */
.section-title {{
    margin-top: 2rem;
    font-size: 1.5rem;
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.75rem;
}}

.auto-wrap-grid {{
    display: grid;
    /* Automatically wraps items, making them at least 280px wide, 
       but allowing them to grow to fill the row */
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
}}

.feature-card {{
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 1rem;
    padding: 1.5rem;
    display: flex;
    align-items: flex-start;
    gap: 1rem;
}}

.feature-card svg {{
    flex-shrink: 0;
    width: 24px;
    height: 24px;
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
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        
        <header class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>

        <!-- Bento Grid Concept -->
        <main class="bento-grid">
            
            <!-- Hero uses Grid Stacking -->
            <article class="bento-item item-hero">
                <div class="hero-bg"></div>
                <div class="hero-content">
                    <h2>Grid Stacking</h2>
                    <p>Overlaid content without position: absolute.</p>
                </div>
            </article>

            <article class="bento-item item-2">
                <div class="bento-icon">
                    <svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="3" y1="9" x2="21" y2="9"></line><line x1="9" y1="21" x2="9" y2="9"></line></svg>
                </div>
                <h3>Bento Layouts</h3>
                <p>Asymmetrical grids defined by visual areas.</p>
            </article>

            <article class="bento-item item-3">
                <div class="bento-icon">
                    <svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg>
                </div>
                <h3>Visual Depth</h3>
                <p>Layered shadows and native hover states.</p>
            </article>

            <article class="bento-item item-4">
                <div class="bento-icon">
                    <svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>
                </div>
                <h3>Responsive</h3>
                <p>Effortlessly reflows utilizing media queries.</p>
            </article>

            <article class="bento-item item-5">
                <div class="bento-icon">
                    <svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>
                </div>
                <h3>Performant</h3>
                <p>Pure CSS layout engine requiring no JavaScript calculation.</p>
            </article>

        </main>

        <!-- Auto-fit Grid Concept -->
        <h2 class="section-title">Auto-Wrapping Secondary Grid</h2>
        <section class="auto-wrap-grid">
            <div class="feature-card">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
                <div>
                    <h3>auto-fit</h3>
                    <p>Fills available rows naturally.</p>
                </div>
            </div>
            <div class="feature-card">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect></svg>
                <div>
                    <h3>minmax()</h3>
                    <p>Clamps boundaries intelligently.</p>
                </div>
            </div>
            <div class="feature-card">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="4 14 10 14 10 20"></polyline><polyline points="20 10 14 10 14 4"></polyline><line x1="14" y1="10" x2="21" y2="3"></line><line x1="3" y1="21" x2="10" y2="14"></line></svg>
                <div>
                    <h3>Fluid Layout</h3>
                    <p>No media queries needed here.</p>
                </div>
            </div>
        </section>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Bento Grid & Stacking - Layout is handled purely by CSS Grid.
// Adding an interaction observer to trigger a subtle entrance animation.
document.addEventListener('DOMContentLoaded', () => {{
    const items = document.querySelectorAll('.bento-item, .feature-card');
    
    // Set initial state
    items.forEach(item => {{
        item.style.opacity = '0';
        item.style.transform = 'translateY(20px)';
        item.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out, box-shadow 0.3s ease, border-color 0.3s ease';
    }});

    const observer = new IntersectionObserver((entries) => {{
        entries.forEach((entry, index) => {{
            if (entry.isIntersecting) {{
                // Stagger the animation slightly based on dom order
                setTimeout(() => {{
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                    
                    // Cleanup transition to not conflict with hover effects
                    setTimeout(() => {{
                        entry.target.style.transition = 'transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease';
                    }}, 600);
                }}, index * 100);
                observer.unobserve(entry.target);
            }}
        }});
    }}, {{ rootMargin: '0px 0px -50px 0px' }});

    items.forEach(item => observer.observe(item));
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
