import os

def create_component(
    output_dir: str,
    title_text: str = "Why not Your own Services?",
    subtitle_text: str = "Start Your Self-hosting Journey with us!",
    color_scheme: str = "light",  # "light" or "dark"
    main_youtube_url: str = "https://youtube.com/@echoesofping",
    hashnode_url: str = "https://echoesofping.hashnode.dev",
    card_1_title: str = "Installation Guide",
    card_1_subtitle: str = "Speedtest-Tracker",
    card_2_title: str = "Setup",
    card_2_subtitle: str = "Uptime-Kuma",
    card_3_title: str = "Playlist",
    card_3_subtitle: str = "HomeLab(Self-hosting)",
) -> dict:
    """
    Create a web component reproducing the "Glassmorphism Hero with Interactive Tabbed Content & Dark Mode"
    visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    os.makedirs(output_dir, exist_ok=True)

    # --- Theme dependent colors ---
    if color_scheme == "dark":
        body_bg = "#0c1a1a"
        body_text = "#d4f9f0"
        card_bg = "#112222"
        card_text_active = "#d4f9f0"
        card_text_inactive = "#97abaa"
        gradient_text_start = "#00ffaa"
        gradient_text_end = "#0066ff"
        main_gradient_start = "#00ffaa"
        main_gradient_end = "#0066ff"
        shadow_color = "rgba(0, 255, 170, 0.1)"
        border_color_switch = "#1a3a3a"
        tab_underline_color = "#00ffaa"
        circle_red_bg = "#1a3a3a"
        circle_yellow_bg = "#1a3a3a"
        circle_green_bg = "#1a3a3a"
        card_hover_border = "#00ffaa" # Adjusted for dark mode
        card_hover_shadow = "rgba(0, 255, 170, 0.2)"
    else: # Light mode
        body_bg = "#f3f3f3"
        body_text = "#292b48"
        card_bg = "#ffffff"
        card_text_active = "#292b48"
        card_text_inactive = "#877f95"
        gradient_text_start = "#fb28cd"
        gradient_text_end = "#7c65d7"
        main_gradient_start = "#fa39ad"
        main_gradient_end = "#fa6c4c"
        shadow_color = "rgba(0, 0, 0, 0.03)"
        border_color_switch = "#f3f3f3"
        tab_underline_color = "#fb28cd"
        circle_red_bg = "#fe642d"
        circle_yellow_bg = "#ffc432"
        circle_green_bg = "#5f8b47"
        card_hover_border = "#fb28cd"
        card_hover_shadow = "rgba(255, 0, 150, 0.1)"


    # --- CSS ---
    css = f"""
@import url('https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Special+Gothic+Expanded+One&display=swap');

/* Base styles */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Poppins', sans-serif;
    background-color: {body_bg};
    color: {body_text};
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: flex-start; /* Align items to the top initially */
    padding-bottom: 2rem; /* Give space for content below hero */
    transition: background-color 0.3s ease-out, color 0.3s ease-out;
}}

.app-container {{
    display: flex;
    justify-content: center;
    align-items: center;
    padding-bottom: 2.5rem; /* pb-10 in Tailwind is 2.5rem */
    position: relative;
    z-index: 10;
    flex-direction: column; /* Ensure vertical stacking */
    min-height: 100vh; /* Ensure it takes full viewport height */
    width: 100%; /* Take full width */
}}

/* Decorative background circles */
.circle {{
    width: 450px;
    height: 450px;
    background: linear-gradient(to bottom, {main_gradient_start}, {main_gradient_end});
    filter: blur(120px);
    border-radius: 50%;
    position: absolute;
    z-index: -1;
}}

.red {{
    background: {circle_red_bg};
    top: 5%;
    left: 10%;
}}

.yellow {{
    background: {circle_yellow_bg};
    bottom: 15%;
    right: 15%;
}}

.green {{
    background: {circle_green_bg};
    top: 25%;
    right: 10%;
}}

/* Header/Navbar styles */
.navbar {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 1.5rem 0; /* py-6 in Tailwind */
    z-index: 20; /* Above main content */
}}

.navbar-content {{
    display: flex;
    align-items: center;
    width: 41.666667%; /* w-5/12 */
    padding: 1rem 1.5rem; /* px-6 py-4 */
    background-color: {card_bg};
    border-radius: 0.375rem; /* rounded-md */
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.03); /* app-shadow */
    transition: background-color 0.3s ease-out, box-shadow 0.3s ease-out;
    backdrop-filter: blur(200px);
}}

