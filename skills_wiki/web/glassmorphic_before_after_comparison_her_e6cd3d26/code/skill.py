def create_component(
    output_dir: str,
    title_text: str = "From Concept to Reality in Milliseconds",
    body_text: str = "Experience the power of our AI engine. Drag the slider to witness rough wireframes turn into production-ready glassmorphism assets instantly.",
    color_scheme: str = "dark",
    accent_color: str = "#007AFF",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Glassmorphic Before/After Comparison Hero.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Helper to calculate RGB glow
    def hex_to_rgba(hex_color, alpha):
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3:
            hex_color = ''.join([c*2 for c in hex_color])
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f"rgba({r}, {g}, {b}, {alpha})"

    if color_scheme == "dark":
        bg_color = "#050A15"
        text_color = "#FFFFFF"
        text_muted = "#94A3B8"
        border_color = "rgba(255, 255, 255, 0.12)"
        surface_color = "rgba(255, 255, 255, 0.03)"
        card_bg = "rgba(255, 255, 255, 0.02)"
        grid_color = "rgba(255, 255, 255, 0.04)"
    else:
        bg_color = "#FAFAFA"
        text_color = "#0F172A"
        text_muted = "#64748B"
        border_color = "rgba(0, 0, 0, 0.1)"
        surface_color = "rgba(255, 255, 255, 0.7)"
        card_bg = "rgba(255, 255, 255, 0.9)"
        grid_color = "rgba(0, 0, 0, 0.04)"

    accent_glow = hex_to_rgba(accent_color, 0.4)
    accent_light = hex_to_rgba(accent_color, 0.1)

    css = f"""/* Glassmorphic Before/After Hero — generated component */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

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
    --accent-glow: {accent_glow};
    --accent-light: {accent_light};
    --border: {border_color};
    --surface: {surface_color};
    --card-bg: {card_bg};
    --grid-color: {grid_color};
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    overflow-x: hidden;
}}

.hero {{
    position: relative;
    width: 100%;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 80px 20px 120px;
    z-index: 1;
}}

.hero-bg {{
    position: absolute;
    inset: 0;
    z-index: -2;
    background-image: 
        linear-gradient(var(--grid-color) 1px, transparent 1px),
        linear-gradient(90deg, var(--grid-color) 1px, transparent 1px);
    background-size: 40px 40px;
    background-position: center center;
    mask-image: radial-gradient(ellipse at top, black 20%, transparent 80%);
    -webkit-mask-image: radial-gradient(ellipse at top, black 20%, transparent 80%);
}}

.hero-glow {{
    position: absolute;
    top: -100px;
    left: 50%;
    transform: translateX(-50%);
    width: 60vw;
    height: 40vh;
    background: radial-gradient(ellipse at center, var(--accent-glow) 0%, transparent 70%);
    z-index: -1;
    pointer-events: none;
    filter: blur(40px);
}}

.hero-content {{
    max-width: 800px;
    text-align: center;
    margin-bottom: 60px;
    animation: fadeUp 0.8s ease-out forwards;
}}

.badge {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 16px;
    border-radius: 20px;
    background: var(--surface);
    border: 1px solid var(--border);
    color: var(--text-muted);
    font-size: 0.875rem;
    font-weight: 500;
    margin-bottom: 24px;
    backdrop-filter: blur(8px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}}

.badge-dot {{
    width: 8px; height: 8px;
    background: var(--accent);
    border-radius: 50%;
    box-shadow: 0 0 10px var(--accent);
}}

.title {{
    font-size: clamp(2.5rem, 5vw, 4.5rem);
    font-weight: 700;
    line-height: 1.1;
    margin-bottom: 24px;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, var(--text) 30%, var(--text-muted));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

.subtitle {{
    font-size: clamp(1.125rem, 2vw, 1.25rem);
    color: var(--text-muted);
    line-height: 1.6;
    margin-bottom: 40px;
    max-width: 600px;
    margin-inline: auto;
}}

.cta-group {{
    display: flex;
    gap: 16px;
    justify-content: center;
}}

.btn {{
    padding: 14px 28px;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    border: none;
    font-family: inherit;
}}

.btn-primary {{
    background: var(--accent);
    color: #ffffff;
    box-shadow: 0 0 20px var(--accent-glow);
}}

.btn-primary:hover {{
    filter: brightness(1.1);
    box-shadow: 0 0 30px var(--accent-glow);
    transform: translateY(-2px);
}}

.btn-outline {{
    background: var(--surface);
    color: var(--text);
    border: 1px solid var(--border);
    backdrop-filter: blur(10px);
}}

.btn-outline:hover {{
    background: var(--border);
}}

/* Comparison Slider */
.comparison-container {{
    position: relative;
    width: 100%;
    max-width: 1040px;
    height: 60vw;
    max-height: 560px;
    min-height: 400px;
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid var(--border);
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.4), 0 0 0 1px rgba(255,255,255,0.05);
    --pos: 50%;
    background: var(--bg);
    animation: fadeUp 1s ease-out 0.2s forwards;
    opacity: 0;
}}

.view {{
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
}}

.view-after {{
    z-index: 1;
}}

.view-before {{
    z-index: 2;
    clip-path: polygon(0 0, var(--pos) 0, var(--pos) 100%, 0 100%);
}}

.view-label {{
    position: absolute;
    top: 24px;
    padding: 8px 16px;
    border-radius: 8px;
    background: rgba(0,0,0,0.6);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.1);
    color: #ffffff;
    font-size: 0.875rem;
    font-weight: 500;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    z-index: 3;
}}

.before-label {{ left: 24px; }}
.after-label {{ right: 24px; }}

.slider-input {{
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    opacity: 0;
    cursor: ew-resize;
    z-index: 10;
    margin: 0;
}}

.slider-handle {{
    position: absolute;
    top: 0;
    bottom: 0;
    left: var(--pos);
    width: 2px;
    background: var(--accent);
    transform: translateX(-50%);
    pointer-events: none;
    z-index: 5;
    box-shadow: 0 0 15px var(--accent-glow);
}}

.slider-thumb {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 48px;
    height: 48px;
    background: var(--bg);
    border: 2px solid var(--accent);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--accent);
    box-shadow: 0 0 20px var(--accent-glow);
    transition: transform 0.1s;
}}

.slider-input:active ~ .slider-handle .slider-thumb {{
    transform: translate(-50%, -50%) scale(1.1);
}}

/* Mock UI Layout */
.ui-grid {{
    width: 100%; height: 100%;
    padding: 4%;
    display: grid; gap: 3%;
    grid-template-columns: 220px 1fr;
    grid-template-rows: min-content 1fr;
}}

@media (max-width: 768px) {{
    .ui-grid {{ grid-template-columns: 80px 1fr; }}
    .ui-sidebar-item {{ height: 12px!important; }}
    .hifi-metric {{ font-size: 1.25rem!important; }}
}}

/* Wireframe (Before) Specifics */
.wf-ui {{ background: var(--bg); }}
.wf-box {{ border: 2px dashed var(--border); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: var(--border); font-family: monospace; font-size: 12px; }}
.wf-header {{ grid-column: 1 / 3; height: 60px; padding: 0 24px; justify-content: flex-start; }}
.wf-sidebar {{ display: flex; flex-direction: column; gap: 16px; padding: 24px; }}
.wf-sidebar-item {{ height: 20px; border: 2px dashed var(--border); border-radius: 6px; }}
.wf-main {{ display: grid; gap: 3%; grid-template-columns: 1fr 1fr; grid-template-rows: auto 1fr; }}
.wf-card {{ height: 120px; }}
.wf-chart {{ grid-column: 1 / 3; }}

/* Hi-Fi (After) Specifics */
.hifi-ui {{ background: linear-gradient(135deg, var(--bg) 0%, #080c16 100%); }}
.hifi-box {{ background: var(--card-bg); backdrop-filter: blur(16px); border: 1px solid var(--border); border-radius: 12px; position: relative; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }}
.hifi-header {{ grid-column: 1 / 3; height: 60px; display: flex; align-items: center; justify-content: space-between; padding: 0 24px; }}
.hifi-logo {{ width: 100px; height: 16px; background: var(--text); border-radius: 4px; opacity: 0.9; }}
.hifi-avatar {{ width: 32px; height: 32px; background: linear-gradient(135deg, var(--accent), #fff); border-radius: 50%; box-shadow: 0 0 10px var(--accent-glow);}}

.hifi-sidebar {{ display: flex; flex-direction: column; gap: 16px; padding: 24px; }}
.hifi-sidebar-item {{ height: 20px; background: var(--surface); border-radius: 6px; }}
.hifi-sidebar-item:first-child {{ background: var(--accent-light); border-left: 2px solid var(--accent); }}

.hifi-main {{ display: grid; gap: 3%; grid-template-columns: 1fr 1fr; grid-template-rows: auto 1fr; }}
.hifi-card {{ height: 120px; padding: 24px; display: flex; flex-direction: column; justify-content: center; }}
.hifi-card::before {{ content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 2px; background: linear-gradient(90deg, transparent, var(--accent), transparent); opacity: 0.5; }}
.hifi-metric {{ font-size: 2rem; font-weight: 700; color: var(--text); margin-bottom: 4px; }}
.hifi-label {{ font-size: 0.875rem; color: var(--text-muted); }}

.hifi-chart {{ grid-column: 1 / 3; padding: 32px; display: flex; align-items: flex-end; gap: 12px; }}
.hifi-bar {{ 
    flex: 1; background: linear-gradient(to top, var(--accent), transparent); 
    border-radius: 4px 4px 0 0; border-top: 2px solid var(--accent); opacity: 0.8;
    transform-origin: bottom;
    animation: grow 1.5s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
}}

@keyframes grow {{
    from {{ transform: scaleY(0.1); opacity: 0; }}
    to {{ transform: scaleY(1); opacity: 0.8; }}
}}

@keyframes fadeUp {{
    from {{ opacity: 0; transform: translateY(20px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="hero">
        <div class="hero-bg"></div>
        <div class="hero-glow"></div>
        
        <div class="hero-content">
            <div class="badge">
                <div class="badge-dot"></div>
                v2.0 Beta Live
            </div>
            <h1 class="title">{title_text}</h1>
            <p class="subtitle">{body_text}</p>
            <div class="cta-group">
                <button class="btn btn-primary">Join Beta</button>
                <button class="btn btn-outline">View Gallery</button>
            </div>
        </div>
        
        <div class="comparison-container">
            <!-- After View (Base layer) -->
            <div class="view view-after">
                <div class="ui-grid hifi-ui">
                    <div class="hifi-box hifi-header">
                        <div class="hifi-logo"></div>
                        <div class="hifi-avatar"></div>
                    </div>
                    <div class="hifi-box hifi-sidebar">
                        <div class="hifi-sidebar-item"></div>
                        <div class="hifi-sidebar-item"></div>
                        <div class="hifi-sidebar-item"></div>
                        <div class="hifi-sidebar-item"></div>
                    </div>
                    <div class="hifi-main">
                        <div class="hifi-box hifi-card">
                            <div class="hifi-metric">8,249</div>
                            <div class="hifi-label">Active Tokens</div>
                        </div>
                        <div class="hifi-box hifi-card">
                            <div class="hifi-metric">24ms</div>
                            <div class="hifi-label">Generation Speed</div>
                        </div>
                        <div class="hifi-box hifi-chart">
                            <div class="hifi-bar" style="height: 30%; animation-delay: 0.1s"></div>
                            <div class="hifi-bar" style="height: 50%; animation-delay: 0.2s"></div>
                            <div class="hifi-bar" style="height: 80%; animation-delay: 0.3s"></div>
                            <div class="hifi-bar" style="height: 40%; animation-delay: 0.4s"></div>
                            <div class="hifi-bar" style="height: 90%; animation-delay: 0.5s"></div>
                            <div class="hifi-bar" style="height: 60%; animation-delay: 0.6s"></div>
                            <div class="hifi-bar" style="height: 75%; animation-delay: 0.7s"></div>
                        </div>
                    </div>
                </div>
                <div class="view-label after-label">High-Fidelity</div>
            </div>
            
            <!-- Before View (Clipped layer) -->
            <div class="view view-before">
                <div class="ui-grid wf-ui">
                    <div class="wf-box wf-header">Navbar</div>
                    <div class="wf-box wf-sidebar">
                        <div class="wf-sidebar-item"></div>
                        <div class="wf-sidebar-item"></div>
                        <div class="wf-sidebar-item"></div>
                        <div class="wf-sidebar-item"></div>
                    </div>
                    <div class="wf-main">
                        <div class="wf-box wf-card">Metric Block</div>
                        <div class="wf-box wf-card">Metric Block</div>
                        <div class="wf-box wf-chart">Data Visualization</div>
                    </div>
                </div>
                <div class="view-label before-label">Wireframe</div>
            </div>
            
            <!-- Slider Control -->
            <input type="range" min="0" max="100" value="50" class="slider-input" aria-label="Compare wireframe to high-fidelity design">
            <div class="slider-handle">
                <div class="slider-thumb">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="m14 18-6-6 6-6"/>
                        <path d="m10 18 6-6-6-6"/>
                    </svg>
                </div>
            </div>
        </div>
    </main>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Glassmorphic Before/After Hero — interactive behavior
document.addEventListener('DOMContentLoaded', () => {
    const slider = document.querySelector('.slider-input');
    const container = document.querySelector('.comparison-container');
    
    // Update clip-path and handle position based on input range
    slider.addEventListener('input', (e) => {
        container.style.setProperty('--pos', `${e.target.value}%`);
    });
    
    // Optional: Add a slight parallax effect to the hero glow on mouse move
    const glow = document.querySelector('.hero-glow');
    document.addEventListener('mousemove', (e) => {
        const x = (e.clientX / window.innerWidth - 0.5) * 40;
        const y = (e.clientY / window.innerHeight - 0.5) * 40;
        glow.style.transform = `translate(calc(-50% + ${x}px), ${y}px)`;
    });
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
