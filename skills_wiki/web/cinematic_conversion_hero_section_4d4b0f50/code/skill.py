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
    Create a web component reproducing the Cinematic Conversion Hero Section.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#050505"
        text_color = "#ffffff"
        text_muted = "rgba(255, 255, 255, 0.7)"
        border_color = "rgba(255, 255, 255, 0.15)"
        # Cinematic space background
        bg_image = "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?q=80&w=2048&auto=format&fit=crop"
        overlay = f"linear-gradient(to right, {bg_color} 0%, {bg_color} 30%, rgba(5,5,5,0.7) 60%, rgba(5,5,5,0) 100%)"
        logo_filter = "brightness(0) invert(1) opacity(0.5)"
    else:
        bg_color = "#ffffff"
        text_color = "#111827"
        text_muted = "rgba(17, 24, 39, 0.7)"
        border_color = "rgba(0, 0, 0, 0.1)"
        # Lighter abstract tech background
        bg_image = "https://images.unsplash.com/photo-1557683316-973673baf926?q=80&w=2000&auto=format&fit=crop"
        overlay = f"linear-gradient(to right, {bg_color} 0%, {bg_color} 40%, rgba(255,255,255,0.8) 70%, rgba(255,255,255,0) 100%)"
        logo_filter = "grayscale(100%) opacity(0.6)"

    # === CSS ===
    css = f"""/* Cinematic Conversion Hero Section */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500&family=Montserrat:wght@700;800;900&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --text-muted: {text_muted};
    --accent-color: {accent_color};
    --border-color: {border_color};
}}

body {{
    font-family: 'Inter', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}}

.hero-wrapper {{
    width: 100%;
    max-width: {width_px}px;
    min-height: {height_px}px;
    position: relative;
    display: flex;
    flex-direction: column;
    padding: 2rem 4rem;
    overflow: hidden;
    background-image: {overlay}, url('{bg_image}');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}}

/* Header / Nav */
.header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 10;
}}

.logo {{
    font-family: 'Montserrat', sans-serif;
    font-weight: 800;
    font-size: 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    letter-spacing: -0.5px;
}}

.logo i {{
    color: var(--accent-color);
    font-size: 1.75rem;
}}

.nav-links {{
    display: flex;
    align-items: center;
    gap: 2rem;
}}

.nav-links a {{
    color: var(--text-color);
    text-decoration: none;
    font-size: 0.875rem;
    font-weight: 500;
    transition: opacity 0.2s ease;
}}

.nav-links a:hover {{
    opacity: 0.7;
}}

/* Buttons */
.btn {{
    display: inline-block;
    padding: 0.75rem 1.5rem;
    border-radius: 4px;
    font-weight: 600;
    font-size: 0.875rem;
    text-decoration: none;
    transition: all 0.3s ease;
    cursor: pointer;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

.btn-ghost {{
    border: 1px solid var(--border-color);
    color: var(--text-color);
    background: transparent;
}}

.btn-ghost:hover {{
    background: rgba(255,255,255,0.1);
    border-color: var(--text-color);
}}

.btn-primary {{
    background: var(--accent-color);
    color: #ffffff;
    border: none;
    padding: 1rem 2rem;
    font-size: 1rem;
    box-shadow: 0 4px 14px rgba(230, 36, 41, 0.4);
}}

.btn-primary:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(230, 36, 41, 0.6);
    filter: brightness(1.1);
}}

/* Main Content */
.hero-main {{
    flex: 1;
    display: flex;
    align-items: center;
    z-index: 10;
    margin: 4rem 0;
}}

.hero-content {{
    max-width: 650px;
}}

.headline {{
    font-family: 'Montserrat', sans-serif;
    font-weight: 900;
    font-size: 4.5rem;
    line-height: 1.05;
    letter-spacing: -1.5px;
    margin-bottom: 1.5rem;
}}

.description {{
    font-size: 1.25rem;
    line-height: 1.6;
    color: var(--text-muted);
    margin-bottom: 2.5rem;
    max-width: 550px;
}}

/* Social Proof */
.social-proof {{
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-top: 2rem;
}}

.avatars {{
    display: flex;
}}

.avatars img {{
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: 2px solid var(--bg-color);
    margin-left: -12px;
    object-fit: cover;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}}

.avatars img:first-child {{
    margin-left: 0;
}}

.social-text {{
    font-size: 0.875rem;
    color: var(--text-muted);
    line-height: 1.4;
}}

.social-text strong {{
    color: var(--text-color);
}}

/* Trust Badges Footer */
.trust-bar {{
    display: flex;
    align-items: center;
    gap: 2rem;
    padding-top: 2rem;
    border-top: 1px solid var(--border-color);
    z-index: 10;
}}

.trust-label {{
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1px;
}}

.logos {{
    display: flex;
    gap: 2.5rem;
    align-items: center;
}}

.logos i {{
    font-size: 1.75rem;
    filter: {logo_filter};
    transition: filter 0.3s ease, opacity 0.3s ease;
}}

.logos i:hover {{
    filter: none;
    opacity: 1;
    color: var(--text-color);
}}

/* Entrance Animation Classes */
.stagger-in {{
    opacity: 0;
    transform: translateY(20px);
}}

/* Responsive */
@media (max-width: 1024px) {{
    .hero-wrapper {{ padding: 2rem; }}
    .headline {{ font-size: 3.5rem; }}
}}
@media (max-width: 768px) {{
    .hero-wrapper {{ background-image: {overlay}, url('{bg_image}'); background-position: right center; }}
    .headline {{ font-size: 2.5rem; }}
    .nav-links a:not(.btn) {{ display: none; }}
    .trust-bar {{ flex-direction: column; align-items: flex-start; gap: 1rem; }}
    .logos {{ flex-wrap: wrap; gap: 1.5rem; }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hero Section</title>
    <!-- FontAwesome for Icons/Logos -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="hero-wrapper">
        
        <header class="header stagger-in">
            <div class="logo">
                <i class="fa-solid fa-jedi"></i> REBEL
            </div>
            <nav class="nav-links">
                <a href="#">Our Ships</a>
                <a href="#">Mission</a>
                <a href="#">Donations</a>
                <a href="#" class="btn btn-ghost">Sign In</a>
            </nav>
        </header>

        <main class="hero-main">
            <div class="hero-content">
                <h1 class="headline stagger-in">{title_text}</h1>
                <p class="description stagger-in">{body_text}</p>
                
                <div class="stagger-in">
                    <a href="#" class="btn btn-primary">JOIN NOW FOR FREE</a>
                </div>
                
                <div class="social-proof stagger-in">
                    <div class="avatars">
                        <img src="https://i.pravatar.cc/150?img=11" alt="Member">
                        <img src="https://i.pravatar.cc/150?img=33" alt="Member">
                        <img src="https://i.pravatar.cc/150?img=12" alt="Member">
                        <img src="https://i.pravatar.cc/150?img=47" alt="Member">
                    </div>
                    <div class="social-text">
                        <strong>Obi Wan</strong> and 4,000 others<br>have already joined
                    </div>
                </div>
            </div>
        </main>
        
        <footer class="trust-bar stagger-in">
            <span class="trust-label">As Seen On:</span>
            <div class="logos">
                <i class="fa-brands fa-aws" title="AWS"></i>
                <i class="fa-brands fa-hbo" title="HBO"></i>
                <i class="fa-brands fa-playstation" title="PlayStation"></i>
                <i class="fa-brands fa-xbox" title="Xbox"></i>
                <i class="fa-brands fa-galactic-senate" title="Galactic Senate"></i>
            </div>
        </footer>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Staggered entrance animation for hero elements
document.addEventListener('DOMContentLoaded', () => {{
    const elements = document.querySelectorAll('.stagger-in');
    
    // Set initial transition styles via JS to keep CSS clean
    elements.forEach((el, index) => {{
        el.style.transition = `opacity 0.8s cubic-bezier(0.16, 1, 0.3, 1) ${{index * 0.15}}s, transform 0.8s cubic-bezier(0.16, 1, 0.3, 1) ${{index * 0.15}}s`;
    }});

    // Small delay to ensure CSS is ready before triggering reflow
    setTimeout(() => {{
        elements.forEach(el => {{
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
        }});
    }}, 100);
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
