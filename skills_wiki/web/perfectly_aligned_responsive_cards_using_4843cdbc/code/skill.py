def create_component(
    output_dir: str,
    title_text: str = "Aligned Card Layouts",
    body_text: str = "Notice how the buttons are perfectly aligned across all cards, despite the varying text lengths. This is achieved natively using CSS Subgrid.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#8b5cf6",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the CSS Subgrid Card Alignment effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
        surface_color = "rgba(255, 255, 255, 0.04)"
        border_color = "rgba(255, 255, 255, 0.08)"
        text_muted = "rgba(255, 255, 255, 0.7)"
        card_shadow = "0 8px 32px rgba(0, 0, 0, 0.3)"
    else:
        bg_color = "#f4f5f7"
        text_color = "#111827"
        surface_color = "#ffffff"
        border_color = "rgba(0, 0, 0, 0.06)"
        text_muted = "rgba(0, 0, 0, 0.6)"
        card_shadow = "0 8px 24px rgba(0, 0, 0, 0.04)"

    # === CSS ===
    css = f"""/* Perfectly Aligned Cards with CSS Subgrid */
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
    --border: {border_color};
    --shadow: {card_shadow};
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
    /* Optional: allows natural scrolling if content overflows */
    overflow-y: auto; 
    overflow-x: hidden;
}}

.container {{
    max-width: var(--width);
    width: 100%;
    padding: 3rem 2rem;
    margin: 0 auto;
}}

.header {{
    text-align: center;
    margin-bottom: 4rem;
    max-width: 600px;
    margin-inline: auto;
}}

.title {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    letter-spacing: -0.02em;
}}

.body-text {{
    font-size: 1.125rem;
    color: var(--text-muted);
    line-height: 1.6;
}}

/* -- Grid Wrapper -- */
.wrapper {{
    display: grid;
    /* Automatically creates columns based on available width */
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 2rem;
    align-items: start;
}}

/* -- Card Component (Fallback & Base) -- */
.card {{
    position: relative;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2rem;
    box-shadow: var(--shadow);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    overflow: hidden;
    
    /* Flexbox Fallback for older browsers */
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    height: 100%;
}}

.card::before {{
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: var(--accent);
    opacity: 0.8;
}}

.card:hover {{
    transform: translateY(-4px);
}}

/* -- CSS Subgrid Magic -- */
@supports (grid-template-rows: subgrid) {{
    .card {{
        /* Override Flexbox */
        display: grid;
        /* Inherit 3 row tracks from the parent wrapper */
        grid-template-rows: subgrid;
        /* Span exactly 3 rows in the parent (Title, Paragraph, Button) */
        grid-row: span 3;
        /* Override parent gap to define explicit inner spacing */
        gap: 1.5rem;
    }}
}}

/* -- Card Internals -- */
.card-title {{
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--text);
    line-height: 1.3;
}}

.card-text {{
    font-size: 1rem;
    line-height: 1.6;
    color: var(--text-muted);
}}

.card-button {{
    /* Pushes button to bottom in Flexbox fallback */
    margin-top: auto; 
    /* Ensures button stays at bottom of its grid track in Subgrid */
    align-self: end;  
    
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.875rem 1.5rem;
    background: var(--accent);
    color: #ffffff; /* Guaranteed contrast against accent */
    border: none;
    border-radius: 8px;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    transition: opacity 0.2s ease, filter 0.2s ease;
}}

.card-button:hover {{
    filter: brightness(1.1);
}}

.card-button:focus-visible {{
    outline: 2px solid var(--text);
    outline-offset: 4px;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <header class="header">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </header>

        <div class="wrapper">
            <!-- Card 1: Short Text -->
            <article class="card">
                <h2 class="card-title">Custom Websites</h2>
                <p class="card-text">We design fast, modern, and responsive websites that help your business look professional on every device.</p>
                <button class="card-button">Learn More</button>
            </article>

            <!-- Card 2: Long Text (Forces other buttons down via subgrid) -->
            <article class="card">
                <h2 class="card-title">Full-Service Web Development</h2>
                <p class="card-text">Need a more complex solution? We develop complete web applications with solid architecture, clean code, and a focus on long-term maintainability. Whether it's booking systems, dashboards, or custom APIs — we've got it covered.</p>
                <button class="card-button">Discover</button>
            </article>

            <!-- Card 3: Medium Text -->
            <article class="card">
                <h2 class="card-title">SEO & Performance Optimization</h2>
                <p class="card-text">Slow site? Dropping rankings? We audit, optimize, and rebuild the technical foundation of your website to improve loading speed and overall user experience.</p>
                <button class="card-button">Optimize</button>
            </article>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// CSS Subgrid interactive demonstration logic
document.addEventListener('DOMContentLoaded', () => {{
    // Detect CSS Subgrid support and log it
    const supportsSubgrid = CSS.supports('grid-template-rows', 'subgrid');
    console.log('CSS Subgrid Support Status:', supportsSubgrid ? 'Supported ✅' : 'Not Supported ❌ - Falling back to Flexbox');

    // Optional: Add simple button click interactions
    const buttons = document.querySelectorAll('.card-button');
    buttons.forEach(button => {{
        button.addEventListener('click', (e) => {{
            const originalText = e.target.innerText;
            e.target.innerText = "Processing...";
            e.target.style.opacity = "0.7";
            
            setTimeout(() => {{
                e.target.innerText = originalText;
                e.target.style.opacity = "1";
            }}, 1000);
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
