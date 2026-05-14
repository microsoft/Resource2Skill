def create_component(
    output_dir: str,
    title_text: str = "Latest Arrivals",
    body_text: str = "Explore our responsive grid gallery.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#6366f1",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Auto-Fit Grid with Grid Stacking.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#0f1117"
        text_color = "#f8f9fa"
        text_muted = "#a1a1aa"
        surface_color = "rgba(255, 255, 255, 0.03)"
        surface_border = "rgba(255, 255, 255, 0.08)"
        gradient_overlay = "linear-gradient(to top, rgba(15, 17, 23, 0.95) 0%, rgba(15, 17, 23, 0.4) 50%, rgba(15, 17, 23, 0) 100%)"
    else:
        bg_color = "#f4f4f5"
        text_color = "#18181b"
        text_muted = "#52525b"
        surface_color = "rgba(0, 0, 0, 0.03)"
        surface_border = "rgba(0, 0, 0, 0.08)"
        gradient_overlay = "linear-gradient(to top, rgba(244, 244, 245, 0.95) 0%, rgba(244, 244, 245, 0.4) 50%, rgba(244, 244, 245, 0) 100%)"

    # === CSS ===
    css = f"""/* Responsive Auto-Fit Card Gallery & Grid Stacking */
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
    --surface-border: {surface_border};
    --overlay: {gradient_overlay};
    --width: {width_px}px;
    --height: {height_px}px;
    --card-min-width: 280px;
    --gap: 1.5rem;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    padding: 2rem;
    overflow-x: hidden;
}}

.app-wrapper {{
    width: 100%;
    max-width: var(--width);
    /* For demonstration purposes, allowing height to grow but setting a min-height */
    min-height: var(--height);
    display: flex;
    flex-direction: column;
    gap: 2rem;
}}

.header {{
    text-align: left;
    margin-bottom: 1rem;
}}

.header h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    margin-bottom: 0.5rem;
}}

.header p {{
    color: var(--text-muted);
    font-size: 1.1rem;
}}

/* MACRO LAYOUT: Grid Wrapping (Auto-fit + MinMax) */
.gallery-grid {{
    display: grid;
    /* The Magic Line: Responsive without media queries */
    grid-template-columns: repeat(auto-fit, minmax(var(--card-min-width), 1fr));
    gap: var(--gap);
    width: 100%;
}}

/* MICRO LAYOUT: Grid Stacking */
.card {{
    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows: 1fr;
    border-radius: 16px;
    overflow: hidden;
    background: var(--surface);
    border: 1px solid var(--surface-border);
    height: 380px;
    text-decoration: none;
    transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), 
                box-shadow 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    cursor: pointer;
    
    /* Starting state for JS intersection observer */
    opacity: 0;
    transform: translateY(30px);
}}

/* Stacking trick: Everything goes into line 1 to 2 */
.card > * {{
    grid-area: 1 / 1 / 2 / 2;
}}

.card-img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}}

.card-overlay {{
    background: var(--overlay);
    z-index: 1;
}}

.card-content {{
    z-index: 2;
    /* Align content inside the grid cell */
    place-self: end start;
    padding: 1.5rem;
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
}}

.card-title {{
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text);
    margin: 0;
}}

.card-price {{
    font-size: 1rem;
    font-weight: 500;
    color: var(--accent);
}}

/* Hover Interactions */
.card:hover {{
    transform: translateY(-6px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}}

.card:hover .card-img {{
    transform: scale(1.06);
}}

/* JS Animation States */
.card.visible {{
    opacity: 1;
    transform: translateY(0);
}}
"""

    # Generate Card HTML dynamically
    cards_html = ""
    for i in range(1, 9):
        cards_html += f"""
            <a href="#" class="card" aria-label="View Item {i}">
                <img src="https://picsum.photos/seed/{i+20}/600/800" alt="Item {i}" class="card-img" loading="lazy">
                <div class="card-overlay"></div>
                <div class="card-content">
                    <h3 class="card-title">Curated Item {i}</h3>
                    <span class="card-price">$ {(i * 24.99):.2f}</span>
                </div>
            </a>"""

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
    <main class="app-wrapper">
        <header class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>

        <!-- The Responsive Grid Wrapping Component -->
        <section class="gallery-grid" id="gallery">
            {cards_html}
        </section>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Staggered reveal animation using Intersection Observer
document.addEventListener('DOMContentLoaded', () => {{
    const cards = document.querySelectorAll('.card');
    
    // Intersection Observer setup
    const observerOptions = {{
        root: null,
        rootMargin: '0px',
        threshold: 0.1 // Trigger when 10% of the card is visible
    }};

    const cardObserver = new IntersectionObserver((entries, observer) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                // Add visible class to trigger CSS transition
                entry.target.classList.add('visible');
                // Stop observing once revealed
                observer.unobserve(entry.target);
            }}
        }});
    }}, observerOptions);

    // Apply staggered transition delays based on grid position
    cards.forEach((card, index) => {{
        // Optional: add a slight staggered delay for visual flair 
        // Note: In a fully dynamic fluid grid, row/col detection is complex, 
        // so we use a simple modulo for a rolling wave effect.
        const delay = (index % 4) * 100; 
        card.style.transitionDelay = `${{delay}}ms, 0ms`; // Delay for transform/opacity, 0ms for box-shadow on hover
        
        cardObserver.observe(card);
    }});
    
    // Remove the transition delay after initial entry so hover effects are instant
    cards.forEach(card => {{
        card.addEventListener('transitionend', function handler(e) {{
            if (e.propertyName === 'opacity') {{
                card.style.transitionDelay = '0ms, 0ms';
                card.removeEventListener('transitionend', handler);
            }}
        }});
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
