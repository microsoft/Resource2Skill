### 1. High-level Design Pattern Extraction

> **Skill Name**: Glassmorphism Hero Dashboard with Ambient Orb & Theme Toggle

* **Core Visual Mechanism**: The defining visual signature is a translucent, frosted-glass interface layered over a stark, solid background illuminated by a heavily blurred, vibrant gradient shape (an "ambient orb"). This technique leverages CSS `backdrop-filter: blur()` combined with a semi-transparent `rgba` background for the glass pane, and a secondary element behind it using `filter: blur(120px)` to create a diffused lighting effect. 
* **Why Use This Skill (Rationale)**: Glassmorphism creates a sense of depth and hierarchy without relying on harsh drop shadows. The ambient glowing orb provides visual interest and color dynamic, drawing the eye, while the frosted glass ensures that text remains legible. Adding a seamless dark/light mode toggle enhances user agency and shows off the ambient lighting effect across different contrast environments.
* **Overall Applicability**: Perfect for modern SaaS landing pages, personal portfolio hero sections, dashboard interfaces, and interactive application framing where a "premium, high-tech" aesthetic is desired.
* **Value Addition**: Transforms a flat, static layout into a dynamic, spatial environment. The ambient backlight makes the UI feel responsive and alive, establishing a polished, "app-like" feel rather than a traditional webpage.
* **Browser Compatibility**: `backdrop-filter` is well-supported in modern browsers (Edge, Chrome, Firefox, Safari). However, it requires hardware acceleration to be performant. Older browsers will fall back to the semi-transparent background color without the blur. 

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Glass Panel**: Created using `background: rgba(255, 255, 255, 0.5)` (or a dark equivalent) with `backdrop-filter: blur(20px)` and a subtle 1px semi-transparent border (`rgba(255,255,255,0.2)`) to simulate the glass edge.
  - **Ambient Orb**: A `div` strictly positioned behind the glass panel, completely rounded (`border-radius: 50%`), filled with a bright `linear-gradient`, and radically softened using `filter: blur(120px)`.
  - **Color Logic**:
    - *Light Theme*: Background `#f3f3f3`, Orb `linear-gradient(to bottom, #ffa9ad, #fa5c4c)`, Text `#111827`, Glass `rgba(255, 255, 255, 0.6)`.
    - *Dark Theme*: Background `#0d111c`, Orb `linear-gradient(to bottom, #00ffaa, #00b6ff)`, Text `#f8fafc`, Glass `rgba(15, 23, 42, 0.6)`.
  - **Typography**: Clean geometric sans-serif (like *Poppins* or *Inter*). Heavily weighted titles (600/700) contrasting with light, readable body copy (400).

* **Step B: Layout & Compositional Style**
  - **Z-Index Layering**: Absolute positioning is crucial here. The container must maintain `z-index: 10`, while the ambient orb sits at `z-index: -1` and `position: absolute`.
  - **Flexbox Structure**: The internal structure utilizes Flexbox for the header (space-between), navigation tabs (gap-based row flex), and content alignment.
  - **Spatial Feel**: Extremely generous padding (e.g., `32px` to `48px` inside the glass container) ensures the UI feels uncluttered.

* **Step C: Interactive Behavior & Animations**
  - **Theme Toggle**: A hidden `<input type="checkbox">` wrapped in a `<label>` creates a custom toggle switch. A sliding thumb shifts position using `transform: translateX()`.
  - **Transitions**: Smooth state changes across the application are handled via a global `transition: background-color 0.3s ease, color 0.3s ease`.
  - **JavaScript**: A simple script listens for the `change` event on the toggle switch, toggling a specific `.dark-theme` or `.light-theme` class on the document body, triggering CSS variable swaps.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Frosted glass UI | CSS `backdrop-filter` | Native CSS feature; achieves the glass effect performantly without JS or canvas tricks. |
