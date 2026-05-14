def create_component(
    output_dir: str,
    title_text: str = "It's your universe, it's time to save it",
    body_text: str = "The Rebel alliance is fighting to get rid of the evil empire. Join the resistance to create a better future for your children.",
    color_scheme: str = "dark",
    accent_color: str = "#e63946", # Rebel Red
    width_px: int = 1440,
    height_px: int = 900,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Epic Dark Mode Hero with Social Proof.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Force dark theme as the tutorial is specifically about a dark "epic" space theme
    # but adapt if light is strictly requested
    if color_scheme == "light":
        bg_color = "#f0f4f8"
        text_color = "#101828"
        text_muted = "#475467"
        nav_border = "rgba(0,0,0,0.05)"
        bg_image = "none"
        logo_opacity = "0.4"
    else:
        bg_color = "#080b13"
        text_color = "#ffffff"
        text_muted = "#8b949e"
        nav_border = "rgba(255,255,255,0.05)"
        bg_image = "url('https://images.unsplash.com/photo-1506318137071-a8e063b4bec0?q=80&w=3000&auto=format&fit=crop')"
        logo_opacity = "0.5"

    css = f"""/* Epic Hero with Social Proof */
:root {{
    --bg-color: {bg_color};
    --text-primary: {text_color};
    --text-secondary: {text_muted};
    --accent-color: {accent_color};
    --nav-border: {nav_border};
    --font-heading: 'Montserrat', system-ui, sans-serif;
    --font-body: 'Inter', system-ui, sans-serif;
    --comp-width: {width_px}px;
    --comp-height: {height_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: var(--font-body);
    background-color: var(--bg-color);
    background-image: linear-gradient(to bottom, rgba(8, 11, 19, 0.8), rgba(8, 11, 19, 1)), {bg_image};
    background-size: cover;
    background-position: center;
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    /* Optional: constrain to requested dimensions for preview purposes */
    padding: 2rem;
}}

.hero-wrapper {{
    width: 100%;
    max-width: var(--comp-width);
    min-height: calc(var(--comp-height) - 4rem);
    background: radial-gradient(circle at 50% 0%, rgba(255,255,255,0.03) 0%, transparent 50%);
    border: 1px solid var(--nav-border);
    border-radius: 24px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    position: relative;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}}

/* Navigation */
.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem 3rem;
    border-bottom: 1px solid var(--nav-border);
    z-index: 10;
}}

.nav-logo {{
    font-family: var(--font-heading);
    font-weight: 800;
    font-size: 1.25rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    letter-spacing: -0.5px;
}}

.nav-logo i {{
    color: var(--accent-color);
    font-size: 1.5rem;
}}

.nav-links {{
    display: flex;
    gap: 2.5rem;
}}

.nav-links a {{
    color: var(--text-secondary);
    text-decoration: none;
    font-weight: 500;
    font-size: 0.95rem;
    transition: color 0.2s ease;
}}

.nav-links a:hover {{
    color: var(--text-primary);
}}

.btn-ghost {{
    background: transparent;
    border: 1px solid var(--nav-border);
    color: var(--text-primary);
    padding: 0.6rem 1.25rem;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
}}

.btn-ghost:hover {{
    background: rgba(255,255,255,0.05);
    border-color: rgba(255,255,255,0.2);
}}

/* Main Hero Layout */
.hero-main {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    flex: 1;
    padding: 4rem 3rem;
    gap: 4rem;
    align-items: center;
    z-index: 2;
}}

.hero-content {{
    display: flex;
    flex-direction: column;
    gap: 2rem;
    max-width: 600px;
}}

.hero-title {{
    font-family: var(--font-heading);
    font-size: clamp(3rem, 5vw, 4.5rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.03em;
    text-wrap: balance;
}}

.hero-description {{
    font-size: 1.125rem;
    line-height: 1.6;
    color: var(--text-secondary);
    max-width: 85%;
}}

/* CTA & Social Proof Area */
.hero-action-area {{
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    margin-top: 1rem;
}}

.btn-primary {{
    background: var(--accent-color);
    color: #fff;
    border: none;
    padding: 1rem 2rem;
    font-size: 1.125rem;
    font-weight: 700;
    border-radius: 8px;
    cursor: pointer;
    align-self: flex-start;
    transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.2s ease;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

.btn-primary:hover {{
    transform: translateY(-3px);
    box-shadow: 0 10px 20px -10px var(--accent-color);
}}

.social-proof {{
    display: flex;
    align-items: center;
    gap: 1rem;
}}

.avatar-group {{
    display: flex;
}}

.avatar {{
    width: 36px;
    height: 36px;
    border-radius: 50%;
    border: 3px solid var(--bg-color);
    margin-left: -12px;
    object-fit: cover;
    background-color: #333;
}}

.avatar:first-child {{
    margin-left: 0;
}}

.social-text {{
    font-size: 0.875rem;
    color: var(--text-secondary);
    font-weight: 500;
}}

.social-text strong {{
    color: var(--text-primary);
}}

/* Hero Graphic */
.hero-visual {{
    position: relative;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    perspective: 1000px;
}}

.visual-image {{
    width: 130%;
    max-width: 800px;
    /* Using mix-blend-mode to make a standard space image look like a cutout composite */
    mix-blend-mode: lighten;
    filter: drop-shadow(0 0 40px rgba(0,0,0,0.8));
    transition: transform 0.1s ease-out;
    transform-style: preserve-3d;
}}

/* Trust Logos */
.trust-strip {{
    padding: 2rem 3rem;
    border-top: 1px solid var(--nav-border);
    display: flex;
    align-items: center;
    gap: 2rem;
    background: rgba(0,0,0,0.2);
    z-index: 2;
}}

.trust-label {{
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--text-secondary);
    font-weight: 600;
    white-space: nowrap;
}}

.trust-logos {{
    display: flex;
    gap: 3rem;
    align-items: center;
    flex-wrap: wrap;
}}

.trust-logos i {{
    font-size: 2rem;
    color: #ffffff;
    opacity: {logo_opacity};
    transition: opacity 0.3s ease, transform 0.3s ease;
    cursor: default;
}}

.trust-logos i:hover {{
    opacity: 1;
    transform: translateY(-2px);
}}

/* Responsive */
@media (max-width: 968px) {{
    .hero-main {{
        grid-template-columns: 1fr;
        text-align: center;
        gap: 2rem;
        padding: 3rem 2rem;
    }}
    
    .hero-content {{
        margin: 0 auto;
        align-items: center;
    }}
    
    .hero-description {{
        max-width: 100%;
    }}
    
    .btn-primary {{
        align-self: center;
    }}
    
    .nav-links {{
        display: none;
    }}
    
    .trust-strip {{
        flex-direction: column;
        gap: 1rem;
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Montserrat:wght@700;800;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <div class="hero-wrapper">
        <!-- Navigation -->
        <nav class="navbar">
            <div class="nav-logo">
                <i class="fa-solid fa-meteor"></i>
                Alliance
            </div>
            <div class="nav-links">
                <a href="#">Our Ships</a>
                <a href="#">Mission</a>
                <a href="#">Donations</a>
            </div>
            <button class="btn-ghost">Log In</button>
        </nav>

        <!-- Main Content -->
        <main class="hero-main">
            <div class="hero-content">
                <h1 class="hero-title">{title_text}</h1>
                <p class="hero-description">{body_text}</p>
                
                <div class="hero-action-area">
                    <button class="btn-primary">Join Now For Free</button>
                    
                    <div class="social-proof">
                        <div class="avatar-group">
                            <img src="https://i.pravatar.cc/100?img=11" alt="User" class="avatar">
                            <img src="https://i.pravatar.cc/100?img=12" alt="User" class="avatar">
                            <img src="https://i.pravatar.cc/100?img=33" alt="User" class="avatar">
                            <img src="https://i.pravatar.cc/100?img=14" alt="User" class="avatar">
                        </div>
                        <div class="social-text">
                            <strong>Obi Wan</strong> and <strong>4,000 others</strong> have already joined
                        </div>
                    </div>
                </div>
            </div>

            <div class="hero-visual">
                <!-- Using an abstract space/tech placeholder that works well with screen/lighten blend modes -->
                <img src="https://images.unsplash.com/photo-1614732414444-096e5f1122a5?q=80&w=1000&auto=format&fit=crop" alt="Hero Graphic" class="visual-image" id="parallax-img">
            </div>
        </main>

        <!-- Trust Signals -->
        <div class="trust-strip">
            <span class="trust-label">As seen on</span>
            <div class="trust-logos">
                <i class="fa-brands fa-aws"></i>
                <i class="fa-brands fa-space-awesome"></i>
                <i class="fa-brands fa-reddit-alien"></i>
                <i class="fa-brands fa-galactic-senate"></i>
                <i class="fa-brands fa-rebel"></i>
            </div>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    js = """// Epic Dark Mode Hero - Interaction Logic
document.addEventListener('DOMContentLoaded', () => {
    const wrapper = document.querySelector('.hero-wrapper');
    const visualImg = document.getElementById('parallax-img');
    
    // Subtle Parallax Effect on Mouse Move to simulate depth
    if (window.matchMedia("(hover: hover)").matches) {
        wrapper.addEventListener('mousemove', (e) => {
            const rect = wrapper.getBoundingClientRect();
            
            // Calculate mouse position relative to the center of the wrapper
            const centerX = rect.left + rect.width / 2;
            const centerY = rect.top + rect.height / 2;
            
            const moveX = (e.clientX - centerX) / centerX;
            const moveY = (e.clientY - centerY) / centerY;
            
            // Apply a slight inverse translation and rotation for a 3D float effect
            const maxTranslation = 20; // pixels
            const maxRotation = 5; // degrees
            
            visualImg.style.transform = `
                translate(${-moveX * maxTranslation}px, ${-moveY * maxTranslation}px)
                rotateY(${moveX * maxRotation}deg)
                rotateX(${-moveY * maxRotation}deg)
            `;
        });
        
        // Reset position when mouse leaves
        wrapper.addEventListener('mouseleave', () => {
            visualImg.style.transform = `translate(0px, 0px) rotateY(0deg) rotateX(0deg)`;
            visualImg.style.transition = 'transform 0.5s ease-out';
        });
        
        // Remove transition during active movement for snappiness
        wrapper.addEventListener('mouseenter', () => {
            visualImg.style.transition = 'none';
        });
    }
});
"""

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
