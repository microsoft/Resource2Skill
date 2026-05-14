def create_component(
    output_dir: str,
    title_text: str = "IT'S YOUR UNIVERSE, IT'S TIME TO SAVE IT.",
    body_text: str = "The Rebel alliance is fighting to get rid of the evil empire. Join the resistance to create a better future for your children.",
    color_scheme: str = "dark",
    accent_color: str = "#e52424",
    width_px: int = 1440,
    height_px: int = 900,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Epic Cinematic Hero Section with Social Proof.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Enforce dark theme as it is core to the cinematic pattern shown
    bg_color = "#050814"
    text_color = "#ffffff"
    subtext_color = "#a0aab8"

    css = f"""/* Epic Cinematic Hero Section */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --subtext-color: {subtext_color};
    --accent-color: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

.hero-wrapper {{
    width: var(--width);
    height: var(--height);
    position: relative;
    overflow: hidden;
    /* Cinematic gradient overlay merging into a space background */
    background: linear-gradient(90deg, rgba(5,8,20,1) 0%, rgba(5,8,20,0.8) 40%, rgba(5,8,20,0.1) 100%), 
                url('https://images.unsplash.com/photo-1462331940025-496dfbfc7564?q=80&w=2000&auto=format&fit=crop') center/cover;
    display: flex;
    flex-direction: column;
}}

/* --- Navigation --- */
.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 32px 64px;
    z-index: 10;
}}

.logo {{
    font-family: 'Oswald', sans-serif;
    font-size: 24px;
    font-weight: 700;
    text-transform: uppercase;
    display: flex;
    align-items: center;
    gap: 12px;
}}

.logo-icon {{
    width: 32px;
    height: 32px;
    background-color: var(--accent-color);
    border-radius: 50%;
    display: inline-block;
}}

.nav-links {{
    display: flex;
    gap: 32px;
    list-style: none;
}}

.nav-links a {{
    color: var(--text-color);
    text-decoration: none;
    font-size: 14px;
    font-weight: 500;
    opacity: 0.8;
    transition: opacity 0.2s;
}}

.nav-links a:hover {{
    opacity: 1;
}}

.btn-ghost {{
    background: transparent;
    border: 2px solid rgba(255, 255, 255, 0.3);
    color: var(--text-color);
    padding: 10px 24px;
    font-family: 'Oswald', sans-serif;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    cursor: pointer;
    transition: all 0.3s ease;
}}

.btn-ghost:hover {{
    border-color: var(--text-color);
    background: rgba(255, 255, 255, 0.1);
}}

/* --- Main Hero Content --- */
.hero-content {{
    flex: 1;
    display: flex;
    align-items: center;
    padding: 0 64px;
    z-index: 10;
}}

.hero-text-col {{
    max-width: 600px;
    display: flex;
    flex-direction: column;
    gap: 24px;
}}

.hero-title {{
    font-family: 'Oswald', sans-serif;
    font-size: 64px;
    font-weight: 700;
    line-height: 1.1;
    text-transform: uppercase;
    letter-spacing: -1px;
}}

.hero-desc {{
    font-size: 18px;
    line-height: 1.6;
    color: var(--subtext-color);
    max-width: 500px;
}}

.btn-primary {{
    background-color: var(--accent-color);
    color: #fff;
    border: none;
    padding: 18px 40px;
    font-family: 'Oswald', sans-serif;
    font-size: 18px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    cursor: pointer;
    align-self: flex-start;
    transition: transform 0.2s ease, filter 0.2s ease;
    box-shadow: 0 10px 30px rgba(229, 36, 36, 0.3);
}}

.btn-primary:hover {{
    transform: translateY(-2px);
    filter: brightness(1.1);
}}

/* --- Social Proof: Avatar Pile --- */
.social-proof-avatars {{
    display: flex;
    align-items: center;
    gap: 16px;
    margin-top: 8px;
}}

.avatar-group {{
    display: flex;
}}

.avatar {{
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: 3px solid var(--bg-color);
    margin-left: -12px;
    object-fit: cover;
}}

.avatar:first-child {{
    margin-left: 0;
}}

.social-proof-text {{
    font-size: 14px;
    color: var(--subtext-color);
}}

.social-proof-text strong {{
    color: var(--text-color);
}}

/* --- Graphic Placeholder --- */
.hero-graphic-col {{
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
}}

.floating-element {{
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 70%);
    border-radius: 50%;
    animation: float 6s ease-in-out infinite;
}}

@keyframes float {{
    0% {{ transform: translateY(0px); }}
    50% {{ transform: translateY(-20px); }}
    100% {{ transform: translateY(0px); }}
}}

/* --- Footer Social Proof: Logos --- */
.social-proof-logos {{
    display: flex;
    align-items: center;
    gap: 40px;
    padding: 32px 64px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    background: linear-gradient(0deg, rgba(0,0,0,0.4) 0%, rgba(0,0,0,0) 100%);
    z-index: 10;
}}

.logos-label {{
    font-family: 'Oswald', sans-serif;
    text-transform: uppercase;
    color: var(--subtext-color);
    font-size: 14px;
    letter-spacing: 1px;
}}

.logo-strip {{
    display: flex;
    gap: 40px;
    opacity: 0.5;
}}

.mock-logo {{
    font-family: 'Oswald', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: var(--text-color);
    display: flex;
    align-items: center;
    gap: 8px;
}}

.mock-logo-shape {{
    width: 20px;
    height: 20px;
    background: var(--text-color);
}}
.shape-circle {{ border-radius: 50%; }}
.shape-triangle {{ clip-path: polygon(50% 0%, 0% 100%, 100% 100%); }}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Epic Hero Section</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Oswald:wght@500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="hero-wrapper">
        
        <!-- Navigation -->
        <nav class="navbar">
            <div class="logo">
                <span class="logo-icon"></span>
                REBEL
            </div>
            <ul class="nav-links">
                <li><a href="#">Our Ships</a></li>
                <li><a href="#">Mission</a></li>
                <li><a href="#">Donations</a></li>
            </ul>
            <button class="btn-ghost">JOIN NOW</button>
        </nav>

        <!-- Main Hero Content -->
        <main class="hero-content">
            <div class="hero-text-col">
                <h1 class="hero-title">{title_text}</h1>
                <p class="hero-desc">{body_text}</p>
                
                <button class="btn-primary">JOIN NOW FOR FREE</button>
                
                <!-- Optimization: Avatar Pile Social Proof -->
                <div class="social-proof-avatars">
                    <div class="avatar-group">
                        <img src="https://i.pravatar.cc/100?img=3" alt="User" class="avatar">
                        <img src="https://i.pravatar.cc/100?img=11" alt="User" class="avatar">
                        <img src="https://i.pravatar.cc/100?img=12" alt="User" class="avatar">
                        <img src="https://i.pravatar.cc/100?img=15" alt="User" class="avatar">
                    </div>
                    <span class="social-proof-text"><strong>Obi Wan</strong> and 4,000 others have already joined</span>
                </div>
            </div>
            
            <div class="hero-graphic-col">
                <!-- Abstract floating element representing the ship/hero graphic -->
                <div class="floating-element"></div>
            </div>
        </main>

        <!-- Optimization: Media Logos Social Proof -->
        <footer class="social-proof-logos">
            <span class="logos-label">As Seen On:</span>
            <div class="logo-strip">
                <div class="mock-logo"><div class="mock-logo-shape shape-circle"></div> NEWS NETWORK</div>
                <div class="mock-logo"><div class="mock-logo-shape shape-triangle"></div> GALACTIC TV</div>
                <div class="mock-logo"><div class="mock-logo-shape"></div> THE DAILY</div>
            </div>
        </footer>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Simple interaction to enhance the social proof strip on hover
document.addEventListener('DOMContentLoaded', () => {
    const logoStrip = document.querySelector('.logo-strip');
    
    // Brighten logos on hover to show interactivity without stealing focus permanently
    logoStrip.addEventListener('mouseenter', () => {
        logoStrip.style.transition = 'opacity 0.3s ease';
        logoStrip.style.opacity = '1';
    });
    
    logoStrip.addEventListener('mouseleave', () => {
        logoStrip.style.opacity = '0.5';
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
