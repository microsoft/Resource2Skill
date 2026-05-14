### 1. High-level Design Pattern Extraction

> **Skill Name**: Dynamic Glassmorphism Theme Toggle

* **Core Visual Mechanism**: The defining mechanism is a fluid, CSS-variable-driven transition between light and dark modes. It uses an interactive toggle switch that triggers a global body class change (`.dark-mode`). The aesthetic heavily relies on glassmorphism (`backdrop-filter: blur()`) applied to the main content container, which sits atop a subtle, colorful ambient background glow. When the theme swaps, the background, text colors, and surface opacities interpolate smoothly, providing a polished and satisfying visual shift.

* **Why Use This Skill (Rationale)**: Implementing a dark mode toggle is an essential UX requirement for modern web applications. Doing it via a top-level CSS class (like on the `<body>` tag) that switches CSS variables ensures the entire color system updates simultaneously and reliably. Adding a transition duration to the background and color properties creates a premium, seamless experience rather than a jarring flash of color.

* **Overall Applicability**: This pattern is universally applicable across modern websites, particularly useful in SaaS dashboards, portfolios, blogs, and settings panels where user customization and visual comfort in low-light environments are prioritized.

* **Value Addition**: Beyond a standard harsh color swap, this technique incorporates a frosted-glass overlay that adapts its opacity based on the active theme, maintaining depth and visual hierarchy. The ambient background blob also reacts by dimming in dark mode, ensuring the contrast remains optimal.

* **Browser Compatibility**: Fully supported in modern browsers. `backdrop-filter` requires the `-webkit-` prefix for older Safari versions. CSS variables and `classList.toggle` are universally supported.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Theming Logic**: Defined at the `:root` level with light mode defaults and overridden inside `body.dark-mode`. 
  - **Colors (Light Theme)**: Background `#f3f4f6`, Text `#1f2937`, Card Surface `rgba(255, 255, 255, 0.7)`.
  - **Colors (Dark Theme)**: Background `#111827`, Text `#f9fafb`, Card Surface `rgba(31, 41, 55, 0.7)`.
  - **Accent**: A vivid color (configurable, e.g., cyan or pink) used for the active toggle state and the ambient background glow.
  - **Typography**: Clean sans-serif ('Inter' or 'Poppins') with high contrast weights.
  - **Key CSS Properties**: `transition` for smooth crossfading, `backdrop-filter: blur(20px)` for the frosted glass effect, and CSS variables (`var(--bg)`) to manage states without duplicating classes.

* **Step B: Layout & Compositional Style**
  - **Layout**: Centered using Flexbox on the `<body>`. The main card has a responsive width bounded by the provided parameters but defaults to a max width of 90% to prevent overflow.
  - **Layering (Z-Index)**: 
    - `-1`: The ambient gradient blob (decorative).
    - `1`: The main glass card container.
  - **Proportions**: The toggle switch is a classic 60x32px pill shape with a 24px sliding circular thumb, offering an accessible hit target.

* **Step C: Interactive Behavior & Animations**
  - **Trigger**: A visually hidden `<input type="checkbox">` wrapped in a `<label>`.
  - **DOM Manipulation**: JavaScript listens for the `change` event on the checkbox and adds/removes the `dark-mode` class on the `document.body`.
  - **Transitions**: 
    - The body background and text color crossfade over `0.4s ease`.
    - The toggle thumb translates on the X-axis using `cubic-bezier(0.4, 0, 0.2, 1)` for a snappy, physics-based sliding feel.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Theme State Management** | CSS Variables + JS class toggle | The most robust and scalable way to handle dark mode. JS handles the state, CSS variables dynamically update the colors. |
