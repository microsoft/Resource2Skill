def create_component(
    output_dir: str,
    title_text: str = "Keyframe Choreography",
    body_text: str = "Hover over this card to pause the animation. Click the button to reverse the orbital direction using JavaScript.",
    color_scheme: str = "dark",
    accent_color: str = "#00ea8b",
    width_px: int = 400,
    height_px: int = 400,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Multi-Stage Orbital Keyframe effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#080b12"
        surface_color = "#121826"
        border_color = "#202838"
        text_primary = "#ffffff"
        text_secondary = "#94a3b8"
    else:
        bg_color = "#f1f5f9"
        surface_color = "#ffffff"
        border_color = "#e2e8f0"
        text_primary = "#0f172a"
        text_secondary = "#475569"

    # Define the travel distance based on dimensions
    travel_x = int(width_px * 0.75)
    travel_y = int(height_px * 0.75)

    css = f"""/* Keyframe Choreography — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --surface-color: {surface_color};
    --border-color: {border_color};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --accent-color: {accent_color};
    --card-width: {width_px}px;
    --card-height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.card-container {{
    position: relative;
    width: var(--card-width);
    height: var(--card-height);
    background-color: var(--surface-color);
    border: 1px solid var(--border-color);
    border-radius: 24px;
    padding: 40px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    overflow: hidden;
    z-index: 1;
}}

.content {{
    z-index: 10;
    pointer-events: none;
}}

h1 {{
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 12px;
    letter-spacing: -0.025em;
}}

p {{
    font-size: 0.95rem;
    color: var(--text-secondary);
    line-height: 1.6;
    max-width: 80%;
    margin: 0 auto;
}}

/* The Animated Element */
.orbiter {{
    position: absolute;
    top: 20px;
    left: 20px;
    width: 40px;
    height: 40px;
    background-color: var(--accent-color);
    border-radius: 50%;
    box-shadow: 0 0 20px var(--accent-color), 0 0 40px var(--accent-color);
    
    /* Animation Shorthand: name | duration | timing-function | delay | iteration-count | direction | fill-mode */
    animation: squarePath 4s ease-in-out 0s infinite normal both;
    z-index: 5;
}}

/* Hover to Pause (from the tutorial) */
.card-container:hover .orbiter {{
    animation-play-state: paused;
}}

/* Multi-step Keyframes (0%, 25%, 50%, 75%, 100%) */
@keyframes squarePath {{
    0% {{
        transform: translate(0, 0) scale(1);
    }}
    25% {{
        transform: translate(calc(var(--card-width) - 80px), 0) scale(1.2);
    }}
    50% {{
        transform: translate(calc(var(--card-width) - 80px), calc(var(--card-height) - 80px)) scale(1);
    }}
    75% {{
        transform: translate(0, calc(var(--card-height) - 80px)) scale(0.8);
    }}
    100% {{
        transform: translate(0, 0) scale(1);
    }}
}}

/* Controls */
.controls {{
    margin-top: 32px;
    z-index: 20;
}}

.btn {{
    background-color: transparent;
    color: var(--text-primary);
    border: 1px solid var(--border-color);
    padding: 10px 20px;
    border-radius: 8px;
    font-size: 0.9rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    font-family: inherit;
}}

.btn:hover {{
    border-color: var(--accent-color);
    color: var(--accent-color);
}}

/* Accessibility: Respect Reduced Motion Preferences */
@media (prefers-reduced-motion: reduce) {{
    .orbiter {{
        animation: none;
        display: none;
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    
    <div class="card-container">
        <!-- The Animated Keyframe Element -->
        <div class="orbiter" id="orbiter"></div>
        
        <!-- Content -->
        <div class="content">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </div>
    </div>

    <div class="controls">
        <button class="btn" id="directionToggle">Reverse Direction</button>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Keyframe Choreography — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const orbiter = document.getElementById('orbiter');
    const toggleBtn = document.getElementById('directionToggle');
    
    let isReversed = false;

    // Dynamically altering the CSS animation-direction property
    toggleBtn.addEventListener('click', () => {{
        isReversed = !isReversed;
        
        if (isReversed) {{
            orbiter.style.animationDirection = 'reverse';
            toggleBtn.textContent = 'Set Normal Direction';
        }} else {{
            orbiter.style.animationDirection = 'normal';
            toggleBtn.textContent = 'Reverse Direction';
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
