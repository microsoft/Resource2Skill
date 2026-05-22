def create_component(
    output_dir: str,
    title_text: str = "Bento Grid Mastery",
    body_text: str = "Building asymmetric layouts with CSS Grid Areas and Stacking.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#8b5cf6",     # Default purple accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Bento Grid UI.
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_color = "#f8fafc"
        text_muted = "#cbd5e1"
        surface_color = "#1e293b"
        border_color = "#334155"
        shadow_color = "rgba(0,0,0,0.4)"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        text_muted = "#475569"
        surface_color = "#ffffff"
        border_color = "#e2e8f0"
        shadow_color = "rgba(0,0,0,0.05)"

    # === CSS ===
    css = f"""/* Bento Grid UI & Grid Stacking */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --surface: {surface_color};
    --border: {border_color};
    --shadow: {shadow_color};
    --max-width: {width_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 2rem;
}}

.header {{
    text-align: center;
    margin-bottom: 3rem;
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

/* -- Core Bento Grid -- */
.bento-grid {{
    display: grid;
    width: 100%;
    max-width: var(--max-width);
    /* 4 Column layout for Desktop */
    grid-template-columns: repeat(4, 1fr);
    grid-auto-rows: minmax(220px, auto);
    gap: 1.5rem;
    
    /* Visual layout mapping */
    grid-template-areas: 
        "hero hero card1 card2"
        "hero hero card3 card4";
}}

/* -- Bento Cards Base -- */
.bento-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 24px;
    padding: 1.5rem;
    overflow: hidden;
    position: relative;
    box-shadow: 0 4px 6px -1px var(--shadow);
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s ease;
    display: flex;
    flex-direction: column;
}}

.bento-card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 10px 15px -3px var(--shadow), 0 0 0 2px var(--accent);
}}

/* Assigning Areas */
.hero  {{ grid-area: hero; padding: 0; border: none; }}
.card1 {{ grid-area: card1; }}
.card2 {{ grid-area: card2; }}
.card3 {{ grid-area: card3; }}
.card4 {{ grid-area: card4; }}

/* -- Grid Stacking Concept (Hero Card) -- */
.hero {{
    display: grid;
    /* Create a single cell grid */
    grid-template-columns: 1fr;
    grid-template-rows: 1fr;
    border-radius: 24px;
}}

/* Target all direct children of the hero and place them in the exact same cell */
.hero > * {{
    grid-area: 1 / 1 / -1 / -1;
}}

.hero-bg {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 24px;
    z-index: 1;
}}

.hero-overlay {{
    background: linear-gradient(to top, rgba(15,23,42,0.95) 0%, rgba(15,23,42,0.2) 60%, transparent 100%);
    border-radius: 24px;
    z-index: 2;
}}

.hero-content {{
    z-index: 3;
    /* Place the content at the bottom left using place-self */
    place-self: end start;
    padding: 2.5rem;
    color: #ffffff; /* Always white due to dark overlay */
}}

.hero-content h2 {{
    font-size: 2.2rem;
    font-weight: 700;
    margin-bottom: 0.75rem;
    line-height: 1.1;
}}

.hero-content p {{
    color: #cbd5e1;
    font-size: 1.05rem;
    max-width: 80%;
}}

/* -- Standard Card Content -- */
.card-icon {{
    display: flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    border-radius: 12px;
    background: color-mix(in srgb, var(--accent) 15%, transparent);
    color: var(--accent);
    margin-bottom: 1.25rem;
}}

.card-icon svg {{
    width: 24px;
    height: 24px;
}}

.bento-card h3 {{
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}}

.bento-card p {{
    color: var(--text-muted);
    font-size: 0.95rem;
    line-height: 1.5;
    flex-grow: 1;
}}

/* -- Responsive Restructuring -- */

/* Tablet: 2 Columns */
@media (max-width: 900px) {{
    .bento-grid {{
        grid-template-columns: repeat(2, 1fr);
        grid-template-areas: 
            "hero hero"
            "hero hero"
            "card1 card2"
            "card3 card4";
    }}
}}

/* Mobile: 1 Column */
@media (max-width: 600px) {{
    .bento-grid {{
        grid-template-columns: 1fr;
        grid-auto-rows: minmax(200px, auto);
        grid-template-areas: 
            "hero"
            "hero"
            "card1"
            "card2"
            "card3"
            "card4";
    }}
    .hero-content {{ padding: 1.5rem; }}
    .hero-content h2 {{ font-size: 1.75rem; }}
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
    
    <div class="header">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </div>

    <div class="bento-grid">
        
        <!-- Hero Card utilizing Grid Stacking -->
        <div class="bento-card hero">
            <img class="hero-bg" src="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=2564&auto=format&fit=crop" alt="Abstract Art">
            <div class="hero-overlay"></div>
            <div class="hero-content">
                <h2>Grid Stacking Power</h2>
                <p>These elements are layered without position: absolute. They simply share the same grid cell.</p>
            </div>
        </div>

        <!-- Small Card 1 -->
        <div class="bento-card card1">
            <div class="card-icon">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
            </div>
            <h3>Responsive Areas</h3>
            <p>Rearrange entire layouts using text strings in media queries.</p>
        </div>

        <!-- Small Card 2 -->
        <div class="bento-card card2">
            <div class="card-icon">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z"></path></svg>
            </div>
            <h3>Alignment</h3>
            <p>Perfect vertical and horizontal centering out of the box.</p>
        </div>

        <!-- Small Card 3 -->
        <div class="bento-card card3">
            <div class="card-icon">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7v8a2 2 0 002 2h6M8 7V5a2 2 0 012-2h4.586a1 1 0 01.707.293l4.414 4.414a1 1 0 01.293.707V15a2 2 0 01-2 2h-2M8 7H6a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2v-2"></path></svg>
            </div>
            <h3>Fluid Tracks</h3>
            <p>Using minmax() to ensure tracks scale gracefully.</p>
        </div>

        <!-- Small Card 4 -->
        <div class="bento-card card4">
            <div class="card-icon">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>
            </div>
            <h3>Viewports</h3>
            <p>Auto-fits content beautifully across all modern screens.</p>
        </div>

    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Optional: Add subtle entry animations via JS
document.addEventListener('DOMContentLoaded', () => {
    const cards = document.querySelectorAll('.bento-card');
    
    // Set initial state
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = `opacity 0.6s ease ${index * 0.1}s, transform 0.6s ease ${index * 0.1}s`;
    });

    // Trigger reflow and play animation
    setTimeout(() => {
        cards.forEach(card => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
            
            // Cleanup inline transition after entry so hover states take over
            setTimeout(() => {
                card.style.transition = 'transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s ease';
            }, 1000);
        });
    }, 100);
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
