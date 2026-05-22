# 3D Flip Card Hover Effect

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: 3D Flip Card Hover Effect

* **Core Visual Mechanism**: A two-sided card that rotates 180 degrees along the Y-axis in 3D space when hovered or focused. This is achieved using CSS 3D transforms, specifically the `perspective` property on a parent container to establish depth, `transform-style: preserve-3d` on the flipping element to maintain spatial relationships of its children, and `backface-visibility: hidden` to ensure the reverse side of an element is invisible when turned away from the viewer.
* **Why Use This Skill (Rationale)**: The flip card effect introduces spatial depth and interactivity, making UI elements feel tactile. From a UX perspective, it serves as an excellent progressive disclosure mechanism—saving initial screen space by hiding secondary information (like a product description, team member bio, or pricing details) until the user expresses intent by hovering.
* **Overall Applicability**: Ideal for flashcards, e-learning platforms, product galleries, pricing tiers, team/staff bios, and feature highlight grids.
* **Value Addition**: Transforms a static block of information into an engaging micro-interaction. It encourages user exploration and provides twice the real estate within the same physical footprint on the screen.
* **Browser Compatibility**: Excellent. The properties `transform-style: preserve-3d`, `perspective`, and `backface-visibility` are fully supported in all modern browsers. 


### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Structure**: A `.card-container` wrapper that provides perspective, a `.card` inner wrapper that actually rotates, and two stacked sibling elements (`.front` and `.back`).
  - **Color Logic**: High contrast is often used to differentiate the two sides. The front typically features a solid accent color (e.g., `#007bff` blue), while the back reveals a different color (e.g., `#28a745` green) or a neutral surface with dark text. 
  - **Typography**: Centered sans-serif typography (like 'Inter' or 'Calibri') ensures high legibility.
  - **Key CSS Properties**: `perspective`, `transform-style: preserve-3d`, `backface-visibility: hidden`, `transform: rotateY()`.

* **Step B: Layout & Compositional Style**
  - **Layout System**: The `.card-container` explicitly defines the width and height dimensions. The inner `.card` takes up 100% of this space and is positioned relatively. The `.front` and `.back` faces are positioned absolutely (`top: 0; left: 0; width: 100%; height: 100%`) to stack perfectly on top of each other. 
  - **Flexbox**: Used within the faces to perfectly center the text horizontally and vertically.

* **Step C: Interactive Behavior & Animations**
  - **Hover Trigger**: The `:hover` state is applied to the `.card-container` rather than the `.card` itself. This prevents annoying flickering/glitching that occurs if the mouse loses contact with the rotating boundary of the card mid-flip.
  - **Transition**: A smooth `transition: transform 0.6s` creates a deliberate, physical-feeling rotation.
  - **Rotation Logic**: The `.front` is at `0deg`. The `.back` is pre-rotated to `180deg` so it faces away. On hover, the `.card` wrapper is rotated `180deg`, swinging the front face away and bringing the pre-rotated back face into view at exactly `0deg` relative to the viewer.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| 3D Depth | CSS `perspective` | Creates a realistic vanishing point for the rotation, making the edges appear to move towards/away from the viewer. |
