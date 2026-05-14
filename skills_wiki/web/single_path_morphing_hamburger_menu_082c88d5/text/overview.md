# Single-Path Morphing Hamburger Menu

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Single-Path Morphing Hamburger Menu

* **Core Visual Mechanism**: This technique uses a singular, cleverly constructed SVG `<path>` to represent a hamburger menu, and animates it into a "close" (X) icon exclusively through CSS path manipulation. It achieves this by shrinking the hamburger lines into dots, sliding those dots invisibly along the path using `stroke-dashoffset` and `stroke-dasharray`, then expanding them back out to form an X while translating and rotating the entire SVG.
* **Why Use This Skill (Rationale)**: Traditional hamburger animations require 3 separate HTML elements (e.g., `span`s) that rely on messy absolute positioning and scaling. The single-path SVG approach provides hardware-accelerated, mathematically perfect intersections, allowing for "swirling" dot animations that feel incredibly organic and fluid without relying on external libraries like GSAP or Lottie.
* **Overall Applicability**: Perfect for high-end UI headers, floating action buttons (FABs), and mobile navigation toggles where micro-interactions are critical for product feel. It brings a "premium" software aesthetic to functional UI.
* **Value Addition**: It condenses multiple DOM elements into one semantic `<svg>` inside a `<button>`, reducing markup while introducing a highly polished, bespoke animation that delights users.
* **Browser Compatibility**: Fully supported in modern browsers. Relies on standard CSS transforms (`rotate`, `translate`) on SVG elements and `stroke-dasharray` animations (Supported in Chrome 85+, Safari 14+, Firefox 72+). 

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **SVG Path Magic**: The magic resides in `d="m 20 40 h 60 a 1 1 0 0 1 0 20 h -60 a 1 1 0 0 1 0 -40 h 30 v 70"`. This continuous line traverses the top layer, arcs to the bottom layer, arcs again, and intersects itself with a vertical line. 
  - **Stroke Properties**: `stroke-linecap="round"` is critical. When the `stroke-dasharray` gap is large and the dash is `0`, the round cap ensures it renders as a perfect circular dot rather than disappearing.
  - **Color Logic**: A vivid accent stroke `var(--accent)` (e.g., `#00bfff`) against a subdued surface backdrop `rgba(255,255,255,0.06)` creates strong icon legibility.

* **Step B: Layout & Compositional Style**
  - The SVG uses `viewBox="0 0 100 100"`. The design aligns geometrically with the mathematical center (`50 50`).
  - By manipulating the CSS properties `translate: 0 -10px` and `rotate: 0.125turn`, the intersection of the newly formed paths perfectly aligns with the center of the previous hamburger icon. 

* **Step C: Interactive Behavior & Animations**
  - The behavior is state-driven via JavaScript updating `aria-expanded="true" / "false"`, making it fully accessible while hooking CSS animations natively to the semantic state.
  - **Keyframes Phase 1 (`0% - 40%`)**: The dash sizes reduce to `0`, leaving two dots.
  - **Keyframes Phase 2 (`40% - 60%`)**: The gaps and offsets are drastically changed (`stroke-dashoffset: -90`), sliding the dots along the unseen path to their new target origins, combined with rotation and translation.
  - **Keyframes Phase 3 (`60% - 100%`)**: The dashes grow back out (`60`), intersecting precisely to form an `X` (or "plus" that is rotated 45 degrees).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Single-Element Structure | Inline SVG Path | Provides raw graphical precision; inherently responsive and scales without pixelation. |
