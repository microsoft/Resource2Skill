def create_component(
    output_dir: str,
    title_text: str = "Overview Dashboard",
    body_text: str = "A comprehensive look at your metrics.",
    color_scheme: str = "dark",        
    accent_color: str = "#8a2be2",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Bento Grid with Grid Stacking.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#0a0a0f"
        text_color = "#ffffff"
        text_muted = "#a0a0a5"
        surface_color = "rgba(255, 255, 255, 0.04)"
        surface_hover = "rgba(255, 255, 255, 0.08)"
        border_color = "rgba(255, 255, 255, 0.1)"
    else:
        bg_color = "#f4f5f7"
        text_color = "#111118"
        text_muted = "#505055"
        surface_color = "#ffffff"
        surface_hover = "#fafafa"
        border_color = "rgba(0, 0, 0, 0.08)"

    css = f"""/* Responsive Bento Grid — generated component */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --surface: {surface_color};
    --surface-hover: {surface_hover};
    --border: {border_color};
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
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    overflow-x: hidden;
}}

.wrapper {{
    width: 100%;
    max-width: var(--width);
}}

.header {{
    margin-bottom: 2rem;
    text-align: left;
}}

.header h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
}}

.header p {{
    color: var(--text-muted);
    font-size: 1.1rem;
}}

/* Macro Layout: The Bento Grid */
.bento-grid {{
    display: grid;
    gap: 1.5rem;
    /* 4 Columns by default */
    grid-template-columns: repeat(4, 1fr);
    grid-auto-rows: minmax(200px, auto);
    
    /* The Magic String Map defining the layout */
    grid-template-areas:
        "hero hero stats1 stats2"
        "hero hero wide wide"
        "box1 box2 wide wide";
}}

/* Assigning elements to grid areas */
.bento-hero {{ grid-area: hero; }}
.bento-stats1 {{ grid-area: stats1; }}
.bento-stats2 {{ grid-area: stats2; }}
.bento-wide {{ grid-area: wide; }}
.bento-box1 {{ grid-area: box1; }}
.bento-box2 {{ grid-area: box2; }}

/* Base Card Styling */
.bento-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 1.5rem;
    padding: 1.5rem;
    overflow: hidden;
    transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    
    /* Animation initial state */
    opacity: 0;
    transform: translateY(20px);
}}

.bento-card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(0,0,0,0.1);
    border-color: var(--accent);
    background: var(--surface-hover);
}}

/* Card Content Styling */
.bento-card h3 {{
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}}

.bento-card p {{
    color: var(--text-muted);
    font-size: 0.95rem;
    line-height: 1.5;
}}

.bento-card .metric {{
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--accent);
    margin-top: auto;
    padding-top: 1rem;
}}

/* Micro Layout: Grid Stacking (Video Tutorial Highlight) */
.grid-stack {{
    display: grid;
    padding: 0; /* Remove padding to let image bleed */
}}

.grid-stack > * {{
    /* Force all children into cell row 1, col 1 */
    grid-column: 1 / 2;
    grid-row: 1 / 2;
}}

.grid-stack img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    z-index: 1;
}}

.grid-stack .overlay {{
    background: linear-gradient(to top, rgba(0,0,0,0.9) 0%, rgba(0,0,0,0.2) 50%, rgba(0,0,0,0) 100%);
    z-index: 2;
}}

.grid-stack .content {{
    z-index: 3;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    color: white; /* Always white over dark overlay */
}}

.grid-stack .content h3 {{ color: white; }}
.grid-stack .content p {{ color: rgba(255,255,255,0.8); }}

/* Responsive Grid Wrapping via Media Queries */
@media (max-width: 1024px) {{
    .bento-grid {{
        /* Shift to 2 columns */
        grid-template-columns: repeat(2, 1fr);
        grid-template-areas:
            "hero hero"
            "hero hero"
            "stats1 stats2"
            "wide wide"
            "box1 box2";
    }}
}}

@media (max-width: 600px) {{
    .header h1 {{ font-size: 2rem; }}
    
    .bento-grid {{
        /* Shift to 1 column */
        grid-template-columns: 1fr;
        grid-template-areas:
            "hero"
            "stats1"
            "stats2"
            "wide"
            "box1"
            "box2";
    }}
    
    .bento-hero {{
        min-height: 300px;
    }}
}}

/* Utility for animation */
.bento-card.visible {{
    opacity: 1;
    transform: translateY(0);
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
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
            <!-- Hero Card (Using Grid Stacking trick) -->
            <article class="bento-card bento-hero grid-stack">
                <img src="https://images.unsplash.com/photo-1557683316-973673baf926?q=80&w=1200&auto=format&fit=crop" alt="Abstract Gradient">
                <div class="overlay"></div>
                <div class="content">
                    <h3>Performance Deep Dive</h3>
                    <p>Analyze your real-time traffic, interactions, and conversion funnels to scale your product faster.</p>
                </div>
            </article>

            <!-- Standard Cards -->
            <article class="bento-card bento-stats1">
                <h3>Total Revenue</h3>
                <p>Up from last quarter</p>
                <div class="metric">$42.8k</div>
            </article>

            <article class="bento-card bento-stats2">
                <h3>Active Users</h3>
                <p>Currently online</p>
                <div class="metric">1,402</div>
            </article>

            <!-- Wide Card (Using Grid Stacking trick) -->
            <article class="bento-card bento-wide grid-stack">
                <img src="https://images.unsplash.com/photo-1550684848-fac1c5b4e853?q=80&w=1200&auto=format&fit=crop" alt="Data Analytics">
                <div class="overlay"></div>
                <div class="content">
                    <h3>Global Reach</h3>
                    <p>Your systems are currently serving requests from 42 different countries with zero latency spikes.</p>
                </div>
            </article>

            <article class="bento-card bento-box1">
                <h3>Server Load</h3>
                <p>Current CPU usage across all active containers.</p>
                <div class="metric" style="color: #00d2ff;">24%</div>
            </article>

            <article class="bento-card bento-box2">
                <h3>Error Rate</h3>
                <p>Reported anomalies in the last 24 hours.</p>
                <div class="metric" style="color: #ff3366;">0.1%</div>
            </article>
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Intersection Observer for staggered entrance animations
document.addEventListener('DOMContentLoaded', () => {{
    const cards = document.querySelectorAll('.bento-card');
    
    const observerOptions = {{
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    }};

    const observer = new IntersectionObserver((entries, observer) => {{
        entries.forEach((entry, index) => {{
            if (entry.isIntersecting) {{
                // Stagger the animation based on the element's order
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
