def create_component(
    output_dir: str,
    title_text: str = "Discover the Features",
    body_text: str = "A responsive, asymmetrical layout powered by CSS Grid Areas.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#6366f1",     # CSS hex color for accent (e.g., Indigo)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Bento Box Grid visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_color = "#f8fafc"
        text_muted = "#94a3b8"
        surface_color = "rgba(255, 255, 255, 0.05)"
        surface_hover = "rgba(255, 255, 255, 0.08)"
        border_color = "rgba(255, 255, 255, 0.1)"
        shadow_color = "rgba(0, 0, 0, 0.3)"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        text_muted = "#475569"
        surface_color = "#ffffff"
        surface_hover = "#f1f5f9"
        border_color = "rgba(0, 0, 0, 0.05)"
        shadow_color = "rgba(0, 0, 0, 0.05)"

    # === CSS ===
    css = f"""/* Responsive Bento Grid Component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --surface: {surface_color};
    --surface-hover: {surface_hover};
    --border: {border_color};
    --shadow: {shadow_color};
    --max-width: {width_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 4rem 2rem;
    overflow-x: hidden;
}}

.header {{
    text-align: center;
    margin-bottom: 3rem;
    max-width: 600px;
}}

.title {{
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -0.025em;
    margin-bottom: 1rem;
}}

.body-text {{
    font-size: 1.125rem;
    color: var(--text-muted);
    line-height: 1.6;
}}

/* === BENTO GRID LAYOUT === */
.bento-grid {{
    display: grid;
    width: 100%;
    max-width: var(--max-width);
    /* 4 Column layout by default */
    grid-template-columns: repeat(4, 1fr);
    /* Automatically size rows, min 220px */
    grid-auto-rows: minmax(220px, auto);
    gap: 1.5rem;
    
    /* The Magic: Mapping the layout */
    grid-template-areas:
        "box-1 box-1 box-2 box-3"
        "box-1 box-1 box-4 box-5";
}}

/* Base Box Styles */
.box {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 1.5rem;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
    position: relative;
    overflow: hidden;
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), 
                box-shadow 0.3s cubic-bezier(0.4, 0, 0.2, 1), 
                background 0.3s ease;
    
    /* Animation initial state */
    opacity: 0;
    transform: translateY(20px);
}}

.box.visible {{
    opacity: 1;
    transform: translateY(0);
}}

.box:hover {{
    transform: translateY(-4px);
    box-shadow: 0 12px 24px var(--shadow);
    background: var(--surface-hover);
}}

/* Assigning Grid Areas */
.box-1 {{ grid-area: box-1; }}
.box-2 {{ grid-area: box-2; }}
.box-3 {{ grid-area: box-3; }}
.box-4 {{ grid-area: box-4; }}
.box-5 {{ grid-area: box-5; }}

/* === GRID STACKING (BOX 1 HERO) === */
.box-1 {{
    /* Create a 1-cell grid to stack elements on top of each other */
    display: grid;
    grid-template-areas: "stack";
    padding: 0; /* Remove padding so background fills */
    border: none;
}}

.box-1 > * {{
    /* Both the background and content sit in the exact same cell */
    grid-area: stack;
}}

.box-1 .bg-gradient {{
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, var(--accent), #3b82f6, #9333ea);
    opacity: 0.9;
    border-radius: 1.5rem;
}}

.box-1 .content {{
    z-index: 1;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    padding: 2.5rem;
    color: #ffffff;
}}

.box-1 h2 {{
    font-size: 2rem;
    margin-bottom: 0.5rem;
}}

.box-1 p {{
    color: rgba(255,255,255,0.8);
    font-size: 1.1rem;
}}

/* Standard Box Content */
.icon-wrapper {{
    width: 48px;
    height: 48px;
    border-radius: 12px;
    background: rgba(99, 102, 241, 0.1); /* Derived from accent roughly */
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1.5rem;
    color: var(--accent);
}}

.box h3 {{
    font-size: 1.25rem;
    margin-bottom: 0.5rem;
}}

.box p {{
    color: var(--text-muted);
    font-size: 0.95rem;
    line-height: 1.5;
}}

/* === RESPONSIVE RESTRUCTURING === */

/* Tablet Breakpoint */
@media (max-width: 900px) {{
    .bento-grid {{
        grid-template-columns: repeat(3, 1fr);
        grid-template-areas:
            "box-1 box-1 box-2"
            "box-1 box-1 box-3"
            "box-4 box-5 box-5";
    }}
}}

/* Mobile Breakpoint */
@media (max-width: 600px) {{
    .bento-grid {{
        grid-template-columns: 1fr;
        grid-template-areas:
            "box-1"
            "box-2"
            "box-3"
            "box-4"
            "box-5";
    }}
    .box-1 {{
        min-height: 300px;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    
    <div class="header">
        <h1 class="title">{title_text}</h1>
        <p class="body-text">{body_text}</p>
    </div>

    <div class="bento-grid">
        
        <!-- Box 1: Hero spanning 2x2 with Grid Stacking -->
        <div class="box box-1">
            <div class="bg-gradient"></div>
            <div class="content">
                <h2>Performance Analytics</h2>
                <p>Real-time insights powered by advanced CSS Grid layouts.</p>
            </div>
        </div>

        <!-- Box 2 -->
        <div class="box box-2">
            <div class="icon-wrapper">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
            </div>
            <h3>Lightning Fast</h3>
            <p>Optimized rendering without heavy JavaScript calculations.</p>
        </div>

        <!-- Box 3 -->
        <div class="box box-3">
            <div class="icon-wrapper">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg>
            </div>
            <h3>Adaptive Layout</h3>
            <p>Bento grids restructure flawlessly across mobile devices.</p>
        </div>

        <!-- Box 4 -->
        <div class="box box-4">
            <div class="icon-wrapper">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            </div>
            <h3>Secure Core</h3>
            <p>Built with native web standards ensuring top security.</p>
        </div>

        <!-- Box 5 -->
        <div class="box box-5">
            <div class="icon-wrapper">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>
            </div>
            <h3>Seamless Integration</h3>
            <p>Easily drop this component into existing application views.</p>
        </div>

    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Staggered entrance animation using Intersection Observer
document.addEventListener('DOMContentLoaded', () => {{
    const boxes = document.querySelectorAll('.box');
    
    const observerOptions = {{
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    }};

    const observer = new IntersectionObserver((entries, observer) => {{
        entries.forEach((entry, index) => {{
            if (entry.isIntersecting) {{
                // Stagger the animation timing based on index
                setTimeout(() => {{
                    entry.target.classList.add('visible');
                }}, index * 100); // 100ms delay between each box
                
                // Stop observing once animated in
                observer.unobserve(entry.target);
            }}
        }});
    }}, observerOptions);

    boxes.forEach(box => {{
        observer.observe(box);
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
