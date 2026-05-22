# Animated Conic Glow Border

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Animated Conic Glow Border

* **Core Visual Mechanism**: This pattern creates a continuous, chasing neon border effect around a card. It uses CSS `conic-gradient()` applied to `::before` and `::after` absolute pseudo-elements positioned directly behind the main card (`z-index: -1`). The magic comes from animating the starting angle of the conic gradient using a custom CSS Houdini `@property`, combined with `filter: blur()` on one of the pseudo-elements to create an outer glow.
* **Why Use This Skill (Rationale)**: Static borders can feel rigid. This technique introduces fluid, futuristic motion that draws the user's eye without relying on heavy JavaScript or SVG particle rendering. The glowing tail effect provides a sense of direction and energy (often called a "cyberpunk" or "gamer" aesthetic).
* **Overall Applicability**: Ideal for highlighting active states, premium pricing tiers, special feature callouts, or "pro" user badges. It excels in dark-mode interfaces where the glowing accent color can contrast sharply with the dark background.
* **Value Addition**: Transforms a basic container into a focal point with high perceived production value. It adds depth through layering (solid card over animated gradient over blurred glow) using only a single HTML node.
* **Browser Compatibility**: This effect relies heavily on the CSS `@property` rule to animate the `<angle>` value of the gradient. This is supported in modern browsers (Chrome 85+, Edge 85+, Safari 16.4+, Firefox 128+). For unsupported browsers, the component gracefully degrades to a static (non-spinning) gradient border.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Single HTML Node**: The entire effect wraps around one container (`.card`).
  - **Color Logic**: A high-contrast dark theme works best.
    - Page Background: `#0d111c`
    - Card Surface: `#1c1f2b` (must be completely opaque to hide the gradients beneath)
    - Gradient Tail: Transitions from `transparent` (70% of the circle) to a vivid accent color (e.g., Cyan `#00ffff` or Neon Pink).
  - **Typographic Hierarchy**: Clean, geometric sans-serif (like *Inter* or *Poppins*). The title is semi-bold and bright white, while the body text is slightly muted to maintain focus on the border.
  - **Key CSS Properties**: `conic-gradient`, `@property`, `filter: blur`, `padding` with `box-sizing: content-box`.

* **Step B: Layout & Compositional Style**
  - **Stacking Context Trick**: The `.card` is `position: relative` but **must not** declare a `z-index` or `transform`. This ensures it doesn't create a new isolated stacking context.
  - **Layering**: The pseudo-elements (`::before`, `::after`) are `position: absolute` with `z-index: -1`, forcing them behind the `.card`'s opaque background but above the document's background.
  - **Proportions**: To create the border, the pseudo-elements are sized at `100%` of the card, but `padding: 3px` and `box-sizing: content-box` are applied. This forces the gradient to stick out exactly `3px` beyond the card's dimensions.

* **Step C: Interactive Behavior & Animations**
  - **Continuous Loop**: Uses a pure CSS `@keyframes` animation running infinitely.
  - **Animation Logic**: The CSS `@property --angle` is transitioned from `0deg` to `360deg` continuously over `3s` with a `linear` timing function to ensure smooth, un-accelerated rotation.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Chasing Border Line | `conic-gradient` & `padding` | `padding` + `content-box` neatly frames the pseudo-element slightly larger than the parent without complex width calculations. |
