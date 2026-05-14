def create_component(
    output_dir: str,
    title_text: str = "WELCOME TO MY FIRST WEBSITE",
    paragraph_text: str = "Nam interdum felis at felis placerat, sed varius massa ultricies. Integer quis nisi non dolor scelerisque efficitur at sed turpis.",
    button_text: str = "MY WORK",
    quote1_text: str = "“The more that you read, the more things you will know. The more that you learn, the more places you’ll go.” — Dr. Seuss",
    quote2_text: str = "“For the best return on your money, pour your purse into your head.” — Benjamin Franklin",
    color_scheme: str = "dark",  # "dark" or "light"
    accent_color: str = "#c13584",  # CSS hex color for accent (Magenta/Purple)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Hero Section with Layered Background and Flexible Content Zones visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color_main = "#1A253A"  # Dark blue for main hero section
        bg_color_body_pattern = "#1d1d1d" # Dark gray for overall body, underlying pattern
        text_color = "#ffffff"
        header_bg_color = "#ffffff" # White for header
        header_text_color = "#1a1a2e" # Dark for header text
        button_hover_color = "#9e2f6e" # Darker accent
    else: # Light scheme - inverted versions
        bg_color_main = "#e5eaf5" # Lighter blue for main hero section
        bg_color_body_pattern = "#cccccc" # Lighter gray for overall body
        text_color = "#1a1a2e"
        header_bg_color = "#1a1a2e"
        header_text_color = "#ffffff"
        button_hover_color = "#8b2a5f" # Darker accent

    # === CSS ===
    css = f"""/* Responsive Hero Section with Layered Background and Flexible Content Zones — generated component */
@import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-main: {bg_color_main};
    --bg-body-pattern: {bg_color_body_pattern};
    --text: {text_color};
    --accent: {accent_color};
    --accent-hover: {button_hover_color};
    --header-bg: {header_bg_color};
    --header-text: {header_text_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Roboto', sans-serif;
    background-color: var(--bg-body-pattern); /* Base background for the pattern */
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column; /* Ensure header and main stack vertically */
    overflow-x: hidden; /* Prevent horizontal scroll from positioning */
}}

/* Header Styling (from previous lessons in tutorial, simplified) */
.header-main {{
    position: fixed;
    top: 0;
    width: 100%;
    height: 60px;
    background-color: var(--header-bg);
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 20px;
    z-index: 1000; /* Ensure header is on top */
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}}

.header-main-logo img {{
    height: 40px; /* Example logo height */
    /*filter: invert(var(--color-scheme-invert, 0)); /* Adjust logo color based on scheme */
}}

.header-main-nav ul {{
    list-style: none;
    display: flex;
}}

.header-main-nav li a {{
    color: var(--header-text);
    text-decoration: none;
    padding: 10px 15px;
    font-weight: 500;
    transition: color 0.3s ease;
}}

.header-main-nav li a:hover {{
    color: var(--accent);
}}

/* Main Hero Section Styling */
main {{
    width: 100%;
    height: calc(100vh - 60px); /* Full viewport height minus header height */
    margin-top: 60px; /* Push content down below fixed header */
    background-color: var(--bg-main);
    background-image: url('img/Portrait.png'), url('img/BG.png'); /* Layered backgrounds: portrait on top of pattern */
    background-size: 70vh, cover; /* Adjust portrait size based on viewport height, cover pattern */
    background-repeat: no-repeat, no-repeat; /* No repeating for both */
    background-position: bottom center, center; /* Portrait at bottom center, pattern centered */
    display: flex;
    justify-content: center; /* Center content horizontally */
    align-items: center; /* Center content vertically */
    column-gap: 20vh; /* Gap between intro and quotes, relative to viewport height */
    z-index: 100; /* Ensure main content is behind header on scroll */
}}

/* Content Blocks within Main */
.main-intro, .main-quotes {{
    position: relative; /* For fine-tuned positioning within flex container */
    max-width: 500px; /* Limit width of content blocks */
    padding-bottom: 8vh; /* Space from bottom for content inside */
}}

/* Specific positioning for intro and quotes using relative offsets */
.main-intro {{
    right: 20vh; /* Push intro section towards the left */
}}

.main-quotes {{
    left: 4vh; /* Push quotes section towards the right */
}}

/* Text Styling */
h1 {{
    font-size: 96px;
    line-height: 106px;
    color: var(--text);
    font-family: 'Roboto', sans-serif;
    font-weight: 600;
    text-transform: uppercase;
}}

.main-intro p {{
    font-size: 18px;
    line-height: 30px;
    color: var(--text);
    font-family: 'Roboto', sans-serif;
    font-weight: 400; /* Default weight for paragraphs */
}}

/* Quote specific styling */
.main-quotes p {{
    font-size: 18px; /* Maintain font size */
    line-height: 30px; /* Maintain line height */
    border-left: 4px solid var(--accent); /* Accent border on left */
    padding-left: 20px; /* Space between border and text */
    margin: 40px 0; /* Vertical margin between quotes */
}}

.main-quotes p:nth-child(2) {{ /* Target the second paragraph (second quote) */
    margin-left: 100px; /* Push the second quote further right for visual separation */
}}

/* Button Styling */
.main-intro a {{
    font-size: 18px;
    display: block; /* Make it a block element to apply padding/width */
    background-color: var(--accent);
    color: var(--text);
    text-decoration: none;
    padding: 10px 20px;
    width: fit-content; /* Fit content for the button width */
    margin-top: 30px; /* Space above the button */
    border-radius: 5px;
    transition: background-color 0.3s ease;
}}

.main-intro a:hover {{
    background-color: var(--accent-hover);
}}

/* Line breaks for styling purpose (as used in tutorial) */
.br-line {{
    display: block;
}}
"""

    # === HTML ===
    # Adjusted HTML to use <span> with class for line breaks within H1 and P,
    # as <br> tags were problematic for direct string replacement in the original approach.
    # Added social media links (though not explicitly styled beyond the nav)
    # The image paths are relative to the img_dir.
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dani Krossing Portfolio</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="header-main">
        <div class="header-main-logo">
            <img src="img/logo.png" alt="imagon logo">
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
            <a href="https://www.facebook.com"><img src="img/facebook-color.png" alt="Facebook"></a>
            <a href="https://www.instagram.com"><img src="img/instagram-color.png" alt="Instagram"></a>
        </div>
    </header>

    <main>
        <div class="main-intro">
            <h1>{title_text.replace(' ', ' ').replace('TO MY FIRST', '<span class="br-line"></span>TO MY FIRST').replace('WEBSITE', '<span class="br-line"></span>WEBSITE')}</h1>
            <p>{paragraph_text.replace(';', '; <span class="br-line"></span>')}</p>
            <a href="#">{button_text}</a>
        </div>
        <div class="main-quotes">
            <p>{quote1_text.replace('Dr. Seuss', '<span class="br-line"></span>Dr. Seuss')}</p>
            <p>{quote2_text.replace('Benjamin Franklin', '<span class="br-line"></span>Benjamin Franklin')}</p>
        </div>
    </main>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    # No custom JS required for this specific visual reproduction.
    js = """// No custom JavaScript needed for this component's visual effects.
"""

    # === Write files ===
    files = []
    # Create dummy image files if they don't exist for local testing
    img_dir = os.path.join(output_dir, "img")
    os.makedirs(img_dir, exist_ok=True)

    # Dummy image content (1x1 transparent GIF)
    dummy_gif_content = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
    # For a simple pattern, a small textured image would be better than 1x1
    # For the portrait, a placeholder image of a person.

    # Ensure img/logo.png exists
    logo_path = os.path.join(img_dir, "logo.png")
    if not os.path.exists(logo_path):
        with open(logo_path, "wb") as f:
            f.write(dummy_gif_content) # Placeholder
    files.append(logo_path)

    # Ensure img/BG.png exists (pattern background)
    bg_pattern_path = os.path.join(img_dir, "BG.png")
    if not os.path.exists(bg_pattern_path):
        # Using a slightly different dummy to represent a pattern
        with open(bg_pattern_path, "wb") as f:
            f.write(dummy_gif_content) # Placeholder
    files.append(bg_pattern_path)

    # Ensure img/Portrait.png exists
    portrait_path = os.path.join(img_dir, "Portrait.png")
    if not os.path.exists(portrait_path):
        with open(portrait_path, "wb") as f:
            f.write(dummy_gif_content) # Placeholder
    files.append(portrait_path)
    
    # Dummy social icons
    fb_icon_path = os.path.join(img_dir, "facebook-color.png")
    if not os.path.exists(fb_icon_path):
        with open(fb_icon_path, "wb") as f:
            f.write(dummy_gif_content)
    files.append(fb_icon_path)

    ig_icon_path = os.path.join(img_dir, "instagram-color.png")
    if not os.path.exists(ig_icon_path):
        with open(ig_icon_path, "wb") as f:
            f.write(dummy_gif_content)
    files.append(ig_icon_path)


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
