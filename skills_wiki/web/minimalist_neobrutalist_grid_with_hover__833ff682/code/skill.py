def create_component(
    output_dir: str,
    title_text: str = "Recent Projects",
    body_text: str = "A showcase of responsive grid cards featuring hover-invert interactions and gradient typography.",
    color_scheme: str = "light",       # "light" works best for the high-contrast neobrutalist vibe
    accent_color: str = "#009dff",     # Start of gradient
    accent_color_alt: str = "#ff00ff", # End of gradient
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Minimalist Neobrutalist Grid.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors (Neobrutalism relies heavily on black/white extremes)
    if color_scheme == "dark":
        bg_color = "#0a0a0a"
        text_color = "#ffffff"
        surface_bg = "#111111"
    else:
        bg_color = "#ffffff"
        text_color = "#111111"
        surface_bg = "#f9f9f9"

    # === CSS ===
    css = f"""/* Minimalist Neobrutalist Grid Component */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --surface-bg: {surface_bg};
    --accent-start: {accent_color};
    --accent-end: {accent_color_alt};
    --border-radius: 2.5rem;
    --transition-speed: 0.3s;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 4rem 2rem;
    overflow-x: hidden;
}}

.container {{
    width: 100%;
    max-width: {width_px}px;
}}

/* Header Styles */
.section-header {{
    text-align: center;
    margin-bottom: 4rem;
    opacity: 0;
    transform: translateY(20px);
}}

.section-title {{
    font-size: clamp(2.5rem, 5vw, 4rem);
    font-weight: 700;
    letter-spacing: -0.03em;
    margin-bottom: 1rem;
}}

.gradient-text {{
    background: linear-gradient(to right, var(--accent-start), var(--accent-end));
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    display: inline-block;
}}

.section-desc {{
    font-size: 1.125rem;
    color: var(--text-color);
    opacity: 0.8;
    max-width: 600px;
    margin: 0 auto;
    line-height: 1.6;
}}

/* Grid & Card Styles */
.grid-container {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 2rem;
}}

.card {{
    background-color: var(--bg-color);
    border: 2px solid var(--text-color);
    border-radius: var(--border-radius);
    padding: 2.5rem;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    cursor: pointer;
    transition: transform var(--transition-speed) cubic-bezier(0.4, 0, 0.2, 1),
                background-color var(--transition-speed) ease,
                color var(--transition-speed) ease,
                border-color var(--transition-speed) ease;
    
    /* Entrance Animation Initial State */
    opacity: 0;
    transform: translateY(30px);
}}

.card-icon-wrapper {{
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: var(--surface-bg);
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background var(--transition-speed) ease;
}}

.card-icon {{
    font-size: 1.5rem;
    background: linear-gradient(to right, var(--accent-start), var(--accent-end));
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}}

.card-title {{
    font-size: 1.5rem;
    font-weight: 600;
}}

.card-desc {{
    font-size: 1rem;
    line-height: 1.5;
    opacity: 0.8;
    flex-grow: 1; /* Pushes buttons to the bottom */
}}

.card-actions {{
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
}}

.btn {{
    padding: 0.75rem 1.5rem;
    border-radius: 2rem;
    border: 2px solid var(--text-color);
    background: transparent;
    color: var(--text-color);
    font-weight: 600;
    font-family: inherit;
    font-size: 0.9rem;
    transition: all var(--transition-speed) ease;
}}

/* Hover Invert Interaction Mechanism */
.card:hover {{
    transform: translateY(-10px) scale(1.02);
    background-color: var(--text-color);
    color: var(--bg-color);
}}

/* Invert nested elements on card hover */
.card:hover .card-icon-wrapper {{
    background: rgba(255,255,255,0.1);
}}

.card:hover .btn {{
    border-color: var(--bg-color);
    color: var(--bg-color);
}}

/* Button Hover (Secondary inversion) */
.card:hover .btn:hover {{
    background: var(--bg-color);
    color: var(--text-color);
}}

/* JS Entrance Animation Classes */
.animate-in {{
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
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    
    <!-- Font Awesome for Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- Component Styles -->
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <div class="container">
        <!-- Header -->
        <header class="section-header js-observe">
            <h2 class="section-title">
                {title_text.split()[0] if " " in title_text else title_text}
                <span class="gradient-text">{title_text.split(maxsplit=1)[1] if " " in title_text else ""}</span>
            </h2>
            <p class="section-desc">{body_text}</p>
        </header>

        <!-- Dynamic Grid -->
        <main class="grid-container">
            
            <!-- Card 1 -->
            <article class="card js-observe" style="transition-delay: 0.1s;">
                <div class="card-icon-wrapper">
                    <i class="fa-solid fa-code card-icon"></i>
                </div>
                <h3 class="card-title">Frontend Engineering</h3>
                <p class="card-desc">Building scalable, responsive architecture using pure HTML/CSS and modern layout techniques.</p>
                <div class="card-actions">
                    <button class="btn">Live Demo</button>
                    <button class="btn">Source Code</button>
                </div>
            </article>

            <!-- Card 2 -->
            <article class="card js-observe" style="transition-delay: 0.2s;">
                <div class="card-icon-wrapper">
                    <i class="fa-solid fa-laptop-code card-icon"></i>
                </div>
                <h3 class="card-title">System Design</h3>
                <p class="card-desc">Architecting robust web components with auto-fitting grids and resilient flexible boundaries.</p>
                <div class="card-actions">
                    <button class="btn">Live Demo</button>
                </div>
            </article>

            <!-- Card 3 -->
            <article class="card js-observe" style="transition-delay: 0.3s;">
                <div class="card-icon-wrapper">
                    <i class="fa-solid fa-list-check card-icon"></i>
                </div>
                <h3 class="card-title">Interaction Design</h3>
                <p class="card-desc">Applying tactile physics and visual feedback loops to elements via high-contrast color inversion.</p>
                <div class="card-actions">
                    <button class="btn">Live Demo</button>
                    <button class="btn">Case Study</button>
                </div>
            </article>

        </main>
    </div>

    <!-- Component Logic -->
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""/**
 * Minimalist Grid - Intersection Observer Logic
 * Triggers entrance animations when cards scroll into the viewport.
 */
document.addEventListener('DOMContentLoaded', () => {{
    
    // Select all elements that need to animate in
    const observerElements = document.querySelectorAll('.js-observe');
    
    // Configuration for the observer
    const observerOptions = {{
        root: null,           // Use the viewport as the bounding box
        rootMargin: '0px',    // No margin
        threshold: 0.1        // Trigger when 10% of the element is visible
    }};
    
    // Create the Intersection Observer
    const observer = new IntersectionObserver((entries, observer) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                // Add the CSS animation class
                entry.target.classList.add('animate-in');
                // Unobserve to ensure it only animates once
                observer.unobserve(entry.target);
            }}
        }});
    }}, observerOptions);
    
    // Attach observer to each element
    observerElements.forEach(el => {{
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
