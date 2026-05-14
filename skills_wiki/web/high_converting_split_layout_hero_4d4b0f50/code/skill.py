def create_component(
    output_dir: str,
    title_text: str = "It's your universe, it's time to save it",
    body_text: str = "The Rebel alliance is fighting to get rid of the evil empire. Join the resistance to create a better future for your children.",
    color_scheme: str = "dark",
    accent_color: str = "#e62429",
    width_px: int = 1440,
    height_px: int = 900,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the High-Converting Split-Layout Hero.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme logic
    if color_scheme == "dark":
        bg_color = "#0b0d12"
        text_color = "#ffffff"
        text_secondary = "#94a3b8"
        nav_text = "#e2e8f0"
        logo_filter = "brightness(0) invert(1) opacity(0.5)"
        logo_hover = "brightness(0) invert(1) opacity(1)"
        card_bg = "rgba(255, 255, 255, 0.05)"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        text_secondary = "#475569"
        nav_text = "#334155"
        logo_filter = "brightness(0) opacity(0.4)"
        logo_hover = "brightness(0) opacity(0.9)"
        card_bg = "rgba(0, 0, 0, 0.03)"

    css = f"""/* High-Converting Split-Layout Hero */
:root {{
    --bg-color: {bg_color};
    --text-primary: {text_color};
    --text-secondary: {text_secondary};
    --accent-color: {accent_color};
    --nav-text: {nav_text};
    --logo-filter: {logo_filter};
    --logo-hover: {logo_hover};
    --card-bg: {card_bg};
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-primary);
    min-height: 100vh;
    overflow-x: hidden;
    position: relative;
}}

/* Dynamic Background Stars (Only visible in dark mode, subtle in light) */
.starfield {{
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    z-index: -1;
    pointer-events: none;
    background: radial-gradient(circle at 80% 20%, rgba(255,255,255,0.05) 0%, transparent 40%);
}}

/* Layout Container */
.site-wrapper {{
    max-width: {width_px}px;
    min-height: {height_px}px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    padding: 0 4rem;
}}

/* Navigation */
.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2rem 0;
}}

.logo {{
    font-size: 1.5rem;
    font-weight: 800;
    letter-spacing: -1px;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}}

.logo-icon {{
    width: 32px;
    height: 32px;
    background: var(--accent-color);
    border-radius: 50%;
    position: relative;
    overflow: hidden;
}}

.logo-icon::after {{
    content: '';
    position: absolute;
    width: 16px;
    height: 16px;
    background: var(--bg-color);
    border-radius: 50%;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
}}

.nav-links {{
    display: flex;
    gap: 2.5rem;
    list-style: none;
}}

.nav-links a {{
    color: var(--nav-text);
    text-decoration: none;
    font-weight: 500;
    font-size: 0.95rem;
    transition: color 0.3s ease;
}}

.nav-links a:hover {{
    color: var(--text-primary);
}}

.nav-cta {{
    padding: 0.75rem 1.5rem;
    background: transparent;
    color: var(--text-primary);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 4px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
}}

.nav-cta:hover {{
    border-color: var(--text-primary);
}}

/* Hero Section */
.hero-main {{
    flex: 1;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4rem;
    align-items: center;
    padding: 4rem 0;
}}

.hero-text {{
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}}

.hero-text h1 {{
    font-size: clamp(3rem, 5vw, 4.5rem);
    line-height: 1.1;
    font-weight: 800;
    letter-spacing: -0.03em;
}}

.hero-text p {{
    font-size: 1.125rem;
    line-height: 1.6;
    color: var(--text-secondary);
    max-width: 90%;
}}

/* CTA & Social Proof */
.cta-group {{
    display: flex;
    align-items: center;
    gap: 2rem;
    margin-top: 1rem;
}}

.btn-primary {{
    background: var(--accent-color);
    color: #ffffff;
    border: none;
    padding: 1.25rem 2.5rem;
    font-size: 1.125rem;
    font-weight: 700;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 15px rgba(230, 36, 41, 0.2);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}

.btn-primary:hover {{
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(230, 36, 41, 0.4);
}}

/* Avatar Stack */
.social-proof {{
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-top: 1rem;
}}

.avatar-stack {{
    display: flex;
}}

.avatar {{
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: 3px solid var(--bg-color);
    background-color: var(--card-bg);
    background-size: cover;
    background-position: center;
    margin-left: -12px;
    position: relative;
    transition: transform 0.2s ease;
}}

.avatar:hover {{
    transform: translateY(-5px);
    z-index: 10;
}}

.avatar:first-child {{
    margin-left: 0;
}}

.social-text {{
    font-size: 0.875rem;
    color: var(--text-secondary);
}}

.social-text strong {{
    color: var(--text-primary);
}}

/* Hero Graphics */
.hero-visual {{
    position: relative;
    width: 100%;
    height: 600px;
    perspective: 1000px;
}}

.visual-element {{
    width: 100%;
    height: 100%;
    background-image: url('https://images.unsplash.com/photo-1614729939124-032f0b56c9ce?q=80&w=800&auto=format&fit=crop');
    background-size: contain;
    background-position: center;
    background-repeat: no-repeat;
    animation: float 6s ease-in-out infinite;
    transform-style: preserve-3d;
    filter: drop-shadow(0 20px 40px rgba(0,0,0,0.5));
}}

/* Trust Bar (As seen on) */
.trust-bar {{
    display: flex;
    align-items: center;
    gap: 3rem;
    padding: 3rem 0;
    border-top: 1px solid var(--card-bg);
    margin-top: auto;
}}

.trust-label {{
    font-size: 0.875rem;
    color: var(--text-secondary);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}

.trust-logos {{
    display: flex;
    gap: 3rem;
    align-items: center;
    flex-wrap: wrap;
}}

.trust-logo {{
    height: 24px;
    filter: var(--logo-filter);
    transition: filter 0.3s ease;
}}

.trust-logo:hover {{
    filter: var(--logo-hover);
}}

@keyframes float {{
    0% {{ transform: translateY(0px) rotateX(0) rotateY(0); }}
    50% {{ transform: translateY(-20px) rotateX(2deg) rotateY(-2deg); }}
    100% {{ transform: translateY(0px) rotateX(0) rotateY(0); }}
}}

/* Responsive */
@media (max-width: 1024px) {{
    .site-wrapper {{ padding: 0 2rem; }}
    .hero-main {{ gap: 2rem; }}
    .hero-text h1 {{ font-size: 3rem; }}
}}

@media (max-width: 768px) {{
    .hero-main {{ grid-template-columns: 1fr; text-align: center; }}
    .hero-text {{ align-items: center; }}
    .hero-text p {{ max-width: 100%; }}
    .cta-group {{ flex-direction: column; gap: 1.5rem; }}
    .nav-links {{ display: none; }}
    .trust-bar {{ flex-direction: column; gap: 1.5rem; justify-content: center; }}
    .hero-visual {{ height: 400px; }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="starfield" id="starfield"></div>
    
    <div class="site-wrapper">
        <header class="navbar">
            <div class="logo">
                <div class="logo-icon"></div>
                Rebel
            </div>
            <ul class="nav-links">
                <li><a href="#">Our Ships</a></li>
                <li><a href="#">Mission</a></li>
                <li><a href="#">Donations</a></li>
            </ul>
            <button class="nav-cta">Log In</button>
        </header>

        <main class="hero-main">
            <div class="hero-text">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
                
                <div class="cta-group">
                    <button class="btn-primary">Join Now For Free</button>
                </div>
                
                <div class="social-proof">
                    <div class="avatar-stack">
                        <div class="avatar" style="background-image: url('https://i.pravatar.cc/150?img=11'); z-index: 4;"></div>
                        <div class="avatar" style="background-image: url('https://i.pravatar.cc/150?img=12'); z-index: 3;"></div>
                        <div class="avatar" style="background-image: url('https://i.pravatar.cc/150?img=33'); z-index: 2;"></div>
                        <div class="avatar" style="background-image: url('https://i.pravatar.cc/150?img=14'); z-index: 1;"></div>
                    </div>
                    <div class="social-text">
                        <strong>Obi Wan</strong> and 4,000 others have already joined
                    </div>
                </div>
            </div>

            <div class="hero-visual">
                <div class="visual-element" id="hero-graphic"></div>
            </div>
        </main>

        <footer class="trust-bar">
            <span class="trust-label">As seen on</span>
            <div class="trust-logos">
                <!-- Using generic SVG placeholders that look like media logos -->
                <img src="https://upload.wikimedia.org/wikipedia/commons/b/b1/CNN.svg" alt="CNN" class="trust-logo">
                <img src="https://upload.wikimedia.org/wikipedia/commons/a/a2/BBC_News_2022_%28Alt%2C_stacked%29.svg" alt="BBC" class="trust-logo">
                <img src="https://upload.wikimedia.org/wikipedia/commons/2/2f/Fox_News_Channel_logo.svg" alt="Fox" class="trust-logo">
                <img src="https://upload.wikimedia.org/wikipedia/commons/8/80/Vice_logo.svg" alt="Vice" class="trust-logo">
            </div>
        </footer>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// High-Converting Split-Layout Hero - Interactive Behavior

document.addEventListener('DOMContentLoaded', () => {{
    // 1. Generate CSS Starfield dynamically for the background
    const starfield = document.getElementById('starfield');
    if (starfield && '{color_scheme}' === 'dark') {{
        let stars = '';
        // Generate 150 random stars
        for (let i = 0; i < 150; i++) {{
            const x = Math.floor(Math.random() * 100);
            const y = Math.floor(Math.random() * 100);
            const size = Math.random() * 2;
            const opacity = Math.random() * 0.8 + 0.2;
            stars += `${{x}}vw ${{y}}vh 0 ${{size}}px rgba(255, 255, 255, ${{opacity}}),`;
        }}
        // Remove trailing comma
        stars = stars.slice(0, -1);
        
        // Apply as box-shadow to a pseudo element
        const style = document.createElement('style');
        style.textContent = `
            .starfield::before {{
                content: '';
                position: absolute;
                top: 0; left: 0;
                width: 1px; height: 1px;
                background: transparent;
                box-shadow: ${{stars}};
            }}
        `;
        document.head.appendChild(style);
    }}

    // 2. 3D Mouse Parallax Effect on Hero Graphic
    const heroVisualContainer = document.querySelector('.hero-visual');
    const heroGraphic = document.getElementById('hero-graphic');

    if (heroVisualContainer && heroGraphic) {{
        heroVisualContainer.addEventListener('mousemove', (e) => {{
            const rect = heroVisualContainer.getBoundingClientRect();
            
            // Calculate mouse position relative to the center of the container (-1 to 1)
            const x = (e.clientX - rect.left - rect.width / 2) / (rect.width / 2);
            const y = (e.clientY - rect.top - rect.height / 2) / (rect.height / 2);
            
            // Apply rotation (max 15 degrees)
            const rotateX = y * -15;
            const rotateY = x * 15;
            
            // Temporarily pause the float animation to apply the precise mouse transform
            heroGraphic.style.animationPlayState = 'paused';
            heroGraphic.style.transform = `translateY(0) rotateX(${{rotateX}}deg) rotateY(${{rotateY}}deg) scale3d(1.05, 1.05, 1.05)`;
        }});

        // Reset when mouse leaves
        heroVisualContainer.addEventListener('mouseleave', () => {{
            heroGraphic.style.transform = '';
            heroGraphic.style.animationPlayState = 'running';
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
