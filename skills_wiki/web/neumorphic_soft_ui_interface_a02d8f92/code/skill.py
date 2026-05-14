def create_component(
    output_dir: str,
    title_text: str = "Living Room",
    body_text: str = "Adjust ambient lighting and system state.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Neumorphic (Soft UI) visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#292d32"
        text_color = "#ffffff"
        shadow_dark = "rgba(0, 0, 0, 0.35)"
        shadow_light = "rgba(255, 255, 255, 0.06)"
        text_opacity = "0.6"
    else:
        bg_color = "#e0e5ec"
        text_color = "#4a4a4a"
        shadow_dark = "rgba(163, 177, 198, 0.6)"
        shadow_light = "rgba(255, 255, 255, 0.9)"
        text_opacity = "0.7"

    # === CSS ===
    css = f"""/* Neumorphism Interface — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --shadow-dark: {shadow_dark};
    --shadow-light: {shadow_light};
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
    overflow: hidden;
}}

.container {{
    width: var(--width);
    height: var(--height);
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--bg);
}}

/* -- Core Neumorphic Utilities -- */
.neu-outset {{
    background: var(--bg);
    box-shadow: 8px 8px 16px var(--shadow-dark), 
               -8px -8px 16px var(--shadow-light);
}}

.neu-inset {{
    background: var(--bg);
    box-shadow: inset 6px 6px 12px var(--shadow-dark), 
               inset -6px -6px 12px var(--shadow-light);
}}

/* -- Component Layout -- */
.neu-card {{
    border-radius: 32px;
    padding: 48px 32px;
    width: min(90%, 380px);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 40px;
    /* Larger shadow for the main card depth */
    box-shadow: 16px 16px 32px var(--shadow-dark), 
               -16px -16px 32px var(--shadow-light);
    background: var(--bg);
}}

.header {{
    text-align: center;
}}

.title {{
    font-size: 24px;
    font-weight: 700;
    margin-bottom: 8px;
    color: var(--text);
    letter-spacing: -0.5px;
}}

.body-text {{
    font-size: 14px;
    font-weight: 400;
    opacity: {text_opacity};
    color: var(--text);
    line-height: 1.5;
}}

.controls {{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 32px;
    width: 100%;
}}

/* -- Custom Neumorphic Toggle -- */
.neu-toggle input {{
    display: none;
}}

.toggle-track {{
    width: 80px;
    height: 40px;
    border-radius: 40px;
    position: relative;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    padding: 0 4px;
}}

.toggle-thumb {{
    width: 32px;
    height: 32px;
    border-radius: 50%;
    transition: transform 0.4s cubic-bezier(0.4, 0.0, 0.2, 1);
    display: flex;
    justify-content: center;
    align-items: center;
}}

.indicator {{
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: var(--text);
    opacity: 0.2;
    transition: all 0.3s ease;
}}

.neu-toggle input:checked + .toggle-track .toggle-thumb {{
    transform: translateX(40px);
}}

.neu-toggle input:checked + .toggle-track .indicator {{
    background: var(--accent);
    opacity: 1;
    box-shadow: 0 0 10px var(--accent);
}}

/* -- Status Display -- */
.status-display {{
    width: 100%;
    padding: 16px;
    border-radius: 16px;
    text-align: center;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    transition: color 0.3s ease;
    color: var(--text);
}}

/* -- Action Button -- */
.neu-btn {{
    appearance: none;
    border: none;
    outline: none;
    color: var(--text);
    font-size: 16px;
    font-weight: 600;
    padding: 18px 32px;
    border-radius: 100px;
    cursor: pointer;
    width: 100%;
    transition: all 0.2s ease;
    letter-spacing: 0.5px;
}}

.neu-btn:active {{
    box-shadow: inset 6px 6px 12px var(--shadow-dark), 
               inset -6px -6px 12px var(--shadow-light);
    color: var(--accent);
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
        <div class="neu-card">
            
            <div class="header">
                <h1 class="title">{title_text}</h1>
                <p class="body-text">{body_text}</p>
            </div>
            
            <div class="controls">
                <!-- Neumorphic Toggle Switch -->
                <label class="neu-toggle">
                    <input type="checkbox" id="main-toggle">
                    <div class="toggle-track neu-inset">
                        <div class="toggle-thumb neu-outset">
                            <div class="indicator"></div>
                        </div>
                    </div>
                </label>
                
                <!-- Neumorphic Data Well -->
                <div class="status-display neu-inset" id="status-text">
                    System Offline
                </div>
            </div>

            <!-- Neumorphic Action Button -->
            <button class="neu-btn neu-outset" id="action-btn">Refresh State</button>
            
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Interactive logic for Neumorphic components
document.addEventListener('DOMContentLoaded', () => {{
    const toggle = document.getElementById('main-toggle');
    const statusText = document.getElementById('status-text');
    const btn = document.getElementById('action-btn');

    // Toggle switch interaction
    toggle.addEventListener('change', (e) => {{
        if(e.target.checked) {{
            statusText.textContent = 'System Active';
            statusText.style.color = 'var(--accent)';
        }} else {{
            statusText.textContent = 'System Offline';
            statusText.style.color = 'var(--text)';
        }}
    }});

    // Button press simulation
    btn.addEventListener('click', () => {{
        const originalText = btn.textContent;
        btn.textContent = 'Syncing...';
        btn.style.color = 'var(--accent)';
        
        setTimeout(() => {{
            btn.textContent = originalText;
            btn.style.color = 'var(--text)';
        }}, 800);
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
