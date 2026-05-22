### 1. High-level Design Pattern Extraction

> **Skill Name**: Epic Dark Mode Hero with Integrated Social Proof

* **Core Visual Mechanism**: A high-contrast, dark-themed hero layout characterized by massive, impactful typography on the left and a prominent, dynamic feature graphic on the right. The defining signature is the strategic layering of **conversion elements** directly into the visual flow: a vibrant, high-contrast Call-To-Action (CTA) button, immediately followed by overlapping user avatars (social proof), and grounded by a monochromatic "As Seen On" trust logo strip at the layout's base.
* **Why Use This Skill (Rationale)**: This layout applies core conversion psychology. It doesn't just present information; it actively builds trust. The massive headline grabs attention, the bright CTA provides a clear exit node, the avatars trigger the "bandwagon effect" (showing others have safely taken the action), and the media logos at the bottom borrow authority. The dark mode creates a cinematic, premium, and focused environment that makes the CTA and images pop.
* **Overall Applicability**: Ideal for SaaS landing pages, gaming portals, community recruitment drives, or any high-stakes digital product where establishing immediate credibility and driving a specific signup/join action is the primary goal.
* **Value Addition**: Transforms a standard informational header into a high-converting funnel entry point by surrounding the main action with psychological safety signals (trust and popularity).
* **Browser Compatibility**: Excellent. Relies on standard CSS Flexbox/Grid and fundamental CSS properties. The optional JS parallax effect degrades gracefully. Supported in all modern browsers (Chrome, Firefox, Safari, Edge).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**:
    - Deep space/dark background: `#0b0f19` (creates the cinematic void).
    - Primary Text: `#ffffff` (maximum contrast).
    - Secondary Text: `#8b949e` (recedes slightly to establish hierarchy).
    - Accent/CTA: A vivid, urgent color like `#e63946` (red) or `#00bfff` (cyan) that completely stands out from the dark background.
  - **Typographic Hierarchy**:
    - Headline (`h1`): Over-sized (e.g., `4rem`+), sans-serif (like 'Montserrat' or 'Inter' black/bold), tight line-height (`1.1`), often with a slight negative letter-spacing for impact.
    - Body (`p`): Legible, medium weight, `1.125rem` to `1.25rem`.
    - Social Proof Text: Smaller (`0.875rem`), muted color.
  - **Visual Anchors**: Overlapping circular avatars with thick background-colored borders (`box-shadow: 0 0 0 3px var(--bg)` or border) to create a stacking effect.

* **Step B: Layout & Compositional Style**
  - **Layout System**: A wrapper utilizing CSS Grid or Flexbox to create a 2-column layout on desktop (`grid-template-columns: 1fr 1fr` or `55% 45%`).
  - **Spatial Feel**: Asymmetric balance. The heavy text and dense social proof on the left are balanced by a large, singular, airy graphic on the right.
  - **Z-index Layering**: Background starfield/texture at `z-index: -1`, main content at `0`, and floating elements in the graphic container overlapping slightly.

* **Step C: Interactive Behavior & Animations**
  - **Hover Effects**: The primary CTA button scales up slightly (`transform: translateY(-2px)`) and gains a pronounced drop shadow. Trust logos transition from grayscale/low-opacity to full opacity on hover.
  - **JavaScript Enhancement**: A subtle mouse-tracking parallax effect on the hero graphic adds depth and a "premium" feel, mimicking a 3D environment.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **2-Column Layout** | CSS Grid | Provides rigid, predictable column sizing (`1fr 1fr`) that easily collapses to a single column on mobile using media queries. |
| **Social Proof Avatars** | CSS Flexbox + negative margins | Simplest way to create a horizontal row of perfectly overlapping circles without absolute positioning math. |
| **Trust Logo Strip** | FontAwesome SVGs | Reliable, scalable vector logos loaded via CDN to represent the "As Seen On" media companies without needing external image assets. |
| **Cinematic Background** | CSS Gradients + Image | Combining a dark radial gradient with a subtle starry background image creates a deep, non-flat canvas for the content. |
| **Epic Movement** | Vanilla JS `mousemove` | Adds a subtle 3D parallax effect to the hero image, making the static composition feel alive and "epic" as requested in the tutorial's aesthetic. |

