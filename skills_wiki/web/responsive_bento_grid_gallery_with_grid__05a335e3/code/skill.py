def create_component(
    output_dir: str,
    title_text: str = "Unleash Your Creativity",
    body_text: str = "Experience a seamless workflow with our powerful, intuitive, and lightning-fast grid-driven interface. Built for modern teams.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#6366f1",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Bento Grid visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Parse accent color to create a transparent glow
    accent_hex = accent_color.lstrip('#')
    if len(accent_hex) == 6:
        r, g, b = tuple(int(accent_hex[i:i+2], 16) for i in (0, 2, 4))
        accent_glow = f"rgba({r}, {g}, {b}, 0.15)"
        accent_border = f"rgba({r}, {g}, {b}, 0.4)"
    else:
        # Fallbacks
        accent_glow = "rgba(99, 102, 241, 0.15)"
        accent_border = "rgba(99, 102, 241, 0.4)"

    if color_scheme == "dark":
        bg_color = "#09090b"
        surface_color = "#18181b"
        border_color = "#27272a"
        text_primary = "#fafafa"
        text_secondary = "#a1a1aa"
    else:
        bg_color = "#f3f4f6"
        surface_color = "#ffffff"
        border_color = "#e5e7eb"
        text_primary = "#111827"
        text_secondary = "#4b5563"

    # === CSS ===
    css = f"""/* Responsive Bento Grid — generated component */
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --surface: {surface_color};
    --border: {border_color};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --accent: {accent_color};
    --accent-glow: {accent_glow};
    --accent-border: {accent_border};
    --max-width: {width_px}px;
    --min-height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

.container {{
    width: 100%;
    max-width: var(--max-width);
    min-height: var(--min-height);
    display: flex;
    flex-direction: column;
    justify-content: center;
}}

/* Bento Grid Layout Setup */
.bento-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    grid-template-rows: repeat(2, minmax(300px, auto));
    gap: 1.5rem;
    grid-template-areas:
        "hero hero box2 box3"
        "hero hero box4 box5";
}}

/* Bento Cards Shared Styles */
.bento-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 24px;
    padding: 2rem;
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    transition: transform 0.3s ease, border-color 0.3s ease;
    cursor: default;
}}

.bento-card:hover {{
    transform: translateY(-4px);
    border-color: var(--accent-border);
}}

/* Interactive Spotlight Effect */
.bento-card::before {{
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(
        600px circle at var(--mouse-x, 50%) var(--mouse-y, 50%), 
        var(--accent-glow), 
        transparent 40%
    );
    opacity: 0;
    transition: opacity 0.3s ease;
    pointer-events: none;
    z-index: 0;
}}

.bento-card:hover::before {{
    opacity: 1;
}}

.bento-card > * {{
    position: relative;
    z-index: 1;
}}

/* Specific Area Assignments */
.box-hero {{ grid-area: hero; }}
.box-2 {{ grid-area: box2; justify-content: center; align-items: center; text-align: center; }}
.box-3 {{ grid-area: box3; justify-content: center; align-items: center; text-align: center; }}
.box-4 {{ grid-area: box4; justify-content: center; align-items: center; text-align: center; }}
.box-5 {{ grid-area: box5; justify-content: center; align-items: center; text-align: center; }}

/* Grid Stacking implementation inside Hero Box */
.box-hero {{
    display: grid;
    grid-template-areas: "stack";
    padding: 0; /* Let gradient stretch to edges */
}}

.box-hero > * {{
    grid-area: stack;
}}

.hero-background {{
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, var(--accent-glow) 0%, transparent 100%);
    border-radius: 24px;
}}

.hero-content {{
    place-self: end start; /* Align to bottom left */
    padding: 3rem;
}}

.hero-content h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    letter-spacing: -0.02em;
    line-height: 1.1;
}}

.hero-content p {{
    font-size: 1.1rem;
    color: var(--text-secondary);
    line-height: 1.6;
    max-width: 80%;
}}

/* Smaller Box Content Styling */
.icon-wrapper {{
    width: 64px;
    height: 64px;
    border-radius: 16px;
    background: color-mix(in srgb, var(--accent) 15%, transparent);
    color: var(--accent);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    margin-bottom: 1.5rem;
}}

.box-title {{
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}}

.box-desc {{
    font-size: 0.95rem;
    color: var(--text-secondary);
    line-height: 1.5;
}}

/* Responsive Breakpoints */
@media (max-width: 1024px) {{
    .bento-grid {{
        grid-template-columns: repeat(2, 1fr);
        grid-template-rows: auto;
        grid-template-areas:
            "hero hero"
            "box2 box3"
            "box4 box5";
    }}
    .bento-grid {{ gap: 1rem; }}
}}

@media (max-width: 640px) {{
    .bento-grid {{
        grid-template-columns: 1fr;
        grid-template-areas:
            "hero"
            "box2"
            "box3"
            "box4"
            "box5";
    }}
    .hero-content {{ padding: 2rem; }}
    .hero-content h1 {{ font-size: 2rem; }}
    .hero-content p {{ max-width: 100%; }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="bento-grid">
            
            <!-- Hero Card demonstrating Grid Stacking -->
            <div class="bento-card box-hero">
                <div class="hero-background"></div>
                <div class="hero-content">
                    <h1>{title_text}</h1>
                    <p>{body_text}</p>
                </div>
            </div>

            <!-- Feature Card 1 -->
            <div class="bento-card box-2">
                <div class="icon-wrapper">
                    <i class="fa-solid fa-chart-line"></i>
                </div>
                <h3 class="box-title">Analytics</h3>
                <p class="box-desc">Real-time insights and monitoring.</p>
            </div>

            <!-- Feature Card 2 -->
            <div class="bento-card box-3">
                <div class="icon-wrapper">
                    <i class="fa-solid fa-bolt"></i>
                </div>
                <h3 class="box-title">Lightning Fast</h3>
                <p class="box-desc">Optimized for global edge delivery.</p>
            </div>

            <!-- Feature Card 3 -->
            <div class="bento-card box-4">
                <div class="icon-wrapper">
                    <i class="fa-solid fa-shield-halved"></i>
                </div>
                <h3 class="box-title">Secure</h3>
                <p class="box-desc">Enterprise-grade infrastructure.</p>
            </div>

            <!-- Feature Card 4 -->
            <div class="bento-card box-5">
                <div class="icon-wrapper">
                    <i class="fa-solid fa-wand-magic-sparkles"></i>
                </div>
                <h3 class="box-title">AI Powered</h3>
                <p class="box-desc">Automated workflows and tagging.</p>
            </div>

        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Bento Grid — interactive spotlight behavior
document.addEventListener('DOMContentLoaded', () => {{
    const cards = document.querySelectorAll('.bento-card');

    cards.forEach(card => {{
        card.addEventListener('mousemove', (e) => {{
            const rect = card.getBoundingClientRect();
            // Calculate mouse position relative to the card
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            // Set custom properties to drive the CSS radial gradient
            card.style.setProperty('--mouse-x', `${{x}}px`);
            card.style.setProperty('--mouse-y', `${{y}}px`);
        }});
        
        // Optional: Reset position when mouse leaves
        card.addEventListener('mouseleave', () => {{
            card.style.setProperty('--mouse-x', `50%`);
            card.style.setProperty('--mouse-y', `50%`);
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
