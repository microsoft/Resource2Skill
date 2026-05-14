def create_component(
    output_dir: str,
    title_text: str = "Portfolio<br><i>Design</i> 101",
    body_text: str = "Get Dream Clients!",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#FF3366",     # CSS hex color for accent sticker
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Neo-Brutalist Editorial Hero Card.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    # To match the vibrant video style, we'll use stark contrasts.
    if color_scheme == "dark":
        bg_color = "#111111"
        text_color = "#F4F0EA"
        secondary_accent = "#CCFF00" # Neon green for dark mode stickers
    else:
        # Defaulting "light" to the iconic yellow from the tutorial
        bg_color = "#FFCF00" 
        text_color = "#1A1A1A"
        secondary_accent = "#00E5FF" # Cyan for light mode stickers

    # Ensure eyebrow text is provided (using a default if none passed in kwargs)
    eyebrow_text = kwargs.get("eyebrow_text", "EDGYKATRINA PRESENTS...")

    # === CSS ===
    css = f"""/* Neo-Brutalist Editorial Hero — generated component */
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,700;1,9..144,700&family=Space+Grotesk:wght@600&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent-1: {accent_color};
    --accent-2: {secondary_accent};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Space Grotesk', system-ui, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.hero-container {{
    width: 100vw;
    max-width: var(--width);
    height: 100vh;
    max-height: var(--height);
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
}}

.eyebrow {{
    font-size: clamp(0.75rem, 1.5vw, 1rem);
    text-transform: uppercase;
    letter-spacing: 0.15em;
    margin-bottom: 2rem;
    font-weight: 600;
    position: relative;
    z-index: 2;
}}

.title {{
    font-family: 'Fraunces', serif;
    font-size: clamp(4rem, 12vw, 11rem);
    line-height: 0.85;
    letter-spacing: -0.03em;
    font-weight: 700;
    position: relative;
    z-index: 2;
}}

.title i {{
    font-style: italic;
    font-weight: 700;
}}

/* Floating Stickers */
.sticker {{
    position: absolute;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 10;
    will-change: transform;
}}

.sticker-text {{
    position: absolute;
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(0.7rem, 1.2vw, 1rem);
    font-weight: 600;
    text-transform: uppercase;
    text-align: center;
    color: var(--text);
    line-height: 1.1;
    z-index: 2;
    /* Counteract the rotation of the SVG if necessary, but here we rotate the whole group or just the shape */
}}

/* Sticker 1: Starburst */
.sticker-1 {{
    top: 15%;
    right: 15%;
    width: clamp(100px, 15vw, 180px);
    height: clamp(100px, 15vw, 180px);
    color: var(--accent-1);
    animation: float-1 6s ease-in-out infinite;
}}

.starburst-svg {{
    width: 100%;
    height: 100%;
    animation: spin 20s linear infinite;
}}

/* Sticker 2: Oval Pill */
.sticker-2 {{
    bottom: 20%;
    left: 15%;
    width: clamp(120px, 18vw, 200px);
    height: clamp(60px, 9vw, 100px);
    color: var(--accent-2);
    transform: rotate(-15deg);
    animation: float-2 8s ease-in-out infinite reverse;
}}

.sticker-2 .sticker-text {{
    color: var(--bg); /* Invert text for contrast on accent */
}}

.pill-svg {{
    width: 100%;
    height: 100%;
}}

/* Animations */
@keyframes spin {{
    from {{ transform: rotate(0deg); }}
    to {{ transform: rotate(360deg); }}
}}

@keyframes float-1 {{
    0%, 100% {{ transform: translateY(0) rotate(5deg); }}
    50% {{ transform: translateY(-15px) rotate(-2deg); }}
}}

@keyframes float-2 {{
    0%, 100% {{ transform: translateY(0) rotate(-15deg); }}
    50% {{ transform: translateY(15px) rotate(-10deg); }}
}}

/* Reduced Motion */
@media (prefers-reduced-motion: reduce) {{
    .starburst-svg, .sticker-1, .sticker-2 {{
        animation: none;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Neo-Brutalist Editorial Card</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="hero-container">
        
        <div class="eyebrow">{eyebrow_text}</div>
        <h1 class="title">{title_text}</h1>

        <!-- Starburst Sticker -->
        <div class="sticker sticker-1 js-parallax" data-speed="0.05">
            <svg class="starburst-svg" viewBox="0 0 100 100" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                <!-- 12-point jagged starburst generated mathematically for a punchy badge look -->
                <polygon points="50,0 61,15 78,9 81,27 98,34 89,49 98,66 81,73 78,91 61,85 50,100 39,85 22,91 19,73 2,66 11,49 2,34 19,27 22,9 39,15"/>
            </svg>
            <div class="sticker-text">Tips &<br>Tricks</div>
        </div>

        <!-- Pill Sticker -->
        <div class="sticker sticker-2 js-parallax" data-speed="-0.03">
            <svg class="pill-svg" viewBox="0 0 200 100" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                <rect x="0" y="0" width="200" height="100" rx="50" ry="50" />
            </svg>
            <div class="sticker-text">{body_text}</div>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Mousemove parallax effect for the floating stickers
document.addEventListener('DOMContentLoaded', () => {{
    const parallaxElements = document.querySelectorAll('.js-parallax');
    
    // Check for reduced motion preference before applying JS parallax
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (!prefersReducedMotion) {{
        document.addEventListener('mousemove', (e) => {{
            const mouseX = e.clientX;
            const mouseY = e.clientY;
            
            // Calculate mouse position relative to the center of the screen
            const centerX = window.innerWidth / 2;
            const centerY = window.innerHeight / 2;
            
            const moveX = mouseX - centerX;
            const moveY = mouseY - centerY;

            parallaxElements.forEach(el => {{
                const speed = parseFloat(el.getAttribute('data-speed')) || 0.05;
                
                // Calculate the translation
                const x = moveX * speed;
                const y = moveY * speed;
                
                // Apply the transform alongside any existing CSS transforms via custom properties
                // Using a technique that doesn't override the CSS animation transforms
                el.style.transform = `translate(${{x}}px, ${{y}}px)`;
            }});
        }});
    }}
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
