def create_component(
    output_dir: str,
    title_text: str = "WELCOME<br>TO MY FIRST<br>WEBSITE",
    body_text: str = "Nam interdum felis at felis placerat, sed varius<br>massa ultricies. Integer quis nisi non<br>dolor<br>scelerisque efficitur at sed turpis.",
    quote1_text: str = "\"The more that you read, the more<br>things you will know. The more that<br>you learn, the more places you'll go.\"<br>- Dr. Seuss",
    quote2_text: str = "\"For the best return on your<br>money, pour your purse<br>into your head.\"<br>- Benjamin Franklin",
    button_text: str = "MY WORK",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#c13584",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Dual-Panel Hero Section with Overlaid Portrait visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#1A253A"  # Dark blue from video
        text_color = "#ffffff"
        header_bg_color = "#ffffff"
        header_text_color = "#333333"
        accent_hover_color = "#9e2f6e" # Darker magenta
        pattern_bg_path = "img/BG.png" # Assuming pattern.png for background pattern
        portrait_img_path = "img/portrait.png" # Assuming portrait.png for main image
    else: # Light theme (inverted from dark, not explicitly in video but follows scheme)
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        header_bg_color = "#f8f9fa"
        header_text_color = "#1a1a2e"
        accent_hover_color = "#a00050" # Darker magenta
        pattern_bg_path = "img/BG.png" # Use same pattern, maybe with filter
        portrait_img_path = "img/portrait.png"

    # Create dummy image files if they don't exist
    for img_path in [pattern_bg_path, portrait_img_path]:
        full_img_path = os.path.join(output_dir, img_path)
        os.makedirs(os.path.dirname(full_img_path), exist_ok=True)
        if not os.path.exists(full_img_path):
            from PIL import Image
            img_type = img_path.split('/')[-1].split('.')[0]
            if img_type == 'BG':
                # Create a simple repeating pattern
                img_size = (100, 100)
                img = Image.new('RGBA', img_size, (26, 37, 58, 255)) # Dark blue from video
                for x in range(0, img_size[0], 10):
                    for y in range(0, img_size[1], 10):
                        if (x // 10 + y // 10) % 2 == 0:
                            ImageDraw.Draw(img).rectangle([x, y, x + 10, y + 10], fill=(51, 65, 85, 255)) # Darker blue square
                img.save(full_img_path)
            elif img_type == 'portrait':
                # Create a simple silhouette or placeholder image
                img_size = (400, 600)
                img = Image.new('RGBA', img_size, (0, 0, 0, 0)) # Transparent background
                ImageDraw.Draw(img).rectangle([50, 50, 350, 550], fill=(0, 0, 0, 255)) # Black rectangle for silhouette
                img.save(full_img_path)


    # === CSS ===
    css = f"""/* Responsive Dual-Panel Hero Section with Overlaid Portrait — generated component */
@import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --accent-hover: {accent_hover_color};
    --header-bg: {header_bg_color};
    --header-text: {header_text_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Roboto', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    overflow-x: hidden; /* Prevent horizontal scroll from relative positioning */
}}

/* Header styling (fixed from previous lessons) */
.header-main {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 60px; /* Assuming 60px height from video */
    background-color: var(--header-bg);
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 20px;
    z-index: 1000;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}}
.header-main-logo img {{
    height: 40px; /* Adjust logo size */
}}
.header-main-nav ul {{
    list-style: none;
    display: flex;
}}
.header-main-nav li {{
    margin-left: 20px;
}}
.header-main-nav a {{
    text-decoration: none;
    color: var(--header-text);
    font-weight: 500;
}}
.header-main-sa a {{
    text-decoration: none;
    color: var(--header-text);
    margin-left: 15px;
}}


main {{
    width: 100%;
    height: calc(100vh - 60px); /* Adjust for fixed header height */
    margin-top: 60px; /* Push main content below fixed header */
    background-color: var(--bg);
    display: flex;
    justify-content: center;
    align-items: center;
    column-gap: 20vh; /* Responsive gap between flex items */
    position: relative; /* Needed for z-index context */
    z-index: 100; /* Ensure main content is above potential background elements but below header */

    background-image: url('../{portrait_img_path}'), url('../{pattern_bg_path}');
    background-size: 70vh, cover; /* Portrait 70vh, pattern covers */
    background-repeat: no-repeat, repeat; /* Portrait no-repeat, pattern repeats */
    background-position: bottom center, center; /* Portrait at bottom center, pattern centered */
}}

h1 {{
    font-size: 96px;
    line-height: 106px;
    color: var(--text);
    font-weight: 600;
    text-transform: uppercase;
}}

p {{
    font-size: 18px;
    line-height: 30px;
    color: var(--text);
    font-weight: 400;
}}

a {{
    cursor: pointer;
    font-size: 18px;
    line-height: 30px;
    color: var(--text);
    font-weight: 400;
    text-decoration: none;
}}

.main-intro {{
    position: relative; /* For fine positioning */
    right: 20vh; /* Shift left panel to the left */
    padding-bottom: 8vh; /* Push content up slightly from bottom */
}}

.main-intro h1 {{
    /* Using specific style from default.css to override */
    font-size: 96px; /* Specific override for this h1 */
    line-height: 106px;
}}

.main-intro p {{
    margin-bottom: 30px; /* Space between paragraph and button */
}}

.main-intro a {{
    display: block;
    width: fit-content;
    background-color: var(--accent);
    padding: 10px 20px;
    border-radius: 5px;
    transition: background-color 0.3s ease;
}}

.main-intro a:hover {{
    background-color: var(--accent-hover);
}}

.main-quotes {{
    position: relative; /* For fine positioning */
    left: 4vh; /* Shift right panel to the right */
    padding-bottom: 8vh; /* Push content up slightly from bottom */
}}

.main-quotes p {{
    border-left: 4px solid var(--accent);
    padding-left: 20px;
    margin: 40px 0; /* Space between quotes */
}}

.main-quotes p:nth-child(2) {{
    margin-left: 100px; /* Indent second quote */
}}

/* Responsive adjustments */
@media (max-width: 768px) {{
    main {{
        flex-direction: column; /* Stack panels vertically on smaller screens */
        column-gap: 0;
        padding-top: 20px;
    }}
    .main-intro, .main-quotes {{
        position: static; /* Remove relative positioning offsets */
        text-align: center;
        padding-bottom: 20px;
    }}
    .main-intro h1 {{
        font-size: 64px; /* Adjust h1 size for smaller screens */
        line-height: 72px;
    }}
    .main-intro p, .main-intro a {{
        margin-left: auto;
        margin-right: auto;
    }}
    .main-quotes p {{
        margin-left: auto;
        margin-right: auto;
    }}
    .main-quotes p:nth-child(2) {{
        margin-left: auto; /* Center second quote as well */
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hero Section</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="header-main">
        <div class="header-main-logo">
            <img src="https://via.placeholder.com/60x40.png?text=LOGO" alt="Logo">
        </div>
        <nav class="header-main-nav">
            <ul>
                <li><a href="#">HOME</a></li>
                <li><a href="#">GALLERY</a></li>
                <li><a href="#">ABOUT US</a></li>
                <li><a href="#">CONTACT</a></li>
            </ul>
        </nav>
        <div class="header-main-sa">
            <a href="https://www.facebook.com">FB</a>
            <a href="https://www.instagram.com">IG</a>
        </div>
    </header>

    <main>
        <div class="main-intro">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <a href="#">{button_text}</a>
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
    js = f"""// Responsive Dual-Panel Hero Section with Overlaid Portrait — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    // No specific JavaScript interactions required for the core visual effect as described in the tutorial.
    // CSS handles all layout, styling, and hover effects.
}});
"""

    # === Write files ===
    files = []
    from PIL import Image, ImageDraw
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
