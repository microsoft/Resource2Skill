### 1. High-level Design Pattern Extraction

> **Skill Name**: Animated Theme Toggle & Global Dark Mode Strategy

* **Core Visual Mechanism**: A seamless, global state transition from a light to a dark aesthetic (or vice versa), driven by a smooth, interactive "pill" toggle switch. The technique relies on swapping a central CSS class (e.g., `.dark-mode`) on the root or body element, which triggers a cascade of CSS custom property (variable) updates. This results in a synchronized cross-fade of backgrounds, typography, and card surfaces, while the toggle switch itself animates physically (translating horizontally) to reinforce the state change.
* **Why Use This Skill (Rationale)**: Offering a dark mode improves accessibility and reduces eye strain in low-light environments. Providing a smooth animation during the transition prevents jarring visual flashes, creating a polished, premium feel that respects user preference. The physical toggle provides an immediate, intuitive mental model of a binary state.
* **Overall Applicability**: Essential for modern web applications, SaaS dashboards, blogs, portfolios, and documentation sites where users spend extended periods reading or interacting with dense information.
* **Value Addition**: Transforms a static interface into a user-centric, adaptable environment. The animated toggle and fading colors elevate the perceived quality and technical sophistication of the application.
* **Browser Compatibility**: Fully supported in all modern browsers. Relies on CSS Custom Properties (Variables), CSS Transitions, and the `:checked` pseudo-class (supported in IE11+, Edge, Chrome, Firefox, Safari).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**:
    - *Light Mode*: Background `#f8f9fa`, Surface/Cards `#ffffff`, Text `#1a1a2e`, Soft Shadows `rgba(0,0,0,0.05)`.
    - *Dark Mode*: Background `#0f172a`, Surface/Cards `#1e293b`, Text `#f8fafc`, Soft Shadows `rgba(0,0,0,0.3)`.
    - *Accent*: Configurable (e.g., `#8b5cf6` purple or `#00bfff` cyan), used for the toggle thumb or active states.
  - **Typography**: Clean sans-serif (e.g., 'Inter' or 'Poppins') with distinct font weights (600 for headings, 400 for body) to maintain legibility in both contrast modes.
  - **CSS Constructs**: Heavy use of `var(--token-name)` for all colors. Smooth `transition: background-color 0.3s ease, color 0.3s ease;` applied globally.

* **Step B: Layout & Compositional Style**
  - The toggle is typically positioned in a header or navigation bar.
  - The switch uses an absolute-positioned "thumb" (the circle) inside a relative-positioned "track" (the pill).
  - A hidden `<input type="checkbox">` acts as the state manager. The `<label>` wraps the custom design, making it clickable.

* **Step C: Interactive Behavior & Animations**
  - **Toggle Animation**: When the hidden checkbox is `:checked`, the thumb translates horizontally using `transform: translateX(...)`.
  - **Icon Morphing**: FontAwesome icons (Sun/Moon) cross-fade or swap opacity based on the checked state.
  - **JavaScript Role**: A lightweight event listener attaches to the checkbox. On `change`, it toggles a class (e.g., `dark-mode`) on `document.body` and can optionally save the preference to `localStorage`.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Global Theming | CSS Custom Properties (Variables) | Allows instantaneous, global color swapping by merely changing one parent class, avoiding the need for JS to iterate over elements. |
