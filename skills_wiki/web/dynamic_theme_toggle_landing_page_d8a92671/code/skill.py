def create_component(
    output_dir: str,
    title_text: str = "Level up your",
    accent_text: str = "Coding Skills",
    body_text: str = "We're providing quality content on Web Development and other programming languages for free. Join us now and level up your coding skills.",
    color_scheme: str = "light",       # "dark" or "light"
    accent_color: str = "#7cd1b8",     # Mint green accent from tutorial
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Dynamic Theme Toggle Landing Page.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)
    
    initial_theme_class = "dark-theme" if color_scheme == "dark" else ""

    # === CSS ===
    css = f"""/* Dynamic Theme Toggle Landing Page */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');

:root {{
    /* Base Color Tokens */
    --bg-light: #ffffff;
    --text-light: #1b1b1b;
    --bg-dark: #1b1b1b;
    --text-dark: #ffffff;
    
    /* Configurable Accent */
    --accent-color: {accent_color};
    
    /* Transition Settings */
    --transition-speed: 0.4s;
}}

body {{
    margin: 0;
    padding: 0;
    background-color: #e0e5ec; /* Outer backdrop for preview context */
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    font-family: 'Poppins', sans-serif;
}}

/* The main component wrapper acts as the theme context */
.theme-wrapper {{
    width: {width_px}px;
    height: {height_px}px;
    max-width: 100vw;
    
    /* Default to Light Mode Variables */
    --current-bg: var(--bg-light);
    --current-text: var(--text-light);
    
    background-color: var(--current-bg);
    color: var(--current-text);
    transition: background-color var(--transition-speed) ease, color var(--transition-speed) ease;
    
    display: flex;
    flex-direction: column;
    position: relative;
    overflow: hidden;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}}

/* Override variables when dark-theme class is active */
.theme-wrapper.dark-theme {{
    --current-bg: var(--bg-dark);
    --current-text: var(--text-dark);
}}

/* --- Navbar --- */
.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 30px 5%;
}}

.logo {{
    font-size: 1.5rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1px;
}}

.logo span {{
    color: var(--accent-color);
}}

.nav-links {{
    list-style: none;
    display: flex;
    gap: 30px;
    margin: 0;
    padding: 0;
}}

.nav-links a {{
    text-decoration: none;
    color: var(--current-text);
    font-weight: 600;
    font-size: 0.95rem;
    text-transform: uppercase;
    transition: color 0.2s ease;
}}

.nav-links a:hover {{
    color: var(--accent-color);
}}

.theme-toggle {{
    background: transparent;
    border: none;
    color: var(--current-text);
    font-size: 1.5rem;
    cursor: pointer;
    transition: transform 0.2s ease, color var(--transition-speed) ease;
    outline: none;
}}

.theme-toggle:hover {{
    color: var(--accent-color);
    transform: scale(1.1) rotate(-10deg);
}}

/* --- Hero Section --- */
.hero {{
    flex: 1;
    display: flex;
    align-items: center;
    padding: 0 5%;
}}

.hero-content {{
    flex: 1;
    padding-right: 5%;
    z-index: 2;
}}

.hero-content h1 {{
    font-size: clamp(2.5rem, 4vw, 4rem);
    line-height: 1.1;
    font-weight: 800;
    text-transform: uppercase;
    margin: 0 0 20px 0;
}}

.hero-content .accent {{
    color: var(--accent-color);
}}

.hero-content p {{
    font-size: 1rem;
    line-height: 1.6;
    margin-bottom: 40px;
    opacity: 0.85;
    max-width: 85%;
}}

.hero-actions {{
    display: flex;
    align-items: center;
    gap: 30px;
}}

.btn-primary {{
    background-color: var(--current-text);
    color: var(--current-bg);
    border: 2px solid var(--current-text);
    padding: 12px 30px;
    font-size: 1rem;
    font-weight: 600;
    border-radius: 4px;
    cursor: pointer;
    text-transform: uppercase;
    transition: background-color var(--transition-speed), color var(--transition-speed), transform 0.2s ease;
    font-family: inherit;
}}

.btn-primary:hover {{
    transform: translateY(-3px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}}

.social-links {{
    display: flex;
    gap: 15px;
}}

.social-links a {{
    color: var(--current-text);
    font-size: 1.5rem;
    transition: color 0.2s ease, transform 0.2s ease;
}}

.social-links a:hover {{
    color: var(--accent-color);
    transform: translateY(-3px);
}}

/* --- Hero Image Placeholder (SVG Blob) --- */
.hero-image {{
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
}}

.blob-shape {{
    width: 100%;
    max-width: 500px;
    fill: var(--accent-color);
    opacity: 0.9;
    animation: morph 8s ease-in-out infinite alternate, float 6s ease-in-out infinite alternate;
}}

@keyframes morph {{
    0% {{ border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%; }}
    50% {{ border-radius: 30% 60% 70% 40% / 50% 60% 30% 60%; }}
    100% {{ border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%; }}
}}

@keyframes float {{
    0% {{ transform: translateY(0px); }}
    100% {{ transform: translateY(-20px); }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text} {accent_text}</title>
    <!-- FontAwesome for Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    
    <!-- Component Wrapper acts as the theming context boundary -->
    <div class="theme-wrapper {initial_theme_class}" id="theme-context">
        
        <nav class="navbar">
            <div class="logo">Coding<span>Master</span></div>
            <ul class="nav-links">
                <li><a href="#">Home</a></li>
                <li><a href="#">About</a></li>
                <li><a href="#">Services</a></li>
                <li><a href="#">Join Us</a></li>
            </ul>
            <button class="theme-toggle" id="theme-btn" aria-label="Toggle Dark/Light Mode">
                <i class="fas fa-moon"></i>
            </button>
        </nav>

        <main class="hero">
            <div class="hero-content">
                <h1>{title_text} <br><span class="accent">{accent_text}</span></h1>
                <p>{body_text}</p>
                <div class="hero-actions">
                    <button class="btn-primary">Apply Now</button>
                    <div class="social-links">
                        <a href="#" aria-label="GitHub"><i class="fab fa-github"></i></a>
                        <a href="#" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
                        <a href="#" aria-label="LinkedIn"><i class="fab fa-linkedin-in"></i></a>
                    </div>
                </div>
            </div>
            
            <div class="hero-image">
                <!-- Decorative Abstract SVG Blob replacing external image dependencies -->
                <svg class="blob-shape" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
                    <path d="M44.7,-76.4C58.8,-69.2,71.8,-59.1,81.6,-46.1C91.4,-33.1,98,-16.6,97.3,-0.4C96.6,15.8,88.6,31.6,78.2,45.2C67.8,58.8,55.1,70.2,40.7,77.5C26.3,84.8,10.2,88,-5.5,86.6C-21.2,85.2,-36.5,79.2,-50.2,70.6C-63.9,62,-76,50.8,-83.4,37.1C-90.8,23.4,-93.5,7.2,-91.3,-8.3C-89.1,-23.8,-82,-38.6,-71.4,-50.3C-60.8,-62,-46.7,-70.6,-32.1,-76.7C-17.5,-82.8,-2.4,-86.4,12.2,-84.9C26.8,-83.4,41.9,-76.8,53.4,-67.2Z" transform="translate(100 100)" />
                </svg>
            </div>
        </main>

    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Dynamic Theme Toggle Logic
document.addEventListener('DOMContentLoaded', () => {{
    const themeContext = document.getElementById('theme-context');
    const themeBtn = document.getElementById('theme-btn');
    const themeIcon = themeBtn.querySelector('i');

    // Function to update the icon based on current class
    const updateIcon = () => {{
        if (themeContext.classList.contains('dark-theme')) {{
            // Currently dark, show Sun to indicate switch to light
            themeIcon.className = 'fas fa-sun';
        }} else {{
            // Currently light, show Moon to indicate switch to dark
            themeIcon.className = 'fas fa-moon';
        }}
    }};

    // Initialize icon state on load
    updateIcon();

    // Toggle event
    themeBtn.addEventListener('click', () => {{
        themeContext.classList.toggle('dark-theme');
        updateIcon();
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
