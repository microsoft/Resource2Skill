# Interactive SaaS Hero with Embedded Product Demo

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Interactive SaaS Hero with Embedded Product Demo

* **Core Visual Mechanism**: A modern, dark-themed SaaS hero section featuring a centralized, highly prominent "Browser Mockup" container. The defining feature is that this container isn't a static image or a standard video player—it hosts a simulated, interactive click-through product demo (mimicking tools like Supademo). A pulsating "hotspot" guides the user through a simulated workflow, overlaid on a stylized dashboard interface.
* **Why Use This Skill (Rationale)**: The tutorial emphasizes that modern buyers want to "try before they buy" immediately. Static screenshots or long text walls create friction. An interactive demo in the hero section builds trust instantly, reduces friction, and allows users to understand the product's value by *doing* rather than *watching*.
* **Overall Applicability**: Perfect for B2B SaaS landing pages, developer tools, financial tech platforms, and any software marketing page where the user interface is a primary selling point.
* **Value Addition**: Transforms a passive reading experience into an active learning experience right at the top of the funnel. It significantly increases time-on-page and engagement rates compared to a standard static hero section.
* **Browser Compatibility**: Uses standard CSS Grid/Flexbox, `radial-gradient`, `box-shadow`, and vanilla JavaScript. Compatible with all modern browsers (Edge, Chrome, Firefox, Safari).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  * **Color Logic**: Deep dark background (`#0d111c`) with subtle glowing ambient lights behind the main container to draw the eye. High-contrast white text (`#ffffff`), and a vibrant accent color (`#635bff` or user-defined) used for buttons, glowing hotspots, and interactive tooltips.
  * **Typography**: Clean, sans-serif typography using 'Inter'. Large, commanding `h1` (e.g., 3.5rem, bold, slightly tight tracking `-0.02em`) and readable, subdued `p` subheadings (`#9ca3af`, 1.25rem).
  * **Structural Elements**: A macOS-style browser frame containing three colored dots (red, yellow, green) to instantly communicate "this is a software window".

* **Step B: Layout & Compositional Style**
  * **Layout System**: A vertical Flexbox stack. The text content (Headline, Subhead, CTA) sits centered at the top, followed by a large, prominent mock browser window directly below it.
  * **Spatial Feel**: Generous padding (e.g., `80px` top and bottom) to let the hero breathe. The mock browser has a subtle, semi-transparent border (`rgba(255, 255, 255, 0.1)`) and a deep shadow (`box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5)`) to lift it off the background.

* **Step C: Interactive Behavior & Animations**
  * **The "Hotspot" Loop**: A pulsating dot (created via CSS `@keyframes` scaling a semi-transparent ring) acts as the primary interactive element.
  * **JavaScript State Machine**: A lightweight JS script tracks the `currentStep`. When the hotspot is clicked, the script translates the hotspot to the next target element in the mock UI and updates the instruction tooltip, simulating a guided product tour.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Dark SaaS Hero Layout | CSS Flexbox & Grid | Provides flawless responsive centering and structural alignment without JS overhead. |
| Ambient Glow Effect | CSS `radial-gradient` | Creates the premium "glowing" aesthetic common in modern dev/SaaS tools behind the hero image. |
| Browser Mockup UI | HTML/CSS | Simple `div` borders and border-radii accurately mimic an OS window without needing heavy external image assets. |
| Interactive Demo Flow | Vanilla JavaScript | Calculates absolute coordinates of mock UI elements and animates the hotspot to simulate the "Supademo" interactive experience shown in the video. |
| Pulsating Hotspot | CSS `@keyframes` | Native GPU-accelerated animation for the pulsing ring to draw user attention. |

