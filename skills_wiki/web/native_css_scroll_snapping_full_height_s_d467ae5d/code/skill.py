def create_component(
    output_dir: str,
    title_text: str = "CSS Scroll Snapping",
    body_text: str = "Scroll down to see the snapping effect in action. This section aligns perfectly to the top.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#e63946",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Native CSS Scroll Snapping effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        body_bg = "#090a0f"
        bg_color = "#1a1a2e"
        text_color = "#f0f0f0"
    else:
        body_bg = "#e9ecef"
        bg_color = "#ffffff"
        text_color = "#1a1a2e"

    # === CSS ===
    css = f"""/* CSS Scroll Snapping — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --body-bg: {body_bg};
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--body-bg);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    /* Prevent the body from scrolling so only the component scrolls */
    overflow: hidden; 
}}

/* The Scrolling Container */
.container {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    
    /* Enable vertical scrolling */
    overflow-y: scroll;
    /* Hide scrollbar for cleaner look (optional, but nice for components) */
    scrollbar-width: none; 
    
    /* The Magic: Force scroll to snap on the Y axis */
    scroll-snap-type: y mandatory;
    scroll-behavior: smooth;
    
    background: var(--bg);
    border-radius: 12px;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
}}

.container::-webkit-scrollbar {{
    display: none;
}}

/* The Snap Targets */
.section {{
    /* Match the container's height so it fills the view exactly */
    height: 100%;
    width: 100%;
    
    /* The Magic: Tell the container where to snap to this element */
    scroll-snap-align: start;
    /* Prevent snapping to the middle of the element if user scrolls fast */
    scroll-snap-stop: always;
    
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

/* Alternating Color Logic */
.section:nth-child(odd) {{
    background: var(--bg);
    color: var(--text);
}}

.section:nth-child(even) {{
    background: var(--accent);
    color: #ffffff; /* High contrast text on accent */
}}

/* Typography */
.content {{
    max-width: 800px;
    text-align: center;
}}

.content h2 {{
    font-size: 3.5rem;
    font-weight: 700;
    margin-bottom: 1.5rem;
    letter-spacing: -0.02em;
}}

.content p {{
    font-size: 1.25rem;
    line-height: 1.6;
    opacity: 0.9;
}}

/* Responsive text scaling */
@media (max-width: 768px) {{
    .content h2 {{ font-size: 2.5rem; }}
    .content p {{ font-size: 1.1rem; }}
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
    <div class="container">
        <!-- Section 1 -->
        <section class="section">
            <div class="content">
                <h2>{title_text}</h2>
                <p>{body_text}</p>
            </div>
        </section>
        
        <!-- Section 2 -->
        <section class="section">
            <div class="content">
                <h2>Section Two</h2>
                <p>The second section snaps securely into place. Notice how the container refuses to let you rest halfway between the two backgrounds.</p>
            </div>
        </section>
        
        <!-- Section 3 -->
        <section class="section">
            <div class="content">
                <h2>Section Three</h2>
                <p>Because we use <code>scroll-snap-type: mandatory</code>, the browser calculates the closest snap point and automatically glides the user to perfect alignment.</p>
            </div>
        </section>
        
        <!-- Section 4 -->
        <section class="section">
            <div class="content">
                <h2>Native & Performant</h2>
                <p>No JavaScript is required for this logic. Scrolling remains hardware-accelerated and perfectly supports touch-swipes on mobile devices.</p>
            </div>
        </section>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// No JavaScript is required for the scroll snapping logic.
// This file is included to satisfy component structure requirements.
document.addEventListener('DOMContentLoaded', () => {
    console.log("CSS Scroll Snapping Component Loaded Successfully.");
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
