def create_component(
    output_dir: str,
    title_text: str = "BrandName",
    body_text: str = "Welcome to our responsive website. Resize your browser window to see the horizontal navigation links collapse into a hamburger menu.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#39ffde",     # CSS hex color for the CTA/Hover accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Sticky Navigation Bar.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os
    import html

    os.makedirs(output_dir, exist_ok=True)

    # Sanitize inputs
    safe_title = html.escape(title_text)
    safe_body = html.escape(body_text)

    # Deriving theme colors
    if color_scheme == "dark":
        bg_color = "#121212"
        nav_bg = "#1e1e1e"
        text_color = "#f0f0f0"
        hover_text_color = "#121212"  # Text color when CTA button is hovered (filled)
    else:
        bg_color = "#f8f9fa"
        nav_bg = "#ffffff"
        text_color = "#111111"
        hover_text_color = "#ffffff"  # Text color when CTA button is hovered (filled)

    # === CSS ===
    css = f"""/* Responsive Sticky Navigation Bar — Generated Component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --nav-bg: {nav_bg};
    --text: {text_color};
    --accent: {accent_color};
    --hover-text: {hover_text_color};
    --max-width: {width_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 200vh; /* Forced height to demonstrate sticky scroll */
}}

/* Navigation Bar Base */
nav {{
    position: sticky;
    top: 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 40px;
    background-color: var(--nav-bg);
    min-height: 70px;
    z-index: 1000;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}}

.logo {{
    display: flex;
    align-items: center;
    gap: 10px;
}}

.logo h3 {{
    font-size: 22px;
    font-weight: 700;
    letter-spacing: 0.5px;
}}

/* Desktop Link Styling */
.nav-links {{
    display: flex;
    align-items: center;
    list-style: none;
    gap: 32px;
}}

.nav-links a {{
    color: var(--text);
    text-decoration: none;
    text-transform: uppercase;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 1px;
    transition: color 0.2s ease-in-out;
}}

.nav-links a:hover {{
    color: var(--accent);
}}

/* Call to Action Button */
.nav-cta-button {{
    padding: 10px 24px;
    border: 2px solid var(--accent);
    border-radius: 50px;
    color: var(--accent) !important;
    transition: all 0.2s ease-in-out !important;
}}

.nav-cta-button:hover {{
    background-color: var(--accent);
    color: var(--hover-text) !important;
}}

/* Hamburger Icon (Hidden on Desktop) */
.hamburger {{
    display: none;
    cursor: pointer;
    flex-direction: column;
    justify-content: space-between;
    width: 28px;
    height: 18px;
    padding: 2px 0;
}}

.hamburger .bar {{
    height: 2px;
    width: 100%;
    background-color: var(--text);
    border-radius: 4px;
    transition: all 0.3s ease;
}}

/* Page Content Formatting */
.content-wrapper {{
    max-width: var(--max-width);
    margin: 80px auto;
    padding: 0 40px;
}}

.content-wrapper h1 {{
    font-size: 3rem;
    margin-bottom: 20px;
}}

.content-wrapper p {{
    font-size: 1.1rem;
    line-height: 1.7;
    opacity: 0.8;
}}

/* --- Mobile Responsiveness (Breakpoint: 768px) --- */
@media (max-width: 768px) {{
    nav {{
        flex-wrap: wrap; /* Allows links to drop below logo */
        padding: 15px 24px;
    }}

    .hamburger {{
        display: flex; /* Reveal mobile toggle */
    }}

    .nav-links {{
        display: none; /* Hidden by default on mobile */
        flex-basis: 100%; /* Force onto a new line */
        flex-direction: column;
        align-items: center;
        padding: 20px 0 10px 0;
        gap: 20px;
    }}

    /* Class added via JavaScript */
    .nav-links.active {{
        display: flex;
    }}

    .nav-cta-button {{
        margin-top: 10px;
        width: 100%;
        text-align: center;
    }}
}}
"""

    # === HTML ===
    html_str = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title} | Navigation</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <nav>
        <div class="logo">
            <!-- Example minimal SVG Logo icon -->
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polygon points="12 2 2 22 22 22"></polygon>
            </svg>
            <h3>{safe_title}</h3>
        </div>
        
        <!-- Accessible Hamburger Button -->
        <div class="hamburger" role="button" aria-label="Toggle navigation menu" aria-expanded="false" tabindex="0">
            <div class="bar"></div>
            <div class="bar"></div>
            <div class="bar"></div>
        </div>

        <ul class="nav-links">
            <li><a href="#">Home</a></li>
            <li><a href="#">About</a></li>
            <li><a href="#">Cases</a></li>
            <li><a href="#">Services</a></li>
            <li><a href="#" class="nav-cta-button">Contact</a></li>
        </ul>
    </nav>

    <main class="content-wrapper">
        <h1>Welcome to {safe_title}</h1>
        <p>{safe_body}</p>
        <br><br><br><br>
        <p><em>(Scroll down to see the navigation bar stick to the top of the viewport.)</em></p>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Sticky Navigation Bar Logic
document.addEventListener('DOMContentLoaded', () => {{
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    // Toggle menu open/close
    const toggleMenu = () => {{
        const isActive = navLinks.classList.toggle('active');
        // Update accessibility attributes
        hamburger.setAttribute('aria-expanded', isActive);
    }};

    // Mouse Click Event
    hamburger.addEventListener('click', toggleMenu);

    // Keyboard Accessibility (Enter / Space bar)
    hamburger.addEventListener('keydown', (e) => {{
        if (e.key === 'Enter' || e.key === ' ') {{
            e.preventDefault();
            toggleMenu();
        }}
    }});
}});
"""

    # === Write files ===
    files = []
    for fname, content in [("index.html", html_str), ("style.css", css), ("script.js", js)]:
        path = os.path.join(output_dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        files.append(path)

    return {
        "html": html_str,
        "css": css,
        "js": js,
        "files": files,
    }
