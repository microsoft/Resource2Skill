def create_component(
    output_dir: str,
    title_text: str = "Glassmorphism Component",
    body_text: str = "This component demonstrates the proper implementation of the glassmorphism effect using backdrop-filter and semi-transparent RGBA backgrounds. Move your mouse to see the refraction.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1000,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Advanced Glassmorphism effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Helper to convert hex to RGB string for CSS
    def hex_to_rgb_str(hex_code):
        hex_code = hex_code.lstrip('#')
        if len(hex_code) == 3:
            hex_code = ''.join(c + c for c in hex_code)
        r, g, b = tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))
        return f"{r}, {g}, {b}"

    accent_rgb = hex_to_rgb_str(accent_color)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_base = "#0d111c"
        text_color = "#ffffff"
        text_muted = "rgba(255, 255, 255, 0.7)"
        glass_bg = "linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.02) 100%)"
        glass_border = "rgba(255, 255, 255, 0.15)"
        glass_shadow = "rgba(0, 0, 0, 0.4)"
        blob_color_2 = "88, 28, 235" # secondary purple
    else:
        bg_base = "#e2e8f0"
        text_color = "#0f172a"
        text_muted = "rgba(15, 23, 42, 0.7)"
        glass_bg = "linear-gradient(135deg, rgba(255, 255, 255, 0.5) 0%, rgba(255, 255, 255, 0.2) 100%)"
        glass_border = "rgba(255, 255, 255, 0.6)"
        glass_shadow = "rgba(0, 0, 0, 0.1)"
        blob_color_2 = "255, 180, 50" # secondary orange/yellow

    # Escape HTML inputs
    import html as html_lib
    title_text = html_lib.escape(title_text)
    body_text = html_lib.escape(body_text)

    # === CSS ===
    css = f"""/* Glassmorphism — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-base: {bg_base};
    --text-primary: {text_color};
    --text-muted: {text_muted};
    --glass-bg: {glass_bg};
    --glass-border: {glass_border};
    --glass-shadow: {glass_shadow};
    --accent-rgb: {accent_rgb};
    --secondary-rgb: {blob_color_2};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg-base);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.scene-container {{
    width: var(--width);
    height: var(--height);
    position: relative;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--bg-base);
    border-radius: 12px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}}

/* Dynamic Background Elements to show off the blur */
.bg-blobs {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1;
    pointer-events: none;
}}

.blob {{
    position: absolute;
    border-radius: 50%;
    filter: blur(60px);
    opacity: 0.7;
    transition: transform 0.2s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}}

.blob-1 {{
    width: 300px;
    height: 300px;
    background: rgba(var(--accent-rgb), 0.8);
    top: -50px;
    left: 10%;
    animation: float 8s ease-in-out infinite alternate;
}}

.blob-2 {{
    width: 400px;
    height: 400px;
    background: rgba(var(--secondary-rgb), 0.6);
    bottom: -100px;
    right: 5%;
    animation: float 12s ease-in-out infinite alternate-reverse;
}}

.blob-3 {{
    width: 250px;
    height: 250px;
    background: rgba(var(--accent-rgb), 0.5);
    bottom: 20%;
    left: 20%;
    animation: float 10s ease-in-out infinite alternate;
}}

/* The Core Glass Component */
.glass-card {{
    position: relative;
    z-index: 10;
    width: 90%;
    max-width: 500px;
    padding: 48px;
    
    /* Level 2 & 3 Technique: Semi-transparent background */
    background: var(--glass-bg);
    
    /* Level 1 & 2 Technique: The Blur (with Safari prefix) */
    -webkit-backdrop-filter: blur(24px);
    backdrop-filter: blur(24px);
    
    /* Physical characteristics */
    border-radius: 24px;
    border: 1px solid var(--glass-border);
    border-top: 1px solid rgba(255, 255, 255, 0.4); /* Highlight edge */
    border-left: 1px solid rgba(255, 255, 255, 0.3); /* Highlight edge */
    box-shadow: 0 16px 40px var(--glass-shadow);
    
    /* Inner Layout */
    display: flex;
    flex-direction: column;
    gap: 20px;
    transform: translateY(0);
    transition: transform 0.4s ease, box-shadow 0.4s ease;
}}

.glass-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 25px 50px var(--glass-shadow);
}}

.card-title {{
    font-size: 28px;
    font-weight: 700;
    letter-spacing: -0.5px;
    line-height: 1.2;
}}

.card-body {{
    font-size: 16px;
    font-weight: 400;
    line-height: 1.6;
    color: var(--text-muted);
}}

.card-action {{
    margin-top: 12px;
    padding: 12px 24px;
    background: rgba(var(--accent-rgb), 0.9);
    color: #fff;
    border: none;
    border-radius: 8px;
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
    align-self: flex-start;
    transition: background 0.3s ease, transform 0.2s ease;
    box-shadow: 0 4px 12px rgba(var(--accent-rgb), 0.4);
}}

.card-action:hover {{
    background: rgba(var(--accent-rgb), 1);
    transform: translateY(-2px);
}}

/* Keyframes for ambient blob movement */
@keyframes float {{
    0% {{ transform: translate(0, 0) scale(1); }}
    33% {{ transform: translate(30px, -50px) scale(1.1); }}
    66% {{ transform: translate(-20px, 20px) scale(0.9); }}
    100% {{ transform: translate(0, 0) scale(1); }}
}}
"""

    # === HTML ===
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Glassmorphism Component</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="scene-container">
        
        <!-- Background elements to be blurred by the glass -->
        <div class="bg-blobs">
            <div class="blob blob-1"></div>
            <div class="blob blob-2"></div>
            <div class="blob blob-3"></div>
        </div>

        <!-- The Glass Panel -->
        <div class="glass-card">
            <h1 class="card-title">{title_text}</h1>
            <p class="card-body">{body_text}</p>
            <button class="card-action">Learn More</button>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Parallax / Interactive mouse tracking for the background blobs
// This accentuates the real-time calculation of the backdrop-filter.

document.addEventListener('DOMContentLoaded', () => {{
    const container = document.querySelector('.scene-container');
    const blobs = document.querySelectorAll('.blob');

    if (!container || blobs.length === 0) return;

    container.addEventListener('mousemove', (e) => {{
        // Calculate mouse position relative to center of container
        const rect = container.getBoundingClientRect();
        const x = e.clientX - rect.left - (rect.width / 2);
        const y = e.clientY - rect.top - (rect.height / 2);

        // Apply slight parallax movement to blobs
        blobs.forEach((blob, index) => {{
            // Different blobs move at different speeds
            const speed = (index + 1) * 0.05; 
            const moveX = x * speed;
            const moveY = y * speed;
            
            // We use JS to update a transform offset alongside the CSS animation
            blob.style.transform = `translate(${{moveX}}px, ${{moveY}}px)`;
        }});
    }});

    // Reset position when mouse leaves
    container.addEventListener('mouseleave', () => {{
        blobs.forEach(blob => {{
            blob.style.transform = `translate(0px, 0px)`;
        }});
    }});
}});
"""

    # === Write files ===
    files = []
    for fname, content in [("index.html", html_content), ("style.css", css), ("script.js", js)]:
        path = os.path.join(output_dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        files.append(path)

    return {
        "html": html_content,
        "css": css,
        "js": js,
        "files": files,
    }
