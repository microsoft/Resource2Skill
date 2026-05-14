def create_component(
    output_dir: str,
    title_text: str = "Platform Analytics",
    body_text: str = "A comprehensive overview of your active deployments, user metrics, and system health.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#8b5cf6",     # CSS hex color for accent (e.g., Tailwind Violet-500)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Bento Grid & Stacked Overlays visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#0f172a"          # Slate 900
        surface_color = "#1e293b"     # Slate 800
        surface_hover = "#334155"     # Slate 700
        text_primary = "#f8fafc"      # Slate 50
        text_secondary = "#94a3b8"    # Slate 400
        border_color = "rgba(255, 255, 255, 0.08)"
        shadow = "0 10px 30px -10px rgba(0, 0, 0, 0.5)"
    else:
        bg_color = "#f8fafc"          # Slate 50
        surface_color = "#ffffff"     # White
        surface_hover = "#f1f5f9"     # Slate 100
        text_primary = "#0f172a"      # Slate 900
        text_secondary = "#64748b"    # Slate 500
        border_color = "rgba(0, 0, 0, 0.06)"
        shadow = "0 10px 30px -10px rgba(0, 0, 0, 0.08)"

    # === CSS ===
    css = f"""/* Responsive Bento Grid & Stacked Overlays */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --surface: {surface_color};
    --surface-hover: {surface_hover};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --border: {border_color};
    --accent: {accent_color};
    --shadow: {shadow};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 3rem 1.5rem;
    overflow-x: hidden;
}}

.header {{
    max-width: min(var(--width), 100%);
    width: 100%;
    margin-bottom: 2.5rem;
    text-align: left;
}}

.header h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -0.025em;
    margin-bottom: 0.75rem;
}}

.header p {{
    color: var(--text-secondary);
    font-size: 1.125rem;
    max-width: 600px;
    line-height: 1.6;
}}

/* -- BENTO GRID MACRO-LAYOUT -- */
.bento-grid {{
    display: grid;
    max-width: min(var(--width), 100%);
    width: 100%;
    gap: 1.25rem;
    
    /* Desktop default: 4 columns */
    grid-template-columns: repeat(4, 1fr);
    grid-auto-rows: 220px;
    grid-template-areas:
        "hero hero stat1 stat2"
        "hero hero stacked stacked";
}}

/* -- CARDS COMMON -- */
.bento-card {{
    background: var(--surface);
    border-radius: 1.5rem;
    border: 1px solid var(--border);
    padding: 2rem;
    box-shadow: var(--shadow);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: transform 0.3s ease, box-shadow 0.3s ease, background 0.3s ease;
    overflow: hidden;
    position: relative;
    
    /* Initial state for entrance animation */
    opacity: 0;
    transform: translateY(20px);
}}

.bento-card.visible {{
    opacity: 1;
    transform: translateY(0);
}}

.bento-card:hover {{
    transform: translateY(-4px) scale(1.01);
    box-shadow: 0 20px 40px -10px rgba(0,0,0,0.2);
    background: var(--surface-hover);
}}

.card-icon {{
    font-size: 2rem;
    color: var(--accent);
    margin-bottom: 1rem;
}}

.card-title {{
    font-size: 1rem;
    color: var(--text-secondary);
    font-weight: 500;
    margin-bottom: 0.5rem;
}}

.card-value {{
    font-size: 2rem;
    font-weight: 700;
    line-height: 1.1;
}}

/* -- SPECIFIC CARD AREAS -- */
.card-hero {{
    grid-area: hero;
}}

.card-hero .card-value {{
    font-size: 3.5rem;
    background: linear-gradient(135deg, var(--text-primary), var(--accent));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 1rem;
}}

.card-hero p {{
    color: var(--text-secondary);
    font-size: 1.1rem;
    line-height: 1.6;
}}

.card-stat1 {{ grid-area: stat1; }}
.card-stat2 {{ grid-area: stat2; }}

/* -- GRID STACKING MICRO-LAYOUT -- */
.card-stacked {{
    grid-area: stacked;
    padding: 0; /* reset padding for edge-to-edge bg */
    border: none;
    
    /* The core stacking mechanism */
    display: grid;
    grid-template-areas: "stack";
    place-items: end start; /* Bottom Left align */
}}

/* Children share the exact same grid area */
.card-stacked > .bg-visual,
.card-stacked > .content-overlay {{
    grid-area: stack;
    width: 100%;
    height: 100%;
}}

.card-stacked > .bg-visual {{
    background: linear-gradient(135deg, var(--accent), #ec4899);
    opacity: 0.85;
    border-radius: 1.5rem;
    position: relative;
    overflow: hidden;
}}

.card-stacked > .bg-visual::after {{
    content: '';
    position: absolute;
    inset: 0;
    background-image: radial-gradient(rgba(255,255,255,0.3) 2px, transparent 2px);
    background-size: 20px 20px;
    opacity: 0.5;
}}

.card-stacked > .content-overlay {{
    padding: 2rem;
    z-index: 2;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);
    border-radius: 1.5rem;
}}

.card-stacked .card-title,
.card-stacked .card-value {{
    color: #ffffff; /* Force white on vibrant bg */
}}

/* -- RESPONSIVE MEDIA QUERIES -- */
@media (max-width: 900px) {{
    .bento-grid {{
        grid-template-columns: repeat(2, 1fr);
        grid-auto-rows: 200px;
        grid-template-areas:
            "hero hero"
            "hero hero"
            "stat1 stat2"
            "stacked stacked";
    }}
}}

@media (max-width: 600px) {{
    .bento-grid {{
        grid-template-columns: 1fr;
        grid-auto-rows: minmax(180px, auto);
        grid-template-areas:
            "hero"
            "stat1"
            "stat2"
            "stacked";
    }}
    .card-hero .card-value {{ font-size: 2.5rem; }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="style.css">
    <!-- Phosphor Icons for crisp, scalable iconography -->
    <script src="https://unpkg.com/@phosphor-icons/web"></script>
</head>
<body>
    
    <header class="header">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </header>

    <main class="bento-grid">
        
        <!-- Card 1: Hero (Spans 2x2 on Desktop) -->
        <article class="bento-card card-hero">
            <div>
                <i class="ph ph-chart-polar card-icon"></i>
                <h2 class="card-title">Total Active Sessions</h2>
                <div class="card-value">284,392</div>
            </div>
            <p>Up 14.5% from last week. Traffic is heavily concentrated in the North American and EU-West regions during peak operational hours.</p>
        </article>

        <!-- Card 2: Stat 1 -->
        <article class="bento-card card-stat1">
            <i class="ph ph-lightning card-icon"></i>
            <div>
                <h2 class="card-title">Avg Latency</h2>
                <div class="card-value">42ms</div>
            </div>
        </article>

        <!-- Card 3: Stat 2 -->
        <article class="bento-card card-stat2">
            <i class="ph ph-cpu card-icon"></i>
            <div>
                <h2 class="card-title">System Load</h2>
                <div class="card-value">18%</div>
            </div>
        </article>

        <!-- Card 4: Stacked Overlay (Spans 2x1 on Desktop) -->
        <article class="bento-card card-stacked">
            <!-- Grid Stacking Layer 1: Background Visual -->
            <div class="bg-visual"></div>
            
            <!-- Grid Stacking Layer 2: Text Content overlay -->
            <div class="content-overlay">
                <i class="ph ph-rocket card-icon" style="color:#fff;"></i>
                <h2 class="card-title">Deployment Status</h2>
                <div class="card-value">All Systems Operational</div>
            </div>
        </article>

    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// JS: Intersection Observer for staggered entrance animations
document.addEventListener('DOMContentLoaded', () => {{
    const cards = document.querySelectorAll('.bento-card');
    
    const observerOptions = {{
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    }};

    const observer = new IntersectionObserver((entries, observer) => {{
        entries.forEach((entry) => {{
            if (entry.isIntersecting) {{
                // Add staggered delay based on CSS order
                const element = entry.target;
                const index = Array.from(cards).indexOf(element);
                
                setTimeout(() => {{
                    element.classList.add('visible');
                }}, index * 100); // 100ms stagger between cards
                
                // Stop observing once animated
                observer.unobserve(element);
            }}
        }});
    }}, observerOptions);

    cards.forEach(card => {{
        observer.observe(card);
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