> **Feasibility Assessment**: 95%. The code perfectly reproduces the strategic layout, the social proof mechanics, the typography hierarchy, and the trust signals demonstrated in the tutorial. The exact custom composited Star Wars imagery from the video is replaced with generic high-quality space/tech placeholder imagery, but the visual pattern and layout physics are completely preserved.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "It's your universe, it's time to save it",
    body_text: str = "The Rebel alliance is fighting to get rid of the evil empire. Join the resistance to create a better future for your children.",
    color_scheme: str = "dark",
    accent_color: str = "#e63946", # Rebel Red
    width_px: int = 1440,
    height_px: int = 900,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Epic Dark Mode Hero with Social Proof.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Force dark theme as the tutorial is specifically about a dark "epic" space theme
    # but adapt if light is strictly requested
    if color_scheme == "light":
        bg_color = "#f0f4f8"
        text_color = "#101828"
        text_muted = "#475467"
        nav_border = "rgba(0,0,0,0.05)"
        bg_image = "none"
        logo_opacity = "0.4"
    else:
        bg_color = "#080b13"
        text_color = "#ffffff"
        text_muted = "#8b949e"
        nav_border = "rgba(255,255,255,0.05)"
        bg_image = "url('https://images.unsplash.com/photo-1506318137071-a8e063b4bec0?q=80&w=3000&auto=format&fit=crop')"
        logo_opacity = "0.5"

    css = f"""/* Epic Hero with Social Proof */
:root {{
    --bg-color: {bg_color};
    --text-primary: {text_color};
    --text-secondary: {text_muted};
    --accent-color: {accent_color};
    --nav-border: {nav_border};
    --font-heading: 'Montserrat', system-ui, sans-serif;
    --font-body: 'Inter', system-ui, sans-serif;
    --comp-width: {width_px}px;
    --comp-height: {height_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: var(--font-body);
    background-color: var(--bg-color);
    background-image: linear-gradient(to bottom, rgba(8, 11, 19, 0.8), rgba(8, 11, 19, 1)), {bg_image};
    background-size: cover;
    background-position: center;
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    /* Optional: constrain to requested dimensions for preview purposes */
    padding: 2rem;
}}

.hero-wrapper {{
    width: 100%;
    max-width: var(--comp-width);
    min-height: calc(var(--comp-height) - 4rem);
    background: radial-gradient(circle at 50% 0%, rgba(255,255,255,0.03) 0%, transparent 50%);
    border: 1px solid var(--nav-border);
    border-radius: 24px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    position: relative;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}}

/* Navigation */
.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem 3rem;
    border-bottom: 1px solid var(--nav-border);
    z-index: 10;
}}

.nav-logo {{
    font-family: var(--font-heading);
    font-weight: 800;
    font-size: 1.25rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    letter-spacing: -0.5px;
}}

.nav-logo i {{
    color: var(--accent-color);
    font-size: 1.5rem;
}}

.nav-links {{
    display: flex;
    gap: 2.5rem;
}}

.nav-links a {{
    color: var(--text-secondary);
    text-decoration: none;
    font-weight: 500;
    font-size: 0.95rem;
    transition: color 0.2s ease;
}}

.nav-links a:hover {{
    color: var(--text-primary);
}}

.btn-ghost {{
    background: transparent;
    border: 1px solid var(--nav-border);
    color: var(--text-primary);
    padding: 0.6rem 1.25rem;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
}}

.btn-ghost:hover {{
    background: rgba(255,255,255,0.05);
    border-color: rgba(255,255,255,0.2);
}}

/* Main Hero Layout */
.hero-main {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    flex: 1;
    padding: 4rem 3rem;
    gap: 4rem;
    align-items: center;
    z-index: 2;
}}

.hero-content {{
    display: flex;
    flex-direction: column;
    gap: 2rem;
    max-width: 600px;
}}

.hero-title {{
    font-family: var(--font-heading);
    font-size: clamp(3rem, 5vw, 4.5rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.03em;
    text-wrap: balance;
}}

.hero-description {{
    font-size: 1.125rem;
    line-height: 1.6;
    color: var(--text-secondary);
    max-width: 85%;
}}

/* CTA & Social Proof Area */
.hero-action-area {{
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    margin-top: 1rem;
}}

.btn-primary {{
    background: var(--accent-color);
    color: #fff;
    border: none;
    padding: 1rem 2rem;
    font-size: 1.125rem;
    font-weight: 700;
    border-radius: 8px;
    cursor: pointer;
    align-self: flex-start;
    transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.2s ease;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

.btn-primary:hover {{
    transform: translateY(-3px);
    box-shadow: 0 10px 20px -10px var(--accent-color);
}}

.social-proof {{
    display: flex;
    align-items: center;
    gap: 1rem;
}}

.avatar-group {{
    display: flex;
}}

.avatar {{
    width: 36px;
    height: 36px;
    border-radius: 50%;
    border: 3px solid var(--bg-color);
    margin-left: -12px;
    object-fit: cover;
    background-color: #333;
}}

.avatar:first-child {{
    margin-left: 0;
}}

.social-text {{
    font-size: 0.875rem;
    color: var(--text-secondary);
    font-weight: 500;
}}

.social-text strong {{
    color: var(--text-primary);
}}

/* Hero Graphic */
.hero-visual {{
    position: relative;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    perspective: 1000px;
}}

.visual-image {{
    width: 130%;
    max-width: 800px;
    /* Using mix-blend-mode to make a standard space image look like a cutout composite */
    mix-blend-mode: lighten;
    filter: drop-shadow(0 0 40px rgba(0,0,0,0.8));
    transition: transform 0.1s ease-out;
    transform-style: preserve-3d;
}}

/* Trust Logos */
.trust-strip {{
    padding: 2rem 3rem;
    border-top: 1px solid var(--nav-border);
    display: flex;
    align-items: center;
    gap: 2rem;
    background: rgba(0,0,0,0.2);
    z-index: 2;
}}

.trust-label {{
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--text-secondary);
    font-weight: 600;
    white-space: nowrap;
}}

.trust-logos {{
    display: flex;
    gap: 3rem;
    align-items: center;
    flex-wrap: wrap;
}}

.trust-logos i {{
    font-size: 2rem;
    color: #ffffff;
    opacity: {logo_opacity};
    transition: opacity 0.3s ease, transform 0.3s ease;
    cursor: default;
}}

.trust-logos i:hover {{
    opacity: 1;
    transform: translateY(-2px);
}}

/* Responsive */
@media (max-width: 968px) {{
    .hero-main {{
        grid-template-columns: 1fr;
        text-align: center;
        gap: 2rem;
        padding: 3rem 2rem;
    }}
    
    .hero-content {{
        margin: 0 auto;
        align-items: center;
    }}
    
    .hero-description {{
        max-width: 100%;
    }}
    
    .btn-primary {{
        align-self: center;
    }}
    
    .nav-links {{
        display: none;
    }}
    
    .trust-strip {{
        flex-direction: column;
        gap: 1rem;
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Montserrat:wght@700;800;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <div class="hero-wrapper">
        <!-- Navigation -->
        <nav class="navbar">
            <div class="nav-logo">
                <i class="fa-solid fa-meteor"></i>
                Alliance
            </div>
            <div class="nav-links">
                <a href="#">Our Ships</a>
                <a href="#">Mission</a>
                <a href="#">Donations</a>
            </div>
            <button class="btn-ghost">Log In</button>
        </nav>

        <!-- Main Content -->
        <main class="hero-main">
            <div class="hero-content">
                <h1 class="hero-title">{title_text}</h1>
                <p class="hero-description">{body_text}</p>
                
                <div class="hero-action-area">
                    <button class="btn-primary">Join Now For Free</button>
                    
                    <div class="social-proof">
                        <div class="avatar-group">
                            <img src="https://i.pravatar.cc/100?img=11" alt="User" class="avatar">
                            <img src="https://i.pravatar.cc/100?img=12" alt="User" class="avatar">
                            <img src="https://i.pravatar.cc/100?img=33" alt="User" class="avatar">
                            <img src="https://i.pravatar.cc/100?img=14" alt="User" class="avatar">
                        </div>
                        <div class="social-text">
                            <strong>Obi Wan</strong> and <strong>4,000 others</strong> have already joined
                        </div>
                    </div>
                </div>
            </div>

            <div class="hero-visual">
                <!-- Using an abstract space/tech placeholder that works well with screen/lighten blend modes -->
                <img src="https://images.unsplash.com/photo-1614732414444-096e5f1122a5?q=80&w=1000&auto=format&fit=crop" alt="Hero Graphic" class="visual-image" id="parallax-img">
            </div>
        </main>

        <!-- Trust Signals -->
        <div class="trust-strip">
            <span class="trust-label">As seen on</span>
            <div class="trust-logos">
                <i class="fa-brands fa-aws"></i>
                <i class="fa-brands fa-space-awesome"></i>
                <i class="fa-brands fa-reddit-alien"></i>
                <i class="fa-brands fa-galactic-senate"></i>
                <i class="fa-brands fa-rebel"></i>
            </div>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    js = """// Epic Dark Mode Hero - Interaction Logic
