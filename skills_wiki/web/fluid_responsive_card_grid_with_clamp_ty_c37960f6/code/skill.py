def create_component(
    output_dir: str,
    title_text: str = "Fluid Responsive Design",
    body_text: str = "Resize the browser to see the grid and typography scale seamlessly without media queries.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#8b5cf6",     # CSS hex color for accent (default: vivid purple)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Fluid Responsive Card Grid visual effect.
    """
    import os
    import html

    os.makedirs(output_dir, exist_ok=True)

    # Safe HTML escaping
    safe_title = html.escape(title_text)
    safe_body = html.escape(body_text)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_color = "#f8fafc"
        text_muted = "#94a3b8"
        card_bg = "rgba(255, 255, 255, 0.05)"
        card_border = "rgba(255, 255, 255, 0.1)"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        text_muted = "#475569"
        card_bg = "#ffffff"
        card_border = "rgba(0, 0, 0, 0.1)"

    # === CSS ===
    css = f"""/* Fluid Responsive Card Grid */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --card-bg: {card_bg};
    --card-border: {card_border};
    --max-width: {width_px}px;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    padding: 2rem;
    line-height: 1.6;
}}

.container {{
    width: 100%;
    max-width: var(--max-width);
    /* Ensure the component takes up at least the requested height if needed */
    min-height: {height_px}px; 
    display: flex;
    flex-direction: column;
    gap: 3rem;
}}

header {{
    text-align: center;
    max-width: 800px;
    margin: 0 auto;
}}

/* FLUID TYPOGRAPHY USING CLAMP */
/* clamp(MIN_SIZE, FLUID_SIZE, MAX_SIZE) */
.fluid-title {{
    /* Falls back to 2rem on very old browsers, otherwise fluidly scales */
    font-size: 2rem; 
    font-size: clamp(2rem, 5vw, 4rem);
    font-weight: 800;
    margin-bottom: 1rem;
    background: linear-gradient(135deg, var(--text), var(--accent));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.2;
}}

.fluid-subtitle {{
    font-size: 1rem;
    font-size: clamp(1rem, 2vw, 1.25rem);
    color: var(--text-muted);
}}

/* FLUID GRID LAYOUT */
/* The magic responsive grid formula. No media queries required. */
.grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    width: 100%;
}}

/* CARD STYLING */
.card {{
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 16px;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
    
    /* Animation state applied by JS */
    opacity: 0;
    transform: translateY(30px);
}}

.card.visible {{
    opacity: 1;
    transform: translateY(0);
}}

.card:hover {{
    transform: translateY(-8px);
    border-color: var(--accent);
    box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.3), 0 0 20px -10px var(--accent);
}}

/* RESPONSIVE IMAGE PLACEHOLDER */
.card-image-wrapper {{
    width: 100%;
    /* Replaces fixed heights, ensures scaling keeps proportions */
    aspect-ratio: 16 / 9; 
    background: linear-gradient(45deg, var(--card-border), transparent);
    border-radius: 8px;
    overflow: hidden;
    position: relative;
}}

.card-image-wrapper::after {{
    content: '';
    position: absolute;
    inset: 0;
    background: var(--accent);
    opacity: 0.2;
    mix-blend-mode: overlay;
}}

.card-content {{
    display: flex;
    flex-direction: column;
    flex-grow: 1; /* Pushes button to bottom */
    gap: 0.75rem;
}}

.card-title {{
    font-size: clamp(1.25rem, 2.5vw, 1.5rem);
    font-weight: 700;
}}

.card-text {{
    color: var(--text-muted);
    font-size: 0.95rem;
}}

.card-btn {{
    /* margin-top: auto pushes the button to the bottom of the flex container */
    margin-top: auto; 
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    border: none;
    background-color: var(--card-border);
    color: var(--text);
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.2s ease, color 0.2s ease;
}}

.card:hover .card-btn {{
    background-color: var(--accent);
    color: #ffffff;
}}
"""

    # === HTML ===
    # Including the crucial viewport meta tag mentioned in the tutorial
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <!-- Crucial for responsive design on mobile -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="container">
        <header>
            <h1 class="fluid-title">{safe_title}</h1>
            <p class="fluid-subtitle">{safe_body}</p>
        </header>

        <section class="grid">
            <!-- Card 1 -->
            <article class="card">
                <div class="card-image-wrapper"></div>
                <div class="card-content">
                    <h2 class="card-title">Responsive Layout</h2>
                    <p class="card-text">Using CSS Grid with auto-fit and minmax() creates a layout that wraps intelligently based on available space.</p>
                </div>
                <button class="card-btn">Learn More</button>
            </article>

            <!-- Card 2 -->
            <article class="card">
                <div class="card-image-wrapper" style="background: linear-gradient(120deg, var(--accent), transparent)"></div>
                <div class="card-content">
                    <h2 class="card-title">Fluid Typography</h2>
                    <p class="card-text">The clamp() function allows text to scale perfectly between minimum and maximum bounds. No breakpoints needed.</p>
                </div>
                <button class="card-btn">Learn More</button>
            </article>

            <!-- Card 3 -->
            <article class="card">
                <div class="card-image-wrapper" style="background: linear-gradient(200deg, var(--text-muted), transparent)"></div>
                <div class="card-content">
                    <h2 class="card-title">Flexible Media</h2>
                    <p class="card-text">Using relative widths (100%) and aspect-ratios ensures images and media objects conform to their containers gracefully.</p>
                </div>
                <button class="card-btn">Learn More</button>
            </article>

            <!-- Card 4 -->
            <article class="card">
                <div class="card-image-wrapper"></div>
                <div class="card-content">
                    <h2 class="card-title">Modern Alignments</h2>
                    <p class="card-text">Flexbox inside the card structure, coupled with margin-top: auto, keeps UI elements consistently aligned at the bottom.</p>
                </div>
                <button class="card-btn">Learn More</button>
            </article>
        </section>
    </main>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Intersection Observer to handle elegant reveal animations
document.addEventListener('DOMContentLoaded', () => {{
    const cards = document.querySelectorAll('.card');

    // Setup the observer
    const observerOptions = {{
        root: null, // use viewport
        rootMargin: '0px',
        threshold: 0.1 // trigger when 10% of the card is visible
    }};

    const cardObserver = new IntersectionObserver((entries, observer) => {{
        entries.forEach((entry, index) => {{
            if (entry.isIntersecting) {{
                // Add a staggered delay based on the element's index
                setTimeout(() => {{
                    entry.target.classList.add('visible');
                }}, index * 100); // 100ms stagger
                
                // Stop observing once revealed
                observer.unobserve(entry.target);
            }}
        }});
    }}, observerOptions);

    // Observe all cards
    cards.forEach(card => {{
        cardObserver.observe(card);
    }});
}});
"""

    # === Write files ===
    files = []
    for fname, content in [("index.html", html_content), ("style.css", css), ("script.js", js)]:
        path = os.path.join(output_dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        files.append(path)

    return {
        "html": html_content,
        "css": css,
        "js": js,
        "files": files,
    }
