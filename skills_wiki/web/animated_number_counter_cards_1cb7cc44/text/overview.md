# Animated Number Counter Cards

## Analysis

# High-level Design Pattern Extraction

> **Skill Name**: Animated Number Counter Cards

* **Core Visual Mechanism**: A row of elegant, stylized cards displaying statistics. Each card features an icon, a label, and a number that dynamically counts up from zero to its target value when rendered. The cards are unified by a distinct accent color applied to the icons and a thick bottom border, contrasting against a dark or muted background.
* **Why Use This Skill (Rationale)**: Static numbers often fail to convey the scale or impact of achievements. Animating numbers upward draws the user's eye and builds a subtle sense of momentum and success. Framing these numbers inside dedicated, elevated cards gives the data visual importance and separation from surrounding text.
* **Overall Applicability**: Ideal for "About Us" sections, SaaS landing pages showing usage metrics, portfolio sites displaying completed projects, or any scenario where quantitative proof (e.g., "Meals Delivered," "Happy Customers") is a key selling point. 
* **Value Addition**: Transforms plain text statistics into an engaging micro-interaction. The inclusion of an `IntersectionObserver` in the robust version ensures the animation only plays when the user actually scrolls down to see it, maximizing the impact.
* **Browser Compatibility**: Broadly supported. Uses standard Flexbox/Grid for layout, native CSS variables, and the `requestAnimationFrame` and `IntersectionObserver` JavaScript APIs, all of which are fully supported in all modern browsers.

---

# Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Containers**: Simple `<div>` elements acting as cards with soft border radii and subtle drop shadows.
  - **Color Logic**: High contrast is key. The original uses a deep background (`#121317`), slightly lighter card surfaces (`#21242b`), pure white numbers for emphasis, and a bright neon accent (`#18f98f`) for icons and structural borders.
  - **Typography**: Uses *Poppins*, a geometric sans-serif font. The numbers are weighted heavier (`600`) and sized much larger (`2.5em`) than the descriptive text (`400`, `1em`) to establish a clear visual hierarchy.
  - **Icons**: Font Awesome icons sized to match the typography weight, colored using the accent color.

* **Step B: Layout & Compositional Style**
  - **Layout System**: CSS Flexbox is used to distribute the cards evenly. `flex-wrap: wrap` and `min-width` properties ensure the layout collapses gracefully into a column on mobile devices.
  - **Alignment**: Everything inside the cards is center-aligned (`align-items: center`, `text-align: center`), creating a balanced, symmetrical feel.
  - **Accents**: The bottom border (`border-bottom: 6px solid var(--accent)`) grounds the card visually and provides an anchor point for the eye.

* **Step C: Interactive Behavior & Animations**
  - **Count-Up Animation**: JavaScript interpolates the value from `0` to the target `data-val`. The original video uses a simple `setInterval`, but a much more robust approach uses `requestAnimationFrame` with an easing function to ensure smooth 60FPS performance and a natural deceleration as the number reaches its target.
  - **Hover Effects**: A subtle CSS transform (`translateY(-5px)`) provides tactile feedback when the user mouses over the cards.

---

# Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Layout & Responsiveness** | CSS Flexbox | Provides flexible, auto-wrapping distribution for the card row without complex media queries. |
| **Icons** | Font Awesome CDN | Easiest way to drop consistent, scalable vector icons into the layout. |
| **Count-up Animation** | JS `requestAnimationFrame` | Much smoother and more performant than the video's `setInterval` approach. Allows for custom easing (slowing down at the end) and guarantees completion regardless of frame rate. |
| **Animation Trigger** | JS `IntersectionObserver` | An enhancement over the tutorial: ensures the numbers only start counting when the user scrolls them into view, rather than firing instantly on page load. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Our Impact in Numbers",
    body_text: str = "See how we're making a difference every single day.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#18f98f",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Animated Number Counter Cards.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#121317"
        surface_color = "#21242b"
        text_primary = "#ffffff"
        text_secondary = "#e0e0e0"
        shadow = "rgba(0, 0, 0, 0.4)"
    else:
        bg_color = "#f3f4f6"
        surface_color = "#ffffff"
        text_primary = "#111827"
        text_secondary = "#4b5563"
        shadow = "rgba(0, 0, 0, 0.08)"

    # === CSS ===
    css = f"""/* Animated Number Counter Cards */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --surface-color: {surface_color};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --accent-color: {accent_color};
    --shadow: {shadow};
}}

body {{
    font-family: 'Poppins', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

.section-container {{
    max-width: {width_px}px;
    width: 100%;
    text-align: center;
}}

.header {{
    margin-bottom: 3rem;
}}

.header h1 {{
    font-size: 2.5rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}}

.header p {{
    font-size: 1.1rem;
    color: var(--text-secondary);
}}

.stats-wrapper {{
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 2rem;
    width: 100%;
}}

.stat-card {{
    background-color: var(--surface-color);
    flex: 1;
    min-width: 240px;
    max-width: 300px;
    padding: 2.5rem 1.5rem;
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border-bottom: 8px solid var(--accent-color);
    box-shadow: 0 10px 30px var(--shadow);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}}

.stat-card:hover {{
    transform: translateY(-8px);
    box-shadow: 0 15px 40px var(--shadow);
}}

.stat-icon {{
    font-size: 2.8rem;
    color: var(--accent-color);
    margin-bottom: 1rem;
}}

.stat-num {{
    font-size: 3rem;
    font-weight: 600;
    color: var(--text-primary);
    line-height: 1.2;
    margin-bottom: 0.25rem;
}}

.stat-text {{
    font-size: 1.05rem;
    color: var(--text-secondary);
    font-weight: 400;
}}

/* Responsive Adjustments */
@media screen and (max-width: 768px) {{
    .stats-wrapper {{
        gap: 1.5rem;
    }}
    .stat-card {{
        min-width: calc(50% - 1.5rem);
    }}
}}

@media screen and (max-width: 480px) {{
    .stat-card {{
        min-width: 100%;
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
    <!-- Font Awesome for Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="section-container">
        <div class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </div>

        <div class="stats-wrapper">
            <!-- Card 1 -->
            <div class="stat-card">
                <i class="fas fa-utensils stat-icon"></i>
                <span class="stat-num" data-val="400">0</span>
                <span class="stat-text">Meals Delivered</span>
            </div>
            
            <!-- Card 2 -->
            <div class="stat-card">
                <i class="fas fa-smile-beam stat-icon"></i>
                <span class="stat-num" data-val="340">0</span>
                <span class="stat-text">Happy Customers</span>
            </div>
            
            <!-- Card 3 -->
            <div class="stat-card">
                <i class="fas fa-list stat-icon"></i>
                <span class="stat-num" data-val="225">0</span>
                <span class="stat-text">Menu Items</span>
            </div>
            
            <!-- Card 4 -->
            <div class="stat-card">
                <i class="fas fa-star stat-icon"></i>
                <span class="stat-num" data-val="280">0</span>
                <span class="stat-text">Five Stars</span>
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Animated Number Counter Logic
document.addEventListener('DOMContentLoaded', () => {{
    const valueDisplays = document.querySelectorAll('.stat-num');
    const animationDuration = 2500; // Total animation time in ms

    // Easing function for smoother deceleration at the end
    // easeOutQuart
    const easeOut = (t) => 1 - Math.pow(1 - t, 4);

    const animateValue = (el) => {{
        const endValue = parseInt(el.getAttribute('data-val'), 10);
        let startTimestamp = null;

        const step = (timestamp) => {{
            if (!startTimestamp) startTimestamp = timestamp;
            
            // Calculate progress between 0 and 1
            const progress = Math.min((timestamp - startTimestamp) / animationDuration, 1);
            
            // Apply easing
            const easedProgress = easeOut(progress);
            
            // Calculate current value and update DOM
            const currentValue = Math.floor(easedProgress * endValue);
            el.textContent = currentValue;
            
            // Continue animation if not reached 100%
            if (progress < 1) {{
                window.requestAnimationFrame(step);
            }} else {{
                el.textContent = endValue; // Ensure exact final value is set
            }}
        }};
        
        window.requestAnimationFrame(step);
    }};

    // Use Intersection Observer to only start animations when cards scroll into view
    const observerOptions = {{
        root: null,
        rootMargin: '0px',
        threshold: 0.3 // Trigger when 30% of the card is visible
    }};

    const observer = new IntersectionObserver((entries, observer) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                animateValue(entry.target);
                // Unobserve so it only animates once per page load
                observer.unobserve(entry.target);
            }}
        }});
    }}, observerOptions);

    // Attach observer to all number elements
    valueDisplays.forEach(display => {{
        observer.observe(display);
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