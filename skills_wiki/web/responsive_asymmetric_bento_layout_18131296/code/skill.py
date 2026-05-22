def create_component(
    output_dir: str,
    title_text: str = "Bento Grid System",
    body_text: str = "Responsive, asymmetric layouts powered by Flexbox.",
    color_scheme: str = "dark",
    accent_color: str = "#8733fc",
    width_px: int = 1000,
    height_px: int = 800,
    **kwargs,
) -> dict:
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derived colors mapped to the video's vibrant bento palette
    if color_scheme == "dark":
        bg_color = "#141414"
        text_color = "#ffffff"
        c_red = "#f93131"
        c_orange = "#fb9510"
        c_blue = "#3b31f5"
    else:
        bg_color = "#f4f4f5"
        text_color = "#18181b"
        c_red = "#e11d48"
        c_orange = "#ea580c"
        c_blue = "#4f46e5"

    css = f"""/* Responsive Asymmetric Bento Layout */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --c-header: {accent_color};
    --c-left: {c_red};
    --c-right: {c_orange};
    --c-footer: {c_blue};
    --radius: 2em;
    --gap: 1em;
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: #000;
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.component-wrapper {{
    width: var(--width);
    height: var(--height);
    background: var(--bg);
    overflow-y: auto;
    padding: 2em 3em;
    /* Define container for relative responsiveness */
    container-type: inline-size;
    container-name: bento;
}}

/* Base Container Rules */
.container {{
    display: flex;
    flex-direction: column;
    gap: var(--gap);
    /* Make each layout group take roughly the full height of the wrapper */
    min-height: calc(100cqh - 4em);
    margin-bottom: var(--gap);
}}

.container:last-child {{
    margin-bottom: 0;
}}

/* Universal Block Styling */
.block {{
    border-radius: var(--radius);
    padding: 2em;
    display: flex;
    flex-direction: column;
    justify-content: center;
    transition: transform 0.2s ease, filter 0.2s ease;
}}

.block:hover {{
    transform: scale(0.99);
    filter: brightness(1.1);
}}

/* Flex Proportions - Vertical (1:4 ratio) */
.header, .footer {{
    flex: 1;
}}

.block-group {{
    flex: 4;
    display: flex;
    gap: var(--gap);
}}

/* Flex Proportions - Horizontal (2:1 ratio) */
.col-left {{
    flex: 2;
}}

.col-right {{
    flex: 1;
}}

/* Specific Colors */
.header {{ background-color: var(--c-header); }}
.col-left {{ background-color: var(--c-left); }}
.col-right {{ background-color: var(--c-right); }}
.footer {{ background-color: var(--c-footer); }}

/* Alternating Layout Logic */
.container.second .block-group {{
    flex-direction: row-reverse;
}}

/* Typography */
h1 {{ font-size: 2.5rem; font-weight: 700; letter-spacing: -0.02em; margin-bottom: 0.2em; }}
h2 {{ font-size: 1.5rem; font-weight: 600; }}
p {{ font-size: 1rem; opacity: 0.9; line-height: 1.5; }}

/* Container Query Responsiveness (Replaces standard Media Queries) */
@container bento (max-width: 768px) {{
    .block-group, .container.second .block-group {{
        flex-direction: column;
    }}
    .component-wrapper {{
        padding: 1.5em;
    }}
    /* Adjust flex weights for mobile stacking */
    .col-left, .col-right {{
        flex: 1; 
    }}
    h1 {{ font-size: 2rem; }}
}}
"""

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
    <div class="component-wrapper">
        
        <!-- Standard Layout -->
        <div class="container">
            <header class="block header">
                <h1>{title_text}</h1>
            </header>
            
            <section class="block-group">
                <div class="block col-left">
                    <h2>Primary Focus</h2>
                    <p>{body_text}</p>
                </div>
                <div class="block col-right">
                    <h2>Secondary</h2>
                </div>
            </section>
        </div>

        <!-- Alternating Layout -->
        <div class="container second">
            <section class="block-group">
                <div class="block col-left">
                    <h2>Feature Deep Dive</h2>
                    <p>Flipped layout using row-reverse, placing the wider block on the right.</p>
                </div>
                <div class="block col-right">
                    <h2>Quick Stat</h2>
                </div>
            </section>
            
            <footer class="block footer">
                <h2>System Footer</h2>
            </footer>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// No JavaScript required for this core Flexbox layout.
// Hover states are handled entirely via CSS transitions.
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
