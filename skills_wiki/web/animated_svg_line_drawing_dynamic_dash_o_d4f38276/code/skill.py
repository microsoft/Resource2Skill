def create_component(
    output_dir: str,
    title_text: str = "Animated Vector Logo",
    body_text: str = "Watch the lines draw themselves dynamically.",
    color_scheme: str = "custom",      # "custom" uses the video's pastel gradient
    accent_color: str = "#ffffff",     # Color of the drawing line
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the SVG Line Drawing Animation.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Background Logic ===
    if color_scheme == "custom":
        # Video's specific pastel gradient
        bg_css = "background: linear-gradient(100deg, #a9c9ff 0%, #ffbbec 100%);"
        text_color = "#ffffff"
    elif color_scheme == "dark":
        bg_css = "background-color: #0f172a;"
        text_color = "#f8fafc"
    else:
        bg_css = "background-color: #f8fafc;"
        text_color = "#0f172a"
        if accent_color == "#ffffff":
            accent_color = "#3b82f6" # Ensure line is visible on light bg

    # Complex default SVG demonstrating intersecting shapes similar to the video's vibe
    svg_content = """
        <svg viewBox="0 0 200 200" class="animated-svg">
            <defs>
                <!-- Optional: Glow filter for the lines -->
                <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
                    <feGaussianBlur stdDeviation="2" result="blur" />
                    <feComposite in="SourceGraphic" in2="blur" operator="over" />
                </filter>
            </defs>
            <!-- A set of intertwined geometric paths -->
            <circle cx="100" cy="100" r="70" />
            <circle cx="65" cy="100" r="35" />
            <circle cx="135" cy="100" r="35" />
            <path d="M 30,100 Q 100,20 170,100 T 30,100" />
            <path d="M 30,100 Q 100,180 170,100 T 30,100" />
            <line x1="30" y1="100" x2="170" y2="100" />
            <line x1="100" y1="30" x2="100" y2="170" />
        </svg>
    """

    # === CSS ===
    css = f"""/* Animated SVG Line Drawing */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    {bg_css}
    color: {text_color};
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.container {{
    width: 100%;
    max-width: {width_px}px;
    height: {height_px}px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
}}

.title {{
    font-size: 2rem;
    font-weight: 300;
    letter-spacing: 0.1em;
    margin-bottom: 0.5rem;
    opacity: 0;
    animation: fadeIn 1s ease forwards 2.5s; /* Appears after drawing mostly finishes */
}}

.body-text {{
    font-size: 1rem;
    opacity: 0.8;
    margin-bottom: 3rem;
    opacity: 0;
    animation: fadeIn 1s ease forwards 2.8s;
}}

/* === Core SVG Animation Styles === */
.animated-svg {{
    width: 300px;
    height: 300px;
    /* Base styles for the lines */
    fill: none;
    stroke: {accent_color};
    stroke-width: 1.5;
    stroke-linecap: round;
    stroke-linejoin: round;
    /* filter: url(#glow); Optional */
}}

/* Target all valid geometry elements inside the SVG */
.animated-svg path,
.animated-svg circle,
.animated-svg line,
.animated-svg rect,
.animated-svg polygon,
.animated-svg polyline {{
    /* 
       These variables are injected dynamically via JavaScript.
       Fallback to 1000 just in case JS fails to run.
    */
    --path-length: 1000;
    --draw-delay: 0s;
    --draw-duration: 2s;

    stroke-dasharray: var(--path-length);
    stroke-dashoffset: var(--path-length);
    
    /* 
       The forwards fill-mode ensures the lines stay visible 
       after the animation completes 
    */
    animation: drawLine var(--draw-duration) cubic-bezier(0.4, 0, 0.2, 1) var(--draw-delay) forwards;
}}

/* The magic keyframe */
@keyframes drawLine {{
    100% {{
        stroke-dashoffset: 0;
    }}
}}

@keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(10px); }}
    to {{ opacity: 1; transform: translateY(0); }}
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        {svg_content}
        <h1 class="title">{title_text}</h1>
        <p class="body-text">{body_text}</p>
    </div>
    
    <!-- Reload button for demonstration purposes -->
    <button id="replay" style="position:fixed; bottom: 20px; right: 20px; padding: 10px 20px; background: rgba(0,0,0,0.2); border: 1px solid rgba(255,255,255,0.3); color: white; border-radius: 6px; cursor: pointer; font-family: 'Inter', sans-serif;">Replay Animation</button>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Animated SVG Line Drawing Logic
document.addEventListener('DOMContentLoaded', () => {{
    
    function setupSVGAnimation() {{
        // Select all geometry elements that can have a stroke within our target SVG
        const shapes = document.querySelectorAll('.animated-svg path, .animated-svg circle, .animated-svg line, .animated-svg rect, .animated-svg polygon, .animated-svg polyline');
        
        shapes.forEach((shape, index) => {{
            // 1. Calculate the exact length of the shape
            const length = shape.getTotalLength();
            
            // 2. Set the length as a CSS variable for that specific element
            // We add a tiny bit extra (0.5) to prevent rounding errors causing tiny gaps
            shape.style.setProperty('--path-length', length + 0.5);
            
            // 3. Stagger the animation. 
            // Calculate delay based on index to make them draw sequentially or slightly overlapped.
            const delay = index * 0.15; // 0.15 seconds between each path starting
            shape.style.setProperty('--draw-delay', `${{delay}}s`);
            
            // Optional: Vary duration based on line length so long lines draw faster to keep up
            // const duration = Math.max(1.5, length / 200); 
            // shape.style.setProperty('--draw-duration', `${{duration}}s`);
            
            // Reset animation to allow replays
            shape.style.animation = 'none';
            shape.offsetHeight; // Trigger reflow
            shape.style.animation = null; 
        }});
    }}

    // Initialize on load
    setupSVGAnimation();

    // Setup Replay Button
    document.getElementById('replay').addEventListener('click', () => {{
        // Reset titles
        const titles = document.querySelectorAll('.title, .body-text');
        titles.forEach(t => {{
            t.style.animation = 'none';
            t.offsetHeight; 
            t.style.animation = null;
        }});
        // Reset SVG
        setupSVGAnimation();
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
