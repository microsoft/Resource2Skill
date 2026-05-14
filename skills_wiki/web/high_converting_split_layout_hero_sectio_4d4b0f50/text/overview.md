### 1. High-level Design Pattern Extraction

> **Skill Name**: High-Converting Split-Layout Hero Section

* **Core Visual Mechanism**: A Z-pattern, dark-themed hero section utilizing stark contrast (deep background, bright white text, vibrant accent button). It features a split composition where the left side serves as an anchored text hierarchy (Headline -> Subtitle -> Primary CTA -> Social Proof -> Trust Badges), and the right side hosts a dynamic, large-scale visual that breaks out of a rigid grid to create depth and motion.
* **Why Use This Skill (Rationale)**: This is a masterclass in conversion-driven design. By stacking value propositions (the headline), removing friction (the CTA saying "for free"), providing immediate social validation (avatar stack), and establishing authority (media logos), it systematically answers user objections within the first viewport.
* **Overall Applicability**: Essential for SaaS landing pages, recruitment portals, campaign websites, and product launches where capturing immediate user buy-in is critical.
* **Value Addition**: Transforms a standard introductory header into a persuasive, high-trust funnel entry point. The combination of floating visuals and strict left-aligned typographic hierarchy guides the eye precisely where the designer wants it to go.
* **Browser Compatibility**: Fully compatible with modern browsers. Relies on standard CSS Flexbox/Grid, `mix-blend-mode` for image compositing, and standard DOM events for subtle interaction. (Supported in Chrome 49+, Safari 10+, Firefox 52+).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**: Deep space dark background (`#07080A`), stark white text (`#FFFFFF`), muted secondary text (`#A1A1AA`), and a highly visible accent color (e.g., bright red `#E62429` or cyan) for the primary conversion button.
  - **Typographic Hierarchy**: Sans-serif, tightly tracked fonts (like `Inter` or `Titling Gothic`). The `h1` is massive (e.g., 3.5rem, weight 800, `-0.02em` letter-spacing). The subtitle is readable and medium-weight (1.125rem).
  - **Social Proof & Trust**: Small, circular avatars stacked with a negative left margin (`-10px`) and white borders to separate them. Trust logos are rendered in a single color (usually white/grey) with reduced opacity (`0.5`) to not distract from the main CTA.

* **Step B: Layout & Compositional Style**
  - **Layout System**: The main wrapper is a two-column CSS Grid (`grid-template-columns: 1.2fr 1fr`) on desktop, collapsing to a single column on mobile. 
  - **Navigation**: A top Flexbox bar featuring a logo on the far left, centered navigation links, and a secondary "Ghost" (outlined) CTA on the far right.
  - **Image Compositing**: To mimic the Photoshop "composite" technique shown in the video, the right-side image uses `mix-blend-mode: screen` or `lighten` over the dark background, allowing subjects (like a spaceship or astronaut) to appear seamlessly integrated into the space background without needing a transparent PNG.

* **Step C: Interactive Behavior & Animations**
  - **Hover Effects**: Buttons scale slightly (`transform: scale(1.02)`) and ghost buttons fill with the accent color.
  - **Parallax Animation**: A lightweight JavaScript mouse-move event listener applies a subtle translation (`transform: translate(x, y)`) to the main visual, simulating the floating 3D depth of space.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Responsive Split Layout** | CSS Grid & Flexbox | Cleanest way to manage the 2-column hero and 1-column mobile degradation without JS. |
