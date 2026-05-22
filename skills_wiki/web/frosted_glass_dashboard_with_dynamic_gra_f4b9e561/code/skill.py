def create_component(
    output_dir: str,
    title_text: str = "Why not Your own Services?",
    body_text: str = "Start Your Self-hosting Journey with us!",
    color_scheme: str = "light",  # "dark" or "light"
    accent_color: str = "#fb28cd",  # Main accent color (e.g., used in header)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the "Frosted Glass Dashboard with Dynamic Gradients and Dark Mode Toggle" visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Base colors (more robust with variables)
    light_bg = "#f3f3f3"
    light_text = "#292b48"
    light_text_gray = "#877f95"
    light_card_bg = "rgba(255, 255, 255, 0.8)"
    light_card_border = "#e0e0e0" # Lighter border for light card
    light_shadow = "rgba(0, 0, 0, 0.03)"

    dark_bg = "#0c1a1a"
    dark_text = "#ffffff"
    dark_text_gray = "#c0c0c0"
    dark_card_bg = "rgba(17, 34, 34, 0.8)" # Adjusted for slight transparency
    dark_card_border = "#2a2a2a" # Darker border for dark card
    dark_shadow = "rgba(0, 0, 0, 0.03)" # Same transparent shadow, but on dark bg

    # Gradient colors for circles
    circle1_light_gradient = "linear-gradient(to bottom, #fa39ad 40%, #fa6c4c 50%)"
    circle2_light_gradient = "linear-gradient(to bottom, #ffc432 40%, #ff283d 50%)"
    circle1_dark_gradient = "linear-gradient(to bottom, #00ffaa 40%, #0066ff 60%)"
    circle2_dark_gradient = "linear-gradient(to bottom, #5bde47 40%, #5fc651 50%)"

    # Tailwind CDN link (JIT version)
    tailwind_cdn = "https://cdn.tailwindcss.com?plugins=forms"
    
    # Custom fonts from Google Fonts
    google_fonts_link = """<link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@100;200;300;400;500;600;700;800;900&family=Special+Gothic+Expanded+One&display=swap" rel="stylesheet">"""
    # Font Awesome CDN
    font_awesome_cdn = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css">'

    css = f"""
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@100;200;300;400;500;600;700;800;900&family=Special+Gothic+Expanded+One&display=swap');
    @tailwind base;
    @tailwind components;
    @tailwind utilities;

    /* Custom CSS Variables & Transitions */
    body {{
        --bg-color: {light_bg};
        --text-color: {light_text};
        --text-color-gray: {light_text_gray};
        --card-bg: {light_card_bg};
        --card-border-color: {light_card_border};
        --circle1-gradient: {circle1_light_gradient};
        --circle2-gradient: {circle2_light_gradient};
        --shadow-color: {light_shadow};
        transition: background-color 0.3s ease, color 0.3s ease;
        font-family: 'Poppins', sans-serif; /* Default Poppins */
    }}

    body.dark-mode {{
        --bg-color: {dark_bg};
        --text-color: {dark_text};
        --text-color-gray: {dark_text_gray};
        --card-bg: {dark_card_bg};
        --card-border-color: {dark_card_border};
        --circle1-gradient: {circle1_dark_gradient};
        --circle2-gradient: {circle2_dark_gradient};
        --shadow-color: {dark_shadow};
    }}

    /* Global Body Styles */
    body {{
        background-color: var(--bg-color);
        color: var(--text-color);
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        margin: 0;
        padding: 0;
    }}

    /* Blurred Circles */
    .circle {{
        width: 450px;
        height: 450px;
        background: linear-gradient(to bottom, {accent_color} 40%, #fa6c4c 50%); /* Base for animation */
        filter: blur(120px);
        position: absolute;
        border-radius: 50%;
        opacity: 0.7;
        pointer-events: none; /* Allows clicks to pass through */
        transition: background 0.3s ease, filter 0.3s ease;
    }}

    .circle:nth-child(1) {{
        top: -100px;
        left: -100px;
        background: var(--circle1-gradient);
    }}

    .circle:nth-child(2) {{
        bottom: -100px;
        right: -100px;
        background: var(--circle2-gradient);
    }}

    /* App Container (Frosted Glass Card) */
    .app-container {{
        position: relative;
        z-index: 10;
        background: var(--card-bg);
        backdrop-filter: blur(120px);
        border: 2px solid var(--card-border-color);
        border-radius: 1rem; /* rounded-xl */
        box-shadow: 0 10px 25px var(--shadow-color);
        transition: background 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
        padding: 2.5rem 1.5rem; /* px-6 py-4 equivalent from Tailwind */
        width: 100%;
        max-width: {width_px * 0.6}px; /* Adjusted to be 60% of max width */
        min-height: {height_px * 0.8}px; /* Adjusted to be 80% of max height */
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
    }}
    @media (min-width: 768px) {{ /* md:w-6/12 */
        .app-container {{
            max-width: {width_px * 0.5}px;
        }}
    }}
    @media (min-width: 1024px) {{ /* lg:w-5/12 */
        .app-container {{
            max-width: {width_px * 0.4}px;
        }}
    }}

    /* Header & Navigation */
    .app-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        position: absolute;
        top: 0;
        left: 0;
        padding: 1.5rem; /* p-6 */
        z-index: 20;
    }}
    .app-header-left, .app-header-right {{
        display: flex;
        align-items: center;
    }}
    .app-header-link {{
        display: flex;
        align-items: center;
        padding: 0.5rem 0.75rem; /* px-3 py-2 */
        border-radius: 0.5rem; /* rounded-md */
        text-decoration: none;
        color: var(--text-color);
        font-weight: 500;
        margin-left: 1rem; /* ml-4 */
        transition: background-color 0.2s ease, color 0.2s ease;
    }}
    .app-header-link:hover {{
        background-color: rgba(255, 255, 255, 0.1);
    }}
    .app-header-link i {{
        margin-right: 0.5rem;
    }}
    .app-header-link.youtube-link {{
        color: #e04b85; /* text-pink-400 */
    }}
    .app-header-link.hashnode-link {{
        color: {light_text}; /* text-black */
    }}
    body.dark-mode .app-header-link.hashnode-link {{
        color: {dark_text}; /* text-white */
    }}
    .app-header-link.join-now {{
        background-color: {light_text}; /* bg-black */
        color: {light_bg}; /* text-white */
        padding: 0.75rem 1.25rem; /* px-5 py-3 */
        border-radius: 0.75rem; /* rounded-lg */
        font-weight: 600;
    }}
    body.dark-mode .app-header-link.join-now {{
        background-color: {dark_text};
        color: {dark_bg};
    }}

    /* Main Title & Subtitle */
    .app-title {{
        font-family: 'Special Gothic Expanded One', sans-serif;
        font-size: 3rem; /* text-4xl */
        font-weight: 800; /* font-extrabold */
        margin-bottom: 0.5rem; /* mb-4 */
        background: linear-gradient(45deg, #fb28cd, #7c65d7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        transition: all 0.3s ease;
    }}
    .app-subtitle {{
        font-family: 'Poppins', sans-serif;
        font-weight: 500; /* font-semibold */
        font-size: 1.125rem; /* text-lg */
        color: var(--text-color);
        margin-bottom: 2rem; /* my-16 */
    }}
    .body-dark-mode .app-title {{
        background: linear-gradient(45deg, #00ffaa, #0066ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}

    /* Tab Navigation */
    .tab-navigation {{
        display: flex;
        justify-content: center;
        margin-top: 2rem; /* mt-8 */
        margin-bottom: 1.5rem; /* mb-6 */
        width: 100%;
        max-width: 400px;
        font-family: 'Poppins', sans-serif;
        font-weight: 600; /* font-semibold */
        position: relative;
    }}
    .tab-navigation span {{
        padding: 0.75rem 1.5rem; /* py-3 px-6 */
        cursor: pointer;
        position: relative;
        z-index: 1;
        color: var(--text-color-gray);
        transition: color 0.3s ease;
    }}
    .tab-navigation span.active {{
        color: var(--text-color);
    }}
    .tab-indicator {{
        position: absolute;
        bottom: 0;
        left: 0;
        height: 2px;
        background-color: {accent_color};
        width: calc(100% / 3); /* For 3 tabs */
        transition: transform 0.3s ease-out;
        z-index: 0;
    }}

    /* Content Cards Section */
    .content-cards-section {{
        display: flex;
        flex-wrap: wrap;
        gap: 1.5rem; /* gap-6 */
        justify-content: center;
        width: 100%;
        margin-top: 2rem;
    }}
    .content-card {{
        flex: 1 1 calc(33.333% - 1rem); /* w-1/3 with gap-6 */
        min-width: 250px;
        background-color: var(--bg-color); /* Matches body BG in light mode */
        border: 2px solid var(--card-border-color);
        border-radius: 0.75rem; /* rounded-xl */
        box-shadow: 0 5px 15px var(--shadow-color);
        padding: 1.5rem; /* p-6 */
        text-align: left;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: background-color 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
        cursor: pointer;
    }}
    .content-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }}
    .content-card-title {{
        font-family: 'Poppins', sans-serif;
        font-weight: 600; /* font-semibold */
        font-size: 1.125rem; /* text-lg */
        color: {accent_color}; /* app-color-lavender */
        margin-bottom: 0.5rem;
    }}
    .content-card-subtitle {{
        font-family: 'Poppins', sans-serif;
        font-weight: 400;
        font-size: 0.875rem; /* text-sm */
        color: var(--text-color);
    }}

    /* Dark Mode Switch */
    .switch {{
        position: relative;
        display: inline-block;
        width: 44px; /* w-11 */
        height: 24px; /* h-6 */
        margin-left: 1rem; /* ml-4 */
        vertical-align: middle;
    }}

    .switch-checkbox {{
        display: none;
    }}

    .switch-bg {{
        position: absolute;
        cursor: pointer;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: #fb28cd; /* bg-pink-500 */
        border-radius: 15px; /* rounded-full */
        transition: background-color 0.4s;
    }}

    .switch-indicator {{
        position: absolute;
        content: "";
        height: 20px; /* h-5 */
        width: 20px; /* w-5 */
        left: 2px;
        bottom: 2px;
        background-color: white; /* bg-white */
        border-radius: 50%; /* rounded-full */
        transition: transform 0.4s;
    }}

    .switch-checkbox:checked + .switch-bg {{
        background-color: #5fc651; /* bg-green-500 */
    }}

    .switch-checkbox:checked + .switch-bg .switch-indicator {{
        transform: translateX(20px);
    }}
    """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Echoes of Ping | Home</title>
    {google_fonts_link}
    {font_awesome_cdn}
    <script src="{tailwind_cdn}"></script>
    <link rel="stylesheet" href="style.css">
    <style type="text/tailwindcss">
        @layer base {{
            body {{
                @apply transition-colors duration-300;
            }}
            .app-header-link {{
                @apply block py-2 px-3 rounded-md text-base font-medium;
            }}
            .app-header-link.active {{
                @apply bg-gray-900 text-white;
            }}
        }}
    </style>
</head>
<body>
    <div class="circle"></div>
    <div class="circle"></div>

    <div class="app-container w-5/12 mx-auto px-6 py-4 rounded-xl shadow-md transition duration-300">
        <div class="app-header w-full flex justify-between items-center top-0 left-0 p-6 absolute">
            <div class="app-header-left flex items-center">
                <span class="font-bold app-color-black ml-4 mr-auto text-xs">echoesofping.hashnode.dev</span>
            </div>
            <div class="app-header-right flex items-center">
                <a href="https://youtube.com/@echoes-of-ping" target="_blank" rel="noopener noreferrer" class="app-header-link mr-auto flex items-center bg-white dark:bg-white border-2 border-transparent rounded-md px-6 py-4 ml-3 app-shadow hover:border-[{accent_color}] dark:hover:border-[#22d3ee] transition duration-300">
                    <i class="fa-brands fa-youtube app-color-dribbble dark:text-pink-400 mr-2 text-pink-400"></i>
                    <span class="font-bold app-color-black dark:text-text-black text-xs">Youtube</span>
                </a>
                <a href="#" class="app-header-link ml-4 mr-auto flex items-center bg-white dark:bg-white border-2 border-transparent rounded-md px-6 py-4 app-shadow hover:border-[{accent_color}] dark:hover:border-[#22d3ee] transition duration-300">
                    <span class="font-bold app-color-black dark:text-text-black text-xs">Join now</span>
                </a>
                <div class="app-header-link ml-4 mr-2 flex items-center app-bg-light-white-2 mx-4">
                    <i class="fa-regular fa-user mr-2 app-color-black"></i>
                    <i class="fa-solid fa-angle-down text-xs app-color-black"></i>
                </div>
            </div>
        </div>

        <div class="flex flex-col text-center my-36">
            <span class="font-semibole text-4xl mb-4 app-title">{title_text}</span>
            <span class="app-color-black font-semibold">{body_text}</span>
        </div>

        <div class="flex flex-col flex-grow w-full items-center">
            <div class="flex pr-4">
                <span class="font-semibole text-sm app-colo-gray w-14 mx-1 active" data-tab="posts">Posts</span>
                <span class="font-semibole text-sm app-colo-gray w-14 mx-1" data-tab="blogs">Blogs</span>
                <span class="font-semibole text-sm app-colo-gray w-14 mx-1" data-tab="videos">Videos</span>
                <label class="flex items-center cursor-pointer">
                    <span class="font-semibole text-sm app-color-black mr-6">Lights</span>
                    <div class="switch">
                        <input type="checkbox" id="darkToggle" class="switch-checkbox">
                        <div class="switch-bg">
                            <div class="switch-indicator"></div>
                        </div>
                    </div>
                </label>
            </div>
            <div class="mt-16 flex flex-col items-center w-full">
                <span class="font-semibole text-lg app-color-lavendar" data-tab-content="posts">
                    Installation Guide
                </span>
                <span class="font-semibole text-xs app-color-black" data-tab-content="posts">
                    Speedtest-Tracker
                </span>
            </div>
            <div class="mt-16 flex flex-col items-center w-full hidden" data-tab-content="blogs">
                <span class="font-semibole text-lg app-color-lavendar">
                    Setup
                </span>
                <span class="font-semibole text-xs app-color-black">
                    Uptime-Kuma
                </span>
            </div>
            <div class="mt-16 flex flex-col items-center w-full hidden" data-tab-content="videos">
                <span class="font-semibole text-lg app-color-lavendar">
                    Playlist
                </span>
                <span class="font-semibole text-xs app-color-black">
                    HomeLab (Self-hosting)
                </span>
            </div>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    js = f"""
    document.addEventListener('DOMContentLoaded', () => {{
        // Dark Mode Toggle
        const darkToggle = document.getElementById('darkToggle');
        darkToggle.addEventListener('change', function() {{
            document.body.classList.toggle('dark-mode', this.checked);
        }});

        // Tab Switching
        const tabs = document.querySelectorAll('.tab-navigation span');
        const tabIndicator = document.querySelector('.tab-indicator');
        const tabContents = document.querySelectorAll('[data-tab-content]');

        function updateTabIndicator(activeTab) {{
            if (activeTab) {{
                const tabWidth = activeTab.offsetWidth;
                const tabLeft = activeTab.offsetLeft;
                tabIndicator.style.width = `${{tabWidth}}px`;
                tabIndicator.style.transform = `translateX(${{tabLeft}}px)`;
            }}
        }}

        tabs.forEach(tab => {{
            tab.addEventListener('click', () => {{
                tabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                updateTabIndicator(tab);

                const targetTab = tab.getAttribute('data-tab');
                tabContents.forEach(content => {{
                    content.classList.add('hidden');
                }});
                document.querySelector(`[data-tab-content="${{targetTab}}"]`).classList.remove('hidden');
            }});
        }});

        // Set initial active tab and indicator
        const initialActiveTab = document.querySelector('.tab-navigation span.active');
        if (initialActiveTab) {{
            updateTabIndicator(initialActiveTab);
            const targetTab = initialActiveTab.getAttribute('data-tab');
            document.querySelectorAll('[data-tab-content]').forEach(content => {{
                content.classList.add('hidden');
            }});
            document.querySelector(`[data-tab-content="${{targetTab}}"]`).classList.remove('hidden');
        }}
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

