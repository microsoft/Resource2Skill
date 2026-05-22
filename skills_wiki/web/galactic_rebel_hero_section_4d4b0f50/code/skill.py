import os
import base64

def create_component(
    output_dir: str,
    title_text: str = "IT'S YOUR UNIVERSE, IT'S TIME TO SAVE IT",
    body_text: str = "The Rebel Alliance is fighting to get rid of the evil empire. Join the resistance to create a better future for your children.",
    button_text: str = "JOIN NOW FOR FREE",
    logo_text: str = "Rebel Alliance",
    social_proof_text: str = "Obi Wan and 4,000 others have already joined.",
    color_scheme: str = "dark",  # "dark" or "light"
    accent_color: str = "#FF0000",  # CSS hex color for accent (red for Rebel Alliance)
    width_px: int = 1280,
    height_px: int = 720,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the "Galactic Rebel Hero Section" visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#0A0A1A"
        text_color = "#FFFFFF"
        sub_text_color = "#CCCCCC"
        ghost_button_border_color = "#FFFFFF"
        footer_bg_color = "rgba(0,0,0,0.5)"
    else:
        bg_color = "#F8F9FA"
        text_color = "#1A1A2E"
        sub_text_color = "#495057"
        ghost_button_border_color = "#1A1A2E"
        footer_bg_color = "rgba(255,255,255,0.7)"

    # Base64 encoded Rebel Alliance logo (simple Starbird icon)
    rebel_logo_svg_base64 = base64.b64encode(b"""<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
      <path fill="red" d="M50 0C22.386 0 0 22.386 0 50s22.386 50 50 50 50-22.386 50-50S77.614 0 50 0zm0 18.75c17.29 0 31.25 13.96 31.25 31.25S67.29 81.25 50 81.25 18.75 67.29 18.75 50 32.71 18.75 50 18.75zM50 31.25c-10.355 0-18.75 8.395-18.75 18.75S39.645 68.75 50 68.75 68.75 60.355 68.75 50 60.355 31.25 50 31.25z"/>
    </svg>""").decode('utf-8')

    # Image URLs for public domain/free use assets (for main visuals)
    space_bg_url = "https://images.unsplash.com/photo-1506443171337-88981ef0e85a?ixlib=rb-1.2.1&auto=format&fit=crop&w=1920&q=80"
    xwing_url = "https://www.pngall.com/wp-content/uploads/5/Star-Wars-X-Wing-PNG-Image.png"
    death_star_url = "https://png.pngtree.com/png-clipart/20230206/original/pngtree-death-star-png-image_8944594.png"
    
    # Generic profile photos
    profile_photo_1 = "https://via.placeholder.com/30/0000FF/FFFFFF?text=P1"
    profile_photo_2 = "https://via.placeholder.com/30/FF00FF/FFFFFF?text=P2"
    profile_photo_3 = "https://via.placeholder.com/30/00FF00/FFFFFF?text=P3"

    # Generic "As Seen On" logos
    cnn_logo = "https://via.placeholder.com/80x30/FFFFFF/000000?text=CNN"
    fox_logo = "https://via.placeholder.com/80x30/FFFFFF/000000?text=FOX"
    abc_logo = "https://via.placeholder.com/80x30/FFFFFF/000000?text=ABC"
    cw_logo = "https://via.placeholder.com/80x30/FFFFFF/000000?text=CW"


    # === CSS ===
    css = f"""
/* Galactic Rebel Hero Section — generated component */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Oswald:wght@700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-primary: {bg_color};
    --text-primary: {text_color};
    --text-secondary: {sub_text_color};
    --accent-color: {accent_color};
    --ghost-btn-border: {ghost_button_border_color};
    --footer-bg: {footer_bg_color};
    --section-width: {width_px}px;
    --section-height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg-primary);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden; /* Hide overflow from absolute positioned images */
}}

.hero-section {{
    width: var(--section-width);
    height: var(--section-height);
    position: relative;
    background-image: linear-gradient(
        90deg, 
        rgba(10,10,26,0.9) 0%, 
        rgba(10,10,26,0.6) 50%, 
        rgba(10,10,26,0) 100%
    ), url('{space_bg_url}');
    background-size: cover;
    background-position: center;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    padding: 2.5rem; /* ~40px */
    color: var(--text-primary);
}}

.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    padding-bottom: 2rem;
    z-index: 10;
}}

.logo-container {{
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

.rebel-logo {{
    height: 30px;
    width: 30px;
    fill: var(--accent-color);
}}

.logo-text {{
    font-size: 1.5rem; /* ~24px */
    font-weight: 700;
    color: var(--text-primary);
    text-decoration: none;
}}

.nav-links {{
    display: flex;
    gap: 1.25rem; /* ~20px */
}}

.nav-links a {{
    color: var(--text-primary);
    text-decoration: none;
    font-weight: 500;
    padding: 0.5rem 0.75rem;
    border-radius: 5px;
    transition: background-color 0.3s ease-in-out;
}}

.nav-links a:hover {{
    background-color: rgba(255, 255, 255, 0.1);
}}

.nav-button {{
    padding: 0.6rem 1.25rem;
    border-radius: 5px;
    font-size: 1rem;
    font-weight: 600;
    text-decoration: none;
    cursor: pointer;
    transition: background-color 0.3s ease-in-out, border-color 0.3s ease-in-out, color 0.3s ease-in-out;
}}

.nav-button.filled {{
    background: var(--accent-color);
    color: var(--text-primary);
    border: none;
}}

.nav-button.filled:hover {{
    background-color: darken(var(--accent-color), 10%);
}}

.nav-button.ghost {{
    background: transparent;
    color: var(--text-primary);
    border: 1px solid var(--ghost-btn-border);
}}

.nav-button.ghost:hover {{
    background-color: rgba(255, 255, 255, 0.1);
    border-color: var(--text-primary);
}}

.hero-content-wrapper {{
    width: 100%;
    display: flex;
    justify-content: flex-start;
    align-items: flex-end; /* Align bottom elements */
    flex-grow: 1; /* Take up available space */
    padding-bottom: 2rem;
    position: relative;
    z-index: 5;
}}

.hero-content {{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 1.25rem; /* ~20px */
    max-width: 50%; /* Adjust as needed to avoid image overlap */
    padding-left: 2rem;
}}

.hero-title {{
    font-family: 'Oswald', sans-serif;
    font-size: 3.8rem; /* ~60px */
    line-height: 1.1;
    color: var(--text-primary);
    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    margin-bottom: 0.5rem;
}}

.hero-text {{
    font-size: 1.125rem; /* ~18px */
    max-width: 550px;
    color: var(--text-secondary);
}}

.main-cta-button {{
    background: var(--accent-color);
    color: var(--text-primary);
    padding: 1rem 1.875rem; /* ~16px 30px */
    border: none;
    border-radius: 5px;
    font-size: 1.25rem; /* ~20px */
    font-weight: 600;
    cursor: pointer;
    text-decoration: none;
    display: inline-block;
    transition: background-color 0.3s ease-in-out;
    margin-top: 1rem;
}}

.main-cta-button:hover {{
    background-color: darken(var(--accent-color), 15%);
}}

.social-proof {{
    display: flex;
    align-items: center;
    gap: 0.625rem; /* ~10px */
    margin-top: 1.25rem;
    font-size: 0.875rem; /* ~14px */
    color: var(--text-secondary);
}}

.profile-img {{
    width: 2.25rem; /* ~36px */
    height: 2.25rem; /* ~36px */
    border-radius: 50%;
    border: 2px solid var(--text-primary);
    object-fit: cover;
}}

.x-wing-img, .death-star-img {{
    position: absolute;
    z-index: 1;
    pointer-events: none; /* Allows clicks to pass through to underlying elements */
}}

.x-wing-img {{
    width: 450px; /* Adjust size */
    right: 5%;
    bottom: 20%;
    transform: rotate(-15deg);
    filter: drop-shadow(0 0 15px rgba(var(--accent-color), 0.7));
}}

.death-star-img {{
    width: 350px; /* Adjust size */
    right: 0%;
    top: 5%;
    transform: rotate(25deg);
    filter: drop-shadow(0 0 10px rgba(0,0,0,0.7));
}}

.as-seen-on {{
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 2rem; /* ~30px */
    padding: 1.25rem 2.5rem;
    background: var(--footer-bg);
    margin-top: auto;
    z-index: 10;
}}

.as-seen-on-logo {{
    height: 1.875rem; /* ~30px */
    filter: grayscale(100%) brightness(200%);
    opacity: 0.7;
    object-fit: contain;
}}

/* Responsive adjustments */
@media (max-width: 768px) {{
    .hero-section {{
        padding: 1.5rem;
        height: auto; /* Allow height to adjust */
    }}
    .navbar {{
        flex-direction: column;
        gap: 1rem;
    }}
    .nav-links {{
        flex-wrap: wrap;
        justify-content: center;
        gap: 0.8rem;
    }}
    .hero-content {{
        max-width: 100%;
        text-align: center;
        align-items: center;
        padding-left: 0;
    }}
    .hero-title {{
        font-size: 2.5rem;
    }}
    .hero-text {{
        font-size: 1rem;
    }}
    .x-wing-img, .death-star-img {{
        position: relative;
        transform: none !important;
        margin-top: 1rem;
        right: auto;
        bottom: auto;
        top: auto;
        width: 80%; /* Make images smaller and centered */
        max-width: 300px;
        order: -1; /* Place images above text on small screens */
    }}
    .hero-content-wrapper {{
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }}
    .social-proof {{
        flex-wrap: wrap;
        justify-content: center;
    }}
    .as-seen-on {{
        flex-wrap: wrap;
        gap: 1rem;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Oswald:wght@700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <section class="hero-section" role="region" aria-label="Hero Section">
        <header class="navbar">
            <a href="#" class="logo-container" aria-label="{logo_text} Home">
                <svg class="rebel-logo" dangerouslySetInnerHTML={{ __html: "<!-- inline svg -->" }}><use xlink:href="#rebel-logo-path"></use></svg>
                <img src="data:image/svg+xml;base64,{rebel_logo_svg_base64}" alt="Rebel Alliance Logo" class="rebel-logo">
                <span class="logo-text">{logo_text}</span>
            </a>
            <nav class="nav-links" aria-label="Main Navigation">
                <a href="#" role="button">Our Ships</a>
                <a href="#" role="button">Mission</a>
                <a href="#" role="button">Donations</a>
                <a href="#" class="nav-button ghost" role="button">JOIN NOW</a>
            </nav>
        </header>

        <div class="hero-content-wrapper">
            <img src="{death_star_url}" alt="Destroyed Death Star" class="death-star-img" aria-hidden="true">
            <img src="{xwing_url}" alt="X-Wing Starfighter" class="x-wing-img" aria-hidden="true">
            
            <div class="hero-content">
                <h1 class="hero-title">{title_text}</h1>
                <p class="hero-text">{body_text}</p>
                <a href="#" class="main-cta-button" role="button">{button_text}</a>
                <div class="social-proof">
                    <img src="{profile_photo_1}" alt="Obi Wan Profile Photo" class="profile-img">
                    <img src="{profile_photo_2}" alt="Profile Photo" class="profile-img">
                    <img src="{profile_photo_3}" alt="Profile Photo" class="profile-img">
                    <span>{social_proof_text}</span>
                </div>
            </div>
        </div>

        <footer class="as-seen-on" role="contentinfo">
            <span>As Seen On:</span>
            <img src="{cnn_logo}" alt="CNN Logo" class="as-seen-on-logo">
            <img src="{fox_logo}" alt="FOX Logo" class="as-seen-on-logo">
            <img src="{abc_logo}" alt="ABC Logo" class="as-seen-on-logo">
            <img src="{cw_logo}" alt="CW Logo" class="as-seen-on-logo">
        </footer>
    </section>
</body>
</html>"""

    # === JavaScript ===
    js = f"""
// Galactic Rebel Hero Section — interactive behavior (minimal for static design)
document.addEventListener('DOMContentLoaded', () => {{
    // No specific interactive behaviors are required for the core static visual effect
    // as demonstrated in the final output of the tutorial video.
    // Add custom JavaScript here for dynamic elements or animations if needed.
}});
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

