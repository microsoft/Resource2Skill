def create_component(
    output_dir: str,
    title_text: str = "DIV 1: JS Parallax",
    body_text: str = "Scroll down to experience the depth",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#800000",     # CSS hex color for accent (e.g., maroon)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Dual-Method Parallax Scrolling visual effect.
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    # The cards will contrast against the background scheme
    if color_scheme == "dark":
        card_bg = "#eeeeee"
        card_text = "#1a1a2e"
        secondary_color = "#00adb5" # Aqua variant from the tutorial
    else:
        card_bg = "#1a1a2e"
        card_text = "#eeeeee"
        secondary_color = "#a8d8ea"

    # === CSS ===
    css = f"""/* Dual-Method Parallax Scrolling — Generated Component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --accent: {accent_color};
    --secondary: {secondary_color};
    --card-bg: {card_bg};
    --card-text: {card_text};
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    /* Hide x-overflow to prevent horizontal scrollbars during parallax calculation */
    overflow-x: hidden; 
}}

/* Sections represent the distinct visual blocks */
.section {{
    display: flex;
    align-items: center;
    justify-content: center;
    /* Use dynamic viewport height, but respect the minimum requested height */
    height: 100vh;
    min-height: {height_px}px;
    width: 100%;
    position: relative;
}}

/* High-contrast foreground cards */
.card {{
    background: var(--card-bg);
    color: var(--card-text);
    padding: 24px 48px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    z-index: 10;
}}

.card h2 {{
    font-size: 3.5rem;
    font-weight: 800;
    margin-bottom: 0.5rem;
    letter-spacing: -1px;
}}

.card p {{
    font-size: 1.25rem;
    opacity: 0.8;
}}

/* -- Parallax Implementations -- */

.js-parallax {{
    background-image: url('https://images.unsplash.com/photo-1555066931-4365d14bab8c?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80');
    background-size: cover;
    background-position: center 0px;
    background-repeat: no-repeat;
    /* Hint to browser for scroll performance */
    will-change: background-position;
}}

.css-parallax {{
    background-image: url('https://images.unsplash.com/photo-1517694712202-14dd9538aa97?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80');
    background-size: cover;
    background-position: center center;
    background-repeat: no-repeat;
    /* Native CSS Parallax */
    background-attachment: fixed;
}}

/* Solid color dividing sections */
.solid-accent {{
    background-color: var(--accent);
}}

.solid-secondary {{
    background-color: var(--secondary);
}}

/* Accessibility: Disable parallax for users sensitive to motion */
@media (prefers-reduced-motion: reduce) {{
    .js-parallax, .css-parallax {{
        background-attachment: scroll !important;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    
    <!-- Section 1: Javascript-driven Fractional Parallax -->
    <div class="section js-parallax" id="parallax">
        <div class="card">
            <h2>{title_text}</h2>
            <p>{body_text}</p>
        </div>
    </div>

    <!-- Section 2: Solid Dividing Block -->
    <div class="section solid-accent">
        <div class="card">
            <h2>DIV 2</h2>
            <p>Solid Color Divider</p>
        </div>
    </div>

    <!-- Section 3: CSS-driven Fixed Parallax -->
    <div class="section css-parallax">
        <div class="card">
            <h2>DIV 3: CSS Parallax</h2>
            <p>background-attachment: fixed</p>
        </div>
    </div>

    <!-- Section 4: Secondary Solid Dividing Block -->
    <div class="section solid-secondary">
        <div class="card">
            <h2>DIV 4</h2>
            <p>End of Sequence</p>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Dual-Method Parallax Scrolling Logic
document.addEventListener('DOMContentLoaded', () => {{
    const parallaxEl = document.getElementById('parallax');
    
    // Check if user has requested reduced motion for accessibility
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

    // Use requestAnimationFrame to optimize scroll event handling and prevent layout jank
    let ticking = false;

    window.addEventListener('scroll', () => {{
        // Abort calculation if reduced motion is enabled
        if (prefersReducedMotion.matches) return;

        let offset = window.pageYOffset || document.documentElement.scrollTop;

        if (!ticking) {{
            window.requestAnimationFrame(() => {{
                // Multiplier 0.7 makes the background image move slightly slower 
                // than the page scroll, creating a sense of distance.
                parallaxEl.style.backgroundPositionY = (offset * 0.7) + 'px';
                ticking = false;
            }});
            ticking = true;
        }}
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
