### 1. High-level Design Pattern Extraction

> **Skill Name**: Ambient Glassmorphism Theme-Toggler

*   **Core Visual Mechanism**: This pattern relies on a combination of **ambient blurred shapes** (`filter: blur()`) sitting behind **frosted glass containers** (`backdrop-filter: blur()`). The visual signature is driven by CSS Custom Properties (variables) that allow a seamless transition between a bright, vivid light mode (e.g., pink/red ambient glow) and a deep, neon-tinted dark mode (e.g., teal/green ambient glow). 
*   **Why Use This Skill (Rationale)**: Glassmorphism combined with ambient glowing backgrounds creates a sense of physical depth and modern elegance. By tying these layers to a dark/light toggle, the UI feels dynamic and highly responsive to user preferences, reducing eye strain while maintaining a high-end aesthetic.
*   **Overall Applicability**: Ideal for personal portfolio hero sections, SaaS dashboard entry pages, "Link-in-bio" pages, and modern web application landing pages where a clean, tech-forward first impression is required.
*   **Value Addition**: Compared to standard flat colored backgrounds, this technique provides texture and lighting. The background isn't a static image; it feels like an atmospheric light source illuminating the frosted glass panels from behind.
*   **Browser Compatibility**: Requires modern browsers. `backdrop-filter` is well-supported but historically required `-webkit-` prefixes on older Safari versions. CSS variables and `filter: blur()` are universally supported in modern environments.

### 2. Visual & Technical Breakdown

*   **Step A: Core Visual Elements**
    *   **Ambient Light Blob**: A simple `div` with `border-radius: 50%` and a massive `filter: blur(100px)`. 
    *   **Frosted Glass Panels**: Achieved using `background: rgba(..., 0.5)` combined with `backdrop-filter: blur(16px)` and a subtle 1px semi-transparent border to simulate a glass edge.
    *   **Color Logic**:
        *   *Light Mode*: Background `#f8f9fa`, Text `#1e293b`, Ambient Blob (Accent) `#ff4757`, Glass `rgba(255, 255, 255, 0.6)`.
        *   *Dark Mode*: Background `#0f172a`, Text `#f8f9fa`, Ambient Blob `#20c997`, Glass `rgba(15, 23, 42, 0.6)`.
    *   **Typography**: Clean, geometric sans-serif (Poppins), utilizing font weights (300 for labels, 600/700 for headings) to establish hierarchy.

*   **Step B: Layout & Compositional Style**
    *   **Positioning**: The ambient blob uses `position: absolute` and a low `z-index` to sit behind all content. The main layout uses CSS Flexbox.
    *   **Spacing**: Generous padding (`32px` to `48px`) inside glass containers to give the text room to breathe, enhancing the "premium" feel.
    *   **Proportions**: The toggle switch is kept compact (e.g., `44px` wide) and neatly tucked in the upper right or right-aligned within a navigation bar.

*   **Step C: Interactive Behavior & Animations**
    *   **Theme Transition**: A smooth crossfade between light and dark modes achieved via `transition: background-color 0.4s ease, color 0.4s ease`. The ambient blob also transitions its background color.
    *   **Toggle Switch**: A hidden HTML checkbox paired with a `<label>`. CSS `transform: translateX()` moves the toggle circle, and `transition` makes it slide smoothly.
    *   **JavaScript Role**: JS is strictly used to listen for the checkbox `change` event and toggle a `.dark` class on the `<body>` element. CSS handles all the visual rendering.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
