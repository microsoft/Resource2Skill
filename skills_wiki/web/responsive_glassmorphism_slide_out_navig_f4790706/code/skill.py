def create_component(
    output_dir: str,
    title_text: str = "Explore the Cosmos",
    body_text: str = "Let's face it; if you want to go to space, you might as well genuinely go to outer space and not hover kind of on the edge of it. Well sit back, and relax because we'll give you a truly out of this world experience!",
    color_scheme: str = "dark",        
    accent_color: str = "#00bfff",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Glassmorphism Slide-out Navigation.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme properties
    if color_scheme == "dark":
        bg_gradient = "linear-gradient(135deg, #0b0d17, #151a2e, #1a2a44)"
        text_color = "#ffffff"
        text_muted = "rgba(255, 255, 255, 0.7)"
        surface_color = "rgba(255, 255, 255, 0.05)"
        surface_fallback = "rgba(21, 26, 46, 0.95)"
    else:
        bg_gradient = "linear-gradient(135deg, #eef2f3, #e0eaf5, #a3bded)"
        text_color = "#0b0d17"
        text_muted = "rgba(11, 13, 23, 0.7)"
        surface_color = "rgba(255, 255, 255, 0.4)"
        surface_fallback = "rgba(255, 255, 255, 0.95)"

    css = f"""/* Responsive Glassmorphism Slide-out Navigation */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-grad: {bg_gradient};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --surface: {surface_color};
    --surface-fallback: {surface_fallback};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: #000;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

/* Component Isolation */
.container {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    position: relative;
    overflow: hidden;
    background: var(--bg-grad);
    color: var(--text);
    container-type: inline-size;
}}

/* --- Header & Logo --- */
.primary-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2rem;
}}

.logo svg {{
    display: block;
}}

/* --- Mobile Nav Toggle Button --- */
.mobile-nav-toggle {{
    position: absolute;
    z-index: 9999;
    top: 2rem;
    right: 2rem;
    background: transparent;
    border: none;
    color: var(--text);
    cursor: pointer;
    width: 2rem;
    height: 2rem;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: transform 0.3s ease;
}}

.mobile-nav-toggle:hover {{
    transform: scale(1.1);
}}

/* Icon Swapping via ARIA State */
.mobile-nav-toggle .icon-close {{ display: none; }}
.mobile-nav-toggle[aria-expanded="true"] .icon-close {{ display: block; }}
.mobile-nav-toggle[aria-expanded="true"] .icon-hamburger {{ display: none; }}

/* --- Main Navigation Panel --- */
.primary-navigation {{
    position: absolute;
    z-index: 1000;
    inset: 0 0 0 30%; /* Snap to right, leaving 30% gap */
    list-style: none;
    padding: min(30cqh, 10rem) 2rem;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 2rem;
    background: var(--surface-fallback); /* Fallback */
    
    /* Hardware accelerated transition */
    transform: translateX(100%);
    transition: transform 350ms cubic-bezier(0.4, 0, 0.2, 1);
}}

@supports (backdrop-filter: blur(1.5rem)) {{
    .primary-navigation {{
        background: var(--surface);
        backdrop-filter: blur(1.5rem);
        -webkit-backdrop-filter: blur(1.5rem);
    }}
}}

/* Open State */
.primary-navigation[data-visible="true"] {{
    transform: translateX(0%);
}}

/* Navigation Links */
.primary-navigation a {{
    text-decoration: none;
    color: var(--text);
    text-transform: uppercase;
    letter-spacing: 3px;
    font-size: 1.125rem;
    font-weight: 400;
    display: flex;
    align-items: center;
    transition: opacity 0.2s ease;
}}

.primary-navigation a:hover {{
    opacity: 0.7;
}}

.primary-navigation a span {{
    font-weight: 700;
    margin-right: 0.75em;
    color: var(--text);
}}

/* Accessibility Utility */
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

/* --- Main Content Layout --- */
.main-content {{
    padding: 4rem 2rem;
    max-width: 600px;
    margin-top: 5vh;
}}

.title {{
    font-size: clamp(3rem, 10cqw, 7rem);
    text-transform: uppercase;
    letter-spacing: 4px;
    margin-bottom: 1.5rem;
    line-height: 1.1;
}}

.body-text {{
    font-size: 1.125rem;
    line-height: 1.8;
    margin-bottom: 2.5rem;
    color: var(--text-muted);
}}

.btn-primary {{
    background: transparent;
    color: var(--text);
    border: 2px solid var(--accent);
    padding: 1.25rem 2.5rem;
    font-size: 1.125rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    border-radius: 50px;
    cursor: pointer;
    transition: all 0.3s ease;
}}

.btn-primary:hover {{
    background: var(--accent);
    color: #fff;
    box-shadow: 0 0 20px var(--accent);
}}

/* --- Desktop Layout (Container Query) --- */
@container (min-width: 45em) {{
    .mobile-nav-toggle {{
        display: none;
    }}
    
    .primary-navigation {{
        inset: 2.5rem 0 auto auto; /* Anchor top right */
        transform: translateX(0);
        flex-direction: row;
        padding-block: 2.5rem;
        padding-inline: clamp(3rem, 7cqw, 7rem);
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Navigation Component</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        
        <header class="primary-header">
            <!-- Logo SVG -->
            <div class="logo">
                <svg viewBox="0 0 100 100" width="40" height="40" fill="var(--accent)">
                    <circle cx="50" cy="50" r="50"/>
                    <polygon points="50,10 90,90 50,70 10,90" fill="var(--surface-fallback)"/>
                </svg>
            </div>
            
            <!-- Mobile Toggle -->
            <button class="mobile-nav-toggle" aria-controls="primary-navigation" aria-expanded="false">
                <span class="sr-only">Menu</span>
                <svg class="icon-hamburger" viewBox="0 0 100 80" width="30" height="30" fill="currentColor">
                    <rect width="100" height="15" rx="8"></rect>
                    <rect y="32" width="100" height="15" rx="8"></rect>
                    <rect y="65" width="100" height="15" rx="8"></rect>
                </svg>
                <svg class="icon-close" viewBox="0 0 100 100" width="30" height="30" fill="currentColor">
                    <path d="M15,15 L85,85 M85,15 L15,85" stroke="currentColor" stroke-width="15" stroke-linecap="round"></path>
                </svg>
            </button>

            <!-- Navigation Bar -->
            <nav>
                <ul id="primary-navigation" data-visible="false" class="primary-navigation">
                    <li><a href="#"><span aria-hidden="true">00</span> Home</a></li>
                    <li><a href="#"><span aria-hidden="true">01</span> Destination</a></li>
                    <li><a href="#"><span aria-hidden="true">02</span> Crew</a></li>
                    <li><a href="#"><span aria-hidden="true">03</span> Technology</a></li>
                </ul>
            </nav>
        </header>

        <!-- Main Hero Content -->
        <main class="main-content">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
            <button class="btn-primary">Explore</button>
        </main>
        
    </div>
    <script src="script.js"></script>
</body>
</html>
"""

    js = """document.addEventListener('DOMContentLoaded', () => {
    const nav = document.querySelector('#primary-navigation');
    const navToggle = document.querySelector('.mobile-nav-toggle');

    // Ensure elements exist before binding
    if (!nav || !navToggle) return;

    navToggle.addEventListener('click', () => {
        // Retrieve current state from DOM
        const visibility = nav.getAttribute('data-visible');
        
        if (visibility === 'false') {
            // Open menu
            nav.setAttribute('data-visible', 'true');
            navToggle.setAttribute('aria-expanded', 'true');
        } else {
            // Close menu
            nav.setAttribute('data-visible', 'false');
            navToggle.setAttribute('aria-expanded', 'false');
        }
    });
});
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
