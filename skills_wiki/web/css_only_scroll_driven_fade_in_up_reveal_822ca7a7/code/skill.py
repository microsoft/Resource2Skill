def create_component(
    output_dir: str,
    title_text: str = "Re-Shape Your Body",
    body_text: str = "Scroll down to see the CSS-only scroll-driven animations in action.",
    color_scheme: str = "dark",
    accent_color: str = "#ff4500",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the CSS-Only Scroll-Driven Fade-In-Up Reveal.
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
        surface_color = "#1a1f2e"
        border_color = "rgba(255, 255, 255, 0.1)"
    else:
        bg_color = "#f4f6f8"
        text_color = "#111827"
        surface_color = "#ffffff"
        border_color = "rgba(0, 0, 0, 0.1)"

    # === CSS ===
    css = f"""/* CSS-Only Scroll-Driven Fade-In-Up Reveal */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --surface-color: {surface_color};
    --border-color: {border_color};
    --accent-color: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    line-height: 1.6;
    overflow-x: hidden;
}}

.viewport-container {{
    max-width: var(--width);
    margin: 0 auto;
    padding: 0 2rem;
}}

/* Hero Section (to push content down and force scrolling) */
.hero {{
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    border-bottom: 1px solid var(--border-color);
}}

.hero h1 {{
    font-size: 4rem;
    font-weight: 800;
    margin-bottom: 1rem;
    color: var(--accent-color);
    text-transform: uppercase;
    letter-spacing: -0.02em;
}}

.hero p {{
    font-size: 1.25rem;
    opacity: 0.8;
    max-width: 600px;
}}

.scroll-indicator {{
    margin-top: 3rem;
    animation: bounce 2s infinite;
    opacity: 0.5;
}}

@keyframes bounce {{
    0%, 20%, 50%, 80%, 100% {{ transform: translateY(0); }}
    40% {{ transform: translateY(-20px); }}
    60% {{ transform: translateY(-10px); }}
}}

/* Grid Layout for scroll items */
.content-section {{
    padding: 6rem 0;
}}

.grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 3rem;
}}

.card {{
    background-color: var(--surface-color);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 2rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}}

.card-img {{
    width: 100%;
    height: 240px;
    background: linear-gradient(135deg, var(--border-color), var(--surface-color));
    border-radius: 8px;
    margin-bottom: 1.5rem;
}}

.card h3 {{
    font-size: 1.5rem;
    margin-bottom: 0.75rem;
}}

/* 
=====================================================
CORE SKILL: Scroll-Driven Animation Utility Class 
=====================================================
*/
@media (prefers-reduced-motion: no-preference) {{
    .scroll-fade-in {{
        /* Bind the animation */
        animation: scroll-fade-in linear forwards;
        /* Link animation progress to the element entering the viewport */
        animation-timeline: view();
        /* Start when element enters, finish when element is fully in view */
        animation-range: entry;
    }}

    @keyframes scroll-fade-in {{
        0% {{
            transform: translateY(200px);
            opacity: 0;
        }}
        50% {{
            /* Delay opacity change until halfway through the movement */
            opacity: 0; 
        }}
        100% {{
            transform: translateY(0px);
            opacity: 1;
        }}
    }}
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
    
    <section class="hero viewport-container">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
        <div class="scroll-indicator">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="12" y1="5" x2="12" y2="19"></line>
                <polyline points="19 12 12 19 5 12"></polyline>
            </svg>
        </div>
    </section>

    <section class="content-section viewport-container">
        <div class="grid">
            <!-- Items with the scroll-fade-in utility class -->
            <article class="card scroll-fade-in">
                <div class="card-img"></div>
                <h3>Work at your own pace</h3>
                <p>Vivamus dapibus lacus sed risus vestibulum, at tincidunt libero elementum. Aenean odio metus, facilisis fermentum lorem sit amet.</p>
            </article>

            <article class="card scroll-fade-in">
                <div class="card-img"></div>
                <h3>Discover the class for you</h3>
                <p>Aenean odio metus, facilisis fermentum lorem sit amet, molestie facilisis turpis. Aliquam porta justo vitae tempus posuere.</p>
            </article>

            <article class="card scroll-fade-in">
                <div class="card-img"></div>
                <h3>Nutrition Advice</h3>
                <p>Nullam sit amet diam pulvinar, tincidunt tellus id, pulvinar ligula. Nam nec lacinia enim, ac volutpat urna.</p>
            </article>

            <article class="card scroll-fade-in">
                <div class="card-img"></div>
                <h3>Strength Assessment</h3>
                <p>Vivamus dapibus lacus sed risus vestibulum, at tincidunt libero elementum. Aenean odio metus, facilisis fermentum lorem sit amet.</p>
            </article>
        </div>
    </section>
    
    <!-- Spacer to allow scrolling past the last elements -->
    <div style="height: 50vh;"></div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// No JavaScript is required for this scroll-driven animation.
// It is entirely powered by the modern CSS animation-timeline API.
console.log('Scroll-driven animations are handled by CSS.');
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
