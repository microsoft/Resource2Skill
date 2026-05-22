### 1. High-level Design Pattern Extraction

> **Skill Name**: Split-Content Central-Subject Hero

* **Core Visual Mechanism**: A full-height hero section characterized by a balanced, symmetrical composition. A large central visual subject (usually a portrait or product) is anchored at the bottom center. Typography is split into two distinct columns framing the subject: a bold, commanding headline block on the left, and supporting, slightly offset text (like quotes or features) on the right. The background layers subtle geometric patterns to add depth without distracting from the foreground.
* **Why Use This Skill (Rationale)**: This layout solves the classic "text overlaying image" readability problem. By centering the subject and flanking it with text, you maintain high typographic contrast and legibility while still featuring a prominent, humanizing, or product-focused central element. It creates an editorial, magazine-like feel.
* **Overall Applicability**: Ideal for personal portfolios (where the portrait is the creator), product landing pages (where a device sits in the center), and SaaS homepages aiming for a bold, personality-driven aesthetic.
* **Value Addition**: Compared to a standard left-aligned hero, this pattern creates a dramatic sense of scale and depth. The separation of introductory text and secondary quotes forces a clear visual hierarchy, guiding the user's eye across the entire viewport.
* **Browser Compatibility**: Fully supported in modern browsers. Uses CSS Flexbox, `clamp()` for fluid typography, and CSS custom variables. No legacy browser support issues.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**: Deep background (`#0f172a` for dark mode) overlaid with a subtle repeating pattern (`rgba(255,255,255,0.05)`). A vivid accent color (`#c13584`) is used sparingly for buttons and structural borders.
  - **Typographic Hierarchy**: Heavy, uppercase sans-serif (`font-weight: 900`) for the main `<h1>` to establish authority. The secondary text uses a standard weight with increased line-height (`1.6`) for readability.
  - **CSS Properties**: Uses `radial-gradient` for generating a pure-CSS background pattern, `border-left` for structured quotes, and `transform` for centering and parallax offsets.

* **Step B: Layout & Compositional Style**
  - **Layout System**: The primary container uses CSS Flexbox (`display: flex; justify-content: space-between; align-items: center;`) combined with a large `gap` to naturally separate the left and right text blocks, leaving an empty channel in the center.
  - **Layering (Z-index)**:
    - Layer 0: Background color and CSS pattern.
    - Layer 1: Absolute-positioned central subject (portrait), anchored to the `bottom` and centered via `left: 50%; transform: translateX(-50%)`.
    - Layer 2: Relative-positioned Flexbox container holding the text, ensuring text remains clickable and selectable above the imagery.

* **Step C: Interactive Behavior & Animations**
  - **Hover Effects**: The primary call-to-action button features a smooth `background-color` transition.
  - **JavaScript Enhancements**: Adding a subtle, cursor-driven parallax effect to the central subject dramatically enhances the perception of depth, separating the foreground text from the background layers.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Background Pattern | CSS `radial-gradient` | Creates a scalable, lightweight geometric texture without requiring external image assets. |
