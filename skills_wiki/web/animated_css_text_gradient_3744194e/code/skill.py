def create_component(
    output_dir: str,
    title_text: str = "Ibiza Summer Sessions",
    body_text: str = "A deep dive into CSS text gradients and animations.",
    color_scheme: str = "light",        # "dark" or "light"
    accent_color: str = "#757595",      # Fallback and selection color
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Animated CSS Text Gradient visual effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#a0aabf"
    else:
        bg_color = "#ffffff"
        text_color = "#4a4a5e"

    # === CSS ===
    css = f"""/* Animated CSS Text Gradient — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Rubik', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
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
    text-align: center;
}}

.gradient-text {{
    /* Base presentation styles */
    font-size: clamp(3rem, 8vw, 6rem);
    font-weight: 900;
    font-style: italic;
    line-height: 1.1;
    margin-bottom: 1rem;
    max-width: 1000px;
    
    /* 1. Fallback for older browsers (e.g., IE11) */
    color: var(--accent);
}}

/* 2. Apply gradient ONLY if the browser supports clipping it to text */
@supports (-webkit-background-clip: text) or (background-clip: text) {{
    .gradient-text {{
        /* The specific gradient from the tutorial */
        background-image: linear-gradient(120deg, #5ee7df 0%, #b490ca 100%);
        
        /* Make background larger so we can animate its position */
        background-size: 200% auto;
        
        /* Clip background to text shape */
        -webkit-background-clip: text;
        background-clip: text;
        
        /* Make actual text transparent so background shows through */
        color: transparent;
        
        /* Trigger the animation */
        animation: flowGradient 5s ease-in-out infinite alternate;
    }}
}}

/* 3. Ensure selection looks normal (transparent text highlights poorly by default) */
.gradient-text::selection {{
    background-color: var(--accent);
    color: #ffffff;
    -webkit-text-fill-color: #ffffff; /* Overrides the transparent color in webkit */
}}

.subtitle {{
    font-size: 1.25rem;
    font-weight: 400;
    opacity: 0.8;
    max-width: 600px;
}}

/* Animation Keyframes */
@keyframes flowGradient {{
    0% {{
        background-position: 0% 50%;
    }}
    100% {{
        background-position: 100% 50%;
    }}
}}

/* Accessibility: Disable animation if user prefers reduced motion */
@media (prefers-reduced-motion: reduce) {{
    .gradient-text {{
        animation: none;
        background-position: 0% 50%;
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
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Rubik:ital,wght@0,400;1,900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1 class="gradient-text">{title_text}</h1>
        <p class="subtitle">{body_text}</p>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Animated CSS Text Gradient — pure CSS implementation
// No JavaScript required for the core visual effect.
document.addEventListener('DOMContentLoaded', () => {{
    console.log("Component loaded. Gradient clipping and animation handled via CSS.");
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
