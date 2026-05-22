# Role: Agent_Skill_Distiller

### 1. High-level Design Pattern Extraction

> **Skill Name**: Ambient Glassmorphism Theme Switcher

* **Core Visual Mechanism**: The defining visual signature is a heavy reliance on *ambient background light* created by absolute-positioned, heavily blurred shapes (`filter: blur(120px)`) sitting behind a frosted glass container (`backdrop-filter: blur()`). A custom-styled, pill-shaped toggle switch drives a seamless transition between a Light theme (soft greys with warm magenta/orange ambient light) and a Dark theme (deep space blacks with neon cyan/blue ambient light). The entire mood of the interface transforms fluidly when toggled.
* **Why Use This Skill (Rationale)**: Traditional dark mode toggles often just flip background and text colors. By incorporating blurred ambient gradients, the toggle becomes an emotional, spatial transition. The glassmorphism ensures that the UI remains legible while dynamically adopting the color hues of the underlying ambient light, creating a highly cohesive and premium feel.
* **Overall Applicability**: Perfect for modern SaaS landing pages, portfolio sites, Web3 applications, and personalized dashboards where aesthetic impact and immersive user experience are priorities.
* **Value Addition**: It elevates a standard utility (theme switching) into a delightful micro-interaction. The layered blurs create a sense of depth (Z-axis) that makes the interface feel like physical frosted glass floating over colored neon lights.
* **Browser Compatibility**: Requires modern browsers supporting `backdrop-filter` (Safari requires `-webkit-` prefix) and CSS Custom Properties. Minimum versions: Chrome 76, Safari 9 (with prefix), Firefox 103, Edge 70.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Ambient Orbs**: Large `div` elements with `border-radius: 50%`, linear gradients, and massive `blur()` filters.
    - *Light Mode Colors*: Background `#f3f3f3`. Orb gradient from `#fa39ad` (magenta) to `#fa6c4c` (orange).
    - *Dark Mode Colors*: Background `#0c1a1a`. Orb gradient from `#00ffaa` (neon green) to `#0066ff` (bright blue).
  - **Glass Panel**: Translucent overlay.
    - *Light Mode*: `rgba(255, 255, 255, 0.6)` with white border.
    - *Dark Mode*: `rgba(13, 17, 28, 0.6)` with subtle grey border.
  - **Typography**: Clean geometric sans-serif (Inter/Poppins). Hierarchy relies on high contrast in both themes.
  - **Custom Toggle**: Hidden checkbox mapped to a styled label. The indicator translates along the X-axis while changing color.

* **Step B: Layout & Compositional Style**
  - **Layout**: CSS Flexbox centers the main glass panel within the viewport. The ambient orbs are `position: absolute` and pushed to the background (`z-index: 0`). The glass panel is brought forward (`z-index: 10`).
  - **Proportions**: The toggle switch is exactly `50px` wide and `28px` tall, with a `22px` indicator leaving a perfect 3px inner padding.

* **Step C: Interactive Behavior & Animations**
  - **Theming**: Driven entirely by CSS Custom Properties (Variables) attached to the `body`. Toggling a `.dark-mode` class updates the variables, cascading changes instantly.
  - **Smooth Transitions**: Elements use `transition: all 0.4s ease` for colors and opacities.
  - **Toggle Animation**: The switch indicator uses a bouncy cubic-bezier (`transition: transform 0.3s cubic-bezier(0.4, 0.0, 0.2, 1)`) for a tactile physical feel.
  - **JS Logic**: Minimal JS just listens for the `change` event on the checkbox and toggles the class on the `body`.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Theme State Management** | CSS Custom Properties + JS class toggle | Cleaner than managing inline styles via JS; allows CSS to handle all hardware-accelerated transitions. |
