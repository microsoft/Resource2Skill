def create_component(
    output_dir: str,
    title_text: str = "It's your universe, it's time to save it",
    body_text: str = "The alliance is fighting to get rid of the evil empire. Join the resistance to create a better future for your children.",
    color_scheme: str = "dark",
    accent_color: str = "#d32f2f", # Crimson Red
    width_px: int = 1440,
    height_px: int = 900,
    **kwargs,
) -> dict:
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derived colors
    bg_color = "#08090d" if color_scheme == "dark" else "#f0f2f5"
    text_color = "#ffffff" if color_scheme == "dark" else "#111827"
    text_muted = "rgba(255,255,255,0.7)" if color_scheme == "dark" else "rgba(0,0,0,0.6)"
    nav_bg = "rgba(8, 9, 13, 0.8)" if color_scheme == "dark" else "rgba(255, 255, 255, 0.8)"
    
    # Placeholder Images for Cinematic Feel
    bg_image = "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?auto=format&fit=crop&w=2048&q=80" # Space nebula
    focal_image = "https://images.unsplash.com/photo-1614729939124-032f0b56c9ce?auto=format&fit=crop&w=800&q=80&transparent=1" # Abstract planet/object (using generic space obj as placeholder for spaceship)
    
    css = f"""/* Cinematic Dark Hero — generated component */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Oswald:wght@500;700&display=swap');

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
    --nav-bg: {nav_bg};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', sans-serif;
    background-color: var(--bg-base);
    color: var(--text-main);
    display: flex;
    justify-content: center;
    min-height: 100vh;
    overflow-x: hidden;
}}

.hero-wrapper {{
    width: 100%;
    max-width: var(--width);
    min-height: var(--height);
    position: relative;
    display: flex;
    flex-direction: column;
    /* Cinematic background blend */
    background-image: linear-gradient(to right, rgba(8,9,13,0.95) 0%, rgba(8,9,13,0.4) 100%), url('{bg_image}');
    background-size: cover;
    background-position: center;
}}

/* Navigation */
.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2rem 5%;
    background: var(--nav-bg);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid rgba(255,255,255,0.05);
}}

.logo {{
    font-family: 'Oswald', sans-serif;
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
    background: var(--accent);
    border-radius: 50%;
}}

.nav-links {{
    display: flex;
    gap: 2rem;
    list-style: none;
}}

.nav-links a {{
    color: var(--text-main);
    text-decoration: none;
    font-size: 0.95rem;
    font-weight: 500;
    transition: color 0.3s ease;
}}

.nav-links a:hover {{ color: var(--accent); }}

.btn {{
    padding: 0.75rem 1.5rem;
    border-radius: 4px;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 0.95rem;
    cursor: pointer;
    transition: all 0.3s ease;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

.btn-ghost {{
    background: transparent;
    color: var(--text-main);
    border: 1px solid rgba(255,255,255,0.3);
}}

.btn-ghost:hover {{
    border-color: var(--text-main);
    background: rgba(255,255,255,0.05);
}}

.btn-primary {{
    background: var(--accent);
    color: white;
    border: none;
    padding: 1rem 2rem;
    font-size: 1rem;
    box-shadow: 0 4px 15px rgba(211, 47, 47, 0.4);
}}

.btn-primary:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(211, 47, 47, 0.6);
}}

/* Main Content Area */
.hero-content {{
    flex: 1;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4rem;
    padding: 4rem 5%;
    align-items: center;
}}

.text-col {{
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    animation: fadeUp 1s ease-out forwards;
}}

.title {{
    font-family: 'Oswald', sans-serif;
    font-size: 4.5rem;
    font-weight: 700;
    line-height: 1.1;
    text-transform: uppercase;
}}

.body-text {{
    font-size: 1.125rem;
    line-height: 1.6;
    color: var(--text-muted);
    max-width: 90%;
}}

.cta-group {{
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-top: 1rem;
}}

.social-proof-users {{
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-top: 1rem;
}}

.avatars {{
    display: flex;
}}

.avatars img {{
    width: 32px;
    height: 32px;
    border-radius: 50%;
    border: 2px solid var(--bg-base);
    margin-left: -10px;
}}
.avatars img:first-child {{ margin-left: 0; }}

.social-proof-text {{
    font-size: 0.875rem;
    color: var(--text-muted);
}}

/* Image Column */
.image-col {{
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
}}

.floating-hero-img {{
    width: 100%;
    max-width: 600px;
    border-radius: 50%; /* Making placeholder circular to fit space theme better */
    box-shadow: 0 0 100px rgba(255,255,255,0.1);
    animation: float 6s ease-in-out infinite;
}}

/* Social Proof Footer */
.hero-footer {{
    padding: 2rem 5%;
    display: flex;
    align-items: center;
    gap: 2rem;
    border-top: 1px solid rgba(255,255,255,0.05);
    background: linear-gradient(to top, rgba(0,0,0,0.5), transparent);
}}

.footer-label {{
    font-size: 0.875rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1px;
    white-space: nowrap;
}}

.logos-container {{
    display: flex;
    gap: 3rem;
    opacity: 0.5;
    flex-wrap: wrap;
}}

.logos-container img {{
    height: 24px;
    filter: grayscale(100%) brightness(200%);
}}

/* Animations */
@keyframes float {{
    0% {{ transform: translateY(0px); }}
    50% {{ transform: translateY(-20px); }}
    100% {{ transform: translateY(0px); }}
}}

@keyframes fadeUp {{
    from {{ opacity: 0; transform: translateY(30px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

/* Responsive */
@media (max-width: 968px) {{
    .hero-content {{
        grid-template-columns: 1fr;
        text-align: center;
        gap: 2rem;
    }}
    .title {{ font-size: 3rem; }}
    .body-text {{ max-width: 100%; margin: 0 auto; }}
    .text-col {{ align-items: center; }}
    .social-proof-users {{ justify-content: center; }}
    .nav-links {{ display: none; }} /* Simple mobile handling */
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cinematic Hero</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="hero-wrapper">
        
        <header class="navbar">
            <div class="logo">
                <div class="logo-icon"></div>
                ALLIANCE
            </div>
            <ul class="nav-links">
                <li><a href="#">Our Fleet</a></li>
                <li><a href="#">Mission</a></li>
                <li><a href="#">Donations</a></li>
            </ul>
            <button class="btn btn-ghost">Sign In</button>
        </header>

        <main class="hero-content">
            <div class="text-col">
                <h1 class="title">{title_text}</h1>
                <p class="body-text">{body_text}</p>
                
                <div class="cta-group">
                    <div><button class="btn btn-primary">JOIN NOW FOR FREE</button></div>
                    
                    <div class="social-proof-users">
                        <div class="avatars">
                            <img src="https://i.pravatar.cc/100?img=11" alt="User">
                            <img src="https://i.pravatar.cc/100?img=33" alt="User">
                            <img src="https://i.pravatar.cc/100?img=12" alt="User">
                        </div>
                        <span class="social-proof-text"><strong>O. Kenobi</strong> and 4,000 others have already joined.</span>
                    </div>
                </div>
            </div>

            <div class="image-col">
                <!-- Using a placeholder space object to represent the cinematic foreground element -->
                <img src="{focal_image}" alt="Hero focal point" class="floating-hero-img">
            </div>
        </main>

        <footer class="hero-footer">
            <span class="footer-label">As Seen On:</span>
            <div class="logos-container">
                <!-- Placeholder generic logos for social proof -->
                <img src="https://upload.wikimedia.org/wikipedia/commons/e/e6/CNN_logo_-_white.png" alt="CNN">
                <img src="https://upload.wikimedia.org/wikipedia/commons/2/22/Fox_News_Channel_logo.png" alt="FOX">
                <img src="https://upload.wikimedia.org/wikipedia/commons/4/4b/NBC_logo_%28white%29.svg" alt="NBC">
            </div>
        </footer>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Parallax effect on mouse move to enhance the cinematic depth
document.addEventListener('DOMContentLoaded', () => {{
    const heroWrapper = document.querySelector('.hero-wrapper');
    const floatingImg = document.querySelector('.floating-hero-img');

    heroWrapper.addEventListener('mousemove', (e) => {{
        const xPos = (e.clientX / window.innerWidth - 0.5) * 20; // Max 20px movement
        const yPos = (e.clientY / window.innerHeight - 0.5) * 20;
        
        // Add subtle parallax opposite to mouse movement
        floatingImg.style.transform = `translate(${{-xPos}}px, ${{yPos}}px)`;
    }});

    heroWrapper.addEventListener('mouseleave', () => {{
        // Reset to CSS animation
        floatingImg.style.transform = '';
    }});
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