| Split Layout | CSS Flexbox + `gap` | Cleaner and more responsive than the absolute/relative pixel-pushing (e.g., `right: 20vh`) shown in the raw tutorial. |
| Central Subject | Inline SVG + Absolute Positioning | Provides a robust placeholder that demonstrates the framing effect without relying on external image hosting. |
| Depth Perception | JS `mousemove` Listener | Adds a lightweight parallax translation to the central subject, simulating the spatial depth intended by the design. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "WELCOME<br>TO MY FIRST<br>WEBSITE",
    body_text: str = "Nam interdum felis at felis placerat, sed varius massa ultricies. Integer quis nisi non dolor scelerisque efficitur at sed turpis.",
    color_scheme: str = "dark",
    accent_color: str = "#c13584",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Split-Content Central-Subject Hero effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme derivation
    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_color = "#f8fafc"
        text_muted = "rgba(248, 250, 252, 0.75)"
        pattern_color = "rgba(255, 255, 255, 0.04)"
        subject_color = "#1e293b"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        text_muted = "rgba(15, 23, 42, 0.75)"
        pattern_color = "rgba(0, 0, 0, 0.04)"
        subject_color = "#e2e8f0"

    # Hover color derivation (slightly darker/lighter)
    accent_hover = f"{accent_color}dd"

    css = f"""/* Split-Content Central-Subject Hero */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --accent-hover: {accent_hover};
    --pattern: {pattern_color};
    --subject: {subject_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Roboto', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}}

.hero-container {{
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    background-color: var(--bg);
    /* Procedural geometric background pattern */
    background-image: 
        linear-gradient(45deg, var(--pattern) 25%, transparent 25%, transparent 75%, var(--pattern) 75%, var(--pattern)),
        linear-gradient(45deg, var(--pattern) 25%, transparent 25%, transparent 75%, var(--pattern) 75%, var(--pattern));
    background-size: 60px 60px;
    background-position: 0 0, 30px 30px;
    border-radius: 12px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}}

/* Central Subject Layer */
.portrait-layer {{
    position: absolute;
    bottom: -20px;
    left: 50%;
    transform: translateX(-50%);
    width: clamp(280px, 40%, 450px);
    height: 85%;
    z-index: 1;
    display: flex;
    align-items: flex-end;
    justify-content: center;
    will-change: transform;
    transition: transform 0.1s ease-out;
}}

.portrait-layer svg {{
    width: 100%;
    height: auto;
    color: var(--subject);
    filter: drop-shadow(0 20px 30px rgba(0,0,0,0.4));
}}

/* Typography Layout Layer */
.content-wrapper {{
    position: relative;
    z-index: 2;
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    padding: 0 5%;
    /* Creates the central void for the portrait */
    gap: clamp(40px, 25%, 350px);
    pointer-events: none; /* Let clicks pass through empty space */
}}

.main-intro, .main-quotes {{
    flex: 1;
    pointer-events: auto; /* Re-enable clicks on text blocks */
}}

.main-intro {{
    max-width: 480px;
}}

.main-intro h1 {{
    font-size: clamp(36px, 4vw, 72px);
    line-height: 1.05;
    font-weight: 900;
    text-transform: uppercase;
    margin-bottom: 24px;
    letter-spacing: -0.02em;
}}

.main-intro p {{
    font-size: 18px;
    line-height: 1.6;
    color: var(--text-muted);
    margin-bottom: 32px;
}}

.btn {{
    display: inline-block;
    background-color: var(--accent);
    color: #ffffff;
    padding: 14px 28px;
    text-decoration: none;
    font-weight: 700;
    text-transform: uppercase;
    font-size: 14px;
    letter-spacing: 1px;
    border-radius: 4px;
    transition: background-color 0.2s ease, transform 0.2s ease;
}}

.btn:hover {{
    background-color: var(--accent-hover);
    transform: translateY(-2px);
}}

.main-quotes {{
    max-width: 380px;
    border-left: 4px solid var(--accent);
    padding-left: 24px;
    display: flex;
    flex-direction: column;
    gap: 32px;
}}

.quote-block p {{
    font-size: 15px;
    line-height: 1.7;
    color: var(--text-muted);
    font-style: italic;
}}

.quote-block span {{
    display: block;
    margin-top: 12px;
    font-size: 14px;
    font-weight: 700;
    color: var(--text);
    font-style: normal;
}}

/* Responsive behavior */
@media (max-width: 900px) {{
    .content-wrapper {{
        flex-direction: column;
        text-align: center;
        gap: 60px;
        padding: 40px 20px;
        background: radial-gradient(circle at center, var(--bg) 40%, transparent 80%);
    }}
    .portrait-layer {{
        opacity: 0.2; /* Subdue image on mobile so text remains readable */
    }}
    .main-quotes {{
        border-left: none;
        border-top: 4px solid var(--accent);
        padding-left: 0;
        padding-top: 24px;
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Split-Content Parallax Hero</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,400;0,700;0,900;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="hero-container">
        
        <!-- Central Subject / Portrait Layer -->
        <div class="portrait-layer" id="parallax-subject">
            <!-- Generic human silhouette placeholder SVG -->
            <svg viewBox="0 0 200 250" xmlns="http://www.w3.org/2000/svg">
                <!-- Shoulders / Torso -->
                <path d="M100,100 C150,100 180,140 190,250 L10,250 C20,140 50,100 100,100 Z" fill="currentColor"/>
                <!-- Head -->
                <circle cx="100" cy="65" r="45" fill="currentColor"/>
            </svg>
        </div>

        <!-- Typography Layer -->
        <div class="content-wrapper">
            
            <div class="main-intro">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
                <a href="#" class="btn">My Work</a>
            </div>

            <div class="main-quotes">
                <div class="quote-block">
                    <p>"The more that you read, the more things you will know. The more that you learn, the more places you'll go."</p>
                    <span>- Dr. Seuss</span>
                </div>
                <div class="quote-block">
                    <p>"For the best return on your money, pour your purse into your head."</p>
                    <span>- Benjamin Franklin</span>
                </div>
            </div>

        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Adds lightweight cursor parallax to the central subject
document.addEventListener('DOMContentLoaded', () => {
    const container = document.querySelector('.hero-container');
    const subject = document.getElementById('parallax-subject');

    if (!container || !subject) return;

    container.addEventListener('mousemove', (e) => {
        // Calculate cursor position relative to container center (-1 to 1)
        const rect = container.getBoundingClientRect();
        const xPos = (e.clientX - rect.left) / rect.width - 0.5;
        const yPos = (e.clientY - rect.top) / rect.height - 0.5;

        // Subtle movement constraints (adjust multipliers for stronger effect)
        const xOffset = xPos * 30; // max 15px movement
        const yOffset = yPos * 15; // max 7.5px movement

        // Apply transform. Note: we keep the -50% base translation required for centering
        subject.style.transform = `translateX(calc(-50% + ${xOffset}px)) translateY(${yOffset}px)`;
    });

    // Reset position on mouse leave
    container.addEventListener('mouseleave', () => {
        subject.style.transform = `translateX(-50%) translateY(0px)`;
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

* **Accessibility**: 
  - Text nodes have a dedicated `--text-muted` fallback color mapped ensuring proper contrast ratios against the background while distinguishing from the primary `h1` text. 
  - The decorative SVG placeholder correctly lacks specific `aria` roles as it is purely decorative; however, if replaced with an actual `<img>`, it should have an empty `alt=""` attribute to hide it from screen readers, preventing redundant information as the surrounding text carries the semantic context.
* **Performance**:
  - The parallax calculation uses `getBoundingClientRect()` within a `mousemove` listener. While lightweight in this context, for complex production sites, this operation could be throttled via `requestAnimationFrame` to prevent main-thread jank during rapid mouse movements.
  - The `will-change: transform;` property is applied to the central subject to hardware-accelerate the parallax transformation, maintaining smooth 60fps rendering.
  - Using CSS pseudo-gradients (`linear-gradient`) instead of importing large `.png` textures significantly reduces HTTP requests and Time-to-Interactive (TTI).