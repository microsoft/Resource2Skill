def create_component(
    output_dir: str,
    title_text: str = "It's your universe, it's time to save it",
    body_text: str = "The Rebel Alliance is fighting to get rid of the evil empire, join the resistance to create a better future for your children.",
    color_scheme: str = "dark",        # "dark" or "light" (dark is default as per video)
    accent_color: str = "#e50914",     # Vibrant red for main CTA
    width_px: int = 1440,              # Based on typical desktop screen size
    height_px: int = 800,              # Standard hero section height
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the "Narrative Hero Section with Conversion Optimization"
    visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#1a1a2e" # Deep blue/purple from video
        text_color = "#ffffff"
        header_bg = "rgba(0, 0, 0, 0.4)" # Slightly transparent header
        social_proof_bg = "rgba(139, 0, 0, 0.5)" # Semi-transparent dark red for bottom bar
        network_logo_filter = "brightness(0) invert(1)" # White logos
        placeholder_color = "#333333"
    else: # Light scheme - adjusted for contrast but maintaining style
        bg_color = "#f0f2f5"
        text_color = "#333333"
        header_bg = "rgba(255, 255, 255, 0.7)"
        social_proof_bg = "rgba(255, 100, 100, 0.6)"
        network_logo_filter = "none" # Original color logos
        placeholder_color = "#cccccc"


    # Using a generic space background image.
    # User is expected to replace ships/death star with their own imagery.
    # Placeholder for ship/death star composition
    hero_image_url = "https://images.unsplash.com/photo-1502134259463-662580a65668?q=80&w=2670&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" # Generic space
    
    # Placeholder profile images
    profile_img_1 = "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?q=80&w=2574&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
    profile_img_2 = "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?q=80&w=2670&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
    profile_img_3 = "https://images.unsplash.com/photo-1544005313-94ddf0286df2?q=80&w=2576&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"

    # Placeholder network logos (using generic icons for demonstration)
    network_logos = [
        "https://upload.wikimedia.org/wikipedia/commons/2/22/ABC_logo_black_and_white.svg",
        "https://upload.wikimedia.org/wikipedia/commons/e/ed/Fox_broadcasting_company_logo.svg",
        "https://upload.wikimedia.org/wikipedia/commons/6/67/CNN_Logo_White.svg",
        "https://upload.wikimedia.org/wikipedia/commons/a/a2/The_CW_Television_Network_logo.svg",
    ]


    # === CSS ===
    css = f"""
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Titillium+Web:wght@700;900&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --accent-color: {accent_color};
    --header-bg: {header_bg};
    --social-proof-bg: {social_proof_bg};
    --placeholder-color: {placeholder_color};
    --network-logo-filter: {network_logo_filter};
    --hero-width: {width_px}px;
    --hero-height: {height_px}px;
}}

body {{
    font-family: 'Inter', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    margin: 0;
}}

.hero-section {{
    position: relative;
    width: var(--hero-width);
    height: var(--hero-height);
    background-image: url('{hero_image_url}');
    background-size: cover;
    background-position: center;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    text-align: center;
    overflow: hidden;
}}

/* Overlay for better text readability */
.hero-overlay {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(to right, rgba(0,0,0,0.8) 0%, rgba(0,0,0,0.4) 50%, rgba(0,0,0,0) 100%);
    pointer-events: none;
}}

/* Header Styling */
.hero-header {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 40px;
    background-color: var(--header-bg);
    backdrop-filter: blur(5px); /* Optional subtle blur for header */
    -webkit-backdrop-filter: blur(5px);
    z-index: 10;
}}

.logo-container {{
    display: flex;
    align-items: center;
    gap: 10px;
    font-family: 'Titillium Web', sans-serif;
    font-weight: 900;
    font-size: 24px;
    color: var(--text-color);
}}

.rebel-logo {{
    width: 30px;
    height: 30px;
    fill: var(--accent-color);
}}

.nav-links {{
    display: flex;
    gap: 30px;
}}

.nav-link {{
    color: var(--text-color);
    text-decoration: none;
    font-weight: 600;
    font-size: 16px;
    padding: 5px 0;
    position: relative;
    transition: color 0.3s ease;
}}

.nav-link::after {{
    content: '';
    position: absolute;
    left: 0;
    bottom: 0;
    width: 0;
    height: 2px;
    background-color: var(--accent-color);
    transition: width 0.3s ease;
}}

.nav-link:hover::after {{
    width: 100%;
}}

.main-cta-button {{
    background-color: var(--accent-color);
    color: var(--text-color);
    padding: 10px 20px;
    border-radius: 5px;
    text-decoration: none;
    font-weight: 600;
    font-size: 16px;
    border: none;
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.2s ease;
}}

.main-cta-button:hover {{
    background-color: darken(var(--accent-color), 10%); /* Placeholder for darker red */
    transform: translateY(-2px);
}}


/* Hero Content Styling */
.hero-content {{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: center;
    padding: 0 80px;
    text-align: left;
    height: 100%;
    max-width: 50%;
    position: relative;
    z-index: 5;
}}

.hero-content h1 {{
    font-family: 'Titillium Web', sans-serif;
    font-weight: 900;
    font-size: 64px;
    line-height: 1.1;
    margin-bottom: 20px;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
}}

.hero-content p {{
    font-size: 20px;
    line-height: 1.5;
    margin-bottom: 30px;
    text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.6);
}}

.primary-cta {{
    background-color: var(--accent-color);
    color: var(--text-color);
    padding: 15px 30px;
    border-radius: 8px;
    text-decoration: none;
    font-family: 'Titillium Web', sans-serif;
    font-weight: 700;
    font-size: 20px;
    border: none;
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.2s ease;
    display: flex;
    align-items: center;
    gap: 10px;
    box-shadow: 0 5px 15px rgba(var(--accent-color-rgb, 229, 9, 20), 0.4);
}}

.primary-cta:hover {{
    background-color: #c90812; /* Darker red on hover */
    transform: translateY(-3px);
}}

/* Social Proof Users */
.social-proof-users {{
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 20px;
    position: relative;
    left: 80px; /* Align with hero content */
    z-index: 5;
}}

.profile-images {{
    display: flex;
    margin-right: 10px;
}}

.profile-image {{
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: 2px solid var(--text-color);
    background-color: var(--placeholder-color);
    object-fit: cover;
    margin-right: -10px; /* Overlap effect */
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
}}

.profile-image:first-child {{
    z-index: 3;
}}
.profile-image:nth-child(2) {{
    z-index: 2;
}}
.profile-image:last-child {{
    z-index: 1;
}}

.users-joined-text {{
    font-size: 16px;
    font-weight: 400;
    text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.6);
}}

/* Social Proof Media */
.social-proof-media {{
    width: 100%;
    padding: 20px 40px;
    background-color: var(--social-proof-bg);
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 50px;
    position: relative;
    z-index: 10;
}}

.media-logo {{
    height: 30px;
    filter: var(--network-logo-filter);
    opacity: 0.7;
    transition: opacity 0.3s ease;
}}

.media-logo:hover {{
    opacity: 1;
}}

/* Placeholder for main hero visual */
.hero-visual-placeholder {{
    position: absolute;
    right: 80px;
    bottom: 100px;
    width: 500px;
    height: 300px;
    background-color: rgba(var(--placeholder-color-rgb, 51, 51, 51), 0.3); /* Semi-transparent placeholder */
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    font-style: italic;
    color: var(--text-color);
    text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    z-index: 3; /* Below text, above background image */
    background-image: url('https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Death_Star_II_in_orbit.png/1024px-Death_Star_II_in_orbit.png'); /* Death Star Placeholder */
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
}}
.hero-ship-placeholder {{
    position: absolute;
    right: 50px;
    bottom: 50px;
    width: 400px;
    height: 250px;
    background-image: url('https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/X-wing_Flight_%28Edited%29.png/1280px-X-wing_Flight_%28Edited%29.png'); /* X-Wing Placeholder */
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
    z-index: 4;
}}


/* Utility to darken color in CSS (basic approach, not fully dynamic without JS or preprocessor) */
:root {{
  --accent-color-rgb: 229, 9, 20; /* RGB for #e50914 */
  --placeholder-color-rgb: 51, 51, 51;
}}
.primary-cta:hover {{
  background-color: #c90812; /* Directly specified darker red */
}}
.main-cta-button:hover {{
  background-color: #c90812; /* Directly specified darker red */
}}

    """

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Perfect Hero Section</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Titillium+Web:wght@700;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
</head>
<body>
    <div class="hero-section">
        <div class="hero-overlay"></div>

        <header class="hero-header">
            <a href="#" class="logo-container">
                <svg class="rebel-logo" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm0 2.25c4.786 0 8.687 3.901 8.687 8.687a8.687 8.687 0 0 1-8.687 8.687A8.687 8.687 0 0 1 3.313 10.937C3.313 6.151 7.214 2.25 12 2.25zm.038 2.261L8.72 9.073l-.004-.002-3.155 3.524 3.167-.003 3.155 3.524 3.155-3.524 3.167.003-3.155-3.524-3.32-.004z"/>
                </svg>
                <span>Rebel Alliance</span>
            </a>
            <nav class="nav-links">
                <a href="#" class="nav-link">Our Ships</a>
                <a href="#" class="nav-link">Mission</a>
                <a href="#" class="nav-link">Donations</a>
                <a href="#" class="main-cta-button">JOIN NOW</a>
            </nav>
        </header>

        <div class="hero-content">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <a href="#" class="primary-cta">
                JOIN NOW FOR FREE <i class="fas fa-arrow-right"></i>
            </a>
            <div class="social-proof-users">
                <div class="profile-images">
                    <img src="{profile_img_1}" alt="Profile 1" class="profile-image">
                    <img src="{profile_img_2}" alt="Profile 2" class="profile-image">
                    <img src="{profile_img_3}" alt="Profile 3" class="profile-image">
                </div>
                <span class="users-joined-text">Obi Wan and 4,000 others have already joined</span>
            </div>
        </div>

        <div class="hero-visual-placeholder"></div>
        <div class="hero-ship-placeholder"></div>
        
        <div class="social-proof-media">
            <span style="color: var(--text-color); font-weight: 600; font-size: 16px;">As Seen On:</span>
            {''.join([f'<img src="{logo}" alt="Media Logo" class="media-logo">' for logo in network_logos])}
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""
document.addEventListener('DOMContentLoaded', () => {{
    // Simple JS for future interactive elements, or button feedback
    const primaryCta = document.querySelector('.primary-cta');
    if (primaryCta) {{
        primaryCta.addEventListener('click', (e) => {{
            console.log('Primary CTA clicked!');
            // Add custom conversion tracking or animation here
        }});
    }}

    const mainCtaButtons = document.querySelectorAll('.main-cta-button');
    mainCtaButtons.forEach(button => {{
        button.addEventListener('click', (e) => {{
            console.log('Main CTA in header clicked!');
        }});
    }});
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

