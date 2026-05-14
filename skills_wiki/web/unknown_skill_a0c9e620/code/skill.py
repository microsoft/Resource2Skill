def create_component(
    output_dir: str,
    title_text: str = "Wavy Hover Interaction",
    body_text: str = "Hover over the brutalist button to reveal the fluid cutout animation.",
    color_scheme: str = "dark",        
    accent_color: str = "#00bfff",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    import os
    import urllib.parse

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#ffffff"
        border_color = "#ffffff"
    else:
        bg_color = "#f8f9fa"
        text_color = "#000000"
        border_color = "#000000"

    # === Generate SVG Data URI ===
    # SVG Path draws a continuous wave. It oscillates between Y=10 and Y=90, filling down to Y=100.
    raw_svg = f'<svg viewBox="0 0 100 100" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg"><path d="M0,50 Q25,10 50,50 T100,50 L100,100 L0,100 Z" fill="{bg_color}"/></svg>'
    encoded_svg = urllib.parse.quote(raw_svg)
    svg_data_uri = f"data:image/svg+xml;utf8,{encoded_svg}"

    # === CSS ===
    css = f"""/* Neubrutalist Wavy Hover Button */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --border: {border_color};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.container {{
    width: var(--width);
    height: var(--height);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 3rem;
    text-align: center;
}}

.title {{
    font-size: 2.5rem;
    font-weight: 800;
    letter-spacing: -0.02em;
}}

.body-text {{
    font-size: 1.1rem;
    opacity: 0.8;
    max-width: 500px;
}}

/* Component Styles */
.wavy-btn {{
    appearance: none;
    background-color: var(--accent);
    border: 3px solid var(--border);
    border-radius: 8px;
    box-shadow: 4px 4px 0 var(--border);
    cursor: pointer;
    position: relative;
    overflow: hidden;
    display: inline-flex;
    justify-content: center;
    align-items: center;
    min-width: 260px;
    height: 68px;
    padding: 0 2.5rem;
    outline: none;
    transition: box-shadow 0.3s ease, transform 0.1s ease;
}}

/* Hover & Focus state */
.wavy-btn:hover,
.wavy-btn:focus-visible {{
    box-shadow: 6px 6px 0 var(--border);
}}

/* Active/Click state for tactile feedback */
.wavy-btn:active {{
    transform: translate(2px, 2px);
    box-shadow: 2px 2px 0 var(--border);
}}

.wavy-btn-text {{
    font-size: 1.25rem;
    font-weight: 800;
    color: var(--text);
    letter-spacing: 0.05em;
    position: relative;
    z-index: 10;
    pointer-events: none; /* Prevents text from interfering with hover */
}}

/* Decoupled Animation Wrappers */
.wave-wrapper {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    /* Start hidden below the button */
    transform: translateY(100%);
    transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    z-index: 1;
    pointer-events: none;
}}

/* Slide up on hover */
.wavy-btn:hover .wave-wrapper,
.wavy-btn:focus-visible .wave-wrapper {{
    transform: translateY(0%);
}}

.wave-inner {{
    width: 200%; /* Double width to allow sliding */
    height: 100%;
    background-image: url("{svg_data_uri}");
    background-size: 50% 100%; /* 1 SVG tile = 100% of button width */
    background-repeat: repeat-x;
    /* Continuous motion */
    animation: wave-slide 1.5s linear infinite;
}}

/* Shift left by 50% of the 200% container = exactly 1 SVG tile */
@keyframes wave-slide {{
    0% {{ transform: translateX(0); }}
    100% {{ transform: translateX(-50%); }}
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div>
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
        
        <!-- Component -->
        <button class="wavy-btn" aria-label="Interactive wavy button">
            <span class="wavy-btn-text">HOVER ME!</span>
            <div class="wave-wrapper">
                <div class="wave-inner"></div>
            </div>
        </button>
        
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    # No JS is strictly required for the core visual pattern, 
    # but we include a simple event listener to handle click feedback dynamically if needed.
    js = f"""// Wavy Button Interactivity
document.addEventListener('DOMContentLoaded', () => {{
    const wavyBtn = document.querySelector('.wavy-btn');
    
    // Optional: Log interaction
    wavyBtn.addEventListener('click', () => {{
        console.log('Wavy button clicked!');
    }});
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
