def create_component(
    output_dir: str,
    title_text: str = "Nick Williams",
    body_text: str = "I'm thrilled to tell you a bit about myself. I have over six years of IT experience, specializing in PHP, Database Development, and open-source frameworks.",
    color_scheme: str = "dark",
    accent_color: str = "#4bd5c4",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#151b24"
        card_bg = "#212a36"
        card_border = "rgba(255, 255, 255, 0.05)"
        text_main = "#f8fafc"
        text_muted = "#94a3b8"
        sidebar_bg = "#1a222c"
        hover_bg = "rgba(255, 255, 255, 0.08)"
    else:
        bg_color = "#f1f5f9"
        card_bg = "#ffffff"
        card_border = "rgba(0, 0, 0, 0.08)"
        text_main = "#0f172a"
        text_muted = "#64748b"
        sidebar_bg = "#e2e8f0"
        hover_bg = "rgba(0, 0, 0, 0.05)"

    # === CSS ===
    css = f"""/* Bento Box vCard Dashboard */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --card-bg: {card_bg};
    --card-border: {card_border};
    --text-main: {text_main};
    --text-muted: {text_muted};
    --sidebar-bg: {sidebar_bg};
    --accent: {accent_color};
    --hover-bg: {hover_bg};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-main);
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    /* Simulated ambient background glow */
    background-image: radial-gradient(circle at 50% 0%, rgba(75, 213, 196, 0.05) 0%, transparent 50%);
}}

.app-wrapper {{
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    max-height: 95vh;
    display: flex;
    gap: 20px;
    padding: 20px;
}}

/* Sidebar Nav */
.sidebar {{
    width: 80px;
    background-color: var(--sidebar-bg);
    border-radius: 24px;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 30px 0;
    gap: 20px;
    border: 1px solid var(--card-border);
}}

.nav-item {{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
    color: var(--text-muted);
    text-decoration: none;
    font-size: 0.75rem;
    font-weight: 500;
    padding: 12px 10px;
    border-radius: 16px;
    cursor: pointer;
    transition: all 0.3s ease;
    width: 64px;
}}

.nav-item i {{
    font-size: 1.25rem;
    transition: color 0.3s ease;
}}

.nav-item:hover {{
    background-color: var(--hover-bg);
    color: var(--text-main);
}}

.nav-item.active {{
    background-color: rgba(75, 213, 196, 0.1); /* fallback opacity */
    background-color: color-mix(in srgb, var(--accent) 15%, transparent);
    color: var(--accent);
}}

/* Content Area */
.content-area {{
    flex: 1;
    position: relative;
    overflow: hidden;
}}

.section-content {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    opacity: 0;
    pointer-events: none;
    transform: translateY(10px);
    transition: opacity 0.4s ease, transform 0.4s ease;
    display: flex;
    gap: 24px;
}}

.section-content.active {{
    opacity: 1;
    pointer-events: auto;
    transform: translateY(0);
}}

/* Cards Base */
.card {{
    background-color: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 24px;
    padding: 32px;
    display: flex;
    flex-direction: column;
}}

/* Profile Col */
.profile-col {{
    flex: 0 0 320px;
    align-items: center;
    text-align: center;
}}

.avatar-wrapper {{
    width: 140px;
    height: 140px;
    border-radius: 30%; /* Squircle */
    overflow: hidden;
    margin-bottom: 20px;
    border: 4px solid var(--card-bg);
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    background-color: var(--sidebar-bg);
}}

.avatar-wrapper img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
}}

.profile-col h1 {{
    font-size: 1.5rem;
    margin-bottom: 4px;
}}

.profile-col h2 {{
    font-size: 0.9rem;
    color: var(--accent);
    font-weight: 500;
    margin-bottom: 24px;
}}

.social-links {{
    display: flex;
    gap: 12px;
    margin-bottom: auto;
}}

.social-btn {{
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: var(--hover-bg);
    color: var(--text-main);
    display: flex;
    align-items: center;
    justify-content: center;
    text-decoration: none;
    transition: all 0.3s ease;
}}

.social-btn:hover {{
    background-color: var(--accent);
    color: var(--bg-color);
}}

.action-btns {{
    width: 100%;
    display: flex;
    gap: 12px;
    margin-top: 24px;
}}

.btn {{
    flex: 1;
    padding: 12px;
    border-radius: 12px;
    border: none;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
}}

.btn-primary {{
    background-color: var(--hover-bg);
    color: var(--text-main);
}}

.btn-primary:hover {{
    background-color: var(--card-border);
}}

.btn-accent {{
    background-color: var(--accent);
    color: #000;
}}

.btn-accent:hover {{
    opacity: 0.9;
}}

/* Details Col Grid */
.details-col {{
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 24px;
}}

.bio-card h3 {{
    font-size: 1.5rem;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}}

.bio-card p {{
    color: var(--text-muted);
    line-height: 1.6;
}}

.stats-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
}}

.stat-card {{
    padding: 24px;
    align-items: flex-start;
    justify-content: center;
}}

.stat-value {{
    font-size: 2rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 4px;
}}

.stat-icon {{
    color: var(--accent);
    font-size: 1.5rem;
}}

.stat-label {{
    color: var(--text-muted);
    font-size: 0.85rem;
}}

/* Skills Area */
.skills-card h3 {{
    margin-bottom: 20px;
}}

.skills-wrapper {{
    display: flex;
    gap: 32px;
}}

.skills-icons {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    flex: 1;
}}

.skill-box {{
    background-color: var(--hover-bg);
    border: 1px solid var(--card-border);
    border-radius: 16px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 16px 12px;
    gap: 8px;
    transition: all 0.3s ease;
}}

.skill-box:hover {{
    border-color: var(--accent);
}}

.skill-box i {{
    font-size: 1.8rem;
    color: var(--accent);
}}

.skill-box span {{
    font-size: 0.75rem;
    font-weight: 600;
}}

.skills-meters {{
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 20px;
}}

/* Radial Progress */
.radial-container {{
    display: flex;
    gap: 20px;
    margin-bottom: 10px;
}}

.radial-item {{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
}}

.radial-circle {{
    width: 64px;
    height: 64px;
    border-radius: 50%;
    background: conic-gradient(var(--accent) var(--p), var(--hover-bg) 0deg);
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
}}

.radial-circle::before {{
    content: "";
    position: absolute;
    width: 52px;
    height: 52px;
    background-color: var(--card-bg);
    border-radius: 50%;
}}

.radial-circle span {{
    position: relative;
    z-index: 1;
    font-size: 0.8rem;
    font-weight: 600;
}}

.radial-label {{ font-size: 0.8rem; color: var(--text-muted); }}

/* Linear Progress */
.linear-item {{
    width: 100%;
}}

.linear-label {{
    display: flex;
    justify-content: space-between;
    font-size: 0.85rem;
    margin-bottom: 8px;
    color: var(--text-muted);
}}

.linear-bar-bg {{
    width: 100%;
    height: 6px;
    background-color: var(--hover-bg);
    border-radius: 4px;
    overflow: hidden;
}}

.linear-bar-fill {{
    height: 100%;
    background-color: var(--accent);
    border-radius: 4px;
}}

/* Responsive */
@media (max-width: 1024px) {{
    .app-wrapper {{ flex-direction: column; height: auto; max-height: none; }}
    .sidebar {{ width: 100%; flex-direction: row; justify-content: center; padding: 15px; border-radius: 16px; }}
    .nav-item {{ width: auto; padding: 10px 20px; }}
    .section-content {{ position: relative; opacity: 1; transform: none; display: none; flex-direction: column; }}
    .section-content.active {{ display: flex; }}
    .profile-col {{ flex: auto; }}
    .stats-grid {{ grid-template-columns: repeat(1, 1fr); }}
    .skills-wrapper {{ flex-direction: column; }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text} - Portfolio</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-wrapper">
        
        <!-- Sidebar Navigation -->
        <aside class="sidebar">
            <div class="nav-item active" data-target="about">
                <i class="fa-solid fa-user"></i>
                <span>ABOUT</span>
            </div>
            <div class="nav-item" data-target="resume">
                <i class="fa-solid fa-file-lines"></i>
                <span>RESUME</span>
            </div>
            <div class="nav-item" data-target="projects">
                <i class="fa-solid fa-briefcase"></i>
                <span>PROJECTS</span>
            </div>
            <div class="nav-item" data-target="contact">
                <i class="fa-solid fa-envelope"></i>
                <span>CONTACT</span>
            </div>
        </aside>

        <!-- Main Content Area -->
        <main class="content-area">
            
            <!-- About Section (Active) -->
            <section id="about" class="section-content active">
                
                <!-- Left Column: Profile -->
                <div class="card profile-col">
                    <div class="avatar-wrapper">
                        <!-- Placeholder avatar -->
                        <img src="https://i.pravatar.cc/300?img=11" alt="Profile Avatar">
                    </div>
                    <h1>{title_text}</h1>
                    <h2>Full-Stack Web Developer</h2>
                    
                    <div class="social-links">
                        <a href="#" class="social-btn"><i class="fa-brands fa-github"></i></a>
                        <a href="#" class="social-btn"><i class="fa-brands fa-twitter"></i></a>
                        <a href="#" class="social-btn"><i class="fa-brands fa-linkedin-in"></i></a>
                    </div>

                    <div class="action-btns">
                        <button class="btn btn-primary">My Resume</button>
                        <button class="btn btn-accent"><i class="fa-solid fa-paper-plane"></i> Contact Me</button>
                    </div>
                </div>

                <!-- Right Column: Details -->
                <div class="details-col">
                    
                    <!-- Bio Box -->
                    <div class="card bio-card">
                        <h3>Hey there! <span style="font-size: 1.2rem;">👋</span></h3>
                        <p>{body_text}</p>
                    </div>

                    <!-- Stats Row -->
                    <div class="stats-grid">
                        <div class="card stat-card">
                            <div class="stat-value">
                                <i class="fa-solid fa-layer-group stat-icon"></i> 2K+
                            </div>
                            <div class="stat-label">Website Designed</div>
                        </div>
                        <div class="card stat-card">
                            <div class="stat-value">
                                <i class="fa-solid fa-award stat-icon"></i> 5+
                            </div>
                            <div class="stat-label">Years of Experience</div>
                        </div>
                        <div class="card stat-card">
                            <div class="stat-value">
                                <i class="fa-solid fa-rocket stat-icon"></i> 4K
                            </div>
                            <div class="stat-label">Completed Projects</div>
                        </div>
                    </div>

                    <!-- Skills Box -->
                    <div class="card skills-card">
                        <h3>My Skills</h3>
                        <div class="skills-wrapper">
                            
                            <!-- Skill Icons Grids -->
                            <div class="skills-icons">
                                <div class="skill-box">
                                    <i class="fa-brands fa-html5"></i><span>HTML5</span>
                                </div>
                                <div class="skill-box">
                                    <i class="fa-brands fa-css3-alt"></i><span>CSS3</span>
                                </div>
                                <div class="skill-box">
                                    <i class="fa-brands fa-react"></i><span>React</span>
                                </div>
                                <div class="skill-box">
                                    <i class="fa-brands fa-python"></i><span>Python</span>
                                </div>
                            </div>

                            <!-- Skill Progress Meters -->
                            <div class="skills-meters">
                                <div class="radial-container">
                                    <div class="radial-item">
                                        <div class="radial-circle" style="--p: 65%;"><span>65%</span></div>
                                        <span class="radial-label">MySQL</span>
                                    </div>
                                    <div class="radial-item">
                                        <div class="radial-circle" style="--p: 85%;"><span>85%</span></div>
                                        <span class="radial-label">PostgreSQL</span>
                                    </div>
                                </div>

                                <div class="linear-item">
                                    <div class="linear-label"><span>Node Js</span><span>90%</span></div>
                                    <div class="linear-bar-bg"><div class="linear-bar-fill" style="width: 90%;"></div></div>
                                </div>
                            </div>

                        </div>
                    </div>

                </div>
            </section>

            <!-- Placeholder Section (Resume) -->
            <section id="resume" class="section-content">
                <div class="card" style="width:100%; display:flex; align-items:center; justify-content:center;">
                    <h2>Resume Section Content</h2>
                </div>
            </section>

            <!-- Placeholder Section (Projects) -->
            <section id="projects" class="section-content">
                <div class="card" style="width:100%; display:flex; align-items:center; justify-content:center;">
                    <h2>Projects Section Content</h2>
                </div>
            </section>

            <!-- Placeholder Section (Contact) -->
            <section id="contact" class="section-content">
                <div class="card" style="width:100%; display:flex; align-items:center; justify-content:center;">
                    <h2>Contact Section Content</h2>
                </div>
            </section>

        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Bento Box vCard Dashboard - Tab Switching Logic
document.addEventListener('DOMContentLoaded', () => {{
    const navItems = document.querySelectorAll('.nav-item');
    const sections = document.querySelectorAll('.section-content');

    navItems.forEach(item => {{
        item.addEventListener('click', () => {{
            // 1. Remove active state from all nav items and sections
            navItems.forEach(n => n.classList.remove('active'));
            sections.forEach(s => s.classList.remove('active'));

            // 2. Add active state to clicked item
            item.classList.add('active');

            // 3. Find matching section and activate it
            const targetId = item.getAttribute('data-target');
            const targetSection = document.getElementById(targetId);
            
            if (targetSection) {{
                targetSection.classList.add('active');
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
