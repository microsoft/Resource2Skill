def create_component(
    output_dir: str,
    title_text: str = "Cool tutorial!",
    body_text: str = "Do you like these kind of fast coding tutorials? Let me know in the comments section below.",
    color_scheme: str = "light",        # "dark" or "light"
    accent_color: str = "#8b53bd",     # CSS hex color for accent (Purple matches the tutorial)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Smooth Fade-In Centered Modal.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#000000"
        container_bg = "#111111"
        text_color = "#ffffff"
        card_bg = "#222222"
        card_text = "#ffffff"
        text_muted = "#aaaaaa"
        backdrop = "rgba(0, 0, 0, 0.7)"
    else:
        bg_color = "#e2e8f0"
        container_bg = "#ffffff"
        text_color = "#333333"
        card_bg = "#ffffff"
        card_text = "#111111"
        text_muted = "#666666"
        backdrop = "rgba(0, 0, 0, 0.5)"

    # === CSS ===
    css = f"""/* Smooth Fade-In Centered Modal */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --container-bg: {container_bg};
    --text: {text_color};
    --card-bg: {card_bg};
    --card-text: {card_text};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --backdrop: {backdrop};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Poppins', 'Inter', system-ui, -apple-system, sans-serif;
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
    max-width: 100vw;
    max-height: 100vh;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: var(--container-bg);
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    overflow: hidden; /* Contains the absolute modal */
}}

/* Button Styling */
.btn {{
    background: var(--accent);
    color: #ffffff;
    border: none;
    border-radius: 20px;
    padding: 10px 25px;
    font-family: inherit;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    transition: opacity 0.2s ease;
}}

.btn:hover {{
    opacity: 0.9;
}}

.btn:active {{
    opacity: 0.7;
}}

/* Modal Overlay Wrapper */
.modal {{
    /* position: fixed; is standard for full-page modals, but absolute is used here to sandbox it within the container */
    position: absolute; 
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: var(--backdrop);
    display: flex;
    align-items: center;
    justify-content: center;
    
    /* Hidden state */
    opacity: 0;
    z-index: -1;
    pointer-events: none;
    
    /* Animation timing */
    transition: opacity 0.3s ease-in-out, z-index 0s linear 0.3s;
}}

/* Modal Active State */
.modal.open {{
    opacity: 1;
    z-index: 999;
    pointer-events: auto;
    transition: opacity 0.3s ease-in-out, z-index 0s linear 0s;
}}

/* Inner Modal Card */
.modal-inner {{
    background-color: var(--card-bg);
    color: var(--card-text);
    border-radius: 20px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    padding: 24px 32px;
    text-align: center;
    width: 380px;
    max-width: 90%;
    
    /* Subtle pop-in effect */
    transform: translateY(10px) scale(0.95);
    transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}}

.modal.open .modal-inner {{
    transform: translateY(0) scale(1);
}}

.modal-inner h2 {{
    margin: 0;
    font-size: 1.5rem;
    font-weight: 600;
}}

.modal-inner p {{
    line-height: 1.6;
    margin: 15px 0 25px 0;
    color: var(--text-muted);
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
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <!-- Trigger Button -->
        <button id="openModal" class="btn">Open Modal</button>

        <!-- The Modal -->
        <div class="modal" id="modal">
            <div class="modal-inner">
                <h2>{title_text}</h2>
                <p>{body_text}</p>
                <button id="closeModal" class="btn">Close</button>
            </div>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""document.addEventListener('DOMContentLoaded', () => {{
    const openBtn = document.getElementById('openModal');
    const closeBtn = document.getElementById('closeModal');
    const modal = document.getElementById('modal');

    // Open Modal
    openBtn.addEventListener('click', () => {{
        modal.classList.add('open');
    }});

    // Close Modal via Button
    closeBtn.addEventListener('click', () => {{
        modal.classList.remove('open');
    }});

    // Optional UX enhancement: Close Modal when clicking the dark backdrop
    modal.addEventListener('click', (e) => {{
        if (e.target === modal) {{
            modal.classList.remove('open');
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
