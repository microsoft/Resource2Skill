def create_component(
    output_dir: str,
    title_text: str = "Loading Sequence...",
    body_text: str = "Please wait while we establish a connection.",
    color_scheme: str = "dark",
    accent_color: str = "#00ffff", # Cyan neon glow
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Tumbling Neon Loader visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#0a0a0f"
        text_color = "#e0e0e0"
    else:
        bg_color = "#f0f2f5"
        text_color = "#333333"

    css = f"""/* 3D Tumbling Neon Loader */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --accent-color: {accent_color};
    --loader-size: 60px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.container {{
    width: {width_px}px;
    height: {height_px}px;
    max-width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 40px;
}}

.text-content {{
    text-align: center;
    display: flex;
    flex-direction: column;
    gap: 12px;
}}

.title {{
    font-size: 1.5rem;
    font-weight: 600;
    letter-spacing: 1px;
}}

.body-text {{
    font-size: 0.9rem;
    opacity: 0.7;
}}

/* === Core Animation Component === */
.loading-box {{
    height: var(--loader-size);
    width: var(--loader-size);
    border: 6px solid var(--accent-color);
    border-radius: 4px;
    /* Create the neon effect with inner and outer shadows */
    box-shadow: 0 0 12px var(--accent-color), inset 0 0 12px var(--accent-color);
    /* Apply the animation */
    animation: tumbling-sequence 2.5s ease-in-out infinite;
}}

@keyframes tumbling-sequence {{
    0% {{
        transform: rotateX(0deg) rotateY(0deg) rotateZ(0deg);
    }}
    33% {{
        /* Flip vertically */
        transform: rotateX(180deg) rotateY(0deg) rotateZ(0deg);
    }}
    67% {{
        /* Maintain vertical flip, add horizontal flip */
        transform: rotateX(180deg) rotateY(180deg) rotateZ(0deg);
    }}
    100% {{
        /* Maintain previous flips, add flat spin to reset */
        transform: rotateX(180deg) rotateY(180deg) rotateZ(180deg);
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>3D Tumbling Loader</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <!-- The Animated Element -->
        <div class="loading-box"></div>
        
        <div class="text-content">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// 3D Tumbling Neon Loader
document.addEventListener('DOMContentLoaded', () => {{
    // The animation is pure CSS, but we hook into JS here for 
    // potential dynamic lifecycle management (e.g., hiding the loader when content is ready).
    
    // Example: log when the component is ready
    console.log('Loader initialized. Pure CSS animations running.');
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
