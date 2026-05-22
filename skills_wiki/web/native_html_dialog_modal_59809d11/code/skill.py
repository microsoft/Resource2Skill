def create_component(
    output_dir: str,
    title_text: str = "Native HTML Modal",
    body_text: str = "This modal is powered entirely by the native HTML <dialog> element. It requires minimal JavaScript, manages focus automatically, and can be closed using the Escape key.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#6366f1",     # CSS hex color for accent (indigo)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Native HTML Dialog Modal.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        page_bg = "#0f172a"
        page_text = "#94a3b8"
        dialog_bg = "#1e293b"
        dialog_text = "#f8fafc"
        backdrop_color = "rgba(0, 0, 0, 0.7)"
        border_color = "#334155"
    else:
        page_bg = "#f1f5f9"
        page_text = "#475569"
        dialog_bg = "#ffffff"
        dialog_text = "#0f172a"
        backdrop_color = "rgba(15, 23, 42, 0.4)"
        border_color = "#e2e8f0"

    # === CSS ===
    css = f"""/* Native HTML Dialog Modal — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --page-bg: {page_bg};
    --page-text: {page_text};
    --dialog-bg: {dialog_bg};
    --dialog-text: {dialog_text};
    --accent: {accent_color};
    --backdrop: {backdrop_color};
    --border: {border_color};
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--page-bg);
    color: var(--page-text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 2rem;
    overflow: hidden;
}}

/* Main Page Content styling */
.hero {{
    text-align: center;
    max-width: 600px;
    padding: 2rem;
}}

.hero h1 {{
    color: var(--dialog-text);
    margin-bottom: 1rem;
}}

/* Button Styling */
button {{
    background: var(--accent);
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
    font-weight: 600;
    border-radius: 6px;
    cursor: pointer;
    transition: filter 0.2s ease, transform 0.1s ease;
}}

button:hover {{
    filter: brightness(1.1);
}}

button:active {{
    transform: scale(0.98);
}}

button.outline-btn {{
    background: transparent;
    color: var(--dialog-text);
    border: 1px solid var(--border);
}}

button.outline-btn:hover {{
    background: var(--border);
}}

/* === The Native Dialog Element === */
dialog.custom-modal {{
    /* The browser automatically centers the dialog when opened via showModal() */
    background: var(--dialog-bg);
    color: var(--dialog-text);
    
    /* Reset default browser styles */
    border: 0; 
    
    /* Custom presentation */
    border-radius: 12px;
    padding: 2rem;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
    
    /* Sizing constraints */
    width: 90%;
    max-width: 450px;
    
    /* Ensure it handles long content gracefully */
    max-height: 85vh;
    overflow-y: auto;
}}

/* === The Backdrop === */
/* Styled pseudo-element that appears behind the modal */
dialog.custom-modal::backdrop {{
    background: var(--backdrop);
    backdrop-filter: blur(4px); /* Modern touch for frosted glass effect */
}}

/* Dialog Inner Content Styling */
.modal-header {{
    margin-bottom: 1rem;
}}

.modal-header h2 {{
    font-size: 1.5rem;
}}

.modal-body {{
    line-height: 1.6;
    margin-bottom: 2rem;
    color: var(--page-text);
}}

/* Flex container for modal action buttons */
.modal-actions {{
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
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
    
    <div class="hero">
        <h1>{title_text}</h1>
        <p>Explore the power of the native dialog element.</p>
        <br>
        <button id="open-modal-btn">Open Dialog</button>
    </div>

    <!-- The Native Dialog Element -->
    <dialog id="my-modal" class="custom-modal">
        <div class="modal-header">
            <h2>Settings Update</h2>
        </div>
        
        <div class="modal-body">
            <p>{body_text}</p>
        </div>

        <div class="modal-actions">
            <!-- Form method="dialog" automatically closes the modal on submit without JS -->
            <form method="dialog">
                <button type="submit" class="outline-btn">Close natively</button>
            </form>
            
            <!-- Standard button handled via JS -->
            <button id="close-modal-btn">Close via JS</button>
        </div>
    </dialog>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Native HTML Dialog Modal — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const modal = document.querySelector('#my-modal');
    const openBtn = document.querySelector('#open-modal-btn');
    const closeBtn = document.querySelector('#close-modal-btn');

    // 1. Open the modal using .showModal()
    // NOTE: .show() exists but does not create the backdrop or act as a true modal. 
    // Always use .showModal() for traditional popups.
    openBtn.addEventListener('click', () => {{
        modal.showModal();
    }});

    // 2. Close the modal using .close()
    // (Note: The "Close natively" button works automatically because it is 
    // a submit button inside a <form method="dialog">)
    closeBtn.addEventListener('click', () => {{
        modal.close();
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
