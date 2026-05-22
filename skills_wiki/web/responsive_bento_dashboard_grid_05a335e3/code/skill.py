def create_component(
    output_dir: str,
    title_text: str = "Bento Grid Dashboard",
    body_text: str = "A fully responsive, fluid CSS Grid layout utilizing auto-fit, minmax, and span features.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#6366f1",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 900,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Bento Dashboard Grid visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#0B0F19"
        text_color = "#F3F4F6"
        text_muted = "#9CA3AF"
        surface_color = "#1F2937"
        surface_hover = "#374151"
        border_color = "rgba(255, 255, 255, 0.05)"
        shadow = "0 10px 30px -10px rgba(0, 0, 0, 0.5)"
    else:
        bg_color = "#F9FAFB"
        text_color = "#111827"
        text_muted = "#4B5563"
        surface_color = "#FFFFFF"
        surface_hover = "#F3F4F6"
        border_color = "rgba(0, 0, 0, 0.05)"
        shadow = "0 10px 30px -10px rgba(0, 0, 0, 0.05)"

    # === CSS ===
    css = f"""/* Responsive Bento Dashboard Grid */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

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
    --surface-hover: {surface_hover};
    --border: {border_color};
    --shadow: {shadow};
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 2rem;
}}

.app-wrapper {{
    width: 100%;
    max-width: {width_px}px;
    margin: 0 auto;
}}

.header {{
    margin-bottom: 2.5rem;
    text-align: center;
}}

.header h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -0.025em;
    margin-bottom: 0.5rem;
}}

.header p {{
    color: var(--text-muted);
    font-size: 1.1rem;
}}

/* === Core Grid Magic === */
.bento-grid {{
    display: grid;
    /* auto-fit + minmax creates fluid columns without media queries for standard cards */
    grid-template-columns: repeat(auto-fit, minmax(min(100%, 250px), 1fr));
    /* Fixed row height to maintain masonry/bento proportion */
    grid-auto-rows: 240px;
    gap: 1.5rem;
    
    /* Animation initial state container */
    opacity: 1;
}}

/* Bento Grid Items */
.bento-item {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    box-shadow: var(--shadow);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
    
    /* For JS Staggered Animation */
    opacity: 0;
    transform: translateY(20px);
}}

/* Layout Modifiers for the 'Bento' asymmetry */
@media (min-width: 600px) {{
    .span-col-2 {{
        grid-column: span 2;
    }}
    .span-row-2 {{
        grid-row: span 2;
    }}
}}

/* Large hero block spans both to create a massive focus point */
@media (min-width: 900px) {{
    .span-large {{
        grid-column: span 2;
        grid-row: span 2;
    }}
}}

/* Hover Interactions */
.bento-item:hover {{
    transform: translateY(-4px) scale(1.01);
    border-color: var(--accent);
    box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.15);
}}

/* Internal Card Styling using Flexbox */
.item-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: auto;
}}

.icon-box {{
    width: 48px;
    height: 48px;
    border-radius: 12px;
    background: rgba(156, 163, 175, 0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--accent);
}}

.item-title {{
    font-size: 1.25rem;
    font-weight: 600;
    margin-top: 1rem;
    margin-bottom: 0.5rem;
}}

.item-desc {{
    color: var(--text-muted);
    font-size: 0.9rem;
    line-height: 1.5;
}}

.highlight-metric {{
    font-size: 3rem;
    font-weight: 700;
    color: var(--text);
    margin-top: 1rem;
}}

/* Grid Stacking Concept (Covered in video) */
.stacked-card {{
    display: grid;
    /* Create a 1x1 grid inside the card */
    grid-template-columns: 1fr;
    grid-template-rows: 1fr;
    padding: 0; /* Remove padding to let image fill */
}}

.stacked-card > * {{
    /* Place all children in the exact same cell */
    grid-column: 1 / -1;
    grid-row: 1 / -1;
}}

.stacked-img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    z-index: 1;
    opacity: 0.6;
    transition: opacity 0.3s ease;
}}

.stacked-card:hover .stacked-img {{
    opacity: 0.3;
}}

.stacked-content {{
    z-index: 2;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    background: linear-gradient(to top, var(--bg) 0%, transparent 80%);
}}

/* JS Animation class */
.bento-item.animate-in {{
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
    <link rel="stylesheet" href="style.css">
    <!-- External Icon Set -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <div class="app-wrapper">
        <header class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>

        <main class="bento-grid">
            
            <!-- Standard Item -->
            <article class="bento-item">
                <div class="item-header">
                    <div class="icon-box"><i class="fa-solid fa-chart-line fa-xl"></i></div>
                </div>
                <div>
                    <h2 class="item-title">Analytics</h2>
                    <p class="item-desc">Real-time data visualization via fluid grid layouts.</p>
                </div>
            </article>

            <!-- Large Feature (Spans 2 columns, 2 rows) -->
            <article class="bento-item span-large">
                <div class="item-header">
                    <div class="icon-box"><i class="fa-solid fa-layer-group fa-xl"></i></div>
                    <span style="color: var(--accent); font-weight: 600;">Pro Feature</span>
                </div>
                <div style="margin-top: auto;">
                    <div class="highlight-metric">2.4M+</div>
                    <h2 class="item-title">Active Grid Renderings</h2>
                    <p class="item-desc">Using repeat, auto-fit, and minmax, this block naturally adapts. On smaller screens, the media queries drop the span property, forcing it to fall back into a fluid, single-column layout automatically.</p>
                </div>
            </article>

            <!-- Tall Item (Spans 2 rows) -->
            <article class="bento-item span-row-2">
                <div class="item-header">
                    <div class="icon-box"><i class="fa-solid fa-mobile-screen fa-xl"></i></div>
                </div>
                <div>
                    <h2 class="item-title">Responsive</h2>
                    <p class="item-desc">Notice how vertical rhythms are preserved using grid-auto-rows. This card spans exactly two base rows plus the gap space.</p>
                </div>
            </article>

            <!-- Wide Item (Spans 2 cols) -->
            <article class="bento-item span-col-2">
                <div class="item-header">
                    <div class="icon-box"><i class="fa-solid fa-code fa-xl"></i></div>
                </div>
                <div>
                    <h2 class="item-title">Implicit vs Explicit</h2>
                    <p class="item-desc">Elements placed without explicitly defined row tracks fall into the implicit grid generated by CSS.</p>
                </div>
            </article>

            <!-- Standard Item -->
            <article class="bento-item">
                <div class="item-header">
                    <div class="icon-box"><i class="fa-solid fa-bolt fa-xl"></i></div>
                </div>
                <div>
                    <h2 class="item-title">Performance</h2>
                    <p class="item-desc">Native CSS calculation outperforms JS window listener logic.</p>
                </div>
            </article>

            <!-- Stacked Element (Demonstrating Grid Stacking from video) -->
            <article class="bento-item stacked-card span-col-2">
                <img src="https://images.unsplash.com/photo-1550684848-fac1c5b4e853?auto=format&fit=crop&q=80&w=1000" alt="Abstract Code" class="stacked-img">
                <div class="stacked-content">
                    <h2 class="item-title" style="margin-top: 0;">Grid Stacking Magic</h2>
                    <p class="item-desc">This card uses a 1x1 grid internally, placing both the image and this text overlay in grid-column: 1 / -1. No absolute positioning needed!</p>
                </div>
            </article>

        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Bento Dashboard Grid - Interactions
document.addEventListener('DOMContentLoaded', () => {{
    const gridItems = document.querySelectorAll('.bento-item');
    
    // Staggered cascade entrance animation
    gridItems.forEach((item, index) => {{
        // Apply a staggered transition delay based on the element's index
        item.style.transitionDelay = `${{index * 0.08}}s`;
        
        // Trigger the animation in the next frame to allow DOM to paint initial state
        requestAnimationFrame(() => {{
            item.classList.add('animate-in');
        }});
        
        // Remove the transition delay after animation completes 
        // so hover effects don't inherit the delay
        setTimeout(() => {{
            item.style.transitionDelay = '0s';
        }}, (index * 80) + 300); // delay + transition duration
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