| :--- | :--- | :--- |
| **Glass panels** | CSS `backdrop-filter` | Native GPU-accelerated blur, perfectly reproduces the tutorial's frosted look. |
| **Ambient glowing blob** | CSS `filter: blur()` | Simple to implement, dynamic, and easily transitioned via CSS variables. |
| **Theme Toggling** | Vanilla JS + CSS Variables | JavaScript manages state (`.dark` class), while CSS variables instantly cascade the color updates without complex DOM manipulation. |
| **Icons & Typography** | Google Fonts + FontAwesome | Matches the clean, modern web aesthetic seen in the reference video. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Why not Your own Services?",
    body_text: str = "Start Your Self-Hosting Journey with us!",
    color_scheme: str = "light",       # "dark" or "light"
    accent_color: str = "#ff4757",     # Used for the ambient blob in light mode
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Ambient Glassmorphism Theme-Toggler.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)
    
    # Pre-calculate dark mode blob color based on input, or default to teal
    dark_blob_color = "#20c997" if accent_color == "#ff4757" else accent_color
    
    # Initial class state based on parameter
    initial_body_class = "dark" if color_scheme == "dark" else ""
    checkbox_checked = "checked" if color_scheme == "dark" else ""

    # === CSS (Using double braces {{ }} to escape standard CSS brackets for Python f-string) ===
    css = f"""/* Glassmorphism & Theme Variables */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

:root {{
    /* Base Dimensions */
    --comp-width: {width_px}px;
    --comp-height: {height_px}px;

    /* Light Theme Variables (Default) */
    --bg-color: #f8f9fa;
    --text-primary: #0f172a;
    --text-secondary: #64748b;
    --ambient-blob: {accent_color};
    --glass-bg: rgba(255, 255, 255, 0.6);
    --glass-border: rgba(255, 255, 255, 0.4);
    --card-hover: rgba(255, 255, 255, 0.8);
    --toggle-bg: #cbd5e1;
    --toggle-knob: #ffffff;
}}

body.dark {{
    /* Dark Theme Variables */
    --bg-color: #0f172a;
    --text-primary: #f8f9fa;
    --text-secondary: #94a3b8;
    --ambient-blob: {dark_blob_color};
    --glass-bg: rgba(15, 23, 42, 0.6);
    --glass-border: rgba(255, 255, 255, 0.08);
    --card-hover: rgba(30, 41, 59, 0.8);
    --toggle-bg: #334155;
    --toggle-knob: #20c997;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Poppins', sans-serif;
    background-color: #1e1e1e; /* Outer background to frame the component */
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}}

/* The main component wrapper acts as the screen/viewport */
.app-container {{
    width: 100%;
    max-width: var(--comp-width);
    height: var(--comp-height);
    background-color: var(--bg-color);
    position: relative;
    overflow: hidden;
    color: var(--text-primary);
    transition: background-color 0.5s ease, color 0.5s ease;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    border-radius: 16px;
    display: flex;
    flex-direction: column;
}}

/* Ambient Background Blob */
.ambient-blob {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 60%;
    height: 60%;
    background-color: var(--ambient-blob);
    border-radius: 50%;
    filter: blur(120px);
    z-index: 0;
    opacity: 0.7;
    transition: background-color 0.8s ease;
    pointer-events: none;
}}

/* Foreground Content */
.content-wrapper {{
    position: relative;
    z-index: 10;
    display: flex;
    flex-direction: column;
    height: 100%;
    padding: 2rem 4rem;
}}

/* Navbar & Toggle */
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
    background: var(--glass-bg);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    padding: 8px 16px;
    border-radius: 30px;
    border: 1px solid var(--glass-border);
    transition: all 0.3s ease;
}}

.theme-toggle-wrapper span {{
    font-size: 0.9rem;
    font-weight: 500;
}}

.toggle-checkbox {{
    display: none;
}}

.toggle-label {{
    width: 46px;
    height: 24px;
    background-color: var(--toggle-bg);
    border-radius: 24px;
    position: relative;
    cursor: pointer;
    transition: background-color 0.3s ease;
}}

.toggle-label::after {{
    content: '';
    position: absolute;
    top: 2px;
    left: 2px;
    width: 20px;
    height: 20px;
    background-color: var(--toggle-knob);
    border-radius: 50%;
    transition: transform 0.3s cubic-bezier(0.4, 0.0, 0.2, 1), background-color 0.3s ease;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}}

.toggle-checkbox:checked + .toggle-label::after {{
    transform: translateX(22px);
}}

/* Hero Section */
.hero {{
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
}}

.hero h1 {{
    font-size: 3.5rem;
    font-weight: 600;
    margin-bottom: 1rem;
    letter-spacing: -1px;
}}

.hero p {{
    font-size: 1.1rem;
    color: var(--text-secondary);
    font-weight: 400;
}}

/* Cards Section */
.glass-panel {{
    background: var(--glass-bg);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid var(--glass-border);
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 2rem;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
    transition: all 0.3s ease;
}}

.card {{
    background: transparent;
    padding: 1.5rem;
    border-radius: 12px;
    cursor: pointer;
    transition: background 0.3s ease, transform 0.2s ease;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}}

.card:hover {{
    background: var(--card-hover);
    transform: translateY(-2px);
}}

.card span {{
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--text-secondary);
    font-weight: 600;
}}

.card h3 {{
    font-size: 1.2rem;
    font-weight: 500;
}}

/* Responsive fallbacks inside component */
@container (max-width: 800px) {{
    .glass-panel {{
        grid-template-columns: 1fr;
    }}
    .hero h1 {{
        font-size: 2.5rem;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body class="{initial_body_class}">

    <div class="app-container" style="container-type: inline-size;">
        
        <!-- The Ambient Glow -->
        <div class="ambient-blob"></div>

        <div class="content-wrapper">
            
            <!-- Top Navigation / Controls -->
            <header>
                <div class="theme-toggle-wrapper">
                    <span>Lights</span>
                    <input type="checkbox" id="themeToggle" class="toggle-checkbox" {checkbox_checked}>
                    <label for="themeToggle" class="toggle-label"></label>
                </div>
            </header>

            <!-- Hero Content -->
            <main class="hero">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
            </main>

            <!-- Glassmorphism Cards Container -->
            <section class="glass-panel">
                <div class="card">
                    <span>Installation Guide</span>
                    <h3>Speedtest-Tracker</h3>
                </div>
                <div class="card">
                    <span>Setup</span>
                    <h3>Uptime-Kuma</h3>
                </div>
                <div class="card">
                    <span>Playlist</span>
                    <h3>HomeLab(Self-hosting)</h3>
                </div>
            </section>

        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Ambient Glassmorphism Theme-Toggler Script
document.addEventListener('DOMContentLoaded', () => {{
    const themeToggle = document.getElementById('themeToggle');
    const body = document.body;

    // Listen for toggle switch changes
    themeToggle.addEventListener('change', (e) => {{
        if (e.target.checked) {{
            body.classList.add('dark');
        }} else {{
            body.classList.remove('dark');
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

*   **Accessibility**:
    *   The toggle switch uses a hidden native `<input type="checkbox">` linked to a visually styled `<label>` via the `for` attribute. This ensures the toggle is keyboard navigable (via Tab) and screen-reader friendly without requiring complex ARIA attributes or custom JS keydown handlers.
    *   Contrast ratios are mapped in the CSS variables to ensure the primary text remains legible against the background variations.
*   **Performance**:
    *   `filter: blur()` on a large element can be somewhat taxing on low-end mobile GPUs. However, because it is applied to a single background `div` without continuous animation (it only animates color on theme toggle), it is generally performant. 
    *   `backdrop-filter` is applied to structural containers. `transform: translateX` is used for the toggle switch movement, ensuring hardware acceleration is utilized and layout repaints are avoided.
    *   CSS Grid and Flexbox are used for structural layout, reducing reliance on expensive absolute positioning loops. Responsive behavior is handled via modern `@container` queries mapped to the component itself, avoiding global window resizing scripts.