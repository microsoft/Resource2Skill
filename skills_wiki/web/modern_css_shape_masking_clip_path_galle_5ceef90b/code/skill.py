def create_component(
    output_dir: str,
    title_text: str = "CSS Clip-Path Shapes",
    body_text: str = "Hover over the cards to see the clip-path morphing animations.",
    color_scheme: str = "dark",
    accent_color: str = "#00e5ff", 
    width_px: int = 1000,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Modern CSS Shape Masking (Clip-Path Gallery) visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#050914"
        text_color = "#ffffff"
        card_bg = "linear-gradient(135deg, #1a233a 0%, #0d111c 100%)"
        grid_lines = "rgba(255,255,255,0.05)"
    else:
        bg_color = "#f4f7f6"
        text_color = "#111827"
        card_bg = "linear-gradient(135deg, #ffffff 0%, #e2e8f0 100%)"
        grid_lines = "rgba(0,0,0,0.05)"

    # === CSS ===
    css = f"""/* Modern CSS Shape Masking (Clip-Path Gallery) */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --card-bg: {card_bg};
    --grid-lines: {grid_lines};
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
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    /* Subtle background grid to emphasize geometry */
    background-image: 
        linear-gradient(var(--grid-lines) 1px, transparent 1px),
        linear-gradient(90deg, var(--grid-lines) 1px, transparent 1px);
    background-size: 40px 40px;
}}

.container {{
    width: 100%;
    max-width: var(--width);
    min-height: var(--height);
    padding: 3rem 1.5rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 3rem;
}}

.header {{
    text-align: center;
    max-width: 600px;
}}

.title {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    letter-spacing: -0.05em;
}}

.title span {{
    color: var(--accent);
}}

.body-text {{
    font-size: 1.1rem;
    opacity: 0.8;
    line-height: 1.6;
}}

/* Grid Layout for Cards */
.shape-gallery {{
    display: flex;
    flex-wrap: wrap;
    gap: 2rem;
    justify-content: center;
    width: 100%;
}}

/* Base Card Styles */
.shape-card {{
    position: relative;
    width: 220px;
    height: 220px;
    background: var(--card-bg);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-decoration: none;
    color: var(--text);
    transition: clip-path 0.5s cubic-bezier(0.25, 1, 0.5, 1), transform 0.3s ease;
    /* Inner glow effect */
    box-shadow: inset 0 0 0 2px rgba(255,255,255,0.1);
}}

.shape-card:hover {{
    transform: translateY(-5px);
    /* Morph to full rectangle on hover */
    clip-path: polygon(0% 0%, 100% 0%, 100% 100%, 0% 100%) !important;
}}

.shape-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(135deg, var(--accent) 0%, transparent 100%);
    opacity: 0.15;
    z-index: 0;
}}

.shape-content {{
    position: relative;
    z-index: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
}}

.shape-content svg {{
    width: 40px;
    height: 40px;
    fill: var(--accent);
    transition: transform 0.3s ease;
}}

.shape-card:hover .shape-content svg {{
    transform: scale(1.1);
}}

.shape-label {{
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    font-size: 0.85rem;
}}

.shape-code {{
    font-family: monospace;
    font-size: 0.7rem;
    opacity: 0.6;
    background: rgba(0,0,0,0.3);
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
}}

/* === Specific Clip-Path Implementations === */

/* 1. Circle */
.shape-circle {{
    clip-path: circle(40% at 50% 50%);
}}

/* 2. Ellipse */
.shape-ellipse {{
    clip-path: ellipse(45% 30% at 50% 50%);
}}

/* 3. Inset */
.shape-inset {{
    clip-path: inset(10% 15% 10% 15% round 20px);
}}

/* 4. Polygon (Hexagon) */
.shape-polygon {{
    clip-path: polygon(50% 5%, 95% 25%, 95% 75%, 50% 95%, 5% 75%, 5% 25%);
}}

/* 5. Path (Custom SVG Path logic applied to a 220x220 box) */
.shape-path {{
    /* Using absolute coordinates matching the 220px box */
    clip-path: path("M 20 20 L 200 20 L 200 150 A 30 30 0 0 1 170 180 L 50 180 A 30 30 0 0 0 20 210 Z");
}}

/* Responsive adjustments */
@media (max-width: 768px) {{
    .shape-card {{
        width: 180px;
        height: 180px;
    }}
    .shape-path {{
        /* Path needs scaling adjustment on resize, so we fallback to a complex polygon for small screens */
        clip-path: polygon(10% 10%, 90% 10%, 90% 70%, 75% 85%, 25% 85%, 10% 100%);
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
    <div class="container">
        <header class="header">
            <h1 class="title">CSS <span>Clip-Path</span> Shapes</h1>
            <p class="body-text">{body_text}</p>
        </header>

        <main class="shape-gallery">
            
            <!-- 1. Circle -->
            <a href="#" class="shape-card shape-circle">
                <div class="shape-content">
                    <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"></circle></svg>
                    <span class="shape-label">Circle</span>
                    <span class="shape-code">circle(40%)</span>
                </div>
            </a>

            <!-- 2. Ellipse -->
            <a href="#" class="shape-card shape-ellipse">
                <div class="shape-content">
                    <svg viewBox="0 0 24 24"><ellipse cx="12" cy="12" rx="10" ry="6"></ellipse></svg>
                    <span class="shape-label">Ellipse</span>
                    <span class="shape-code">ellipse(...)</span>
                </div>
            </a>

            <!-- 3. Inset -->
            <a href="#" class="shape-card shape-inset">
                <div class="shape-content">
                    <svg viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="4"></rect></svg>
                    <span class="shape-label">Inset</span>
                    <span class="shape-code">inset(10%...round)</span>
                </div>
            </a>

            <!-- 4. Polygon -->
            <a href="#" class="shape-card shape-polygon">
                <div class="shape-content">
                    <svg viewBox="0 0 24 24"><polygon points="12 2 22 8.5 22 15.5 12 22 2 15.5 2 8.5 12 2"></polygon></svg>
                    <span class="shape-label">Polygon</span>
                    <span class="shape-code">polygon(50% 5%...)</span>
                </div>
            </a>

            <!-- 5. Path -->
            <a href="#" class="shape-card shape-path">
                <div class="shape-content">
                    <svg viewBox="0 0 24 24"><path d="M4 4 h16 v10 a4 4 0 0 1 -4 4 h-8 a4 4 0 0 0 -4 4 z"></path></svg>
                    <span class="shape-label">Path</span>
                    <span class="shape-code">path("M...")</span>
                </div>
            </a>

        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Modern CSS Shape Masking - Interaction Enhancement
document.addEventListener('DOMContentLoaded', () => {{
    const cards = document.querySelectorAll('.shape-card');

    // Add a subtle particle click effect to demonstrate hit-area mapping
    // clip-path naturally restricts pointer events to the visible clipped area!
    cards.forEach(card => {{
        card.addEventListener('click', (e) => {{
            e.preventDefault();
            
            // Create a ripple element
            const ripple = document.createElement('div');
            
            // Styling the ripple
            Object.assign(ripple.style, {{
                position: 'absolute',
                left: `${{e.offsetX}}px`,
                top: `${{e.offsetY}}px`,
                width: '10px',
                height: '10px',
                background: 'var(--accent)',
                borderRadius: '50%',
                transform: 'translate(-50%, -50%)',
                animation: 'rippleAnim 0.6s ease-out forwards',
                pointerEvents: 'none',
                zIndex: '10'
            }});
            
            card.appendChild(ripple);
            
            // Cleanup
            setTimeout(() => {{
                ripple.remove();
            }}, 600);
        }});
    }});
    
    // Inject keyframes for the ripple
    const style = document.createElement('style');
    style.textContent = `
        @keyframes rippleAnim {{
            0% {{ transform: translate(-50%, -50%) scale(1); opacity: 1; }}
            100% {{ transform: translate(-50%, -50%) scale(20); opacity: 0; }}
        }}
    `;
    document.head.appendChild(style);
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
