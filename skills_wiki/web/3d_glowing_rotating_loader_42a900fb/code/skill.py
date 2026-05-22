def create_component(
    output_dir: str,
    title_text: str = "Loading Sequence",
    body_text: str = "Initializing secure connection...",
    color_scheme: str = "dark",
    accent_color: str = "#00ffff",  # Aqua neon
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Glowing Rotating Loader effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#040716" # Deep space blue-black
        text_color = "#e2e8f0"
        subtext_color = "#94a3b8"
    else:
        bg_color = "#f8f9fa"
        text_color = "#0f172a"
        subtext_color = "#64748b"

    # === CSS ===
    css = f"""/* 3D Glowing Rotating Loader */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --subtext: {subtext_color};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    overflow: hidden;
}}

.container {{
    width: var(--width);
    height: var(--height);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 40px;
    position: relative;
}}

/* Loader Core Styles */
.loader-wrapper {{
    /* Provides perspective to make the 3D rotation look slightly volumetric if desired, 
       though the tutorial uses isometric orthographic projection by omitting it. */
    perspective: 800px; 
}}

.loader {{
    width: 50px;
    height: 50px;
    border: 6px solid var(--accent);
    border-radius: 4px;
    /* Outset and Inset shadows create the glowing neon tube effect */
    box-shadow: 
        0 0 12px var(--accent), 
        0 0 12px var(--accent) inset;
    
    /* Animation Shorthand: name | duration | timing-function | iteration-count */
    animation: spin3D 2s ease-in-out infinite;
}}

/* Typography */
.text-content {{
    text-align: center;
    display: flex;
    flex-direction: column;
    gap: 8px;
}}

.title {{
    font-size: 1.5rem;
    font-weight: 600;
    letter-spacing: 0.5px;
}}

.body-text {{
    font-size: 0.95rem;
    color: var(--subtext);
}}

/* Screen reader only class for accessibility */
.sr-only {{
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border-width: 0;
}}

/* Keyframes for the 3D Rotation */
@keyframes spin3D {{
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

/* Accessibility: Respect user preference for reduced motion */
@media (prefers-reduced-motion: reduce) {{
    .loader {{
        animation: pulseFade 1.5s ease-in-out infinite alternate;
        box-shadow: none; /* Reduce visual intensity */
    }}
}}

@keyframes pulseFade {{
    0% {{ opacity: 0.5; }}
    100% {{ opacity: 1; }}
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
    <main class="container" aria-live="polite" aria-busy="true">
        <!-- Visual Loader -->
        <div class="loader-wrapper" aria-hidden="true">
            <div class="loader"></div>
        </div>
        
        <!-- Screen Reader Status -->
        <span class="sr-only">Loading, please wait.</span>

        <!-- Text Context -->
        <div class="text-content">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
    </main>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// 3D Glowing Rotating Loader — Interactive Behavior
document.addEventListener('DOMContentLoaded', () => {{
    // The core loader is entirely CSS-driven.
    // This script demonstrates how you might programmatically halt the loader
    // once a hypothetical data fetch is complete.

    const container = document.querySelector('.container');
    
    // Simulate a network request resolving after 6 seconds
    /*
    setTimeout(() => {{
        container.setAttribute('aria-busy', 'false');
        container.innerHTML = `
            <div class="text-content" style="animation: pulseFade 0.5s ease-out forwards;">
                <h1 class="title" style="color: var(--accent);">Load Complete</h1>
                <p class="body-text">Welcome back.</p>
            </div>
        `;
    }}, 6000);
    */
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
