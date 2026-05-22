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
    Create a web component reproducing the Immersive Dark-Theme Hero with Social Proof.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#050508"
        bg_gradient = "radial-gradient(circle at 70% 30%, #1a1a2e 0%, #050508 60%)"
        text_primary = "#ffffff"
        text_secondary = "rgba(255, 255, 255, 0.7)"
        border_color = "rgba(255, 255, 255, 0.1)"
    else:
        bg_color = "#f4f4f5"
        bg_gradient = "radial-gradient(circle at 70% 30%, #ffffff 0%, #e2e8f0 80%)"
        text_primary = "#0f172a"
        text_secondary = "rgba(15, 23, 42, 0.7)"
        border_color = "rgba(0, 0, 0, 0.1)"

    # === CSS ===
    css = f"""/* Immersive Hero Component */
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;700;800&family=Inter:wght@400;500&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --bg-grad: {bg_gradient};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --accent: {accent_color};
    --border: {border_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', sans-serif;
    background-color: var(--bg);
    background-image: var(--bg-grad);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow-x: hidden;
}}

/* Simulated Stars using multiple box-shadows (for dark mode) */
.stars {{
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    width: 100%; height: 100%;
    z-index: 0;
    pointer-events: none;
    background: transparent;
    opacity: {1 if color_scheme == "dark" else 0};
}}
.stars::after {{
    content: "";
    position: absolute;
    width: 2px; height: 2px;
    background: transparent;
    box-shadow: 
        10vw 20vh #fff, 30vw 80vh #fff, 50vw 40vh #fff, 70vw 90vh #fff, 90vw 10vh #fff,
        20vw 60vh #fff, 40vw 10vh #fff, 60vw 70vh #fff, 80vw 30vh #fff, 95vw 50vh #fff,
        5vw 5vh #fff, 15vw 95vh #fff, 25vw 25vh #fff, 85vw 85vh #fff, 45vw 45vh #fff;
    opacity: 0.3;
}}

.container {{
    width: 100%;
    max-width: var(--width);
    min-height: var(--height);
    margin: 0 auto;
    position: relative;
    z-index: 1;
    display: flex;
    flex-direction: column;
    padding: 2rem 4rem;
}}

/* HEADER */
header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 4rem;
    z-index: 10;
}}

.logo {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-family: 'Montserrat', sans-serif;
    font-weight: 800;
    font-size: 1.5rem;
    letter-spacing: -0.02em;
}}

.logo-icon {{
    width: 32px;
    height: 32px;
    background: var(--accent);
    clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
}}

nav {{
    display: flex;
    gap: 2.5rem;
}}

nav a {{
    color: var(--text-primary);
    text-decoration: none;
    font-size: 0.875rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    transition: color 0.3s ease;
}}

nav a:hover {{
    color: var(--accent);
}}

/* HERO SECTION */
.hero {{
    display: grid;
    grid-template-columns: 1.2fr 0.8fr;
    align-items: center;
    gap: 4rem;
    flex: 1;
    position: relative;
}}

.hero-content {{
    display: flex;
    flex-direction: column;
    gap: 2rem;
    z-index: 10;
}}

.headline {{
    font-family: 'Montserrat', sans-serif;
    font-weight: 800;
    font-size: clamp(3rem, 5vw, 4.5rem);
    line-height: 1.05;
    letter-spacing: -0.03em;
    color: var(--text-primary);
}}

.body-text {{
    font-size: 1.125rem;
    line-height: 1.6;
    color: var(--text-secondary);
    max-width: 500px;
}}

.cta-group {{
    display: flex;
    gap: 1rem;
    align-items: center;
}}

.btn {{
    padding: 1rem 2rem;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 0.95rem;
    text-decoration: none;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    border-radius: 4px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
}}

.btn-primary {{
    background-color: var(--accent);
    color: #ffffff;
    border: 2px solid var(--accent);
    box-shadow: 0 4px 14px rgba(0,0,0,0.25);
}}

.btn-primary:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(230, 36, 41, 0.4);
}}

.btn-outline {{
    background-color: transparent;
    color: var(--text-primary);
    border: 2px solid var(--border);
}}

.btn-outline:hover {{
    border-color: var(--text-primary);
    background-color: rgba(255,255,255,0.05);
}}

/* HERO VISUAL (CSS Graphic to mimic Planet & Ship depth) */
.hero-visual {{
    position: relative;
    width: 100%;
    height: 100%;
    min-height: 500px;
    z-index: 5;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.planet {{
    position: absolute;
    width: 350px;
    height: 350px;
    border-radius: 50%;
    background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.1) 0%, rgba(0,0,0,0.8) 90%);
    box-shadow: inset -20px -20px 40px rgba(0,0,0,0.5), 0 0 60px rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.05);
    right: -10%;
}}

.spaceship {{
    position: absolute;
    width: 180px;
    height: 60px;
    background: linear-gradient(90deg, var(--accent) 0%, #ffffff 100%);
    clip-path: polygon(0 40%, 80% 40%, 100% 50%, 80% 60%, 0 60%, 15% 50%);
    top: 55%;
    left: 10%;
    transform: rotate(-15deg);
    filter: drop-shadow(0 10px 20px rgba(0,0,0,0.5));
    animation: float 6s ease-in-out infinite;
}}

.spaceship::after {{
    content: '';
    position: absolute;
    left: -20px; top: 40%; height: 20%; width: 40px;
    background: cyan;
    filter: blur(10px);
}}

@keyframes float {{
    0%, 100% {{ transform: rotate(-15deg) translateY(0); }}
    50% {{ transform: rotate(-15deg) translateY(-20px); }}
}}

/* SOCIAL PROOF / TRUST BAR */
.social-proof {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 4rem;
    padding-top: 2rem;
    border-top: 1px solid var(--border);
    z-index: 10;
    flex-wrap: wrap;
    gap: 2rem;
}}

.users-joined {{
    display: flex;
    align-items: center;
    gap: 1rem;
}}

.avatars {{
    display: flex;
}}

.avatar {{
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: 3px solid var(--bg);
    margin-left: -12px;
    background-size: cover;
    background-position: center;
    background-color: #333;
}}

.avatar:first-child {{ margin-left: 0; }}

.proof-text {{
    font-size: 0.875rem;
    color: var(--text-secondary);
    font-weight: 500;
}}

.proof-text strong {{
    color: var(--text-primary);
}}

.featured-in {{
    display: flex;
    align-items: center;
    gap: 1.5rem;
}}

.featured-label {{
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-secondary);
}}

.logos {{
    display: flex;
    gap: 1.5rem;
    opacity: 0.5;
}}

.logo-placeholder {{
    font-family: 'Montserrat', sans-serif;
    font-weight: 800;
    font-size: 1.25rem;
    color: var(--text-primary);
    text-transform: uppercase;
}}

/* ANIMATIONS */
.animate-up {{
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 0.8s ease, transform 0.8s cubic-bezier(0.2, 0.8, 0.2, 1);
}}

.animate-up.visible {{
    opacity: 1;
    transform: translateY(0);
}}

.delay-1 {{ transition-delay: 0.1s; }}
.delay-2 {{ transition-delay: 0.2s; }}
.delay-3 {{ transition-delay: 0.3s; }}
.delay-4 {{ transition-delay: 0.4s; }}

/* RESPONSIVE */
@media (max-width: 992px) {{
    .hero {{ grid-template-columns: 1fr; text-align: center; gap: 2rem; }}
    .hero-content {{ align-items: center; }}
    .hero-visual {{ display: none; /* Hide complex graphic on small screens to save space */ }}
    header {{ flex-direction: column; gap: 1.5rem; padding-bottom: 2rem; }}
    .social-proof {{ flex-direction: column; justify-content: center; text-align: center; }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="stars"></div>
    
    <div class="container">
        <header class="animate-up">
            <div class="logo">
                <div class="logo-icon"></div>
                Rebel Alliance
            </div>
            <nav>
                <a href="#">Our Ships</a>
                <a href="#">Mission</a>
                <a href="#">Donations</a>
            </nav>
            <a href="#" class="btn btn-outline">Join Now</a>
        </header>

        <section class="hero">
            <div class="hero-content">
                <h1 class="headline animate-up delay-1">{title_text}</h1>
                <p class="body-text animate-up delay-2">{body_text}</p>
                <div class="cta-group animate-up delay-3">
                    <a href="#" class="btn btn-primary">Join Now For Free</a>
                </div>
            </div>

            <div class="hero-visual animate-up delay-2">
                <div class="planet"></div>
                <div class="spaceship"></div>
            </div>
        </section>

        <div class="social-proof animate-up delay-4">
            <div class="users-joined">
                <div class="avatars">
                    <div class="avatar" style="background-image: url('https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=100&q=80')"></div>
                    <div class="avatar" style="background-image: url('https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=100&q=80')"></div>
                    <div class="avatar" style="background-image: url('https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=100&q=80')"></div>
                </div>
                <div class="proof-text">
                    <strong>Obi Wan</strong> and <strong>4,000 others</strong> have already joined
                </div>
            </div>

            <div class="featured-in">
                <span class="featured-label">As Seen On</span>
                <div class="logos">
                    <span class="logo-placeholder">IGN</span>
                    <span class="logo-placeholder">FOX</span>
                    <span class="logo-placeholder">NBC</span>
                </div>
            </div>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Immersive Hero Component - Animations
document.addEventListener('DOMContentLoaded', () => {{
    // Trigger entrance animations
    const animatedElements = document.querySelectorAll('.animate-up');
    
    // Small timeout to ensure DOM is fully ready and CSS is parsed
    setTimeout(() => {{
        animatedElements.forEach(el => {{
            el.classList.add('visible');
        }});
    }}, 50);

    // Subtle parallax effect on hero visual
    const heroVisual = document.querySelector('.hero-visual');
    if (heroVisual) {{
        window.addEventListener('mousemove', (e) => {{
            const x = (e.clientX / window.innerWidth - 0.5) * 20;
            const y = (e.clientY / window.innerHeight - 0.5) * 20;
            heroVisual.style.transform = `translate(${{x}}px, ${{y}}px)`;
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
