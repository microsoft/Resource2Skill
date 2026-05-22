### 1. High-level Design Pattern Extraction

> **Skill Name**: Dynamic Gradient Theme Switcher with Pill Toggle

* **Core Visual Mechanism**: A sleek, pill-shaped toggle switch that triggers a smooth transition between a "Light Mode" and a "Dark Mode". The defining aesthetic signature is the use of rich, vibrant CSS background gradients that smoothly morph between states (e.g., from an airy white/pink gradient to a deep slate/teal gradient), paired with a custom CSS sliding-circle toggle element.
* **Why Use This Skill (Rationale)**: Implementing a dark mode toggle improves UX by empowering users to match their UI to their environment or visual preferences, reducing eye strain. The gradient backgrounds avoid the harshness of pure black or pure white, creating a more immersive, premium feel. 
* **Overall Applicability**: Highly applicable for SaaS landing pages, modern portfolios, blog hero sections, and personalized dashboards where a premium visual aesthetic and user comfort are priorities.
* **Value Addition**: Compared to a static layout, an interactive theme switch breathes life into a page. The fluid transition of typography colors, background gradients, and surface shadows adds a layer of kinetic polish that elevates the perceived quality of the application.
* **Browser Compatibility**: Fully supported in all modern browsers. Uses CSS variables (Custom Properties) and standard CSS transitions. Minimum requirements: Chrome 49+, Firefox 49+, Safari 31+, Edge 15+.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **HTML/CSS Constructs**: Uses standard HTML layout (`<header>`, `<main>`, `<div>`) paired with a visually hidden `<input type="checkbox">` overlaid with a custom styled `<label>` to act as the pill toggle.
  - **Color Logic**:
    - *Light Theme*: Background relies on a soft linear gradient (e.g., `#fdfbfb` to a soft pink/grey). Text is deep slate (`#1e293b`).
    - *Dark Theme*: Background switches to a deep, rich gradient (e.g., `#0f172a` to `#064e3b`). Text becomes an off-white (`#f8fafc`).
  - **Typographic Hierarchy**: Employs geometric sans-serif fonts (like `Poppins` or `Inter`). The hero title is bold and large (e.g., `800` weight, `3rem`), while the subtitle and UI labels are lighter (`400`/`500` weight, `1rem`).
  - **CSS Properties**: Driven by CSS Variables (`--bg-gradient`, `--text-color`). Smoothness is achieved via `transition: background 0.4s ease, color 0.4s ease`.

* **Step B: Layout & Compositional Style**
  - **Layout System**: Utilizes CSS Flexbox. The top header uses `justify-content: flex-end` or `space-between` to push the "Lights" toggle to the right. The main hero section uses `flex-direction: column` and `align-items: center` with ample whitespace (`gap`, `padding`) to center the primary content.
  - **Z-index Layering**: The sliding circle inside the pill toggle uses absolute positioning (`position: absolute`) within a relatively positioned container to slide above the track.

* **Step C: Interactive Behavior & Animations**
  - **The Toggle Slider**: The track (`.slider`) changes background color, and the inner circle translates horizontally (`transform: translateX(24px)`) when the hidden checkbox is `:checked`. Both properties use a `0.3s` transition.
  - **JavaScript Logic**: A vanilla JavaScript event listener on the checkbox detects `change` events and toggles a `data-theme="dark"` attribute on the `<html>` or `<body>` element.
  - **Morphing**: Because CSS variables are reassigned under the `[data-theme="dark"]` selector, any element using those variables automatically transitions to the new value if a CSS `transition` is applied.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Theme State Management** | JS + `data-theme` attribute | Standard, clean approach for dark mode. JS handles the click, CSS handles all visual changes. |
