def create_component(
    output_dir: str,
    title_text: str = "CSS Only Scroll Snapping Carousel",
    body_text: str = "A smooth, lightweight image slider built entirely without JavaScript.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#ffffff",     # CSS hex color for accent
    width_px: int = 800,
    height_px: int = 450,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the CSS-Only Scroll Snapping Carousel effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#111418"
        text_color = "#f4f4f5"
        shadow_color = "rgba(0, 0, 0, 0.7)"
        nav_bg = accent_color
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        shadow_color = "rgba(0, 0, 0, 0.15)"
        nav_bg = accent_color if accent_color != "#ffffff" else "#333333"

    # === CSS ===
    css = f"""/* CSS-Only Scroll Snapping Carousel */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {nav_bg};
    --shadow: {shadow_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

header {{
    text-align: center;
    margin-bottom: 2rem;
}}

header h1 {{
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}}

header p {{
    font-size: 0.95rem;
    opacity: 0.8;
}}

/* --- Carousel Container --- */
.slider-wrapper {{
    position: relative;
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    margin: 0 auto;
}}

/* --- The Scrolling Area --- */
.slider {{
    display: flex;
    width: 100%;
    height: 100%;
    overflow-x: auto;
    
    /* Core Snapping Logic */
    scroll-snap-type: x mandatory;
    scroll-behavior: smooth;
    
    /* Aesthetics */
    border-radius: 0.5rem;
    box-shadow: 0 1.5rem 3rem -0.75rem var(--shadow);
    
    /* Hide scrollbar for cleaner look (optional but recommended) */
    -ms-overflow-style: none;  /* IE and Edge */
    scrollbar-width: none;     /* Firefox */
}}

.slider::-webkit-scrollbar {{
    display: none; /* Chrome, Safari and Opera */
}}

/* --- The Images --- */
.slider img {{
    /* Take up exactly one full container width, never shrink */
    flex: 1 0 100%;
    height: 100%;
    object-fit: cover;
    
    /* Tell the browser where to snap to */
    scroll-snap-align: start;
}}

/* --- Navigation Overlay --- */
.slider-nav {{
    display: flex;
    column-gap: 1rem;
    position: absolute;
    bottom: 1.25rem;
    left: 50%;
    transform: translateX(-50%);
    z-index: 1;
}}

.slider-nav a {{
    width: 0.5rem;
    height: 0.5rem;
    border-radius: 50%;
    background-color: var(--accent);
    opacity: 0.5;
    transition: opacity 250ms ease, transform 250ms ease;
    text-decoration: none;
}}

.slider-nav a:hover,
.slider-nav a:focus {{
    opacity: 1;
    transform: scale(1.2);
}}

/* Respect user preferences for reduced motion */
@media (prefers-reduced-motion: reduce) {{
    .slider {{
        scroll-behavior: auto;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </header>

    <section class="slider-wrapper" aria-label="Image Carousel">
        <div class="slider">
            <!-- 
              IDs must match the anchor tags below.
              Using Unsplash placeholder images representing space (as in tutorial).
            -->
            <img id="slide-1" src="https://images.unsplash.com/photo-1614730321146-b6fa6a46bcb4?q=80&w=1200&auto=format&fit=crop" alt="3D rendering of an imaginary orange planet in space">
            <img id="slide-2" src="https://images.unsplash.com/photo-1614729939124-03290b56c9ce?q=80&w=1200&auto=format&fit=crop" alt="3D rendering of an imaginary green planet in space">
            <img id="slide-3" src="https://images.unsplash.com/photo-1543722530-d2c3201371e7?q=80&w=1200&auto=format&fit=crop" alt="3D rendering of an imaginary blue planet in space">
        </div>
        
        <div class="slider-nav" aria-label="Carousel Navigation">
            <a href="#slide-1" aria-label="Go to slide 1"></a>
            <a href="#slide-2" aria-label="Go to slide 2"></a>
            <a href="#slide-3" aria-label="Go to slide 3"></a>
        </div>
    </section>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    # Pure CSS execution means JS is empty, but provided to fulfill structural requirements
    js = f"""// CSS Only Carousel
// No JavaScript required for core functionality!
// Scroll snapping and navigation are handled entirely by CSS and HTML Anchor tags.

document.addEventListener('DOMContentLoaded', () => {{
    console.log("Carousel initialized without JavaScript dependencies.");
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
