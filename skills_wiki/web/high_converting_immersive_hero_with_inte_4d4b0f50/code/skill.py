def create_component(
    output_dir: str,
    title_text: str = "It's your universe, it's time to save it",
    body_text: str = "The alliance is fighting to get rid of the old ways. Join the resistance to create a better future for your workflow.",
    color_scheme: str = "dark",
    accent_color: str = "#e63946",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the High-Converting Immersive Hero visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#0b0e14"
        text_primary = "#ffffff"
        text_secondary = "#a0aab2"
        badge_color = "rgba(255,255,255,0.4)"
        glow_color = "rgba(230, 57, 70, 0.15)" # Default red-ish glow
    else:
        bg_color = "#f4f6f8"
        text_primary = "#111827"
        text_secondary = "#4b5563"
        badge_color = "rgba(0,0,0,0.4)"
        glow_color = "rgba(230, 57, 70, 0.08)"

    # CSS
    css = f"""/* High-Converting Immersive Hero */
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --accent: {accent_color};
    --badge-color: {badge_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    /* Subtle radial glow to create depth */
    background-image: radial-gradient(circle at 75% 40%, {glow_color} 0%, transparent 50%);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow-x: hidden;
}}

.hero-wrapper {{
    width: 100%;
    max-width: var(--width);
    min-height: var(--height);
    margin: 0 auto;
    padding: 40px 24px;
    display: flex;
    flex-direction: column;
}}

/* Navigation */
.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 24px 0;
    margin-bottom: 40px;
}}

.nav-brand {{
    font-size: 1.5rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    display: flex;
    align-items: center;
    gap: 12px;
}}

.nav-brand i {{
    color: var(--accent);
    font-size: 1.8rem;
}}

.nav-links {{
    display: flex;
    gap: 32px;
    list-style: none;
}}

.nav-links a {{
    color: var(--text-primary);
    text-decoration: none;
    font-size: 0.95rem;
    font-weight: 500;
    opacity: 0.8;
    transition: opacity 0.2s;
}}

.nav-links a:hover {{
    opacity: 1;
}}

/* Main Hero Content */
.hero-container {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 60px;
    flex: 1;
}}

.hero-content {{
    flex: 1;
    max-width: 600px;
    display: flex;
    flex-direction: column;
    gap: 28px;
    z-index: 10;
}}

.hero-title {{
    font-size: 4.5rem;
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -2px;
}}

.hero-body {{
    font-size: 1.25rem;
    line-height: 1.6;
    color: var(--text-secondary);
    max-width: 90%;
}}

.hero-actions {{
    display: flex;
    align-items: center;
    gap: 24px;
    margin-top: 12px;
}}

.btn-primary {{
    background-color: var(--accent);
    color: #ffffff; /* Always white text on accent for contrast */
    text-decoration: none;
    padding: 18px 36px;
    border-radius: 4px;
    font-weight: 700;
    font-size: 1.1rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border: 2px solid transparent;
}}

.btn-primary:hover {{
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
    background-color: transparent;
    border-color: var(--accent);
    color: var(--text-primary);
}}

/* Social Proof */
.social-proof {{
    display: flex;
    align-items: center;
    gap: 16px;
    margin-top: 16px;
}}

.avatar-stack {{
    display: flex;
}}

.avatar {{
    width: 44px;
    height: 44px;
    border-radius: 50%;
    border: 3px solid var(--bg);
    margin-left: -16px;
    object-fit: cover;
    background-color: #333;
}}

.avatar:first-child {{
    margin-left: 0;
}}

.social-text {{
    font-size: 0.9rem;
    color: var(--text-secondary);
    font-weight: 500;
}}

/* Trust Badges */
.trust-badges-container {{
    margin-top: 48px;
    display: flex;
    flex-direction: column;
    gap: 16px;
}}

.trust-label {{
    font-size: 0.85rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
}}

.badges-row {{
    display: flex;
    gap: 32px;
    align-items: center;
}}

.badges-row i {{
    font-size: 2rem;
    color: var(--badge-color);
    transition: color 0.3s ease;
}}

.badges-row i:hover {{
    color: var(--text-primary);
}}

/* Hero Visual (Right Side) */
.hero-visual {{
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
}}

.floating-object {{
    width: 100%;
    max-width: 650px;
    animation: float 6s ease-in-out infinite;
    filter: drop-shadow(0 30px 40px rgba(0,0,0,0.4));
}}

@keyframes float {{
    0% {{ transform: translateY(0px) rotate(0deg); }}
    50% {{ transform: translateY(-20px) rotate(1.5deg); }}
    100% {{ transform: translateY(0px) rotate(0deg); }}
}}

/* Responsive Design */
@media (max-width: 968px) {{
    .hero-container {{
        flex-direction: column-reverse;
        text-align: center;
        padding-top: 40px;
    }}
    .hero-content {{
        align-items: center;
    }}
    .hero-body {{
        max-width: 100%;
    }}
    .hero-title {{
        font-size: 3.5rem;
    }}
    .badges-row {{
        justify-content: center;
    }}
}}
"""

    # HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hero Component</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="hero-wrapper">
        
        <!-- Navigation -->
        <nav class="navbar">
            <div class="nav-brand">
                <i class="fa-solid fa-meteor"></i> ALLIANCE
            </div>
            <ul class="nav-links">
                <li><a href="#">Our Mission</a></li>
                <li><a href="#">Fleet</a></li>
                <li><a href="#">Donate</a></li>
            </ul>
        </nav>

        <!-- Main Hero -->
        <main class="hero-container">
            
            <!-- Left Column: Copy & Conversion -->
            <div class="hero-content">
                <h1 class="hero-title">{title_text}</h1>
                <p class="hero-body">{body_text}</p>
                
                <div class="hero-actions">
                    <a href="#" class="btn-primary">Join Now For Free</a>
                </div>

                <!-- Social Proof Element -->
                <div class="social-proof">
                    <div class="avatar-stack">
                        <img src="https://i.pravatar.cc/100?img=11" alt="Member" class="avatar">
                        <img src="https://i.pravatar.cc/100?img=33" alt="Member" class="avatar">
                        <img src="https://i.pravatar.cc/100?img=68" alt="Member" class="avatar">
                        <img src="https://i.pravatar.cc/100?img=47" alt="Member" class="avatar">
                    </div>
                    <span class="social-text"><strong>Obi Wan</strong> and 4,000 others have already joined</span>
                </div>

                <!-- Trust Badges -->
                <div class="trust-badges-container">
                    <span class="trust-label">As seen on:</span>
                    <div class="badges-row">
                        <i class="fa-brands fa-apple" title="Apple"></i>
                        <i class="fa-brands fa-microsoft" title="Microsoft"></i>
                        <i class="fa-brands fa-amazon" title="Amazon"></i>
                        <i class="fa-brands fa-google" title="Google"></i>
                        <i class="fa-brands fa-figma" title="Figma"></i>
                    </div>
                </div>
            </div>

            <!-- Right Column: Visual -->
            <div class="hero-visual">
                <!-- An abstract SVG replacing the complex spacecraft, ensuring self-contained reliable rendering while maintaining the high-tech/sci-fi vibe -->
                <svg class="floating-object" viewBox="0 0 400 400" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="200" cy="200" r="160" fill="url(#paint0_linear)" fill-opacity="0.1"/>
                    <path d="M110 200L290 100V300L110 200Z" fill="url(#paint1_linear)"/>
                    <path d="M150 200L270 140V260L150 200Z" fill="var(--accent)" opacity="0.8"/>
                    <circle cx="200" cy="200" r="40" fill="var(--bg)"/>
                    <circle cx="200" cy="200" r="20" fill="var(--accent)"/>
                    
                    <defs>
                        <linearGradient id="paint0_linear" x1="40" y1="40" x2="360" y2="360" gradientUnits="userSpaceOnUse">
                            <stop stop-color="var(--text-primary)"/>
                            <stop offset="1" stop-color="var(--text-primary)" stop-opacity="0"/>
                        </linearGradient>
                        <linearGradient id="paint1_linear" x1="110" y1="100" x2="290" y2="300" gradientUnits="userSpaceOnUse">
                            <stop stop-color="var(--text-secondary)"/>
                            <stop offset="1" stop-color="var(--bg)"/>
                        </linearGradient>
                    </defs>
                </svg>
            </div>

        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # JS (No complex JS needed, adding a simple observer for entry animation to enhance the feel)
    js = """// Optional: Add subtle entry animations on load
document.addEventListener('DOMContentLoaded', () => {
    const contentElems = document.querySelectorAll('.hero-title, .hero-body, .hero-actions, .social-proof, .trust-badges-container');
    
    contentElems.forEach((elem, index) => {
        elem.style.opacity = '0';
        elem.style.transform = 'translateY(20px)';
        elem.style.transition = `opacity 0.6s ease-out, transform 0.6s ease-out`;
        elem.style.transitionDelay = `${index * 0.15}s`;
        
        // Trigger reflow
        void elem.offsetWidth; 
        
        setTimeout(() => {
            elem.style.opacity = '1';
            elem.style.transform = 'translateY(0)';
        }, 100);
    });
});
"""

    # Write files
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
