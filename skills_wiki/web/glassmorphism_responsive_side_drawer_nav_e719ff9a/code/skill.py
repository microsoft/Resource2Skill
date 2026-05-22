def create_component(
    output_dir: str,
    title_text: str = "Explore Next Generation Navigation",
    body_text: str = "Resize the browser to see the layout shift, and click the menu icon on smaller screens to see the glassmorphism side drawer in action.",
    color_scheme: str = "dark",
    accent_color: str = "#00bfff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Glassmorphism Responsive Side-Drawer Navbar.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Establish theme variables based on the selected scheme
    if color_scheme == "dark":
        bg_url = "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2000&auto=format&fit=crop"
        text_color = "#ffffff"
        glass_bg = "rgba(255, 255, 255, 0.05)"
        glass_fallback = "rgba(11, 13, 23, 0.9)"
        nav_hover = "rgba(255, 255, 255, 0.5)"
    else:
        # A lighter landscape image for light mode to show off the blur
        bg_url = "https://images.unsplash.com/photo-1506744626753-1fa7673e5e48?q=80&w=2000&auto=format&fit=crop"
        text_color = "#000000"
        glass_bg = "rgba(255, 255, 255, 0.6)"
        glass_fallback = "rgba(255, 255, 255, 0.95)"
        nav_hover = "rgba(0, 0, 0, 0.5)"

    css = f"""/* Glassmorphism Responsive Side-Drawer Navbar */
:root {{
    --text-color: {text_color};
    --accent: {accent_color};
    --glass-bg: {glass_bg};
    --glass-fallback: {glass_fallback};
    --nav-hover: {nav_hover};
    --width: {width_px}px;
    --height: {height_px}px;
}}

/* Resets */
*, *::before, *::after {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    color: var(--text-color);
    background-image: url('{bg_url}');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    min-height: 100vh;
    overflow-x: hidden;
}}

.preview-container {{
    max-width: var(--width);
    min-height: var(--height);
    margin: 0 auto;
    position: relative;
}}

/* Utility Classes */
.sr-only {{
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}}

.flex {{
    display: flex;
    gap: var(--gap, 1rem);
}}

/* Typography */
.nav-text {{
    font-family: 'Space Grotesk', sans-serif;
    letter-spacing: 2.7px;
    text-transform: uppercase;
    text-decoration: none;
    color: var(--text-color);
    font-size: 0.9rem;
    position: relative;
    padding-block: 2rem;
}}

.nav-number {{
    font-weight: 700;
    margin-inline-end: 0.75em;
}}

/* Primary Header */
.primary-header {{
    justify-content: space-between;
    align-items: center;
    padding-top: 2rem;
    padding-inline: max(2rem, 5vw);
}}

.logo svg {{
    width: 48px;
    height: 48px;
    fill: var(--text-color);
}}

/* Mobile Nav Toggle Button */
.mobile-nav-toggle {{
    display: none;
    background: transparent;
    border: none;
    cursor: pointer;
    z-index: 9999;
}}

.mobile-nav-toggle svg {{
    width: 24px;
    height: 24px;
    fill: var(--text-color);
    transition: transform 0.3s ease;
}}

.icon-close {{
    display: none;
}}

/* Mobile Layout */
@media (max-width: 45em) {{
    .primary-navigation {{
        --gap: 2em;
        position: fixed;
        z-index: 1000;
        inset: 0 0 0 30%;
        flex-direction: column;
        padding: min(30vh, 10rem) 2em;
        transform: translateX(100%);
        transition: transform 350ms ease-out;
        
        /* Fallback background */
        background: var(--glass-fallback);
    }}

    @supports (backdrop-filter: blur(1rem)) {{
        .primary-navigation {{
            background: var(--glass-bg);
            backdrop-filter: blur(1.5rem);
            -webkit-backdrop-filter: blur(1.5rem);
        }}
    }}

    .primary-navigation[data-visible="true"] {{
        transform: translateX(0);
    }}

    .mobile-nav-toggle {{
        display: block;
        position: absolute;
        top: 2.5rem;
        right: max(2rem, 5vw);
    }}

    .mobile-nav-toggle[aria-expanded="true"] .icon-hamburger {{
        display: none;
    }}
    
    .mobile-nav-toggle[aria-expanded="true"] .icon-close {{
        display: block;
    }}

    /* Adjust padding for mobile links */
    .nav-text {{
        padding-block: 0.5rem;
    }}
}}

/* Desktop Layout */
@media (min-width: 45.001em) {{
    .primary-navigation {{
        --gap: clamp(1.5rem, 5vw, 3rem);
        padding-block: 0;
        padding-inline: clamp(3rem, 7vw, 7rem);
        background: var(--glass-fallback);
    }}

    @supports (backdrop-filter: blur(1rem)) {{
        .primary-navigation {{
            background: var(--glass-bg);
            backdrop-filter: blur(1.5rem);
            -webkit-backdrop-filter: blur(1.5rem);
        }}
    }}

    /* Underline Hover Indicator */
    .nav-text::after {{
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 3px;
        background-color: var(--text-color);
        opacity: 0;
        transition: opacity 0.2s ease-in-out;
    }}

    .nav-text:hover::after,
    .nav-text:focus::after {{
        opacity: 0.5;
    }}
    
    /* Simulate active state */
    li.active .nav-text::after {{
        opacity: 1;
    }}
}}

/* Page Content Styling */
.hero-content {{
    padding: clamp(3rem, 10vw, 10rem) max(2rem, 5vw);
    max-width: 600px;
}}

.hero-content h1 {{
    font-size: clamp(2.5rem, 5vw, 5rem);
    text-transform: uppercase;
    margin-bottom: 1.5rem;
    line-height: 1.1;
    text-shadow: 0 4px 10px rgba(0,0,0,0.5);
}}

.hero-content p {{
    font-size: 1.125rem;
    line-height: 1.6;
    text-shadow: 0 2px 5px rgba(0,0,0,0.5);
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&family=Space+Grotesk:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="preview-container">
        <header class="primary-header flex">
            <div class="logo">
                <a href="#">
                    <!-- Abstract Star/Space Logo -->
                    <svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="24" cy="24" r="24" fill="{text_color}"/>
                        <path d="M24 0C24 0 24 24 0 24C0 24 24 24 24 48C24 48 24 24 48 24C48 24 24 24 24 0Z" fill="var(--bg)"/>
                    </svg>
                </a>
            </div>

            <button class="mobile-nav-toggle" aria-controls="primary-navigation" aria-expanded="false">
                <span class="sr-only">Menu</span>
                <!-- Hamburger Icon -->
                <svg class="icon-hamburger" viewBox="0 0 24 21" xmlns="http://www.w3.org/2000/svg">
                    <g fill-rule="evenodd">
                        <path d="M0 0h24v3H0zM0 9h24v3H0zM0 18h24v3H0z"/>
                    </g>
                </svg>
                <!-- Close Icon -->
                <svg class="icon-close" viewBox="0 0 21 21" xmlns="http://www.w3.org/2000/svg">
                    <g fill-rule="evenodd">
                        <path d="M2.404.222l18.384 18.384-2.182 2.182L.222 2.404z"/>
                        <path d="M.222 18.606L18.606.222l2.182 2.182L2.404 20.788z"/>
                    </g>
                </svg>
            </button>

            <nav>
                <ul id="primary-navigation" data-visible="false" class="primary-navigation flex" style="list-style: none;">
                    <li class="active">
                        <a class="nav-text" href="#">
                            <span class="nav-number" aria-hidden="true">00</span>Home
                        </a>
                    </li>
                    <li>
                        <a class="nav-text" href="#">
                            <span class="nav-number" aria-hidden="true">01</span>Destination
                        </a>
                    </li>
                    <li>
                        <a class="nav-text" href="#">
                            <span class="nav-number" aria-hidden="true">02</span>Crew
                        </a>
                    </li>
                    <li>
                        <a class="nav-text" href="#">
                            <span class="nav-number" aria-hidden="true">03</span>Technology
                        </a>
                    </li>
                </ul>
            </nav>
        </header>

        <main class="hero-content">
            <h1 style="color: var(--accent);">{title_text}</h1>
            <p>{body_text}</p>
        </main>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Glassmorphism Side-Drawer Logic
document.addEventListener('DOMContentLoaded', () => {{
    const primaryNav = document.querySelector('.primary-navigation');
    const navToggle = document.querySelector('.mobile-nav-toggle');

    if (!primaryNav || !navToggle) return;

    navToggle.addEventListener('click', () => {{
        // Check custom data attribute state
        const visibility = primaryNav.getAttribute('data-visible');
        
        // Toggle states
        if (visibility === "false") {{
            primaryNav.setAttribute('data-visible', 'true');
            navToggle.setAttribute('aria-expanded', 'true');
            
            // Optional: Prevent scrolling on body when mobile menu is open
            document.body.style.overflow = 'hidden';
        }} else {{
            primaryNav.setAttribute('data-visible', 'false');
            navToggle.setAttribute('aria-expanded', 'false');
            
            // Restore scrolling
            document.body.style.overflow = '';
        }}
    }});

    // Handle viewport resizing to ensure state resets if resized from mobile to desktop
    window.addEventListener('resize', () => {{
        if (window.innerWidth > 720) {{ // Roughly 45em
            primaryNav.setAttribute('data-visible', 'false');
            navToggle.setAttribute('aria-expanded', 'false');
            document.body.style.overflow = '';
        }}
    }});
}});
"""

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
