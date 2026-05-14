def create_component(
    output_dir: str,
    title_text: str = "CSS Animation Core",
    body_text: str = "Hover over the card to see a transition, and observe the keyframe spinner loop.",
    color_scheme: str = "dark",
    accent_color: str = "#ff2a7a",
    width_px: int = 1000,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the CSS Animation and Transition effects.
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
        surface_color = "rgba(255, 255, 255, 0.05)"
        border_color = "rgba(255, 255, 255, 0.1)"
        text_muted = "#8b949e"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        surface_color = "#ffffff"
        border_color = "rgba(0, 0, 0, 0.1)"
        text_muted = "#666666"

    # === CSS ===
    css = f"""/* Native CSS Motion — generated component */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --surface: {surface_color};
    --border: {border_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    /* subtle star-like radial gradient background */
    background-image: radial-gradient(circle at 15% 50%, rgba(255, 255, 255, 0.02) 0%, transparent 20%),
                      radial-gradient(circle at 85% 30%, rgba(255, 255, 255, 0.02) 0%, transparent 20%);
}}

.container {{
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    gap: 3rem;
}}

.header {{
    text-align: center;
}}

.header h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    margin-bottom: 0.5rem;
}}

.header p {{
    color: var(--text-muted);
    font-size: 1.1rem;
}}

.demo-grid {{
    display: flex;
    gap: 3rem;
    width: 100%;
    max-width: 800px;
    justify-content: center;
}}

.demo-column {{
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.5rem;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 3rem 2rem;
}}

.demo-column h2 {{
    font-size: 1.25rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--accent);
}}

/* =========================================
   TECHNIQUE 1: CSS TRANSITIONS
   State A to State B over time
   ========================================= */
.transition-target {{
    /* Base State (State A) */
    opacity: 0.4;
    transform: translateY(0) scale(1);
    background-color: transparent;
    border: 2px solid var(--border);
    color: var(--text);
    padding: 1rem 2rem;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    
    /* The Engine: Interpolating properties */
    transition: opacity 230ms ease-in-out,
                transform 400ms cubic-bezier(0.175, 0.885, 0.32, 1.275), /* Slight bounce */
                border-color 230ms linear,
                background-color 230ms linear,
                box-shadow 230ms ease;
}}

.transition-target:hover {{
    /* Hover State (State B) */
    opacity: 1;
    transform: translateY(-8px) scale(1.05);
    border-color: var(--accent);
    background-color: color-mix(in srgb, var(--accent) 15%, transparent);
    box-shadow: 0 12px 24px color-mix(in srgb, var(--accent) 20%, transparent);
}}

/* =========================================
   TECHNIQUE 2: CSS KEYFRAMES
   Continuous, multi-step timeline
   ========================================= */

/* The Element */
.keyframe-target {{
    width: 64px;
    height: 64px;
    border: 6px solid var(--border);
    border-top-color: var(--accent);
    border-radius: 50%;
    
    /* The Engine: Applying the timeline */
    /* animation: name duration timing-function iteration-count */
    animation: tutorialSpinner 2s ease-in-out infinite;
}}

/* The Timeline definition (mimicking video precisely) */
@keyframes tutorialSpinner {{
    from {{
        transform: rotate(0deg);
    }}
    25% {{
        /* Pulls back slightly before spinning */
        transform: rotate(-45deg);
    }}
    to {{
        transform: rotate(360deg);
    }}
}}

/* Adding a secondary pulse animation to show composability */
.pulse-indicator {{
    width: 12px;
    height: 12px;
    background-color: var(--accent);
    border-radius: 50%;
    position: absolute;
    top: 2rem;
    right: 2rem;
    animation: pulseAlpha 1.5s ease-in-out infinite alternate;
}}

@keyframes pulseAlpha {{
    0% {{ opacity: 0.2; box-shadow: 0 0 0 0 rgba(0,0,0,0); }}
    100% {{ opacity: 1; box-shadow: 0 0 15px var(--accent); }}
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
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="pulse-indicator"></div>
        
        <header class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>

        <div class="demo-grid">
            <!-- Technique 1 -->
            <div class="demo-column">
                <h2>Transition</h2>
                <p style="color: var(--text-muted); font-size: 0.9rem; text-align: center;">State change triggered by pseudo-class</p>
                <button class="transition-target">Hover For State B</button>
            </div>

            <!-- Technique 2 -->
            <div class="demo-column">
                <h2>Keyframes</h2>
                <p style="color: var(--text-muted); font-size: 0.9rem; text-align: center;">Multi-step loop bound to timeline</p>
                <div class="keyframe-target"></div>
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Native CSS Motion — generated component
document.addEventListener('DOMContentLoaded', () => {
    // No JavaScript is required for the core visual effects.
    // CSS Transitions and Keyframes handle all rendering natively on the GPU.
    console.log("CSS animations initialized.");
});
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
