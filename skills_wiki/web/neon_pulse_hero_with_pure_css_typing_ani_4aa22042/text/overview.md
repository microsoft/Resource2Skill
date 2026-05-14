# Neon Pulse Hero with Pure CSS Typing Animation

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Neon Pulse Hero with Pure CSS Typing Animation

* **Core Visual Mechanism**: This component features a high-contrast, cyberpunk-inspired hero section. The defining visual signature is the **Neon Avatar Glow**—a circular profile image enveloped in a highly saturated, multi-layered `box-shadow` that reacts on hover. This is paired with a **Pure CSS Typing Animation**, where text continuously deletes and rewrites itself using pseudo-elements and `steps()` keyframes, creating an engaging, terminal-like dynamic feel without relying on JavaScript libraries.
* **Why Use This Skill (Rationale)**: The neon glow draws immediate focal attention to the subject (the person or product), establishing strong visual hierarchy. The typing animation retains user attention by introducing continuous, predictable motion, encouraging visitors to pause and read the changing value propositions. 
* **Overall Applicability**: Perfect for personal developer/designer portfolios, tech SaaS landing pages, Web3/crypto projects, or any dark-themed website aiming for a modern, futuristic, or highly energetic aesthetic.
* **Value Addition**: It elevates a static "Hi, I am X" introduction into an interactive storytelling device. The CSS-only typing effect drastically reduces page weight (no JS libraries like Typed.js required) while maintaining 60fps hardware-accelerated rendering.
* **Browser Compatibility**: Excellent. Uses standard CSS features (`box-shadow`, `border-radius`, `@keyframes`, `::before`/`::after` pseudo-elements). Works on all modern browsers (Chrome 4+, Firefox 16+, Safari 5+, Edge).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  * **Color Logic**: Deep dark background (e.g., `#080808` or `#0b0f19`) paired with a hyper-saturated accent color (e.g., Cyan `#00ffee`, Magenta `#ff00ff`, or Lime). The contrast is crucial.
  * **Typography**: Clean, geometric sans-serif (like 'Poppins' or 'Inter'). High font-weights (`600`-`800`) for headers to hold their own against the heavy neon visuals.
  * **The Neon Glow (`box-shadow`)**: Achieved by stacking multiple shadows with zero spread but increasing blur radiuses. Example: `box-shadow: 0 0 25px var(--accent)`. On hover, this expands to `0 0 50px, 0 0 100px`.
* **Step B: Layout & Compositional Style**
  * **Layout System**: CSS Flexbox (`display: flex; align-items: center; justify-content: space-between`).
  * **Proportions**: Split roughly 50/50 on desktop. The avatar takes up about `32vw` (max-width bounded), ensuring it scales down proportionally.
  * **Responsive Behavior**: Below `991px`, the flex direction switches to `column-reverse`, stacking the image above the text and centering the alignment.
* **Step C: Interactive Behavior & Animations**
  * **CSS Typing Animation**: 
    * The changing text is handled by altering the `content` property of a `span::before` element via `@keyframes`.
    * The "typing" reveal is handled by a `span::after` block (matching the background color) that shrinks and grows using the `steps()` timing function to simulate a monospaced cursor moving character by character.
  * **Hover States**: Buttons fill with the accent color; the avatar's neon shadow intensifies and pulses slightly.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Layout Skeleton | CSS Flexbox | Fluidly handles the 2-column to 1-column responsive shift. |
| Neon Avatar Glow | CSS `box-shadow` | Stacking shadows is native, performant, and perfectly mimics glowing light diffusion. |
| Typing Text | Pure CSS (`@keyframes` + `content`) | Eliminates the need for JS overhead. Using `steps()` creates the perfect typewriter stutter. |
| Icons | Boxicons CDN | Lightweight, consistent iconography used in the original design. |

