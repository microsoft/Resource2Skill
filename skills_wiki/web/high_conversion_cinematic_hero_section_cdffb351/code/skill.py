def create_component(
    output_dir: str,
    title_text: str = "It's your universe, it's time to save it",
    body_text: str = "The Rebel alliance is fighting to get rid of the evil empire. Join the resistance to create a better future for your children.",
    color_scheme: str = "dark",
    accent_color: str = "#e62429",
    width_px: int = 1440,
    height_px: int = 900,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the High-Conversion Cinematic Hero Section.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derived theme settings
    if color_scheme == "dark":
        bg_color = "#050608"
        bg_glow = "#1a1c29"
        text_main = "#ffffff"
        text_muted = "#9ca3af"
        nav_text = "#d1d5db"
    else:
        # Fallback light mode, though this pattern is natively dark-themed
        bg_color = "#f3f4f6"
        bg_glow = "#ffffff"
        text_main = "#111827"
        text_muted = "#4b5563"
        nav_text = "#374151"

    css = f"""/* High-Conversion Cinematic Hero Section */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500&family=Oswald:wght@500;700&display=swap');

:root {{
    --bg-base: {bg_color};
    --bg-glow: {bg_glow};
    --text-main: {text_main};
    --text-muted: {text_muted};
    --nav-text: {nav_text};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', sans-serif;
    background-color: var(--bg-base);
    color: var(--text-main);
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    /* Create a cinematic deep space glow effect on the right */
    background-image: radial-gradient(circle at 75% 50%, var(--bg-glow) 0%, var(--bg-base) 60%);
    overflow-x: hidden;
}}

.hero-container {{
    width: 100%;
    max-width: var(--width);
    min-height: var(--height);
    display: flex;
    flex-direction: column;
    padding: 2rem 4rem;
    position: relative;
}}

/* Navigation */
.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 2rem;
    animation: fadeDown 0.8s ease forwards;
}}

.logo {{
    font-family: 'Oswald', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    text-transform: uppercase;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

.logo-mark {{
    width: 24px;
    height: 24px;
    background-color: var(--accent);
    border-radius: 50%;
    display: inline-block;
}}

.nav-links {{
    display: flex;
    gap: 2.5rem;
    list-style: none;
}}

.nav-links a {{
    color: var(--nav-text);
    text-decoration: none;
    font-size: 0.875rem;
    font-weight: 500;
    transition: color 0.2s ease;
}}

.nav-links a:hover {{
    color: var(--text-main);
}}

.btn-ghost {{
    background: transparent;
    color: var(--text-main);
    border: 1px solid rgba(255, 255, 255, 0.2);
    padding: 0.5rem 1.5rem;
    border-radius: 4px;
    font-weight: 500;
    font-size: 0.875rem;
    cursor: pointer;
    transition: all 0.2s ease;
}}

.btn-ghost:hover {{
    border-color: var(--text-main);
    background: rgba(255, 255, 255, 0.05);
}}

/* Main Content Area */
.hero-content {{
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    max-width: 600px; /* Restrict width to keep text legible and leave space for visual */
    z-index: 10;
}}

.headline {{
    font-family: 'Oswald', sans-serif;
    font-size: clamp(3rem, 5vw, 4.5rem);
    line-height: 1.1;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
    animation: slideUp 0.8s ease 0.2s forwards;
    opacity: 0;
}}

.body-text {{
    font-size: 1.125rem;
    line-height: 1.6;
    color: var(--text-muted);
    margin-bottom: 2.5rem;
    max-width: 90%;
    animation: slideUp 0.8s ease 0.3s forwards;
    opacity: 0;
}}

/* Action Zone (CTA + Social Proof) */
.action-zone {{
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    animation: slideUp 0.8s ease 0.4s forwards;
    opacity: 0;
}}

.btn-primary {{
    background-color: var(--accent);
    color: #ffffff;
    border: none;
    padding: 1rem 2.5rem;
    font-family: 'Oswald', sans-serif;
    font-size: 1.125rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    border-radius: 4px;
    cursor: pointer;
    align-self: flex-start;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}

.btn-primary:hover {{
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(230, 36, 41, 0.3);
}}

/* Social Proof Avatars */
.social-proof {{
    display: flex;
    align-items: center;
    gap: 1rem;
}}

.avatars {{
    display: flex;
}}

.avatar {{
    width: 36px;
    height: 36px;
    border-radius: 50%;
    border: 2px solid var(--bg-base);
    margin-left: -12px;
    background-size: cover;
    background-position: center;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.7rem;
    font-weight: bold;
    color: white;
}}

.avatar:first-child {{
    margin-left: 0;
}}

.social-text {{
    font-size: 0.875rem;
    color: var(--nav-text);
}}

.social-text strong {{
    color: var(--text-main);
}}

/* Trust Badges */
.trust-badges {{
    margin-top: 4rem;
    animation: fadeUp 1s ease 0.6s forwards;
    opacity: 0;
}}

.trust-label {{
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-muted);
    margin-bottom: 1rem;
}}

.logos-container {{
    display: flex;
    gap: 2rem;
    align-items: center;
}}

.mock-logo {{
    font-family: 'Oswald', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--nav-text);
    filter: grayscale(100%) opacity(0.5);
    transition: filter 0.3s ease;
    cursor: default;
}}

.mock-logo:hover {{
    filter: grayscale(0%) opacity(1);
}}

/* Animations */
@keyframes fadeDown {{
    from {{ opacity: 0; transform: translateY(-20px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

@keyframes slideUp {{
    from {{ opacity: 0; transform: translateY(30px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

@keyframes fadeUp {{
    from {{ opacity: 0; transform: translateY(10px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

/* Responsive */
@media (max-width: 1024px) {{
    .hero-container {{ padding: 2rem; }}
    .headline {{ font-size: 3.5rem; }}
}}

@media (max-width: 768px) {{
    .nav-links {{ display: none; }}
    .headline {{ font-size: 2.5rem; }}
    .hero-content {{ max-width: 100%; align-items: center; text-align: center; }}
    .btn-primary {{ align-self: center; }}
    .logos-container {{ justify-content: center; }}
    .trust-badges {{ text-align: center; }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text.split(',')[0]} - Hero Section</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="hero-container">
        <!-- Navigation -->
        <nav class="navbar">
            <div class="logo">
                <span class="logo-mark"></span>
                Rebel Alliance
            </div>
            <ul class="nav-links">
                <li><a href="#">Our Ships</a></li>
                <li><a href="#">Mission</a></li>
                <li><a href="#">Donations</a></li>
            </ul>
            <button class="btn-ghost">Member Login</button>
        </nav>

        <!-- Main Content -->
        <main class="hero-content">
            <h1 class="headline">{title_text}</h1>
            <p class="body-text">{body_text}</p>
            
            <div class="action-zone">
                <button class="btn-primary">Join Now For Free</button>
                
                <div class="social-proof">
                    <div class="avatars">
                        <div class="avatar" style="background-color: #3b82f6;">OW</div>
                        <div class="avatar" style="background-color: #10b981;">LS</div>
                        <div class="avatar" style="background-color: #8b5cf6;">HS</div>
                        <div class="avatar" style="background-color: #f59e0b;">CP</div>
                    </div>
                    <span class="social-text"><strong>Obi Wan</strong> and 4,000 others have already joined</span>
                </div>
            </div>

            <!-- Trust Badges -->
            <div class="trust-badges">
                <div class="trust-label">As Seen On</div>
                <div class="logos-container">
                    <span class="mock-logo">NBC</span>
                    <span class="mock-logo">FOX</span>
                    <span class="mock-logo">CBS</span>
                    <span class="mock-logo">HULU</span>
                </div>
            </div>
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// High-Conversion Hero Interactions
document.addEventListener('DOMContentLoaded', () => {
    // Add subtle interactive tilt to the primary button (optional flourish)
    const primaryBtn = document.querySelector('.btn-primary');
    
    if (primaryBtn) {
        primaryBtn.addEventListener('mousemove', (e) => {
            const rect = primaryBtn.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            // Calculate rotation based on cursor position
            const xRotation = ((y - rect.height / 2) / rect.height) * -10;
            const yRotation = ((x - rect.width / 2) / rect.width) * 10;
            
            primaryBtn.style.transform = `perspective(500px) scale(1.02) rotateX(${xRotation}deg) rotateY(${yRotation}deg)`;
        });
        
        primaryBtn.addEventListener('mouseleave', () => {
            primaryBtn.style.transform = 'perspective(500px) scale(1) rotateX(0) rotateY(0)';
        });
    }
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
