def create_component(
    output_dir: str,
    title_text: str = "ActiveLink.",
    body_text: str = "Welcome to our responsive single-page platform. Scroll down to explore our services and portfolio.",
    color_scheme: str = "dark",
    accent_color: str = "#00efff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Scroll-Spy Navigation Bar effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#1f242d"
        alt_bg_color = "#323946"
        header_bg = "#11141a"
        text_color = "#ffffff"
        nav_text = "#ffffff"
    else:
        bg_color = "#f0f2f5"
        alt_bg_color = "#e4e6eb"
        header_bg = "#ffffff"
        text_color = "#1a1a1a"
        nav_text = "#333333"

    # === CSS ===
    css = f"""/* Scroll-Spy Navigation Component */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --alt-bg: {alt_bg_color};
    --header-bg: {header_bg};
    --text: {text_color};
    --nav-text: {nav_text};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Poppins', sans-serif;
    background: #000;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

/* Constrained container for reproducible isolation */
.scroll-container {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    overflow-y: auto;
    overflow-x: hidden;
    position: relative;
    background: var(--bg);
    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
}}

/* Sticky Header */
header {{
    position: sticky;
    top: 0;
    left: 0;
    width: 100%;
    padding: 25px 8%;
    background: var(--header-bg);
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 100;
}}

.logo {{
    font-size: 28px;
    color: var(--nav-text);
    text-decoration: none;
    font-weight: 700;
    letter-spacing: -0.5px;
}}

.nav-links a {{
    font-size: 18px;
    color: var(--nav-text);
    text-decoration: none;
    font-weight: 500;
    margin-left: 35px;
    transition: color 0.3s ease;
}}

.nav-links a:hover,
.nav-links a.active {{
    color: var(--accent);
}}

/* Full-height Content Sections */
section {{
    min-height: var(--height);
    display: flex;
    justify-content: center;
    align-items: center;
    background: var(--bg);
    padding: 100px 8%;
}}

section:nth-of-type(even) {{
    background: var(--alt-bg);
}}

.section-content {{
    text-align: center;
    max-width: 800px;
}}

section h2 {{
    font-size: clamp(60px, 8vw, 100px);
    font-weight: 700;
    color: var(--text);
    margin-bottom: 20px;
}}

section p {{
    font-size: 18px;
    line-height: 1.6;
    color: var(--text);
    opacity: 0.8;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text} Navigation</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <div class="scroll-container">
        <header>
            <a href="#home" class="logo">{title_text}</a>
            <nav class="nav-links">
                <a href="#home" class="active">Home</a>
                <a href="#about">About</a>
                <a href="#services">Services</a>
                <a href="#portfolio">Portfolio</a>
                <a href="#contact">Contact</a>
            </nav>
        </header>

        <section id="home">
            <div class="section-content">
                <h2>Home</h2>
                <p>{body_text}</p>
            </div>
        </section>
        
        <section id="about">
            <div class="section-content">
                <h2>About</h2>
            </div>
        </section>
        
        <section id="services">
            <div class="section-content">
                <h2>Services</h2>
            </div>
        </section>
        
        <section id="portfolio">
            <div class="section-content">
                <h2>Portfolio</h2>
            </div>
        </section>
        
        <section id="contact">
            <div class="section-content">
                <h2>Contact</h2>
            </div>
        </section>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""document.addEventListener('DOMContentLoaded', () => {{
    const container = document.querySelector('.scroll-container');
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('.nav-links a');
    const header = document.querySelector('header');

    // 1. Hande clicks for smooth scrolling inside the constrained container
    navLinks.forEach(link => {{
        link.addEventListener('click', (e) => {{
            e.preventDefault();
            const targetId = link.getAttribute('href').substring(1);
            const targetSection = document.getElementById(targetId);
            
            if (targetSection) {{
                const headerHeight = header.offsetHeight;
                container.scrollTo({{
                    // Subtract header height so content isn't hidden under the sticky nav
                    top: targetSection.offsetTop - headerHeight,
                    behavior: 'smooth'
                }});
            }}
        }});
    }});

    // 2. Scroll Spy Logic
    container.addEventListener('scroll', () => {{
        let top = container.scrollTop;
        const headerHeight = header.offsetHeight;
        
        sections.forEach(sec => {{
            // Calculate effective position relative to scroll container
            let offset = sec.offsetTop - headerHeight - 150; // 150px buffer to trigger slightly early
            let height = sec.offsetHeight;
            let id = sec.getAttribute('id');

            // Check if current scroll position is within the bounds of this section
            if (top >= offset && top < offset + height) {{
                
                // Clear active state from all links
                navLinks.forEach(link => {{
                    link.classList.remove('active');
                }});
                
                // Add active state to corresponding link
                let activeLink = document.querySelector(`.nav-links a[href="#${{id}}"]`);
                if (activeLink) {{
                    activeLink.classList.add('active');
                }}
            }}
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