| Path Morphing | CSS `stroke-dasharray` & `stroke-dashoffset` | Allows "drawing" and "erasing" sections of the SVG dynamically without JS frame loops. |
| Movement & Swirl | CSS `@keyframes` with `translate`/`rotate` | Hardware-accelerated transforms yield native 60fps+ rendering for the complex overlapping motion. |
| State Management | JS & `aria-expanded` | The most robust, accessible way to toggle states, tying semantic HTML directly to CSS hooks. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Premium Navigation",
    body_text: str = "Click the interactive SVG menu button below to experience the single-path morphing animation.",
    color_scheme: str = "dark",
    accent_color: str = "#00E5FF",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Single-Path Morphing Hamburger Menu effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os
    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_color = "#f8fafc"
        surface_color = "#1e293b"
        border_color = "rgba(255, 255, 255, 0.1)"
        hover_surface = "#334155"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        surface_color = "#ffffff"
        border_color = "rgba(0, 0, 0, 0.1)"
        hover_surface = "#f1f5f9"

    css = f"""/* Single-Path Morphing Hamburger Menu */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --hover-surface: {hover_surface};
    --border: {border_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 20px;
    width: 100%;
    max-width: 420px;
    padding: 2rem;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}}

.header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
}}

.header-content h1 {{
    font-size: 1.5rem;
    font-weight: 600;
    letter-spacing: -0.025em;
    margin-bottom: 0.25rem;
}}

.header-content p {{
    font-size: 0.875rem;
    opacity: 0.7;
    max-width: 250px;
    line-height: 1.4;
}}

/* === The Interactive Button === */
.menu-btn {{
    background: transparent;
    border: 1px solid var(--border);
    border-radius: 16px;
    cursor: pointer;
    width: 64px;
    height: 64px;
    display: grid;
    place-items: center;
    transition: background 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
}}

.menu-btn:hover, .menu-btn[aria-expanded="true"] {{
    background: var(--hover-surface);
    border-color: var(--accent);
    box-shadow: 0 4px 20px -8px var(--accent);
}}

/* === The Core SVG Magic === */
.hamburger-svg {{
    width: 48px;
    height: 48px;
    overflow: visible;
}}

.hamburger-path {{
    fill: none;
    stroke: var(--accent);
    stroke-width: 8;
    stroke-linecap: round;
    stroke-linejoin: round;
    /* Geometrically locked transform origin relative to 100x100 viewBox */
    transform-origin: 50px 50px; 
    
    animation-duration: 0.7s;
    animation-fill-mode: forwards;
    animation-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
    
    /* Initial Hamburger State */
    stroke-dasharray: 60 31 60 300;
    stroke-dashoffset: 0;
}}

/* State: Transition to Close (X) */
.menu-btn[aria-expanded="true"] .hamburger-path {{
    animation-name: path-to-close;
}}

/* State: Transition back to Hamburger (only trigger if interacted with) */
.menu-btn.interacted[aria-expanded="false"] .hamburger-path {{
    animation-name: path-to-open;
}}

/* Keyframes for morphing */
@keyframes path-to-close {{
    0% {{
        stroke-dasharray: 60 31 60 300;
        stroke-dashoffset: 0;
        translate: 0 0;
        rotate: 0turn;
    }}
    40% {{
        stroke-dasharray: 0 91 0 300;
        stroke-dashoffset: 0;
        translate: 0 0;
        rotate: 0turn;
    }}
    60% {{
        stroke-dasharray: 0 165 0 300;
        stroke-dashoffset: -90;
        translate: 0 -10px;
        rotate: 0.125turn;
    }}
    100% {{
        stroke-dasharray: 60 105 60 300;
        stroke-dashoffset: -90;
        translate: 0 -10px;
        rotate: 0.125turn;
    }}
}}

@keyframes path-to-open {{
    0% {{
        stroke-dasharray: 60 105 60 300;
        stroke-dashoffset: -90;
        translate: 0 -10px;
        rotate: 0.125turn;
    }}
    40% {{
        stroke-dasharray: 0 165 0 300;
        stroke-dashoffset: -90;
        translate: 0 -10px;
        rotate: 0.125turn;
    }}
    60% {{
        stroke-dasharray: 0 91 0 300;
        stroke-dashoffset: 0;
        translate: 0 0;
        rotate: 0turn;
    }}
    100% {{
        stroke-dasharray: 60 31 60 300;
        stroke-dashoffset: 0;
        translate: 0 0;
        rotate: 0turn;
    }}
}}

/* === Staggered Nav Menu Reveal === */
.nav-menu {{
    display: grid;
    grid-template-rows: 0fr;
    transition: grid-template-rows 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}}

.nav-menu ul {{
    overflow: hidden;
    list-style: none;
    display: flex;
    flex-direction: column;
}}

.nav-menu li {{
    padding: 1rem 0;
    border-bottom: 1px solid var(--border);
    transform: translateY(12px);
    opacity: 0;
    transition: transform 0.4s ease, opacity 0.4s ease;
    font-weight: 500;
    color: var(--accent);
    cursor: pointer;
}}

.nav-menu li:last-child {{
    border-bottom: none;
}}

.menu-btn[aria-expanded="true"] ~ .nav-menu {{
    grid-template-rows: 1fr;
    margin-top: 1rem;
}}

.menu-btn[aria-expanded="true"] ~ .nav-menu li {{
    transform: translateY(0);
    opacity: 1;
}}

.menu-btn[aria-expanded="true"] ~ .nav-menu li:nth-child(1) {{ transition-delay: 0.15s; }}
.menu-btn[aria-expanded="true"] ~ .nav-menu li:nth-child(2) {{ transition-delay: 0.25s; }}
.menu-btn[aria-expanded="true"] ~ .nav-menu li:nth-child(3) {{ transition-delay: 0.35s; }}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="card">
        <header class="header">
            <div class="header-content">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
            </div>
            
            <button class="menu-btn" aria-controls="nav-menu" aria-expanded="false" aria-label="Toggle navigation">
                <svg class="hamburger-svg" viewBox="0 0 100 100">
                    <path class="hamburger-path" d="m 20 40 h 60 a 1 1 0 0 1 0 20 h -60 a 1 1 0 0 1 0 -40 h 30 v 70" />
                </svg>
            </button>
            
        </header>

        <nav id="nav-menu" class="nav-menu">
            <ul>
                <li>Dashboard Overview</li>
                <li>Account Settings</li>
                <li>Sign Out</li>
            </ul>
        </nav>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    js = """document.addEventListener('DOMContentLoaded', () => {
    const menuBtn = document.querySelector('.menu-btn');

    menuBtn.addEventListener('click', () => {
        // Evaluate the current state
        const isExpanded = menuBtn.getAttribute('aria-expanded') === 'true';
        
        // Toggle state
        menuBtn.setAttribute('aria-expanded', !isExpanded);
        
        // Flag to prevent 'path-to-open' animation from playing automatically on initial page load
        if (!menuBtn.classList.contains('interacted')) {
            menuBtn.classList.add('interacted');
        }
    });
});
"""

    # Write files
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
  - The implementation uses a native `<button>` element inherently granting keyboard navigability (Tab and Enter/Space support). 
  - The ARIA attribute `aria-expanded` accurately tracks and broadcasts the UI state to screen readers. We hook CSS directly to this attribute (e.g., `[aria-expanded="true"]`) creating a single source of truth for both visuals and accessibility.
* **Performance**: 
  - The animation relies on standard CSS properties like `translate`, `rotate`, and `stroke-dasharray/offset`. Using these avoids expensive browser reflows (layout recalculation) which normally happen when manipulating width/height or top/left margins. 
  - All visual transition is calculated optimally by the browser engine (GPU compositing applied efficiently to transforms). Note that SVG rendering engines can occasionally incur minute repaints, but for sparse graphics like a hamburger icon, the impact is utterly negligible.