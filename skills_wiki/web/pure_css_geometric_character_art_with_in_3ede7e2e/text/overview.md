# Pure CSS Geometric Character Art (with Interactive Eye Tracking)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Pure CSS Geometric Character Art (with Interactive Eye Tracking)

* **Core Visual Mechanism**: This pattern constructs vector-style illustrations exclusively using semantic HTML `<div>` elements and CSS. It relies heavily on absolute positioning within a relative container, careful manipulation of `border-radius` (turning squares into circles or ovals), and strategic omission of specific borders (e.g., `border-bottom: transparent`) to create open curves like smiles and noses. Pseudo-elements (`::before`, `::after`) are used extensively to draw grouped, repeated elements (like inner pupils or multiple eyelashes) without bloating the DOM.
* **Why Use This Skill (Rationale)**: Drawing with CSS leverages the browser's native rendering engine, resulting in infinitely scalable, crisp visuals with zero HTTP requests for external image assets. It forces a deep understanding of the CSS box model, stacking contexts (`z-index`), and positioning.
* **Overall Applicability**: Perfect for 404 error page mascots, interactive Easter eggs, playful loading states, custom avatars, or brand elements on portfolio sites.
* **Value Addition**: Transforms standard web layout tools into a creative canvas. By adding a small layer of JavaScript to track mouse coordinates, the static CSS art becomes a delightful, interactive component that responds to the user.
* **Browser Compatibility**: Excellent. Relies on standard CSS Level 3 properties (`border-radius`, `transform`, `absolute` positioning) supported in all modern browsers (Chrome, Safari, Firefox, Edge).

---

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Constructs**: Nested `div` elements representing anatomical parts.
  - **Color Logic**:
    - Base Character Skin: Vibrant yellow `#f3f717`
    - Outlines & Details: Solid dark gray/black `#1a1a1a`
    - Eyeballs & Teeth: Pure white `#ffffff`
    - Irises: Bright blue `#2ba2d4`
    - Pores/Spots: Black `#000000` with `opacity: 0.15` to dynamically blend with the yellow skin.
  - **CSS Properties**: Focuses on `border`, `border-radius`, `transform` (rotate, translate), and `box-shadow` for depth.

* **Step B: Layout & Compositional Style**
  - **Layout System**: The character container uses `position: relative` with fixed dimensions (e.g., `250px` by `250px`). All child anatomy elements use `position: absolute`.
  - **Proportions**:
    - Eyes take up ~30% of the width and are positioned symmetrically along the upper third.
    - The smile is an oversized oval positioned centrally, where only the bottom border is visible.
  - **Z-Index Strategy**:
    - Teeth (`z-index: 0`) tuck behind the smile line.
    - Smile (`z-index: 1`) overlays the background.
    - Eyes (`z-index: 2`) and Nose (`z-index: 5`) sit on top to create depth.

* **Step C: Interactive Behavior & Animations**
  - **JS Cursor Tracking**: An event listener on the `document` tracks `mousemove`. Trigonometry (`Math.atan2` and `Math.hypot`) calculates the angle and distance from the center of the eyes to the cursor, mapping that vector to a CSS `transform: translate()` on the irises, creating a "look around" effect.

---

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Character Shapes** | CSS Box Model & Borders | High performance, crisp scaling, no external SVG assets required. |
| **Open Curves (Smile/Nose)** | Partial CSS Borders | Setting `border-top: transparent` on an oval perfectly simulates a curved drawn stroke. |
| **Repeated Details (Lashes)** | CSS `::before` / `::after` | Keeps HTML semantic and minimal. One `div` can draw three strokes. |
| **Eye Tracking** | Vanilla JS `mousemove` | Native DOM API provides real-time cursor coordinates to dynamically update CSS variables or transforms. |

