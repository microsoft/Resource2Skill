# Orchestrated GSAP Entry Timeline

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Orchestrated GSAP Entry Timeline

* **Core Visual Mechanism**: A highly choreographed, sequential load-in sequence for a webpage layout using GreenSock Animation Platform (GSAP). The technique utilizes a central `gsap.timeline()` to sequence multiple elements entering the viewport from different directions (top, left, right, bottom) using a mix of `from()`, `to()`, and `fromTo()` methods. It features varied easing curves (bounce, elastic, power-in), staggered fades, absolute timeline offsets, and a programmatic reverse function triggered by a user interaction.
* **Why Use This Skill (Rationale)**: Native CSS animations can become notoriously fragile and complex when managing long sequences of staggered delays. GSAP timelines centralize this logic, allowing developers to orchestrate a "symphony" of UI components loading in with precise timing, offsets, and physics-based easing. The ability to easily reverse the entire sequence with varied time scales provides a satisfying exit animation.
* **Overall Applicability**: Perfect for splash screens, dashboard initial loads, portfolio hero reveals, and presentation websites where the entrance of the UI is part of the storytelling.
* **Value Addition**: Transforms a static page load into a premium, cinematic experience. It guides the user's eye around the interface in a specific order (e.g., Header -> Links -> Content -> Footer), establishing a strong sense of spatial layout and hierarchy.
* **Browser Compatibility**: GSAP ensures broad cross-browser consistency (Chrome, Firefox, Safari, Edge, Safari iOS). Requires modern browsers that support basic CSS transforms and Flexbox/Grid for the underlying layout. 

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  *   **Structural Blocks**: Header, Left Sidebar, Right Sidebar, Footer, and a Center Content area.
  *   **CSS Properties**: Relies heavily on CSS `transform` (`translateY`, `translateX`, `scale`, `rotate`) to push elements off-screen initially.
  *   **Overflow Control**: The `body` must utilize `overflow: hidden;` during the entry animation to prevent massive scrollbars from appearing when elements (like the right sidebar) are positioned `100vw` off-screen.

* **Step B: Layout & Compositional Style**
  *   **Flexbox Hierarchy**: 
      *   Main container uses `display: flex; flex-direction: column; height: 100vh;`.
      *   The middle section uses `flex-grow: 1; display: flex; justify-content: space-between;` to push the sidebars to the edges and keep the button centered.
  *   **Z-index Layering**: Sidebars, header, and footer sit on standard planes, but their initial CSS states (e.g., `transform: translateY(100%)` for the footer) prepare them for the JavaScript interpolation.

* **Step C: Interactive Behavior & Animations**
  *   **Header Drop**: Uses `gsap.from()` with `y: '-100%'` and an `ease: 'bounce'` to drop and settle.
  *   **Link Stagger**: Uses `gsap.from()` with `opacity: 0` and a `stagger: 0.2` property to fade in children sequentially.
  *   **Sidebar Slides**: Uses absolute timeline positioning (e.g., `, 1` and `, 1.5`) to force the animations to start exactly at those second marks on the timeline, regardless of the previous animations' durations. One uses `ease: 'power2.in'` to accelerate.
  *   **Footer Pop**: Uses `gsap.to()` animating `y: 0` with an `ease: 'elastic'` to snap up from the bottom.
  *   **Button Spin**: Uses `gsap.fromTo()` to explicitly declare both starting (`opacity: 0, scale: 0, rotation: 720`) and ending (`opacity: 1, scale: 1, rotation: 0`) states.
  *   **Reverse Logic**: Clicking the button triggers `timeline.timeScale(3)` to speed it up 3x, followed by `timeline.reverse()` to play the timeline backward.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Sequential entry logic | GSAP (`gsap.timeline`) | Simplifies chaining, offsets, and staggering compared to complex CSS `animation-delay` calculations. |
| Playback reversal | GSAP `timeline.reverse()` | Native method inside GSAP to perfectly reverse interpolated values and easings at accelerated speeds. |
| Page Layout | CSS Flexbox | Matches the tutorial's straightforward Header/Sidebars/Footer block model, cleanly adapting to viewport dimensions. |

