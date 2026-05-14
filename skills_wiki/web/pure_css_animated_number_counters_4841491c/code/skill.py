def create_component(
    output_dir: str,
    title_text: str = "Platform Metrics",
    body_text: str = "Live data rendering purely via CSS `@property` counters.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1000,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Pure CSS Animated Number Counter effect.
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
        surface_color = "rgba(255, 255, 255, 0.04)"
        border_color = "rgba(255, 255, 255, 0.08)"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        surface_color = "rgba(0, 0, 0, 0.03)"
        border_color = "rgba(0, 0, 0, 0.08)"

    # Hardcoded values for the demonstration
    val1, val2, val3 = 1025, 89, 432

    # === CSS ===
    css = f"""/* Pure CSS Animated Number Counters */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --border: {border_color};
    --width: {width_px}px;
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
}}

.container {{
    width: 100%;
    max-width: var(--width);
    display: flex;
    flex-direction: column;
    gap: 3.5rem;
}}

.header {{
    text-align: center;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}}

.title {{
    font-size: 2.5rem;
    font-weight: 800;
    letter-spacing: -0.02em;
}}

.body-text {{
    font-size: 1.1rem;
    opacity: 0.6;
}}

.stats-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 1.5rem;
}}

.stat-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 2.5rem 2rem;
    text-align: center;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.02);
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    transition: transform 0.3s ease, background 0.3s ease;
}}

.stat-card:hover {{
    transform: translateY(-4px);
    background: var(--border);
}}

/* Tabular-nums prevents the text from jittering horizontally as numbers cycle */
.stat-number {{
    font-size: 4rem;
    font-weight: 800;
    color: var(--accent);
    line-height: 1;
    font-variant-numeric: tabular-nums;
}}

.stat-label {{
    font-size: 1.05rem;
    font-weight: 600;
    opacity: 0.8;
}}

/* ========================================= */
/* === THE MAGIC: CSS COUNTER ANIMATIONS === */
/* ========================================= */

@property --num1 {{ syntax: "<integer>"; initial-value: 0; inherits: false; }}
@property --num2 {{ syntax: "<integer>"; initial-value: 0; inherits: false; }}
@property --num3 {{ syntax: "<integer>"; initial-value: 0; inherits: false; }}

@keyframes countUp1 {{ to {{ --num1: {val1}; }} }}
@keyframes countUp2 {{ to {{ --num2: {val2}; }} }}
@keyframes countUp3 {{ to {{ --num3: {val3}; }} }}

/* Bind the custom property to the CSS counter */
.stat-1::after {{ counter-reset: c1 var(--num1); content: counter(c1); }}
.stat-2::after {{ counter-reset: c2 var(--num2); content: counter(c2); }}
.stat-3::after {{ counter-reset: c3 var(--num3); content: counter(c3); }}

/* Trigger animation only when the parent gets the .in-view class from JS */
.in-view .stat-1::after {{ animation: countUp1 2.5s cubic-bezier(0.16, 1, 0.3, 1) forwards; }}
.in-view .stat-2::after {{ animation: countUp2 2.5s cubic-bezier(0.16, 1, 0.3, 1) forwards 0.2s; }}
.in-view .stat-3::after {{ animation: countUp3 2.5s cubic-bezier(0.16, 1, 0.3, 1) forwards 0.4s; }}

/* === Accessibility: Reduce Motion === */
@media (prefers-reduced-motion: reduce) {{
    .stat-1::after {{ animation: none !important; content: "{val1}"; }}
    .stat-2::after {{ animation: none !important; content: "{val2}"; }}
    .stat-3::after {{ animation: none !important; content: "{val3}"; }}
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <header class="header">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </header>
        
        <!-- We use aria-label on the container because screen readers often ignore pseudo-element content -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number stat-1" aria-label="{val1}" role="text"></div>
                <div class="stat-label">Total Users</div>
            </div>
            <div class="stat-card">
                <div class="stat-number stat-2" aria-label="{val2}" role="text"></div>
                <div class="stat-label">Active Projects</div>
            </div>
            <div class="stat-card">
                <div class="stat-number stat-3" aria-label="{val3}" role="text"></div>
                <div class="stat-label">Global Servers</div>
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Intersection Observer to trigger the CSS animation when scrolled into view
document.addEventListener('DOMContentLoaded', () => {{
    const observerOptions = {{
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    }};

    const observer = new IntersectionObserver((entries) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                // Adding the class triggers the CSS @keyframes
                entry.target.classList.add('in-view');
                // Unobserve after animating once
                observer.unobserve(entry.target);
            }}
        }});
    }}, observerOptions);

    const grid = document.querySelector('.stats-grid');
    if (grid) {{
        observer.observe(grid);
    }}
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
