def create_component(
    output_dir: str,
    title_text: str = "Modals are awesome 😎",
    body_text: str = "Lorem ipsum dolor sit amet consectetur, adipisicing elit. Architecto possimus expedita, officiis vitae, minus alias id necessitatibus earum tenetur asperiores quaerat ad commodi rerum nisi esse mollitia fugiat iure eveniet.",
    color_scheme: str = "light",        # "dark" or "light"
    accent_color: str = "#47a386",      # Tutorial used a dark cyan
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Elegant Fade-In Modal visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#121212"
        text_color = "#f5f5f5"
        modal_bg = "#1e1e1e"
        modal_overlay = "rgba(0, 0, 0, 0.7)"
        p_opacity = "0.8"
    else:
        bg_color = "#f0f2f5"
        text_color = "#333333"
        modal_bg = "#ffffff"
        modal_overlay = "rgba(0, 0, 0, 0.3)"
        p_opacity = "0.7"

    # === CSS ===
    css = f"""/* Elegant Fade-In Modal */
* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --modal-bg: {modal_bg};
    --modal-overlay: {modal_overlay};
    --accent-color: {accent_color};
    --p-opacity: {p_opacity};
}}

body {{
    font-family: 'Poppins', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh; /* Allow it to fit inside the test viewport */
}}

/* App Container (Mocking a page) */
.app-container {{
    width: {width_px}px;
    height: {height_px}px;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
}}

/* General Button Styles */
button {{
    background-color: var(--accent-color);
    color: #ffffff;
    border: 0;
    border-radius: 5px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    padding: 10px 25px;
    font-size: 14px;
    font-family: inherit;
    cursor: pointer;
    transition: transform 0.1s ease, box-shadow 0.1s ease;
}}

button:active {{
    transform: scale(0.98);
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}}

/* Modal Container (The dark overlay) */
.modal-container {{
    background-color: var(--modal-overlay);
    display: flex;
    align-items: center;
    justify-content: center;
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    
    /* Animation / Hide logic */
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.3s ease;
    z-index: 1000;
}}

/* The active state class controlled by JS */
.modal-container.show {{
    opacity: 1;
    pointer-events: auto;
}}

/* Modal Content Box */
.modal {{
    background-color: var(--modal-bg);
    border-radius: 5px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    padding: 30px 50px;
    width: 600px;
    max-width: 90%; /* Responsive constraint */
    text-align: center;
    
    /* Optional: add slight pop-in animation to the inner box */
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
    opacity: var(--p-opacity);
    font-size: 14px;
    line-height: 1.6;
    margin-bottom: 20px;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Elegant Fade-In Modal</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    
    <div class="app-container">
        <!-- Main Application Trigger -->
        <button id="open">Click me please</button>

        <!-- Modal Overlay and Box -->
        <div class="modal-container" id="modal_container">
            <div class="modal">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
                <button id="close">Close me</button>
            </div>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Modal Interactive Behavior
document.addEventListener('DOMContentLoaded', () => {{
    // Grab elements from the DOM
    const openBtn = document.getElementById('open');
    const closeBtn = document.getElementById('close');
    const modalContainer = document.getElementById('modal_container');

    // Add 'show' class to reveal the modal
    openBtn.addEventListener('click', () => {{
        modalContainer.classList.add('show');
    }});

    // Remove 'show' class to hide the modal
    closeBtn.addEventListener('click', () => {{
        modalContainer.classList.remove('show');
    }});
    
    // Optional UI enhancement: Close modal when clicking on the dark overlay background
    modalContainer.addEventListener('click', (e) => {{
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
