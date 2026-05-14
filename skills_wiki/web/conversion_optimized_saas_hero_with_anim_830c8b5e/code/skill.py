def create_component(
    output_dir: str,
    title_text: str = "Power your end-to-end sales process",
    body_text: str = "Automate routine tasks with the power of generative AI. Connect the right people, find anything you need, and automate the rest.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#6366f1",     # CSS hex color for accent (e.g. Indigo)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Conversion-Optimized SaaS Hero.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#0b0f19"
        text_color = "#f8fafc"
        text_muted = "#94a3b8"
        surface_color = "#1e293b"
        surface_border = "#334155"
        logo_color = "#64748b"
        demo_bg = "#0f172a"
        skeleton_base = "#334155"
        skeleton_highlight = "#475569"
    else:
        bg_color = "#ffffff"
        text_color = "#0f172a"
        text_muted = "#475569"
        surface_color = "#f8fafc"
        surface_border = "#e2e8f0"
        logo_color = "#94a3b8"
        demo_bg = "#ffffff"
        skeleton_base = "#e2e8f0"
        skeleton_highlight = "#f1f5f9"

    # === CSS ===
    css = f"""/* SaaS Hero Component */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;800&display=swap');

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
    --surface-border: {surface_border};
    --logo-color: {logo_color};
    --demo-bg: {demo_bg};
    --skeleton-base: {skeleton_base};
    --skeleton-highlight: {skeleton_highlight};
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
    line-height: 1.5;
}}

.hero-wrapper {{
    width: 100%;
    max-width: var(--width);
    min-height: var(--height);
    padding: 4rem 2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 4rem;
    flex-wrap: wrap;
}}

/* Left Column: Content */
.hero-content {{
    flex: 1;
    min-width: 340px;
    max-width: 540px;
    display: flex;
    flex-direction: column;
    gap: 2rem;
}}

.hero-title {{
    font-size: clamp(2.5rem, 5vw, 3.5rem);
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -0.03em;
}}

.hero-body {{
    font-size: 1.125rem;
    color: var(--text-muted);
    line-height: 1.6;
}}

.hero-cta-group {{
    display: flex;
    align-items: center;
    gap: 1rem;
    flex-wrap: wrap;
}}

.btn-primary {{
    background-color: var(--accent);
    color: #ffffff;
    border: none;
    padding: 1rem 2rem;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    text-decoration: none;
    box-shadow: 0 4px 14px 0 rgba(0, 0, 0, 0.1);
    position: relative;
    overflow: hidden;
}}

.btn-primary:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
    filter: brightness(1.1);
}}

.btn-secondary {{
    background-color: transparent;
    color: var(--text);
    border: 1px solid var(--surface-border);
    padding: 1rem 2rem;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
}}

.btn-secondary:hover {{
    background-color: var(--surface);
}}

/* Social Proof */
.social-proof {{
    margin-top: 1rem;
    padding-top: 2rem;
    border-top: 1px solid var(--surface-border);
}}

.social-proof p {{
    font-size: 0.875rem;
    color: var(--text-muted);
    font-weight: 500;
    margin-bottom: 1rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}

.social-logos {{
    display: flex;
    gap: 2rem;
    align-items: center;
    flex-wrap: wrap;
}}

.social-logos i {{
    font-size: 1.75rem;
    color: var(--logo-color);
    transition: color 0.3s ease;
}}

.social-logos i:hover {{
    color: var(--text);
}}

/* Right Column: Animated Demo */
.hero-visual {{
    flex: 1;
    min-width: 340px;
    position: relative;
    perspective: 1000px;
}}

.mock-window {{
    background: var(--demo-bg);
    border: 1px solid var(--surface-border);
    border-radius: 12px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    overflow: hidden;
    transform: rotateY(-5deg) rotateX(5deg);
    animation: float 6s ease-in-out infinite;
}}

.mock-header {{
    height: 40px;
    background: var(--surface);
    border-bottom: 1px solid var(--surface-border);
    display: flex;
    align-items: center;
    padding: 0 1rem;
    gap: 0.5rem;
}}

.dot {{
    width: 10px;
    height: 10px;
    border-radius: 50%;
}}
.dot.red {{ background: #ef4444; }}
.dot.yellow {{ background: #eab308; }}
.dot.green {{ background: #22c55e; }}

.mock-body {{
    padding: 2rem;
    min-height: 300px;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}}

/* AI / Software Animation Elements */
.mock-search {{
    height: 40px;
    width: 100%;
    background: var(--surface);
    border: 1px solid var(--surface-border);
    border-radius: 6px;
    display: flex;
    align-items: center;
    padding: 0 1rem;
}}

.mock-cursor-line {{
    height: 20px;
    width: 2px;
    background: var(--accent);
    animation: blink 1s infinite;
}}

.mock-typing {{
    display: inline-block;
    overflow: hidden;
    white-space: nowrap;
    border-right: 2px solid transparent;
    animation: typing 4s steps(30, end) infinite;
    color: var(--text);
    font-size: 0.875rem;
    font-weight: 500;
}}

.mock-results {{
    display: flex;
    flex-direction: column;
    gap: 1rem;
}}

.mock-result-card {{
    background: var(--surface);
    border: 1px solid var(--surface-border);
    padding: 1rem;
    border-radius: 6px;
    opacity: 0;
    transform: translateY(10px);
    animation: fadeUp 4s ease-out infinite;
}}

.mock-result-card:nth-child(2) {{
    animation-delay: 0.5s;
}}

.mock-result-card:nth-child(3) {{
    animation-delay: 1s;
}}

.skeleton-line {{
    height: 12px;
    background: var(--skeleton-base);
    border-radius: 4px;
    margin-bottom: 0.75rem;
    position: relative;
    overflow: hidden;
}}

.skeleton-line::after {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(90deg, transparent, var(--skeleton-highlight), transparent);
    animation: shimmer 2s infinite;
    transform: translateX(-100%);
}}

.skeleton-line.short {{ width: 60%; }}
.skeleton-line.badge {{ width: 20%; height: 20px; border-radius: 10px; background: var(--accent); opacity: 0.8; margin-top: 1rem; margin-bottom: 0; }}

/* Keyframes */
@keyframes float {{
    0%, 100% {{ transform: rotateY(-5deg) rotateX(5deg) translateY(0); }}
    50% {{ transform: rotateY(-5deg) rotateX(5deg) translateY(-15px); }}
}}

@keyframes blink {{
    0%, 100% {{ opacity: 1; }}
    50% {{ opacity: 0; }}
}}

@keyframes typing {{
    0%, 20% {{ width: 0; }}
    40%, 80% {{ width: 100%; border-right-color: var(--accent); }}
    90%, 100% {{ width: 100%; border-right-color: transparent; opacity: 0; }}
}}

@keyframes fadeUp {{
    0%, 40% {{ opacity: 0; transform: translateY(10px); }}
    50%, 90% {{ opacity: 1; transform: translateY(0); }}
    100% {{ opacity: 0; transform: translateY(-10px); }}
}}

@keyframes shimmer {{
    100% {{ transform: translateX(100%); }}
}}

@media (max-width: 900px) {{
    .hero-wrapper {{ flex-direction: column; justify-content: center; text-align: center; }}
    .hero-content {{ align-items: center; max-width: 100%; }}
    .hero-cta-group {{ justify-content: center; }}
    .social-logos {{ justify-content: center; }}
    .mock-window {{ transform: none; animation: floatMobile 6s ease-in-out infinite; margin-top: 2rem; }}
    
    @keyframes floatMobile {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-15px); }}
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
    
    <!-- Font Awesome for Social Proof Logos -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/brands.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/fontawesome.min.css">
    
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="hero-wrapper">
        
        <!-- Left Content Section -->
        <div class="hero-content">
            <h1 class="hero-title">{title_text}</h1>
            <p class="hero-body">{body_text}</p>
            
            <div class="hero-cta-group">
                <a href="#" class="btn-primary" id="main-cta">Start for free today</a>
                <a href="#" class="btn-secondary">Request a demo</a>
            </div>
            
            <div class="social-proof">
                <p>Trusted by innovative teams worldwide</p>
                <div class="social-logos">
                    <i class="fa-brands fa-stripe"></i>
                    <i class="fa-brands fa-aws"></i>
                    <i class="fa-brands fa-slack"></i>
                    <i class="fa-brands fa-google"></i>
                    <i class="fa-brands fa-figma"></i>
                </div>
            </div>
        </div>
        
        <!-- Right Visual / Animated Demo Section -->
        <div class="hero-visual">
            <div class="mock-window">
                <div class="mock-header">
                    <div class="dot red"></div>
                    <div class="dot yellow"></div>
                    <div class="dot green"></div>
                </div>
                <div class="mock-body">
                    <!-- Simulating a user prompt or AI command -->
                    <div class="mock-search">
                        <div class="mock-typing">Generate an automated outreach workflow...</div>
                        <div class="mock-cursor-line"></div>
                    </div>
                    
                    <!-- Simulating software producing results -->
                    <div class="mock-results">
                        <div class="mock-result-card">
                            <div class="skeleton-line"></div>
                            <div class="skeleton-line short"></div>
                            <div class="skeleton-line badge"></div>
                        </div>
                        <div class="mock-result-card">
                            <div class="skeleton-line"></div>
                            <div class="skeleton-line short"></div>
                            <div class="skeleton-line badge"></div>
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
    js = f"""// Button Ripple / Click Micro-interaction
document.addEventListener('DOMContentLoaded', () => {{
    const btn = document.getElementById('main-cta');
    
    btn.addEventListener('click', function(e) {{
        e.preventDefault();
        
        // Visual feedback on click
        this.style.transform = 'scale(0.95)';
        
        // Add a temporary text change to simulate action
        const originalText = this.innerText;
        this.innerText = 'Setting up workspace...';
        
        setTimeout(() => {{
            this.style.transform = 'translateY(-2px)';
            this.innerText = originalText;
        }}, 600);
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
