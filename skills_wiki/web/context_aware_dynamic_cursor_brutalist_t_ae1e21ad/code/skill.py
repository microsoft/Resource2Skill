def create_component(
    output_dir: str,
    title_text: str = "Creative Product Designer",
    body_text: str = "Hover over the elements below to see the context-aware cursor in action.",
    color_scheme: str = "light",        
    accent_color: str = "#f15a24",     # Orange accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Context-Aware Custom Cursor Hero effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#121212"
        text_color = "#f4f4f0"
        surface_color = "#222222"
        muted_text = "#888888"
    else:
        bg_color = "#f4f4f0"
        text_color = "#111111"
        surface_color = "#e0e0d8"
        muted_text = "#666666"

    # === CSS ===
    css = f"""/* Context-Aware Custom Cursor & Brutalist Hero */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --muted: {muted_text};
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    overflow-x: hidden;
    padding: 40px;
}}

/* Disable default cursors only on devices with a mouse */
@media (pointer: fine) {{
    body, a, button, .project-card {{
        cursor: none !important;
    }}
}}

/* Hide custom cursor on touch devices */
@media (pointer: coarse), (hover: none) {{
    .custom-cursor {{
        display: none !important;
    }}
}}

.container {{
    width: 100%;
    max-width: {width_px}px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    min-height: {height_px}px;
}}

.hero {{
    margin-bottom: 80px;
}}

.hero-title {{
    font-size: clamp(3rem, 8vw, 8rem);
    font-weight: 800;
    line-height: 0.9;
    letter-spacing: -0.04em;
    text-transform: uppercase;
    max-width: 900px;
    margin-bottom: 24px;
}}

.hero-subtitle {{
    font-size: clamp(1rem, 2vw, 1.5rem);
    font-weight: 400;
    color: var(--muted);
    max-width: 600px;
    line-height: 1.5;
    /* Create a target area for the cursor */
    display: inline-block; 
}}

.projects-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 40px;
}}

.project-card {{
    display: flex;
    flex-direction: column;
    gap: 16px;
    text-decoration: none;
    color: inherit;
}}

.project-image {{
    width: 100%;
    aspect-ratio: 4/3;
    border-radius: 12px;
    background-color: var(--surface);
    transition: transform 0.5s cubic-bezier(0.16, 1, 0.3, 1);
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

/* Mimic the purple card seen in the video */
.project-card.featured .project-image {{
    background-color: #9b51e0;
}}

.project-card:hover .project-image {{
    transform: scale(0.97);
}}

.project-title {{
    font-size: 1.25rem;
    font-weight: 600;
    letter-spacing: -0.01em;
}}

/* --- Custom Cursor Styles --- */
.custom-cursor {{
    position: fixed;
    top: 0;
    left: 0;
    width: 16px;
    height: 16px;
    background-color: var(--accent);
    border-radius: 50%;
    pointer-events: none; /* Critical: allows clicking/hovering elements underneath */
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
    /* Centering offset is handled in JS */
    transition: width 0.4s cubic-bezier(0.25, 1, 0.5, 1), 
                height 0.4s cubic-bezier(0.25, 1, 0.5, 1),
                background-color 0.4s ease;
    will-change: transform, width, height;
}}

.custom-cursor.active {{
    width: 100px;
    height: 100px;
}}

.cursor-text {{
    color: #ffffff; /* High contrast inner text */
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    opacity: 0;
    transition: opacity 0.2s ease;
    text-align: center;
    padding: 10px;
    line-height: 1.2;
}}

.custom-cursor.active .cursor-text {{
    opacity: 1;
    transition-delay: 0.1s; /* Slight delay so the circle expands before text appears */
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
        <div class="hero">
            <h1 class="hero-title">{title_text}</h1>
            <p class="hero-subtitle" data-cursor="Read Bio">{body_text}</p>
        </div>
        
        <div class="projects-grid">
            <a href="#" class="project-card featured" data-cursor="See Project">
                <div class="project-image">
                    <!-- Abstract representation of an interface inside the card -->
                    <div style="width: 70%; height: 60%; background: rgba(255,255,255,0.1); border-radius: 8px; border-top: 20px solid rgba(255,255,255,0.2);"></div>
                </div>
                <h3 class="project-title">Talent Linker App</h3>
            </a>
            
            <a href="#" class="project-card" data-cursor="Play Reel">
                <div class="project-image"></div>
                <h3 class="project-title">Motion Design Reel</h3>
            </a>
        </div>
    </div>

    <!-- The Custom Cursor DOM Element -->
    <div class="custom-cursor" id="cursor">
        <span class="cursor-text" id="cursor-text"></span>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Context-Aware Dynamic Cursor Logic
document.addEventListener('DOMContentLoaded', () => {{
    // Exit immediately if the user is on a touch device
    if (!window.matchMedia("(pointer: fine)").matches) return;

    const cursor = document.getElementById('cursor');
    const cursorText = document.getElementById('cursor-text');
    
    // Start coordinates in the center of the screen
    let mouseX = window.innerWidth / 2;
    let mouseY = window.innerHeight / 2;
    
    // Eased coordinates
    let cursorX = mouseX;
    let cursorY = mouseY;
    
    // Easing factor (0.1 to 0.3 is ideal for premium feeling trailing)
    const speed = 0.2; 
    
    // Animation Loop
    function render() {{
        // Linear Interpolation (Lerp) formula
        cursorX += (mouseX - cursorX) * speed;
        cursorY += (mouseY - cursorY) * speed;
        
        // Use translate3d for GPU acceleration. Subtract 50% to perfectly center the circle on the pointer.
        cursor.style.transform = `translate3d(calc(${{cursorX}}px - 50%), calc(${{cursorY}}px - 50%), 0)`;
        
        requestAnimationFrame(render);
    }}
    
    // Start loop
    requestAnimationFrame(render);
    
    // Update target coordinates on mouse move
    window.addEventListener('mousemove', (e) => {{
        mouseX = e.clientX;
        mouseY = e.clientY;
    }});
    
    // Handle Interactive Context Zones
    const targets = document.querySelectorAll('[data-cursor]');
    
    targets.forEach(target => {{
        target.addEventListener('mouseenter', () => {{
            const text = target.getAttribute('data-cursor');
            if (text) {{
                cursorText.innerText = text;
                cursor.classList.add('active');
            }}
        }});
        
        target.addEventListener('mouseleave', () => {{
            cursor.classList.remove('active');
            // We do NOT clear the innerText immediately, so it fades out smoothly rather than snapping empty
        }});
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
