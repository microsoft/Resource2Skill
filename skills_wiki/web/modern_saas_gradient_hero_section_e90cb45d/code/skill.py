def create_component(
    output_dir: str,
    title_text: str = "Built For Fast, Aligned",
    highlight_text: str = "Growth",
    body_text: str = "Acurio helps B2B teams streamline operations, collaborate, and scale with confidence.",
    badge_text: str = "Trusted by 1000s of growing B2B teams",
    color_scheme: str = "light",       # "dark" or "light"
    accent_color_1: str = "#3562F1",   # Start of gradient (Blue)
    accent_color_2: str = "#D946EF",   # End of gradient (Magenta)
    width_px: int = 1440,
    height_px: int = 900,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Modern SaaS Gradient Hero Section.
    """
    import os
    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0A0A0A"
        text_primary = "#FFFFFF"
        text_secondary = "#A1A1AA"
        border_color = "#27272A"
        surface_bg = "#18181B"
        grid_color = "rgba(255,255,255,0.03)"
        shadow_color = "rgba(0,0,0,0.5)"
    else:
        bg_color = "#FFFFFF"
        text_primary = "#1D1F20"
        text_secondary = "#6B7280"
        border_color = "#E5E7EB"
        surface_bg = "#FFFFFF"
        grid_color = "rgba(0,0,0,0.03)"
        shadow_color = "rgba(0,0,0,0.08)"

    # === CSS ===
    css = f"""/* Modern SaaS Gradient Hero Section */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {{
    --bg-color: {bg_color};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --border-color: {border_color};
    --surface-bg: {surface_bg};
    --shadow-color: {shadow_color};
    --accent-1: {accent_color_1};
    --accent-2: {accent_color_2};
    --grid-color: {grid_color};
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    overflow-x: hidden;
    position: relative;
}}

/* Diagonal Background Pattern */
body::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: repeating-linear-gradient(
        45deg,
        var(--grid-color) 0,
        var(--grid-color) 1px,
        transparent 1px,
        transparent 40px
    );
    z-index: -1;
    pointer-events: none;
    mask-image: linear-gradient(to bottom, black 20%, transparent 100%);
    -webkit-mask-image: linear-gradient(to bottom, black 20%, transparent 100%);
}}

.hero-container {{
    width: 100%;
    max-width: {width_px}px;
    min-height: {height_px}px;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 2rem 1.5rem;
}}

/* Navigation */
.navbar {{
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 0;
    animation: fadeDown 0.8s ease-out;
}}

