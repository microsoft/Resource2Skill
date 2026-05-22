### 1. High-level Design Pattern Extraction

> **Skill Name**: Dynamic CSS Variable Theming (Glassmorphic Dark Mode)

* **Core Visual Mechanism**: A smooth, script-triggered transition between entirely distinct visual themes (Light to Dark). It uses CSS Custom Properties (variables) updated via a state class (`.dark-mode`) on the `body`. The visual signature is characterized by changing not just solid backgrounds, but also shifting gradients, swapping glassmorphism for solid flat surfaces, and inverting text contrast, all orchestrated simultaneously.
* **Why Use This Skill (Rationale)**: Dark mode is an accessibility and user-preference standard. Using CSS variables tied to a top-level DOM class allows for instantaneous, highly performant theme switching across the entire application without needing to swap stylesheets or re-render components in JavaScript.
* **Overall Applicability**: SaaS dashboards, landing pages, documentation sites, and portfolios. It is especially effective when the design uses vivid accent gradients that need to shift their mood (e.g., from warm pinks to cold cyans) alongside the background.
* **Value Addition**: Transforms a static interface into a personalized, reactive environment. The use of transitions on background and text color properties creates a fluid, polished feel that avoids jarring flashes of light/dark.
* **Browser Compatibility**: Fully supported in all modern browsers. CSS Custom Properties and `backdrop-filter` (for the glassmorphism) are universally supported in evergreen versions of Chrome, Safari, Edge, and Firefox.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Light Mode Palette**: Background `#f8f9fa` (off-white), Container `#ffffff`, Text `#1a1a2e` (near black), Background Gradient Glow `linear-gradient(to bottom, #fa39ad 40%, #fa6c4c 60%)`.
  - **Dark Mode Palette**: Background `#000a0a` (deepest green/black), Container `#001515` (dark green), Text `#d0f9f0` (light cyan), Background Gradient Glow `linear-gradient(to bottom, #00ffaa 40%, #0066ff 60%)`.
  - **Glassmorphism**: In light mode, the cards use `rgba(255, 255, 255, 0.7)` with `backdrop-filter: blur(20px)` to allow the pink gradient to bleed through. In dark mode, they switch to a solid, slightly elevated `#001515` with a subtle cyan shadow.
  - **Typography**: Clean, geometric sans-serif (Poppins/Inter) with high contrast tracking for headers.

* **Step B: Layout & Compositional Style**
  - **Hierarchy**: Centralized hero text with a bottom-heavy grid for cards. 
  - **Layout Mechanism**: CSS Flexbox is used for the top navigation and the control bar (Tabs + Toggle). CSS Grid is used to align the bottom cards evenly.
  - **Layering (Z-Index)**: A glowing, heavily blurred (`filter: blur(120px)`) circle sits at `z-index: 0`, while the main app container sits at `z-index: 1`, allowing the blur to act as an ambient light source behind the translucent cards.

* **Step C: Interactive Behavior & Animations**
  - **Theme Toggle**: A hidden native checkbox overlaying a styled `label`. CSS adjacent sibling selectors (`input:checked + .slider`) handle the visual translation of the toggle pill (`transform: translateX(100%)`).
  - **The Transition**: The `body` and `.card` elements have `transition: background-color 0.3s ease, color 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;`. When JS adds the `.dark-mode` class to the body, the CSS variables change, and the browser interpolates the colors smoothly over 300ms.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Theme State Management** | JavaScript DOM class toggle | A single click listener on a checkbox that toggles a class on the `body` is the most robust, standard way to handle top-level theming. |