*Feasibility Assessment*: 90%. While we cannot embed a real 3rd-party "Supademo" iframe (since we lack a live URL to the user's specific product), we perfectly reproduce the *pattern* by building a simulated mock-dashboard with a functional, state-driven click-through hotspot system.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Banking Built for Modern SaaS Startups",
    body_text: str = "A fast, secure, and intuitive platform that helps teams manage cash, cards, payments, and treasury — all in one powerful dashboard.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#635bff",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 900,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Interactive SaaS Hero visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#0a0c10"
        text_color = "#ffffff"
        text_muted = "#9ca3af"
        surface_color = "#11141d"
        border_color = "rgba(255, 255, 255, 0.1)"
        mock_ui_bg = "#0d1117"
        mock_ui_element = "rgba(255, 255, 255, 0.05)"
    else:
        bg_color = "#f9fafb"
        text_color = "#111827"
        text_muted = "#4b5563"
        surface_color = "#ffffff"
        border_color = "rgba(0, 0, 0, 0.1)"
        mock_ui_bg = "#f3f4f6"
        mock_ui_element = "rgba(0, 0, 0, 0.05)"

    # === CSS ===
    css = f"""/* Interactive SaaS Hero — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --surface: {surface_color};
    --border: {border_color};
    --mock-bg: {mock_ui_bg};
    --mock-element: {mock_ui_element};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    overflow-x: hidden;
    position: relative;
}}

/* Ambient Background Glow */
body::before {{
    content: '';
    position: absolute;
    top: -20%;
    left: 50%;
    transform: translateX(-50%);
    width: 80%;
    height: 800px;
    background: radial-gradient(circle, var(--accent) 0%, transparent 60%);
    opacity: 0.15;
    filter: blur(100px);
    z-index: -1;
    pointer-events: none;
}}

.hero-container {{
    max-width: var(--width);
    width: 100%;
    padding: 80px 24px;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    z-index: 1;
}}

.hero-text {{
    max-width: 800px;
    margin-bottom: 60px;
}}

.hero-title {{
    font-size: clamp(2.5rem, 5vw, 4rem);
    font-weight: 700;
    line-height: 1.1;
    letter-spacing: -0.02em;
    margin-bottom: 24px;
}}

.hero-subtitle {{
    font-size: 1.25rem;
    color: var(--text-muted);
    line-height: 1.6;
    margin-bottom: 32px;
    max-width: 650px;
    margin-left: auto;
    margin-right: auto;
}}

.cta-button {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background-color: var(--accent);
    color: #ffffff;
    padding: 14px 28px;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 500;
    text-decoration: none;
    transition: transform 0.2s, box-shadow 0.2s;
    border: none;
    cursor: pointer;
}}

.cta-button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 10px 25px -5px rgba(99, 91, 255, 0.4);
}}

/* Browser Mockup / Interactive Demo */
.demo-window {{
    width: 100%;
    max-width: 1024px;
    background-color: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    position: relative;
    aspect-ratio: 16 / 10;
    display: flex;
    flex-direction: column;
}}

.browser-chrome {{
    height: 48px;
    background-color: var(--surface);
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    padding: 0 16px;
    gap: 8px;
}}

.chrome-dot {{
    width: 12px;
    height: 12px;
    border-radius: 50%;
}}
.chrome-dot.red {{ background-color: #ff5f56; }}
.chrome-dot.yellow {{ background-color: #ffbd2e; }}
.chrome-dot.green {{ background-color: #27c93f; }}

.chrome-url {{
    margin: 0 auto;
    background-color: var(--mock-bg);
    padding: 6px 64px;
    border-radius: 6px;
    font-size: 0.75rem;
    color: var(--text-muted);
    transform: translateX(-24px); /* offset for dots */
}}

/* Mock Dashboard Layout */
.demo-dashboard {{
    flex: 1;
    background-color: var(--mock-bg);
    display: flex;
    position: relative;
}}

.mock-sidebar {{
    width: 220px;
    border-right: 1px solid var(--border);
    padding: 24px 16px;
    display: flex;
    flex-direction: column;
    gap: 12px;
}}

.mock-nav-item {{
    height: 32px;
    border-radius: 6px;
    background-color: transparent;
    transition: background-color 0.2s;
}}
.mock-nav-item.active {{
    background-color: var(--mock-element);
}}

.mock-main {{
    flex: 1;
    padding: 32px;
    display: flex;
    flex-direction: column;
    gap: 24px;
}}

.mock-header-block {{
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.mock-title-skeleton {{
    width: 200px;
    height: 28px;
    background-color: var(--mock-element);
    border-radius: 6px;
}}

.mock-btn-skeleton {{
    width: 120px;
    height: 36px;
    background-color: var(--accent);
    border-radius: 6px;
}}

.mock-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
}}

.mock-card {{
    height: 120px;
    background-color: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
}}

.mock-table {{
    flex: 1;
    background-color: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    margin-top: 16px;
}}

/* Interactive Demo Overlay System */
.demo-overlay {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 10;
}}

.hotspot-wrapper {{
    position: absolute;
    pointer-events: auto;
    transform: translate(-50%, -50%);
    transition: left 0.6s cubic-bezier(0.34, 1.56, 0.64, 1), top 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
    z-index: 20;
}}

.hotspot {{
    width: 24px;
    height: 24px;
    background-color: var(--accent);
    border-radius: 50%;
    cursor: pointer;
    position: relative;
    box-shadow: 0 0 0 4px rgba(0,0,0,0.2);
}}

.hotspot::before {{
    content: '';
    position: absolute;
    top: -8px;
    left: -8px;
    right: -8px;
    bottom: -8px;
    border-radius: 50%;
    border: 2px solid var(--accent);
    animation: pulse 2s infinite;
}}

@keyframes pulse {{
    0% {{ transform: scale(0.8); opacity: 1; }}
    100% {{ transform: scale(2); opacity: 0; }}
}}

.tooltip {{
    position: absolute;
    top: calc(100% + 16px);
    left: 50%;
    transform: translateX(-50%);
    background-color: var(--text);
    color: var(--bg);
    padding: 12px 16px;
    border-radius: 8px;
    font-size: 0.875rem;
    font-weight: 500;
    white-space: nowrap;
    pointer-events: none;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
    opacity: 0;
    transition: opacity 0.3s ease;
}}

.tooltip.show {{
    opacity: 1;
}}

.tooltip::before {{
    content: '';
    position: absolute;
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%);
    border-width: 8px;
    border-style: solid;
    border-color: transparent transparent var(--text) transparent;
}}

/* End Screen */
.demo-complete {{
    position: absolute;
    inset: 0;
    background-color: rgba(0,0,0,0.8);
    backdrop-filter: blur(4px);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.4s;
    z-index: 30;
}}

.demo-complete.show {{
    opacity: 1;
    pointer-events: auto;
}}

.demo-complete h3 {{
    font-size: 1.5rem;
    margin-bottom: 16px;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="hero-container">
        <div class="hero-text">
            <h1 class="hero-title">{title_text}</h1>
            <p class="hero-subtitle">{body_text}</p>
            <button class="cta-button">Open a Free Account</button>
        </div>

        <div class="demo-window" id="demo-window">
            <div class="browser-chrome">
                <div class="chrome-dot red"></div>
                <div class="chrome-dot yellow"></div>
                <div class="chrome-dot green"></div>
                <div class="chrome-url">app.mercury.demo</div>
            </div>
            
            <div class="demo-dashboard">
                <div class="mock-sidebar">
                    <div class="mock-nav-item active"></div>
                    <div class="mock-nav-item" id="target-1"></div>
                    <div class="mock-nav-item"></div>
                    <div class="mock-nav-item"></div>
                </div>
                <div class="mock-main">
                    <div class="mock-header-block">
                        <div class="mock-title-skeleton"></div>
                        <div class="mock-btn-skeleton" id="target-3"></div>
                    </div>
                    <div class="mock-grid">
                        <div class="mock-card"></div>
                        <div class="mock-card" id="target-2"></div>
                        <div class="mock-card"></div>
                    </div>
                    <div class="mock-table" id="target-4"></div>
                </div>

                <div class="demo-overlay" id="demo-overlay">
                    <div class="hotspot-wrapper" id="hotspot-wrapper">
                        <div class="hotspot" id="hotspot"></div>
                        <div class="tooltip" id="tooltip">Click to navigate</div>
                    </div>
                </div>

                <div class="demo-complete" id="demo-complete">
                    <h3>Demo Complete!</h3>
                    <button class="cta-button" onclick="location.reload()">Replay Demo</button>
                </div>
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Interactive SaaS Hero Demo Logic
document.addEventListener('DOMContentLoaded', () => {{
    const demoWindow = document.getElementById('demo-window');
    const hotspotWrapper = document.getElementById('hotspot-wrapper');
    const hotspot = document.getElementById('hotspot');
    const tooltip = document.getElementById('tooltip');
    const completeScreen = document.getElementById('demo-complete');

    // Define the interactive steps
    const steps = [
        {{ targetId: 'target-1', text: 'Navigate to Payments' }},
        {{ targetId: 'target-2', text: 'View Recent Transactions' }},
        {{ targetId: 'target-3', text: 'Create New Payment Link' }},
        {{ targetId: 'target-4', text: 'Review Account History' }}
    ];

    let currentStepIndex = 0;

    // Initialize layout
    function positionHotspot(index) {{
        if (index >= steps.length) {{
            completeDemo();
            return;
        }}

        const step = steps[index];
        const targetEl = document.getElementById(step.targetId);
        
        if (!targetEl) return;

        // Calculate coordinates relative to the demo dashboard area
        const dashboardRect = document.querySelector('.demo-dashboard').getBoundingClientRect();
        const targetRect = targetEl.getBoundingClientRect();

        const relativeX = targetRect.left - dashboardRect.left + (targetRect.width / 2);
        const relativeY = targetRect.top - dashboardRect.top + (targetRect.height / 2);

        // Move the hotspot
        hotspotWrapper.style.left = `${{relativeX}}px`;
        hotspotWrapper.style.top = `${{relativeY}}px`;
        
        // Update tooltip text and show
        tooltip.textContent = step.text;
        tooltip.classList.remove('show');
        
        // Simulate loading/transition feeling
        setTimeout(() => {{
            tooltip.classList.add('show');
        }}, 300);

        // Add visual feedback to target
        document.querySelectorAll('.mock-nav-item, .mock-card, .mock-table, .mock-btn-skeleton').forEach(el => {{
            el.style.boxShadow = 'none';
        }});
        targetEl.style.boxShadow = '0 0 0 2px var(--accent)';
    }}

    function completeDemo() {{
        hotspotWrapper.style.display = 'none';
        completeScreen.classList.add('show');
    }}

    // Handle hotspot clicks
    hotspot.addEventListener('click', () => {{
        tooltip.classList.remove('show');
        
        // Brief delay to make it feel like real software responding
        setTimeout(() => {{
            currentStepIndex++;
            positionHotspot(currentStepIndex);
        }}, 150);
    }});

    // Handle window resizing to keep hotspot aligned
    window.addEventListener('resize', () => {{
        if (currentStepIndex < steps.length) {{
            positionHotspot(currentStepIndex);
        }}
    }});

    // Kick off the first step
    setTimeout(() => {{
        positionHotspot(0);
    }}, 500);
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

* **Accessibility**:
  * The current interactive demo relies heavily on visual cues (the pulsating hotspot and simulated mouse tracking). In a real production environment where accessibility is strictly required, the demo wrapper (`.demo-window`) should be paired with an `aria-label` stating "Interactive product demonstration", and the hotspot button should be focusable via `tabindex="0"` with proper keyboard event listeners (`keydown` -> 'Enter'/'Space') to allow keyboard navigation through the steps.
  * Contrast ratios between text and background in the Dark Theme exceed the WCAG AA minimum 4.5:1 requirement.
* **Performance**:
  * The pulsing animation relies on `transform` and `opacity` properties which are hardware-accelerated, minimizing layout recalculations and ensuring buttery 60fps animations.
  * The positioning logic uses `.getBoundingClientRect()` triggered during window resize events. While fast, if this component is placed on a page with heavy DOM reflows, attaching a `debounce()` function to the `resize` listener in `script.js` is recommended.