> **Feasibility Assessment**: 100% reproduction. The code translates the exact structural blocks and GSAP timeline chaining demonstrated in the tutorial, while elevating the raw garish colors used in the video into a highly polished, responsive dashboard wireframe utilizing the function parameters.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Dashboard Reveal",
    body_text: str = "GSAP Timeline Orchestration",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Orchestrated GSAP Entry Timeline visual effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#0a0a0a"
        surface_color = "#171717"
        surface_border = "#262626"
        text_color = "#f5f5f5"
        text_muted = "#a3a3a3"
    else:
        bg_color = "#f5f5f5"
        surface_color = "#ffffff"
        surface_border = "#e5e5e5"
        text_color = "#171717"
        text_muted = "#525252"

    # === CSS ===
    css = f"""/* Orchestrated GSAP Entry Timeline */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --surface: {surface_color};
    --border: {surface_border};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    /* Prevents horizontal/vertical scrollbars during off-screen entry animations */
    overflow: hidden; 
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}}

.app-frame {{
    width: {width_px}px;
    height: {height_px}px;
    max-width: 100vw;
    max-height: 100vh;
    display: flex;
    flex-direction: column;
    background-color: var(--bg);
    position: relative;
    overflow: hidden;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}}

/* Header */
.header {{
    height: 15%;
    background-color: var(--accent);
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 2rem;
    z-index: 10;
}}

.header h2 {{
    font-weight: 600;
    letter-spacing: -0.02em;
}}

.nav-links {{
    display: flex;
    gap: 2rem;
}}

.link {{
    font-weight: 500;
    opacity: 0.9;
    cursor: pointer;
}}

/* Middle Content Area */
.content-area {{
    flex-grow: 1;
    display: flex;
    justify-content: space-between;
    position: relative;
}}

/* Sidebars */
.sidebar {{
    width: 20%;
    background-color: var(--surface);
    border-left: 1px solid var(--border);
    border-right: 1px solid var(--border);
    padding: 2rem;
    z-index: 5;
}}

.sidebar h3 {{
    font-size: 0.875rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-muted);
    margin-bottom: 1.5rem;
}}

.sidebar-item {{
    height: 2.5rem;
    background-color: var(--bg);
    border: 1px solid var(--border);
    border-radius: 0.375rem;
    margin-bottom: 1rem;
}}

/* Center Main Area */
.main-center {{
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 2rem;
    z-index: 1;
}}

.main-center h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
}}

.main-center p {{
    color: var(--text-muted);
    margin-bottom: 2rem;
}}

/* Reverse Button */
.reverse-btn {{
    background-color: var(--text);
    color: var(--bg);
    border: none;
    padding: 0.875rem 2rem;
    font-size: 1rem;
    font-weight: 600;
    border-radius: 9999px;
    cursor: pointer;
    transition: transform 0.2s ease, background-color 0.2s ease;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}}

.reverse-btn:hover {{
    transform: translateY(-2px);
    background-color: var(--accent);
    color: #fff;
}}

/* Footer */
.footer {{
    height: 10%;
    background-color: var(--surface);
    border-top: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.875rem;
    color: var(--text-muted);
    z-index: 10;
    /* Starting position out-of-frame for gsap.to() demonstration */
    transform: translateY(100%); 
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
    <!-- Load GSAP from CDN -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
</head>
<body>
    <div class="app-frame">
        
        <!-- Header -->
        <header class="header">
            <h2>System.</h2>
            <div class="nav-links">
                <div class="link">Home</div>
                <div class="link">Analytics</div>
                <div class="link">Settings</div>
            </div>
        </header>

        <!-- Main Content (Sidebars + Center) -->
        <main class="content-area">
            
            <aside class="sidebar sidebar-left">
                <h3>Navigation</h3>
                <div class="sidebar-item"></div>
                <div class="sidebar-item"></div>
                <div class="sidebar-item"></div>
            </aside>

            <div class="main-center">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
                <button class="reverse-btn">Reverse Sequence!</button>
            </div>

            <aside class="sidebar sidebar-right">
                <h3>Details</h3>
                <div class="sidebar-item"></div>
                <div class="sidebar-item"></div>
            </aside>

        </main>

        <!-- Footer -->
        <footer class="footer">
            Status: System Loaded Successfully
        </footer>

    </div>

    <!-- Application Script -->
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Ensure DOM is loaded
document.addEventListener('DOMContentLoaded', () => {{
    
    // 1. Initialize GSAP Timeline with default duration
    const tl = gsap.timeline({{ defaults: {{ duration: 1 }} }});

    // 2. Orchestrate Sequence
    tl.from('.header', {{ 
        y: '-100%', 
        ease: 'bounce' 
    }})
    .from('.link', {{ 
        opacity: 0, 
        stagger: 0.15 
    }})
    // Absolute position: starts exactly at 1 second on the timeline
    .from('.sidebar-right', {{ 
        x: '100vw', 
        ease: 'power2.in' 
    }}, 1)
    // Absolute position: starts exactly at 1.5 seconds
    .from('.sidebar-left', {{ 
        x: '-100%' 
    }}, 1.5)
    // The footer already has 'transform: translateY(100%)' in CSS. We animate it TO 0.
    // Absolute position: starts at 2.5 seconds
    .to('.footer', {{ 
        y: 0, 
        ease: 'elastic' 
    }}, 2.5)
    // fromTo forces both explicit start and end states
    // Absolute position: starts at 3 seconds
    .fromTo('.reverse-btn', 
        {{ opacity: 0, scale: 0, rotation: 720 }}, 
        {{ opacity: 1, scale: 1, rotation: 0 }}, 
    3);

    // Optional: Reveal the central text alongside the button
    tl.from('.main-center h1, .main-center p', {{
        opacity: 0,
        y: 20,
        stagger: 0.2
    }}, 3.2);

    // 3. Interactive Reversal Logic
    const reverseBtn = document.querySelector('.reverse-btn');
    
    reverseBtn.addEventListener('click', () => {{
        // Speed up the reversal by 3x for a snappier exit
        tl.timeScale(3);
        // Play timeline backwards
        tl.reverse();
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

* **Performance**: 
  * **GPU Acceleration**: GSAP optimizes `transform` (`x`, `y`, `scale`, `rotation`) and `opacity` properties under the hood by mapping them to hardware-accelerated composite layers. This avoids triggering browser reflows/repaints compared to animating properties like `top`, `left`, `width`, or `height`.
  * The `body { overflow: hidden; }` prevents layout thrashing caused by the appearance and disappearance of massive scrollbars when elements are shifted off-canvas (e.g. `x: '100vw'`).
* **Accessibility**:
  * **Prefers Reduced Motion**: Advanced GSAP timelines should ideally respect `prefers-reduced-motion`. In a production environment, you would wrap the timeline logic in a media query check: `window.matchMedia('(prefers-reduced-motion: reduce)').matches`. If true, bypass the timeline or switch to a simple opacity-only `.to('.app-frame', { opacity: 1, duration: 0.5 })` fade-in.
  * **Focus Management**: Off-screen elements natively maintain their tab-index in HTML unless manually overridden or given `display: none` / `visibility: hidden`. Since GSAP alters `transform`, keyboard users might tab to a button that is currently functionally off-screen. Setting initial states via `gsap.fromTo` (or chaining `.set()` early in the timeline to handle `visibility`) handles these a11y edge-cases.