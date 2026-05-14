# Continuous CSS Gradient Wave Background

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Continuous CSS Gradient Wave Background

* **Core Visual Mechanism**: The effect relies on an oversized pseudo-canvas (a `div` that is significantly wider than its container) filled with a repeating linear gradient. By animating the horizontal position of this oversized element back and forth using CSS `@keyframes`, it creates the illusion of a continuous, fluid, wave-like transition of colors across the screen. 

* **Why Use This Skill (Rationale)**: This technique provides a dynamic, organic sense of movement to a web page without the heavy payload of a video background or the computational overhead of WebGL/Canvas. The slow shifting of colors feels calming and modern, drawing the eye without distracting from foreground content.

* **Overall Applicability**: This pattern is excellent for hero sections, landing page headers, login screens, or full-page immersive backgrounds where you want a "living" aesthetic rather than a static flat color.

* **Value Addition**: It elevates a standard gradient background from a static design choice into an interactive-feeling experience. It implies depth and fluidity, making the interface feel more premium and modern.

* **Browser Compatibility**: This technique uses standard CSS features (`linear-gradient`, `absolute` positioning, and `@keyframes`). It is universally supported across all modern browsers (Chrome, Firefox, Safari, Edge).


### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **HTML Structure**: Extremely simple. A `.wave-container` acts as the mask, and a nested `.wave` element acts as the moving texture.
  - **Color Logic**: The tutorial uses an alternating sequence of `lightskyblue` and `darkblue`. The repetition of the colors within the gradient definition (`lightskyblue, darkblue, lightskyblue, darkblue...`) is what creates the "stripes" of the wave.
  - **CSS Properties**: The aesthetic is entirely driven by `background: linear-gradient(...)`.

* **Step B: Layout & Compositional Style**
  - **Container**: The `.wave-container` is constrained to a specific height (e.g., `600px`) and uses `overflow: hidden; position: relative;` to act as a window masking the larger element inside.
  - **Oversized Element**: The `.wave` element uses `width: 200%;` and `height: 100%;`. It is positioned `absolute`ly to the container. The extra width provides the "track" for the animation to slide along.

* **Step C: Interactive Behavior & Animations**
  - The animation is a pure CSS `@keyframes` loop running infinitely over a long duration (30 seconds).
  - The tutorial animates the `left` property from `-80%` to `0%` to `-100%`. *(Note: While the tutorial animates `left`, modern CSS best practices dictate animating `transform: translateX()` instead to avoid browser layout recalculation jank. The reproduction code will upgrade this for better performance).*


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Wave texture | CSS `linear-gradient` | Exact reproduction of the tutorial's method for creating the color bands. |
| Masking | CSS `overflow: hidden` | Standard approach to hide the oversized moving element. |
| Movement | CSS `@keyframes` & `transform` | Upgraded from the tutorial's `left` property to `transform: translateX()` to ensure GPU-accelerated, buttery smooth 60fps animation. |

> **Feasibility Assessment**: 100% reproduction. The core aesthetic and movement are perfectly captured using pure CSS. The implementation has been slightly optimized for modern rendering performance while maintaining identical visual output.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Fluid Gradient Wave",
    body_text: str = "A pure CSS animated background technique.",
    color_scheme: str = "dark",        
    accent_color: str = "#00bfff",     
    width_px: int = 1200,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Continuous CSS Gradient Wave Background.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#050B14" # Deep dark blue for contrast
        text_color = "#ffffff"
        text_shadow = "rgba(0, 0, 0, 0.8)"
    else:
        bg_color = "#e6f0fa" # Light ice blue
        text_color = "#111827"
        text_shadow = "rgba(255, 255, 255, 0.8)"

    # Create the repeating gradient string based on the accent color
    # Repeating 4 times to ensure smooth transitions across the 200% width
    color1 = accent_color
    color2 = bg_color
    gradient_stops = f"{color1}, {color2}, {color1}, {color2}, {color1}, {color2}, {color1}, {color2}"

    # === CSS ===
    css = f"""/* Continuous CSS Gradient Wave Background */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --text-shadow: {text_shadow};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: #1a1a1a; /* Outer background */
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.wave-container {{
    width: var(--width);
    max-width: 100vw;
    height: var(--height);
    position: relative;
    overflow: hidden;
    border-radius: 12px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    background-color: var(--bg-color);
}}

.wave {{
    position: absolute;
    bottom: 0;
    left: 0;
    height: 100%;
    /* 200% width allows the gradient to slide horizontally without running out of texture */
    width: 200%; 
    background: linear-gradient(to right, {gradient_stops});
    /* We use transform instead of 'left' (as seen in the tutorial) for GPU acceleration */
    animation: wave-motion 30s ease-in-out infinite;
}}

.content-overlay {{
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
    z-index: 10;
    color: var(--text-color);
    text-shadow: 0 4px 12px var(--text-shadow);
}}

.content-overlay h1 {{
    font-size: 3.5rem;
    font-weight: 700;
    letter-spacing: -0.05em;
    margin-bottom: 1rem;
}}

.content-overlay p {{
    font-size: 1.25rem;
    font-weight: 300;
    opacity: 0.9;
    max-width: 600px;
}}

/* The keyframes mimic the tutorial's logic but use performant transforms */
@keyframes wave-motion {{
    0% {{
        transform: translateX(-40%);
    }}
    25% {{
        transform: translateX(-20%);
    }}
    50% {{
        transform: translateX(0%);
    }}
    75% {{
        transform: translateX(-30%);
    }}
    100% {{
        transform: translateX(-40%); /* Must match 0% for seamless loop */
    }}
}}

/* Respect user preferences for reduced motion */
@media (prefers-reduced-motion: reduce) {{
    .wave {{
        animation: none;
        transform: translateX(0);
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
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="wave-container">
        <!-- The animated background layer -->
        <div class="wave"></div>
        
        <!-- Foreground content added for practical component usage -->
        <div class="content-overlay">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Continuous CSS Gradient Wave Background
document.addEventListener('DOMContentLoaded', () => {{
    // The animation is entirely CSS-driven. 
    // This JS file is included for structure and future extensibility.
    console.log("Wave background initialized.");
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


### 4. Accessibility & Performance Notes

* **Performance Optimization**: The original tutorial animated the `left` CSS property. Animating layout properties like `left` forces the browser to recalculate layout and repaint pixels on every single frame, which can cause significant jitter ("jank") on lower-end devices and drain battery life. The reproduction code has been upgraded to animate `transform: translateX()`. Transforms are handled by the GPU (Compositor thread) and are drastically more performant.
* **Accessibility (a11y)**: Large moving areas can trigger motion sickness or vestibular disorders in some users. The provided CSS includes a `@media (prefers-reduced-motion: reduce)` media query that stops the animation for users who have requested reduced motion at the OS level.
* **Contrast**: Text overlaid on an actively changing gradient can suffer from readability issues depending on where the color stops align. To mitigate this, a `text-shadow` has been added to the `.content-overlay` text elements to ensure legibility regardless of which color is passing underneath it.