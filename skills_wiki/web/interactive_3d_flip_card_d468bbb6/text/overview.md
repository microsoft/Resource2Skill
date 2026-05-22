# Interactive 3D Flip Card

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Interactive 3D Flip Card

* **Core Visual Mechanism**: A two-sided card that flips along the Y-axis when hovered, simulating a physical 3D object. The effect is achieved using CSS 3D transforms (`rotateY` and `perspective`), combined with `backface-visibility: hidden` to seamlessly swap the front and back faces mid-rotation. 
* **Why Use This Skill (Rationale)**: This interaction provides a highly satisfying tactile experience. It allows for high information density in a constrained layout—perfect for progressive disclosure, where a clean visual hook (the front) gives way to dense technical details or actions (the back) only when the user expresses interest.
* **Overall Applicability**: E-commerce product showcases (image on front, specs and "Buy" button on back), team member directory grids (photo on front, bio on back), pricing tables, and interactive flashcards.
* **Value Addition**: It transforms a static block of information into an engaging micro-interaction, saving screen real estate while maintaining a clean initial aesthetic.
* **Browser Compatibility**: Fully supported in all modern browsers. Uses standard CSS 3D transforms. 


### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **HTML Structure**: A parent wrapper, containing two sibling `div` elements representing the front and back faces.
  - **Color Logic**: Uses a neutral surface color for the cards (e.g., `#ffffff` for light theme or `#1e1e1e` for dark theme) against a contrasting background to make the card geometry pop. An accent color is used for calls-to-action on the back face.
  - **Typography**: Clean sans-serif hierarchy. The front prioritizes visuals (large image/icon), while the back uses a structured list for specifications and bold typography for pricing.
  - **Key CSS Properties**: `transform: perspective(...) rotateY(...)`, `backface-visibility: hidden`, `position: absolute`.

* **Step B: Layout & Compositional Style**
  - **Layering**: The front and back faces are layered directly on top of each other using `position: absolute; top: 0; left: 0; width: 100%; height: 100%;`.
  - **Internal Alignment**: Both faces utilize CSS Flexbox (`display: flex; flex-direction: column; align-items: center; justify-content: center;`) to perfectly center the internal content regardless of card dimensions.
  - **Proportions**: Fixed aspect ratio logic (e.g., 300px by 400px), with content spaced out evenly.

* **Step C: Interactive Behavior & Animations**
  - **The Animation**: The flip is driven entirely by CSS `:hover` states triggering a transition. 
  - **Transform Arc**:
    - *Front Face*: Starts at `rotateY(0deg)`. On hover, rotates to `rotateY(-180deg)` (spinning away from the user).
    - *Back Face*: Starts at `rotateY(180deg)` (upside down and mirrored behind the front). On hover, rotates to `rotateY(0deg)` (facing the user).
  - **Timing**: `transition: transform 0.5s ease-in-out` ensures a smooth, weighty physical feel to the rotation.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| 3D Flip Rotation | CSS `transform: rotateY()` + `perspective()` | Native GPU-accelerated 3D rendering engine in browsers. |
| Face Hiding | CSS `backface-visibility: hidden` | Core requirement for 2-sided 3D objects; prevents mirrored content bleeding through. |
| Layout Overlay | CSS `position: absolute` | Stacks the front and back perfectly on top of each other within the main flow container. |
| Interactive State | CSS `:hover` and `:focus-within` | Pure CSS solution, avoids JavaScript overhead, accessible to keyboard users. |

