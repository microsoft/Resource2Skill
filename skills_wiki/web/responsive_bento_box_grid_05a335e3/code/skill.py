def create_component(
    output_dir: str,
    title_text: str = "Discover the Features",
    body_text: str = "A seamless, asymmetric Bento Box layout powered by CSS Grid.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#8a2be2",     # CSS hex color for accent (e.g., BlueViolet)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Bento Grid layout.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#09090b"
        text_color = "#f4f4f5"
        text_muted = "#a1a1aa"
        surface_color = "rgba(255, 255, 255, 0.03)"
        border_color = "rgba(255, 255, 255, 0.08)"
        shadow = "0 8px 32px rgba(0, 0, 0, 0.4)"
        spotlight_color = "rgba(255, 255, 255, 0.06)"
    else:
        bg_color = "#f4f4f5"
        text_color = "#09090b"
        text_muted = "#52525b"
        surface_color = "#ffffff"
        border_color = "rgba(0, 0, 0, 0.05)"
        shadow = "0 8px 24px rgba(0, 0, 0, 0.06)"
        spotlight_color = "rgba(0, 0, 0, 0.03)"

    # Determine if text on accent color should be dark or light
    # For a robust component, we apply a safe stark white for deeply saturated accents, 
    # but a simple semi-transparent dark overlay can also ensure contrast.
    accent_text = "#ffffff"

    # === CSS ===
    css = f"""/* Responsive Bento Grid — Generated Component */
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
    --accent-text: {accent_text};
    --surface: {surface_color};
    --border: {border_color};
    --shadow: {shadow};
    --spotlight: {spotlight_color};
    --max-width: {width_px}px;
    --min-height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

.wrapper {{
    width: 100%;
    max-width: var(--max-width);
    min-height: var(--min-height);
    display: flex;
    flex-direction: column;
    justify-content: center;
}}

.header {{
    text-align: center;
    margin-bottom: 3rem;
}}

.header h1 {{
    font-size: clamp(2rem, 4vw, 3rem);
    font-weight: 700;
    letter-spacing: -0.02em;
    margin-bottom: 1rem;
}}

.header p {{
    color: var(--text-muted);
    font-size: 1.125rem;
    max-width: 600px;
    margin: 0 auto;
    line-height: 1.6;
}}

/* -- BENTO GRID SYSTEM -- */
.bento-grid {{
    display: grid;
    gap: 1.5rem;
    /* 4 Columns for Desktop */
    grid-template-columns: repeat(4, 1fr);
    grid-template-rows: repeat(2, minmax(280px, 1fr));
    grid-template-areas:
        "box-1 box-1 box-2 box-3"
        "box-1 box-1 box-4 box-5";
    width: 100%;
}}

/* The Grid Cards */
.box {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 1.5rem;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow);
    transition: transform 0.4s cubic-bezier(0.25, 1, 0.5, 1), box-shadow 0.4s ease;
    cursor: pointer;
}}

.box:hover {{
    transform: translateY(-4px) scale(1.01);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}}

/* Dynamic Mouse Spotlight */
.box::before {{
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(
        600px circle at var(--mouse-x, 50%) var(--mouse-y, 50%), 
        var(--spotlight), 
        transparent 40%
    );
    z-index: 0;
    opacity: 0;
    transition: opacity 0.5s ease;
    pointer-events: none;
}}

.bento-grid:hover .box::before {{
    opacity: 1;
}}

/* Content above the spotlight */
.box-content {{
    position: relative;
    z-index: 1;
    display: flex;
    flex-direction: column;
    height: 100%;
}}

/* Assigning Areas */
.box-1 {{ grid-area: box-1; background: var(--accent); color: var(--accent-text); border: none; }}
.box-2 {{ grid-area: box-2; }}
.box-3 {{ grid-area: box-3; }}
.box-4 {{ grid-area: box-4; }}
.box-5 {{ grid-area: box-5; }}

/* Inner content styling */
.box-icon {{
    font-size: 2rem;
    margin-bottom: 1.5rem;
    opacity: 0.9;
}}
.box-1 .box-icon {{ font-size: 3rem; }}

.box h3 {{
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.75rem;
}}
.box-1 h3 {{
    font-size: 2rem;
    margin-bottom: 1rem;
}}

.box p {{
    color: var(--text-muted);
    font-size: 0.95rem;
    line-height: 1.5;
}}
.box-1 p {{
    color: rgba(255,255,255,0.85);
    font-size: 1.125rem;
}}

/* Push text to bottom for some cards */
.push-bottom {{
    margin-top: auto;
}}

/* -- RESPONSIVE WRAPPING -- */
@media (max-width: 1024px) {{
    .bento-grid {{
        grid-template-columns: repeat(3, 1fr);
        grid-template-rows: repeat(3, minmax(250px, 1fr));
        grid-template-areas:
            "box-1 box-1 box-2"
            "box-1 box-1 box-3"
            "box-4 box-5 box-5";
    }}
}}

@media (max-width: 768px) {{
    .bento-grid {{
        grid-template-columns: repeat(2, 1fr);
        grid-template-rows: repeat(4, minmax(240px, 1fr));
        grid-template-areas:
            "box-1 box-1"
            "box-1 box-1"
            "box-2 box-3"
            "box-4 box-5";
    }}
}}

@media (max-width: 480px) {{
    .bento-grid {{
        grid-template-columns: 1fr;
        grid-template-rows: auto;
        grid-template-areas:
            "box-1"
            "box-2"
            "box-3"
            "box-4"
            "box-5";
    }}
    .box {{
        min-height: 250px;
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
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="wrapper">
        <header class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>

        <main class="bento-grid" id="bento">
            <!-- Hero Card -->
            <article class="box box-1">
                <div class="box-content">
                    <i class="fa-solid fa-wand-magic-sparkles box-icon"></i>
                    <div class="push-bottom">
                        <h3>Dynamic CSS Grid</h3>
                        <p>Utilizing grid-template-areas to craft an asymmetric, highly engaging hierarchy. The Hero block anchors the eye, spanning multiple rows and columns seamlessly.</p>
                    </div>
                </div>
            </article>

            <!-- Card 2 -->
            <article class="box box-2">
                <div class="box-content">
                    <i class="fa-solid fa-layer-group box-icon"></i>
                    <div class="push-bottom">
                        <h3>Fluid Spans</h3>
                        <p>Fractional units adapt to any container effortlessly.</p>
                    </div>
                </div>
            </article>

            <!-- Card 3 -->
            <article class="box box-3">
                <div class="box-content">
                    <i class="fa-solid fa-mobile-screen box-icon"></i>
                    <div class="push-bottom">
                        <h3>Responsive</h3>
                        <p>Breaks down beautifully from 4 columns to a stacked mobile view.</p>
                    </div>
                </div>
            </article>

            <!-- Card 4 -->
            <article class="box box-4">
                <div class="box-content">
                    <i class="fa-solid fa-bolt box-icon"></i>
                    <div class="push-bottom">
                        <h3>Performance</h3>
                        <p>No layout thrashing. GPU-accelerated hover states.</p>
                    </div>
                </div>
            </article>

            <!-- Card 5 -->
            <article class="box box-5">
                <div class="box-content">
                    <i class="fa-solid fa-code box-icon"></i>
                    <div class="push-bottom">
                        <h3>Interactive Glow</h3>
                        <p>Move your cursor over the grid. A combination of Javascript event listeners and CSS custom properties creates a smooth radial-gradient spotlight.</p>
                    </div>
                </div>
            </article>
        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Mouse Spotlight Tracking Logic
document.addEventListener('DOMContentLoaded', () => {{
    const bentoGrid = document.getElementById('bento');
    const cards = document.querySelectorAll('.box');

    // Add a mousemove listener to the grid container
    bentoGrid.addEventListener('mousemove', (e) => {{
        for(const card of cards) {{
            // Calculate the cursor position relative to each individual card
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            // Set local CSS variables for the radial-gradient position
            card.style.setProperty('--mouse-x', `${{x}}px`);
            card.style.setProperty('--mouse-y', `${{y}}px`);
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
