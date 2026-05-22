def create_component(
    output_dir: str,
    title_text: str = "IT'S YOUR UNIVERSE, IT'S TIME TO SAVE IT",
    body_text: str = "The Rebel Alliance is fighting to get rid of the evil empire, join the resistance to create a better future for your children.",
    color_scheme: str = "dark",        # "dark" or "light" (dark is default and demonstrated)
    accent_color: str = "#E50914",     # CSS hex color for accent (red for Rebel Alliance)
    width_px: int = 1440,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the "Galactic Hero Section Design" visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_gradient_start = "#1a0033"
        bg_gradient_end = "#000000"
        text_color = "#FFFFFF"
        nav_link_color = "#CCCCCC"
        social_proof_text = "#AAAAAA"
        social_proof_logo_filter = "brightness(0) invert(1)" # To make them white on dark background
    else: # Light scheme - not explicitly demonstrated in video but good to have
        bg_gradient_start = "#f0f8ff"
        bg_gradient_end = "#e6f2ff"
        text_color = "#1a1a2e"
        nav_link_color = "#555555"
        social_proof_text = "#777777"
        social_proof_logo_filter = "none"

    # Royalty-free image URLs for demonstration, mimicking the video's aesthetic
    # Original video uses copyrighted Star Wars assets. These are substitutes.
    starfield_bg_url = "https://images.unsplash.com/photo-1536440136665-c99a6f79020a?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80"
    spaceship_img_url = "https://images.unsplash.com/photo-1596700071370-1f13b4c979cf?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80" # Generic Sci-Fi ship
    planet_img_url = "https://images.unsplash.com/photo-1543085526-7c0552b36e3c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80" # Generic destroyed planet

    # CNN, FOX, ABC, CBS, CW - royalty-free logos for "as seen on"
    # Using white versions for dark mode, or default for light mode
    cnn_logo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/CNN_logo.svg/512px-CNN_logo.svg.png"
    fox_logo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Fox_Broadcasting_Company_logo.svg/512px-Fox_Broadcasting_Company_logo.svg.png"
    abc_logo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/ABC_logo_2021.svg/512px-ABC_logo_2021.svg.png"
    cbs_logo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/CBS_logo_2022.svg/512px-CBS_logo_2022.svg.png"
    cw_logo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/The_CW_logo.svg/512px-The_CW_logo.svg.png"


    # === CSS ===
    css = f"""
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800&family=Inter:wght@400;600&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-gradient-start: {bg_gradient_start};
    --bg-gradient-end: {bg_gradient_end};
    --text-color: {text_color};
    --accent-color: {accent_color};
    --nav-link-color: {nav_link_color};
    --social-proof-text: {social_proof_text};
    --social-proof-logo-filter: {social_proof_logo_filter};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, var(--bg-gradient-start), var(--bg-gradient-end));
    background-image: url('{starfield_bg_url}');
    background-size: cover;
    background-position: center;
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow-x: hidden;
    position: relative;
}}

.site-container {{
    max-width: var(--width);
    min-height: var(--height);
    margin: auto;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    padding: 20px 40px;
    position: relative;
    z-index: 10; /* Ensure content is above background images */
}}

header {{
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 0;
    color: var(--text-color);
}}

.logo-container {{
    display: flex;
    align-items: center;
    gap: 10px;
}}

.rebel-logo {{
    width: 30px;
    height: 30px;
    fill: var(--accent-color);
}}

.logo-text {{
    font-family: 'Montserrat', sans-serif;
    font-weight: 800;
    font-size: 24px;
    text-transform: uppercase;
    letter-spacing: 1px;
}}

nav ul {{
    list-style: none;
    display: flex;
    gap: 30px;
}}

nav a {{
    color: var(--nav-link-color);
    text-decoration: none;
    font-weight: 600;
    font-size: 16px;
    transition: color 0.3s ease;
}}

nav a:hover {{
    color: var(--text-color);
}}

.btn-join-now {{
    background-color: var(--accent-color);
    color: var(--text-color);
    padding: 10px 25px;
    border: none;
    border-radius: 5px;
    text-decoration: none;
    font-weight: 600;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.2s ease;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

.btn-join-now:hover {{
    background-color: #c00711; /* Darker red on hover */
    transform: translateY(-2px);
}}

.hero-section {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    padding: 60px 0;
    flex-grow: 1;
    gap: 40px;
}}

.hero-text-content {{
    flex: 1;
    max-width: 50%;
    text-align: left;
    padding-right: 40px;
}}

.hero-text-content h1 {{
    font-family: 'Montserrat', sans-serif;
    font-weight: 800;
    font-size: 64px;
    line-height: 1.1;
    margin-bottom: 20px;
}}

.hero-text-content p {{
    font-size: 20px;
    line-height: 1.6;
    margin-bottom: 30px;
    color: var(--nav-link-color);
}}

.btn-primary {{
    background-color: var(--accent-color);
    color: var(--text-color);
    padding: 15px 35px;
    border: none;
    border-radius: 8px;
    font-family: 'Montserrat', sans-serif;
    font-weight: 700;
    font-size: 18px;
    text-transform: uppercase;
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.2s ease;
    letter-spacing: 1px;
    display: inline-block;
    margin-bottom: 20px;
}}

.btn-primary:hover {{
    background-color: #c00711;
    transform: translateY(-3px);
}}

.social-proof-users {{
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 20px;
}}

.avatar-stack {{
    display: flex;
}}

.avatar {{
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: #555; /* Placeholder color */
    border: 2px solid var(--text-color);
    margin-left: -10px;
}}

.avatar:first-child {{
    margin-left: 0;
}}

.avatar-text {{
    font-size: 16px;
    color: var(--social-proof-text);
    margin-left: 10px;
}}

.hero-image-container {{
    flex: 1;
    position: relative;
    height: 500px;
    max-width: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.spaceship-img {{
    position: absolute;
    width: 70%;
    height: auto;
    object-fit: contain;
    right: 0%;
    top: 50%;
    transform: translateY(-50%) rotate(5deg);
    filter: drop-shadow(0 0 15px rgba(0, 191, 255, 0.4));
}}

.planet-img {{
    position: absolute;
    width: 45%;
    height: auto;
    object-fit: contain;
    left: 10%;
    top: 50%;
    transform: translateY(-50%) scale(0.9);
    opacity: 0.8;
    filter: drop-shadow(0 0 10px rgba(255, 0, 0, 0.3));
}}

.as-seen-on {{
    width: 100%;
    background-color: rgba(0, 0, 0, 0.5); /* Slightly darker band */
    padding: 20px 0;
    text-align: center;
    margin-top: 40px;
    border-radius: 8px;
}}

.as-seen-on-title {{
    font-size: 14px;
    font-weight: 600;
    color: var(--social-proof-text);
    text-transform: uppercase;
    margin-bottom: 15px;
    letter-spacing: 1px;
}}

.news-logos {{
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 40px;
    flex-wrap: wrap;
}}

.news-logo {{
    height: 30px; /* Adjust as needed */
    object-fit: contain;
    filter: var(--social-proof-logo-filter);
    opacity: 0.7;
}}

/* Responsive adjustments */
@media (max-width: 1024px) {{
    .hero-section {{
        flex-direction: column;
        text-align: center;
        padding: 40px 0;
    }}
    .hero-text-content {{
        max-width: 90%;
        padding-right: 0;
    }}
    .hero-text-content h1 {{
        font-size: 48px;
    }}
    .hero-image-container {{
        height: 400px;
        max-width: 90%;
    }}
    .spaceship-img {{
        width: 80%;
        right: auto;
        left: 50%;
        transform: translateX(-50%) rotate(5deg);
    }}
    .planet-img {{
        width: 50%;
        left: 20%;
        transform: translateY(-50%) scale(0.9);
    }}
    header {{
        flex-direction: column;
        gap: 15px;
    }}
    nav ul {{
        gap: 20px;
    }}
}}

@media (max-width: 768px) {{
    .hero-text-content h1 {{
        font-size: 36px;
    }}
    .hero-text-content p {{
        font-size: 18px;
    }}
    .btn-primary {{
        padding: 12px 25px;
        font-size: 16px;
    }}
    .news-logos {{
        gap: 20px;
    }}
    .news-logo {{
        height: 25px;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rebel Alliance - {title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="site-container" style="width: {width_px}px;">
        <header>
            <div class="logo-container">
                <svg class="rebel-logo" viewBox="0 0 100 100">
                    <path d="M 50 0 L 20 20 L 30 50 L 20 80 L 50 100 L 80 80 L 70 50 L 80 20 L 50 0 Z M 50 20 L 40 30 L 40 70 L 50 80 L 60 70 L 60 30 L 50 20 Z"/>
                </svg>
                <span class="logo-text">Rebel Alliance</span>
            </div>
            <nav>
                <ul>
                    <li><a href="#ships">Our Ships</a></li>
                    <li><a href="#mission">Mission</a></li>
                    <li><a href="#donations">Donations</a></li>
                    <li><button class="btn-join-now">Join Now</button></li>
                </ul>
            </nav>
        </header>

        <div class="hero-section">
            <div class="hero-text-content">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
                <button class="btn-primary">JOIN NOW FOR FREE</button>
                <div class="social-proof-users">
                    <div class="avatar-stack">
                        <img class="avatar" src="https://i.pravatar.cc/40?img=68" alt="Obi Wan Kenobi">
                        <img class="avatar" src="https://i.pravatar.cc/40?img=69" alt="Leia Organa">
                        <img class="avatar" src="https://i.pravatar.cc/40?img=70" alt="Han Solo">
                    </div>
                    <span class="avatar-text">Obi Wan and 4,000 others have already joined</span>
                </div>
            </div>
            <div class="hero-image-container">
                <img class="planet-img" src="{planet_img_url}" alt="Destroyed Planet">
                <img class="spaceship-img" src="{spaceship_img_url}" alt="Rebel Spaceship">
            </div>
        </div>

        <div class="as-seen-on">
            <h3 class="as-seen-on-title">As Seen On</h3>
            <div class="news-logos">
                <img class="news-logo" src="{cnn_logo_url}" alt="CNN Logo">
                <img class="news-logo" src="{fox_logo_url}" alt="FOX Logo">
                <img class="news-logo" src="{abc_logo_url}" alt="ABC Logo">
                <img class="news-logo" src="{cbs_logo_url}" alt="CBS Logo">
                <img class="news-logo" src="{cw_logo_url}" alt="The CW Logo">
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """
document.addEventListener('DOMContentLoaded', () => {
    // No complex interactive behavior specifically demonstrated for the hero section's visual effect
    // in the final video output, so this file remains largely empty for this skill.
    // Standard button clicks and navigation would be handled here in a full application.
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
