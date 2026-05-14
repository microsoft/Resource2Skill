def create_component(
    output_dir: str,
    title_text: str = "Coding2Go",
    body_text: str = "Resize the browser or container window to watch the desktop navigation collapse into a frosted-glass mobile sidebar.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Glassmorphism Sidebar effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        page_bg = "#0d111c"
        nav_bg = "#161b22"
        nav_text = "#f0f0f0"
        sidebar_bg = "rgba(22, 27, 34, 0.6)"
        hover_bg = "rgba(255, 255, 255, 0.1)"
        shadow = "rgba(0, 0, 0, 0.5)"
    else:
        page_bg = "#f8f9fa"
        nav_bg = "#ffffff"
        nav_text = "#24292f"
        sidebar_bg = "rgba(255, 255, 255, 0.6)"
        hover_bg = "rgba(0, 0, 0, 0.05)"
        shadow = "rgba(0, 0, 0, 0.1)"

    # === CSS ===
    css = f"""/* Glassmorphism Responsive Sidebar — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --page-bg: {page_bg};
    --nav-bg: {nav_bg};
    --nav-text: {nav_text};
    --sidebar-bg: {sidebar_bg};
    --hover-bg: {hover_bg};
    --shadow: {shadow};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #333; /* Outer environment background */
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

/* Main wrapper to act as our isolated viewport */
.container {{
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    position: relative;
    overflow: hidden; /* Keeps sidebar contained */
    /* Dynamic gradient background to demonstrate glassmorphism */
    background: radial-gradient(circle at top right, color-mix(in srgb, var(--accent) 30%, transparent), var(--page-bg));
    box-shadow: 0 15px 35px rgba(0,0,0,0.2);
    
    /* Crucial: Establish a container for component-level media queries */
    container-type: inline-size;
    container-name: viewport;
}}

/* ==================== 
   Desktop Navigation 
   ==================== */
nav {{
    background-color: var(--nav-bg);
    box-shadow: 0 3px 10px var(--shadow);
    height: 60px;
    display: flex;
    align-items: center;
    padding: 0 24px;
    position: relative;
    z-index: 10;
}}

.logo {{
    font-weight: 700;
    font-size: 1.25rem;
    color: var(--nav-text);
    text-decoration: none;
    margin-right: auto; /* Pushes list items to the right */
    letter-spacing: -0.5px;
}}

.nav-links {{
    display: flex;
    list-style: none;
    height: 100%;
}}

.nav-links li {{
    height: 100%;
}}

.nav-links a, .menu-btn {{
    height: 100%;
    padding: 0 20px;
    display: flex;
    align-items: center;
    text-decoration: none;
    color: var(--nav-text);
    font-size: 0.95rem;
    font-weight: 500;
    transition: background-color 0.2s ease, color 0.2s ease;
    background: transparent;
    border: none;
    cursor: pointer;
}}

.nav-links a:hover, .menu-btn:hover {{
    background-color: var(--hover-bg);
    color: var(--accent);
}}

.menu-item {{
    display: none; /* Hidden on large screens */
}}


/* ==================== 
   Mobile Sidebar 
   ==================== */
.sidebar {{
    position: absolute;
    top: 0;
    right: 0;
    height: 100%;
    width: 260px;
    background-color: var(--sidebar-bg);
    
    /* The Glassmorphism Effect */
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    
    box-shadow: -5px 0 25px var(--shadow);
    display: flex;
    flex-direction: column;
    list-style: none;
    z-index: 999;
    
    /* Animation state */
    transform: translateX(100%);
    transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}}

.sidebar.active {{
    transform: translateX(0);
}}

.sidebar li {{
    width: 100%;
}}

.sidebar a, .close-btn {{
    width: 100%;
    padding: 20px 24px;
    display: flex;
    align-items: center;
    text-decoration: none;
    color: var(--nav-text);
    font-size: 1.05rem;
    font-weight: 500;
    background: transparent;
    border: none;
    cursor: pointer;
    transition: background-color 0.2s ease, padding-left 0.2s ease;
}}

.sidebar a:hover, .close-btn:hover {{
    background-color: var(--hover-bg);
    color: var(--accent);
    padding-left: 28px; /* Subtle hover nudge */
}}

.sidebar .close-item {{
    margin-bottom: 10px;
}}

/* ==================== 
   Main Content Area
   ==================== */
.content {{
    padding: 60px 40px;
    color: var(--nav-text);
    max-width: 800px;
}}

.content h1 {{
    font-size: 2.5rem;
    margin-bottom: 16px;
}}

.content p {{
    font-size: 1.1rem;
    line-height: 1.6;
    opacity: 0.8;
}}


/* ==================== 
   Container Queries (Responsiveness)
   ==================== */
@container viewport (max-width: 800px) {{
    .hideOnMobile {{
        display: none;
    }}
    .menu-item {{
        display: block; /* Show hamburger button */
    }}
    .content h1 {{ font-size: 2rem; }}
}}

@container viewport (max-width: 400px) {{
    .sidebar {{
        width: 100%; /* Full screen takeover on very small devices */
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
    <!-- Fonts & Icons -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0" />
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <!-- Container acts as an isolated viewport for reliable component rendering -->
    <div class="container">
    
        <!-- Desktop Nav -->
        <nav>
            <a href="#" class="logo">{title_text}</a>
            <ul class="nav-links">
                <li class="hideOnMobile"><a href="#">Blog</a></li>
                <li class="hideOnMobile"><a href="#">Products</a></li>
                <li class="hideOnMobile"><a href="#">About</a></li>
                <li class="hideOnMobile"><a href="#">Forum</a></li>
                <li class="hideOnMobile"><a href="#">Login</a></li>
                <li class="menu-item">
                    <button class="menu-btn" aria-label="Open Mobile Menu">
                        <span class="material-symbols-outlined">menu</span>
                    </button>
                </li>
            </ul>
        </nav>

        <!-- Slide-out Sidebar -->
        <ul class="sidebar">
            <li class="close-item">
                <button class="close-btn" aria-label="Close Mobile Menu">
                    <span class="material-symbols-outlined">close</span>
                </button>
            </li>
            <li><a href="#">Blog</a></li>
            <li><a href="#">Products</a></li>
            <li><a href="#">About</a></li>
            <li><a href="#">Forum</a></li>
            <li><a href="#">Login</a></li>
        </ul>
        
        <!-- Page Content -->
        <main class="content">
            <h1>Welcome to {title_text}</h1>
            <p>{body_text}</p>
        </main>

    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Sidebar Interaction Logic
document.addEventListener('DOMContentLoaded', () => {{
    const sidebar = document.querySelector('.sidebar');
    const menuBtn = document.querySelector('.menu-btn');
    const closeBtn = document.querySelector('.close-btn');

    // Open sidebar
    menuBtn.addEventListener('click', () => {{
        sidebar.classList.add('active');
    }});

    // Close sidebar
    closeBtn.addEventListener('click', () => {{
        sidebar.classList.remove('active');
    }});

    // Optional: Close sidebar when clicking outside of it
    document.addEventListener('click', (e) => {{
        if (!sidebar.contains(e.target) && !menuBtn.contains(e.target) && sidebar.classList.contains('active')) {{
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
