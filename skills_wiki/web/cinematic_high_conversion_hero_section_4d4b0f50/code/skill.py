def create_component(
    output_dir: str,
    title_text: str = "It's your universe,<br>it's time to save it",
    body_text: str = "The Rebel alliance is fighting to get rid of the evil empire, join the resistance to create a better future for your children.",
    color_scheme: str = "dark",
    accent_color: str = "#e52b22", # Rebel Red
    width_px: int = 1440,
    height_px: int = 900,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Cinematic High-Conversion Hero Section.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color_start = "#05070a"
        bg_color_end = "#13192b"
        text_primary = "#ffffff"
        text_secondary = "#94a3b8"
        border_color = "rgba(255, 255, 255, 0.1)"
        surface_glass = "rgba(255, 255, 255, 0.05)"
    else:
        bg_color_start = "#e2e8f0"
        bg_color_end = "#f8fafc"
        text_primary = "#0f172a"
        text_secondary = "#475569"
        border_color = "rgba(0, 0, 0, 0.1)"
        surface_glass = "rgba(0, 0, 0, 0.05)"

    # === CSS ===
    css = f"""/* Cinematic High-Conversion Hero Section */
:root {{
    --bg-start: {bg_color_start};
    --bg-end: {bg_color_end};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --accent: {accent_color};
    --border: {border_color};
    --glass: {surface_glass};
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: radial-gradient(circle at 50% 50%, var(--bg-end) 0%, var(--bg-start) 100%);
    color: var(--text-primary);
    min-height: 100vh;
    overflow-x: hidden;
}}

/* Canvas Background */
#starfield {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 0;
    pointer-events: none;
}}

.hero-wrapper {{
    position: relative;
    width: 100%;
    max-width: {width_px}px;
    min-height: {height_px}px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    z-index: 1;
    padding: 2rem 4rem;
}}

/* Navigation */
.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 2rem;
}}

.logo {{
    font-family: 'Montserrat', sans-serif;
    font-weight: 800;
    font-size: 1.5rem;
    letter-spacing: -0.5px;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

.logo-icon {{
    width: 24px;
    height: 24px;
    background: var(--accent);
    border-radius: 50%;
    display: inline-block;
}}

.nav-links {{
    display: flex;
    gap: 2.5rem;
}}

.nav-links a {{
    color: var(--text-primary);
    text-decoration: none;
    font-size: 0.95rem;
    font-weight: 500;
    transition: opacity 0.2s;
}}

.nav-links a:hover {{
    opacity: 0.7;
}}

/* Buttons */
.btn {{
    display: inline-block;
    padding: 0.8rem 1.8rem;
    font-weight: 600;
    font-size: 0.9rem;
    text-decoration: none;
    border-radius: 4px;
    transition: all 0.3s ease;
    cursor: pointer;
    font-family: 'Montserrat', sans-serif;
    letter-spacing: 0.5px;
}}

.btn-outline {{
    border: 1px solid var(--text-primary);
    color: var(--text-primary);
    background: transparent;
}}

.btn-outline:hover {{
    background: var(--text-primary);
    color: var(--bg-start);
}}

.btn-primary {{
    background: var(--accent);
    color: #fff;
    border: 1px solid var(--accent);
    font-size: 1.1rem;
    padding: 1rem 2.5rem;
    box-shadow: 0 4px 14px rgba(229, 43, 34, 0.4);
}}

.btn-primary:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(229, 43, 34, 0.6);
}}

/* Main Hero Content */
.hero-main {{
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 2rem;
}}

.hero-content {{
    max-width: 600px;
    display: flex;
    flex-direction: column;
    gap: 2rem;
    align-items: flex-start;
}}

.title {{
    font-family: 'Montserrat', sans-serif;
    font-size: 4rem;
    font-weight: 900;
    line-height: 1.1;
    letter-spacing: -1px;
}}

.body-text {{
    font-size: 1.1rem;
    line-height: 1.6;
    color: var(--text-secondary);
    max-width: 90%;
}}

/* Social Proof Section */
.social-proof {{
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-top: 0.5rem;
}}

.avatar-group {{
    display: flex;
}}

.avatar {{
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: 3px solid var(--bg-start);
    margin-left: -12px;
    background: var(--glass);
    object-fit: cover;
}}

.avatar:first-child {{
    margin-left: 0;
}}

.proof-text {{
    font-size: 0.85rem;
    color: var(--text-secondary);
    font-weight: 500;
}}

/* As Seen On */
.as-seen-on {{
    margin-top: 1.5rem;
    width: 100%;
}}

.as-seen-label {{
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--text-secondary);
    margin-bottom: 0.8rem;
    display: block;
}}

.logos-container {{
    display: flex;
    gap: 2rem;
    align-items: center;
    opacity: 0.5;
    filter: grayscale(100%);
}}

.logo-mock {{
    font-family: 'Montserrat', sans-serif;
    font-weight: 800;
    font-size: 1.5rem;
    letter-spacing: -1px;
}}

/* Visual Graphic (Right Side) */
.hero-visual {{
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
}}

/* CSS-based Spaceship Shape */
.abstract-ship {{
    width: 450px;
    height: 250px;
    background: linear-gradient(135deg, var(--glass) 0%, transparent 100%);
    backdrop-filter: blur(8px);
    border: 1px solid var(--border);
    clip-path: polygon(0% 45%, 70% 45%, 70% 0%, 100% 50%, 70% 100%, 70% 55%, 0% 55%);
    transform: rotate(-10deg);
    animation: float 6s ease-in-out infinite;
    position: relative;
}}

.abstract-ship::after {{
    content: '';
    position: absolute;
    right: 0;
    top: 50%;
    transform: translateY(-50%);
    width: 20px;
    height: 20px;
    background: var(--accent);
    border-radius: 50%;
    box-shadow: 0 0 30px 10px var(--accent);
}}

@keyframes float {{
    0%, 100% {{ transform: translateY(0) rotate(-10deg); }}
    50% {{ transform: translateY(-25px) rotate(-8deg); }}
}}

/* Responsive */
@media (max-width: 992px) {{
    .hero-main {{ flex-direction: column; gap: 4rem; text-align: center; }}
    .hero-content {{ align-items: center; }}
    .title {{ font-size: 3rem; }}
    .social-proof, .logos-container {{ justify-content: center; }}
    .abstract-ship {{ width: 300px; height: 160px; }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>High-Conversion Hero</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Montserrat:wght@600;800;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <canvas id="starfield"></canvas>
    
    <div class="hero-wrapper">
        <nav class="navbar">
            <div class="logo">
                <span class="logo-icon"></span>
                Rebel Alliance
            </div>
            <div class="nav-links">
                <a href="#">Our Ships</a>
                <a href="#">Mission</a>
                <a href="#">Donations</a>
            </div>
            <a href="#" class="btn btn-outline">JOIN NOW</a>
        </nav>

        <main class="hero-main">
            <div class="hero-content">
                <h1 class="title">{title_text}</h1>
                <p class="body-text">{body_text}</p>
                
                <a href="#" class="btn btn-primary">JOIN NOW FOR FREE</a>

                <div class="social-proof">
                    <div class="avatar-group">
                        <img src="https://ui-avatars.com/api/?name=Luke+S&background=random&color=fff" alt="User" class="avatar">
                        <img src="https://ui-avatars.com/api/?name=Leia+O&background=random&color=fff" alt="User" class="avatar">
                        <img src="https://ui-avatars.com/api/?name=Han+S&background=random&color=fff" alt="User" class="avatar">
                        <img src="https://ui-avatars.com/api/?name=Chewy&background=random&color=fff" alt="User" class="avatar">
                    </div>
                    <span class="proof-text">Obi Wan and 4,000 others have already joined</span>
                </div>

                <div class="as-seen-on">
                    <span class="as-seen-label">As Seen On:</span>
                    <div class="logos-container">
                        <span class="logo-mock">NBC</span>
                        <span class="logo-mock">FOX</span>
                        <span class="logo-mock" style="font-family: serif; font-style: italic;">The Daily</span>
                    </div>
                </div>
            </div>

            <div class="hero-visual">
                <!-- CSS Shape representing the cinematic visual from the tutorial -->
                <div class="abstract-ship"></div>
            </div>
        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Canvas Starfield for Deep Space Background
document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('starfield');
    const ctx = canvas.getContext('2d');
    
    let width, height;
    let stars = [];

    function resize() {
        width = window.innerWidth;
        height = window.innerHeight;
        canvas.width = width;
        canvas.height = height;
        initStars();
    }

    function initStars() {
        stars = [];
        const numStars = Math.floor((width * height) / 3000); // Density
        for(let i = 0; i < numStars; i++) {
            stars.push({
                x: Math.random() * width,
                y: Math.random() * height,
                radius: Math.random() * 1.5,
                speed: Math.random() * 0.5 + 0.1,
                alpha: Math.random()
            });
        }
    }

    function draw() {
        ctx.clearRect(0, 0, width, height);
        
        stars.forEach(star => {
            ctx.beginPath();
            ctx.arc(star.x, star.y, star.radius, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(255, 255, 255, ${star.alpha})`;
            ctx.fill();
            
            // Move star
            star.x -= star.speed;
            
            // Reset if goes off screen
            if (star.x < 0) {
                star.x = width;
                star.y = Math.random() * height;
            }
            
            // Twinkle effect
            star.alpha += (Math.random() - 0.5) * 0.1;
            if (star.alpha < 0.1) star.alpha = 0.1;
            if (star.alpha > 1) star.alpha = 1;
        });
        
        requestAnimationFrame(draw);
    }

    window.addEventListener('resize', resize);
    resize();
    draw();
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
        "files": files,
    }
