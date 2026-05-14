# Scroll-Activated Statistics Grid

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Scroll-Activated Statistics Grid

* **Core Visual Mechanism**: A solid-color, full-width banner containing a grid of statistics. As the banner scrolls into the viewport, the numbers dynamically count up from zero to their target values. The items are separated by clean, minimal CSS pseudo-element divider lines that adapt their orientation (vertical to horizontal) based on screen size.
* **Why Use This Skill (Rationale)**: Animated numbers draw the user's eye and create a sense of momentum and scale. Instead of presenting static numbers (which users might skim over), the animation forces a brief moment of engagement, emphasizing the magnitude of the achievements or data being presented.
* **Overall Applicability**: Perfect for "About Us" pages, SaaS landing pages (e.g., highlighting user count, uptime percentage, or money saved), portfolio sites (e.g., projects completed, lines of code), or annual reports. 
* **Value Addition**: It transforms static text into a micro-interaction. The use of CSS Grid combined with dynamic pseudo-elements ensures the UI remains pristine across devices without cluttering the DOM with extra `<hr>` tags or divider `<div>`s.
* **Browser Compatibility**: Uses CSS Grid and modern JavaScript (`IntersectionObserver`). Fully supported in all modern browsers (Edge, Chrome, Firefox, Safari).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Containers**: A full-width wrapper (`background-color`), a constrained inner container (`max-width: 900px`), and individual counter blocks.
  - **Typography**: Large, bold primary numbers (often 3em+ in size), sometimes accompanied by suffixes (`+`, `%`). Smaller, muted or lighter-weight labels underneath (1em size).
  - **Color Logic**: A high-contrast split. The background is typically a vivid brand color (e.g., bright blue `#4193ff`), with pure white (`#ffffff`) text and dividers to maximize legibility.
  - **Dividers**: Created using CSS `::before` or `::after` pseudo-elements.

* **Step B: Layout & Compositional Style**
  - **Desktop Layout**: 4-column CSS Grid (`grid-template-columns: repeat(4, 1fr)`). Gap ensures spacing. Vertical dividers run between columns.
  - **Tablet Layout**: 2-column Grid. The vertical divider on the 2nd item is hidden so it doesn't bleed into the margin.
  - **Mobile Layout**: 1-column Grid. Dividers rotate 90 degrees to become horizontal separators between rows.
  - **Alignment**: Text is centered (`text-align: center`) within each grid cell.

* **Step C: Interactive Behavior & Animations**
  - **Trigger Mechanism**: An `IntersectionObserver` detects when the container enters the viewport. This is far more performant than the traditional `window.addEventListener('scroll')` used in older tutorials.
  - **Animation Logic**: A JavaScript loop (using `requestAnimationFrame` or `setTimeout`) continuously increments the DOM node's `innerText` until it matches the `data-target` attribute.
  - **Reset Behavior**: When the user scrolls back up past the element, the numbers reset to 0, allowing the animation to replay on subsequent downward scrolls.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Scroll Detection** | JS `IntersectionObserver` | Modern, performant native API. Replaces the tutorial's janky scroll event listener and manual `offsetTop` math. |
