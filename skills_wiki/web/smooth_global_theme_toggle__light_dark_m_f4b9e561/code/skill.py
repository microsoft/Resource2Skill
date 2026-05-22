def create_component(
    output_dir: str,
    title_text: str = "Why Not Your Own Services?",
    body_text: str = "Start Your Self-Hosting Journey with us!",
    color_scheme: str = "light",       # "dark" or "light" (initial state)
    accent_color: str = "#d946ef",     # CSS hex color for light mode accent (pink)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Smooth Global Theme Toggle visual effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Base theme configurations
    dark_bg = "#0f172a"          # Slate 900
    dark_text = "#f8fafc"        # Slate 50
    dark_accent = "#14b8a6"      # Teal 500
    
    light_bg = "#fdfbfb"         # Off-white
    light_text = "#0f172a"       # Slate 900
    light_accent = accent_color

    is_dark = str(color_scheme == "dark").lower()

    # === CSS ===
    css = f"""/* Theme Toggle Component Styles */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

:root {{
    --bg-color: {light_bg};
    --text-color: {light_text};
    --accent-glow: {light_accent};
    --glass-bg: rgba(255, 255, 255, 0.4);
    --glass-border: rgba(255, 255, 255, 0.2);
    --toggle-bg: #e2e8f0;
}}

body.dark-mode {{
    --bg-color: {dark_bg};
    --text-color: {dark_text};
    --accent-glow: {dark_accent};
    --glass-bg: rgba(15, 23, 42, 0.6);
    --glass-border: rgba(255, 255, 255, 0.05);
    --toggle-bg: #334155;
}}

body {{
    font-family: 'Poppins', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    transition: background-color 0.4s ease, color 0.4s ease;
    min-height: 100vh;
    margin: 0;
    overflow-x: hidden;
}}

/* Ambient Background Glow */
.ambient-glow {{
    position: absolute;
    width: 600px;
    height: 400px;
    background: var(--accent-glow);
    filter: blur(140px);
    border-radius: 50%;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    opacity: 0.15;
    z-index: -1;
    pointer-events: none;
    transition: background 0.6s ease, opacity 0.4s ease;
}}

body.dark-mode .ambient-glow {{
    opacity: 0.25;
}}

/* Glassmorphism Panel */
.glass-panel {{
    background: var(--glass-bg);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid var(--glass-border);
    transition: background 0.4s ease, border-color 0.4s ease;
}}

/* Custom Toggle Switch Styles */
.toggle-checkbox:checked + .toggle-label .toggle-bg {{
    background-color: var(--accent-glow);
}}

.toggle-checkbox:checked + .toggle-label .toggle-indicator {{
    transform: translateX(24px);
}}

.toggle-bg {{
    background-color: var(--toggle-bg);
    transition: background-color 0.3s ease;
}}

.toggle-indicator {{
    transition: transform 0.3s cubic-bezier(0.4, 0.0, 0.2, 1);
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <!-- Tailwind CSS for rapid layout -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="style.css">
</head>
<body class="antialiased relative {'dark-mode' if color_scheme == 'dark' else ''}" style="width: {width_px}px; height: {height_px}px; margin: 0 auto; position: relative;">
    
    <!-- Background Environmental Glow -->
    <div class="ambient-glow"></div>

    <main class="w-full h-full flex flex-col items-center pt-32 px-8">
        
        <!-- Hero Text -->
        <div class="text-center mb-16 z-0">
            <h1 class="text-4xl md:text-5xl font-semibold mb-4 tracking-tight">{title_text}</h1>
            <p class="text-lg opacity-80">{body_text}</p>
        </div>

        <!-- Navigation & Toggle Panel (Glassmorphism) -->
        <nav class="glass-panel w-full max-w-4xl rounded-2xl p-6 flex flex-col md:flex-row justify-between items-center shadow-lg gap-6 z-10">
            
            <div class="flex gap-8 font-medium opacity-90">
                <a href="#" class="hover:opacity-60 transition-opacity">Posts</a>
                <a href="#" class="hover:opacity-60 transition-opacity">Blogs</a>
                <a href="#" class="hover:opacity-60 transition-opacity border-b-2 border-current pb-1">Videos</a>
            </div>

            <!-- Theme Toggle Switch -->
            <div class="flex items-center gap-4">
                <span class="text-sm font-semibold opacity-80 tracking-wide uppercase">Lights</span>
                
                <input type="checkbox" id="themeToggle" class="toggle-checkbox hidden" {'checked' if color_scheme == 'dark' else ''}>
                <label for="themeToggle" class="toggle-label flex items-center cursor-pointer">
                    <!-- Toggle Track -->
                    <div class="toggle-bg relative w-14 h-8 rounded-full shadow-inner">
                        <!-- Toggle Dot -->
                        <div class="toggle-indicator absolute left-1 top-1 w-6 h-6 bg-white rounded-full shadow transition-transform flex items-center justify-center"></div>
                    </div>
                </label>
            </div>
            
        </nav>

        <!-- Dummy Content Cards -->
        <div class="w-full max-w-4xl grid grid-cols-1 md:grid-cols-3 gap-6 mt-8 z-10">
            <div class="glass-panel p-6 rounded-xl shadow hover:-translate-y-1 transition-transform cursor-pointer">
                <p class="text-xs opacity-60 uppercase font-semibold mb-1">Installation Guide</p>
                <h3 class="font-semibold text-lg">Speedtest-Tracker</h3>
            </div>
            <div class="glass-panel p-6 rounded-xl shadow hover:-translate-y-1 transition-transform cursor-pointer">
                <p class="text-xs opacity-60 uppercase font-semibold mb-1">Setup</p>
                <h3 class="font-semibold text-lg">Uptime-Kuma</h3>
            </div>
            <div class="glass-panel p-6 rounded-xl shadow hover:-translate-y-1 transition-transform cursor-pointer">
                <p class="text-xs opacity-60 uppercase font-semibold mb-1">Playlist</p>
                <h3 class="font-semibold text-lg">HomeLab (Self-hosting)</h3>
            </div>
        </div>

    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Theme Toggle Logic
document.addEventListener('DOMContentLoaded', () => {{
    const themeToggle = document.getElementById('themeToggle');
    
    // Listen for toggle changes
    themeToggle.addEventListener('change', (e) => {{
        if (e.target.checked) {{
            document.body.classList.add('dark-mode');
        }} else {{
            document.body.classList.remove('dark-mode');
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
