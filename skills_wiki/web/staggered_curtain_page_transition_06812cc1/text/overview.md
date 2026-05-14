# Staggered Curtain Page Transition

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Staggered Curtain Page Transition

* **Core Visual Mechanism**: This pattern replaces instant page loads with a theatrical, highly polished transition. Two rows of solid-colored blocks animate vertically (`scaleY`) to obscure the viewport. The top row grows downwards (`transform-origin: top`), and the bottom row grows upwards (`transform-origin: bottom`). By using a staggered delay across the columns, it creates a "zipper" or "closing/opening curtain" effect before revealing the new content.
* **Why Use This Skill (Rationale)**: Native browser route changes can feel jarring, often flashing unstyled text or white screens. A custom transition maintains user immersion, reinforces brand identity through movement and color, and provides perceived performance benefits by giving the user something beautiful to look at while the next view prepares.
* **Overall Applicability**: Ideal for creative portfolios, digital agency sites, premium e-commerce experiences, or any Single Page Application (SPA) where you want to emphasize spatial awareness and fluid movement between distinct sections.
* **Value Addition**: It elevates a standard website into a "digital experience." The motion implies depth and deliberateness, masking the mechanical nature of DOM updates.
* **Browser Compatibility**: Broadly supported. Uses standard CSS Flexbox and Transforms (`scaleY`), which are heavily hardware-accelerated. The JavaScript relies on modern ES6 (Promises, arrow functions) and the GSAP library, meaning it works on all modern browsers (minimum Chrome 60+, Safari 11+, Firefox 55+).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **HTML Structure**: An overlay container (`.transition`) sits on top of the main app content. Inside are two `.transition-row` divs, each containing 5 `.block` divs.
  - **Color Logic**: A strong contrast is required. The tutorial uses a vibrant purple accent (`#746df8`) against a clean background, drawing all attention to the transition geometry.
  - **Typography**: Uses a geometric sans-serif for navigation and a high-contrast serif for the hero titles, enforcing a premium editorial feel.
  - **CSS Properties**: `transform: scaleY()`, `transform-origin`, and `will-change: transform` do the heavy lifting for performance. 

* **Step B: Layout & Compositional Style**
  - **Layout System**: Pure CSS Flexbox. The `.transition` container is absolute/fixed. The rows have `flex: 1` to equally divide the height (50% each). The blocks have `flex: 1` to equally divide the width (20% each). This avoids hardcoded percentages and adapts beautifully to any aspect ratio.
  - **Z-index**: The transition overlay operates on a high `z-index` (e.g., 10) to cover all underlying content (`z-index: 1`).

* **Step C: Interactive Behavior & Animations**
  - **Event Interception**: Click events on navigation links are intercepted (`e.preventDefault()`). 
  - **Animation State Machine**: 
    1. Click triggers `animateTransition()`: Blocks scale `0 -> 1`.
    2. Promise resolves: DOM content updates (simulating navigation).
    3. Triggers `revealTransition()`: Blocks scale `1 -> 0`.
  - **Stagger & Grid Logic**: GSAP's `stagger` property is used with `grid: [2, 5]` and `axis: "x"`. This explicitly tells the animation engine to treat the 10 blocks as a 2x5 grid and sweep across them horizontally, syncing the top and bottom columns perfectly.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Layout Grid** | CSS Flexbox | `flex: 1` auto-calculates equal 50% heights and 20% widths perfectly without math. |
| **Transform Origins** | CSS `transform-origin` | Splitting the origins (`top` for row 1, `bottom` for row 2) natively handles the bidirectional scaling. |
| **Animation Choreography** | GSAP 3 | Handling a 2D staggered delay manually in CSS is extremely tedious. GSAP's `stagger: { grid: [2,5], axis: "x" }` solves it in 4 lines of code. |
| **State/Navigation Handling** | JS Promises | Wrapping the GSAP timelines in Promises allows perfectly timed execution of DOM content swapping mid-transition. |

