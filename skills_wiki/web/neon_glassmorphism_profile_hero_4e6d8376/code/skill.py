def create_component(
    output_dir: str,
    title_text: str = "Hi, It's John Doe",
    body_text: str = "I'm a Web Developer. I specialize in building responsive, interactive, and highly performant web applications with modern design aesthetics.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#ea580c",     # Base neon accent (e.g., Orange)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Neon Glassmorphism Profile Hero.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os
    import re

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#080808"
        bg_color_rgb = "0, 0, 0"
        text_color = "#ffffff"
    else:
        bg_color = "#f4f4f9"
        bg_color_rgb = "255, 255, 255"
        text_color = "#1a1a1a"

    # Minimal logic to generate a complementary gradient color based on the accent
    # For a perfect reproduction, we usually transition from the accent to a lighter/yellowish tone.
    # We will use the provided accent and a hardcoded bright yellow for the gradient to mimic the tutorial's fire/neon vibe.
    gradient_secondary = "#fffd15" if color_scheme == "dark" else "#ffb300"

    # === CSS ===
    css = f"""/* Neon Glassmorphism Hero — generated component */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;800&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    text-decoration: none;
    list-style: none;
    scroll-behavior: smooth;
}}

:root {{
    --bg-color: {bg_color};
    --bg-color-rgb: {bg_color_rgb};
    --text-color: {text_color};
    --main-color: {accent_color};
    --gradient-sec: {gradient_secondary};
    --container-width: {width_px}px;
    --container-height: {height_px}px;
}}

body {{
    font-family: 'Poppins', sans-serif;
    background: var(--bg-color);
    color: var(--text-color);
    overflow-x: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}}

.wrapper {{
    width: 100%;
    max-width: var(--container-width);
    min-height: var(--container-height);
    position: relative;
    background: var(--bg-color);
    box-shadow: 0 0 50px rgba(0,0,0,0.5);
    overflow: hidden;
}}

/* Header & Glassmorphism */
.header {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    padding: 2rem 10%;
    background: rgba(var(--bg-color-rgb), 0.3);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 1000;
}}

.logo {{
    font-size: 2rem;
    color: var(--text-color);
    font-weight: 800;
    cursor: pointer;
    transition: 0.3s ease;
}}

.logo:hover {{
    transform: scale(1.05);
}}

.logo span {{
    background: linear-gradient(270deg, var(--main-color) 10%, var(--gradient-sec) 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}}

.navbar a {{
    font-size: 1.1rem;
    color: var(--text-color);
    margin-left: 2.5rem;
    font-weight: 500;
    transition: 0.3s ease;
    border-bottom: 3px solid transparent;
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

.gradient-btn {{
    display: inline-block;
    padding: 0.8rem 2rem;
    background: var(--main-color);
    color: #fff;
    border-radius: 3rem;
    font-size: 1rem;
    font-weight: 600;
    border: 2px solid transparent;
    transition: 0.3s ease-in-out;
    cursor: pointer;
    box-shadow: 0 0 15px var(--main-color);
}}

.gradient-btn:hover {{
    transform: scale(1.05);
    box-shadow: 0 0 30px var(--main-color);
}}

/* Hero Section */
.home {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10rem 10% 4rem;
    min-height: 100%;
    gap: 3rem;
}}

.home-content {{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    max-width: 600px;
}}

.home-content h1 {{
    font-size: 4.5rem;
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 1rem;
}}

.home-content h1 span {{
    background: linear-gradient(270deg, var(--main-color) 10%, var(--gradient-sec) 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}}

.home-content h3 {{
    font-size: 2.5rem;
    margin-bottom: 1.5rem;
}}

.home-content h3 span {{
    color: var(--main-color);
}}

.home-content p {{
    font-size: 1.1rem;
    line-height: 1.6;
    margin-bottom: 2rem;
    color: rgba(var(--text-color), 0.8);
}}

/* Social Icons */
.social-icons {{
    display: flex;
    gap: 1rem;
    margin-bottom: 2.5rem;
}}

.social-icons a {{
    display: inline-flex;
    justify-content: center;
    align-items: center;
    width: 3.5rem;
    height: 3.5rem;
    background: transparent;
    border: 2px solid var(--main-color);
    border-radius: 50%;
    font-size: 1.8rem;
    color: var(--main-color);
    transition: 0.3s ease-in-out;
}}

.social-icons a:hover {{
    background: var(--main-color);
    color: var(--bg-color);
    transform: scale(1.1) translateY(-5px);
    box-shadow: 0 0 20px var(--main-color);
}}

/* Hero Image & Glow Effect */
.home-img img {{
    width: 25vw;
    max-width: 450px;
    min-width: 280px;
    border-radius: 50%;
    box-shadow: 0 0 25px var(--main-color);
    transition: 0.4s ease-in-out;
    object-fit: cover;
    aspect-ratio: 1/1;
}}

.home-img img:hover {{
    box-shadow: 0 0 40px var(--main-color), 0 0 80px var(--main-color);
}}

/* Responsive Breakpoints */
@media (max-width: 991px) {{
    .home {{
        flex-direction: column-reverse;
        justify-content: center;
        text-align: center;
        padding-top: 8rem;
    }}
    .home-content {{
        align-items: center;
    }}
    .home-img img {{
        width: 60vw;
        margin-bottom: 2rem;
    }}
}}

@media (max-width: 768px) {{
    .header {{
        padding: 1.5rem 5%;
    }}
    #menu-icon {{
        display: block;
    }}
    .navbar {{
        position: absolute;
        top: 100%;
        left: 0;
        width: 100%;
        padding: 1rem 5%;
        background: rgba(var(--bg-color-rgb), 0.95);
        backdrop-filter: blur(15px);
        display: none;
        flex-direction: column;
        text-align: left;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
    }}
    .navbar.active {{
        display: flex;
    }}
    .navbar a {{
        margin: 1rem 0;
        display: block;
        font-size: 1.2rem;
    }}
    .gradient-btn.header-btn {{
        display: none; /* Hide button on mobile header to save space */
    }}
    .home-content h1 {{ font-size: 3.5rem; }}
    .home-content h3 {{ font-size: 2rem; }}
}}
"""

    # Parse Title for <span> injection
    # Assuming user inputs something like "Hi, It's John" -> we want "John" to be styled
    title_parts = title_text.rsplit(' ', 1)
    if len(title_parts) > 1:
        formatted_title = f"{title_parts[0]} <span>{title_parts[1]}</span>"
    else:
        formatted_title = f"<span>{title_text}</span>"

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Neon Profile Hero</title>
    <!-- BoxIcons for social and menu icons -->
    <link href='https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css' rel='stylesheet'>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="wrapper">
        <header class="header">
            <a href="#" class="logo">Dev<span>Folio</span></a>
            <i class='bx bx-menu' id="menu-icon"></i>
            <nav class="navbar">
                <a href="#home" class="active">Home</a>
                <a href="#about">About</a>
                <a href="#projects">Projects</a>
                <a href="#contact">Contact</a>
            </nav>
            <button class="gradient-btn header-btn">Hire Me</button>
        </header>

        <section class="home" id="home">
            <div class="home-content">
                <h1>{formatted_title}</h1>
                <h3>A Creative <span>Professional</span></h3>
                <p>{body_text}</p>
                
                <div class="social-icons">
                    <a href="#"><i class='bx bxl-github'></i></a>
                    <a href="#"><i class='bx bxl-linkedin'></i></a>
                    <a href="#"><i class='bx bxl-twitter'></i></a>
                    <a href="#"><i class='bx bxl-dribbble'></i></a>
                </div>

                <div class="btn-group">
                    <button class="gradient-btn">View Work</button>
                </div>
            </div>

            <div class="home-img">
                <!-- Using a high-quality placeholder for immediate visual verification -->
                <img src="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1000&auto=format&fit=crop" alt="Profile Avatar">
            </div>
        </section>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Neon Glassmorphism Profile - Mobile Menu Toggle
document.addEventListener('DOMContentLoaded', () => {{
    const menuIcon = document.querySelector('#menu-icon');
    const navbar = document.querySelector('.navbar');

    menuIcon.addEventListener('click', () => {{
        // Toggle the icon from hamburger to 'X'
        menuIcon.classList.toggle('bx-x');
        // Reveal the navigation menu
        navbar.classList.toggle('active');
    }});

    // Close menu when a link is clicked
    const navLinks = document.querySelectorAll('.navbar a');
    navLinks.forEach(link => {{
        link.addEventListener('click', () => {{
            menuIcon.classList.remove('bx-x');
            navbar.classList.remove('active');
            
            // Handle active state indicator
            navLinks.forEach(l => l.classList.remove('active'));
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
