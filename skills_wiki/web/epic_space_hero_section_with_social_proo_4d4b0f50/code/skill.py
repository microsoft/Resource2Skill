def create_component(
    output_dir: str,
    title_text: str = "IT'S YOUR UNIVERSE, IT'S TIME TO SAVE IT",
    body_text: str = "The Rebel Alliance is fighting to get rid of the evil empire, join the resistance to create a better future for your children.",
    color_scheme: str = "dark",  # "dark" or "light" (will primarily use dark as per tutorial)
    accent_color: str = "#E01A24",  # Red for Rebel Alliance
    width_px: int = 1200,
    height_px: int = 700,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the "Epic Space Hero Section with Social Proof" visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # --- Derived colors (primarily dark theme as per tutorial) ---
    if color_scheme == "dark":
        bg_color = "#0D111C"
        text_color = "#FFFFFF"
        secondary_text_color = "#E0E0E0"
        nav_button_bg = "transparent"
        nav_button_border = f"1px solid {accent_color}"
        social_proof_bg = "#880E1A" # Darker red for "As Seen On"
    else: # Light theme, though tutorial focuses on dark
        bg_color = "#F8F9FA"
        text_color = "#1A1A2E"
        secondary_text_color = "#343A40"
        nav_button_bg = "transparent"
        nav_button_border = f"1px solid {accent_color}"
        social_proof_bg = "#E0E0E0"

    # --- Image URLs ---
    # Using specific public/fan-wiki images for direct reproduction of the tutorial's visual.
    # These URLs might not be stable long-term, but capture the current tutorial state.
    x_wing_img_url = "https://sw.novelonlinefull.com/uploads/chapter/2020_05/x_wing_starfighter.jpg"
    death_star_img_url = "https://static.wikia.nocookie.net/starwars/images/f/f6/Death_Star_II_concept_art_1.png/revision/latest?cb=20150917024346"
    space_bg_url = "https://images.hdqwalls.com/download/milky-way-galaxy-stars-4k-qj-1920x1080.jpg"
    rebel_alliance_logo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Alliance_Starbird.svg/1200px-Alliance_Starbird.svg.png"

    # Generic profile photos and "as seen on" logos (grayscale for consistency)
    obi_wan_profile = "https://upload.wikimedia.org/wikipedia/en/3/30/Obi-Wan_Kenobi.png" # Ewan McGregor version
    leia_profile = "https://upload.wikimedia.org/wikipedia/en/1/1b/Princess_Leia_Organa.jpg"
    cnn_logo_white = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/CNN_logo_white.svg/2560px-CNN_logo_white.svg.png"
    fox_logo_white = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Fox_Broadcasting_Company_logo.svg/2560px-Fox_Broadcasting_Company_logo.svg.png"
    abc_logo_white = "https://upload.wikimedia.wikipedia.org/wikipedia/commons/thumb/c/cb/ABC_logo_2021.svg/2560px-ABC_logo_2021.svg.png"


    # === CSS ===
    css = f"""
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@700&family=Inter:wght@400;600;700&display=swap');

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --secondary-text: {secondary_text_color};
    --accent: {accent_color};
    --nav-btn-bg: {nav_button_bg};
    --nav-btn-border: {nav_button_border};
    --social-proof-bg: {social_proof_bg};
    --component-width: {width_px}px;
    --component-height: {height_px}px;
}}

body {{
    font-family: 'Inter', sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow-x: hidden; /* Prevent horizontal scroll */
}}

.hero-section {{
    width: var(--component-width);
    height: var(--component-height);
    position: relative;
    display: flex;
    flex-direction: column;
    background-image: url('{space_bg_url}');
    background-size: cover;
    background-position: center;
    color: var(--text);
}}

.overlay {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.4); /* Dark overlay for readability */
    z-index: 1;
}}

.content-wrapper {{
    position: relative;
    z-index: 2;
    display: flex;
    flex-grow: 1;
    padding: 20px 40px;
    gap: 40px;
    align-items: center; /* Align items vertically in center */
}}

.left-content {{
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    max-width: 50%;
    padding-right: 20px;
}}

.right-imagery {{
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    height: 100%;
    width: 50%;
}}

.x-wing {{
    position: absolute;
    width: 60%;
    max-width: 500px;
    height: auto;
    transform: rotate(5deg) translateX(-10%);
    bottom: 5%;
    right: 5%;
    z-index: 3;
}}

.death-star {{
    position: absolute;
    width: 40%;
    max-width: 350px;
    height: auto;
    top: 0%;
    right: 0%;
    z-index: 2;
}}

.header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 40px;
    background: rgba(0, 0, 0, 0.6);
    position: relative;
    z-index: 10;
}}

.logo-container {{
    display: flex;
    align-items: center;
    gap: 10px;
}}

.rebel-logo {{
    width: 30px;
    height: 30px;
    filter: brightness(0) invert(1) sepia(100%) saturate(1000%) hue-rotate(340deg); /* Red color */
}}

.rebel-alliance-text {{
    font-family: 'Oswald', sans-serif;
    font-weight: 700;
    font-size: 24px;
    color: var(--text);
    letter-spacing: 1px;
}}

.nav-links {{
    display: flex;
    gap: 25px;
    list-style: none;
}}

.nav-links a {{
    color: var(--text);
    text-decoration: none;
    font-weight: 600;
    font-size: 16px;
    transition: color 0.2s ease-in-out;
}}

.nav-links a:hover {{
    color: var(--accent);
}}

.nav-button {{
    background: var(--nav-btn-bg);
    border: var(--nav-btn-border);
    color: var(--accent);
    padding: 8px 15px;
    text-decoration: none;
    border-radius: 5px;
    font-weight: 700;
    font-size: 14px;
    transition: all 0.2s ease-in-out;
    cursor: pointer;
}}

.nav-button:hover {{
    background: var(--accent);
    color: var(--text);
    border-color: var(--accent);
}}

.headline {{
    font-family: 'Oswald', sans-serif;
    font-size: 64px;
    font-weight: 700;
    line-height: 1.1;
    margin-bottom: 20px;
    color: var(--text);
}}

.description {{
    font-size: 18px;
    line-height: 1.5;
    margin-bottom: 30px;
    color: var(--secondary-text);
}}

.main-cta-button {{
    background: var(--accent);
    color: var(--text);
    padding: 15px 30px;
    text-decoration: none;
    border-radius: 5px;
    font-weight: 700;
    font-size: 18px;
    transition: background 0.2s ease-in-out, transform 0.2s ease-in-out;
    cursor: pointer;
    border: none;
    display: inline-block;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}}

.main-cta-button:hover {{
    background: darken(var(--accent), 10%); /* Placeholder for actual darken function */
    transform: translateY(-2px);
}}

/* For simplicity, using a static dark red for hover on main button if Sass darken() is not available */
.main-cta-button:hover {{
    background: #B2151D; /* A slightly darker red */
}}

.social-proof {{
    position: relative;
    z-index: 2;
    background: var(--social-proof-bg);
    padding: 15px 40px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
}}

.joined-members {{
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
}}

.profile-pic {{
    width: 30px;
    height: 30px;
    border-radius: 50%;
    object-fit: cover;
    border: 1px solid var(--text);
}}

.joined-text {{
    font-size: 14px;
    font-weight: 600;
    color: var(--text);
}}

.as-seen-on {{
    display: flex;
    align-items: center;
    gap: 20px;
    flex-wrap: wrap;
}}

.as-seen-on-text {{
    font-size: 14px;
    font-weight: 600;
    color: var(--text);
    text-transform: uppercase;
}}

.media-logo {{
    height: 20px;
    filter: grayscale(100%) brightness(0) invert(1); /* White grayscale for dark background */
    opacity: 0.7;
}}

@media (max-width: 900px) {{
    .hero-section {{
        height: auto;
        min-height: 100vh;
    }}
    .content-wrapper {{
        flex-direction: column;
        text-align: center;
        padding: 20px;
        gap: 20px;
    }}
    .left-content {{
        max-width: 100%;
        padding-right: 0;
    }}
    .right-imagery {{
        width: 100%;
        height: 300px; /* Fixed height for mobile imagery */
        justify-content: center;
    }}
    .headline {{
        font-size: 48px;
    }}
    .description {{
        font-size: 16px;
    }}
    .x-wing {{
        width: 70%;
        bottom: 10%;
        right: auto;
        left: 50%;
        transform: translateX(-50%) rotate(5deg);
    }}
    .death-star {{
        width: 50%;
        top: 0;
        right: 0;
    }}
    .header {{
        flex-direction: column;
        gap: 15px;
    }}
    .nav-links {{
        justify-content: center;
    }}
    .social-proof {{
        flex-direction: column;
        text-align: center;
        gap: 15px;
    }}
    .as-seen-on {{
        justify-content: center;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rebel Alliance Hero Section</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="hero-section">
        <div class="overlay"></div>
        <div class="header">
            <div class="logo-container">
                <img src="{rebel_alliance_logo_url}" alt="Rebel Alliance Logo" class="rebel-logo">
                <span class="rebel-alliance-text">Rebel Alliance</span>
            </div>
            <ul class="nav-links">
                <li><a href="#">Our Ships</a></li>
                <li><a href="#">Mission</a></li>
                <li><a href="#">Donations</a></li>
                <li><a href="#" class="nav-button">JOIN NOW</a></li>
            </ul>
        </div>
        <div class="content-wrapper">
            <div class="left-content">
                <h1 class="headline">{title_text}</h1>
                <p class="description">{body_text}</p>
                <a href="#" class="main-cta-button">JOIN NOW FOR FREE</a>
                <div class="joined-members">
                    <img src="{obi_wan_profile}" alt="Obi Wan Kenobi" class="profile-pic">
                    <img src="{leia_profile}" alt="Princess Leia" class="profile-pic">
                    <span class="joined-text">Obi Wan and 4,000 others have already joined!</span>
                </div>
            </div>
            <div class="right-imagery">
                <img src="{death_star_img_url}" alt="Ruined Death Star" class="death-star">
                <img src="{x_wing_img_url}" alt="X-Wing Starfighter" class="x-wing">
            </div>
        </div>
        <div class="social-proof">
            <span class="as-seen-on-text">As Seen On:</span>
            <div class="as-seen-on">
                <img src="{abc_logo_white}" alt="ABC Logo" class="media-logo">
                <img src="{cnn_logo_white}" alt="CNN Logo" class="media-logo">
                <img src="{fox_logo_white}" alt="FOX Logo" class="media-logo">
                <!-- Add more logos as desired -->
            </div>
        </div>
    </div>
</body>
</html>"""

    # === JavaScript ===
    js = """// No specific JavaScript interactions shown in the tutorial for this component.
// CSS handles all hover effects and layout.
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