> **Feasibility Assessment**: 100% reproduction. To make the component purely standalone and testable via `file://`, the code simulates navigating to a new HTML page by intercepting the click, animating the curtain, modifying the DOM text, and revealing the screen—exactly matching the visual flow of a multi-page setup.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "INDEX",
    body_text: str = "",
    color_scheme: str = "light",        
    accent_color: str = "#746df8",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Staggered Curtain Page Transition visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#111111"
        text_color = "#f3f3f0"
    else:
        bg_color = "#f3f3f0"
        text_color = "#111111"

    css = f"""/* Staggered Curtain Page Transition */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    background-color: #000;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    font-family: 'Inter', system-ui, sans-serif;
}}

/* Component Container (acts as the simulated viewport) */
.container {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    background: var(--bg);
    color: var(--text);
    position: relative;
    overflow: hidden;
    container-type: inline-size;
    box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5);
}}

/* Layout Elements */
nav {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    padding: 3cqw 4cqw;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 1;
}}

.logo {{
    font-weight: 700;
    font-size: 1.25rem;
    letter-spacing: -0.02em;
}}

.nav-items {{
    display: flex;
    gap: 3rem;
}}

.nav-items a {{
    text-decoration: none;
    color: var(--text);
    font-weight: 500;
    font-size: 0.95rem;
    transition: opacity 0.2s ease;
}}

.nav-items a:hover {{
    opacity: 0.5;
}}

.hero {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    width: 100%;
}}

.hero h1 {{
    font-family: 'Playfair Display', serif;
    font-size: 14cqw;
    line-height: 0.9;
    letter-spacing: -0.02em;
    font-weight: 600;
}}

/* Transition Effect Overlay */
.transition {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    z-index: 10;
    pointer-events: none; /* Allows clicking underlying nav when hidden */
}}

.transition-row {{
    flex: 1;
    display: flex;
}}

.block {{
    flex: 1;
    background-color: var(--accent);
    transform: scaleY(1); /* Blocks cover screen initially */
    will-change: transform;
}}

.row-1 .block {{
    transform-origin: top;
}}

.row-2 .block {{
    transform-origin: bottom;
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&family=Playfair+Display:ital,wght@0,600;1,600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
    <!-- Load GSAP for advanced staggering -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
</head>
<body>
    <div class="container">
        
        <!-- Main App Content -->
        <main class="app">
            <nav>
                <div class="logo">Codegrid</div>
                <div class="nav-items">
                    <a href="#" data-target="INDEX">Home</a>
                    <a href="#" data-target="ABOUT">About</a>
                    <a href="#" data-target="CONTACT">Contact</a>
                </div>
            </nav>
            <div class="hero" aria-live="polite">
                <h1 id="page-title">{title_text}</h1>
            </div>
        </main>

        <!-- Transition Overlay -->
        <div class="transition" aria-hidden="true">
            <div class="transition-row row-1">
                <div class="block"></div><div class="block"></div><div class="block"></div><div class="block"></div><div class="block"></div>
            </div>
            <div class="transition-row row-2">
                <div class="block"></div><div class="block"></div><div class="block"></div><div class="block"></div><div class="block"></div>
            </div>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Staggered Curtain Page Transition Logic
document.addEventListener('DOMContentLoaded', () => {{
    
    // 1. Trigger the opening reveal animation on page load
    revealTransition();

    // 2. Intercept navigation links
    document.querySelectorAll('.nav-items a').forEach(link => {{
        link.addEventListener('click', (e) => {{
            e.preventDefault();
            const targetTitle = e.currentTarget.getAttribute('data-target');
            const currentTitle = document.getElementById('page-title').textContent;
            
            // Only animate if navigating to a different page
            if (targetTitle !== currentTitle) {{
                
                // Close the curtain
                animateTransition().then(() => {{
                    
                    // --- SIMULATED ROUTING ---
                    // Replace this block with actual window.location.href changes in a real MPA
                    document.getElementById('page-title').textContent = targetTitle;
                    
                    // Open the curtain to reveal new content
                    revealTransition();
                }});
            }}
        }});
    }});
}});

/**
 * Animates blocks from scaleY: 0 to scaleY: 1 (Closing the curtain)
 * Returns a Promise that resolves when animation finishes
 */
function animateTransition() {{
    return new Promise((resolve) => {{
        gsap.set('.block', {{ visibility: 'visible', scaleY: 0 }});
        gsap.to('.block', {{
            scaleY: 1,
            duration: 1,
            stagger: {{
                each: 0.1,
                from: 'start',
                grid: [2, 5], // Tells GSAP this is a 2-row, 5-column layout
                axis: 'x'     // Stagger horizontally across columns
            }},
            ease: 'power4.inOut',
            onComplete: resolve
        }});
    }});
}}

/**
 * Animates blocks from scaleY: 1 to scaleY: 0 (Opening the curtain)
 * Returns a Promise that resolves when animation finishes
 */
function revealTransition() {{
    return new Promise((resolve) => {{
        gsap.set('.block', {{ scaleY: 1 }});
        gsap.to('.block', {{
            scaleY: 0,
            duration: 1,
            stagger: {{
                each: 0.1,
                from: 'start',
                grid: [2, 5], 
                axis: 'x'
            }},
            ease: 'power4.inOut',
            onComplete: () => {{
                // Hide to ensure they don't block pointer events accidentally
                gsap.set('.block', {{ visibility: 'hidden' }}); 
                resolve();
            }}
        }});
    }});
}}
"""

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
  * The `.transition` element acts entirely as a visual flair, so `aria-hidden="true"` is applied to prevent screen readers from announcing empty blocks.
  * In the SPA simulation, the `.hero` container includes `aria-live="polite"` so that when the text is swapped out dynamically, screen readers announce the new page title.
  * *Enhancement Note*: For production use, checking `window.matchMedia('(prefers-reduced-motion: reduce)').matches` and bypassing the GSAP animation (resolving the Promise immediately) is recommended for vestibular accessibility.
* **Performance**: 
  * CSS applies `will-change: transform` to the `.block` elements. Because we are animating `scaleY` instead of `height`, we completely avoid triggering browser Layout/Reflow recalculations. The GPU handles the scaling natively.
  * Keeping `pointer-events: none` on the transition layer is critical so users can actually interact with the page once the blocks are hidden.