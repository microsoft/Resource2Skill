def create_component(
    output_dir: str,
    title_text: str = "Split Layout",
    body_text: str = "Interactive Web Experience",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#e63946",     # CSS hex color for accent (defaults to an energetic red)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Split-Screen Layout.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_color = "#f8fafc"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"

    # === CSS ===
    css = f"""/* Responsive Split-Screen Layout — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: #000;
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.split-container {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    display: flex;
    flex-direction: column; /* Mobile first: vertically stacked */
    position: relative;
    overflow: hidden;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.4);
}}

@media (min-width: 768px) {{
    .split-container {{
        flex-direction: row; /* Desktop: side-by-side */
    }}
}}

/* Individual Panes */
.pane {{
    flex: 1; /* Takes exactly equal space */
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 2rem;
    text-align: center;
    cursor: pointer;
    transition: flex 0.5s cubic-bezier(0.16, 1, 0.3, 1), background-color 0.3s ease;
}}

.pane-left {{
    background-color: var(--bg);
    color: var(--text);
}}

.pane-right {{
    background-color: var(--accent);
    color: #ffffff; /* Assuming accent is vibrant, white text ensures contrast */
}}

/* Hover interaction: Expands the hovered side on desktop */
@media (min-width: 768px) {{
    .split-container:hover .pane {{
        flex: 1; 
    }}
    .split-container .pane:hover {{
        flex: 1.15;
    }}
}}

/* Typography */
.pane-title {{
    font-size: 1.5rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
    transition: transform 0.3s ease;
}}

.pane-desc {{
    font-size: 0.95rem;
    opacity: 0.7;
    max-width: 250px;
    line-height: 1.5;
}}

.pane:hover .pane-title {{
    transform: translateY(-5px);
}}

/* Central absolute branding element (Inspiration from video intro) */
.center-brand {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 10;
    pointer-events: none; /* Let clicks pass through to panes */
    color: #ffffff;
    mix-blend-mode: difference; /* Creates striking contrast across the boundary */
    font-size: clamp(2rem, 5vw, 3.5rem);
    font-weight: 800;
    letter-spacing: -0.02em;
    text-align: center;
    white-space: nowrap;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="split-container">
        
        <!-- Central Absolute Overlay -->
        <div class="center-brand">{title_text}</div>

        <!-- Left Pane -->
        <div class="pane pane-left">
            <h2 class="pane-title">Left Side</h2>
            <p class="pane-desc">Discover the simple desktop experience.</p>
        </div>

        <!-- Right Pane -->
        <div class="pane pane-right">
            <h2 class="pane-title">Right Side</h2>
            <p class="pane-desc">{body_text}</p>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Split-Screen Layout — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const panes = document.querySelectorAll('.pane');

    // Optional: Add click handlers to panes for demonstration
    panes.forEach(pane => {{
        pane.addEventListener('click', () => {{
            const side = pane.classList.contains('pane-left') ? 'Left' : 'Right';
            console.log(`Navigating to ${{side}} side content...`);
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