.nav-brand {{
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

.nav-brand svg {{
    width: 28px;
    height: 28px;
    fill: url(#brand-grad);
}}

.nav-links {{
    display: flex;
    gap: 2rem;
}}

.nav-links a {{
    text-decoration: none;
    color: var(--text-secondary);
    font-weight: 500;
    font-size: 0.95rem;
    transition: color 0.2s;
}}

.nav-links a:hover {{
    color: var(--text-primary);
}}

.nav-actions {{
    display: flex;
    gap: 1rem;
    align-items: center;
}}

/* Hero Content */
.hero-content {{
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    margin-top: 6rem;
    max-width: 800px;
    z-index: 10;
}}

/* Badge */
.badge {{
    display: inline-flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.25rem 0.75rem 0.25rem 0.25rem;
    background: var(--surface-bg);
    border: 1px solid var(--border-color);
    border-radius: 999px;
    font-size: 0.875rem;
    font-weight: 500;
    margin-bottom: 2rem;
    animation: fadeUp 0.8s ease-out 0.2s both;
}}

.badge-pill {{
    background: linear-gradient(135deg, var(--accent-1), var(--accent-2));
    color: white;
    padding: 0.2rem 0.6rem;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}

/* Typography */
.hero-title {{
    font-size: clamp(3rem, 5vw, 4.5rem);
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -0.03em;
    margin-bottom: 1.5rem;
    animation: fadeUp 0.8s ease-out 0.3s both;
}}

.text-gradient {{
    background: linear-gradient(135deg, var(--accent-1), var(--accent-2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    color: transparent;
}}

.hero-subtitle {{
    font-size: 1.125rem;
    color: var(--text-secondary);
    line-height: 1.6;
    max-width: 600px;
    margin-bottom: 2.5rem;
    animation: fadeUp 0.8s ease-out 0.4s both;
}}

/* Buttons */
.cta-group {{
    display: flex;
    gap: 1rem;
    animation: fadeUp 0.8s ease-out 0.5s both;
}}

.btn {{
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    font-weight: 500;
    font-size: 1rem;
    text-decoration: none;
    transition: all 0.2s ease;
    cursor: pointer;
    border: none;
    display: inline-flex;
    align-items: center;
    justify-content: center;
}}

.btn-primary {{
    background: linear-gradient(135deg, var(--accent-1), var(--accent-2));
    color: white;
    box-shadow: 0 4px 14px var(--shadow-color);
}}

.btn-primary:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px var(--shadow-color);
}}

.btn-outline {{
    background: transparent;
    color: var(--text-primary);
    border: 1px solid var(--border-color);
}}

.btn-outline:hover {{
    background: var(--border-color);
}}

.btn-nav {{
    background: transparent;
    color: var(--text-primary);
    padding: 0.5rem 1rem;
}}
.btn-nav:hover {{
    background: var(--border-color);
}}

/* Mockup UI */
.mockup-wrapper {{
    margin-top: 4rem;
    width: 100%;
    max-width: 1000px;
    perspective: 1000px;
    animation: fadeUp 1s ease-out 0.7s both;
}}

.mockup-window {{
    width: 100%;
    height: 500px;
    background: var(--surface-bg);
    border-radius: 12px;
    border: 1px solid var(--border-color);
    box-shadow: 0 25px 50px -12px var(--shadow-color);
    display: flex;
    flex-direction: column;
    overflow: hidden;
}}

.mockup-header {{
    height: 48px;
    border-bottom: 1px solid var(--border-color);
    display: flex;
    align-items: center;
    padding: 0 1.5rem;
    gap: 0.5rem;
}}

.dot {{
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: var(--border-color);
}}

.mockup-body {{
    flex: 1;
    display: flex;
    padding: 2rem;
    gap: 2rem;
    position: relative;
}}

.mockup-sidebar {{
    width: 200px;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}}

.skeleton-line {{
    height: 12px;
    border-radius: 4px;
    background: var(--border-color);
    opacity: 0.5;
}}

.mockup-main {{
    flex: 1;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    grid-template-rows: auto 1fr;
    gap: 1.5rem;
}}

.skeleton-card {{
    background: var(--bg-color);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}}

.chart-area {{
    grid-column: span 2;
    background: var(--bg-color);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    position: relative;
    overflow: hidden;
}}

/* Center Play Button Overlay */
.play-overlay {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 64px;
    height: 64px;
    background: linear-gradient(135deg, var(--accent-1), var(--accent-2));
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 10px 25px var(--shadow-color);
    cursor: pointer;
    transition: transform 0.2s ease;
}}

.play-overlay:hover {{
    transform: translate(-50%, -50%) scale(1.1);
}}

.play-overlay svg {{
    width: 24px;
    height: 24px;
    fill: white;
    margin-left: 4px;
}}

/* Animations */
@keyframes fadeUp {{
    from {{ opacity: 0; transform: translateY(20px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

@keyframes fadeDown {{
    from {{ opacity: 0; transform: translateY(-20px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

/* Responsive */
@media (max-width: 768px) {{
    .nav-links {{ display: none; }}
    .hero-title {{ font-size: 2.5rem; }}
    .mockup-sidebar {{ display: none; }}
    .mockup-main {{ grid-template-columns: 1fr; }}
    .chart-area {{ grid-column: span 1; }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text} {highlight_text}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    
    <svg width="0" height="0" class="hidden">
      <defs>
        <linearGradient id="brand-grad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="{accent_color_1}" />
          <stop offset="100%" stop-color="{accent_color_2}" />
        </linearGradient>
      </defs>
    </svg>

    <div class="hero-container">
        
        <nav class="navbar">
            <div class="nav-brand">
                <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 2L2 12l10 10 10-10L12 2zm0 4.5l5.5 5.5-5.5 5.5L6.5 12 12 6.5z"/>
                </svg>
                acurio
            </div>
            <div class="nav-links">
                <a href="#">Features</a>
                <a href="#">Pricing</a>
                <a href="#">Use Cases</a>
                <a href="#">Resources</a>
                <a href="#">Contact</a>
            </div>
            <div class="nav-actions">
                <a href="#" class="btn btn-nav">Login</a>
                <a href="#" class="btn btn-primary">Get Started</a>
            </div>
        </nav>

        <main class="hero-content">
            
            <div class="badge">
                <span class="badge-pill">New</span>
                <span>{badge_text}</span>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="9 18 15 12 9 6"></polyline>
                </svg>
            </div>

            <h1 class="hero-title">
                {title_text} <br/> <span class="text-gradient">{highlight_text}</span>
            </h1>

            <p class="hero-subtitle">
                {body_text}
            </p>

            <div class="cta-group">
                <a href="#" class="btn btn-primary">Start for free</a>
                <a href="#" class="btn btn-outline">Book a Demo</a>
            </div>
        </main>

        <!-- CSS Representation of the Dashboard Image to ensure standalone reproducibility -->
        <div class="mockup-wrapper">
            <div class="mockup-window">
                <div class="mockup-header">
                    <div class="dot" style="background: #ef4444"></div>
                    <div class="dot" style="background: #f59e0b"></div>
                    <div class="dot" style="background: #10b981"></div>
                </div>
                <div class="mockup-body">
                    <div class="mockup-sidebar">
                        <div class="skeleton-line" style="width: 80%; margin-bottom: 2rem;"></div>
                        <div class="skeleton-line" style="width: 60%;"></div>
                        <div class="skeleton-line" style="width: 75%;"></div>
                        <div class="skeleton-line" style="width: 50%;"></div>
                        <div class="skeleton-line" style="width: 65%;"></div>
                    </div>
                    <div class="mockup-main">
                        <div class="skeleton-card">
                            <div class="skeleton-line" style="width: 40%;"></div>
                            <div class="skeleton-line" style="width: 90%; height: 24px;"></div>
                        </div>
                        <div class="skeleton-card">
                            <div class="skeleton-line" style="width: 50%;"></div>
                            <div class="skeleton-line" style="width: 70%; height: 24px;"></div>
                        </div>
                        <div class="chart-area">
                            <div class="play-overlay">
                                <svg viewBox="0 0 24 24">
                                    <path d="M5 3l14 9-14 9V3z"/>
                                </svg>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Interactivity logic for Mockup Play Button
document.addEventListener('DOMContentLoaded', () => {
    const playBtn = document.querySelector('.play-overlay');
    
    if(playBtn) {
        playBtn.addEventListener('click', () => {
            playBtn.style.transform = 'translate(-50%, -50%) scale(0.9)';
            setTimeout(() => {
                playBtn.style.transform = 'translate(-50%, -50%) scale(1)';
                // Normally this would trigger a video modal
            }, 150);
        });
    }
});
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
