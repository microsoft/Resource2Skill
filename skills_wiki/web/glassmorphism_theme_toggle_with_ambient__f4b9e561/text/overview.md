### 1. High-level Design Pattern Extraction

> **Skill Name**: Glassmorphism Theme Toggle with Ambient Gradient Orbs

* **Core Visual Mechanism**: This component demonstrates a modern, fluid light/dark theme switch. The core aesthetic relies on **glassmorphism** (`backdrop-filter: blur()`) applied to UI panels, which overlay large, absolutely positioned background circles treated with an extreme `filter: blur(120px)`. When the hidden-checkbox toggle is triggered, JavaScript switches a class that crossfades a set of CSS variables, simultaneously recoloring the background, the blurred orbs, the glass cards, and the typography.
* **Why Use This Skill (Rationale)**: The combination of frosted glass and ambient, glowing orbs creates a sense of volumetric depth without 3D rendering. The smooth transition between a bright, airy light mode and a deep, moody dark mode gives users a highly tactile and satisfying interaction, enhancing perceived application quality.
* **Overall Applicability**: Ideal for SaaS dashboard hero sections, portfolio homepages, personalized settings panels, or any modern web application aiming for a premium, highly polished "macOS/iOS" aesthetic.
* **Value Addition**: Compared to standard background-color theme switching, this technique introduces depth, light refraction, and spatial layering. The ambient orbs prevent the background from feeling flat, while the glassmorphism ensures text readability regardless of the dynamic background underneath.
* **Browser Compatibility**: Requires modern browsers supporting `backdrop-filter` and CSS Variables (custom properties). `-webkit-` prefixes are included for broader Safari compatibility.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Ambient Orbs**: `div` elements border-radiused to 50% and given an extreme `filter: blur(120px)`.
  - **Color Logic (Light Mode)**: 
    - Background: Soft pink/purple tint (`#faf5ff`)
    - Orbs: Pastel pinks and purples (`#fbcfe8`, `#e9d5ff`, `#fecaca`)
    - Glass Card: Semi-transparent white (`rgba(255, 255, 255, 0.5)`) with a white border.
  - **Color Logic (Dark Mode)**:
    - Background: Deep dark green (`#064e3b`)
    - Orbs: Emeralds and bright teals (`#059669`, `#047857`, `#10b981`)
    - Glass Card: Semi-transparent dark green (`rgba(2, 44, 34, 0.4)`) with a faint white border.
  - **Typography**: Google Fonts 'Poppins', utilizing font weights 400, 500, 600, and 700 to establish hierarchy.

* **Step B: Layout & Compositional Style**
  - **Layout System**: Absolute positioning for the background orbs. Flexbox for the main vertical column, the horizontal toolbar (tabs and toggle), and CSS Grid for the 3-column feature cards.
  - **Z-Index Layering**: 
    - `z-index: 0` for background orbs
    - `z-index: 10` for the glassmorphic content layers (`.content-layer`)
  - **Spatial Feel**: Abundant padding (e.g., 60px 80px container padding, 24px card padding) and generous gaps create an airy, premium feel.

* **Step C: Interactive Behavior & Animations**
  - **Toggle Mechanism**: Pure CSS `input[type="checkbox"]:checked ~ label` architecture controls the physical slide of the toggle pill.
  - **Theme Switching**: JavaScript watches the `change` event on the checkbox and adds/removes a `.dark-mode` class on the main wrapper.
  - **Crossfading**: All colors, orb backgrounds, and card borders utilize a `transition: 0.5s ease` to ensure the transition between light and dark modes is a fluid morph rather than a harsh cut.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Theme State** | CSS Variables + JS class toggle | Centralizes color logic. JS handles the state cleanly, while CSS natively interpolates the crossfade transitions between variables. |
