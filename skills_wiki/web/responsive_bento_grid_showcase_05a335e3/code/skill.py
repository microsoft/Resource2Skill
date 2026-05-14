def create_component(
    output_dir: str,
    title_text: str = "Discover Our Features",
    body_text: str = "A powerful, asymmetric grid layout for highlighting key capabilities.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#6366f1",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Bento Grid visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_primary = "#f8fafc"
        text_secondary = "#94a3b8"
        card_bg = "rgba(30, 41, 59, 0.7)"
        card_border = "rgba(255, 255, 255, 0.08)"
        glow_color = f"{accent_color}33" # 20% opacity hex
    else:
        bg_color = "#f8fafc"
        text_primary = "#0f172a"
        text_secondary = "#64748b"
        card_bg = "rgba(255, 255, 255, 0.9)"
        card_border = "rgba(0, 0, 0, 0.08)"
        glow_color = f"{accent_color}22"

    # === CSS ===
    css = f"""/* Responsive Bento Grid Showcase */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --accent: {accent_color};
    --card-bg: {card_bg};
    --card-border: {card_border};
    --glow-color: {glow_color};
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

/* Header Section */
.header {{
    text-align: center;
    margin-bottom: 3rem;
    max-width: 600px;
}}

.header h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    letter-spacing: -0.025em;
}}

.header p {{
    color: var(--text-secondary);
    font-size: 1.125rem;
    line-height: 1.6;
}}

/* Bento Grid Container */
.bento-grid {{
    display: grid;
    width: 100%;
    max-width: {width_px}px;
    gap: 1.5rem;
    
    /* Desktop Layout: 4 columns */
    grid-template-columns: repeat(4, 1fr);
    grid-auto-rows: minmax(180px, auto);
    
    /* The Magic Map */
    grid-template-areas:
        "hero hero item1 item2"
        "hero hero item3 item3"
        "item4 item5 item5 item6";
}}

/* Individual Grid Area Assignments */
.bento-item:nth-child(1) {{ grid-area: hero; }}
.bento-item:nth-child(2) {{ grid-area: item1; }}
.bento-item:nth-child(3) {{ grid-area: item2; }}
.bento-item:nth-child(4) {{ grid-area: item3; }}
.bento-item:nth-child(5) {{ grid-area: item4; }}
.bento-item:nth-child(6) {{ grid-area: item5; }}
.bento-item:nth-child(7) {{ grid-area: item6; }}

/* Bento Card Styling */
.bento-item {{
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 24px;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s ease;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
}}

/* JS Mouse Glow Effect */
.bento-item::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: radial-gradient(
        800px circle at var(--mouse-x, -500px) var(--mouse-y, -500px),
        var(--glow-color),
        transparent 40%
    );
    z-index: 0;
    pointer-events: none;
    opacity: 0;
    transition: opacity 0.5s ease;
}}

.bento-item:hover::before {{
    opacity: 1;
}}

.bento-item:hover {{
    transform: translateY(-4px) scale(1.01);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}}

/* Content z-index to stay above glow */
.bento-content {{
    position: relative;
    z-index: 1;
}}

.bento-icon {{
    display: flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    background: var(--accent);
    color: #fff;
    border-radius: 14px;
    margin-bottom: auto;
    font-size: 1.5rem;
    font-weight: bold;
}}

.bento-title {{
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    margin-top: 1.5rem;
}}

.bento-desc {{
    color: var(--text-secondary);
    font-size: 0.95rem;
    line-height: 1.5;
}}

/* Special Hero Styling */
.bento-item:nth-child(1) .bento-title {{
    font-size: 2rem;
}}

.bento-item:nth-child(1) .bento-desc {{
    font-size: 1.1rem;
}}

/* Responsive Design */

/* Tablet Layout */
@media (max-width: 968px) {{
    .bento-grid {{
        grid-template-columns: repeat(2, 1fr);
        grid-template-areas:
            "hero hero"
            "hero hero"
            "item1 item2"
            "item3 item3"
            "item5 item5"
            "item4 item6";
    }}
}}

/* Mobile Layout */
@media (max-width: 640px) {{
    .bento-grid {{
        grid-template-columns: 1fr;
        grid-auto-rows: minmax(200px, auto);
        grid-template-areas:
            "hero"
            "item1"
            "item2"
            "item3"
            "item4"
            "item5"
            "item6";
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
    <link rel="stylesheet" href="style.css">
</head>
<body>
    
    <div class="header">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </div>

    <section class="bento-grid">
        <!-- Hero Card (2x2) -->
        <article class="bento-item">
            <div class="bento-content">
                <div class="bento-icon">✦</div>
                <h2 class="bento-title">Absolute Control</h2>
                <p class="bento-desc">Harness the power of CSS Grid template areas to explicitly place elements exactly where they belong across multiple viewports.</p>
            </div>
        </article>

        <!-- Standard Cards (1x1) -->
        <article class="bento-item">
            <div class="bento-content">
                <div class="bento-icon">1</div>
                <h2 class="bento-title">Responsive</h2>
                <p class="bento-desc">Adapts seamlessly from desktop to mobile.</p>
            </div>
        </article>

        <article class="bento-item">
            <div class="bento-content">
                <div class="bento-icon">2</div>
                <h2 class="bento-title">Fluid</h2>
                <p class="bento-desc">Fractional units distribute space perfectly.</p>
            </div>
        </article>

        <!-- Wide Card (2x1) -->
        <article class="bento-item">
            <div class="bento-content">
                <div class="bento-icon">⚡</div>
                <h2 class="bento-title">High Performance</h2>
                <p class="bento-desc">No heavy JS calculations required for the layout geometry.</p>
            </div>
        </article>

        <!-- Standard Card (1x1) -->
        <article class="bento-item">
            <div class="bento-content">
                <div class="bento-icon">3</div>
                <h2 class="bento-title">Clean</h2>
                <p class="bento-desc">Semantic HTML structures.</p>
            </div>
        </article>

        <!-- Wide Card (2x1) -->
        <article class="bento-item">
            <div class="bento-content">
                <div class="bento-icon">∞</div>
                <h2 class="bento-title">Infinite Combinations</h2>
                <p class="bento-desc">Redraw the grid-template map using media queries to completely restructure your UI instantly.</p>
            </div>
        </article>

        <!-- Standard Card (1x1) -->
        <article class="bento-item">
            <div class="bento-content">
                <div class="bento-icon">4</div>
                <h2 class="bento-title">Modern</h2>
                <p class="bento-desc">Apple & Windows UI inspired.</p>
            </div>
        </article>
    </section>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Mouse Glow Tracking
document.addEventListener('DOMContentLoaded', () => {{
    const bentoItems = document.querySelectorAll('.bento-item');

    // Update CSS custom properties based on mouse position
    const handleMouseMove = (e) => {{
        const target = e.currentTarget;
        const rect = target.getBoundingClientRect();
        
        // Calculate mouse position relative to the element
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        // Update CSS variables
        target.style.setProperty('--mouse-x', `${{x}}px`);
        target.style.setProperty('--mouse-y', `${{y}}px`);
    }};

    // Attach listeners to all bento cards
    bentoItems.forEach(item => {{
        item.addEventListener('mousemove', handleMouseMove);
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
