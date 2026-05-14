# Pure CSS Character Illustration

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Pure CSS Character Illustration

* **Core Visual Mechanism**: This technique uses pure CSS to draw complex, recognizable illustrations (in this case, a cartoon character avatar). The signature method is **Border Masking**—assembling simple geometric `div`s via absolute positioning and carefully overlapping their backgrounds to hide specific border segments. This fuses multiple disparate shapes (a rectangle for a head, a rounded square for a nose) into a single, seamless silhouette with a unified outer stroke.
* **Why Use This Skill (Rationale)**: CSS art is lightweight, infinitely scalable, and inherently animatable without the overhead of SVG DOM parsing or external image requests. It forces a component-based way of thinking about visual geometry. Adding subtle CSS animations (like blinking) or JS tracking (eyes following the cursor) gives the character an organic, lively feel that engages users deeply.
* **Overall Applicability**: Perfect for creative 404 pages, onboarding mascots, interactive avatars, loader animations, and Easter eggs. It showcases technical craftsmanship and adds a layer of delight to otherwise standard interfaces.
* **Value Addition**: It replaces static PNGs/SVGs with a living, code-based entity. Because it is built from DOM elements, it can react to user states dynamically (e.g., character smiles when a form is valid, looks down at an input field, or changes hair color based on a theme).
* **Browser Compatibility**: Excellent. Relies on fundamental CSS properties (`absolute` positioning, `border-radius`, `transform`, `z-index`) supported universally. 

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**: Uses a flat, vibrant, comic-book style. The skin tone (`#fcd5b4` or `#fee1c3`), a vivid accent for the hair, and solid `#111` for the ink lines. 
  - **Structural Components**: 
    - **Face Base**: A rounded rectangle.
    - **Nose & Ear**: Overlapping shapes with asymmetric `border-radius` (e.g., `25px 0 0 25px`).
    - **Hair**: CSS triangles created using 0-height/width elements with thick, colored bottom borders and transparent side borders.
    - **Eyes**: Circles with absolute-positioned inner pupils.
  - **CSS Drivers**: `border-width` combined with `box-sizing: border-box` is critical. If a 50px wide nose with a 2px border is shifted `-48px` left, its background perfectly aligns with the inner edge of the face's border, hiding the connecting seam.

