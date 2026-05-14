def create_component(
    output_dir: str,
    title_text: str = "Animation Timelines",
    body_text: str = "Scroll to trigger native CSS view() animations and explore 3D keyframe loaders.",
    color_scheme: str = "dark",
    accent_color: str = "#00e5ff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing CSS Scroll-Driven Reveals and 3D Keyframe Loaders.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme logic based on scheme
    if color_scheme == "dark":
        bg_color = "#0d1117"
        text_color = "#c9d1d9"
        surface_color = "#161b22"
        border_color = "#30363d"
        surface_alt = "#21262d"
        text_muted = "#8b949e"
    else:
        bg_color = "#f6f8fa"
        text_color = "#24292f"
        surface_color = "#ffffff"
        border_color = "#d0d7de"
        surface_alt = "#eaeef2"
        text_muted = "#57606a"

    # Generate grid cards dynamically
    cards_html = ""
    for i in range(1, 25):
        cards_html += f"""
                <div class="card-wrapper">
                    <div class="card">
                        <div class="card-icon">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                                <line x1="3" y1="9" x2="21" y2="9"></line>
                                <line x1="9" y1="21" x2="9" y2="9"></line>
                            </svg>
                        </div>
                        <h3>Block {i}</h3>
                        <p>Scroll-driven opacity and scale interpolation powered by native CSS timelines.</p>
                    </div>
                </div>"""

    # === CSS ===
    css = f"""/* CSS Scroll-Driven Reveal & 3D Loader Component */
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
    --border: {border_color};
    --surface-alt: {surface_alt};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

/* Outer wrapper acting as the application window */
.app-window {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    background: var(--bg);
    overflow-y: auto;
    overflow-x: hidden;
    position: relative;
    border: 1px solid var(--border);
    box-shadow: 0 24px 48px rgba(0, 0, 0, 0.2);
    border-radius: 16px;
    padding: 40px;
}}

/* Custom Scrollbar for the App Window */
.app-window::-webkit-scrollbar {{ width: 8px; }}
.app-window::-webkit-scrollbar-track {{ background: transparent; }}
.app-window::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 4px; }}
.app-window::-webkit-scrollbar-thumb:hover {{ background: var(--accent); }}

.hero {{
    text-align: center;
    margin-bottom: 60px;
    padding-top: 20px;
}}

.title {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 12px;
    color: var(--text);
}}

.body-text {{
    font-size: 1.1rem;
    color: var(--text-muted);
    max-width: 600px;
    margin: 0 auto;
}}

.grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 24px;
}}

/* --- SCROLL REVEAL ANIMATION (Applied to Wrapper) --- */
/* The wrapper handles scroll transforms, preventing conflicts with hover */
.card-wrapper {{
    animation: scroll-reveal linear both;
    animation-timeline: view();
    animation-range: entry 10% cover 30%;
}}

@keyframes scroll-reveal {{
    from {{
        opacity: 0;
        transform: translateY(60px) scale(0.9);
    }}
    to {{
        opacity: 1;
        transform: translateY(0) scale(1);
    }}
}}

/* --- HOVER INTERACTION (Applied to Inner Card) --- */
.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px;
    height: 100%;
    display: flex;
    flex-direction: column;
    gap: 12px;
    transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), 
                border-color 0.3s ease, 
                box-shadow 0.3s ease;
}}

.card:hover {{
    transform: translateY(-8px);
    border-color: var(--accent);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
}}

.card-icon {{
    width: 48px;
    height: 48px;
    background: var(--surface-alt);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 8px;
}}

.card h3 {{
    font-size: 1.2rem;
    font-weight: 600;
}}

.card p {{
    font-size: 0.95rem;
    color: var(--text-muted);
    line-height: 1.5;
}}

/* --- 3D LOADER SECTION --- */
.loader-section {{
    padding: 100px 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 24px;
    color: var(--text-muted);
}}

.loader {{
    width: 44px;
    height: 44px;
    border: 4px solid var(--accent);
    border-radius: 8px;
    /* Combined outset and inset shadows as per tutorial */
    box-shadow: 0 0 12px var(--accent), inset 0 0 12px var(--accent);
    animation: loader-spin 2s ease-in infinite;
}}

/* Video Tutorial's specific 3D keyframe sequence */
@keyframes loader-spin {{
    0%   {{ transform: rotateX(0deg) rotateY(0deg) rotateZ(0deg); }}
    33%  {{ transform: rotateX(180deg) rotateY(0deg) rotateZ(0deg); }}
    67%  {{ transform: rotateX(180deg) rotateY(180deg) rotateZ(0deg); }}
    100% {{ transform: rotateX(180deg) rotateY(180deg) rotateZ(180deg); }}
}}

/* Accessibility fallback */
@media (prefers-reduced-motion: reduce) {{
    .card-wrapper, .loader, .card {{
        animation: none !important;
        transition: none !important;
        transform: none !important;
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
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-window">
        <header class="hero">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </header>
        
        <div class="grid">
{cards_html}
        </div>

        <div class="loader-section">
            <div class="loader"></div>
            <p>Waiting for more data...</p>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Native CSS handles the scroll interactions and 3D rendering.
// This script ensures basic console reporting.
document.addEventListener('DOMContentLoaded', () => {
    console.log("CSS Scroll-Driven Components initialized successfully.");
    
    // Check for animation-timeline support warning
    if (!CSS.supports('animation-timeline: view()')) {
        console.warn("Notice: Your browser does not fully support 'animation-timeline: view()'. The elements will default to their fully visible states gracefully.");
    }
});
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
