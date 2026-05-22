def create_component(
    output_dir: str,
    title_text: str = "It's your universe, it's time to save it",
    body_text: str = "The Rebel alliance is fighting to get rid of the evil empire, join the resistance to create a better future for your children.",
    color_scheme: str = "dark",
    accent_color: str = "#ef4444",
    width_px: int = 1280,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Conversion-Optimized Split Hero Section.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Convert hex accent color to RGB for box-shadows and alpha blending
    hex_c = accent_color.lstrip('#')
    if len(hex_c) == 6:
        r, g, b = tuple(int(hex_c[i:i+2], 16) for i in (0, 2, 4))
    else:
        r, g, b = (239, 68, 68) # Fallback red

    # Theme logic
    if color_scheme == "dark":
        bg_color = "#050510"
        text_main = "#ffffff"
        text_muted = "#94a3b8"
        border_color = "rgba(255, 255, 255, 0.15)"
        bg_image = "url('https://images.unsplash.com/photo-1506703719100-a0f3a48c0f86?q=80&w=2560&auto=format&fit=crop')"
    else:
        bg_color = "#f8fafc"
        text_main = "#0f172a"
        text_muted = "#64748b"
        border_color = "rgba(0, 0, 0, 0.15)"
        bg_image = f"radial-gradient(circle at 80% 50%, rgba({r},{g},{b}, 0.1) 0%, transparent 50%)"

    css = f"""/* Conversion-Optimized Split Hero Section */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-main: {text_main};
    --text-muted: {text_muted};
    --border-color: {border_color};
    --accent: {accent_color};
    --accent-rgb: {r}, {g}, {b};
    --bg-image: {bg_image};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    background-image: var(--bg-image);
    background-size: cover;
    background-position: center;
    color: var(--text-main);
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    overflow-x: hidden;
}}

.wrapper {{
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    max-height: 100vh;
    display: flex;
    flex-direction: column;
    padding: 0 2rem;
    position: relative;
    z-index: 1;
}}

/* Header */
.header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2rem 0;
    opacity: 0; /* Handled by JS */
}}

.logo {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-weight: 800;
    font-size: 1.25rem;
    letter-spacing: -0.02em;
}}

.nav {{
    display: flex;
    gap: 2.5rem;
}}

.nav a {{
    color: var(--text-main);
    text-decoration: none;
    font-weight: 500;
    font-size: 0.95rem;
    transition: color 0.2s;
}}

.nav a:hover {{
    color: var(--accent);
}}

/* Buttons */
.btn {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.875rem 1.75rem;
    font-weight: 600;
    text-decoration: none;
    border-radius: 4px;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    cursor: pointer;
}}

.btn-ghost {{
    border: 1px solid var(--border-color);
    color: var(--text-main);
}}

.btn-ghost:hover {{
    border-color: var(--text-main);
}}

.btn-primary {{
    background: var(--accent);
    color: #ffffff; /* Always white for primary CTA */
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-size: 0.875rem;
    box-shadow: 0 4px 14px rgba(var(--accent-rgb), 0.2);
}}

.btn-primary:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(var(--accent-rgb), 0.4);
}}

/* Main Hero Grid */
.hero {{
    flex: 1;
    display: grid;
    grid-template-columns: 1fr 1fr;
    align-items: center;
    gap: 4rem;
    padding-bottom: 2rem;
}}

.hero-content {{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}}

.badge {{
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border: 1px solid var(--accent);
    color: var(--accent);
    border-radius: 50px;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 1.5rem;
    opacity: 0;
}}

h1 {{
    font-size: clamp(2.5rem, 4vw, 4rem);
    line-height: 1.1;
    font-weight: 800;
    letter-spacing: -0.02em;
    margin-bottom: 1.25rem;
    opacity: 0;
}}

.body-text {{
    font-size: 1.125rem;
    line-height: 1.6;
    color: var(--text-muted);
    max-width: 480px;
    margin-bottom: 2.5rem;
    opacity: 0;
}}

.cta-group {{
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-bottom: 3rem;
    opacity: 0;
}}

/* Social Proof */
.social-proof {{
    display: flex;
    align-items: center;
    gap: 1rem;
}}

.avatars {{
    display: flex;
}}

.avatar {{
    width: 32px;
    height: 32px;
    border-radius: 50%;
    border: 2px solid var(--bg-color);
    margin-left: -10px;
    background: #ccc;
    object-fit: cover;
}}

.avatar:first-child {{
    margin-left: 0;
}}

.proof-text {{
    font-size: 0.875rem;
    color: var(--text-muted);
}}

/* Trust Logos */
.trust-row {{
    display: flex;
    align-items: center;
    gap: 1.5rem;
    padding-top: 2rem;
    border-top: 1px solid var(--border-color);
    width: 100%;
    opacity: 0;
}}

.trust-label {{
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-muted);
    font-weight: 600;
}}

.trust-logos {{
    display: flex;
    gap: 2rem;
}}

.logo-ph {{
    font-family: system-ui, sans-serif;
    font-weight: 800;
    font-size: 1.1rem;
    color: var(--text-muted);
    opacity: 0.5;
    letter-spacing: -0.02em;
}}

/* Hero Visual (Right Column) */
.hero-visual {{
    position: relative;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    opacity: 0;
}}

.portal {{
    width: 380px;
    height: 380px;
    border-radius: 50%;
    box-shadow: 
        0 0 80px rgba(var(--accent-rgb), 0.2), 
        inset 0 0 80px rgba(var(--accent-rgb), 0.2);
    border: 1px solid rgba(var(--accent-rgb), 0.4);
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    animation: float 6s ease-in-out infinite;
}}

.portal::before {{
    content: '';
    position: absolute;
    width: 130%;
    height: 130%;
    border-radius: 50%;
    border: 1px dashed var(--border-color);
    animation: spin 30s linear infinite;
}}

.portal-core {{
    width: 180px;
    height: 180px;
    border-radius: 50%;
    background: radial-gradient(circle, var(--accent), transparent 70%);
    opacity: 0.6;
    animation: pulse 4s ease-in-out infinite alternate;
    filter: blur(8px);
}}

/* Keyframes */
@keyframes float {{
    0%, 100% {{ transform: translateY(0); }}
    50% {{ transform: translateY(-20px); }}
}}

@keyframes spin {{
    0% {{ transform: rotate(0deg); }}
    100% {{ transform: rotate(360deg); }}
}}

@keyframes pulse {{
    0% {{ transform: scale(0.9); opacity: 0.4; }}
    100% {{ transform: scale(1.1); opacity: 0.8; }}
}}

@media (max-width: 900px) {{
    .hero {{ grid-template-columns: 1fr; text-align: center; gap: 2rem; }}
    .hero-content {{ align-items: center; }}
    .nav {{ display: none; }}
    .trust-row {{ justify-content: center; flex-direction: column; gap: 1rem; }}
    .portal {{ width: 280px; height: 280px; }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="wrapper">
        <header class="header">
            <div class="logo">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="var(--accent)"><path d="M12 2L2 22h20L12 2zm0 4.5l6.5 13h-13L12 6.5z"/></svg>
                <span>Rebel Base</span>
            </div>
            <nav class="nav">
                <a href="#">Our Fleet</a>
                <a href="#">Mission</a>
                <a href="#">Donations</a>
            </nav>
            <a href="#" class="btn btn-ghost">Sign In</a>
        </header>

        <main class="hero">
            <div class="hero-content">
                <div class="badge">Join now for free</div>
                <h1>{title_text}</h1>
                <p class="body-text">{body_text}</p>

                <div class="cta-group">
                    <a href="#" class="btn btn-primary">Join The Resistance</a>
                    <div class="social-proof">
                        <div class="avatars">
                            <!-- Robust placeholder faces -->
                            <img src="https://i.pravatar.cc/100?img=11" alt="User" class="avatar">
                            <img src="https://i.pravatar.cc/100?img=32" alt="User" class="avatar">
                            <img src="https://i.pravatar.cc/100?img=33" alt="User" class="avatar">
                        </div>
                        <span class="proof-text">Obi Wan and 4,000 others have already joined</span>
                    </div>
                </div>

                <div class="trust-row">
                    <span class="trust-label">As seen on:</span>
                    <div class="trust-logos">
                        <span class="logo-ph">GALACTIC NEWS</span>
                        <span class="logo-ph">HOLONET</span>
                        <span class="logo-ph">OUTER RIM</span>
                    </div>
                </div>
            </div>

            <div class="hero-visual">
                <!-- Pure CSS Abstract Representation of the Tutorial's Star/Ship -->
                <div class="portal">
                    <div class="portal-core"></div>
                </div>
            </div>
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Conversion-Optimized Split Hero Section - Entrance Animations
document.addEventListener('DOMContentLoaded', () => {{
    // Select elements in the order they should appear
    const animateElements = [
        '.header',
        '.badge',
        'h1',
        '.body-text',
        '.cta-group',
        '.trust-row',
        '.hero-visual'
    ];

    // Apply starting state and transitions
    animateElements.forEach((selector, index) => {{
        const el = document.querySelector(selector);
        if (el) {{
            // Set initial state
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            
            // Wait for next frame to ensure initial state is rendered, then animate
            requestAnimationFrame(() => {{
                setTimeout(() => {{
                    el.style.transition = 'opacity 0.8s ease-out, transform 0.8s cubic-bezier(0.16, 1, 0.3, 1)';
                    el.style.opacity = '1';
                    el.style.transform = 'translateY(0)';
                }}, index * 100); // 100ms stagger between elements
            }});
        }}
    }});
}});
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
