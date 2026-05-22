def create_component(
    output_dir: str,
    title_text: str = "User Profile",
    body_text: str = "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quo porro fugit aut tempora esse, in labore, eos molestias exercitiationem odit officia soluta alias ipsum similique quia beatae. Commodi numquam voluptate.",
    color_scheme: str = "light",
    accent_color: str = "#3b82f6",
    width_px: int = 600,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Attribute-Driven Multi-Modal System.
    Includes two modals to demonstrate the attribute-mapping architecture.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#1e293b"
        text_color = "#f8fafc"
        surface_color = "#0f172a"
        overlay_color = "rgba(0, 0, 0, 0.85)"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        surface_color = "#ffffff"
        overlay_color = "rgba(16, 16, 16, 0.8)"

    # === CSS ===
    css = f"""/* Attribute-Driven Multi-Modal System */
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
    --overlay: {overlay_color};
    --modal-width: {width_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
}}

/* Trigger Buttons */
.btn {{
    display: block;
    margin: 10px auto;
    font-size: 1rem;
    padding: 12px 24px;
    background-color: var(--surface);
    color: var(--text);
    border: 2px solid var(--accent);
    border-radius: 6px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.2s ease;
}}

.btn:hover {{
    background-color: var(--accent);
    color: #fff;
}}

/* --- Modal Architecture --- */

/* 1. Outer Overlay */
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

/* Visibility Toggle */
.modal.active {{
    display: block;
    opacity: 1;
}}

/* 2. Scroll Wrapper */
.inner_modal {{
    max-height: 100vh;
    box-sizing: border-box;
    display: block;
    overflow-y: auto;
    height: 100%;
    width: 100%;
    padding: 0 20px;
}}

/* 3. Content Box */
.modal_content {{
    width: var(--modal-width);
    max-width: 100%;
    background-color: var(--surface);
    display: block;
    margin: 5vh auto; /* Centers horizontally, pushes down 5vh, allows bottom expansion */
    padding: 50px;
    border-radius: 8px;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    animation: modalSlideIn 0.3s ease-out forwards;
}}

.modal_content h2 {{
    padding-bottom: 20px;
    font-size: 2rem;
    color: var(--accent);
}}

.modal_content p {{
    line-height: 1.6;
    color: var(--text);
    opacity: 0.9;
}}

@keyframes modalSlideIn {{
    from {{
        transform: translateY(-20px);
        opacity: 0;
    }}
    to {{
        transform: translateY(0);
        opacity: 1;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Multi-Modal Architecture</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    
    <!-- Trigger Buttons utilizing custom attributes for targeting -->
    <button class="btn" open-modal="true" modal-id="profile">Open {title_text}</button>
    <button class="btn" open-modal="true" modal-id="settings">Open Settings Modal</button>

    <!-- Modal 1: Profile -->
    <div class="modal" id="profile">
        <div class="inner_modal">
            <div class="modal_content">
                <h2>{title_text}</h2>
                <p>{body_text}</p>
            </div>
        </div>
    </div>

    <!-- Modal 2: Settings (Demonstrating Multi-Modal Capability) -->
    <div class="modal" id="settings">
        <div class="inner_modal">
            <div class="modal_content">
                <h2>Settings Dashboard</h2>
                <p>This is a completely separate modal triggered by the exact same JavaScript function. The architecture maps the button's "modal-id" attribute to this div's ID.</p>
                <br>
                <button class="btn close-btn" style="margin:0;">Simulate Inner Button Action</button>
            </div>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Attribute-Driven Multi-Modal System (Vanilla JS Port)
document.addEventListener('DOMContentLoaded', () => {
    
    // 1. OPEN MODALS
    // Find all elements that declare themselves as modal triggers
    const modalTriggers = document.querySelectorAll('[open-modal="true"]');
    
    modalTriggers.forEach(trigger => {
        trigger.addEventListener('click', () => {
            // Read the target ID from the button's attribute
            const modalId = trigger.getAttribute('modal-id');
            const targetModal = document.getElementById(modalId);
            
            if (targetModal) {
                targetModal.classList.add('active');
                // Optional: Prevent body scrolling when modal is open
                document.body.style.overflow = 'hidden'; 
            }
        });
    });

    // 2. CLOSE MODALS
    // Find all modals to attach background click listeners
    const modals = document.querySelectorAll('.modal');
    
    modals.forEach(modal => {
        modal.addEventListener('click', (e) => {
            // Check if the actual clicked element was the scroll wrapper (the dark background)
            // If they clicked the white .modal_content box, this will be false
            if (e.target.classList.contains('inner_modal')) {
                modal.classList.remove('active');
                document.body.style.overflow = ''; // Restore scrolling
            }
        });
    });

});
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
