def create_component(
    output_dir: str,
    title_text: str = "Responsive Auto-Fit Grid",
    body_text: str = "Resize your browser window. This grid automatically calculates columns and wraps items without a single media query.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#ff3366",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Zero-Media-Query Fluid Grid System.
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0a0c10"
        text_color = "#e6edf3"
        text_muted = "rgba(230, 237, 243, 0.7)"
        surface_color = "rgba(255, 255, 255, 0.03)"
        grid_line = "rgba(255, 255, 255, 0.04)"
        border_color = "rgba(255, 255, 255, 0.08)"
        shadow = "0 4px 12px rgba(0, 0, 0, 0.2)"
        hover_shadow = "0 16px 40px rgba(0, 0, 0, 0.5)"
    else:
        bg_color = "#f6f8fa"
        text_color = "#1f2328"
        text_muted = "rgba(31, 35, 40, 0.7)"
        surface_color = "#ffffff"
        grid_line = "rgba(0, 0, 0, 0.05)"
        border_color = "rgba(0, 0, 0, 0.08)"
        shadow = "0 4px 12px rgba(0, 0, 0, 0.04)"
        hover_shadow = "0 16px 32px rgba(0, 0, 0, 0.12)"

    # === CSS ===
    css = f"""/* Zero-Media-Query Fluid Grid System */
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
    --grid-line: {grid_line};
    --border: {border_color};
    --shadow: {shadow};
    --hover-shadow: {hover_shadow};
    --width: {width_px}px;
    --min-height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: var(--min-height);
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
    overflow-x: hidden;
}}

/* Technical Grid Background Pattern */
body::before {{
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(var(--grid-line) 1px, transparent 1px),
        linear-gradient(90deg, var(--grid-line) 1px, transparent 1px);
    background-size: 40px 40px;
    background-position: center top;
    z-index: -1;
    pointer-events: none;
    /* Fade out towards the edges */
    mask-image: radial-gradient(ellipse at center 40%, black 30%, transparent 80%);
    -webkit-mask-image: radial-gradient(ellipse at center 40%, black 30%, transparent 80%);
}}

.container {{
    width: 100%;
    max-width: var(--width);
    margin: 0 auto;
    padding: 80px 24px;
}}

.header {{
    text-align: center;
    margin-bottom: 60px;
    max-width: 600px;
    margin-inline: auto;
}}

.header h1 {{
    font-size: clamp(2rem, 4vw, 2.75rem);
    font-weight: 700;
    margin-bottom: 16px;
    letter-spacing: -0.02em;
}}

.header p {{
    font-size: 1.1rem;
    line-height: 1.6;
    color: var(--text-muted);
}}

/* --- THE CORE GRID MAGIC --- */
.auto-fit-grid {{
    display: grid;
    /* 
      auto-fit: create as many columns as possible
      minmax(min(100%, 280px), 1fr): Cards are at least 280px, but will shrink if container is < 280px. 
      Otherwise, they stretch evenly (1fr) to fill remaining space.
    */
    grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr));
    gap: 24px;
    width: 100%;
}}

/* Card Wrapper handles the entrance animation */
.card-wrapper {{
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 0.7s cubic-bezier(0.16, 1, 0.3, 1), 
                transform 0.7s cubic-bezier(0.16, 1, 0.3, 1);
}}

.card-wrapper.is-visible {{
    opacity: 1;
    transform: translateY(0);
}}

/* The actual Card */
.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 32px 24px;
    height: 100%;
    display: flex;
    flex-direction: column;
    gap: 16px;
    box-shadow: var(--shadow);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    position: relative;
    overflow: hidden;
    transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1), 
                box-shadow 0.3s ease, 
                border-color 0.3s ease;
    cursor: default;
}}

/* Animated top border highlight */
.card::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: var(--accent);
    transform: scaleX(0);
    transform-origin: left;
    transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}}

.card:hover::before {{
    transform: scaleX(1);
}}

.card:hover {{
    transform: translateY(-8px);
    box-shadow: var(--hover-shadow);
    border-color: color-mix(in srgb, var(--accent) 50%, transparent);
}}

.card-icon {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    border-radius: 12px;
    background: color-mix(in srgb, var(--accent) 15%, transparent);
    color: var(--accent);
    font-size: 1.25rem;
    margin-bottom: 8px;
}}

.card-title {{
    font-size: 1.25rem;
    font-weight: 600;
}}

.card-desc {{
    font-size: 0.95rem;
    line-height: 1.6;
    color: var(--text-muted);
    margin-top: auto; /* Pushes description up, keeping cards uniform */
}}
"""

    # === HTML ===
    cards_data = [
        {"icon": "fa-th-large", "title": "Auto-Fit Algorithm", "desc": "Fluid layouts that automatically evaluate container space to generate new column tracks without media queries."},
        {"icon": "fa-ruler-combined", "title": "Fractional Units", "desc": "The 'fr' unit intelligently distributes available space among grid tracks, preventing awkward pixel math."},
        {"icon": "fa-border-all", "title": "Perfect Gutters", "desc": "Maintain precise, consistent spacing between items using the 'gap' property without margins collapsing."},
        {"icon": "fa-layer-group", "title": "Implicit Grids", "desc": "Seamlessly handles dynamic content injections that exceed your explicitly defined grid rows."},
        {"icon": "fa-object-group", "title": "Template Areas", "desc": "Provides the capability to define complex UI structural layouts using semantic, readable named string areas."},
        {"icon": "fa-align-center", "title": "Box Alignment", "desc": "Total micro-level control over horizontal and vertical item placement with justify and align properties."}
    ]

    cards_html = ""
    for card in cards_data:
        cards_html += f"""
            <div class="card-wrapper">
                <div class="card">
                    <div class="card-icon"><i class="fa-solid {card['icon']}"></i></div>
                    <h3 class="card-title">{card['title']}</h3>
                    <p class="card-desc">{card['desc']}</p>
                </div>
            </div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    
    <!-- Fonts & Icons -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- Styles -->
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>
        
        <main class="auto-fit-grid">
            {cards_html}
        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Staggered Entrance Animation via Intersection Observer
document.addEventListener('DOMContentLoaded', () => {{
    const wrappers = document.querySelectorAll('.card-wrapper');

    // Create the observer
    const observer = new IntersectionObserver((entries) => {{
        entries.forEach((entry) => {{
            if (entry.isIntersecting) {{
                // Trigger the CSS transition by adding class
                entry.target.classList.add('is-visible');
                // Stop observing once animated in
                observer.unobserve(entry.target);
            }}
        }});
    }}, {{
        threshold: 0.1, // Trigger when 10% of card is visible
        rootMargin: "0px 0px -20px 0px"
    }});

    // Observe all cards and apply a staggered transition delay
    wrappers.forEach((wrapper, index) => {{
        // Calculate a repeating stagger delay (groups of 3)
        // This ensures the first row loads 0s, 0.1s, 0.2s, etc.
        const staggerIndex = index % 3;
        wrapper.style.transitionDelay = `${{staggerIndex * 0.1}}s`;
        
        observer.observe(wrapper);
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
