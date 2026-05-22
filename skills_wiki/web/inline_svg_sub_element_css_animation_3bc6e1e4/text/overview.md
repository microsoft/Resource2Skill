# Inline SVG Sub-element CSS Animation

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Inline SVG Sub-element CSS Animation

* **Core Visual Mechanism**: Embedding scalable vector graphics (SVG) directly into the HTML DOM and animating individual nodes (paths, groups, shapes) using native CSS `@keyframes`. The crucial technique here is applying `transform-box: fill-box` combined with `transform-origin` to ensure that transforms (like rotation and scaling) happen relative to the *individual shape's bounding box*, rather than the global coordinate space of the entire SVG canvas.
* **Why Use This Skill (Rationale)**: SVGs are natively hardware-accelerated, resolution-independent, and incredibly lightweight compared to video or GIF. By animating sub-elements via CSS, you bring static illustrations to life organically without needing heavy external JavaScript libraries (like GSAP or Lottie) or complex `<canvas>` rendering logic.
* **Overall Applicability**: Perfect for hero section illustrations, empty-state graphics, loading indicators, animated logos, and playful micro-interactions on modern landing pages.
* **Value Addition**: Transforms a static graphic into a lively, narrative piece of UI. A spinning wheel and bouncing character immediately draw the user's eye and add a premium, highly-polished feel to the digital experience.
* **Browser Compatibility**: Broadly supported. The `transform-box: fill-box` property is supported in all modern browsers (Chrome 64+, Firefox 55+, Safari 11+, Edge 79+). 

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **HTML Structure**: An inline `<svg>` tag where specific components (wheels, chassis, rider, shadows) are wrapped in `<g>` (group) tags with semantic `id` attributes (e.g., `#left-wheel`).
  - **Color Logic**: Utilizes CSS custom variables mapped to SVG `fill` and `stroke` properties. This makes the entire complex illustration instantly themeable (e.g., switching between dark/light modes).
  - **CSS Properties**: The heavy lifting is done by `animation`, `transform`, `transform-origin`, and `transform-box`.

* **Step B: Layout & Compositional Style**
  - **Spatial Feel**: The SVG uses a custom `viewBox` (e.g., `0 0 600 400`), making the graphic intrinsically responsive—it scales perfectly inside its parent flex/grid container.
  - **Z-Index Layering**: SVG layering is determined strictly by DOM order. Background blobs and shadows are placed at the top of the SVG code, followed by back wheels, the vehicle chassis, the rider, and front-facing elements.

* **Step C: Interactive Behavior & Animations**
  - **Spinning Wheels**: Constant, infinite rotation using a `linear` timing function so there is no start/stop stutter.
  - **Bouncing Chassis**: A smooth vertical translation combined with a slight rotation (`translateY` + `rotateZ`), animated using an `alternate ease-in-out` timing function to mimic suspension and gravity.
  - **Secondary Motion**: An attached element (like an antenna or a hat) animates at a slightly faster frequency than the body to create overlapping action and follow-through, adhering to classical animation principles.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Illustration Structure** | Inline HTML `<svg>` | Exposes internal SVG nodes (paths, groups) directly to the browser's CSS engine. |
| **Component Grouping** | `<g id="...">` tags | Allows specific clusters of vector shapes to be targeted by CSS selectors. |
| **Local Transformations** | CSS `transform-box: fill-box` | **Critical fix:** Forces the `transform-origin` to calculate from the bounding box of the specific `<g>` instead of the 0,0 coordinate of the entire SVG canvas. |
| **Motion & Easing** | CSS `@keyframes` | Native, performant, GPU-accelerated motion without JS overhead. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Let's Get Moving",
    body_text: str = "Bring your static vector illustrations to life using native CSS keyframes and the magic of the transform-box property.",
    color_scheme: str = "light",        
    accent_color: str = "#6366f1",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Inline SVG Sub-element CSS Animation.
    """
    import os
    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_color = "#f8fafc"
        surface_color = "#1e293b"
        shadow_color = "rgba(0, 0, 0, 0.6)"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        surface_color = "#ffffff"
        shadow_color = "rgba(0, 0, 0, 0.08)"

    # === CSS ===
    css = f"""/* Inline SVG Sub-element Animation */
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
    --shadow: {shadow_color};
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
    overflow-x: hidden;
}}

.container {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    padding: 4rem;
    gap: 4rem;
}}

.text-content {{
    flex: 1;
    max-width: 500px;
}}

.title {{
    font-size: 3.5rem;
    font-weight: 800;
    margin-bottom: 1.5rem;
    line-height: 1.1;
    letter-spacing: -0.03em;
}}

.body-text {{
    font-size: 1.25rem;
    opacity: 0.8;
    line-height: 1.6;
}}

.illustration {{
    flex: 1;
    width: 100%;
    max-width: 600px;
}}

.illustration svg {{
    width: 100%;
    height: auto;
    overflow: visible;
}}

/* =========================================
   CORE ANIMATION SKILL 
   ========================================= */

/* The wheels spin infinitely. Linear timing ensures no stuttering. */
#left-wheel, #right-wheel {{
    animation: spin 1s infinite linear;
    transform-origin: center;
    /* CRITICAL: forces origin to the wheel's center, not the SVG's top-left */
    transform-box: fill-box; 
}}

/* The chassis and rider bounce up and down slightly */
#scooter-and-rider {{
    animation: bounce 0.6s infinite alternate ease-in-out;
    transform-origin: bottom;
    transform-box: fill-box;
}}

/* The antenna bobbles at a faster rate to create overlapping action */
#antenna {{
    animation: bobble 0.35s infinite alternate ease-in-out;
    transform-origin: bottom;
    transform-box: fill-box;
}}

