import os

def create_component(
    output_dir: str,
    brand_name: str = "BrandName",
    nav_links: list = None,
    contact_text: str = "Contact",
    color_scheme: str = "dark",  # "dark" or "light"
    accent_color: str = "#39ffde",  # CSS hex color for accent (turquoise from video)
    width_px: int = 1200,  # Default desktop width for illustration, mostly informational
    height_px: int = 800,  # Default height for illustration, mostly informational
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Navigation Bar with Hamburger Menu visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    if nav_links is None:
        nav_links = ["Home", "About", "Cases", "Services"]

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        body_bg_color = "#222222" # Dark gray from video
        nav_bg_color = "#ffffff" # White from video
        text_color_primary = "#111111" # Dark text from video
        text_color_secondary = "#ffffff" # White text for hover/button bg
        hamburger_bar_color = "#111111"
        logo_text_color = "#111111"
    else: # Light scheme (inverted or adjusted for light backgrounds)
        body_bg_color = "#f8f9fa" # Lighter background
        nav_bg_color = "#ffffff"
        text_color_primary = "#333333" # Darker text for general use
        text_color_secondary = "#ffffff"
        hamburger_bar_color = "#333333"
        logo_text_color = "#333333"
        
    # Standard Meyer Reset CSS CDN
    reset_css_cdn = "https://meyerweb.com/eric/tools/css/reset/reset.css"
    
    # Simple inline SVG for logo icon (similar to video's placeholder)
    logo_svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="{hamburger_bar_color}" stroke="{hamburger_bar_color}" stroke-width="0" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z"/>
    </svg>
    """

    # Generate navigation links HTML
    nav_links_html_items = []
    for link in nav_links:
        nav_links_html_items.append(f'            <li><a href="#{link.lower()}">{link}</a></li>')
    nav_links_html_items.append(f'            <li><a class="nav-cta-button" href="#contact">{contact_text}</a></li>')
    final_nav_links_html = "\n".join(nav_links_html_items)

    # === CSS ===
    css = f"""
/* General Styles */
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

body {{
    background-color: {body_bg_color};
    font-family: 'Roboto', sans-serif;
    line-height: 1; /* Reset from meyerweb.css */
    min-height: 100vh; /* Ensure body takes full viewport height for scrolling demo */
}}

nav {{
    position: sticky;
    top: 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px;
    background-color: {nav_bg_color};
    z-index: 1000; /* Ensure nav is always on top */
    box-shadow: 0 2px 5px rgba(0,0,0,0.1); /* Subtle shadow for depth */
}}

.logo {{
    display: flex;
    align-items: center;
}}

.logo svg {{
    width: 40px; 
    height: 40px;
    margin-right: 5px; /* Space between icon and text */
}}

.logo h3 {{
    margin-left: 10px;
    color: {logo_text_color};
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
    margin: 0 5px; /* Spacing between links */
}}

.nav-links a {{
    display: block;
    padding: 30px 16px;
    color: {text_color_primary};
    text-decoration: none;
    font-size: 16px;
    font-family: 'Roboto', sans-serif;
    font-weight: 500; /* RobotoMedium */
    text-transform: uppercase;
    transition: all ease-in-out 100ms;
    white-space: nowrap; /* Prevent links from wrapping */
}}

.nav-links a:hover {{
    background-color: {accent_color};
    color: {text_color_secondary}; /* Change text color on hover for contrast */
}}

.nav-links .nav-cta-button {{
    padding: 10px 18px;
    margin-left: 16px;
    border: {accent_color} solid 2px;
    border-radius: 50px;
    background-color: transparent; /* Default transparent */
    color: {accent_color}; /* Default accent color */
}}

.nav-links .nav-cta-button:hover {{
    background-color: {accent_color};
    color: {text_color_secondary}; /* Text color changes to white on hover */
}}

.hamburger {{
    display: none; /* Hidden in desktop */
    cursor: pointer;
    width: 34px;
    height: 30px; /* Give it a height to contain bars */
    flex-direction: column;
    justify-content: space-around;
    align-items: center;
    padding: 3px 0; /* Vertical padding for bars */
}}

.hamburger .bar {{
    width: 100%; /* Ensure bars span hamburger width */
    height: 4px;
    background-color: {hamburger_bar_color};
    margin: 3px 0; /* Vertical margin for bars */
}}

/* Responsive Design */
@media (max-width: 768px) {{
    nav {{
        flex-wrap: wrap;
        padding: 15px 20px; /* Adjust padding for mobile */
        height: 80px; /* Fixed height for mobile nav bar */
    }}

    .hamburger {{
        display: flex; /* Show hamburger in mobile */
        margin-left: auto; /* Push to the right */
        order: 2; /* Position after logo in the flex container */
    }}

    .logo {{
        order: 1; /* Position before hamburger */
    }}
    
    .logo h3 {{
        font-size: 24px; /* Slightly smaller on mobile */
    }}

    .nav-links {{
        display: none; /* Hidden initially, JavaScript toggles this */
        flex-basis: 100%; /* Takes full width below logo/hamburger */
        flex-direction: column; /* Stack links vertically */
        background-color: {nav_bg_color}; /* Background for dropdown */
        position: absolute;
        top: 80px; /* Position below the nav bar height */
        left: 0;
        width: 100%;
        padding: 20px 0;
        box-shadow: 0 5px 10px rgba(0,0,0,0.1);
        opacity: 0; /* Start hidden, JS will toggle opacity with display */
        transition: opacity 0.3s ease-in-out;
    }}
    
    .nav-links.open {{
        display: flex; /* Show when JS opens it */
        opacity: 1; /* Fade in */
    }}

    .nav-links li {{
        flex-basis: 100%; /* Each link takes full width */
        margin: 0; /* Remove horizontal margin */
    }}

    .nav-links a {{
        text-align: center;
        font-size: 22px; /* Larger font size for mobile links */
        padding: 15px 10px; /* Adjust padding for mobile links */
    }}

    .nav-links .nav-cta-button {{
        padding: 15px 20px; /* Adjust padding for mobile button */
        margin: 20px auto 0 auto; /* Center button and add top margin */
        border: {accent_color} solid 2px; /* Add border back to button */
        border-radius: 50px; /* Add border-radius back to button */
        width: fit-content; /* Adjust width to fit content */
        color: {accent_color}; /* Ensure button text is accent color */
    }}
    
    .nav-links .nav-cta-button:hover {{
        background-color: {accent_color};
        color: {text_color_secondary};
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{brand_name} - Responsive Navigation</title>
    <link rel="stylesheet" href="{reset_css_cdn}">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <nav>
        <div class="logo">
            {logo_svg}
            <h3 class="BrandName">{brand_name}</h3>
        </div>
        <div class="hamburger">
            <div class="bar"></div>
            <div class="bar"></div>
            <div class="bar"></div>
        </div>
        <ul class="nav-links">
{final_nav_links_html}
        </ul>
    </nav>
    <!-- Placeholder for content area to enable scrolling demonstration -->
    <div style="height: 150vh; background-color: {body_bg_color}; display: flex; align-items: center; justify-content: center; color: {text_color_secondary}; font-size: 2em;">
        Scroll down to see sticky nav!
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""
document.addEventListener('DOMContentLoaded', () => {{
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    let menuOpen = false;

    // Adjust menu visibility on initial load based on screen width
    function setInitialMenuState() {{
        if (window.innerWidth <= 768) {{
            navLinks.style.display = 'none';
            navLinks.classList.remove('open');
            menuOpen = false;
        }} else {{
            navLinks.style.display = 'flex';
            navLinks.classList.remove('open');
            menuOpen = false;
        }}
    }}
    setInitialMenuState(); // Call on load

    hamburger.addEventListener('click', () => {{
        if (menuOpen === false) {{
            navLinks.style.display = 'flex'; // Make display block/flex immediately
            // Timeout allows browser to render display:flex before applying opacity transition
            setTimeout(() => navLinks.classList.add('open'), 10); 
            menuOpen = true;
        }} else {{
            navLinks.classList.remove('open'); // Remove class for opacity transition
            // Timeout waits for opacity transition to complete before setting display:none
            setTimeout(() => navLinks.style.display = 'none', 300); 
            menuOpen = false;
        }}
    }});

    // Optional: Close menu if a link is clicked (useful for single-page apps)
    navLinks.querySelectorAll('a').forEach(link => {{
        link.addEventListener('click', () => {{
            if (window.innerWidth <= 768 && menuOpen) {{
                navLinks.classList.remove('open');
                setTimeout(() => navLinks.style.display = 'none', 300);
                menuOpen = false;
            }}
        }});
    }});

    // Handle window resize for proper desktop/mobile transition
    window.addEventListener('resize', () => {{
        if (window.innerWidth > 768) {{
            navLinks.style.display = 'flex'; // Always show in desktop
            navLinks.classList.remove('open');
            menuOpen = false; // Reset menu state
        }} else {{
            if (!menuOpen) {{ // Only hide if not explicitly opened by hamburger
                 navLinks.style.display = 'none';
                 navLinks.classList.remove('open');
            }}
        }}
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