| **Toggle Switch UI** | CSS Checkbox Hack | Connects a `<label>` to a hidden `<input type="checkbox">`. Allows `:checked` state to animate the switch without writing JS for the UI micro-interaction. |
| **Glassmorphism** | CSS `backdrop-filter` | Provides native real-time blurring of the elements rendered strictly behind the target, avoiding expensive canvas operations. |
| **Ambient Orbs** | CSS `filter: blur()` | Simple absolutely positioned `div` elements scaled up and blurred heavily create organic gradients with very low performance overhead. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Why not Your own Services?",
    body_text: str = "Start Your Self-Hosting Journey with us!",
    color_scheme: str = "light",        # "dark" or "light"
    accent_color: str = "#d946ef",      # Base accent color (purple-pink)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Glassmorphism Theme Toggle effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Determine initial state attributes based on color_scheme
    wrapper_class = "app-wrapper" if color_scheme == "light" else "app-wrapper dark-mode"
    checked_attr = "checked" if color_scheme == "light" else ""

    # === CSS ===
    css = f"""/* Glassmorphism Theme Toggle — generated component */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --width: {width_px}px;
    --height: {height_px}px;
    --accent: {accent_color};
}}

body {{
    font-family: 'Poppins', system-ui, -apple-system, sans-serif;
    background-color: #0f172a; /* Outer dark frame */
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    overflow: hidden;
}}

.app-wrapper {{
    /* Light Mode Base Variables */
    --bg-color: #faf5ff;
    --text-color: #1e293b;
    --card-bg: rgba(255, 255, 255, 0.5);
    --card-border: rgba(255, 255, 255, 0.8);
    --switch-bg: var(--accent);
    --switch-indicator: #ffffff;
    --orb-1: #fbcfe8;
    --orb-2: #e9d5ff;
    --orb-3: #fecaca;

    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    background-color: var(--bg-color);
    color: var(--text-color);
    position: relative;
    overflow: hidden;
    border-radius: 16px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    transition: background-color 0.6s ease, color 0.6s ease;
}}

/* Dark Mode Overrides */
.app-wrapper.dark-mode {{
    --bg-color: #064e3b;
    --text-color: #f8fafc;
    --card-bg: rgba(2, 44, 34, 0.4);
    --card-border: rgba(255, 255, 255, 0.08);
    --switch-bg: rgba(255, 255, 255, 0.2);
    --switch-indicator: #ffffff;
    --orb-1: #059669;
    --orb-2: #047857;
    --orb-3: #10b981;
}}

/* Ambient Orbs */
.orb {{
    position: absolute;
    border-radius: 50%;
    filter: blur(120px);
    z-index: 0;
    transition: background-color 0.6s ease;
}}

.orb-1 {{
    top: -15%; left: -10%;
    width: 600px; height: 600px;
    background-color: var(--orb-1);
}}

.orb-2 {{
    bottom: -20%; right: -10%;
    width: 700px; height: 700px;
    background-color: var(--orb-2);
}}

.orb-3 {{
    top: 30%; left: 50%;
    transform: translateX(-50%);
    width: 500px; height: 500px;
    background-color: var(--orb-3);
}}

/* Content Layout */
.content-layer {{
    position: relative;
    z-index: 10;
    height: 100%;
    display: flex;
    flex-direction: column;
    padding: 60px 80px;
}}

.header {{
    text-align: center;
    margin-bottom: 40px;
}}

.header h1 {{
    font-size: 3.2rem;
    font-weight: 600;
    margin-bottom: 12px;
    letter-spacing: -0.03em;
}}

.header p {{
    font-size: 1.1rem;
    font-weight: 500;
    opacity: 0.8;
}}

/* Glassmorphism Card Utility */
.card {{
    background: var(--card-bg);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border: 1px solid var(--card-border);
    transition: background-color 0.6s ease, border-color 0.6s ease, box-shadow 0.6s ease;
}}

/* Toolbar (Tabs & Toggle) */
.toolbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 40px;
    margin-bottom: auto;
    border-radius: 100px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
}}

.tabs {{
    display: flex;
    gap: 32px;
}}

.tab {{
    font-weight: 500;
    font-size: 1rem;
    cursor: pointer;
    opacity: 0.5;
    transition: opacity 0.3s ease;
    padding: 8px 0;
}}

.tab:hover, .tab.active {{
    opacity: 1;
}}

.tab.active {{
    position: relative;
}}

.tab.active::after {{
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 3px;
    background-color: var(--text-color);
    border-radius: 3px;
    transition: background-color 0.6s ease;
}}

/* Toggle Switch UI */
.toggle-container {{
    display: flex;
    align-items: center;
    gap: 16px;
}}

.toggle-text {{
    font-weight: 600;
    font-size: 0.95rem;
}}

.toggle-input {{
    display: none;
}}

.toggle-label-switch {{
    position: relative;
    display: inline-block;
    width: 52px;
    height: 28px;
    cursor: pointer;
    border-radius: 30px;
    background-color: var(--switch-bg);
    transition: background-color 0.4s ease;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
}}

.toggle-indicator {{
    position: absolute;
    top: 3px;
    left: 3px;
    width: 22px;
    height: 22px;
    background-color: var(--switch-indicator);
    border-radius: 50%;
    transition: transform 0.4s cubic-bezier(0.4, 0.0, 0.2, 1), background-color 0.4s ease;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}}

.toggle-input:checked + .toggle-label-switch .toggle-indicator {{
    transform: translateX(24px);
}}

/* Grid Cards */
.card-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
}}

.grid-card {{
    padding: 28px 24px;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.03);
    cursor: pointer;
}}

.grid-card:hover {{
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.08);
    transform: translateY(-2px);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}}

.grid-card h3 {{
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    opacity: 0.6;
    margin-bottom: 8px;
}}

.grid-card p {{
    font-size: 1.3rem;
    font-weight: 600;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Theme Toggle Component</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <div class="{wrapper_class}">
        <!-- Ambient Glowing Orbs -->
        <div class="orb orb-1"></div>
        <div class="orb orb-2"></div>
        <div class="orb orb-3"></div>

        <!-- Glassmorphism Content Layer -->
        <div class="content-layer">
            
            <div class="header">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
            </div>

            <div class="toolbar card">
                <div class="tabs">
                    <span class="tab">Posts</span>
                    <span class="tab">Blogs</span>
                    <span class="tab active">Videos</span>
                </div>
                
                <div class="toggle-container">
                    <span class="toggle-text">Lights</span>
                    <input type="checkbox" id="themeToggle" class="toggle-input" {checked_attr}>
                    <label for="themeToggle" class="toggle-label-switch">
                        <span class="toggle-indicator"></span>
                    </label>
                </div>
            </div>

            <div class="card-grid">
                <div class="grid-card card">
                    <h3>Installation Guide</h3>
                    <p>Speedtest-Tracker</p>
                </div>
                <div class="grid-card card">
                    <h3>Setup</h3>
                    <p>Uptime-Kuma</p>
                </div>
                <div class="grid-card card">
                    <h3>Playlist</h3>
                    <p>HomeLab (Self-hosting)</p>
                </div>
            </div>

        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Theme Toggle Logic
document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('themeToggle');
    const appWrapper = document.querySelector('.app-wrapper');
    
    // Listen for toggle changes
    themeToggle.addEventListener('change', (e) => {
        if (!e.target.checked) {
            // Unchecked == Lights Off == Dark Mode
            appWrapper.classList.add('dark-mode');
        } else {
            // Checked == Lights On == Light Mode
            appWrapper.classList.remove('dark-mode');
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
  - The toggle implementation uses a native `<input type="checkbox">` structurally, meaning keyboard users can technically interact with it if they tab to it. However, because `display: none;` removes it from the tab order, a more strictly accessible implementation would visually hide the input using `.sr-only` utility classes (clipping) rather than `display: none;`, allowing screen readers and keyboard focus to remain intact.
  - Color contrast dynamically adapts depending on the theme applied, maintaining high legibility over the blurred gradients.
* **Performance**: 
  - `backdrop-filter` triggers hardware-accelerated rendering but can impact FPS on lower-end devices if applied to many overlapping large elements. Here, it is restricted safely to structural cards.
  - The extreme `filter: blur()` applied to the background orbs is very performant in modern browsers because it calculates once and doesn't constantly repaint unless the orb transforms dynamically. Transitions are limited to `background-color` and `color` variables, triggering inexpensive paints rather than expensive reflows.