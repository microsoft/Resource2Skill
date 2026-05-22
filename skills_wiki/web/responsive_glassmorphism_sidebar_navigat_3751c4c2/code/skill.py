def create_component(
    output_dir: str,
    title_text: str = "Coding2Go Style Navbar",
    body_text: str = "Resize the container or your browser to see the responsive glassmorphism navigation in action.",
    color_scheme: str = "light",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Glassmorphism Sidebar Navigation visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        nav_bg = "rgba(20, 20, 20, 0.95)"
        text_col = "#f0f0f0"
        hover_bg = "rgba(255, 255, 255, 0.1)"
        glass_bg = "rgba(10, 10, 10, 0.5)"
        shadow_col = "rgba(0, 0, 0, 0.5)"
        page_bg = "#111"
    else:
        nav_bg = "rgba(255, 255, 255, 0.95)"
        text_col = "#1a1a1a"
        hover_bg = "#f0f0f0"
        glass_bg = "rgba(255, 255, 255, 0.25)"
        shadow_col = "rgba(0, 0, 0, 0.1)"
        page_bg = "#f5f5f5"

    # === CSS ===
    css = f"""/* Responsive Glassmorphism Sidebar Navigation */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --nav-bg: {nav_bg};
    --text-col: {text_col};
    --hover-bg: {hover_bg};
    --glass-bg: {glass_bg};
    --shadow-col: {shadow_col};
    --accent: {accent_color};
    --page-bg: {page_bg};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #333; /* Dark outer background to frame the preview */
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.preview-container {{
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    position: relative;
    overflow: hidden;
    background-color: var(--page-bg);
    background-image: url('https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=1200&q=80');
    background-size: cover;
    background-position: center;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    display: flex;
    flex-direction: column;
    resize: both; /* Allows the user to manually resize the container to test responsiveness */
}}

/* Navbar Core */
nav {{
    background-color: var(--nav-bg);
    box-shadow: 0 3px 5px var(--shadow-col);
    position: relative;
    z-index: 100;
}}

nav ul {{
    width: 100%;
    list-style: none;
    display: flex;
    justify-content: flex-end;
    align-items: center;
}}

nav li {{
    height: 50px;
}}

/* Full height anchor tags for optimal click targets */
nav a {{
    height: 100%;
    padding: 0 30px;
    text-decoration: none;
    display: flex;
    align-items: center;
    color: var(--text-col);
    font-weight: 500;
    transition: background-color 0.2s ease, color 0.2s ease;
}}

nav a:hover {{
    background-color: var(--hover-bg);
    color: var(--accent);
}}

/* The magic flexbox trick to push links to the right */
nav li.logo {{
    margin-right: auto;
    font-weight: 700;
    font-size: 1.25rem;
    letter-spacing: -0.5px;
}}

/* Sidebar Overlay */
.sidebar {{
    position: absolute; /* Absolute to the preview-container */
    top: 0;
    right: 0;
    height: 100%;
    width: 250px;
    background-color: var(--glass-bg);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    box-shadow: -10px 0 20px var(--shadow-col);
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    z-index: 999;
    
    /* Smooth sliding animation instead of raw display: none */
    transform: translateX(100%);
    transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    will-change: transform;
}}

.sidebar.active {{
    transform: translateX(0);
}}

.sidebar li {{
    width: 100%;
}}

.sidebar a {{
    width: 100%;
}}

.menu-button {{
    display: none;
}}

/* Hero Content Area for context */
.content {{
    padding: 60px 40px;
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    color: #fff;
    text-shadow: 0 2px 10px rgba(0,0,0,0.8);
}}

.content h1 {{
    font-size: 3rem;
    margin-bottom: 1rem;
}}

.content p {{
    font-size: 1.2rem;
    max-width: 600px;
    line-height: 1.5;
}}

/* Responsive Breakpoints */
@media (max-width: 800px) {{
    .hideOnMobile {{
        display: none;
    }}
    .menu-button {{
        display: block;
    }}
}}

@media (max-width: 400px) {{
    .sidebar {{
        width: 100%;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="preview-container">
        <nav>
            <!-- Sidebar Navigation -->
            <ul class="sidebar">
                <li class="close-btn">
                    <a href="#" aria-label="Close menu">
                        <svg xmlns="http://www.w3.org/2000/svg" height="26" viewBox="0 96 960 960" width="26" fill="currentColor">
                            <path d="m249 849-42-42 231-231-231-231 42-42 231 231 231-231 42 42-231 231 231 231-42 42-231-231-231 231Z"/>
                        </svg>
                    </a>
                </li>
                <li><a href="#">Blog</a></li>
                <li><a href="#">Products</a></li>
                <li><a href="#">About</a></li>
                <li><a href="#">Forum</a></li>
                <li><a href="#">Login</a></li>
            </ul>

            <!-- Main Top Navigation -->
            <ul class="main-nav">
                <li class="logo"><a href="#">Coding2Go</a></li>
                <li class="hideOnMobile"><a href="#">Blog</a></li>
                <li class="hideOnMobile"><a href="#">Products</a></li>
                <li class="hideOnMobile"><a href="#">About</a></li>
                <li class="hideOnMobile"><a href="#">Forum</a></li>
                <li class="hideOnMobile"><a href="#">Login</a></li>
                <li class="menu-button">
                    <a href="#" aria-label="Open menu">
                        <svg xmlns="http://www.w3.org/2000/svg" height="26" viewBox="0 96 960 960" width="26" fill="currentColor">
                            <path d="M120 816v-60h720v60H120Zm0-210v-60h720v60H120Zm0-210v-60h720v60H120Z"/>
                        </svg>
                    </a>
                </li>
            </ul>
        </nav>

        <!-- Dummy Content -->
        <main class="content">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Sidebar Toggle Logic
document.addEventListener('DOMContentLoaded', () => {{
    const showBtn = document.querySelector('.menu-button a');
    const hideBtn = document.querySelector('.close-btn a');
    const sidebar = document.querySelector('.sidebar');

    if (showBtn && sidebar) {{
        showBtn.addEventListener('click', (e) => {{
            e.preventDefault();
            // Adds active class to trigger CSS transform
            sidebar.classList.add('active');
        }});
    }}

    if (hideBtn && sidebar) {{
        hideBtn.addEventListener('click', (e) => {{
            e.preventDefault();
            // Removes active class to slide it back out
            sidebar.classList.remove('active');
        }});
    }}
    
    // Optional: Close sidebar when clicking outside of it
    document.addEventListener('click', (e) => {{
        if (sidebar.classList.contains('active') && 
            !sidebar.contains(e.target) && 
            !showBtn.contains(e.target)) {{
            sidebar.classList.remove('active');
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