| Ambient glowing orb | CSS `filter: blur()` | Simple absolute div with a massive blur simulates a glowing volumetric light efficiently. |
| Custom Toggle Switch | CSS `:checked` + `transform` | Pure CSS approach for form controls. Avoids heavy JS animation libraries for simple states. |
| Theme switching | CSS Variables + JS Toggle | Swapping a class on the `<body>` that redefines CSS `--variables` is the most scalable way to implement robust theming. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Why not Your own Services?",
    body_text: str = "Start Your Self-Hosting Journey with us!",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#ec4899",     # Pink accent default
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Glassmorphism Hero with Theme Toggle effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Determine default and alternate states based on input
    is_dark = color_scheme.lower() == "dark"
    
    # CSS Variable logic: We set base variables based on user selection, 
    # and alt variables inside the .theme-toggled class
    css = f"""/* Glassmorphism Dashboard & Theme Toggle */
:root {{
    --width-px: {width_px}px;
    --height-px: {height_px}px;
    --accent: {accent_color};
    --transition-speed: 0.4s;
}}

/* Base Theme Variables */
body {{
    /* Theme: {color_scheme.upper()} */
    --bg-color: { "#0f172a" if is_dark else "#f3f3f3" };
    --text-primary: { "#f8fafc" if is_dark else "#111827" };
    --text-secondary: { "#94a3b8" if is_dark else "#6b7280" };
    --glass-bg: { "rgba(15, 23, 42, 0.65)" if is_dark else "rgba(255, 255, 255, 0.65)" };
    --glass-border: { "rgba(255, 255, 255, 0.08)" if is_dark else "rgba(255, 255, 255, 0.4)" };
    --glass-shadow: { "rgba(0, 0, 0, 0.3)" if is_dark else "rgba(0, 0, 0, 0.05)" };
    --orb-gradient: { "linear-gradient(135deg, #00ffaa 0%, #00b6ff 100%)" if is_dark else "linear-gradient(135deg, #ffa9ad 0%, #fa5c4c 100%)" };
    --card-bg: { "rgba(30, 41, 59, 0.5)" if is_dark else "rgba(255, 255, 255, 0.8)" };
    --card-hover: { "rgba(51, 65, 85, 0.8)" if is_dark else "rgba(255, 255, 255, 1)" };
}}

/* Alternate Theme Variables (Toggled) */
body.theme-toggled {{
    /* Theme: { "LIGHT" if is_dark else "DARK" } */
    --bg-color: { "#f3f3f3" if is_dark else "#0f172a" };
    --text-primary: { "#111827" if is_dark else "#f8fafc" };
    --text-secondary: { "#6b7280" if is_dark else "#94a3b8" };
    --glass-bg: { "rgba(255, 255, 255, 0.65)" if is_dark else "rgba(15, 23, 42, 0.65)" };
    --glass-border: { "rgba(255, 255, 255, 0.4)" if is_dark else "rgba(255, 255, 255, 0.08)" };
    --glass-shadow: { "rgba(0, 0, 0, 0.05)" if is_dark else "rgba(0, 0, 0, 0.3)" };
    --orb-gradient: { "linear-gradient(135deg, #ffa9ad 0%, #fa5c4c 100%)" if is_dark else "linear-gradient(135deg, #00ffaa 0%, #00b6ff 100%)" };
    --card-bg: { "rgba(255, 255, 255, 0.8)" if is_dark else "rgba(30, 41, 59, 0.5)" };
    --card-hover: { "rgba(255, 255, 255, 1)" if is_dark else "rgba(51, 65, 85, 0.8)" };
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Poppins', system-ui, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow-x: hidden;
    transition: background-color var(--transition-speed) ease, color var(--transition-speed) ease;
}}

/* Main wrapper to enforce dimension constraints */
.layout-wrapper {{
    width: 100%;
    max-width: var(--width-px);
    min-height: var(--height-px);
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 2rem;
}}

/* === Ambient Orb === */
.ambient-orb {{
    position: absolute;
    width: 500px;
    height: 500px;
    background: var(--orb-gradient);
    border-radius: 50%;
    filter: blur(120px);
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 0;
    opacity: 0.8;
    transition: background var(--transition-speed) ease;
    pointer-events: none;
}}

/* === Glassmorphism Container === */
.glass-panel {{
    position: relative;
    z-index: 10;
    background: var(--glass-bg);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border: 1px solid var(--glass-border);
    border-radius: 24px;
    box-shadow: 0 25px 50px -12px var(--glass-shadow);
    padding: 2.5rem;
    display: flex;
    flex-direction: column;
    gap: 3rem;
    transition: background var(--transition-speed) ease, border-color var(--transition-speed) ease, box-shadow var(--transition-speed) ease;
}}

/* Header & Nav */
.panel-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.logo-wrap {{
    display: flex;
    align-items: center;
    gap: 12px;
    font-weight: 600;
    font-size: 1.1rem;
}}

.logo-dot {{
    width: 12px;
    height: 12px;
    background: var(--accent);
    border-radius: 50%;
    box-shadow: 0 0 10px var(--accent);
}}

/* Main Hero Content */
.hero-content {{
    text-align: center;
    padding: 3rem 0;
}}

.hero-title {{
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 1rem;
    letter-spacing: -0.02em;
}}

.hero-subtitle {{
    font-size: 1.125rem;
    color: var(--text-secondary);
    font-weight: 400;
}}

/* Bottom Navigation / Tabs */
.content-tabs {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--glass-border);
    padding-bottom: 1.5rem;
    margin-bottom: 1rem;
}}

.tab-group {{
    display: flex;
    gap: 2rem;
}}

.tab-link {{
    font-weight: 500;
    color: var(--text-secondary);
    cursor: pointer;
    transition: color 0.2s;
    position: relative;
}}

.tab-link:hover, .tab-link.active {{
    color: var(--text-primary);
}}

.tab-link.active::after {{
    content: '';
    position: absolute;
    bottom: -1.65rem;
    left: 0;
    width: 100%;
    height: 3px;
    background: var(--accent);
    border-radius: 3px 3px 0 0;
}}

/* Grid Cards */
.cards-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
}}

.service-card {{
    background: var(--card-bg);
    border: 1px solid var(--glass-border);
    border-radius: 16px;
    padding: 1.5rem;
    transition: all 0.3s ease;
    cursor: pointer;
}}

.service-card:hover {{
    background: var(--card-hover);
    transform: translateY(-4px);
    box-shadow: 0 10px 25px -5px var(--glass-shadow);
}}

.service-label {{
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-secondary);
    margin-bottom: 0.5rem;
}}

.service-name {{
    font-weight: 600;
    font-size: 1.125rem;
}}

/* === Theme Toggle Switch === */
.theme-toggle-wrapper {{
    display: flex;
    align-items: center;
    gap: 12px;
}}

.toggle-label {{
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--text-secondary);
}}

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
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: var(--card-bg);
    border: 1px solid var(--glass-border);
    transition: var(--transition-speed);
    border-radius: 34px;
}}

.slider:before {{
    position: absolute;
    content: "";
    height: 20px;
    width: 20px;
    left: 3px;
    bottom: 3px;
    background-color: var(--text-primary);
    transition: var(--transition-speed);
    border-radius: 50%;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}}

input:checked + .slider {{
    background-color: var(--accent);
    border-color: var(--accent);
}}

input:checked + .slider:before {{
    transform: translateX(24px);
    background-color: #fff;
}}

/* Responsive fallbacks */
@media (max-width: 900px) {{
    .cards-grid {{
        grid-template-columns: 1fr;
    }}
    .tab-group {{
        gap: 1rem;
    }}
    .hero-title {{
        font-size: 2.25rem;
    }}
}}
"""

    # Determine switch checked state based on initial theme config
    # We will let "checked" mean "toggled state". So initially it's unchecked.
    # The label reflects the "opposite" or just a generic "Lights" label as in the video.
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <div class="layout-wrapper">
        <!-- Diffused Ambient Lighting Orb -->
        <div class="ambient-orb"></div>

        <!-- Glassmorphic Main Interface -->
        <div class="glass-panel">
            
            <!-- Header -->
            <header class="panel-header">
                <div class="logo-wrap">
                    <div class="logo-dot"></div>
                    <span>Echoes of Ping / Home</span>
                </div>
                
                <div class="theme-toggle-wrapper">
                    <span class="toggle-label">Lights</span>
                    <label class="switch" aria-label="Toggle Theme">
                        <input type="checkbox" id="theme-switch">
                        <span class="slider"></span>
                    </label>
                </div>
            </header>

            <!-- Hero Section -->
            <main class="hero-content">
                <h1 class="hero-title">{title_text}</h1>
                <p class="hero-subtitle">{body_text}</p>
            </main>

            <!-- Lower Section: Tabs & Grid -->
            <div class="bottom-section">
                <div class="content-tabs">
                    <div class="tab-group">
                        <span class="tab-link">Posts</span>
                        <span class="tab-link">Blogs</span>
                        <span class="tab-link active">Videos</span>
                    </div>
                </div>

                <div class="cards-grid">
                    <div class="service-card">
                        <div class="service-label">Installation Guide</div>
                        <div class="service-name">Speedtest-Tracker</div>
                    </div>
                    <div class="service-card">
                        <div class="service-label">Setup</div>
                        <div class="service-name">Uptime-Kuma</div>
                    </div>
                    <div class="service-card">
                        <div class="service-label">Playlist</div>
                        <div class="service-name">HomeLab(Self-hosting)</div>
                    </div>
                </div>
            </div>

        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>
