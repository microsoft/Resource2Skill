def create_component(
    output_dir: str,
    title_text: str = "TVS Pharmacy",
    body_text: str = "Now delivering Rx + more. Find out now",
    color_scheme: str = "light",       # "dark" or "light"
    accent_color: str = "#cc0000",     # Original tutorial used red
    width_px: int = 400,               # Mobile viewport width
    height_px: int = 800,              # Mobile viewport height
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Mobile App Shell visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#121212"
        surface_color = "#1e1e1e"
        text_color = "#e0e0e0"
        text_muted = "#a0a0a0"
        border_color = "#333333"
        footer_bg = "#000000"
        shadow = "rgba(0, 0, 0, 0.5)"
    else:
        bg_color = "#ffffff"
        surface_color = "#ffffff"
        text_color = "#333333"
        text_muted = "#666666"
        border_color = "#e0e0e0"
        footer_bg = "#f8f9fa"
        shadow = "rgba(0, 0, 0, 0.08)"

    # === CSS ===
    css = f"""/* Mobile App Shell — generated component */
:root {{
    --bg: {bg_color};
    --surface: {surface_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --border: {border_color};
    --footer-bg: {footer_bg};
    --shadow: {shadow};
    --accent: {accent_color};
    /* Darken accent color natively in CSS using a black semi-transparent overlay */
    --accent-dark: linear-gradient(rgba(0, 0, 0, 0.2), rgba(0, 0, 0, 0.2)), linear-gradient(var(--accent), var(--accent));
    
    --app-width: {width_px}px;
    --app-height: {height_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Roboto', sans-serif;
    background-color: #f0f2f5; /* Outer desktop background */
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

/* Device Simulator Wrapper */
.device-container {{
    width: 100%;
    max-width: var(--app-width);
    height: var(--app-height);
    background: var(--bg);
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    box-shadow: 0 20px 40px rgba(0,0,0,0.2);
    border-radius: 12px;
    border: 8px solid #222; /* Simulated device bezel */
}}

/* === SPLASH SCREEN === */
#splash {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: var(--bg);
    z-index: 100;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    transition: opacity 1s ease-in-out;
    color: var(--accent);
}}
#splash.fade {{
    opacity: 0;
    pointer-events: none;
}}
#splash i {{
    font-size: 5rem;
    margin-bottom: 1rem;
}}

/* === APP LAYOUT ARCHITECTURE === */
.app-content {{
    flex: 1 0 auto;
    display: flex;
    flex-direction: column;
    overflow-y: auto;
    overflow-x: hidden;
}}

/* Header */
.app-header {{
    background: var(--accent);
    color: white;
    padding: 15px 15px 20px 15px;
    display: flex;
    flex-direction: column;
    align-items: center;
    box-shadow: 0 3px 10px rgba(0,0,0,0.2);
    z-index: 10;
}}
.app-header h1 {{
    font-size: 1.4rem;
    margin-bottom: 12px;
    font-weight: 700;
}}
.app-header h1 i {{
    margin-right: 8px;
}}
.search-bar {{
    width: 100%;
    max-width: 320px;
    padding: 10px 15px;
    border-radius: 4px;
    border: none;
    outline: none;
    font-size: 0.9rem;
}}

/* Subheader */
.subheader {{
    background-image: var(--accent-dark);
    color: white;
    padding: 15px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}
.subheader-text p {{
    font-size: 0.9rem;
    line-height: 1.4;
}}
.subheader-text .highlight {{
    font-weight: bold;
    display: flex;
    align-items: center;
    gap: 5px;
    margin-top: 4px;
}}
.subheader-icon {{
    font-size: 2rem;
    opacity: 0.9;
}}

/* Dashboard Grid */
.grid-container {{
    padding: 15px;
    flex: 1;
}}
.grid {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
}}
/* Responsive trigger matching tutorial */
@media (min-width: 768px) {{
    .grid {{
        grid-template-columns: repeat(3, 1fr);
    }}
}}

.grid-item {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 15px;
    display: flex;
    flex-direction: column;
    box-shadow: 0 2px 5px var(--shadow);
    cursor: pointer;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}
.grid-item:active {{
    transform: scale(0.98);
}}
.grid-item h4 {{
    color: var(--text);
    font-size: 1rem;
    margin-bottom: 4px;
}}
.grid-item p {{
    color: var(--text-muted);
    font-size: 0.75rem;
    margin-bottom: 15px;
    line-height: 1.3;
}}
.grid-item .item-icon {{
    align-self: flex-end;
    font-size: 2.5rem;
    color: var(--accent);
    margin-top: auto;
}}

/* Sticky Footer */
.app-footer {{
    flex-shrink: 0;
    background: var(--footer-bg);
    border-top: 1px solid var(--border);
    padding: 10px 0;
    padding-bottom: max(10px, env(safe-area-inset-bottom)); /* iOS safe area */
}}
.app-footer ul {{
    list-style: none;
    display: flex;
    justify-content: space-around;
    align-items: center;
}}
.app-footer li {{
    display: flex;
    flex-direction: column;
    align-items: center;
    color: var(--text-muted);
    font-size: 0.7rem;
    cursor: pointer;
    transition: color 0.2s ease;
}}
.app-footer li:hover, .app-footer li.active {{
    color: var(--accent);
}}
.app-footer li i {{
    font-size: 1.4rem;
    margin-bottom: 4px;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <!-- Fonts and Icons matching original tutorial requirements -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <div class="device-container">
        
        <!-- Splash Overlay -->
        <div id="splash">
            <i class="fa fa-heartbeat"></i>
            <h2>{title_text}</h2>
        </div>

        <!-- Scrollable Content Area -->
        <div class="app-content">
            
            <header class="app-header">
                <h1><i class="fa fa-heartbeat"></i> {title_text}</h1>
                <input type="text" class="search-bar" placeholder="Search...">
            </header>

            <div class="subheader">
                <div class="subheader-text">
                    <p>{body_text}</p>
                    <p class="highlight">Find out now <i class="fa fa-chevron-right"></i></p>
                </div>
                <div class="subheader-icon">
                    <i class="fa fa-truck"></i>
                </div>
            </div>

            <div class="grid-container">
                <div class="grid">
                    <div class="grid-item">
                        <h4>Pharmacy</h4>
                        <p>2 Rx ready for refill</p>
                        <i class="fa fa-medkit item-icon"></i>
                    </div>
                    <div class="grid-item">
                        <h4>Deals & Rewards</h4>
                        <p>2 ExtraCare offers expiring</p>
                        <i class="fa fa-star item-icon" style="color: #f1c40f;"></i>
                    </div>
                    <div class="grid-item">
                        <h4>MinuteClinic</h4>
                        <p>Schedule an appointment</p>
                        <i class="fa fa-user-md item-icon"></i>
                    </div>
                    <div class="grid-item">
                        <h4>Shop</h4>
                        <p>Free shipping on orders $35+</p>
                        <i class="fa fa-shopping-cart item-icon"></i>
                    </div>
                    <div class="grid-item">
                        <h4>Photo</h4>
                        <p>Same day pickup available</p>
                        <i class="fa fa-camera item-icon"></i>
                    </div>
                    <div class="grid-item">
                        <h4>Weekly Ad</h4>
                        <p>View your local deals</p>
                        <i class="fa fa-newspaper-o item-icon"></i>
                    </div>
                </div>
            </div>

        </div>

        <!-- Sticky Bottom Footer -->
        <footer class="app-footer">
            <ul>
                <li class="active">
                    <i class="fa fa-home"></i>
                    <span>Home</span>
                </li>
                <li>
                    <i class="fa fa-barcode"></i>
                    <span>Show Card</span>
                </li>
                <li>
                    <i class="fa fa-user"></i>
                    <span>Account</span>
                </li>
                <li>
                    <i class="fa fa-map-marker"></i>
                    <span>Find Store</span>
                </li>
            </ul>
        </footer>

    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Mobile App Shell — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const splash = document.getElementById('splash');
    
    // Simulate app load time, then trigger fade out
    setTimeout(() => {{
        splash.classList.add('fade');
        
        // Remove from DOM entirely after transition completes (1 second)
        // This ensures the splash screen doesn't block pointer events
        setTimeout(() => {{
            splash.style.display = 'none';
        }}, 1000);
        
    }}, 1500); // 1.5 seconds loading simulation
    
    // Optional: Add active state toggling for footer icons
    const footerItems = document.querySelectorAll('.app-footer li');
    footerItems.forEach(item => {{
        item.addEventListener('click', function() {{
            footerItems.forEach(i => i.classList.remove('active'));
            this.classList.add('active');
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