document.addEventListener('DOMContentLoaded', () => {
    const wrapper = document.querySelector('.hero-wrapper');
    const visualImg = document.getElementById('parallax-img');
    
    // Subtle Parallax Effect on Mouse Move to simulate depth
    if (window.matchMedia("(hover: hover)").matches) {
        wrapper.addEventListener('mousemove', (e) => {
            const rect = wrapper.getBoundingClientRect();
            
            // Calculate mouse position relative to the center of the wrapper
            const centerX = rect.left + rect.width / 2;
            const centerY = rect.top + rect.height / 2;
            
            const moveX = (e.clientX - centerX) / centerX;
            const moveY = (e.clientY - centerY) / centerY;
            
            // Apply a slight inverse translation and rotation for a 3D float effect
            const maxTranslation = 20; // pixels
            const maxRotation = 5; // degrees
            
            visualImg.style.transform = `
                translate(${-moveX * maxTranslation}px, ${-moveY * maxTranslation}px)
                rotateY(${moveX * maxRotation}deg)
                rotateX(${-moveY * maxRotation}deg)
            `;
        });
        
        // Reset position when mouse leaves
        wrapper.addEventListener('mouseleave', () => {
            visualImg.style.transform = `translate(0px, 0px) rotateY(0deg) rotateX(0deg)`;
            visualImg.style.transition = 'transform 0.5s ease-out';
        });
        
        // Remove transition during active movement for snappiness
        wrapper.addEventListener('mouseenter', () => {
            visualImg.style.transition = 'none';
        });
    }
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
  - Semantic HTML tags (`<nav>`, `<main>`, `<h1>`) are used for proper document outline.
  - Color contrast meets WCAG AA standards (white text on near-black background). The muted secondary text (`#8b949e`) on the very dark background (`#080b13`) has a contrast ratio of ~4.9:1, which passes the 4.5:1 requirement for normal text.
  - The `alt` attributes are provided for the avatars and the main feature image.
  - Social proof avatars should theoretically have proper descriptive `alt` tags if representing real people; placeholders here use generic text.
* **Performance**:
  - The parallax effect in `script.js` uses simple CSS transforms (`translate`, `rotate`) which are GPU-accelerated, avoiding layout thrashing.
  - The `mousemove` event is not artificially throttled via `requestAnimationFrame` here because the calculations are extremely lightweight, but in a production environment with other heavy scripts, wrapping the transform update in a `requestAnimationFrame` would be best practice.
  - FontAwesome is loaded via CDN; in a strict performance environment, extracting only the 5 required SVG paths and inline them into the HTML would save a render-blocking network request.
  - The `mix-blend-mode` on the image is relatively cheap on modern devices but can cause slight composite layer repaints on very old mobile hardware.