def create_component(
    output_dir: str,
    title_text: str = "It's your universe, it's time to save it",
    body_text: str = "The alliance is fighting to get rid of the empire. Join the resistance to create a better future for your children.",
    color_scheme: str = "dark",
    accent_color: str = "#d90429",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Authority-Driven Split Hero layout.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#0b0d17"
        text_primary = "#ffffff"
        text_secondary = "#9cb3c9"
        border_color = "rgba(255, 255, 255, 0.15)"
        sphere_color = "radial-gradient(circle at 30% 30%, #2a2d3e, #0b0d17)"
    else:
        bg_color = "#f8f9fa"
        text_primary = "#111424"
        text_secondary = "#4a5568"
        border_color = "rgba(0, 0, 0, 0.1)"
        sphere_color = "radial-gradient(circle at 30% 30%, #e2e8f0, #cbd5e0)"

    css = f"""/* Authority-Driven Split Hero */
:root {{
    --bg: {bg_color};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --accent: {accent_color};
    --border: {border_color};
    --sphere: {sphere_color};
    
    --width: {width_px}px;
    --height: {height_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: var(--bg);
    color: var(--text-primary);
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    /* Subtle starry atmosphere */
    background-image: 
        radial-gradient(2px 2px at 20px 30px, rgba(255,255,255,0.2), rgba(0,0,0,0)),
        radial-gradient(2px 2px at 40px 70px, rgba(255,255,255,0.2), rgba(0,0,0,0)),
        radial-gradient(2px 2px at 90px 40px, rgba(255,255,255,0.2), rgba(0,0,0,0));
    background-repeat: repeat;
    background-size: 200px 200px;
}}

.hero-wrapper {{
    width: 100%;
    max-width: var(--width);
    min-height: var(--height);
    display: flex;
    flex-direction: column;
    padding: 2rem 4rem;
    position: relative;
    overflow: hidden;
}}

/* === HEADER === */
header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 10;
}}

.logo {{
    font-weight: 800;
    font-size: 1.25rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

.logo-icon {{
    width: 24px;
    height: 24px;
    background: var(--accent);
    border-radius: 4px;
    transform: rotate(45deg);
}}

nav {{
    display: flex;
    gap: 2rem;
}}

nav a {{
    color: var(--text-primary);
    text-decoration: none;
    font-size: 0.9rem;
    font-weight: 500;
    transition: opacity 0.2s;
}}

nav a:hover {{
    opacity: 0.7;
}}

.btn {{
    padding: 0.75rem 1.5rem;
    border-radius: 4px;
    font-weight: 600;
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.3s ease;
    text-decoration: none;
    display: inline-block;
}}

.btn-ghost {{
    background: transparent;
    border: 2px solid var(--accent);
    color: var(--accent);
}}

.btn-ghost:hover {{
    background: var(--accent);
    color: #fff;
}}

.btn-solid {{
    background: var(--accent);
    color: #fff;
    border: 2px solid var(--accent);
    box-shadow: 0 4px 14px rgba(0,0,0,0.25);
}}

.btn-solid:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.4);
}}

/* === MAIN HERO CONTENT === */
main {{
    flex: 1;
    display: flex;
    align-items: center;
    gap: 4rem;
    margin-top: 2rem;
    z-index: 10;
}}

.hero-text {{
    flex: 1;
    max-width: 550px;
}}

.hero-text h1 {{
    font-size: 3.5rem;
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -0.03em;
    margin-bottom: 1.5rem;
}}

.hero-text p {{
    font-size: 1.1rem;
    line-height: 1.6;
    color: var(--text-secondary);
    margin-bottom: 2.5rem;
    max-width: 90%;
}}

.cta-group {{
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}}

.social-proof {{
    display: flex;
    align-items: center;
    gap: 1rem;
}}

.avatars {{
    display: flex;
}}

.avatar {{
    width: 36px;
    height: 36px;
    border-radius: 50%;
    border: 3px solid var(--bg);
    margin-left: -12px;
    background-color: var(--border);
    background-size: cover;
}}

.avatar:first-child {{ margin-left: 0; background-image: url('https://i.pravatar.cc/100?img=11'); }}
.avatar:nth-child(2) {{ background-image: url('https://i.pravatar.cc/100?img=12'); }}
.avatar:nth-child(3) {{ background-image: url('https://i.pravatar.cc/100?img=13'); }}
.avatar:nth-child(4) {{ background-image: url('https://i.pravatar.cc/100?img=14'); }}

.social-proof p {{
    font-size: 0.85rem;
    margin-bottom: 0;
    color: var(--text-secondary);
    font-weight: 500;
}}

.social-proof strong {{
    color: var(--text-primary);
}}

/* === HERO VISUAL COMPOSITION === */
.hero-visual {{
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    height: 100%;
}}

/* Background object representing the setting (e.g., Death Star) */
.visual-bg-sphere {{
    position: absolute;
    width: 350px;
    height: 350px;
    background: var(--sphere);
    border-radius: 50%;
    right: 0;
    box-shadow: inset -20px -20px 40px rgba(0,0,0,0.5), 0 0 60px rgba(255,255,255,0.03);
}}

/* Foreground object representing action (e.g., Spaceship) */
.visual-fg-shape {{
    position: absolute;
    width: 280px;
    height: 120px;
    background: linear-gradient(135deg, var(--accent), #ff8fa3);
    /* Creates a sharp, aerodynamic shape */
    clip-path: polygon(0% 40%, 60% 30%, 75% 0%, 100% 50%, 75% 100%, 60% 70%, 0% 60%);
    left: 10%;
    top: 50%;
    margin-top: -60px;
    filter: drop-shadow(0 30px 40px rgba(0,0,0,0.6));
    animation: float 6s ease-in-out infinite;
    z-index: 2;
}}

.visual-fg-shape::after {{
    content: '';
    position: absolute;
    right: 0;
    top: 40%;
    width: 40px;
    height: 20%;
    background: #fff;
    filter: blur(8px);
}}

@keyframes float {{
    0%, 100% {{ transform: translateY(0) rotate(-5deg); }}
    50% {{ transform: translateY(-25px) rotate(2deg); }}
}}

/* === TRUST BADGES FOOTER === */
footer {{
    margin-top: 4rem;
    padding-top: 2rem;
    border-top: 1px solid var(--border);
    display: flex;
    align-items: center;
    gap: 3rem;
    z-index: 10;
}}

.footer-label {{
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-secondary);
    font-weight: 600;
}}

.logos {{
    display: flex;
    gap: 3rem;
    align-items: center;
}}

.logo-placeholder {{
    font-weight: 800;
    font-size: 1.5rem;
    color: var(--text-primary);
    opacity: 0.3;
    letter-spacing: -0.05em;
    transition: opacity 0.3s;
}}

.logo-placeholder:hover {{
    opacity: 0.7;
}}

/* Responsive */
@media (max-width: 900px) {{
    main {{
        flex-direction: column;
        text-align: center;
    }}
    .hero-text p {{
        margin: 0 auto 2.5rem auto;
    }}
    .cta-group {{
        align-items: center;
    }}
    .hero-visual {{
        width: 100%;
        min-height: 300px;
    }}
    .visual-fg-shape {{
        left: 50%;
        transform: translateX(-50%) rotate(-5deg);
    }}
    @keyframes float {{
        0%, 100% {{ transform: translate(-50%, 0) rotate(-5deg); }}
        50% {{ transform: translate(-50%, -20px) rotate(2deg); }}
    }}
    footer {{
        flex-direction: column;
        gap: 1.5rem;
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hero Section - {title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <div class="hero-wrapper">
        <header>
            <div class="logo">
                <div class="logo-icon"></div>
                Alliance
            </div>
            <nav>
                <a href="#">Our Ships</a>
                <a href="#">Mission</a>
                <a href="#">Donations</a>
            </nav>
            <a href="#" class="btn btn-ghost">JOIN NOW</a>
        </header>

        <main>
            <div class="hero-text">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
                
                <div class="cta-group">
                    <div>
                        <a href="#" class="btn btn-solid">JOIN NOW FOR FREE</a>
                    </div>
                    
                    <div class="social-proof">
                        <div class="avatars">
                            <div class="avatar"></div>
                            <div class="avatar"></div>
                            <div class="avatar"></div>
                            <div class="avatar"></div>
                        </div>
                        <p><strong>Obi Wan</strong> and 4,000 others have joined</p>
                    </div>
                </div>
            </div>

            <div class="hero-visual">
                <div class="visual-bg-sphere"></div>
                <div class="visual-fg-shape"></div>
            </div>
        </main>

        <footer>
            <div class="footer-label">As seen on</div>
            <div class="logos">
                <div class="logo-placeholder">NBC</div>
                <div class="logo-placeholder">FOX</div>
                <div class="logo-placeholder">THE CW</div>
                <div class="logo-placeholder" style="font-family: serif; font-style: italic;">Forbes</div>
            </div>
        </footer>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    js = """// Interaction Logic for Authority-Driven Split Hero
document.addEventListener('DOMContentLoaded', () => {
    // Optional: Add subtle mouse-move parallax to the hero visual for premium feel
    const visualWrapper = document.querySelector('.hero-visual');
    const fgShape = document.querySelector('.visual-fg-shape');
    const bgSphere = document.querySelector('.visual-bg-sphere');

    if(visualWrapper && fgShape && bgSphere) {
        document.addEventListener('mousemove', (e) => {
            const xAxis = (window.innerWidth / 2 - e.pageX) / 50;
            const yAxis = (window.innerHeight / 2 - e.pageY) / 50;
            
            fgShape.style.transform = `translate(${xAxis * 1.5}px, ${yAxis * 1.5}px)`;
            bgSphere.style.transform = `translate(${xAxis * 0.5}px, ${yAxis * 0.5}px)`;
        });
        
        // Reset transform on mouse leave to prevent conflicts with keyframe animation
        document.addEventListener('mouseleave', () => {
            fgShape.style.transform = '';
            bgSphere.style.transform = '';
        });
    }
});
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
