def create_component(
    output_dir: str,
    title_text: str = "IT'S YOUR UNIVERSE, IT'S TIME TO SAVE IT",
    body_text: str = "The resistance is fighting to get rid of the evil empire. Join the alliance to create a better future for your children.",
    color_scheme: str = "dark",
    accent_color: str = "#E63946",
    width_px: int = 1440,
    height_px: int = 900,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the High-Converting Dark Theme Hero Section.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === CSS ===
    css = f"""/* High-Converting Dark Theme Hero Section */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500&family=Oswald:wght@600;700&display=swap');

:root {{
    --bg-base: #0B0C10;
    --text-main: #FFFFFF;
    --text-muted: #A9B1C2;
    --accent: {accent_color};
    --border-color: rgba(255, 255, 255, 0.1);
    --width: {width_px}px;
    --height: {height_px}px;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', sans-serif;
    background-color: var(--bg-base);
    color: var(--text-main);
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

.wrapper {{
    width: var(--width);
    height: var(--height);
    background-image: linear-gradient(to right, rgba(11, 12, 16, 0.95) 0%, rgba(11, 12, 16, 0.7) 50%, rgba(11, 12, 16, 0.3) 100%), url('https://images.unsplash.com/photo-1462331940025-496dfbfc7564?q=80&w=2000&auto=format&fit=crop');
    background-size: cover;
    background-position: center;
    position: relative;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}}

/* Navbar */
.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2rem 4rem;
    z-index: 10;
}}

.logo {{
    font-family: 'Oswald', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    text-transform: uppercase;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

.logo-icon {{
    width: 24px;
    height: 24px;
    background-color: var(--accent);
    mask: url('data:image/svg+xml;utf8,<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 2L2 22h20L12 2z"/></svg>') no-repeat center / contain;
    -webkit-mask: url('data:image/svg+xml;utf8,<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 2L2 22h20L12 2z"/></svg>') no-repeat center / contain;
}}

.nav-links {{
    display: flex;
    gap: 2rem;
    list-style: none;
}}

.nav-links a {{
    color: var(--text-main);
    text-decoration: none;
    font-size: 0.9rem;
    font-weight: 500;
    opacity: 0.8;
    transition: opacity 0.2s ease;
}}

.nav-links a:hover {{
    opacity: 1;
}}

/* Buttons */
.btn {{
    font-family: 'Oswald', sans-serif;
    text-transform: uppercase;
    text-decoration: none;
    padding: 0.8rem 2rem;
    font-size: 1rem;
    font-weight: 600;
    letter-spacing: 1px;
    border-radius: 2px;
    transition: all 0.3s ease;
    cursor: pointer;
    display: inline-block;
}}

.btn-primary {{
    background-color: var(--accent);
    color: white;
    border: 2px solid var(--accent);
    box-shadow: 0 4px 14px rgba(230, 57, 70, 0.4);
}}

.btn-primary:hover {{
    background-color: transparent;
    box-shadow: 0 0 0 transparent;
}}

.btn-ghost {{
    background-color: transparent;
    color: white;
    border: 2px solid rgba(255, 255, 255, 0.3);
}}

.btn-ghost:hover {{
    border-color: white;
    background-color: rgba(255, 255, 255, 0.1);
}}

/* Hero Section */
.hero {{
    flex: 1;
    display: flex;
    align-items: center;
    padding: 0 4rem;
    position: relative;
    z-index: 5;
}}

.hero-content {{
    max-width: 600px;
}}

.hero h1 {{
    font-family: 'Oswald', sans-serif;
    font-size: 4.5rem;
    line-height: 1.1;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
    text-wrap: balance;
}}

.hero p {{
    font-size: 1.1rem;
    color: var(--text-muted);
    line-height: 1.6;
    margin-bottom: 2.5rem;
    max-width: 85%;
}}

/* Avatar Social Proof */
.social-proof-micro {{
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-top: 2rem;
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
    font-size: 0.85rem;
    color: var(--text-muted);
}}

.proof-text strong {{
    color: var(--text-main);
}}

/* Hero Visual Composition (CSS Generated) */
.hero-visual {{
    position: absolute;
    right: 5%;
    top: 20%;
    width: 600px;
    height: 600px;
    pointer-events: none;
}}

.planet {{
    position: absolute;
    top: 50px;
    right: 50px;
    width: 400px;
    height: 400px;
    border-radius: 50%;
    background: radial-gradient(circle at 30% 30%, #3a3f58, #0B0C10);
    box-shadow: inset -30px -30px 60px rgba(0,0,0,0.8), 0 0 40px rgba(255,255,255,0.05);
}}

.ship-placeholder {{
    position: absolute;
    top: 200px;
    left: -50px;
    width: 350px;
    height: 150px;
    background: linear-gradient(135deg, rgba(255,255,255,0.8), rgba(255,255,255,0.2));
    clip-path: polygon(0 40%, 80% 0, 100% 50%, 80% 100%, 0 60%, 20% 50%);
    transform: rotate(-15deg);
    filter: drop-shadow(20px 20px 20px rgba(0,0,0,0.5));
    animation: float 6s ease-in-out infinite;
}}

.ship-engine {{
    position: absolute;
    right: -10px;
    top: 50%;
    transform: translateY(-50%);
    width: 40px;
    height: 20px;
    background: #00ffff;
    border-radius: 50%;
    filter: blur(10px);
}}

@keyframes float {{
    0%, 100% {{ transform: translateY(0) rotate(-15deg); }}
    50% {{ transform: translateY(-20px) rotate(-12deg); }}
}}

/* Bottom Logo Banner */
.social-proof-banner {{
    border-top: 1px solid var(--border-color);
    padding: 1.5rem 4rem;
    display: flex;
    align-items: center;
    gap: 2rem;
    background-color: rgba(11, 12, 16, 0.4);
    backdrop-filter: blur(5px);
    z-index: 10;
}}

.banner-label {{
    font-size: 0.8rem;
    text-transform: uppercase;
    color: var(--text-muted);
    font-weight: 600;
    letter-spacing: 1px;
}}

.logo-group {{
    display: flex;
    gap: 3rem;
    align-items: center;
}}

.press-logo {{
    height: 24px;
    fill: var(--text-muted);
    opacity: 0.5;
    transition: all 0.3s ease;
    cursor: pointer;
}}

.press-logo:hover {{
    opacity: 1;
    fill: var(--text-main);
}}

/* Responsive adjustments */
@media (max-width: 1024px) {{
    .hero h1 {{ font-size: 3.5rem; }}
    .hero-visual {{ display: none; }}
    .wrapper {{ background-image: linear-gradient(to right, rgba(11, 12, 16, 0.95) 0%, rgba(11, 12, 16, 0.8) 100%), url('https://images.unsplash.com/photo-1462331940025-496dfbfc7564?q=80&w=2000&auto=format&fit=crop'); }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hero Section</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="wrapper">
        <nav class="navbar">
            <div class="logo">
                <div class="logo-icon"></div>
                Vanguard
            </div>
            <ul class="nav-links">
                <li><a href="#">Our Fleet</a></li>
                <li><a href="#">The Mission</a></li>
                <li><a href="#">Manifesto</a></li>
            </ul>
            <a href="#" class="btn btn-ghost">Sign In</a>
        </nav>

        <main class="hero">
            <div class="hero-content">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
                <a href="#" class="btn btn-primary">Join Now For Free</a>
                
                <div class="social-proof-micro">
                    <div class="avatar-stack">
                        <img src="https://i.pravatar.cc/100?img=11" alt="Member" class="avatar">
                        <img src="https://i.pravatar.cc/100?img=12" alt="Member" class="avatar">
                        <img src="https://i.pravatar.cc/100?img=33" alt="Member" class="avatar">
                        <img src="https://i.pravatar.cc/100?img=44" alt="Member" class="avatar">
                    </div>
                    <div class="proof-text">
                        <strong>Commander Rey</strong> and 4,000 others<br>have already enlisted.
                    </div>
                </div>
            </div>

            <div class="hero-visual">
                <div class="planet"></div>
                <div class="ship-placeholder">
                    <div class="ship-engine"></div>
                </div>
            </div>
        </main>

        <section class="social-proof-banner">
            <span class="banner-label">Intercepted On:</span>
            <div class="logo-group">
                <!-- Generic SVG logos simulating media outlets -->
                <svg class="press-logo" viewBox="0 0 100 30" xmlns="http://www.w3.org/2000/svg"><path d="M10,5 h20 v20 h-20 z M40,5 h10 l10,20 h-10 z M70,5 h20 v5 h-15 v2 h10 v5 h-10 v3 h15 v5 h-20 z"/></svg>
                <svg class="press-logo" viewBox="0 0 100 30" xmlns="http://www.w3.org/2000/svg"><circle cx="15" cy="15" r="10"/><path d="M35,5 h10 v20 h-10 z M55,5 h20 v5 h-15 v2 h10 v5 h-10 v3 h15 v5 h-20 z"/></svg>
                <svg class="press-logo" viewBox="0 0 100 30" xmlns="http://www.w3.org/2000/svg"><path d="M10,25 l10,-20 l10,20 h-5 l-5,-10 l-5,10 z M40,5 h10 q10,0 10,10 q0,10 -10,10 h-10 z m5,5 v10 h5 q5,0 5,-5 q0,-5 -5,-5 z"/></svg>
                <svg class="press-logo" viewBox="0 0 100 30" xmlns="http://www.w3.org/2000/svg"><path d="M10,15 q0,-10 10,-10 t10,10 t-10,10 t-10,-10 M40,5 h5 v20 h-5 z M60,5 h20 v5 h-15 v2 h10 v5 h-10 v3 h15 v5 h-20 z"/></svg>
            </div>
        </section>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Interactive behavior for the Hero Section
document.addEventListener('DOMContentLoaded', () => {{
    // Optional: Add simple parallax effect to the visual elements based on mouse movement
    const visualGroup = document.querySelector('.hero-visual');
    const ship = document.querySelector('.ship-placeholder');
    const planet = document.querySelector('.planet');

    if(visualGroup && ship && planet) {{
        document.addEventListener('mousemove', (e) => {{
            const xAxis = (window.innerWidth / 2 - e.pageX) / 50;
            const yAxis = (window.innerHeight / 2 - e.pageY) / 50;

            // Move foreground elements more than background elements
            ship.style.transform = `rotate(-15deg) translate(${{xAxis}}px, ${{yAxis}}px)`;
            planet.style.transform = `translate(${{xAxis / 3}}px, ${{yAxis / 3}}px)`;
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
