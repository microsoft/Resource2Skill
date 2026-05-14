def create_component(
    output_dir: str,
    title_text: str = "Glassmorphism",
    body_text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Dicta sapiente illo ut rerum at nemo in sed cupiditate Odio voluptatum excepturi.",
    color_scheme: str = "light",       # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent text/highlights
    width_px: int = 400,
    height_px: int = 500,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Glassmorphism Card visual effect.
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        # Deep space / oceanic gradient to show off blur
        page_bg = "linear-gradient(135deg, #0f2027, #203a43, #2c5364)"
        text_color = "#ffffff"
        glass_bg = "rgba(13, 17, 28, 0.25)"
        border_top = "rgba(255, 255, 255, 0.15)"
        border_left = "rgba(255, 255, 255, 0.05)"
        shadow = "rgba(0, 0, 0, 0.3)"
    else:
        # Vibrant pastel gradient to show off blur
        page_bg = "linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%)"
        text_color = "#1a1a2e"
        glass_bg = "rgba(255, 255, 255, 0.25)"
        border_top = "rgba(255, 255, 255, 0.6)"
        border_left = "rgba(255, 255, 255, 0.3)"
        shadow = "rgba(0, 0, 0, 0.05)"

    # Escape HTML strings
    import html as html_lib
    safe_title = html_lib.escape(title_text)
    safe_body = html_lib.escape(body_text)

    # === CSS ===
    css = f"""/* Glassmorphism Card Overlay — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --text-color: {text_color};
    --accent: {accent_color};
    --glass-bg: {glass_bg};
    --border-top: {border_top};
    --border-left: {border_left};
    --shadow: {shadow};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: {page_bg};
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    perspective: 1000px; /* For 3D tilt effect */
}}

@keyframes gradientBG {{
    0% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}

/* Decorative background elements to enhance the glass blur visibility */
.circle {{
    position: absolute;
    border-radius: 50%;
    filter: blur(40px);
    z-index: -1;
}}

.circle-1 {{
    width: 300px;
    height: 300px;
    background: var(--accent);
    top: 15%;
    left: 25%;
    opacity: 0.6;
}}

.circle-2 {{
    width: 400px;
    height: 400px;
    background: #ff007f;
    bottom: 10%;
    right: 20%;
    opacity: 0.4;
}}

/* Core Glassmorphism Component */
.glass-container {{
    width: 100%;
    max-width: var(--width);
    min-height: var(--height);
    padding: 40px;
    
    /* Center text like the video */
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    
    /* The Glass Effect */
    background: var(--glass-bg);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    
    /* Edges and shape */
    border-radius: 30px;
    border-top: 1px solid var(--border-top);
    border-left: 1px solid var(--border-left);
    
    /* Soft shadow */
    box-shadow: 10px 10px 30px var(--shadow);
    
    /* Animation / Interaction state */
    transition: transform 0.1s ease-out;
    transform-style: preserve-3d;
}}

.glass-container h1 {{
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 20px;
    letter-spacing: -0.5px;
    color: var(--text-color);
}}

.glass-container p {{
    font-size: 1.1rem;
    line-height: 1.6;
    opacity: 0.9;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <!-- Background decorations for better glass visibility -->
    <div class="circle circle-1"></div>
    <div class="circle circle-2"></div>

    <!-- Main Component -->
    <div class="glass-container">
        <h1>{safe_title}</h1>
        <p>{safe_body}</p>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Glassmorphism - 3D Tilt Interaction
document.addEventListener('DOMContentLoaded', () => {{
    const container = document.querySelector('.glass-container');
    const body = document.querySelector('body');

    // Subtle 3D tilt effect on mouse move
    body.addEventListener('mousemove', (e) => {{
        // Calculate mouse position relative to the center of the screen
        const xAxis = (window.innerWidth / 2 - e.pageX) / 40;
        const yAxis = (window.innerHeight / 2 - e.pageY) / 40;
        
        // Apply rotation to the glass container
        container.style.transform = `rotateY(${{xAxis}}deg) rotateX(${{yAxis}}deg)`;
    }});

    // Reset transform when mouse leaves window
    body.addEventListener('mouseleave', () => {{
        container.style.transform = `rotateY(0deg) rotateX(0deg)`;
        container.style.transition = `transform 0.5s ease`;
    }});

    // Remove transition during movement for snappy response
    body.addEventListener('mouseenter', () => {{
        container.style.transition = `none`;
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
