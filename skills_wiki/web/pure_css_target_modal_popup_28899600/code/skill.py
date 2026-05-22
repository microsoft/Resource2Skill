def create_component(
    output_dir: str,
    title_text: str = "CSS Modal Popup",
    body_text: str = "This popup is created entirely without JavaScript. It uses the CSS :target pseudo-class tied to the URL hash to toggle its visibility and trigger smooth animations.",
    color_scheme: str = "light",        # "dark" or "light"
    accent_color: str = "#b741ee",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Pure CSS :target Modal Popup.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#121212"
        text_color = "#e0e0e0"
        surface_bg = "#242424"
        surface_text = "#ffffff"
        backdrop = "rgba(0, 0, 0, 0.7)"
        shadow = "rgba(0, 0, 0, 0.5)"
    else:
        bg_color = "#f8f9fa"
        text_color = "#333333"
        surface_bg = "#ffffff"
        surface_text = "#111111"
        backdrop = "rgba(0, 0, 0, 0.4)"
        shadow = "rgba(0, 0, 0, 0.15)"

    # === CSS ===
    css = f"""/* Pure CSS :target Modal Popup — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --surface-bg: {surface_bg};
    --surface-text: {surface_text};
    --accent: {accent_color};
    --backdrop: {backdrop};
    --shadow: {shadow};
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}}

/* Main Page Container styling */
.container {{
    width: {width_px}px;
    max-width: 100%;
    height: {height_px}px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
}}

.page-title {{
    margin-bottom: 2rem;
    font-size: 2rem;
    letter-spacing: -0.02em;
    text-transform: uppercase;
}}

/* Buttons */
.btn {{
    display: inline-block;
    padding: 12px 24px;
    background-color: var(--accent);
    color: #ffffff;
    text-decoration: none;
    font-weight: 600;
    border-radius: 8px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    transition: filter 0.2s ease, transform 0.2s ease;
    margin: 0.5rem;
}}

.btn:hover {{
    filter: brightness(1.1);
    transform: translateY(-2px);
}}

/* === The CSS-Only Popup Core Logic === */

.popup-wrapper {{
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: var(--backdrop);
    z-index: 99;
    
    /* Flexbox used to center the popup card */
    display: flex;
    justify-content: center;
    align-items: center;
    
    /* Hidden State */
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.4s ease;
}}

/* When the wrapper's ID matches the URL hash, display it */
.popup-wrapper:target {{
    opacity: 1;
    pointer-events: all;
}}

.popup-inner {{
    background-color: var(--surface-bg);
    color: var(--surface-text);
    padding: 32px;
    width: 90%;
    max-width: 500px;
    border-radius: 16px;
    box-shadow: 0px 8px 24px var(--shadow);
    text-align: left;
    
    /* Slight scale down for an entrance animation */
    transform: scale(0.95);
    transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}}

/* Trigger the inner card to scale up when target is active */
.popup-wrapper:target .popup-inner {{
    transform: scale(1);
}}

.popup-inner h3 {{
    font-size: 1.5rem;
    margin-bottom: 1rem;
}}

.popup-inner p {{
    font-size: 1rem;
    line-height: 1.6;
    color: inherit;
    opacity: 0.8;
    margin-bottom: 2rem;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CSS Popup</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="container">
        <h1 class="page-title">My CSS Popup</h1>
        <div>
            <!-- Triggers updating the URL Hash to #popup1 or #popup2 -->
            <a href="#popup1" class="btn">Open Popup 1</a>
            <a href="#popup2" class="btn">Open Popup 2</a>
        </div>
    </main>

    <!-- Popup 1 -->
    <div id="popup1" class="popup-wrapper">
        <div class="popup-inner">
            <h3>{title_text} 1</h3>
            <p>{body_text}</p>
            <!-- Clicking this sets URL hash to "#" removing the target match -->
            <a href="#" class="btn">Close Popup</a>
        </div>
    </div>

    <!-- Popup 2 -->
    <div id="popup2" class="popup-wrapper">
        <div class="popup-inner">
            <h3>{title_text} 2</h3>
            <p>This is a secondary popup demonstrating how reusable the :target class structure is. You can add as many as you need!</p>
            <a href="#" class="btn">Close Popup</a>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// No JavaScript required for this component!
// The entire state mechanism is handled natively by the browser URL hash and the CSS :target pseudo-class.

console.log("CSS :target Modal Popup successfully loaded. Click the buttons to observe hash-based routing.");
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
