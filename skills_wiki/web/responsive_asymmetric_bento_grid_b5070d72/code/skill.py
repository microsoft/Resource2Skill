def create_component(
    output_dir: str,
    title_text: str = "Platform Capabilities",
    body_text: str = "Everything you need to scale your workflow, packed into a single, lightning-fast interface.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#6366f1",     # Deep indigo/purple accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Asymmetric Bento Grid.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#09090b"  # Zinc 950
        text_main = "#fafafa" # Zinc 50
        text_muted = "#a1a1aa" # Zinc 400
        card_bg = "rgba(255, 255, 255, 0.03)"
        card_border = "rgba(255, 255, 255, 0.08)"
        card_hover_border = "rgba(255, 255, 255, 0.2)"
    else:
        bg_color = "#f4f4f5"  # Zinc 100
        text_main = "#09090b" # Zinc 950
        text_muted = "#52525b" # Zinc 600
        card_bg = "#ffffff"
        card_border = "rgba(0, 0, 0, 0.05)"
        card_hover_border = "rgba(0, 0, 0, 0.15)"

    # === CSS ===
    css = f"""/* Responsive Asymmetric Bento Grid */
:root {{
    --bg-color: {bg_color};
    --text-main: {text_main};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --card-bg: {card_bg};
    --card-border: {card_border};
    --card-hover: {card_hover_border};
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-main);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px 20px;
}}

.section-header {{
    text-align: center;
    max-width: 600px;
    margin-bottom: 48px;
}}

.section-title {{
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    margin-bottom: 16px;
}}

.section-subtitle {{
    font-size: 1.125rem;
    color: var(--text-muted);
    line-height: 1.6;
}}

/* --- THE BENTO GRID --- */
.bento-grid {{
    display: grid;
    width: 100%;
    max-width: {width_px}px;
    /* Baseline 3x3 layout for desktop */
    grid-template-columns: repeat(3, 1fr);
    grid-auto-rows: minmax(220px, auto);
    gap: 24px;
    
    /* The Magic: Mapping out the asymmetric layout visually */
    grid-template-areas: 
        "hero hero top-right"
        "hero hero mid-right"
        "bot-left bottom bottom";
}}

/* Target areas based on grid mapping */
.card-hero {{ grid-area: hero; }}
.card-tr {{ grid-area: top-right; }}
.card-mr {{ grid-area: mid-right; }}
.card-bl {{ grid-area: bot-left; }}
.card-bot {{ grid-area: bottom; }}

/* Card Styling */
.bento-card {{
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 24px;
    padding: 32px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    
    /* Animation initial state */
    opacity: 0;
    transform: translateY(20px);
}}

.bento-card.visible {{
    opacity: 1;
    transform: translateY(0);
}}

.bento-card:hover {{
    transform: translateY(-4px) scale(1.01);
    border-color: var(--card-hover);
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
}}

/* Specific Card Internals */
.card-hero {{
    background: linear-gradient(135deg, var(--card-bg) 0%, var(--card-bg) 100%);
    position: relative;
    overflow: hidden;
    justify-content: flex-end;
}}

/* Inject accent color into hero card */
.card-hero::before {{
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 300px; height: 300px;
    background: var(--accent);
    filter: blur(100px);
    opacity: 0.15;
    border-radius: 50%;
    z-index: 0;
    pointer-events: none;
}}

.card-title {{
    font-size: 1.5rem;
    font-weight: 600;
    z-index: 1;
}}

.card-hero .card-title {{
    font-size: 2.25rem;
    line-height: 1.1;
}}

.card-desc {{
    color: var(--text-muted);
    font-size: 1rem;
    line-height: 1.5;
    z-index: 1;
}}

.stat-number {{
    font-size: 3rem;
    font-weight: 700;
    color: var(--accent);
    margin-top: auto;
}}

/* --- RESPONSIVE ADJUSTMENTS --- */

/* Tablet layout */
@media (max-width: 900px) {{
    .bento-grid {{
        grid-template-columns: repeat(2, 1fr);
        grid-template-areas: 
            "hero hero"
            "hero hero"
            "top-right mid-right"
            "bottom bottom"
            "bot-left bot-left";
    }}
}}

/* Mobile layout */
@media (max-width: 600px) {{
    .bento-grid {{
        grid-template-columns: 1fr;
        grid-auto-rows: minmax(180px, auto);
        /* Simple stack on mobile */
        grid-template-areas: 
            "hero"
            "top-right"
            "mid-right"
            "bottom"
            "bot-left";
    }}
    
    .card-hero .card-title {{
        font-size: 1.75rem;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <header class="section-header">
        <h1 class="section-title">{title_text}</h1>
        <p class="section-subtitle">{body_text}</p>
    </header>

    <!-- Bento Grid Container -->
    <main class="bento-grid" id="bento-grid">
        
        <!-- Main Feature (Spans 2x2) -->
        <div class="bento-card card-hero">
            <h2 class="card-title">Real-time collaboration engine</h2>
            <p class="card-desc">Work together with your entire team seamlessly without merge conflicts or loading screens. Built on modern web sockets.</p>
        </div>

        <!-- Top Right Small Feature -->
        <div class="bento-card card-tr">
            <h2 class="card-title">Lightning Fast</h2>
            <p class="card-desc">Global edge CDN deployment ensures sub-50ms latency.</p>
            <div class="stat-number">48<span style="font-size: 1.5rem">ms</span></div>
        </div>

        <!-- Mid Right Small Feature -->
        <div class="bento-card card-mr">
            <h2 class="card-title">Uptime SLA</h2>
            <p class="card-desc">Enterprise-grade reliability you can trust.</p>
            <div class="stat-number">99.9%</div>
        </div>

        <!-- Bottom Wide Feature -->
        <div class="bento-card card-bot">
            <h2 class="card-title">Advanced Analytics & Reporting</h2>
            <p class="card-desc">Turn raw data into actionable insights instantly. Custom dashboards allow you to track the metrics that actually matter to your business.</p>
        </div>

        <!-- Bottom Left Small Feature -->
        <div class="bento-card card-bl">
            <h2 class="card-title">Security First</h2>
            <p class="card-desc">SOC2 compliant with end-to-end encryption.</p>
        </div>

    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Staggered entrance animation for Bento Grid
document.addEventListener('DOMContentLoaded', () => {{
    const cards = document.querySelectorAll('.bento-card');
    
    // Setup Intersection Observer
    const observerOptions = {{
        root: null,
        rootMargin: '0px',
        threshold: 0.15 // Trigger when 15% of the card is visible
    }};

    const observer = new IntersectionObserver((entries, observer) => {{
        entries.forEach((entry, index) => {{
            if (entry.isIntersecting) {{
                // Add a slight stagger delay based on DOM order
                setTimeout(() => {{
                    entry.target.classList.add('visible');
                }}, index * 100); 
                
                // Stop observing once animated
                observer.unobserve(entry.target);
            }}
        }});
    }}, observerOptions);

    // Apply observer to all cards
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
