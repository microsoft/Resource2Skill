# State-Driven SPA Page Transitions (Swup-style)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: State-Driven SPA Page Transitions (Swup-style)

* **Core Visual Mechanism**: This pattern replaces the harsh, blinking reload of standard web navigation with a smooth, app-like visual transition. It uses JavaScript to intercept link clicks and toggle specific CSS "lifecycle" classes (e.g., `is-animating`, `is-leaving`) on the root HTML element. CSS transitions handle the actual visual morphing (fading out, sliding off-screen), after which the DOM content is swapped, and the classes are removed to trigger the entry animation.
* **Why Use This Skill (Rationale)**: Native applications never flash a white screen when moving between views; they slide, fade, and scale. This technique bridges the gap between traditional websites and Single Page Applications (SPAs), maintaining user context, preserving persistent UI elements (like headers and sidebars), and drastically improving perceived performance.
* **Overall Applicability**: Perfect for marketing websites, portfolios, documentation sites, and SaaS dashboards where a premium, highly polished navigation experience is desired without the overhead of a heavy frontend framework like React or Vue. 
* **Browser Compatibility**: Broadly compatible with all modern browsers. It relies on standard CSS transitions, CSS transforms, and basic DOM manipulation.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Containers**: A persistent `<header>`/`<nav>` and a dynamic `<main>` container where content is swapped.
  - **Color Logic**: A high-contrast aesthetic (e.g., dark theme: `#0d111c` background, `#f0f0f0` text, and a vibrant `#00bfff` accent) helps emphasize the motion of the content block. 
  - **CSS Properties**: The heavy lifting is done via `transition`, `opacity`, and `transform: translate()`.

* **Step B: Layout & Compositional Style**
  - Uses a fixed layout shell where only the inner content region updates. This provides a visual anchor for the user while the content morphs.
  - By manipulating `transform-origin` or combining `translateX/Y`, different elements can express unique personalities (e.g., content fades to the left, while special buttons swipe up).

* **Step C: Interactive Behavior & Animations**
  - **The State Machine**: 
    1. User clicks a link.
    2. Add `.is-animating` and `.is-leaving` to `<html>`. (Content fades/slides out).
    3. Wait for the transition duration (e.g., 500ms).
    4. Replace the DOM content.
    5. Remove `.is-leaving`. (Content is prepped in its "start" position).
    6. Wait one animation frame, then remove `.is-animating`. (Content smoothly animates into place).
  - **Timing**: `500ms cubic-bezier(0.4, 0, 0.2, 1)` provides a snappy but smooth acceleration curve.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Animation States** | Pure CSS classes | Offloads animation to the GPU; easily configurable via `is-animating` and `is-leaving` hooks. |
