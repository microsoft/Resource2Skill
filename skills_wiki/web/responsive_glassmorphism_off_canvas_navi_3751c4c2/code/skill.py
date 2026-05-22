def create_component(
    output_dir: str,
    title_text: str = "Coding2Go",
    body_text: str = "Responsive Glassmorphism Navigation successfully loaded.",
    color_scheme: str = "light",        # "dark" or "light"
    accent_color: str = "#007bff",      # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Glassmorphism Off-Canvas Navigation.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derived theme settings
    if color_scheme == "dark":
        nav_bg = "#1a1a2e"
        nav_text = "#f0f0f0"
        nav_hover = "#2a2a40"
        sidebar_bg = "rgba(26, 26, 46, 0.6)"
        shadow_color = "rgba(0, 0, 0, 0.5)"
    else:
        nav_bg = "#ffffff"
        nav_text = "#000000"
        nav_hover = "#f0f0f0"
        sidebar_bg = "rgba(255, 255, 255, 0.25)"
        shadow_color = "rgba(0, 0, 0, 0.1)"

    # === CSS ===
    css = f"""/* Responsive Glassmorphism Sidebar Navigation */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --nav-bg: {nav_bg};
    --nav-text: {nav_text};
    --nav-hover: {nav_hover};
    --accent: {accent_color};
    --sidebar-bg: {sidebar_bg};
    --shadow: {shadow_color};
    --comp-width: {width_px}px;
    --comp-height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #222;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.component-wrapper {{
    width: var(--comp-width);
    height: var(--comp-height);
    max-width: 100vw;
    position: relative;
    overflow: hidden;
    /* Background image to make the glassmorphism visible */
    background: url('https://images.unsplash.com/photo-1498050108023-c5249f4df085?ixlib=rb-4.0.3&auto=format&fit=crop&w=2072&q=80') center/cover no-repeat;
    container-type: inline-size;
    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
}}

nav {{
    background-color: var(--nav-bg);
    box-shadow: 0 3px 5px var(--shadow);
    position: relative;
    z-index: 10;
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

nav a {{
    height: 100%;
    padding: 0 30px;
    text-decoration: none;
    display: flex;
    align-items: center;
    color: var(--nav-text);
    transition: background-color 0.2s ease, color 0.2s ease;
}}

nav a:hover {{
    background-color: var(--nav-hover);
}}

/* Desktop Specific */
nav li.logo-container {{
    margin-right: auto;
}}

nav .logo {{
    font-weight: 700;
    font-size: 1.25rem;
    color: var(--accent);
}}

.menu-btn {{
    display: none; /* Hidden on desktop */
}}

/* Sidebar Specific */
.sidebar {{
    position: absolute;
    top: 0;
    right: 0;
    height: 100%;
    width: 250px;
    z-index: 999;
    background-color: var(--sidebar-bg);
    -webkit-backdrop-filter: blur(10px);
    backdrop-filter: blur(10px);
    box-shadow: -10px 0 10px var(--shadow);
    display: none; /* Hidden by default, toggled via JS */
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
}}

.sidebar li {{
    width: 100%;
}}

.sidebar a {{
    width: 100%;
}}

.sidebar .close-btn a:hover {{
    color: #ff4757; /* Visual feedback for closing */
}}

/* Content Area */
.content {{
    padding: 40px;
    color: #fff;
    text-shadow: 0 2px 4px rgba(0,0,0,0.8);
}}

.content h1 {{
    font-size: 2.5rem;
    margin-bottom: 10px;
}}

/* Container Queries for Responsiveness */
@container (max-width: 800px) {{
    .hideOnMobile {{
        display: none;
    }}
    .menu-btn {{
        display: block;
    }}
}}

@container (max-width: 400px) {{
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
    <title>{title_text} - Responsive Nav</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="component-wrapper">
        <nav>
            <!-- Off-canvas Sidebar -->
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

            <!-- Main Desktop Navigation -->
            <ul class="desktop-nav">
                <li class="logo-container"><a href="#" class="logo">{title_text}</a></li>
                <li class="hideOnMobile"><a href="#">Blog</a></li>
                <li class="hideOnMobile"><a href="#">Products</a></li>
                <li class="hideOnMobile"><a href="#">About</a></li>
                <li class="hideOnMobile"><a href="#">Forum</a></li>
                <li class="hideOnMobile"><a href="#">Login</a></li>
                <li class="menu-btn">
                    <a href="#" aria-label="Open menu">
                        <svg xmlns="http://www.w3.org/2000/svg" height="26" viewBox="0 96 960 960" width="26" fill="currentColor">
                            <path d="M120 816v-60h720v60H120Zm0-210v-60h720v60H120Zm0-210v-60h720v60H120Z"/>
                        </svg>
                    </a>
                </li>
            </ul>
        </nav>

        <main class="content">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Sidebar Navigation Logic
document.addEventListener('DOMContentLoaded', () => {{
    const sidebar = document.querySelector('.sidebar');
    const menuBtn = document.querySelector('.menu-btn a');
    const closeBtn = document.querySelector('.close-btn a');

    // Open sidebar
    menuBtn.addEventListener('click', (e) => {{
        e.preventDefault();
        sidebar.style.display = 'flex';
    }});

    // Close sidebar
    closeBtn.addEventListener('click', (e) => {{
        e.preventDefault();
        sidebar.style.display = 'none';
    }});

    // Optional: Close sidebar when clicking outside of it
    document.addEventListener('click', (e) => {{
        if (sidebar.style.display === 'flex') {{
            if (!sidebar.contains(e.target) && !menuBtn.contains(e.target)) {{
                sidebar.style.display = 'none';
            }}
        }}
    }});
}});
"""

    # Write files
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
