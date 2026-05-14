def create_component(
    output_dir: str,
    title_text: str = "IT'S YOUR UNIVERSE, IT'S TIME TO SAVE IT",
    body_text: str = "The Rebel alliance is fighting to get rid of the evil empire, join the resistance to create a better future for your children.",
    color_scheme: str = "dark",
    accent_color: str = "#e62429",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_gradient = "radial-gradient(circle at 70% 30%, #1a1c29 0%, #050608 80%)"
        text_color = "#ffffff"
        text_muted = "#8a94a6"
        border_color = "rgba(255, 255, 255, 0.1)"
        avatar_border = "#050608"
    else:
        bg_gradient = "radial-gradient(circle at 70% 30%, #ffffff 0%, #eef1f6 80%)"
        text_color = "#111827"
        text_muted = "#6b7280"
        border_color = "rgba(0, 0, 0, 0.1)"
        avatar_border = "#eef1f6"

    css = f"""/* High-Converting Epic Hero generated component */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500&family=Montserrat:wght@800;900&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_gradient};
    --text-main: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --border: {border_color};
    --avatar-border: {avatar_border};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text-main);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    overflow-x: hidden;
    perspective: 1000px;
}}

/* Navbar */
.navbar {{
    width: 100%;
    max-width: 1400px;
    margin: 0 auto;
    padding: 2rem 5%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 100;
}}

.logo {{
    font-family: 'Montserrat', sans-serif;
    font-weight: 900;
    font-size: 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    text-transform: uppercase;
    letter-spacing: -0.5px;
}}

.logo-icon {{
    width: 32px;
    height: 32px;
    background-color: var(--accent);
    border-radius: 50%;
    position: relative;
}}
.logo-icon::after {{
    content: '';
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 12px; height: 12px;
    background-color: var(--text-main);
    clip-path: polygon(50% 0%, 100% 100%, 50% 75%, 0% 100%);
}}

.nav-links {{
    display: flex;
    gap: 2.5rem;
}}

.nav-links a {{
    color: var(--text-main);
    text-decoration: none;
    font-weight: 500;
    font-size: 0.95rem;
    transition: color 0.3s ease;
}}

.nav-links a:hover {{
    color: var(--accent);
}}

/* Buttons */
.btn {{
    padding: 0.8rem 1.75rem;
    font-family: 'Montserrat', sans-serif;
    font-weight: 800;
    text-transform: uppercase;
    text-decoration: none;
    font-size: 0.9rem;
    letter-spacing: 0.5px;
    border-radius: 4px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
}}

.btn-ghost {{
    background: transparent;
    border: 2px solid var(--text-main);
    color: var(--text-main);
}}

.btn-ghost:hover {{
    background: var(--text-main);
    color: var(--avatar-border);
}}

.btn-primary {{
    background: var(--accent);
    border: 2px solid var(--accent);
    color: #ffffff; /* Explicitly white for contrast on accent */
    padding: 1.2rem 2.5rem;
    font-size: 1.1rem;
    display: inline-block;
    box-shadow: 0 10px 20px -5px rgba(230, 36, 41, 0.4);
}}

.btn-primary:hover {{
    transform: translateY(-3px);
    box-shadow: 0 15px 25px -5px rgba(230, 36, 41, 0.6);
}}

/* Hero Section */
.hero {{
    flex: 1;
    display: flex;
    align-items: center;
    width: 100%;
    max-width: 1400px;
    margin: 0 auto;
    padding: 2rem 5% 4rem;
    position: relative;
    z-index: 10;
}}

.hero-content {{
    flex: 0 0 55%;
    max-width: 650px;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    animation: fadeUp 1s ease-out forwards;
}}

.hero-title {{
    font-family: 'Montserrat', sans-serif;
    font-weight: 900;
    font-size: clamp(3rem, 5vw, 4.5rem);
    line-height: 1.05;
    text-transform: uppercase;
    letter-spacing: -1px;
}}

.hero-desc {{
    font-size: 1.15rem;
    line-height: 1.6;
    color: var(--text-muted);
    max-width: 90%;
    margin-bottom: 1rem;
}}

/* Social Proof Clustering */
.conversion-zone {{
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    margin-top: 1rem;
}}

.social-proof-avatars {{
    display: flex;
    align-items: center;
    gap: 1rem;
}}

.avatars {{
    display: flex;
}}

.avatars img {{
    width: 44px;
    height: 44px;
    border-radius: 50%;
    border: 3px solid var(--avatar-border);
    margin-left: -16px;
    object-fit: cover;
}}

.avatars img:first-child {{
    margin-left: 0;
}}

.proof-text {{
    font-size: 0.9rem;
    color: var(--text-muted);
    line-height: 1.4;
}}
.proof-text strong {{
    color: var(--text-main);
}}

.social-proof-logos {{
    margin-top: 2rem;
    padding-top: 2rem;
    border-top: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    gap: 1rem;
}}

.proof-label {{
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--text-muted);
}}

.logos-strip {{
    display: flex;
    gap: 2.5rem;
    align-items: center;
    flex-wrap: wrap;
}}

.logo-placeholder {{
    font-family: 'Montserrat', sans-serif;
    font-weight: 900;
    font-size: 1.4rem;
    color: var(--text-main);
    opacity: 0.4;
    filter: grayscale(100%);
    transition: opacity 0.3s ease;
    text-transform: uppercase;
}}
.logo-placeholder:hover {{
    opacity: 0.8;
}}

/* Hero Visual Background/Foreground */
.hero-visual {{
    flex: 0 0 45%;
    position: relative;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.hero-image-wrapper {{
    position: relative;
    width: 120%;
    right: -10%;
    animation: float 6s ease-in-out infinite;
    transform-style: preserve-3d;
    will-change: transform;
}}

/* Use a high-quality transparent PNG placeholder from Unsplash via remove.bg or similar, here simulated with a stylized element */
.hero-image-wrapper img {{
    width: 100%;
    height: auto;
    filter: drop-shadow(0 30px 40px rgba(0, 0, 0, 0.6));
    border-radius: 20px;
    /* Simulated 3D ship object using CSS fallback if image fails */
    background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(0,0,0,0.5));
    box-shadow: inset 0 0 0 1px rgba(255,255,255,0.2);
}}

/* Background Atmosphere */
.atmosphere {{
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    overflow: hidden;
    z-index: -1;
    pointer-events: none;
}}

.stars {{
    position: absolute;
    width: 200%; height: 200%;
    background-image: 
        radial-gradient(1px 1px at 20px 30px, #ffffff, rgba(0,0,0,0)),
        radial-gradient(1px 1px at 40px 70px, #ffffff, rgba(0,0,0,0)),
        radial-gradient(2px 2px at 90px 40px, #ffffff, rgba(0,0,0,0)),
        radial-gradient(1.5px 1.5px at 160px 120px, #ffffff, rgba(0,0,0,0));
    background-repeat: repeat;
    background-size: 200px 200px;
    opacity: 0.3;
    animation: starDrift 100s linear infinite;
}}

/* Animations */
@keyframes fadeUp {{
    from {{ opacity: 0; transform: translateY(30px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

@keyframes float {{
    0% {{ transform: translateY(0) rotateX(0deg) rotateY(0deg); }}
    50% {{ transform: translateY(-20px) rotateX(2deg) rotateY(-2deg); }}
    100% {{ transform: translateY(0) rotateX(0deg) rotateY(0deg); }}
}}

@keyframes starDrift {{
    from {{ transform: translate(0, 0); }}
    to {{ transform: translate(-50%, -50%); }}
}}

/* Responsive */
@media (max-width: 968px) {{
    .hero {{
        flex-direction: column;
        text-align: center;
        padding-top: 4rem;
    }}
    .hero-content {{
        flex: 1;
        max-width: 100%;
        align-items: center;
    }}
    .hero-desc {{ margin: 0 auto 1rem; }}
    .social-proof-avatars {{ justify-content: center; }}
    .logos-strip {{ justify-content: center; }}
    .hero-visual {{
        width: 100%;
        margin-top: 4rem;
    }}
    .hero-image-wrapper {{
        width: 90%;
        right: 0;
    }}
    .nav-links {{ display: none; }} /* Mobile menu toggle needed in prod */
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text.title()}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="atmosphere">
        <div class="stars"></div>
    </div>

    <nav class="navbar">
        <div class="logo">
            <div class="logo-icon"></div>
            <span>Rebel Alliance</span>
        </div>
        <div class="nav-links">
            <a href="#">Our Ships</a>
            <a href="#">Mission</a>
            <a href="#">Donations</a>
        </nav>
        <a href="#" class="btn btn-ghost">Join Now</a>
    </nav>

    <main class="hero">
        <div class="hero-content">
            <h1 class="hero-title">{title_text}</h1>
            <p class="hero-desc">{body_text}</p>
            
            <div class="conversion-zone">
                <div>
                    <a href="#" class="btn btn-primary">Join Now For Free</a>
                </div>
                
                <div class="social-proof-avatars">
                    <div class="avatars">
                        <!-- Pravatar placeholder images for social proof -->
                        <img src="https://i.pravatar.cc/150?u=a042581f4e29026704d" alt="User 1">
                        <img src="https://i.pravatar.cc/150?u=a042581f4e29026704e" alt="User 2">
                        <img src="https://i.pravatar.cc/150?u=a042581f4e29026704f" alt="User 3">
                        <img src="https://i.pravatar.cc/150?u=a042581f4e29026704a" alt="User 4">
                    </div>
                    <span class="proof-text"><strong>Obi Wan</strong> and 4,000 others<br>have already joined</span>
                </div>
            </div>

            <div class="social-proof-logos">
                <span class="proof-label">As Seen On</span>
                <div class="logos-strip">
                    <div class="logo-placeholder">NBC</div>
                    <div class="logo-placeholder">FOX</div>
                    <div class="logo-placeholder">The CW</div>
                    <div class="logo-placeholder">CBS</div>
                </div>
            </div>
        </div>

        <div class="hero-visual">
            <div class="hero-image-wrapper">
                <!-- Using a high-quality Unsplash image to represent the hero object -->
                <img src="https://images.unsplash.com/photo-1614730321146-b6fa6a46bcb4?q=80&w=1000&auto=format&fit=crop" alt="Hero Space Object">
            </div>
        </div>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Mouse parallax effect to enhance the immersive 3D space feel
document.addEventListener('DOMContentLoaded', () => {{
    const visualWrapper = document.querySelector('.hero-image-wrapper');
    const atmosphere = document.querySelector('.stars');
    
    // Only apply parallax on desktop devices where hover is a primary input
    if (window.matchMedia("(min-width: 968px)").matches) {{
        document.addEventListener('mousemove', (e) => {{
            const x = e.clientX / window.innerWidth;
            const y = e.clientY / window.innerHeight;
            
            // Move the foreground object slightly towards the mouse
            const moveX = (x - 0.5) * 40; 
            const moveY = (y - 0.5) * 40;
            
            // Move the background slightly away from the mouse
            const bgX = (x - 0.5) * -20;
            const bgY = (y - 0.5) * -20;

            // Apply transforms via requestAnimationFrame for smooth rendering
            requestAnimationFrame(() => {{
                visualWrapper.style.transform = `translate(${{moveX}}px, ${{moveY}}px) rotateX(${{(y - 0.5) * 5}}deg) rotateY(${{(x - 0.5) * -5}}deg)`;
                atmosphere.style.transform = `translate(${{bgX}}px, ${{bgY}}px)`;
            }});
        }});
        
        // Reset transforms when mouse leaves the window
        document.addEventListener('mouseleave', () => {{
            requestAnimationFrame(() => {{
                visualWrapper.style.transform = `translate(0px, 0px) rotateX(0deg) rotateY(0deg)`;
                atmosphere.style.transform = `translate(0px, 0px)`;
            }});
        }});
    }}
}});
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
