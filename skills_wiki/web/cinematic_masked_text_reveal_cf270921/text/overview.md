# Cinematic Masked Text Reveal

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Cinematic Masked Text Reveal

* **Core Visual Mechanism**: This component creates a dramatic, multi-stage typographical entrance. It relies on a CSS "masking" trick: the primary heading has a solid background color matching the page background and a negative bottom margin, causing it to overlap and completely hide the secondary text. By animating `letter-spacing` (creating a tracking-in effect) and then animating the `margin-bottom` back to a positive value, the primary text visually "splits" to reveal the hidden subtitle underneath.
* **Why Use This Skill (Rationale)**: This creates a highly engaging, story-telling feel for text entrances. By separating the visual reveals into phases (appear wide &rarr; contract &rarr; split to reveal subtitle), it guides the user's eye and builds anticipation.
* **Overall Applicability**: Perfect for hero sections on landing pages, cinematic portfolio intros, video game splash screens, or any minimalist design where typography is the primary visual anchor. 
* **Value Addition**: Transforms static text into an orchestrated motion sequence without requiring complex JavaScript, SVG masks, or WebGL. It leverages basic CSS box-model mechanics creatively.
* **Browser Compatibility**: Fully supported across all modern browsers. Uses standard CSS `@keyframes`, flexbox, and basic box-model properties.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**: High contrast minimalist palette. Dark background (`#000000` or `#0d111c`), bright white primary text (`#ffffff`), and a vivid accent color for the secondary text (e.g., `#6ab04c` green).
  - **Typographic Hierarchy**: Bold, geometric sans-serif (like Inter or Roboto). The primary text is massive (e.g., `60px` or `5rem`) and heavily weighted (`700`+). The secondary text is roughly half the size to establish clear dominance.
  - **CSS Properties**: `letter-spacing` (for tracking animation), `margin-bottom` (for spatial manipulation), `background-color` (crucial for creating the solid mask), and `z-index`.

* **Step B: Layout & Compositional Style**
  - Uses CSS Flexbox (`flex-direction: column; align-items: center;`) to center the text blocks cleanly.
  - The primary text dictates the flow. By using `margin-bottom: -0.7em`, it literally pulls the secondary text up into its own bounding box, rendering on top of it due to `z-index: 2` and a solid background.

* **Step C: Interactive Behavior & Animations**
  - **Phase 1 (0-20%)**: Text fades in from transparent while widely tracked (`letter-spacing: 0.5em`).
  - **Phase 2 (20-60%)**: Tracking smoothly contracts to normal spacing.
  - **Phase 3 (60-75%)**: A brief holding pause to let the user register the primary word.
  - **Phase 4 (75-100%)**: The `margin-bottom` transitions to a positive value, pushing the hidden secondary text downward (and moving the primary text upward relative to center), creating a sliding curtain reveal.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Text Entrance** | CSS `@keyframes` `letter-spacing` | Native, performant way to animate typographical tracking. |
| **Reveal Masking** | CSS Background + Negative Margin | A clever, pure CSS technique that avoids complex `clip-path` calculations. By giving the top text a solid background and `z-index`, it acts as a physical curtain over the text below it. |
| **Centering** | CSS Flexbox | Robust alignment that naturally handles the height changes caused by the margin animation. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "WELCOME IN",
    body_text: str = "DARKCODE",
    color_scheme: str = "dark",
    accent_color: str = "#6ab04c",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Cinematic Masked Text Reveal visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#08080c" # Deep black/dark
        text_color = "#ffffff"
    else:
        bg_color = "#f4f4f5" # Off-white
        text_color = "#121212"

    # === CSS ===
    css = f"""/* Cinematic Masked Text Reveal */
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
    overflow: hidden;
}}

.container {{
    width: var(--width);
    height: var(--height);
    display: flex;
    align-items: center;
    justify-content: center;
}}

.reveal-wrapper {{
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
    /* Ensure the entire block remains centered during expansion */
    justify-content: center; 
}}

.primary-text {{
    font-size: clamp(3rem, 6vw, 5.5rem);
    font-weight: 800;
    text-transform: uppercase;
    color: var(--text);
    /* The core trick: solid background to mask the text underneath */
    background: var(--bg);
    position: relative;
    z-index: 2;
    /* Padding prevents text clipping during extreme letter-spacing */
    padding: 0.1em 0.5em; 
    line-height: 1.1;
    
    /* Animation definition */
    animation: sequence-reveal 3.5s cubic-bezier(0.25, 1, 0.5, 1) forwards;
}}

.secondary-text {{
    font-size: clamp(1.2rem, 2.5vw, 2.2rem);
    font-weight: 600;
    text-transform: uppercase;
    color: var(--accent);
    position: relative;
    z-index: 1;
    letter-spacing: 0.1em;
}}

@keyframes sequence-reveal {{
    0% {{
        color: transparent;
        /* Pulls the secondary text up to be hidden behind the primary text's background */
        margin-bottom: -0.7em; 
        letter-spacing: 0.6em;
        transform: translateY(10px);
    }}
    20% {{
        color: var(--text);
        margin-bottom: -0.7em;
        letter-spacing: 0.5em;
        transform: translateY(0);
    }}
    60% {{
        /* Text finishes contracting */
        margin-bottom: -0.7em;
        letter-spacing: 0.1em;
    }}
    75% {{
        /* Pause to read the word before revealing */
        margin-bottom: -0.7em;
        letter-spacing: 0.1em;
    }}
    100% {{
        /* Pushes the secondary text down, revealing it from behind the mask */
        margin-bottom: 0.25em; 
        letter-spacing: 0.1em;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text} Reveal</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="reveal-wrapper">
            <h1 class="primary-text">{title_text}</h1>
            <h2 class="secondary-text">{body_text}</h2>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Cinematic Masked Text Reveal
// This component relies entirely on CSS keyframes and box-model manipulations.
// JavaScript can be used here to re-trigger the animation on demand.

document.addEventListener('DOMContentLoaded', () => {{
    const primaryText = document.querySelector('.primary-text');
    
    // Example: Click the container to replay the animation
    document.querySelector('.container').addEventListener('click', () => {{
        // Force reflow to restart CSS animation
        primaryText.style.animation = 'none';
        void primaryText.offsetWidth; 
        primaryText.style.animation = 'sequence-reveal 3.5s cubic-bezier(0.25, 1, 0.5, 1) forwards';
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