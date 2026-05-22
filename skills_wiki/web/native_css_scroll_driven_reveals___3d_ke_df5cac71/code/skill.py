def create_component(
    output_dir: str,
    title_text: str = "Native CSS Animations",
    body_text: str = "Scroll down to see zero-JS view-timeline animations in action.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00ffff",     # CSS hex color for accent (cyan default)
    width_px: int = 1000,
    height_px: int = 700,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the CSS 3D Loader and View Timeline Scroll animations.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
        surface_color = "rgba(255, 255, 255, 0.05)"
    else:
        bg_color = "#f0f4f8"
        text_color = "#1a1a2e"
        surface_color = "rgba(0, 0, 0, 0.05)"

    # Generate 20 blocks for the scrolling grid
    blocks_html = "\n".join(['            <div class="block"></div>' for _ in range(20)])

    # === CSS ===
    css = f"""/* Native CSS Animations — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #000; /* Outer page bg to frame the component */
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

/* The isolated component container */
.container {{
    width: {width_px}px;
    height: {height_px}px;
    background: var(--bg);
    overflow-y: auto;
    overflow-x: hidden;
    position: relative;
    border-radius: 12px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
    scroll-behavior: smooth;
}}

/* Custom scrollbar for aesthetics */
.container::-webkit-scrollbar {{ width: 8px; }}
.container::-webkit-scrollbar-track {{ background: var(--bg); }}
.container::-webkit-scrollbar-thumb {{ background: var(--surface); border-radius: 4px; }}

/* --- Hero Section & 3D Loader --- */
.hero {{
    height: 70vh; /* Forces content below the fold */
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
    border-bottom: 1px solid var(--surface);
}}

.loading {{
    width: 50px;
    height: 50px;
    border: 5px solid var(--accent);
    border-radius: 3px;
    /* Glow effect using double box-shadow */
    box-shadow: 0 0 15px var(--accent), inset 0 0 15px var(--accent);
    margin-bottom: 2rem;
    animation: spin3D 2.5s ease-in-out infinite;
}}

@keyframes spin3D {{
    0%   {{ transform: rotateX(0deg) rotateY(0deg) rotateZ(0deg); }}
    33%  {{ transform: rotateX(180deg) rotateY(0deg) rotateZ(0deg); }}
    67%  {{ transform: rotateX(180deg) rotateY(180deg) rotateZ(0deg); }}
    100% {{ transform: rotateX(180deg) rotateY(180deg) rotateZ(180deg); }}
}}

.title {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
}}

.subtitle {{
    font-size: 1.1rem;
    color: var(--text);
    opacity: 0.7;
    max-width: 400px;
}}

/* --- Scroll Gallery & View Timeline --- */
.gallery {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 20px;
    padding: 40px;
}}

.block {{
    height: 120px;
    border-radius: 6px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}}

/* Extracted tutorial palette */
.block:nth-child(5n + 1) {{ background: #d9382e; }} /* Red */
.block:nth-child(5n + 2) {{ background: #5f5964; }} /* Slate */
.block:nth-child(5n + 3) {{ background: #f5eed3; }} /* Cream */
.block:nth-child(5n + 4) {{ background: #f9a03f; }} /* Yellow */
.block:nth-child(5n + 5) {{ background: #0b8a8f; }} /* Teal */

/* Scroll-Driven Animation Implementation */
@keyframes scrollReveal {{
    from {{
        opacity: 0;
        transform: scale(0.5) translateY(50px);
    }}
    to {{
        opacity: 1;
        transform: scale(1) translateY(0);
    }}
}}

/* Apply animation only if browser supports view timelines */
@supports (animation-timeline: view()) {{
    .block {{
        animation: scrollReveal linear both;
        animation-timeline: view();
        /* Start animating when element enters, finish when it covers 30% of viewport */
        animation-range: entry 0% cover 30%; 
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
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="hero">
            <div class="loading"></div>
            <h1 class="title">{title_text}</h1>
            <p class="subtitle">{body_text}</p>
        </div>
        
        <div class="gallery">
{blocks_html}
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Native CSS Animations — No JS required for the core effects!
// The view-timeline and 3D rotations are entirely handled by CSS.

document.addEventListener('DOMContentLoaded', () => {{
    // We only use JS here to check for browser support and alert the user if needed
    if (!CSS.supports('animation-timeline', 'view()')) {{
        console.info("Your browser does not support CSS animation-timeline.");
        // A real app might load an IntersectionObserver polyfill here.
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
