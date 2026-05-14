def create_component(
    output_dir: str,
    title_text: str = "CSS Animation Mastery",
    body_text: str = "Scroll down to see native CSS scroll-driven animations in action.",
    color_scheme: str = "dark",
    accent_color: str = "#00efff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#0a0a0f"
        text_color = "#ffffff"
        text_muted = "#a0a0ab"
        surface_color = "rgba(255, 255, 255, 0.04)"
        surface_hover = "rgba(255, 255, 255, 0.08)"
        border_color = "rgba(255, 255, 255, 0.1)"
    else:
        bg_color = "#f4f4f5"
        text_color = "#09090b"
        text_muted = "#52525b"
        surface_color = "#ffffff"
        surface_hover = "#fafafa"
        border_color = "rgba(0, 0, 0, 0.1)"

    css = f"""/* Native CSS Animation Showcase */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --surface: {surface_color};
    --surface-hover: {surface_hover};
    --border: {border_color};
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    /* Ensure scrolling is possible to see the effect */
    min-height: 200vh; 
    overflow-x: hidden;
}}

.app-wrapper {{
    max-width: {width_px}px;
    margin: 0 auto;
    padding: 2rem;
}}

/* =========================================
   1. The 3D Keyframe Loader (From Tutorial)
   ========================================= */
.hero {{
    height: 80vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    gap: 2rem;
}}

.hero h1 {{
    font-size: 3rem;
    font-weight: 700;
    letter-spacing: -0.05em;
}}

.hero p {{
    color: var(--text-muted);
    font-size: 1.25rem;
    max-width: 600px;
}}

.loading-cube {{
    height: 50px;
    width: 50px;
    border: 5px solid var(--accent);
    border-radius: 8px;
    box-shadow: 0 0 20px var(--accent), inset 0 0 10px var(--accent);
    /* 2s duration, ease-in timing, infinite loop */
    animation: loading 2.5s ease-in-out infinite;
}}

/* Complex sequential 3D rotation */
@keyframes loading {{
    0% {{ transform: rotateX(0deg) rotateY(0deg) rotateZ(0deg); }}
    33% {{ transform: rotateX(180deg) rotateY(0deg) rotateZ(0deg); }}
    67% {{ transform: rotateX(180deg) rotateY(180deg) rotateZ(0deg); }}
    100% {{ transform: rotateX(180deg) rotateY(180deg) rotateZ(180deg); }}
}}

/* Scroll indicator */
.scroll-down {{
    margin-top: 4rem;
    font-size: 0.875rem;
    text-transform: uppercase;
    letter-spacing: 0.2em;
    color: var(--text-muted);
    animation: bounce 2s infinite ease-in-out;
}}

@keyframes bounce {{
    0%, 100% {{ transform: translateY(0); }}
    50% {{ transform: translateY(10px); }}
}}

/* =========================================
   2. Transitions & Layout
   ========================================= */
.grid-container {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 2rem;
    padding-bottom: 4rem;
}}

.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2.5rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    
    /* Smooth transition for hover states */
    transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), 
                box-shadow 0.4s ease, 
                border-color 0.4s ease,
                background-color 0.4s ease;
    
    /* Ensure cards are visible by default if scroll-timeline fails */
    opacity: 1;
    transform: scale(1);
}}

.card h2 {{
    font-size: 1.5rem;
    color: var(--accent);
}}

.card p {{
    color: var(--text-muted);
    line-height: 1.6;
}}

/* Hover Interaction */
.card:hover {{
    transform: translateY(-10px) scale(1.02);
    background: var(--surface-hover);
    border-color: var(--accent);
    box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.5), 
                0 0 20px -5px var(--accent);
}}


/* =========================================
   3. Scroll-Driven Animation (From Tutorial)
   ========================================= */
/* We use @supports to act as a fallback. If the browser doesn't 
   support animation-timeline, the cards simply remain visible 
   and the hover transitions still work. */

@supports (animation-timeline: view()) {{
    .card {{
        /* Bind the scrollReveal keyframes */
        animation: scrollReveal linear both;
        
        /* Link animation progress to the element crossing the viewport */
        animation-timeline: view();
        
        /* Start animation when element enters bottom (entry 0%), 
           finish when it covers 30% of the viewport (cover 30%) */
        animation-range: entry 5% cover 30%;
    }}
}}

@keyframes scrollReveal {{
    from {{
        opacity: 0;
        transform: translateY(100px) scale(0.8);
    }}
    to {{
        opacity: 1;
        transform: translateY(0) scale(1);
    }}
}}
"""

    # Generate dummy cards for the HTML
    cards_html = ""
    for i in range(1, 7):
        cards_html += f"""
            <div class="card">
                <h2>Feature Component {i}</h2>
                <p>This card utilizes CSS transitions for its hover state. More importantly, it uses <code>animation-timeline: view()</code> to trigger a scale and fade-in animation as it enters the viewport.</p>
            </div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-wrapper">
        <header class="hero">
            <div class="loading-cube"></div>
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <div class="scroll-down">Scroll to trigger View Timeline</div>
        </header>
        
        <main class="grid-container">
            {cards_html}
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// No JavaScript required! 
// This component relies entirely on modern CSS features:
// - CSS Transitions for hover states
// - CSS @keyframes for the 3D loader
// - CSS animation-timeline for scroll-driven reveals
console.log("Component loaded. Scroll down to see CSS native scroll animations.");
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
