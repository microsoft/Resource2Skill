def create_component(
    output_dir: str,
    title_text: str = "Hi, It's Developer",
    body_text: str = "I'm a passionate frontend developer specializing in creating interactive, glowing web experiences.",
    color_scheme: str = "dark",        
    accent_color: str = "#00ff51",     # Cyberpunk neon green
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Neon Glow Hero & Glass Header effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Force dark scheme mapping for best neon contrast, but allow slight variations
    if color_scheme == "light":
        bg_color = "#f0f0f0"
        second_bg = "#ffffff"
        text_color = "#080808"
        glass_bg = "rgba(255, 255, 255, 0.4)"
        btn_text = "#ffffff"
    else:
        bg_color = "#080808"
        second_bg = "#131313"
        text_color = "#ffffff"
        glass_bg = "rgba(0, 0, 0, 0.3)"
        btn_text = "#000000"

    # === CSS ===
    css = f"""@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;800&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    text-decoration: none;
    outline: none;
}}

:root {{
    --bg-color: {bg_color};
    --second-bg-color: {second_bg};
    --text-color: {text_color};
    --main-color: {accent_color};
    --btn-text: {btn_text};
}}

/* Preview container to simulate browser window for the agent */
.preview-window {{
    width: {width_px}px;
    height: {height_px}px;
    max-width: 100%;
    margin: 0 auto;
    position: relative;
    overflow-y: auto;
    overflow-x: hidden;
    background: var(--bg-color);
    color: var(--text-color);
    font-family: 'Poppins', sans-serif;
    scroll-behavior: smooth;
    border: 1px solid #333;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}}

/* Header / Glassmorphism */
.header {{
    position: sticky;
    top: 0;
    left: 0;
    width: 100%;
    padding: 2rem 8%;
    background: {glass_bg};
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 100;
}}

.logo {{
    font-size: 2rem;
    color: var(--text-color);
    font-weight: 800;
    cursor: pointer;
    transition: 0.3s ease;
}}

.logo span {{
    color: var(--main-color);
}}

.logo:hover {{
    transform: scale(1.05);
}}

.navbar a {{
    font-size: 1rem;
    color: var(--text-color);
    margin-left: 3rem;
    font-weight: 500;
    transition: 0.3s ease;
    border-bottom: 3px solid transparent;
    padding-bottom: 4px;
}}

.navbar a:hover, .navbar a.active {{
    color: var(--main-color);
    border-bottom: 3px solid var(--main-color);
}}

#menu-icon {{
    font-size: 2.5rem;
    color: var(--main-color);
    display: none;
    cursor: pointer;
}}

/* Hero Section */
.home {{
    min-height: calc(100% - 80px); /* Adjusting for header */
    padding: 4rem 8%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 4rem;
}}

.home-content {{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    max-width: 600px;
}}

.home-content h1 {{
    font-size: clamp(2.5rem, 5vw, 4.5rem);
    font-weight: 800;
    line-height: 1.2;
}}

.home-content h1 span {{
    color: var(--main-color);
}}

.home-content h3 {{
    font-size: clamp(1.5rem, 3vw, 2.2rem);
    font-weight: 600;
    color: var(--main-color);
    margin-top: 0.5rem;
}}

.home-content p {{
    font-size: 1rem;
    margin: 1.5rem 0 2rem;
    line-height: 1.6;
    color: var(--text-color);
    opacity: 0.9;
}}

/* Glowing Social Icons */
.social-icons {{
    display: flex;
    gap: 1rem;
    margin-bottom: 2.5rem;
}}

.social-icons a {{
    display: inline-flex;
    justify-content: center;
    align-items: center;
    width: 45px;
    height: 45px;
    background: transparent;
    border: 2px solid var(--main-color);
    border-radius: 50%;
    font-size: 1.5rem;
    color: var(--main-color);
    transition: 0.3s ease;
}}

.social-icons a:hover {{
    background: var(--main-color);
    color: var(--btn-text);
    box-shadow: 0 0 25px var(--main-color);
    transform: translateY(-5px);
}}

/* Buttons */
.btn-group {{
    display: flex;
    gap: 1.5rem;
}}

.btn {{
    display: inline-block;
    padding: 0.8rem 2.2rem;
    background: var(--main-color);
    color: var(--btn-text);
    border: 2px solid var(--main-color);
    border-radius: 3rem;
    font-weight: 600;
    letter-spacing: 1px;
    transition: 0.3s ease;
    box-shadow: 0 0 15px var(--main-color);
}}

.btn:hover {{
    box-shadow: 0 0 25px var(--main-color), 0 0 50px var(--main-color);
    transform: scale(1.05);
}}

.btn.transparent {{
    background: transparent;
    color: var(--main-color);
    box-shadow: none;
}}

.btn.transparent:hover {{
    background: var(--main-color);
    color: var(--btn-text);
    box-shadow: 0 0 25px var(--main-color);
}}

/* Glowing Avatar Image */
.home-img img {{
    width: 100%;
    max-width: 400px;
    aspect-ratio: 1/1;
    object-fit: cover;
    border-radius: 50%;
    box-shadow: 0 0 25px var(--main-color);
    transition: 0.4s ease-in-out;
    border: 4px solid var(--second-bg-color);
}}

.home-img img:hover {{
    box-shadow: 0 0 25px var(--main-color),
                0 0 50px var(--main-color),
                0 0 100px var(--main-color);
    transform: scale(1.02);
}}

/* Responsive Breakpoints */
@media (max-width: 900px) {{
    #menu-icon {{
        display: block;
    }}
    
    .navbar {{
        position: absolute;
        top: 100%;
        right: 0;
        width: 50%;
        padding: 1rem 3rem;
        background: var(--bg-color);
        backdrop-filter: blur(10px);
        border-left: 2px solid var(--main-color);
        border-bottom: 2px solid var(--main-color);
        border-bottom-left-radius: 2rem;
        display: none;
        flex-direction: column;
    }}

    .navbar.active {{
        display: flex;
    }}

    .navbar a {{
        display: block;
        font-size: 1.2rem;
        margin: 1.5rem 0;
        text-align: center;
    }}

    .home {{
        flex-direction: column-reverse;
        text-align: center;
        justify-content: center;
        padding-top: 2rem;
    }}

    .home-content {{
        align-items: center;
    }}

    .home-img img {{
        max-width: 300px;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Neon Portfolio Hero</title>
    <!-- BoxIcons for easy icons -->
    <link href='https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css' rel='stylesheet'>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    
    <!-- Wrapper to simulate standard browser view for agent testing -->
    <div class="preview-window">
        
        <!-- Header / Navbar -->
        <header class="header">
            <a href="#" class="logo">Dev<span>Folio</span></a>
            
            <i class='bx bx-menu' id="menu-icon"></i>
            
            <nav class="navbar">
                <a href="#" class="active">Home</a>
                <a href="#">About</a>
                <a href="#">Services</a>
                <a href="#">Portfolio</a>
                <a href="#">Contact</a>
            </nav>
        </header>

        <!-- Hero Section -->
        <section class="home">
            <div class="home-content">
                <h1>{title_text}</h1>
                <h3>A <span>Creative Problem Solver</span></h3>
                <p>{body_text}</p>
                
                <div class="social-icons">
                    <a href="#"><i class='bx bxl-github'></i></a>
                    <a href="#"><i class='bx bxl-linkedin'></i></a>
                    <a href="#"><i class='bx bxl-twitter'></i></a>
                    <a href="#"><i class='bx bxl-discord'></i></a>
                </div>

                <div class="btn-group">
                    <a href="#" class="btn">Hire Me</a>
                    <a href="#" class="btn transparent">View Work</a>
                </div>
            </div>

            <div class="home-img">
                <!-- Using a placeholder API to get a moody tech image -->
                <img src="https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=600&q=80" alt="Developer Profile">
            </div>
        </section>

    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Neon Glow Portfolio - Interactive Behavior

document.addEventListener('DOMContentLoaded', () => {{
    const menuIcon = document.querySelector('#menu-icon');
    const navbar = document.querySelector('.navbar');

    // Toggle Mobile Menu
    menuIcon.addEventListener('click', () => {{
        // Toggle the active class on the navbar to show/hide it
        navbar.classList.toggle('active');
        
        // Swap the box-icon from menu to X
        if(navbar.classList.contains('active')) {{
            menuIcon.classList.remove('bx-menu');
            menuIcon.classList.add('bx-x');
        }} else {{
            menuIcon.classList.remove('bx-x');
            menuIcon.classList.add('bx-menu');
        }}
    }});

    // Close menu when clicking a nav link (useful for mobile)
    const navLinks = document.querySelectorAll('.navbar a');
    navLinks.forEach(link => {{
        link.addEventListener('click', () => {{
            navbar.classList.remove('active');
            menuIcon.classList.remove('bx-x');
            menuIcon.classList.add('bx-menu');
            
            // Handle active state indicator
            navLinks.forEach(nav => nav.classList.remove('active'));
            link.classList.add('active');
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