| **Smooth Color Transition** | CSS `transition` on body | Applying transitions to `background-color` and `color` on the body ensures a soft crossfade. |
| **Card Transparency** | CSS `backdrop-filter` | Provides native real-time blurring of the decorative background element, creating modern glassmorphism. |
| **Custom Toggle Switch** | Checkbox Hack (CSS `+` selector) | Allows creating a highly stylized, accessible toggle switch without complex JS positioning logic. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Theme Toggle Example",
    body_text: str = "Experience a seamless transition between light and dark modes.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#ec4899",     # Pink accent color
    width_px: int = 600,
    height_px: int = 400,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing a seamless dark mode toggle with glassmorphism.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)
    
    # Determine initial state flags based on the requested color scheme
    is_dark = color_scheme.lower() == "dark"
    body_class = ' class="dark-mode"' if is_dark else ''
    checked_attr = ' checked' if is_dark else ''

    # === CSS ===
    css = f"""/* Theme Toggle — Generated Component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    /* Light Theme Tokens */
    --bg-light: #f3f4f6;
    --text-light: #1f2937;
    --surface-light: rgba(255, 255, 255, 0.65);
    --border-light: rgba(255, 255, 255, 0.5);
    --blob-opacity-light: 0.3;
    
    /* Dark Theme Tokens */
    --bg-dark: #0f172a;
    --text-dark: #f9fafb;
    --surface-dark: rgba(30, 41, 59, 0.65);
    --border-dark: rgba(255, 255, 255, 0.08);
    --blob-opacity-dark: 0.15;

    /* Shared / Dynamic Properties */
    --accent: {accent_color};
    --container-width: {width_px}px;
    --container-height: {height_px}px;
}}

/* Apply Light Mode by Default */
body {{
    --bg: var(--bg-light);
    --text: var(--text-light);
    --surface: var(--surface-light);
    --border: var(--border-light);
    --blob-opacity: var(--blob-opacity-light);
}}

/* Override with Dark Mode Tokens */
body.dark-mode {{
    --bg: var(--bg-dark);
    --text: var(--text-dark);
    --surface: var(--surface-dark);
    --border: var(--border-dark);
    --blob-opacity: var(--blob-opacity-dark);
}}

body {{
    font-family: 'Poppins', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    /* The core transition for the seamless theme swap */
    transition: background-color 0.5s ease, color 0.5s ease;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    position: relative;
}}

/* Decorative Ambient Background */
.ambient-blob {{
    position: absolute;
    width: 60vw;
    height: 60vw;
    max-width: 800px;
    max-height: 800px;
    background: radial-gradient(circle, var(--accent) 0%, transparent 60%);
    filter: blur(80px);
    opacity: var(--blob-opacity);
    z-index: -1;
    pointer-events: none;
    transition: opacity 0.5s ease;
}}

/* Main Glassmorphism Card */
.card {{
    width: var(--container-width);
    min-height: var(--container-height);
    max-width: 90vw;
    padding: 3rem 2rem;
    border-radius: 24px;
    background: var(--surface);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border: 1px solid var(--border);
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.15);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    transition: background-color 0.5s ease, border-color 0.5s ease, box-shadow 0.5s ease;
}}

body.dark-mode .card {{
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.4);
}}

.title {{
    font-size: 2.25rem;
    font-weight: 600;
    margin-bottom: 1rem;
    letter-spacing: -0.02em;
}}

.body-text {{
    font-size: 1.125rem;
    line-height: 1.6;
    opacity: 0.8;
    margin-bottom: 2.5rem;
    max-width: 80%;
}}

/* Custom Toggle Switch Container */
.toggle-wrapper {{
    display: flex;
    align-items: center;
    gap: 1rem;
    font-size: 1.5rem;
    background: rgba(0, 0, 0, 0.05);
    padding: 1rem 1.5rem;
    border-radius: 999px;
    border: 1px solid var(--border);
    transition: background-color 0.5s ease;
}}

body.dark-mode .toggle-wrapper {{
    background: rgba(0, 0, 0, 0.3);
}}

/* The Hidden Input */
.switch {{
    position: relative;
    display: inline-block;
    width: 64px;
    height: 34px;
}}

.switch input {{
    opacity: 0;
    width: 0;
    height: 0;
}}

/* The Sliding Track */
.slider {{
    position: absolute;
    cursor: pointer;
    top: 0; left: 0; right: 0; bottom: 0;
    background-color: rgba(0, 0, 0, 0.2);
    transition: background-color 0.4s ease;
    border-radius: 34px;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
}}

body.dark-mode .slider {{
    background-color: rgba(255, 255, 255, 0.1);
}}

/* The Thumb Indicator */
.slider::before {{
    position: absolute;
    content: "";
    height: 26px;
    width: 26px;
    left: 4px;
    bottom: 4px;
    background-color: white;
    border-radius: 50%;
    transition: transform 0.4s cubic-bezier(0.4, 0.0, 0.2, 1);
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}}

/* Checked States */
input:checked + .slider {{
    background-color: var(--accent);
}}

input:checked + .slider::before {{
    transform: translateX(30px);
}}

/* Accessibility Focus */
input:focus-visible + .slider {{
    outline: 2px solid var(--text);
    outline-offset: 2px;
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
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body{body_class}>
    <div class="ambient-blob"></div>
    
    <div class="card">
        <h1 class="title">{title_text}</h1>
        <p class="body-text">{body_text}</p>
        
        <div class="toggle-wrapper">
            <span class="icon" aria-hidden="true">☀️</span>
            <label class="switch" aria-label="Toggle Theme">
                <input type="checkbox" id="theme-toggle"{checked_attr}>
                <span class="slider"></span>
            </label>
            <span class="icon" aria-hidden="true">🌙</span>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Theme Toggle Interaction Logic
document.addEventListener('DOMContentLoaded', () => {{
    const themeToggle = document.getElementById('theme-toggle');
    
    themeToggle.addEventListener('change', function() {{
        // Toggle the dark-mode class on the body based on checkbox state
        if (this.checked) {{
            document.body.classList.add('dark-mode');
        }} else {{
            document.body.classList.remove('dark-mode');
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
```

### 4. Accessibility & Performance Notes

* **Accessibility**: 
  - The hidden `<input type="checkbox">` handles native keyboard focus, clickability, and state management, ensuring screen readers understand it's a switch element.
  - Added `:focus-visible` styling to the slider container so that keyboard navigators clearly see when the toggle is actively targeted.
  - The decorative sun and moon emojis are wrapped in `<span>` tags with `aria-hidden="true"` so they are ignored by assistive technologies, preventing redundant visual noise. The `<label>` has an explicit `aria-label`.
* **Performance**: 
  - CSS transitions are strictly applied to properties that trigger minimal layout recalculations (`background-color`, `color`, `opacity`, `transform`).
  - The toggle thumb animation uses `transform: translateX()`, which runs on the GPU and skips main-thread paint and layout pipelines, ensuring silky 60fps animations.
  - The `backdrop-filter` is applied cleanly to a single stationary element (the card), maintaining optimal scroll and rendering performance without straining the GPU.