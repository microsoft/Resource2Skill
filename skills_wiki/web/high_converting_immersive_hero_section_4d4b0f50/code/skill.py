def create_component(
    output_dir: str,
    title_text: str = "It's your universe, it's time to save it",
    body_text: str = "The Alliance is fighting to get rid of the evil empire. Join the resistance to create a better future for your children.",
    color_scheme: str = "dark",
    accent_color: str = "#e62429",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the High-Converting Immersive Hero Section.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors (Tutorial relies heavily on dark theme, but we accommodate both)
    if color_scheme == "dark":
        bg_color = "#0b0e14"
        text_primary = "#ffffff"
        text_secondary = "#a0aec0"
        border_color = "rgba(255, 255, 255, 0.1)"
        nav_bg = "rgba(11, 14, 20, 0.8)"
        bg_image = "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?q=80&w=2048&auto=format&fit=crop" # Space
        hero_object = "https://images.unsplash.com/photo-1541185933-ef5d8ed016c2?q=80&w=1000&auto=format&fit=crop" # Sci-fi looking element
    else:
        bg_color = "#f7fafc"
        text_primary = "#1a202c"
        text_secondary = "#4a5568"
        border_color = "rgba(0, 0, 0, 0.1)"
        nav_bg = "rgba(247, 250, 252, 0.8)"
        bg_image = "https://images.unsplash.com/photo-1579546929518-9e396f3cc809?q=80&w=2048&auto=format&fit=crop" # Bright abstract
        hero_object = "https://images.unsplash.com/photo-1518365050014-70fe7232897f?q=80&w=1000&auto=format&fit=crop" # Tech object

    # === CSS ===
    css = f"""/* High-Converting Hero Section */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;800&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --accent: {accent_color};
    --border: {border_color};
    --nav-bg: {nav_bg};
    --max-width: 1200px;
}}

body {{
    font-family: 'Inter', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-primary);
    line-height: 1.5;
    /* Simulate preview window */
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background: #000;
}}

/* Preview container mimicking a browser window */
.preview-window {{
    width: {width_px}px;
    height: {height_px}px;
    position: relative;
    overflow-y: auto;
    overflow-x: hidden;
    background-image: 
        linear-gradient(to right, rgba(11, 14, 20, 0.9) 0%, rgba(11, 14, 20, 0.4) 100%),
        url('{bg_image}');
    background-size: cover;
    background-position: center;
    display: flex;
    flex-direction: column;
    box-shadow: 0 20px 40px rgba(0,0,0,0.5);
}}

/* -- Navigation -- */
nav {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem 5%;
    background: var(--nav-bg);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid var(--border);
    position: sticky;
    top: 0;
    z-index: 100;
}}

.logo {{
    font-size: 1.25rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

.logo-icon {{
    width: 24px;
    height: 24px;
    background: var(--accent);
    border-radius: 4px;
    mask: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 2L2 22h20L12 2z"/></svg>') center/contain no-repeat;
    -webkit-mask: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 2L2 22h20L12 2z"/></svg>') center/contain no-repeat;
}}

.nav-links {{
    display: flex;
    gap: 2rem;
}}

.nav-links a {{
    color: var(--text-primary);
    text-decoration: none;
    font-weight: 500;
    font-size: 0.875rem;
    transition: opacity 0.2s;
}}

.nav-links a:hover {{
    opacity: 0.7;
}}

.btn-ghost {{
    padding: 0.5rem 1rem;
    border: 1px solid var(--border);
    border-radius: 4px;
    background: transparent;
    color: var(--text-primary);
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
}}

.btn-ghost:hover {{
    background: rgba(255,255,255,0.1);
}}

/* -- Main Hero Section -- */
.hero {{
    flex: 1;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4rem;
    max-width: var(--max-width);
    margin: 0 auto;
    padding: 4rem 5% 2rem 5%;
    align-items: center;
}}

/* -- Hero Content (Left) -- */
.hero-content {{
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    z-index: 10;
}}

.fade-up {{
    opacity: 0;
    transform: translateY(20px);
    animation: fadeUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}}

.delay-1 {{ animation-delay: 0.1s; }}
.delay-2 {{ animation-delay: 0.2s; }}
.delay-3 {{ animation-delay: 0.3s; }}
.delay-4 {{ animation-delay: 0.4s; }}

h1 {{
    font-size: clamp(2.5rem, 5vw, 4rem);
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -1px;
}}

.subtitle {{
    font-size: clamp(1rem, 2vw, 1.125rem);
    color: var(--text-secondary);
    max-width: 90%;
}}

.cta-container {{
    display: flex;
    align-items: center;
    gap: 1.5rem;
    margin-top: 1rem;
    flex-wrap: wrap;
}}

.btn-primary {{
    background-color: var(--accent);
    color: #fff;
    padding: 1rem 2rem;
    font-size: 1rem;
    font-weight: 700;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    transition: transform 0.2s, box-shadow 0.2s;
}}

.btn-primary:hover {{
    transform: translateY(-2px) scale(1.02);
    box-shadow: 0 10px 20px rgba(230, 36, 41, 0.3);
}}

/* -- Social Proof -- */
.social-proof {{
    display: flex;
    align-items: center;
}}

.avatar-group {{
    display: flex;
}}

.avatar {{
    width: 36px;
    height: 36px;
    border-radius: 50%;
    border: 2px solid var(--bg-color);
    margin-left: -12px;
    background-size: cover;
    background-position: center;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}}

.avatar:first-child {{
    margin-left: 0;
}}

.social-text {{
    font-size: 0.875rem;
    color: var(--text-secondary);
    margin-left: 12px;
    max-width: 150px;
    line-height: 1.2;
}}

.social-text strong {{
    color: var(--text-primary);
}}

/* -- Hero Visual (Right) -- */
.hero-visual {{
    position: relative;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}}

.hero-image {{
    width: 100%;
    max-width: 500px;
    aspect-ratio: 1;
    border-radius: 50%;
    object-fit: cover;
    box-shadow: 0 0 60px rgba(0,0,0,0.5);
    /* Abstract aesthetic touch to match the 'spaceship' vibe */
    mix-blend-mode: screen; 
    filter: contrast(1.2) brightness(1.1);
    animation: float 6s ease-in-out infinite;
}}

/* -- Trust Badges (Bottom) -- */
.trust-bar {{
    max-width: var(--max-width);
    margin: 0 auto;
    padding: 1rem 5% 2rem 5%;
    display: flex;
    align-items: center;
    gap: 2rem;
    border-top: 1px solid var(--border);
    width: 100%;
    opacity: 0.8;
}}

.trust-label {{
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--text-secondary);
    white-space: nowrap;
}}

.trust-logos {{
    display: flex;
    gap: 2rem;
    align-items: center;
    flex-wrap: wrap;
}}

.trust-logo {{
    font-weight: 800;
    font-size: 1.25rem;
    color: var(--text-secondary);
    letter-spacing: -0.5px;
    filter: grayscale(100%);
    opacity: 0.6;
    transition: opacity 0.3s, filter 0.3s;
    cursor: default;
}}

.trust-logo:hover {{
    opacity: 1;
    filter: grayscale(0%);
}}

/* -- Animations -- */
@keyframes fadeUp {{
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

@keyframes float {{
    0% {{ transform: translateY(0px) rotate(0deg); }}
    50% {{ transform: translateY(-15px) rotate(2deg); }}
    100% {{ transform: translateY(0px) rotate(0deg); }}
}}

/* -- Responsive -- */
@media (max-width: 900px) {{
    .hero {{
        grid-template-columns: 1fr;
        text-align: center;
        gap: 2rem;
        padding-top: 2rem;
    }}
    .hero-content {{
        align-items: center;
    }}
    .subtitle {{
        margin: 0 auto;
    }}
    .cta-container {{
        justify-content: center;
    }}
    .hero-visual {{
        display: none; /* Hide complex visual on small screens to focus on conversion */
    }}
    .trust-bar {{
        flex-direction: column;
        justify-content: center;
        gap: 1rem;
    }}
    .nav-links {{ display: none; }} /* Simple mobile nav hiding for demo */
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>High-Converting Hero</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="preview-window">
        
        <nav>
            <div class="logo">
                <div class="logo-icon"></div>
                ALLIANCE
            </div>
            <div class="nav-links">
                <a href="#">Our Ships</a>
                <a href="#">Mission</a>
                <a href="#">Donations</a>
            </div>
            <button class="btn-ghost">LOG IN</button>
        </nav>

        <main class="hero">
            <div class="hero-content">
                <h1 class="fade-up delay-1">{title_text}</h1>
                <p class="subtitle fade-up delay-2">{body_text}</p>
                
                <div class="cta-container fade-up delay-3">
                    <button class="btn-primary">JOIN NOW FOR FREE</button>
                    
                    <div class="social-proof">
                        <div class="avatar-group">
                            <div class="avatar" style="background-image: url('https://i.pravatar.cc/100?img=11')"></div>
                            <div class="avatar" style="background-image: url('https://i.pravatar.cc/100?img=33')"></div>
                            <div class="avatar" style="background-image: url('https://i.pravatar.cc/100?img=68')"></div>
                            <div class="avatar" style="background-image: url('https://i.pravatar.cc/100?img=47')"></div>
                        </div>
                        <div class="social-text">
                            <strong>Obi Wan</strong> and 4,000 others have already joined
                        </div>
                    </div>
                </div>
            </div>

            <div class="hero-visual fade-up delay-4">
                <img src="{hero_object}" alt="Hero dynamic object" class="hero-image">
            </div>
        </main>

        <footer class="trust-bar fade-up delay-4">
            <span class="trust-label">As seen on:</span>
            <div class="trust-logos">
                <span class="trust-logo" style="font-family: serif; font-style: italic;">The Daily</span>
                <span class="trust-logo" style="letter-spacing: 2px;">NEWS NETWORK</span>
                <span class="trust-logo" style="font-weight: 900;">TECH<span style="color:var(--accent)">CRUNCH</span></span>
                <span class="trust-logo" style="border: 2px solid currentColor; padding: 2px 6px;">Wired</span>
            </div>
        </footer>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// High-Converting Hero - Interaction Logic
document.addEventListener('DOMContentLoaded', () => {{
    // The primary animations are handled via CSS (keyframes and transitions).
    // This script adds subtle mouse-move parallax to the hero image for extra depth.

    const visualContainer = document.querySelector('.hero-visual');
    const heroImage = document.querySelector('.hero-image');

    if (visualContainer && heroImage) {{
        document.addEventListener('mousemove', (e) => {{
            const xAxis = (window.innerWidth / 2 - e.pageX) / 50;
            const yAxis = (window.innerHeight / 2 - e.pageY) / 50;
            
            heroImage.style.transform = `translateY(${{yAxis}}px) translateX(${{xAxis}}px)`;
        }});

        // Reset transform on mouse leave to prevent getting stuck
        document.addEventListener('mouseleave', () => {{
            heroImage.style.transition = 'transform 0.5s ease';
            heroImage.style.transform = `translateY(0px) translateX(0px)`;
            
            // Remove transition so mousemove is snappy again
            setTimeout(() => {{
                heroImage.style.transition = 'none';
            }}, 500);
        }});
    }}
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
