def create_component(
    output_dir: str,
    title_text: str = "Modern Fluid Layouts",
    body_text: str = "Experience the power of CSS Grid stacking and auto-fit minmax() algorithms. Resize your browser to see the fluid wrapping in action.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#6366f1",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Auto-fit Bento Grid & Stack Layout.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0a0a0f"
        text_color = "#ffffff"
        text_muted = "#a0a0ab"
        card_bg = "#14141f"
        overlay_color = "rgba(10, 10, 15, 0.6)"
        card_shadow = "0 20px 40px rgba(0, 0, 0, 0.4)"
    else:
        bg_color = "#f4f4f6"
        text_color = "#111118"
        text_muted = "#555562"
        card_bg = "#ffffff"
        overlay_color = "rgba(255, 255, 255, 0.7)"
        card_shadow = "0 15px 35px rgba(0, 0, 0, 0.05)"

    # === CSS ===
    css = f"""/* Auto-fit Bento Grid & Stack Layout */
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
    --card-bg: {card_bg};
    --overlay: {overlay_color};
    --shadow: {card_shadow};
    --container-width: {width_px}px;
    --min-height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: var(--min-height);
    display: flex;
    flex-direction: column;
    align-items: center;
    overflow-x: hidden;
    line-height: 1.6;
}}

/* Layout Wrapper */
.layout-container {{
    width: 100%;
    max-width: var(--container-width);
    padding: 2rem;
    margin: 0 auto;
}}

/* 1. Grid Stacking Pattern (Hero) */
.hero-stack {{
    display: grid;
    grid-template-areas: "stack";
    width: 100%;
    border-radius: 24px;
    overflow: hidden;
    margin-bottom: 4rem;
    box-shadow: var(--shadow);
}}

.hero-stack > * {{
    grid-area: stack;
}}

.hero-stack .hero-img {{
    width: 100%;
    height: 100%;
    min-height: 400px;
    object-fit: cover;
    z-index: 1;
}}

.hero-stack .hero-content {{
    z-index: 2;
    background: var(--overlay);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 3rem;
}}

.hero-content h1 {{
    font-size: clamp(2.5rem, 5vw, 4.5rem);
    font-weight: 800;
    letter-spacing: -0.03em;
    margin-bottom: 1rem;
    background: linear-gradient(135deg, var(--text), var(--accent));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

.hero-content p {{
    font-size: clamp(1rem, 2vw, 1.25rem);
    max-width: 600px;
    color: var(--text);
    opacity: 0.9;
    margin-bottom: 2rem;
}}

.hero-content .cta-btn {{
    background: var(--accent);
    color: #ffffff;
    border: none;
    padding: 1rem 2rem;
    font-size: 1rem;
    font-weight: 600;
    border-radius: 50px;
    cursor: pointer;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}

.hero-content .cta-btn:hover {{
    transform: translateY(-2px);
    box-shadow: 0 10px 20px {accent_color}66;
}}

/* 2. Responsive Auto-Fit Grid Pattern */
.auto-grid {{
    display: grid;
    /* THE MAGIC CSS: Auto wraps based on available space */
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    padding-bottom: 4rem;
}}

/* Grid Cards */
.card {{
    background: var(--card-bg);
    border-radius: 16px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    box-shadow: var(--shadow);
    transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    opacity: 0;
    transform: translateY(30px);
}}

.card.visible {{
    opacity: 1;
    transform: translateY(0);
}}

.card:hover {{
    transform: translateY(-8px);
    box-shadow: 0 25px 50px rgba(0,0,0,0.2);
}}

/* Reusing grid stack inside smaller cards */
.card-image-stack {{
    display: grid;
    grid-template-areas: "stack";
    height: 220px;
}}

.card-image-stack > * {{
    grid-area: stack;
}}

.card-image-stack img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    z-index: 1;
    transition: transform 0.5s ease;
}}

.card:hover .card-image-stack img {{
    transform: scale(1.05);
}}

.card-badge {{
    z-index: 2;
    align-self: start;
    justify-self: end;
    margin: 1rem;
    background: var(--accent);
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
}}

.card-content {{
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    flex-grow: 1;
}}

.card-content h3 {{
    font-size: 1.25rem;
    margin-bottom: 0.5rem;
}}

.card-content p {{
    color: var(--text-muted);
    font-size: 0.95rem;
    margin-bottom: 1.5rem;
    flex-grow: 1;
}}

.card-content a {{
    color: var(--accent);
    text-decoration: none;
    font-weight: 600;
    font-size: 0.95rem;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
}}

.card-content a::after {{
    content: "→";
    transition: transform 0.2s ease;
}}

.card-content a:hover::after {{
    transform: translateX(4px);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="layout-container">
        
        <!-- Pattern 1: Grid Stacking -->
        <header class="hero-stack">
            <img class="hero-img" src="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=2400&auto=format&fit=crop" alt="Abstract architectural structure" />
            <div class="hero-content">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
                <button class="cta-btn">Explore Grid Layouts</button>
            </div>
        </header>

        <!-- Pattern 2: Auto-fit Responsive Grid -->
        <main class="auto-grid">
            <!-- Card 1 -->
            <article class="card">
                <div class="card-image-stack">
                    <img src="https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=600&auto=format&fit=crop" alt="Cybersecurity" />
                    <span class="card-badge">New</span>
                </div>
                <div class="card-content">
                    <h3>Adaptive Columns</h3>
                    <p>Using the auto-fit algorithm, this card will automatically wrap to the next row when the browser viewport shrinks below the threshold.</p>
                    <a href="#">Learn more</a>
                </div>
            </article>

            <!-- Card 2 -->
            <article class="card">
                <div class="card-image-stack">
                    <img src="https://images.unsplash.com/photo-1620641788421-7a1c342ea42e?q=80&w=600&auto=format&fit=crop" alt="Abstract Gradient" />
                </div>
                <div class="card-content">
                    <h3>Minmax Flexibility</h3>
                    <p>The minmax() function ensures that a column never shrinks below 300px, but allows it to stretch infinitely (1fr) to fill remaining space.</p>
                    <a href="#">View examples</a>
                </div>
            </article>

            <!-- Card 3 -->
            <article class="card">
                <div class="card-image-stack">
                    <img src="https://images.unsplash.com/photo-1563089145-599997674d42?q=80&w=600&auto=format&fit=crop" alt="Neon lights" />
                    <span class="card-badge">Pro Tip</span>
                </div>
                <div class="card-content">
                    <h3>No Media Queries</h3>
                    <p>Notice how this entire layout requires zero breakpoint media queries. The browser's native layout engine handles all the spatial math.</p>
                    <a href="#">See the code</a>
                </div>
            </article>

            <!-- Card 4 -->
            <article class="card">
                <div class="card-image-stack">
                    <img src="https://images.unsplash.com/photo-1558655146-d09347e92766?q=80&w=600&auto=format&fit=crop" alt="Design elements" />
                </div>
                <div class="card-content">
                    <h3>Grid Stacking</h3>
                    <p>Overlays inside these cards are achieved via grid-area sharing a 1x1 cell, ensuring perfectly measured containers without absolute bugs.</p>
                    <a href="#">Read tutorial</a>
                </div>
            </article>
        </main>
        
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Auto-fit Bento Grid & Stack Layout - Interactive Behavior
document.addEventListener('DOMContentLoaded', () => {{
    
    // Intersection Observer for scroll-reveal staggered animations
    const cards = document.querySelectorAll('.card');
    
    const observerOptions = {{
        root: null,
        rootMargin: '0px 0px -50px 0px',
        threshold: 0.1
    }};

    const cardObserver = new IntersectionObserver((entries, observer) => {{
        entries.forEach((entry, index) => {{
            if (entry.isIntersecting) {{
                // Apply staggered delay based on horizontal position (simulated via index)
                setTimeout(() => {{
                    entry.target.classList.add('visible');
                }}, index * 100);
                
                // Stop observing once revealed
                observer.unobserve(entry.target);
            }}
        }});
    }}, observerOptions);

    cards.forEach(card => {{
        cardObserver.observe(card);
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
