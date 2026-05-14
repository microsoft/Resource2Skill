def create_component(
    output_dir: str,
    brand_name: str = "BrandName",
    menu_items: list = None,
    cta_text: str = "Contact",
    color_scheme: str = "dark",  # "dark" or "light"
    accent_color: str = "#39ffde",  # CSS hex color for accent (cyan/teal from video)
    width_px: int = 1200, # This is more for context, responsive design handles actual width
    height_px: int = 800, # This is more for context, responsive design handles actual height
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Header with Hamburger Menu visual effect.

    Writes index.html, style.css, reset.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if menu_items is None:
        menu_items = ["Home", "About", "Cases", "Services"]

    # === Derive theme colors from color_scheme and accent_color ===
    # Colors derived directly from the video for maximum reproduction accuracy.
    # The 'color_scheme' parameter is illustrative, but the video uses specific hex values.
    # Keeping the default video colors for the nav bar and text
    nav_bg_color = "#fff"
    content_bg_color = "#222"
    text_color = "#111"
    
    # === CSS (style.css) ===
    css = f"""/* Responsive Header with Hamburger Menu — generated component */
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap');

body {{
    background-color: {content_bg_color};
}}

nav {{
    position: sticky;
    top: 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px;
    background-color: {nav_bg_color};
    z-index: 1000; /* Ensure nav is on top */
}}

.logo {{
    display: flex;
    align-items: center;
}}

.logo img {{
    width: 40px;
    height: 40px; /* Added height for square aspect */
    fill: {text_color}; /* Color for SVG logo */
}}

.logo h3 {{
    margin-left: 10px;
    color: {text_color};
    text-decoration: none;
    font-size: 28px;
    font-family: 'Roboto', sans-serif;
    font-weight: 400; /* RobotoRegular */
}}

.nav-links {{
    display: flex;
    align-items: center;
    list-style: none;
}}

.nav-links li {{
    margin: 0;
}}

.nav-links a {{
    display: block;
    padding: 30px 16px;
    color: {text_color};
    text-decoration: none;
    font-size: 16px;
    font-family: 'Roboto', sans-serif;
    font-weight: 500; /* RobotoMedium */
    text-transform: uppercase;
    transition: all ease-in-out 100ms;
}}

.nav-links a:hover {{
    background-color: {accent_color};
}}

.nav-links .nav-cta-button {{
    padding: 10px 18px;
    margin-left: 16px;
    border: {accent_color} solid 2px;
    border-radius: 50px;
    transition: all ease-in-out 100ms;
}}

.nav-links .nav-cta-button:hover {{
    background-color: {accent_color};
    color: {nav_bg_color}; /* Change text color on hover for CTA */
}}

.hamburger {{
    display: none; /* Hidden on desktop */
    cursor: pointer;
    width: 34px;
    height: 28px; /* Added height to contain bars */
    flex-direction: column; /* For vertical bars */
    justify-content: space-between; /* Space out bars */
}}

.hamburger .bar {{
    flex-basis: 100%;
    height: 4px;
    background-color: {text_color};
    /* margin: 3px; */ /* Removed to use justify-content: space-between */
    border-radius: 2px;
}}

/* Responsive Design */
@media (max-width: 768px) {{
    nav {{
        flex-wrap: wrap;
        padding: 15px 20px; /* Adjusted padding for mobile */
    }}

    .hamburger {{
        display: flex; /* Visible on mobile */
    }}

    .nav-links {{
        display: none; /* Hidden by default on mobile */
        flex-basis: 100%;
        flex-direction: column; /* Stack vertically */
        align-items: flex-start; /* Align left for mobile menu */
        width: 100%;
        background-color: {nav_bg_color};
        position: absolute;
        top: 100%; /* Position below the nav bar */
        left: 0;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }}
    
    .nav-links.active {{
        display: flex; /* Show when active */
    }}

    .nav-links li {{
        width: 100%; /* Full width for each link */
    }}

    .nav-links a {{
        text-align: left; /* Align text left */
        font-size: 28px;
        padding: 15px 20px; /* Adjusted padding for mobile links */
        width: 100%; /* Ensure full clickable width */
    }}

    .nav-links .nav-cta-button {{
        margin-left: 0;
        border: none;
        border-radius: 0;
        margin-bottom: 0; /* No margin-bottom if menu items are full width */
        background-color: transparent; /* Reset background for mobile CTA */
        color: {text_color}; /* Reset text color for mobile CTA */
        text-align: left;
    }}
    
    .nav-links .nav-cta-button:hover {{
        background-color: {accent_color};
        color: {nav_bg_color};
    }}
}}
"""

    # === HTML (index.html) ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{brand_name} - Responsive Navigation</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="reset.css">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <nav>
        <div class="logo">
            <img src="data:image/svg+xml;base64,PHN2ZyB2aWV3Qm94PSIwIDAgMjQgMjQiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0iTTEyIDJjNS41MjMgMCAxMCA0LjQ3NyAxMCAxMHMtNC40NzcgMTAtMTAgMTAtMTAtNC40NzctMTAtMTBzNC40NzctMTAgMTAtMTBabTAtMiBjLTYuNjI3IDAtMTIgNS4zNzMtMTIgMTJzNS4zNzMgMTIgMTIgMTIgMTItNS4zNzMgMTItMTItNS4zNzMtMTItMTItMTJabTAgNC42NjZjLTQuMTEyIDAtNy4zMzMgMy4yMjEtNy4zMzMgNy4zMzNzMy4yMjEgNy4zMzMgNy4zMzMgNy4zMzMgNy4zMzMtMy4yMjEgNy4zMzMtNy4zMzNzLTMuMjIxLTcuMzMzLTcuMzMzLTcuMzMzeiIgZmlsbD0iIzExMSIvPjwvc3ZnPg==" alt="logo">
            <h3>{brand_name}</h3>
        </div>
        <div class="hamburger">
            <div class="bar"></div>
            <div class="bar"></div>
            <div class="bar"></div>
        </div>
        <ul class="nav-links">
            {''.join([f'<li><a href="#{item.lower()}">{item}</a></li>' for item in menu_items])}
            <li><a href="#contact" class="nav-cta-button">{cta_text}</a></li>
        </ul>
    </nav>

    <!-- Placeholder content to show sticky header and scrolling -->
    <div style="height: 1500px; padding: 20px; font-family: 'Roboto', sans-serif; color: #f0f0f0;">
        <p>Scroll down to see the sticky header in action!</p>
        <p>This is placeholder content.</p>
        <p>... more content ...</p>
        <p>... more content ...</p>
        <p>... more content ...</p>
        <p>... more content ...</p>
        <p>... more content ...</p>
        <p>... more content ...</p>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript (script.js) ===
    js = f"""// Responsive Header with Hamburger Menu — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    let menuOpen = false;

    hamburger.addEventListener('click', () => {{
        if (menuOpen === false) {{
            navLinks.classList.add('active'); // Use class to toggle display
            menuOpen = true;
        }} else {{
            navLinks.classList.remove('active'); // Use class to toggle display
            menuOpen = false;
        }}
    }});
}});
"""

    # === Reset CSS (reset.css) ===
    # Using Eric Meyer's Reset CSS as mentioned in the video.
    reset_css = """
/* Eric Meyer's CSS Reset */
html, body, div, span, applet, object, iframe,
h1, h2, h3, h4, h5, h6, p, blockquote, pre,
a, abbr, acronym, address, big, cite, code,
del, dfn, em, img, ins, kbd, q, s, samp,
small, strike, strong, sub, sup, tt, var,
b, u, i, center,
dl, dt, dd, ol, ul, li,
fieldset, form, label, legend,
table, caption, tbody, tfoot, thead, tr, th, td,
article, aside, canvas, details, embed,
figure, figcaption, footer, header, hgroup,
menu, nav, output, ruby, section, summary,
time, mark, audio, video {
	margin: 0;
	padding: 0;
	border: 0;
	font-size: 100%;
	font: inherit;
	vertical-align: baseline;
}
/* HTML5 display-role reset for older browsers */
article, aside, details, figcaption, figure,
footer, header, hgroup, menu, nav, section {
	display: block;
}
body {
	line-height: 1;
}
ol, ul {
	list-style: none;
}
blockquote, q {
	quotes: none;
}
blockquote:before, blockquote:after,
q:before, q:after {
	content: '';
	content: none;
}
table {
	border-collapse: collapse;
	border-spacing: 0;
}
"""

    # === Write files ===
    files = []
    for fname, content in [
        ("index.html", html),
        ("style.css", css),
        ("script.js", js),
        ("reset.css", reset_css),
    ]:
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

