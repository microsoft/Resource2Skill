### 1. High-level Design Pattern Extraction

> **Skill Name**: Ambient Glassmorphism with Theme Toggling

* **Core Visual Mechanism**: This design pattern combines two powerful CSS techniques: **ambient glowing orbs** (elements with heavy `filter: blur()`) and **frosted glass overlays** (`backdrop-filter: blur()` on semi-transparent containers). The visual signature is a softly glowing, out-of-focus color blob sitting in the background, which is then refracted and softened further by the glassmorphic cards sitting in the foreground. A seamless light/dark theme toggle flips the underlying color palette and the color of the ambient glow.
* **Why Use This Skill (Rationale)**: The heavy background blur combined with foreground frosted glass creates a rich sense of physical depth (z-space) on a flat screen. It feels modern, tactile, and premium. The theme toggle demonstrates user empowerment, allowing the user to dictate the visual comfort of the interface.
* **Overall Applicability**: Ideal for SaaS landing pages, portfolio sites, dashboard overviews, and pricing pages. It works exceptionally well in "hero" sections where you want to draw the user's eye to central value propositions without overwhelming them with sharp, high-contrast imagery.
* **Value Addition**: Transforms a standard grid of boxes into a unified, layered physical space. The ambient glow prevents the background from looking sterile, while the glassmorphism ensures text remains legible regardless of the colorful shapes underneath.
* **Browser Compatibility**: Requires modern browsers supporting `backdrop-filter` (Safari requires the `-webkit-` prefix). `filter: blur()` is widely supported. Minimal JS required just for the class toggling.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Background Base**: Solid base color that switches between light (`#f3f3f3`) and dark (`#001515`).
  - **Ambient Orb**: A large, absolute-positioned `<div>` (e.g., 450x450px) placed at the bottom or behind elements. It has a multi-stop linear gradient and a heavy blur (`filter: blur(120px)`). 
  - **Glass Cards**: Foreground elements with semi-transparent backgrounds (e.g., `rgba(255, 255, 255, 0.6)` in light mode, `rgba(17, 34, 34, 0.6)` in dark mode). They require `backdrop-filter: blur(20px)` to frost the orb behind them.
  - **Typography**: Clean, geometric sans-serif (e.g., *Poppins* or *Inter*). High contrast text colors for readability.

* **Step B: Layout & Compositional Style**
  - **Z-Index Layering**: 
    - Layer 0: Body background
    - Layer 1: Ambient Orb(s)
    - Layer 2: Main Layout Container (relative, z-index: 10)
  - **Grid/Flex**: Cards are organized using CSS Grid (`grid-template-columns: repeat(auto-fit, minmax(250px, 1fr))`) to ensure responsive reflow.
  - **Whitespace**: Generous padding inside cards (24-32px) and gap between grid items (24px) to emphasize the floaty, spacious aesthetic.

* **Step C: Interactive Behavior & Animations**
  - **Theme Toggle**: A pure HTML/CSS styled checkbox (pill shaped) that triggers a JavaScript event listener. The JS simply toggles a `.dark-mode` class on the `<body>`.
  - **Smooth Transitions**: The `<body>` and cards have `transition: background-color 0.3s ease, border-color 0.3s ease` to ensure the theme switch feels like a fluid fade rather than a harsh jump.
  - **Hover States**: Glass cards feature subtle hover transitions (`transform: translateY(-5px)`) and a border color change to the active accent color.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Ambient Glow** | CSS `filter: blur(120px)` | Creates a massive, performant glowing aura without needing canvas rendering or image assets. |
