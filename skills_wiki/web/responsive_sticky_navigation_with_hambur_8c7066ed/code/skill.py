def create_component(
    output_dir: str,
    title_text: str = "BrandName",
    body_text: str = "Scroll down to see the sticky navigation in action. Resize the window to test the mobile hamburger menu.",
    color_scheme: str = "dark",
    accent_color: str = "#39ffde",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Sticky Navigation visual effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os
    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        page_bg = "#121212"
        nav_bg = "#1e1e1e"
        nav_text = "#ffffff"
        hover_text = "#111111" # Dark text on bright accent
        border_color = "rgba(255, 255, 255, 0.1)"
    else:
        page_bg = "#f0f2f5"
        nav_bg = "#ffffff"
        nav_text = "#111111"
        hover_text = "#111111"
        border_color = "rgba(0, 0, 0, 0.1)"

    # === CSS ===
    css = f"""/* Responsive Sticky Navigation */
:root {{
    --page-bg: {page_bg};
    --nav-bg: {nav_bg};
    --nav-text: {nav_text};
    --accent: {accent_color};
    --hover-text: {hover_text};
    --border: {border_color};
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--page-bg);
    color: var(--nav-text);
    min-height: 200vh; /* Force scroll to demonstrate sticky */
}}

/* Desktop Navigation */
nav {{
    position: sticky;
    top: 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: var(--nav-bg);
    padding: 10px 40px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    flex-wrap: wrap; /* Crucial for mobile wrapping */
    z-index: 1000;
}}

.logo {{
    display: flex;
    align-items: center;
    gap: 12px;
    cursor: pointer;
}}

.logo span {{
    font-size: 24px;
    font-weight: 700;
    letter-spacing: 0.5px;
}}

.nav-links {{
    display: flex;
    align-items: center;
    list-style: none;
}}

.nav-links a {{
    color: var(--nav-text);
    text-decoration: none;
    font-size: 14px;
    font-weight: 500;
    text-transform: uppercase;
    padding: 18px 20px;
    display: block;
    transition: all 0.2s ease-in-out;
}}

.nav-links a:hover {{
    background-color: var(--accent);
    color: var(--hover-text);
}}

/* Distinct styling for the CTA button */
.nav-cta-button {{
    margin-left: 16px;
    border: 2px solid var(--accent);
    border-radius: 50px;
    padding: 10px 24px !important;
}}

.hamburger {{
    display: none;
    flex-direction: column;
    gap: 5px;
    cursor: pointer;
    background: none;
    border: none;
    padding: 5px;
}}

.hamburger .bar {{
    width: 28px;
    height: 3px;
    background-color: var(--nav-text);
    border-radius: 2px;
    transition: all 0.3s ease;
}}

/* Main Page Content */
.content {{
    padding: 60px 40px;
    max-width: 800px;
    margin: 0 auto;
}}

.content h1 {{
    font-size: 3rem;
    margin-bottom: 20px;
}}

.content p {{
    font-size: 1.2rem;
    line-height: 1.6;
    opacity: 0.8;
}}

/* Responsive Design (Mobile) */
@media (max-width: 768px) {{
    nav {{
        padding: 15px 20px;
    }}

    .hamburger {{
        display: flex;
    }}

    .nav-links {{
        display: none; /* Hidden by default on mobile */
        width: 100%;
        flex-direction: column;
        margin-top: 15px;
    }}

    .nav-links.active {{
        display: flex;
    }}

    .nav-links li {{
        width: 100%;
    }}

    .nav-links a {{
        text-align: center;
        padding: 20px;
        border-top: 1px solid var(--border);
    }}

    /* Reset CTA styling on mobile to match other links */
    .nav-cta-button {{
        margin-left: 0;
        border: none;
        border-radius: 0;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text} - Navigation</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <nav>
        <div class="logo">
            <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
                <polyline points="2 17 12 22 22 17"></polyline>
                <polyline points="2 12 12 17 22 12"></polyline>
            </svg>
            <span>{title_text}</span>
        </div>
        
        <button class="hamburger" aria-label="Toggle navigation" aria-expanded="false">
            <div class="bar"></div>
            <div class="bar"></div>
            <div class="bar"></div>
        </button>

        <ul class="nav-links">
            <li><a href="#home">Home</a></li>
            <li><a href="#about">About</a></li>
            <li><a href="#cases">Cases</a></li>
            <li><a href="#services">Services</a></li>
            <li><a href="#contact" class="nav-cta-button">Contact</a></li>
        </ul>
    </nav>

    <main class="content">
        <h1>Welcome to {title_text}</h1>
        <p>{body_text}</p>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Navigation Menu Logic
document.addEventListener('DOMContentLoaded', () => {{
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    hamburger.addEventListener('click', () => {{
        // Toggle the visibility class
        navLinks.classList.toggle('active');
        
        // Update accessibility attributes
        const isExpanded = navLinks.classList.contains('active');
        hamburger.setAttribute('aria-expanded', isExpanded);
    }});

    // Optional: Close menu when clicking a link (improves mobile UX)
    const links = document.querySelectorAll('.nav-links a');
    links.forEach(link => {{
        link.addEventListener('click', () => {{
            if (window.innerWidth <= 768) {{
                navLinks.classList.remove('active');
                hamburger.setAttribute('aria-expanded', 'false');
            }}
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
