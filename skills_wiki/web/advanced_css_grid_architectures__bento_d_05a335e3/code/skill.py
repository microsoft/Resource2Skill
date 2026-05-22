def create_component(
    output_dir: str,
    title_text: str = "Grid Architecture Overview",
    body_text: str = "Discover the power of asymmetric Bento layouts and fluidly wrapping Auto-Fit galleries driven entirely by modern CSS Grid.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#6366f1",     # Indigo-500
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Creates a responsive CSS Grid dashboard featuring both a Bento Layout and an Auto-Fit Gallery.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#09090b"
        text_color = "#f8fafc"
        surface_color = "#18181b"
        border_color = "#27272a"
        shadow_color = "rgba(0, 0, 0, 0.4)"
        text_muted = "#a1a1aa"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        surface_color = "#ffffff"
        border_color = "#e2e8f0"
        shadow_color = "rgba(15, 23, 42, 0.08)"
        text_muted = "#64748b"

    # === CSS ===
    css = f"""/* Advanced CSS Grid Architectures */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --border: {border_color};
    --shadow: {shadow_color};
    --text-muted: {text_muted};
    --max-width: {width_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    padding: 4rem 1.5rem;
    line-height: 1.5;
}}

.container {{
    width: 100%;
    max-width: var(--max-width);
    margin: 0 auto;
}}

/* --- Typography & Header --- */
.header {{
    text-align: center;
    margin-bottom: 4rem;
}}

.main-title {{
    font-size: clamp(2rem, 5vw, 3rem);
    font-weight: 700;
    letter-spacing: -0.03em;
    margin-bottom: 1rem;
}}

.main-desc {{
    font-size: 1.125rem;
    color: var(--text-muted);
    max-width: 600px;
    margin: 0 auto;
}}

.section-header {{
    margin: 4rem 0 1.5rem 0;
}}

.section-title {{
    font-size: 1.5rem;
    font-weight: 600;
}}

/* --- Reusable Box Styles --- */
.box, .auto-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 1.5rem;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    position: relative;
    overflow: hidden;
}}

/* --- Hover Effects --- */
/* We apply hover transitions on box-shadow and border to avoid conflicting 
   with the entry animation's transform property */
.box, .auto-card {{
    transition: box-shadow 0.3s ease, border-color 0.3s ease, transform 0.3s ease;
}}

.box:hover, .auto-card:hover {{
    border-color: var(--accent);
    box-shadow: 0 12px 32px var(--shadow);
    transform: translateY(-4px);
}}

/* --- Entry Animation Logic --- */
.animate-in {{
    --delay: 0s;
    opacity: 0;
    transform: translateY(30px);
    /* The entry transition consumes the --delay variable */
    transition: 
        opacity 0.7s ease var(--delay), 
        transform 0.7s cubic-bezier(0.2, 0.8, 0.2, 1) var(--delay);
}}

.animate-in.visible {{
    opacity: 1;
    transform: translateY(0);
}}

/* =========================================
   PATTERN 1: THE BENTO GRID
========================================= */
.bento-grid {{
    display: grid;
    gap: 1.5rem;
    /* 4 Equal Columns */
    grid-template-columns: repeat(4, 1fr);
    /* 2 Explicit Rows */
    grid-template-rows: repeat(2, minmax(220px, auto));
    /* The Magic: Mapping layout visually */
    grid-template-areas:
        "hero hero stat1 stat2"
        "hero hero chart feature";
}}

/* Assigning elements to grid areas */
.bento-hero {{ grid-area: hero; }}
.bento-stat1 {{ grid-area: stat1; justify-content: center; }}
.bento-stat2 {{ grid-area: stat2; justify-content: center; }}
.bento-chart {{ grid-area: chart; padding: 1rem; }}
.bento-feat  {{ grid-area: feature; justify-content: center; }}

/* Bento Inner Typography */
.bento-hero .title {{
    font-size: 2rem;
    font-weight: 600;
    margin-bottom: 1rem;
}}
.bento-hero .desc {{
    color: var(--text-muted);
    margin-bottom: 2rem;
    max-width: 90%;
}}
.btn {{
    background: var(--accent);
    color: #fff;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 0.5rem;
    font-weight: 600;
    font-size: 1rem;
    cursor: pointer;
    margin-top: auto;
    align-self: flex-start;
    transition: opacity 0.2s;
}}
.btn:hover {{ opacity: 0.9; }}

.stat-val {{
    font-size: 3rem;
    font-weight: 700;
    color: var(--accent);
    line-height: 1;
    margin-bottom: 0.5rem;
}}
.stat-lbl {{
    font-size: 0.875rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-muted);
}}
.chart-mock {{
    width: 100%;
    height: 100%;
    border-radius: 0.75rem;
    background: linear-gradient(135deg, var(--accent) 0%, transparent 100%);
    opacity: 0.2;
}}

/* --- Bento Grid Responsive Breakpoints --- */

/* Tablet: Reshuffle to 3 columns */
@media (max-width: 960px) {{
    .bento-grid {{
        grid-template-columns: repeat(3, 1fr);
        grid-template-rows: repeat(3, minmax(180px, auto));
        grid-template-areas:
            "hero hero stat1"
            "hero hero stat2"
            "chart chart feature";
    }}
}}

/* Mobile: Reshuffle to 2 columns */
@media (max-width: 640px) {{
    .bento-grid {{
        grid-template-columns: repeat(2, 1fr);
        grid-template-rows: repeat(4, minmax(180px, auto));
        grid-template-areas:
            "hero hero"
            "hero hero"
            "stat1 stat2"
            "chart feature";
    }}
}}

/* Small Mobile: Single column stack */
@media (max-width: 480px) {{
    .bento-grid {{
        grid-template-columns: 1fr;
        grid-template-rows: auto;
        grid-template-areas:
            "hero"
            "stat1"
            "stat2"
            "chart"
            "feature";
    }}
}}


/* =========================================
   PATTERN 2: THE AUTO-FIT GRID
========================================= */
.auto-grid {{
    display: grid;
    gap: 1.5rem;
    /* The Magic: Natively wraps based on min-width (250px) without media queries */
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
}}

.auto-card {{
    padding: 1.25rem;
    border-radius: 1rem;
}}

.card-img-mock {{
    background: var(--bg);
    height: 140px;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
}}

.card-title {{
    font-weight: 600;
    margin-bottom: 0.25rem;
}}

.card-price {{
    color: var(--text-muted);
    font-size: 0.875rem;
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
</head>
<body>
    <div class="container">
        
        <header class="header animate-in">
            <h1 class="main-title">{title_text}</h1>
            <p class="main-desc">{body_text}</p>
        </header>

        <!-- PATTERN 1: BENTO GRID -->
        <div class="bento-grid">
            <div class="box bento-hero animate-in">
                <h2 class="title">Bento Box Architecture</h2>
                <p class="desc">Notice how this hero cell spans multiple columns and rows. By modifying <code>grid-template-areas</code> in media queries, we completely alter the layout structure without touching HTML.</p>
                <button class="btn">Explore Layouts</button>
            </div>
            
            <div class="box bento-stat1 animate-in">
                <div class="stat-val">4x</div>
                <div class="stat-lbl">Faster Dev Time</div>
            </div>
            
            <div class="box bento-stat2 animate-in">
                <div class="stat-val">100%</div>
                <div class="stat-lbl">Responsive</div>
            </div>
            
            <div class="box bento-chart animate-in">
                <div class="chart-mock"></div>
            </div>
            
            <div class="box bento-feat animate-in">
                <h3 style="margin-bottom: 0.5rem; font-size: 1.1rem;">Explicit Control</h3>
                <p style="font-size: 0.9rem; color: var(--text-muted);">Named areas give semantic meaning to layout logic.</p>
            </div>
        </div>

        <!-- PATTERN 2: AUTO-FIT GRID -->
        <div class="section-header animate-in">
            <h2 class="section-title">Fluid Auto-Fit Gallery</h2>
            <p style="color: var(--text-muted); margin-top: 0.25rem;">Resize the window to watch columns wrap automatically using <code>minmax()</code>.</p>
        </div>

        <div class="auto-grid">
            <div class="auto-card animate-in">
                <div class="card-img-mock"></div>
                <div class="card-title">Alpha Prototype</div>
                <div class="card-price">Grid Element</div>
            </div>
            <div class="auto-card animate-in">
                <div class="card-img-mock"></div>
                <div class="card-title">Beta Prototype</div>
                <div class="card-price">Grid Element</div>
            </div>
            <div class="auto-card animate-in">
                <div class="card-img-mock"></div>
                <div class="card-title">Gamma Prototype</div>
                <div class="card-price">Grid Element</div>
            </div>
            <div class="auto-card animate-in">
                <div class="card-img-mock"></div>
                <div class="card-title">Delta Prototype</div>
                <div class="card-price">Grid Element</div>
            </div>
            <div class="auto-card animate-in">
                <div class="card-img-mock"></div>
                <div class="card-title">Epsilon Prototype</div>
                <div class="card-price">Grid Element</div>
            </div>
            <div class="auto-card animate-in">
                <div class="card-img-mock"></div>
                <div class="card-title">Zeta Prototype</div>
                <div class="card-price">Grid Element</div>
            </div>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Intersection Observer for staggered entry animations
document.addEventListener('DOMContentLoaded', () => {{
    const animatedElements = document.querySelectorAll('.animate-in');
    
    // Configuration for the observer
    const observerOptions = {{
        root: null,
        rootMargin: '0px',
        threshold: 0.1 // Trigger when 10% of the element is visible
    }};

    const observer = new IntersectionObserver((entries, observer) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                // Add the visible class to trigger CSS transition
                entry.target.classList.add('visible');
                // Unobserve so animation only happens once
                observer.unobserve(entry.target);
            }}
        }});
    }}, observerOptions);

    // Apply staggered delays and begin observation
    animatedElements.forEach((el, index) => {{
        // We use a CSS custom property to handle the delay 
        // to prevent overriding standard inline transition properties
        const staggerDelay = (index % 12) * 0.08;
        el.style.setProperty('--delay', `${{staggerDelay}}s`);
        
        observer.observe(el);
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
