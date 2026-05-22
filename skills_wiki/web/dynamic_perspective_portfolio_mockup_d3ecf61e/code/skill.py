def create_component(
    output_dir: str,
    title_text: str = "LemonSqueezy",
    body_text: str = "Empowering creatives on the road to financial freedom through tools, services, and technology.",
    color_scheme: str = "dark",        
    accent_color: str = "#8b5cf6",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Dynamic Perspective Portfolio Mockup.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0a0a0e"
        text_color = "#ffffff"
        text_muted = "#8a8a9e"
        surface_color = "rgba(255, 255, 255, 0.05)"
        mockup_bg = "#0d0d12"
        mockup_surface = "#1a1a24"
        mockup_border = "rgba(255, 255, 255, 0.08)"
        shadow_color = "rgba(0, 0, 0, 0.6)"
        glare_color = "rgba(255, 255, 255, 0.12)"
    else:
        bg_color = "#f4f5f7"
        text_color = "#0f172a"
        text_muted = "#64748b"
        surface_color = "rgba(0, 0, 0, 0.05)"
        mockup_bg = "#ffffff"
        mockup_surface = "#f8fafc"
        mockup_border = "rgba(0, 0, 0, 0.08)"
        shadow_color = "rgba(0, 0, 0, 0.15)"
        glare_color = "rgba(255, 255, 255, 0.4)"

    # === CSS ===
    css = f"""/* Dynamic Perspective Portfolio Mockup — generated component */
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
    --mockup-bg: {mockup_bg};
    --mockup-surface: {mockup_surface};
    --mockup-border: {mockup_border};
    --shadow-color: {shadow_color};
    --glare: {glare_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow-x: hidden;
}}

.container {{
    width: 100%;
    max-width: var(--width);
    min-height: var(--height);
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.showcase-section {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 60px;
    width: 90%;
    max-width: 1100px;
    padding: 40px 0;
}}

.text-content {{
    flex: 1;
    z-index: 2;
}}

.title {{
    font-size: 3.5rem;
    font-weight: 700;
    margin-bottom: 1.2rem;
    line-height: 1.1;
    letter-spacing: -0.03em;
}}

.body-text {{
    font-size: 1.125rem;
    color: var(--text-muted);
    margin-bottom: 2.5rem;
    line-height: 1.6;
    max-width: 400px;
}}

.btn {{
    display: inline-block;
    padding: 0.85rem 1.75rem;
    background: var(--text);
    color: var(--bg);
    text-decoration: none;
    font-weight: 500;
    font-size: 0.95rem;
    border-radius: 8px;
    transition: transform 0.2s, opacity 0.2s;
}}

.btn:hover {{
    transform: translateY(-2px);
    opacity: 0.9;
}}

.mockup-wrapper {{
    flex: 1.3;
    perspective: 2000px;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 40px; 
}}

.mockup-frame {{
    width: 100%;
    aspect-ratio: 4 / 3;
    background: var(--mockup-surface);
    border: 14px solid var(--mockup-bg);
    border-radius: 24px;
    box-shadow:
        0 40px 80px -20px var(--shadow-color),
        inset 0 0 0 1px var(--mockup-border),
        0 0 0 1px var(--mockup-border);
    position: relative;
    transform-style: preserve-3d;
    /* Initial state, updated by JS */
    transform: rotateY(-20deg) rotateX(15deg);
    cursor: grab;
}}

.mockup-frame:active {{
    cursor: grabbing;
}}

/* Inner UI Wireframe Simulation */
.ui-mockup {{
    position: absolute;
    inset: 0;
    border-radius: 8px; 
    background: var(--mockup-bg);
    display: flex;
    overflow: hidden;
}}

.ui-sidebar {{
    width: 25%;
    background: var(--mockup-surface);
    border-right: 1px solid var(--mockup-border);
    padding: 24px 20px;
    display: flex;
    flex-direction: column;
    gap: 28px;
}}

.ui-logo {{
    width: 36px;
    height: 36px;
    border-radius: 10px;
    background: linear-gradient(135deg, var(--accent), #e81cff);
}}

.ui-nav {{
    display: flex;
    flex-direction: column;
    gap: 14px;
}}

.ui-nav-item {{
    height: 10px;
    border-radius: 5px;
    background: var(--mockup-border);
}}

.ui-main {{
    flex: 1;
    display: flex;
    flex-direction: column;
}}

.ui-header {{
    height: 64px;
    border-bottom: 1px solid var(--mockup-border);
    padding: 0 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}}

.ui-search {{
    width: 140px;
    height: 24px;
    border-radius: 12px;
    background: var(--mockup-surface);
}}

.ui-avatar {{
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: var(--mockup-border);
}}

.ui-content {{
    padding: 32px;
    display: flex;
    flex-direction: column;
    gap: 24px;
    flex: 1;
    background: var(--mockup-bg);
}}

.ui-hero {{
    height: 140px;
    border-radius: 12px;
    background: linear-gradient(135deg, var(--mockup-surface) 0%, transparent 100%);
    border: 1px solid var(--mockup-border);
}}

.ui-grid {{
    display: flex;
    gap: 20px;
}}

.ui-card {{
    flex: 1;
    height: 90px;
    border-radius: 12px;
    background: var(--mockup-surface);
    border: 1px solid var(--mockup-border);
}}

/* Dynamic Light Glare */
.glare {{
    position: absolute;
    inset: -14px; /* Cover the bezel too */
    border-radius: 24px;
    background: radial-gradient(circle at 50% 50%, var(--glare) 0%, transparent 60%);
    opacity: 0;
    transition: opacity 0.4s ease;
    pointer-events: none;
    z-index: 10;
}}

/* Responsive */
@media (max-width: 900px) {{
    .showcase-section {{
        flex-direction: column;
        text-align: center;
        gap: 30px;
    }}
    .body-text {{
        margin: 0 auto 2rem auto;
    }}
    .mockup-wrapper {{
        width: 100%;
        padding: 10px;
    }}
    .title {{
        font-size: 2.5rem;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text} — Portfolio Case Study</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="showcase-section">
            
            <div class="text-content">
                <h1 class="title">{title_text}</h1>
                <p class="body-text">{body_text}</p>
                <a href="#" class="btn">Explore Case Study</a>
            </div>
            
            <div class="mockup-wrapper">
                <div class="mockup-frame">
                    <!-- Embedded UI Design Simulation -->
                    <div class="ui-mockup">
                        <div class="ui-sidebar">
                            <div class="ui-logo"></div>
                            <div class="ui-nav">
                                <div class="ui-nav-item" style="width: 80%;"></div>
                                <div class="ui-nav-item" style="width: 50%;"></div>
                                <div class="ui-nav-item" style="width: 70%;"></div>
                                <div class="ui-nav-item" style="width: 60%; margin-top: 20px;"></div>
                            </div>
                        </div>
                        <div class="ui-main">
                            <div class="ui-header">
                                <div class="ui-search"></div>
                                <div class="ui-avatar"></div>
                            </div>
                            <div class="ui-content">
                                <div class="ui-hero"></div>
                                <div class="ui-grid">
                                    <div class="ui-card"></div>
                                    <div class="ui-card"></div>
                                    <div class="ui-card"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <!-- End Embedded UI Design -->
                    
                    <div class="glare"></div>
                </div>
            </div>
            
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Dynamic Perspective Portfolio Mockup — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const wrapper = document.querySelector('.mockup-wrapper');
    const frame = document.querySelector('.mockup-frame');
    const glare = document.querySelector('.glare');

    if (!wrapper || !frame || !glare) return;

    // Default resting angles (matching the tutorial's aesthetic)
    const BASE_X = 15;
    const BASE_Y = -20;

    let targetX = BASE_X; 
    let targetY = BASE_Y; 
    let currentX = BASE_X;
    let currentY = BASE_Y;
    let glareX = 50;
    let glareY = 50;

    // Smooth Lerp Animation Loop
    function animate() {{
        currentX += (targetX - currentX) * 0.08;
        currentY += (targetY - currentY) * 0.08;
        
        // Apply 3D transform
        frame.style.transform = `rotateY(${{currentY}}deg) rotateX(${{currentX}}deg)`;
        requestAnimationFrame(animate);
    }}
    animate();

    wrapper.addEventListener('mousemove', (e) => {{
        const rect = wrapper.getBoundingClientRect();
        
        // Calculate mouse position relative to wrapper center
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        
        // Normalized values between -1 and 1
        const percentX = (x - centerX) / centerX;
        const percentY = (y - centerY) / centerY;
        
        // Map mouse movements to rotation limits (+/- 8deg on X, +/- 12deg on Y)
        targetX = BASE_X - (percentY * 8); 
        targetY = BASE_Y + (percentX * 12);
        
        // Move the glare effect seamlessly
        glareX = (x / rect.width) * 100;
        glareY = (y / rect.height) * 100;
        glare.style.background = `radial-gradient(circle at ${{glareX}}% ${{glareY}}%, var(--glare) 0%, transparent 60%)`;
    }});

    wrapper.addEventListener('mouseenter', () => {{
        glare.style.opacity = '1';
    }});

    wrapper.addEventListener('mouseleave', () => {{
        // Reset to default on exit
        targetX = BASE_X;
        targetY = BASE_Y;
        glare.style.opacity = '0';
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