> **Feasibility Assessment**: 100%. The code precisely replicates the structural logic, 3D math, styling, and interactive behavior demonstrated in the tutorial using modern best practices.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "iPhone XR",
    body_text: str = "Capacity: 256GB\nDisplay: 6.1-inch (diagonal)\nChip: A12 Bionic chip\nCamera: 12MP",
    color_scheme: str = "light",        
    accent_color: str = "#0071e3",     
    width_px: int = 320,
    height_px: int = 420,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Interactive 3D Flip Card visual effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#0a0a0c"
        surface_color = "#1c1c1e"
        text_color = "#f5f5f7"
        text_muted = "#86868b"
        shadow = "0 20px 40px rgba(0,0,0,0.4)"
        border_color = "rgba(255,255,255,0.05)"
    else:
        bg_color = "#f2f2f7"
        surface_color = "#ffffff"
        text_color = "#1d1d1f"
        text_muted = "#86868b"
        shadow = "0 15px 35px rgba(0,0,0,0.1)"
        border_color = "rgba(0,0,0,0.05)"

    # Format list items from newline-separated text
    lines = [line.strip() for line in body_text.split('\n') if line.strip()]
    list_html = "".join([f"<li>{line}</li>" for line in lines])

    # === CSS ===
    css = f"""/* Interactive 3D Flip Card */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --surface: {surface_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --shadow: {shadow};
    --border: {border_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    /* Simulated background landscape for depth */
    background-image: radial-gradient(circle at top right, rgba(255,255,255,0.05), transparent),
                      radial-gradient(circle at bottom left, rgba(0,0,0,0.05), transparent);
}}

/* Main Container */
.flip-card {{
    width: var(--width);
    height: var(--height);
    position: relative;
    cursor: pointer;
    /* Optional: allows card to scale slightly on hover for extra juice */
    transition: transform 0.3s ease;
}}

.flip-card:hover {{
    transform: scale(1.02);
}}

/* Faces common styling */
.card-front, .card-back {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border-radius: 16px;
    background-color: var(--surface);
    box-shadow: var(--shadow);
    border: 1px solid var(--border);
    /* Core 3D styling */
    backface-visibility: hidden;
    transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    
    /* Layout */
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    overflow: hidden;
}}

/* Front specific */
.card-front {{
    /* Perspective applied to the transform itself */
    transform: perspective(1000px) rotateY(0deg);
}}

.device-mockup {{
    width: 60%;
    height: auto;
    margin-bottom: 2rem;
    color: var(--accent);
    filter: drop-shadow(0 10px 10px rgba(0,0,0,0.1));
}}

.front-title {{
    font-size: 1.5rem;
    font-weight: 600;
    letter-spacing: -0.5px;
}}

/* Back specific */
.card-back {{
    /* Back face starts rotated 180 degrees */
    transform: perspective(1000px) rotateY(180deg);
    text-align: center;
    justify-content: space-around;
}}

.back-title {{
    font-size: 1.5rem;
    font-weight: 600;
}}

.specs-list {{
    list-style: none;
    text-align: center;
    width: 100%;
    margin: 1.5rem 0;
}}

.specs-list li {{
    font-size: 0.9rem;
    color: var(--text-muted);
    padding: 0.4rem 0;
    border-bottom: 1px solid var(--border);
}}

.specs-list li:last-child {{
    border-bottom: none;
}}

.price {{
    font-size: 1.75rem;
    font-weight: 700;
    margin-bottom: 1rem;
}}

.buy-btn {{
    background-color: var(--accent);
    color: #ffffff;
    border: none;
    padding: 0.8rem 2rem;
    border-radius: 30px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.2s, transform 0.2s;
    width: 100%;
}}

.buy-btn:hover {{
    filter: brightness(1.1);
    transform: translateY(-2px);
}}

.buy-btn:active {{
    transform: translateY(0);
}}

/* Triggering the Flip */
/* Using :focus-within ensures keyboard users tabing to the button also trigger the flip */
.flip-card:hover .card-front,
.flip-card:focus-within .card-front {{
    transform: perspective(1000px) rotateY(-180deg);
}}

.flip-card:hover .card-back,
.flip-card:focus-within .card-back {{
    transform: perspective(1000px) rotateY(0deg);
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>3D Flip Card</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <!-- tabindex allows keyboard focus -->
    <div class="flip-card" tabindex="0">
        <!-- FRONT FACE -->
        <div class="card-front">
            <!-- SVG placeholder representing the product/image -->
            <svg class="device-mockup" viewBox="0 0 100 200" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="5" y="5" width="90" height="190" rx="15" fill="currentColor" opacity="0.1"/>
                <rect x="5" y="5" width="90" height="190" rx="15" stroke="currentColor" stroke-width="3"/>
                <rect x="35" y="15" width="30" height="5" rx="2.5" fill="currentColor"/>
                <circle cx="50" cy="180" r="8" stroke="currentColor" stroke-width="2"/>
                <path d="M50 100 L50 80 M40 90 L60 90" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>
            </svg>
            <h2 class="front-title">{title_text}</h2>
        </div>

        <!-- BACK FACE -->
        <div class="card-back">
            <h2 class="back-title">{title_text}</h2>
            <ul class="specs-list">
                {list_html}
            </ul>
            <div class="price">$599</div>
            <button class="buy-btn">Buy now</button>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// No JavaScript required for the core flip effect!
// The entire 3D interaction is handled via CSS transforms and pseudo-classes.
document.addEventListener('DOMContentLoaded', () => {
    const buyBtn = document.querySelector('.buy-btn');
    buyBtn.addEventListener('click', (e) => {
        // Prevent click from bubbling if needed, handle cart logic here
        e.stopPropagation(); 
        alert('Added to cart!');
    });
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

* **Accessibility (a11y)**: 
  - Added `tabindex="0"` to the `.flip-card` wrapper.
  - Used the `:focus-within` CSS pseudo-class alongside `:hover` so that when a keyboard-only user Tabs into the card, it automatically flips to reveal the "Buy now" button. 
  - Ensure the SVG uses `currentColor` and that the chosen `accent_color` meets WCAG AA 4.5:1 contrast ratios against the card background.
* **Performance**: 
  - CSS 3D transforms (`rotateY` and `perspective`) automatically trigger hardware acceleration (GPU compositing) in modern browsers, ensuring a 60fps framerate.
  - Using `transform` for animations avoids layout recalculations and repaints, which is much more performant than animating margins, widths, or display properties.