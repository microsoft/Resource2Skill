def create_component(
    output_dir: str,
    title_text: str = "It's your universe, it's time to save it",
    body_text: str = "The Alliance is fighting to restore freedom. Join the resistance to create a better future for the galaxy.",
    color_scheme: str = "dark",        
    accent_color: str = "#e63946",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Conversion-Optimized Hero Section.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#0B0D14"
        text_color = "#FFFFFF"
        text_muted = "rgba(255, 255, 255, 0.65)"
        border_color = "rgba(255, 255, 255, 0.1)"
        nav_hover = "rgba(255, 255, 255, 0.05)"
        ghost_border = "rgba(255, 255, 255, 0.3)"
    else:
        bg_color = "#F8F9FA"
        text_color = "#111827"
        text_muted = "rgba(17, 24, 39, 0.65)"
        border_color = "rgba(0, 0, 0, 0.1)"
        nav_hover = "rgba(0, 0, 0, 0.05)"
        ghost_border = "rgba(0, 0, 0, 0.2)"

    # CSS
    css = f"""/* Conversion-Optimized Hero Section */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --border: {border_color};
    --nav-hover: {nav_hover};
    --ghost-border: {ghost_border};
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    overflow-x: hidden;
    display: flex;
    flex-direction: column;
}}

/* Navbar */
nav {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem 5%;
    max-width: 1400px;
    margin: 0 auto;
    width: 100%;
}}

.logo {{
    font-weight: 800;
    font-size: 1.5rem;
    letter-spacing: -0.5px;
    display: flex;
    align-items: center;
    gap: 8px;
}}

.logo-icon {{
    width: 32px;
    height: 32px;
    background: var(--accent);
    border-radius: 8px;
    display: inline-block;
}}

.nav-links {{
    display: flex;
    gap: 2rem;
}}

.nav-links a {{
    color: var(--text);
    text-decoration: none;
    font-weight: 500;
    font-size: 0.95rem;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    transition: background 0.2s ease;
}}

.nav-links a:hover {{
    background: var(--nav-hover);
}}

/* Hero Section Layout */
.hero {{
    display: grid;
    grid-template-columns: 1.1fr 0.9fr;
    gap: 4rem;
    max-width: 1400px;
    margin: 0 auto;
    padding: 4rem 5%;
    flex: 1;
    align-items: center;
}}

/* Left Column Content */
.hero-content {{
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    animation: fadeUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    opacity: 0;
    transform: translateY(20px);
}}

.hero-title {{
    font-size: clamp(2.5rem, 5vw, 4.5rem);
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -0.02em;
}}

.hero-desc {{
    font-size: clamp(1rem, 1.5vw, 1.25rem);
    color: var(--text-muted);
    line-height: 1.6;
    max-width: 85%;
}}

/* CTA Area */
.cta-group {{
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    margin-top: 1rem;
}}

.buttons {{
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
}}

.btn {{
    padding: 1rem 2rem;
    border-radius: 8px;
    font-weight: 600;
    font-size: 1rem;
    cursor: pointer;
    text-decoration: none;
    transition: all 0.2s ease;
    display: inline-flex;
    align-items: center;
    justify-content: center;
}}

.btn-primary {{
    background-color: var(--accent);
    color: #ffffff;
    border: none;
    box-shadow: 0 4px 14px rgba(0,0,0,0.25);
}}

.btn-primary:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    filter: brightness(1.1);
}}

.btn-ghost {{
    background: transparent;
    color: var(--text);
    border: 2px solid var(--ghost-border);
}}

.btn-ghost:hover {{
    border-color: var(--text);
    background: var(--nav-hover);
}}

.microcopy {{
    font-size: 0.8rem;
    color: var(--text-muted);
    display: flex;
    align-items: center;
    gap: 6px;
}}
.microcopy svg {{ fill: currentColor; width: 14px; height: 14px; }}

/* Trust Signals: Social Proof */
.social-proof {{
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-top: 1.5rem;
}}

.avatars {{
    display: flex;
}}

.avatar {{
    width: 42px;
    height: 42px;
    border-radius: 50%;
    border: 3px solid var(--bg);
    object-fit: cover;
    margin-left: -14px;
    position: relative;
    background-color: #333;
}}

.avatar:first-child {{ margin-left: 0; z-index: 4; }}
.avatar:nth-child(2) {{ z-index: 3; }}
.avatar:nth-child(3) {{ z-index: 2; }}
.avatar:nth-child(4) {{ z-index: 1; }}

.social-text {{
    font-size: 0.875rem;
    color: var(--text-muted);
}}
.social-text strong {{ color: var(--text); font-weight: 600; }}

/* Trust Signals: As Seen On */
.as-seen-on {{
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--border);
    animation: fadeUp 1s cubic-bezier(0.16, 1, 0.3, 1) 0.3s forwards;
    opacity: 0;
}}

.as-seen-on-title {{
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-muted);
    margin-bottom: 1rem;
    font-weight: 600;
}}

.trust-logos {{
    display: flex;
    gap: 2.5rem;
    align-items: center;
    flex-wrap: wrap;
}}

.trust-logo {{
    font-weight: 800;
    font-size: 1.25rem;
    opacity: 0.4;
    filter: grayscale(100%);
    transition: all 0.3s ease;
    cursor: default;
    color: var(--text);
    display: flex;
    align-items: center;
    gap: 4px;
}}

.trust-logo:hover {{
    opacity: 1;
    filter: grayscale(0%);
}}

/* Right Column Image */
.hero-visual {{
    position: relative;
    width: 100%;
    height: 100%;
    min-height: 500px;
    animation: fadeIn 1.2s ease 0.2s forwards;
    opacity: 0;
}}

.hero-image {{
    width: 100%;
    height: 100%;
    object-fit: contain;
    position: absolute;
    top: 0;
    left: 0;
}}

/* Animations */
@keyframes fadeUp {{
    0% {{ opacity: 0; transform: translateY(30px); }}
    100% {{ opacity: 1; transform: translateY(0); }}
}}
@keyframes fadeIn {{
    0% {{ opacity: 0; }}
    100% {{ opacity: 1; }}
}}

/* Responsive */
@media (max-width: 968px) {{
    .hero {{
        grid-template-columns: 1fr;
        text-align: center;
        gap: 3rem;
        padding-top: 2rem;
    }}
    .hero-desc {{ max-width: 100%; margin: 0 auto; }}
    .buttons, .social-proof, .trust-logos {{ justify-content: center; }}
    .cta-group {{ align-items: center; }}
    .hero-visual {{ min-height: 350px; grid-row: 1; }}
    .nav-links {{ display: none; }} /* simplified for mobile */
}}
"""

    # HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <nav>
        <div class="logo">
            <span class="logo-icon"></span> Alliance
        </div>
        <div class="nav-links">
            <a href="#">Our Mission</a>
            <a href="#">Fleet</a>
            <a href="#">Donations</a>
            <a href="#" class="btn btn-primary" style="padding: 0.5rem 1rem; box-shadow:none;">Join Now</a>
        </div>
    </nav>

    <main class="hero">
        <div class="hero-content">
            <h1 class="hero-title">{title_text}</h1>
            <p class="hero-desc">{body_text}</p>
            
            <div class="cta-group">
                <div class="buttons">
                    <a href="#" class="btn btn-primary">JOIN NOW FOR FREE</a>
                    <a href="#" class="btn btn-ghost">Learn More</a>
                </div>
                <span class="microcopy">
                    <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>
                    No credit card required. Cancel anytime.
                </span>
            </div>

            <!-- Optimization: Social Proof -->
            <div class="social-proof">
                <div class="avatars">
                    <img src="https://i.pravatar.cc/100?img=68" alt="User 1" class="avatar">
                    <img src="https://i.pravatar.cc/100?img=33" alt="User 2" class="avatar">
                    <img src="https://i.pravatar.cc/100?img=47" alt="User 3" class="avatar">
                    <img src="https://i.pravatar.cc/100?img=12" alt="User 4" class="avatar">
                </div>
                <div class="social-text">
                    <strong>Obi Wan</strong> and <strong>4,000+ others</strong><br>have already joined the resistance.
                </div>
            </div>

            <!-- Optimization: Authority Badges -->
            <div class="as-seen-on">
                <div class="as-seen-on-title">Featured In</div>
                <div class="trust-logos">
                    <!-- Text-based mock logos for robust rendering -->
                    <div class="trust-logo" style="font-family: serif; font-style: italic;">The Times</div>
                    <div class="trust-logo">
                        <span style="background:var(--text); color:var(--bg); padding: 2px 6px; border-radius: 4px;">TECH</span> WIRE
                    </div>
                    <div class="trust-logo" style="letter-spacing: -2px; text-transform: lowercase; font-size: 1.5rem;">galactic</div>
                    <div class="trust-logo" style="border: 2px solid currentColor; padding: 2px 8px; font-weight: 800;">NN</div>
                </div>
            </div>
        </div>

        <div class="hero-visual">
            <!-- Using a high quality Unsplash space composite placeholder -->
            <img src="https://images.unsplash.com/photo-1462331940025-496dfbfc7564?auto=format&fit=crop&w=1000&q=80" alt="Space visual" class="hero-image" style="border-radius: 16px; object-fit: cover;">
        </div>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # JS
    js = """// Simple interaction logic for the hero section
document.addEventListener('DOMContentLoaded', () => {
    // Subtle parallax effect on the hero image based on mouse movement
    const visual = document.querySelector('.hero-visual');
    const hero = document.querySelector('.hero');

    if(visual && hero && window.innerWidth > 968) {
        hero.addEventListener('mousemove', (e) => {
            const xAxis = (window.innerWidth / 2 - e.pageX) / 50;
            const yAxis = (window.innerHeight / 2 - e.pageY) / 50;
            visual.style.transform = `translate(${xAxis}px, ${yAxis}px)`;
        });

        hero.addEventListener('mouseleave', () => {
            visual.style.transform = `translate(0px, 0px)`;
            visual.style.transition = `transform 0.5s ease`;
        });
        
        hero.addEventListener('mouseenter', () => {
            visual.style.transition = `none`;
        });
    }
});
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
        "files": files
    }
