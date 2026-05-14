def create_component(
    output_dir: str,
    title_text: str = "Modern Layout Systems",
    body_text: str = "Showcasing Bento Grids, Grid Stacking, and Auto-Fit Wrapping.",
    color_scheme: str = "dark",        
    accent_color: str = "#3b82f6",     
    width_px: int = 1200,
    height_px: int = 900,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing Responsive Bento Grids & Wrapping layout patterns.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os
    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0f172a"          # Slate 900
        text_color = "#f8fafc"        # Slate 50
        text_muted = "#94a3b8"        # Slate 400
        surface_color = "#1e293b"     # Slate 800
        border_color = "#334155"      # Slate 700
        hover_surface = "#273449"
    else:
        bg_color = "#f8fafc"          # Slate 50
        text_color = "#0f172a"        # Slate 900
        text_muted = "#64748b"        # Slate 500
        surface_color = "#ffffff"     # White
        border_color = "#e2e8f0"      # Slate 200
        hover_surface = "#f1f5f9"

    # === CSS ===
    css = f"""/* CSS Grid Showcase: Bento, Stacking, & Auto-fit */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --surface: {surface_color};
    --border: {border_color};
    --hover-surface: {hover_surface};
    --accent: {accent_color};
    --max-width: {width_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    padding: 2rem;
    overflow-x: hidden;
}}

.main-wrapper {{
    width: 100%;
    max-width: var(--max-width);
    display: flex;
    flex-direction: column;
    gap: 4rem;
}}

/* Header Typography */
.header {{
    text-align: center;
    margin-bottom: 1rem;
}}
.header h1 {{
    font-size: clamp(2rem, 4vw, 3rem);
    font-weight: 700;
    letter-spacing: -0.03em;
    margin-bottom: 0.5rem;
}}
.header p {{
    color: var(--text-muted);
    font-size: 1.125rem;
}}

/* Component Titles */
.section-title {{
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}}
.section-title::before {{
    content: '';
    display: block;
    width: 12px;
    height: 12px;
    border-radius: 3px;
    background: var(--accent);
}}

/* Shared Card Styles */
.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 1.5rem;
    transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
    display: flex;
    flex-direction: column;
    justify-content: center;
    position: relative;
    overflow: hidden;
    opacity: 0;
    transform: translateY(20px);
}}

.card.animate-in {{
    opacity: 1;
    transform: translateY(0);
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 12px 24px -10px rgba(0, 0, 0, 0.15);
    border-color: var(--accent);
}}

/* =========================================
   SKILL 1: BENTO GRID (Explicit Areas)
   ========================================= */
.bento-grid {{
    display: grid;
    gap: 1.25rem;
    /* Implicit Grid Setup */
    grid-auto-columns: 1fr;
    grid-auto-rows: minmax(180px, auto);
    
    /* Desktop Area Mapping */
    grid-template-areas:
        "hero hero side top-right"
        "hero hero side bottom-right";
}}

.bento-hero {{ grid-area: hero; }}
.bento-side {{ grid-area: side; }}
.bento-tr {{ grid-area: top-right; }}
.bento-br {{ grid-area: bottom-right; }}

/* =========================================
   SKILL 2: GRID STACKING (Overlays)
   ========================================= */
.bento-hero {{
    display: grid;
    grid-template-areas: "stack";
    padding: 0;
    border: none;
}}

.hero-bg {{
    grid-area: stack;
    width: 100%;
    height: 100%;
    object-fit: cover;
    filter: brightness(0.6) saturate(1.2);
    border-radius: 20px;
    z-index: 1;
}}

.hero-content {{
    grid-area: stack;
    z-index: 2;
    place-self: end start; /* Align bottom left */
    padding: 2rem;
    color: #ffffff; /* Always white over dark image */
}}
.hero-content h2 {{
    font-size: 2rem;
    margin-bottom: 0.5rem;
}}

/* Bento Card Internal Content */
.card h3 {{
    font-size: 1.25rem;
    margin-bottom: 0.5rem;
    color: var(--text);
}}
.card p {{
    color: var(--text-muted);
    font-size: 0.95rem;
    line-height: 1.5;
}}
.icon-wrapper {{
    width: 48px;
    height: 48px;
    background: rgba(59, 130, 246, 0.1);
    color: var(--accent);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1rem;
    font-size: 1.5rem;
}}

/* =========================================
   SKILL 3: GRID WRAPPING (Auto-fit)
   ========================================= */
.wrap-grid {{
    display: grid;
    gap: 1.25rem;
    /* The Magic Line for Infinite Responsiveness */
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
}}

/* Responsive Breakpoints for Bento Grid */
@media (max-width: 1024px) {{
    .bento-grid {{
        /* Tablet Configuration */
        grid-template-areas:
            "hero hero side"
            "hero hero side"
            "top-right bottom-right .";
    }}
}}

@media (max-width: 768px) {{
    .bento-grid {{
        /* Mobile Configuration */
        grid-template-areas:
            "hero"
            "side"
            "top-right"
            "bottom-right";
        grid-auto-rows: minmax(150px, auto);
    }}
    
    .bento-hero {{
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="main-wrapper">
        <header class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>

        <!-- Skill 1 & 2: Explicit Bento Grid + Grid Stacking -->
        <section>
            <h2 class="section-title">Implicit Bento Grid & Stacking</h2>
            <div class="bento-grid">
                
                <!-- Hero Card (Demonstrating Grid Stacking) -->
                <div class="card bento-hero">
                    <img src="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=2400&auto=format&fit=crop" alt="Abstract landscape" class="hero-bg">
                    <div class="hero-content">
                        <h2>Grid Stacking</h2>
                        <p>Background and text share the same grid-area.<br>No position absolute required.</p>
                    </div>
                </div>

                <div class="card bento-side">
                    <div class="icon-wrapper">✦</div>
                    <h3>Area Mapping</h3>
                    <p>Rearrange entire layouts purely by changing string arrays in media queries. The HTML order remains completely untouched.</p>
                </div>

                <div class="card bento-tr">
                    <div class="icon-wrapper">▲</div>
                    <h3>Responsive</h3>
                    <p>Fluidly adapts to available screen real estate.</p>
                </div>

                <div class="card bento-br">
                    <div class="icon-wrapper">●</div>
                    <h3>Implicit Rows</h3>
                    <p>Row heights dynamically defined by minmax logic.</p>
                </div>

            </div>
        </section>

        <!-- Skill 3: Auto-fit Grid Wrapping -->
        <section>
            <h2 class="section-title">Auto-Fit Grid Wrapping</h2>
            <div class="wrap-grid">
                
                <div class="card">
                    <h3>Flexible Item 1</h3>
                    <p>Using <code>repeat(auto-fit, minmax(280px, 1fr))</code> allows columns to wrap and stretch to fill the row perfectly.</p>
                </div>
                <div class="card">
                    <h3>Flexible Item 2</h3>
                    <p>No media queries are needed for this section. The browser calculates the breakpoints mathematically.</p>
                </div>
                <div class="card">
                    <h3>Flexible Item 3</h3>
                    <p>Ideal for product lists, blog article cards, and dynamically populated galleries.</p>
                </div>
                <div class="card">
                    <h3>Flexible Item 4</h3>
                    <p>Notice how cards evenly distribute themselves when the container shrinks or grows.</p>
                </div>

            </div>
        </section>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Interaction Logic & Staggered Reveal Animations
document.addEventListener('DOMContentLoaded', () => {
    const cards = document.querySelectorAll('.card');
    
    // Setup Intersection Observer for smooth reveal
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                // Add the animation class
                entry.target.classList.add('animate-in');
                // Unobserve so it only happens once
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Add staggered delay to each card
    cards.forEach((card, index) => {
        card.style.transitionDelay = `${index * 50}ms`;
        observer.observe(card);
    });
});
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
