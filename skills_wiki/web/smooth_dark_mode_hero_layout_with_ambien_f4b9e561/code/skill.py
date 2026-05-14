def create_component(
    output_dir: str,
    title_text: str = "Why Not Your Own Services?",
    body_text: str = "Start Your Self-Hosting Journey with us!",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#d946ef",     # Hex color for accent (e.g., Fuchsia)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Dark Mode Hero & Toggle visual effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)
    
    is_dark = "true" if color_scheme == "dark" else "false"
    checked_attr = "checked" if color_scheme == "dark" else ""
    initial_class = "dark" if color_scheme == "dark" else ""

    # === CSS ===
    css = f"""/* Tailwind Dark Mode Hero — Generated Component */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

:root {{
    /* Light Theme Definitions */
    --c-bg: #f8f9fa;
    --c-text: #0f172a;
    --c-surface: rgba(255, 255, 255, 0.7);
    --c-border: rgba(15, 23, 42, 0.1);
    --c-accent: {accent_color};
    --c-toggle-bg: #cbd5e1;
}}

.dark {{
    /* Dark Theme Definitions */
    --c-bg: #0f172a;
    --c-text: #f8f9fa;
    --c-surface: rgba(30, 41, 59, 0.6);
    --c-border: rgba(255, 255, 255, 0.1);
    --c-toggle-bg: #334155;
}}

/* Universal smooth transitions for theme switching */
*, *::before, *::after {{
    box-sizing: border-box;
}}

.theme-transition {{
    transition: background-color 0.4s ease, color 0.4s ease, border-color 0.4s ease, fill 0.4s ease;
}}

body {{
    margin: 0;
    padding: 0;
    background-color: #000;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    font-family: 'Poppins', sans-serif;
}}

.component-wrapper {{
    width: {width_px}px;
    height: {height_px}px;
    max-width: 100vw;
    max-height: 100vh;
    position: relative;
    overflow: hidden;
    background-color: var(--c-bg);
    color: var(--c-text);
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}}

/* Glow Effect */
.ambient-glow {{
    position: absolute;
    bottom: -10%;
    left: 50%;
    transform: translateX(-50%);
    width: 70%;
    height: 50%;
    background-color: var(--c-accent);
    filter: blur(120px);
    opacity: 0.25;
    border-radius: 50%;
    pointer-events: none;
    z-index: 0;
    transition: opacity 0.4s ease, background-color 0.4s ease;
}}

.dark .ambient-glow {{
    opacity: 0.15;
}}

/* Glassmorphic Cards */
.glass-card {{
    background-color: var(--c-surface);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--c-border);
    z-index: 10;
}}

/* Custom Toggle Switch Logic */
input:checked ~ .toggle-block {{
    background-color: var(--c-toggle-bg);
}}
input:checked ~ .toggle-dot {{
    transform: translateX(1.75rem);
    background-color: var(--c-accent);
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
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Configure Tailwind to use our CSS variables -->
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    colors: {{
                        bg: 'var(--c-bg)',
                        text: 'var(--c-text)',
                        surface: 'var(--c-surface)',
                        border: 'var(--c-border)',
                        accent: 'var(--c-accent)',
                    }}
                }}
            }}
        }}
    </script>
</head>
<body>

    <!-- Main Configurable Application Wrapper -->
    <main id="app-root" class="component-wrapper theme-transition {initial_class} flex flex-col">
        
        <!-- Ambient Glowing Background -->
        <div class="ambient-glow"></div>

        <!-- Header / Navigation -->
        <header class="w-full flex justify-between items-center px-12 py-8 relative z-10 theme-transition">
            <div class="flex items-center gap-2 cursor-pointer group">
                <div class="w-3 h-3 rounded-full bg-red-500"></div>
                <div class="w-3 h-3 rounded-full bg-yellow-500"></div>
                <div class="w-3 h-3 rounded-full bg-green-500"></div>
                <span class="ml-4 font-semibold tracking-wide opacity-80 group-hover:opacity-100 transition-opacity">echoesofping</span>
            </div>
            
            <nav class="hidden md:flex gap-8 font-medium text-sm">
                <a href="#" class="hover:text-accent transition-colors">Posts</a>
                <a href="#" class="hover:text-accent transition-colors">Blogs</a>
                <a href="#" class="hover:text-accent transition-colors border-b-2 border-accent pb-1">Videos</a>
            </nav>

            <div class="flex items-center gap-6">
                <!-- Theme Toggle Switch -->
                <label for="themeToggle" class="flex items-center cursor-pointer gap-3 group">
                    <span class="text-sm font-medium opacity-80 group-hover:opacity-100 transition-opacity select-none">Lights</span>
                    <div class="relative">
                        <input type="checkbox" id="themeToggle" class="sr-only" {checked_attr}>
                        <!-- Background track -->
                        <div class="toggle-block block w-14 h-7 rounded-full theme-transition border border-border" style="background-color: var(--c-toggle-bg);"></div>
                        <!-- Sliding dot -->
                        <div class="toggle-dot absolute left-1 top-1 bg-white w-5 h-5 rounded-full transition-transform duration-300 shadow-md"></div>
                    </div>
                </label>
            </div>
        </header>

        <!-- Hero Content -->
        <section class="flex-grow flex flex-col justify-center items-center text-center px-6 relative z-10 mb-12 theme-transition">
            <h1 class="text-5xl md:text-6xl font-bold mb-4 tracking-tight leading-tight">
                {title_text}
            </h1>
            <p class="text-lg md:text-xl font-medium opacity-80 max-w-2xl">
                {body_text}
            </p>
        </section>

        <!-- Features/Cards Grid -->
        <section class="w-full px-12 pb-16 relative z-10 theme-transition">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-6xl mx-auto">
                <!-- Card 1 -->
                <article class="glass-card rounded-2xl p-6 theme-transition hover:-translate-y-1 transition-transform cursor-pointer shadow-sm hover:shadow-xl hover:border-accent/50">
                    <p class="text-xs font-bold uppercase tracking-wider mb-2 opacity-60">Installation Guide</p>
                    <h3 class="text-xl font-bold">Speedtest-Tracker</h3>
                </article>
                
                <!-- Card 2 -->
                <article class="glass-card rounded-2xl p-6 theme-transition hover:-translate-y-1 transition-transform cursor-pointer shadow-sm hover:shadow-xl hover:border-accent/50">
                    <p class="text-xs font-bold uppercase tracking-wider mb-2 opacity-60">Setup</p>
                    <h3 class="text-xl font-bold">Uptime-Kuma</h3>
                </article>

                <!-- Card 3 -->
                <article class="glass-card rounded-2xl p-6 theme-transition hover:-translate-y-1 transition-transform cursor-pointer shadow-sm hover:shadow-xl hover:border-accent/50">
                    <p class="text-xs font-bold uppercase tracking-wider mb-2 opacity-60">Playlist</p>
                    <h3 class="text-xl font-bold">HomeLab (Self-hosting)</h3>
                </article>
            </div>
        </section>

    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Dark Mode Toggle Logic
document.addEventListener('DOMContentLoaded', () => {{
    const toggleInput = document.getElementById('themeToggle');
    const appRoot = document.getElementById('app-root');

    // Ensure the toggle accurately reflects the initial state
    toggleInput.addEventListener('change', function() {{
        if (this.checked) {{
            appRoot.classList.add('dark');
        }} else {{
            appRoot.classList.remove('dark');
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
