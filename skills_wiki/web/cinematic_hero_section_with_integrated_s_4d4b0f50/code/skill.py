def create_component(
    output_dir: str,
    title_text: str = "It's your universe,<br>it's time to save it",
    body_text: str = "The Rebel alliance is fighting to get rid of the evil empire, join the resistance to create a better future for your children.",
    color_scheme: str = "dark",
    accent_color: str = "#e62e2d",
    width_px: int = 1440,
    height_px: int = 900,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Cinematic Hero Section with Social Proof.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme logic (Tutorial is strictly dark/space themed, but we accommodate logic)
    if color_scheme == "dark":
        text_color = "#ffffff"
        text_muted = "rgba(255, 255, 255, 0.7)"
        bg_image_url = "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?q=80&w=2048&auto=format&fit=crop" # Dark space
        gradient_overlay = "linear-gradient(90deg, rgba(13, 17, 28, 0.95) 0%, rgba(13, 17, 28, 0.6) 40%, rgba(13, 17, 28, 0.1) 100%)"
        border_color = "rgba(255, 255, 255, 0.1)"
    else:
        text_color = "#111827"
        text_muted = "rgba(17, 24, 39, 0.7)"
        bg_image_url = "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2048&auto=format&fit=crop" # Lighter tech/earth
        gradient_overlay = "linear-gradient(90deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 255, 255, 0.7) 40%, rgba(255, 255, 255, 0.2) 100%)"
        border_color = "rgba(0, 0, 0, 0.1)"

    css = f"""/* Cinematic Hero Section */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;900&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --text-primary: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --border: {border_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: #000;
    color: var(--text-primary);
    -webkit-font-smoothing: antialiased;
    overflow-x: hidden;
}}

.hero-wrapper {{
    width: 100%;
    /* Constrain to requested dimensions for testing, normally 100vh/100vw */
    max-width: var(--width);
    height: var(--height);
    margin: 0 auto;
    position: relative;
    display: flex;
    flex-direction: column;
    background-image: {gradient_overlay}, url('{bg_image_url}');
    background-size: cover;
    background-position: center right;
}}

/* Header / Navbar */
.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2rem 4rem;
    z-index: 10;
}}

.brand-logo {{
    font-size: 1.5rem;
    font-weight: 900;
    letter-spacing: -0.05em;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

.brand-icon {{
    width: 32px;
    height: 32px;
    background-color: var(--accent);
    border-radius: 50%;
    display: inline-block;
    mask: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white"><path d="M12 2L2 22h20L12 2z"/></svg>') center/contain no-repeat;
    -webkit-mask: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white"><path d="M12 2L2 22h20L12 2z"/></svg>') center/contain no-repeat;
}}

.nav-links {{
    display: flex;
    gap: 2.5rem;
}}

.nav-links a {{
    color: var(--text-primary);
    text-decoration: none;
    font-weight: 500;
    font-size: 0.95rem;
    transition: color 0.2s ease;
}}

.nav-links a:hover {{
    color: var(--accent);
}}

.btn {{
    padding: 0.75rem 1.5rem;
    font-weight: 700;
    text-transform: uppercase;
    text-decoration: none;
    letter-spacing: 0.05em;
    font-size: 0.85rem;
    border-radius: 4px;
    transition: all 0.3s ease;
    cursor: pointer;
}}

.btn-ghost {{
    color: var(--text-primary);
    border: 2px solid var(--border);
}}

.btn-ghost:hover {{
    border-color: var(--text-primary);
    background: rgba(255,255,255,0.1);
}}

.btn-primary {{
    background-color: var(--accent);
    color: #fff;
    border: 2px solid var(--accent);
    padding: 1rem 2rem;
    font-size: 1rem;
}}

.btn-primary:hover {{
    background-color: transparent;
    color: var(--accent);
}}

/* Main Content */
.hero-content {{
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 0 4rem;
    max-width: 800px;
    z-index: 10;
}}

.hero-title {{
    font-size: clamp(3rem, 5vw, 5rem);
    font-weight: 900;
    line-height: 1.1;
    letter-spacing: -0.03em;
    margin-bottom: 1.5rem;
    text-transform: capitalize;
}}

.hero-subtitle {{
    font-size: 1.125rem;
    line-height: 1.6;
    color: var(--text-muted);
    margin-bottom: 2.5rem;
    max-width: 600px;
}}

/* User Proof Section */
.user-proof {{
    margin-top: 3rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}}

.avatar-group {{
    display: flex;
}}

.avatar {{
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: 2px solid var(--text-primary);
    background-size: cover;
    background-position: center;
    margin-left: -12px;
}}
.avatar:first-child {{ margin-left: 0; }}

.proof-text {{
    font-size: 0.85rem;
    color: var(--text-muted);
    font-weight: 500;
}}

/* Social Proof Footer */
.social-proof-footer {{
    padding: 2rem 4rem;
    display: flex;
    align-items: center;
    gap: 2rem;
    border-top: 1px solid var(--border);
    z-index: 10;
}}

.social-proof-footer span {{
    font-size: 0.85rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 700;
}}

.logos {{
    display: flex;
    gap: 3rem;
    align-items: center;
    opacity: 0.6;
}}

.logo-placeholder {{
    font-weight: 900;
    font-size: 1.25rem;
    letter-spacing: -0.05em;
    color: var(--text-primary);
    /* Mimicking brand logo shapes */
}}

/* Animations */
@keyframes fadeInUp {{
    from {{ opacity: 0; transform: translateY(20px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

.hero-content > * {{
    animation: fadeInUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
    opacity: 0;
}}

.hero-content h1 {{ animation-delay: 0.1s; }}
.hero-content p {{ animation-delay: 0.2s; }}
.hero-content .btn-primary {{ animation-delay: 0.3s; }}
.hero-content .user-proof {{ animation-delay: 0.5s; }}
"""

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
        
        <header class="navbar">
            <div class="brand-logo">
                <span class="brand-icon"></span>
                Rebel
            </div>
            <nav class="nav-links">
                <a href="#">Our Ships</a>
                <a href="#">Mission</a>
                <a href="#">Donations</a>
            </nav>
            <a href="#" class="btn btn-ghost">Join Now</a>
        </header>

        <main class="hero-content">
            <h1 class="hero-title">{title_text}</h1>
            <p class="hero-subtitle">{body_text}</p>
            <div>
                <a href="#" class="btn btn-primary">Join Now For Free</a>
            </div>
            
            <div class="user-proof">
                <div class="avatar-group">
                    <div class="avatar" style="background-image: url('https://images.unsplash.com/photo-1500648767791-00dcc994a43e?q=80&w=150&auto=format&fit=crop')"></div>
                    <div class="avatar" style="background-image: url('https://images.unsplash.com/photo-1494790108377-be9c29b29330?q=80&w=150&auto=format&fit=crop')"></div>
                    <div class="avatar" style="background-image: url('https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=150&auto=format&fit=crop')"></div>
                    <div class="avatar" style="background-image: url('https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=150&auto=format&fit=crop')"></div>
                </div>
                <span class="proof-text">Obi Wan and 4,000 others have already joined</span>
            </div>
        </main>

        <footer class="social-proof-footer">
            <span>As Seen On:</span>
            <div class="logos">
                <div class="logo-placeholder" style="font-family: serif; font-style: italic;">The Times</div>
                <div class="logo-placeholder" style="border: 2px solid currentColor; padding: 2px 6px;">N N N</div>
                <div class="logo-placeholder" style="letter-spacing: 0.1em;">GLOBE</div>
                <div class="logo-placeholder" style="text-transform: lowercase; font-weight: 700;">wire</div>
            </div>
        </footer>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// No complex JS required for this structural design pattern.
// Entrance animations are handled via CSS keyframes.
console.log("Hero section loaded.");
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
