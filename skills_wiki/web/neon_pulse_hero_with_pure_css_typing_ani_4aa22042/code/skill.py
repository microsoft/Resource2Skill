def create_component(
    output_dir: str,
    title_text: str = "Hi, It's Amelia",
    body_text: str = "I'm a passionate creator building digital experiences. I specialize in turning complex problems into elegant, intuitive, and highly performant web solutions.",
    roles: list = ["Frontend Designer", "Web Developer", "UI/UX Expert"],
    color_scheme: str = "dark",        
    accent_color: str = "#00ffee",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Neon Pulse Hero with Pure CSS Typing Animation.
    Writes index.html and style.css to output_dir. No JS required for core effect.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#080808"
        text_color = "#ffffff"
        text_muted = "#a0a0a0"
    else:
        bg_color = "#ffffff"
        text_color = "#111111"
        text_muted = "#555555"

    # === Dynamic CSS Keyframes for Typing Words ===
    # Distribute the roles evenly across 100% of the keyframe timeline
    keyframes_content = ""
    step = 100 / len(roles)
    for i, role in enumerate(roles):
        start = i * step
        end = (i + 1) * step - 1 
        if i == 0:
            keyframes_content += f"0%, {end:.0f}% {{ content: '{role}'; }}\n    "
        else:
            keyframes_content += f"{start:.0f}%, {end:.0f}% {{ content: '{role}'; }}\n    "
    keyframes_content += f"100% {{ content: '{roles[0]}'; }}"

    # === CSS ===
    css = f"""/* Neon Pulse Hero — generated component */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --text-muted: {text_muted};
    --main-color: {accent_color};
}}

body {{
    font-family: 'Poppins', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow-x: hidden;
}}

/* Container constraints mapped to parameters */
.component-wrapper {{
    width: 100%;
    max-width: {width_px}px;
    min-height: {height_px}px;
    display: flex;
    align-items: center;
    padding: 2rem 5%;
}}

.hero {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    gap: 4rem;
}}

/* Left Column: Text Content */
.hero-content {{
    display: flex;
    flex-direction: column;
    max-width: 600px;
}}

.hero-content h1 {{
    font-size: clamp(3rem, 5vw, 4.5rem);
    font-weight: 700;
    line-height: 1.2;
    margin-bottom: 1rem;
}}

.hero-content h1 span {{
    color: var(--main-color);
    text-shadow: 0 0 15px rgba({int(accent_color[1:3], 16)}, {int(accent_color[3:5], 16)}, {int(accent_color[5:7], 16)}, 0.4);
}}

.text-animation {{
    font-size: clamp(1.8rem, 3vw, 2.5rem);
    font-weight: 600;
    min-width: 280px;
    margin-bottom: 1.5rem;
}}

/* Pure CSS Typing Effect Magic */
.text-animation span {{
    position: relative;
    color: var(--main-color);
}}

.text-animation span::before {{
    content: '{roles[0]}';
    color: var(--main-color);
    animation: words 9s infinite;
}}

.text-animation span::after {{
    content: '';
    background-color: var(--bg-color);
    position: absolute;
    width: calc(100% + 8px);
    height: 100%;
    border-left: 3px solid var(--main-color);
    right: -8px;
    animation: cursor 0.6s infinite, typing 9s steps(14) infinite;
}}

@keyframes words {{
    {keyframes_content}
}}

@keyframes typing {{
    10%, 15%, 30%, 35%, 50%, 55%, 70%, 75%, 90%, 95% {{
        width: 0;
    }}
    5%, 20%, 25%, 40%, 45%, 60%, 65%, 80%, 85% {{
        width: calc(100% + 8px);
    }}
}}

@keyframes cursor {{
    0% {{ border-left-color: var(--main-color); }}
    50% {{ border-left-color: transparent; }}
    100% {{ border-left-color: var(--main-color); }}
}}

.hero-content p {{
    font-size: 1rem;
    color: var(--text-muted);
    line-height: 1.6;
    margin-bottom: 2.5rem;
}}

/* Interactive Elements */
.social-icons {{
    display: flex;
    gap: 1rem;
    margin-bottom: 2.5rem;
}}

.social-icons a {{
    display: inline-flex;
    justify-content: center;
    align-items: center;
    width: 2.8rem;
    height: 2.8rem;
    background: transparent;
    border: 2px solid var(--main-color);
    border-radius: 50%;
    font-size: 1.4rem;
    color: var(--main-color);
    text-decoration: none;
    transition: 0.3s ease;
}}

.social-icons a:hover {{
    background: var(--main-color);
    color: var(--bg-color);
    transform: translateY(-5px);
    box-shadow: 0 0 15px var(--main-color);
}}

.btn-group {{
    display: flex;
    gap: 1.5rem;
}}

.btn {{
    display: inline-block;
    padding: 0.8rem 2.2rem;
    background: var(--main-color);
    border: 2px solid var(--main-color);
    border-radius: 2rem;
    color: var(--bg-color);
    font-weight: 600;
    text-decoration: none;
    letter-spacing: 1px;
    transition: 0.3s ease;
}}

.btn:hover {{
    box-shadow: 0 0 25px var(--main-color);
}}

.btn.outline {{
    background: transparent;
    color: var(--main-color);
}}

.btn.outline:hover {{
    background: var(--main-color);
    color: var(--bg-color);
}}

/* Right Column: Neon Avatar */
.hero-img {{
    position: relative;
    width: clamp(250px, 32vw, 450px);
    aspect-ratio: 1 / 1;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    /* The core neon glow */
    box-shadow: 0 0 25px var(--main-color);
    transition: 0.4s ease-in-out;
    cursor: pointer;
}}

.hero-img:hover {{
    box-shadow: 0 0 50px var(--main-color),
                0 0 100px var(--main-color);
}}

.hero-img img {{
    width: 90%;
    height: 90%;
    object-fit: cover;
    border-radius: 50%;
    border: 3px solid rgba(255, 255, 255, 0.1);
}}

/* Responsive Breakpoint */
@media (max-width: 991px) {{
    .hero {{
        flex-direction: column-reverse;
        text-align: center;
        gap: 3rem;
    }}
    
    .hero-content {{
        align-items: center;
    }}
    
    .text-animation span::after {{
        right: auto; /* Fixes cursor alignment when centered */
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Neon Pulse Hero</title>
    <!-- Boxicons for Social Media Icons -->
    <link href='https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css' rel='stylesheet'>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    
    <div class="component-wrapper">
        <section class="hero">
            
            <div class="hero-content">
                <h1>{title_text}</h1>
                <h3 class="text-animation">I'm a <span></span></h3>
                <p>{body_text}</p>
                
                <div class="social-icons">
                    <a href="#"><i class='bx bxl-linkedin'></i></a>
                    <a href="#"><i class='bx bxl-github'></i></a>
                    <a href="#"><i class='bx bxl-twitter'></i></a>
                    <a href="#"><i class='bx bxl-instagram-alt'></i></a>
                </div>
                
                <div class="btn-group">
                    <a href="#" class="btn">Hire Me</a>
                    <a href="#" class="btn outline">Contact</a>
                </div>
            </div>

            <div class="hero-img">
                <!-- Using Unsplash for a high-quality portrait placeholder -->
                <img src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=800&q=80" alt="Avatar Portrait">
            </div>

        </section>
    </div>

    <!-- No JavaScript required for core functionality! -->
    <script src="script.js"></script>
</body>
</html>"""

    # === Empty JS (Skill relies purely on CSS) ===
    js = """// No JavaScript required!
// The typing animation and neon glow interactions are achieved entirely via CSS keyframes and hover states.
console.log("Neon Hero component initialized successfully.");
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
