def create_component(
    output_dir: str,
    title_text: str = "Modern Responsive Design",
    body_text: str = "A toolkit of 5 native CSS/HTML techniques that scale flawlessly across every device, eliminating media query bloat and accessibility traps.",
    color_scheme: str = "dark",
    accent_color: str = "#00bfff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Comprehensive Modern Responsive Foundations.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
        surface_color = "rgba(255, 255, 255, 0.05)"
        border_color = "rgba(255, 255, 255, 0.1)"
        text_muted = "rgba(255, 255, 255, 0.65)"
    else:
        bg_color = "#ffffff"
        text_color = "#1a1a2e"
        surface_color = "rgba(0, 0, 0, 0.03)"
        border_color = "rgba(0, 0, 0, 0.1)"
        text_muted = "rgba(0, 0, 0, 0.65)"

    css = f"""/* Comprehensive Modern Responsive Foundations */
*, *::before, *::after {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --border: {border_color};
    --text-muted: {text_muted};
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    overflow-x: hidden; /* Prevent horizontal scroll from off-canvas elements */
}}

/* 
 * TIP #4: 100dvh (Dynamic Viewport Height)
 * Ensures the wrapper takes the exact visible height on mobile, 
 * ignoring expanding/collapsing browser address bars.
 */
.viewport-wrapper {{
    min-height: 100dvh;
    display: flex;
    flex-direction: column;
}}

/* Header Styles */
.top-bar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem min(5rem, 5vw);
    border-bottom: 1px solid var(--border);
    background: var(--bg);
}}

.logo {{
    font-weight: 700;
    font-size: 1.25rem;
    letter-spacing: -0.5px;
}}

button {{
    background: transparent;
    border: none;
    color: var(--text);
    cursor: pointer;
    transition: color 0.2s ease;
}}

button:hover, button:focus-visible {{
    color: var(--accent);
    outline: none;
}}

.menu-toggle {{
    font-size: 1.75rem;
    padding: 0.25rem;
}}

/* 
 * TIP #1: Relative Padding via min()
 * Establishes a fixed maximum padding (4rem/5rem) on large screens, 
 * but shrinks dynamically to a percentage (8vw/5vw) on mobile.
 */
.main-content {{
    flex: 1;
    padding: min(4rem, 8vw) min(5rem, 5vw);
    max-width: 1400px;
    margin: 0 auto;
    width: 100%;
}}

/* 
 * TIP #2: Fluid Typography via clamp()
 * Combines viewport units (vw) for scaling with rem for base/zoom accessibility.
 * Min size: 2.5rem | Ideal size: 6vw + 1rem | Max size: 5rem
 */
.fluid-title {{
    font-size: clamp(2.5rem, calc(6vw + 1rem), 5rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -1px;
    color: var(--text);
    margin-bottom: 1.5rem;
    max-width: 15ch;
}}

.fluid-title span {{
    color: var(--accent);
}}

.fluid-subtitle {{
    font-size: clamp(1rem, 2vw + 0.5rem, 1.25rem);
    color: var(--text-muted);
    line-height: 1.6;
    margin-bottom: 4rem;
    max-width: 60ch;
}}

/* 
 * TIP #3: Responsive Images via aspect-ratio
 * Prevents cumulative layout shifts (CLS) and guarantees images don't stretch.
 */
.image-gallery {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(min(100%, 300px), 1fr));
    gap: min(2rem, 4vw);
}}

.aspect-img {{
    width: 100%;
    height: auto;
    aspect-ratio: 16 / 9; /* Change to 1/1 or 4/3 as needed */
    object-fit: cover;    /* Ensures image fills the aspect ratio without distortion */
    border-radius: 12px;
    background: var(--surface);
    border: 1px solid var(--border);
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}}

/* 
 * TIP #5: Accessible Off-Canvas Menu Configuration
 * We use opacity/visibility for animation, and HTML 'inert' handles accessibility.
 */
.sidebar {{
    position: fixed;
    top: 0; 
    right: 0; 
    bottom: 0;
    width: min(350px, 85vw);
    background: var(--bg);
    border-left: 1px solid var(--border);
    padding: min(3rem, 6vw);
    transform: translateX(100%);
    opacity: 0;
    visibility: hidden;
    transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), 
                opacity 0.4s ease, 
                visibility 0.4s;
    z-index: 1000;
    box-shadow: -20px 0 50px rgba(0,0,0,0.3);
    display: flex;
    flex-direction: column;
}}

.sidebar.is-open {{
    transform: translateX(0);
    opacity: 1;
    visibility: visible;
}}

.sidebar-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 3rem;
}}

.sidebar-header h2 {{
    font-size: 1.25rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 2px;
}}

.close-toggle {{
    font-size: 2.5rem;
    line-height: 1;
}}

.nav-links {{
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}}

.nav-links a {{
    color: var(--text);
    text-decoration: none;
    font-size: clamp(1.5rem, 3vw, 2rem);
    font-weight: 600;
    transition: color 0.2s;
}}

.nav-links a:hover {{
    color: var(--accent);
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    
    <!-- Sidebar Menu (Hidden by default, 'inert' blocks keyboard/screen-reader focus) -->
    <nav id="sidebar" class="sidebar" inert>
        <div class="sidebar-header">
            <h2>Navigation</h2>
            <button id="close-menu" class="close-toggle" aria-label="Close navigation menu">&times;</button>
        </div>
        <ul class="nav-links">
            <li><a href="#">Capabilities</a></li>
            <li><a href="#">Case Studies</a></li>
            <li><a href="#">Architecture</a></li>
            <li><a href="#">Documentation</a></li>
        </ul>
    </nav>

    <!-- Main Application Wrapper -->
    <div id="app-wrapper" class="viewport-wrapper">
        <header class="top-bar">
            <div class="logo">NexusUI.</div>
            <button id="open-menu" class="menu-toggle" aria-label="Open navigation menu">&#9776;</button>
        </header>
        
        <main class="main-content">
            <h1 class="fluid-title">Responsive <span>Foundations.</span></h1>
            <p class="fluid-subtitle">{body_text}</p>
            
            <div class="image-gallery">
                <img src="https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=800&q=80" alt="Code editor setup" class="aspect-img">
                <img src="https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=800&q=80" alt="Laptop on desk" class="aspect-img">
                <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=800&q=80" alt="Data dashboard" class="aspect-img">
            </div>
        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    js = f"""document.addEventListener('DOMContentLoaded', () => {{
    const sidebar = document.getElementById('sidebar');
    const appWrapper = document.getElementById('app-wrapper');
    const openBtn = document.getElementById('open-menu');
    const closeBtn = document.getElementById('close-menu');

    function openSidebar() {{
        // Visually show sidebar
        sidebar.classList.add('is-open');
        
        // TIP #5: Accessibility State Management
        // Remove 'inert' from sidebar so it becomes interactive
        sidebar.removeAttribute('inert');
        
        // Add 'inert' to the main app wrapper so background content 
        // cannot be clicked or read by screen readers while menu is open.
        appWrapper.setAttribute('inert', '');
        
        // Push focus to the close button for keyboard users
        setTimeout(() => closeBtn.focus(), 50); 
    }}

    function closeSidebar() {{
        // Visually hide sidebar
        sidebar.classList.remove('is-open');
        
        // Reverse 'inert' states
        sidebar.setAttribute('inert', '');
        appWrapper.removeAttribute('inert');
        
        // Return focus to the button that opened the menu
        openBtn.focus();
    }}

    // Event Listeners
    openBtn.addEventListener('click', openSidebar);
    closeBtn.addEventListener('click', closeSidebar);

    // Close menu when pressing Escape key
    document.addEventListener('keydown', (e) => {{
        if (e.key === 'Escape' && sidebar.classList.contains('is-open')) {{
            closeSidebar();
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
