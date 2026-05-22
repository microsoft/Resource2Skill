# Interactive 3D Layered Flip Card

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Interactive 3D Layered Flip Card

* **Core Visual Mechanism**: This pattern utilizes CSS 3D transforms to create an interactive, physical feeling of depth. By utilizing `transform-style: preserve-3d`, a parent container can rotate while allowing its child elements (the front and back faces) to exist in a shared 3D space. The illusion is completed using `backface-visibility: hidden` (hiding the reverse side of an element) and applying `translateZ()` to text elements, causing them to visually "pop out" from the card surface as it rotates.
* **Why Use This Skill (Rationale)**: Flipping cards create a micro-interaction that rewards user curiosity (hovering) with a satisfying, tactile physical motion. Placing information on the back of a card helps declutter interfaces, delaying secondary information until the user actively seeks it. The added `translateZ` depth creates a premium, highly polished feel.
* **Overall Applicability**: Excellent for team member profiles (photo on front, bio on back), product feature highlights, pricing tier details, or interactive portfolio galleries.
* **Value Addition**: It elevates a flat, static UI into an interactive, spatial experience. It saves screen real estate while increasing user engagement through playful discovery.
* **Browser Compatibility**: Fully supported in all modern browsers. `transform-style: preserve-3d` and `backface-visibility` have been standard for years. Older browsers fall back gracefully if animations are ignored, though iOS Safari sometimes requires `-webkit-` prefixes for backface-visibility in highly complex nested scenarios (handled natively in modern versions).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **HTML Construct**: Requires a specific 3-deep nesting structure: Outer Wrapper (`.card-wrapper`), Inner Rotator (`.card-content`), and the Faces (`.card-front`, `.card-back`).
  - **Color Logic**: High contrast is key. The front often uses an image with a blend-mode overlay (e.g., `#0d111c` overlaid on a photo), while the back uses a solid, legible background matching the theme.
  - **CSS Properties**:
    - `perspective`: Applied to the outer wrapper to give the 3D rotation a vanishing point.
    - `transform-style: preserve-3d`: Applied to the rotating container.
    - `backface-visibility: hidden`: Applied to the front and back faces.
    - `transform: rotateY()`: For the flip.
    - `transform: translateZ()`: For the layered pop-out text effect.

* **Step B: Layout & Compositional Style**
  - **Layout system**: CSS Grid or Flexbox can center content inside the faces. The critical layout step is `position: absolute; inset: 0;` applied to both the front and back faces so they stack perfectly on top of one another inside the relative parent.
  - **Z-index layering**: The front face sits naturally on top. The back face is initially rotated `180deg` on the Y-axis so it is facing "away" from the user.

* **Step C: Interactive Behavior & Animations**
  - **Hover Interaction**: `.card-wrapper:hover .card-content { transform: rotateY(0.5turn); }` triggers the flip.
  - **Keyboard Accessibility**: Using `:focus-within` allows keyboard users tabbing through the document to trigger the same flip.
  - **Animation Timing**: A smooth, slightly slowed ease creates the physical feel. `transition: transform 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);`

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Core Flip Animation | Pure CSS (`transform: rotateY`) | Highly performant, hardware-accelerated, requires no JavaScript to calculate frames. |
| 3D Shared Space | CSS `transform-style: preserve-3d` | Native CSS specification built exactly for this purpose. |
| Parallax/Pop-out text | CSS `transform: translateZ()` | Pushes elements towards the viewer on the Z-axis; when combined with rotation, creates striking parallax depth. |
| Hiding the reverse side | CSS `backface-visibility` | Prevents the mirrored, backward text of the flipped element from showing through. |

