def create_component(
    output_dir: str,
    title_text: str = "It's your universe, it's time to save it",
    body_text: str = "The alliance is fighting to get rid of the empire. Join the resistance to create a better future for your children.",
    color_scheme: str = "dark",
    accent_color: str = "#E63946", # Rebel Red
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Trust-Optimized Hero Section.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        text_color = "#ffffff"
        text_muted = "#a0aabf"
        # Left-to-right gradient: dark opaque to transparent
        bg_gradient = "linear-gradient(90deg, rgba(13, 17, 28, 0.95) 0%, rgba(13, 17, 28, 0.8) 40%, rgba(13, 17, 28, 0) 100%)"
        nav_text = "#ffffff"
        trust_border = "rgba(255, 255, 255, 0.1)"
    else:
        text_color = "#111827"
        text_muted = "#4b5563"
        # Left-to-right gradient: light opaque to transparent
        bg_gradient = "linear-gradient(90deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 255, 255, 0.85) 40%, rgba(255, 255, 255, 0) 100%)"
        nav_text = "#111827"
        trust_border = "rgba(0, 0, 0, 0.1)"

    # CSS Content
    css = f"""/* Trust-Optimized Hero Section */
:root {{
    --text-main: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --bg-gradient: {bg_gradient};
    --nav-text: {nav_text};
    --trust-border: {trust_border};
    --comp-width: {width_px}px;
    --comp-height: {height_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: #000;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

/* Main Component Container */
.hero-wrapper {{
    width: var(--comp-width);
    height: var(--comp-height);
    max-width: 100vw;
    position: relative;
    overflow: hidden;
    background-color: #1a1a1a;
    /* Composite background: Gradient over Image */
    background-image: 
        var(--bg-gradient),
        url('https://images.unsplash.com/photo-1614730321146-b6fa6a46bcb4?q=80&w=2000&auto=format&fit=crop');
    background-size: cover;
    background-position: right center;
    color: var(--text-main);
    display: flex;
    flex-direction: column;
}}

/* Navigation */
.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2rem 4rem;
    z-index: 10;
}}

.logo {{
    font-size: 1.5rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

.logo-icon {{
    width: 24px;
    height: 24px;
    background-color: var(--accent);
    border-radius: 50%;
    display: inline-block;
}}

.nav-links {{
    display: flex;
    list-style: none;
    gap: 2.5rem;
}}

.nav-links a {{
    color: var(--nav-text);
    text-decoration: none;
    font-size: 0.95rem;
    font-weight: 500;
    opacity: 0.8;
    transition: opacity 0.2s ease;
}}

.nav-links a:hover {{
    opacity: 1;
}}

.nav-cta {{
    padding: 0.6rem 1.5rem;
    border: 1px solid var(--nav-text);
    border-radius: 4px;
    font-weight: 600;
}}

.nav-cta:hover {{
    background-color: var(--nav-text);
    color: var(--text-main) === '#ffffff' ? '#000' : '#fff';
}}

/* Main Content Area */
.hero-content {{
    flex: 1;
    display: flex;
    align-items: center;
    padding: 0 4rem;
    z-index: 10;
}}

.content-block {{
    max-width: 650px;
    animation: fadeUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    opacity: 0;
    transform: translateY(20px);
}}

.title {{
    font-size: clamp(2.5rem, 4vw, 4rem);
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 1.5rem;
    letter-spacing: -1px;
}}

.body-text {{
    font-size: 1.125rem;
    line-height: 1.6;
    color: var(--text-muted);
    margin-bottom: 2.5rem;
    max-width: 90%;
}}

/* CTA Section */
.cta-group {{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
}}

.primary-cta {{
    display: inline-block;
    background-color: var(--accent);
    color: #ffffff;
    text-decoration: none;
    font-size: 1rem;
    font-weight: 700;
    padding: 1rem 2.5rem;
    border-radius: 4px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
}}

.primary-cta:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    filter: brightness(1.1);
}}

/* Social Proof */
.social-proof {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-top: 0.5rem;
}}

.avatars {{
    display: flex;
}}

.avatar {{
    width: 28px;
    height: 28px;
    border-radius: 50%;
    border: 2px solid var(--bg-gradient); /* matches roughly */
    background-color: #333;
    margin-left: -8px;
    background-size: cover;
}}
.avatar:first-child {{ margin-left: 0; background-image: url('https://i.pravatar.cc/100?img=11'); }}
.avatar:nth-child(2) {{ background-image: url('https://i.pravatar.cc/100?img=12'); }}
.avatar:nth-child(3) {{ background-image: url('https://i.pravatar.cc/100?img=13'); }}

.social-text {{
    font-size: 0.85rem;
    color: var(--text-muted);
}}
.social-text strong {{
    color: var(--text-main);
}}

/* Trust Bar (Bottom) */
.trust-bar {{
    display: flex;
    align-items: center;
    gap: 2rem;
    padding: 2rem 4rem;
    border-top: 1px solid var(--trust-border);
    z-index: 10;
    animation: fadeIn 1s ease 0.5s forwards;
    opacity: 0;
}}

.trust-label {{
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--text-muted);
    font-weight: 600;
}}

.trust-logos {{
    display: flex;
    gap: 2.5rem;
    align-items: center;
    opacity: 0.7;
    filter: grayscale(100%);
}}

.logo-fake-1 {{ font-family: 'Times New Roman', serif; font-weight: bold; font-size: 1.2rem; }}
.logo-fake-2 {{ font-family: Arial, sans-serif; font-weight: 900; font-size: 1.1rem; letter-spacing: -1px; }}
.logo-fake-3 {{ font-family: 'Courier New', monospace; font-weight: bold; font-size: 1.3rem; }}

/* Animations */
@keyframes fadeUp {{
    0% {{ opacity: 0; transform: translateY(30px); }}
    100% {{ opacity: 1; transform: translateY(0); }}
}}
@keyframes fadeIn {{
    0% {{ opacity: 0; }}
    100% {{ opacity: 1; }}
}}
"""

    # HTML Content
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

    <section class="hero-wrapper">
        
        <!-- Top Navigation -->
        <nav class="navbar">
            <div class="logo">
                <span class="logo-icon"></span>
                Alliance
            </div>
            <ul class="nav-links">
                <li><a href="#">Our Mission</a></li>
                <li><a href="#">Resources</a></li>
                <li><a href="#">Donations</a></li>
            </ul>
            <a href="#" class="nav-links nav-cta">Log In</a>
        </nav>

        <!-- Main Content -->
        <div class="hero-content">
            <div class="content-block">
                <h1 class="title">{title_text}</h1>
                <p class="body-text">{body_text}</p>
                
                <div class="cta-group">
                    <a href="#" class="primary-cta">Join Now For Free</a>
                    
                    <div class="social-proof">
                        <div class="avatars">
                            <div class="avatar"></div>
                            <div class="avatar"></div>
                            <div class="avatar"></div>
                        </div>
                        <p class="social-text"><strong>Obi Wan</strong> and 4,000 others have already joined</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Bottom Trust Indicators -->
        <div class="trust-bar">
            <p class="trust-label">As seen on:</p>
            <div class="trust-logos">
                <span class="logo-fake-1">Forbes</span>
                <span class="logo-fake-2">TECHCRUNCH</span>
                <span class="logo-fake-3">WIRED</span>
            </div>
        </div>

    </section>

    <script src="script.js"></script>
</body>
</html>"""

    # JavaScript Content
    js = """// Optional: Add simple parallax effect to background on mousemove
document.addEventListener('DOMContentLoaded', () => {
    const heroWrapper = document.querySelector('.hero-wrapper');
    
    heroWrapper.addEventListener('mousemove', (e) => {
        const { clientX, clientY } = e;
        const xPos = (clientX / window.innerWidth - 0.5) * 10; // Max 10px shift
        const yPos = (clientY / window.innerHeight - 0.5) * 10;
        
        // Slightly shift background position for depth
        heroWrapper.style.backgroundPosition = `calc(100% + ${xPos}px) calc(50% + ${yPos}px)`;
    });
    
    // Reset on mouse leave
    heroWrapper.addEventListener('mouseleave', () => {
        heroWrapper.style.backgroundPosition = 'right center';
        heroWrapper.style.transition = 'background-position 0.5s ease';
    });
    
    heroWrapper.addEventListener('mouseenter', () => {
        heroWrapper.style.transition = 'none';
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