.navbar-content a, .navbar-content span {{
    display: flex;
    align-items: center;
    text-decoration: none;
    font-size: 0.75rem; /* text-xs */
    font-weight: 700; /* font-bold */
    line-height: 1;
    white-space: nowrap;
    color: {body_text};
    transition: color 0.2s ease-in-out;
}}

.navbar-content a:hover {{
    color: {accent_color};
}}

.navbar-content .fa-star {{
    color: {gradient_text_start}; /* app-color-yellow */
    margin-right: 0.5rem; /* mr-2 */
}}

.navbar-content .ml-4 {{
    margin-left: 1rem; /* ml-4 */
}}

.navbar-content .mr-auto {{
    margin-right: auto;
}}

.navbar-content .mr-2 {{
    margin-right: 0.5rem;
}}

.navbar-content .mr-1 {{
    margin-right: 0.25rem;
}}


.fa-ellipsis {{
    color: {card_text_inactive}; /* app-color-lavender */
    font-size: 0.75rem;
    margin-right: 0.5rem;
}}

/* YouTube Link styling */
.navbar-content .youtube-link {{
    color: {body_text}; /* app-color-dribble */
    margin-right: 1rem;
}}

.navbar-content .youtube-link:hover {{
    color: #FF0000; /* YouTube red */
}}

.navbar-content .youtube-link .fa-youtube {{
    font-size: 1rem; /* text-base */
}}

.navbar-content .join-now {{
    color: {card_text_active}; /* app-color-black */
    padding: 0.5rem 1rem; /* px-4 py-2 */
    border-radius: 0.25rem; /* rounded */
    background-color: {accent_color};
}}

.navbar-content .join-now:hover {{
    background-color: {gradient_text_end};
}}

.navbar-content .fa-user-m {{
    color: {card_text_active}; /* app-color-black */
    margin-left: 1rem;
    margin-right: 0.5rem;
}}

.navbar-content .fa-angle-down {{
    color: {card_text_active}; /* app-color-black */
}}

/* Main Hero Section */
.hero-section {{
    display: flex;
    flex-direction: column;
    text-align: center;
    margin-top: 9rem; /* my-36 in Tailwind is 9rem (144px) */
    margin-bottom: 9rem;
    position: relative;
    z-index: 1;
}}

.hero-title {{
    font-family: 'Special Gothic Expanded One', sans-serif;
    font-size: 4rem; /* text-4xl */
    font-weight: 700; /* font-bold */
    background: linear-gradient(45deg, {gradient_text_start}, {gradient_text_end});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 1rem; /* mb-4 */
    line-height: 1; /* Adjust line height for better appearance */
}}

.hero-subtitle {{
    font-size: 1.125rem; /* text-lg */
    font-weight: 500; /* font-semibold */
    color: {body_text}; /* app-color-black */
    max-width: 600px;
    margin: 0 auto;
}}

/* Tabbed content section */
.tab-container {{
    background-color: {card_bg};
    width: 83.333333%; /* w-10/12 */
    padding: 3rem 1.5rem 4rem 1.5rem; /* px-6 pt-12 pb-16 */
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.03); /* app-shadow */
    border-radius: 0.75rem; /* rounded-xl */
    backdrop-filter: blur(200px);
    transition: background-color 0.3s ease-out, box-shadow 0.3s ease-out;
    margin-top: 2rem; /* mt-8 */
}}

.tab-nav {{
    display: flex;
    justify-content: flex-start;
    padding-right: 1rem; /* pr-4 */
    margin-bottom: 2rem; /* mb-8 */
    border-bottom: 2px solid #e0e0e0;
    position: relative;
}}

.tab-nav-item {{
    position: relative;
    padding: 0.5rem 0.75rem; /* px-3 py-2 */
    font-size: 0.875rem; /* text-sm */
    font-weight: 600; /* font-semibold */
    color: {card_text_inactive}; /* app-color-gray */
    cursor: pointer;
    margin-right: 1rem; /* mx-4 */
    transition: color 0.2s ease-in-out;
}}

.tab-nav-item:hover {{
    color: {card_text_active};
}}

.tab-nav-item.active {{
    color: {card_text_active};
}}