| **Photoshop-like Compositing** | CSS `mix-blend-mode` | Using `screen` or `lighten` allows stock imagery with black backgrounds to seamlessly blend into our dark hero background, exactly mirroring the video's composite style. |
| **Social Proof / Trust Badges** | CSS Flexbox + Negative Margins | The avatar stack requires `margin-left: -12px` and `z-index` management. Trust badges use FontAwesome for clean, monochrome SVGs. |
| **Floating Depth Effect** | Vanilla JS `mousemove` | Adds an interactive parallax feel to the hero image, elevating the perceived quality of the page. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "It's your universe, it's time to save it",
    body_text: str = "The Rebel alliance is fighting to get rid of the evil empire. Join the resistance to create a better future for your children.",
    color_scheme: str = "dark",
    accent_color: str = "#E62429",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the High-Converting Split-Layout Hero Section.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Force dark theme for the space/rebel aesthetic shown in the tutorial
    bg_color = "#07080A"
    text_color = "#FFFFFF"
    muted_text = "#A1A1AA"
    surface_border = "rgba(255, 255, 255, 0.1)"

    css = f"""/* High-Converting Hero Section */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --muted: {muted_text};
    --accent: {accent_color};
    --border: {surface_border};
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    /* Subtle starry background gradient */
    background-image: 
        radial-gradient(circle at 15% 50%, rgba(255,255,255,0.04) 0%, transparent 50%),
        radial-gradient(circle at 85% 30%, rgba(255,255,255,0.04) 0%, transparent 50%);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    overflow-x: hidden;
}}

.hero-wrapper {{
    width: 100%;
    max-width: {width_px}px;
    min-height: {height_px}px;
    padding: 2rem 5%;
    display: flex;
    flex-direction: column;
}}

/* --- Navigation --- */
header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 2rem;
    border-bottom: 1px solid var(--border);
}}

.logo {{
    font-size: 1.5rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

.logo i {{
    color: var(--accent);
}}

nav ul {{
    display: flex;
    gap: 2.5rem;
    list-style: none;
}}

nav a {{
    color: var(--text);
    text-decoration: none;
    font-size: 0.95rem;
    font-weight: 500;
    transition: color 0.2s ease;
}}

nav a:hover {{
    color: var(--accent);
}}

/* --- Buttons --- */
.btn {{
    padding: 0.75rem 1.5rem;
    font-size: 0.95rem;
    font-weight: 600;
    text-decoration: none;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.3s ease;
    display: inline-flex;
    align-items: center;
    justify-content: center;
}}

.btn-ghost {{
    background: transparent;
    color: var(--text);
    border: 2px solid var(--border);
}}

.btn-ghost:hover {{
    border-color: var(--text);
}}

.btn-primary {{
    background: var(--accent);
    color: #fff;
    border: 2px solid var(--accent);
    padding: 1rem 2rem;
    font-size: 1.1rem;
}}

.btn-primary:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(230, 36, 41, 0.3);
}}

/* --- Hero Layout --- */
.hero-content {{
    display: grid;
    grid-template-columns: 1.1fr 1fr;
    gap: 4rem;
    flex-grow: 1;
    align-items: center;
    margin-top: 3rem;
}}

/* --- Left Column: Typography & Conversion --- */
.hero-text-block {{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 1.5rem;
    z-index: 10;
}}

h1 {{
    font-size: 4rem;
    line-height: 1.1;
    font-weight: 800;
    letter-spacing: -0.03em;
}}

p.subtitle {{
    font-size: 1.15rem;
    line-height: 1.6;
    color: var(--muted);
    max-width: 90%;
}}

/* --- Social Proof --- */
.social-proof {{
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-top: 1rem;
}}

.avatars {{
    display: flex;
}}

.avatars img {{
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: 2px solid var(--bg);
    object-fit: cover;
    margin-left: -12px;
}}

.avatars img:first-child {{
    margin-left: 0;
}}

.social-text {{
    font-size: 0.85rem;
    color: var(--muted);
}}

.social-text strong {{
    color: var(--text);
}}

/* --- Trust Badges --- */
.trust-badges {{
    margin-top: 3rem;
    padding-top: 2rem;
    border-top: 1px solid var(--border);
    width: 100%;
}}

.trust-badges p {{
    font-size: 0.8rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 1rem;
}}

.logos {{
    display: flex;
    gap: 2rem;
    align-items: center;
    opacity: 0.4;
    filter: grayscale(100%);
    transition: opacity 0.3s ease;
}}

.logos:hover {{
    opacity: 0.8;
}}

.logos i {{
    font-size: 1.8rem;
}}

/* --- Right Column: Visual Compositing --- */
.hero-visual {{
    position: relative;
    width: 100%;
    height: 100%;
    min-height: 500px;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.composite-image {{
    width: 140%; /* Break out of grid */
    max-width: 800px;
    height: auto;
    object-fit: contain;
    /* This perfectly blends black-background stock photos into our dark UI */
    mix-blend-mode: screen; 
    filter: drop-shadow(0 0 30px rgba(255,255,255,0.1));
    will-change: transform;
}}

/* Responsive */
@media (max-width: 968px) {{
    .hero-content {{
        grid-template-columns: 1fr;
        text-align: center;
        gap: 2rem;
    }}
    .hero-text-block {{
        align-items: center;
    }}
    p.subtitle {{
        max-width: 100%;
    }}
    .social-proof {{
        justify-content: center;
    }}
    .logos {{
        justify-content: center;
    }}
    nav ul {{
        display: none; /* simple mobile hide for demo */
    }}
    h1 {{
        font-size: 2.8rem;
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <!-- Typography -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;800&display=swap" rel="stylesheet">
    <!-- Trust Logos via FontAwesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <div class="hero-wrapper">
        <header>
            <div class="logo">
                <i class="fa-solid fa-jedi"></i> REBEL
            </div>
            <nav>
                <ul>
                    <li><a href="#">Our Ships</a></li>
                    <li><a href="#">Mission</a></li>
                    <li><a href="#">Donations</a></li>
                </ul>
            </nav>
            <a href="#" class="btn btn-ghost">JOIN NOW</a>
        </header>

        <main class="hero-content">
            
            <div class="hero-text-block">
                <h1>{title_text}</h1>
                <p class="subtitle">{body_text}</p>
                
                <a href="#" class="btn btn-primary">JOIN NOW FOR FREE</a>
                
                <div class="social-proof">
                    <div class="avatars">
                        <!-- UI Faces for social proof -->
                        <img src="https://randomuser.me/api/portraits/men/32.jpg" alt="User">
                        <img src="https://randomuser.me/api/portraits/women/44.jpg" alt="User">
                        <img src="https://randomuser.me/api/portraits/men/86.jpg" alt="User">
                        <img src="https://randomuser.me/api/portraits/women/12.jpg" alt="User">
                    </div>
                    <div class="social-text">
                        <strong>Obi Wan</strong> and 4,000 others have already joined
                    </div>
                </div>

                <div class="trust-badges">
                    <p>As Seen On:</p>
                    <div class="logos">
                        <i class="fa-brands fa-aws"></i>
                        <i class="fa-brands fa-google"></i>
                        <i class="fa-brands fa-meta"></i>
                        <i class="fa-brands fa-spotify"></i>
                    </div>
                </div>
            </div>

            <div class="hero-visual">
                <!-- Using an Unsplash dark-background image blended with screen mode -->
                <img src="https://images.unsplash.com/photo-1614729939124-032f0b56c9ce?q=80&w=1000&auto=format&fit=crop" 
                     alt="Floating Astronaut Composite" 
                     class="composite-image" 
                     id="parallax-img">
            </div>

        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    js = """// Parallax Effect for the Hero Visual
