def create_component(
    output_dir: str,
    title_text: str = "Modals are 😎",
    body_text: str = "Lorem ipsum dolor sit amet consectetur adipisicing elit. Architecto possimus expedita, officiis vitae, minus alias id necessitatibus earum tenetur asperiores.",
    color_scheme: str = "light",
    accent_color: str = "#47a386",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Smooth Fade-in CSS Modal Overlay.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#121212"
        text_color = "#e0e0e0"
        modal_bg = "#1e1e1e"
        modal_text = "#ffffff"
        overlay_color = "rgba(0, 0, 0, 0.6)"
    else:
        bg_color = "#edeeF6"
        text_color = "#333333"
        modal_bg = "#ffffff"
        modal_text = "#111111"
        overlay_color = "rgba(0, 0, 0, 0.3)"

    # === CSS ===
    css = f"""/* Smooth Fade-in Modal — generated component */
*, *::before, *::after {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --modal-bg: {modal_bg};
    --modal-text: {modal_text};
    --accent: {accent_color};
    --overlay: {overlay_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

/* Component Wrapper (Simulates the browser window) */
.demo-viewport {{
    width: var(--width);
    height: var(--height);
    background-color: var(--bg);
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    border-radius: 8px;
}}

/* Reusable Button Style */
.btn {{
    background-color: var(--accent);
    color: #ffffff;
    border: none;
    border-radius: 5px;
    padding: 10px 25px;
    font-size: 14px;
    font-family: inherit;
    cursor: pointer;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    transition: transform 0.1s ease, box-shadow 0.1s ease;
}}

.btn:active {{
    transform: scale(0.98);
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}}

/* Modal Overlay Container */
.modal-container {{
    background-color: var(--overlay);
    position: absolute; /* Absolute within .demo-viewport, use fixed for full page */
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    
    /* Core Visibility Logic */
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.3s ease;
    z-index: 100;
}}

/* Active State */
.modal-container.show {{
    opacity: 1;
    pointer-events: auto;
}}

/* The Modal Card */
.modal {{
    background-color: var(--modal-bg);
    color: var(--modal-text);
    border-radius: 5px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    padding: 30px 50px;
    width: 600px;
    max-width: 90%;
    text-align: center;
    
    /* Optional: add a slight slide-up effect on reveal */
    transform: translateY(20px);
    transition: transform 0.3s ease;
}}

.modal-container.show .modal {{
    transform: translateY(0);
}}

.modal h1 {{
    margin-bottom: 15px;
    font-size: 24px;
}}

.modal p {{
    opacity: 0.7;
    font-size: 14px;
    line-height: 1.5;
    margin-bottom: 25px;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Modal Component</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="demo-viewport">
        <!-- Trigger Button -->
        <button id="open" class="btn">Click me please</button>

        <!-- Modal Overlay -->
        <div class="modal-container" id="modal_container">
            <div class="modal">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
                <button id="close" class="btn">Close me</button>
            </div>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Smooth Fade-in Modal Behavior
document.addEventListener('DOMContentLoaded', () => {{
    const openBtn = document.getElementById('open');
    const closeBtn = document.getElementById('close');
    const modalContainer = document.getElementById('modal_container');

    // Show modal
    openBtn.addEventListener('click', () => {{
        modalContainer.classList.add('show');
    }});

    // Hide modal
    closeBtn.addEventListener('click', () => {{
        modalContainer.classList.remove('show');
    }});
    
    // Optional Accessibility / UX addition: Close when clicking outside the modal card
    modalContainer.addEventListener('click', (e) => {{
        // If the user clicked directly on the overlay backdrop, not the modal card itself
        if (e.target === modalContainer) {{
            modalContainer.classList.remove('show');
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