.tab-nav-item.active::after {{
    content: "";
    position: absolute;
    bottom: -2px; /* Adjust to sit on the border */
    left: 0;
    width: 100%;
    height: 2px;
    background-color: {tab_underline_color};
    transition: width 0.3s ease-out, left 0.3s ease-out;
}}

/* Toggle Switch Styles */
.switch {{
    position: relative;
    display: inline-block;
    width: 44px; /* Default width */
    height: 24px; /* Default height */
    margin-left: auto; /* Push to the right */
    margin-right: 1rem; /* mr-4 */
    margin-top: 0.5rem; /* mt-2 */
    margin-bottom: 0.5rem; /* mb-2 */
}}

/* Hide default HTML checkbox */
.switch-checkbox {{
    display: none;
}}

/* The slider */
.switch-bg {{
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: {gradient_text_start}; /* Start color */
    border-radius: 15px; /* Rounded corners for the track */
    transition: background-color .4s;
    border: 2px solid white; /* White border for contrast */
}}

.switch-bg:before {{
    position: absolute;
    content: "";
    height: 16px; /* Indicator height */
    width: 16px; /* Indicator width */
    left: 4px; /* Initial position */
    bottom: 2px; /* Align to bottom with border */
    background-color: white;
    border-radius: 50%;
    transition: transform .4s;
}}

/* Checked state */
.switch-checkbox:checked + .switch-bg {{
    background-color: #e9ecfa; /* End color */
}}

.switch-checkbox:checked + .switch-bg:before {{
    transform: translateX(20px); /* Move indicator to the right */
}}

/* Content Cards */
.cards-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr); /* Three columns */
    gap: 1.5rem; /* gap-6 */
    margin-top: 1.5rem; /* mt-6 */
}}

.card {{
    background-color: {card_bg};
    border: 2px solid {border_color_switch};
    padding: 1.5rem; /* p-6 */
    border-radius: 0.5rem; /* rounded-lg */
    box-shadow: 0 4px 6px rgba(0,0,0,0.05); /* shadow-md */
    transition: all 0.3s ease-in-out;
    text-decoration: none; /* For links */
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}}

.card:hover {{
    border-color: {card_hover_border};
    box-shadow: 0 12px 24px {card_hover_shadow};
    transform: translateY(-5px);
}}

.card-title {{
    font-weight: 600; /* font-semibold */
    font-size: 1.25rem; /* text-xl */
    color: {card_text_active}; /* app-color-black */
    margin-bottom: 0.5rem;
}}

.card-subtitle {{
    font-size: 0.875rem; /* text-sm */
    color: {card_text_inactive}; /* app-color-gray */
}}

/* DARK MODE STYLES */
body.dark-mode {{
    background-color: #0c1a1a;
    color: #d4f9f0;
}}

body.dark-mode .app-container {{
    background-color: #081515; /* Darker container background */
}}