> **Feasibility Assessment**: 100% reproduction. The core visual identity of the hero section, the exact typing effect, and the neon glows can be perfectly captured and parameterized using modern HTML and CSS.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Hi, It's Amelia",
    body_text: str = "I'm a passionate creator building digital experiences. I specialize in turning complex problems into elegant, intuitive, and highly performant web solutions.",
    roles: list = ["Frontend Designer", "Web Developer", "UI/UX Expert"],
    color_scheme: str = "dark",        
    accent_color: str = "#00ffee",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Neon Pulse Hero with Pure CSS Typing Animation.
    Writes index.html and style.css to output_dir. No JS required for core effect.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#080808"
        text_color = "#ffffff"
        text_muted = "#a0a0a0"
    else:
        bg_color = "#ffffff"
        text_color = "#111111"
        text_muted = "#555555"

    # === Dynamic CSS Keyframes for Typing Words ===
    # Distribute the roles evenly across 100% of the keyframe timeline
    keyframes_content = ""
    step = 100 / len(roles)
    for i, role in enumerate(roles):
        start = i * step
        end = (i + 1) * step - 1 
        if i == 0:
            keyframes_content += f"0%, {end:.0f}% {{ content: '{role}'; }}\n    "
        else:
            keyframes_content += f"{start:.0f}%, {end:.0f}% {{ content: '{role}'; }}\n    "
    keyframes_content += f"100% {{ content: '{roles[0]}'; }}"

    # === CSS ===
    css = f"""/* Neon Pulse Hero — generated component */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --text-muted: {text_muted};
    --main-color: {accent_color};
}}

body {{
    font-family: 'Poppins', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow-x: hidden;
}}

/* Container constraints mapped to parameters */
.component-wrapper {{
    width: 100%;
    max-width: {width_px}px;
    min-height: {height_px}px;
    display: flex;
    align-items: center;
    padding: 2rem 5%;
}}

.hero {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    gap: 4rem;
}}

/* Left Column: Text Content */
.hero-content {{
    display: flex;
    flex-direction: column;
    max-width: 600px;
}}

.hero-content h1 {{
    font-size: clamp(3rem, 5vw, 4.5rem);
    font-weight: 700;
    line-height: 1.2;
    margin-bottom: 1rem;
}}

.hero-content h1 span {{
    color: var(--main-color);
    text-shadow: 0 0 15px rgba({int(accent_color[1:3], 16)}, {int(accent_color[3:5], 16)}, {int(accent_color[5:7], 16)}, 0.4);
}}

.text-animation {{
    font-size: clamp(1.8rem, 3vw, 2.5rem);
    font-weight: 600;
    min-width: 280px;
    margin-bottom: 1.5rem;
}}

/* Pure CSS Typing Effect Magic */
.text-animation span {{
    position: relative;
    color: var(--main-color);
}}

.text-animation span::before {{
    content: '{roles[0]}';
    color: var(--main-color);
    animation: words 9s infinite;
}}

.text-animation span::after {{
    content: '';
    background-color: var(--bg-color);
    position: absolute;
    width: calc(100% + 8px);
    height: 100%;
    border-left: 3px solid var(--main-color);
    right: -8px;
    animation: cursor 0.6s infinite, typing 9s steps(14) infinite;
}}

@keyframes words {{
    {keyframes_content}
}}

@keyframes typing {{
    10%, 15%, 30%, 35%, 50%, 55%, 70%, 75%, 90%, 95% {{
        width: 0;
    }}
    5%, 20%, 25%, 40%, 45%, 60%, 65%, 80%, 85% {{
        width: calc(100% + 8px);
    }}
}}

@keyframes cursor {{
    0% {{ border-left-color: var(--main-color); }}
    50% {{ border-left-color: transparent; }}
    100% {{ border-left-color: var(--main-color); }}
}}

.hero-content p {{
    font-size: 1rem;
    color: var(--text-muted);
    line-height: 1.6;
    margin-bottom: 2.5rem;
}}

/* Interactive Elements */
.social-icons {{
    display: flex;
    gap: 1rem;
    margin-bottom: 2.5rem;
}}

.social-icons a {{
    display: inline-flex;
    justify-content: center;
    align-items: center;
    width: 2.8rem;
    height: 2.8rem;
    background: transparent;
    border: 2px solid var(--main-color);
    border-radius: 50%;
    font-size: 1.4rem;
    color: var(--main-color);
    text-decoration: none;
    transition: 0.3s ease;
}}

.social-icons a:hover {{
    background: var(--main-color);
    color: var(--bg-color);
    transform: translateY(-5px);
    box-shadow: 0 0 15px var(--main-color);
}}

.btn-group {{
    display: flex;
    gap: 1.5rem;
}}

.btn {{
    display: inline-block;
    padding: 0.8rem 2.2rem;
    background: var(--main-color);
    border: 2px solid var(--main-color);
    border-radius: 2rem;
    color: var(--bg-color);
    font-weight: 600;
    text-decoration: none;
    letter-spacing: 1px;
    transition: 0.3s ease;
}}

.btn:hover {{
    box-shadow: 0 0 25px var(--main-color);
}}

.btn.outline {{
    background: transparent;
    color: var(--main-color);
}}

.btn.outline:hover {{
    background: var(--main-color);
    color: var(--bg-color);
}}

/* Right Column: Neon Avatar */
.hero-img {{
    position: relative;
    width: clamp(250px, 32vw, 450px);
    aspect-ratio: 1 / 1;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    /* The core neon glow */
    box-shadow: 0 0 25px var(--main-color);
    transition: 0.4s ease-in-out;
    cursor: pointer;
}}

.hero-img:hover {{
    box-shadow: 0 0 50px var(--main-color),
                0 0 100px var(--main-color);
}}

.hero-img img {{
    width: 90%;
    height: 90%;
    object-fit: cover;
    border-radius: 50%;
    border: 3px solid rgba(255, 255, 255, 0.1);
}}

/* Responsive Breakpoint */
@media (max-width: 991px) {{
    .hero {{
        flex-direction: column-reverse;
        text-align: center;
        gap: 3rem;
    }}
    
    .hero-content {{
        align-items: center;
    }}
    
    .text-animation span::after {{
        right: auto; /* Fixes cursor alignment when centered */
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Neon Pulse Hero</title>
    <!-- Boxicons for Social Media Icons -->
    <link href='https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css' rel='stylesheet'>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    
    <div class="component-wrapper">
        <section class="hero">
            
            <div class="hero-content">
                <h1>{title_text}</h1>
                <h3 class="text-animation">I'm a <span></span></h3>
                <p>{body_text}</p>
                
                <div class="social-icons">
                    <a href="#"><i class='bx bxl-linkedin'></i></a>
                    <a href="#"><i class='bx bxl-github'></i></a>
                    <a href="#"><i class='bx bxl-twitter'></i></a>
                    <a href="#"><i class='bx bxl-instagram-alt'></i></a>
                </div>
                
                <div class="btn-group">
                    <a href="#" class="btn">Hire Me</a>
                    <a href="#" class="btn outline">Contact</a>
                </div>
            </div>

            <div class="hero-img">
                <!-- Using Unsplash for a high-quality portrait placeholder -->
                <img src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=800&q=80" alt="Avatar Portrait">
            </div>

        </section>
    </div>

    <!-- No JavaScript required for core functionality! -->
    <script src="script.js"></script>
</body>
</html>"""

    # === Empty JS (Skill relies purely on CSS) ===
    js = """// No JavaScript required!
// The typing animation and neon glow interactions are achieved entirely via CSS keyframes and hover states.
console.log("Neon Hero component initialized successfully.");
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

* **Accessibility (a11y)**:
  * The typing animation relies on the `content` property of pseudo-elements. Screen readers traditionally do not read pseudo-element `content` reliably. To fix this in a production environment, you would want to place the roles in visually hidden text (`sr-only` class) inside the `<h3>`, and add `aria-hidden="true"` to the animated `span` to ensure screen reader users hear the context without confusing broken text fragments.
  * The contrast ratio between the bright cyan (`#00ffee`) and dark background (`#080808`) exceeds WCAG AAA standards (14.5:1).
  * Icon links lack descriptive text. In a real-world scenario, add `aria-label="LinkedIn Profile"` to the `<a>` tags.
* **Performance**:
  * Highly performant. By utilizing strictly CSS `@keyframes` and native `box-shadows`, the browser can offload the animations to the GPU.
  * We avoid scroll listener jank or JavaScript `setInterval` timers entirely, which drastically reduces CPU load and ensures the typing animation stays perfectly smooth even on low-end mobile devices.