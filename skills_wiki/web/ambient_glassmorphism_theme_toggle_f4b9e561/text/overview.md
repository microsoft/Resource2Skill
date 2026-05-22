### 1. High-level Design Pattern Extraction

> **Skill Name**: Ambient Glassmorphism Theme Toggle

* **Core Visual Mechanism**: This pattern leverages CSS custom properties (variables) combined with massive, heavily blurred absolute elements (`filter: blur(100px)`) to create an "ambient lighting" effect behind the content. When the user flips the theme toggle, a tiny piece of JavaScript updates a data attribute on the root element. This triggers a cascade of CSS transitions, simultaneously shifting the solid background colors, the text colors, the glassmorphic card backgrounds, and the glowing ambient orbs, creating a cohesive, premium environmental shift.
* **Why Use This Skill (Rationale)**: Standard dark modes often feel stark or flat. By introducing ambient, brightly colored orbs in the background that blur seamlessly into the dark (or light) canvas, you create depth, warmth, and a modern "Web3/SaaS" aesthetic. The glassmorphism (translucent backgrounds with `backdrop-filter`) allows this ambient light to shine through the foreground elements, cementing the illusion of physical layers.
* **Overall Applicability**: Perfect for modern landing pages, SaaS dashboards, portfolio sites, and interactive web applications where a premium, highly polished aesthetic is desired. 
* **Value Addition**: Transforms a basic binary utility (light/dark mode) into an engaging visual experience. It softens the visual transition and creates a more immersive, branded environment by tying the brand's accent colors directly to the "lighting" of the page.
* **Browser Compatibility**: Broadly supported. Relies on `backdrop-filter` and `filter`, which are supported in all modern browsers (Safari, Chrome, Edge, Firefox). Minimal JavaScript is required.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Colors**: 
    - *Dark Theme*: Background (`#0d111c`), Text (`#f0f0f0`), Surface (`rgba(255, 255, 255, 0.05)`). Ambient Orb: User-defined accent color.
    - *Light Theme*: Background (`#f8f9fa`), Text (`#1a1a2e`), Surface (`rgba(255, 255, 255, 0.6)`). Ambient Orb: A softer, alternate tint (e.g., Pink/Lavender).
  - **Typography**: Clean, sans-serif (e.g., `Inter` or `Poppins`), utilizing high contrast for headings and muted opacity for subtitles.
  - **CSS Drivers**: `--css-variables` for theme state, `filter: blur()` for the ambient glow, `backdrop-filter: blur()` for the foreground cards, and `transition: all 0.4s ease-in-out` for the smooth metamorphosis.

* **Step B: Layout & Compositional Style**
  - **Layout System**: Flexbox for the header and overall centering; CSS Grid for the content cards to ensure even spacing and responsiveness.
  - **Layering (Z-index)**:
    - `-1`: Base background color.
    - `0`: Ambient blurred orbs.
    - `1`: Foreground content (Text, Cards, Nav) with glassmorphic properties.

* **Step C: Interactive Behavior & Animations**
  - **Theme Toggle**: A custom CSS checkbox styled as a sliding pill-shaped switch.
  - **Transitions**: The magic happens via CSS `transition`. Because the colors are mapped to CSS variables, altering the `data-theme` attribute causes the browser to automatically interpolate the colors of the background, text, borders, and glows simultaneously over `0.4s`.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Theme State Management** | CSS Variables + JS | CSS variables (`:root`) allow a single JS toggle to cascade color changes across the entire document instantly. |
