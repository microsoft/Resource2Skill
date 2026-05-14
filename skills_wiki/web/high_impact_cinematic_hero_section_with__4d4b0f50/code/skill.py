def create_component(
    output_dir: str,
    title_text: str = "It's your universe, it's time to save it",
    body_text: str = "The Rebel alliance is fighting to get rid of the evil empire. Join the resistance to create a better future for your children.",
    color_scheme: str = "dark",
    accent_color: str = "#d00000",
    width_px: int = 1440,
    height_px: int = 900,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Cinematic Hero with Social Proof visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#050608"
        text_primary = "#ffffff"
        text_secondary = "#a0aab2"
        gradient_start = "rgba(5, 6, 8, 0.95)"
        gradient_end = "rgba(5, 6, 8, 0.2)"
        logo_filter = "grayscale(100%) brightness(200%) opacity(0.6)"
        logo_hover_filter = "grayscale(0%) brightness(100%) opacity(1)"
        bg_image_url = "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?q=80&w=2048&auto=format&fit=crop" # Sci-fi/Space aesthetic
    else:
        bg_color = "#ffffff"
        text_primary = "#111827"
        text_secondary = "#4b5563"
        gradient_start = "rgba(255, 255, 255, 0.95)"
        gradient_end = "rgba(255, 255, 255, 0.2)"
        logo_filter = "grayscale(100%) brightness(0) opacity(0.5)"
        logo_hover_filter = "grayscale(0%) brightness(1) opacity(1)"
        bg_image_url = "https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=2048&auto=format&fit=crop" # Clean tech aesthetic

    css = f"""/* Cinematic Hero Component */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;800&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --accent-color: {accent_color};
    --gradient-start: {gradient_start};
    --gradient-end: {gradient_end};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-primary);
    overflow-x: hidden;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}}

.hero-wrapper {{
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    min-height: 700px;
    position: relative;
    overflow: hidden;
    background-color: var(--bg-color);
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}}

/* Background Image & Gradient Mask */
.hero-bg {{
    position: absolute;
    inset: 0;
    background-image: url('{bg_image_url}');
    background-size: cover;
    background-position: center right;
    z-index: 0;
}}

.hero-gradient {{
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg, var(--gradient-start) 0%, var(--gradient-start) 30%, var(--gradient-end) 100%);
    z-index: 1;
}}

/* Header / Nav */
header {{
    position: relative;
    z-index: 10;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2rem 5%;
}}

.logo {{
    font-size: 1.5rem;
    font-weight: 800;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    cursor: pointer;
}}

.logo svg {{
    width: 32px;
    height: 32px;
    fill: var(--accent-color);
}}

nav ul {{
    display: flex;
    list-style: none;
    gap: 2.5rem;
}}

nav a {{
    color: var(--text-primary);
    text-decoration: none;
    font-weight: 500;
    font-size: 0.95rem;
    transition: opacity 0.2s;
}}

nav a:hover {{
    opacity: 0.7;
}}

.nav-cta {{
    padding: 0.5rem 1.25rem;
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-radius: 4px;
    transition: border-color 0.2s;
}}

.nav-cta:hover {{
    border-color: var(--text-primary);
}}

/* Main Hero Content */
.hero-content {{
    position: relative;
    z-index: 10;
    padding: 4rem 5%;
    max-width: 650px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    height: calc(100% - 100px); /* offset header */
}}

h1 {{
    font-size: clamp(3rem, 5vw, 4.5rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.03em;
    margin-bottom: 1.5rem;
    opacity: 0;
    transform: translateY(20px);
}}

.body-text {{
    font-size: 1.125rem;
    line-height: 1.6;
    color: var(--text-secondary);
    margin-bottom: 2.5rem;
    max-width: 500px;
    opacity: 0;
    transform: translateY(20px);
}}

/* Call to Action Group */
.cta-group {{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
    margin-bottom: 3rem;
    opacity: 0;
    transform: translateY(20px);
}}

.btn-primary {{
    background-color: var(--accent-color);
    color: #ffffff;
    border: none;
    padding: 1.25rem 2.5rem;
    font-size: 1.125rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    border-radius: 4px;
    cursor: pointer;
    transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.2s;
    box-shadow: 0 4px 14px rgba(208, 0, 0, 0.3);
}}

.btn-primary:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(208, 0, 0, 0.4);
}}

.cta-subtext {{
    font-size: 0.875rem;
    color: var(--text-secondary);
    font-weight: 500;
}}

/* Social Proof (Avatars) */
.social-proof {{
    display: flex;
    align-items: center;
    gap: 1rem;
    opacity: 0;
    transform: translateY(20px);
}}

.avatars {{
    display: flex;
}}

.avatar {{
    width: 44px;
    height: 44px;
    border-radius: 50%;
    border: 3px solid var(--bg-color);
    margin-left: -12px;
    background-color: #333;
    object-fit: cover;
}}

.avatar:first-child {{
    margin-left: 0;
}}

.social-text {{
    font-size: 0.9rem;
    font-weight: 500;
    color: var(--text-primary);
}}

.social-text span {{
    color: var(--text-secondary);
}}

/* Press Logos */
.press-section {{
    margin-top: auto;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    padding-top: 1.5rem;
    opacity: 0;
    transform: translateY(20px);
}}

.press-label {{
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-secondary);
    margin-bottom: 1rem;
    font-weight: 600;
}}

.press-logos {{
    display: flex;
    gap: 2.5rem;
    align-items: center;
}}

.press-logos svg {{
    height: 24px;
    width: auto;
    filter: {logo_filter};
    transition: filter 0.3s ease;
}}

.press-logos svg:hover {{
    filter: {logo_hover_filter};
}}

/* Animation Classes added by JS */
.animate-in {{
    animation: fadeUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}}

@keyframes fadeUp {{
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

/* Stagger delays */
h1.animate-in {{ animation-delay: 0.1s; }}
.body-text.animate-in {{ animation-delay: 0.2s; }}
.cta-group.animate-in {{ animation-delay: 0.3s; }}
.social-proof.animate-in {{ animation-delay: 0.4s; }}
.press-section.animate-in {{ animation-delay: 0.6s; }}

@media (max-width: 768px) {{
    header {{ padding: 1.5rem; }}
    nav ul {{ display: none; }} /* Hide on mobile for simplicity in this component */
    .hero-content {{ padding: 2rem; max-width: 100%; }}
    .hero-gradient {{ background: linear-gradient(to top, var(--gradient-start) 0%, var(--gradient-start) 60%, var(--gradient-end) 100%); }}
    .hero-bg {{ background-position: center top; }}
    .press-logos {{ flex-wrap: wrap; gap: 1.5rem; }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <div class="hero-wrapper">
        <div class="hero-bg"></div>
        <div class="hero-gradient"></div>
        
        <header>
            <div class="logo">
                <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 2L2 22h20L12 2zm0 3.8l7.2 14.2H4.8L12 5.8z"/></svg>
                REBEL
            </div>
            <nav>
                <ul>
                    <li><a href="#">Our Ships</a></li>
                    <li><a href="#">Mission</a></li>
                    <li><a href="#">Donations</a></li>
                    <li><a href="#" class="nav-cta">Join Now</a></li>
                </ul>
            </nav>
        </header>

        <main class="hero-content">
            <h1 class="stagger-anim">{title_text}</h1>
            <p class="body-text stagger-anim">{body_text}</p>
            
            <div class="cta-group stagger-anim">
                <button class="btn-primary">Join Now For Free</button>
            </div>

            <div class="social-proof stagger-anim">
                <div class="avatars">
                    <img src="https://i.pravatar.cc/100?img=11" alt="Member" class="avatar">
                    <img src="https://i.pravatar.cc/100?img=12" alt="Member" class="avatar">
                    <img src="https://i.pravatar.cc/100?img=33" alt="Member" class="avatar">
                    <img src="https://i.pravatar.cc/100?img=44" alt="Member" class="avatar">
                </div>
                <div class="social-text">
                    Obi Wan and <span>4,000 others</span><br>have already joined
                </div>
            </div>

            <div class="press-section stagger-anim">
                <div class="press-label">As seen on</div>
                <div class="press-logos">
                    <!-- Generic SVGs representing press logos -->
                    <svg viewBox="0 0 100 30" xmlns="http://www.w3.org/2000/svg"><text x="0" y="22" font-family="Arial" font-weight="900" font-size="24" fill="currentColor">NEWS.CO</text></svg>
                    <svg viewBox="0 0 100 30" xmlns="http://www.w3.org/2000/svg"><text x="0" y="22" font-family="Georgia" font-style="italic" font-weight="bold" font-size="22" fill="currentColor">The Daily</text></svg>
                    <svg viewBox="0 0 100 30" xmlns="http://www.w3.org/2000/svg"><text x="0" y="22" font-family="Courier New" font-weight="bold" font-size="24" fill="currentColor">TECH</text></svg>
                    <svg viewBox="0 0 100 30" xmlns="http://www.w3.org/2000/svg"><text x="0" y="22" font-family="Impact" font-size="26" fill="currentColor">GLOBE</text></svg>
                </div>
            </div>
        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>
"""

    js = """// Cinematic Hero Animation Script
document.addEventListener('DOMContentLoaded', () => {
    // Select all elements that need the stagger animation
    const animatedElements = document.querySelectorAll('.stagger-anim');
    
    // Slight delay to ensure paint is ready and make the load feel intentional
    setTimeout(() => {
        animatedElements.forEach(el => {
            el.classList.add('animate-in');
        });
    }, 150);

    // Optional: Parallax effect on background image based on mouse movement
    const wrapper = document.querySelector('.hero-wrapper');
    const bg = document.querySelector('.hero-bg');

    wrapper.addEventListener('mousemove', (e) => {
        const xPos = (e.clientX / window.innerWidth - 0.5) * 20;
        const yPos = (e.clientY / window.innerHeight - 0.5) * 20;
        
        // Move the background slightly in the opposite direction of the cursor
        bg.style.transform = `translate(${-xPos}px, ${-yPos}px) scale(1.05)`;
    });

    wrapper.addEventListener('mouseleave', () => {
        // Reset position smoothly
        bg.style.transition = 'transform 0.5s ease-out';
        bg.style.transform = 'translate(0, 0) scale(1)';
        
        // Remove transition after it completes so mousemove is snappy again
        setTimeout(() => {
            bg.style.transition = 'none';
        }, 500);
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
