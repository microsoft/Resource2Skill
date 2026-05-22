def create_component(
    output_dir: str,
    title_text: str = '"The most surest way to win is to not lose."',
    body_text: str = "— Sun Tzu, The Art of War",
    color_scheme: str = "dark",
    accent_color: str = "#00bfff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Animated Glowing Gradient Blob visual effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os
    import html

    os.makedirs(output_dir, exist_ok=True)

    # Escape HTML inputs to prevent XSS
    safe_title = html.escape(title_text)
    safe_body = html.escape(body_text)

    # Derive theme configurations
    if color_scheme == "dark":
        bg_color = "#050505"
        text_color = "#ffffff"
        blob_opacity = "0.7"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        blob_opacity = "0.4"  # Reduced opacity so the blur doesn't wash out light backgrounds

    # === CSS ===
    css_content = f"""/* Animated Glowing Gradient Blob — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --blob-opacity: {blob_opacity};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.container {{
    width: var(--width);
    max-width: 100%;
    height: var(--height);
    position: relative;
    background-color: var(--bg);
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}}

/* Outer layer: Provides the massive blur and controls transparency */
.blob-outer-container {{
    position: absolute;
    inset: 0;
    margin: auto;
    width: 100%;
    height: 100%;
    filter: blur(100px);
    z-index: 0;
    opacity: var(--blob-opacity);
    pointer-events: none; /* Allows text selection to pass through */
    transform: translateZ(0); /* Hardware acceleration hint */
}}

/* Inner layer: Dictates the stadium/pill shape and logical scale */
.blob-inner-container {{
    border-radius: 99999px;
    position: absolute;
    inset: 0;
    margin: auto;
    width: 100%;
    height: 100%;
    transform: scale(0.6);
    overflow: hidden;
}}

/* Core layer: Houses the gradient colors and performs the rotation */
.blob {{
    position: absolute;
    inset: 0;
    margin: auto;
    width: 100%;
    height: 100%;
    background: conic-gradient(
        from 0deg,
        var(--accent),
        #ff007f,
        #7f00ff,
        #00ffcc,
        var(--accent)
    );
    animation: spinBlob 8s linear infinite;
    will-change: transform;
}}

/* Scaling by 2x prevents empty corner space while the rectangular box rotates */
@keyframes spinBlob {{
    0% {{ transform: rotate(0deg) scale(2); }}
    100% {{ transform: rotate(1turn) scale(2); }}
}}

/* Foreground Typography */
.content {{
    position: relative;
    z-index: 10;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
    pointer-events: none; /* Let clicks pass down to body naturally if needed */
}}

.title {{
    color: var(--text);
    font-size: clamp(1.8rem, 4vw, 2.5rem);
    font-weight: 700;
    font-style: italic;
    margin-bottom: 16px;
    line-height: 1.2;
    max-width: 80%;
    text-wrap: balance;
    pointer-events: auto; /* Re-enable selection for text */
}}

.body-text {{
    color: var(--accent);
    font-size: 1.1rem;
    font-weight: 500;
    pointer-events: auto;
}}
"""

    # === HTML ===
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Animated Glowing Gradient Blob</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,500;1,700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <!-- Background Animation Effect -->
        <div class="blob-outer-container">
            <div class="blob-inner-container">
                <div class="blob"></div>
            </div>
        </div>
        
        <!-- Foreground Overlay Content -->
        <div class="content">
            <h1 class="title">{safe_title}</h1>
            <p class="body-text">{safe_body}</p>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    # This component is pure CSS, but we fulfill the signature requirement
    js_content = """// Pure CSS Component
// No JavaScript logic is required for the Animated Glowing Gradient Blob
document.addEventListener('DOMContentLoaded', () => {
    console.log("Glowing Gradient initialized.");
});
"""

    # Write files to disk
    files = []
    for fname, content in [("index.html", html_content), ("style.css", css_content), ("script.js", js_content)]:
        path = os.path.join(output_dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        files.append(path)

    return {
        "html": html_content,
        "css": css_content,
        "js": js_content,
        "files": files,
    }
