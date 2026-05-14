# Attribute-Driven Multi-Modal System

## Analysis

# Skill Extraction: Attribute-Driven Multi-Modal System

### 1. High-level Design Pattern Extraction

> **Skill Name**: Attribute-Driven Multi-Modal System

* **Core Visual Mechanism**: A full-viewport, translucent dark overlay containing a centered, scrollable content box. The system supports multiple distinct modals coexisting on the same page, toggled via CSS classes (`display: none` to `display: block`) and mapped through custom HTML data attributes. 
* **Why Use This Skill (Rationale)**: Hardcoding JavaScript for every modal on a page becomes unmaintainable quickly. This pattern uses an architecture where the HTML attributes dictate the behavior (`open-modal="true" modal-id="profile"`). A single, universal JavaScript listener dynamically connects any trigger button to its corresponding modal, allowing infinite scaling of the UI without writing additional JS. Furthermore, its two-layer wrapper design (`.modal` > `.inner_modal`) elegantly solves the problem of modals that are taller than the user's viewport by enabling internal scrolling while keeping the background fixed.
* **Overall Applicability**: Dashboards, administrative interfaces, SaaS platforms, or any page requiring multiple contextual overlays (e.g., Login, User Profile, Settings, Confirmations) without navigating away from the current context.
* **Value Addition**: Transforms a static page into a dynamic application interface. The attribute-targeting logic cleanly decouples the UI layout from the behavioral JavaScript, enforcing a scalable component architecture.
* **Browser Compatibility**: Fully supported across all modern browsers. The original tutorial relies on jQuery, but the provided reproduction translates this logic into modern, performant Vanilla JavaScript, removing external dependencies while maintaining 100% feature parity.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Outer Overlay (`.modal`)**: A fixed, full-screen wrapper with a semi-transparent black background (`rgba(16, 16, 16, 0.8)`). Hidden by default (`display: none`).
  - **Scroll Wrapper (`.inner_modal`)**: Set to `100vh` maximum height with `overflow-y: auto`. This ensures that if the modal content expands beyond the screen size, the user can scroll the modal itself, rather than the background page.
  - **Content Box (`.modal_content`)**: The visible "card" of the modal. Solid white background, constrained width (`width: 600px; max-width: 100%`), with generous internal padding (`50px`).
  - **Trigger Buttons**: Simple block elements with specific mapping attributes.

* **Step B: Layout & Compositional Style**
  - **Positioning Strategy**: The outer container uses `position: fixed; top: 0; z-index: 999;` to trap the visual focus.
  - **Centering Mechanism**: Instead of Flexbox, the tutorial cleverly uses block display with `margin: 5vh auto;` on the content box. This centers the modal horizontally and pushes it down slightly from the top, allowing it to grow vertically downwards. If Flexbox were used to center vertically, excessively tall content would get cut off at the top of the screen.

* **Step C: Interactive Behavior & Animations**
  - **Trigger Event**: Clicking an element with `open-modal="true"` reads its `modal-id` attribute, selects the corresponding modal ID, and adds the `.active` class.
  - **Close Event**: Clicking directly on the `.inner_modal` (the background area surrounding the content box) removes the `.active` class. Crucially, clicking *inside* the `.modal_content` does nothing, preventing accidental closures.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Multi-modal tracking** | Vanilla JS `querySelectorAll` | Replaces the tutorial's jQuery for modern, dependency-free attribute targeting. |
| **Visibility toggling** | CSS class toggling (`.active`) | Simplest, most reliable way to show/hide complex UI elements. |
| **Overflow handling** | CSS `overflow-y: auto` on wrapper | Ensures tall modals don't break the layout or get cut off at the top of the screen. |
| **Background click closing** | JS Event Delegation (`e.target` check) | Allows users to click the dim background to close the modal, matching standard UX expectations. |

#### 3b. Complete Reproduction Code

```python
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
```

### 4. Accessibility & Performance Notes

* **Accessibility**: To make this production-ready for screen readers, you would want to dynamically add `aria-modal="true"`, `role="dialog"`, and trap keyboard focus inside the modal when it opens. The current implementation relies strictly on visual cues matching the tutorial.
* **Performance**: Translating the tutorial from jQuery to Vanilla JavaScript removes the need to download and parse the jQuery library (a saving of ~30KB gzipped). The event delegation pattern (checking `e.target`) ensures that only minimal, highly performant event listeners are attached, preventing memory bloat even if dozens of modals are placed on a single page.
* **Scroll Safety**: The CSS layout (`margin: 5vh auto` inside a `100vh` scrollable wrapper) avoids the common "cutoff" bug found in flexbox-centered modals, ensuring it performs gracefully on mobile devices or screens with short vertical heights. Restoring body scroll upon close guarantees the parent page works as expected afterward.