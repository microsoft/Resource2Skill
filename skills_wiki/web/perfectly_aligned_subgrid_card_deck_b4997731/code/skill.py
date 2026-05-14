def create_component(
    output_dir: str,
    title_text: str = "Subgrid Alignment",
    body_text: str = "Notice how the buttons align perfectly across all cards, despite the varying text lengths in the paragraphs above them.",
    color_scheme: str = "dark",
    accent_color: str = "#22c4ff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Perfectly Aligned Subgrid Card Deck.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os
    import html

    os.makedirs(output_dir, exist_ok=True)

    # Theme definitions based on video aesthetic
    if color_scheme == "dark":
        bg_color = "#150a2e"          # Dark violet/navy background
        surface_color = "#3a197a"     # Elevated purple surface
        text_primary = "#ffffff"
        text_secondary = "#d1c4e9"
    else:
        bg_color = "#f4f5f7"
        surface_color = "#ffffff"
        text_primary = "#111827"
        text_secondary = "#4b5563"

    # Escape texts
    safe_title = html.escape(title_text)
    safe_body = html.escape(body_text)

    # === CSS ===
    css = f"""/* Perfectly Aligned Subgrid Card Deck */
:root {{
    --bg-color: {bg_color};
    --surface-color: {surface_color};
    --accent-color: {accent_color};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --max-width: {width_px}px;
}}

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    line-height: 1.6;
}}

.header {{
    text-align: center;
    margin-bottom: 4rem;
    max-width: 600px;
}}

.header h1 {{
    font-size: 2.5rem;
    margin-bottom: 1rem;
    font-weight: 700;
    letter-spacing: -0.02em;
}}

.header p {{
    color: var(--text-secondary);
    font-size: 1.1rem;
}}

/* The Parent Grid */
.wrapper {{
    display: grid;
    /* Responsive columns that auto-wrap */
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 2rem;
    width: 100%;
    max-width: var(--max-width);
    margin: 0 auto;
}}

/* The Subgrid Cards */
.card {{
    background-color: var(--surface-color);
    border-radius: 12px;
    padding: 2.5rem 2rem;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    
    /* Core Subgrid Magic */
    display: grid;
    grid-template-rows: subgrid;
    /* Span exactly the number of elements inside (h2, p, button = 3) */
    grid-row: span 3;
    
    /* Override the gap inherited from the wrapper so we can use semantic margins */
    gap: 0; 
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
}}

/* Card Elements */
.card h2 {{
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--text-primary);
    align-self: start;
}}

.card p {{
    color: var(--text-secondary);
    font-size: 1rem;
    /* Use margin to separate content since grid gap is 0 */
    margin: 1.5rem 0 2.5rem 0;
    align-self: start;
}}

.card button {{
    background-color: var(--accent-color);
    color: #ffffff;
    border: none;
    padding: 1rem 1.5rem;
    border-radius: 6px;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    transition: filter 0.2s ease, transform 0.1s ease;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    align-self: end;
    /* Subtle shadow for the button based on accent color */
    box-shadow: 0 4px 14px calc(var(--accent-color)40);
}}

.card button:hover {{
    filter: brightness(1.15);
}}

.card button:active {{
    transform: scale(0.97);
}}
"""

    # === HTML ===
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="header">
        <h1>{safe_title}</h1>
        <p>{safe_body}</p>
    </header>

    <main class="wrapper">
        <!-- Card 1 (Short content) -->
        <article class="card">
            <h2>Custom Websites</h2>
            <p>We design fast, modern, and responsive websites that help your business look professional.</p>
            <button>Learn More</button>
        </article>

        <!-- Card 2 (Long content) -->
        <article class="card">
            <h2>Full-Service Web Development</h2>
            <p>Need a more complex solution? We develop complete web applications with solid architecture, clean code, and a focus on long-term maintainability. Whether it's booking systems, dashboards, or custom APIs — we've got it covered.</p>
            <button>Discover</button>
        </article>

        <!-- Card 3 (Medium content) -->
        <article class="card">
            <h2>SEO & Performance Optimization</h2>
            <p>Slow site? Dropping rankings? We audit, optimize, and rebuild the technical foundation of your website to improve loading speed and search visibility.</p>
            <button>Optimize</button>
        </article>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// No complex JavaScript is required for CSS subgrid to function perfectly.
// This empty script serves as a placeholder for potential future interactions.
document.addEventListener('DOMContentLoaded', () => {
    console.log("Subgrid component loaded successfully.");
});
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
