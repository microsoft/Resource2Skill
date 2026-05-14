def create_component(
    output_dir: str,
    title_text: str = "WELCOME TO MY FIRST WEBSITE",
    intro_body_text: str = "Nam interdum felis at felis placerat, sed varius massa ultricies. Integer quis nisi non dolor scelerisque efficitur at sed turpis.",
    link_text: str = "MY WORK",
    quote1_text: str = "“The more that you read, the more things you will know. The more that you learn, the more places you'll go.”<br><br>Dr. Seuss",
    quote2_text: str = "“For the best return on your money, pour your purse into your head.”<br><br>Benjamin Franklin",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#C13584",     # CSS hex color for accent
    width_px: int = 1920,              # Target width for full-screen desktop
    height_px: int = 1080,             # Target height for full-screen desktop
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Flexbox Hero Section with Layered Background and Offset Content visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_main_color = "#1A253A"
        text_color = "#FFFFFF"
        header_bg_color = "#FFFFFF"
        # The main.css has a default background-color for body, but the hero section overrides it.
        # This dark tone for the body matches the original video's empty canvas before styling.
        body_bg_color = "#1D1D1D"
    else:
        bg_main_color = "#E0E8F0"
        text_color = "#1A1A2E"
        header_bg_color = "#FFFFFF" # Assuming header remains white
        body_bg_color = "#F8F9FA"

    # Define common paths for images (assuming they are in output_dir/img)
    img_dir_relative = "img"
    bg_pattern_img = f"{img_dir_relative}/BG.png" # Assuming BG.png is the pattern
    portrait_img = f"{img_dir_relative}/Portrait.png" # Assuming Portrait.png is the portrait


    # === CSS ===
    css = f"""/* Flexbox Hero Section with Layered Background and Offset Content — generated component */
@import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --site-color-01: {accent_color};
    --site-color-01-hover: #9E2F6E; /* Slightly darker accent color for hover */
}}

body {{
    font-family: 'Roboto', sans-serif;
    background-color: {body_bg_color};
    color: {text_color};
    min-height: 100vh;
}}

h1 {{
    font-size: 26px;
    line-height: 32px;
    color: {text_color};
    font-family: 'Roboto', sans-serif;
    font-weight: 600;
    text-transform: uppercase;
}}

p {{
    font-size: 18px;
    line-height: 30px;
    color: {text_color};
    font-family: 'Roboto', sans-serif;
}}

a {{
    font-size: 18px;
    line-height: 30px;
    color: {text_color};
    font-family: 'Roboto', sans-serif;
    cursor: pointer;
}}

.header-main {{
    position: fixed;
    top: 0;
    width: 100%;
    height: 60px; /* Fixed height for the header */
    background-color: {header_bg_color};
    display: flex;
    justify-content: space-between;
    z-index: 1000; /* Ensure header is above other content */
    padding-left: 20px;
    padding-right: 20px;
    align-items: center;
}}

.header-main-logo img {{
    height: 40px; /* Adjust logo height */
}}

.header-main-nav ul {{
    list-style: none;
    display: flex;
    gap: 20px;
}}

.header-main-nav a {{
    text-decoration: none;
    color: #333; /* Darker color for nav links */
    font-weight: 500;
    transition: color 0.3s ease;
}}

.header-main-nav a:hover {{
    color: var(--site-color-01);
}}

.header-main-sm {{
    display: flex;
    gap: 15px;
}}

.header-main-sm div {{
    width: 30px;
    height: 30px;
    background-size: cover;
    background-position: center;
    border-radius: 50%;
}}

/* Main Hero Section Styling */
main {{
    width: 100%;
    /* Calculate height to account for the fixed header */
    height: calc(100vh - 60px); 
    background-color: {bg_main_color};
    background-image: url(../{portrait_img}), url(../{bg_pattern_img});
    background-size: 70vh, cover; /* 70vh for portrait, cover for pattern */
    background-repeat: no-repeat, repeat; /* No repeat for portrait, repeat for pattern */
    background-position: bottom center, center; /* Position portrait at bottom center, pattern centered */
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 60px; /* Push content down to avoid overlapping with fixed header */
    z-index: 100; /* Ensure main content is above background images */
}}

/* Styling for the main content blocks inside the hero */
main .main-intro {{
    position: relative;
    right: 20vh; /* Shift intro block to the left relative to its flex position */
    padding-bottom: 8vh; /* Push content up slightly from the bottom */
}}

main .main-intro h1 {{
    font-size: 96px;
    line-height: 106px;
}}

main .main-intro p {{
    margin-top: 20px;
    max-width: 450px;
}}

main .main-intro a {{
    display: block;
    background-color: var(--site-color-01);
    padding: 10px 20px;
    width: fit-content;
    margin-top: 30px;
    text-decoration: none;
    transition: background-color 0.3s ease;
}}

main .main-intro a:hover {{
    background-color: var(--site-color-01-hover);
}}

main .main-quotes {{
    position: relative;
    left: 4vh; /* Shift quotes block to the right relative to its flex position */
    padding-bottom: 8vh; /* Push content up slightly from the bottom */
}}

main .main-quotes p {{
    border-left: 4px solid var(--site-color-01);
    padding-left: 20px;
    margin: 40px 0;
}}

main .main-quotes p:nth-child(2) {{
    margin-left: 100px; /* Offset the second quote further */
}}

main .main-quotes p:nth-child(2) {{
    margin-left: 100px; /* This is a repeat, ensure only one rule is active */
}}
"""
    # Fix CSS for the nth-child(2) as it's a repeat in the original snippet
    css = css.replace("main .main-quotes p:nth-child(2) {\n    margin-left: 100px; /* This is a repeat, ensure only one rule is active */\n}", "")
    css += f"""
main .main-quotes p:nth-child(2) {{
    margin-left: 100px;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dani Krossing Portfolio</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="header-main">
        <div class="header-main-logo">
            <img src="{img_dir_relative}/logo.png" alt="imagon logo">
        </div>
        <nav class="header-main-nav">
            <ul>
                <li><a href="index.html">HOME</a></li>
                <li><a href="#">GALLERY</a></li>
                <li><a href="#">ABOUT US</a></li>
                <li><a href="#">CONTACT</a></li>
            </ul>
        </nav>
        <div class="header-main-sm">
            <a href="www.facebook.com">
                <div class="header-main-sm-fb"></div>
            </a>
            <a href="www.instagram.com">
                <div class="header-main-sm-in"></div>
            </a>
        </div>
    </header>

    <main>
        <div class="main-intro">
            <h1>{title_text.replace("MY FIRST", "<br>MY FIRST").replace("WEBSITE", "<br>WEBSITE")}</h1>
            <p>{intro_body_text.replace("ultricies.", "ultricies.<br>").replace("non", "non<br>")}</p>
            <a href="#">{link_text}</a>
        </div>

        <div class="main-quotes">
            <p>{quote1_text}</p>
            <p>{quote2_text}</p>
        </div>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    # No custom JS provided in the tutorial for the hero section interaction, but including the file.
    js = """// No specific JavaScript for the hero section was demonstrated in the tutorial.
// This file is included for completeness.
"""
    # Create dummy image files if they don't exist, for local testing without actual images
    # In a real scenario, these would be provided by the user or part of the project assets.
    # For automated execution, the user is responsible for providing images or
    # these paths can be ignored if the agent only checks HTML/CSS correctness.
    dummy_img_dir = os.path.join(output_dir, img_dir_relative)
    os.makedirs(dummy_img_dir, exist_ok=True)
    
    # Placeholder images to avoid broken links
    dummy_logo_path = os.path.join(dummy_img_dir, "logo.png")
    if not os.path.exists(dummy_logo_path):
        with open(dummy_logo_path, "wb") as f:
            # A tiny transparent PNG
            f.write(b'\\x89PNG\\r\\n\\x1a\\n\\x00\\x00\\x00\\rIHDR\\x00\\x00\\x00\\x01\\x00\\x00\\x00\\x01\\x08\\x06\\x00\\x00\\x00\\x1f\\x15\\xc4\\x89\\x00\\x00\\x00\\x0cIDATx\\xda\\xed\\xc1\\x01\\x01\\x00\\x00\\x00\\xc2\\xa0\\xf7Om\\x00\\x00\\x00\\x00IEND\\xaeB`\\x82')
    
    dummy_bg_path = os.path.join(dummy_img_dir, "BG.png")
    if not os.path.exists(dummy_bg_path):
        # A tiny black PNG, representing the pattern
        with open(dummy_bg_path, "wb") as f:
            f.write(b'\\x89PNG\\r\\n\\x1a\\n\\x00\\x00\\x00\\rIHDR\\x00\\x00\\x00\\x01\\x00\\x00\\x00\\x01\\x08\\x00\\x00\\x00\\x00\\x2d\\x1a\\xbf\\x76\\x00\\x00\\x00\\x0cIDATx\\xda\\xed\\xc1\\x01\\x01\\x00\\x00\\x00\\xc2\\xa0\\xf7Om\\x00\\x00\\x00\\x00IEND\\xaeB`\\x82')

    dummy_portrait_path = os.path.join(dummy_img_dir, "Portrait.png")
    if not os.path.exists(dummy_portrait_path):
        # Another tiny black PNG, representing the portrait
        with open(dummy_portrait_path, "wb") as f:
            f.write(b'\\x89PNG\\r\\n\\x1a\\n\\x00\\x00\\x00\\rIHDR\\x00\\x00\\x00\\x01\\x00\\x00\\x00\\x01\\x08\\x00\\x00\\x00\\x00\\x2d\\x1a\\xbf\\x76\\x00\\x00\\x00\\x0cIDATx\\xda\\xed\\xc1\\x01\\x01\\x00\\x00\\x00\\xc2\\xa0\\xf7Om\\x00\\x00\\x00\\x00IEND\\xaeB`\\x82')
    

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

