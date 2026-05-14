def create_component(
    output_dir: str,
    title_text: str = "System Processing",
    body_text: str = "Establishing secure connection to the server...",
    color_scheme: str = "light",        # "dark" or "light"
    accent_color: str = "#5c89ff",     # Base color of the pulsing dots
    width_px: int = 800,
    height_px: int = 500,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Neumorphic Sequential Pulse Loader.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors for Neumorphism ===
    if color_scheme == "dark":
        bg_color = "#2a2b2f"
        text_color = "#e0e0e0"
        shadow_light = "rgba(255, 255, 255, 0.05)"
        shadow_dark = "rgba(0, 0, 0, 0.6)"
        inner_shadow_light = "rgba(255, 255, 255, 0.1)"
        inner_shadow_dark = "rgba(0, 0, 0, 0.4)"
    else:
        bg_color = "#eaeef0"
        text_color = "#666666"
        shadow_light = "rgba(255, 255, 255, 1)"
        shadow_dark = "rgba(0, 0, 0, 0.15)"
        inner_shadow_light = "rgba(255, 255, 255, 0.8)"
        inner_shadow_dark = "rgba(0, 0, 0, 0.2)"

    # === CSS ===
    css = f"""/* Neumorphic Sequential Pulse Loader */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --shadow-light: {shadow_light};
    --shadow-dark: {shadow_dark};
    --inner-light: {inner_shadow_light};
    --inner-dark: {inner_shadow_dark};
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
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 60px;
}}

.text-content {{
    text-align: center;
}}

.title {{
    font-size: 24px;
    font-weight: 600;
    margin-bottom: 12px;
    letter-spacing: 1px;
}}

.body-text {{
    font-size: 15px;
    opacity: 0.8;
}}

/* Loader Core Styles */
.loader {{
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 24px;
}}

.loader span {{
    position: relative;
    width: 50px;
    height: 50px;
    background: var(--bg);
    border-radius: 50%;
    border: 6px solid var(--bg);
    /* The Neumorphic Magic: Outset for the rim, Inset for the crater */
    box-shadow: 
        -8px -8px 15px var(--shadow-light),
        8px 8px 15px var(--shadow-dark),
        inset 3px 3px 5px var(--shadow-dark),
        inset -1px -1px 5px var(--shadow-light);
}}

.loader span::before {{
    content: '';
    position: absolute;
    inset: 0; /* Fills the inside of the border perfectly */
    border-radius: inherit;
    background: var(--accent);
    /* Gives the inner dot a slight 3D spherical feel */
    box-shadow: 
        inset 3px 3px 5px var(--inner-dark),
        inset -1px -1px 5px var(--inner-light);
    transform: scale(0);
    
    /* 4s duration gives enough time for the wave to complete across 7 nodes */
    animation: 
        pulseWave 4s cubic-bezier(0.4, 0, 0.2, 1) infinite,
        colorCycle 6s linear infinite;
    
    /* The core staggering mechanic */    
    animation-delay: calc(var(--i) * 0.2s);
}}

/* Pop in, hold, and pop out smoothly */
@keyframes pulseWave {{
    0%, 5% {{ transform: scale(0); }}
    15%, 70% {{ transform: scale(1); }}
    80%, 100% {{ transform: scale(0); }}
}}

/* Continuous color shift */
@keyframes colorCycle {{
    0% {{ filter: hue-rotate(0deg); }}
    100% {{ filter: hue-rotate(360deg); }}
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="text-content">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
        
        <div class="loader">
            <!-- Inline CSS variables drive the staggered animation delay -->
            <span style="--i:0;"></span>
            <span style="--i:1;"></span>
            <span style="--i:2;"></span>
            <span style="--i:3;"></span>
            <span style="--i:4;"></span>
            <span style="--i:5;"></span>
            <span style="--i:6;"></span>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    # For this specific component, no JS is required for the visual effect.
    # It is included to satisfy the output format requirements.
    js = f"""// Neumorphic Loader Logic
document.addEventListener('DOMContentLoaded', () => {{
    // The visual mechanics are handled entirely by CSS variables and keyframes.
    console.log("Neumorphic Loader Initialized.");
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
