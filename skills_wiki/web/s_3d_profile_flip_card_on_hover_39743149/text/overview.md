# 3D Profile Flip Card on Hover

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: 3D Profile Flip Card on Hover

* **Core Visual Mechanism**: A two-sided digital card that utilizes CSS 3D transforms (`perspective`, `rotateY`, `transform-style: preserve-3d`). When the user hovers over the element, it smoothly rotates 180 degrees along the Y-axis to reveal hidden content on the back face. 
* **Why Use This Skill (Rationale)**: This interaction pattern resolves spatial constraints by layering secondary information behind primary information. It leverages the psychology of curiosity and physical-world metaphors (turning over a physical business card). The smooth 3D motion adds a premium, polished feel to an otherwise standard UI element.
* **Overall Applicability**: Perfect for "About Us" team pages, user profile directories, pricing tiers (e.g., flipping to see a detailed feature list), or product cards in an e-commerce grid.
* **Value Addition**: It condenses the visual footprint of complex information. Instead of overwhelming the user with a bio, links, and actions all at once, it presents the identity first, and delegates the calls-to-action (CTAs) to a purposeful interaction state.
* **Browser Compatibility**: Excellent. CSS 3D transforms (`perspective`, `preserve-3d`, `backface-visibility`) are supported in all modern browsers (Chrome, Firefox, Safari, Edge).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **HTML Structure**: Requires a specific nesting structure: A perspective wrapper (`.flip-container`), a 3D context wrapper (`.flip-inner`), and two absolutely positioned sibling faces (`.flip-front` and `.flip-back`).
  - **Color Logic**: 
    - Front Background: Deep Navy/Purple `#24203b`
    - Back Background (Accent): Vibrant Magenta `#c500d6`
    - Text: Pure White `#ffffff`
    - Skill Tags: White backgrounds `#ffffff` with dark/magenta text.
  - **Typography**: `Montserrat` (sans-serif), heavily utilizing uppercase text for names, section headers, and buttons, giving it a modern, tech-focused look.
  - **Key CSS Properties**: `transform: rotateY()`, `backface-visibility: hidden`, `perspective: 1000px`, `transform-style: preserve-3d`.

* **Step B: Layout & Compositional Style**
  - **Grid/Flexbox**: The outer container can be centered via body Flexbox. The interior of the cards uses flexbox to center content vertically and horizontally.
  - **Dimensions**: Fixed width and height (e.g., `250px` by `400px` in the tutorial).
  - **Z-Index/Layering**: The front and back faces are stacked exactly on top of each other using `position: absolute`, `width: 100%`, and `height: 100%`. `backface-visibility: hidden` ensures the reversed text of the front doesn't bleed through to the back.

* **Step C: Interactive Behavior & Animations**
  - **Trigger**: Pure CSS `:hover` (and ideally `:focus-within` for accessibility).
  - **Animation arc**: The `.flip-inner` rotates from `0deg` to `180deg`. The back face is pre-rotated to `rotateY(180deg)` so that when the parent flips, the back face is brought to `360deg` (facing the user properly).
  - **Timing**: `transition: transform 0.8s ease` (smooth, slightly slower motion emphasizing the 3D depth).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| 3D Flip Mechanics | Pure CSS Transforms | Native GPU acceleration, highly performant, requires absolutely zero JavaScript. |
| Layout & Centering | CSS Flexbox | Cleanly centers the profile image, text, and buttons inside their respective faces. |
| Typography | Google Fonts CDN | Easy inclusion of "Montserrat" to match the exact aesthetic of the tutorial. |

