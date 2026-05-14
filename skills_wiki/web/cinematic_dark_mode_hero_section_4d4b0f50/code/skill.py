def create_component(
    output_dir: str,
    title_text: str = "It's your universe,<br>it's time to save it",
    body_text: str = "The Rebel alliance is fighting to get rid of the evil empire. Join the resistance to create a better future for your children.",
    color_scheme: str = "dark",
    accent_color: str = "#e62b29",
    width_px: int = 1280,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Cinematic Dark Mode Hero Section.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Base theme colors
    bg_color = "#05070a" # Deep space black/blue
    text_color = "#ffffff"
    muted_text = "rgba(255, 255, 255, 0.65)"
    border_color = "rgba(255, 255, 255, 0.15)"

    # CSS
    css = f"""/* Cinematic Hero Section */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;900&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {muted_text};
    --accent: {accent_color};
    --border: {border_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: #000;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

/* Preview Wrapper restricts size to requested dimensions */
.hero-wrapper {{
    width: var(--width);
    height: var(--height);
    background-color: var(--bg);
    /* Simulated starfield background */
    background-image: 
        radial-gradient(circle at 15% 50%, rgba(255, 255, 255, 0.08) 0%, transparent 50%),
        radial-gradient(circle at 85% 30%, rgba(230, 43, 41, 0.05) 0%, transparent 50%);
    color: var(--text);
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    box-shadow: 0 24px 48px rgba(0,0,0,0.5);
}}

/* --- Navigation --- */
.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 24px 48px;
    z-index: 10;
}}

.logo {{
    display: flex;
    align-items: center;
    gap: 12px;
    font-weight: 700;
    font-size: 1.25rem;
    letter-spacing: -0.5px;
}}

.nav-links {{
    display: flex;
    gap: 32px;
    list-style: none;
}}

.nav-links a {{
    color: var(--text-muted);
    text-decoration: none;
    font-weight: 500;
    font-size: 0.9rem;
    transition: color 0.2s ease;
}}

.nav-links a:hover {{
    color: var(--text);
}}

.btn-ghost {{
    border: 2px solid var(--accent);
    background: transparent;
    color: var(--text);
    padding: 10px 24px;
    font-weight: 700;
    text-transform: uppercase;
    font-size: 0.85rem;
    cursor: pointer;
    transition: all 0.2s ease;
}}

.btn-ghost:hover {{
    background: var(--accent);
}}

/* --- Main Content --- */
.hero-main {{
    flex: 1;
    display: grid;
    grid-template-columns: 1fr 1fr;
    padding: 0 48px;
    align-items: center;
    z-index: 5;
}}

.hero-text {{
    display: flex;
    flex-direction: column;
    gap: 24px;
    max-width: 540px;
}}

.headline {{
    font-size: clamp(3rem, 4vw, 4.5rem);
    font-weight: 900;
    line-height: 1.05;
    letter-spacing: -1.5px;
}}

.sub-headline {{
    font-size: 1.1rem;
    color: var(--text-muted);
    line-height: 1.6;
}}

.btn-primary {{
    align-self: flex-start;
    background: var(--accent);
    color: #fff;
    border: none;
    padding: 18px 36px;
    font-weight: 900;
    font-size: 1rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    cursor: pointer;
    box-shadow: 0 4px 14px rgba(230, 43, 41, 0.4);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    margin-top: 8px;
}}

.btn-primary:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(230, 43, 41, 0.6);
}}

/* Social Proof */
.social-proof {{
    display: flex;
    align-items: center;
    gap: 16px;
    margin-top: 16px;
}}

.avatars {{
    display: flex;
}}

.avatar {{
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: 2px solid var(--bg);
    background-color: #333;
    background-size: cover;
    background-position: center;
    margin-left: -12px;
}}

.avatar:first-child {{
    margin-left: 0;
}}

.social-text {{
    font-size: 0.85rem;
    color: var(--text-muted);
    font-weight: 500;
}}

/* --- Visual Foreground --- */
.hero-visual {{
    position: relative;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}}

/* Placeholder for a dramatic cut-out image */
.visual-subject {{
    width: 120%;
    max-width: 800px;
    position: absolute;
    right: -10%;
    filter: drop-shadow(-20px 20px 30px rgba(0,0,0,0.8));
    animation: float 6s ease-in-out infinite;
}}

@keyframes float {{
    0%, 100% {{ transform: translateY(0) rotate(-2deg); }}
    50% {{ transform: translateY(-20px) rotate(1deg); }}
}}

/* --- Footer Logos --- */
.hero-footer {{
    display: flex;
    align-items: center;
    gap: 24px;
    padding: 24px 48px;
    border-top: 1px solid var(--border);
    z-index: 10;
}}

.as-seen {{
    font-size: 0.8rem;
    text-transform: uppercase;
    font-weight: 700;
    color: var(--text-muted);
    letter-spacing: 1px;
}}

.brand-logos {{
    display: flex;
    gap: 32px;
}}

.brand-logo {{
    height: 24px;
    opacity: 0.4;
    filter: grayscale(100%) brightness(200%);
    transition: opacity 0.3s ease;
}}

.brand-logo:hover {{
    opacity: 0.8;
}}
"""

    # HTML
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
        
        <!-- Navbar -->
        <nav class="navbar">
            <div class="logo">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="var(--accent)">
                    <path d="M12 2L1 21h22L12 2zm0 3.99L19.53 19H4.47L12 5.99z"/>
                </svg>
                REBEL ALLIANCE
            </div>
            <ul class="nav-links">
                <li><a href="#">Our Ships</a></li>
                <li><a href="#">Mission</a></li>
                <li><a href="#">Donations</a></li>
            </ul>
            <button class="btn-ghost">Join Now</button>
        </nav>

        <!-- Main Content -->
        <main class="hero-main">
            <div class="hero-text">
                <h1 class="headline">{title_text}</h1>
                <p class="sub-headline">{body_text}</p>
                <button class="btn-primary">Join Now For Free</button>
                
                <div class="social-proof">
                    <div class="avatars">
                        <div class="avatar" style="background-image: url('https://i.pravatar.cc/100?img=11')"></div>
                        <div class="avatar" style="background-image: url('https://i.pravatar.cc/100?img=32')"></div>
                        <div class="avatar" style="background-image: url('https://i.pravatar.cc/100?img=33')"></div>
                        <div class="avatar" style="background-image: url('https://i.pravatar.cc/100?img=68')"></div>
                    </div>
                    <span class="social-text">Obi Wan and 4,000 others have already joined</span>
                </div>
            </div>

            <div class="hero-visual">
                <!-- Using a high-quality transparent PNG placeholder from an open API to simulate the cutout effect -->
                <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/150.png" alt="Hero Subject" class="visual-subject" style="filter: grayscale(100%) contrast(150%) brightness(80%) drop-shadow(-20px 20px 30px rgba(0,0,0,0.8));">
            </div>
        </main>

        <!-- Footer / Authority Logos -->
        <footer class="hero-footer">
            <span class="as-seen">As Seen On:</span>
            <div class="brand-logos">
                <!-- Placeholder SVG logos -->
                <svg class="brand-logo" viewBox="0 0 100 30" fill="currentColor"><text x="0" y="20" font-weight="900" font-size="24">FORBES</text></svg>
                <svg class="brand-logo" viewBox="0 0 100 30" fill="currentColor"><text x="0" y="20" font-weight="900" font-size="24">WIRED</text></svg>
                <svg class="brand-logo" viewBox="0 0 100 30" fill="currentColor"><text x="0" y="20" font-weight="900" font-size="24">CNBC</text></svg>
            </div>
        </footer>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # JavaScript
    js = """// Cinematic Hero Section
document.addEventListener('DOMContentLoaded', () => {
    // Optional: Add simple parallax effect to the hero visual on mousemove
    const visual = document.querySelector('.visual-subject');
    const wrapper = document.querySelector('.hero-wrapper');

    wrapper.addEventListener('mousemove', (e) => {
        const x = (window.innerWidth - e.pageX * 2) / 90;
        const y = (window.innerHeight - e.pageY * 2) / 90;
        
        // Combine mouse parallax with the CSS floating animation
        visual.style.transform = `translateX(${x}px) translateY(${y}px) rotate(-2deg)`;
    });

    wrapper.addEventListener('mouseleave', () => {
        visual.style.transform = `translateX(0) translateY(0) rotate(-2deg)`;
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
