def create_component(
    output_dir: str,
    title_text: str = "It's your universe, it's time to save it",
    body_text: str = "The Alliance is fighting to get rid of the evil empire. Join the resistance to create a better future for your children.",
    color_scheme: str = "dark",
    accent_color: str = "#e62429", # Rebel Red
    width_px: int = 1280,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Cinematic Hero Section with Social Proof.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Use a generic space/sci-fi placeholder image
    bg_image_url = "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?q=80&w=2048&auto=format&fit=crop"

    if color_scheme == "dark":
        bg_base = "#05070a"
        text_primary = "#ffffff"
        text_secondary = "rgba(255, 255, 255, 0.7)"
        overlay_gradient = f"linear-gradient(90deg, {bg_base} 10%, rgba(5,7,10,0.7) 50%, rgba(5,7,10,0.1) 100%)"
    else:
        # While the pattern is "dark cinematic", providing a light fallback
        bg_base = "#f0f2f5"
        text_primary = "#111827"
        text_secondary = "rgba(17, 24, 39, 0.7)"
        overlay_gradient = f"linear-gradient(90deg, {bg_base} 10%, rgba(240,242,245,0.8) 50%, rgba(240,242,245,0.2) 100%)"

    css = f"""/* Cinematic Hero Component */
:root {{
    --accent: {accent_color};
    --bg-base: {bg_base};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --font-heading: 'Inter', system-ui, sans-serif;
    --font-body: 'Inter', system-ui, sans-serif;
    --hero-width: {width_px}px;
    --hero-height: {height_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    background-color: #000;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    font-family: var(--font-body);
    color: var(--text-primary);
}}

/* Container to match requested dimensions */
.hero-wrapper {{
    width: 100%;
    max-width: var(--hero-width);
    height: var(--hero-height);
    position: relative;
    background-color: var(--bg-base);
    background-image: {overlay_gradient}, url('{bg_image_url}');
    background-size: cover;
    background-position: center;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
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
}}

.nav-links {{
    display: flex;
    gap: 2rem;
    list-style: none;
}}

.nav-links a {{
    color: var(--text-primary);
    text-decoration: none;
    font-size: 0.9rem;
    font-weight: 500;
    opacity: 0.8;
    transition: opacity 0.2s ease;
}}

.nav-links a:hover {{
    opacity: 1;
}}

/* Main Content Area */
.hero-main {{
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 0 4rem;
    max-width: 65%;
    z-index: 10;
}}

.hero-title {{
    font-family: var(--font-heading);
    font-size: 4rem;
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 1.5rem;
    letter-spacing: -1px;
    animation: fadeUp 0.8s ease-out forwards;
    opacity: 0;
}}

.hero-body {{
    font-size: 1.25rem;
    line-height: 1.6;
    color: var(--text-secondary);
    margin-bottom: 2.5rem;
    max-width: 80%;
    animation: fadeUp 0.8s ease-out 0.2s forwards;
    opacity: 0;
}}

/* CTA Area */
.cta-group {{
    display: flex;
    flex-direction: column;
    gap: 1rem;
    animation: fadeUp 0.8s ease-out 0.4s forwards;
    opacity: 0;
}}

.btn-primary {{
    background-color: var(--accent);
    color: #fff;
    border: none;
    padding: 1rem 2rem;
    font-size: 1rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    cursor: pointer;
    align-self: flex-start;
    transition: transform 0.2s ease, filter 0.2s ease;
    border-radius: 2px;
}}

.btn-primary:hover {{
    transform: translateY(-2px);
    filter: brightness(1.1);
}}

.social-proof-micro {{
    display: flex;
    align-items: center;
    gap: 1rem;
    font-size: 0.85rem;
    color: var(--text-secondary);
}}

.avatars {{
    display: flex;
}}

.avatar {{
    width: 32px;
    height: 32px;
    border-radius: 50%;
    border: 2px solid var(--bg-base);
    background-color: #333;
    margin-left: -10px;
}}
.avatar:first-child {{ margin-left: 0; }}

/* Footer / As Seen On */
.hero-footer {{
    display: flex;
    align-items: center;
    padding: 2rem 4rem;
    background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);
    z-index: 10;
    border-top: 1px solid rgba(255,255,255,0.05);
}}

.as-seen-text {{
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--text-secondary);
    margin-right: 2rem;
    white-space: nowrap;
}}

.logos-container {{
    display: flex;
    gap: 3rem;
    align-items: center;
    opacity: 0.5;
    filter: grayscale(100%);
    transition: opacity 0.3s ease, filter 0.3s ease;
}}

.logos-container:hover {{
    opacity: 0.8;
    filter: grayscale(50%);
}}

.brand-placeholder {{
    font-weight: 800;
    font-size: 1.2rem;
    color: var(--text-primary);
    letter-spacing: -0.5px;
}}

@keyframes fadeUp {{
    from {{ opacity: 0; transform: translateY(20px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

/* Responsive adjustments */
@media (max-width: 900px) {{
    .hero-main {{ max-width: 80%; padding: 0 2rem; }}
    .hero-title {{ font-size: 3rem; }}
    .navbar, .hero-footer {{ padding: 1.5rem 2rem; }}
}}
@media (max-width: 600px) {{
    .hero-main {{ max-width: 100%; }}
    .hero-title {{ font-size: 2.5rem; }}
    .hero-body {{ font-size: 1.1rem; max-width: 100%; }}
    .nav-links {{ display: none; }}
    .hero-wrapper {{ background-image: linear-gradient(to bottom, rgba(5,7,10,0.8) 0%, var(--bg-base) 100%), url('{bg_image_url}'); }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hero Section Component</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="hero-wrapper">
        <header class="navbar">
            <div class="logo">
                <div class="logo-icon"></div>
                ALLIANCE
            </div>
            <ul class="nav-links">
                <li><a href="#">Our Mission</a></li>
                <li><a href="#">Fleet</a></li>
                <li><a href="#">Donate</a></li>
            </ul>
        </header>

        <main class="hero-main">
            <h1 class="hero-title">{title_text}</h1>
            <p class="hero-body">{body_text}</p>
            
            <div class="cta-group">
                <button class="btn-primary">Join Now For Free</button>
                <div class="social-proof-micro">
                    <div class="avatars">
                        <img src="https://i.pravatar.cc/100?img=11" alt="User" class="avatar">
                        <img src="https://i.pravatar.cc/100?img=12" alt="User" class="avatar">
                        <img src="https://i.pravatar.cc/100?img=13" alt="User" class="avatar">
                    </div>
                    <span>Obi Wan and 4,000 others have already joined</span>
                </div>
            </div>
        </main>

        <footer class="hero-footer">
            <span class="as-seen-text">As Seen On</span>
            <div class="logos-container">
                <!-- Using text placeholders for logos to remain zero-dependency -->
                <div class="brand-placeholder">TECHCRUNCH</div>
                <div class="brand-placeholder">FORBES</div>
                <div class="brand-placeholder">WIRED</div>
                <div class="brand-placeholder">THE VERGE</div>
            </div>
        </footer>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Interaction logic for Cinematic Hero
document.addEventListener('DOMContentLoaded', () => {
    // Simple intersection observer to trigger animations if scrolled into view
    // (Useful if this component is placed lower on a page, though typically it's at the top)
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animationPlayState = 'running';
            }
        });
    }, { threshold: 0.1 });

    const animatedElements = document.querySelectorAll('.hero-title, .hero-body, .cta-group');
    animatedElements.forEach(el => {
        // Ensure animations don't run until visible
        el.style.animationPlayState = 'paused';
        observer.observe(el);
    });
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
