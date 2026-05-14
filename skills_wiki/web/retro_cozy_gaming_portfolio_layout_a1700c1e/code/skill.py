def create_component(
    output_dir: str,
    title_text: str = "Nashallery: Creative Development",
    body_text: str = "Founded by a creative coding community of 515,000+ learners. We create playful, design-forward software projects and tutorials that make coding fun, feminine, and accessible.",
    color_scheme: str = "light",       # "dark" or "light"
    accent_color: str = "#d8b4e2",     # Pastel purple/pink
    width_px: int = 900,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Retro "Cozy Gaming" Portfolio layout.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#1a1829"
        text_color = "#f4eef7"
        text_muted = "#b8b2c1"
        surface_color = "rgba(255, 255, 255, 0.05)"
        divider_color = "rgba(255, 255, 255, 0.1)"
        tag_bg = accent_color
        tag_text = "#1a1829"
    else:
        bg_color = "#fdfbfd"
        text_color = "#2d2a32"
        text_muted = "#5e5b66"
        surface_color = "rgba(0, 0, 0, 0.02)"
        divider_color = "rgba(0, 0, 0, 0.08)"
        tag_bg = accent_color
        tag_text = "#2d2a32"

    # === CSS ===
    css = f"""/* Retro Cozy Portfolio Component */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=VT323&display=swap');

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --surface: {surface_color};
    --divider: {divider_color};
    --tag-bg: {tag_bg};
    --tag-text: {tag_text};
    --max-width: {width_px}px;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
    padding: 40px 20px;
}}

.container {{
    max-width: var(--max-width);
    margin: 0 auto;
}}

/* Header Section */
.site-header {{
    margin-bottom: 40px;
}}

.site-title {{
    font-family: 'VT323', monospace;
    font-size: 2.8rem;
    font-weight: 400;
    margin-bottom: 20px;
    letter-spacing: 0.5px;
}}

.site-description {{
    font-size: 1.05rem;
    color: var(--text-muted);
    max-width: 85%;
}}

.site-description strong {{
    color: var(--text);
    font-weight: 600;
}}

.divider {{
    height: 1px;
    background-color: var(--divider);
    width: 100%;
    margin: 40px 0;
}}

/* Projects Section */
.project {{
    margin-bottom: 80px;
    cursor: pointer;
    transition: transform 0.2s ease;
}}

.project:hover .project-title {{
    text-decoration: underline;
    text-decoration-thickness: 2px;
    text-underline-offset: 4px;
}}

.project-header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin-bottom: 12px;
}}

.project-title {{
    font-family: 'VT323', monospace;
    font-size: 2rem;
    font-weight: 400;
}}

.project-tag {{
    font-family: 'VT323', monospace;
    background-color: var(--tag-bg);
    color: var(--tag-text);
    padding: 4px 12px;
    border-radius: 4px;
    font-size: 1.1rem;
    text-transform: lowercase;
}}

.project-desc {{
    font-size: 1rem;
    color: var(--text-muted);
    margin-bottom: 24px;
}}

/* Styled Media Placeholder (Simulating the animated game screens from the tutorial) */
.project-media {{
    width: 100%;
    height: 450px;
    background: linear-gradient(135deg, var(--surface) 0%, var(--divider) 100%);
    border-radius: 12px;
    border: 2px solid var(--divider);
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
}}

/* Simulated game screen 1 */
.media-1 {{
    background: linear-gradient(180deg, #ffccfc 0%, #a2d2ff 100%);
}}
.media-1::after {{
    content: 'STUDY SODA\\A [ Playing ]';
    white-space: pre;
    font-family: 'VT323', monospace;
    text-align: center;
    color: #fff;
    font-size: 2rem;
    text-shadow: 2px 2px 0px rgba(0,0,0,0.2);
    animation: float 3s ease-in-out infinite;
}}

/* Simulated game screen 2 */
.media-2 {{
    background: linear-gradient(180deg, #ffd6a5 0%, #fdffb6 100%);
}}
.media-2::after {{
    content: 'EGG TIMER\\A 02:59';
    white-space: pre;
    font-family: 'VT323', monospace;
    text-align: center;
    color: #ff9f1c;
    font-size: 2rem;
    animation: pulse 1s infinite alternate;
}}

@keyframes float {{
    0% {{ transform: translateY(0px); }}
    50% {{ transform: translateY(-10px); }}
    100% {{ transform: translateY(0px); }}
}}

@keyframes pulse {{
    0% {{ opacity: 0.7; }}
    100% {{ opacity: 1; }}
}}

/* Responsive */
@media (max-width: 600px) {{
    .site-title {{
        font-size: 2.2rem;
    }}
    .site-description {{
        max-width: 100%;
    }}
    .project-header {{
        flex-direction: column;
        align-items: flex-start;
        gap: 8px;
    }}
    .project-media {{
        height: 300px;
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
    <div class="container">
        
        <header class="site-header">
            <h1 class="site-title">{title_text}</h1>
            <p class="site-description">{body_text}</p>
        </header>

        <div class="divider"></div>

        <main class="projects-list">
            
            <!-- Project 1 -->
            <article class="project" data-link="https://github.com">
                <div class="project-header">
                    <h2 class="project-title">Study Soda</h2>
                    <span class="project-tag">desktop game</span>
                </div>
                <p class="project-desc">An interactive "study until the ice melts" timer built with Godot. Featured on official design accounts.</p>
                <div class="project-media media-1"></div>
            </article>

            <!-- Project 2 -->
            <article class="project" data-link="https://github.com">
                <div class="project-header">
                    <h2 class="project-title">Egg Timer</h2>
                    <span class="project-tag">desktop widget</span>
                </div>
                <p class="project-desc">Cooking timer desktop widget built with ElectronJS. The product video has over 43 million views.</p>
                <div class="project-media media-2"></div>
            </article>

        </main>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Retro Portfolio Interactive Behavior

document.addEventListener('DOMContentLoaded', () => {{
    // 1. Smooth scroll setup (global)
    document.documentElement.style.scrollBehavior = 'smooth';

    // 2. Make project blocks clickable via data-link attribute
    const projects = document.querySelectorAll('.project');
    
    projects.forEach(project => {{
        project.addEventListener('click', (e) => {{
            const url = project.getAttribute('data-link');
            if (url) {{
                // Open link in a new tab (simulating the tutorial's behavior)
                window.open(url, '_blank', 'noopener,noreferrer');
            }}
        }});
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
