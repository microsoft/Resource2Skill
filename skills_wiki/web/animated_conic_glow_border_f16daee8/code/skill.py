def create_component(
    output_dir: str,
    title_text: str = "Animate Borders",
    body_text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Atque ad exercitationem voluptatem ullam et, natus impedit quae veniam optio a doloremque.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00ffff",     # CSS hex color for accent
    width_px: int = 350,
    height_px: int = 400,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Animated Conic Glow Border visual effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os
    import html

    os.makedirs(output_dir, exist_ok=True)

    # Sanitize text inputs for HTML inclusion
    html_safe_title = html.escape(title_text)
    html_safe_body = html.escape(body_text)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0d111c"
        surface_color = "#1c1f2b" # Opaque dark card
        text_color = "#a0aab2"
        title_color = "#ffffff"
    else:
        bg_color = "#e9ecef"
        surface_color = "#ffffff" # Opaque light card
        text_color = "#495057"
        title_color = "#111111"

    # === CSS ===
    css = f"""/* Animated Conic Glow Border */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --surface: {surface_color};
    --text: {text_color};
    --title: {title_color};
    --accent: {accent_color};
    
    --width: {width_px}px;
    --min-height: {height_px}px;
    
    /* Configurable border dimensions */
    --border-thickness: 3px;
    --border-radius: 12px;
    
    /* Fallback angle if @property is unsupported */
    --angle: 0deg; 
}}

/* Houdini API to allow angle animation */
@property --angle {{
    syntax: "<angle>";
    initial-value: 0deg;
    inherits: false;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow-x: hidden; /* Prevent horizontal scroll from extreme blurs */
    padding: 2rem;
}}

/* Main Card Container */
.card {{
    position: relative;
    width: wmin(var(--width), 100%);
    min-height: var(--min-height);
    background: var(--surface);
    padding: 2.5rem;
    border-radius: var(--border-radius);
    
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    
    /* WARNING: Do not add z-index, transform, or opacity here!
       Doing so will create a stacking context and hide the border behind the content. */
}}

/* Typography */
.title {{
    font-size: 1.8rem;
    font-weight: 600;
    color: var(--title);
    margin-bottom: 1rem;
}}

.body-text {{
    font-size: 1rem;
    line-height: 1.6;
    color: var(--text);
}}

/* Animated Pseudo-Elements (Border & Glow) */
.card::after, .card::before {{
    content: '';
    position: absolute;
    height: 100%;
    width: 100%;
    
    /* The gradient tail: transparent for 70% of the circle, then fades to accent */
    background-image: conic-gradient(from var(--angle), transparent 70%, var(--accent));
    
    top: 50%;
    left: 50%;
    translate: -50% -50%;
    z-index: -1;
    
    /* Push the border OUTSIDE the card by the defined thickness */
    padding: var(--border-thickness);
    box-sizing: content-box;
    
    /* Ensure the outer curve parallels the inner curve perfectly */
    border-radius: calc(var(--border-radius) + var(--border-thickness));
    
    /* The continuous rotation */
    animation: spin 3s linear infinite;
}}

/* The specific glow layer */
.card::before {{
    filter: blur(1.5rem);
    opacity: 0.5;
}}

/* Angle Animation Keyframes */
@keyframes spin {{
    from {{
        --angle: 0deg;
    }}
    to {{
        --angle: 360deg;
    }}
}}
"""

    # === HTML ===
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html_safe_title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <!-- 
      The .card element houses the solid background. 
      The animated borders are pseudo-elements generated via CSS.
    -->
    <div class="card">
        <h1 class="title">{html_safe_title}</h1>
        <p class="body-text">{html_safe_body}</p>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Animated Conic Glow Border
// This component relies entirely on CSS @property and conic-gradients.
// No JavaScript is required for the visual rendering loop!

document.addEventListener('DOMContentLoaded', () => {{
    console.log("Card component loaded. Gradient animation handled by CSS Houdini.");
}});
"""

    # === Write files ===
    files = []
    for fname, content in [("index.html", html_content), ("style.css", css), ("script.js", js)]:
        path = os.path.join(output_dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        files.append(path)

    return {
        "html": html_content,
        "css": css,
        "js": js,
        "files": files,
    }
