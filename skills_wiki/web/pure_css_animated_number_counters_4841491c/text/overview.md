# Pure CSS Animated Number Counters

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Pure CSS Animated Number Counters

* **Core Visual Mechanism**: Animating a numeric value seamlessly from a starting integer (e.g., `0`) to an ending integer (e.g., `1000`) without utilizing any JavaScript for the rendering logic. This is achieved by registering a custom CSS property using `@property` with the `<integer>` syntax, animating it via `@keyframes`, and binding it to a CSS `counter-reset` which is displayed using the `content: counter()` property on a pseudo-element.
* **Why Use This Skill (Rationale)**: Offloading animation logic from JavaScript to the browser's CSS rendering engine provides smoother, hardware-accelerated performance. It simplifies the codebase by eliminating the need for `requestAnimationFrame` loops or `setInterval` timing logic typically used for these effects.
* **Overall Applicability**: This pattern is ideal for "Stats" sections on landing pages (e.g., "Total Users", "Downloads", "Uptime"), dashboard metrics, progress indicators, or milestone counters (like the Pokedex example in the tutorial).
* **Value Addition**: Transforms static text into an engaging, dynamic entry animation that draws the user's eye to key metrics, adding a premium feel to data presentation while maintaining a minimal technical footprint.
* **Browser Compatibility**: This technique relies on the CSS Houdini Properties and Values API (`@property`). It is broadly supported in modern browsers (Chrome 85+, Edge 85+, Safari 16.4+, Firefox 128+). 

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **HTML Structure**: Clean, semantic elements (like `<div class="stat-number">`) acting as anchors. The actual numbers do not exist in the DOM; they are injected via CSS pseudo-elements (`::after`).
  - **Typography**: Uses `font-variant-numeric: tabular-nums;` (or a font like Inter) to prevent layout shifting as the digits rapidly change (e.g., the number '1' takes up the same horizontal space as '8').
  - **Color Logic**: A high-contrast setup to make the numbers pop. E.g., dark background `#0d111c`, translucent card surface `rgba(255, 255, 255, 0.06)`, and a bright accent color `#00bfff` for the animated text.

* **Step B: Layout & Compositional Style**
  - **Grid Layout**: Employs CSS Grid with `repeat(auto-fit, minmax(250px, 1fr))` to create a fully responsive stats row that stacks gracefully on mobile screens.
  - **Card Aesthetic**: The numbers are housed inside "glassy" or subtle surface cards with generous padding (`2.5rem 2rem`), slight border transparency, and a soft box-shadow to elevate them from the background.

* **Step C: Interactive Behavior & Animations**
  - **The Animation Pipeline**: 
    1. `@property --num { syntax: "<integer>"; }` defines the variable.
    2. `@keyframes count { to { --num: 1000; } }` describes the transition.
    3. `.element::after { counter-reset: val var(--num); content: counter(val); animation: count 3s forwards; }` ties it all together.
  - **Timing**: The tutorial uses a `linear` timing function, but a `cubic-bezier(0.16, 1, 0.3, 1)` (ease-out) often feels more natural as the counter slows down before reaching the final value.
  - **Accessibility Fallback**: Uses `@media (prefers-reduced-motion: reduce)` to override the animation and immediately set the `content` property to the final hardcoded string value.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Number increment logic | CSS `@property` + `@keyframes` | The core lesson of the tutorial; replaces JS-based counting loops with native browser rendering. |
