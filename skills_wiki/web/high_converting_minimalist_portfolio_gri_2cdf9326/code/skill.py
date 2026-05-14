def create_component(
    output_dir: str,
    title_text: str = "Design That Converts",
    body_text: str = "I help brands navigate their industry by solving complex problems through clean, strategic, and effective visual design.",
    color_scheme: str = "light",        
    accent_color: str = "#2563eb",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the High-Converting Minimalist Portfolio Grid.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0f1115"
        text_color = "#ffffff"
        text_muted = "#9ca3af"
        surface_color = "#1f2229"
        cta_text = "#ffffff" 
    else:
        bg_color = "#ffffff"
        text_color = "#111827"
        text_muted = "#4b5563"
        surface_color = "#f3f4f6"
        cta_text = "#ffffff" 

    # === CSS ===
    css = f"""/* High-Converting Minimalist Portfolio */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

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
    --cta-text: {cta_text};
    --max-width: {width_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
    overflow-x: hidden;
}}

.wrapper {{
    max-width: var(--max-width);
    margin: 0 auto;
    padding: 6rem 2rem;
}}

/* Header / Value Proposition */
.portfolio-header {{
    text-align: center;
    max-width: 800px;
    margin: 0 auto 5rem auto;
}}

.portfolio-header h1 {{
    font-size: clamp(2.5rem, 5vw, 4rem);
    font-weight: 700;
    line-height: 1.1;
    margin-bottom: 1.5rem;
    letter-spacing: -0.03em;
}}

.portfolio-header p {{
    font-size: clamp(1.125rem, 2vw, 1.25rem);
    color: var(--text-muted);
}}

/* Portfolio Grid */
.portfolio-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 2rem;
    margin-bottom: 6rem;
}}

.project-card {{
    position: relative;
    overflow: hidden;
    border-radius: 12px;
    cursor: pointer;
    aspect-ratio: 4 / 3;
    background: var(--surface);
    /* Fallback shadow */
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}}

.project-card img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.7s cubic-bezier(0.165, 0.84, 0.44, 1);
    display: block;
}}

.project-overlay {{
    position: absolute;
    inset: 0;
    background: linear-gradient(to top, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.2) 60%, rgba(0,0,0,0) 100%);
    opacity: 0;
    transition: opacity 0.4s ease;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    padding: 2rem;
    color: #ffffff;
}}

/* Hover States */
.project-card:hover img {{
    transform: scale(1.06);
}}

.project-card:hover .project-overlay {{
    opacity: 1;
}}

.project-title {{
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 0.25rem;
    transform: translateY(20px);
    transition: transform 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
}}

.project-context {{
    font-size: 0.95rem;
    color: rgba(255,255,255,0.8);
    transform: translateY(20px);
    transition: transform 0.4s cubic-bezier(0.165, 0.84, 0.44, 1) 0.05s;
}}

.project-solution {{
    font-size: 0.85rem;
    font-weight: 500;
    color: var(--accent);
    margin-top: 1rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    transform: translateY(20px);
    transition: transform 0.4s cubic-bezier(0.165, 0.84, 0.44, 1) 0.1s;
}}

.project-card:hover .project-title,
.project-card:hover .project-context,
.project-card:hover .project-solution {{
    transform: translateY(0);
}}

/* Call To Action Block */
.cta-section {{
    background: var(--surface);
    border-radius: 24px;
    padding: 5rem 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}}

.cta-section::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: var(--accent);
}}

.cta-section h2 {{
    font-size: clamp(2rem, 4vw, 3rem);
    font-weight: 700;
    margin-bottom: 1rem;
    letter-spacing: -0.02em;
}}

.cta-section p {{
    color: var(--text-muted);
    font-size: 1.125rem;
    margin-bottom: 2.5rem;
    max-width: 500px;
    margin-left: auto;
    margin-right: auto;
}}

.cta-button {{
    display: inline-block;
    background: var(--accent);
    color: var(--cta-text);
    padding: 1.25rem 3rem;
    font-size: 1.125rem;
    font-weight: 600;
    text-decoration: none;
    border-radius: 50px;
    transition: all 0.3s cubic-bezier(0.165, 0.84, 0.44, 1);
}}

.cta-button:hover {{
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    filter: brightness(110%);
}}

/* Scroll Reveal Animations */
.reveal {{
    opacity: 0;
    transform: translateY(40px);
    transition: opacity 0.8s cubic-bezier(0.165, 0.84, 0.44, 1), 
                transform 0.8s cubic-bezier(0.165, 0.84, 0.44, 1);
}}

.reveal.visible {{
    opacity: 1;
    transform: translateY(0);
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
    <div class="wrapper">
        
        <!-- Value Proposition -->
        <header class="portfolio-header reveal">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>

        <!-- Trust Signals / The Work -->
        <div class="portfolio-grid">
            
            <article class="project-card reveal">
                <img src="https://images.unsplash.com/photo-1600132806370-bf17e65e942f?auto=format&fit=crop&w=800&q=80" alt="Fintech Brand Identity">
                <div class="project-overlay">
                    <h3 class="project-title">Aura Financial</h3>
                    <p class="project-context">Brand Identity & App UI</p>
                    <p class="project-solution">Result: 40% Increase in User Onboarding</p>
                </div>
            </article>

            <article class="project-card reveal">
                <img src="https://images.unsplash.com/photo-1561070791-2526d30994b5?auto=format&fit=crop&w=800&q=80" alt="Coffee Packaging">
                <div class="project-overlay">
                    <h3 class="project-title">Origin Roasters</h3>
                    <p class="project-context">Packaging & Print Design</p>
                    <p class="project-solution">Result: Sold out initial run in 2 weeks</p>
                </div>
            </article>

            <article class="project-card reveal">
                <img src="https://images.unsplash.com/photo-1586717791821-3f44a563fa4c?auto=format&fit=crop&w=800&q=80" alt="SaaS Dashboard Design">
                <div class="project-overlay">
                    <h3 class="project-title">Nexus Metrics</h3>
                    <p class="project-context">UX Research & Dashboard UI</p>
                    <p class="project-solution">Result: Reduced client churn by 15%</p>
                </div>
            </article>

            <article class="project-card reveal">
                <img src="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80" alt="Editorial Typography">
                <div class="project-overlay">
                    <h3 class="project-title">Vanguard Magazine</h3>
                    <p class="project-context">Editorial Layout & Typography</p>
                    <p class="project-solution">Result: Won AIGA Design Excellence Award</p>
                </div>
            </article>

            <article class="project-card reveal">
                <img src="https://images.unsplash.com/photo-1634942537034-2531766767d1?auto=format&fit=crop&w=800&q=80" alt="Skincare E-commerce">
                <div class="project-overlay">
                    <h3 class="project-title">Lumina Skincare</h3>
                    <p class="project-context">E-commerce Web Design</p>
                    <p class="project-solution">Result: Doubled mobile conversion rate</p>
                </div>
            </article>

            <article class="project-card reveal">
                <img src="https://images.unsplash.com/photo-1558655146-d09347e92766?auto=format&fit=crop&w=800&q=80" alt="Restaurant Signage">
                <div class="project-overlay">
                    <h3 class="project-title">Osteria 1920</h3>
                    <p class="project-context">Logo & Wayfinding Signage</p>
                    <p class="project-solution">Result: Revitalized local brand presence</p>
                </div>
            </article>

        </div>

        <!-- Conversion / User Path End -->
        <section class="cta-section reveal">
            <h2>Ready to elevate your brand?</h2>
            <p>Let's discuss how we can solve your design challenges and drive real results.</p>
            <a href="#" class="cta-button">Start a Project</a>
        </section>

    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Scroll Reveal Logic for high-end feel
document.addEventListener('DOMContentLoaded', () => {
    
    const observerOptions = {
        root: null,
        rootMargin: '0px 0px -50px 0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                // Stop observing once revealed
                obs.unobserve(entry.target); 
            }
        });
    }, observerOptions);

    const revealElements = document.querySelectorAll('.reveal');
    
    // Add staggered delay to grid items specifically for a cascading entrance
    let gridItemCount = 0;
    revealElements.forEach((el) => {
        if (el.classList.contains('project-card')) {
            el.style.transitionDelay = `${(gridItemCount % 3) * 0.1}s`;
            gridItemCount++;
        }
        observer.observe(el);
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
