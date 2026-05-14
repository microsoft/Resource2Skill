def create_component(
    output_dir: str,
    title_text: str = "The Best Landing Page",
    body_text: str = "Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#ffffff",     # CSS hex color for accent (button borders/hover)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Minimalist High-Contrast Landing Page.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#050505"
        text_color = "#ffffff"
        btn_text_hover = "#000000"
        # If the user passed white as accent for dark mode, text hover should be black
        if accent_color.lower() in ["#ffffff", "#fff", "white"]:
            btn_text_hover = "#000000"
        else:
            btn_text_hover = bg_color
    else:
        bg_color = "#fafafa"
        text_color = "#111111"
        btn_text_hover = "#ffffff"
        # Adjust hover text color if accent is very light
        if accent_color.lower() in ["#ffffff", "#fff", "white", "#fafafa"]:
            btn_text_hover = "#000000"

    # === CSS ===
    css = f"""/* Minimalist Landing Page — generated component */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --accent-color: {accent_color};
    --btn-text-hover: {btn_text_hover};
    --comp-width: {width_px}px;
    --comp-height: {height_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body, html {{
    width: 100%;
    min-height: 100vh;
    background-color: var(--bg-color);
    color: var(--text-color);
    font-family: 'Roboto', sans-serif;
    overflow-x: hidden;
}}

/* Optional: Constrain to provided dimensions if acting as an embedded component */
.viewport-wrapper {{
    width: 100%;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}}

/* Navigation */
.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 85%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 2.5rem 0;
}}

.logo {{
    font-weight: 700;
    letter-spacing: 4px;
    text-transform: uppercase;
    font-size: 1.1rem;
    cursor: pointer;
}}

.nav-links {{
    display: flex;
    list-style: none;
    gap: 2.5rem;
}}

.nav-links a {{
    color: var(--text-color);
    text-decoration: none;
    font-size: 0.95rem;
    padding-bottom: 4px;
    border-bottom: 2px solid transparent;
    transition: border-color 0.3s ease;
}}

.nav-links a:hover {{
    border-color: var(--accent-color);
}}

/* Main Content Area */
.hero-container {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 85%;
    max-width: 1200px;
    margin: 4rem auto;
    flex: 1;
}}

.info-section {{
    width: 45%;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}}

.subtitle {{
    font-size: 0.9rem;
    font-weight: 300;
    margin-bottom: 1rem;
    opacity: 0.8;
}}

.title {{
    font-size: clamp(3rem, 5vw, 5.5rem);
    font-weight: 700;
    line-height: 1.1;
    margin-bottom: 1.5rem;
}}

.desc {{
    font-size: 1.05rem;
    font-weight: 300;
    line-height: 1.6;
    margin-bottom: 2.5rem;
    opacity: 0.9;
    max-width: 90%;
}}

.btn-primary {{
    background: transparent;
    color: var(--text-color);
    border: 2px solid var(--accent-color);
    padding: 12px 32px;
    font-size: 1rem;
    font-weight: 500;
    border-radius: 50px; /* Slight rounding for modern feel */
    cursor: pointer;
    transition: all 0.4s ease;
    font-family: inherit;
}}

.btn-primary:hover {{
    background-color: var(--accent-color);
    color: var(--btn-text-hover);
}}

/* Illustration */
.illustration-section {{
    width: 50%;
    display: flex;
    justify-content: flex-end;
}}

.illustration-section img {{
    width: 100%;
    max-width: 600px;
    height: auto;
    object-fit: contain;
}}

/* Responsive Breakpoints */
@media screen and (max-width: 900px) {{
    .hero-container {{
        flex-direction: column;
        text-align: center;
        margin: 2rem auto;
        gap: 4rem;
    }}

    .info-section {{
        width: 100%;
        align-items: center;
    }}

    .desc {{
        max-width: 100%;
    }}

    .illustration-section {{
        width: 90%;
        justify-content: center;
    }}
}}

@media screen and (max-width: 600px) {{
    .navbar {{
        flex-direction: column;
        gap: 1.5rem;
    }}
    .nav-links {{
        gap: 1.5rem;
    }}
    .title {{
        font-size: 2.5rem;
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
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="viewport-wrapper">
        <nav class="navbar">
            <div class="logo">CODE HERE</div>
            <ul class="nav-links">
                <li><a href="#">Home</a></li>
                <li><a href="#">About</a></li>
                <li><a href="#">Contact</a></li>
            </ul>
        </nav>
        
        <main class="hero-container">
            <section class="info-section">
                <span class="subtitle">Create something simple</span>
                <h1 class="title">{title_text}</h1>
                <p class="desc">{body_text}</p>
                <button class="btn-primary">Get Started</button>
            </section>
            
            <section class="illustration-section">
                <!-- Using a free, open-source illustration placeholder that fits the vibe -->
                <img src="https://illustrations.popsy.co/amber/freelancer.svg" alt="Hero Illustration">
            </section>
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    # No JS required for the core visual reproduction, but file is created to fulfill requirements.
    js = f"""// Minimalist Landing Page - No JS required for core layout
document.addEventListener('DOMContentLoaded', () => {{
    console.log('Landing page loaded successfully.');
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