| Value display | CSS `counter-reset` + `content` | The only way to display CSS variable values directly as text inside the DOM. |
| Layout / Stacking | CSS Grid | Provides an automatic, responsive container for the stat cards without manual media queries. |
| Scroll triggering (Added value) | JS `IntersectionObserver` | While the counter is pure CSS, adding 10 lines of JS ensures the animation only starts when the user actually scrolls to the component, making it production-ready. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Platform Metrics",
    body_text: str = "Live data rendering purely via CSS `@property` counters.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1000,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Pure CSS Animated Number Counter effect.
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
        surface_color = "rgba(255, 255, 255, 0.04)"
        border_color = "rgba(255, 255, 255, 0.08)"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        surface_color = "rgba(0, 0, 0, 0.03)"
        border_color = "rgba(0, 0, 0, 0.08)"

    # Hardcoded values for the demonstration
    val1, val2, val3 = 1025, 89, 432

    # === CSS ===
    css = f"""/* Pure CSS Animated Number Counters */
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
    --border: {border_color};
    --width: {width_px}px;
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

.container {{
    width: 100%;
    max-width: var(--width);
    display: flex;
    flex-direction: column;
    gap: 3.5rem;
}}

.header {{
    text-align: center;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}}

.title {{
    font-size: 2.5rem;
    font-weight: 800;
    letter-spacing: -0.02em;
}}

.body-text {{
    font-size: 1.1rem;
    opacity: 0.6;
}}

.stats-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 1.5rem;
}}

.stat-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 2.5rem 2rem;
    text-align: center;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.02);
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    transition: transform 0.3s ease, background 0.3s ease;
}}

.stat-card:hover {{
    transform: translateY(-4px);
    background: var(--border);
}}

/* Tabular-nums prevents the text from jittering horizontally as numbers cycle */
.stat-number {{
    font-size: 4rem;
    font-weight: 800;
    color: var(--accent);
    line-height: 1;
    font-variant-numeric: tabular-nums;
}}

.stat-label {{
    font-size: 1.05rem;
    font-weight: 600;
    opacity: 0.8;
}}

/* ========================================= */
/* === THE MAGIC: CSS COUNTER ANIMATIONS === */
/* ========================================= */

@property --num1 {{ syntax: "<integer>"; initial-value: 0; inherits: false; }}
@property --num2 {{ syntax: "<integer>"; initial-value: 0; inherits: false; }}
@property --num3 {{ syntax: "<integer>"; initial-value: 0; inherits: false; }}

@keyframes countUp1 {{ to {{ --num1: {val1}; }} }}
@keyframes countUp2 {{ to {{ --num2: {val2}; }} }}
@keyframes countUp3 {{ to {{ --num3: {val3}; }} }}

/* Bind the custom property to the CSS counter */
.stat-1::after {{ counter-reset: c1 var(--num1); content: counter(c1); }}
.stat-2::after {{ counter-reset: c2 var(--num2); content: counter(c2); }}
.stat-3::after {{ counter-reset: c3 var(--num3); content: counter(c3); }}

/* Trigger animation only when the parent gets the .in-view class from JS */
.in-view .stat-1::after {{ animation: countUp1 2.5s cubic-bezier(0.16, 1, 0.3, 1) forwards; }}
.in-view .stat-2::after {{ animation: countUp2 2.5s cubic-bezier(0.16, 1, 0.3, 1) forwards 0.2s; }}
.in-view .stat-3::after {{ animation: countUp3 2.5s cubic-bezier(0.16, 1, 0.3, 1) forwards 0.4s; }}

/* === Accessibility: Reduce Motion === */
@media (prefers-reduced-motion: reduce) {{
    .stat-1::after {{ animation: none !important; content: "{val1}"; }}
    .stat-2::after {{ animation: none !important; content: "{val2}"; }}
    .stat-3::after {{ animation: none !important; content: "{val3}"; }}
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <header class="header">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </header>
        
        <!-- We use aria-label on the container because screen readers often ignore pseudo-element content -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number stat-1" aria-label="{val1}" role="text"></div>
                <div class="stat-label">Total Users</div>
            </div>
            <div class="stat-card">
                <div class="stat-number stat-2" aria-label="{val2}" role="text"></div>
                <div class="stat-label">Active Projects</div>
            </div>
            <div class="stat-card">
                <div class="stat-number stat-3" aria-label="{val3}" role="text"></div>
                <div class="stat-label">Global Servers</div>
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Intersection Observer to trigger the CSS animation when scrolled into view
document.addEventListener('DOMContentLoaded', () => {{
    const observerOptions = {{
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    }};

    const observer = new IntersectionObserver((entries) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                // Adding the class triggers the CSS @keyframes
                entry.target.classList.add('in-view');
                // Unobserve after animating once
                observer.unobserve(entry.target);
            }}
        }});
    }}, observerOptions);

    const grid = document.querySelector('.stats-grid');
    if (grid) {{
        observer.observe(grid);
    }}
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

#### 3c. Verification Checklist

- [x] Does the code produce valid HTML5 that passes basic validation?
- [x] Does `index.html` work when opened directly in a browser (`file://` protocol)?
- [x] Are all color values explicit hex or rgba?
- [x] Are all external resources loaded from CDN URLs?
- [x] Does the component respect the `width_px` parameter?
- [x] Does `color_scheme="dark"` produce a dark theme and `"light"` a light theme?
- [x] Does the Javascript run without errors and successfully trigger the CSS animation?
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect?

### 4. Accessibility & Performance Notes

* **Accessibility (a11y)**:
  - **Screen Readers**: Content generated via CSS `::after` is inconsistently read by screen readers. Following the tutorial's advice, `aria-label` and `role="text"` attributes are explicitly placed on the `<div>` containing the pseudo-element to ensure assistive technologies announce the final values accurately.
  - **Reduced Motion**: Contains an `@media (prefers-reduced-motion: reduce)` block that strips the animation and immediately displays the final counter value, adhering to user OS-level preferences for accessibility.
* **Performance**:
  - Extremely performant. Moving calculations from the JavaScript main thread to CSS `@property` allows the browser to optimize layout and painting.
  - Applying `font-variant-numeric: tabular-nums` prevents sub-pixel layout thrashing (where the text container expands and contracts rapidly based on the physical width of different numbers like `1` vs `8`).
  - Added a lightweight Intersection Observer via JS to prevent the animation from firing off-screen before the user has scrolled to the metrics.