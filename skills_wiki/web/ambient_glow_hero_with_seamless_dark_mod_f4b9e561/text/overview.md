### 1. High-level Design Pattern Extraction

> **Skill Name**: Ambient Glow Hero with Seamless Dark Mode

* **Core Visual Mechanism**: The defining visual signature is a soft, diffuse background gradient achieved via a heavily blurred HTML element (`filter: blur(120px)`) placed behind the main content. This "Ambient Glow" is coupled with a custom JavaScript-triggered Dark Mode that smoothly transitions both the background/foreground colors and the gradient colors of the glow itself, creating a cohesive, deeply integrated theme switch.
* **Why Use This Skill (Rationale)**: The frosted/blurred ambient glow adds spatial depth and a modern "Web3/SaaS" aesthetic without distracting from the typography. The seamless dark mode transition respects user preference and provides immediate, satisfying interactive feedback.
* **Overall Applicability**: Ideal for landing pages, portfolio heroes, SaaS dashboards, and personal "link-in-bio" or self-hosted dashboard pages (as seen in the tutorial).
* **Value Addition**: Compared to a static background, the blurred gradient mesh creates a dynamic, layered feel. Integrating the theme switch directly into the ambient glow's colors makes the dark mode feel like a complete environment change rather than a simple color inversion.
* **Browser Compatibility**: Relies on `filter: blur()`, CSS Custom Properties (Variables), and flexbox. Fully supported in all modern browsers (Chrome 53+, Safari 9.1+, Firefox 35+, Edge 35+). 

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Ambient Glow**: A large, circular `div` rendered as an absolute background layer with a `linear-gradient` and a strong `blur` filter. 
  - **Color Logic**:
    - *Light Mode*: Background `#f8f9fa` (off-white), Text `#1a1a2e` (deep navy/black). The ambient glow uses a warm gradient (e.g., `#ffa9a9` to `#fecfef`).
    - *Dark Mode*: Background `#0d111c` (deep space blue/black), Text `#f0f0f0` (off-white). The ambient glow shifts to a cool gradient (e.g., `#4facfe` to `#00f2fe`).
  - **Typographic Hierarchy**: Driven by the `Poppins` typeface (sans-serif, geometric). Large, bold headings (`600` or `700` weight) paired with slightly muted, regular-weight subheadings.
  - **Custom Toggle Switch**: A stylized `<label>` containing a hidden checkbox, utilizing the `:checked + .slider` sibling selector trick to animate a toggle knob.

* **Step B: Layout & Compositional Style**
  - **Layout System**: The main wrapper uses CSS Flexbox (`display: flex`, `flex-direction: column`, `align-items: center`, `justify-content: center`) to perfectly center the content.
  - **Spatial Feel**: Extremely breathable. The ambient glow occupies about 40-50% of the viewport behind the text, fading into the solid background color.

* **Step C: Interactive Behavior & Animations**
  - **Theme Transition**: Applied to `body` and `.glow-shape`. `transition: background-color 0.4s ease, color 0.4s ease`. This ensures that when the Javascript toggles the `.dark-mode` class, the entire UI cross-fades rather than snapping instantly.
  - **Toggle Animation**: The slider knob translates along the X-axis using `transform: translateX(...)` with a smooth `0.3s cubic-bezier` transition.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Ambient Glow** | CSS `filter: blur()` | Native GPU-accelerated blur applied directly to a gradient `div`. Eliminates the need for massive images or Canvas APIs. |
