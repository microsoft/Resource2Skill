def create_component(
    output_dir: str,
    title_text: str = "User Profile",
    body_text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque nisl eros, pulvinar facilisis justo mollis, auctor consequat urna.",
    color_scheme: str = "light",       # "dark" or "light"
    accent_color: str = "#3b82f6",     # CSS hex color for accent
    width_px: int = 600,               # Max width of the modal content
    height_px: int = 800,              # Not strictly enforced to allow natural flow, but used for preview container
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Modular Responsive Overlay Modal System.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        page_bg = "#0f172a"
        modal_bg = "#1e293b"
        text_color = "#f8fafc"
        text_muted = "#94a3b8"
        overlay_color = "rgba(0, 0, 0, 0.85)"
    else:
        page_bg = "#f1f5f9"
        modal_bg = "#ffffff"
        text_color = "#0f172a"
        text_muted = "#475569"
        overlay_color = "rgba(16, 16, 16, 0.8)"

    # === CSS ===
    css = f"""/* Modular Responsive Overlay Modal System */
:root {{
    --page-bg: {page_bg};
    --modal-bg: {modal_bg};
    --text-main: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --overlay: {overlay_color};
    --modal-max-width: {width_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--page-bg);
    color: var(--text-main);
    line-height: 1.6;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    gap: 20px;
}}

/* Trigger Buttons */
.btn-trigger {{
    background-color: var(--modal-bg);
    color: var(--text-main);
    border: 2px solid var(--accent);
    padding: 12px 24px;
    font-size: 1rem;
    font-weight: 600;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}}

.btn-trigger:hover {{
    background-color: var(--accent);
    color: #ffffff;
}}

/* Outermost Modal Layer - The Overlay */
.modal {{
    width: 100vw;
    height: 100vh;
    background-color: var(--overlay);
    position: fixed;
    top: 0;
    left: 0;
    z-index: 9999;
    display: none; /* Hidden by default */
    opacity: 0;
    transition: opacity 0.3s ease;
}}

/* Active State toggled by JS */
.modal.active {{
    display: block;
    opacity: 1;
}}

/* Inner Modal Layer - Handles Overflow and Scrolling */
.inner_modal {{
    max-height: 100vh;
    width: 100%;
    display: block;
    overflow-y: auto; /* Allows scrolling if content is too tall */
    padding: 0 20px;  /* Prevents content from touching screen edges on mobile */
}}

/* Content Box */
.modal_content {{
    width: 100%;
    max-width: var(--modal-max-width);
    background-color: var(--modal-bg);
    display: block;
    margin: 8vh auto; /* Centers horizontally, offset from top */
    padding: 40px;
    border-radius: 12px;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    transform: translateY(20px);
    transition: transform 0.3s ease;
}}

/* Slide up animation when active */
.modal.active .modal_content {{
    transform: translateY(0);
}}

.modal-header {{
    font-size: 1.75rem;
    font-weight: 700;
    margin-bottom: 16px;
    color: var(--accent);
}}

.modal-body {{
    font-size: 1rem;
    color: var(--text-muted);
    margin-bottom: 24px;
}}

.modal-footer {{
    display: flex;
    justify-content: flex-end;
}}

.btn-close-internal {{
    background-color: transparent;
    color: var(--text-muted);
    border: 1px solid var(--text-muted);
    padding: 8px 16px;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 500;
    transition: all 0.2s ease;
}}

.btn-close-internal:hover {{
    background-color: var(--text-muted);
    color: var(--modal-bg);
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Modular Modal System</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <!-- Trigger Buttons -->
    <button class="btn-trigger" data-open-modal="true" data-modal-id="modal-profile">Open Profile Modal</button>
    <button class="btn-trigger" data-open-modal="true" data-modal-id="modal-login">Open Login Modal</button>

    <!-- Modal 1: Profile -->
    <div class="modal" id="modal-profile" role="dialog" aria-modal="true">
        <div class="inner_modal">
            <div class="modal_content">
                <h2 class="modal-header">{title_text}</h2>
                <p class="modal-body">{body_text}</p>
                <div class="modal-footer">
                    <button class="btn-close-internal" data-close-modal="true">Close</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Modal 2: Login -->
    <div class="modal" id="modal-login" role="dialog" aria-modal="true">
        <div class="inner_modal">
            <div class="modal_content">
                <h2 class="modal-header">Secure Login</h2>
                <p class="modal-body">Please enter your credentials to access your personalized dashboard and account settings.</p>
                <div class="modal-footer">
                    <button class="btn-close-internal" data-close-modal="true">Cancel</button>
                </div>
            </div>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Modular Modal System Interaction Logic

document.addEventListener('DOMContentLoaded', () => {{
    
    // Open Modal Logic
    const openButtons = document.querySelectorAll('[data-open-modal="true"]');
    
    openButtons.forEach(btn => {{
        btn.addEventListener('click', (e) => {{
            const modalId = btn.getAttribute('data-modal-id');
            const targetModal = document.getElementById(modalId);
            
            if (targetModal) {{
                targetModal.classList.add('active');
                // Prevent background scrolling when modal is open
                document.body.style.overflow = 'hidden';
            }}
        }});
    }});

    // Close Modal Logic (Clicking background overlay or specific close buttons)
    const modals = document.querySelectorAll('.modal');
    
    modals.forEach(modal => {{
        modal.addEventListener('click', (e) => {{
            // Check if the user clicked the overlay specifically (.inner_modal) 
            // OR if they clicked a button with the data-close-modal attribute
            const clickedOverlay = e.target.classList.contains('inner_modal');
            const clickedCloseBtn = e.target.closest('[data-close-modal="true"]');
            
            if (clickedOverlay || clickedCloseBtn) {{
                modal.classList.remove('active');
                // Restore background scrolling
                document.body.style.overflow = '';
            }}
        }});
    }});

    // Accessibility feature: Close on Escape key press
    document.addEventListener('keydown', (e) => {{
        if (e.key === 'Escape') {{
            const activeModal = document.querySelector('.modal.active');
            if (activeModal) {{
                activeModal.classList.remove('active');
                document.body.style.overflow = '';
            }}
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
