def create_component(
    output_dir: str,
    title_text: str = "Discover Our Features",
    body_text: str = "A fully responsive grid layout powered by CSS minmax and auto-fit.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#6366f1",     # CSS hex color for accent (indigo by default)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Auto-Wrapping MinMax Card Grid.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#0f172a"          # slate-900
        text_color = "#f8fafc"        # slate-50
        text_muted = "#94a3b8"        # slate-400
        surface_color = "#1e293b"     # slate-800
        surface_hover = "#334155"     # slate-700
        border_color = "#334155"
        shadow = "0 10px 15px -3px rgba(0, 0, 0, 0.5)"
    else:
        bg_color = "#f8fafc"          # slate-50
        text_color = "#0f172a"        # slate-900
        text_muted = "#475569"        # slate-600
        surface_color = "#ffffff"     # white
        surface_hover = "#f1f5f9"     # slate-100
        border_color = "#e2e8f0"
        shadow = "0 10px 15px -3px rgba(0, 0, 0, 0.05)"

    # === CSS ===
    css = f"""/* Responsive MinMax Grid Component */
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
    --surface-hover: {surface_hover};
    --border: {border_color};
    --shadow: {shadow};
    --max-width: {width_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    line-height: 1.5;
}}

.main-wrapper {{
    width: 100%;
    max-width: var(--max-width);
    /* Min height just to satisfy parameter requirement loosely, 
       but allowing natural expansion */
    min-height: {height_px * 0.8}px; 
    display: flex;
    flex-direction: column;
    gap: 3rem;
}}

.header-section {{
    text-align: center;
    max-width: 600px;
    margin: 0 auto;
}}

.header-section h1 {{
    font-size: clamp(2rem, 4vw, 3rem);
    font-weight: 700;
    margin-bottom: 1rem;
    letter-spacing: -0.02em;
}}

.header-section p {{
    color: var(--text-muted);
    font-size: 1.1rem;
}}

/* THE MAGIC CSS GRID */
.grid-container {{
    display: grid;
    /* This single line replaces all media queries for column counts */
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
    width: 100%;
}}

/* Card Styling */
.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), 
                box-shadow 0.3s cubic-bezier(0.4, 0, 0.2, 1),
                border-color 0.3s ease;
    box-shadow: var(--shadow);
    
    /* Animation initial state */
    opacity: 0;
    transform: translateY(20px);
}}

.card:hover {{
    transform: translateY(-6px);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    border-color: var(--accent);
}}

.card-icon-wrapper {{
    width: 48px;
    height: 48px;
    border-radius: 12px;
    background: color-mix(in srgb, var(--accent) 15%, transparent);
    color: var(--accent);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
    margin-bottom: 0.5rem;
}}

.card-title {{
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text);
}}

.card-body {{
    color: var(--text-muted);
    font-size: 0.95rem;
    flex-grow: 1; /* Pushes button to bottom if heights vary */
}}

.card-action {{
    margin-top: 1rem;
    color: var(--accent);
    font-weight: 500;
    font-size: 0.9rem;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    transition: gap 0.2s ease;
}}

.card:hover .card-action {{
    gap: 0.75rem;
}}

/* JS Animation Class */
.card.is-visible {{
    opacity: 1;
    transform: translateY(0);
}}
"""

    # Data for dummy cards
    cards_data = [
        {"icon": "fa-bolt", "title": "Lightning Fast", "desc": "Optimized DOM rendering with zero layout shift constraints."},
        {"icon": "fa-mobile-screen", "title": "Fully Responsive", "desc": "Uses CSS Grid auto-fit and minmax to mathematically wrap content without media queries."},
        {"icon": "fa-layer-group", "title": "Bento Layouts", "desc": "Easily adaptable to complex dashboard layouts by spanning rows and columns."},
        {"icon": "fa-palette", "title": "Themeable", "desc": "Built with CSS custom properties for instant light and dark mode toggling."},
        {"icon": "fa-universal-access", "title": "Accessible", "desc": "Semantic HTML structure with proper contrast ratios and focus states."},
        {"icon": "fa-code", "title": "Clean Code", "desc": "Zero bloat. Minimal CSS architecture achieving maximum flexibility."}
    ]

    cards_html = ""
    for i, card in enumerate(cards_data):
        cards_html += f"""
            <article class="card" style="transition-delay: {i * 75}ms;">
                <div class="card-icon-wrapper">
                    <i class="fa-solid {card['icon']}"></i>
                </div>
                <h2 class="card-title">{card['title']}</h2>
                <p class="card-body">{card['desc']}</p>
                <a href="#" class="card-action">Learn more <i class="fa-solid fa-arrow-right"></i></a>
            </article>"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="main-wrapper">
        <header class="header-section">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>

        <!-- The Responsive CSS Grid -->
        <main class="grid-container">
            {cards_html}
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Staggered Entrance Animation using Intersection Observer
document.addEventListener('DOMContentLoaded', () => {{
    const cards = document.querySelectorAll('.card');

    // Create an intersection observer
    const observerOptions = {{
        root: null,
        rootMargin: '0px',
        threshold: 0.1 // Trigger when 10% of card is visible
    }};

    const observer = new IntersectionObserver((entries, observer) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                // Add class to trigger CSS transition
                entry.target.classList.add('is-visible');
                // Stop observing once animated in
                observer.unobserve(entry.target);
            }}
        }});
    }}, observerOptions);

    // Observe all cards
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
