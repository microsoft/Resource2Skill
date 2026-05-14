def create_component(
    output_dir: str,
    title_text: str = "IT'S YOUR UNIVERSE,\nIT'S TIME TO SAVE IT",
    body_text: str = "The Rebel Alliance is fighting to get rid of the evil empire, join the resistance to create a better future for your children.",
    color_scheme: str = "dark",  # "dark" or "light" (dark is default as in video)
    accent_color: str = "#E03433",  # Red color used for Rebel Alliance elements
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Star Wars-Inspired Hero Section with Social Proof visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # --- Image URLs from the tutorial (for reproduction purposes) ---
    # Note: These images are used for illustrative purposes only, as per the tutorial.
    # For actual projects, ensure proper licensing/copyright.
    rebel_logo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Rebel_Alliance_symbol.svg/1200px-Rebel_Alliance_symbol.svg.png"
    xwing_url = "https://static.wikia.nocookie.net/starwars/images/b/b5/XWing-SW_Facts.png/revision/latest/scale-to-width-down/1200?cb=20140920202951"
    death_star_url = "https://assets.mycast.io/characters/ruined-death-star-2598381-large.jpg"
    space_bg_url = "https://cdn.pixabay.com/photo/2016/10/24/05/23/milky-way-1764619_1280.jpg" # Using a generic space bg from Pixabay

    # --- Social Proof (User) - Generic avatars to avoid copyright on Star Wars cast ---
    profile_pic_1 = "https://i.pravatar.cc/40?img=68"
    profile_pic_2 = "https://i.pravatar.cc/40?img=69"
    profile_pic_3 = "https://i.pravatar.cc/40?img=70"

    # --- Social Proof (Media) - Generic white/grayscale logos ---
    cnn_logo = "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/CNN_logo_transparent_text.svg/1280px-CNN_logo_transparent_text.svg.png"
    abc_logo = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/ABC_logo_2021.svg/1280px-ABC_logo_2021.svg.png"
    cbs_logo = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/CBS_logo_2021.svg/1280px-CBS_logo_2021.svg.png"
    fox_logo = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Fox_News_Channel_logo.svg/1280px-Fox_News_Channel_logo.svg.png"
    cw_logo = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/The_CW_wordmark.svg/1280px-The_CW_wordmark.svg.png"

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#0e0f19"  # Dark space background
        text_color = "#FFFFFF"
        secondary_text_color = "#CCCCCC"
        button_text_color = "#FFFFFF"
        ghost_button_bg = "transparent"
        ghost_button_border = accent_color
    else:
        # Placeholder for a light theme, though video shows dark
        bg_color = "#F0F2F5"
        text_color = "#333333"
        secondary_text_color = "#666666"
        button_text_color = "#FFFFFF"
        ghost_button_bg = "transparent"
        ghost_button_border = accent_color

    # === CSS ===
    css = f"""
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;500;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --secondary-text-color: {secondary_text_color};
    --accent-color: {accent_color};
    --button-text-color: {button_text_color};
    --ghost-button-bg: {ghost_button_bg};
    --ghost-button-border: {ghost_button_border};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    overflow-x: hidden;
    position: relative;
    background-image: url('{space_bg_url}');
    background-size: cover;
    background-position: center;
}}

.hero-section {{
    width: var(--width);
    max-width: 100%;
    height: var(--height);
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    overflow: hidden;
}}

header {{
    width: 100%;
    padding: 20px 30px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: linear-gradient(180deg, rgba(0,0,0,0.8) 0%, rgba(0,0,0,0) 100%);
    position: relative;
    z-index: 10;
}}

.logo-area {{
    display: flex;
    align-items: center;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.8vw;
    font-weight: 700;
    letter-spacing: 0.1em;
    color: var(--text-color);
    text-transform: uppercase;
}}

.logo-area img {{
    height: 45px;
    margin-right: 15px;
}}

nav {{
    display: flex;
    align-items: center;
    gap: 30px;
}}

nav a {{
    color: var(--text-color);
    text-decoration: none;
    font-weight: 500;
    font-size: 1.2vw;
    transition: color 0.3s ease;
}}

nav a:hover {{
    color: var(--accent-color);
}}

.btn {{
    padding: 12px 25px;
    border: none;
    border-radius: 5px;
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    font-size: 1.2vw;
    cursor: pointer;
    text-decoration: none;
    transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
    text-transform: uppercase;
}}

.btn-primary {{
    background-color: var(--accent-color);
    color: var(--button-text-color);
    border: 2px solid var(--accent-color);
}}

.btn-primary:hover {{
    background-color: #A32929; /* Slightly darker red on hover */
    border-color: #A32929;
}}

.btn-ghost {{
    background-color: var(--ghost-button-bg);
    color: var(--accent-color);
    border: 2px solid var(--ghost-button-border);
}}

.btn-ghost:hover {{
    background-color: var(--accent-color);
    color: var(--button-text-color);
}}

.hero-content {{
    position: absolute;
    top: 50%;
    left: 10%;
    transform: translateY(-50%);
    width: 45%;
    max-width: 500px;
    text-align: left;
    z-index: 5;
}}

.hero-content h1 {{
    font-family: 'Bebas Neue', sans-serif;
    font-size: 5.5vw;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 20px;
    color: var(--text-color);
    text-transform: uppercase;
    letter-spacing: 0.1em;
}}

.hero-content p {{
    font-size: 1.5vw;
    line-height: 1.4;
    margin-bottom: 30px;
    color: var(--secondary-text-color);
}}

.hero-content .btn-primary {{
    font-size: 1.2vw;
    padding: 15px 35px;
    letter-spacing: 0.05em;
}}

.hero-image {{
    position: absolute;
    right: 0;
    top: 50%;
    transform: translateY(-50%);
    width: 65%; /* Adjusted for overlapping with content */
    height: 100%;
    overflow: hidden;
    pointer-events: none; /* Allows clicks to pass through */
}}

.hero-image img.xwing {{
    position: absolute;
    top: 50%;
    left: 50%; /* Adjusted to appear mostly on the right */
    transform: translate(-50%, -50%) scale(1.1);
    height: 80%;
    max-width: 120%;
    object-fit: contain;
    filter: drop-shadow(0 0 15px rgba(0, 0, 0, 0.5));
}}

.hero-image img.death-star {{
    position: absolute;
    top: 25%;
    right: 5%;
    transform: translate(0%, -50%) scale(0.6);
    height: 50%;
    object-fit: contain;
    filter: drop-shadow(0 0 20px rgba(0, 0, 0, 0.7));
    opacity: 0.8;
}}

.social-proof-users {{
    position: absolute;
    bottom: 120px;
    left: 10%;
    display: flex;
    align-items: center;
    gap: 10px;
    z-index: 5;
    font-size: 1vw;
    color: var(--secondary-text-color);
}}

.social-proof-users .avatars {{
    display: flex;
}}

.social-proof-users .avatars img {{
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: 2px solid var(--bg-color);
    margin-left: -15px;
    object-fit: cover;
}}

.social-proof-users .avatars img:first-child {{
    margin-left: 0;
}}

.as-seen-on {{
    width: 100%;
    max-width: var(--width);
    padding: 20px 30px;
    background-color: #1a1a2e; /* Darker bar */
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 30px;
    position: absolute;
    bottom: 0;
    z-index: 10;
}}

.as-seen-on p {{
    color: var(--secondary-text-color);
    font-size: 1vw;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    white-space: nowrap;
}}

.as-seen-on .logos {{
    display: flex;
    gap: 25px;
    align-items: center;
}}

.as-seen-on .logos img {{
    height: 25px;
    filter: grayscale(100%) brightness(200%) opacity(0.7);
    mix-blend-mode: luminosity;
}}

/* Responsive adjustments */
@media (max-width: 900px) {{
    .hero-section {{
        flex-direction: column;
        height: auto;
        padding-bottom: 200px; /* Space for as-seen-on at bottom */
    }}
    header {{
        flex-direction: column;
        gap: 20px;
        padding: 20px;
    }}
    .logo-area, nav a, .btn {{
        font-size: 1.8vw;
    }}
    .hero-content {{
        position: relative;
        top: auto;
        left: auto;
        transform: none;
        width: 80%;
        max-width: none;
        text-align: center;
        padding: 50px 0 20px 0;
    }}
    .hero-content h1 {{
        font-size: 8vw;
    }}
    .hero-content p {{
        font-size: 2.5vw;
    }}
    .hero-content .btn-primary {{
        font-size: 2vw;
    }}
    .hero-image {{
        position: relative;
        width: 100%;
        height: 400px;
        transform: none;
    }}
    .hero-image img.xwing {{
        height: 60%;
        left: 50%;
        top: 60%;
    }}
    .hero-image img.death-star {{
        right: 10%;
        top: 20%;
        height: 40%;
    }}
    .social-proof-users {{
        position: relative;
        bottom: auto;
        left: auto;
        justify-content: center;
        padding-top: 20px;
        font-size: 2vw;
    }}
    .as-seen-on {{
        flex-direction: column;
        gap: 15px;
        padding: 15px;
        bottom: 0;
        position: relative; /* Ensure it's part of the flow */
    }}
    .as-seen-on p {{
        font-size: 1.8vw;
    }}
    .as-seen-on .logos {{
        gap: 15px;
    }}
    .as-seen-on .logos img {{
        height: 20px;
    }}
}}

@media (max-width: 600px) {{
    .logo-area, nav a, .btn {{
        font-size: 2.5vw;
    }}
    .hero-content h1 {{
        font-size: 10vw;
    }}
    .hero-content p {{
        font-size: 3.5vw;
    }}
    .hero-content .btn-primary {{
        font-size: 3vw;
    }}
    .social-proof-users {{
        font-size: 2.5vw;
    }}
    .social-proof-users .avatars img {{
        width: 30px;
        height: 30px;
    }}
    .as-seen-on p {{
        font-size: 2.5vw;
    }}
    .as-seen-on .logos img {{
        height: 15px;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{kwargs.get('page_title', 'Rebel Alliance Hero')}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="hero-section">
        <header>
            <div class="logo-area">
                <img src="{rebel_logo_url}" alt="Rebel Alliance Logo">
                Rebel Alliance
            </div>
            <nav>
                <a href="#">Our Ships</a>
                <a href="#">Mission</a>
                <a href="#">Donations</a>
                <a href="#" class="btn btn-ghost">Join Now</a>
            </nav>
        </header>

        <div class="hero-content">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <a href="#" class="btn btn-primary">Join Now For Free</a>

            <div class="social-proof-users">
                <div class="avatars">
                    <img src="{profile_pic_1}" alt="Profile Photo 1">
                    <img src="{profile_pic_2}" alt="Profile Photo 2">
                    <img src="{profile_pic_3}" alt="Profile Photo 3">
                </div>
                <span>Obi-Wan and 4,000 others have already joined</span>
            </div>
        </div>

        <div class="hero-image">
            <img src="{death_star_url}" alt="Ruined Death Star" class="death-star">
            <img src="{xwing_url}" alt="X-Wing Starfighter" class="xwing">
        </div>
        
        <div class="as-seen-on">
            <p>As Seen On</p>
            <div class="logos">
                <img src="{abc_logo}" alt="ABC Logo">
                <img src="{cbs_logo}" alt="CBS Logo">
                <img src="{fox_logo}" alt="FOX Logo">
                <img src="{cnn_logo}" alt="CNN Logo">
                <img src="{cw_logo}" alt="The CW Logo">
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript (minimal, for this design it's mostly CSS) ===
    js = """
document.addEventListener('DOMContentLoaded', () => {
    // No complex JavaScript needed for the core visual reproduction of this hero section.
    // All interactive elements (hovers) are handled via CSS.
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

