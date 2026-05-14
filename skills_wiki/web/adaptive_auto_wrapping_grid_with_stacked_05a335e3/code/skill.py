def create_component(
    output_dir: str,
    title_text: str = "Discover Our Collection",
    body_text: str = "A fluid, auto-wrapping grid utilizing CSS Grid Stacking.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#6366f1",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Adaptive Auto-Wrapping Grid visual effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_color = "#f8fafc"
        text_muted = "#94a3b8"
        card_bg = "#1e293b"
        shadow = "rgba(0, 0, 0, 0.5)"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        text_muted = "#64748b"
        card_bg = "#ffffff"
        shadow = "rgba(0, 0, 0, 0.1)"

    # === CSS ===
    css = f"""/* Adaptive Auto-Wrapping Grid — generated component */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --text-muted: {text_muted};
    --card-bg: {card_bg};
    --accent-color: {accent_color};
    --shadow: {shadow};
    --container-width: {width_px}px;
    --min-card-width: 280px;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    padding: 4rem 2rem;
    display: flex;
    justify-content: center;
    line-height: 1.6;
}}

.wrapper {{
    width: 100%;
    max-width: var(--container-width);
}}

.header {{
    margin-bottom: 3rem;
    text-align: center;
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

/* Macro Layout: Auto-Wrapping Grid */
.grid-container {{
    display: grid;
    /* The magic of CSS Grid: No media queries needed for responsiveness */
    grid-template-columns: repeat(auto-fit, minmax(var(--min-card-width), 1fr));
    gap: 2rem;
}}

/* Micro Layout: Card & Grid Stacking */
.card {{
    display: grid;
    /* Create a 1x1 grid cell for overlapping */
    grid-template-columns: 1fr;
    grid-template-rows: 1fr;
    border-radius: 16px;
    overflow: hidden;
    background-color: var(--card-bg);
    box-shadow: 0 4px 6px -1px var(--shadow), 0 2px 4px -2px var(--shadow);
    text-decoration: none;
    cursor: pointer;
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s ease;
    
    /* Animation initial state */
    opacity: 0;
    transform: translateY(20px);
}}

/* Both children occupy the exact same grid cell */
.card > * {{
    grid-column: 1 / -1;
    grid-row: 1 / -1;
}}

.card-image {{
    width: 100%;
    height: 350px;
    object-fit: cover;
    transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    z-index: 1;
}}

.card-content {{
    z-index: 2;
    /* Pushes content to the bottom of the grid cell */
    align-self: end; 
    padding: 2rem 1.5rem 1.5rem;
    /* Gradient ensures text readability regardless of image */
    background: linear-gradient(to bottom, transparent 0%, rgba(0,0,0,0.4) 30%, rgba(0,0,0,0.9) 100%);
    color: #ffffff; /* Always white due to dark gradient */
}}

.tag {{
    display: inline-block;
    background-color: var(--accent-color);
    color: #fff;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 0.25rem 0.75rem;
    border-radius: 999px;
    margin-bottom: 0.75rem;
}}

.card-title {{
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.25rem;
}}

.card-desc {{
    font-size: 0.9rem;
    color: rgba(255, 255, 255, 0.8);
}}

/* Interactive States */
.card:hover, .card:focus-visible {{
    transform: translateY(-8px);
    box-shadow: 0 20px 25px -5px var(--shadow), 0 8px 10px -6px var(--shadow);
    outline: none;
}}

.card:focus-visible {{
    box-shadow: 0 0 0 3px var(--bg-color), 0 0 0 6px var(--accent-color);
}}

.card:hover .card-image, .card:focus-visible .card-image {{
    transform: scale(1.05);
}}

/* Utility for JS animation */
.card.is-visible {{
    opacity: 1;
    transform: translateY(0);
}}
"""

    # Generate Card HTML dynamically
    cards_html = ""
    placeholders = [
        ("Architecture", "Modern Spaces", "Exploring geometry in urban design."),
        ("Nature", "Alpine Retreats", "High altitude escapes and vistas."),
        ("Technology", "Future Systems", "Neon lights and silicon dreams."),
        ("Abstract", "Color Flow", "Fluid dynamics in digital art."),
        ("Travel", "Desert Roads", "Endless highways to nowhere."),
        ("Design", "Minimalist Living", "Less is more in contemporary spaces.")
    ]

    for i, (tag, title, desc) in enumerate(placeholders):
        # Staggered transition delay based on index for the load animation
        delay = i * 0.1
        cards_html += f"""
            <a href="#" class="card" style="transition-delay: {delay}s, 0s, 0s;">
                <img src="https://picsum.photos/seed/{i+15}/600/800" alt="{title}" class="card-image" loading="lazy">
                <div class="card-content">
                    <span class="tag">{tag}</span>
                    <h2 class="card-title">{title}</h2>
                    <p class="card-desc">{desc}</p>
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
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="wrapper">
        <header class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>

        <main class="grid-container">
            {cards_html}
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Intersection Observer for staggered entrance animations
document.addEventListener('DOMContentLoaded', () => {{
    const cards = document.querySelectorAll('.card');
    
    // Check if user prefers reduced motion
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (prefersReducedMotion) {{
        // If reduced motion is preferred, show all immediately without transition delays
        cards.forEach(card => {{
            card.style.transitionDelay = '0s';
            card.classList.add('is-visible');
        }});
        return;
    }}

    const observerOptions = {{
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    }};

    const observer = new IntersectionObserver((entries, observer) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                // Add class to trigger CSS transition
                entry.target.classList.add('is-visible');
                // Unobserve after showing to prevent re-animating
                observer.unobserve(entry.target);
            }}
        }});
    }}, observerOptions);

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
