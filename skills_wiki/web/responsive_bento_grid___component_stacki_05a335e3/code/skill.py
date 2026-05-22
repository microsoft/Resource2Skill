def create_component(
    output_dir: str,
    title_text: str = "Bento Grid System",
    body_text: str = "A fluid, responsive layout engine powered by CSS Grid Areas and Grid Stacking.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#6366f1",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Bento Grid visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#0f111a"
        text_color = "#f8fafc"
        text_muted = "#94a3b8"
        surface_color = "#1e2130"
        border_color = "#334155"
        shadow_hover = "rgba(0, 0, 0, 0.3)"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        text_muted = "#64748b"
        surface_color = "#ffffff"
        border_color = "#e2e8f0"
        shadow_hover = "rgba(0, 0, 0, 0.08)"

    # === CSS ===
    css = f"""/* Responsive Bento Grid — generated component */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --surface: {surface_color};
    --border: {border_color};
    --shadow-hover: {shadow_hover};
    --width: {width_px}px;
    --height: {height_px}px;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 40px 20px;
    overflow-y: auto;
}}

.container {{
    width: 100%;
    max-width: var(--width);
    display: flex;
    flex-direction: column;
    gap: 32px;
}}

.header {{
    text-align: center;
    max-width: 600px;
    margin: 0 auto;
}}

.title {{
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    margin-bottom: 12px;
}}

.body-text {{
    font-size: 1.1rem;
    color: var(--text-muted);
    line-height: 1.6;
}}

/* -- Macro Layout: The Bento Grid -- */
.bento-grid {{
    display: grid;
    gap: 20px;
    /* Desktop layout */
    grid-template-columns: repeat(4, 1fr);
    grid-auto-rows: minmax(180px, auto);
    grid-template-areas:
        "hero hero top right"
        "hero hero bottom right"
        "feature1 feature2 feature3 feature3";
}}

.card {{
    background: var(--surface);
    border-radius: 24px;
    padding: 24px;
    border: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    gap: 12px;
    position: relative;
    overflow: hidden;
    
    /* Animation initial state */
    opacity: 0;
    transform: translateY(20px);
}}

/* State applied by JS */
.card.visible {{
    opacity: 1;
    transform: translateY(0);
    transition: opacity 0.6s ease-out, transform 0.6s ease-out, box-shadow 0.3s ease;
}}

.card.visible:hover {{
    transform: translateY(-4px);
    box-shadow: 0 16px 32px var(--shadow-hover);
    border-color: var(--accent);
}}

/* -- Micro Layout: Grid Stacking in Hero -- */
.hero {{
    grid-area: hero;
    display: grid;
    padding: 0;
    border: none;
    color: #ffffff; /* Ensure contrast against gradient */
}}

/* Both children occupy the exact same cell, stacking natively */
.hero > * {{
    grid-column: 1 / -1;
    grid-row: 1 / -1;
}}

.hero-bg {{
    background: linear-gradient(135deg, var(--accent), #a855f7);
    width: 100%;
    height: 100%;
    opacity: 0.9;
    transition: transform 0.5s ease;
}}

.hero.visible:hover .hero-bg {{
    transform: scale(1.05);
}}

.hero-content {{
    place-self: end start; /* Align to bottom left */
    padding: 32px;
    z-index: 2;
}}

.hero-content h2 {{
    font-size: 2.25rem;
    font-weight: 700;
    margin-bottom: 8px;
    letter-spacing: -0.02em;
}}

/* -- Assigning grid areas -- */
.top {{ grid-area: top; }}
.right {{ grid-area: right; justify-content: space-between; }}
.bottom {{ grid-area: bottom; }}
.feature1 {{ grid-area: feature1; }}
.feature2 {{ grid-area: feature2; }}
.feature3 {{ grid-area: feature3; justify-content: center; align-items: center; text-align: center; }}

/* -- Card Typography & Embellishments -- */
h3 {{
    font-size: 1.25rem;
    font-weight: 600;
    letter-spacing: -0.01em;
}}

p {{
    font-size: 0.95rem;
    color: var(--text-muted);
    line-height: 1.5;
}}

.chart-placeholder {{
    margin-top: auto;
    height: 48px;
    background: repeating-linear-gradient(
        45deg,
        transparent,
        transparent 8px,
        var(--border) 8px,
        var(--border) 16px
    );
    border-radius: 8px;
    opacity: 0.5;
}}

.stack-placeholder {{
    display: flex;
    margin-top: 16px;
}}

.circle {{
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: var(--surface);
    border: 2px solid var(--border);
    margin-left: -16px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}}

.circle:first-child {{
    margin-left: 0;
    background: var(--accent);
    border-color: var(--accent);
}}

/* -- Responsive Layout Morphing -- */
@media (max-width: 900px) {{
    .bento-grid {{
        grid-template-columns: repeat(2, 1fr);
        grid-template-areas:
            "hero hero"
            "top bottom"
            "right right"
            "feature1 feature2"
            "feature3 feature3";
    }}
}}

@media (max-width: 600px) {{
    .bento-grid {{
        grid-template-columns: 1fr;
        grid-template-areas:
            "hero"
            "top"
            "bottom"
            "right"
            "feature1"
            "feature2"
            "feature3";
    }}
    .hero-content h2 {{ font-size: 1.75rem; }}
    .title {{ font-size: 2rem; }}
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <header class="header">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </header>
        
        <div class="bento-grid">
            <div class="card hero">
                <div class="hero-bg"></div>
                <div class="hero-content">
                    <h2>Grid Stacking</h2>
                    <p>Elements natively layered within the same cell. No absolute positioning required.</p>
                </div>
            </div>
            
            <div class="card top">
                <h3>Analytics</h3>
                <div class="chart-placeholder"></div>
            </div>
            
            <div class="card right">
                <div>
                    <h3>Integrations</h3>
                    <p style="margin-top:8px;">Seamless connections.</p>
                </div>
                <div class="stack-placeholder">
                    <div class="circle"></div>
                    <div class="circle"></div>
                    <div class="circle"></div>
                </div>
            </div>
            
            <div class="card bottom">
                <h3>Real-time</h3>
                <p>Live sync enabled.</p>
            </div>
            
            <div class="card feature1">
                <h3>Fast</h3>
            </div>
            
            <div class="card feature2">
                <h3>Secure</h3>
            </div>
            
            <div class="card feature3">
                <h3>Scalable Architecture</h3>
                <p>Implicit grids handle growth automatically.</p>
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Intersection Observer for staggered entrance animation
document.addEventListener('DOMContentLoaded', () => {{
    const cards = document.querySelectorAll('.card');

    const observer = new IntersectionObserver((entries) => {{
        entries.forEach((entry) => {{
            if (entry.isIntersecting) {{
                // Trigger visibility class
                entry.target.classList.add('visible');
                // Stop observing once animated in
                observer.unobserve(entry.target);
            }}
        }});
    }}, {{
        threshold: 0.1, // Trigger when 10% of card is visible
        rootMargin: '0px 0px -50px 0px' // Slightly delay trigger until it comes up from bottom
    }});

    cards.forEach((card, index) => {{
        // Apply a staggered transition delay based on index
        // Limit delay to prevent massively long wait times on slow scrolls
        const delay = Math.min(index * 75, 400); 
        card.style.transitionDelay = `${{delay}}ms`;
        observer.observe(card);
        
        // Clean up transition delay after animation completes 
        // to prevent sluggish hover effects
        card.addEventListener('transitionend', (e) => {{
            if (e.propertyName === 'transform') {{
                card.style.transitionDelay = '0ms';
            }}
        }}, {{ once: true }});
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