document.addEventListener('DOMContentLoaded', () => {
    const heroVisual = document.querySelector('.hero-visual');
    const image = document.getElementById('parallax-img');

    if (heroVisual && image) {
        heroVisual.addEventListener('mousemove', (e) => {
            // Calculate mouse position relative to the container center
            const rect = heroVisual.getBoundingClientRect();
            const centerX = rect.left + rect.width / 2;
            const centerY = rect.top + rect.height / 2;
            
            const moveX = (e.clientX - centerX) * 0.03;
            const moveY = (e.clientY - centerY) * 0.03;

            // Apply smooth translation
            requestAnimationFrame(() => {
                image.style.transform = `translate(${moveX}px, ${moveY}px)`;
            });
        });

        // Reset position when mouse leaves
        heroVisual.addEventListener('mouseleave', () => {
            requestAnimationFrame(() => {
                image.style.transform = `translate(0px, 0px)`;
                image.style.transition = `transform 0.5s ease-out`;
            });
        });

        // Remove transition during active mousemove to prevent lag
        heroVisual.addEventListener('mouseenter', () => {
            image.style.transition = `none`;
        });
    }
});
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

* **Accessibility**: 
  - Semantic HTML (`<header>`, `<nav>`, `<main>`) is used to organize the page structure natively for screen readers.
  - The contrast ratio between the text (`#FFFFFF` and `#A1A1AA`) against the background (`#07080A`) passes WCAG AAA compliance.
  - Interactive elements (buttons, navigation) are styled distinctly, though standard `:focus-visible` outlines should be added if adapting for production.
* **Performance**:
  - **CSS Compositing**: By using `mix-blend-mode: screen`, we avoid needing a massive, unoptimized transparent PNG. The browser GPU handles the blending of the standard compressed JPG.
  - **Parallax Optimization**: The JavaScript mousemove event is decoupled from the DOM manipulation via `requestAnimationFrame()`, preventing layout thrashing and ensuring the floating animation remains buttery smooth (60fps). `will-change: transform` is applied to the image to hint the browser to hardware-accelerate the layer.