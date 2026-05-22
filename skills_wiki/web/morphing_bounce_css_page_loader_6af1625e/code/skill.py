def create_component(
    output_dir: str,
    title_text: str = "Content Loaded Successfully",
    body_text: str = "This underlying content is revealed once the morphing bounce loader finishes its simulation and is removed from the DOM.",
    color_scheme: str = "dark",
    accent_color: str = "#00bfff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Morphing Bounce CSS Page Loader.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#121212"
        overlay_color = "#222222"
        text_color = "#f0f0f0"
    else:
        bg_color = "#ffffff"
        overlay_color = "#f4f4f4"
        text_color = "#1a1a2e"

    # === CSS ===
    css = f"""/* Morphing Bounce CSS Page Loader */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --overlay: {overlay_color};
    --text: {text_color};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: #000; /* Dark canvas for the demo container */
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.container {{
    width: var(--width);
    height: var(--height);
    position: relative;
    background: var(--bg);
    color: var(--text);
    overflow: hidden;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}}

.title {{
    font-size: 2.5rem;
    margin-bottom: 1rem;
    font-weight: 700;
}}

.body-text {{
    font-size: 1.1rem;
    max-width: 600px;
    line-height: 1.6;
    opacity: 0.8;
}}

/* === LOADER STYLES === */
.loader {{
    position: absolute; /* absolute to contain within .container */
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: var(--overlay);
    z-index: 100;
    
    /* Hidden by default, toggled via class */
    display: none; 
    align-items: center;
    justify-content: center;
}}

.loader.loader-active {{
    display: flex;
}}

/* The animated shape */
.loader::after {{
    content: "";
    width: 50px;
    height: 50px;
    background: var(--accent);
    /* 0.5s duration, infinite loop, back-and-forth direction */
    animation: loaderAnim 0.5s infinite alternate;
}}

/* Keyframes handling the vertical bounce, scale pulse, and border-radius morph */
@keyframes loaderAnim {{
    from {{
        transform: translateY(-50px) scale(0.5);
        border-radius: 50%;
    }}
    to {{
        transform: translateY(50px) scale(1);
        border-radius: 0%;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Morphing Bounce Loader</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <!-- The Loader Overlay -->
        <!-- Starts active to block the content below -->
        <div class="loader loader-active"></div>

        <!-- The underlying content -->
        <h1 class="title">{title_text}</h1>
        <p class="body-text">{body_text}</p>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Morphing Bounce Loader Implementation
document.addEventListener('DOMContentLoaded', () => {{
    const loader = document.querySelector('.loader');
    
    // Simulate a network loading delay so the loader is visible for demonstration.
    // In a production app, you would tie this to window window.addEventListener('load', ...)
    // or the resolution of a data fetching Promise.
    setTimeout(() => {{
        if (loader) {{
            // Remove the active class to hide the overlay and reveal content
            loader.classList.remove('loader-active');
        }}
    }}, 2500); // 2.5 second simulated load time
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
