def create_component(
    output_dir: str,
    title_text: str = "Animated Wave Banner",
    body_text: str = "A smooth, layered CSS motion effect",
    color_scheme: str = "dark",        
    accent_color: str = "#3586ff",     
    width_px: int = 1200,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Infinite Layered Wave Banner visual effect.
    """
    import os
    import html

    os.makedirs(output_dir, exist_ok=True)

    # Escape text inputs
    safe_title = html.escape(title_text)
    safe_body = html.escape(body_text)

    # Determine background colors. The wave color matches the page background 
    # to create a seamless shape-divider effect.
    if color_scheme == "dark":
        page_bg = "#0d111c"
        text_color = "#f0f0f0"
        wave_hex = "0d111c" # stripped of '#' for SVG URI
    else:
        page_bg = "#f8f9fa"
        text_color = "#1a1a2e"
        wave_hex = "f8f9fa"

    # Perfect tiling SVG wave pattern
    svg_data = f"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1000 100' preserveAspectRatio='none'%3E%3Cpath d='M0,100 V 50 Q 250,0 500,50 T 1000,50 V 100 z' fill='%23{wave_hex}'/%3E%3C/svg%3E"

    css = f"""/* Infinite Layered Wave Banner */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --page-bg: {page_bg};
    --text: {text_color};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--page-bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.banner-container {{
    width: var(--width);
    height: var(--height);
    max-width: 100%;
    position: relative;
    background: var(--accent);
    overflow: hidden;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border-radius: 8px; /* Optional standard framing */
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}}

.content {{
    position: relative;
    z-index: 1001;
    text-align: center;
    color: #ffffff; /* Forces white text inside the colored banner */
    padding: 2rem;
    transform: translateY(-20px); /* Visual balance against the waves */
}}

.content h1 {{
    font-size: 3rem;
    font-weight: 700;
    letter-spacing: -0.05em;
    margin-bottom: 0.5rem;
    text-shadow: 0 4px 12px rgba(0,0,0,0.1);
}}

.content p {{
    font-size: 1.125rem;
    opacity: 0.9;
}}

/* Wave Base Styles */
.wave {{
    position: absolute;
    left: 0;
    width: 100%;
    height: 100px;
    background: url("{svg_data}");
    background-size: 1000px 100px;
    pointer-events: none; /* Ignore mouse interactions */
}}

/* Specific Wave Layers */
.wave.wave1 {{
    bottom: 0;
    z-index: 1000;
    opacity: 1;
    animation: animateWave 30s linear infinite;
}}

.wave.wave2 {{
    bottom: 10px;
    z-index: 999;
    opacity: 0.5;
    animation: animateWaveReverse 15s linear infinite;
    animation-delay: -5s;
}}

.wave.wave3 {{
    bottom: 15px;
    z-index: 998;
    opacity: 0.2;
    animation: animateWave 30s linear infinite;
    animation-delay: -2s;
}}

.wave.wave4 {{
    bottom: 20px;
    z-index: 997;
    opacity: 0.7;
    animation: animateWaveReverse 15s linear infinite;
    animation-delay: -5s;
}}

/* Animations */
@keyframes animateWave {{
    0% {{ background-position-x: 0; }}
    100% {{ background-position-x: 1000px; }}
}}

@keyframes animateWaveReverse {{
    0% {{ background-position-x: 0; }}
    100% {{ background-position-x: -1000px; }}
}}
"""

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <section class="banner-container">
        <div class="content">
            <h1>{safe_title}</h1>
            <p>{safe_body}</p>
        </div>
        
        <!-- Animated Layers -->
        <div class="wave wave1"></div>
        <div class="wave wave2"></div>
        <div class="wave wave3"></div>
        <div class="wave wave4"></div>
    </section>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Pure CSS effect, no JavaScript required for core functionality.
// Elements use 'pointer-events: none' natively to avoid blocking interactions.
console.log("Wave component loaded.");
"""

    # Write files
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
