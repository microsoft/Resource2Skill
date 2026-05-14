def create_component(
    output_dir: str,
    title_text: str = "WELCOME<br>TO MY<br>PORTFOLIO",
    body_text: str = "I build interactive, immersive web experiences. Let's create something memorable together.",
    color_scheme: str = "dark",
    accent_color: str = "#C13584",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Layered Portrait Hero Section.
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme colors based on the tutorial's aesthetic
    if color_scheme == "dark":
        bg_color = "#1A253A"
        text_color = "#ffffff"
        text_muted = "rgba(255, 255, 255, 0.7)"
        overlay = "rgba(26, 37, 58, 0.8)"
    else:
        bg_color = "#e2e8f0"
        text_color = "#0f172a"
        text_muted = "rgba(15, 23, 42, 0.7)"
        overlay = "rgba(226, 232, 240, 0.8)"

    # CSS Generation
    css = f"""/* Layered Portrait Hero Section */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --overlay: {overlay};
    --width: {width_px}px;
    --height: {height_px}px;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg-color);
    color: var(--text-color);
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}}

.container {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    
    /* 
       Multiple backgrounds: 
       1. Top layer: The portrait (SVG data URI placeholder)
       2. Bottom layer: A radial gradient texture
    */
    background-image: 
        url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 500'%3E%3Cpath d='M80,500 C80,350 130,280 200,280 C270,280 320,350 320,500 Z' fill='{text_color.replace('#', '%23')}' opacity='0.15'/%3E%3Ccircle cx='200' cy='180' r='80' fill='{text_color.replace('#', '%23')}' opacity='0.15'/%3E%3C/svg%3E"),
        radial-gradient(circle at center, var(--overlay) 0%, var(--bg-color) 100%);
    background-size: 70vh, cover;
    background-repeat: no-repeat, no-repeat;
    background-position: bottom center, center;
    transition: background-position 0.1s ease-out;
}}

/* Left Block - Primary Info */
.main-intro {{
    position: relative;
    right: 12%; /* Pushes the block left, away from the portrait */
    max-width: 450px;
    z-index: 10;
    animation: fadeInUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
}}

.main-intro h1 {{
    font-size: clamp(2.5rem, 5vw, 5rem);
    line-height: 1.05;
    font-weight: 800;
    text-transform: uppercase;
    margin-bottom: 24px;
    letter-spacing: -0.02em;
}}

.main-intro p {{
    font-size: 18px;
    line-height: 1.6;
    color: var(--text-muted);
    margin-bottom: 40px;
}}

.cta-button {{
    display: inline-block;
    background-color: var(--accent);
    color: #ffffff;
    text-decoration: none;
    padding: 16px 32px;
    font-size: 14px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    border-radius: 2px;
    transition: filter 0.2s ease, transform 0.2s ease;
}}

.cta-button:hover {{
    filter: brightness(1.2);
    transform: translateY(-2px);
}}

/* Right Block - Secondary Info */
.main-quotes {{
    position: relative;
    left: 8%; /* Pushes the block right, away from the portrait */
    max-width: 320px;
    border-left: 4px solid var(--accent);
    padding-left: 24px;
    z-index: 10;
    opacity: 0;
    animation: fadeInUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) 0.3s forwards;
}}

.quote-item {{
    margin-bottom: 32px;
}}

.quote-item:last-child {{
    margin-bottom: 0;
}}

.quote-item p {{
    font-size: 16px;
    line-height: 1.7;
    margin-bottom: 12px;
    font-style: italic;
}}

.quote-author {{
    font-size: 14px;
    font-weight: 600;
    color: var(--accent);
}}

/* Keyframes */
@keyframes fadeInUp {{
    from {{
        opacity: 0;
        transform: translateY(30px);
    }}
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

/* Basic Responsiveness for smaller preview windows */
@media (max-width: 900px) {{
    .container {{
        flex-direction: column;
        justify-content: center;
        padding: 40px;
        background-position: bottom right -10vw, center;
    }}
    .main-intro, .main-quotes {{
        position: static;
        max-width: 100%;
        margin: 20px 0;
    }}
}}
"""

    # HTML Generation
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hero Section Component</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        
        <div class="main-intro">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <a href="#" class="cta-button">View My Work</a>
        </div>

        <div class="main-quotes">
            <div class="quote-item">
                <p>"The more that you read, the more things you will know. The more that you learn, the more places you'll go."</p>
                <span class="quote-author">— Dr. Seuss</span>
            </div>
            <div class="quote-item">
                <p>"An investment in knowledge pays the best interest."</p>
                <span class="quote-author">— Benjamin Franklin</span>
            </div>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # JS Generation (Adds Parallax enhancement)
    js = """document.addEventListener('DOMContentLoaded', () => {
    const container = document.querySelector('.container');

    // Add subtle mousemove parallax to the background portrait
    container.addEventListener('mousemove', (e) => {
        // Calculate normalized mouse position (-1 to 1)
        const x = (e.clientX / window.innerWidth - 0.5) * 2;
        const y = (e.clientY / window.innerHeight - 0.5) * 2;

        // Shift background position slightly (offsetting the 'bottom center' default)
        const shiftX = x * -20; // Move up to 20px opposite to mouse
        const shiftY = y * -10; 

        // Update the first background (portrait), leave the second (texture) alone
        container.style.backgroundPosition = `calc(50% + ${shiftX}px) calc(100% + ${shiftY}px), center`;
    });

    // Reset smoothly on mouse leave
    container.addEventListener('mouseleave', () => {
        container.style.backgroundPosition = 'bottom center, center';
        container.style.transition = 'background-position 0.5s ease-out';
        
        // Remove transition after reset so mousemove is snappy again
        setTimeout(() => {
            container.style.transition = 'none';
        }, 500);
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
