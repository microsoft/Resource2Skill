def create_component(
    output_dir: str,
    title_text: str = "System Activity Monitor",
    body_text: str = "Demonstrating multi-stage CSS keyframes with spatial translation and color morphing.",
    color_scheme: str = "dark",
    accent_color: str = "#00bfff",
    width_px: int = 800,
    height_px: int = 500,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Multi-Stage Keyframe Animation.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0f172a"
        card_bg = "#1e293b"
        text_color = "#f8fafc"
        text_muted = "#94a3b8"
        track_bg = "#334155"
        # Animation spectrum colors (modernized from Red/Green/Blue/Yellow)
        c_start = accent_color
        c_mid1 = "#10b981" # Emerald
        c_mid2 = "#8b5cf6" # Violet
        c_mid3 = "#f59e0b" # Amber
    else:
        bg_color = "#f8fafc"
        card_bg = "#ffffff"
        text_color = "#0f172a"
        text_muted = "#64748b"
        track_bg = "#e2e8f0"
        c_start = accent_color
        c_mid1 = "#059669" 
        c_mid2 = "#6d28d9" 
        c_mid3 = "#d97706" 

    # === CSS ===
    css = f"""/* Continuous Multi-Stage Activity Pulse */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --card-bg: {card_bg};
    --text-color: {text_color};
    --text-muted: {text_muted};
    --track-bg: {track_bg};
    
    /* Animation Color Spectrum */
    --color-0: {c_start};
    --color-25: {c_mid1};
    --color-50: {c_mid2};
    --color-75: {c_mid3};
    --color-100: {c_start};
    
    --container-width: {width_px}px;
    --container-height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.widget-container {{
    width: 100%;
    max-width: var(--container-width);
    height: var(--container-height);
    background: var(--card-bg);
    border-radius: 24px;
    padding: 48px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 40px;
}}

.header {{
    text-align: center;
}}

.header h1 {{
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 12px;
    letter-spacing: -0.025em;
}}

.header p {{
    color: var(--text-muted);
    font-size: 1.1rem;
    line-height: 1.6;
}}

/* The Track */
.animation-track {{
    width: 100%;
    height: 80px;
    background: var(--track-bg);
    border-radius: 40px;
    position: relative;
    padding: 10px;
    /* Box shadow for depth */
    box-shadow: inset 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}}

/* The Animated Element */
.animated-node {{
    width: 60px;
    height: 60px;
    background-color: var(--color-0);
    border-radius: 50%;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -2px rgba(0, 0, 0, 0.15);
    
    /* 
       Applying the multi-stage animation:
       name: complexPath
       duration: 6s
       timing-function: ease-in-out
       delay: 0s
       iteration-count: infinite
       direction: normal (relies on keyframes to loop back)
    */
    animation: complexPath 6s ease-in-out infinite;
}}

/* Pause utility class toggled by JS */
.animated-node.paused {{
    animation-play-state: paused;
}}

/* 
  The Core Skill: Percentage-based Keyframes 
  Translating across the track while shifting colors.
  We use calc() to ensure it stays within the parent track relative to its own size.
*/
@keyframes complexPath {{
    0% {{
        transform: translateX(0);
        background-color: var(--color-0);
    }}
    25% {{
        /* Move 25% across the track */
        transform: translateX(calc((100vw * 0.25) - 40px)); /* fallback */
        transform: translateX(calc((var(--container-width) - 180px) * 0.25));
        background-color: var(--color-25);
    }}
    50% {{
        /* Max extension - move to the far right */
        transform: translateX(calc(var(--container-width) - 180px));
        background-color: var(--color-50);
    }}
    75% {{
        /* Return journey intermediate step */
        transform: translateX(calc((var(--container-width) - 180px) * 0.4));
        background-color: var(--color-75);
    }}
    100% {{
        /* Seamless return to origin */
        transform: translateX(0);
        background-color: var(--color-100);
    }}
}}

/* Controls */
.controls {{
    display: flex;
    justify-content: center;
    gap: 16px;
}}

button {{
    padding: 12px 24px;
    border-radius: 8px;
    border: none;
    background: var(--track-bg);
    color: var(--text-color);
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
}}

button:hover {{
    background: var(--color-50);
    color: white;
    transform: translateY(-2px);
}}

button:active {{
    transform: translateY(0);
}}

/* Responsive adjustments */
@media (max-width: 850px) {{
    .widget-container {{ width: 90%; padding: 32px; }}
    @keyframes complexPath {{
        0% {{ transform: translateX(0); background-color: var(--color-0); }}
        25% {{ transform: translateX(calc((90vw - 120px) * 0.25)); background-color: var(--color-25); }}
        50% {{ transform: translateX(calc(90vw - 120px)); background-color: var(--color-50); }}
        75% {{ transform: translateX(calc((90vw - 120px) * 0.4)); background-color: var(--color-75); }}
        100% {{ transform: translateX(0); background-color: var(--color-100); }}
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="widget-container">
        <header class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>

        <!-- The core animation staging area -->
        <div class="animation-track">
            <div class="animated-node" id="targetNode"></div>
        </div>

        <div class="controls">
            <button id="toggleBtn">Pause Animation</button>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Interactive Behavior for Multi-Stage Animation
document.addEventListener('DOMContentLoaded', () => {{
    const node = document.getElementById('targetNode');
    const toggleBtn = document.getElementById('toggleBtn');
    
    let isPlaying = true;

    // Toggle animation-play-state
    toggleBtn.addEventListener('click', () => {{
        if (isPlaying) {{
            node.classList.add('paused');
            toggleBtn.textContent = 'Play Animation';
        }} else {{
            node.classList.remove('paused');
            toggleBtn.textContent = 'Pause Animation';
        }}
        isPlaying = !isPlaying;
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
