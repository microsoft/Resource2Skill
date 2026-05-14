import os

def create_component(
    output_dir: str,
    title_text: str = "Why not Your own Services?",
    subtitle_text: str = "Start Your Self-hosting Journey with us!",
    color_scheme: str = "light",  # "dark" or "light"
    accent_color: str = "#fb28cd",  # Main accent color for light mode pink
    width_px: int = 1920,
    height_px: int = 1080,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the "Glassmorphism Hero with Dynamic Content & Dark Mode Toggle" visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    os.makedirs(output_dir, exist_ok=True)

    # --- Theme Colors ---
    if color_scheme == "dark":
        body_bg_color = "#0c1a1a"
        body_text_color = "#a6f9f0"
        glassmorphism_bg = "rgba(0, 0, 0, 0.2)"
        glassmorphism_border = "#1a1a3a"
        gradient_start = "#00ffaa"
        gradient_middle = "#0066ff"
        gradient_end = "#9eafcf"
        text_color_black = "#a6f9f0" # Light text for dark mode
        text_color_gray = "#8bcfd3" # Lighter text for dark mode
        text_color_dribble = "#fffff" # White for Dribble icon, it needs to pop.
        toggle_bg = "#9ecfa" # Light blue for toggle bg
        card_bg_color = "rgba(0, 0, 0, 0.2)"
        card_border_color = "rgba(26, 26, 58, 0.5)"
    else: # light
        body_bg_color = "#f7f8ff"
        body_text_color = "#292b48"
        glassmorphism_bg = "rgba(255, 255, 255, 0.8)"
        glassmorphism_border = "rgba(255, 255, 255, 0.9)"
        gradient_start = "#fb28cd"
        gradient_middle = "#f8a2ad"
        gradient_end = "#fac4c"
        text_color_black = "#292b48" # Dark text for light mode
        text_color_gray = "#877f95" # Darker gray text for light mode
        text_color_dribble = "#fffff" # White for Dribble icon, it needs to pop.
        toggle_bg = "#fb28cd" # Pink for toggle bg
        card_bg_color = "rgba(255, 255, 255, 0.8)"
        card_border_color = "rgba(255, 255, 255, 0.9)"


    # === CSS ===
    css = f"""
@import url('https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Special+Gothic+Expanded+One&display=swap');

body {{
    font-family: 'Poppins', sans-serif;
    background-color: {body_bg_color};
    color: {body_text_color};
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    transition: background-color 0.3s ease-out, color 0.3s ease-out;
}}

.app-container {{
    min-height: {height_px}px;
    width: {width_px}px;
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
}}

.background-gradient {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(45deg, {gradient_start} 0%, {gradient_middle} 50%, {gradient_end} 100%);
    background-size: 200% 200%;
    animation: pulse-gradient 10s infinite alternate linear;
    filter: blur(120px);
    opacity: 0.7;
    z-index: 0;
}}

@keyframes pulse-gradient {{
    0% {{ background-position: 0% 50%; }}
    100% {{ background-position: 100% 50%; }}
}}

.header {{
    position: absolute;
    top: 0;
    width: 90%;
    max-width: {width_px * 0.9}px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 1.5rem;
    background-color: {glassmorphism_bg};
    backdrop-filter: blur(20px);
    border: 2px solid {glassmorphism_border};
    border-radius: 0.5rem; /* rounded-md */
    margin-top: 2rem;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease-out;
    z-index: 10;
}}

.header-left, .header-right {{
    display: flex;
    align-items: center;
}}

.header-item {{
    display: flex;
    align-items: center;
    padding: 0.5rem 1rem;
    cursor: pointer;
    text-decoration: none;
    color: {text_color_black};
    font-weight: 500;
    transition: color 0.2s ease-in-out;
}}

.header-item:hover {{
    color: {accent_color};
}}

.icon {{
    margin-right: 0.5rem;
    font-size: 0.875rem; /* text-xs */
}}

.header-item span {{
    font-size: 0.875rem; /* text-xs */
}}

.app-title {{
    font-family: 'Special Gothic Expanded One', sans-serif;
    font-weight: 600; /* semibold */
    font-size: 3rem; /* text-4xl */
    line-height: 1;
    margin-bottom: 1rem; /* mb-4 */
    background: linear-gradient(45deg, {accent_color}, {gradient_middle});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    transition: all 0.3s ease-out;
    z-index: 1;
}}

.app-subtitle {{
    color: {body_text_color};
    font-weight: 500; /* font-semibold */
    transition: color 0.3s ease-out;
    z-index: 1;
}}

.bottom-content-bar {{
    position: absolute;
    bottom: 2.5rem; /* pb-10 + margin-bottom */
    width: 90%;
    max-width: {width_px * 0.9}px;
    display: flex;
    justify-content: space-around;
    align-items: center;
    padding: 1.5rem; /* px-6 py-4 (approx) */
    background-color: {card_bg_color};
    backdrop-filter: blur(20px);
    border: 2px solid {card_border_color};
    border-radius: 0.75rem; /* rounded-md */
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease-out;
    z-index: 10;
}}

.tab-nav {{
    display: flex;
    align-items: center;
    flex: 1;
}}

.tab-item {{
    position: relative;
    font-weight: 600; /* font-semibold */
    font-size: 0.875rem; /* text-sm */
    color: {text_color_gray};
    cursor: pointer;
    padding: 0.5rem 1rem;
    margin-right: 2rem; /* mx-12 approx */
    transition: color 0.2s ease-in-out;
    white-space: nowrap;
}}

.tab-item:hover {{
    color: {body_text_color};
}}

.tab-item.active {{
    color: {text_color_black};
}}

.tab-item.active::after {{
    content: '';
    position: absolute;
    bottom: -15px; /* -20px - 5px for border */
    left: 50%;
    transform: translateX(-50%);
    width: 100%;
    height: 2px;
    background-color: {accent_color};
    transition: all 0.3s ease-out;
}}

.content-cards {{
    display: flex;
    flex-wrap: wrap; /* Allow cards to wrap on smaller screens */
    gap: 1.5rem; /* Space between cards */
    margin-top: 1.5rem;
    width: 100%; /* Take full width of parent */
    justify-content: center;
}}

.card {{
    flex: 1 1 calc(33.333% - 1.5rem); /* w-1/3 with gap for 3 columns */
    min-width: 250px; /* Minimum width for cards */
    background-color: {card_bg_color};
    backdrop-filter: blur(10px);
    border: 2px solid {card_border_color};
    border-radius: 0.75rem; /* rounded-xl */
    padding: 1.5rem;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
    transition: all 0.3s ease-out;
    cursor: pointer;
}}

.card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}}

.card-title {{
    font-weight: 600;
    color: {body_text_color};
    font-size: 1.125rem; /* text-lg */
    margin-bottom: 0.5rem;
}}

.card-subtitle {{
    font-weight: 500;
    color: {text_color_gray};
    font-size: 0.75rem; /* text-xs */
}}

/* --- Dark Mode Styles --- */
body.dark-mode {{
    background-color: {body_bg_color};
    color: {body_text_color};
}}

body.dark-mode .header {{
    background-color: {glassmorphism_bg};
    border-color: {glassmorphism_border};
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
}}

body.dark-mode .header-item {{
    color: {text_color_black};
}}

body.dark-mode .header-item:hover {{
    color: {gradient_middle};
}}

body.dark-mode .app-title {{
    background: linear-gradient(45deg, {gradient_start}, {gradient_middle});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

body.dark-mode .app-subtitle {{
    color: {body_text_color};
}}

body.dark-mode .bottom-content-bar {{
    background-color: {card_bg_color};
    border-color: {card_border_color};
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
}}

body.dark-mode .tab-item {{
    color: {text_color_gray};
}}

body.dark-mode .tab-item:hover {{
    color: {body_text_color};
}}

body.dark-mode .tab-item.active {{
    color: {body_text_color};
}}

body.dark-mode .tab-item.active::after {{
    background-color: {gradient_middle};
}}

body.dark-mode .card {{
    background-color: {card_bg_color};
    border-color: {card_border_color};
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}}

body.dark-mode .card-title {{
    color: {body_text_color};
}}

body.dark-mode .card-subtitle {{
    color: {text_color_gray};
}}

.switch {{
    position: relative;
    display: inline-block;
    width: 40px; /* Adjust width as needed */
    height: 24px; /* Adjust height as needed */
    margin-left: 1rem;
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
    background-color: {toggle_bg}; /* Pink for light mode */
    border-radius: 24px;
    transition: background-color 0.4s;
    box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.2);
}}

.switch-indicator {{
    position: absolute;
    content: "";
    height: 20px; /* Slightly smaller than bg height */
    width: 20px; /* Slightly smaller than bg height */
    left: 2px;
    bottom: 2px;
    background-color: white;
    border-radius: 50%;
    transition: transform 0.4s;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}}

.switch-checkbox:checked + .switch-bg {{
    background-color: {toggle_bg}; /* Light blue for dark mode */
}}

.switch-checkbox:checked + .switch-bg .switch-indicator {{
    transform: translateX(16px); /* 40px width - 20px indicator width - 2*2px padding = 16px */
}}

/* Icon colors based on mode for header */
.header .fa-star {{ color: #ffa41d; }} /* app-color-yellow */
.header .app-color-black {{ color: {text_color_black}; }}
.header .app-color-dribbble {{ color: {text_color_dribble}; }}
.header .app-color-black {{ color: {text_color_black}; }}

.header .app-color-gray {{ color: {text_color_gray}; }}
.header .app-color-lavender {{ color: #7c65d7; }}
.header .app-color-pink {{ color: {accent_color}; }}

body.dark-mode .header .fa-star {{ color: #ffe54b; }} /* dark mode yellow */
body.dark-mode .header .app-color-black {{ color: {text_color_black}; }}
body.dark-mode .header .app-color-dribbble {{ color: {text_color_dribble}; }}
body.dark-mode .header .app-color-black {{ color: {text_color_black}; }}

body.dark-mode .header .app-color-gray {{ color: {text_color_gray}; }}
body.dark-mode .header .app-color-lavender {{ color: #a0a8f9; }}
body.dark-mode .header .app-color-pink {{ color: {gradient_middle}; }} /* Adjust pink for dark mode */

/* Specific card content colors */
.card-content-1 .card-title {{ color: {body_text_color}; }}
.card-content-1 .card-subtitle {{ color: {text_color_gray}; }}
.card-content-2 .card-title {{ color: {body_text_color}; }}
.card-content-2 .card-subtitle {{ color: {text_color_gray}; }}
.card-content-3 .card-title {{ color: {body_text_color}; }}
.card-content-3 .card-subtitle {{ color: {text_color_gray}; }}

/* Tailwind classes that might need override in specific cases or for custom elements */
.font-semibold {{ font-weight: 600; }}
.text-4xl {{ font-size: 2.25rem; line-height: 2.5rem; }}
.mb-4 {{ margin-bottom: 1rem; }}
.mx-1 {{ margin-left: 0.25rem; margin-right: 0.25rem; }}
.text-xs {{ font-size: 0.75rem; line-height: 1rem; }}
.text-lg {{ font-size: 1.125rem; line-height: 1.75rem; }}
.w-full {{ width: 100%; }}
.w-px {{ width: 1px; }} /* Placeholder/debug width if needed */
.h-2 {{ height: 0.5rem; }}
.rounded-full {{ border-radius: 9999px; }}
.relative {{ position: relative; }}
.flex {{ display: flex; }}
.flex-col {{ flex-direction: column; }}
.items-center {{ align-items: center; }}
.justify-center {{ justify-content: center; }}
.justify-between {{ justify-content: space-between; }}
.space-x-4 > :not([hidden]) ~ :not([hidden]) {{ margin-left: 1rem; }}
.mr-2 {{ margin-right: 0.5rem; }}
.mr-auto {{ margin-right: auto; }}
.mr-auto-active {{ margin-right: 0; }} /* Override for active tab to control spacing */
.mt-16 {{ margin-top: 4rem; }}
.pb-10 {{ padding-bottom: 2.5rem; }}
.px-6 {{ padding-left: 1.5rem; padding-right: 1.5rem; }}
.py-4 {{ padding-top: 1rem; padding-bottom: 1rem; }}
.rounded-md {{ border-radius: 0.375rem; }}
.rounded-xl {{ border-radius: 0.75rem; }}
.transition {{ transition-property: all; transition-duration: 150ms; transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1); }}
.duration-300 {{ transition-duration: 300ms; }}
.border-transparent {{ border-color: transparent; }}
.cursor-pointer {{ cursor: pointer; }}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Echoes Of Ping | Home</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Special+Gothic+Expanded+One&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css">
    <link href="https://cdn.tailwindcss.com" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="background-gradient"></div>
    <div class="app-container flex justify-center items-end pb-10">
        <div class="header">
            <div class="header-left">
                <a href="https://echoesofping.hashnode.dev" target="_blank" rel="noopener noreferrer" class="header-item">
                    <i class="icon fa-solid fa-star"></i>
                    <span>echoesofping.hashnode.dev</span>
                </a>
                <a href="https://youtube.com/@echoes-of-ping" target="_blank" rel="noopener noreferrer" class="header-item">
                    <i class="icon fa-brands fa-youtube"></i>
                    <span>Youtube</span>
                </a>
            </div>
            <div class="header-right">
                <span class="header-item">Join now</span>
                <span class="header-item">
                    <i class="icon fa-regular fa-user mr-2"></i>
                </span>
                <div class="switch">
                    <input type="checkbox" id="darkToggle" class="switch-checkbox">
                    <label for="darkToggle" class="switch-bg">
                        <span class="switch-indicator"></span>
                    </label>
                </div>
            </div>
        </div>

        <div class="flex flex-col text-center mt-16">
            <h1 class="app-title">{title_text}</h1>
            <span class="app-subtitle">{subtitle_text}</span>
        </div>

        <div class="bottom-content-bar">
            <div class="tab-nav">
                <span class="tab-item">Posts</span>
                <span class="tab-item">Blogs</span>
                <span class="tab-item active">Videos</span>
            </div>
            <div class="content-cards">
                <div class="card card-content-1">
                    <span class="card-title">Installation Guide</span>
                    <span class="card-subtitle">Speedtest-Tracker</span>
                </div>
                <div class="card card-content-2">
                    <span class="card-title">Setup</span>
                    <span class="card-subtitle">Uptime-Kuma</span>
                </div>
                <div class="card card-content-3">
                    <span class="card-title">Playlist</span>
                    <span class="card-subtitle">HomeLab(Self-hosting)</span>
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

    // Check for saved theme preference
    if (localStorage.getItem('theme') === 'dark') {
        document.body.classList.add('dark-mode');
        darkToggle.checked = true;
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

    // Handle active tab indicator (static for now, but ready for dynamic)
    const tabItems = document.querySelectorAll('.tab-item');
    tabItems.forEach(item => {
        item.addEventListener('click', () => {
            tabItems.forEach(tab => tab.classList.remove('active'));
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
