def create_component(
    output_dir: str,
    title_text: str = "Discover Features",
    body_text: str = "Everything you need, packed into a beautiful layout.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#8b5cf6",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Bento Grid with Stacked Layers.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Theme Definition ===
    if color_scheme == "dark":
        bg_color = "#0f172a"
        card_bg = "#1e293b"
        text_primary = "#f8fafc"
        text_secondary = "#94a3b8"
        border_color = "rgba(255, 255, 255, 0.05)"
        shadow = "0 10px 30px -10px rgba(0, 0, 0, 0.5)"
        glass_bg = "rgba(15, 23, 42, 0.6)"
    else:
        bg_color = "#f8fafc"
        card_bg = "#ffffff"
        text_primary = "#0f172a"
        text_secondary = "#475569"
        border_color = "rgba(0, 0, 0, 0.05)"
        shadow = "0 10px 30px -10px rgba(0, 0, 0, 0.05)"
        glass_bg = "rgba(255, 255, 255, 0.6)"

    # === CSS ===
    css = f"""/* Responsive Bento Grid — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --card-bg: {card_bg};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --accent: {accent_color};
    --border: {border_color};
    --shadow: {shadow};
    --glass-bg: {glass_bg};
    --max-width: {width_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 4rem 2rem;
    overflow-x: hidden;
}}

.header {{
    text-align: center;
    margin-bottom: 3rem;
    max-width: 600px;
}}

.header h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    margin-bottom: 1rem;
    background: linear-gradient(to right, var(--text-primary), var(--accent));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

.header p {{
    font-size: 1.125rem;
    color: var(--text-secondary);
    line-height: 1.6;
}}

/* --- Bento Grid Layout --- */
.bento-grid {{
    display: grid;
    width: 100%;
    max-width: var(--max-width);
    gap: 1.5rem;
    /* Explicit Desktop Layout Mapping */
    grid-template-columns: repeat(4, 1fr);
    grid-auto-rows: 250px;
    grid-template-areas: 
        "hero hero side-top side-top"
        "hero hero flat-1 flat-2";
}}

/* Card Assignments */
.card-hero {{ grid-area: hero; }}
.card-side-top {{ grid-area: side-top; }}
.card-flat-1 {{ grid-area: flat-1; }}
.card-flat-2 {{ grid-area: flat-2; }}

/* Responsive Overrides via Media Queries */
@media (max-width: 900px) {{
    .bento-grid {{
        grid-template-columns: repeat(2, 1fr);
        grid-auto-rows: 220px;
        grid-template-areas: 
            "hero hero"
            "hero hero"
            "side-top side-top"
            "flat-1 flat-2";
    }}
}}

@media (max-width: 500px) {{
    .bento-grid {{
        grid-template-columns: 1fr;
        grid-auto-rows: minmax(200px, auto);
        grid-template-areas: 
            "hero"
            "side-top"
            "flat-1"
            "flat-2";
    }}
}}

/* --- Card Styles --- */
.bento-card {{
    background: var(--card-bg);
    border-radius: 24px;
    border: 1px solid var(--border);
    box-shadow: var(--shadow);
    padding: 2rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    overflow: hidden;
    position: relative;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    opacity: 0; /* For JS Animation */
    transform: translateY(20px);
}}

.bento-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 20px 40px -10px rgba(0,0,0,0.2);
}}

.bento-card h2 {{
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}}

.bento-card p {{
    color: var(--text-secondary);
    line-height: 1.5;
    font-size: 0.95rem;
}}

.icon-wrapper {{
    width: 48px;
    height: 48px;
    border-radius: 12px;
    background: var(--bg);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1.5rem;
    color: var(--accent);
}}

/* --- Grid Stacking Technique (Hero Card) --- */
/* Turning the card itself into a grid to stack content over background natively */
.card-hero {{
    display: grid;
    padding: 0; /* Remove padding to let image fill */
}}

.card-hero > * {{
    /* Place all direct children into grid row 1, col 1 */
    grid-area: 1 / 1 / 2 / 2;
}}

.hero-bg {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    background: linear-gradient(135deg, var(--accent), #f43f5e);
    border-radius: 24px;
}}

.hero-content {{
    place-self: end start; /* Align to bottom-left */
    background: var(--glass-bg);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    margin: 1.5rem;
    padding: 1.5rem;
    border-radius: 16px;
    border: 1px solid var(--border);
}}

.hero-content h2, .hero-content p {{
    color: var(--text-primary);
}}

/* Utilities */
.visible {{
    opacity: 1;
    transform: translateY(0);
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
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    
    <header class="header">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </header>

    <section class="bento-grid">
        
        <!-- Hero Card demonstrating 'Grid Stacking' -->
        <article class="bento-card card-hero">
            <div class="hero-bg"></div>
            <div class="hero-content">
                <h2>Advanced Layouts</h2>
                <p>Using CSS Grid Stacking to place content securely over backgrounds without absolute positioning.</p>
            </div>
        </article>

        <!-- Standard Bento Cards -->
        <article class="bento-card card-side-top">
            <div class="icon-wrapper">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="3" y1="9" x2="21" y2="9"></line><line x1="9" y1="21" x2="9" y2="9"></line></svg>
            </div>
            <div>
                <h2>Explicit Areas</h2>
                <p>Map out complex interfaces intuitively using grid-template-areas.</p>
            </div>
        </article>

        <article class="bento-card card-flat-1">
            <div>
                <h2>Fractional Units</h2>
                <p>Fluid scaling with 1fr units ensures a perfect fit.</p>
            </div>
        </article>

        <article class="bento-card card-flat-2">
            <div>
                <h2>Responsive Reflow</h2>
                <p>Completely reorganize layouts via simple media queries.</p>
            </div>
        </article>

    </section>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Interaction Logic: Intersection Observer for Staggered Fade-In
document.addEventListener('DOMContentLoaded', () => {{
    const cards = document.querySelectorAll('.bento-card');
    
    const observerOptions = {{
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    }};

    const observer = new IntersectionObserver((entries, observer) => {{
        entries.forEach((entry, index) => {{
            if (entry.isIntersecting) {{
                // Stagger the animation based on DOM order
                setTimeout(() => {{
                    entry.target.classList.add('visible');
                }}, index * 100); 
                observer.unobserve(entry.target);
            }}
        }});
    }}, observerOptions);

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