* **Step B: Layout & Compositional Style**
  - The character uses `position: relative` for its main wrapper, while every anatomical part uses `position: absolute`.
  - **Z-Index Layering**: Creates 3D depth in a profile view.
    - `z-index: 5`: Back eye, back eyebrow, back hair, neck (behind the face).
    - `z-index: 10`: Face base.
    - `z-index: 15`: Nose, Ear (on top to mask the face's border).
    - `z-index: 20`: Front eye, mouth (highest priority).

* **Step C: Interactive Behavior & Animations**
  - **Blinking**: A CSS keyframe animation scales the eyes vertically (`transform: scaleY(0.1)`) for a fraction of a second, looping infinitely to simulate organic blinking.
  - **Floating**: A slow, infinite vertical translation on the character wrapper makes the avatar feel alive.
  - **Gaze Tracking**: JavaScript calculates the angle and distance from the cursor to the eyes using `Math.atan2` and `Math.hypot`, translating the pupils slightly within the bounds of the sclera (white part of the eye).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Geometric Character** | Pure CSS (`div`s + `border-radius`) | Perfectly reproduces the tutorial's focus on DOM-based illustration. |
| **Seamless Outlines** | CSS Border Masking | Placing elements exactly over border seams with specific borders removed (`border-right: none`) fuses shapes perfectly. |
| **Spiky Hair** | CSS Border Triangles | Avoids SVGs; uses the tutorial's method of transparent adjacent borders. |
| **Eye Tracking** | JS `mousemove` + Math | Adds an interactive "wow" factor, building upon the static CSS shapes. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "CSS Avatar",
    body_text: str = "A pure CSS illustration built with absolute positioning and border masking.",
    color_scheme: str = "dark",
    accent_color: str = "#20a44a",
    width_px: int = 1000,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Pure CSS Character Illustration effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Convert hex accent to RGB for rgba() usage
    hex_color = accent_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    accent_rgb = f"{rgb[0]}, {rgb[1]}, {rgb[2]}"

    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_color = "#f8fafc"
        text_muted = "#94a3b8"
        skin_color = "#fcd5b4"
        line_color = "#111111"
        shirt_color = "#334155"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        text_muted = "#64748b"
        skin_color = "#fee1c3"
        line_color = "#111111"
        shirt_color = "#ffffff"

    css = f"""/* Pure CSS Character Illustration */
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
    --accent-rgb: {accent_rgb};
    --skin: {skin_color};
    --line: {line_color};
    --shirt: {shirt_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
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
    position: relative;
}}

.layout-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 60px;
    width: 100%;
    max-width: 1000px;
    padding: 40px;
    align-items: center;
}}

/* --- Text Content --- */
.text-content {{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}}

.badge {{
    display: inline-block;
    padding: 6px 14px;
    background: rgba(var(--accent-rgb), 0.1);
    color: var(--accent);
    border: 1px solid rgba(var(--accent-rgb), 0.3);
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 20px;
}}

.title {{
    font-size: 3rem;
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 20px;
}}

.body-text {{
    font-size: 1.125rem;
    line-height: 1.6;
    color: var(--text-muted);
    margin-bottom: 30px;
}}

/* --- CSS Art Container --- */
.art-content {{
    display: flex;
    justify-content: center;
    align-items: center;
    height: 400px;
}}

.character-wrapper {{
    animation: float 6s infinite ease-in-out;
}}

.character {{
    position: relative;
    width: 60px;
    height: 180px;
    transform: scale(1.6);
    /* Offset scaling visually */
    transform-origin: center center;
}}

/* --- Character Anatomy --- */
.head-base {{
    position: absolute;
    left: 0;
    top: 30px;
    width: 60px;
    height: 150px;
    background: var(--skin);
    border: 2px solid var(--line);
    border-radius: 10px 10px 20px 20px;
    z-index: 10;
}}

/* Border Masking Technique: Nose covers left border of head-base */
.nose {{
    position: absolute;
    width: 50px;
    height: 40px;
    background: var(--skin);
    border: 2px solid var(--line);
    border-right: none;
    border-radius: 20px 0 0 20px;
    left: -48px; /* Perfectly aligns background with inner edge of face border */
    top: 60px;
    z-index: 15;
}}

/* Border Masking Technique: Ear covers right border of head-base */
.ear {{
    position: absolute;
    width: 20px;
    height: 30px;
    background: var(--skin);
    border: 2px solid var(--line);
    border-left: none;
    border-radius: 0 15px 15px 0;
    right: -18px; 
    top: 80px;
    z-index: 15;
}}

.eye-front, .eye-back {{
    position: absolute;
    background: #fff;
    border: 2px solid var(--line);
    border-radius: 50%;
    animation: blink 4.5s infinite;
    transform-origin: center 70%;
}}

.eye-front {{
    width: 35px;
    height: 50px;
    left: -20px;
    top: 15px;
    z-index: 20;
}}

.eye-back {{
    width: 32px;
    height: 44px;
    left: 36px;
    top: 5px;
    z-index: 5; /* Hidden behind face to give 3D perspective */
}}

.pupil {{
    position: absolute;
    width: 8px;
    height: 8px;
    background: var(--line);
    border-radius: 50%;
    left: 50%;
    top: 50%;
    margin-left: -4px;
    margin-top: -4px;
    transition: transform 0.1s ease-out;
}}

.eyebrow {{
    position: absolute;
    width: 25px;
    height: 6px;
    background: var(--accent);
    border-radius: 3px;
    z-index: 25;
}}

.eyebrow-front {{
    top: 2px;
    left: -25px;
    transform: rotate(-10deg);
}}

.eyebrow-back {{
    top: -5px;
    left: 30px;
    transform: rotate(15deg);
    z-index: 6;
}}

.mouth {{
    position: absolute;
    width: 25px;
    height: 15px;
    border-bottom: 2px solid var(--line);
    border-radius: 0 0 50% 50%;
    left: -5px;
    top: 110px;
    z-index: 20;
    transform: rotate(-10deg);
}}

/* --- CSS Triangles for Hair --- */
.hair-group {{
    position: absolute;
    top: -15px;
    left: 5px;
    z-index: 5;
}}

.spike {{
    position: absolute;
    width: 0;
    height: 0;
    border-left: 8px solid transparent;
    border-right: 8px solid transparent;
    transform-origin: bottom center;
}}

.spike1 {{ border-bottom: 45px solid var(--accent); transform: rotate(-40deg); left: -15px; top: 0px; }}
.spike2 {{ border-bottom: 55px solid var(--accent); transform: rotate(-15deg); left: 0px; top: -10px; }}
.spike3 {{ border-bottom: 60px solid var(--accent); transform: rotate(10deg); left: 15px; top: -15px; }}
.spike4 {{ border-bottom: 45px solid var(--accent); transform: rotate(35deg); left: 30px; top: 0px; }}

/* --- Body --- */
.neck {{
    position: absolute;
    width: 20px;
    height: 40px;
    background: var(--skin);
    border: 2px solid var(--line);
    border-top: none;
    left: 20px;
    top: 178px;
    z-index: 5;
}}

.shirt {{
    position: absolute;
    width: 80px;
    height: 40px;
    background: var(--shirt);
    border: 2px solid var(--line);
    border-radius: 40px 40px 0 0;
    left: -10px;
    top: 216px;
    z-index: 6;
}}

/* --- Animations --- */
@keyframes blink {{
    0%, 96%, 100% {{ transform: scaleY(1); }}
    98% {{ transform: scaleY(0.1); }}
}}

@keyframes float {{
    0%, 100% {{ transform: translateY(0); }}
    50% {{ transform: translateY(-12px); }}
}}

@media (max-width: 768px) {{
    .layout-grid {{ grid-template-columns: 1fr; text-align: center; gap: 20px; }}
    .text-content {{ align-items: center; }}
    .title {{ font-size: 2.5rem; }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="layout-grid">
            <div class="text-content">
                <div class="badge">CSS Illustration</div>
                <h1 class="title">{title_text}</h1>
                <p class="body-text">{body_text}</p>
            </div>
            
            <div class="art-content">
                <div class="character-wrapper">
                    <div class="character">
                        <div class="hair-group">
                            <div class="spike spike1"></div>
                            <div class="spike spike2"></div>
                            <div class="spike spike3"></div>
                            <div class="spike spike4"></div>
                        </div>
                        
                        <div class="neck"></div>
                        <div class="shirt"></div>
                        
                        <div class="eyebrow eyebrow-back"></div>
                        <div class="eye-back"><div class="pupil"></div></div>
                        
                        <div class="head-base"></div>
                        <div class="ear"></div>
                        <div class="nose"></div>
                        
                        <div class="eyebrow eyebrow-front"></div>
                        <div class="eye-front"><div class="pupil"></div></div>
                        <div class="mouth"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Pure CSS Character - Interactive Gaze Tracking
document.addEventListener('DOMContentLoaded', () => {
    const character = document.querySelector('.character');
    const pupils = document.querySelectorAll('.pupil');
    
    // Add eye tracking behavior
    document.addEventListener('mousemove', (e) => {
        if (!character) return;
        
        pupils.forEach(pupil => {
            const eye = pupil.parentElement;
            const rect = eye.getBoundingClientRect();
            
            // Find absolute center of the eye
            const eyeCenterX = rect.left + rect.width / 2;
            const eyeCenterY = rect.top + rect.height / 2;
            
            // Calculate angle and distance to cursor
            const angle = Math.atan2(e.clientY - eyeCenterY, e.clientX - eyeCenterX);
            // Cap the distance so pupil stays inside the eye (max 8px radius)
            const distance = Math.min(8, Math.hypot(e.clientX - eyeCenterX, e.clientY - eyeCenterY) / 15);
            
            // Calculate X/Y offsets
            const x = distance * Math.cos(angle);
            const y = distance * Math.sin(angle);
            
            // Apply translation on top of the CSS-defined absolute centering
            pupil.style.transform = `translate(${x}px, ${y}px)`;
        });
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