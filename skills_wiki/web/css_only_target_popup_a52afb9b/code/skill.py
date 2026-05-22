def create_component(
    output_dir: str,
    title_text: str = "CSS-Only Popup",
    body_text: str = "This modal is powered entirely by CSS. No JavaScript is required. The magic happens using the :target pseudo-class and URL hashes.",
    color_scheme: str = "light",       # "dark" or "light"
    accent_color: str = "#B741EE",     # Default to the tutorial's purple
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the CSS-Only Target Popup visual effect.
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#121212"
        text_color = "#f0f0f0"
        card_bg = "#1e1e2f"
        card_text = "#ffffff"
        overlay_color = "rgba(0, 0, 0, 0.7)"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        card_bg = "#ffffff"
        card_text = "#333333"
        overlay_color = "rgba(0, 0, 0, 0.3)"

    # === CSS ===
    css = f"""/* CSS-Only Target Popup — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: {bg_color};
    color: {text_color};
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow-x: hidden;
}}

/* Main container styling for the demo */
.demo-container {{
    width: {width_px}px;
    max-width: 100%;
    height: {height_px}px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
    position: relative;
}}

.main-title {{
    font-size: 2.5rem;
    margin-bottom: 24px;
    text-transform: uppercase;
    letter-spacing: 1px;
}}

.button-group {{
    display: flex;
    gap: 16px;
}}

/* Shared Button Styles */
.btn {{
    display: inline-block;
    padding: 12px 24px;
    background-color: {accent_color};
    color: #ffffff;
    text-decoration: none;
    font-weight: 700;
    text-transform: uppercase;
    border-radius: 8px;
    transition: transform 0.2s ease, opacity 0.2s ease;
    cursor: pointer;
}}

.btn:hover {{
    opacity: 0.9;
    transform: translateY(-2px);
}}

/* === CORE POPUP MECHANISM === */
.popup {{
    /* Hidden state */
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.4s ease;
    
    /* Overlay positioning */
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 99;
    background-color: {overlay_color};
    
    /* Flexbox for centering the inner card */
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 16px;
}}

/* Activation state via :target */
.popup:target {{
    opacity: 1;
    pointer-events: all;
}}

/* Inner Modal Card */
.popup-inner {{
    background-color: {card_bg};
    color: {card_text};
    padding: 40px 32px;
    max-width: 600px;
    width: 100%;
    border-radius: 16px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
    text-align: left;
    
    /* Slight drop-in animation setup */
    transform: translateY(20px);
    transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}}

/* Trigger inner animation when target is active */
.popup:target .popup-inner {{
    transform: translateY(0);
}}

.popup-title {{
    font-size: 1.75rem;
    margin-bottom: 16px;
    color: {card_text};
}}

.popup-body {{
    font-size: 1.1rem;
    line-height: 1.6;
    margin-bottom: 32px;
    opacity: 0.85;
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
    
    <div class="demo-container">
        <h1 class="main-title">My CSS Popup</h1>
        
        <div class="button-group">
            <!-- Triggers updating the URL hash to #popup1 -->
            <a href="#popup1" class="btn">Open Popup 1</a>
            <!-- Triggers updating the URL hash to #popup2 -->
            <a href="#popup2" class="btn">Open Popup 2</a>
        </div>
    </div>

    <!-- POPUP 1 -->
    <div id="popup1" class="popup">
        <div class="popup-inner">
            <h3 class="popup-title">{title_text}</h3>
            <p class="popup-body">{body_text}</p>
            <!-- Closes the popup by clearing the specific hash (linking to #) -->
            <a href="#" class="btn">Close Popup</a>
        </div>
    </div>

    <!-- POPUP 2 (Demonstrating multi-modal support automatically) -->
    <div id="popup2" class="popup">
        <div class="popup-inner">
            <h3 class="popup-title">Popup 2</h3>
            <p class="popup-body">Because this relies purely on CSS and HTML ID attributes, you can have as many popups on the page as you want without writing any additional routing or state-management logic.</p>
            <a href="#" class="btn">Close Popup</a>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// CSS-Only Target Popup — Interactive behavior
// The core mechanism is entirely CSS-based using the :target pseudo-class.
// No JavaScript is required to open, animate, or close these popups.

document.addEventListener('DOMContentLoaded', () => {{
    console.log("Component loaded. Popups are fully operational without JS.");
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
