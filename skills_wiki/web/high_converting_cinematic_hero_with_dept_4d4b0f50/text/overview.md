### 1. High-level Design Pattern Extraction

> **Skill Name**: High-Converting Cinematic Hero with Depth Composition & Social Proof

* **Core Visual Mechanism**: A dramatic, two-column split layout using a deep, dark theme (often space or abstract textures). It utilizes extreme depth of field—layering a far-background element (like a planet or distant texture), a mid-ground focus, and a prominent foreground subject that breaks the grid on the right side. On the left, it employs high-contrast typography and dense "trust signal" clustering (overlapping avatars and media logos) directly surrounding the primary Call to Action (CTA).
* **Why Use This Skill (Rationale)**: This layout is engineered for conversion. The dark background creates an immersive, premium, or dramatic feel. By clustering the CTA with social proof (avatars showing "others joined") and authority signals ("As seen on"), it lowers user friction and builds immediate trust. The visual depth guides the eye across the screen from the copy to the hero image.
* **Overall Applicability**: Perfect for SaaS landing pages, gaming websites, movie promotions, event registrations, or any high-stakes recruitment/signup page where building excitement and trust simultaneously is crucial.
* **Value Addition**: Transforms a standard text-and-image header into an immersive narrative experience. It doesn't just present information; it creates an atmosphere and actively works to overcome user hesitation through visual psychology.
* **Browser Compatibility**: Fully supported in modern browsers. Uses CSS Grid, Flexbox, native CSS filters, and basic DOM event listeners for parallax. Minimum required: Chrome 57+, Firefox 52+, Safari 10.1+.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**: Deep, near-black space background (`#050814`). High contrast white text (`#ffffff`) for headlines, slightly dimmed grey (`#a0aab8`) for body copy to reduce eye strain. A stark, saturated accent color (e.g., Rebel Red `#e62429` or Cyan) for the primary CTA button.
  - **Typographic Hierarchy**:
    - Headline: Very large, bold, tightly spaced (e.g., `Oswald` or `Titling Gothic`), conveying urgency or scale.
    - Body: Clean, highly legible sans-serif (e.g., `Inter`).
    - Labels ("As seen on"): Small, all-caps, highly tracked (spaced out) for a refined look.
  - **Trust Signals**: Small circular avatars (32px) overlapping by `-10px` with a border matching the background. Logos rendered in monochrome white with reduced opacity (`0.5`).

* **Step B: Layout & Compositional Style**
  - **Layout System**: CSS Grid creates the primary 2-column structure (`1fr 1fr`).
  - **Composition**: The left column acts as the anchor, strictly left-aligned. The right column acts as a stage.
  - **Z-index Layering**:
    1. Base Background (Stars/Texture)
    2. Deep Background Object (Planet/Death Star)
    3. Grid Container (Text on left)
    4. Foreground Hero Object (Ship/Product breaking out of its container bounds).

* **Step C: Interactive Behavior & Animations**
  - **Hover Effects**: CTA button scales up slightly (`scale(1.05)`) with a glow effect on hover. Ghost buttons in the nav reverse their colors.
  - **Parallax Depth**: JavaScript tracks mouse movement to shift the background, deep objects, and foreground objects at different rates, simulating a 3D environment.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Primary Layout** | CSS Grid | Provides rigid structure for the 2-column split while allowing absolute positioning for depth layers. |
