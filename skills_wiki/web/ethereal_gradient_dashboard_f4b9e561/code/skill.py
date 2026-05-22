def create_component(
    output_dir: str,
    title_text: str = "Why not Your own Services?",
    body_text: str = "Start Your Self-hosting Journey with us!",
    color_scheme: str = "light",  # "dark" or "light"
    accent_color: str = "#fb28cd",  # Main accent color, used for highlight
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Ethereal Gradient Dashboard visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # --- Theme Variables ---
    # Light Mode Colors
    light_app_bg = "#f3f3f3"
    light_app_text = "#292b48"
    light_app_blur_bg = "rgba(255, 255, 255, 0.5)"
    light_app_card_bg = "#ffffff"
    light_app_card_border = "#ee5e4b"
    light_app_card_hover_border = "#22d3ee"
    light_app_title_grad_start = "#fb28cd"
    light_app_title_grad_end = "#7c65d7"
    light_app_main_gradient_start = "#fa39ad"
    light_app_main_gradient_end = "#fa6c4c"
    light_app_dark_text_color = "#292b48"
    light_app_light_text_color = "#877f95"
    light_app_pink_color = "#fb28cd"
    light_app_yellow_color = "#ffc432"
    light_app_switch_bg = "#fb28cd"
    light_app_switch_indicator_bg = "#ffffff"

    # Dark Mode Colors
    dark_app_bg = "#0c1a1a"
    dark_app_text = "#a6f6ff"
    dark_app_blur_bg = "rgba(0, 255, 255, 0.08)"
    dark_app_card_bg = "#111222"
    dark_app_card_border = "#1a3a3a"
    dark_app_card_hover_border = "#fb28cd"
    dark_app_title_grad_start = "#00ffaa"
    dark_app_title_grad_end = "#0066ff"
    dark_app_main_gradient_start = "#00ffaa"
    dark_app_main_gradient_end = "#0066ff"
    dark_app_dark_text_color = "#f0f0f0"
    dark_app_light_text_color = "#88c7fd"
    dark_app_pink_color = "#fb28cd"
    dark_app_yellow_color = "#f6f6f6"
    dark_app_switch_bg = "#00ffaa"
    dark_app_switch_indicator_bg = "#ffffff"

    # Set initial theme variables based on color_scheme
    if color_scheme == "dark":
        current_app_bg = dark_app_bg
        current_app_text = dark_app_text
        current_app_blur_bg = dark_app_blur_bg
        current_app_card_bg = dark_app_card_bg
        current_app_card_border = dark_app_card_border
        current_app_card_hover_border = dark_app_card_hover_border
        current_app_title_grad_start = dark_app_title_grad_start
        current_app_title_grad_end = dark_app_title_grad_end
        current_app_main_gradient_start = dark_app_main_gradient_start
        current_app_main_gradient_end = dark_app_main_gradient_end
        current_app_dark_text_color = dark_app_dark_text_color
        current_app_light_text_color = dark_app_light_text_color
        current_app_pink_color = dark_app_pink_color
        current_app_yellow_color = dark_app_yellow_color
        current_app_switch_bg = dark_app_switch_bg
        current_app_switch_indicator_bg = dark_app_switch_indicator_bg
    else: # light
        current_app_bg = light_app_bg
        current_app_text = light_app_text
        current_app_blur_bg = light_app_blur_bg
        current_app_card_bg = light_app_card_bg
        current_app_card_border = light_app_card_border
        current_app_card_hover_border = light_app_card_hover_border
        current_app_title_grad_start = light_app_title_grad_start
        current_app_title_grad_end = light_app_title_grad_end
        current_app_main_gradient_start = light_app_main_gradient_start
        current_app_main_gradient_end = light_app_main_gradient_end
        current_app_dark_text_color = light_app_dark_text_color
        current_app_light_text_color = light_app_light_text_color
        current_app_pink_color = light_app_pink_color
        current_app_yellow_color = light_app_yellow_color
        current_app_switch_bg = light_app_switch_bg
        current_app_switch_indicator_bg = light_app_switch_indicator_bg

    # === CSS ===
    css = f"""
@import url('https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Special+Gothic+Expanded+One&display=swap');
@tailwind base;
@tailwind components;
@tailwind utilities;

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Poppins', sans-serif;
    transition: background-color 0.3s, color 0.3s;
    background-color: {current_app_bg};
    color: {current_app_text};
    min-height: 100vh;
    overflow-x: hidden;
    position: relative;
}}

/* Custom CSS Variables for Theming */
body {{
    --app-bg: {current_app_bg};
    --app-text: {current_app_text};
    --app-blur-bg: {current_app_blur_bg};
    --app-card-bg: {current_app_card_bg};
    --app-card-border: {current_app_card_border};
    --app-card-hover-border: {current_app_card_hover_border};
    --app-title-grad-start: {current_app_title_grad_start};
    --app-title-grad-end: {current_app_title_grad_end};
    --app-main-gradient-start: {current_app_main_gradient_start};
    --app-main-gradient-end: {current_app_main_gradient_end};
    --app-dark-text-color: {current_app_dark_text_color};
    --app-light-text-color: {current_app_light_text_color};
    --app-pink-color: {current_app_pink_color};
    --app-yellow-color: {current_app_yellow_color};
    --app-switch-bg: {current_app_switch_bg};
    --app-switch-indicator-bg: {current_app_switch_indicator_bg};
}}

body.dark-mode {{
    --app-bg: {dark_app_bg};
    --app-text: {dark_app_text};
    --app-blur-bg: {dark_app_blur_bg};
    --app-card-bg: {dark_app_card_bg};
    --app-card-border: {dark_app_card_border};
    --app-card-hover-border: {dark_app_card_hover_border};
    --app-title-grad-start: {dark_app_title_grad_start};
    --app-title-grad-end: {dark_app_title_grad_end};
    --app-main-gradient-start: {dark_app_main_gradient_start};
    --app-main-gradient-end: {dark_app_main_gradient_end};
    --app-dark-text-color: {dark_app_dark_text_color};
    --app-light-text-color: {dark_app_light_text_color};
    --app-pink-color: {dark_app_pink_color};
    --app-yellow-color: {dark_app_yellow_color};
    --app-switch-bg: {dark_app_switch_bg};
    --app-switch-indicator-bg: {dark_app_switch_indicator_bg};
}}


/* App Colors & Backgrounds */
.app-color-black {{ color: var(--app-dark-text-color); }}
.app-color-gray {{ color: var(--app-light-text-color); }}
.app-color-pink {{ color: var(--app-pink-color); }}
.app-color-yellow {{ color: var(--app-yellow-color); }}
.app-bg-light-white {{ background-color: var(--app-card-bg); }}
.app-bg-light-white-2 {{ background-color: var(--app-blur-bg); }}

/* Background Gradient Blob */
.circle {{
    width: 450px;
    height: 450px;
    background: linear-gradient(to bottom, var(--app-main-gradient-start) 40%, var(--app-main-gradient-end) 50%);
    filter: blur(120px);
    animation: gradient-animation 15s ease-in-out infinite alternate;
}}

@keyframes gradient-animation {{
    0% {{
        transform: translateY(0) translateX(0);
        filter: blur(120px);
    }}
    25% {{
        transform: translateY(50px) translateX(-50px);
        filter: blur(100px);
    }}
    50% {{
        transform: translateY(-50px) translateX(50px);
        filter: blur(150px);
    }}
    75% {{
        transform: translateY(50px) translateX(50px);
        filter: blur(100px);
    }}
    100% {{
        transform: translateY(0) translateX(0);
        filter: blur(120px);
    }}
}}

/* App Title Gradient Text */
.app-title {{
    background: linear-gradient(45deg, var(--app-title-grad-start), var(--app-title-grad-end));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: text-gradient-animation 10s ease-in-out infinite alternate;
}}

@keyframes text-gradient-animation {{
    0% {{
        background-position: 0% 50%;
    }}
    100% {{
        background-position: 100% 50%;
    }}
}}

/* Active Tab Indicator */
.app-tabs span.active {{
    position: relative;
    color: var(--app-text);
}}
.app-tabs span.active::after {{
    content: '';
    position: absolute;
    bottom: -10px; /* Adjust as needed */
    left: 0;
    width: 100%;
    height: 2px; /* Thickness of the underline */
    background-color: var(--app-dark-text-color); /* Color of the underline */
    transition: width 0.3s ease-out;
}}

/* Switch Styling */
.switch-checkbox {{
    display: none;
}}

.switch {{
    position: relative;
}}

.switch-bg {{
    height: 24px;
    width: 44px;
    background: var(--app-switch-bg);
    border-radius: 15px;
    cursor: pointer;
    transition: background-color 0.2s;
}}

.switch-indicator {{
    position: absolute;
    top: 2px;
    left: 2px;
    height: 20px;
    width: 20px;
    background: var(--app-switch-indicator-bg);
    border-radius: 50%;
    transition: transform 0.2s ease-out;
}}

.switch-checkbox:checked + .switch-bg .switch-indicator {{
    transform: translateX(20px);
}}

/* Custom blur effect from video */
.app-shadow {{
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.03);
    backdrop-filter: blur(20px); /* Adjust blur strength as needed */
    -webkit-backdrop-filter: blur(20px);
}}
.dark-mode .app-shadow {{
     box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1); /* Darker shadow for dark mode */
     backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
}}

/* Specific text styles based on video */
.font-semibold.text-sm {{
    font-weight: 600;
    font-size: 0.875rem; /* 14px */
}}
.font-bold.text-xs {{
    font-weight: 700;
    font-size: 0.75rem; /* 12px */
}}
.font-semibold.text-lg {{
    font-weight: 600;
    font-size: 1.125rem; /* 18px */
}}
.text-4xl {{
    font-size: 2.25rem; /* 36px */
    line-height: 1.1;
}}
.text-xs {{
    font-size: 0.75rem; /* 12px */
    line-height: 1rem;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en" class="{color_scheme}-mode">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Echoes of Ping | Home</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Special+Gothic+Expanded+One&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css">
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-container flex justify-center items-end pb-10 min-h-screen">
        <div class="absolute top-16 flex flex-col w-full items-center">
            <div class="flex items-center w-full px-6">
                <a href="https://echoesofping.hashnode.dev" target="_blank" rel="noopener noreferrer" class="mr-auto flex items-center bg-[var(--app-card-bg)] border-2 border-[var(--app-card-border)] rounded-md px-6 py-4 ml-3 app-shadow hover:border-[var(--app-card-hover-border)] transition duration-300">
                    <i class="fa-solid fa-ellipsis app-color-black dark:app-color-black mr-4 text-xs"></i>
                    <span class="font-bold app-color-black text-xs mr-auto auto-text-xs">echoesofping.hashnode.dev</span>
                </a>
                <a href="https://youtube.com/@echoes-of-ping" target="_blank" rel="noopener noreferrer" class="mr-auto flex items-center bg-[var(--app-card-bg)] border-2 border-[var(--app-card-border)] rounded-md px-6 py-4 ml-3 app-shadow hover:border-[var(--app-card-hover-border)] transition duration-300">
                    <i class="fa-brands fa-youtube app-color-black dark:text-pink-400 mr-2 text-xl"></i>
                    <span class="font-bold app-color-black text-xs">YouTube</span>
                </a>
                <span class="font-bold app-color-black text-xs mr-4 auto-text-xs">Join now</span>
                <i class="fa-regular fa-user mr-2 app-color-black text-xl"></i>
                <i class="fa-solid fa-angle-down text-xs app-color-black"></i>
            </div>
            <div class="flex flex-col text-center my-36">
                <span class="font-semibold text-4xl mb-4 app-title">{title_text}</span>
                <span class="app-color-black font-semibold text-base">{body_text}</span>
            </div>
            <div class="flex bg-[var(--app-blur-bg)] w-10/12 px-6 py-4 rounded-md app-shadow transition duration-300">
                <span class="font-semibold text-sm app-color-gray w-14 mx-12 active" id="posts-tab">Posts</span>
                <span class="font-semibold text-sm app-color-gray w-14 mx-12" id="blogs-tab">Blogs</span>
                <span class="font-semibold text-sm app-color-gray w-14 mx-12 mr-auto-active" id="videos-tab">Videos</span>
                <label class="flex items-center cursor-pointer">
                    <span class="font-semibold text-sm app-color-black mr-6">Lights</span>
                    <div class="switch">
                        <input type="checkbox" id="darkToggle" class="switch-checkbox" {"checked" if color_scheme == "dark" else ""}>
                        <div class="switch-bg">
                            <div class="switch-indicator"></div>
                        </div>
                    </div>
                </label>
            </div>
            <div class="flex mt-16 bg-[var(--app-blur-bg)] mx-6 flex flex-col w-1/3 p-6 rounded-xl app-shadow border-2 border-[var(--app-card-border)]">
                <span class="font-semibold text-xs app-color-pink">Installation Guide</span>
                <span class="font-semibold text-lg app-color-black">Speedtest-Tracker</span>
            </div>
            <div class="flex mt-16 bg-[var(--app-blur-bg)] mx-6 flex flex-col w-1/3 p-6 rounded-xl app-shadow border-2 border-[var(--app-card-border)]">
                <span class="font-semibold text-xs app-color-yellow">Setup</span>
                <span class="font-semibold text-lg app-color-black">Uptime-Kuma</span>
            </div>
            <div class="flex mt-16 bg-[var(--app-blur-bg)] mx-6 flex flex-col w-1/3 p-6 rounded-xl app-shadow border-2 border-[var(--app-card-border)]">
                <span class="font-semibold text-xs app-color-lavender">Playlist</span>
                <span class="font-semibold text-lg app-color-black">HomeLab(Self-hosting)</span>
            </div>
        </div>
        <div class="circle rounded-full absolute top-0 left-1/2 -translate-x-1/2"></div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""
document.addEventListener('DOMContentLoaded', () => {{
    const darkToggle = document.getElementById('darkToggle');
    const body = document.body;
    const tabs = document.querySelectorAll('.app-tabs span');

    // Load theme preference from localStorage
    if (localStorage.getItem('dark-mode') === 'true') {{
        body.classList.add('dark-mode');
        darkToggle.checked = true;
    }} else if (localStorage.getItem('dark-mode') === 'false') {{
        body.classList.remove('dark-mode');
        darkToggle.checked = false;
    }} else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {{
        body.classList.add('dark-mode');
        darkToggle.checked = true;
    }}

    darkToggle.addEventListener('change', () => {{
        if (darkToggle.checked) {{
            body.classList.add('dark-mode');
            localStorage.setItem('dark-mode', 'true');
        }} else {{
            body.classList.remove('dark-mode');
            localStorage.setItem('dark-mode', 'false');
        }}
    }});

    // Tab active state logic
    tabs.forEach(tab => {{
        tab.addEventListener('click', () => {{
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
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

