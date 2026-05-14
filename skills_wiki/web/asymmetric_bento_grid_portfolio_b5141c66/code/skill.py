def create_component(
    output_dir: str,
    title_text: str = "Hi, I'm Alex. A full-stack developer.",
    body_text: str = "I build digital products that solve user problems and boast breathtaking interfaces.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#6366f1",     # CSS hex color for accent (e.g., Indigo)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Asymmetric Bento Grid Portfolio.
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Helper to create rgba from hex for glows
    def hex_to_rgba(hex_code, alpha):
        hex_code = hex_code.lstrip('#')
        if len(hex_code) == 3:
            hex_code = ''.join(c + c for c in hex_code)
        r, g, b = tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))
        return f"rgba({r}, {g}, {b}, {alpha})"

    accent_glow = hex_to_rgba(accent_color, 0.25)
    accent_surface = hex_to_rgba(accent_color, 0.1)

    if color_scheme == "dark":
        bg_color = "#090a0f"
        text_color = "#ffffff"
        muted_text = "#8b949e"
        surface_color = "rgba(255, 255, 255, 0.02)"
        surface_hover = "rgba(255, 255, 255, 0.04)"
        border_color = "rgba(255, 255, 255, 0.08)"
    else:
        bg_color = "#f4f5f7"
        text_color = "#111827"
        muted_text = "#4b5563"
        surface_color = "#ffffff"
        surface_hover = "#f9fafb"
        border_color = "rgba(0, 0, 0, 0.08)"

    css = f"""/* Asymmetric Bento Grid — generated component */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {muted_text};
    --surface: {surface_color};
    --surface-hover: {surface_hover};
    --border: {border_color};
    --accent: {accent_color};
    --accent-glow: {accent_glow};
    --accent-surface: {accent_surface};
    --width: {width_px}px;
    --height: {height_px}px;
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
    align-items: center;
    justify-content: center;
    padding: 40px 20px;
    position: relative;
    overflow-x: hidden;
}}

/* Ambient Background Glow */
body::before {{
    content: '';
    position: absolute;
    top: -20%;
    left: 10%;
    width: 60vw;
    height: 60vw;
    background: radial-gradient(circle, var(--accent-surface) 0%, transparent 60%);
    filter: blur(80px);
    z-index: -1;
    pointer-events: none;
}}

.container {{
    width: 100%;
    max-width: var(--width);
    /* For visual preview purposes, min-height allows the grid to flex natively */
    min-height: min(var(--height), 90vh); 
}}

/* === Grid Layout === */
.bento-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    grid-auto-rows: minmax(180px, auto);
    gap: 24px;
}}

/* === Bento Card Base === */
.bento-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 24px;
    padding: 32px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
    overflow: hidden;
    transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1), 
                border-color 0.4s ease, 
                box-shadow 0.4s ease,
                background 0.4s ease;
    text-decoration: none;
    color: inherit;
}}

.bento-card:hover {{
    transform: translateY(-4px);
    border-color: var(--accent);
    background: var(--surface-hover);
    box-shadow: 0 12px 32px -12px var(--accent-glow);
}}

/* Card Spanning Utilities */
.span-2x2 {{ grid-column: span 2; grid-row: span 2; }}
.span-2x1 {{ grid-column: span 2; grid-row: span 1; }}
.span-3x1 {{ grid-column: span 3; grid-row: span 1; }}

/* === Typography & Internal Elements === */
h1 {{
    font-size: clamp(2rem, 3vw, 3rem);
    line-height: 1.1;
    font-weight: 700;
    margin-bottom: 16px;
    letter-spacing: -0.02em;
}}

h3 {{
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 8px;
}}

p {{
    color: var(--text-muted);
    line-height: 1.6;
    font-size: 1.05rem;
}}

.stat-val {{
    font-size: 3.5rem;
    font-weight: 800;
    color: var(--accent);
    line-height: 1;
    margin-bottom: 8px;
}}

/* Tech Stack Pills */
.pill-container {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: auto;
}}

.pill {{
    background: var(--accent-surface);
    color: var(--accent);
    padding: 6px 14px;
    border-radius: 100px;
    font-size: 0.85rem;
    font-weight: 500;
    border: 1px solid var(--accent-glow);
}}

/* Featured Project Image Faux UI */
.project-ui {{
    margin-top: 20px;
    height: 100px;
    background: linear-gradient(135deg, rgba(255,255,255,0.05), transparent);
    border-radius: 12px 12px 0 0;
    border: 1px solid var(--border);
    border-bottom: none;
    position: relative;
    overflow: hidden;
}}
.project-ui::before {{
    content: '';
    position: absolute;
    top: 12px; left: 16px;
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--border);
    box-shadow: 14px 0 0 var(--border), 28px 0 0 var(--border);
}}

/* CTA Card */
.cta-card {{
    background: var(--accent);
    color: #fff; /* Always white text on accent for contrast */
    border: none;
    justify-content: center;
    align-items: center;
    text-align: center;
}}
.cta-card p {{ color: rgba(255,255,255,0.8); }}
.cta-card:hover {{
    background: var(--accent);
    box-shadow: 0 16px 40px -8px var(--accent-glow);
    filter: brightness(1.1);
}}
.arrow {{
    font-size: 2rem;
    margin-top: 12px;
    transition: transform 0.3s ease;
}}
.cta-card:hover .arrow {{
    transform: translateX(6px) rotate(-45deg);
}}

/* === Responsiveness === */
@media (max-width: 1024px) {{
    .bento-grid {{ grid-template-columns: repeat(3, 1fr); }}
    .span-3x1 {{ grid-column: span 2; }}
}}

@media (max-width: 768px) {{
    .bento-grid {{ grid-template-columns: repeat(2, 1fr); }}
    .span-2x2, .span-2x1, .span-3x1 {{ grid-column: span 2; }}
}}

@media (max-width: 480px) {{
    .bento-grid {{ grid-template-columns: 1fr; }}
    .span-2x2, .span-2x1, .span-3x1 {{ grid-column: span 1; }}
    .bento-card {{ padding: 24px; }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bento Grid Portfolio</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="bento-grid">
            
            <!-- Main Intro (2x2) -->
            <div class="bento-card span-2x2">
                <div>
                    <h1>{title_text}</h1>
                    <p>{body_text}</p>
                </div>
                <div class="pill-container" style="margin-top: 32px;">
                    <span class="pill">Available for work</span>
                    <span class="pill" style="background: transparent; border-color: var(--border); color: var(--text-muted)">Remote</span>
                </div>
            </div>

            <!-- Stat 1 (1x1) -->
            <div class="bento-card">
                <div class="stat-val">5+</div>
                <p>Years of<br>Experience</p>
            </div>

            <!-- Stat 2 (1x1) -->
            <div class="bento-card">
                <div class="stat-val">40</div>
                <p>Projects<br>Delivered</p>
            </div>

            <!-- Stack (2x1) -->
            <div class="bento-card span-2x1">
                <h3>My Stack</h3>
                <p>Technologies I work with daily</p>
                <div class="pill-container">
                    <span class="pill">React</span>
                    <span class="pill">TypeScript</span>
                    <span class="pill">Node.js</span>
                    <span class="pill">Python</span>
                    <span class="pill">CSS Grid</span>
                </div>
            </div>

            <!-- Featured Project (3x1) -->
            <a href="#" class="bento-card span-3x1">
                <div>
                    <h3>Featured Project: FinTech Dashboard</h3>
                    <p>A complex data visualization tool for enterprise finance teams.</p>
                </div>
                <div class="project-ui"></div>
            </a>

            <!-- CTA (1x1) -->
            <a href="#" class="bento-card cta-card">
                <h3>Let's Talk</h3>
                <p>Start a project</p>
                <div class="arrow">&rarr;</div>
            </a>

        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Optional: Add simple entry animations using Intersection Observer
document.addEventListener('DOMContentLoaded', () => {
    const cards = document.querySelectorAll('.bento-card');
    
    // Initial state
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        // Stagger animation based on DOM order
        card.style.transitionDelay = `${index * 0.05}s`;
    });

    // Reveal on load/scroll
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                // Reset transition after entrance so hover effects work smoothly
                setTimeout(() => {
                    entry.target.style.transition = 'transform 0.4s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.4s ease, box-shadow 0.4s ease, background 0.4s ease';
                    entry.target.style.transitionDelay = '0s';
                }, 600 + (cards.length * 50)); 
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    cards.forEach(card => observer.observe(card));
});
"""

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
