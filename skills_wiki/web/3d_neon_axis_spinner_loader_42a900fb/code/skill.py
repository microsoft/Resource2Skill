def create_component(
    output_dir: str,
    title_text: str = "Processing Data",
    body_text: str = "Please wait while we initialize the environment.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00ffff",     # CSS hex color for accent (aqua/cyan)
    width_px: int = 800,
    height_px: int = 500,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Neon Axis Spinner Loader.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os
    import html as html_lib

    os.makedirs(output_dir, exist_ok=True)

    # Escape text to prevent XSS and formatting issues
    safe_title = html_lib.escape(title_text)
    safe_body = html_lib.escape(body_text)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#040716"
        text_color = "#ffffff"
        surface_color = "rgba(255, 255, 255, 0.03)"
        btn_bg = "rgba(255, 255, 255, 0.08)"
        btn_hover = "rgba(255, 255, 255, 0.15)"
        border_color = "rgba(255, 255, 255, 0.1)"
    else:
        bg_color = "#f0f2f5"
        text_color = "#0a0c10"
        surface_color = "#ffffff"
        btn_bg = "rgba(0, 0, 0, 0.05)"
        btn_hover = "rgba(0, 0, 0, 0.1)"
        border_color = "rgba(0, 0, 0, 0.1)"

    # === CSS ===
    css = f"""/* 3D Neon Axis Spinner — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --btn-bg: {btn_bg};
    --btn-hover: {btn_hover};
    --border: {border_color};
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

.widget-container {{
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    max-height: 90vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 3rem 2rem;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
}}

/* === Core Animation Visuals === */
.loader-wrapper {{
    /* Adding perspective adds deeper 3D illusion to the tumbling */
    perspective: 800px; 
    margin-bottom: 2.5rem;
}}

.loader {{
    width: 50px;
    height: 50px;
    border: 6px solid var(--accent);
    border-radius: 4px;
    /* Simultaneous outer and inner glow */
    box-shadow: 0 0 12px var(--accent), inset 0 0 12px var(--accent);
    
    /* The core tumbling animation */
    animation: axis-spin 2.4s ease-in-out infinite;
    
    /* Hardware acceleration hint */
    will-change: transform;
}}

@keyframes axis-spin {{
    0% {{
        transform: rotateX(0deg) rotateY(0deg) rotateZ(0deg);
    }}
    33% {{
        transform: rotateX(180deg) rotateY(0deg) rotateZ(0deg);
    }}
    67% {{
        transform: rotateX(180deg) rotateY(180deg) rotateZ(0deg);
    }}
    100% {{
        transform: rotateX(180deg) rotateY(180deg) rotateZ(180deg);
    }}
}}

/* Typography & Controls */
.title {{
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 0.75rem;
    letter-spacing: 0.5px;
    text-align: center;
}}

.body-text {{
    font-size: 1rem;
    color: var(--text);
    opacity: 0.7;
    margin-bottom: 2.5rem;
    text-align: center;
    max-width: 80%;
    line-height: 1.5;
}}

.controls button {{
    background: var(--btn-bg);
    color: var(--text);
    border: 1px solid var(--border);
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    font-size: 0.9rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    gap: 8px;
}}

.controls button:hover {{
    background: var(--btn-hover);
    border-color: var(--accent);
    box-shadow: 0 0 8px rgba(0, 255, 255, 0.2);
}}

.controls button:active {{
    transform: scale(0.96);
}}

.controls button .indicator {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--accent);
    box-shadow: 0 0 6px var(--accent);
    transition: background 0.3s;
}}

.controls button.paused .indicator {{
    background: #ff4757;
    box-shadow: 0 0 6px #ff4757;
}}

/* A11y: Reduce motion preference */
@media (prefers-reduced-motion: reduce) {{
    .loader {{
        animation: pulse 2s ease-in-out infinite;
    }}
    
    @keyframes pulse {{
        0%, 100% {{ opacity: 1; transform: scale(1); }}
        50% {{ opacity: 0.5; transform: scale(0.95); }}
    }}
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="widget-container">
        
        <div class="loader-wrapper">
            <div class="loader" id="spinner" role="status" aria-label="Loading animation"></div>
        </div>
        
        <h1 class="title">{safe_title}</h1>
        <p class="body-text">{safe_body}</p>
        
        <div class="controls">
            <button id="togglePlayBtn" aria-pressed="false">
                <span class="indicator"></span>
                <span id="btnText">Pause Animation</span>
            </button>
        </div>

    </main>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// 3D Neon Axis Spinner — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const spinner = document.getElementById('spinner');
    const toggleBtn = document.getElementById('togglePlayBtn');
    const btnText = document.getElementById('btnText');
    
    let isRunning = true;

    toggleBtn.addEventListener('click', () => {{
        if (isRunning) {{
            // Pause the CSS animation exactly where it currently is
            spinner.style.animationPlayState = 'paused';
            
            // Update UI
            btnText.textContent = 'Resume Animation';
            toggleBtn.classList.add('paused');
            toggleBtn.setAttribute('aria-pressed', 'true');
        }} else {{
            // Resume the CSS animation
            spinner.style.animationPlayState = 'running';
            
            // Update UI
            btnText.textContent = 'Pause Animation';
            toggleBtn.classList.remove('paused');
            toggleBtn.setAttribute('aria-pressed', 'false');
        }}
        
        isRunning = !isRunning;
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
