def create_component(
    output_dir: str,
    title_text: str = "Creative Link Hover Effects",
    body_text: str = "Hover over the links below to explore six distinct, pure CSS interaction patterns extracted from the tutorial.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Creative CSS Link Hover Gallery.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
        surface_color = "rgba(255, 255, 255, 0.05)"
        surface_border = "rgba(255, 255, 255, 0.1)"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        surface_color = "#ffffff"
        surface_border = "rgba(0, 0, 0, 0.1)"

    css = f"""/* Creative CSS Link Hover Gallery */
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
    --border: {surface_border};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    line-height: 1.6;
    padding: 2rem;
}}

.container {{
    width: 100%;
    max-width: var(--width);
    margin: 0 auto;
}}

.header {{
    text-align: center;
    margin-bottom: 4rem;
}}

.header h1 {{
    font-size: 2.5rem;
    margin-bottom: 1rem;
    font-weight: 700;
}}

.header p {{
    font-size: 1.1rem;
    opacity: 0.8;
    max-width: 600px;
    margin: 0 auto;
}}

.grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 2rem;
    list-style: none;
}}

.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    padding: 3rem 2rem;
    border-radius: 12px;
    font-size: 1.25rem;
    position: relative;
}}

.card::before {{
    content: counter(card-counter);
    counter-increment: card-counter;
    position: absolute;
    top: 1rem;
    left: 1rem;
    font-size: 0.875rem;
    font-weight: 700;
    background: var(--border);
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 4px;
}}

.grid {{
    counter-reset: card-counter;
}}

/* --- Base Link Styles --- */
a {{
    text-decoration: none;
    color: var(--accent);
    font-weight: 700;
    vertical-align: top;
}}

/* --- Effect 1: Inset Box Shadow --- */
.link-1 {{
    padding: 0.25rem 0.5rem;
    margin: 0 -0.5rem;
    box-shadow: inset 0 0 0 0 var(--accent);
    transition: color 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
    border-radius: 4px;
}}
.link-1:hover {{
    color: var(--bg);
    box-shadow: inset 300px 0 0 0 var(--accent);
}}

/* --- Effect 2: Center Out Underline --- */
.link-2 {{
    position: relative;
}}
.link-2::before {{
    content: '';
    position: absolute;
    top: 100%;
    left: 0;
    width: 100%;
    height: 3px;
    background-color: var(--accent);
    transform: scaleX(0);
    transition: transform 0.3s ease-in-out;
}}
.link-2:hover::before {{
    transform: scaleX(1);
}}

/* --- Effect 3: Alternating Origin --- */
.link-3 {{
    position: relative;
}}
.link-3::before {{
    content: '';
    position: absolute;
    top: 100%;
    left: 0;
    width: 100%;
    height: 3px;
    background-color: var(--accent);
    transform: scaleX(0);
    transform-origin: right;
    transition: transform 0.3s ease-in-out;
}}
.link-3:hover::before {{
    transform-origin: left;
    transform: scaleX(1);
}}

/* --- Effect 4: Text Replace (Sliding) --- */
.link-4 {{
    position: relative;
    overflow: hidden;
    display: inline-block;
}}
.link-4 span {{
    display: inline-block;
    transition: transform 0.3s ease-in-out;
}}
.link-4::after {{
    content: attr(data-replace);
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    transform: translate3d(-150%, 0, 0);
    transition: transform 0.3s ease-in-out;
    color: var(--accent);
}}
.link-4:hover span {{
    transform: translate3d(150%, 0, 0);
}}
.link-4:hover::after {{
    transform: translate3d(0, 0, 0);
}}

/* --- Effect 5: Expand Multiple Properties --- */
.link-5 {{
    position: relative;
    transition: color 0.3s ease-in-out;
    z-index: 1;
}}
.link-5::before {{
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 3px;
    background-color: var(--accent);
    z-index: -1;
    transition: all 0.3s ease-in-out;
    border-radius: 2px;
}}
.link-5:hover {{
    color: var(--bg);
}}
.link-5:hover::before {{
    height: 110%;
    width: calc(100% + 12px);
    left: -6px;
    bottom: -5%;
}}

/* --- Effect 6: Multi-line Background Gradient --- */
.link-6 {{
    background-image: linear-gradient(to bottom, transparent 50%, var(--accent) 50%);
    background-size: auto 200%;
    background-position: 0 0;
    transition: background-position 0.3s ease, color 0.3s ease;
    padding: 0.1rem 0;
}}
.link-6:hover {{
    background-position: 0 100%;
    color: var(--bg);
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </div>

        <ul class="grid">
            <li class="card">
                This is a very stylish <a href="#" class="link-1">link</a> that uses an inset box shadow to fill the background.
            </li>
            
            <li class="card">
                This one uses a pseudo-element to create an underline that draws from the <a href="#" class="link-2">center out</a>.
            </li>
            
            <li class="card">
                The third style uses alternating <a href="#" class="link-3">transformation origins</a> to slide in from the left and out to the right.
            </li>
            
            <li class="card">
                Using overflow and translations, we can get a <a href="#" class="link-4" data-replace="surprise!"><span>link</span></a> that swaps its text on hover.
            </li>
            
            <li class="card">
                Our fifth entry transitions <a href="#" class="link-5">multiple CSS properties</a>, expanding a small line into a full background highlight.
            </li>
            
            <li class="card">
                The final approach uses an oversized <a href="#" class="link-6">background gradient</a> to highlight text that might span across multiple lines beautifully.
            </li>
        </ul>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Creative CSS Link Hover Gallery
// All hover effects are driven by pure CSS.
// This script applies a simple stagger fade-in animation on load.

document.addEventListener('DOMContentLoaded', () => {{
    const cards = document.querySelectorAll('.card');
    
    // Initial state
    cards.forEach(card => {{
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    }});

    // Staggered reveal
    setTimeout(() => {{
        cards.forEach((card, index) => {{
            setTimeout(() => {{
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }}, index * 100);
        }});
    }}, 100);
}});
"""

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
