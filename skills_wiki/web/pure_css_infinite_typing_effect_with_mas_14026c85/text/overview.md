# Pure CSS Infinite Typing Effect with Mask Block

## Analysis

Here is the comprehensive extraction of the web development skill from the tutorial, complete with reusable and configurable code.

### 1. High-level Design Pattern Extraction

> **Skill Name**: Pure CSS Infinite Typing Effect with Mask Block

* **Core Visual Mechanism**: This component creates a continuous typewriter effect that cycles through a list of words. Instead of using JavaScript to manipulate text content character by character, it uses a clever pure CSS trick: an absolutely positioned "masking block" (`::after` pseudo-element) covers the text (`::before` pseudo-element) and matches the background color. By animating the `width` of this mask from 100% to 0% using the `steps()` timing function, it reveals the text underneath in discrete, character-sized chunks, perfectly simulating a typing motion. The left border of this mask acts as the blinking cursor.
* **Why Use This Skill (Rationale)**: This technique captures user attention immediately and adds a dynamic, dynamic "developer/tech" aesthetic. It allows a single headline to deliver multiple keywords (e.g., roles, features, or benefits) without taking up vertical real estate or requiring the user to scroll or click.
* **Overall Applicability**: Ideal for portfolio hero sections (e.g., "I'm a Developer/Designer/Creator"), SaaS landing page headers ("Build better APIs/Websites/Tools"), or dynamic terminal-style command displays.
* **Value Addition**: It delivers the exact visual flair of a complex JavaScript typing library using only lightweight CSS animations. It is highly performant because it relies on standard CSS keyframe interpolation.
* **Browser Compatibility**: Excellent. Relies on standard CSS `@keyframes`, pseudo-elements (`::before`, `::after`), and the `steps()` timing function. Fully supported in all modern browsers (Chrome, Firefox, Safari, Edge).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **HTML Structure**: A minimalistic structure requiring only a wrapper `div` and a single empty `span`. The actual rotating text and the mask are entirely generated via CSS pseudo-elements.
  - **Color Logic**: The effect mandates a solid background color (e.g., dark slate `#2f3542`) because the masking block must perfectly blend into the background to hide the text. The dynamic text and cursor use a contrasting, vibrant accent color (e.g., coral `#ff7f50`).
  - **Typographic Hierarchy**: Uses a bold, geometric sans-serif font (Montserrat) at a large size (34px) to make the typing action clearly legible.
  - **CSS Properties**: `content` swapping inside keyframes, `steps()` timing function for chunky animation, and `calc()` for precise padding and cursor overhang.

* **Step B: Layout & Compositional Style**
  - **Layout System**: Flexbox is used to center the headline in the viewport. `display: inline-block` on the target `span` ensures it automatically resizes its width to fit whichever word is currently being displayed via the `content` property.
  - **Spatial Feel**: The cursor slightly overhangs the end of the text. This is achieved by setting the mask to `right: -8px` and `width: calc(100% + 8px)`, giving the cursor room to blink without touching the last letter.

* **Step C: Interactive Behavior & Animations**
  - **Typing Animation (`typing` keyframes)**: Animates the mask width. `width: 100%` covers the text (empty state). `width: 0%` reveals the text (typed state).
  - **Text Swapping (`words` keyframes)**: Instantly changes the `content` of the `::before` element at mathematically calculated intervals.
  - **Cursor Blinking (`cursor` keyframes)**: Alternates the `border-left-color` between the accent color and `transparent`.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Typing character reveal | CSS `width` animation + `steps()` | The `steps()` function creates discrete jumps instead of smooth sliding, perfectly faking a typewriter. |
| Text replacement | CSS `content` in `@keyframes` | Allows swapping words strictly in CSS without JavaScript DOM manipulation. |
| Blinking Cursor | CSS animated `border-left` | Applying the border to the moving mask block ensures the cursor naturally follows the "typing" edge. |