> **Feasibility Assessment**: 100% reproduction of the tutorial's core mechanism, enhanced with an interactive eye-tracking behavior to demonstrate the practical application of building CSS characters.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "CSS Character Art",
    body_text: str = "Move your mouse to look around!",
    color_scheme: str = "dark",
    accent_color: str = "#f3f717",
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Pure CSS Character Construction.
    Includes JS for interactive eye tracking.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme definitions
    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_color = "#f8fafc"
        card_bg = "#1e293b"
    else:
        bg_color = "#f1f5f9"
        text_color = "#0f172a"
        card_bg = "#ffffff"

    css = f"""/* Pure CSS Character Art — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --card-bg: {card_bg};
    --stroke: #1a1a1a;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.page-title {{
    margin-bottom: 8px;
    font-size: 2rem;
    font-weight: 700;
}}

.page-subtitle {{
    margin-bottom: 40px;
    opacity: 0.8;
    font-size: 1.1rem;
}}

/* Character Container */
.character-box {{
    width: 250px;
    height: 250px;
    background-color: var(--accent);
    border: 4px solid var(--stroke);
    position: relative;
    border-radius: 16px;
    box-shadow: inset -15px -15px 0 rgba(0,0,0,0.08), 
                0 20px 40px rgba(0,0,0,0.2);
    overflow: hidden;
    transition: transform 0.3s ease;
}}

.character-box:hover {{
    transform: translateY(-5px);
}}

/* Spots / Pores */
.spot {{
    position: absolute;
    background: #000;
    border-radius: 50%;
    opacity: 0.15;
}}
.s1 {{ width: 35px; height: 40px; top: 12%; left: 8%; transform: rotate(15deg); }}
.s2 {{ width: 20px; height: 20px; top: 75%; left: 12%; transform: rotate(-20deg); }}
.s3 {{ width: 45px; height: 35px; top: 80%; right: 8%; transform: rotate(45deg); }}
.s4 {{ width: 25px; height: 25px; top: 22%; right: 12%; }}

/* Eyes */
.eye {{
    position: absolute;
    width: 76px;
    height: 76px;
    background: #fff;
    border-radius: 50%;
    border: 3px solid var(--stroke);
    top: 35%;
    transform: translateY(-50%);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 2;
    box-shadow: inset 0 4px 8px rgba(0,0,0,0.1);
}}
.left-eye {{ left: 16%; }}
.right-eye {{ right: 16%; }}

/* Irises (Dynamic via JS) */
.iris {{
    width: 34px;
    height: 34px;
    background: #2ba2d4;
    border-radius: 50%;
    border: 2px solid var(--stroke);
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    /* Will be translated by JS, so we use a snappy transition */
    transition: transform 0.05s linear; 
}}

.pupil {{
    width: 14px;
    height: 14px;
    background: var(--stroke);
    border-radius: 50%;
    position: relative;
}}

/* Eye Highlight */
.pupil::after {{
    content: '';
    position: absolute;
    width: 4px;
    height: 4px;
    background: white;
    border-radius: 50%;
    top: 2px;
    left: 2px;
}}

/* Eyelashes */
.eyelashes {{
    position: absolute;
    width: 4px;
    height: 18px;
    background: var(--stroke);
    top: 10%;
    border-radius: 2px;
}}
.left-lash {{ left: 30%; }}
.right-lash {{ right: 30%; }}

.eyelashes::before, .eyelashes::after {{
    content: '';
    position: absolute;
    width: 4px;
    height: 16px;
    background: var(--stroke);
    border-radius: 2px;
}}
.eyelashes::before {{
    transform: rotate(-35deg);
    left: -18px;
    top: 5px;
}}
.eyelashes::after {{
    transform: rotate(35deg);
    left: 18px;
    top: 5px;
}}

/* Nose - Open Curve */
.nose {{
    position: absolute;
    width: 28px;
    height: 38px;
    border: 3px solid var(--stroke);
    border-bottom-color: transparent;
    border-radius: 50%;
    background: var(--accent);
    top: 43%;
    left: 50%;
    transform: translateX(-50%);
    z-index: 5;
}}

/* Smile - Open Curve */
.smile {{
    position: absolute;
    width: 150px;
    height: 70px;
    border-bottom: 4px solid var(--stroke);
    border-radius: 50%;
    top: 40%;
    left: 50%;
    transform: translateX(-50%);
    z-index: 1;
}}

/* Teeth */
.tooth {{
    position: absolute;
    width: 22px;
    height: 26px;
    background: #fff;
    border: 3px solid var(--stroke);
    border-top: none;
    top: calc(40% + 70px - 2px); /* Snaps to the bottom border of the smile */
    z-index: 0;
}}
.t-left {{ left: 41%; }}
.t-right {{ left: 50%; }}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1 class="page-title">{title_text}</h1>
    <p class="page-subtitle">{body_text}</p>
    
    <div class="character-box">
        <!-- Pores -->
        <div class="spot s1"></div>
        <div class="spot s2"></div>
        <div class="spot s3"></div>
        <div class="spot s4"></div>
        
        <!-- Eyelashes -->
        <div class="eyelashes left-lash"></div>
        <div class="eyelashes right-lash"></div>
        
        <!-- Left Eye -->
        <div class="eye left-eye">
            <div class="iris">
                <div class="pupil"></div>
            </div>
        </div>
        
        <!-- Right Eye -->
        <div class="eye right-eye">
            <div class="iris">
                <div class="pupil"></div>
            </div>
        </div>
        
        <!-- Nose -->
        <div class="nose"></div>
        
        <!-- Smile -->
        <div class="smile"></div>
        
        <!-- Teeth -->
        <div class="tooth t-left"></div>
        <div class="tooth t-right"></div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Eye Tracking Interaction
document.addEventListener('DOMContentLoaded', () => {{
    const irises = document.querySelectorAll('.iris');
    
    // Throttle via requestAnimationFrame for smooth performance
    let isTracking = false;
    let targetX = 0;
    let targetY = 0;

    const trackEyes = () => {{
        irises.forEach(iris => {{
            // Get center coordinates of each eye
            const rect = iris.parentElement.getBoundingClientRect();
            const eyeCenterX = rect.left + rect.width / 2;
            const eyeCenterY = rect.top + rect.height / 2;
            
            // Calculate angle between cursor and eye center
            const angle = Math.atan2(targetY - eyeCenterY, targetX - eyeCenterX);
            
            // Calculate distance, capping it so the iris doesn't leave the eyeball
            const maxDistance = 14; // pixels
            const rawDistance = Math.hypot(targetX - eyeCenterX, targetY - eyeCenterY) / 15;
            const distance = Math.min(maxDistance, rawDistance);
            
            // Calculate new X and Y transform
            const moveX = Math.cos(angle) * distance;
            const moveY = Math.sin(angle) * distance;
            
            iris.style.transform = `translate(${{moveX}}px, ${{moveY}}px)`;
        }});
        isTracking = false;
    }};

    document.addEventListener('mousemove', (e) => {{
        targetX = e.clientX;
        targetY = e.clientY;
        
        if (!isTracking) {{
            isTracking = true;
            requestAnimationFrame(trackEyes);
        }}
    }});
    
    // Reset eyes when mouse leaves window
    document.addEventListener('mouseleave', () => {{
        irises.forEach(iris => {{
            iris.style.transform = `translate(0px, 0px)`;
        }});
    }});
}});
"""

    # Write files
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

* **Accessibility**: Pure CSS art elements are inherently not interpreted as "images" by screen readers. If this component conveys important information or acts as a mascot, the parent `.character-box` should be given `role="img"` and an `aria-label="Illustration of a geometric character"`. 
* **Performance (Rendering)**: The CSS construction utilizes standard geometry and layout techniques that are extremely fast for the browser to paint. It completely avoids the network payload of an equivalent rasterized PNG or detailed SVG.
* **Performance (JavaScript)**: The `mousemove` event triggers rapidly. To maintain 60 FPS and prevent jank, the code wraps the style recalculation inside a `requestAnimationFrame` flag (`isTracking`). This ensures DOM updates only occur when the browser is ready to paint the next frame.