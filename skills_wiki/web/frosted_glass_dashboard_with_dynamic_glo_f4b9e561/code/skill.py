def create_component(
    output_dir: str,
    title_text: str = "Why not Your own Services?",
    body_text: str = "Start Your Self-hosting Journey with us!",
    color_scheme: str = "light",  # "dark" or "light"
    accent_color: str = "#fb28cd",  # Main accent color (pink for light mode base)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Frosted Glass Dashboard with Dynamic Glow visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === CSS ===
    css = f"""
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@100;200;300;400;500;600;700;800;900&family=Special+Gothic+Expanded+One&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    /* Light Mode Colors */
    --body-bg: #f3f3f3;
    --text-color-primary: #292b48;
    --text-color-secondary: #877f95;
    --card-bg: rgba(255, 255, 255, 0.5);
    --card-border: transparent;
    --shadow-color: rgba(0, 0, 0, 0.08);
    --hero-glow-start: rgba(250, 57, 173, 0.2); /* #fa39ad with opacity */
    --hero-glow-end: transparent;
    --title-gradient-start: #fb28cd;
    --title-gradient-end: #7c65d7;
    --switch-bg-color: #fb28cd; /* Pink for light mode */
    --switch-indicator-color: #fff;
    --nav-item-active-line: #292b48; /* Black for light mode */
    --inner-card-bg: #f7f8ff;
    --top-nav-link-color: #292b48;
}}

body.dark-mode {{
    /* Dark Mode Overrides */
    --body-bg: #0c1a1a; /* Dark green/blue background */
    --text-color-primary: #a4f9f0; /* Light teal text */
    --text-color-secondary: #877f95;
    --card-bg: rgba(255, 255, 255, 0.05);
    --card-border: #1a3a3a;
    --shadow-color: rgba(0, 255, 255, 0.1);
    --hero-glow-start: rgba(0, 255, 170, 0.2); /* #00ffaa with opacity */
    --hero-glow-end: transparent;
    --title-gradient-start: #00ffaa;
    --title-gradient-end: #0066ff;
    --switch-bg-color: #00ffaa; /* Teal for dark mode */
    --switch-indicator-color: #fff;
    --nav-item-active-line: #a4f9f0;
    --inner-card-bg: #112222;
    --top-nav-link-color: #a4f9f0;
}}

body {{
    background-color: var(--body-bg);
    color: var(--text-color-primary);
    min-height: 100vh;
    display: flex;
    justify-content: flex-start;
    align-items: center;
    flex-direction: column;
    overflow-x: hidden;
    transition: background-color 0.3s ease-in-out, color 0.3s ease-in-out;
    font-family: 'Poppins', sans-serif;
}}

.circle {{
    position: absolute;
    top: -100px;
    left: 50%;
    transform: translateX(-50%);
    width: 800px;
    height: 800px;
    background: radial-gradient(circle at center, var(--hero-glow-start) 0%, var(--hero-glow-end) 60%);
    filter: blur(150px);
    border-radius: 50%;
    z-index: -1;
    transition: background 0.3s ease-in-out, filter 0.3s ease-in-out;
}}

.app-container {{
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    min-height: 100vh;
    padding: 20px;
}}

/* Top Navigation Bar */
.nav-bar {{
    width: {width_px * 0.8}px; /* Approx 80% of specified width */
    max-width: {width_px}px; /* Adjusted to fit the video look */
    display: flex;
    align-items: center;
    padding: 10px 0;
    font-size: 0.875rem;
    font-weight: 500;
    position: relative;
    z-index: 20;
}}

.nav-bar > a {{
    display: flex;
    align-items: center;
    text-decoration: none;
    color: var(--top-nav-link-color);
    margin-right: 20px;
    transition: color 0.3s ease-in-out;
}}

.nav-bar > a:hover {{
    opacity: 0.8;
}}

.nav-bar > a i {{
    margin-right: 8px;
    font-size: 1rem;
    color: var(--top-nav-link-color);
    transition: color 0.3s ease-in-out;
}}

/* Specific icon colors, as they are static or less affected by dark mode */
.nav-bar > a .fa-star {{ color: #ffa41d; }} /* Yellow */
.nav-bar > a .fa-youtube {{ color: #ff0000; }} /* YouTube Red */
.nav-bar > a .fa-dribbble {{ color: #ea4c89; }} /* Dribbble Pink */
.nav-bar .right-nav {{
    display: flex;
    align-items: center;
    gap: 15px;
    margin-left: auto;
}}

.nav-bar .right-nav span {{
    font-weight: 600;
    font-size: 0.875rem;
    color: var(--text-color-primary);
    cursor: pointer;
    user-select: none;
    transition: color 0.3s ease-in-out;
}}
.nav-bar .right-nav span:hover {{
    color: var(--title-gradient-start); /* Use accent for hover */
}}

.nav-bar .right-nav i {{
    font-size: 0.875rem;
    color: var(--text-color-primary);
    cursor: pointer;
    transition: color 0.3s ease-in-out;
}}

/* Hero Section */
.hero-content {{
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    margin-top: 100px;
    margin-bottom: 80px;
    position: relative;
    z-index: 1;
}}

.app-title {{
    font-family: 'Special Gothic Expanded One', sans-serif;
    font-size: 3rem;
    font-weight: 700;
    line-height: 1.2;
    background: linear-gradient(45deg, var(--title-gradient-start), var(--title-gradient-end));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    transition: background 0.3s ease-in-out;
}}

.app-subtitle {{
    font-size: 1rem;
    font-weight: 500;
    color: var(--text-color-secondary);
    margin-top: 10px;
    transition: color 0.3s ease-in-out;
}}

/* Main Content Card */
.main-content-card {{
    position: relative;
    width: {width_px * 0.6}px; /* 60% of specified width */
    max-width: 900px;
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    padding: 2.5rem 1.5rem;
    border-radius: 0.75rem;
    box-shadow: 0 10px 25px var(--shadow-color);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    transition: background 0.3s ease-in-out, border-color 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
    z-index: 10;
}}

.tabs {{
    display: flex;
    justify-content: center;
    margin-bottom: 20px;
    border-bottom: 1px solid rgba(0, 0, 0, 0.1);
    padding-bottom: 10px;
    position: relative;
}}
body.dark-mode .tabs {{
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}}

.tab-item {{
    font-weight: 600;
    font-size: 0.875rem;
    color: var(--text-color-secondary);
    padding: 5px 15px;
    cursor: pointer;
    position: relative;
    transition: color 0.3s ease-in-out;
    user-select: none;
}}

.tab-item.active {{
    color: var(--text-color-primary);
}}

.tab-item.active::after {{
    content: '';
    position: absolute;
    bottom: -11px;
    left: 15px;
    width: calc(100% - 30px);
    height: 2px;
    background-color: var(--nav-item-active-line);
    transition: background-color 0.3s ease-in-out;
}}

.cards-grid {{
    display: flex;
    gap: 1.5rem;
    justify-content: center;
    flex-wrap: wrap;
}}

.content-card {{
    background-color: var(--inner-card-bg);
    border-radius: 0.5rem;
    padding: 1rem;
    flex: 1 1 calc(33% - 1rem); /* Approx w-1/3 minus gap */
    min-width: 180px;
    max-width: 250px; /* Max width to prevent excessive stretching */
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out, background-color 0.3s ease-in-out;
    cursor: pointer;
}}
.content-card:hover {{
    transform: translateY(-3px);
    box-shadow: 0 8px 12px var(--shadow-color);
}}

.card-title {{
    font-weight: 600;
    font-size: 0.95rem;
    color: var(--text-color-primary);
    margin-bottom: 5px;
    transition: color 0.3s ease-in-out;
}}

.card-subtitle {{
    font-size: 0.8rem;
    color: var(--text-color-secondary);
    transition: color 0.3s ease-in-out;
}}

/* Dark Mode Switch */
.lights-toggle {{
    position: absolute;
    right: 0;
    top: 50%;
    transform: translateY(-50%);
    display: flex;
    align-items: center;
}}

.switch-label {{
    display: flex;
    align-items: center;
    cursor: pointer;
    font-weight: 600;
    font-size: 0.875rem;
    color: var(--text-color-primary);
    transition: color 0.3s ease-in-out;
    user-select: none;
}}

.lights-text {{
    margin-right: 10px;
}}

.switch-checkbox {{
    display: none;
}}

.switch-bg {{
    position: relative;
    width: 44px;
    height: 24px;
    background-color: var(--switch-bg-color);
    border-radius: 15px;
    transition: background-color 0.3s ease-in-out;
}}

.switch-indicator {{
    position: absolute;
    top: 2px;
    left: 2px;
    width: 20px;
    height: 20px;
    background-color: var(--switch-indicator-color);
    border-radius: 50%;
    transition: transform 0.2s ease-in-out;
}}

.switch-checkbox:checked + .switch-bg .switch-indicator {{
    transform: translateX(20px);
}}

/* Responsive adjustments */
@media (max-width: 768px) {{
    .main-content-card {{
        width: 90%;
        padding: 1.5rem 1rem;
    }}
    .hero-content {{
        margin-top: 50px;
        margin-bottom: 50px;
    }}
    .app-title {{
        font-size: 2.2rem;
    }}
    .app-subtitle {{
        font-size: 0.9rem;
    }}
    .cards-grid {{
        flex-direction: column;
        align-items: center;
    }}
    .content-card {{
        max-width: 100%;
        flex: 1 1 100%;
    }}
    .tabs {{
        flex-wrap: wrap;
        justify-content: space-between;
        gap: 10px;
    }}
    .lights-toggle {{
        position: relative;
        top: auto;
        transform: none;
        margin-left: auto;
        margin-top: 10px;
        width: 100%;
        justify-content: flex-end;
    }}
    .nav-bar {{
        width: 100%;
        flex-wrap: wrap;
        justify-content: center;
        gap: 10px;
    }}
    .nav-bar > a {{
        margin-right: 0;
    }}
    .nav-bar .right-nav {{
        margin-left: 0;
        width: 100%;
        justify-content: center;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Echoes of Ping | Home</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Special+Gothic+Expanded+One&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="circle"></div>
    <div class="app-container">
        <!-- Top Navigation -->
        <div class="nav-bar">
            <a href="https://echoesofping.hashnode.dev" target="_blank" rel="noopener noreferrer">
                <i class="fa-solid fa-star app-color-yellow"></i>
                <span style="font-weight: 700;">echoesofping.hashnode.dev</span>
            </a>
            <div class="right-nav">
                <a href="https://youtube.com/@echoes-of-ping" target="_blank" rel="noopener noreferrer">
                    <i class="fa-brands fa-youtube"></i>
                    <span style="font-weight: 700;">Youtube</span>
                </a>
                <span style="font-weight: 700;">Join Now</span>
                <i class="fa-regular fa-user"></i>
                <i class="fa-solid fa-angle-down"></i>
            </div>
        </div>

        <!-- Hero Section -->
        <div class="hero-content">
            <span class="app-title">{title_text}</span>
            <span class="app-subtitle">{body_text}</span>
        </div>

        <!-- Main Content Card -->
        <div class="main-content-card">
            <div class="tabs">
                <span class="tab-item" data-tab="posts">Posts</span>
                <span class="tab-item" data-tab="blogs">Blogs</span>
                <span class="tab-item active" data-tab="videos">Videos</span>
                <div class="lights-toggle">
                    <label class="switch-label" for="darkToggle">
                        <span class="lights-text">Lights</span>
                        <input type="checkbox" id="darkToggle" class="switch-checkbox">
                        <div class="switch-bg">
                            <div class="switch-indicator"></div>
                        </div>
                    </label>
                </div>
            </div>
            <div class="cards-grid">
                <div class="content-card">
                    <span class="card-title">Installation Guide</span>
                    <span class="card-subtitle">Speedtest-Tracker</span>
                </div>
                <div class="content-card">
                    <span class="card-title">Setup</span>
                    <span class="card-subtitle">Uptime-Kuma</span>
                </div>
                <div class="content-card">
                    <span class="card-title">Playlist</span>
                    <span class="card-subtitle">HomeLab(Self-hosting)</span>
                </div>
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """
document.addEventListener('DOMContentLoaded', () => {
    const darkToggle = document.getElementById('darkToggle');
    const body = document.body;
    const tabItems = document.querySelectorAll('.tab-item');

    // Load theme preference from localStorage
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        body.classList.add('dark-mode');
        darkToggle.checked = true;
    } else {
        // Ensure light mode is applied if no preference or 'light' is saved
        body.classList.remove('dark-mode');
        darkToggle.checked = false; // Ensure checkbox reflects current mode
    }

    // Toggle dark mode on switch change
    darkToggle.addEventListener('change', () => {
        if (darkToggle.checked) {
            body.classList.add('dark-mode');
            localStorage.setItem('theme', 'dark');
        } else {
            body.classList.remove('dark-mode');
            localStorage.setItem('theme', 'light');
        }
    });

    // Handle tab clicks
    tabItems.forEach(item => {
        item.addEventListener('click', () => {
            tabItems.forEach(tab => tab.classList.remove('active'));
            item.classList.add('active');
            // In a real application, you would load/display content here based on item.dataset.tab
            // For this reproduction, only visual active state changes.
        });
    });
});
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

