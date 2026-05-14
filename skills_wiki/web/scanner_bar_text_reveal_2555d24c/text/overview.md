# Scanner Bar Text Reveal

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Scanner Bar Text Reveal

* **Core Visual Mechanism**: A cinematic text reveal effect achieved by clipping a dynamic background to the text's shape using `background-clip: text`. Instead of a standard fade or slide, the effect creates a "scanning laser" by animating `background-size` to form a horizontal strip and moving `background-position-y` up and down the text block. The animation concludes by expanding the background to 100% height, permanently revealing the solid text.
* **Why Use This Skill (Rationale)**: This interaction borrows aesthetics from sci-fi and retro-futurism (reminiscent of a CRT scanline or laser reveal). It breaks the monotony of standard opacity fades and immediately hooks user attention while making the text itself the centerpiece of the animation.
* **Overall Applicability**: Excellent for high-impact hero sections, landing page headlines, storytelling scroll experiences, or portfolio headers.
* **Value Addition**: Adds a dynamic, spatial dimension to plain text without needing external SVGs, canvas rendering, or heavy JavaScript animation libraries.
* **Browser Compatibility**: `background-clip: text` requires the `-webkit-` prefix in most browsers (including Safari and Chrome). The implementation uses `@supports` feature queries to gracefully fallback to standard solid text on unsupported or older browsers.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Typographic Hierarchy**: Relies on a massive, bold font (`900` weight) to ensure the background animation has enough "surface area" inside the letterforms to be highly visible and legible.
  - **Color Logic**: Uses a transparent text color and a dynamic background. The background is generated via a solid `linear-gradient` (acting as a highly scalable colored block that replaces the 1x1 pixel image used in the video).
  - **CSS Constructs**: `background-clip: text`, `-webkit-background-clip: text`, `color: transparent`, and `@supports` feature queries.

* **Step B: Layout & Compositional Style**
  - The text is prominently center-aligned within a flexible container.
  - Generous whitespace around the text draws visual focus exclusively to the high-contrast animation.

* **Step C: Interactive Behavior & Animations**
  - The animation sequence is triggered via an `IntersectionObserver` when the element scrolls into view.
  - **Keyframe Arc (`reveal-background`)**:
    - `0% - 10%`: A horizontal bar forms at the top of the text (`background-size: 15%`).
    - `10% - 35%`: The bar sweeps down to the bottom (`background-position-y: 100%`).
    - `35% - 45%`: The bar pauses briefly at the bottom.
    - `45% - 70%`: The bar sweeps back up to the top.
    - `70% - 100%`: The bar expands its height from 15% to 100%, filling the entire text block completely.
  - `animation-fill-mode: forwards` locks the final fully-filled state so the text remains readable.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Scanning bar effect | CSS `background-size` & `background-position` | Allows independent control of the height (size) and vertical placement (position) of the colored background block. |
| Text masking | CSS `background-clip: text` | Native, performant way to mask generic elements to text geometry. |
| Scalable background block | CSS `linear-gradient()` | Replaces the 1x1 pixel JPG from the original tutorial, eliminating the need for external assets while maintaining perfect pixel-sharp scaling. |
| Viewport triggering | JS `IntersectionObserver` | Ensures the 2-second animation only plays when the user is actually looking at the text. |

> **Feasibility Assessment**: 100%. The reproduction code accurately recreates the CSS animation timing, background clipping, and fallback mechanisms demonstrated in the tutorial, while optimizing it to remove external image dependencies.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "REVEAL TEXT",
    body_text: str = "A cinematic scanning bar text reveal effect driven purely by CSS background clipping.",
    color_scheme: str = "dark",        
    accent_color: str = "#ffffff",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Scanner Bar Text Reveal visual effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#0a0a10"
        text_color = "#a0a0b0"
    else:
        bg_color = "#f4f4f8"
        text_color = "#4a4a50"
        # If light mode and white accent is requested, fall back to a dark accent for visibility
        if accent_color.lower() in ["#fff", "#ffffff", "white"]:
            accent_color = "#111111"

    # === CSS ===
    css = f"""/* Scanner Bar Text Reveal */
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
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
}}

.reveal-text {{
    font-size: clamp(3rem, 10vw, 8rem);
    font-weight: 900;
    line-height: 1.1;
    letter-spacing: -0.02em;
    text-transform: uppercase;
    color: var(--accent); /* Fallback for unsupported browsers */
    margin-bottom: 1.5rem;
}}

.body-text {{
    font-size: 1.25rem;
    line-height: 1.6;
    max-width: 600px;
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.8s ease, transform 0.8s ease;
}}

/* Only apply complex animation if background-clip: text is supported */
@supports (-webkit-background-clip: text) or (background-clip: text) {{
    .reveal-text {{
        color: transparent;
        /* Use a solid linear gradient as a scalable background block */
        background-image: linear-gradient(var(--accent), var(--accent));
        background-repeat: no-repeat;
        
        /* Set initial state to invisible */
        background-size: 100% 0%;
        background-position-y: 0%;
        
        -webkit-background-clip: text;
        background-clip: text;
    }}
    
    .reveal-text.animate {{
        animation: reveal-background 2s ease-in-out forwards;
    }}
}}

/* Fade in the body text after the title animation completes */
.body-text.animate {{
    opacity: 1;
    transform: translateY(0);
    transition-delay: 1.5s; /* Align with the ending phase of the text reveal */
}}

/* The Core Scanning Bar Keyframes */
@keyframes reveal-background {{
    0% {{
        background-size: 100% 0%;
        background-position-y: 0%;
    }}
    10% {{
        background-size: 100% 15%; /* Expands to a 15% high horizontal bar */
        background-position-y: 0%;
    }}
    35%, 45% {{
        background-size: 100% 15%;
        background-position-y: 100%; /* Sweeps down to the bottom */
    }}
    70% {{
        background-size: 100% 15%;
        background-position-y: 0%; /* Sweeps back up to the top */
    }}
    100% {{
        background-size: 100% 100%; /* Expands to completely fill the text */
        background-position-y: 0%;
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
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1 class="reveal-text">{title_text}</h1>
        <p class="body-text">{body_text}</p>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Scanner Bar Text Reveal - Orchestration
document.addEventListener('DOMContentLoaded', () => {{
    const observerOptions = {{
        root: null,
        rootMargin: '0px',
        threshold: 0.2 // Trigger when 20% of the element is visible
    }};

    const observer = new IntersectionObserver((entries) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                // Add class to trigger CSS animation
                entry.target.classList.add('animate');
                // Stop observing once the animation has been triggered
                observer.unobserve(entry.target);
            }}
        }});
    }}, observerOptions);

    // Observe both the title and the body text
    const animatedElements = document.querySelectorAll('.reveal-text, .body-text');
    animatedElements.forEach(el => observer.observe(el));
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

* **Accessibility**: 
  - Text remains perfectly screen-reader friendly because standard HTML `<h1>` and `<p>` tags are used. No pseudo-elements or cloned duplicate nodes hide the semantic structure.
  - In a production environment, `prefers-reduced-motion: reduce` media queries should be implemented to disable the sweeping keyframes and instantly set `background-size: 100% 100%` for sensitive users.
* **Performance**: 
  - The animation exclusively alters `background-size` and `background-position`. While slightly more expensive than compositing transforms like `translate`, the area is constrained by the clipping path.
  - Intersection Observer ensures the animation only consumes resources when naturally scrolled into the user's viewport.