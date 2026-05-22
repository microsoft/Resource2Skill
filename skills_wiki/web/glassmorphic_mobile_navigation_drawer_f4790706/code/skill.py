def create_component(
    output_dir: str,
    title_text: str = "Space Tourism",
    body_text: str = "Explore the edges of the galaxy.",
    color_scheme: str = "dark",
    accent_color: str = "#d0d6f9",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Glassmorphic Mobile Navigation Drawer.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Base themes based on color scheme
    if color_scheme == "dark":
        text_color = "#ffffff"
        nav_bg_fallback = "hsl(0 0% 0% / 0.8)"
        nav_bg_glass = "hsl(0 0% 100% / 0.05)"
        bg_url = "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2072&auto=format&fit=crop"
    else:
        text_color = "#0b0d17"
        nav_bg_fallback = "hsl(0 0% 100% / 0.9)"
        nav_bg_glass = "hsl(0 0% 100% / 0.5)"
        bg_url = "https://images.unsplash.com/photo-1444703686981-a3abbc4d4fe3?q=80&w=2070&auto=format&fit=crop"

    css = f"""/* Glassmorphic Mobile Navigation Drawer */
*, *::before, *::after {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

:root {{
    --text: {text_color};
    --accent: {accent_color};
    --nav-bg-fallback: {nav_bg_fallback};
    --nav-bg-glass: {nav_bg_glass};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: #121212;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

/* Mockup Container (Acts as our Viewport) */
.device-mockup {{
    container-type: inline-size;
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    background-image: url('{bg_url}');
    background-size: cover;
    background-position: center;
    position: relative;
    border-radius: 12px;
    box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5);
    overflow: hidden;
    
    /* Allow user to resize the container to easily test the responsive breakpoints! */
    resize: horizontal;
}}

/* Header Layout */
.primary-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 2rem clamp(1rem, 5cqw, 3rem);
    position: relative;
    z-index: 100;
}}

.logo {{
    width: 48px;
    height: 48px;
}}

/* Primary Navigation Styles */
.primary-navigation {{
    list-style: none;
    display: flex;
    gap: clamp(1.5rem, 5cqw, 3rem);
}}

.primary-navigation a {{
    text-decoration: none;
    color: var(--text);
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 0.9rem;
    display: flex;
    align-items: center;
    gap: 0.75em;
    transition: color 0.2s ease;
}}

.primary-navigation a:hover,
.primary-navigation a:focus {{
    color: var(--accent);
}}

.primary-navigation span[aria-hidden="true"] {{
    font-weight: 700;
}}

/* Accessibility utility */
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

/* Mobile Toggle Button */
.mobile-nav-toggle {{
    display: none;
}}

/* Mobile / Small Screen Styles */
@container (max-width: 35em) {{
    .primary-navigation {{
        position: absolute;
        z-index: 1000;
        /* Start from top edge, right edge, bottom edge, and 30% from left */
        inset: 0 0 0 30%;
        flex-direction: column;
        padding: min(30cqh, 8rem) 2rem;
        
        background: var(--nav-bg-fallback);
        transform: translateX(100%);
        transition: transform 350ms ease-out;
    }}
    
    /* Apply Glassmorphism if supported */
    @supports (backdrop-filter: blur(1rem)) or (-webkit-backdrop-filter: blur(1rem)) {{
        .primary-navigation {{
            background: var(--nav-bg-glass);
            backdrop-filter: blur(1.5rem);
            -webkit-backdrop-filter: blur(1.5rem);
        }}
    }}

    /* Reveal State */
    .primary-navigation[data-visible="true"] {{
        transform: translateX(0%);
    }}

    /* Toggle Button Setup */
    .mobile-nav-toggle {{
        display: block;
        position: absolute;
        z-index: 9999;
        background: transparent;
        border: 0;
        top: 2rem;
        right: 2rem;
        width: 2rem;
        aspect-ratio: 1;
        cursor: pointer;
        color: var(--text);
    }}
    
    .mobile-nav-toggle:focus-visible {{
        outline: 2px solid var(--accent);
        outline-offset: 4px;
    }}

    /* SVG Icon Swapping logic */
    .icon-close {{
        display: none;
    }}
    
    .mobile-nav-toggle[aria-expanded="true"] .icon-hamburger {{
        display: none;
    }}
    
    .mobile-nav-toggle[aria-expanded="true"] .icon-close {{
        display: block;
    }}
}}

/* Page Content Overlay */
.hero-content {{
    position: absolute;
    bottom: 20%;
    left: 10%;
    color: var(--text);
    max-width: 450px;
}}

.hero-content h1 {{
    font-size: clamp(2.5rem, 8cqw, 5rem);
    text-transform: uppercase;
    letter-spacing: 4px;
    margin-bottom: 1rem;
}}

.hero-content p {{
    font-size: 1.1rem;
    line-height: 1.6;
    color: var(--accent);
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text} Component</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <!-- Drag the right edge of this container to view the breakpoint switch! -->
    <div class="device-mockup">
        <header class="primary-header">
            <div>
                <!-- Mock Logo -->
                <svg class="logo" viewBox="0 0 48 48" width="48" height="48">
                    <circle cx="24" cy="24" r="20" fill="none" stroke="var(--text)" stroke-width="4"/>
                    <circle cx="24" cy="24" r="8" fill="var(--text)"/>
                </svg>
            </div>

            <!-- Hamburger Menu Button -->
            <button class="mobile-nav-toggle" aria-controls="primary-navigation" aria-expanded="false">
                <span class="sr-only">Menu</span>
                <svg class="icon-hamburger" viewBox="0 0 24 21" width="100%" height="100%">
                    <rect width="24" height="3" fill="currentColor"/>
                    <rect y="9" width="24" height="3" fill="currentColor"/>
                    <rect y="18" width="24" height="3" fill="currentColor"/>
                </svg>
                <svg class="icon-close" viewBox="0 0 24 24" width="100%" height="100%">
                    <path d="M2.4 2.4l19.2 19.2M21.6 2.4L2.4 21.6" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>
                </svg>
            </button>

            <!-- Navigation Drawer -->
            <nav>
                <ul id="primary-navigation" data-visible="false" class="primary-navigation">
                    <li>
                        <a href="#">
                            <span aria-hidden="true">00</span> Home
                        </a>
                    </li>
                    <li>
                        <a href="#">
                            <span aria-hidden="true">01</span> Destination
                        </a>
                    </li>
                    <li>
                        <a href="#">
                            <span aria-hidden="true">02</span> Crew
                        </a>
                    </li>
                    <li>
                        <a href="#">
                            <span aria-hidden="true">03</span> Technology
                        </a>
                    </li>
                </ul>
            </nav>
        </header>

        <main class="hero-content">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Glassmorphic Mobile Navigation State Management
document.addEventListener('DOMContentLoaded', () => {{
    const nav = document.querySelector('.primary-navigation');
    const navToggle = document.querySelector('.mobile-nav-toggle');

    navToggle.addEventListener('click', () => {{
        // Get current visibility state
        const isVisible = nav.getAttribute('data-visible') === 'true';

        // Toggle state
        if (!isVisible) {{
            nav.setAttribute('data-visible', 'true');
            navToggle.setAttribute('aria-expanded', 'true');
        }} else {{
            nav.setAttribute('data-visible', 'false');
            navToggle.setAttribute('aria-expanded', 'false');
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
