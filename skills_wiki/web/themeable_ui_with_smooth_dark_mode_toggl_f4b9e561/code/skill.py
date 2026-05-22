def create_component(
    output_dir: str,
    title_text: str = "Why Not Your Own Services?",
    body_text: str = "Start Your Self-Hosting Journey with us!",
    color_scheme: str = "light",       # "dark" or "light" (initial state)
    accent_color: str = "#ec4899",     # Pink-500 equivalent
    width_px: int = 1000,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Smooth Dark Mode Toggle UI.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)
    
    # Determine initial checked state for the toggle based on Python param
    is_dark = color_scheme == "dark"
    checked_attr = 'checked="checked"' if is_dark else ""
    initial_class = "dark" if is_dark else ""

    # === CSS ===
    css = f"""/* Smooth Dark Mode UI - Generated Component */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

:root {{
    --accent: {accent_color};
    
    /* Light Theme Variables */
    --bg-main: #f3f4f6;
    --bg-surface: #ffffff;
    --text-primary: #111827;
    --text-secondary: #6b7280;
    --border-color: #e5e7eb;
    --shadow-color: rgba(0, 0, 0, 0.05);
}}

/* Dark Theme Variables applied when .dark is present */
.theme-wrapper.dark {{
    --bg-main: #0f172a;
    --bg-surface: #1e293b;
    --text-primary: #f9fafb;
    --text-secondary: #94a3b8;
    --border-color: #334155;
    --shadow-color: rgba(0, 0, 0, 0.3);
}}

/* Base Styling */
body {{
    margin: 0;
    padding: 0;
    background-color: #000; /* Outer canvas */
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}}

.theme-wrapper {{
    font-family: 'Poppins', sans-serif;
    background-color: var(--bg-main);
    color: var(--text-primary);
    width: 100%;
    max-width: {width_px}px;
    min-height: {height_px}px;
    position: relative;
    overflow-y: auto;
    overflow-x: hidden;
    
    /* The magic sauce for smooth theme switching */
    transition: background-color 0.4s ease, color 0.4s ease;
}}

/* Ensure surfaces fade smoothly too */
.surface-element {{
    background-color: var(--bg-surface);
    border: 1px solid var(--border-color);
    box-shadow: 0 4px 6px -1px var(--shadow-color), 0 2px 4px -1px var(--shadow-color);
    transition: background-color 0.4s ease, border-color 0.4s ease, box-shadow 0.4s ease;
}}

.text-muted {{
    color: var(--text-secondary);
    transition: color 0.4s ease;
}}

/* Custom Toggle Switch */
.switch-container {{
    display: flex;
    align-items: center;
    gap: 12px;
    font-weight: 500;
}}

.switch {{
    position: relative;
    display: inline-block;
    width: 52px;
    height: 28px;
}}

.switch input {{
    opacity: 0;
    width: 0;
    height: 0;
}}

.slider {{
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #cbd5e1;
    transition: .4s;
    border-radius: 34px;
}}

.theme-wrapper.dark .slider {{
    background-color: #475569;
}}

.slider:before {{
    position: absolute;
    content: "";
    height: 20px;
    width: 20px;
    left: 4px;
    bottom: 4px;
    background-color: white;
    transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    border-radius: 50%;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}}

/* Checked State */
input:checked + .slider {{
    background-color: var(--accent);
}}

input:checked + .slider:before {{
    transform: translateX(24px);
}}

/* Nav links */
.nav-link {{
    cursor: pointer;
    padding: 8px 16px;
    border-radius: 8px;
    transition: all 0.2s;
}}
.nav-link:hover {{
    background-color: var(--border-color);
}}
.nav-link.active {{
    color: var(--text-primary);
    font-weight: 600;
    position: relative;
}}
.nav-link.active::after {{
    content: '';
    position: absolute;
    bottom: 0;
    left: 16px;
    right: 16px;
    height: 3px;
    background-color: var(--accent);
    border-radius: 3px 3px 0 0;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <!-- Tailwind CSS for rapid structural layout -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    
    <!-- Wrapper controls the theme -->
    <div id="theme-wrapper" class="theme-wrapper {initial_class} shadow-2xl rounded-xl">
        <main class="w-full max-w-5xl mx-auto px-8 py-12">
            
            <!-- Hero Section -->
            <div class="text-center mt-12 mb-16">
                <h1 class="text-4xl md:text-5xl font-bold mb-4 tracking-tight">{title_text}</h1>
                <p class="text-muted text-lg">{body_text}</p>
            </div>

            <!-- Navigation & Control Bar -->
            <div class="surface-element flex flex-col md:flex-row justify-between items-center rounded-2xl p-4 mb-10">
                <div class="flex gap-2 text-muted mb-4 md:mb-0">
                    <span class="nav-link">Posts</span>
                    <span class="nav-link">Blogs</span>
                    <span class="nav-link active">Videos</span>
                </div>
                
                <!-- Toggle Mechanism -->
                <div class="switch-container">
                    <span class="text-sm uppercase tracking-wider">Lights</span>
                    <label class="switch">
                        <input type="checkbox" id="theme-toggle" {checked_attr}>
                        <span class="slider"></span>
                    </label>
                </div>
            </div>

            <!-- Content Grid -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <!-- Card 1 -->
                <div class="surface-element p-6 rounded-2xl cursor-pointer hover:-translate-y-1 transform transition-transform duration-300">
                    <p class="text-sm font-semibold text-muted uppercase tracking-wider mb-1">Installation Guide</p>
                    <h3 class="text-xl font-bold">Speedtest-Tracker</h3>
                </div>
                
                <!-- Card 2 -->
                <div class="surface-element p-6 rounded-2xl cursor-pointer hover:-translate-y-1 transform transition-transform duration-300">
                    <p class="text-sm font-semibold text-muted uppercase tracking-wider mb-1">Setup</p>
                    <h3 class="text-xl font-bold">Uptime-Kuma</h3>
                </div>
                
                <!-- Card 3 -->
                <div class="surface-element p-6 rounded-2xl cursor-pointer hover:-translate-y-1 transform transition-transform duration-300">
                    <p class="text-sm font-semibold text-muted uppercase tracking-wider mb-1">Playlist</p>
                    <h3 class="text-xl font-bold">HomeLab (Self-hosting)</h3>
                </div>
            </div>
            
        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Smooth Dark Mode UI - Interaction Logic
document.addEventListener('DOMContentLoaded', () => {{
    const toggleInput = document.getElementById('theme-toggle');
    const themeWrapper = document.getElementById('theme-wrapper');

    // Toggle theme on switch change
    toggleInput.addEventListener('change', function() {{
        if (this.checked) {{
            themeWrapper.classList.add('dark');
        }} else {{
            themeWrapper.classList.remove('dark');
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
