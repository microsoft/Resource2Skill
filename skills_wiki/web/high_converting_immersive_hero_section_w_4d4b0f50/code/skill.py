def create_component(
    output_dir: str,
    title_text: str = "It's your universe, it's time to save it",
    body_text: str = "The Rebel alliance is fighting to get rid of the evil empire, join the resistance to create a better future for your children.",
    color_scheme: str = "dark",
    accent_color: str = "#e62429", # Rebel Red
    width_px: int = 1440,
    height_px: int = 900,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the High-Converting Hero Section.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme handling
    if color_scheme == "dark":
        bg_color = "#090a0f" # Deep space black
        bg_gradient = f"radial-gradient(circle at 75% 50%, #1a1e29 0%, {bg_color} 60%)"
        text_color = "#ffffff"
        text_muted = "rgba(255, 255, 255, 0.7)"
        nav_bg = "rgba(9, 10, 15, 0.8)"
    else:
        # Fallback light theme if requested
        bg_color = "#f4f5f7"
        bg_gradient = f"radial-gradient(circle at 75% 50%, #ffffff 0%, {bg_color} 60%)"
        text_color = "#111827"
        text_muted = "rgba(17, 24, 39, 0.7)"
        nav_bg = "rgba(244, 245, 247, 0.8)"

    css = f"""/* High-Converting Hero Section */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Oswald:wght@600;700&display=swap');

:root {{
    --bg-color: {bg_color};
    --bg-gradient: {bg_gradient};
    --text-color: {text_color};
    --text-muted: {text_muted};
    --accent-color: {accent_color};
    --nav-bg: {nav_bg};
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', sans-serif;
    background-color: var(--bg-color);
    background-image: var(--bg-gradient);
    color: var(--text-color);
    min-height: 100vh;
    overflow-x: hidden;
    display: flex;
    flex-direction: column;
}}

.hero-wrapper {{
    width: 100%;
    max-width: {width_px}px;
    min-height: {height_px}px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    position: relative;
}}

/* --- Navigation Header --- */
header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2rem 5%;
    position: relative;
    z-index: 10;
}}

.logo-container {{
    display: flex;
    align-items: center;
    gap: 12px;
    font-family: 'Oswald', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: 1px;
}}

.logo-icon {{
    width: 32px;
    height: 32px;
    background-color: var(--accent-color);
    clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
    display: inline-block;
}}

nav ul {{
    display: flex;
    align-items: center;
    gap: 2rem;
    list-style: none;
}}

nav a {{
    color: var(--text-color);
    text-decoration: none;
    font-weight: 500;
    font-size: 0.95rem;
    transition: color 0.3s ease;
}}

nav a:hover {{
    color: var(--accent-color);
}}

/* Buttons */
.btn {{
    display: inline-block;
    padding: 12px 28px;
    font-family: 'Oswald', sans-serif;
    font-weight: 700;
    font-size: 1.1rem;
    text-transform: uppercase;
    text-decoration: none;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.3s ease;
}}

.btn-outline {{
    background: transparent;
    color: var(--text-color);
    border: 2px solid var(--text-color);
}}

.btn-outline:hover {{
    background: var(--text-color);
    color: var(--bg-color);
}}

.btn-primary {{
    background: var(--accent-color);
    color: #ffffff;
    border: 2px solid var(--accent-color);
    padding: 16px 36px;
    font-size: 1.2rem;
    box-shadow: 0 4px 14px rgba(230, 36, 41, 0.4);
}}

.btn-primary:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(230, 36, 41, 0.6);
}}

/* --- Main Hero Content --- */
.hero-main {{
    flex: 1;
    display: grid;
    grid-template-columns: 1fr 1fr;
    align-items: center;
    padding: 0 5%;
    gap: 4rem;
    z-index: 5;
}}

.hero-text {{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 1.5rem;
    max-width: 600px;
}}

h1.headline {{
    font-family: 'Oswald', sans-serif;
    font-size: clamp(3.5rem, 5vw, 5rem);
    line-height: 1.1;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: -0.5px;
}}

p.subhead {{
    font-size: 1.15rem;
    line-height: 1.6;
    color: var(--text-muted);
    margin-bottom: 1rem;
}}

/* Social Proof Block */
.social-proof {{
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-top: 1rem;
}}

.avatar-group {{
    display: flex;
}}

.avatar-group img {{
    width: 36px;
    height: 36px;
    border-radius: 50%;
    border: 2px solid var(--bg-color);
    margin-left: -12px;
}}
.avatar-group img:first-child {{ margin-left: 0; }}

.social-proof-text {{
    font-size: 0.9rem;
    color: var(--text-muted);
    font-weight: 500;
}}

/* --- Hero Image Asset --- */
.hero-visual {{
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    animation: float 6s ease-in-out infinite;
}}

.placeholder-ship {{
    width: 80%;
    height: 400px;
    background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 100%);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 20px;
    backdrop-filter: blur(10px);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-muted);
    font-family: 'Oswald', sans-serif;
    letter-spacing: 2px;
    transform: rotate(-5deg);
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}}

@keyframes float {{
    0% {{ transform: translateY(0px); }}
    50% {{ transform: translateY(-20px); }}
    100% {{ transform: translateY(0px); }}
}}

/* --- Authority Band (Bottom) --- */
.authority-band {{
    padding: 2rem 5%;
    display: flex;
    align-items: center;
    gap: 2rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    margin-top: auto;
    z-index: 10;
}}

.authority-label {{
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--text-muted);
    font-weight: 600;
}}

.authority-logos {{
    display: flex;
    gap: 2.5rem;
    opacity: 0.6;
}}

.authority-logos span {{
    font-family: 'Oswald', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
}}

/* Responsive */
@media (max-width: 968px) {{
    .hero-main {{
        grid-template-columns: 1fr;
        text-align: center;
        gap: 2rem;
        padding-top: 2rem;
    }}
    .hero-text {{
        align-items: center;
        margin: 0 auto;
    }}
    nav ul {{ display: none; }} /* Simple hide for mobile in this demo */
    .authority-band {{
        flex-direction: column;
        justify-content: center;
        text-align: center;
        padding-bottom: 2rem;
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hero Component</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

<div class="hero-wrapper">
    <!-- Header Navigation -->
    <header>
        <div class="logo-container">
            <span class="logo-icon"></span>
            Rebel Alliance
        </div>
        <nav>
            <ul>
                <li><a href="#">Our Ships</a></li>
                <li><a href="#">Mission</a></li>
                <li><a href="#">Donations</a></li>
                <li><a href="#" class="btn btn-outline">Join Now</a></li>
            </ul>
        </nav>
    </header>

    <!-- Main Content Split -->
    <main class="hero-main">
        <div class="hero-text">
            <h1 class="headline">{title_text}</h1>
            <p class="subhead">{body_text}</p>
            
            <a href="#" class="btn btn-primary">Join Now For Free</a>
            
            <!-- Social Proof Mechanism -->
            <div class="social-proof">
                <div class="avatar-group">
                    <img src="https://ui-avatars.com/api/?name=Obi+Wan&background=random" alt="User avatar">
                    <img src="https://ui-avatars.com/api/?name=Luke+S&background=random" alt="User avatar">
                    <img src="https://ui-avatars.com/api/?name=Leia+O&background=random" alt="User avatar">
                </div>
                <div class="social-proof-text">
                    <strong>Obi Wan</strong> and 4,000 others have already joined
                </div>
            </div>
        </div>

        <div class="hero-visual">
            <!-- In a real scenario, this is an <img> tag with a transparent PNG -->
            <div class="placeholder-ship">
                [ Insert Transparent Subject Image Here ]
            </div>
        </div>
    </main>

    <!-- Authority / Trust Band -->
    <div class="authority-band">
        <div class="authority-label">As Seen On:</div>
        <div class="authority-logos">
            <span>CNN</span>
            <span>FOX</span>
            <span>NBC</span>
            <span>THE CW</span>
        </div>
    </div>
</div>

<script src="script.js"></script>
</body>
</html>
"""

    js = """// No complex JS required for the core visual pattern.
// Hover states and the floating animation are handled via pure CSS for better performance.
console.log("Hero component loaded successfully.");
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
