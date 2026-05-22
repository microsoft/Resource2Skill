def create_component(
    output_dir: str,
    title_text: str = "Why not Your own Services?",
    body_text: str = "Start Your Self-Hosting Journey with us! Toggle the switch to change the mood.",
    color_scheme: str = "light",        # "dark" or "light"
    accent_color: str = "#fa39ad",      # Base accent color (used for light mode orb)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Ambient Glassmorphism Theme Switcher.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)
    
    # Determine initial states based on color_scheme parameter
    body_class = ' class="dark-mode"' if color_scheme == "dark" else ""
    checked_attr = ' checked' if color_scheme == "dark" else ""

    # === CSS ===
    css = f"""/* Ambient Glassmorphism Theme Switcher */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    /* Light Theme Defaults */
    --bg-color: #f3f3f3;
    --text-color: #1a1a2e;
    --text-muted: #666;
    
    /* Light Mode Ambient Orbs */
    --orb-1-start: {accent_color};
    --orb-1-end: #fa6c4c;
    --orb-2-start: #ffb2cd;
    --orb-2-end: #ffecd2;
    
    /* Light Mode Glass */
    --glass-bg: rgba(255, 255, 255, 0.6);
    --glass-border: rgba(255, 255, 255, 0.8);
    --glass-shadow: rgba(0, 0, 0, 0.05);
    
    /* Light Mode Switch */
    --switch-bg: #ffb2cd;
    --switch-handle: #ffffff;
}}

body.dark-mode {{
    /* Dark Theme Overrides */
    --bg-color: #0c1a1a;
    --text-color: #ffffff;
    --text-muted: #a0aab5;
    
    /* Dark Mode Ambient Orbs */
    --orb-1-start: #00ffaa;
    --orb-1-end: #0066ff;
    --orb-2-start: #4a00e0;
    --orb-2-end: #8e2de2;
    
    /* Dark Mode Glass */
    --glass-bg: rgba(12, 26, 26, 0.5);
    --glass-border: rgba(255, 255, 255, 0.08);
    --glass-shadow: rgba(0, 0, 0, 0.3);
    
    /* Dark Mode Switch */
    --switch-bg: #00ffaa;
    --switch-handle: #0c1a1a;
}}

body {{
    font-family: 'Poppins', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    position: relative;
    transition: background-color 0.6s ease, color 0.6s ease;
}}

/* Ambient Background Orbs */
.ambient-orb {{
    position: absolute;
    border-radius: 50%;
    filter: blur(100px);
    z-index: 0;
    transition: background 0.8s ease, opacity 0.8s ease;
}}

.orb-1 {{
    width: 450px;
    height: 450px;
    top: 10%;
    left: 20%;
    background: linear-gradient(135deg, var(--orb-1-start), var(--orb-1-end));
    opacity: 0.8;
}}

.orb-2 {{
    width: 350px;
    height: 350px;
    bottom: 10%;
    right: 20%;
    background: linear-gradient(135deg, var(--orb-2-start), var(--orb-2-end));
    opacity: 0.6;
}}

/* Main Application Container */
.app-container {{
    position: relative;
    z-index: 10;
    width: 90%;
    max-width: 900px;
    height: 60vh;
    min-height: 500px;
    
    /* Glassmorphism Core */
    background: var(--glass-bg);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border: 1px solid var(--glass-border);
    border-radius: 24px;
    box-shadow: 0 20px 40px var(--glass-shadow);
    
    padding: 40px;
    display: flex;
    flex-direction: column;
    transition: all 0.6s ease;
}}

/* Header & Toggle Layout */
.header {{
    display: flex;
    justify-content: flex-end;
    align-items: center;
    width: 100%;
    margin-bottom: 60px;
}}

.theme-toggle-wrapper {{
    display: flex;
    align-items: center;
    gap: 16px;
    font-weight: 600;
    font-size: 0.95rem;
}}

/* Custom CSS Switch */
.switch-checkbox {{
    display: none;
}}

.switch-label {{
    width: 54px;
    height: 30px;
    background-color: var(--switch-bg);
    border-radius: 100px;
    position: relative;
    cursor: pointer;
    transition: background-color 0.4s ease;
}}

.switch-indicator {{
    width: 24px;
    height: 24px;
    background-color: var(--switch-handle);
    border-radius: 50%;
    position: absolute;
    top: 3px;
    left: 3px;
    transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1), background-color 0.4s ease;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}}

.switch-checkbox:checked + .switch-label .switch-indicator {{
    transform: translateX(24px);
}}

/* Typography inside Glass */
.content {{
    text-align: center;
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}}

h1 {{
    font-size: 3.5rem;
    font-weight: 700;
    margin-bottom: 20px;
    line-height: 1.2;
    letter-spacing: -1px;
}}

p {{
    font-size: 1.25rem;
    color: var(--text-muted);
    font-weight: 400;
    max-width: 600px;
    line-height: 1.6;
    transition: color 0.6s ease;
}}

/* Responsive Scaling */
@media (max-width: 768px) {{
    h1 {{ font-size: 2.5rem; }}
    .app-container {{ padding: 24px; height: 80vh; }}
    .orb-1 {{ width: 300px; height: 300px; }}
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
<body{body_class} style="width: {width_px}px; height: {height_px}px; max-width: 100vw; max-height: 100vh;">
    
    <!-- Ambient Lighting Layer -->
    <div class="ambient-orb orb-1"></div>
    <div class="ambient-orb orb-2"></div>

    <!-- Glassmorphism Application Layer -->
    <div class="app-container">
        
        <!-- Header with Switch -->
        <header class="header">
            <div class="theme-toggle-wrapper">
                <span id="theme-label">Lights</span>
                <input type="checkbox" id="theme-toggle" class="switch-checkbox"{checked_attr}>
                <label for="theme-toggle" class="switch-label" aria-label="Toggle dark mode">
                    <span class="switch-indicator"></span>
                </label>
            </div>
        </header>

        <!-- Main Content -->
        <main class="content">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </main>
        
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Ambient Glassmorphism Theme Switcher Logic
document.addEventListener('DOMContentLoaded', () => {{
    const themeToggle = document.getElementById('theme-toggle');
    const themeLabel = document.getElementById('theme-label');
    const body = document.body;

    // Optional: Synchronize label text with state
    const updateLabel = (isDark) => {{
        // While the video keeps it as "Lights", changing it provides better UX feedback
        themeLabel.textContent = isDark ? "Neon" : "Lights"; 
    }};

    // Initialize state
    updateLabel(themeToggle.checked);

    // Event Listener for the custom toggle
    themeToggle.addEventListener('change', function() {{
        const isDarkMode = this.checked;
        
        // Toggle class to trigger CSS Variable cascade
        if (isDarkMode) {{
            body.classList.add('dark-mode');
        }} else {{
            body.classList.remove('dark-mode');
        }}
        
        updateLabel(isDarkMode);
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
