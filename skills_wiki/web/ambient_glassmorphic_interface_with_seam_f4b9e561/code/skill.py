def create_component(
    output_dir: str,
    title_text: str = "Why Not Your Own Services?",
    body_text: str = "Start Your Self-Hosting Journey with us!",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#fa39ad",     # Base accent color (pinkish by default)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Ambient Glassmorphic Hero with Theme Toggle.
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)
    
    # Evaluate initial dark mode state
    is_dark = color_scheme.lower() == "dark"
    html_class = ' class="dark"' if is_dark else ''
    checkbox_checked = 'checked' if not is_dark else '' # Let's say checked = light mode (Lights ON)

    # === CSS (Custom base styles & Blob positioning) ===
    css = f"""/* Custom Styles for Ambient Glow */
:root {{
    --accent: {accent_color};
}}

body {{
    font-family: 'Poppins', system-ui, -apple-system, sans-serif;
    transition: background-color 0.5s ease, color 0.5s ease;
}}

/* The glowing ambient blob */
.ambient-blob {{
    position: absolute;
    width: 500px;
    height: 500px;
    border-radius: 50%;
    background: linear-gradient(to bottom right, var(--accent) 20%, #fa6c4c 80%);
    filter: blur(140px);
    opacity: 0.5;
    z-index: 0;
    pointer-events: none;
    transform: translate3d(0, 0, 0); /* Force GPU acceleration */
    top: 50%;
    left: 50%;
    transform: translate(-50%, -30%);
    transition: opacity 0.5s ease;
}}

.dark .ambient-blob {{
    opacity: 0.35; /* Slightly dimmer in dark mode for better contrast */
}}

/* Custom Toggle Switch styling */
.toggle-checkbox:checked + .toggle-label {{
    background-color: var(--accent);
}}
.toggle-checkbox:checked + .toggle-label .toggle-dot {{
    transform: translateX(100%);
}}

/* Container specific sizing */
.app-viewport {{
    width: 100%;
    max-width: {width_px}px;
    min-height: {height_px}px;
    margin: 0 auto;
    position: relative;
    overflow: hidden;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en"{html_class}>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <!-- FontAwesome for Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    colors: {{
                        background: '#f8f9fa',
                        backgroundDark: '#0d0f10',
                    }}
                }}
            }}
        }}
    </script>
    <link rel="stylesheet" href="style.css">
</head>
<body class="bg-background dark:bg-backgroundDark text-gray-900 dark:text-gray-100 antialiased overflow-x-hidden selection:bg-pink-500 selection:text-white">
    
    <div class="app-viewport flex flex-col pt-8 pb-16 px-6 relative z-10">
        
        <!-- Ambient Background Glow -->
        <div class="ambient-blob"></div>

        <!-- Navigation Bar -->
        <nav class="flex justify-between items-center w-full max-w-5xl mx-auto relative z-20">
            <div class="flex items-center gap-2 text-xl font-bold tracking-tight">
                <div class="w-3 h-3 rounded-full bg-red-500"></div>
                <div class="w-3 h-3 rounded-full bg-yellow-500"></div>
                <div class="w-3 h-3 rounded-full bg-green-500"></div>
                <span class="ml-4">AppHost</span>
            </div>
            
            <div class="flex items-center gap-6">
                <a href="#" class="hover:text-[var(--accent)] transition-colors font-medium flex items-center gap-2">
                    <i class="fa-brands fa-youtube text-red-500 text-xl"></i> YouTube
                </a>
                <button class="bg-gray-900 dark:bg-white text-white dark:text-gray-900 px-5 py-2 rounded-full font-semibold hover:opacity-90 transition">
                    Join now
                </button>
            </div>
        </nav>

        <!-- Hero Section -->
        <main class="flex-grow flex flex-col justify-center items-center text-center mt-24 relative z-20">
            <h1 class="text-5xl md:text-6xl font-bold mb-6 tracking-tight drop-shadow-sm">
                {title_text}
            </h1>
            <p class="text-lg md:text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto mb-16 font-medium">
                {body_text}
            </p>

            <!-- Mid-level Navigation/Tabs & Toggle -->
            <div class="w-full max-w-4xl flex flex-col md:flex-row justify-between items-center mb-8 gap-6 border-b border-gray-200 dark:border-gray-800 pb-4">
                <div class="flex gap-8 text-lg font-semibold text-gray-500 dark:text-gray-400">
                    <a href="#" class="hover:text-gray-900 dark:hover:text-white transition">Posts</a>
                    <a href="#" class="hover:text-gray-900 dark:hover:text-white transition">Blogs</a>
                    <a href="#" class="text-gray-900 dark:text-white border-b-2 border-[var(--accent)] pb-1 transition">Videos</a>
                </div>
                
                <!-- Dark Mode Toggle -->
                <div class="flex items-center gap-3">
                    <span class="text-sm font-semibold text-gray-600 dark:text-gray-300">Lights</span>
                    <label for="themeToggle" class="flex items-center cursor-pointer">
                        <div class="relative">
                            <input type="checkbox" id="themeToggle" class="sr-only toggle-checkbox" {checkbox_checked}>
                            <div class="toggle-label block bg-gray-300 dark:bg-gray-700 w-12 h-7 rounded-full transition-colors duration-300"></div>
                            <div class="toggle-dot absolute left-1 top-1 bg-white w-5 h-5 rounded-full transition-transform duration-300 flex items-center justify-center shadow-sm"></div>
                        </div>
                    </label>
                </div>
            </div>

            <!-- Content Cards Grid -->
            <div class="w-full max-w-4xl grid grid-cols-1 md:grid-cols-3 gap-6">
                <!-- Card 1 -->
                <div class="bg-white/60 dark:bg-gray-800/40 backdrop-blur-md border border-white/40 dark:border-gray-700/50 p-6 rounded-2xl shadow-xl dark:shadow-2xl text-left hover:-translate-y-1 transition-transform duration-300 cursor-pointer">
                    <p class="text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-2">Installation Guide</p>
                    <h3 class="text-xl font-bold">Speedtest-Tracker</h3>
                </div>
                <!-- Card 2 -->
                <div class="bg-white/60 dark:bg-gray-800/40 backdrop-blur-md border border-white/40 dark:border-gray-700/50 p-6 rounded-2xl shadow-xl dark:shadow-2xl text-left hover:-translate-y-1 transition-transform duration-300 cursor-pointer">
                    <p class="text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-2">Setup</p>
                    <h3 class="text-xl font-bold">Uptime-Kuma</h3>
                </div>
                <!-- Card 3 -->
                <div class="bg-white/60 dark:bg-gray-800/40 backdrop-blur-md border border-white/40 dark:border-gray-700/50 p-6 rounded-2xl shadow-xl dark:shadow-2xl text-left hover:-translate-y-1 transition-transform duration-300 cursor-pointer">
                    <p class="text-xs font-bold text-[var(--accent)] uppercase tracking-wider mb-2">Playlist</p>
                    <h3 class="text-xl font-bold">HomeLab (Self-hosting)</h3>
                </div>
            </div>
        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Handle Theme Toggling
document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('themeToggle');
    const htmlElement = document.documentElement;

    // The checkbox is considered "checked" when lights are ON (Light Mode)
    // If it's unchecked, it's Dark Mode.
    
    // Initialize switch based on current HTML class (handles server-side defaults)
    if (htmlElement.classList.contains('dark')) {
        themeToggle.checked = false;
    } else {
        themeToggle.checked = true;
    }

    themeToggle.addEventListener('change', (e) => {
        // Toggle logic: checked = light mode, unchecked = dark mode
        if (e.target.checked) {
            htmlElement.classList.remove('dark');
        } else {
            htmlElement.classList.add('dark');
        }
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
