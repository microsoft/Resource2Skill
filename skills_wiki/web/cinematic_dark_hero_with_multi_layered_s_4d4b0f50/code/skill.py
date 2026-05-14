def create_component(
    output_dir: str,
    title_text: str = "IT's YOUR UNIVERSE,<br>IT'S TIME TO SAVE IT.",
    body_text: str = "The Rebel Alliance is fighting to get rid of the evil empire. Join the resistance to create a better future for your children.",
    color_scheme: str = "dark",
    accent_color: str = "#E50914", # Cinematic Red
    width_px: int = 1440,
    height_px: int = 900,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Cinematic Dark Hero pattern.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Base theme configuration
    bg_color = "#080b12"
    text_color = "#ffffff"
    text_muted = "rgba(255, 255, 255, 0.75)"
    bg_image_url = "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?q=80&w=2048&auto=format&fit=crop"

    # === CSS ===
    css = f"""/* Cinematic Dark Hero — Generated Component */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Oswald:wght@500;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-base: {bg_color};
    --text-main: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --font-heading: 'Oswald', sans-serif;
    --font-body: 'Inter', system-ui, sans-serif;
    --hero-width: {width_px}px;
    --hero-height: {height_px}px;
}}

body {{
    font-family: var(--font-body);
    background-color: var(--bg-base);
    color: var(--text-main);
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

/* Preview Container Constrain */
.preview-window {{
    width: 100%;
    max-width: var(--hero-width);
    height: 100vh;
    max-height: var(--hero-height);
    position: relative;
    overflow: hidden;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}}

/* Hero Section Architecture */
.hero-section {{
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    /* Layer gradient over image for contrast */
    background: linear-gradient(90deg, rgba(8,11,18,0.95) 0%, rgba(8,11,18,0.6) 50%, rgba(8,11,18,0.1) 100%),
                url('{bg_image_url}') center/cover no-repeat;
    position: relative;
}}

/* Header / Navigation */
.hero-header {{
    padding: 2rem 4rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 10;
}}

.logo {{
    font-family: var(--font-heading);
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: 1px;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

.logo-icon {{
    width: 24px;
    height: 24px;
    fill: var(--accent);
}}

.nav-links {{
    display: flex;
    gap: 2.5rem;
    align-items: center;
}}

.nav-links a {{
    color: var(--text-main);
    text-decoration: none;
    font-size: 0.95rem;
    font-weight: 500;
    transition: color 0.2s ease;
}}

.nav-links a:hover {{
    color: var(--accent);
}}

/* Buttons */
.btn {{
    padding: 0.8rem 2rem;
    font-family: var(--font-heading);
    font-size: 1rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 1px;
    text-decoration: none;
    border-radius: 4px;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    cursor: pointer;
    display: inline-block;
}}

.btn-ghost {{
    background: transparent;
    border: 2px solid var(--accent);
    color: var(--text-main);
}}

.btn-ghost:hover {{
    background: var(--accent);
}}

.btn-primary {{
    background: var(--accent);
    color: #fff;
    border: 2px solid var(--accent);
    padding: 1.2rem 3rem;
    font-size: 1.2rem;
    box-shadow: 0 10px 20px -10px var(--accent);
}}

.btn-primary:hover {{
    transform: translateY(-3px);
    box-shadow: 0 15px 25px -10px var(--accent);
}}

/* Main Content Area */
.hero-main {{
    flex-grow: 1;
    display: flex;
    align-items: center;
    padding: 0 4rem;
    z-index: 10;
}}

.content-block {{
    max-width: 650px;
}}

.content-block h1 {{
    font-family: var(--font-heading);
    font-size: 4.5rem;
    line-height: 1.1;
    margin-bottom: 1.5rem;
    text-transform: uppercase;
    letter-spacing: -1px;
}}

.content-block p {{
    font-size: 1.25rem;
    line-height: 1.6;
    color: var(--text-muted);
    margin-bottom: 2.5rem;
    max-width: 90%;
}}

/* Social Proof 1: Avatars */
.social-proof-users {{
    margin-top: 2rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}}

.avatar-stack {{
    display: flex;
}}

.avatar {{
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: 2px solid var(--bg-base);
    object-fit: cover;
}}

.avatar:not(:first-child) {{
    margin-left: -15px;
}}

.proof-text {{
    font-size: 0.9rem;
    color: var(--text-muted);
    font-weight: 500;
}}

/* Social Proof 2: Authority Logos Footer */
.hero-footer {{
    padding: 2rem 4rem;
    display: flex;
    align-items: center;
    gap: 2rem;
    border-top: 1px solid rgba(255,255,255,0.05);
    background: linear-gradient(to top, rgba(0,0,0,0.4), transparent);
    z-index: 10;
}}

.footer-label {{
    font-size: 0.85rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
    white-space: nowrap;
}}

.logo-strip {{
    display: flex;
    gap: 3rem;
    align-items: center;
    flex-wrap: wrap;
}}

.authority-logo {{
    height: 30px;
    /* Turn any SVG/image into a subtle watermark */
    filter: grayscale(100%) brightness(200%) opacity(0.4);
    transition: filter 0.3s ease;
}}

.authority-logo:hover {{
    filter: grayscale(100%) brightness(200%) opacity(0.8);
}}

/* Animation Classes */
.animate-element {{
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.8s ease-out, transform 0.8s cubic-bezier(0.2, 0.8, 0.2, 1);
}}

.animate-element.is-visible {{
    opacity: 1;
    transform: translateY(0);
}}

@media (max-width: 768px) {{
    .content-block h1 {{ font-size: 3rem; }}
    .hero-header, .hero-main, .hero-footer {{ padding: 1.5rem 2rem; }}
    .nav-links {{ display: none; }} /* Simple mobile handling */
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cinematic Hero Pattern</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="preview-window">
        <section class="hero-section">
            
            <header class="hero-header animate-element" style="transition-delay: 0.1s;">
                <div class="logo">
                    <!-- Generic abstract logo icon -->
                    <svg class="logo-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 2L2 22h20L12 2zm0 3.8l7.5 15h-15L12 5.8z" />
                        <path d="M12 10l-4 8h8l-4-8z" />
                    </svg>
                    REBEL ALLIANCE
                </div>
                <nav class="nav-links">
                    <a href="#">Our Ships</a>
                    <a href="#">Mission</a>
                    <a href="#">Donations</a>
                    <a href="#" class="btn btn-ghost">Join Now</a>
                </nav>
            </header>

            <main class="hero-main">
                <div class="content-block">
                    <h1 class="animate-element" style="transition-delay: 0.2s;">{title_text}</h1>
                    <p class="animate-element" style="transition-delay: 0.3s;">{body_text}</p>
                    
                    <a href="#" class="btn btn-primary animate-element" style="transition-delay: 0.4s;">Join Now For Free</a>
                    
                    <div class="social-proof-users animate-element" style="transition-delay: 0.5s;">
                        <div class="avatar-stack">
                            <img src="https://i.pravatar.cc/100?img=11" alt="User" class="avatar">
                            <img src="https://i.pravatar.cc/100?img=12" alt="User" class="avatar">
                            <img src="https://i.pravatar.cc/100?img=13" alt="User" class="avatar">
                            <img src="https://i.pravatar.cc/100?img=14" alt="User" class="avatar">
                        </div>
                        <span class="proof-text">Obi Wan and 4,000 others have already joined</span>
                    </div>
                </div>
            </main>

            <footer class="hero-footer animate-element" style="transition-delay: 0.6s;">
                <span class="footer-label">As seen on:</span>
                <div class="logo-strip">
                    <!-- Inline SVGs acting as placeholder authority logos -->
                    <svg class="authority-logo" viewBox="0 0 100 30" xmlns="http://www.w3.org/2000/svg">
                        <text x="0" y="22" font-family="Arial" font-weight="bold" font-size="24" fill="#fff">TECHCRUNCH</text>
                    </svg>
                    <svg class="authority-logo" viewBox="0 0 100 30" xmlns="http://www.w3.org/2000/svg">
                        <text x="0" y="22" font-family="Times New Roman" font-weight="bold" font-size="24" fill="#fff">Forbes</text>
                    </svg>
                    <svg class="authority-logo" viewBox="0 0 100 30" xmlns="http://www.w3.org/2000/svg">
                        <text x="0" y="22" font-family="Arial" font-weight="900" font-style="italic" font-size="24" fill="#fff">WIRED</text>
                    </svg>
                </div>
            </footer>

        </section>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Cinematic Dark Hero — Entrance Animation Logic
document.addEventListener('DOMContentLoaded', () => {{
    // Trigger entrance animations shortly after load to ensure smooth rendering
    setTimeout(() => {{
        const elements = document.querySelectorAll('.animate-element');
        elements.forEach(el => {{
            el.classList.add('is-visible');
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