"""

    js = """// Glassmorphism Theme Toggle Logic
document.addEventListener('DOMContentLoaded', () => {
    const themeSwitch = document.getElementById('theme-switch');
    
    if (themeSwitch) {
        themeSwitch.addEventListener('change', (e) => {
            // Toggling this class shifts all CSS variables to their alternate state
            if (e.target.checked) {
                document.body.classList.add('theme-toggled');
            } else {
                document.body.classList.remove('theme-toggled');
            }
        });
    }
});
"""

    # Write files to the specified output directory
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
  - The toggle `<label>` implements an `aria-label="Toggle Theme"` to ensure screen readers understand the purpose of the generic slider shapes.
  - Using a hidden `<input type="checkbox">` maintains native focus states and keyboard usability (`Tab` to focus, `Space` to toggle) which is completely lost if building a switch out of purely `div` tags and click listeners.
  - The font uses Google's geometric *Poppins* with high-contrast text mapped securely across themes via CSS variables.

* **Performance**:
  - The ambient orb relies on `filter: blur(120px)` and the panel uses `backdrop-filter: blur(24px)`. These are **computationally expensive** operations for the browser's compositor. Ensure the orb does not animate positionally on every frame (like following a mouse) unless heavily throttled, as massive blurs redrawing constantly cause significant scroll/render jank on low-end devices.
  - The toggle switch animation uses `transform: translateX()`, which triggers hardware-accelerated composition rather than heavy layout reflows (avoiding `left`/`margin` transitions). Default `will-change: transform` isn't strictly necessary here due to the small footprint, but the GPU acceleration guarantees a 60fps sliding effect.