| **Color Swapping** | CSS Custom Properties (Variables) | Allows defining a color system once and redefining it inside a `.dark-mode` scope, automatically updating all child elements. |
| **Smooth Transition** | CSS `transition` | Native CSS interpolation of `background-color` and `color` provides GPU-accelerated, jank-free 60fps animations. |
| **Toggle Switch UI** | CSS Checkbox Hack | Hiding the actual input and styling the adjacent `label` allows for a fully custom, animated switch without heavy JS logic. |
| **Ambient Background Glow** | CSS `filter: blur()` | A simple `div` with a gradient and high blur radius perfectly simulates an ambient light source behind the UI. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Why not Your own Services?",
    body_text: str = "Start Your Self-hosting Journey with us!",
    color_scheme: str = "light",        # "dark" or "light" defaults
    accent_color: str = "#00ffaa",      # Applied to dark mode accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the CSS Variable Dark Mode toggle effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)
    
    # Pre-calculate boolean for template injection
    is_dark = "checked" if color_scheme == "dark" else ""
    initial_class = "dark-mode" if color_scheme == "dark" else ""

    # === CSS ===
    css = f"""/* Dynamic CSS Variable Theming */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    /* LIGHT MODE (Default) */
    --bg-page: #e5e7eb;
    --bg-app: #ffffff;
    --text-primary: #111827;
    --text-secondary: #6b7280;
    
    --glow-gradient: linear-gradient(to bottom, #fa39ad 40%, #fa6c4c 60%);
    --card-bg: rgba(255, 255, 255, 0.6);
    --card-border: transparent;
    --card-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    
    --toggle-bg: #d1d5db;
    --toggle-indicator: #ffffff;
    
    --nav-active-bg: #f3f4f6;
    
    --transition-speed: 0.3s;
}}

body.dark-mode {{
    /* DARK MODE OVERRIDES */
    --bg-page: #000000;
    --bg-app: #011111;
    --text-primary: #d0f9f0;
    --text-secondary: #88cfd3;
    
    --glow-gradient: linear-gradient(to bottom, {accent_color} 40%, #0066ff 60%);
    --card-bg: #001a1a;
    --card-border: #003333;
    --card-shadow: 0 10px 25px rgba(0, 255, 170, 0.1);
    
    --toggle-bg: {accent_color};
    --toggle-indicator: #1a202c;
    
    --nav-active-bg: #002222;
}}

body {{
    font-family: 'Poppins', sans-serif;
    background-color: var(--bg-page);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    /* Transition applied to body handles page background */
    transition: background-color var(--transition-speed) ease;
}}

/* App Window Wrapper */
.app-window {{
    width: {width_px}px;
    height: {height_px}px;
    max-width: 100%;
    background-color: var(--bg-app);
    border-radius: 16px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    /* Transition for app background */
    transition: background-color var(--transition-speed) ease;
}}

/* Ambient Glow Effect */
.ambient-glow {{
    position: absolute;
    width: 500px;
    height: 500px;
    background: var(--glow-gradient);
    filter: blur(120px);
    border-radius: 50%;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -20%);
    z-index: 0;
    opacity: 0.5;
    /* Transition for gradient shifts */
    transition: background var(--transition-speed) ease;
}}

/* Header Fake Controls */
.header {{
    padding: 24px 32px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 10;
}}

.mac-dots {{
    display: flex;
    gap: 8px;
}}
.dot {{
    width: 12px; height: 12px; border-radius: 50%;
}}
.dot.red {{ background: #ff5f56; }}
.dot.yellow {{ background: #ffbd2e; }}
.dot.green {{ background: #27c93f; }}

.join-btn {{
    background: transparent;
    border: none;
    color: var(--text-primary);
    font-family: inherit;
    font-weight: 500;
    cursor: pointer;
    transition: color var(--transition-speed) ease;
}}

/* Main Content Area */
.main-content {{
    flex: 1;
    z-index: 10;
    display: flex;
    flex-direction: column;
    padding: 0 64px 48px;
}}

.hero {{
    text-align: center;
    margin-top: 60px;
    margin-bottom: 80px;
}}

.title {{
    color: var(--text-primary);
    font-size: 3rem;
    font-weight: 600;
    letter-spacing: -0.02em;
    margin-bottom: 12px;
    transition: color var(--transition-speed) ease;
}}

.subtitle {{
    color: var(--text-secondary);
    font-size: 1.1rem;
    transition: color var(--transition-speed) ease;
}}

/* Control Bar (Tabs & Switch) */
.control-bar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 32px;
}}

.tabs {{
    display: flex;
    gap: 32px;
}}

.tab {{
    color: var(--text-secondary);
    font-weight: 500;
    cursor: pointer;
    padding: 8px 16px;
    border-radius: 8px;
    transition: all var(--transition-speed) ease;
}}

.tab.active {{
    color: var(--text-primary);
    background-color: var(--nav-active-bg);
}}

.toggle-wrapper {{
    display: flex;
    align-items: center;
    gap: 16px;
}}

.toggle-label {{
    color: var(--text-primary);
    font-weight: 500;
    transition: color var(--transition-speed) ease;
}}

/* The Custom Switch */
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
    background-color: var(--toggle-bg);
    transition: background-color var(--transition-speed) ease;
    border-radius: 34px;
}}

.slider:before {{
    position: absolute;
    content: "";
    height: 20px;
    width: 20px;
    left: 4px;
    bottom: 4px;
    background-color: var(--toggle-indicator);
    transition: transform var(--transition-speed) cubic-bezier(0.4, 0.0, 0.2, 1), background-color var(--transition-speed) ease;
    border-radius: 50%;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}}

input:checked + .slider:before {{
    transform: translateX(24px);
}}

/* Cards Grid */
.cards-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
    margin-top: auto;
}}

.card {{
    background-color: var(--card-bg);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid var(--card-border);
    padding: 24px;
    border-radius: 12px;
    box-shadow: var(--card-shadow);
    display: flex;
    flex-direction: column;
    gap: 8px;
    transition: all var(--transition-speed) ease;
}}

.card-tag {{
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    color: var(--text-secondary);
    letter-spacing: 0.05em;
    transition: color var(--transition-speed) ease;
}}

.card h3 {{
    color: var(--text-primary);
    font-size: 1.25rem;
    font-weight: 600;
    transition: color var(--transition-speed) ease;
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
<body class="{initial_class}">
    
    <div class="app-window">
        <!-- Background Ambient Light -->
        <div class="ambient-glow"></div>
        
        <header class="header">
            <div class="mac-dots">
                <div class="dot red"></div>
                <div class="dot yellow"></div>
                <div class="dot green"></div>
            </div>
            <button class="join-btn">Join now &rarr;</button>
        </header>

        <main class="main-content">
            <div class="hero">
                <h1 class="title">{title_text}</h1>
                <p class="subtitle">{body_text}</p>
            </div>

            <div class="control-bar">
                <div class="tabs">
                    <span class="tab">Posts</span>
                    <span class="tab">Blogs</span>
                    <span class="tab active">Videos</span>
                </div>
                
                <div class="toggle-wrapper">
                    <span class="toggle-label">Lights</span>
                    <label class="switch" aria-label="Toggle Dark Mode">
                        <input type="checkbox" id="themeToggle" {is_dark}>
                        <span class="slider"></span>
                    </label>
                </div>
            </div>

            <div class="cards-grid">
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
                    <h3>HomeLab(Self-hosting)</h3>
                </div>
            </div>
        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""/**
 * Dynamic Theme Switcher Logic
 * Listens to the checkbox state and toggles the .dark-mode class on the body.
 * CSS Custom Properties handle all the actual color/background changes.
 */
document.addEventListener('DOMContentLoaded', () => {{
    const themeToggle = document.getElementById('themeToggle');
    
    // Listen for changes on the toggle input
    themeToggle.addEventListener('change', (e) => {{
        if (e.target.checked) {{
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