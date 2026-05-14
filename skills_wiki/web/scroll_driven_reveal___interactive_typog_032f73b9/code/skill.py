def create_component(
    output_dir: str,
    title_text: str = "Welcome to",
    body_text: str = "Tomorrow isn't just a cookie company, it's a revolution in the world of sweets.",
    color_scheme: str = "dark",
    accent_color: str = "#cc3f4e",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Scroll-Driven Reveal & Interactive Typography effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#131217"
        text_color = "#ffffff"
        surface_color = "#1e1d24"
        muted_text = "#a0a0a0"
    else:
        bg_color = "#f4f4f5"
        text_color = "#111827"
        surface_color = "#ffffff"
        muted_text = "#6b7280"

    # === CSS ===
    css = f"""/* Scroll-Driven Reveal & Interactive Typography */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --accent-color: {accent_color};
    --surface-color: {surface_color};
    --muted-text: {muted_text};
    --container-width: {width_px}px;
    --container-height: {height_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: #000; /* Outer background */
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    overflow: hidden;
}}

.app-container {{
    width: var(--container-width);
    height: var(--container-height);
    background-color: var(--bg-color);
    color: var(--text-color);
    overflow-y: auto;
    overflow-x: hidden;
    position: relative;
    box-shadow: 0 0 50px rgba(0,0,0,0.5);
    scroll-behavior: smooth;
}}

/* Typography */
h1 {{
    font-size: 4rem;
    line-height: 1.1;
    font-weight: 800;
    margin-bottom: 2rem;
    letter-spacing: -0.02em;
}}

h2 {{
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 1.5rem;
}}

p {{
    font-size: 1.25rem;
    color: var(--muted-text);
    line-height: 1.6;
    max-width: 600px;
}}

/* Layout Sections */
.section {{
    min-height: 80vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 4rem 10%;
}}

.section.center {{
    align-items: center;
    text-align: center;
}}

/* Animated Hero Keyword */
.keyword {{
    color: var(--accent-color);
    display: inline-block;
    position: relative;
    opacity: 0;
    /* text-decoration wavy simulates the squiggly line from the video */
    text-decoration: underline wavy var(--accent-color);
    text-underline-offset: 8px;
    text-decoration-thickness: 3px;
    
    /* The animation execution */
    animation: slideInKeyword 0.6s cubic-bezier(0.2, 0.8, 0.2, 1) 0.5s forwards;
}}

@keyframes slideInKeyword {{
    0% {{
        opacity: 0;
        transform: translateX(-60%);
    }}
    100% {{
        opacity: 1;
        transform: translateX(0);
    }}
}}

/* Custom CTA Button with Expanding pseudo-element */
.cta-button {{
    color: var(--text-color);
    background-color: transparent;
    border: none;
    font-size: 1.25rem;
    font-weight: 700;
    position: relative;
    padding: 16px 24px;
    margin-top: 2rem;
    cursor: pointer;
    z-index: 1;
    display: inline-flex;
    align-items: center;
    font-family: inherit;
}}

.cta-button::after {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    width: 64px; /* Starting block width */
    background-color: var(--accent-color);
    z-index: -1;
    transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}}

.cta-button:hover::after {{
    width: 100%;
}}

/* Scroll Reveal Utility Classes */
.scroll-reveal {{
    opacity: 0;
    transform: translateY(40px);
    transition: all 0.8s cubic-bezier(0.2, 0.8, 0.2, 1);
}}

.scroll-reveal.visible {{
    opacity: 1;
    transform: translateY(0);
}}

/* Feature Card Layout */
.feature-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-top: 3rem;
}}

.feature-card {{
    background: var(--surface-color);
    padding: 2.5rem;
    border-radius: 8px;
    border-top: 4px solid var(--accent-color);
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text} Tomorrow</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-container" id="scroll-root">
        
        <!-- Hero Section -->
        <section class="section">
            <div>
                <h1>
                    {title_text}<br>
                    <span class="keyword">tomorrow</span><br>
                    we got cookies
                </h1>
                <button class="cta-button">Order now!</button>
            </div>
        </section>

        <!-- Feature Section 1 -->
        <section class="section">
            <h2 class="scroll-reveal">Innovation at Its Core</h2>
            <p class="scroll-reveal">{body_text}</p>
            
            <div class="feature-grid">
                <div class="feature-card scroll-reveal">
                    <h3 style="margin-bottom: 1rem; color: var(--accent-color);">Custom Shapes</h3>
                    <p>Every cookie is mathematically engineered for optimal crunch dynamics.</p>
                </div>
                <div class="feature-card scroll-reveal" style="transition-delay: 0.2s;">
                    <h3 style="margin-bottom: 1rem; color: var(--accent-color);">Hyper-Flavor</h3>
                    <p>Next-gen flavor profiles crafted by algorithmic taste optimization.</p>
                </div>
            </div>
        </section>

        <!-- Final CTA Section -->
        <section class="section center">
            <h2 class="scroll-reveal">Custom Cookies</h2>
            <p class="scroll-reveal" style="margin: 0 auto;">Make your own today!</p>
            <div class="scroll-reveal" style="transition-delay: 0.2s;">
                <button class="cta-button">Start Building</button>
            </div>
        </section>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Scroll-Driven Reveal & Interactive Typography
document.addEventListener('DOMContentLoaded', () => {
    // We observe elements specifically within our custom scrollable container
    const scrollContainer = document.getElementById('scroll-root');
    
    // Setup IntersectionObserver for high-performance scroll triggers
    const observerOptions = {
        root: scrollContainer,
        rootMargin: '0px 0px -50px 0px', // Trigger slightly before it enters the viewport
        threshold: 0.1 // Trigger when 10% of the element is visible
    };

    const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Add the CSS class that triggers the transition
                entry.target.classList.add('visible');
                
                // Unobserve after animating so it doesn't repeat on scroll up
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Find all elements with the scroll-reveal class and observe them
    const revealElements = document.querySelectorAll('.scroll-reveal');
    revealElements.forEach(el => revealObserver.observe(el));
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
