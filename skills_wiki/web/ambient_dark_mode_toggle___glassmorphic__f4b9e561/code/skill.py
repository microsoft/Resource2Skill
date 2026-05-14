def create_component(
    output_dir: str,
    title_text: str = "Why not Your own Services?",
    body_text: str = "Start Your Self-hosting Journey with us!",
    color_scheme: str = "light",       # "dark" or "light"
    accent_color: str = "#d946ef",     # Pink/Fuchsia default matching the video's aesthetic
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Ambient Dark Mode Toggle & Glassmorphic Layout.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Boolean to set initial checked state for the HTML checkbox
    is_dark = "checked" if color_scheme == "dark" else ""
    initial_html_class = "dark" if color_scheme == "dark" else ""

    # === CSS ===
    css = f"""/* Base styles & Ambient Blob Overrides */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

:root {{
    --width: {width_px}px;
    --height: {height_px}px;
    --accent: {accent_color};
}}

body {{
    margin: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background-color: #e5e7eb; /* Fallback body background */
}}

/* Framing the specific component dimensions */
.component-frame {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    position: relative;
    overflow: hidden;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    border-radius: 1rem;
}}

/* Ambient Background Blobs */
.blob {{
    position: absolute;
    border-radius: 50%;
    filter: blur(120px);
    z-index: 0;
    pointer-events: none;
}}

.blob-1 {{
    top: -10%;
    left: -10%;
    width: 500px;
    height: 500px;
    background-color: var(--accent);
    opacity: 0.3;
    transition: opacity 0.5s ease;
}}

.blob-2 {{
    bottom: -20%;
    right: -10%;
    width: 600px;
    height: 600px;
    background-color: #3b82f6; /* Blueish secondary accent */
    opacity: 0.2;
    transition: opacity 0.5s ease;
}}

/* Adjust blob opacities in dark mode for better contrast */
.dark .blob-1 {{ opacity: 0.15; }}
.dark .blob-2 {{ opacity: 0.1; }}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en" class="{initial_html_class}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Theme Toggle Component</title>
    <link rel="stylesheet" href="style.css">
    
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- Tailwind Configuration -->
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    fontFamily: {{
                        sans: ['Poppins', 'sans-serif'],
                    }},
                    colors: {{
                        brand: 'var(--accent)',
                        lightBg: '#f8f9fa',
                        darkBg: '#0f151a'
                    }}
                }}
            }}
        }}
    </script>
</head>
<body class="antialiased">

    <!-- The Reproducible Component Window -->
    <main class="component-frame bg-lightBg dark:bg-darkBg transition-colors duration-500 ease-in-out flex flex-col relative">
        
        <!-- Ambient Blobs -->
        <div class="blob blob-1"></div>
        <div class="blob blob-2"></div>

        <!-- Content Container -->
        <div class="relative z-10 flex-1 flex flex-col items-center justify-center p-8 text-center">
            <h1 class="text-4xl md:text-5xl font-semibold text-gray-900 dark:text-white mb-4 transition-colors duration-500">
                {title_text}
            </h1>
            <p class="text-lg text-gray-600 dark:text-gray-400 mb-16 transition-colors duration-500">
                {body_text}
            </p>

            <!-- Interactive Tab & Toggle Bar -->
            <div class="flex flex-wrap items-center justify-center gap-8 md:gap-16 px-8 py-4 bg-white/40 dark:bg-black/20 backdrop-blur-md rounded-2xl border border-white/20 dark:border-gray-800/50 shadow-sm">
                
                <nav class="flex items-center gap-8 text-sm font-medium text-gray-500 dark:text-gray-400">
                    <a href="#" class="hover:text-gray-900 dark:hover:text-white transition-colors">Posts</a>
                    <a href="#" class="hover:text-gray-900 dark:hover:text-white transition-colors">Blogs</a>
                    
                    <!-- Active Tab Indicator Example -->
                    <div class="relative text-gray-900 dark:text-white cursor-pointer">
                        Videos
                        <div class="absolute -bottom-2 left-0 w-full h-0.5 bg-brand rounded-full"></div>
                    </div>
                </nav>

                <div class="w-px h-8 bg-gray-300 dark:bg-gray-700 hidden md:block"></div>

                <!-- The Core Theme Toggle Switch -->
                <label for="themeToggle" class="flex items-center gap-4 cursor-pointer group">
                    <span class="text-sm font-medium text-gray-700 dark:text-gray-300 group-hover:text-gray-900 dark:group-hover:text-white transition-colors">
                        Lights
                    </span>
                    <div class="relative">
                        <!-- Hidden Checkbox matching peer logic -->
                        <input type="checkbox" id="themeToggle" class="sr-only peer" {is_dark}>
                        
                        <!-- Toggle Track -->
                        <div class="w-14 h-8 bg-gray-200 dark:bg-gray-800 rounded-full peer-checked:bg-brand transition-colors duration-300 shadow-inner border border-black/5 dark:border-white/5"></div>
                        
                        <!-- Toggle Dot -->
                        <div class="absolute top-1 left-1 bg-white w-6 h-6 rounded-full shadow transition-transform duration-300 peer-checked:translate-x-6 flex items-center justify-center">
                            <!-- Optional icon inside the dot could go here -->
                        </div>
                    </div>
                </label>
            </div>
        </div>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""document.addEventListener('DOMContentLoaded', () => {{
    const toggleInput = document.getElementById('themeToggle');
    const htmlElement = document.documentElement;

    // Listen for toggle switch changes
    toggleInput.addEventListener('change', function() {{
        if (this.checked) {{
            htmlElement.classList.add('dark');
        }} else {{
            htmlElement.classList.remove('dark');
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
