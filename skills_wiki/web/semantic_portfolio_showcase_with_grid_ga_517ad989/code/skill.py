def create_component(
    output_dir: str,
    title_text: str = "Hey Friends!",
    body_text: str = "I'm an independent creator with a passion for building beautiful, performant experiences. Welcome to my digital garden.",
    color_scheme: str = "light",       # "dark" or "light"
    accent_color: str = "#f08d4f",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Semantic Portfolio Showcase.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os
    import json

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        base_color = "#121212"
        surface_color = "#1e1e1e"
        text_color = "#ffffff"
        text_muted = "#a0a0a0"
    else:
        base_color = "#ffffff"
        surface_color = "#f6f6f9"
        text_color = "#1a1a1a"
        text_muted = "#555555"

    # === CSS ===
    css = f"""/* Semantic Portfolio Showcase */
:root {{
    --base-color: {base_color};
    --surface-color: {surface_color};
    --text-color: {text_color};
    --text-muted: {text_muted};
    --primary-color: {accent_color};
    --max-width: {width_px}px;
}}

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: var(--base-color);
    color: var(--text-color);
    line-height: 1.6;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 20px;
}}

/* Wrapper to simulate the requested dimensions */
.portfolio-wrapper {{
    width: 100%;
    max-width: var(--max-width);
    height: {height_px}px;
    background: var(--base-color);
    overflow-y: auto;
    border-radius: 12px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    position: relative;
    scroll-behavior: smooth;
}}

/* Typography */
h1, h2, h3, h4 {{
    font-family: 'Merriweather', serif;
    font-weight: 700;
    margin-bottom: 0.5em;
    line-height: 1.2;
}}

p {{
    margin-bottom: 1.5em;
    color: var(--text-muted);
}}

/* Global Sections */
section {{
    padding: 4em 2em;
    width: min(100%, 1000px);
    margin: 0 auto;
}}

.surface-section {{
    background-color: var(--surface-color);
    border-radius: 1em;
    margin-bottom: 4em;
}}

/* Flex Layouts */
.flex-container {{
    display: flex;
    flex-wrap: wrap;
    gap: 3em;
    align-items: center;
    justify-content: space-between;
}}

.text-container {{
    flex: 1 1 30em;
}}

.hero-image-wrapper {{
    flex: 1 1 20em;
    display: flex;
    justify-content: center;
}}

.hero-image {{
    max-width: 100%;
    border-radius: 1em;
    object-fit: cover;
}}

/* Buttons */
.cta-button {{
    display: inline-block;
    padding: 0.75em 1.5em;
    background-color: var(--primary-color);
    color: #fff;
    text-decoration: none;
    border-radius: 0.5em;
    font-weight: 600;
    transition: transform 0.2s ease, opacity 0.2s ease;
    margin-right: 1em;
    margin-bottom: 1em;
    border: 2px solid transparent;
}}

.cta-button.secondary {{
    background-color: transparent;
    color: var(--text-color);
    border-color: var(--text-color);
}}

.cta-button:hover {{
    transform: translateY(-2px);
    opacity: 0.9;
}}

/* Grid Gallery */
.grid-gallery-section h2 {{
    text-align: center;
    margin-bottom: 1.5em;
}}

.grid-container {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    grid-template-rows: repeat(2, 250px);
    grid-template-areas: 
        "img-1 img-1 img-2 img-3"
        "img-1 img-1 img-4 img-5";
    gap: 1em;
    width: 100%;
}}

.grid-container img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 0.75em;
    transition: transform 150ms ease;
    cursor: pointer;
}}

.grid-container img:hover {{
    transform: scale(1.03);
    z-index: 10;
    position: relative;
    box-shadow: 0 10px 20px rgba(0,0,0,0.15);
}}

.img-1 {{ grid-area: img-1; }}
.img-2 {{ grid-area: img-2; }}
.img-3 {{ grid-area: img-3; }}
.img-4 {{ grid-area: img-4; }}
.img-5 {{ grid-area: img-5; }}

/* FAQ Accordion (HTML Details/Summary) */
.faq-section h2 {{
    text-align: center;
    margin-bottom: 1.5em;
}}

details {{
    background-color: var(--base-color);
    border: 1px solid var(--surface-color);
    border-radius: 0.5em;
    margin-bottom: 1em;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}}

summary {{
    padding: 1.2em;
    font-size: 1.1rem;
    font-weight: 600;
    font-family: 'Merriweather', serif;
    cursor: pointer;
    list-style: none; /* remove default triangle in some browsers */
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: background-color 0.2s ease;
}}

summary::-webkit-details-marker {{
    display: none;
}}

summary::after {{
    content: '+';
    font-size: 1.5rem;
    line-height: 1;
    color: var(--primary-color);
    transition: transform 0.3s ease;
}}

details[open] summary::after {{
    transform: rotate(45deg);
}}

details[open] summary {{
    background-color: var(--surface-color);
    border-bottom: 1px solid rgba(0,0,0,0.05);
}}

details > p {{
    padding: 1.2em;
    margin: 0;
}}

/* Responsive Design */
@media (max-width: 800px) {{
    .grid-container {{
        grid-template-columns: repeat(2, 1fr);
        grid-template-rows: repeat(3, 200px);
        grid-template-areas: 
            "img-1 img-1"
            "img-2 img-3"
            "img-4 img-5";
    }}
}}

@media (max-width: 600px) {{
    section {{
        padding: 3em 1.5em;
    }}
    .grid-container {{
        display: flex;
        flex-direction: column;
    }}
    .grid-container img {{
        height: 250px;
    }}
}}
"""

    # === HTML ===
    # Escaping title and body safely
    import html as html_module
    safe_title = html_module.escape(title_text)
    safe_body = html_module.escape(body_text)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title}</title>
    <!-- External Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Merriweather:wght@700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <div class="portfolio-wrapper">
        <!-- Hero Section -->
        <section class="hero-section">
            <div class="flex-container">
                <div class="text-container">
                    <h1>{safe_title}</h1>
                    <p>{safe_body}</p>
                    <a href="#work" class="cta-button">See my Work</a>
                    <a href="#contact" class="cta-button secondary">Contact Me</a>
                </div>
                <div class="hero-image-wrapper">
                    <img src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" alt="Portrait" class="hero-image" loading="lazy">
                </div>
            </div>
        </section>

        <!-- Grid Gallery Section -->
        <section id="work" class="grid-gallery-section surface-section">
            <h2>Some of my best work</h2>
            <div class="grid-container">
                <img src="https://images.unsplash.com/photo-1469474968028-56623f02e42e?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80" alt="Landscape 1" class="img-1" loading="lazy">
                <img src="https://images.unsplash.com/photo-1447752875215-b2761acb3c5d?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80" alt="Nature 2" class="img-2" loading="lazy">
                <img src="https://images.unsplash.com/photo-1433086966358-54859d0ed716?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80" alt="Bridge 3" class="img-3" loading="lazy">
                <img src="https://images.unsplash.com/photo-1472214103451-9374bd1c798e?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80" alt="Mountains 4" class="img-4" loading="lazy">
                <img src="https://images.unsplash.com/photo-1501854140801-50d01698950b?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80" alt="Forest 5" class="img-5" loading="lazy">
            </div>
        </section>

        <!-- FAQ Section (No JS Details/Summary) -->
        <section id="contact" class="faq-section surface-section">
            <h2>Common Questions</h2>
            
            <details>
                <summary>How much does a project cost?</summary>
                <p>Every project is entirely unique. Pricing is determined after a detailed discovery call where we align on scope, deliverables, and timelines. Projects typically start at $2,500.</p>
            </details>

            <details>
                <summary>Do you take on international clients?</summary>
                <p>Yes! I work with clients all around the globe. We coordinate communication asynchronously and schedule key meetings to accommodate timezone differences smoothly.</p>
            </details>

            <details>
                <summary>How can I contact you?</summary>
                <p>The best way to reach me is via email at <strong>hello@example.com</strong>. I typically respond within 24-48 business hours.</p>
            </details>
        </section>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    # The beauty of this pattern is that it requires 0 JavaScript to function.
    js = f"""// Semantic Portfolio Showcase
// The layout, grid gallery, and accordion are fully functional using native HTML5 and CSS.
// No JavaScript is required for the core visual mechanisms!

document.addEventListener('DOMContentLoaded', () => {{
    console.log("Portfolio loaded natively. Zero JS layout dependencies required.");
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
