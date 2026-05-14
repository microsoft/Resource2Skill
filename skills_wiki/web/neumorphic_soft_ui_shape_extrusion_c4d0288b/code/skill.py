def create_component(
    output_dir: str,
    title_text: str = "Neumorphic Control",
    body_text: str = "Interact with the elements to see the soft-UI extrusion and inset shadow effects.",
    color_scheme: str = "light",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1000,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Neumorphic (Soft UI) visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Neumorphic Color Math / Theme Selection ===
    if color_scheme == "dark":
        bg_color = "#292d32"
        light_shadow = "#363c42"
        dark_shadow = "#1c1e22"
        text_color = "#a0aec0"
        text_heading = "#ffffff"
    else:
        bg_color = "#e0e5ec"
        light_shadow = "#ffffff"
        dark_shadow = "#a3b1c6"
        text_color = "#718096"
        text_heading = "#2d3748"

    # === CSS ===
    css = f"""/* Neumorphic Shape Extrusion — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-base: {bg_color};
    --shadow-light: {light_shadow};
    --shadow-dark: {dark_shadow};
    --text-main: {text_heading};
    --text-sub: {text_color};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-base);
    color: var(--text-main);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

.dashboard-container {{
    width: 100%;
    max-width: var(--width);
    min-height: 600px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4rem;
}}

.header-section {{
    text-align: center;
    max-width: 600px;
}}

.header-section h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    letter-spacing: -0.05em;
}}

.header-section p {{
    color: var(--text-sub);
    line-height: 1.6;
}}

/* The Core Neumorphic Display Area */
.neu-showcase {{
    display: flex;
    gap: 4rem;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
}}

/* Base Neumorphic Class applied to all shapes */
.neu-element {{
    background-color: var(--bg-base);
    border: none;
    outline: none;
    display: flex;
    justify-content: center;
    align-items: center;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    color: var(--text-main);
    font-size: 1.2rem;
    font-weight: 600;
}}

/* 1. The Large Circle (from the video) */
.neu-circle {{
    width: 250px;
    height: 250px;
    border-radius: 50%;
    /* The core neumorphic shadows */
    box-shadow: 
        20px 20px 60px var(--shadow-dark),
        -20px -20px 60px var(--shadow-light);
}}

.neu-circle:hover {{
    /* Convex appearance on hover */
    background: linear-gradient(145deg, var(--shadow-light) 0%, var(--bg-base) 100%);
    transform: translateY(-5px);
    box-shadow: 
        25px 25px 65px var(--shadow-dark),
        -25px -25px 65px var(--shadow-light);
}}

/* 2. The Interactive Button */
.neu-button {{
    padding: 1.5rem 3rem;
    border-radius: 20px;
    cursor: pointer;
    box-shadow: 
        10px 10px 30px var(--shadow-dark),
        -10px -10px 30px var(--shadow-light);
}}

.neu-button:active, .neu-button.active-state {{
    /* Pressed/Inset state */
    box-shadow: 
        inset 10px 10px 20px var(--shadow-dark),
        inset -10px -10px 20px var(--shadow-light);
    color: var(--accent);
    transform: translateY(2px);
}}

/* 3. The Concave Card */
.neu-card {{
    width: 250px;
    height: 250px;
    border-radius: 42px;
    /* Simulate a bowl/concave shape by reversing gradient vs shadows */
    background: linear-gradient(145deg, var(--shadow-dark), var(--shadow-light));
    box-shadow: 
        15px 15px 40px var(--shadow-dark),
        -15px -15px 40px var(--shadow-light);
    padding: 2rem;
    text-align: center;
    flex-direction: column;
    gap: 1rem;
}}

.neu-icon {{
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background-color: var(--bg-base);
    box-shadow: 
        inset 5px 5px 10px var(--shadow-dark),
        inset -5px -5px 10px var(--shadow-light);
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
    <div class="dashboard-container">
        
        <div class="header-section">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </div>

        <div class="neu-showcase">
            <!-- Shape 1: Concave Card -->
            <div class="neu-element neu-card">
                <div class="neu-icon"></div>
                <span style="font-size: 1rem; color: var(--text-sub);">Concave Shape</span>
            </div>

            <!-- Shape 2: Large Floating Circle -->
            <div class="neu-element neu-circle" id="main-circle">
                Hover Me
            </div>

            <!-- Shape 3: Interactive Button -->
            <button class="neu-element neu-button" id="toggle-btn">
                Press Me
            </button>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Interactive logic for Neumorphic components
document.addEventListener('DOMContentLoaded', () => {{
    const btn = document.getElementById('toggle-btn');
    const circle = document.getElementById('main-circle');

    // Add a satisfying toggle interaction to the button
    btn.addEventListener('click', () => {{
        btn.classList.toggle('active-state');
        
        if (btn.classList.contains('active-state')) {{
            btn.textContent = 'Pressed!';
            circle.style.boxShadow = 'inset 20px 20px 60px var(--shadow-dark), inset -20px -20px 60px var(--shadow-light)';
            circle.textContent = 'Recessed';
            circle.style.color = 'var(--accent)';
        }} else {{
            btn.textContent = 'Press Me';
            circle.style.boxShadow = ''; // Reverts to CSS stylesheet value
            circle.textContent = 'Hover Me';
            circle.style.color = 'var(--text-main)';
        }}
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
