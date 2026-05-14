def create_component(
    output_dir: str,
    title_text: str = "Bento Layout System",
    body_text: str = "A modern, responsive grid utilizing string-based template areas and zero-absolute-position stacking for seamless content layering.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#8b5cf6",     # Vivid Purple
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Bento Grid with Stacking effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#09090b"
        text_color = "#fafafa"
        text_muted = "#a1a1aa"
        surface_color = "rgba(255, 255, 255, 0.03)"
        surface_hover = "rgba(255, 255, 255, 0.06)"
        border_color = "rgba(255, 255, 255, 0.08)"
        shadow = "0 10px 40px rgba(0, 0, 0, 0.4)"
    else:
        bg_color = "#f4f4f5"
        text_color = "#09090b"
        text_muted = "#52525b"
        surface_color = "#ffffff"
        surface_hover = "#fafafa"
        border_color = "rgba(0, 0, 0, 0.06)"
        shadow = "0 10px 40px rgba(0, 0, 0, 0.05)"

    # === CSS ===
    css = f"""/* Bento Grid Component */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --surface: {surface_color};
    --surface-hover: {surface_hover};
    --border: {border_color};
    --shadow: {shadow};
    --max-width: {width_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    overflow-x: hidden;
}}

/* -- Grid Layout Architecture -- */
.bento-wrapper {{
    width: 100%;
    max-width: var(--max-width);
}}

.bento-container {{
    display: grid;
    /* Desktop: 4 columns */
    grid-template-columns: repeat(4, 1fr);
    /* Desktop: 2 rows with a minimum height */
    grid-template-rows: repeat(2, minmax(280px, auto));
    gap: 1.5rem;
    
    /* The Magic String Layout */
    grid-template-areas:
        "hero hero box2 box3"
        "hero hero box4 box5";
}}

/* -- Item Base Styling -- */
.bento-item {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 28px;
    box-shadow: var(--shadow);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    position: relative;
    /* Smooth transition for mouseleave */
    transition: background 0.3s ease, border-color 0.3s ease;
    /* Entry animation applied via keyframes */
    animation: slideUpFade 0.7s cubic-bezier(0.16, 1, 0.3, 1) backwards;
}}

/* Staggered entry */
.bento-item.hero {{ animation-delay: 0.1s; grid-area: hero; }}
.bento-item.box2 {{ animation-delay: 0.2s; grid-area: box2; }}
.bento-item.box3 {{ animation-delay: 0.3s; grid-area: box3; }}
.bento-item.box4 {{ animation-delay: 0.4s; grid-area: box4; }}
.bento-item.box5 {{ animation-delay: 0.5s; grid-area: box5; }}

/* -- Grid Stacking Technique (Hero Box) -- */
/* Notice: NO absolute positioning is used here! */
.bento-item.hero {{
    display: grid;
    grid-template-areas: "stack";
}}

.hero .bg-layer {{
    grid-area: stack; /* Assign to stack area */
    background: radial-gradient(circle at 80% 20%, var(--accent) 0%, transparent 60%);
    opacity: 0.15;
    z-index: 1;
}}

.hero .content-layer {{
    grid-area: stack; /* Assign to SAME stack area */
    z-index: 2;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    padding: 3rem;
}}

/* -- Standard Box Content -- */
.box-content {{
    padding: 2rem;
    display: flex;
    flex-direction: column;
    height: 100%;
    z-index: 2;
}}

.badge {{
    align-self: flex-start;
    background: rgba(139, 92, 246, 0.15); /* Accent tint */
    color: var(--accent);
    padding: 0.4rem 0.8rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: auto; /* Pushes content down if needed */
}}

.icon-wrapper {{
    width: 48px;
    height: 48px;
    border-radius: 14px;
    background: rgba(255, 255, 255, 0.05);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--accent);
    font-size: 1.25rem;
    margin-bottom: auto; /* Pushes text to the bottom */
}}

.bento-item h2 {{
    font-size: 2rem;
    font-weight: 600;
    margin-bottom: 0.75rem;
    letter-spacing: -0.02em;
}}

.bento-item h3 {{
    font-size: 1.25rem;
    font-weight: 500;
    margin-bottom: 0.5rem;
}}

.bento-item p {{
    color: var(--text-muted);
    font-size: 0.95rem;
    line-height: 1.5;
}}

/* -- Animations -- */
@keyframes slideUpFade {{
    0% {{ opacity: 0; transform: translateY(30px); }}
    100% {{ opacity: 1; transform: translateY(0); }}
}}

/* -- Responsive Reflows -- */
@media (max-width: 1024px) {{
    .bento-container {{
        /* Tablet: 2 columns */
        grid-template-columns: repeat(2, 1fr);
        grid-template-rows: repeat(4, minmax(220px, auto));
        grid-template-areas:
            "hero hero"
            "hero hero"
            "box2 box3"
            "box4 box5";
    }}
}}

@media (max-width: 640px) {{
    .bento-container {{
        /* Mobile: 1 column */
        grid-template-columns: 1fr;
        grid-auto-rows: minmax(200px, auto);
        /* Redefine areas into a simple vertical stack */
        grid-template-areas:
            "hero"
            "box2"
            "box3"
            "box4"
            "box5";
    }}
    .hero .content-layer {{
        padding: 2rem;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Responsive Bento Grid</title>
    <!-- Fonts & Icons -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <div class="bento-wrapper">
        <div class="bento-container">
            
            <!-- Hero Item using Grid Stacking -->
            <div class="bento-item hero">
                <div class="bg-layer"></div>
                <div class="content-layer">
                    <span class="badge" style="margin-bottom: 1rem;">Core Concept</span>
                    <h2>{title_text}</h2>
                    <p>{body_text}</p>
                </div>
            </div>

            <!-- Standard Items -->
            <div class="bento-item box2">
                <div class="box-content">
                    <div class="icon-wrapper">
                        <i class="fa-solid fa-layer-group"></i>
                    </div>
                    <h3>Grid Areas</h3>
                    <p>Strings mapping layout structures dynamically.</p>
                </div>
            </div>

            <div class="bento-item box3">
                <div class="box-content">
                    <div class="icon-wrapper">
                        <i class="fa-solid fa-mobile-screen-button"></i>
                    </div>
                    <h3>Responsive</h3>
                    <p>Seamless structural reflows via media queries.</p>
                </div>
            </div>

            <div class="bento-item box4">
                <div class="box-content">
                    <div class="icon-wrapper">
                        <i class="fa-solid fa-code"></i>
                    </div>
                    <h3>Clean DOM</h3>
                    <p>No wrapper divs needed for repositioning.</p>
                </div>
            </div>

            <div class="bento-item box5">
                <div class="box-content">
                    <div class="icon-wrapper">
                        <i class="fa-solid fa-bolt"></i>
                    </div>
                    <h3>Performant</h3>
                    <p>Native CSS grid algorithms render instantly.</p>
                </div>
            </div>

        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// 3D Hover Tilt Effect for Bento Items
document.addEventListener('DOMContentLoaded', () => {{
    const bentoItems = document.querySelectorAll('.bento-item');

    // Only apply hover effects on non-touch devices
    if (window.matchMedia("(pointer: fine)").matches) {{
        bentoItems.forEach(item => {{
            
            item.addEventListener('mousemove', (e) => {{
                // Get mouse position relative to the element
                const rect = item.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                // Calculate center
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                
                // Calculate rotation (divisor controls intensity)
                const rotateX = ((y - centerY) / 25).toFixed(2);
                const rotateY = ((centerX - x) / 25).toFixed(2);
                
                item.style.transform = `perspective(1000px) rotateX(${{rotateX}}deg) rotateY(${{rotateY}}deg) scale3d(1.02, 1.02, 1.02)`;
                item.style.zIndex = 10;
            }});
            
            item.addEventListener('mouseleave', () => {{
                // Reset with a smooth transition via JS assignment
                item.style.transition = 'transform 0.5s cubic-bezier(0.16, 1, 0.3, 1)';
                item.style.transform = `perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)`;
                item.style.zIndex = 1;
                
                // Remove transition class after it finishes so mousemove is snappy again
                setTimeout(() => {{
                    item.style.transition = 'background 0.3s ease, border-color 0.3s ease';
                }}, 500);
            }});
            
            item.addEventListener('mouseenter', () => {{
                // Remove transition on enter for immediate mouse tracking
                item.style.transition = 'none';
            }});
        }});
    }}
}});
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