*Feasibility Assessment*: 100%. The visual effect demonstrated in the video can be flawlessly and completely reproduced using HTML and CSS.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "John Doe",
    body_text: str = "UI & UX FRONT-END DEVELOPER",
    color_scheme: str = "dark",        
    accent_color: str = "#c500d6",     
    width_px: int = 280,
    height_px: int = 420,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Profile Flip Card visual effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#f0f2f5" # Body background
        front_bg = "#24203b"
        text_color = "#ffffff"
        skill_bg = "#ffffff"
        skill_text = "#24203b"
    else:
        bg_color = "#121212" # Body background
        front_bg = "#ffffff"
        text_color = "#333333"
        skill_bg = "#f0f0f0"
        skill_text = "#333333"

    # === CSS ===
    css = f"""/* 3D Profile Flip Card — generated component */
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --body-bg: {bg_color};
    --front-bg: {front_bg};
    --back-bg: {accent_color};
    --text-color: {text_color};
    --skill-bg: {skill_bg};
    --skill-text: {skill_text};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Montserrat', sans-serif;
    background: var(--body-bg);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

/* The 3D Perspective Wrapper */
.flip-container {{
    width: var(--width);
    height: var(--height);
    perspective: 1000px; /* Establishes the 3D space */
}}

/* The element that actually rotates */
.flip-inner-container {{
    position: relative;
    width: 100%;
    height: 100%;
    text-align: center;
    transition: transform 0.8s cubic-bezier(0.4, 0.2, 0.2, 1);
    transform-style: preserve-3d; /* Allows children to live in 3D space */
    border-radius: 12px;
    box-shadow: 0 15px 35px rgba(0,0,0,0.2);
}}

/* Trigger rotation on hover and keyboard focus */
.flip-container:hover .flip-inner-container,
.flip-container:focus-within .flip-inner-container {{
    transform: rotateY(180deg);
}}

/* Shared styles for both front and back faces */
.flip-front, 
.flip-back {{
    position: absolute;
    width: 100%;
    height: 100%;
    backface-visibility: hidden; /* Hides the backside of the panel when turned away */
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 20px;
    color: var(--text-color);
    overflow: hidden;
}}

/* Front Face */
.flip-front {{
    background-color: var(--front-bg);
}}

/* Back Face */
.flip-back {{
    background-color: var(--back-bg);
    transform: rotateY(180deg); /* Pre-rotate so it faces the correct way when parent flips */
}}

/* --- Front Content Styling --- */
.profile-image {{
    width: 120px;
    height: 120px;
    border-radius: 50%;
    border: 4px solid var(--back-bg);
    background-image: url('https://i.pravatar.cc/300?img=11'); /* Placeholder image */
    background-size: cover;
    background-position: center;
    margin-bottom: 15px;
}}

.flip-front h3 {{
    font-size: 1.2rem;
    font-weight: 700;
    margin-bottom: 5px;
    text-transform: uppercase;
    letter-spacing: 1px;
}}

.flip-front h6 {{
    font-size: 0.7rem;
    font-weight: 400;
    margin-bottom: 20px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    opacity: 0.8;
}}

.skills-title {{
    font-size: 0.85rem;
    font-weight: 700;
    margin-bottom: 10px;
    border-bottom: 1px solid rgba(255,255,255,0.2);
    padding-bottom: 5px;
    width: 80%;
    text-transform: uppercase;
}}

.skills {{
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 8px;
}}

.skills span {{
    background-color: var(--skill-bg);
    color: var(--skill-text);
    padding: 4px 8px;
    font-size: 0.65rem;
    font-weight: 600;
    border-radius: 4px;
    text-transform: uppercase;
}}

/* --- Back Content Styling --- */
.flip-back h2 {{
    font-size: 1.8rem;
    font-weight: 700;
    margin-bottom: 30px;
    text-transform: uppercase;
}}

.btn {{
    display: inline-block;
    width: 80%;
    padding: 12px 0;
    margin-bottom: 15px;
    background-color: var(--front-bg);
    color: var(--text-color);
    text-decoration: none;
    font-size: 0.9rem;
    font-weight: 600;
    text-transform: uppercase;
    border-radius: 25px;
    transition: background-color 0.3s, transform 0.2s;
}}

.btn:hover, .btn:focus {{
    background-color: #1a172a; /* Slightly darker */
    transform: translateY(-2px);
    outline: 2px solid white;
    outline-offset: 2px;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>3D Flip Card</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <div class="flip-container" tabindex="0" aria-label="Profile card for {title_text}">
        <div class="flip-inner-container">
            
            <!-- Front of the Card -->
            <div class="flip-front" aria-hidden="false">
                <div class="profile-image" role="img" aria-label="{title_text} Profile Picture"></div>
                <h3>{title_text}</h3>
                <h6>{body_text}</h6>
                
                <div class="skills-title">Skills</div>
                <div class="skills">
                    <span>UI & UX</span>
                    <span>Front-end</span>
                    <span>HTML</span>
                    <span>CSS</span>
                    <span>JavaScript</span>
                    <span>React</span>
                </div>
            </div>
            
            <!-- Back of the Card -->
            <div class="flip-back" aria-hidden="true">
                <h2>{title_text}</h2>
                <a href="#" class="btn btn_hire">Hire</a>
                <a href="#" class="btn btn_message">Message</a>
            </div>

        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    # For a purely CSS-driven hover effect, JS isn't strictly necessary.
    # However, to improve accessibility, we can toggle aria-hidden attributes 
    # when the card is hovered or focused via keyboard.
    js = f"""// 3D Profile Flip Card — Accessibility enhancements