| **Ambient Glow** | CSS `filter: blur()` | Applied to absolute positioned `div`s, it creates soft, performant gradient lighting without needing complex SVG or Canvas APIs. |
| **Glassmorphic Cards** | CSS `backdrop-filter` | Provides native real-time blurring of the ambient background beneath the cards, creating the illusion of frosted glass. |
| **Smooth Transition** | CSS `transition` | Applying a blanket transition to colors and backgrounds ensures the light-to-dark shift feels like a cinematic fade rather than a harsh cut. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Why not Your own Services?",
    body_text: str = "Start Your Self-Hosting Journey with us!",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#10b981",     # Default to a nice teal/green like the video's dark mode
    width_px: int = 1000,
    height_px: int = 700,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Ambient Glassmorphism Theme Toggle.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # We use a complementary color for the light mode ambient glow to mimic the video's pink -> green shift.
    light_ambient = "#f472b6" # Soft pink

    # === CSS ===
    css = f"""/* Ambient Glassmorphism Theme Toggle */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

/* Theme Variable Definitions */
:root[data-theme="light"] {{
    --bg-color: #f8f9fa;
    --text-color: #0f172a;
    --text-muted: #64748b;
    --surface-bg: rgba(255, 255, 255, 0.7);
    --surface-border: rgba(0, 0, 0, 0.05);
    --ambient-color: {light_ambient};
    --toggle-bg: #cbd5e1;
    --toggle-knob: #ffffff;
}}

:root[data-theme="dark"] {{
    --bg-color: #0d111c;
    --text-color: #f8fafc;
    --text-muted: #94a3b8;
    --surface-bg: rgba(255, 255, 255, 0.03);
    --surface-border: rgba(255, 255, 255, 0.08);
    --ambient-color: {accent_color};
    --toggle-bg: {accent_color};
    --toggle-knob: #ffffff;
}}

body {{
    font-family: 'Poppins', system-ui, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow-x: hidden;
    /* The core smooth transition for the whole theme */
    transition: background-color 0.5s ease, color 0.5s ease;
}}

.app-container {{
    width: 100%;
    max-width: {width_px}px;
    min-height: {height_px}px;
    position: relative;
    display: flex;
    flex-direction: column;
    padding: 40px;
    z-index: 1;
}}

/* Ambient Glowing Orb */
.ambient-glow {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 600px;
    height: 400px;
    background: var(--ambient-color);
    filter: blur(120px);
    border-radius: 50%;
    opacity: 0.35;
    z-index: -1;
    transition: background 0.6s ease, opacity 0.6s ease;
    pointer-events: none;
}}

/* Header & Toggle */
header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 80px;
}}

.logo-placeholder {{
    font-weight: 700;
    font-size: 1.25rem;
    letter-spacing: -0.5px;
}}

.toggle-wrapper {{
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 0.9rem;
    font-weight: 500;
}}

/* Custom Checkbox Switch */
.switch {{
    position: relative;
    display: inline-block;
    width: 48px;
    height: 26px;
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
    transition: .4s;
    border-radius: 34px;
}}

.slider:before {{
    position: absolute;
    content: "";
    height: 18px;
    width: 18px;
    left: 4px;
    bottom: 4px;
    background-color: var(--toggle-knob);
    transition: .4s cubic-bezier(0.4, 0.0, 0.2, 1);
    border-radius: 50%;
}}

input:checked + .slider:before {{
    transform: translateX(22px);
}}

/* Main Content */
.hero {{
    text-align: center;
    margin-bottom: 60px;
}}

.hero h1 {{
    font-size: 3.5rem;
    font-weight: 600;
    margin-bottom: 12px;
    letter-spacing: -1px;
}}

.hero p {{
    font-size: 1.1rem;
    color: var(--text-muted);
    transition: color 0.5s ease;
}}

/* Glassmorphic Grid */
.grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 24px;
    width: 100%;
}}

.card {{
    background: var(--surface-bg);
    border: 1px solid var(--surface-border);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-radius: 16px;
    padding: 32px;
    display: flex;
    flex-direction: column;
    gap: 12px;
    transition: background 0.5s ease, border-color 0.5s ease, transform 0.3s ease, box-shadow 0.3s ease;
    cursor: pointer;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(0,0,0,0.1);
}}

.card-tag {{
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--ambient-color);
    transition: color 0.5s ease;
}}

.card h3 {{
    font-size: 1.25rem;
    font-weight: 600;
}}

/* Responsive adjustments */
@media (max-width: 768px) {{
    .hero h1 {{ font-size: 2.5rem; }}
    .app-container {{ padding: 20px; }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en" data-theme="{color_scheme}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="ambient-glow"></div>
    
    <div class="app-container">
        <header>
            <div class="logo-placeholder">Echoes of Ping</div>
            <div class="toggle-wrapper">
                <span>Lights</span>
                <label class="switch">
                    <!-- The JS will ensure this matches the initial data-theme -->
                    <input type="checkbox" id="themeToggle">
                    <span class="slider"></span>
                </label>
            </div>
        </header>

        <main>
            <section class="hero">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
            </section>

            <section class="grid">
                <div class="card">
                    <span class="card-tag">Installation Guide</span>
                    <h3>Speedtest-Tracker</h3>
                </div>
                <div class="card">
                    <span class="card-tag">Setup</span>
                    <h3>Uptime-Kuma</h3>
                </div>
                <div class="card">
                    <span class="card-tag">Playlist</span>
                    <h3>HomeLab (Self-hosting)</h3>
                </div>
            </section>
        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""document.addEventListener('DOMContentLoaded', () => {{
    const themeToggle = document.getElementById('themeToggle');
    const htmlElement = document.documentElement;
    
    // Set initial toggle state based on the HTML data attribute
    // In this UI logic: "Lights" ON (checked) = Light Theme, OFF (unchecked) = Dark Theme
    const isLightMode = htmlElement.getAttribute('data-theme') === 'light';
    themeToggle.checked = isLightMode;

    themeToggle.addEventListener('change', (e) => {{
        if (e.target.checked) {{
            htmlElement.setAttribute('data-theme', 'light');
        }} else {{
            htmlElement.setAttribute('data-theme', 'dark');
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

* **Accessibility (a11y)**: 
  - The custom toggle switch wraps a native `<input type="checkbox">`, which maintains keyboard focusability and screen reader state (checked/unchecked). 
  - The contrasting text colors defined in the CSS variables (`#f8fafc` on `#0d111c` for dark, `#0f172a` on `#f8f9fa` for light) exceed the WCAG AA minimum 4.5:1 contrast ratio.
  - The `pointer-events: none;` property is applied to `.ambient-glow` to ensure the blurred background div does not intercept mouse clicks or touch events meant for the actual foreground interactive components.
* **Performance**: 
  - Using `filter: blur(120px)` on large elements can be somewhat demanding on lower-end mobile GPUs. However, by strictly applying `transition` only to `background-color` and `opacity` (and not animating layout properties like `width` or `transform` on the blurred element itself), we prevent layout thrashing and maintain 60FPS. 
  - `backdrop-filter` is hardware-accelerated in modern browsers, but utilizing the `-webkit-` prefix ensures fallback compatibility for older Safari environments.