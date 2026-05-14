def create_component(
    output_dir: str,
    title_text: str = "Why not Your own Services?",
    subtitle_text: str = "Start Your Self-hosting Journey with us!",
    color_scheme: str = "light",        # "dark" or "light"
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Ethereal Gradient Landing Page visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        # Global
        body_bg = "#0c1a1a"
        body_color = "#d4f9f0"
        # Hero Circle
        circle_gradient = "linear-gradient(to bottom, #00ffaa, #00bfff 60%)"
        # Title
        title_gradient = "linear-gradient(45deg, #00ffcc, #33ccff)"
        # Nav bg
        nav_bg = "#112222"
        # Nav item text
        nav_item_color = "#a4f9f0"
        # Nav item hover border (matches YouTube link hover)
        nav_item_border_hover = "#ff28cd"
        # Toggle bg checked
        toggle_bg_checked = "#00ffaa"
        # Hashnode / YouTube / Join Now buttons
        button_bg = "#f7f8ff" # Buttons remain light, but hover is dark themed
        button_border = "transparent"
        button_border_hover = "#22d3ee" # Cyan for Hashnode/Default
        # Custom button colors
        dribbble_color = "#048b85"
        youtube_color = "#ff0000"


    else: # light mode
        # Global
        body_bg = "#f3f3f3"
        body_color = "#292b48"
        # Hero Circle
        circle_gradient = "linear-gradient(to bottom, #fa39ad 40%, #fa6c4c 50%)"
        # Title
        title_gradient = "linear-gradient(45deg, #fb28cd, #7c65d7)"
        # Nav bg
        nav_bg = "#ffffff"
        # Nav item text
        nav_item_color = "#877f95"
        # Nav item hover border
        nav_item_border_hover = "#22d3ee" # Cyan for Hashnode/Default
        # Toggle bg checked
        toggle_bg_checked = "#fb28cd"
        # Hashnode / YouTube / Join Now buttons
        button_bg = "#f7f8ff"
        button_border = "transparent"
        button_border_hover = "#22d3ee" # Cyan for Hashnode/Default
        # Custom button colors
        dribbble_color = "#ee5e4b" # Reddish for Dribbble-like link
        youtube_color = "#ffc432" # Yellowish for YouTube-like link


    # === CSS ===
    css = f"""
@import url('https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap');

body {{
    font-family: 'Poppins', sans-serif;
    transition: background-color 0.3s, color 0.3s;
    background-color: {body_bg};
    color: {body_color};
}}

.app-container {{
    min-height: 100vh;
    width: 100vw;
    display: flex;
    justify-content: center;
    align-items: end;
    padding-bottom: 2.5rem; /* pb-10 */
    position: relative;
    overflow: hidden;
}}

.circle {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 450px;
    height: 450px;
    border-radius: 9999px; /* rounded-full */
    background: {circle_gradient};
    filter: blur(120px);
    z-index: 0;
}}

/* Custom Colors */
.app-color-yellow {{ color: {youtube_color}; }}
.app-color-black {{ color: {body_color}; }}
.app-color-gray {{ color: {nav_item_color}; }}
.app-color-lavender {{ color: #9ea1cf; }}
.app-color-pink {{ color: #fb28cd; }}
.app-color-dribbble {{ color: {dribbble_color}; }}

/* Background Colors */
.app-bg-light-white {{ background-color: #f7f8ff; }}
.app-bg-light-white-2 {{ background-color: #eff2fc; }}


.app-shadow {{
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.03);
}}

.app-title {{
    background: {title_gradient};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    color: transparent; /* Fallback for non-webkit browsers */
}}

.active::after {{
    content: '';
    position: absolute;
    bottom: -8px;
    left: 0;
    width: 100%;
    height: 2px;
    background: {title_gradient};
    transition: width 0.3s ease-in-out, background 0.3s ease-in-out;
}}

.tab-item:hover::after {{
    width: 100%;
}}


/* DARK MODE STYLES */
body.dark-mode {{
    background-color: {body_bg};
    color: {body_color};
}}

body.dark-mode .app-container {{
    background-color: {body_bg}; /* Ensure container also reflects dark mode background */
}}

body.dark-mode .circle {{
    background: {circle_gradient};
}}

body.dark-mode .app-title {{
    background: {title_gradient};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    color: transparent; /* Fallback */
}}

/* For elements that should change their background */
body.dark-mode .app-bg-light-white {{ background-color: #112222; border-color: #1a3a3a !important; }}
body.dark-mode .app-bg-light-white-2 {{ background-color: #112222; border-color: #1a3a3a !important; }}

body.dark-mode .app-color-yellow {{ color: #ffc432; }}
body.dark-mode .app-color-black {{ color: #d4f9f0; }}
body.dark-mode .app-color-gray {{ color: #a4f9f0; }}
body.dark-mode .app-color-lavender {{ color: #a4f9f0; }}
body.dark-mode .app-color-pink {{ color: #ff28cd; }}
body.dark-mode .app-color-dribbble {{ color: #00ffaa; }}


/* SWITCH TOGGLE */
.switch {{
    position: relative;
    display: inline-block;
    width: 44px; /* width-11 */
    height: 24px; /* h-6 */
    z-index: 10;
}}

.switch-checkbox {{
    display: none;
}}

.switch-bg {{
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: {toggle_bg_checked};
    border-radius: 15px; /* rounded-full */
    transition: background-color 0.2s ease-out;
}}

.switch-indicator {{
    position: absolute;
    content: '';
    height: 20px; /* h-5 */
    width: 20px; /* w-5 */
    left: 2px; /* left-0.5 */
    bottom: 2px; /* bottom-0.5 */
    background-color: #ffffff;
    border-radius: 50%; /* rounded-full */
    transition: transform 0.2s ease-out;
}}

.switch-checkbox:checked + .switch-bg {{
    background-color: {toggle_bg_checked}; /* Magenta for light mode, Green for dark mode */
}}

.switch-checkbox:checked + .switch-bg .switch-indicator {{
    transform: translateX(20px); /* Move 20px to the right for 44px width */
}}

/* Styles for cards */
.content-card {{
    background-color: #ffffff; /* Default light background */
    padding: 1.5rem; /* p-6 */
    border-radius: 1rem; /* rounded-xl */
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Subtle shadow */
    transition: background-color 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
}}

body.dark-mode .content-card {{
    background-color: #112222; /* Darker background in dark mode */
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3); /* Darker shadow in dark mode */
}}

/* For the tab items (Posts, Blogs, Videos) */
.tab-item {{
    position: relative;
    font-weight: 600; /* font-semibold */
    font-size: 0.875rem; /* text-sm */
    color: {nav_item_color}; /* app-color-gray */
    padding: 0.5rem 0.75rem; /* px-3 py-2 */
    margin-right: 0.75rem; /* mr-3 */
    cursor: pointer;
    transition: color 0.3s ease-in-out;
    white-space: nowrap;
}}

.tab-item:hover {{
    color: {body_color};
}}

.tab-item.active {{
    color: {body_color}; /* Active color matches body text */
}}

.tab-item.active::after {{
    content: '';
    position: absolute;
    bottom: -8px; /* Position below text */
    left: 0;
    width: 100%;
    height: 2px;
    background: {title_gradient}; /* Dynamic gradient underline */
    transition: all 0.3s ease-in-out;
}}

/* Ensure elements inside cards have correct colors */
.content-card .text-xs,
.content-card .text-lg,
.content-card .text-xl {{
    color: {body_color};
    transition: color 0.3s ease-in-out;
}}

body.dark-mode .content-card .text-xs,
body.dark-mode .content-card .text-lg,
body.dark-mode .content-card .text-xl {{
    color: {body_color}; /* Also light in dark mode for card text */
}}

/* Small dots */
.red-dot {{ background-color: #ee5e4b; }}
.yellow-dot {{ background-color: #ffc432; }}
.green-dot {{ background-color: #5fc651; }}

/* Specific styling for nav buttons in dark mode */
body.dark-mode .nav-button.bg-white {{
    background-color: #112222 !important; /* Dark background */
    border-color: #1a3a3a !important; /* Darker border */
}}
body.dark-mode .nav-button.dark\\:hover\\:border-\\[\\#22d3ee\\]:hover {{
    border-color: #22d3ee !important;
}}
body.dark-mode .nav-button.dark\\:hover\\:border-\\[\\#ff28cd\\]:hover {{
    border-color: #ff28cd !important;
}}
body.dark-mode .nav-button .app-color-black {{
    color: #d4f9f0 !important;
}}

body.dark-mode .nav-button .fa-user {{
    color: #d4f9f0 !important;
}}

body.dark-mode .nav-button .fa-angle-down {{
    color: #d4f9f0 !important;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Echoes of Ping | Home</title>
    <!-- Google Fonts Poppins -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@100;200;300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css">
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Custom Styles -->
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-container">
        <div class="circle"></div>
        <div class="absolute top-16 flex flex-col w-full items-center">
            <div class="flex items-center justify-center space-x-2">
                <div class="h-2 w-2 rounded-full mx-1 red-dot"></div>
                <div class="h-2 w-2 rounded-full mx-1 yellow-dot"></div>
                <div class="h-2 w-2 rounded-full mx-1 green-dot"></div>
            </div>

            <div class="flex items-center justify-between w-10/12 px-6 py-4 rounded-md app-shadow transition duration-300 app-bg-light-white mt-8 mb-8">
                <!-- Left Nav Items -->
                <div class="flex items-center space-x-4">
                    <a href="echoesofping.hashnode.dev" target="_blank" rel="noopener noreferrer" class="mr-auto flex items-center nav-button app-bg-light-white border-2 border-transparent rounded-md px-6 py-4 ml-3 app-shadow dark:hover:border-[#22d3ee] transition duration-300">
                        <i class="fa-solid fa-star app-color-yellow text-xs"></i>
                        <span class="font-bold app-color-black ml-4 mr-auto text-xs">echoesofping.hashnode.dev</span>
                    </a>
                    <a href="https://youtube.com/@echoes-of-ping" target="_blank" rel="noopener noreferrer" class="mr-auto flex items-center nav-button app-bg-light-white border-2 border-transparent rounded-md px-6 py-4 ml-3 app-shadow dark:hover:border-[#ff28cd] transition duration-300">
                        <i class="fa-brands fa-youtube app-color-dribbble dark:text-pink-400 mr-2"></i>
                        <span class="font-bold app-color-black dark:text-text-black text-xs">Youtube</span>
                    </a>
                </div>

                <!-- Right Nav Items -->
                <div class="flex items-center space-x-4">
                    <a href="#" class="flex items-center nav-button app-bg-light-white border-2 border-transparent rounded-md px-6 py-4 ml-3 app-shadow dark:hover:border-[#22d3ee] transition duration-300">
                        <span class="font-bold app-color-black text-xs">Join Now</span>
                        <i class="fa-regular fa-user ml-2 app-color-black"></i>
                        <i class="fa-solid fa-angle-down text-xs app-color-black"></i>
                    </a>
                    <label class="flex items-center cursor-pointer switch">
                        <input type="checkbox" id="darkToggle" class="switch-checkbox">
                        <div class="switch-bg">
                            <div class="switch-indicator"></div>
                        </div>
                        <span class="font-semibold text-sm app-color-black mr-6 ml-3">Lights</span>
                    </label>
                </div>
            </div>

            <div class="flex flex-col text-center my-36">
                <span class="font-semibold text-4xl mb-4 app-title">{title_text}</span>
                <span class="app-color-black font-semibold">{subtitle_text}</span>
            </div>

            <div class="app-bg-light-white w-10/12 px-6 pt-12 pb-16 app-shadow rounded-xl backdrop-blur-[200px] transition duration-300">
                <div class="flex pr-4">
                    <span class="tab-item font-semibold text-sm app-color-gray w-14 mx-12 active">Posts</span>
                    <span class="tab-item font-semibold text-sm app-color-gray w-14 mx-12">Blogs</span>
                    <span class="tab-item font-semibold text-sm app-color-gray w-14 mx-12 mr-auto active">Videos</span>
                </div>
                <div class="flex mt-16 mx-6 flex-col lg:flex-row w-full items-center lg:items-start lg:justify-between space-y-8 lg:space-y-0 lg:space-x-8">
                    <div class="content-card app-bg-light-white-2 p-6 rounded-xl w-full lg:w-1/3">
                        <span class="font-semibold text-lg app-color-black">Installation Guide</span>
                        <h2 class="font-bold text-xl app-color-black mt-2">Speedtest-Tracker</h2>
                    </div>
                    <div class="content-card app-bg-light-white-2 p-6 rounded-xl w-full lg:w-1/3">
                        <span class="font-semibold text-lg app-color-black">Setup</span>
                        <h2 class="font-bold text-xl app-color-black mt-2">Uptime-Kuma</h2>
                    </div>
                    <div class="content-card app-bg-light-white-2 p-6 rounded-xl w-full lg:w-1/3">
                        <span class="font-semibold text-lg app-color-black">Playlist</span>
                        <h2 class="font-bold text-xl app-color-black mt-2">HomeLab (Self-hosting)</h2>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """
document.addEventListener('DOMContentLoaded', () => {
    const darkToggle = document.getElementById('darkToggle');

    // Set initial theme based on localStorage or user preference
    if (localStorage.getItem('theme') === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.body.classList.add('dark-mode');
        darkToggle.checked = true;
    } else {
        document.body.classList.remove('dark-mode');
        darkToggle.checked = false;
    }

    darkToggle.addEventListener('change', function() {
        if (this.checked) {
            document.body.classList.add('dark-mode');
            localStorage.setItem('theme', 'dark');
        } else {
            document.body.classList.remove('dark-mode');
            localStorage.setItem('theme', 'light');
        }
    });

    const tabItems = document.querySelectorAll('.tab-item');
    tabItems.forEach(item => {
        item.addEventListener('click', () => {
            tabItems.forEach(i => i.classList.remove('active'));
            item.classList.add('active');
        });
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