| **Ambient Light Orbs** | `filter: blur()` | Native CSS blur allows for responsive, fluid gradients that interact beautifully with transparent overlays. |
| **Frosted Overlay** | CSS `backdrop-filter` | Provides the genuine glassmorphism effect, distorting the ambient orbs behind it in real-time. |
| **Custom Toggle Switch** | Checkbox + Label + `:checked` pseudo-class | Completely accessible and semantically correct way to create a custom switch without complex JS state logic. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Why not Your own Services?",
    body_text: str = "Start Your Self-Hosting Journey with us! Toggle the switch to change the mood.",
    color_scheme: str = "light",        # "dark" or "light"
    accent_color: str = "#fa39ad",      # Base accent color (used for light mode orb)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Ambient Glassmorphism Theme Switcher.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)
    
    # Determine initial states based on color_scheme parameter
    body_class = ' class="dark-mode"' if color_scheme == "dark" else ""
    checked_attr = ' checked' if color_scheme == "dark" else ""

    # === CSS ===
    css = f"""/* Ambient Glassmorphism Theme Switcher */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    /* Light Theme Defaults */
    --bg-color: #f3f3f3;
    --text-color: #1a1a2e;
    --text-muted: #666;
    
    /* Light Mode Ambient Orbs */
    --orb-1-start: {accent_color};
    --orb-1-end: #fa6c4c;
    --orb-2-start: #ffb2cd;
    --orb-2-end: #ffecd2;
    
    /* Light Mode Glass */
    --glass-bg: rgba(255, 255, 255, 0.6);
    --glass-border: rgba(255, 255, 255, 0.8);
    --glass-shadow: rgba(0, 0, 0, 0.05);
    
    /* Light Mode Switch */
    --switch-bg: #ffb2cd;
    --switch-handle: #ffffff;
}}

body.dark-mode {{
    /* Dark Theme Overrides */
    --bg-color: #0c1a1a;
    --text-color: #ffffff;
    --text-muted: #a0aab5;
    
    /* Dark Mode Ambient Orbs */
    --orb-1-start: #00ffaa;
    --orb-1-end: #0066ff;
    --orb-2-start: #4a00e0;
    --orb-2-end: #8e2de2;
    
    /* Dark Mode Glass */
    --glass-bg: rgba(12, 26, 26, 0.5);
    --glass-border: rgba(255, 255, 255, 0.08);
    --glass-shadow: rgba(0, 0, 0, 0.3);
    
    /* Dark Mode Switch */
    --switch-bg: #00ffaa;
    --switch-handle: #0c1a1a;
}}

body {{
    font-family: 'Poppins', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    position: relative;
    transition: background-color 0.6s ease, color 0.6s ease;
}}

/* Ambient Background Orbs */
.ambient-orb {{
    position: absolute;
    border-radius: 50%;
    filter: blur(100px);
    z-index: 0;
    transition: background 0.8s ease, opacity 0.8s ease;
}}

.orb-1 {{
    width: 450px;
    height: 450px;
    top: 10%;
    left: 20%;
    background: linear-gradient(135deg, var(--orb-1-start), var(--orb-1-end));
    opacity: 0.8;
}}

.orb-2 {{
    width: 350px;
    height: 350px;
    bottom: 10%;
    right: 20%;
    background: linear-gradient(135deg, var(--orb-2-start), var(--orb-2-end));
    opacity: 0.6;
}}

/* Main Application Container */
.app-container {{
    position: relative;
    z-index: 10;
    width: 90%;
    max-width: 900px;
    height: 60vh;
    min-height: 500px;
    
    /* Glassmorphism Core */
    background: var(--glass-bg);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border: 1px solid var(--glass-border);
    border-radius: 24px;
    box-shadow: 0 20px 40px var(--glass-shadow);
    
    padding: 40px;
    display: flex;
    flex-direction: column;
    transition: all 0.6s ease;
}}

/* Header & Toggle Layout */
.header {{
    display: flex;
    justify-content: flex-end;
    align-items: center;
    width: 100%;
    margin-bottom: 60px;
}}

.theme-toggle-wrapper {{
    display: flex;
    align-items: center;
    gap: 16px;
    font-weight: 600;
    font-size: 0.95rem;
}}

/* Custom CSS Switch */
.switch-checkbox {{
    display: none;
}}

.switch-label {{
    width: 54px;
    height: 30px;
    background-color: var(--switch-bg);
    border-radius: 100px;
    position: relative;
    cursor: pointer;
    transition: background-color 0.4s ease;
}}

.switch-indicator {{
    width: 24px;
    height: 24px;
    background-color: var(--switch-handle);
    border-radius: 50%;
    position: absolute;
    top: 3px;
    left: 3px;
    transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1), background-color 0.4s ease;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}}

.switch-checkbox:checked + .switch-label .switch-indicator {{
    transform: translateX(24px);
}}

/* Typography inside Glass */
.content {{
    text-align: center;
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}}

h1 {{
    font-size: 3.5rem;
    font-weight: 700;
    margin-bottom: 20px;
    line-height: 1.2;
    letter-spacing: -1px;
}}

p {{
    font-size: 1.25rem;
    color: var(--text-muted);
    font-weight: 400;
    max-width: 600px;
    line-height: 1.6;
    transition: color 0.6s ease;
}}

/* Responsive Scaling */
@media (max-width: 768px) {{
    h1 {{ font-size: 2.5rem; }}
    .app-container {{ padding: 24px; height: 80vh; }}
    .orb-1 {{ width: 300px; height: 300px; }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body{body_class} style="width: {width_px}px; height: {height_px}px; max-width: 100vw; max-height: 100vh;">
    
    <!-- Ambient Lighting Layer -->
    <div class="ambient-orb orb-1"></div>
    <div class="ambient-orb orb-2"></div>

    <!-- Glassmorphism Application Layer -->
    <div class="app-container">
        
        <!-- Header with Switch -->
        <header class="header">
            <div class="theme-toggle-wrapper">
                <span id="theme-label">Lights</span>
                <input type="checkbox" id="theme-toggle" class="switch-checkbox"{checked_attr}>
                <label for="theme-toggle" class="switch-label" aria-label="Toggle dark mode">
                    <span class="switch-indicator"></span>
                </label>
            </div>
        </header>

        <!-- Main Content -->
        <main class="content">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </main>
        
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Ambient Glassmorphism Theme Switcher Logic
document.addEventListener('DOMContentLoaded', () => {{
    const themeToggle = document.getElementById('theme-toggle');
    const themeLabel = document.getElementById('theme-label');
    const body = document.body;

    // Optional: Synchronize label text with state
    const updateLabel = (isDark) => {{
        // While the video keeps it as "Lights", changing it provides better UX feedback
        themeLabel.textContent = isDark ? "Neon" : "Lights"; 
    }};

    // Initialize state
    updateLabel(themeToggle.checked);

    // Event Listener for the custom toggle
    themeToggle.addEventListener('change', function() {{
        const isDarkMode = this.checked;
        
        // Toggle class to trigger CSS Variable cascade
        if (isDarkMode) {{
            body.classList.add('dark-mode');
        }} else {{
            body.classList.remove('dark-mode');
        }}
        
        updateLabel(isDarkMode);
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

* **Accessibility (a11y)**:
  * The custom toggle uses a genuine `<input type="checkbox">` hidden via `display: none` visually, but linked to a `<label>` using the `for` attribute. This guarantees that clicking the label toggles the state reliably.
  * *Note*: If stricter screen-reader support is needed, the checkbox should be hidden using `.sr-only` clipping CSS rather than `display: none`, so it remains focusable via keyboard navigation.
  * Color contrast ratios dynamically shift via CSS variables, ensuring the text remains highly readable over the changing frosted glass backgrounds.
* **Performance**:
  * `backdrop-filter` is hardware-accelerated but can be demanding on low-end mobile devices when layered. Providing a fallback background color with higher opacity ensures it degrades gracefully if the blur isn't rendered.
  * Animating CSS variables (like `--bg-color`) is generally smooth in modern browsers, but for strictly 60fps animations, animating `opacity` or `transform` is preferred. The custom toggle indicator uses `transform: translateX()`, which triggers no layout reflows, ensuring the physical movement of the switch is perfectly smooth.