def create_component(
    output_dir: str,
    title_text: str = "IT'S YOUR UNIVERSE,\nIT'S TIME TO SAVE IT",
    body_text: str = "The alliance is fighting to get rid of the evil empire. Join the resistance to create a better future for your children.",
    color_scheme: str = "dark",
    accent_color: str = "#d32f2f",
    width_px: int = 1440,
    height_px: int = 900,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the High-Converting Epic Sci-Fi Hero Section.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#0b0d14"
        bg_gradient = "radial-gradient(circle at center, #1a1e2d 0%, #050608 100%)"
        text_color = "#f4f4f6"
        text_muted = "#a0a5b5"
        surface_color = "rgba(255, 255, 255, 0.15)"
        planet_bg = "radial-gradient(circle at 70% 30%, #2a2d3e 10%, #0f111a 60%, #000 100%)"
    else:
        bg_color = "#f4f5f8"
        bg_gradient = "radial-gradient(circle at center, #ffffff 0%, #e0e4eb 100%)"
        text_color = "#0b0d14"
        text_muted = "#5a6072"
        surface_color = "rgba(0, 0, 0, 0.15)"
        planet_bg = "radial-gradient(circle at 70% 30%, #eef0f5 10%, #d1d6e0 60%, #a0a5b5 100%)"

    # === CSS ===
    css = f"""/* High-Converting Epic Hero Section */
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;500;600;800&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --bg-gradient: {bg_gradient};
    --text-color: {text_color};
    --text-muted: {text_muted};
    --accent-color: {accent_color};
    --surface-color: {surface_color};
    --planet-bg: {planet_bg};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: var(--bg-color);
    color: var(--text-color);
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

.hero-wrapper {{
    width: 100%;
    max-width: var(--width);
    min-height: var(--height);
    background: var(--bg-gradient);
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}}

/* Background Scenic Element */
.planet {{
    position: absolute;
    top: -15%;
    right: -10%;
    width: 65vw;
    height: 65vw;
    max-width: 900px;
    max-height: 900px;
    border-radius: 50%;
    background: var(--planet-bg);
    opacity: 0.9;
    z-index: 0;
    pointer-events: none;
}}

/* Header Navigation */
.header {{
    position: relative;
    z-index: 10;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2rem 4rem;
}}

.logo {{
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.2rem;
    letter-spacing: 2px;
    color: var(--accent-color);
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

.nav {{
    display: flex;
    gap: 2.5rem;
}}

.nav a {{
    color: var(--text-color);
    text-decoration: none;
    font-weight: 500;
    font-size: 0.95rem;
    transition: opacity 0.2s;
}}

.nav a:hover {{
    opacity: 0.7;
}}

/* Buttons */
.btn {{
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}}

.btn-ghost {{
    padding: 0.8rem 1.8rem;
    background: transparent;
    color: var(--text-color);
    border: 2px solid var(--surface-color);
}}

.btn-ghost:hover {{
    border-color: var(--text-color);
}}

.btn-primary {{
    background: var(--accent-color);
    color: #ffffff; /* Always white for contrast */
    border: none;
    padding: 1.2rem 2.8rem;
    font-size: 1.1rem;
    box-shadow: 0 10px 25px rgba(211, 47, 47, 0.3);
}}

.btn-primary:hover {{
    transform: translateY(-3px);
    box-shadow: 0 15px 35px rgba(211, 47, 47, 0.4);
    filter: brightness(1.1);
}}

/* Hero Layout */
.hero-body {{
    position: relative;
    z-index: 10;
    flex: 1;
    display: grid;
    grid-template-columns: 1fr 1fr;
    align-items: center;
    padding: 2rem 4rem 4rem 4rem;
    gap: 4rem;
}}

.hero-content {{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 2rem;
}}

.title {{
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(3.5rem, 6vw, 6rem);
    line-height: 0.95;
    letter-spacing: 1px;
    white-space: pre-line;
    color: var(--text-color);
    text-transform: uppercase;
}}

.description {{
    font-size: 1.15rem;
    line-height: 1.6;
    color: var(--text-muted);
    max-width: 480px;
}}

/* Micro-components: Trust Elements */
.social-proof {{
    display: flex;
    align-items: center;
    gap: 1rem;
    background: var(--surface-color);
    padding: 0.5rem 1rem 0.5rem 0.5rem;
    border-radius: 50px;
}}

.avatars {{
    display: flex;
}}

.avatar {{
    width: 32px;
    height: 32px;
    border-radius: 50%;
    border: 2px solid var(--bg-color);
    margin-left: -10px;
}}

.avatar:first-child {{
    margin-left: 0;
}}

.proof-text {{
    font-size: 0.85rem;
    color: var(--text-color);
    font-weight: 500;
}}

.as-seen-on {{
    margin-top: 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.8rem;
}}

.seen-text {{
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: var(--text-muted);
    font-weight: 600;
}}

.logos {{
    display: flex;
    align-items: center;
    gap: 1.5rem;
    opacity: 0.5;
    color: var(--text-color);
    transition: opacity 0.3s;
}}

.logos:hover {{
    opacity: 0.8;
}}

/* Hero Visual: CSS Generated Composition */
.hero-visual {{
    position: relative;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}}

.floating-orb {{
    width: 280px;
    height: 280px;
    border-radius: 50%;
    background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.9), rgba(255,255,255,0.0));
    box-shadow: 
        inset -15px -15px 40px rgba(0,0,0,0.6),
        0 0 50px var(--accent-color),
        0 0 100px rgba(255,255,255,0.15);
    animation: float 6s ease-in-out infinite;
    position: relative;
}}

.floating-orb::after {{
    content: '';
    position: absolute;
    top: 50%; left: 50%;
    width: 120%; height: 120%;
    transform: translate(-50%, -50%);
    border-radius: 50%;
    border: 1px solid var(--accent-color);
    opacity: 0.3;
    animation: pulse 3s ease-in-out infinite alternate;
}}

/* Animations */
@keyframes float {{
    0%   {{ transform: translateY(0px) rotate(0deg); }}
    50%  {{ transform: translateY(-30px) rotate(5deg); }}
    100% {{ transform: translateY(0px) rotate(0deg); }}
}}

@keyframes pulse {{
    0%   {{ transform: translate(-50%, -50%) scale(1); opacity: 0.1; }}
    100% {{ transform: translate(-50%, -50%) scale(1.1); opacity: 0.4; }}
}}

@keyframes slideUp {{
    from {{ opacity: 0; transform: translateY(30px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}

.hero-content > * {{
    animation: slideUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    opacity: 0;
}}

.hero-content > .title         {{ animation-delay: 0.1s; }}
.hero-content > .description   {{ animation-delay: 0.2s; }}
.hero-content > .btn-primary   {{ animation-delay: 0.3s; }}
.hero-content > .social-proof  {{ animation-delay: 0.4s; }}
.hero-content > .as-seen-on    {{ animation-delay: 0.5s; }}

/* Responsive Degradation */
@media (max-width: 968px) {{
    .hero-body {{
        grid-template-columns: 1fr;
        text-align: center;
        padding: 2rem;
    }}
    .hero-content {{
        align-items: center;
    }}
    .nav {{ display: none; }}
    .planet {{
        top: -20%; right: -20%;
        width: 100vw; height: 100vw;
    }}
    .hero-visual {{
        display: none;
    }}
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
    <div class="hero-wrapper">
        <!-- Deep Space Background Element -->
        <div class="planet"></div>
        
        <header class="header">
            <div class="logo">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2L2 22h20L12 2zm0 4.5l6.5 13h-13L12 6.5z"/>
                </svg>
                REBEL
            </div>
            <nav class="nav">
                <a href="#">Our Fleet</a>
                <a href="#">The Mission</a>
                <a href="#">Donations</a>
            </nav>
            <button class="btn btn-ghost">Member Login</button>
        </header>

        <main class="hero-body">
            <div class="hero-content">
                <h1 class="title">{title_text}</h1>
                <p class="description">{body_text}</p>
                
                <button class="btn btn-primary">Join Now For Free</button>
                
                <!-- Trust Elements -->
                <div class="social-proof">
                    <div class="avatars">
                        <div class="avatar" style="background: linear-gradient(135deg, #f09433, #dc2743);"></div>
                        <div class="avatar" style="background: linear-gradient(135deg, #1cb5e0, #000851);"></div>
                        <div class="avatar" style="background: linear-gradient(135deg, #00C9FF, #92FE9D);"></div>
                        <div class="avatar" style="background: linear-gradient(135deg, #FDBB2D, #22C1C3);"></div>
                    </div>
                    <span class="proof-text">Obi Wan and 4,000 others have already joined</span>
                </div>

                <div class="as-seen-on">
                    <span class="seen-text">As Seen On:</span>
                    <div class="logos">
                        <!-- Typographic Logo Placeholders -->
                        <span style="font-family: serif; font-weight: bold; font-size: 1.5rem;">CNN</span>
                        <span style="font-family: sans-serif; font-weight: 900; font-size: 1.4rem; letter-spacing: -1px;">FOX</span>
                        <span style="font-family: sans-serif; font-weight: bold; font-size: 1.2rem; border: 2px solid currentColor; padding: 2px 6px;">BBC</span>
                    </div>
                </div>
            </div>

            <!-- Foreground Visual Focal Point -->
            <div class="hero-visual">
                <div class="floating-orb"></div>
            </div>
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Optional: Add simple parallax effect to the planet on mousemove for extra depth
document.addEventListener('DOMContentLoaded', () => {
    const hero = document.querySelector('.hero-wrapper');
    const planet = document.querySelector('.planet');

    if (hero && planet) {
        hero.addEventListener('mousemove', (e) => {
            const x = (e.clientX / window.innerWidth - 0.5) * 20;
            const y = (e.clientY / window.innerHeight - 0.5) * 20;
            
            // Move opposite to cursor for parallax depth
            planet.style.transform = `translate(${-x}px, ${-y}px)`;
        });
    }
});
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
