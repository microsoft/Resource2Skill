def create_component(
    output_dir: str,
    logo_text: str = "CSSsnippets",
    nav_links: list = None,
    button_text: str = "Login",
    color_scheme: str = "dark",  # "dark" or "light"
    accent_color: str = "#38bdf8",  # CSS hex color for accent
    width_px: int = 1200,  # Max-width for the overall container
    height_px: int = 800,  # Min-height for the body to display multiple navs
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Frosted Glow Navigation Bar visual effect.

    Generates five variations of the navbar layouts shown in the tutorial.
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if nav_links is None:
        nav_links = ["Home", "Services", "Portfolio", "About"]

    # --- Derive theme colors ---
    # Colors directly from the video tutorial's dark theme
    body_bg = "#0f172a"
    body_text = "#f0f0f0"
    nav_bg_rgba = "rgba(255, 255, 255, 0.05)"
    nav_border_rgba = "rgba(255, 255, 255, 0.1)"
    nav_link_color = "#e2e8f0"
    nav_button_text_color = "#0f172a"
    darker_accent_blue = "#00a9f3" # From button hover in video

    if color_scheme == "light":
        # Simple inversion for light mode - adjust as needed for optimal contrast
        body_bg = "#f0f0f0"
        body_text = "#0f172a"
        nav_bg_rgba = "rgba(0, 0, 0, 0.05)"
        nav_border_rgba = "rgba(0, 0, 0, 0.1)"
        nav_link_color = "#1a1a2e"
        nav_button_text_color = "#f0f0f0"
        # Accent colors remain the same as they are vibrant
        # darker_accent_blue = "#00a9f3"

    # Convert nav_links list to HTML list items
    all_nav_links_html = "".join([f'<li><a href="#">{link}</a></li>' for link in nav_links])
    nav_links_html_part1 = "".join([f'<li><a href="#">{link}</a></li>' for link in nav_links[:len(nav_links)//2]])
    nav_links_html_part2 = "".join([f'<li><a href="#">{link}</a></li>' for link in nav_links[len(nav_links)//2:]])

    # === CSS ===
    css = f"""
    /* Frosted Glow Navigation Bar — generated component */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    *, *::before, *::after {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}

    :root {{
        --body-bg: {body_bg};
        --body-text: {body_text};
        --accent-blue: {accent_color};
        --darker-accent-blue: {darker_accent_blue};
        --nav-bg: {nav_bg_rgba};
        --nav-border: {nav_border_rgba};
        --nav-link-color: {nav_link_color};
        --nav-button-text-color: {nav_button_text_color};
        --component-max-width: {width_px}px;
        --body-min-height: {height_px}px;
    }}

    body {{
        font-family: 'Poppins', sans-serif;
        background: var(--body-bg);
        color: var(--body-text);
        min-height: var(--body-min-height);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        overflow-x: hidden; /* Prevent horizontal scroll from padding */
        padding: 2rem; /* Added padding to make space for multiple navbars */
    }}

    h2 {{
        text-align: center;
        padding: 2rem 0 1rem;
        color: var(--accent-blue);
    }}

    .navbar-container {{
        width: 100%;
        max-width: var(--component-max-width); /* Constrain overall width */
    }}

    nav {{
        width: 100%;
        padding: 1rem 5%;
        background: var(--nav-bg);
        border-bottom: 1px solid var(--nav-border);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px); /* Safari compatibility */
        margin-bottom: 2rem; /* Spacing between navbars */
        border-radius: 8px; /* Added for a slightly cleaner look, not in video but common */
    }}

    /* Basic shared nav styles for logo, links, buttons */
    .logo {{
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--accent-blue);
        letter-spacing: 1px;
        text-decoration: none; /* In case logo is wrapped in <a> */
    }}

    .nav-links {{
        list-style: none;
        display: flex;
        gap: 2rem;
    }}

    .nav-links li a {{
        position: relative;
        font-size: 1.05rem;
        font-weight: 500;
        text-decoration: none;
        color: var(--nav-link-color);
        transition: 0.3s;
        display: inline-block; /* Essential for padding/margin on older browsers if applied */
    }}

    .nav-links li a:hover {{
        color: var(--accent-blue);
        text-shadow: 0 0 10px var(--accent-blue);
    }}

    .btns {{
        display: flex; /* To contain multiple buttons if needed */
    }}

    .btn {{
        padding: 0.5rem 1.5rem;
        border-radius: 30px;
        font-weight: 600;
        font-size: 1rem;
        background: var(--accent-blue);
        color: var(--nav-button-text-color);
        box-shadow: 0 0 15px var(--accent-blue);
        border: none;
        cursor: pointer;
        transition: 0.3s;
    }}

    .btn:hover {{
        background: var(--darker-accent-blue);
        box-shadow: 0 0 25px var(--darker-accent-blue);
    }}

    /* --- Navbar Type Specific Layouts --- */

    /* Navbar Type 1: Logo left, Links center, Button right */
    .nav-type-1 {{
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}

    /* Navbar Type 2: Logo left, Links & Button right */
    .nav-type-2 {{
        display: flex;
        align-items: center;
        justify-content: flex-end; /* Push nav-links and btns to the right */
    }}
    .nav-type-2 .logo {{
        margin-right: auto; /* Push logo to the far left */
    }}
    .nav-type-2 .nav-links {{
        margin-right: 30px; /* Spacing between links and button */
    }}

    /* Navbar Type 3: Logo & Links grouped left, Button right */
    .nav-type-3 {{
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}
    .nav-type-3 .nav-group {{ /* This is a nested flex container */
        display: flex;
        align-items: center;
        gap: 2rem; /* Spacing between logo and nav-links */
    }}

    /* Navbar Type 4: Links left, Logo center, Button right */
    .nav-type-4 {{
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}
    .nav-type-4 .logo {{
        /* Adjust margin for visual centering. This is sensitive to content width. */
        margin-left: auto; /* Pushes logo away from nav-links */
        margin-right: 15rem; /* Pushes logo away from button, as per video's manual adjustment */
    }}
    /* The nav-links implicitly gets margin-right: auto from the logo's margin-left: auto */

    /* Navbar Type 5: Links half left, Logo center, Links half right (no button) */
    .nav-type-5 {{
        display: flex;
        align-items: center;
        justify-content: center; /* Center all main children */
        gap: 3rem; /* Spacing between the two nav-links groups and the logo */
    }}
    /* No .btns div in this type's HTML */
    """

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flexbox Navbar Variations</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="navbar-container">
        <h2>Navbar Type - 1 (Logo Left, Links Center, Button Right)</h2>
        <nav class="nav-type-1">
            <div class="logo">{logo_text}</div>
            <ul class="nav-links">
                {all_nav_links_html}
            </ul>
            <div class="btns">
                <button class="btn">{button_text}</button>
            </div>
        </nav>

        <h2>Navbar Type - 2 (Logo Left, Links & Button Grouped Right)</h2>
        <nav class="nav-type-2">
            <div class="logo">{logo_text}</div>
            <ul class="nav-links">
                {all_nav_links_html}
            </ul>
            <div class="btns">
                <button class="btn">{button_text}</button>
            </div>
        </nav>

        <h2>Navbar Type - 3 (Logo & Links Grouped Left, Button Right)</h2>
        <nav class="nav-type-3">
            <div class="nav-group">
                <div class="logo">{logo_text}</div>
                <ul class="nav-links">
                    {all_nav_links_html}
                </ul>
            </div>
            <div class="btns">
                <button class="btn">{button_text}</button>
            </div>
        </nav>

        <h2>Navbar Type - 4 (Links Left, Logo Center, Button Right)</h2>
        <nav class="nav-type-4">
            <ul class="nav-links">
                {all_nav_links_html}
            </ul>
            <div class="logo">{logo_text}</div>
            <div class="btns">
                <button class="btn">{button_text}</button>
            </div>
        </nav>

        <h2>Navbar Type - 5 (Links Half-Left, Logo Center, Links Half-Right)</h2>
        <nav class="nav-type-5">
            <ul class="nav-links">
                {nav_links_html_part1}
            </ul>
            <div class="logo">{logo_text}</div>
            <ul class="nav-links">
                {nav_links_html_part2}
            </ul>
        </nav>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    # No dynamic JS behavior for these layouts, so script.js can be empty or just boilerplate
    js = """// Frosted Glow Navigation Bar — no specific interactive behavior beyond CSS hovers
document.addEventListener('DOMContentLoaded', () => {
    // All layout and interactive effects for these navbars are handled via CSS Flexbox and hover states.
    // JavaScript could be added here for responsive (hamburger) menus, scroll effects, etc., if desired.
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
