def create_component(
    output_dir: str,
    title_text: str = "Why not Your own Services?",
    body_text: str = "Start Your Self-Hosting Journey with us!",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#ec4899",     # Pink accent default
    width_px: int = 1000,
    height_px: int = 700,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Animated Sliding Tab Navigation 
    with ambient glowing background and theme toggle.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Base setup
    default_dark = "dark" if color_scheme == "dark" else ""
    
    # === CSS ===
    css = f"""/* Animated Sliding Tabs Component */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap');

:root {{
    /* Light Theme Variables (Default) */
    --bg-base: #f8fafc;
    --text-main: #0f172a;
    --text-muted: #64748b;
    --nav-bg: rgba(255, 255, 255, 0.6);
    --pill-bg: #ffffff;
    --pill-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    --glow-1: {accent_color};
    --glow-2: #8b5cf6;
}}

.dark {{
    /* Dark Theme Variables */
    --bg-base: #020617;
    --text-main: #f8fafc;
    --text-muted: #94a3b8;
    --nav-bg: rgba(30, 41, 59, 0.5);
    --pill-bg: #334155;
    --pill-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
    --glow-1: #059669; /* Deep emerald */
    --glow-2: #0284c7; /* Deep blue */
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Poppins', sans-serif;
    background-color: #000; /* Outer canvas */
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

.widget-container {{
    width: {width_px}px;
    height: {height_px}px;
    max-width: 100%;
    background-color: var(--bg-base);
    color: var(--text-main);
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    align-items: center;
    transition: background-color 0.5s ease, color 0.5s ease;
    border-radius: 16px;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
}}

/* Ambient Background Glows */
.ambient-glow {{
    position: absolute;
    border-radius: 50%;
    filter: blur(80px);
    opacity: 0.4;
    z-index: 0;
    transition: background-color 0.8s ease;
    pointer-events: none;
}}

.glow-1 {{
    width: 600px;
    height: 600px;
    background-color: var(--glow-1);
    top: -200px;
    left: -100px;
}}

.glow-2 {{
    width: 500px;
    height: 500px;
    background-color: var(--glow-2);
    bottom: -150px;
    right: -100px;
}}

/* Header & Controls */
.header-controls {{
    width: 100%;
    display: flex;
    justify-content: flex-end;
    padding: 24px 32px;
    z-index: 10;
}}

.theme-toggle {{
    background: var(--nav-bg);
    border: 1px solid rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    padding: 8px 16px;
    border-radius: 20px;
    cursor: pointer;
    font-family: inherit;
    font-size: 14px;
    font-weight: 500;
    color: var(--text-main);
    display: flex;
    align-items: center;
    gap: 8px;
    transition: all 0.2s ease;
}}

.theme-toggle:hover {{
    transform: translateY(-2px);
}}

/* Content Area */
.content-wrapper {{
    z-index: 10;
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    margin-top: 60px;
}}

.main-title {{
    font-size: 42px;
    font-weight: 600;
    margin-bottom: 8px;
    text-align: center;
}}

.subtitle {{
    font-size: 16px;
    color: var(--text-muted);
    margin-bottom: 48px;
    text-align: center;
}}

/* Navigation Bar */
.tab-nav {{
    background: var(--nav-bg);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 8px;
    border-radius: 100px;
    display: inline-flex;
    position: relative;
}}

.tab-indicator {{
    position: absolute;
    top: 8px;
    left: 0;
    height: calc(100% - 16px);
    background: var(--pill-bg);
    border-radius: 100px;
    box-shadow: var(--pill-shadow);
    transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1), width 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    z-index: 1;
}}

.tab-btn {{
    position: relative;
    z-index: 2;
    background: transparent;
    border: none;
    padding: 12px 32px;
    font-family: inherit;
    font-size: 15px;
    font-weight: 500;
    color: var(--text-muted);
    cursor: pointer;
    border-radius: 100px;
    transition: color 0.3s ease;
}}

.tab-btn:hover {{
    color: var(--text-main);
}}

.tab-btn.active {{
    color: var(--text-main);
    font-weight: 600;
}}

/* Dummy Content Grid */
.tab-content-area {{
    margin-top: 48px;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
    width: 80%;
    opacity: 0;
    transform: translateY(10px);
    animation: fadeUp 0.5s forwards 0.2s;
}}

.content-card {{
    background: var(--nav-bg);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.05);
    padding: 24px;
    border-radius: 16px;
    height: 120px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}}

.card-label {{ font-size: 12px; color: var(--text-muted); margin-bottom: 4px; }}
.card-title {{ font-size: 18px; font-weight: 600; }}

@keyframes fadeUp {{
    to {{ opacity: 1; transform: translateY(0); }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="widget-container {default_dark}" id="appRoot">
        
        <!-- Ambient Orbs -->
        <div class="ambient-glow glow-1"></div>
        <div class="ambient-glow glow-2"></div>

        <!-- Header -->
        <div class="header-controls">
            <button class="theme-toggle" id="themeToggle">
                <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
                    <circle cx="12" cy="12" r="5"></circle>
                    <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"></path>
                </svg>
                Toggle Theme
            </button>
        </div>

        <div class="content-wrapper">
            <h1 class="main-title">{title_text}</h1>
            <p class="subtitle">{body_text}</p>

            <!-- Navigation -->
            <nav class="tab-nav">
                <div class="tab-indicator" id="tabIndicator"></div>
                <button class="tab-btn active">Posts</button>
                <button class="tab-btn">Blogs</button>
                <button class="tab-btn">Videos</button>
            </nav>

            <!-- Dummy Content to visualize layout -->
            <div class="tab-content-area">
                <div class="content-card">
                    <span class="card-label">Installation Guide</span>
                    <span class="card-title">Speedtest-Tracker</span>
                </div>
                <div class="content-card">
                    <span class="card-label">Setup</span>
                    <span class="card-title">Uptime-Kuma</span>
                </div>
                <div class="content-card">
                    <span class="card-label">Playlist</span>
                    <span class="card-title">HomeLab</span>
                </div>
            </div>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""document.addEventListener('DOMContentLoaded', () => {{
    const tabs = document.querySelectorAll('.tab-btn');
    const indicator = document.getElementById('tabIndicator');
    const themeToggle = document.getElementById('themeToggle');
    const appRoot = document.getElementById('appRoot');

    // --- Sliding Tab Logic ---
    function updateIndicator(activeTab) {{
        // Get the width of the clicked tab
        const width = activeTab.offsetWidth;
        // Get the position relative to the nav container
        const left = activeTab.offsetLeft;
        
        // Apply to indicator
        indicator.style.width = `${{width}}px`;
        indicator.style.transform = `translateX(${{left}}px)`;
    }}

    // Initialize indicator position
    const initialActive = document.querySelector('.tab-btn.active');
    if (initialActive) {{
        // Use a slight timeout to ensure DOM is fully rendered for accurate width reading
        setTimeout(() => updateIndicator(initialActive), 50);
    }}

    // Handle tab clicks
    tabs.forEach(tab => {{
        tab.addEventListener('click', (e) => {{
            // Remove active class from all
            tabs.forEach(t => t.classList.remove('active'));
            // Add active class to clicked
            e.target.classList.add('active');
            
            // Move indicator
            updateIndicator(e.target);
        }});
    }});

    // Handle window resize (recalculate indicator position)
    window.addEventListener('resize', () => {{
        const activeTab = document.querySelector('.tab-btn.active');
        if (activeTab) updateIndicator(activeTab);
    }});

    // --- Theme Toggle Logic ---
    themeToggle.addEventListener('click', () => {{
        appRoot.classList.toggle('dark');
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