| Dual-Sided Stacking | CSS `absolute` positioning + `backface-visibility` | Perfectly overlaps the faces and natively hides whichever face is rotated past 90 degrees. |
| Animation State | CSS `:hover` + `:focus-within` | Pure CSS solution; no JavaScript required for the hover trigger. Focus-within adds essential keyboard accessibility. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Front Side of the Card",
    body_text: str = "Back Side of the Card\nSecondary details revealed on hover.",
    color_scheme: str = "light",
    accent_color: str = "#007bff",
    width_px: int = 300,
    height_px: int = 400,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Flip Card Hover Effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os
    import html

    os.makedirs(output_dir, exist_ok=True)
    
    # Escape user text to prevent HTML injection
    safe_title = html.escape(title_text)
    safe_body = html.escape(body_text).replace('\n', '<br>')

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        page_bg = "#0d111c"
        page_text = "#f0f0f0"
        front_bg = accent_color
        front_text = "#ffffff"
        back_bg = "#1a2235"
        back_text = "#ffffff"
        back_border = f"2px solid {accent_color}"
    else:
        page_bg = "#f8f9fa"
        page_text = "#1a1a2e"
        front_bg = accent_color
        front_text = "#ffffff"
        back_bg = "#ffffff"
        back_text = "#1a1a2e"
        back_border = f"2px solid {accent_color}"

    # === CSS ===
    css = f"""/* 3D Flip Card Hover Effect — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --page-bg: {page_bg};
    --page-text: {page_text};
    --front-bg: {front_bg};
    --front-text: {front_text};
    --back-bg: {back_bg};
    --back-text: {back_text};
    --back-border: {back_border};
    --card-width: {width_px}px;
    --card-height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--page-bg);
    color: var(--page-text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

/* The container establishes the 3D perspective */
.card-container {{
    perspective: 1000px; /* Lower value = more extreme 3D effect */
    width: var(--card-width);
    max-width: 90vw; /* Responsive safeguard */
    height: var(--card-height);
    max-height: 90vh; /* Responsive safeguard */
    cursor: pointer;
}}

/* The inner card handles the 3D space context and transition */
.card {{
    position: relative;
    width: 100%;
    height: 100%;
    transform-style: preserve-3d;
    transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
    border-radius: 12px;
}}

/* Trigger flip on hover (mouse) or focus-within (keyboard tabbing) */
.card-container:hover .card,
.card-container:focus-within .card {{
    transform: rotateY(180deg);
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.25);
}}

/* Shared styles for both faces */
.front, .back {{
    position: absolute;
    width: 100%;
    height: 100%;
    border-radius: 12px;
    /* Crucial: hides the reverse side when turned around */
    backface-visibility: hidden;
    -webkit-backface-visibility: hidden; /* Safari fallback */
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 2rem;
}}

/* Front face specific styles */
.front {{
    background-color: var(--front-bg);
    color: var(--front-text);
    /* Explicitly state 0deg to prevent visual bugs in some browsers */
    transform: rotateY(0deg); 
}}

.front h2 {{
    font-size: 1.5rem;
    font-weight: 600;
    line-height: 1.3;
}}

/* Back face specific styles */
.back {{
    background-color: var(--back-bg);
    color: var(--back-text);
    border: var(--back-border);
    /* Pre-rotate the back face so it's upside down initially */
    transform: rotateY(180deg);
}}

.back p {{
    font-size: 1.125rem;
    line-height: 1.6;
    opacity: 0.9;
}}

/* Accessibility: respect user preferences for motion */
@media (prefers-reduced-motion: reduce) {{
    .card {{
        transition: none;
    }}
}}
"""

    # === HTML ===
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>3D Flip Card Effect</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <!-- tabindex="0" makes the container keyboard focusable -->
    <div class="card-container" tabindex="0" aria-label="Interactive Flip Card">
        <div class="card">
            <!-- Front side -->
            <div class="front" aria-hidden="true">
                <h2>{safe_title}</h2>
            </div>
            <!-- Back side -->
            <div class="back">
                <p>{safe_body}</p>
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// 3D Flip Card Effect
// The core animation is driven purely by CSS :hover and :focus-within.
// This JS file is included for potential future extensions, such as handling click-to-flip on mobile devices.

document.addEventListener('DOMContentLoaded', () => {{
    const container = document.querySelector('.card-container');
    const card = document.querySelector('.card');

    // Optional: Add toggle behavior for touch devices
    container.addEventListener('click', () => {{
        // If you wanted a purely JS driven toggle state instead of CSS hover:
        // card.style.transform = card.style.transform === 'rotateY(180deg)' ? 'rotateY(0deg)' : 'rotateY(180deg)';
    }});
}});
"""

    # === Write files ===
    files = []
    for fname, content in [("index.html", html_content), ("style.css", css), ("script.js", js)]:
        path = os.path.join(output_dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        files.append(path)

    return {
        "html": html_content,
        "css": css,
        "js": js,
        "files": files,
    }
```

### 4. Accessibility & Performance Notes

* **Accessibility (a11y)**: 
  * The `.card-container` is given `tabindex="0"` allowing keyboard users to tab to it.
  * The CSS includes `.card-container:focus-within .card`, which triggers the 180-degree flip when the element receives keyboard focus, ensuring parity with the mouse `:hover` experience.
  * A `prefers-reduced-motion` media query instantly switches the front to the back without the 0.6-second physical rotation animation to accommodate users susceptible to vestibular motion triggers.
  * `aria-hidden="true"` can be applied logically if the front text is redundant to screen readers once flipped, though structuring proper alternative text is context-dependent.
* **Performance**: 
  * The `transform` property is GPU-accelerated. Pushing the rotation task to the composite thread ensures a smooth 60fps animation without triggering expensive layout recalculations (reflow) or repaints.
  * `-webkit-backface-visibility` is included as a vendor prefix to ensure Safari handles the dual-pane overlap correctly without visual glitching during the animation curve.