def create_component(
    output_dir: str,
    title_text: str = "Loading...",
    body_text: str = "", # Unused in this specific layout, but preserved for signature
    color_scheme: str = "dark",
    accent_color: str = "#2196f3",
    width_px: int = 350,
    height_px: int = 350,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Circular Neon Spinner effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#262626"
        ring_bg = "#131313"
        text_color = accent_color
    else:
        bg_color = "#f8f9fa"
        ring_bg = "#e0e0e0"
        text_color = accent_color

    # === CSS ===
    css = f"""/* Circular Neon Spinner */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --ring-bg: {ring_bg};
    --accent: {accent_color};
    --text: {text_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.loading-container {{
    width: var(--width);
    height: var(--height);
    /* Ensure it remains square on small viewports */
    max-width: 90vw;
    max-height: 90vw;
    aspect-ratio: 1 / 1;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
}}

/* The Spinning Ring */
.loading-container::before {{
    content: '';
    position: absolute;
    inset: 0; /* shorthand for top:0; left:0; width:100%; height:100% */
    border: 10px solid var(--ring-bg);
    border-top: 10px solid var(--accent);
    border-radius: 50%;
    animation: spin 2s linear infinite;
}}

.loading-text {{
    color: var(--text);
    /* Scale font down on smaller screens */
    font-size: clamp(16px, calc(var(--width) * 0.1), 40px);
    letter-spacing: 5px;
    text-transform: uppercase;
    font-weight: 500;
    
    /* Counteract the off-center effect caused by trailing letter-spacing */
    padding-left: 5px; 
    z-index: 1; /* Keeps text above the ring if overlapping */
}}

@keyframes spin {{
    0% {{
        transform: rotate(0deg);
    }}
    100% {{
        transform: rotate(360deg);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="loading-container" aria-busy="true" aria-label="Loading">
        <div class="loading-text">{title_text}</div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Circular Neon Spinner
// Pure CSS implementation. JS provided for structure.
document.addEventListener('DOMContentLoaded', () => {{
    console.log("Spinner initialized.");
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