| **Routing / Content Swap** | Vanilla JS (Virtual Router) | The tutorial uses `swup.js`, which relies on the `fetch` API. Fetching local files triggers CORS errors when opened via the `file://` protocol. To strictly satisfy the **"must be viewable by simply opening the file in a browser"** requirement, I implemented a lightweight virtual router in JS that perfectly mimics Swup's CSS state-machine logic without needing a local web server. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Smooth Transitions",
    body_text: str = "Click the navigation links above to see the page transition effect without a hard browser reload. This mimics modern SPA routing.",
    color_scheme: str = "dark",
    accent_color: str = "#00bfff",
    width_px: int = 1000,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the SPA Page Transition visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
        surface_color = "#161b26"
        border_color = "rgba(255, 255, 255, 0.08)"
    else:
        bg_color = "#e9ecef"
        text_color = "#1a1a2e"
        surface_color = "#ffffff"
        border_color = "rgba(0, 0, 0, 0.08)"

    # === CSS ===
    css = f"""/* Smooth SPA Transitions */
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
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.app-container {{
    width: {width_px}px;
    height: {height_px}px;
    background: var(--surface);
    border-radius: 12px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    border: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    overflow: hidden;
}}

/* -- Header & Nav -- */
header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem 2.5rem;
    border-bottom: 1px solid var(--border);
}}

.logo {{
    font-weight: 700;
    font-size: 1.25rem;
    letter-spacing: -0.5px;
}}

.logo span {{
    color: var(--accent);
}}

nav {{
    display: flex;
    gap: 2rem;
}}

nav a {{
    color: var(--text);
    text-decoration: none;
    font-weight: 500;
    font-size: 0.95rem;
    opacity: 0.7;
    transition: opacity 0.2s, color 0.2s;
}}

nav a:hover {{
    opacity: 1;
}}

nav a.active {{
    opacity: 1;
    color: var(--accent);
}}

/* -- Main Content Area -- */
main {{
    padding: 3rem 2.5rem;
    flex: 1;
    display: flex;
    flex-direction: column;
}}

.title {{
    font-size: 2.5rem;
    margin-bottom: 1rem;
    font-weight: 600;
    letter-spacing: -1px;
}}

.body-text {{
    font-size: 1.1rem;
    line-height: 1.6;
    opacity: 0.8;
    max-width: 600px;
}}

.btn {{
    align-self: flex-start;
    margin-top: 2rem;
    padding: 0.8rem 1.5rem;
    background: var(--accent);
    color: #fff;
    border: none;
    border-radius: 6px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}}

/* =========================================
   CORE SKILL: TRANSITION LIFECYCLE HOOKS
   ========================================= */

/* Default State (Entered / Idle) */
.transition-fade {{
    transition: all 500ms cubic-bezier(0.4, 0, 0.2, 1);
    opacity: 1;
    transform: translateX(0);
}}

/* Entry State (Animating IN from the right) */
html.is-animating .transition-fade {{
    opacity: 0;
    transform: translateX(40px);
}}

/* Exit State (Animating OUT to the left) */
html.is-animating.is-leaving .transition-fade {{
    opacity: 0;
    transform: translateX(-40px);
}}


/* Alternate element-specific animation (Swipe) */
.transition-swipe {{
    transition: all 500ms cubic-bezier(0.4, 0, 0.2, 1);
    opacity: 1;
    transform: translateY(0);
}}

html.is-animating .transition-swipe {{
    opacity: 0;
    transform: translateY(40px); /* Enters from bottom */
}}

html.is-animating.is-leaving .transition-swipe {{
    opacity: 0;
    transform: translateY(-40px); /* Leaves to top */
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
</head>
<body>
    <div class="app-container">
        <header>
            <div class="logo">SPA<span>Motion</span></div>
            <nav>
                <a href="#" data-target="home" class="active">Home</a>
                <a href="#" data-target="pricing">Pricing</a>
                <a href="#" data-target="about">About</a>
            </nav>
        </header>
        
        <!-- The container that gets swapped and animated -->
        <main id="swup">
            <div class="transition-fade">
                <h1 class="title">{title_text}</h1>
                <p class="body-text">{body_text}</p>
            </div>
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Virtual Pages Data (Simulating server HTML responses)
const pages = {{
    'home': `
        <div class="transition-fade">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
    `,
    'pricing': `
        <div class="transition-fade">
            <h1 class="title">Flexible Pricing</h1>
            <p class="body-text">We offer multiple tiers for different needs. Notice how this text fades and slides in smoothly.</p>
        </div>
        <button class="btn transition-swipe">Purchase Now</button>
    `,
    'about': `
        <div class="transition-fade">
            <h1 class="title">About This Effect</h1>
            <p class="body-text">This simulates the Swup.js lifecycle. Elements are assigned lifecycle classes (is-animating, is-leaving) to trigger CSS-based entry and exit states.</p>
        </div>
    `
}};

document.addEventListener('DOMContentLoaded', () => {{
    const navLinks = document.querySelectorAll('nav a');
    const mainContainer = document.getElementById('swup');
    let isNavigating = false;

    navLinks.forEach(link => {{
        link.addEventListener('click', (e) => {{
            e.preventDefault();
            if (isNavigating) return; // Prevent spam clicking

            const target = e.target.getAttribute('data-target');
            if (!pages[target]) return;

            isNavigating = true;

            // Update Nav Active State
            navLinks.forEach(l => l.classList.remove('active'));
            e.target.classList.add('active');

            const html = document.documentElement;
            
            // 1. Start Leave Animation
            html.classList.add('is-animating', 'is-leaving');
            
            // 2. Wait for exit transition to complete (500ms matches CSS)
            setTimeout(() => {{
                
                // 3. Swap the DOM content
                mainContainer.innerHTML = pages[target];
                
                // 4. Remove 'is-leaving' to prep elements in their Entry start state
                html.classList.remove('is-leaving');
                
                // 5. Force a reflow so the browser registers the start state
                requestAnimationFrame(() => {{
                    requestAnimationFrame(() => {{
                        
                        // 6. Remove 'is-animating' to trigger the Entry transition
                        html.classList.remove('is-animating');
                        
                        // Unlock routing after entry finishes
                        setTimeout(() => {{
                            isNavigating = false;
                        }}, 500);

                    }});
                }});

            }}, 500); 
        }});
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

#### 3c. Verification Checklist

- [x] Does the code produce valid HTML5 that passes basic validation?
- [x] Does `index.html` work when opened directly in a browser (`file://` protocol)? *(Yes, virtual router avoids CORS)*
- [x] Are all color values explicit hex or rgba?
- [x] Does the component respect the `width_px` and `height_px` parameters?
- [x] Does the JavaScript run without console errors?
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect? *(Yes, identical visual physics to Swup.js)*

### 4. Accessibility & Performance Notes

* **Accessibility**: 
  - For production, if mimicking SPA routing, you must manually manage browser focus. When new content loads, focus should be programmatically moved to the newly injected `<h1>` (which should have `tabindex="-1"`) so screen readers announce the page change.
  - Adding `@media (prefers-reduced-motion: reduce)` to override the `.transition-fade` with `transition: none` is recommended for users who experience motion sickness.
* **Performance**: 
  - CSS transforms (`translateX/Y`) and `opacity` are used exclusively, avoiding layout recalculations during the animation sequence and ensuring hardware acceleration (60fps).
  - The JS script utilizes a boolean lock (`isNavigating`) to safely discard rapid, spammy clicks that would otherwise break the state machine timings.