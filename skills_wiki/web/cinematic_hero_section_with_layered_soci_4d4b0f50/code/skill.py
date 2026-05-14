def create_component(
    output_dir: str,
    title_text: str = "It's your universe, it's time to save it",
    body_text: str = "The Alliance is fighting to get rid of the evil empire, join the resistance to create a better future for your children.",
    color_scheme: str = "dark",
    accent_color: str = "#E62429",
    width_px: int = 1440,
    height_px: int = 900,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Cinematic Hero Section with Social Proof.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme logic
    if color_scheme == "dark":
        text_main = "#ffffff"
        text_muted = "#a0aabf"
        bg_image_url = "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?ixlib=rb-4.0.3&auto=format&fit=crop&w=2048&q=80"
        overlay_gradient = "linear-gradient(90deg, rgba(9, 10, 15, 0.95) 0%, rgba(9, 10, 15, 0.8) 40%, rgba(9, 10, 15, 0.1) 100%)"
        border_color = "rgba(255, 255, 255, 0.1)"
        avatar_border = "#090a0f"
    else:
        text_main = "#111827"
        text_muted = "#4b5563"
        bg_image_url = "https://images.unsplash.com/photo-1507608616759-54f48f0af0ee?ixlib=rb-4.0.3&auto=format&fit=crop&w=2048&q=80"
        overlay_gradient = "linear-gradient(90deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 255, 255, 0.8) 40%, rgba(255, 255, 255, 0.1) 100%)"
        border_color = "rgba(0, 0, 0, 0.1)"
        avatar_border = "#ffffff"

    # === CSS ===
    css = f"""/* Cinematic Hero Component */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500&family=Montserrat:wght@800;900&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --text-main: {text_main};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --border: {border_color};
    --avatar-border: {avatar_border};
    --width: {width_px}px;
    --height: {height_px}px;
    
    --font-heading: 'Montserrat', sans-serif;
    --font-body: 'Inter', sans-serif;
}}

body {{
    font-family: var(--font-body);
    background: #000;
    color: var(--text-main);
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

/* Main Container matching requested dimensions */
.hero-wrapper {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    position: relative;
    display: flex;
    flex-direction: column;
    background-image: url('{bg_image_url}');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    overflow: hidden;
}}

/* Gradient Overlay for Readability */
.hero-wrapper::before {{
    content: '';
    position: absolute;
    inset: 0;
    background: {overlay_gradient};
    z-index: 1;
}}

/* Ensures content sits above the overlay */
.hero-wrapper > * {{
    position: relative;
    z-index: 2;
}}

/* Navigation Bar */
.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2rem 4rem;
}}

.logo {{
    font-family: var(--font-heading);
    font-size: 1.5rem;
    font-weight: 900;
    letter-spacing: -0.5px;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

.logo-icon {{
    width: 32px;
    height: 32px;
    fill: var(--accent);
}}

.nav-links {{
    display: flex;
    gap: 2.5rem;
    list-style: none;
}}

.nav-links a {{
    color: var(--text-main);
    text-decoration: none;
    font-size: 0.95rem;
    font-weight: 500;
    transition: color 0.2s;
}}

.nav-links a:hover {{
    color: var(--accent);
}}

/* Buttons */
.btn {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.875rem 2rem;
    font-family: var(--font-heading);
    font-weight: 800;
    text-transform: uppercase;
    text-decoration: none;
    letter-spacing: 0.5px;
    border-radius: 4px;
    transition: all 0.3s ease;
    cursor: pointer;
}}

.btn-primary {{
    background-color: var(--accent);
    color: #ffffff;
    border: 2px solid var(--accent);
}}

.btn-primary:hover {{
    background-color: transparent;
    color: var(--accent);
}}

.btn-ghost {{
    background-color: transparent;
    color: var(--text-main);
    border: 2px solid var(--border);
    padding: 0.6rem 1.5rem;
}}

.btn-ghost:hover {{
    border-color: var(--accent);
    color: var(--accent);
}}

/* Main Hero Content area */
.hero-content {{
    flex: 1;
    display: flex;
    align-items: center;
    padding: 0 4rem;
}}

.hero-text-block {{
    max-width: 650px;
}}

.hero-title {{
    font-family: var(--font-heading);
    font-size: clamp(3rem, 5vw, 4.5rem);
    line-height: 1.1;
    font-weight: 900;
    letter-spacing: -1.5px;
    margin-bottom: 1.5rem;
}}

.hero-body {{
    font-size: 1.125rem;
    line-height: 1.6;
    color: var(--text-muted);
    margin-bottom: 2.5rem;
    max-width: 500px;
}}

/* Social Proof: Avatars */
.social-proof-avatars {{
    display: flex;
    align-items: center;
    margin-top: 2rem;
}}

.avatar-stack {{
    display: flex;
}}

.avatar-stack img {{
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: 3px solid var(--avatar-border);
    margin-left: -12px;
    object-fit: cover;
}}

.avatar-stack img:first-child {{
    margin-left: 0;
}}

.avatar-text {{
    margin-left: 1rem;
    font-size: 0.875rem;
    color: var(--text-muted);
    font-weight: 500;
}}

.avatar-text span {{
    color: var(--text-main);
    font-weight: 700;
}}

/* Social Proof: Authority Logos */
.social-proof-logos {{
    display: flex;
    align-items: center;
    padding: 2rem 4rem;
    border-top: 1px solid var(--border);
    gap: 2rem;
}}

.social-proof-logos span {{
    font-size: 0.875rem;
    color: var(--text-muted);
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 1px;
}}

.logo-strip {{
    display: flex;
    align-items: center;
    gap: 3rem;
}}

.logo-strip svg {{
    height: 24px;
    fill: var(--text-main);
    opacity: 0.4;
    filter: grayscale(100%);
    transition: all 0.3s ease;
}}

.logo-strip svg:hover {{
    opacity: 1;
    filter: grayscale(0%);
}}

/* Responsive */
@media (max-width: 768px) {{
    .navbar, .hero-content, .social-proof-logos {{ padding: 1.5rem; }}
    .nav-links, .btn-ghost {{ display: none; }}
    .logo-strip {{ gap: 1.5rem; flex-wrap: wrap; }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cinematic Hero Section</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="hero-wrapper">
        
        <!-- Navigation -->
        <nav class="navbar">
            <div class="logo">
                <svg class="logo-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 2L2 22h20L12 2zm0 4.5l6.5 13h-13L12 6.5z"/>
                </svg>
                ALLIANCE
            </div>
            <ul class="nav-links">
                <li><a href="#">Our Ships</a></li>
                <li><a href="#">Mission</a></li>
                <li><a href="#">Donations</a></li>
            </ul>
            <a href="#" class="btn btn-ghost">Join Now</a>
        </nav>

        <!-- Hero Content -->
        <main class="hero-content">
            <div class="hero-text-block">
                <h1 class="hero-title">{title_text}</h1>
                <p class="hero-body">{body_text}</p>
                
                <a href="#" class="btn btn-primary">Join Now For Free</a>
                
                <!-- Social Proof: Avatars -->
                <div class="social-proof-avatars">
                    <div class="avatar-stack">
                        <img src="https://i.pravatar.cc/100?img=33" alt="User">
                        <img src="https://i.pravatar.cc/100?img=47" alt="User">
                        <img src="https://i.pravatar.cc/100?img=12" alt="User">
                        <img src="https://i.pravatar.cc/100?img=68" alt="User">
                    </div>
                    <div class="avatar-text">
                        <span>Obi Wan</span> and 4,000 others have already joined
                    </div>
                </div>
            </div>
        </main>

        <!-- Social Proof: Logos -->
        <div class="social-proof-logos">
            <span>As Seen On:</span>
            <div class="logo-strip">
                <!-- Generic SVG Logos for demonstration -->
                <svg viewBox="0 0 100 30"><text x="0" y="22" font-family="Arial" font-weight="bold" font-size="24">Forbes</text></svg>
                <svg viewBox="0 0 100 30"><text x="0" y="22" font-family="Arial" font-weight="bold" font-size="24" font-style="italic">WIRED</text></svg>
                <svg viewBox="0 0 100 30"><text x="0" y="22" font-family="Georgia" font-weight="bold" font-size="22">The Times</text></svg>
                <svg viewBox="0 0 100 30"><text x="0" y="22" font-family="Arial" font-weight="bold" font-size="24">TechCrunch</text></svg>
            </div>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Component behaviors
document.addEventListener('DOMContentLoaded', () => {{
    // Add subtle entrance animation for hero content
    const heroContent = document.querySelector('.hero-text-block');
    
    heroContent.animate([
        {{ opacity: 0, transform: 'translateY(20px)' }},
        {{ opacity: 1, transform: 'translateY(0)' }}
    ], {{
        duration: 800,
        easing: 'cubic-bezier(0.2, 0.8, 0.2, 1)',
        fill: 'forwards'
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
