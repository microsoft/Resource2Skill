# Centered Hero with Floating Parallax Elements

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Centered Hero with Floating Parallax Elements

* **Core Visual Mechanism**: A highly focused, center-aligned typography layout (headline, subheadline, call-to-action) surrounded by a constellation of absolute-positioned floating elements (user avatars, glassmorphism text badges, or abstract shapes). These peripheral elements feature continuous CSS "levitation" animations combined with a cursor-tracking JavaScript parallax effect, creating a dynamic, layered depth of field.
* **Why Use This Skill (Rationale)**: This layout perfectly balances extreme clarity with rich visual interest. By centering the core value proposition, the reading path is frictionless. By offloading branding, social proof (user avatars), and secondary features (badges) to the periphery, the design communicates a dense amount of context without cluttering the primary cognitive area.
* **Overall Applicability**: Ideal for SaaS landing pages, community-driven platforms, modern startup homepages, and portfolio sites. It thrives where you need to showcase a vibrant ecosystem or user base while driving a singular primary action (like joining a waitlist or signing up).
* **Value Addition**: Transforms a static, boring text-centered hero into an immersive, interactive environment. The parallax depth makes the webpage feel like a spatial software interface rather than a flat document.
* **Browser Compatibility**: Uses `backdrop-filter` for glassmorphism, CSS `clamp()` for responsive typography, and CSS variables. Supported by all modern browsers (Chrome 76+, Safari 13.1+, Firefox 70+, Edge 79+).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**: Utilizes a deep contrast logic. A dark theme might use a midnight blue background (`#0f172a`), stark white text (`#f8fafc`), and a vibrant accent (e.g., Indigo `#6366f1`). Floating badges use a semi-transparent surface color (`rgba(30, 41, 59, 0.6)`) with `backdrop-filter` to create frosted glass.
  - **Typographic Hierarchy**: Driven by the `Inter` font. The H1 is massive, bold (weight 800), and tightly tracked (`letter-spacing: -0.03em`) using `clamp()` to scale fluidly. The subtitle is semi-transparent and readable (1.125rem).
  - **Ambient Lighting**: A soft radial gradient centered behind the text, derived from the accent color with low opacity, ties the floating elements and text together.

* **Step B: Layout & Compositional Style**
  - **Layout System**: The main hero wrapper uses Flexbox (`flex-direction: column`, `align-items: center`, `justify-content: center`) for perfect vertical/horizontal centering.
  - **Spatial Strategy**: The floating elements are removed from the document flow via `position: absolute`. They are distributed using percentage-based `top`, `bottom`, `left`, and `right` coordinates to ensure they frame the text symmetrically without overlapping it.
  - **Z-Index Layering**: Background gradient (0) → Floating Elements (5) → Central Text Content (10).

* **Step C: Interactive Behavior & Animations**
  - **Continuous Float**: Pure CSS `@keyframes` translateY animation applied to the inner element of each floating item, creating a slow, desynchronized bobbing effect (using negative animation delays like `-2s` to offset the loops).
  - **Cursor Parallax**: JavaScript tracks `mousemove` events on the container. The cursor's normalized coordinates (-0.5 to +0.5) multiply against a custom `data-depth` attribute on each floating wrapper, moving foreground objects faster than background objects to simulate 3D space.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Responsive Typography** | CSS `clamp()` | Allows the massive headline to scale perfectly down to mobile without media query breakpoints. |
