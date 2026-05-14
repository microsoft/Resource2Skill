def create_component(
    output_dir: str,
    title_text: str = "CSS Subgrid Alignment",
    body_text: str = "Notice how the buttons below always align perfectly, regardless of the paragraph length above them.",
    color_scheme: str = "dark",
    accent_color: str = "#22c4ff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the CSS Subgrid alignment effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#0b0f19" # Deep dark
        text_color = "#f0f0f0"
        text_muted = "#a0aabf"
        surface_color = "#151b2b" # Elevated card color
        border_color = "rgba(255, 255, 255, 0.05)"
    else:
        bg_color = "#f4f6f8" # Light grey base
        text_color = "#111827"
        text_muted = "#4b5563"
        surface_color = "#ffffff"
        border_color = "rgba(0, 0, 0, 0.05)"

    # === CSS ===
    css = f"""/* Aligned Card Layouts with CSS Subgrid */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --surface: {surface_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --border: {border_color};
    --width: {width_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
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
    gap: 3rem;
}}

.header {{
    text-align: center;
}}

.header h1 {{
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}}

.header p {{
    color: var(--text-muted);
    font-size: 1.1rem;
}}

/* 
  THE CORE SKILL: CSS SUBGRID
  1. The Parent Wrapper establishes the main grid columns.
*/
.wrapper {{
    display: grid;
    /* Responsive columns that wrap automatically */
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    /* Main gap between cards */
    gap: 2rem; 
}}

/* 
  2. The Child Card becomes a grid itself.
*/
.card {{
    background-color: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 2rem;
    
    display: grid;
    /* Instructs the card to use the parent grid's row tracks */
    grid-template-rows: subgrid;
    /* Tells the card to span across 3 rows (heading, text, button) */
    grid-row: span 3;
    
    /* Overrides the inherited parent gap so internal spacing isn't huge */
    gap: 0; 
    
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05), 0 10px 15px rgba(0, 0, 0, 0.025);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 12px 20px rgba(0, 0, 0, 0.08), 0 20px 25px rgba(0, 0, 0, 0.05);
}}

/* Card internal elements */
.card h2 {{
    font-size: 1.5rem;
    margin-bottom: 1rem;
    color: var(--text);
    align-self: start;
}}

.card p {{
    font-size: 1rem;
    line-height: 1.6;
    color: var(--text-muted);
    /* Margins handle internal spacing since gap is 0 */
    margin-bottom: 2rem; 
    align-self: start;
}}

.card button {{
    background-color: var(--accent);
    color: #000; /* Assuming light text for bright accent */
    border: none;
    border-radius: 6px;
    padding: 1rem 1.5rem;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    transition: filter 0.2s ease;
    align-self: end; /* Pushes button to bottom of its track */
    width: 100%;
}}

.card button:hover {{
    filter: brightness(1.15);
}}

/* Fallback for browsers that do not support subgrid */
@supports not (grid-template-rows: subgrid) {{
    .card {{
        display: flex;
        flex-direction: column;
    }}
    .card p {{
        flex-grow: 1; /* Fallback mimics the effect using flexbox */
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </div>
        
        <!-- Parent Grid -->
        <div class="wrapper">
            
            <!-- Card 1 (Short Content) -->
            <div class="card">
                <h2>Custom Websites</h2>
                <p>We design fast, modern, and responsive websites that help your business look professional on every device.</p>
                <button>Learn More</button>
            </div>

            <!-- Card 2 (Long Content to demonstrate subgrid alignment) -->
            <div class="card">
                <h2>Full-Service Web Development</h2>
                <p>Need a more complex solution? We develop complete web applications with solid architecture, clean code, and a focus on long-term maintainability. Whether it's booking systems, dashboards, or custom APIs — we've got it covered.</p>
                <button>Discover</button>
            </div>

            <!-- Card 3 (Medium Content) -->
            <div class="card">
                <h2>SEO & Performance</h2>
                <p>Slow site? Dropping rankings? We audit, optimize, and rebuild the technical foundation of your website to improve loading speed and search visibility.</p>
                <button>Optimize</button>
            </div>

        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    # CSS Subgrid operates entirely in the CSS layout engine. No JS is required for the core behavior.
    js = f"""// Component initialized.
// Notice that NO Javascript is required to calculate heights or align the buttons.
// CSS Subgrid handles the alignment natively in the browser's rendering engine.

document.addEventListener('DOMContentLoaded', () => {{
    console.log("CSS Subgrid component loaded successfully.");
    
    // Optional interaction just for feedback
    const buttons = document.querySelectorAll('.card button');
    buttons.forEach(btn => {{
        btn.addEventListener('click', (e) => {{
            const originalText = e.target.innerText;
            e.target.innerText = "Processing...";
            e.target.style.filter = "brightness(0.8)";
            
            setTimeout(() => {{
                e.target.innerText = originalText;
                e.target.style.filter = "";
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