| **Frosted Glass** | CSS `backdrop-filter: blur(20px)` | Native CSS approach to refract elements beneath it. Includes `-webkit-` fallback. |
| **Theme Switching** | CSS Custom Properties + JS | JS applies a `.dark-mode` class; CSS variables automatically redefine the entire palette seamlessly. |
| **Layout** | CSS Grid & Flexbox | Auto-responsive grid structure ensures the cards arrange themselves logically without JS resizing. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Why Not Your Own Services?",
    body_text: str = "Start your self-hosting journey with us! Discover modern, beautiful architectures.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#fa39ad",     # Accent color for hovers/toggles
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Ambient Glassmorphism with Theme Toggle effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Determine initial mode class based on color_scheme
    body_class = "dark-mode" if color_scheme == "dark" else ""
    toggle_checked = "checked" if color_scheme == "dark" else ""

    # === CSS ===
    css = f"""/* Base & Reset */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    /* Default (Light Mode) Variables */
    --bg-base: #f3f3f3;
    --text-primary: #1a1a2e;
    --text-secondary: #4a4a68;
    --card-bg: rgba(255, 255, 255, 0.7);
    --card-border: rgba(255, 255, 255, 0.5);
    --card-border-hover: {accent_color};
    --orb-gradient: linear-gradient(to bottom, #fa39ad 30%, #fa6c4c 70%);
    --toggle-bg: #ccc;
    --accent: {accent_color};
}}

body.dark-mode {{
    /* Dark Mode Variables */
    --bg-base: #001515;
    --text-primary: #ffffff;
    --text-secondary: #a0b0b0;
    --card-bg: rgba(17, 34, 34, 0.6);
    --card-border: rgba(255, 255, 255, 0.1);
    --card-border-hover: #00ffaa; /* Specific dark mode accent */
    --orb-gradient: linear-gradient(to bottom, #00ffaa 40%, #0066ff 80%);
    --toggle-bg: #334444;
    --accent: #00ffaa;
}}

body {{
    font-family: 'Poppins', system-ui, sans-serif;
    background-color: var(--bg-base);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow-x: hidden;
    position: relative;
    transition: background-color 0.4s ease, color 0.4s ease;
}}

.app-wrapper {{
    width: 100%;
    max-width: {width_px}px;
    min-height: {height_px}px;
    position: relative;
    padding: 2rem;
    display: flex;
    flex-direction: column;
}}

/* === Ambient Glowing Orb === */
.ambient-orb {{
    position: absolute;
    bottom: -10%;
    left: 50%;
    transform: translateX(-50%);
    width: 500px;
    height: 500px;
    border-radius: 50%;
    background: var(--orb-gradient);
    filter: blur(140px);
    z-index: 0;
    opacity: 0.8;
    pointer-events: none;
    transition: background 0.5s ease;
}}

/* === Main Layout (Above Orb) === */
.content-layer {{
    position: relative;
    z-index: 10;
    display: flex;
    flex-direction: column;
    gap: 3rem;
    flex: 1;
}}

/* === Header & Toggle === */
header {{
    display: flex;
    justify-content: flex-end;
    align-items: center;
    padding: 1rem 0;
}}

.theme-toggle-wrapper {{
    display: flex;
    align-items: center;
    gap: 12px;
    font-weight: 500;
    font-size: 0.9rem;
}}

.switch {{
    position: relative;
    display: inline-block;
    width: 50px;
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
    background-color: var(--toggle-bg);
    transition: 0.4s;
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
    transition: 0.4s;
    border-radius: 50%;
}}

input:checked + .slider {{
    background-color: var(--accent);
}}

input:checked + .slider:before {{
    transform: translateX(22px);
}}

/* === Hero Section === */
.hero {{
    text-align: center;
    margin-top: 2rem;
}}

.hero h1 {{
    font-size: clamp(2rem, 4vw, 3.5rem);
    font-weight: 600;
    margin-bottom: 1rem;
    letter-spacing: -0.02em;
}}

.hero p {{
    font-size: 1.1rem;
    color: var(--text-secondary);
    max-width: 600px;
    margin: 0 auto;
}}

/* === Glassmorphic Cards Grid === */
.grid-container {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
    margin-top: 2rem;
}}

.glass-card {{
    background: var(--card-bg);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 2px solid var(--card-border);
    border-radius: 1.5rem;
    padding: 2rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
    transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    cursor: pointer;
}}

.glass-card:hover {{
    transform: translateY(-5px);
    border-color: var(--card-border-hover);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
}}

.glass-card h3 {{
    font-size: 1.25rem;
    font-weight: 600;
}}

.glass-card span.badge {{
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--text-secondary);
    font-weight: 500;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <!-- Google Fonts for typography styling -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body class="{body_class}">
    <div class="ambient-orb"></div>
    
    <div class="app-wrapper">
        <div class="content-layer">
            
            <header>
                <div class="theme-toggle-wrapper">
                    <span>Lights</span>
                    <label class="switch">
                        <input type="checkbox" id="themeToggle" {toggle_checked}>
                        <span class="slider"></span>
                    </label>
                </div>
            </header>

            <section class="hero">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
            </section>

            <section class="grid-container">
                <div class="glass-card">
                    <span class="badge">Installation Guide</span>
                    <h3>Speedtest-Tracker</h3>
                </div>
                <div class="glass-card">
                    <span class="badge">Setup</span>
                    <h3>Uptime-Kuma</h3>
                </div>
                <div class="glass-card">
                    <span class="badge">Playlist</span>
                    <h3>HomeLab (Self-hosting)</h3>
                </div>
                <div class="glass-card">
                    <span class="badge">Network</span>
                    <h3>Nginx Proxy Manager</h3>
                </div>
            </section>
            
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('themeToggle');

    // Toggle theme by adding/removing 'dark-mode' class on the body
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

* **Accessibility (a11y)**:
  * The toggle switch is built securely using an `<input type="checkbox">` hidden visually but retaining functional structure inside a `<label>`. This allows standard keyboard tab-targeting and spacebar toggling.
  * Contrast ratios are maintained deliberately by updating both the background colors and text colors (`--text-primary` and `--text-secondary`) inside the CSS variables during the theme switch.
* **Performance**:
  * **Heavy Blurs**: The `.ambient-orb` relies on a massive `filter: blur(140px)`. While this creates a gorgeous effect natively, exceptionally large CSS blurs can cause layout painting bottlenecks on low-end mobile devices. If deploying to highly restricted mobile environments, baking the glowing orb into a low-resolution `.png` or `.webp` image is a common optimization hack.
  * **Backdrop-Filter**: The cards utilize `backdrop-filter: blur(20px)`. This triggers the GPU compositing layers. It is lightweight for modern devices but requires the `-webkit-` prefix for maximum iOS/Safari compatibility (included in the code).
  * **Hardware Acceleration**: The hover states animate the `transform` property (`translateY`) rather than `top` or `margin`, ensuring smooth 60fps animations devoid of browser layout thrashing.