/* The floor shadow shrinks slightly as the scooter bounces up */
#floor-shadow {{
    animation: shadow-pulse 0.6s infinite alternate ease-in-out;
    transform-origin: center;
    transform-box: fill-box;
}}

/* Keyframes */
@keyframes spin {{
    from {{ transform: rotateZ(0deg); }}
    to {{ transform: rotateZ(360deg); }}
}}

@keyframes bounce {{
    from {{ transform: translateY(0px) rotateZ(0deg); }}
    to {{ transform: translateY(-10px) rotateZ(-1.5deg); }}
}}

@keyframes bobble {{
    from {{ transform: rotateZ(-12deg); }}
    to {{ transform: rotateZ(18deg); }}
}}

@keyframes shadow-pulse {{
    from {{ transform: scale(1); opacity: 1; }}
    to {{ transform: scale(0.85); opacity: 0.6; }}
}}

/* Responsive behavior */
@media (max-width: 960px) {{
    .container {{
        flex-direction: column;
        justify-content: center;
        text-align: center;
        padding: 2rem;
        height: auto;
    }}
    .title {{ font-size: 2.5rem; }}
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="text-content">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
        
        <div class="illustration">
            <!-- Inline SVG allows CSS to target internal IDs -->
            <svg viewBox="0 0 600 400" xmlns="http://www.w3.org/2000/svg">
                <!-- Decorative Background Blob -->
                <path d="M 120 220 C 80 120, 380 30, 480 130 C 580 230, 480 380, 280 380 C 80 380, 160 320, 120 220 Z" 
                      fill="var(--accent)" opacity="0.15" />

                <!-- Floor Shadow -->
                <ellipse id="floor-shadow" cx="300" cy="340" rx="160" ry="12" fill="var(--shadow)" />

                <!-- Grouping the main body components to animate them together -->
                <g id="scooter-and-rider">
                    
                    <!-- Frame -->
                    <rect x="180" y="270" width="240" height="16" rx="8" fill="var(--text)" />
                    
                    <!-- Steering Column -->
                    <g transform="translate(390, 270) rotate(15) translate(-390, -270)">
                        <rect x="384" y="140" width="12" height="140" rx="6" fill="var(--text)" />
                    </g>
                    
                    <!-- Handlebars -->
                    <rect x="360" y="130" width="50" height="12" rx="6" fill="var(--accent)" />

                    <!-- Rider Body -->
                    <rect x="230" y="150" width="70" height="120" rx="24" fill="var(--surface)" stroke="var(--text)" stroke-width="6" />
                    
                    <!-- Rider Leg -->
                    <path d="M 265 240 L 265 270 L 310 270" fill="none" stroke="var(--text)" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" />
                    
                    <!-- Rider Arm -->
                    <path d="M 265 210 Q 330 210 380 136" fill="none" stroke="var(--text)" stroke-width="12" stroke-linecap="round" />
                    
                    <!-- Rider Head -->
                    <circle cx="265" cy="120" r="35" fill="var(--surface)" stroke="var(--text)" stroke-width="6" />
                    
                    <!-- Visor/Eye -->
                    <rect x="275" y="105" width="25" height="15" rx="7.5" fill="var(--accent)" />
                    
                    <!-- Antenna (Secondary Animation) -->
                    <g id="antenna">
                        <line x1="265" y1="85" x2="265" y2="40" stroke="var(--text)" stroke-width="6" stroke-linecap="round" />
                        <circle cx="265" cy="40" r="14" fill="var(--accent)" />
                    </g>

                </g>

                <!-- Independent Wheels -->
                <g id="left-wheel">
                    <circle cx="180" cy="290" r="45" fill="var(--bg)" stroke="var(--text)" stroke-width="12" />
                    <circle cx="180" cy="290" r="15" fill="var(--accent)" />
                    <line x1="180" y1="245" x2="180" y2="335" stroke="var(--text)" stroke-width="6" />
                    <line x1="135" y1="290" x2="225" y2="290" stroke="var(--text)" stroke-width="6" />
                </g>
                
                <g id="right-wheel">
                    <circle cx="420" cy="290" r="45" fill="var(--bg)" stroke="var(--text)" stroke-width="12" />
                    <circle cx="420" cy="290" r="15" fill="var(--accent)" />
                    <line x1="420" y1="245" x2="420" y2="335" stroke="var(--text)" stroke-width="6" />
                    <line x1="375" y1="290" x2="465" y2="290" stroke="var(--text)" stroke-width="6" />
                </g>
            </svg>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Inline SVG CSS Animations do not require JavaScript!
// The entire logic is handled by CSS Keyframes and `transform-box: fill-box`.
document.addEventListener('DOMContentLoaded', () => {
    console.log("SVG Animation Loaded.");
});
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

* **Accessibility**: Because this is fundamentally a decorative graphic, it's best practice to add `aria-hidden="true"` to the `<svg>` element or provide a `<title>` and `<desc>` element within the SVG for screen readers. Users with vestibular disorders may be sensitive to continuous looping animations. A `prefers-reduced-motion` media query should be implemented in production environments to pause the keyframes:
  ```css
  @media (prefers-reduced-motion: reduce) {
      #left-wheel, #right-wheel, #scooter-and-rider, #antenna, #floor-shadow {
          animation: none !important;
      }
  }
  ```
* **Performance**: Animating SVG transforms (`translate`, `rotate`, `scale`) is hardware accelerated by modern browsers. However, animating complex SVG properties like `d` (paths) or `stroke-dashoffset` can sometimes cause CPU spikes. Because this pattern relies strictly on basic bounding-box transforms (`transform-box`), it remains incredibly performant and fluid even on mobile devices. Ensure `will-change: transform` is used if rendering issues arise on low-end hardware.