> **Feasibility Assessment**: 100%. This is a textbook CSS feature that can be perfectly reproduced without external libraries or JavaScript.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "THE FAIR",
    body_text: str = "Step right up and experience the magic of the midway. Thrills, games, and memories await on the other side.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 400,
    height_px: int = 550,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Interactive 3D Layered Flip Card.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#111827"
        text_primary = "#f9fafb"
        text_secondary = "#d1d5db"
        card_back_bg = "#1f2937"
        overlay = "rgba(17, 24, 39, 0.7)"
    else:
        bg_color = "#f3f4f6"
        text_primary = "#111827"
        text_secondary = "#4b5563"
        card_back_bg = "#ffffff"
        overlay = "rgba(255, 255, 255, 0.7)"

    # Image placeholder for the front of the card
    front_image = "https://images.unsplash.com/photo-1513159446162-54eb8bdaa79b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"

    css = f"""/* Interactive 3D Layered Flip Card */
:root {{
    --bg-color: {bg_color};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --card-back-bg: {card_back_bg};
    --accent: {accent_color};
    --overlay: {overlay};
    --card-width: {width_px}px;
    --card-height: {height_px}px;
}}

*, *::before, *::after {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 2rem;
}}

/* 1. The Outer Wrapper dictates the perspective */
.card-wrapper {{
    width: var(--card-width);
    height: var(--card-height);
    perspective: 1500px; /* Gives the 3D effect a vanishing point */
    cursor: pointer;
}}

/* 2. The Inner Content holds the 3D space and handles the rotation */
.card-content {{
    width: 100%;
    height: 100%;
    position: relative;
    transition: transform 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    transform-style: preserve-3d; /* CRITICAL: Allows children to share 3D space */
}}

/* Trigger the flip on hover or keyboard focus */
.card-wrapper:hover .card-content,
.card-wrapper:focus-within .card-content {{
    transform: rotateY(0.5turn); /* 180 degrees */
}}

/* 3. The Faces */
.card-front,
.card-back {{
    position: absolute;
    inset: 0; /* top:0, bottom:0, left:0, right:0 */
    border-radius: 16px;
    backface-visibility: hidden; /* CRITICAL: Hides the reverse side */
    transform-style: preserve-3d; /* Allows nested elements to pop out */
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 2.5rem;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}}

/* Front Styling */
.card-front {{
    background-image: linear-gradient(var(--overlay), var(--overlay)), url('{front_image}');
    background-size: cover;
    background-position: center;
}}

.card-front h2 {{
    font-size: 2.5rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #ffffff; /* Always white due to image overlay */
    /* Pop-out effect */
    transform: translateZ(80px);
    text-shadow: 0 10px 20px rgba(0,0,0,0.5);
}}

.card-front p {{
    color: var(--accent);
    font-weight: 600;
    margin-top: 0.5rem;
    /* Secondary pop-out effect */
    transform: translateZ(50px); 
}}

/* Back Styling */
.card-back {{
    background-color: var(--card-back-bg);
    /* Initially flip the back face so it faces away */
    transform: rotateY(0.5turn);
    text-align: center;
}}

.card-back h3 {{
    font-size: 1.5rem;
    margin-bottom: 1rem;
    color: var(--accent);
    /* Pop-out effect on the back face */
    transform: translateZ(60px);
}}

.card-back p {{
    font-size: 1rem;
    line-height: 1.6;
    color: var(--text-secondary);
    /* Pop-out effect on the back face */
    transform: translateZ(40px);
}}

/* Adding an interactive button for semantic focus-within */
.btn {{
    margin-top: 2rem;
    padding: 0.75rem 1.5rem;
    background-color: var(--accent);
    color: #fff;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    transform: translateZ(50px);
    transition: background-color 0.2s;
}}

.btn:hover, .btn:focus {{
    filter: brightness(1.1);
    outline: 2px solid var(--text-primary);
    outline-offset: 2px;
}}

/* Accessibility: Reduced Motion */
@media (prefers-reduced-motion: reduce) {{
    .card-content {{
        transition: none;
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>3D Layered Flip Card</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <!-- Outer Wrapper -->
    <div class="card-wrapper" tabindex="0">
        
        <!-- Rotating Container -->
        <div class="card-content">
            
            <!-- Front Face -->
            <div class="card-front">
                <h2>{title_text}</h2>
                <p>Hover to discover</p>
            </div>

            <!-- Back Face -->
            <div class="card-back">
                <h3>Behind the Scenes</h3>
                <p>{body_text}</p>
                <button class="btn">Learn More</button>
            </div>

        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    js = """// Pure CSS implementation. 
// JavaScript is included here as part of the component structure, 
// but the 3D flip and layering logic is entirely handled by CSS hover states and 3D transforms.

document.addEventListener('DOMContentLoaded', () => {
    // Optional: Add click listener for mobile devices where hover isn't present
    const wrapper = document.querySelector('.card-wrapper');
    
    wrapper.addEventListener('click', () => {
        // Toggle focus on click for better mobile experience
        if(document.activeElement === wrapper) {
            document.activeElement.blur();
        } else {
            wrapper.focus();
        }
    });
});
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

*   **Accessibility**: 
    *   **Keyboard Navigation**: The code utilizes `:focus-within` combined with `tabindex="0"` on the `.card-wrapper`. This ensures that users navigating via the `Tab` key can trigger the flip animation and interact with the button on the back.
    *   **Screen Readers**: Screen readers parse the DOM linearly. They will read the front text, followed immediately by the back text. This is usually acceptable, but if strict separation is required, JS would be needed to toggle `aria-hidden` attributes during the flip.
    *   **Reduced Motion**: A `@media (prefers-reduced-motion: reduce)` query is included to disable the transition duration, causing the card to instantly snap to the back side for users who suffer from vestibular motion sensitivity.
*   **Performance**:
    *   Using `transform: rotateY` triggers GPU-hardware acceleration, ensuring a smooth 60fps frame rate without repainting layout elements.
    *   `backface-visibility` combined with 3D context can occasionally cause minor anti-aliasing (jagged edges) on text in certain WebKit rendering scenarios. Adding a subtle `box-shadow: 0 0 1px rgba(0,0,0,0)` to text elements can force sub-pixel rendering if this occurs, though it is largely resolved in modern browsers.