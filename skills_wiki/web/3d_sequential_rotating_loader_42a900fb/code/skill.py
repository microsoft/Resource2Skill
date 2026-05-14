def create_component(
    output_dir: str,
    title_text: str = "Loading Data...",
    body_text: str = "Click the square to pause/play the animation.",
    color_scheme: str = "dark",
    accent_color: str = "#00FFFF",  # Defaulting to the 'aqua' from the tutorial
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Sequential Rotating Loader effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme colors based on color_scheme
    if color_scheme == "dark":
        bg_color = "#040716" # Match the specific deep blue/black from the video
        text_color = "#E2E8F0"
        card_bg = "rgba(255, 255, 255, 0.03)"
    else:
        bg_color = "#F8FAFC"
        text_color = "#0F172A"
        card_bg = "rgba(0, 0, 0, 0.03)"

    css = f"""/* 3D Sequential Rotating Loader */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --accent-color: {accent_color};
    --card-bg: {card_bg};
    --container-width: {width_px}px;
    --container-height: {height_px}px;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.widget-container {{
    width: var(--container-width);
    height: var(--container-height);
    background-color: var(--card-bg);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 40px;
    position: relative;
    box-shadow: 0 20px 40px rgba(0,0,0,0.2);
}}

.header {{
    text-align: center;
    z-index: 20;
}}

.title {{
    font-size: 1.5rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    margin-bottom: 8px;
}}

.subtitle {{
    font-size: 0.9rem;
    opacity: 0.7;
    font-weight: 300;
}}

/* === Core Loader Styles === */
.loader-wrapper {{
    perspective: 800px; /* Adds 3D perspective to the container */
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100px;
    height: 100px;
}}

.loading {{
    height: 50px;
    width: 50px;
    border: 6px solid var(--accent-color);
    border-radius: 4px;
    box-shadow: 
        0 0 8px var(--accent-color), 
        0 0 8px var(--accent-color) inset;
    z-index: 10;
    cursor: pointer;
    
    /* Animation Shorthand: duration | timing-function | iteration-count | name */
    animation: 2s ease-in-out infinite loading-sequence;
    
    /* Allows JS to pause/play */
    animation-play-state: running;
    transition: transform 0.2s, filter 0.2s;
}}

.loading:hover {{
    filter: brightness(1.3);
}}

/* === Keyframes Sequence === */
@keyframes loading-sequence {{
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

/* Play State indicator UI */
.status-badge {{
    margin-top: -10px;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    background: rgba(255,255,255,0.1);
    color: var(--text-color);
    transition: background 0.3s, color 0.3s;
}}

.status-badge.paused {{
    background: #EF4444; /* red */
    color: white;
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="widget-container">
        <div class="header">
            <h1 class="title">{title_text}</h1>
            <p class="subtitle">{body_text}</p>
        </div>
        
        <div class="loader-wrapper">
            <div class="loading" id="loader-cube" title="Click to Play/Pause" role="button" aria-label="Loading animation"></div>
        </div>

        <div class="status-badge" id="status">Running</div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""document.addEventListener('DOMContentLoaded', () => {{
    const loader = document.getElementById('loader-cube');
    const statusBadge = document.getElementById('status');

    // Toggle animation play state on click
    loader.addEventListener('click', () => {{
        // Get the computed style to check the current play state
        const currentState = window.getComputedStyle(loader).animationPlayState;
        
        if (currentState === 'running') {{
            loader.style.animationPlayState = 'paused';
            statusBadge.textContent = 'Paused';
            statusBadge.classList.add('paused');
        }} else {{
            loader.style.animationPlayState = 'running';
            statusBadge.textContent = 'Running';
            statusBadge.classList.remove('paused');
        }}
    }});
}});
"""

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
