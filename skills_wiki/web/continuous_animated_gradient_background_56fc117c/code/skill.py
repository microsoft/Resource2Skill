def create_component(
    output_dir: str,
    title_text: str = "Animated Gradient",
    body_text: str = "A smooth, continuous flow of colors built with pure CSS.",
    color_scheme: str = "dark",        # "dark" or "light" determines foreground contrast
    accent_color: str = "#f48e21",     # Used as one of the gradient stops
    width_px: int = 1000,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Animated Gradient Background effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors and gradient stops ===
    if color_scheme == "dark":
        text_color = "#ffffff"
        card_bg = "rgba(20, 20, 30, 0.4)"
        card_border = "rgba(255, 255, 255, 0.1)"
        # Dark vibrant theme inspired by the video, weaving in the accent
        c1 = "#d2001a"
        c2 = "#7462ff"
        c3 = accent_color
        c4 = "#23d5ab"
    else:
        text_color = "#1a1a2e"
        card_bg = "rgba(255, 255, 255, 0.5)"
        card_border = "rgba(255, 255, 255, 0.4)"
        # Lighter/Pastel variant weaving in the accent
        c1 = "#ff9a9e"
        c2 = "#fecfef"
        c3 = accent_color
        c4 = "#a1c4fd"

    # === CSS ===
    css = f"""/* Continuous Animated Gradient Background */
:root {{
    --width: {width_px}px;
    --height: {height_px}px;
    --text-color: {text_color};
    --card-bg: {card_bg};
    --card-border: {card_border};
    
    /* Gradient Color Stops */
    --color-1: {c1};
    --color-2: {c2};
    --color-3: {c3};
    --color-4: {c4};
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #000; /* Fallback */
    overflow: hidden;
}}

.animated-container {{
    width: var(--width);
    height: var(--height);
    max-width: 100%;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 20px 50px rgba(0,0,0,0.3);
    
    /* The Core Technique */
    background: linear-gradient(
        45deg, 
        var(--color-1), 
        var(--color-2), 
        var(--color-3), 
        var(--color-4)
    );
    background-size: 300% 300%;
    animation: gradientShift 12s ease-in-out infinite;
}}

/* Keyframes for panning the oversized background */
@keyframes gradientShift {{
    0% {{
        background-position: 0% 50%;
    }}
    50% {{
        background-position: 100% 50%;
    }}
    100% {{
        background-position: 0% 50%;
    }}
}}

/* Foreground Content Styling for demonstration */
.content-card {{
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    padding: 3rem 4rem;
    border-radius: 16px;
    text-align: center;
    color: var(--text-color);
    max-width: 80%;
    transform: translateY(20px);
    opacity: 0;
    animation: fadeUp 1s cubic-bezier(0.16, 1, 0.3, 1) forwards 0.5s;
}}

.content-card h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    letter-spacing: -0.03em;
}}

.content-card p {{
    font-size: 1.125rem;
    line-height: 1.6;
    opacity: 0.9;
}}

@keyframes fadeUp {{
    to {{
        transform: translateY(0);
        opacity: 1;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <!-- The container hosts the animated background -->
    <div class="animated-container">
        
        <!-- Foreground content with glassmorphism to contrast with vibrant background -->
        <div class="content-card">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Pure CSS handles the animation for this component.
// JavaScript is included here as a placeholder for future interactivity.
document.addEventListener('DOMContentLoaded', () => {
    console.log("Animated Gradient Component Loaded.");
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
