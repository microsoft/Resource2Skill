def create_component(
    output_dir: str,
    title_text: str = "My Work & FAQs",
    body_text: str = "A curated selection of recent photography and common questions.",
    color_scheme: str = "light",       # "dark" or "light"
    accent_color: str = "#ff7a59",     # CSS hex color for accent
    width_px: int = 1000,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Asymmetric Bento Grid & Native Accordion.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#121212"
        text_color = "#f4f4f5"
        text_muted = "#a1a1aa"
        surface_color = "#1f1f22"
        surface_hover = "#27272a"
        border_color = "#3f3f46"
    else:
        bg_color = "#fafafa"
        text_color = "#18181b"
        text_muted = "#52525b"
        surface_color = "#ffffff"
        surface_hover = "#f4f4f5"
        border_color = "#e4e4e7"

    # === CSS ===
    css = f"""/* Bento Grid & Accordion Component */
@import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&family=Inter:wght@400;500&display=swap');

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
    --max-width: {width_px}px;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    padding: 2rem 1rem;
    line-height: 1.6;
}}

/* Typography */
h2, h3 {{
    font-family: 'Merriweather', serif;
    color: var(--text);
    margin-bottom: 1rem;
}}

.header-text {{
    text-align: center;
    margin-bottom: 3rem;
}}

.header-text p {{
    color: var(--text-muted);
    max-width: 600px;
    margin: 0 auto;
}}

/* Section Constraints */
.section-container {{
    width: min(var(--max-width), 100%);
    margin: 0 auto 5rem auto;
}}

/* === BENTO GRID GALLERY === */
.grid-container {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    grid-template-rows: repeat(2, 1fr);
    grid-template-areas: 
        "img-1 img-1 img-2 img-3"
        "img-1 img-1 img-4 img-5";
    gap: 1rem;
    aspect-ratio: 16 / 9; /* Keeps layout proportional on desktop */
}}

.grid-item {{
    overflow: hidden;
    border-radius: 12px;
    background: var(--surface);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}}

.grid-item img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}}

.grid-item:hover img {{
    transform: scale(1.08);
}}

/* Area Assignments */
.img-1 {{ grid-area: img-1; }}
.img-2 {{ grid-area: img-2; }}
.img-3 {{ grid-area: img-3; }}
.img-4 {{ grid-area: img-4; }}
.img-5 {{ grid-area: img-5; }}

/* === NATIVE ACCORDION FAQ === */
.faq-container {{
    display: flex;
    flex-direction: column;
    gap: 1rem;
}}

details {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}}

summary {{
    padding: 1.25rem;
    font-weight: 500;
    cursor: pointer;
    list-style: none; /* Hide default arrow in some browsers */
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: var(--surface);
    transition: background 0.2s ease;
}}

summary:hover {{
    background: var(--surface-hover);
}}

/* Custom Arrow indicator */
summary::after {{
    content: "▼";
    font-size: 0.8rem;
    color: var(--accent);
    transition: transform 0.3s ease;
}}

details[open] summary::after {{
    transform: rotate(180deg);
}}

/* Hide standard marker */
summary::-webkit-details-marker {{
    display: none;
}}

details p {{
    padding: 0 1.25rem 1.25rem 1.25rem;
    color: var(--text-muted);
    border-top: 1px solid transparent;
}}

details[open] summary {{
    border-bottom: 1px solid var(--border);
    margin-bottom: 1rem;
}}

/* === RESPONSIVE FALLBACKS === */
@media (max-width: 768px) {{
    .grid-container {{
        display: flex;
        flex-direction: column;
        aspect-ratio: auto;
    }}
    
    .grid-item {{
        height: 250px; /* Give flex items a set height on mobile */
    }}
    
    .img-1 {{
        height: 400px; /* Make the hero image taller */
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
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <!-- Header Section -->
    <header class="section-container header-text">
        <h2>{title_text}</h2>
        <p>{body_text}</p>
    </header>

    <!-- Bento Grid Gallery Section -->
    <section class="section-container">
        <div class="grid-container">
            <div class="grid-item img-1">
                <img src="https://images.unsplash.com/photo-1469474968028-56623f02e42e?auto=format&fit=crop&q=80&w=1200" alt="Nature landscape hero">
            </div>
            <div class="grid-item img-2">
                <img src="https://images.unsplash.com/photo-1501854140801-50d01698950b?auto=format&fit=crop&q=80&w=600" alt="Mountain view">
            </div>
            <div class="grid-item img-3">
                <img src="https://images.unsplash.com/photo-1472214103451-9374bd1c798e?auto=format&fit=crop&q=80&w=600" alt="Forest valley">
            </div>
            <div class="grid-item img-4">
                <img src="https://images.unsplash.com/photo-1426604966848-d7adac402bff?auto=format&fit=crop&q=80&w=600" alt="Sunset over hills">
            </div>
            <div class="grid-item img-5">
                <img src="https://images.unsplash.com/photo-1470071131384-001b85755b36?auto=format&fit=crop&q=80&w=600" alt="Morning mist">
            </div>
        </div>
    </section>

    <!-- Native Accordion FAQ Section -->
    <section class="section-container">
        <h3 style="text-align: center; margin-bottom: 2rem;">Common Questions</h3>
        <div class="faq-container">
            <details>
                <summary>How much does a photoshoot cost?</summary>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Similique qui explicabo voluptatum tenetur. Praesentium voluptatum repellendus asperiores eos.</p>
            </details>
            <details>
                <summary>Do you do weddings?</summary>
                <p>Assumenda dolore dolor aliquid totam nostrum libero repellendus architecto. Ut enim ad minima veniam, quis nostrum exercitationem.</p>
            </details>
            <details>
                <summary>How can I contact you?</summary>
                <p>You can reach out via the contact form on my main portfolio page or send a direct message to my official Instagram account linked above.</p>
            </details>
        </div>
    </section>

    <!-- Intentionally empty JS as the tutorial focuses on a zero-JS approach -->
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// No JavaScript required!
// This component relies entirely on HTML5 native <details>/<summary> tags for the accordion 
// and CSS Grid for the responsive layout, maximizing performance and accessibility.
console.log('Component loaded successfully without JavaScript dependencies.');
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
