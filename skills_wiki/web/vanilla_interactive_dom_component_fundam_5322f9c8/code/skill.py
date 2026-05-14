def create_component(
    output_dir: str,
    title_text: str = "Web Fundamentals",
    body_text: str = "This interactive card is built using the core pillars of web development: HTML, CSS, and Vanilla JavaScript.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 400,
    height_px: int = 500,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Vanilla Interactive DOM Component.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
        surface_color = "rgba(255, 255, 255, 0.06)"
        button_text = "#ffffff"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        surface_color = "rgba(0, 0, 0, 0.04)"
        button_text = "#ffffff"

    # === CSS ===
    css = f"""/* Vanilla Interactive DOM Component — generated styles */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --btn-text: {button_text};
    --width: {width_px}px;
    --min-height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

#interactive-card {{
    width: var(--width);
    min-height: var(--min-height);
    background: var(--surface);
    border: 2px solid var(--accent);
    padding: 32px;
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    gap: 20px;
}}

.card-title {{
    color: var(--accent);
    font-size: 1.8rem;
    font-weight: 700;
}}

.card-body {{
    font-size: 1rem;
    line-height: 1.5;
}}

#dynamic-list {{
    list-style-position: inside;
    background: rgba(0, 0, 0, 0.1);
    padding: 16px;
    border-radius: 4px;
    font-family: monospace;
    font-size: 1.1rem;
}}

#dynamic-list li {{
    margin-bottom: 8px;
}}

#dynamic-list li:last-child {{
    margin-bottom: 0;
}}

#action-btn {{
    margin-top: auto; /* Pushes button to bottom if height allows */
    padding: 12px 24px;
    background: var(--accent);
    color: var(--btn-text);
    border: none;
    border-radius: 4px;
    font-size: 1.1rem;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s ease;
}}

#action-btn:hover {{
    opacity: 0.9;
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
    
    <div id="interactive-card">
        <h2 class="card-title">{title_text}</h2>
        <p class="card-body">{body_text}</p>
        
        <!-- This list will be populated by JavaScript -->
        <ul id="dynamic-list"></ul>
        
        <button id="action-btn">Trigger Action</button>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Vanilla JavaScript Fundamentals
document.addEventListener('DOMContentLoaded', function() {{
    
    // 1. Variables, Arrays, and Loops for DOM manipulation
    var coreSkills = ['HTML5 Structure', 'CSS3 Styling', 'JavaScript Logic', 'DOM Manipulation'];
    var listElement = document.getElementById('dynamic-list');
    var listHTML = '';

    for (var i = 0; i < coreSkills.length; i++) {{
        listHTML = listHTML + '<li>' + coreSkills[i] + '</li>';
    }}
    
    // Injecting the generated HTML string into the DOM
    listElement.innerHTML = listHTML;


    // 2. Event Listeners and Conditional Logic
    var actionBtn = document.getElementById('action-btn');
    var hasBeenClicked = false;

    actionBtn.addEventListener('click', function() {{
        if (hasBeenClicked === false) {{
            // Update DOM element text and style
            actionBtn.innerHTML = 'Event Fired Successfully!';
            actionBtn.style.background = '#28a745'; // Success green
            hasBeenClicked = true;
            
            console.log('Button was clicked for the first time.');
        }} else {{
            // Trigger native browser alert for subsequent clicks
            alert('You have already triggered the action on this component!');
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