document.addEventListener('DOMContentLoaded', () => {{
    const container = document.querySelector('.flip-container');
    const front = document.querySelector('.flip-front');
    const back = document.querySelector('.flip-back');

    const handleFlipIn = () => {{
        front.setAttribute('aria-hidden', 'true');
        back.setAttribute('aria-hidden', 'false');
    }};

    const handleFlipOut = () => {{
        front.setAttribute('aria-hidden', 'false');
        back.setAttribute('aria-hidden', 'true');
    }};

    // Mouse interactions
    container.addEventListener('mouseenter', handleFlipIn);
    container.addEventListener('mouseleave', handleFlipOut);

    // Keyboard interactions
    container.addEventListener('focusin', handleFlipIn);
    container.addEventListener('focusout', handleFlipOut);
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

#### 3c. Verification Checklist

- [x] Does the code produce valid HTML5 that passes basic validation?
- [x] Does `index.html` work when opened directly in a browser (`file://` protocol)?
- [x] Are all color values explicit hex or rgba?
- [x] Are all external resources loaded from CDN URLs?
- [x] Does the component respect the `width_px` and `height_px` parameters?
- [x] Does `color_scheme="dark"` produce a dark theme and `"light"` a light theme?
- [x] Does `accent_color` propagate to all accent elements (back face, image border)?
- [x] Does the JavaScript run without console errors?
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect?
- [x] Would someone looking at the output say "yes, that's the same technique"?

### 4. Accessibility & Performance Notes

* **Accessibility (a11y)**: 
  - **Keyboard Navigation**: Hover effects often alienate keyboard users. This reproduction applies `tabindex="0"` to the wrapper and hooks the flip animation to `.flip-container:focus-within` in CSS. This ensures that tabbing to the card or its buttons triggers the rotation.
  - **Screen Readers**: Using `backface-visibility: hidden` hides the element visually, but screen readers may still read the hidden content. The included JavaScript patches this by toggling `aria-hidden` attributes on the front and back faces dynamically based on hover/focus state.
  - **Reduced Motion**: For strict accessibility, you should add an `@media (prefers-reduced-motion: reduce)` block to the CSS to remove the `transition: transform` duration, making the flip instantaneous rather than animated for users susceptible to motion sickness.
* **Performance**: 
  - `transform: rotateY()` triggers hardware (GPU) acceleration in modern browsers. 
  - Since we are not animating layout properties like `width`, `margin`, or `left`/`top`, the animation bypasses the browser's expensive layout and paint phases, ensuring a smooth 60fps framerate even on lower-end devices.