| Outer Glow | CSS `filter: blur()` | Native GPU-accelerated blur applied to a duplicated pseudo-element creates a perfect soft neon cast. |
| Continuous Rotation | `@property` + `@keyframes` | Animating a CSS custom property of type `<angle>` is the only performant way to smoothly rotate a CSS gradient natively without JS `requestAnimationFrame`. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Animate Borders",
    body_text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Atque ad exercitationem voluptatem ullam et, natus impedit quae veniam optio a doloremque.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00ffff",     # CSS hex color for accent
    width_px: int = 350,
    height_px: int = 400,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Animated Conic Glow Border visual effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os
    import html

    os.makedirs(output_dir, exist_ok=True)

    # Sanitize text inputs for HTML inclusion
    html_safe_title = html.escape(title_text)
    html_safe_body = html.escape(body_text)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0d111c"
        surface_color = "#1c1f2b" # Opaque dark card
        text_color = "#a0aab2"
        title_color = "#ffffff"
    else:
        bg_color = "#e9ecef"
        surface_color = "#ffffff" # Opaque light card
        text_color = "#495057"
        title_color = "#111111"

    # === CSS ===
    css = f"""/* Animated Conic Glow Border */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --surface: {surface_color};
    --text: {text_color};
    --title: {title_color};
    --accent: {accent_color};
    
    --width: {width_px}px;
    --min-height: {height_px}px;
    
    /* Configurable border dimensions */
    --border-thickness: 3px;
    --border-radius: 12px;
    
    /* Fallback angle if @property is unsupported */
    --angle: 0deg; 
}}

/* Houdini API to allow angle animation */
@property --angle {{
    syntax: "<angle>";
    initial-value: 0deg;
    inherits: false;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow-x: hidden; /* Prevent horizontal scroll from extreme blurs */
    padding: 2rem;
}}

/* Main Card Container */
.card {{
    position: relative;
    width: wmin(var(--width), 100%);
    min-height: var(--min-height);
    background: var(--surface);
    padding: 2.5rem;
    border-radius: var(--border-radius);
    
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    
    /* WARNING: Do not add z-index, transform, or opacity here!
       Doing so will create a stacking context and hide the border behind the content. */
}}

/* Typography */
.title {{
    font-size: 1.8rem;
    font-weight: 600;
    color: var(--title);
    margin-bottom: 1rem;
}}

.body-text {{
    font-size: 1rem;
    line-height: 1.6;
    color: var(--text);
}}

/* Animated Pseudo-Elements (Border & Glow) */
.card::after, .card::before {{
    content: '';
    position: absolute;
    height: 100%;
    width: 100%;
    
    /* The gradient tail: transparent for 70% of the circle, then fades to accent */
    background-image: conic-gradient(from var(--angle), transparent 70%, var(--accent));
    
    top: 50%;
    left: 50%;
    translate: -50% -50%;
    z-index: -1;
    
    /* Push the border OUTSIDE the card by the defined thickness */
    padding: var(--border-thickness);
    box-sizing: content-box;
    
    /* Ensure the outer curve parallels the inner curve perfectly */
    border-radius: calc(var(--border-radius) + var(--border-thickness));
    
    /* The continuous rotation */
    animation: spin 3s linear infinite;
}}

/* The specific glow layer */
.card::before {{
    filter: blur(1.5rem);
    opacity: 0.5;
}}

/* Angle Animation Keyframes */
@keyframes spin {{
    from {{
        --angle: 0deg;
    }}
    to {{
        --angle: 360deg;
    }}
}}
"""

    # === HTML ===
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html_safe_title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <!-- 
      The .card element houses the solid background. 
      The animated borders are pseudo-elements generated via CSS.
    -->
    <div class="card">
        <h1 class="title">{html_safe_title}</h1>
        <p class="body-text">{html_safe_body}</p>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Animated Conic Glow Border
// This component relies entirely on CSS @property and conic-gradients.
// No JavaScript is required for the visual rendering loop!

document.addEventListener('DOMContentLoaded', () => {{
    console.log("Card component loaded. Gradient animation handled by CSS Houdini.");
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

* **Accessibility**: 
  - The endless looping animation might be distracting or cause issues for users with vestibular disorders. In a production environment, it is highly recommended to wrap the `animation` declaration inside a `@media (prefers-reduced-motion: no-preference)` query so the gradient remains static for those who request less motion.
  - The contrast ratio relies entirely on the selected text color and surface background color. The defaults provided (`#ffffff` on `#1c1f2b`) easily exceed the WCAG AA minimum 4.5:1 ratio.
* **Performance**: 
  - Using CSS custom properties (`@property`) to animate `<angle>` values within a gradient forces paint recalculations. While modern browser engines handle this quite well, applying this effect to hundreds of elements simultaneously on a single page might degrade framerate.
  - `filter: blur(1.5rem)` is a GPU-intensive operation. Keeping the physical pixel size of the card constrained will maintain 60fps scrolling on lower-end mobile devices. Ensure `will-change: filter` is **not** globally applied, as browsers auto-optimize this locally better than forced rasterization.