| **Dynamic Styling** | CSS Custom Properties (Variables) | Allows a single toggle to globally update background gradients, text colors, and UI elements seamlessly. |
| **Smooth Transitions** | CSS `transition` | Hardware-accelerated, performant way to smoothly morph colors and transform the pill slider. |
| **Pill Toggle Switch** | Checkbox Hack (CSS) | By hiding the actual checkbox and styling its associated `<label>`, we get semantic, accessible toggle behavior without extra JS state logic. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Why Not Your Own Services?",
    body_text: str = "Start Your Self-hosting Journey with us!",
    color_scheme: str = "light",       # initial state: "dark" or "light"
    accent_color: str = "#ec4899",     # Default light pink accent
    width_px: int = 1000,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Theme Switcher with Pill Toggle visual effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)
    
    # Checkbox initial state based on color_scheme
    is_checked = "checked" if color_scheme == "dark" else ""
    initial_theme = color_scheme

    # === CSS ===
    css = f"""/* Theme Switcher — generated component */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    /* Default Light Theme Variables */
    --bg-gradient: linear-gradient(135deg, #fdfbfb 0%, #f4eff4 100%);
    --text-main: #1e293b;
    --text-muted: #64748b;
    --accent: {accent_color};
    --toggle-track: #cbd5e1;
    --toggle-circle: #ffffff;
    --surface-bg: rgba(255, 255, 255, 0.7);
    --shadow: 0 10px 30px rgba(0,0,0,0.05);
}}

[data-theme="dark"] {{
    /* Dark Theme Variables */
    --bg-gradient: linear-gradient(135deg, #0f172a 0%, #064e3b 100%);
    --text-main: #f8fafc;
    --text-muted: #94a3b8;
    --accent: #10b981; /* Emerald green for dark mode accent */
    --toggle-track: #1e293b;
    --toggle-circle: #10b981;
    --surface-bg: rgba(15, 23, 42, 0.7);
    --shadow: 0 10px 30px rgba(0,0,0,0.3);
}}

body {{
    font-family: 'Poppins', sans-serif;
    background: var(--bg-gradient);
    color: var(--text-main);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    /* The transition creates the smooth morph between light/dark modes */
    transition: background 0.5s ease, color 0.5s ease;
}}

.app-container {{
    width: 100%;
    max-width: {width_px}px;
    height: {height_px}px;
    background: var(--surface-bg);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-radius: 24px;
    box-shadow: var(--shadow);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    position: relative;
    border: 1px solid rgba(255,255,255,0.1);
    transition: background 0.5s ease, box-shadow 0.5s ease;
}}

/* Header & Nav */
.header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2rem 3rem;
}}

.logo {{
    font-weight: 800;
    font-size: 1.25rem;
    letter-spacing: -0.5px;
    color: var(--text-main);
}}

/* Toggle Switch Container */
.theme-switch-wrapper {{
    display: flex;
    align-items: center;
    gap: 12px;
    font-weight: 600;
    font-size: 0.95rem;
    color: var(--text-main);
}}

/* The switch - the box around the slider */
.theme-switch {{
    position: relative;
    display: inline-block;
    width: 52px;
    height: 28px;
}}

/* Hide default HTML checkbox */
.theme-switch input {{
    opacity: 0;
    width: 0;
    height: 0;
}}

/* The slider track */
.slider {{
    position: absolute;
    cursor: pointer;
    top: 0; left: 0; right: 0; bottom: 0;
    background-color: var(--toggle-track);
    transition: .4s;
    border-radius: 34px;
}}

/* The slider circle */
.slider:before {{
    position: absolute;
    content: "";
    height: 20px;
    width: 20px;
    left: 4px;
    bottom: 4px;
    background-color: var(--toggle-circle);
    transition: transform .4s cubic-bezier(0.4, 0, 0.2, 1), background-color .4s;
    border-radius: 50%;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}}

/* Checked State */
input:checked + .slider {{
    /* Optional: keep track same or change it. We handle colors via CSS vars mostly */
}}

input:checked + .slider:before {{
    transform: translateX(24px);
}}

/* Hero Section */
.hero {{
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 2rem;
}}

.hero h1 {{
    font-size: clamp(2rem, 4vw, 3.5rem);
    font-weight: 800;
    line-height: 1.2;
    margin-bottom: 1rem;
    letter-spacing: -1px;
}}

.hero p {{
    font-size: 1.1rem;
    color: var(--text-muted);
    font-weight: 400;
    max-width: 600px;
    margin-bottom: 2.5rem;
}}

.btn-primary {{
    background: var(--accent);
    color: #fff;
    border: none;
    padding: 14px 32px;
    border-radius: 50px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.2s, opacity 0.2s;
    font-family: inherit;
}}

.btn-primary:hover {{
    transform: translateY(-2px);
    opacity: 0.9;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en" data-theme="{initial_theme}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Theme Switcher Component</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <div class="app-container">
        <!-- Header with Toggle -->
        <header class="header">
            <div class="logo">Echoes.</div>
            
            <div class="theme-switch-wrapper">
                <span id="theme-label">Lights</span>
                <label class="theme-switch" for="checkbox" aria-label="Toggle Dark Mode">
                    <input type="checkbox" id="checkbox" {is_checked} />
                    <div class="slider"></div>
                </label>
            </div>
        </header>

        <!-- Main Hero Content -->
        <main class="hero">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <button class="btn-primary">Get Started</button>
        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Select the theme toggle checkbox
const toggleSwitch = document.querySelector('#checkbox');

// Function to switch theme
function switchTheme(e) {
    if (e.target.checked) {
        document.documentElement.setAttribute('data-theme', 'dark');
    } else {
        document.documentElement.setAttribute('data-theme', 'light');
    }
}

// Add event listener to the toggle switch
toggleSwitch.addEventListener('change', switchTheme, false);
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
  - The hidden checkbox `<input type="checkbox">` is paired perfectly with a semantic `<label for="checkbox">`. This ensures that screen readers can focus on the checkbox, and clicking the label activates it.
  - Provided an `aria-label="Toggle Dark Mode"` to the label container for further context.
  - High contrast is maintained in both themes. The dark theme avoids pure black backgrounds, using dark slates and teals which reduce visual glare and improve readability of light text (`WCAG` compliant contrast ratio).
* **Performance**: 
  - The background morph and the slider animation rely on CSS `transition`. The slider specifically transitions `transform: translateX()`, which leverages hardware/GPU acceleration avoiding layout repaints.
  - Changing CSS Custom Properties directly on the `:root` via the `data-theme` attribute is highly performant. The browser dynamically recalculates styles for elements consuming those variables without requiring costly DOM iteration or inline style injection via JS.