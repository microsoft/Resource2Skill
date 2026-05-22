def create_component(
    output_dir: str,
    title_text: str = "CSS Illustration",
    body_text: str = "Hover to interact, click to snap a photo.",
    color_scheme: str = "light",        
    accent_color: str = "#2abaac",     
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Pure CSS Camera Icon effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme handling (The camera colors remain mostly static to preserve the illustration, 
    # but the environment changes based on the theme)
    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_color = "#f8fafc"
    else:
        bg_color = "#86c1c9" # The distinct light teal from the tutorial
        text_color = "#0f172a"

    # CSS
    css = f"""/* Pure CSS Camera Component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    
    /* Illustration static colors */
    --cam-body: #3e4854;
    --cam-btn: #647177;
    --cam-ring: #dfeae6;
    
    /* Layout */
    --container-width: {width_px}px;
    --container-height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.container {{
    width: 100%;
    max-width: var(--container-width);
    height: var(--container-height);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 40px;
    padding: 20px;
}}

/* Text Content */
.text-content {{
    text-align: center;
    z-index: 10;
}}

.title {{
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 8px;
    letter-spacing: -0.02em;
}}

.body-text {{
    font-size: 1rem;
    opacity: 0.8;
    max-width: 400px;
}}

/* 
  Camera Illustration 
  Uses 'em' units so the entire graphic can be scaled simply 
  by changing the font-size of the .camera-wrapper
*/
.camera-wrapper {{
    /* Base scale dynamic calculation based on container sizes */
    font-size: calc(min(var(--container-width), var(--container-height)) / 45);
    perspective: 1000px;
}}

.camera {{
    width: 30em;
    height: 20em;
    background-color: var(--cam-body);
    border-radius: 1.5em;
    position: relative;
    box-shadow: 0.1em 0.1em 0.4em rgba(0, 0, 0, 0.8);
    cursor: pointer;
    transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.4s ease;
}}

.camera:hover {{
    transform: translateY(-0.5em) scale(1.02);
    box-shadow: 0.2em 0.4em 1em rgba(0, 0, 0, 0.6);
}}

.button {{
    width: 5em;
    height: 2em;
    background-color: var(--cam-btn);
    border-radius: 0.3em 0.3em 0 0;
    position: absolute;
    top: -2em;
    left: 2.5em;
    transition: transform 0.15s cubic-bezier(0.4, 0, 0.2, 1);
    z-index: -1; /* Placed behind the main body curve */
}}

/* Mechanical press interaction */
.camera:active .button {{
    transform: translateY(1.2em);
}}

.lens {{
    width: 15em;
    height: 15em;
    border-radius: 50%;
    border: 2.5em solid var(--cam-ring);
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: var(--accent);
    /* Hard-stop gradient creates the diagonal glass reflection */
    background-image: linear-gradient(-45deg, transparent 49%, rgba(0, 0, 0, 0.15) 50%);
    box-shadow: 
        inset 0.2em 0.2em 0.8em rgba(0, 0, 0, 0.8), 
        0.2em 0.2em 0.8em rgba(0, 0, 0, 0.8);
    transition: background-color 0.3s ease;
}}

.flash {{
    width: 2em;
    height: 2em;
    border-radius: 50%;
    background-color: var(--accent);
    position: absolute;
    top: 2em;
    right: 2em;
    box-shadow: inset 0.2em 0.2em 0.2em rgba(0, 0, 0, 0.8);
    transition: background-color 0.3s ease;
}}

/* Flash interaction */
.camera:active .flash {{
    background-color: #ffffff;
    box-shadow: 0 0 2em 0.5em rgba(255, 255, 255, 0.8), inset 0.2em 0.2em 0.2em rgba(0, 0, 0, 0.8);
}}
"""

    # HTML
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
        <!-- aria-label provides context for screen readers as this is a visual CSS construct -->
        <div class="camera-wrapper">
            <div class="camera" role="img" aria-label="Illustration of a digital camera">
                <div class="button"></div>
                <div class="lens"></div>
                <div class="flash"></div>
            </div>
        </div>
        
        <div class="text-content">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # JavaScript (Empty as functionality is purely CSS, but included for structure)
    js = """// Pure CSS implementation. 
// JavaScript can be added here if external state management is required.
document.addEventListener('DOMContentLoaded', () => {
    const camera = document.querySelector('.camera');
    
    // Optional: Add a sound effect or trigger an event on click
    camera.addEventListener('click', () => {
        console.log('Photo snapped!');
    });
});
"""

    # Write files
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
