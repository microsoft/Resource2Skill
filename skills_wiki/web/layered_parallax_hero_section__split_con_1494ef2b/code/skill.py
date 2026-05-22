def create_component(
    output_dir: str,
    title_text: str = "Welcome\nto my first\nwebsite",
    body_text: str = "A journey into digital creation, layering aesthetics and functionality.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#C13584",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Layered Parallax Hero Section effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Format the title for HTML line breaks
    title_html = title_text.replace("\n", "<br>")

    # Theme logic
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#ffffff"
        pattern_fill = "%23ffffff"
    else:
        bg_color = "#e4e7eb"
        text_color = "#111827"
        pattern_fill = "%23000000"
        
    avatar_fill = text_color.replace("#", "%23")

    # We generate robust SVG data URIs for the background layers to ensure the component works instantly
    # Foreground: An abstract minimal bust/avatar shape
    avatar_svg = f"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'><circle cx='100' cy='70' r='40' fill='{avatar_fill}' opacity='0.15'/><path d='M 20 200 C 20 130 180 130 180 200 Z' fill='{avatar_fill}' opacity='0.15'/></svg>"
    
    # Background: A geometric checkerboard texture
    pattern_svg = f"data:image/svg+xml;utf8,<svg width='40' height='40' xmlns='http://www.w3.org/2000/svg'><path d='M0 0h40v40H0z' fill='none'/><path d='M0 0h20v20H0zM20 20h20v20H20z' fill='{pattern_fill}' opacity='0.03'/></svg>"

    # === CSS ===
    css = f"""/* Layered Parallax Hero Section */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow-x: hidden;
}}

/* The Core Wrapper */
.hero {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 25vw; /* Keeps the center clear for the background subject */
    padding: 0 40px;
    
    /* MULTIPLE BACKGROUND LAYERS */
    /* Layer 1 (Top): Foreground subject */
    /* Layer 2 (Bottom): Repeating geometric texture */
    background-image: 
        url("{avatar_svg}"),
        url("{pattern_svg}");
    
    /* Subject scales with height, pattern is fixed size */
    background-size: 70vh, 40px 40px;
    background-repeat: no-repeat, repeat;
    
    /* Default position, will be overridden by JS for parallax */
    background-position: bottom center, center;
    
    /* Smooth out the parallax shift */
    transition: background-position 0.1s ease-out;
}}

/* Left Container: Heavy Typography */
.hero-intro {{
    max-width: 400px;
    z-index: 10;
}}

.hero-intro h1 {{
    font-size: clamp(2.5rem, 5vw, 4.5rem);
    line-height: 1.1;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: -0.02em;
    margin-bottom: 24px;
}}

.hero-intro p {{
    font-size: 1.125rem;
    line-height: 1.6;
    opacity: 0.85;
    margin-bottom: 32px;
}}

.btn {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background-color: var(--accent);
    color: #ffffff;
    padding: 14px 28px;
    font-size: 0.875rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    text-decoration: none;
    border-radius: 4px;
    transition: all 0.2s ease;
}}

.btn:hover {{
    filter: brightness(0.85);
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}}

/* Right Container: Quotes and Validation */
.hero-quotes {{
    max-width: 350px;
    z-index: 10;
    display: flex;
    flex-direction: column;
    gap: 40px;
}}

.quote {{
    border-left: 4px solid var(--accent);
    padding-left: 20px;
    font-size: 0.95rem;
    line-height: 1.6;
    font-style: italic;
    opacity: 0.9;
}}

.quote span {{
    display: block;
    margin-top: 12px;
    font-style: normal;
    font-weight: 600;
    font-size: 0.85rem;
    opacity: 0.7;
}}

/* The Cascading Step Effect */
.hero-quotes .quote:nth-child(2) {{
    margin-left: 60px;
}}

/* Responsive Breakpoints */
@media (max-width: 900px) {{
    .hero {{
        flex-direction: column;
        gap: 60px;
        background-position: bottom right -10vw, center;
        background-size: 50vh, 40px 40px;
        padding: 60px 20px;
        height: auto;
    }}
    .hero-quotes .quote:nth-child(2) {{
        margin-left: 20px; /* reduce step on mobile */
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text.replace(chr(10), ' ')}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,400;0,600;0,800;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="hero">
        <div class="hero-intro">
            <h1>{title_html}</h1>
            <p>{body_text}</p>
            <a href="#" class="btn">View My Work</a>
        </div>
        
        <div class="hero-quotes">
            <p class="quote">
                "The more that you read, the more things you will know. The more that you learn, the more places you'll go."
                <span>- Dr. Seuss</span>
            </p>
            <p class="quote">
                "For the best return on your money, pour your purse into your head."
                <span>- Benjamin Franklin</span>
            </p>
        </div>
    </main>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Parallax depth effect on the stacked background layers
document.addEventListener('DOMContentLoaded', () => {{
    const hero = document.querySelector('.hero');
    
    // Check if the user prefers reduced motion for accessibility
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    
    if (!prefersReducedMotion) {{
        document.addEventListener('mousemove', (e) => {{
            // Calculate cursor offset from center (-1 to 1)
            const xOffset = (e.clientX / window.innerWidth - 0.5) * 2;
            const yOffset = (e.clientY / window.innerHeight - 0.5) * 2;
            
            // Move foreground by max 15px
            const shiftX = xOffset * 15;
            const shiftY = yOffset * 15;
            
            // Apply new position to ONLY the foreground layer (the first background definition)
            // The pattern remains fixed at 'center'
            requestAnimationFrame(() => {{
                hero.style.backgroundPosition = `calc(50% + ${shiftX}px) calc(100% + ${shiftY}px), center`;
            }});
        }});
        
        // Reset position on mouseleave
        document.addEventListener('mouseleave', () => {{
            hero.style.backgroundPosition = 'bottom center, center';
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
