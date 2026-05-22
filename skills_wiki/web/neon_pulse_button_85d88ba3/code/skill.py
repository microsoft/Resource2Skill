def create_component(
    output_dir: str,
    title_text: str = "Ready to Launch?",
    body_text: str = "Experience the next generation of interactive web components.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for left glow/border
    width_px: int = 1000,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Neon Pulse Button visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derived theme colors based on the scheme
    if color_scheme == "dark":
        bg_color = "#08080c"
        text_color = "#f0f0f0"
        btn_inner = "#0d0d12"
        btn_text = "#ffffff"
    else:
        bg_color = "#f4f4f6"
        text_color = "#1a1a2e"
        btn_inner = "#ffffff"
        btn_text = "#1a1a2e"

    # === CSS ===
    css = f"""/* Neon Pulse Button — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    
    /* Glow definitions */
    --glow-left: var(--accent);
    --glow-right: #ff0055; /* Complementary vibrant pink */
    
    /* Button internal styling */
    --btn-inner: {btn_inner};
    --btn-text: {btn_text};
    
    /* Container dimensions */
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

.container {{
    width: var(--width);
    height: var(--height);
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.content {{
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 4rem;
}}

.title {{
    font-size: 3.5rem;
    font-weight: 700;
    letter-spacing: -0.02em;
}}

.body-text {{
    font-size: 1.2rem;
    opacity: 0.7;
    max-width: 500px;
    margin-top: -2.5rem;
    line-height: 1.6;
}}

/* ========================================= */
/* NEON BUTTON CORE                          */
/* ========================================= */

.neon-btn-container {{
    position: relative;
    display: inline-block;
}}

/* Ambient Background Glows */
.glow-left, .glow-right {{
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    width: 70%;
    height: 140%;
    filter: blur(40px);
    z-index: -1;
    opacity: 0.4;
    transition: all 0.5s cubic-bezier(0.25, 1, 0.5, 1);
}}

.glow-left {{
    left: -15%;
    background: var(--glow-left);
}}

.glow-right {{
    right: -15%;
    background: var(--glow-right);
}}

/* Hover interaction on ambient glows */
.neon-btn-container:hover .glow-left,
.neon-btn-container:hover .glow-right {{
    opacity: 0.7;
    filter: blur(50px);
}}

/* Click interaction on ambient glows */
.neon-btn-container.clicked .glow-left,
.neon-btn-container.clicked .glow-right {{
    opacity: 1;
    filter: blur(60px);
    transform: translateY(-50%) scale(1.15);
}}

/* Physical Button Element */
.neon-btn {{
    position: relative;
    padding: 22px 64px;
    background: transparent;
    border: none;
    border-radius: 100px;
    cursor: pointer;
    outline: none;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    transition: transform 0.2s cubic-bezier(0.25, 1, 0.5, 1);
    -webkit-tap-highlight-color: transparent;
}}

/* Button Layer Logic */
.neon-btn-border,
.neon-btn-highlight,
.neon-btn-bg {{
    position: absolute;
    border-radius: 100px;
    pointer-events: none;
}}

/* 1. The Gradient Border (slightly larger than button) */
.neon-btn-border {{
    top: -2px; left: -2px; right: -2px; bottom: -2px;
    background: linear-gradient(90deg, var(--glow-left), var(--glow-right));
    z-index: 1;
}}

/* 2. Sweeping Light Highlight (only visible on hover) */
.neon-btn-highlight {{
    top: -2px; left: -2px; right: -2px; bottom: -2px;
    background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.9) 50%, transparent 100%);
    z-index: 2;
    background-size: 300% 100%;
    opacity: 0;
    transition: opacity 0.3s ease;
}}

/* 3. Solid Inner Fill (carves out the border) */
.neon-btn-bg {{
    top: 0; left: 0; right: 0; bottom: 0;
    background: var(--btn-inner);
    z-index: 3;
    transition: opacity 0.3s ease;
}}

/* 4. Button Text */
.neon-btn-text {{
    position: relative;
    z-index: 4;
    color: var(--btn-text);
    font-size: 1.5rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    pointer-events: none;
    transition: color 0.3s ease, text-shadow 0.3s ease;
}}

/* ========================================= */
/* HOVER & CLICK STATE LOGIC                 */
/* ========================================= */

.neon-btn-container:hover .neon-btn-highlight {{
    opacity: 1;
    animation: border-sweep 2s infinite linear;
}}

@keyframes border-sweep {{
    0% {{ background-position: 100% 0; }}
    100% {{ background-position: 0% 0; }}
}}

.neon-btn-container.clicked .neon-btn {{
    transform: scale(0.96);
}}

/* Fading out the inner bg reveals the gradient border spanning the whole button */
.neon-btn-container.clicked .neon-btn-bg {{
    opacity: 0; 
}}

.neon-btn-container.clicked .neon-btn-text {{
    color: #ffffff;
    text-shadow: 0 0 10px rgba(255,255,255,0.6);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="content">
            <h1 class="title">{title_text}</h1>
            {f'<p class="body-text">{body_text}</p>' if body_text else ''}
            
            <div class="neon-btn-container">
                <div class="glow-left"></div>
                <div class="glow-right"></div>
                
                <button class="neon-btn" aria-label="Blast off interaction">
                    <!-- Component Layers -->
                    <span class="neon-btn-border"></span>
                    <span class="neon-btn-highlight"></span>
                    <span class="neon-btn-bg"></span>
                    
                    <!-- Text Layer -->
                    <span class="neon-btn-text">Blast off!</span>
                </button>
            </div>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Neon Pulse Button — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const container = document.querySelector('.neon-btn-container');
    const btn = document.querySelector('.neon-btn');

    btn.addEventListener('click', () => {{
        // Prevent re-triggering while animation is playing
        if (container.classList.contains('clicked')) return;
        
        // Trigger the visual fill state
        container.classList.add('clicked');
        
        // Remove the state after 1.2 seconds to allow clicking again
        setTimeout(() => {{
            container.classList.remove('clicked');
        }}, 1200);
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