| **Number Animation** | JS `requestAnimationFrame` | Provides a smoother 60FPS count-up animation compared to `setTimeout`, avoiding main thread blocking. |
| **Responsive Dividers** | CSS `:not(:last-child)::after` | Keeps the HTML clean. Modifying `content`, `width`, and `height` inside media queries perfectly handles the vertical-to-horizontal shift. |
| **Grid Layout** | CSS Grid | Native `repeat()` and `gap` make the 4-col to 2-col to 1-col transitions trivial. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Our Company Impact",
    body_text: str = "Scroll down to see the live metrics.",
    color_scheme: str = "light",        
    accent_color: str = "#4193ff",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Scroll-Activated Statistics Grid.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        page_bg = "#0d111c"
        page_text = "#f0f0f0"
    else:
        page_bg = "#f8f9fa"
        page_text = "#1a1a2e"

    css = f"""/* Scroll-Activated Statistics Grid */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --page-bg: {page_bg};
    --page-text: {page_text};
    --accent: {accent_color};
    --text-on-accent: #ffffff;
    --divider-color: rgba(255, 255, 255, 0.6);
    --max-width: 900px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--page-bg);
    color: var(--page-text);
    min-height: 100vh;
    overflow-x: hidden;
}}

/* Spacer to allow scrolling to the element */
.hero-spacer {{
    height: 80vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
}}

.hero-spacer h1 {{
    font-size: 2.5rem;
    margin-bottom: 1rem;
}}

.hero-spacer p {{
    font-size: 1.1rem;
    opacity: 0.7;
}}

/* Banner Container */
.stats-banner {{
    background-color: var(--accent);
    color: var(--text-on-accent);
    padding: 4rem 2rem;
    width: 100%;
}}

/* Grid Layout */
.stats-grid {{
    max-width: var(--max-width);
    margin: 0 auto;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 3rem 2rem;
}}

.stat-item {{
    text-align: center;
    position: relative;
}}

/* Typography */
.stat-value-container {{
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    line-height: 1;
    display: flex;
    justify-content: center;
    align-items: baseline;
}}

.stat-label {{
    font-size: 1rem;
    font-weight: 500;
    opacity: 0.9;
    letter-spacing: 0.5px;
}}

/* Vertical Dividers */
.stat-item:not(:last-child)::after {{
    content: '';
    position: absolute;
    right: -1rem; /* Half of grid gap */
    top: 50%;
    transform: translateY(-50%);
    width: 2px;
    height: 80%;
    background-color: var(--divider-color);
}}

/* Tablet Breakpoint (2 Columns) */
@media (max-width: 900px) {{
    .stats-grid {{
        grid-template-columns: repeat(2, 1fr);
        gap: 4rem 2rem;
    }}
    
    /* Remove vertical divider from the 2nd item (end of row 1) */
    .stat-item:nth-child(2)::after {{
        display: none;
    }}
    
    /* Add horizontal divider below row 1 */
    .stat-item:nth-child(1)::before,
    .stat-item:nth-child(2)::before {{
        content: '';
        position: absolute;
        bottom: -2rem; /* Half of row gap */
        left: 50%;
        transform: translateX(-50%);
        width: 80%;
        height: 2px;
        background-color: var(--divider-color);
    }}
}}

/* Mobile Breakpoint (1 Column) */
@media (max-width: 600px) {{
    .stats-grid {{
        grid-template-columns: 1fr;
        gap: 4rem;
    }}
    
    /* Remove all vertical dividers */
    .stat-item::after {{
        display: none !important;
    }}
    
    /* Turn all dividers (except last) into horizontal lines */
    .stat-item:not(:last-child)::before {{
        content: '';
        position: absolute;
        bottom: -2rem;
        left: 50%;
        transform: translateX(-50%);
        width: 60px; /* Short horizontal line */
        height: 2px;
        background-color: var(--divider-color);
    }}
}}
"""

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
    
    <div class="hero-spacer">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
        <p style="margin-top: 2rem;">↓</p>
    </div>

    <!-- Scroll Activated Stats Banner -->
    <section class="stats-banner" id="stats-section">
        <div class="stats-grid">
            
            <div class="stat-item">
                <div class="stat-value-container">
                    <span class="count-up" data-target="156">0</span>
                </div>
                <p class="stat-label">Projects Completed</p>
            </div>
            
            <div class="stat-item">
                <div class="stat-value-container">
                    <span class="count-up" data-target="227">0</span>
                </div>
                <p class="stat-label">Satisfied Clients</p>
            </div>
            
            <div class="stat-item">
                <div class="stat-value-container">
                    <span class="count-up" data-target="91">0</span>
                    <span class="suffix">%</span>
                </div>
                <p class="stat-label">Success Rate</p>
            </div>
            
            <div class="stat-item">
                <div class="stat-value-container">
                    <span class="count-up" data-target="30">0</span>
                    <span class="suffix">+</span>
                </div>
                <p class="stat-label">Years Experience</p>
            </div>

        </div>
    </section>

    <!-- Bottom spacer so we can scroll past it and trigger resets -->
    <div style="height: 100vh;"></div>

    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Scroll-Activated Counter Logic
document.addEventListener('DOMContentLoaded', () => {{
    const statsSection = document.getElementById('stats-section');
    const counters = document.querySelectorAll('.count-up');
    let activated = false;

    // Easing function for smooth slowdown at the end of the count
    const easeOutQuad = (t) => t * (2 - t);
    const animationDuration = 2000; // 2 seconds

    const runAnimations = () => {{
        counters.forEach(counter => {{
            const target = parseInt(counter.getAttribute('data-target'), 10);
            let startTime = null;

            const step = (currentTime) => {{
                if (!startTime) startTime = currentTime;
                const progress = Math.min((currentTime - startTime) / animationDuration, 1);
                
                // Calculate current value based on easing
                const easedProgress = easeOutQuad(progress);
                const currentValue = Math.floor(easedProgress * target);
                
                counter.innerText = currentValue;

                if (progress < 1) {{
                    requestAnimationFrame(step);
                }} else {{
                    counter.innerText = target; // Ensure exact final value
                }}
            }};
            
            requestAnimationFrame(step);
        }});
    }};

    const resetAnimations = () => {{
        counters.forEach(counter => {{
            counter.innerText = '0';
        }});
    }};

    // Use Intersection Observer to detect scroll position
    const observer = new IntersectionObserver((entries) => {{
        const entry = entries[0];
        
        if (entry.isIntersecting && !activated) {{
            // Scrolled into view
            activated = true;
            runAnimations();
        }} else if (!entry.isIntersecting && entry.boundingClientRect.top > 0 && activated) {{
            // Scrolled back up past the container
            activated = false;
            resetAnimations();
        }}
    }}, {{
        threshold: 0.2 // Trigger when 20% of the banner is visible
    }});

    if (statsSection) {{
        observer.observe(statsSection);
    }}
}});
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
  * The changing numbers can be problematic for screen readers, as they might attempt to announce every increment. A best practice (not strictly in the video, but important) would be to add `aria-hidden="true"` to the animating `span`, and provide a visually hidden `.sr-only` span that contains the final target value so screen readers just read the final correct number immediately.
  * Contrast ratio between the accent banner (blue) and the white text exceeds WCAG AA standards.
* **Performance**:
  * **Intersection Observer**: By using `IntersectionObserver`, we avoid the performance penalty of firing a function on every single `scroll` event.
  * **requestAnimationFrame**: The JS loop in this reproduced code uses `requestAnimationFrame` instead of `setTimeout(fn, 10)` (which was used in the video). `requestAnimationFrame` aligns with the browser's display refresh rate (usually 60fps) and prevents visual tearing and unnecessary CPU usage when the tab is inactive.
  * **Hardware Acceleration**: The grid layout and CSS divider lines are painted efficiently without triggering continuous browser reflows.