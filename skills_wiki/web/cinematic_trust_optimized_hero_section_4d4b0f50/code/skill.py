def create_component(
    output_dir: str,
    title_text: str = "IT'S YOUR UNIVERSE, IT'S TIME TO SAVE IT.",
    body_text: str = "The Rebel alliance is fighting to get rid of the evil empire. Join the resistance to create a better future for your children.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#E50914",     # Cinematic Red
    width_px: int = 1440,
    height_px: int = 900,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Cinematic Trust-Optimized Hero.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0B0C10"
        text_color = "#FFFFFF"
        text_muted = "#A0AAB2"
        surface_color = "rgba(11, 12, 16, 0.6)"
        trust_bar_bg = "rgba(11, 12, 16, 0.4)"
        bg_image = "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?auto=format&fit=crop&w=2048&q=80" # Space nebula
        border_color = "rgba(255, 255, 255, 0.15)"
        logo_filter = "brightness(0) invert(1)" # Make logos white
    else:
        bg_color = "#F0F2F5"
        text_color = "#111827"
        text_muted = "#4B5563"
        surface_color = "rgba(255, 255, 255, 0.7)"
        trust_bar_bg = "rgba(255, 255, 255, 0.6)"
        bg_image = "https://images.unsplash.com/photo-1557683316-973673baf926?auto=format&fit=crop&w=2048&q=80" # Light abstract
        border_color = "rgba(0, 0, 0, 0.15)"
        logo_filter = "brightness(0)" # Make logos black

    # === CSS ===
    css = f"""/* Cinematic Trust-Optimized Hero */
:root {{
    --bg-color: {bg_color};
    --text-primary: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --surface: {surface_color};
    --trust-bg: {trust_bar_bg};
    --border: {border_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-primary);
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}}

.hero-wrapper {{
    width: var(--width);
    height: var(--height);
    position: relative;
    overflow: hidden;
    background-image: url('{bg_image}');
    background-size: cover;
    background-position: center;
    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
}}

.hero-overlay {{
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg, var(--bg-color) 0%, var(--surface) 50%, transparent 100%);
    z-index: 1;
}}

.hero-content-area {{
    position: relative;
    z-index: 2;
    height: 100%;
    display: flex;
    flex-direction: column;
    padding: 0 4rem;
}}

/* Navigation */
.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2rem 0;
}}

.logo {{
    font-family: 'Oswald', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

.nav-links {{
    display: flex;
    gap: 2.5rem;
    list-style: none;
}}

.nav-links a {{
    color: var(--text-primary);
    text-decoration: none;
    font-weight: 500;
    font-size: 0.95rem;
    transition: opacity 0.3s;
}}

.nav-links a:hover {{
    opacity: 0.7;
}}

/* Buttons */
.btn {{
    padding: 0.8rem 1.8rem;
    font-family: 'Oswald', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    cursor: pointer;
    border-radius: 4px;
    transition: all 0.3s ease;
}}

.btn-ghost {{
    background: transparent;
    color: var(--text-primary);
    border: 2px solid var(--border);
}}

.btn-ghost:hover {{
    background: var(--text-primary);
    color: var(--bg-color);
}}

.btn-primary {{
    background: var(--accent);
    color: #fff;
    border: 2px solid var(--accent);
    padding: 1.2rem 2.5rem;
    font-size: 1.2rem;
    box-shadow: 0 10px 20px rgba(229, 9, 20, 0.3);
}}

.btn-primary:hover {{
    transform: translateY(-2px);
    box-shadow: 0 15px 25px rgba(229, 9, 20, 0.4);
}}

/* Main Hero Text */
.hero-main {{
    margin-top: auto;
    margin-bottom: auto;
    max-width: 600px;
}}

.hero-main h1 {{
    font-family: 'Oswald', sans-serif;
    font-size: 4.5rem;
    line-height: 1.1;
    margin-bottom: 1.5rem;
    text-transform: uppercase;
}}

.hero-main p {{
    font-size: 1.15rem;
    line-height: 1.6;
    color: var(--text-muted);
    margin-bottom: 2.5rem;
}}

/* Conversion / Social Proof Area */
.cta-group {{
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}}

.social-proof {{
    display: flex;
    align-items: center;
    gap: 1rem;
}}

.avatars {{
    display: flex;
}}

.avatars img {{
    width: 36px;
    height: 36px;
    border-radius: 50%;
    border: 2px solid var(--bg-color);
    margin-left: -12px;
    object-fit: cover;
}}

.avatars img:first-child {{
    margin-left: 0;
}}

.social-text {{
    font-size: 0.9rem;
    color: var(--text-muted);
}}

.social-text strong {{
    color: var(--text-primary);
}}

/* Trust Bar */
.trust-bar {{
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    background: var(--trust-bg);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-top: 1px solid var(--border);
    padding: 1.5rem 4rem;
    display: flex;
    align-items: center;
    gap: 2rem;
    z-index: 10;
}}

.trust-label {{
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--text-muted);
    font-weight: 600;
}}

.trust-logos {{
    display: flex;
    gap: 3rem;
    align-items: center;
    font-size: 1.8rem;
    color: var(--text-primary);
    opacity: 0.6;
}}

.trust-logos i {{
    transition: opacity 0.3s;
}}

.trust-logos i:hover {{
    opacity: 1;
}}

/* Animations */
.anim-up {{
    opacity: 0;
    transform: translateY(30px);
    animation: fadeUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}}

@keyframes fadeUp {{
    to {{ opacity: 1; transform: translateY(0); }}
}}

.delay-1 {{ animation-delay: 0.1s; }}
.delay-2 {{ animation-delay: 0.3s; }}
.delay-3 {{ animation-delay: 0.5s; }}
.delay-4 {{ animation-delay: 0.7s; }}
.delay-5 {{ animation-delay: 0.9s; }}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hero Component</title>
    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Oswald:wght@600;700&display=swap" rel="stylesheet">
    <!-- Icons for Trust Logos -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="hero-wrapper">
        <div class="hero-overlay"></div>
        
        <div class="hero-content-area">
            <!-- Navigation -->
            <nav class="navbar anim-up delay-1">
                <div class="logo">
                    <i class="fa-solid fa-meteor" style="color: var(--accent);"></i>
                    REBEL ALLIANCE
                </div>
                <ul class="nav-links">
                    <li><a href="#">Our Ships</a></li>
                    <li><a href="#">Mission</a></li>
                    <li><a href="#">Donations</a></li>
                </ul>
                <button class="btn btn-ghost">JOIN NOW</button>
            </nav>

            <!-- Main Content -->
            <main class="hero-main">
                <h1 class="anim-up delay-2">{title_text}</h1>
                <p class="anim-up delay-3">{body_text}</p>
                
                <div class="cta-group anim-up delay-4">
                    <button class="btn btn-primary">JOIN NOW FOR FREE</button>
                    
                    <div class="social-proof">
                        <div class="avatars">
                            <img src="https://i.pravatar.cc/100?img=11" alt="User 1">
                            <img src="https://i.pravatar.cc/100?img=12" alt="User 2">
                            <img src="https://i.pravatar.cc/100?img=33" alt="User 3">
                            <img src="https://i.pravatar.cc/100?img=68" alt="User 4">
                        </div>
                        <span class="social-text"><strong>Obi Wan</strong> and 4,000 others have already joined</span>
                    </div>
                </div>
            </main>
        </div>

        <!-- Trust Bar -->
        <div class="trust-bar anim-up delay-5">
            <span class="trust-label">As Seen On:</span>
            <div class="trust-logos">
                <i class="fa-brands fa-hacker-news"></i>
                <i class="fa-brands fa-reddit-alien"></i>
                <i class="fa-brands fa-discord"></i>
                <i class="fa-brands fa-twitch"></i>
            </div>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Interactivity and dynamic effects
document.addEventListener('DOMContentLoaded', () => {
    const heroWrapper = document.querySelector('.hero-wrapper');
    
    // Optional: Add a subtle parallax effect to the background on mouse move
    heroWrapper.addEventListener('mousemove', (e) => {
        const x = (e.clientX / window.innerWidth - 0.5) * 15;
        const y = (e.clientY / window.innerHeight - 0.5) * 15;
        
        // Slightly shift the background image for a cinematic depth effect
        heroWrapper.style.backgroundPosition = `calc(50% + ${x}px) calc(50% + ${y}px)`;
    });

    // Reset background position on mouse leave
    heroWrapper.addEventListener('mouseleave', () => {
        heroWrapper.style.backgroundPosition = 'center';
    });
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