| **Trust Clusters** | CSS Flexbox | Perfect for aligning the overlapping avatars and the row of authority logos. |
| **Visual Depth / Layers** | CSS `absolute` + `z-index` | Allows elements to exist outside standard document flow to create foreground/background separation. |
| **Cinematic Parallax** | JavaScript `mousemove` | Calculates cursor position to translate layered elements at varying speeds, creating the core "depth" illusion seen in the tutorial's composition logic. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "It's your universe, it's time to save it",
    body_text: str = "The alliance is fighting to get rid of the evil empire. Join the resistance to create a better future for everyone.",
    color_scheme: str = "dark",
    accent_color: str = "#e62429",
    width_px: int = 1440,
    height_px: int = 900,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Cinematic Hero with Depth & Social Proof.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Note: color_scheme parameter is accepted but the core pattern 
    # relies heavily on a dark, cinematic aesthetic for the contrast to work as intended.
    bg_color = "#070b14" if color_scheme == "dark" else "#1a1a24"
    text_color = "#ffffff"
    text_muted = "#9ca3af"

    css = f"""/* Cinematic Hero Component */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Oswald:wght@600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-base: {bg_color};
    --text-main: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --container-width: 1200px;
}}

body {{
    font-family: 'Inter', sans-serif;
    background-color: var(--bg-base);
    color: var(--text-main);
    min-height: 100vh;
    overflow-x: hidden;
}}

/* --- Navigation --- */
nav {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2rem 5%;
    max-width: var(--container-width);
    margin: 0 auto;
    position: relative;
    z-index: 10;
}}

.logo {{
    font-family: 'Oswald', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: 1px;
    display: flex;
    align-items: center;
    gap: 10px;
}}

.logo-mark {{
    width: 32px;
    height: 32px;
    background: var(--accent);
    border-radius: 50%;
    /* Abstract logo representation */
    clip-path: polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%);
}}

.nav-links {{
    display: flex;
    gap: 2rem;
    list-style: none;
}}

.nav-links a {{
    color: var(--text-main);
    text-decoration: none;
    font-size: 0.9rem;
    font-weight: 500;
    transition: opacity 0.3s;
}}

.nav-links a:hover {{
    opacity: 0.7;
}}

.btn-ghost {{
    padding: 0.75rem 1.5rem;
    background: transparent;
    border: 2px solid var(--text-main);
    color: var(--text-main);
    font-weight: 600;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.3s ease;
}}

.btn-ghost:hover {{
    background: var(--text-main);
    color: var(--bg-base);
}}

/* --- Hero Section & Layout --- */
.hero-wrapper {{
    position: relative;
    width: 100vw;
    height: calc(100vh - 100px); /* subtract nav height roughly */
    min-height: 700px;
    overflow: hidden;
    display: flex;
    align-items: center;
}}

/* Depth Layers */
.layer {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    will-change: transform;
}}

.layer-bg {{
    background-image: radial-gradient(circle at center, rgba(255,255,255,0.05) 0%, transparent 70%),
                      url('https://images.unsplash.com/photo-1506703719100-a0f3a48c0f41?q=80&w=2000&auto=format&fit=crop');
    background-size: cover;
    background-position: center;
    opacity: 0.4;
    z-index: 1;
    transform: scale(1.1); /* Buffer for parallax movement */
}}

.layer-mid {{
    z-index: 2;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding-right: 15%;
}}

/* Simulated planet/Death Star in background */
.distant-object {{
    width: 400px;
    height: 400px;
    border-radius: 50%;
    background: radial-gradient(circle at 30% 30%, #3a4052, #0d111c);
    box-shadow: inset -30px -30px 60px rgba(0,0,0,0.8), 0 0 100px rgba(0,0,0,0.5);
    opacity: 0.6;
    filter: blur(2px);
}}

.hero-container {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    max-width: var(--container-width);
    margin: 0 auto;
    padding: 0 5%;
    position: relative;
    z-index: 5;
    width: 100%;
}}

/* --- Left Column: Content & Trust Signals --- */
.hero-content {{
    display: flex;
    flex-direction: column;
    justify-content: center;
}}

.title {{
    font-family: 'Oswald', sans-serif;
    font-size: clamp(3.5rem, 5vw, 5.5rem);
    line-height: 1.1;
    text-transform: uppercase;
    letter-spacing: -1px;
    margin-bottom: 1.5rem;
    text-shadow: 0 10px 30px rgba(0,0,0,0.5);
}}

.body-text {{
    font-size: 1.125rem;
    line-height: 1.6;
    color: var(--text-muted);
    margin-bottom: 2.5rem;
    max-width: 90%;
}}

.cta-group {{
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    margin-bottom: 3rem;
}}

.btn-primary {{
    align-self: flex-start;
    padding: 1rem 2.5rem;
    background: var(--accent);
    color: white;
    font-size: 1.125rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    box-shadow: 0 4px 15px rgba(230, 36, 41, 0.3);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}}

.btn-primary:hover {{
    transform: translateY(-2px) scale(1.02);
    box-shadow: 0 8px 25px rgba(230, 36, 41, 0.5);
}}

/* Social Proof Avatars */
.social-proof {{
    display: flex;
    align-items: center;
    gap: 1rem;
}}

.avatars {{
    display: flex;
}}

.avatar {{
    width: 36px;
    height: 36px;
    border-radius: 50%;
    border: 2px solid var(--bg-base);
    margin-left: -12px;
    background-size: cover;
}}

.avatar:nth-child(1) {{ margin-left: 0; background-color: #4b5563; }}
.avatar:nth-child(2) {{ background-color: #6b7280; }}
.avatar:nth-child(3) {{ background-color: #9ca3af; }}
.avatar:nth-child(4) {{ background-color: #d1d5db; }}

.proof-text {{
    font-size: 0.875rem;
    color: var(--text-muted);
}}

.proof-text strong {{
    color: var(--text-main);
}}

/* Authority Logos */
.authority-signals {{
    margin-top: auto;
    border-top: 1px solid rgba(255,255,255,0.1);
    padding-top: 1.5rem;
}}

.authority-label {{
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--text-muted);
    margin-bottom: 1rem;
}}

.logos-container {{
    display: flex;
    gap: 2rem;
    align-items: center;
    opacity: 0.5;
    filter: grayscale(100%) contrast(200%);
}}

.logo-placeholder {{
    font-family: 'Oswald', sans-serif;
    font-weight: 700;
    font-size: 1.2rem;
}}

/* --- Right Column: Foreground Image --- */
.hero-visual {{
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
}}

/* Represents the hero ship/product breaking out of layout */
.hero-object {{
    position: relative;
    z-index: 10;
    width: 120%; /* Break grid bounds */
    height: 400px;
    margin-right: -20%;
    background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 100%);
    backdrop-filter: blur(10px);
    border-top: 1px solid rgba(255,255,255,0.2);
    border-left: 1px solid rgba(255,255,255,0.2);
    border-radius: 20px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    transform: perspective(1000px) rotateY(-15deg) rotateX(5deg);
    display: flex;
    align-items: center;
    justify-content: center;
    color: rgba(255,255,255,0.5);
    font-style: italic;
    transition: transform 0.1s ease-out;
}}

/* Engine glow effect */
.hero-object::after {{
    content: '';
    position: absolute;
    bottom: -20px;
    right: 10%;
    width: 100px;
    height: 30px;
    background: var(--accent);
    filter: blur(30px);
    border-radius: 50%;
}}

@media (max-width: 968px) {{
    .hero-container {{
        grid-template-columns: 1fr;
        text-align: center;
    }}
    .hero-content {{
        align-items: center;
    }}
    .btn-primary {{
        align-self: center;
    }}
    .hero-visual {{
        display: none; /* Simplify on mobile or adjust stacking */
    }}
    .distant-object {{
        right: 50%;
        transform: translateX(50%);
    }}
    .nav-links {{ display: none; }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cinematic Hero</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <nav>
        <div class="logo">
            <div class="logo-mark"></div>
            ALLIANCE
        </div>
        <ul class="nav-links">
            <li><a href="#">Our Fleet</a></li>
            <li><a href="#">Mission</a></li>
            <li><a href="#">Intel</a></li>
        </ul>
        <button class="btn-ghost">LOG IN</button>
    </nav>

    <main class="hero-wrapper">
        <!-- Parallax Depth Layers -->
        <div class="layer layer-bg" data-speed="0.02"></div>
        <div class="layer layer-mid" data-speed="0.05">
            <div class="distant-object"></div>
        </div>

        <div class="hero-container">
            <div class="hero-content">
                <h1 class="title">{title_text}</h1>
                <p class="body-text">{body_text}</p>
                
                <div class="cta-group">
                    <button class="btn-primary">Join Now For Free</button>
                    
                    <!-- Trust Cluster: Social Proof -->
                    <div class="social-proof">
                        <div class="avatars">
                            <div class="avatar" style="background-image: url('https://i.pravatar.cc/100?img=11');"></div>
                            <div class="avatar" style="background-image: url('https://i.pravatar.cc/100?img=12');"></div>
                            <div class="avatar" style="background-image: url('https://i.pravatar.cc/100?img=33');"></div>
                            <div class="avatar" style="background-image: url('https://i.pravatar.cc/100?img=14');"></div>
                        </div>
                        <div class="proof-text">
                            <strong>Obi Wan</strong> and 4,000 others joined
                        </div>
                    </div>
                </div>

                <!-- Trust Cluster: Authority Proof -->
                <div class="authority-signals">
                    <div class="authority-label">Verified Transmissions By</div>
                    <div class="logos-container">
                        <div class="logo-placeholder">CNY</div>
                        <div class="logo-placeholder">GALAXY NEWS</div>
                        <div class="logo-placeholder">HOLONET</div>
                    </div>
                </div>
            </div>

            <div class="hero-visual layer" data-speed="-0.08">
                <!-- Stand-in for the main hero object (e.g. Spaceship) -->
                <div class="hero-object">
                    [ Hero Foreground Subject ]
                </div>
            </div>
        </div>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Parallax Depth Effect Script
document.addEventListener('DOMContentLoaded', () => {{
    const layers = document.querySelectorAll('.layer');
    const heroObject = document.querySelector('.hero-object');
    
    let mouseX = 0;
    let mouseY = 0;
    let currentX = 0;
    let currentY = 0;

    // Listen for mouse movement
    window.addEventListener('mousemove', (e) => {{
        // Normalize mouse coordinates from -1 to 1 based on screen center
        mouseX = (e.clientX - window.innerWidth / 2) / (window.innerWidth / 2);
        mouseY = (e.clientY - window.innerHeight / 2) / (window.innerHeight / 2);
    }});

    // Animation loop for smooth easing
    function animate() {{
        // Ease current coordinates towards target coordinates
        currentX += (mouseX - currentX) * 0.1;
        currentY += (mouseY - currentY) * 0.1;

        // Apply transforms to parallax layers
        layers.forEach(layer => {{
            const speed = parseFloat(layer.getAttribute('data-speed'));
            const x = currentX * window.innerWidth * speed;
            const y = currentY * window.innerHeight * speed;
            
            // Maintain original scale if present
            const scale = layer.classList.contains('layer-bg') ? 'scale(1.1)' : '';
            layer.style.transform = `${scale} translate(${{x}}px, ${{y}}px)`;
        }});

        // Add subtle rotation tilt to the main hero object
        if (heroObject) {{
            const rotX = 5 - (currentY * 10);
            const rotY = -15 + (currentX * 10);
            heroObject.style.transform = `perspective(1000px) rotateY(${{rotY}}deg) rotateX(${{rotX}}deg)`;
        }}

        requestAnimationFrame(animate);
    }}

    animate();
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
  - The color scheme ensures high contrast (white text on near-black background).
  - Semantic HTML structure (`<nav>`, `<main>`, `<h1>`).
  - To be fully accessible, the placeholder avatars should ideally have `aria-label` or `alt` attributes if they were `<img>` tags (used as background-images here for easy styling, which hides them from screen readers—acceptable since they are purely decorative social proof, and the adjacent text conveys the meaning).
  - *Recommendation*: Add a `prefers-reduced-motion` media query in CSS to disable the JavaScript parallax loop and CSS transition times for users sensitive to motion.
* **Performance**:
  - The parallax effect uses `requestAnimationFrame` and interpolates values (easing) to ensure smooth 60fps rendering without jank, rather than firing CSS updates directly on every single `mousemove` event.
  - Parallax elements use `will-change: transform` to hint to the browser to promote them to their own GPU layers, preventing costly repaints of the entire document during mouse movement.