> **Feasibility Assessment**: 100%. The provided Python generator dynamically calculates the correct CSS keyframe percentages based on any provided list of words, making the pure-CSS logic robust and highly configurable.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "I'm a",
    words_list: list = None,
    color_scheme: str = "dark",
    accent_color: str = "#ff7f50",
    width_px: int = 1000,
    height_px: int = 600,
    **kwargs,
) -> dict:
    import os

    # Default word list if none provided
    if not words_list:
        words_list = ["Youtuber", "Blogger", "Developer", "Designer", "Gamer"]

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#2f3542" # Muted dark slate
        text_color = "#ffffff"
    else:
        bg_color = "#f4f6f8"
        text_color = "#2d3436"

    # --- Core Algorithmic Keyframe Generation ---
    # To make this pure CSS effect parameterizable, we must dynamically calculate 
    # the exact percentages for the keyframes based on the number of words.
    n_words = len(words_list)
    cycle_pct = 100 / n_words
    duration = n_words * 4  # 4 seconds allocated per word

    # Dynamic step count based on the longest word ensures smooth typing chunks
    max_len = max([len(w) for w in words_list])
    steps_count = max(10, max_len + 2)

    width_0_pcts = []
    width_100_pcts = [0.0]
    content_keyframes = ""

    for i, word in enumerate(words_list):
        start = i * cycle_pct
        
        # Timeline logic for a single word cycle:
        # Phase 1: Hold empty (mask full width)
        # Phase 2: Type out (mask shrinks to 0)
        # Phase 3: Hold text (mask stays 0)
        # Phase 4: Delete back (mask grows to full width)
        
        width_100_pcts.append(start + cycle_pct * 0.25)
        width_0_pcts.append(start + cycle_pct * 0.50)
        width_0_pcts.append(start + cycle_pct * 0.75)
        width_100_pcts.append(start + cycle_pct)

        # Content swap happens exactly at the start of its cycle
        content_keyframes += f"    {start:g}% {{ content: '{word}'; }}\n"

    # Format percentage lists for CSS selectors
    width_100_pcts = sorted(list(set(width_100_pcts)))
    width_0_pcts = sorted(list(set(width_0_pcts)))
    w0_selectors = ", ".join([f"{p:g}%" for p in width_0_pcts])
    w100_selectors = ", ".join([f"{p:g}%" for p in width_100_pcts])

    # === CSS ===
    css = f"""/* Pure CSS Typing Effect */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --duration: {duration}s;
    --steps: {steps_count};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Montserrat', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
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

.typing-wrapper {{
    font-size: 2.5rem;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
}}

.prefix {{
    margin-right: 12px;
}}

/* The parent span adapts to the width of its ::before content automatically */
.animated-text {{
    position: relative;
    display: inline-block;
}}

/* ::before holds the actual changing text */
.animated-text::before {{
    content: "{words_list[0]}"; 
    color: var(--accent);
    animation: words var(--duration) infinite;
}}

/* ::after acts as a mask block covering the text, shrinking/growing to simulate typing */
.animated-text::after {{
    content: "";
    position: absolute;
    right: -8px; /* Slight overhang for the cursor */
    top: 0;
    height: 100%;
    width: calc(100% + 8px);
    
    /* CRITICAL: Background must perfectly match the container background */
    background-color: var(--bg); 
    
    /* The left edge of the mask acts as the cursor */
    border-left: 3px solid var(--accent);
    
    animation:
        cursor 0.8s infinite,
        typing var(--duration) steps(var(--steps)) infinite;
}}

/* Blinking cursor animation */
@keyframes cursor {{
    0%, 100% {{ border-left-color: transparent; }}
    50% {{ border-left-color: var(--accent); }}
}}

/* Word swapping animation */
@keyframes words {{
{content_keyframes}
}}

/* Typing (mask width) animation */
@keyframes typing {{
    {w0_selectors} {{
        width: 0;
    }}
    {w100_selectors} {{
        width: calc(100% + 8px);
    }}
}}

/* Responsive Scaling */
@media (max-width: 768px) {{
    .typing-wrapper {{
        font-size: 1.8rem;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CSS Typing Animation</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="typing-wrapper">
            <span class="prefix">{title_text}</span>
            <span class="animated-text"></span>
        </div>
    </div>
</body>
</html>"""

    # === Write files ===
    files = []
    for fname, content in [("index.html", html), ("style.css", css)]:
        path = os.path.join(output_dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        files.append(path)

    return {
        "html": html,
        "css": css,
        "js": "", # No JavaScript required for this effect
        "files": files,
    }
```

### 4. Accessibility & Performance Notes

* **Accessibility constraint**: Because the text swapping relies entirely on CSS `content` properties inside pseudo-elements, screen readers typically will only read the initial DOM content (which is empty in the `span`) and may not announce the dynamically rotating words. If the rotating words contain critical information, consider adding a visually hidden `.sr-only` span containing the full list of words for screen reader context.
* **Reduced Motion**: For users with vestibular disorders, blinking and rapid typing effects can be disruptive. In a production environment, wrap the animations in a `@media (prefers-reduced-motion: reduce)` block and simply display a static string (e.g., "Developer & Designer") without the typing animations.
* **Performance**: This method is exceptionally performant compared to JavaScript typing libraries. It causes no DOM reflows via script injection, relying entirely on browser-optimized CSS animation engines. The limitation is that it requires a solid background color (no gradients or images directly behind the text) for the `::after` mask to function correctly.