| **Dark Mode State** | JS DOM manipulation | Toggling a `.dark` class on the `<body>` is the most robust way to trigger cascading CSS variable overrides. |
| **Smooth Color Transitions** | CSS `transition` | Applying transitions to `background-color` and `color` ensures the theme switch cross-fades elegantly. |
| **Custom Toggle** | Hidden Checkbox CSS | The `input[type="checkbox"]:checked ~ span` pattern avoids complex JS state management for the switch animation. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Why Not Your Own Services?",
    body_text: str = "Start Your Self-Hosting Journey with us!",
    color_scheme: str = "light",       # "dark" or "light"
    accent_color: str = "#b829e3",     # CSS hex color for accent/toggle
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Ambient Glow Hero and Dark Mode toggle.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Determine initial state based on requested color scheme
    is_dark = color_scheme == "dark"
    body_class = ' class="dark-mode"' if is_dark else ''
    checkbox_checked = ' checked' if is_dark else ''

    # === CSS ===
    # Notice the double curly braces {{ }} to escape Python f-string formatting for CSS blocks
    css = f"""/* Ambient Glow Hero Component */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    /* Light Theme Variables */
    --bg-color: #f8f9fa;
    --text-color: #1a1a2e;
    --text-muted: #5a5a6e;
    --accent: {accent_color};
    --glow-grad-start: #ff9a9e;
    --glow-grad-end: #fecfef;
    
    --container-width: {width_px}px;
    --container-height: {height_px}px;
}}

body.dark-mode {{
    /* Dark Theme Variables */
    --bg-color: #0d111c;
    --text-color: #f0f0f0;
    --text-muted: #a0a0b0;
    --glow-grad-start: #4facfe;
    --glow-grad-end: #00f2fe;
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
    /* Smooth theme transitions */
    transition: background-color 0.5s ease, color 0.5s ease;
}}

.app-container {{
    position: relative;
    width: 100%;
    max-width: var(--container-width);
    height: var(--container-height);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
}}

/* The Ambient Glow Shape */
.glow-shape {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 450px;
    height: 450px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--glow-grad-start), var(--glow-grad-end));
    filter: blur(120px);
    z-index: -1;
    opacity: 0.8;
    transition: background 0.5s ease;
}}

.hero-content {{
    z-index: 1;
}}

.hero-title {{
    font-size: 3.5rem;
    font-weight: 600;
    margin-bottom: 1rem;
    letter-spacing: -0.02em;
}}

.hero-subtitle {{
    font-size: 1.125rem;
    color: var(--text-muted);
    font-weight: 400;
    transition: color 0.5s ease;
}}

/* Top Navigation / Controls */
.top-nav {{
    position: absolute;
    top: 2rem;
    right: 2rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    z-index: 10;
}}

.nav-label {{
    font-size: 0.9rem;
    font-weight: 500;
}}

/* Custom Toggle Switch */
.switch {{
    position: relative;
    display: inline-block;
    width: 52px;
    height: 28px;
}}

.switch input {{
    opacity: 0;
    width: 0;
    height: 0;
}}

.slider {{
    position: absolute;
    cursor: pointer;
    top: 0; left: 0; right: 0; bottom: 0;
    background-color: #d1d5db;
    transition: .4s cubic-bezier(0.4, 0.0, 0.2, 1);
    border-radius: 34px;
}}

.slider:before {{
    position: absolute;
    content: "";
    height: 20px;
    width: 20px;
    left: 4px;
    bottom: 4px;
    background-color: white;
    transition: .4s cubic-bezier(0.4, 0.0, 0.2, 1);
    border-radius: 50%;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}}

/* Switch active states */
body.dark-mode .slider {{
    background-color: var(--accent);
}}

input:checked + .slider:before {{
    transform: translateX(24px);
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
<body{body_class}>
    
    <div class="app-container">
        
        <!-- Controls -->
        <nav class="top-nav">
            <span class="nav-label">Lights</span>
            <label class="switch" aria-label="Toggle Dark Mode">
                <input type="checkbox" id="theme-toggle"{checkbox_checked}>
                <span class="slider"></span>
            </label>
        </nav>

        <!-- Ambient Background Glow -->
        <div class="glow-shape"></div>

        <!-- Main Content -->
        <main class="hero-content">
            <h1 class="hero-title">{title_text}</h1>
            <p class="hero-subtitle">{body_text}</p>
        </main>
        
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Handle Dark Mode Toggle
document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');
    
    themeToggle.addEventListener('change', (e) => {
        if (e.target.checked) {
            document.body.classList.add('dark-mode');
        } else {
            document.body.classList.remove('dark-mode');
        }
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

* **Accessibility**: 
  * The toggle switch uses semantic HTML (`<label>` enclosing an `<input type="checkbox">`) ensuring standard keyboard focus and spacebar activation work out of the box. 
  * An `aria-label="Toggle Dark Mode"` is provided for screen readers to understand the purpose of the visually-hidden checkbox.
  * Contrast ratios in both the dark and light configurations meet WCAG AA standards (deep black on off-white, and bright white on deep space blue).
* **Performance**:
  * **Blur Impact**: CSS `filter: blur(120px)` requires significant computational power to render. By applying it to an absolutely positioned `div` with a solid shape and negative `z-index`, we avoid forcing the browser to recalculate blurs over complex text or interactive elements.
  * **Transition Optimization**: The slider knob animation relies exclusively on `transform: translateX()`, which triggers hardware-accelerated compositing without causing browser layout repaints, ensuring a 60fps interaction even on lower-end devices.