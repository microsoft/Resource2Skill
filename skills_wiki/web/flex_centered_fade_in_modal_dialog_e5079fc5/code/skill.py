def create_component(
    output_dir: str,
    title_text: str = "Cool tutorial!",
    body_text: str = "Do you like these kind of fast coding tutorials? Let me know in the comments section below. 🤓",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#8853bd",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Flex-Centered Fade-In Modal visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#1a1a2e"
        modal_bg_color = "#2a2a3e"
        text_color = "#f0f0f0"
    else:
        bg_color = "#f8f9fa"
        modal_bg_color = "#ffffff"
        text_color = "#111111"

    # === CSS ===
    css = f"""/* Flex-Centered Fade-In Modal — generated component */
* {{
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --modal-bg: {modal_bg_color};
    --text-color: {text_color};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Poppins', system-ui, -apple-system, sans-serif;
    background: var(--bg-color);
    color: var(--text-color);
    margin: 0;
    min-height: var(--height);
    display: flex;
    align-items: flex-start;
    justify-content: center;
    padding-top: 60px;
    overflow: hidden;
}}

button {{
    background-color: var(--accent);
    border-radius: 20px;
    border: 0;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.3);
    color: #fff;
    cursor: pointer;
    padding: 10px 25px;
    font-family: inherit;
    font-size: 1rem;
    font-weight: 500;
    transition: opacity 0.2s ease;
}}

button:active {{
    opacity: 0.8;
}}

/* The overlay backdrop */
.modal {{
    background-color: rgba(0, 0, 0, 0.4);
    opacity: 0;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    transition: all 0.3s ease-in-out;
    z-index: -1;
    
    /* Flexbox centering magic */
    display: flex;
    align-items: center;
    justify-content: center;
}}

/* The active state toggled via JS */
.modal.open {{
    opacity: 1;
    z-index: 999;
}}

/* The content box */
.modal-inner {{
    background-color: var(--modal-bg);
    border-radius: 8px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    padding: 25px 30px;
    text-align: center;
    width: 380px;
    max-width: 90vw;
}}

.modal-inner h2 {{
    margin: 0 0 15px 0;
    font-size: 1.5rem;
}}

.modal-inner p {{
    line-height: 1.6;
    margin: 0 0 20px 0;
    font-size: 0.95rem;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Modal Tutorial Component</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    
    <button id="openModal">Open Modal</button>

    <div class="modal" id="modal" role="dialog" aria-modal="true">
        <div class="modal-inner">
            <h2>{title_text}</h2>
            <p>{body_text}</p>
            <button id="closeModal">Close</button>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Modal toggle logic
document.addEventListener('DOMContentLoaded', () => {{
    const openBtn = document.getElementById("openModal");
    const closeBtn = document.getElementById("closeModal");
    const modal = document.getElementById("modal");

    // Open modal
    openBtn.addEventListener("click", () => {{
        modal.classList.add("open");
    }});

    // Close modal via button
    closeBtn.addEventListener("click", () => {{
        modal.classList.remove("open");
    }});

    // UX Enhancement: Close modal when clicking the backdrop
    modal.addEventListener("click", (e) => {{
        if (e.target === modal) {{
            modal.classList.remove("open");
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