body.dark-mode .circle {{
    background: linear-gradient(to bottom, #00ffaa, #0066ff);
}}

body.dark-mode .navbar-content, body.dark-mode .tab-container, body.dark-mode .card {{
    background-color: #112222;
    box-shadow: 0 10px 25px rgba(0, 255, 170, 0.1);
    border-color: #1a3a3a;
}}

body.dark-mode .navbar-content a, body.dark-mode .navbar-content span,
body.dark-mode .hero-subtitle, body.dark-mode .card-title {{
    color: #d4f9f0;
}}

body.dark-mode .tab-nav-item, body.dark-mode .card-subtitle {{
    color: #97abaa;
}}

body.dark-mode .tab-nav-item.active {{
    color: #00ffaa;
}}

body.dark-mode .tab-nav-item.active::after {{
    background-color: #00ffaa;
}}

body.dark-mode .navbar-content .youtube-link {{
    color: #d4f9f0;
}}

body.dark-mode .navbar-content .fa-star, body.dark-mode .navbar-content .fa-ellipsis,
body.dark-mode .navbar-content .fa-user-m, body.dark-mode .navbar-content .fa-angle-down {{
    color: #d4f9f0; /* Ensure icons are visible */
}}

body.dark-mode .navbar-content .join-now {{
    background-color: #00ffaa; /* Dark mode accent */
    color: #1a1a2e; /* Dark text for bright button */
}}

body.dark-mode .card:hover {{
    border-color: #00ffaa;
    box-shadow: 0 12px 24px rgba(0, 255, 170, 0.2);
}}

body.dark-mode .switch-bg {{
    background-color: #00ffaa; /* Dark mode switch track color */
    border-color: #1a3a3a; /* Dark mode switch border color */
}}
body.dark-mode .switch-bg:before {{
    background-color: #0066ff; /* Dark mode switch indicator color */
}}
body.dark-mode .switch-checkbox:checked + .switch-bg {{
    background-color: #e9ecfa; /* Dark mode checked track color */
}}
body.dark-mode .switch-checkbox:checked + .switch-bg:before {{
    background-color: #00ffaa; /* Dark mode checked indicator color */
}}

@media (max-width: 768px) {{
    .navbar-content {{
        width: 90%;
        padding: 0.75rem 1rem;
    }}
    .hero-title {{
        font-size: 2.5rem;
    }}
    .hero-subtitle {{
        font-size: 1rem;
        padding: 0 1rem;
    }}
    .tab-container {{
        width: 95%;
        padding: 1.5rem 1rem 2rem 1rem;
    }}
    .cards-grid {{
        grid-template-columns: 1fr; /* Single column on mobile */
    }}
    .navbar-content a, .navbar-content span {{
        font-size: 0.65rem;
    }}
}}

    """

    # --- HTML ---
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Echoes of Ping | Home</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Special+Gothic+Expanded+One&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-container">
        <!-- Background Circles -->
        <div class="circle red"></div>
        <div class="circle yellow"></div>
        <div class="circle green"></div>

        <!-- Navbar (top) -->
        <div class="navbar">
            <div class="navbar-content">
                <i class="fa-solid fa-star"></i>
                <span class="font-bold ml-4 mr-auto text-xs">{hashnode_url}</span>
                <i class="fa-solid fa-ellipsis mr-2"></i>
                <a href="{main_youtube_url}" target="_blank" rel="noopener noreferrer" class="youtube-link">
                    <i class="fa-brands fa-youtube mr-1"></i>
                    <span>YouTube</span>
                </a>
                <span class="font-bold text-xs">Join Now</span>
                <i class="fa-solid fa-user-m ml-4 mr-2"></i>
                <i class="fa-solid fa-angle-down"></i>
                <!-- Dark Mode Toggle -->
                <label class="switch">
                    <input type="checkbox" id="darkToggle" class="switch-checkbox">
                    <span class="switch-bg"></span>
                    <span class="switch-indicator"></span>
                </label>
            </div>
        </div>

        <!-- Hero Section -->
        <div class="hero-section">
            <span class="hero-title">{title_text}</span>
            <span class="hero-subtitle">{subtitle_text}</span>
        </div>

        <!-- Tabbed Content Section -->
        <div class="tab-container">
            <div class="tab-nav">
                <span class="tab-nav-item active">Posts</span>
                <span class="tab-nav-item">Blogs</span>
                <span class="tab-nav-item">Videos</span>
            </div>
            <div class="cards-grid">
                <a href="#" class="card">
                    <span class="card-title">{card_1_title}</span>
                    <span class="card-subtitle">{card_1_subtitle}</span>
                </a>
                <a href="#" class="card">
                    <span class="card-title">{card_2_title}</span>
                    <span class="card-subtitle">{card_2_subtitle}</span>
                </a>
                <a href="#" class="card">
                    <span class="card-title">{card_3_title}</span>
                    <span class="card-subtitle">{card_3_subtitle}</span>
                </a>
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>
    """

    # --- JavaScript ---
    js = f"""
document.addEventListener('DOMContentLoaded', () => {{
    const darkToggle = document.getElementById('darkToggle');
    const tabNavItems = document.querySelectorAll('.tab-nav-item');

    // Load saved theme preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark-mode') {{
        document.body.classList.add('dark-mode');
        darkToggle.checked = true;
    }}

    // Dark mode toggle functionality
    darkToggle.addEventListener('change', function() {{
        document.body.classList.toggle('dark-mode', this.checked);
        localStorage.setItem('theme', this.checked ? 'dark-mode' : 'light-mode');
    }});

    // Tab navigation active state
    tabNavItems.forEach(item => {{
        item.addEventListener('click', () => {{
            tabNavItems.forEach(nav => nav.classList.remove('active'));
            item.classList.add('active');
        }});
    }});
}});
    """

    # --- Write files ---
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