| Toggle Switch State | CSS `:checked` Pseudo-class | The "Checkbox Hack" allows pure CSS state management for the visual switch, ensuring zero-lag animations independent of the JS thread. |
| Smooth Fades | CSS `transition` | Applying a 0.3s transition to `background-color` and `color` on the `*` selector or specific generic elements ensures everything cross-fades naturally. |
| State Persistence | JavaScript `classList.toggle` | Required to sync the toggle switch with the `body` class to activate the CSS variables globally. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Why Not Your Own Services?",
    body_text: str = "Start Your Self-Hosting Journey with us! Experience seamless theme transitions.",
    color_scheme: str = "light",       # "dark" or "light" sets the initial state
    accent_color: str = "#8b5cf6",     # CSS hex color for accent (e.g., purple)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing an Animated Theme Toggle & Dark Mode Strategy.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)
    
    is_dark = "true" if color_scheme.lower() == "dark" else "false"

    # === CSS ===
    css = f"""/* Animated Theme Toggle & Global Dark Mode */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

:root {{
    /* Light Theme Variables (Default) */
    --bg-color: #f4f4f5;
    --surface-color: #ffffff;
    --text-primary: #18181b;
    --text-secondary: #52525b;
    --accent-color: {accent_color};
    --border-color: #e4e4e7;
    --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
    
    /* Toggle Specific */
    --toggle-track: #d4d4d8;
    --toggle-thumb: #ffffff;
    --icon-sun: #f59e0b;
    --icon-moon: #a1a1aa;
}}

body.dark-mode {{
    /* Dark Theme Variables */
    --bg-color: #09090b;
    --surface-color: #18181b;
    --text-primary: #f4f4f5;
    --text-secondary: #a1a1aa;
    --border-color: #27272a;
    --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2);
    
    /* Toggle Specific */
    --toggle-track: #27272a;
    --toggle-thumb: #18181b;
    --icon-sun: #52525b;
    --icon-moon: #818cf8;
}}

/* Global Reset & Transitions */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Poppins', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-primary);
    transition: background-color 0.4s ease, color 0.4s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

.viewport {{
    width: {width_px}px;
    height: {height_px}px;
    max-width: 100%;
    max-height: 100vh;
    position: relative;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    background-color: var(--bg-color);
    transition: background-color 0.4s ease;
}}

/* Header & Navigation */
header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2rem 4rem;
    border-bottom: 1px solid var(--border-color);
    transition: border-color 0.4s ease;
}}

.logo {{
    font-size: 1.25rem;
    font-weight: 700;
    letter-spacing: -0.025em;
}}

.logo span {{
    color: var(--accent-color);
}}

/* Toggle Switch Styles */
.theme-toggle-wrapper {{
    display: flex;
    align-items: center;
    gap: 1rem;
}}

.theme-toggle-label {{
    font-size: 0.9rem;
    font-weight: 500;
    color: var(--text-secondary);
    transition: color 0.4s ease;
}}

.switch {{
    position: relative;
    display: inline-block;
    width: 64px;
    height: 32px;
}}

.switch input {{
    opacity: 0;
    width: 0;
    height: 0;
}}

.slider {{
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: var(--toggle-track);
    transition: .4s;
    border-radius: 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 8px;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
}}

.slider i {{
    font-size: 14px;
    z-index: 1;
    transition: color 0.4s ease;
}}

.fa-sun {{ color: var(--icon-sun); }}
.fa-moon {{ color: var(--icon-moon); }}

.slider::before {{
    position: absolute;
    content: "";
    height: 24px;
    width: 24px;
    left: 4px;
    bottom: 4px;
    background-color: var(--toggle-thumb);
    transition: .4s cubic-bezier(0.4, 0.0, 0.2, 1);
    border-radius: 50%;
    z-index: 2;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}}

input:checked + .slider {{
    background-color: var(--accent-color);
}}

input:checked + .slider::before {{
    transform: translateX(32px);
    background-color: #ffffff;
}}

input:checked + .slider .fa-moon {{
    color: #ffffff;
}}

/* Main Content Area */
main {{
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 4rem 2rem;
    text-align: center;
}}

h1 {{
    font-size: 3.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    color: var(--text-primary);
    transition: color 0.4s ease;
}}

p {{
    font-size: 1.2rem;
    color: var(--text-secondary);
    max-width: 600px;
    margin-bottom: 3rem;
    transition: color 0.4s ease;
}}

/* Cards Grid */
.cards-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
    width: 100%;
    max-width: 1000px;
}}

.card {{
    background-color: var(--surface-color);
    padding: 2rem;
    border-radius: 1rem;
    box-shadow: var(--shadow);
    border: 1px solid var(--border-color);
    text-align: left;
    transition: background-color 0.4s ease, transform 0.3s ease, box-shadow 0.3s ease, border-color 0.4s ease;
    cursor: pointer;
}}

.card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    border-color: var(--accent-color);
}}

.card h3 {{
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}}

.card p {{
    font-size: 0.95rem;
    margin-bottom: 0;
}}

/* Decorative Background Glow */
.glow {{
    position: absolute;
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, var(--accent-color) 0%, transparent 70%);
    opacity: 0.08;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    pointer-events: none;
    z-index: 0;
    transition: opacity 0.4s ease;
}}

body.dark-mode .glow {{
    opacity: 0.15;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <!-- FontAwesome for Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body class="{'dark-mode' if is_dark == 'true' else ''}">
    <div class="viewport">
        <div class="glow"></div>
        
        <header>
            <div class="logo">Echoes<span>.dev</span></div>
            
            <div class="theme-toggle-wrapper">
                <span class="theme-toggle-label">Lights</span>
                <label class="switch">
                    <input type="checkbox" id="theme-toggle" {'checked' if is_dark == 'true' else ''}>
                    <div class="slider">
                        <i class="fa-solid fa-moon"></i>
                        <i class="fa-solid fa-sun"></i>
                    </div>
                </label>
            </div>
        </header>

        <main>
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
            
            <div class="cards-grid">
                <div class="card">
                    <h3>Speedtest Tracker</h3>
                    <p>Installation guide and monitoring setup.</p>
                </div>
                <div class="card">
                    <h3>Uptime-Kuma</h3>
                    <p>Self-hosted monitoring tool configuration.</p>
                </div>
                <div class="card">
                    <h3>HomeLab Core</h3>
                    <p>Building your self-hosted infrastructure.</p>
                </div>
            </div>
        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Theme Toggle Interaction Logic
document.addEventListener('DOMContentLoaded', () => {{
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;

    // Optional: Check local storage for saved preference
    // This is commented out to respect the initial python parameter, 
    // but in production, you would retrieve state here.
    /*
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {{
        body.classList.add('dark-mode');
        themeToggle.checked = true;
    }}
    */

    // Listen for toggle changes
    themeToggle.addEventListener('change', (e) => {{
        if (e.target.checked) {{
            body.classList.add('dark-mode');
            // localStorage.setItem('theme', 'dark');
        }} else {{
            body.classList.remove('dark-mode');
            // localStorage.setItem('theme', 'light');
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

#### 3c. Verification Checklist

- [x] Does the code produce valid HTML5 that passes basic validation?
- [x] Does `index.html` work when opened directly in a browser (`file://` protocol)?
- [x] Are all color values explicit hex or rgba?
- [x] Are all external resources loaded from CDN URLs?
- [x] Does the component respect the `width_px` and `height_px` parameters?
- [x] Does `color_scheme="dark"` produce a dark theme and `"light"` a light theme initially?
- [x] Does `accent_color` propagate to the toggle switch active state and card hover borders?
- [x] Are `title_text` and `body_text` injected correctly?
- [x] Does the JavaScript run without console errors and successfully toggle the `.dark-mode` class?
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect (smooth background fades, moving toggle pill with icons)?

### 4. Accessibility & Performance Notes

* **Accessibility**:
  - The toggle uses standard `<label>` and `<input type="checkbox">` syntax, ensuring semantic meaning and making it keyboard focusable via `Tab`. Pressing `Space` will toggle the switch for keyboard users.
  - Color choices maintain high contrast ratios in both light and dark modes (WCAG AA compliant).
  - *Enhancement for Production*: Add `aria-label="Toggle dark mode"` to the input and use `@media (prefers-reduced-motion: reduce)` to disable the `transition` declarations for users sensitive to motion.
* **Performance**:
  - The implementation is extremely lightweight. Relying on CSS Custom Properties means the browser recalculates styles efficiently without JavaScript DOM thrashing.
  - The toggle thumb animation uses `transform: translateX(...)` instead of animating `left` or `margin`, enabling GPU acceleration and avoiding layout recalculation (reflow) on every frame, maintaining a buttery smooth 60fps.