| **Floating Badges** | CSS `backdrop-filter: blur()` | Native GPU-accelerated glassmorphism; essential for overlapping elements elegantly. |
| **Ambient Glow** | CSS `radial-gradient` | Creates a focal spotlight effect without requiring heavy images or canvas. |
| **Continuous Bobbing** | CSS `@keyframes` | Extremely performant; handles the continuous idle animation natively. |
| **Mouse Parallax Depth** | Vanilla JS `mousemove` + CSS `transform` | Smoothly overrides layout position dynamically; applied to a wrapper div so it doesn't collide with the CSS keyframe transforms. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Meet Your<br>Creative Tribe.",
    body_text: str = "The community and training platform built to help you double your impact, learn new skills, and connect with peers.",
    cta_text: str = "Join the Waitlist",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#6366f1",     # Indigo accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the "Centered Hero with Floating Parallax Elements" visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3:
            hex_color = ''.join([c*2 for c in hex_color])
        return f"{int(hex_color[0:2], 16)}, {int(hex_color[2:4], 16)}, {int(hex_color[4:6], 16)}"

    accent_rgb = hex_to_rgb(accent_color)

    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_color = "#f8fafc"
        text_rgb = hex_to_rgb(text_color)
        surface_color = "rgba(30, 41, 59, 0.6)"
        border_color = "rgba(255, 255, 255, 0.1)"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        text_rgb = hex_to_rgb(text_color)
        surface_color = "rgba(255, 255, 255, 0.6)"
        border_color = "rgba(0, 0, 0, 0.05)"

    css = f"""/* Centered Hero with Floating Parallax Elements */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-rgb: {text_rgb};
    --accent: {accent_color};
    --accent-rgb: {accent_rgb};
    --surface: {surface_color};
    --border: {border_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: #000; /* Outer canvas */
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    overflow: hidden;
}}

.hero-container {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    background-color: var(--bg);
    color: var(--text);
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

/* Ambient Background Glow */
.hero-container::before {{
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 60%;
    height: 60%;
    background: radial-gradient(circle, rgba(var(--accent-rgb), 0.15) 0%, rgba(var(--accent-rgb), 0) 70%);
    z-index: 0;
    pointer-events: none;
}}

/* Central Content */
.hero-content {{
    position: relative;
    z-index: 10;
    text-align: center;
    max-width: 720px;
    padding: 0 24px;
}}

.hero-title {{
    font-size: clamp(2.5rem, 6vw, 4.5rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.03em;
    margin-bottom: 24px;
}}

.hero-subtitle {{
    font-size: clamp(1rem, 2vw, 1.125rem);
    line-height: 1.6;
    color: rgba(var(--text-rgb), 0.75);
    margin-bottom: 40px;
    max-width: 600px;
    margin-inline: auto;
}}

.btn-primary {{
    background-color: var(--accent);
    color: #ffffff;
    font-size: 1.125rem;
    font-weight: 600;
    padding: 16px 36px;
    border-radius: 9999px;
    border: none;
    cursor: pointer;
    box-shadow: 0 10px 25px -5px rgba(var(--accent-rgb), 0.5);
    transition: all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
}}

.btn-primary:hover {{
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 15px 35px -5px rgba(var(--accent-rgb), 0.6);
}}

/* Floating Elements */
.floating-layer {{
    position: absolute;
    inset: 0;
    z-index: 5;
    pointer-events: none; /* Let clicks pass through */
}}

.float-wrapper {{
    position: absolute;
    /* Smooths out the JS mousemove parallax */
    transition: transform 0.4s ease-out;
    will-change: transform;
}}

.anim-float {{
    animation: levitate 6s ease-in-out infinite;
}}

.float-avatar {{
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid var(--surface);
    box-shadow: 0 10px 25px rgba(0,0,0,0.15);
}}

.float-badge {{
    background: var(--surface);
    color: var(--text);
    padding: 12px 20px;
    border-radius: 24px;
    font-size: 0.875rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 8px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid var(--border);
    white-space: nowrap;
}}

/* Specific Sizes and Positions */
.avatar-sm {{ width: 50px; height: 50px; }}
.avatar-md {{ width: 70px; height: 70px; }}
.avatar-lg {{ width: 90px; height: 90px; }}

.item-1 {{ top: 15%; left: 10%; }}
.item-2 {{ top: 45%; left: 5%; }}
.item-3 {{ bottom: 18%; left: 15%; }}
.item-4 {{ top: 20%; right: 10%; }}
.item-5 {{ top: 55%; right: 8%; }}
.item-6 {{ bottom: 25%; right: 15%; }}

/* Animation offsets to randomize bobbing */
.delay-1 {{ animation-delay: 0s; }}
.delay-2 {{ animation-delay: -1.5s; animation-duration: 5s; }}
.delay-3 {{ animation-delay: -3s; animation-duration: 7s; }}
.delay-4 {{ animation-delay: -0.5s; animation-duration: 6.5s; }}
.delay-5 {{ animation-delay: -2s; animation-duration: 5.5s; }}
.delay-6 {{ animation-delay: -4s; animation-duration: 6s; }}

@keyframes levitate {{
    0%, 100% {{ transform: translateY(0px); }}
    50% {{ transform: translateY(-15px); }}
}}

/* Responsive hiding for very small screens */
@media (max-width: 768px) {{
    .float-wrapper {{ display: none; }}
    .hero-container::before {{ width: 100%; height: 100%; }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Centered Hero Layout</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <section class="hero-container">
        
        <!-- Peripheral Floating Layer -->
        <div class="floating-layer" aria-hidden="true">
            <div class="float-wrapper item-1" data-depth="1.2">
                <div class="anim-float delay-1">
                    <img src="https://i.pravatar.cc/150?img=68" alt="" class="float-avatar avatar-sm">
                </div>
            </div>
            <div class="float-wrapper item-2" data-depth="2.5">
                <div class="anim-float delay-2">
                    <div class="float-badge">🎨 New design competition</div>
                </div>
            </div>
            <div class="float-wrapper item-3" data-depth="0.8">
                <div class="anim-float delay-3">
                    <img src="https://i.pravatar.cc/150?img=47" alt="" class="float-avatar avatar-lg">
                </div>
            </div>
            <div class="float-wrapper item-4" data-depth="1.8">
                <div class="anim-float delay-4">
                    <div class="float-badge">💬 Just landed a $10k project!</div>
                </div>
            </div>
            <div class="float-wrapper item-5" data-depth="1.1">
                <div class="anim-float delay-5">
                    <img src="https://i.pravatar.cc/150?img=33" alt="" class="float-avatar avatar-md">
                </div>
            </div>
            <div class="float-wrapper item-6" data-depth="2.2">
                <div class="anim-float delay-6">
                    <div class="float-badge">💡 How do I price this site?</div>
                </div>
            </div>
        </div>

        <!-- Core Content -->
        <div class="hero-content">
            <h1 class="hero-title">{title_text}</h1>
            <p class="hero-subtitle">{body_text}</p>
            <button class="btn-primary" aria-label="{cta_text}">{cta_text}</button>
        </div>

    </section>
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Parallax Mouse tracking for floating elements
document.addEventListener('DOMContentLoaded', () => {{
    const container = document.querySelector('.hero-container');
    const wrappers = document.querySelectorAll('.float-wrapper');

    // Only apply parallax on desktop dimensions where elements are visible
    if (window.innerWidth <= 768) return;

    container.addEventListener('mousemove', (e) => {{
        const rect = container.getBoundingClientRect();
        
        // Normalize mouse coordinates to range [-0.5, 0.5]
        const x = (e.clientX - rect.left) / rect.width - 0.5;
        const y = (e.clientY - rect.top) / rect.height - 0.5;

        wrappers.forEach(wrapper => {{
            const depth = parseFloat(wrapper.getAttribute('data-depth')) || 1;
            // The deeper the depth multiplier, the more the element moves
            const moveX = x * -50 * depth; 
            const moveY = y * -50 * depth;
            
            wrapper.style.transform = `translate(${{moveX}}px, ${{moveY}}px)`;
        }});
    }});

    // Gracefully reset elements to center origin when mouse leaves hero
    container.addEventListener('mouseleave', () => {{
        wrappers.forEach(wrapper => {{
            wrapper.style.transform = `translate(0px, 0px)`;
        }});
    }});
}});
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
  - The entire `.floating-layer` uses `aria-hidden="true"`. This is crucial because the badges and avatars serve as decorative ambiance supplementing the hero copy. Screen readers will skip this visual noise and focus directly on the semantic `h1`, `p`, and `button` inside `.hero-content`.
  - The primary CTA button includes an `aria-label` attribute mapped to the button text to explicitly state its intent.
  - Text-to-background contrast relies on generating properly tinted RGB variations ensuring it remains above WCAG AA minimums (via the semi-transparent `rgba(var(--text-rgb), 0.75)` mapping against the solid background).

* **Performance**:
  - **CSS Layer Separation**: By isolating the continuous bobbing `@keyframes` on the `.anim-float` child elements, and mapping the JavaScript mousemove updates only to the `.float-wrapper` parent elements, the browser avoids repainting conflicts. The CSS animations remain on the GPU composer thread.
  - **Parallax Interpolation (Lerp)**: Instead of manually building a `requestAnimationFrame` lerp loop in JavaScript (which can be heavy), the component uses CSS `transition: transform 0.4s ease-out;` directly on the wrapper. When the JS fires on `mousemove`, the CSS engine acts as a hardware-accelerated tweening engine, creating a buttery-smooth parallax interpolation almost completely free of script execution jank.
  - **Responsive cull**: The JavaScript parallax halts initialization and the CSS `display: none` engages for floating elements if the viewport drops below `768px`, saving mobile devices from rendering 6 overlapping blurred elements.