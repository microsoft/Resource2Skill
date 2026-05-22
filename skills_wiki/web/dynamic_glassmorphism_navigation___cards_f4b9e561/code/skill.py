import os

def create_component(
    output_dir: str,
    title_text: str = "Why not Your own Services?",
    body_text: str = "Start Your Self-hosting Journey with us!",
    color_scheme: str = "light",        # "dark" or "light"
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the "Dynamic Glassmorphism Navigation & Cards" visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    os.makedirs(output_dir, exist_ok=True)

    # --- Theme dependent colors ---
    if color_scheme == "dark":
        body_bg_start = "#0c1a1a"
        text_color = "#d4f9f0"
        surface_bg_color = "rgba(0, 0, 0, 0.1)" # Darker glass effect
        border_color = "#1a3a3a"
        accent_purple = "#9ea1cf" # Lavender from video for UI highlights
        accent_teal = "#5fc651" # Green from video for title gradient
        card_text_color = "#d4f9f0"
        card_bg_light = "rgba(255, 255, 255, 0.08)"
        card_bg_light_2 = "rgba(255, 255, 255, 0.05)" # Slightly different for depth
        app_shadow = "rgba(0, 0, 0, 0.6)" # Darker shadow for dark mode
        active_tab_color_main = "#00ffa2" # Teal for dark mode active tab
        active_tab_color_sub = "#00d1a1" # Slightly darker teal
        nav_tab_text_color = "#88c7fd" # Light blue for inactive tabs
        hover_border_color_main = "#22d3ee" # Cyan for hashnode hover
        hover_border_color_sub = "#fb28cd" # Pink for youtube hover
        join_now_bg_color = "black" # Button background in light mode
        join_now_text_color = "white" # Button text in light mode
        user_icon_color = "#f0f0f0" # User icon color in dark mode
        lights_text_color = "#f0f0f0" # "Lights" text color in dark mode

    else: # light mode
        body_bg_start = "#f3f3f3"
        text_color = "#292b48"
        surface_bg_color = "rgba(255, 255, 255, 0.5)" # Lighter glass effect
        border_color = "#e0e0e0"
        accent_purple = "#9ea1cf" # Lavender from video for UI highlights
        accent_teal = "#5fc651" # Green from video for title gradient
        card_text_color = "#555555" # Default text color for cards
        card_bg_light = "white"
        card_bg_light_2 = "#eff2fc" # Slightly different for depth
        app_shadow = "rgba(0, 0, 0, 0.08)" # Lighter shadow for light mode
        active_tab_color_main = "#ff62d0" # Pink for light mode active tab
        active_tab_color_sub = "#fa39ad" # Slightly darker pink
        nav_tab_text_color = "#877f95" # Gray for inactive tabs
        hover_border_color_main = "#ee5e4b" # Red for hashnode hover
        hover_border_color_sub = "#ffc432" # Yellow for youtube hover
        join_now_bg_color = "black" # Button background in light mode
        join_now_text_color = "white" # Button text in light mode
        user_icon_color = "#292b48" # User icon color in light mode
        lights_text_color = "#292b48" # "Lights" text color in light mode

    # Define common styles for background glow circles based on the primary video colors
    circle_red_gradient = "linear-gradient(to bottom, #fa39ad, #fa6c4c)"
    circle_yellow_gradient = "linear-gradient(to bottom, #ffc432, #ffb300)"
    circle_green_gradient = "linear-gradient(to bottom, #5bd0a7, #5fc651)"

    # --- CSS ---
    css = f"""
@import url('https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Special+Gothic+Expanded+One&display=swap');

/* Base Styles */
*::before, *::after {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Poppins', sans-serif;
    background-color: #f3f3f3; /* Light mode default */
    color: #292b48; /* Light mode default text */
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    transition: background-color 0.3s ease-in-out, color 0.3s ease-in-out;
    position: relative;
    overflow: hidden;
}}

/* Main app container */
.app-container {{
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    width: 100%;
    max-width: 1400px;
    min-height: 100vh;
    padding-bottom: 40px;
    position: relative;
    z-index: 1;
    background-color: rgba(255, 255, 255, 0); /* Transparent initially to show body bg */
}}

/* Background glow effect */
.circle {{
    position: absolute;
    border-radius: 50%;
    filter: blur(120px);
    z-index: 0;
    opacity: 0.7;
    animation: pulse 4s infinite alternate ease-in-out;
}}

.circle.red {{
    background: {circle_red_gradient};
    width: 450px;
    height: 450px;
    top: -100px;
    left: -150px;
}}

.circle.yellow {{
    background: {circle_yellow_gradient};
    width: 350px;
    height: 350px;
    bottom: -100px;
    right: -100px;
}}

.circle.green {{
    background: {circle_green_gradient};
    width: 400px;
    height: 400px;
    top: 50%;
    left: 30%;
    transform: translateY(-50%);
}}

@keyframes pulse {{
    0% {{ transform: scale(1) translateY(-50%); opacity: 0.7; }}
    50% {{ transform: scale(1.05) translateY(-48%); opacity: 0.8; }}
    100% {{ transform: scale(1) translateY(-50%); opacity: 0.7; }}
}}

/* Header Section */
.app-title {{
    font-family: 'Special Gothic Expanded One', sans-serif;
    font-size: 3.5rem;
    font-weight: 400;
    line-height: 1.2;
    text-align: center;
    margin-top: 50px;
    margin-bottom: 10px;
    color: transparent;
    background: linear-gradient(45deg, #ff62d0, #b366ff); /* Pink to purple gradient (light) */
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    transition: all 0.3s ease-in-out;
}}

.app-subtitle {{
    font-size: 1.2rem;
    font-weight: 300;
    text-align: center;
    margin-bottom: 40px;
    opacity: 0.8;
    color: #292b48; /* Light mode default */
    transition: color 0.3s ease-in-out;
}}

/* Nav bar */
.absolute.top-16 {{
    position: absolute;
    top: 16px;
    width: 100%;
}}

.flex {{
    display: flex;
}}

.flex-col {{
    flex-direction: column;
}}

.w-full {{
    width: 100%;
}}

.items-center {{
    align-items: center;
}}

.items-end {{
    align-items: flex-end;
}}

.justify-center {{
    justify-content: center;
}}

.justify-between {{
    justify-content: space-between;
}}

.px-6 {{
    padding-left: 24px;
    padding-right: 24px;
}}

.py-4 {{
    padding-top: 16px;
    padding-bottom: 16px;
}}

.ml-auto {{
    margin-left: auto;
}}

.mr-auto {{
    margin-right: auto;
}}

.mr-2 {{
    margin-right: 8px;
}}

.mr-4 {{
    margin-right: 16px;
}}

.my-36 {{
    margin-top: 144px;
    margin-bottom: 144px;
}}

.rounded-full {{
    border-radius: 9999px;
}}

.rounded-md {{
    border-radius: 6px;
}}

.rounded-xl {{
    border-radius: 12px;
}}

.app-bg-white {{
    background-color: white;
}}

.app-bg-light-white {{
    background-color: white; /* Card bg light mode */
}}

.app-bg-light-white-2 {{
    background-color: #eff2fc; /* Nav item bg light mode */
}}

.app-shadow {{
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08); /* Light mode shadow */
}}

.transition-duration-300 {{
    transition-duration: 300ms;
}}

.app-color-yellow {{
    color: #f7b900; /* Font Awesome star color (yellow) */
    transition: color 0.3s ease-in-out;
}}

.app-color-black {{
    color: #292b48; /* General dark text */
    transition: color 0.3s ease-in-out;
}}

.app-color-gray {{
    color: #877f95; /* Inactive nav tab text color */
    transition: color 0.3s ease-in-out;
}}

.app-color-lavender {{
    color: #9ea1cf; /* General lavender accent */
    transition: color 0.3s ease-in-out;
}}

.app-color-pink {{
    color: #ff62d0; /* General pink accent */
    transition: color 0.3s ease-in-out;
}}

.app-color-dribbble {{
    color: #ea4c89; /* Dribbble icon color */
}}

.text-xs {{
    font-size: 0.75rem;
    line-height: 1rem;
}}

.text-sm {{
    font-size: 0.875rem;
    line-height: 1.25rem;
}}

.text-lg {{
    font-size: 1.125rem;
    line-height: 1.75rem;
}}

.text-pink-400 {{
    color: #f472b6;
}}

.text-black {{
    color: black;
}}

.font-bold {{
    font-weight: 700;
}}

.font-semibold {{
    font-weight: 600;
}}

.border-2 {{
    border-width: 2px;
}}

.border-transparent {{
    border-color: transparent;
}}

/* Custom switch styles */
.switch {{
    position: relative;
    display: inline-block;
    width: 44px;
    height: 24px;
}}

.switch input {{
    opacity: 0;
    width: 0;
    height: 0;
}}

.switch-bg {{
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #ff62d0; /* Light mode on state */
    border-radius: 15px;
    transition: background-color 0.4s ease-in-out;
    border: 2px solid white;
}}

.switch-bg:before {{
    position: absolute;
    content: "";
    height: 16px;
    width: 16px;
    left: 4px;
    bottom: 2px;
    background-color: white;
    border-radius: 50%;
    transition: transform 0.4s ease-in-out;
}}

input:checked + .switch-bg {{
    background-color: #9ecffa; /* Light mode off state */
    border: 2px solid white;
}}

input:checked + .switch-bg:before {{
    transform: translateX(18px);
}}

.lights-text {{
    color: #292b48; /* Light mode default */
    margin-left: 8px;
    font-size: 0.875rem;
    font-weight: 600;
    transition: color 0.3s ease-in-out;
}}


/* Dark mode styles */
body.dark-mode {{
    background-color: #0c1a1a;
    color: #d4f9f0;
}}

body.dark-mode .app-container {{
    background-color: rgba(0, 0, 0, 0.1);
}}

body.dark-mode .app-title {{
    background: linear-gradient(45deg, {accent_teal}, {active_tab_color_main});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

body.dark-mode .app-subtitle {{
    color: #d4f9f0;
}}

body.dark-mode .app-bg-light-white {{
    background-color: #081515;
    border-color: #1a3a3a;
}}

body.dark-mode .app-bg-light-white-2 {{
    background-color: #122222;
    border-color: #1a3a3a;
}}

body.dark-mode .app-shadow {{
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.6);
}}

body.dark-mode .app-color-yellow {{
    color: #f7b900;
}}

body.dark-mode .app-color-black {{
    color: #d4f9f0; /* Text color in dark mode */
}}

body.dark-mode .app-color-gray {{
    color: #88c7fd;
}}

body.dark-mode .app-color-lavender {{
    color: #9ea1cf;
}}

body.dark-mode .app-color-pink {{
    color: #00ffa2;
}}

body.dark-mode .lights-text {{
    color: #d4f9f0;
}}

body.dark-mode .switch-bg {{
    background-color: #00ffa2; /* Dark mode on state */
}}
body.dark-mode input:checked + .switch-bg {{
    background-color: #8c3cf3; /* Dark mode off state */
}}


/* Nav tabs */
.tabs-container {{
    display: flex;
    justify-content: center;
    gap: 20px;
    background: rgba(255, 255, 255, 0.5); /* Light mode glass effect */
    backdrop-filter: blur(20px);
    border-radius: 12px;
    padding: 10px 20px;
    margin-bottom: 30px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    border: 1px solid #e0e0e0; /* Light mode border */
    transition: all 0.3s ease-in-out;
    position: relative;
}}

.nav-tab {{
    position: relative;
    padding: 8px 15px;
    font-weight: 600;
    color: #877f95; /* Light mode inactive text */
    cursor: pointer;
    transition: color 0.3s ease-in-out;
}}

.nav-tab:hover {{
    color: #292b48; /* Light mode hover text */
}}

.nav-tab.active {{
    color: #292b48; /* Light mode active text */
}}

.nav-tab.active::after {{
    content: '';
    position: absolute;
    bottom: -5px;
    left: 50%;
    transform: translateX(-50%);
    width: 70%;
    height: 2px;
    background: #ff62d0; /* Light mode active underline */
    border-radius: 2px;
    transition: all 0.3s ease-in-out;
}}

body.dark-mode .tabs-container {{
    background: rgba(0, 0, 0, 0.1); /* Dark mode glass effect */
    border: 1px solid #1a3a3a; /* Dark mode border */
}}

body.dark-mode .nav-tab {{
    color: #88c7fd; /* Dark mode inactive text */
}}

body.dark-mode .nav-tab:hover {{
    color: #d4f9f0; /* Dark mode hover text */
}}

body.dark-mode .nav-tab.active {{
    color: #d4f9f0; /* Dark mode active text */
}}

body.dark-mode .nav-tab.active::after {{
    background: #00ffa2; /* Dark mode active underline */
}}


/* Content Cards */
.cards-grid {{
    display: flex;
    gap: 20px;
    justify-content: center;
    width: 100%;
    max-width: 1000px;
    padding: 20px 0;
}}

.card {{
    background: white; /* Light mode card bg */
    backdrop-filter: blur(10px);
    border-radius: 10px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    border: 1px solid #e0e0e0; /* Light mode card border */
    flex: 1;
    min-width: 250px;
    transition: all 0.3s ease-in-out;
}}

.card-title {{
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 10px;
    color: #555555; /* Light mode card text */
    transition: color 0.3s ease-in-out;
}}

.card-subtitle {{
    font-size: 0.9rem;
    color: #877f95; /* Light mode card subtitle */
    transition: color 0.3s ease-in-out;
}}

/* Other interactive elements */
a.top-nav-item, .join-now {{
    transition: all 0.3s ease-in-out;
    cursor: pointer;
}}

a.top-nav-item:hover, .join-now:hover {{
    transform: translateY(-2px);
}}

.join-now {{
    padding: 8px 16px;
    background-color: black;
    color: white;
    border-radius: 6px;
    font-weight: 600;
    text-decoration: none;
    margin-left: 16px;
}}

.user-icon {{
    color: #292b48;
    font-size: 1.25rem;
    margin-left: 16px;
    margin-right: 8px;
}}

/* Media queries for responsiveness */
@media (max-width: 768px) {{
    .app-title {{
        font-size: 2.5rem;
    }}
    .app-subtitle {{
        font-size: 1rem;
    }}
    .absolute.top-16 {{
        flex-wrap: wrap;
        justify-content: center;
        padding-top: 10px;
    }}
    .top-nav-item, .join-now, .user-icon {{
        margin-bottom: 10px;
        margin-left: 5px;
        margin-right: 5px;
    }}
    .tabs-container {{
        flex-wrap: wrap;
        gap: 10px;
        padding: 5px 10px;
    }}
    .cards-grid {{
        flex-direction: column;
        align-items: center;
    }}
    .card {{
        min-width: unset;
        width: 90%;
    }}
    .circle {{
        filter: blur(80px);
    }}
}}
"""

    # --- HTML ---
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Echoes of Ping | Home</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Special+Gothic+Expanded+One&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-container">
        <div class="absolute top-16 flex w-full items-center px-6" style="justify-content: space-between;">
            <a href="https://echos-of-ping.hashnode.dev" target="_blank" rel="noopener noreferrer" class="top-nav-item flex items-center app-bg-light-white-2 border-2 border-transparent rounded-md px-6 py-4 mr-auto app-shadow hover:border-[{hover_border_color_main}] transition duration-300">
                <i class="fa-solid fa-star app-color-yellow text-xs"></i>
                <span class="font-bold app-color-black ml-4 text-xs">echos-of-ping.hashnode.dev</span>
            </a>
            <a href="https://youtube.com/@echoes-of-ping" target="_blank" rel="noopener noreferrer" class="top-nav-item flex items-center app-bg-light-white-2 border-2 border-transparent rounded-md px-6 py-4 ml-3 app-shadow hover:border-[{hover_border_color_sub}] transition duration-300">
                <i class="fa-brands fa-youtube app-color-dribbble mr-2"></i>
                <span class="font-bold app-color-black text-xs">Youtube</span>
            </a>
            <a href="#" class="join-now">Join now</a>
            <i class="fa-regular fa-user user-icon"></i>
            <i class="fa-solid fa-angle-down text-xs app-color-black"></i>
        </div>
        <div class="flex flex-col text-center my-36">
            <span class="font-semibold text-4xl mb-4 app-title">{title_text}</span>
            <span class="app-subtitle font-semibold">{body_text}</span>
        </div>
        <div class="tabs-container">
            <span class="nav-tab" id="postsTab">Posts</span>
            <span class="nav-tab" id="blogsTab">Blogs</span>
            <span class="nav-tab active" id="videosTab">Videos</span>
            <label class="nav-tab switch" id="lightsToggle">
                <input type="checkbox" id="darkToggle" class="switch-checkbox">
                <span class="switch-bg"></span>
                <span class="lights-text">Lights</span>
            </label>
        </div>
        <div class="cards-grid">
            <div class="card app-bg-light-white">
                <span class="card-title">Installation Guide</span>
                <span class="card-subtitle">Speedtest-Tracker</span>
            </div>
            <div class="card app-bg-light-white">
                <span class="card-title">Setup</span>
                <span class="card-subtitle">Uptime-Kuma</span>
            </div>
            <div class="card app-bg-light-white">
                <span class="card-title">Playlist</span>
                <span class="card-subtitle">HomeLab (Self-hosting)</span>
            </div>
        </div>
    </div>
    <div class="circle red"></div>
    <div class="circle yellow"></div>
    <div class="circle green"></div>
    <script src="script.js"></script>
</body>
</html>"""

    # --- JavaScript ---
    js = f"""
document.addEventListener('DOMContentLoaded', () => {{
    const darkToggle = document.getElementById('darkToggle');
    const body = document.body;
    const navTabs = document.querySelectorAll('.nav-tab');

    // Load theme from localStorage
    if (localStorage.getItem('theme') === 'dark') {{
        body.classList.add('dark-mode');
        darkToggle.checked = true;
    }} else {{
        body.classList.remove('dark-mode');
        darkToggle.checked = false;
    }}

    // Dark mode toggle functionality
    darkToggle.addEventListener('change', function() {{
        body.classList.toggle('dark-mode', this.checked);
        localStorage.setItem('theme', this.checked ? 'dark' : 'light');
    }});

    // Active tab functionality
    navTabs.forEach(tab => {{
        tab.addEventListener('click', () => {{
            navTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
        }});
    }});

    // Set initial active tab (e.g., 'Videos' from the video)
    const videosTab = document.getElementById('videosTab');
    if (videosTab) {{
        videosTab.classList.add('active');
    }}
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
