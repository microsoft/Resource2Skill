def create_component(
    output_dir: str,
    title_text: str = "Analytics Dashboard",
    body_text: str = "A comprehensive overview of your system's performance metrics.",
    color_scheme: str = "dark",        
    accent_color: str = "#8b5cf6",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Bento Grid with Grid Stacking.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_color = "#f8fafc"
        text_muted = "#94a3b8"
        surface_color = "rgba(255, 255, 255, 0.03)"
        border_color = "rgba(255, 255, 255, 0.08)"
        shadow = "0 10px 30px -10px rgba(0,0,0,0.5)"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        text_muted = "#64748b"
        surface_color = "#ffffff"
        border_color = "rgba(0, 0, 0, 0.08)"
        shadow = "0 10px 30px -10px rgba(0,0,0,0.05)"

    # === CSS ===
    css = f"""/* Bento Grid Component */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --surface: {surface_color};
    --border: {border_color};
    --shadow: {shadow};
    --max-width: {width_px}px;
    --min-height: {height_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: grid;
    place-items: center;
    padding: 2rem;
}}

.wrapper {{
    width: 100%;
    max-width: var(--max-width);
    min-height: var(--min-height);
    display: flex;
    flex-direction: column;
    gap: 2rem;
}}

.header {{
    text-align: center;
    margin-bottom: 1rem;
}}

.header h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -0.025em;
    margin-bottom: 0.5rem;
}}

.header p {{
    color: var(--text-muted);
    font-size: 1.125rem;
}}

/* --- Bento Grid Layout --- */
.bento-grid {{
    display: grid;
    gap: 1.5rem;
    /* 4 columns by default */
    grid-template-columns: repeat(4, 1fr);
    /* Establish implicit row heights to keep blocks uniform */
    grid-auto-rows: minmax(180px, auto);
    /* The Magic: Grid Template Areas */
    grid-template-areas: 
        "hero hero stats chart"
        "hero hero tasks activity";
}}

/* Setup grid area assignments */
.card-hero     {{ grid-area: hero; }}
.card-stats    {{ grid-area: stats; }}
.card-chart    {{ grid-area: chart; }}
.card-tasks    {{ grid-area: tasks; }}
.card-activity {{ grid-area: activity; }}

/* --- Card Styling --- */
.bento-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 1.5rem;
    padding: 1.5rem;
    box-shadow: var(--shadow);
    display: flex;
    flex-direction: column;
    justify-content: center;
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.3s ease;
    opacity: 0;
    transform: translateY(20px);
    overflow: hidden;
    position: relative;
}}

.bento-card.visible {{
    opacity: 1;
    transform: translateY(0);
}}

.bento-card:hover {{
    transform: translateY(-4px) scale(1.01);
    border-color: var(--accent);
}}

.card-title {{
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: var(--text);
}}

.card-value {{
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--accent);
}}

/* --- Grid Stacking Technique (Hero Card) --- */
.card-hero {{
    padding: 0; /* Remove padding to let image bleed */
    /* Make the hero card itself a single-cell grid */
    display: grid;
    grid-template-areas: "stack";
    place-items: center; /* Center content horizontally & vertically */
}}

.card-hero > * {{
    /* Both the image and the content share the 'stack' cell */
    grid-area: stack;
}}

.hero-img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    z-index: 1;
    opacity: 0.6;
    transition: transform 0.7s ease;
}}

.card-hero:hover .hero-img {{
    transform: scale(1.05);
}}

.hero-content {{
    z-index: 2; /* Sits on top of the image */
    text-align: center;
    padding: 2rem;
    background: rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    border-radius: 1rem;
    color: #ffffff; /* Force white for image overlay */
    max-width: 80%;
}}

.hero-content h2 {{
    font-size: 2rem;
    margin-bottom: 0.5rem;
}}

/* --- Tablet Responsive --- */
@media (max-width: 1024px) {{
    .bento-grid {{
        grid-template-columns: repeat(3, 1fr);
        grid-template-areas: 
            "hero hero stats"
            "hero hero chart"
            "tasks activity activity";
    }}
}}

/* --- Mobile Responsive --- */
@media (max-width: 768px) {{
    .bento-grid {{
        grid-template-columns: 1fr;
        grid-auto-rows: minmax(200px, auto);
        /* Stack everything linearly, but keep hero large */
        grid-template-areas: 
            "hero"
            "stats"
            "chart"
            "tasks"
            "activity";
    }}
    
    .card-hero {{
        min-height: 300px;
    }}
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
    <div class="wrapper">
        <header class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>

        <main class="bento-grid">
            <!-- Grid Stacking Overlay Hero -->
            <article class="bento-card card-hero">
                <img src="https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=1200&q=80" alt="Tech Background" class="hero-img">
                <div class="hero-content">
                    <h2>System Architecture</h2>
                    <p>Real-time processing across global distributed nodes.</p>
                </div>
            </article>

            <!-- Standard Bento Cells -->
            <article class="bento-card card-stats">
                <h3 class="card-title">Active Users</h3>
                <div class="card-value">14.2k</div>
                <p style="color: var(--text-muted); margin-top: auto; font-size: 0.9rem;">↑ 12% from last week</p>
            </article>

            <article class="bento-card card-chart">
                <h3 class="card-title">Server Load</h3>
                <div class="card-value">34%</div>
                <p style="color: var(--text-muted); margin-top: auto; font-size: 0.9rem;">Optimal operating range</p>
            </article>

            <article class="bento-card card-tasks">
                <h3 class="card-title">Pending Jobs</h3>
                <div class="card-value" style="color: var(--text);">128</div>
            </article>

            <article class="bento-card card-activity">
                <h3 class="card-title">Network Status</h3>
                <p style="color: var(--text-muted); margin-bottom: 1rem;">All endpoints are currently responding within acceptable latency thresholds.</p>
                <div style="margin-top: auto; display: flex; align-items: center; gap: 0.5rem;">
                    <span style="width: 10px; height: 10px; border-radius: 50%; background: {accent_color}; display: inline-block;"></span>
                    <span style="font-weight: 600;">Systems Online</span>
                </div>
            </article>
        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Intersection Observer for staggered entrance animation
document.addEventListener('DOMContentLoaded', () => {{
    const cards = document.querySelectorAll('.bento-card');
    
    // Observer configuration
    const observerOptions = {{
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    }};

    const observer = new IntersectionObserver((entries, observer) => {{
        entries.forEach((entry, index) => {{
            if (entry.isIntersecting) {{
                // Stagger the animation based on DOM order
                setTimeout(() => {{
                    entry.target.classList.add('visible');
                }}, index * 100); 
                
                // Stop observing once visible
                observer.unobserve(entry.target);
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
