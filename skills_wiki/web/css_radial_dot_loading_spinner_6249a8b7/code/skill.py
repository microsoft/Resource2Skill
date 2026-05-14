def create_component(
    output_dir: str,
    title_text: str = "Loading Application...",
    body_text: str = "Please wait while we fetch your data.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Circular Dot Loading Spinner.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    # Using the vibrant blue from the tutorial as the default light-mode accent,
    # and standardizing a dark mode to match modern dashboard aesthetics.
    if color_scheme == "dark":
        bg_color = "#0f172a" # Deep slate dark
        text_color = "#f8fafc"
        dot_color = accent_color if accent_color != "#00bfff" else "#ffffff"
    else:
        bg_color = "#f4f7f6" # Soft off-white
        text_color = "#0f172a"
        dot_color = accent_color if accent_color != "#00bfff" else "#4070f4"

    # Configuration for the spinner geometry
    num_dots = 15
    radius = "35px"
    dot_size = "10px"
    animation_duration = "1.5s"

    # Generate HTML spans dynamically for the python string
    spans_html = "\n".join([f'                <span style="--i:{i};"></span>' for i in range(1, num_dots + 1)])

    # === CSS ===
    css = f"""/* CSS Radial Dot Loading Spinner */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --dot-color: {dot_color};
    --radius: {radius};
    --dot-size: {dot_size};
    --duration: {animation_duration};
    --num-dots: {num_dots};
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

.container {{
    width: {width_px}px;
    height: {height_px}px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 48px;
}}

/* Text Content Styling */
.text-wrapper {{
    text-align: center;
    z-index: 10;
}}

.title {{
    font-size: 24px;
    font-weight: 600;
    letter-spacing: 0.5px;
    margin-bottom: 8px;
}}

.body-text {{
    font-size: 14px;
    font-weight: 400;
    opacity: 0.7;
}}

/* Loader Core Styling */
.loader-wrapper {{
    /* Create a relative bounding box that accounts for the outward translation of absolute children */
    width: calc(var(--radius) * 2 + var(--dot-size));
    height: calc(var(--radius) * 2 + var(--dot-size));
    display: flex;
    align-items: center;
    justify-content: center;
}}

.dots {{
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.dots span {{
    position: absolute;
    width: var(--dot-size);
    height: var(--dot-size);
    background: var(--dot-color);
    border-radius: 50%;
    
    /* 
       1. Rotate local coordinate system based on index 
       2. Translate outward along the new Y axis to form the circle 
    */
    transform: rotate(calc(var(--i) * (360deg / var(--num-dots)))) translateY(var(--radius));
    
    /* Apply opacity fade */
    animation: spinnerFade var(--duration) linear infinite;
    
    /* Stagger the start time based on index */
    animation-delay: calc(var(--i) * (var(--duration) / var(--num-dots)));
}}

/* Keyframes for the trailing fade effect */
@keyframes spinnerFade {{
    0% {{
        opacity: 1;
        transform: rotate(calc(var(--i) * (360deg / var(--num-dots)))) translateY(var(--radius)) scale(1.2);
    }}
    100% {{
        opacity: 0.1;
        transform: rotate(calc(var(--i) * (360deg / var(--num-dots)))) translateY(var(--radius)) scale(0.8);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        
        <!-- The Spinner Component -->
        <div class="loader-wrapper" role="status" aria-label="Loading">
            <div class="dots">
{spans_html}
            </div>
        </div>

        <!-- Accompanying Text -->
        <div class="text-wrapper">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    # This component is pure CSS. The JS file is provided to satisfy structural requirements
    # and can be used for future logic (e.g. hiding the loader when a task is complete).
    js = f"""// CSS Radial Dot Loading Spinner
document.addEventListener('DOMContentLoaded', () => {{
    console.log("Spinner initialized successfully. Animation is running on pure CSS.");
    
    // Example hook: how you might remove the loader via JS
    /*
    setTimeout(() => {{
        const loader = document.querySelector('.loader-wrapper');
        if(loader) loader.style.display = 'none';
    }}, 5000);
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
