def create_component(
    output_dir: str,
    title_text: str = "Cinematic Hero",
    body_text: str = "A pure CSS gradient overlay without extra DOM elements.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Zero-Element Video Overlay Hero.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Convert hex to rgba for the overlay gradient
    def hex_to_rgba(hex_code, alpha):
        hex_code = hex_code.lstrip('#')
        if len(hex_code) == 3:
            hex_code = ''.join(c + c for c in hex_code)
        r = int(hex_code[0:2], 16)
        g = int(hex_code[2:4], 16)
        b = int(hex_code[4:6], 16)
        return f"rgba({r}, {g}, {b}, {alpha})"

    if color_scheme == "dark":
        text_color = "#ffffff"
        bg_base = "rgba(13, 17, 28, 0.85)"
        accent_rgba = hex_to_rgba(accent_color, 0.4)
    else:
        text_color = "#1a1a2e"
        bg_base = "rgba(248, 249, 250, 0.85)"
        accent_rgba = hex_to_rgba(accent_color, 0.3)

    # === CSS ===
    css = f"""/* Zero-Element Video Overlay Hero — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #111;
}}

.hero-container {{
    width: var(--width);
    height: var(--height);
    position: relative;
    overflow: hidden;
    
    /* Flexbox used to center the content over the video */
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 2rem;
    
    /* THE CORE TRICK: The container's background acts as the video overlay.
       Because this container does NOT form a stacking context (no z-index, no transform), 
       its block background is painted over the negative z-index video child. */
    background: linear-gradient(135deg, {bg_base} 0%, {accent_rgba} 100%);
    color: {text_color};
}}

.video-bg {{
    position: absolute;
    /* Pushes the video behind the container's background color */
    z-index: -1; 
    
    /* Classic centering and scaling technique for background videos */
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    min-width: 100%;
    min-height: 100%;
    
    pointer-events: none; /* Ensures the video doesn't capture clicks */
    object-fit: cover; /* Modern failsafe */
}}

.hero-content {{
    max-width: 800px;
    z-index: 1; /* Ensures text stays on top */
}}

.hero-title {{
    font-size: 4rem;
    font-weight: 700;
    margin-bottom: 1.5rem;
    letter-spacing: -0.03em;
    line-height: 1.1;
    text-shadow: 0 4px 24px rgba(0, 0, 0, 0.2);
}}

.hero-body {{
    font-size: 1.25rem;
    font-weight: 300;
    opacity: 0.9;
    line-height: 1.6;
    text-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    
    <div class="hero-container">
        <!-- 
          HTML5 Video:
          - autoplay: Starts automatically
          - muted: Required by most modern browsers for autoplay to work
          - loop: Infinite replay
          - playsinline: Required for iOS to play background video without opening full-screen player
        -->
        <video class="video-bg" autoplay muted loop playsinline>
            <source src="https://www.w3schools.com/howto/rain.mp4" type="video/mp4">
            Your browser does not support HTML5 video.
        </video>

        <div class="hero-content">
            <h1 class="hero-title">{title_text}</h1>
            <p class="hero-body">{body_text}</p>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Zero-Element Video Overlay Hero
// No JavaScript is strictly required for this CSS painting order trick to function.
document.addEventListener('DOMContentLoaded', () => {
    const video = document.querySelector('.video-bg');
    
    // Failsafe: Ensure video actually plays even if browser policies initially block it
    if (video) {
        video.play().catch(error => {
            console.log("Autoplay was prevented by browser policy. User interaction may be required.", error);
        });
    }
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
