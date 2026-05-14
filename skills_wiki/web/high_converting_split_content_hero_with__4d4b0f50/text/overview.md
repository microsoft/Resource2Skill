### 1. High-level Design Pattern Extraction

> **Skill Name**: High-Converting Split-Content Hero with Social Proof

* **Core Visual Mechanism**: A full-bleed, cinematic split-screen layout (roughly 60/40 text-to-image ratio). It features massive, tightly-leaded uppercase typography on the left, counterbalanced by a large dynamic visual on the right. Crucially, it clusters conversion elements—a vibrant primary CTA button and overlapping avatar social proof—immediately below the primary value proposition, anchoring the page with an "As Seen On" trust bar at the bottom.
* **Why Use This Skill (Rationale)**: This is a battle-tested pattern in conversion rate optimization (CRO). It leverages the F-pattern reading behavior: the eye scans from the top-left logo, drops to the massive headline, reads the subhead, and stops at the brightly colored CTA. Embedding social proof (avatars) directly adjacent to the CTA reduces friction and builds immediate trust right at the point of action.
* **Overall Applicability**: Ideal for SaaS landing pages, gaming/Web3 platforms, political or movement recruitment (as seen in the video's "Rebel Alliance" example), and high-ticket service sales pages. It works best when you have a singular, highly desirable action you want the user to take.
* **Value Addition**: Compared to a standard centered text hero, this layout provides superior information density while maintaining breathability. It separates the logical appeal (text/trust badges) from the emotional appeal (dynamic imagery), allowing both to shine without overlapping and hurting legibility.
* **Browser Compatibility**: Fully supported in all modern browsers. Uses standard CSS Flexbox and Grid.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**: Deep, dark cinematic background (`#0a0b10`) contrasted with a high-energy accent color (e.g., Star Wars red `#e62429`). Text is high-contrast white (`#ffffff`) for headings and a softer gray (`#8a8d98`) for body text to reduce eye strain.
  - **Typographic Hierarchy**:
    - *Headings*: Ultra-bold, condensed sans-serif (e.g., `Oswald`), uppercase, very tight line-height (`1.05`), large font sizes (`clamp(3rem, 5vw, 5.5rem)`).
    - *Body/UI*: Clean, readable geometric sans-serif (e.g., `Inter`), regular weight, relaxed line-height (`1.6`).
  - **Trust Signals**: Circular overlapping avatars (`border-radius: 50%`, `margin-left: -10px`, bordered by background color to create visual separation). Desaturated network logos at the footer (`filter: grayscale(100%) opacity(50%)`).

* **Step B: Layout & Compositional Style**
  - **Overall Container**: `min-height: 100vh` using Flexbox column layout.
  - **Header & Footer**: Flex containers with `justify-content: space-between` and `align-items: center`.
  - **Main Content**: CSS Grid (`grid-template-columns: 1.2fr 1fr`). The text column is constrained slightly to ensure readable line lengths, while the image column is allowed to bleed towards the right edge.
  - **Z-index**: The floating visual element is kept at a lower z-index than the text to prevent interference on smaller screens.

* **Step C: Interactive Behavior & Animations**
  - **Hover States**: Buttons scale up slightly (`transform: scale(1.05)`) and increase shadow intensity on hover. Ghost buttons invert colors or gain an outline glow.
  - **Parallax Motion**: A subtle JavaScript-driven mousemove event shifts the right-side visual element opposite to the cursor, providing a "cinematic 3D" feel fitting for a space/epic theme.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Split Layout Structure | CSS Grid + Flexbox | Grid handles the 60/40 split perfectly, Flexbox manages header/footer alignment. |
| Cinematic Typography | Google Fonts (Oswald/Inter) | Closely matches the bold "Titling Gothic" aesthetic from the tutorial. |
| Overlapping Avatars | CSS Negative Margin | Pure CSS solution (`margin-left: -12px`) for stacking images without JS. |
| Dynamic 3D Visual | JS `mousemove` + CSS Transform | Simple, performant way to mimic the floating spaceship effect without heavy WebGL. |
| Starfield/Space Depth | CSS Radial Gradient | Achieves the cinematic vignette lighting effect purely in CSS. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "It's your universe, it's time to save it",
    body_text: str = "The Rebel alliance is fighting to get rid of the evil empire. Join the resistance to create a better future for your children.",
    color_scheme: str = "dark",
    accent_color: str = "#e62429",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the High-Converting Split-Content Hero pattern.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#0a0b10"
        bg_gradient = f"radial-gradient(circle at 75% 50%, rgba(255,255,255,0.08) 0%, {bg_color} 60%)"
        text_color = "#ffffff"
        text_muted = "#8a8d98"
        border_color = "rgba(255, 255, 255, 0.15)"
        logo_filter = "grayscale(100%) opacity(0.4) brightness(200%)"
    else:
        bg_color = "#ffffff"
        bg_gradient = f"radial-gradient(circle at 75% 50%, rgba(0,0,0,0.05) 0%, {bg_color} 60%)"
        text_color = "#111827"
        text_muted = "#4b5563"
        border_color = "rgba(0, 0, 0, 0.15)"
        logo_filter = "grayscale(100%) opacity(0.5)"

    css = f"""/* High-Converting Split Hero */
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@600;700&family=Inter:wght@400;500;600&display=swap');

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --border: {border_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: var(--bg);
    background-image: {bg_gradient};
    color: var(--text);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    overflow-x: hidden;
}}

.hero-container {{
    width: 100%;
    max-width: var(--width);
    min-height: var(--height);
    display: flex;
    flex-direction: column;
    position: relative;
}}

/* --- Header Navigation --- */
.header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2rem 4rem;
    z-index: 10;
}}

.logo {{
    font-family: 'Oswald', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    text-transform: uppercase;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

.logo-icon {{
    width: 24px;
    height: 24px;
    fill: var(--accent);
}}

.nav-links {{
    display: flex;
    gap: 2.5rem;
}}

.nav-links a {{
    color: var(--text);
    text-decoration: none;
    font-size: 0.95rem;
    font-weight: 500;
    transition: color 0.2s;
}}

.nav-links a:hover {{
    color: var(--accent);
}}

/* --- Buttons --- */
.btn {{
    padding: 0.875rem 2rem;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 0.95rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border: none;
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
    color: #ffffff;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
    padding: 1.25rem 2.5rem;
    font-size: 1.1rem;
}}

.btn-primary:hover {{
    transform: translateY(-2px) scale(1.02);
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.4);
    filter: brightness(1.1);
}}

/* --- Main Layout --- */
.hero-main {{
    flex-grow: 1;
    display: grid;
    grid-template-columns: 1.2fr 1fr;
    align-items: center;
    padding: 0 4rem;
    gap: 4rem;
}}

.text-content {{
    display: flex;
    flex-direction: column;
    z-index: 5;
}}

.title {{
    font-family: 'Oswald', sans-serif;
    font-size: clamp(3.5rem, 5vw, 5.5rem);
    font-weight: 700;
    line-height: 1.05;
    text-transform: uppercase;
    letter-spacing: -1px;
    margin-bottom: 1.5rem;
    text-wrap: balance;
}}

.subtitle {{
    font-size: 1.125rem;
    line-height: 1.7;
    color: var(--text-muted);
    margin-bottom: 3rem;
    max-width: 90%;
}}

.cta-group {{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 1.5rem;
}}

/* --- Social Proof --- */
.social-proof {{
    display: flex;
    align-items: center;
    gap: 1rem;
}}

.avatars {{
    display: flex;
}}

.avatars img {{
    width: 44px;
    height: 44px;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid var(--bg);
    margin-left: -14px;
}}

.avatars img:first-child {{
    margin-left: 0;
}}

.social-text {{
    font-size: 0.9rem;
    color: var(--text-muted);
}}

.social-text strong {{
    color: var(--text);
}}

/* --- Trust Bar --- */
.trust-bar {{
    padding: 2rem 4rem;
    display: flex;
    align-items: center;
    gap: 2rem;
    border-top: 1px solid var(--border);
    margin-top: auto;
}}

.trust-label {{
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1px;
}}

.trust-logos {{
    display: flex;
    gap: 2.5rem;
    align-items: center;
}}

.logo-fake {{
    font-family: 'Oswald', sans-serif;
    font-size: 1.25rem;
    font-weight: 700;
    filter: {logo_filter};
    transition: filter 0.3s;
    user-select: none;
}}

.logo-fake:hover {{
    filter: grayscale(0%) opacity(1) brightness(100%);
}}

/* --- Visual Element (Right Side) --- */
.visual-content {{
    position: relative;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    perspective: 1000px;
}}

.floating-graphic {{
    width: 400px;
    height: 400px;
    position: relative;
    transition: transform 0.1s ease-out;
}}

/* Abstract Ship/Tech Shape to simulate the tutorial's X-Wing */
.shape-polygon {{
    position: absolute;
    top: 20%;
    left: 10%;
    width: 80%;
    height: 60%;
    background: var(--accent);
    clip-path: polygon(0% 40%, 100% 0%, 80% 100%, 20% 60%);
    box-shadow: inset 0 0 40px rgba(0,0,0,0.5);
}}

.shape-orb {{
    position: absolute;
    top: 10%;
    right: 5%;
    width: 150px;
    height: 150px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--text) 0%, transparent 80%);
    opacity: 0.15;
    backdrop-filter: blur(10px);
}}

.shape-grid {{
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image: linear-gradient(var(--border) 1px, transparent 1px),
                      linear-gradient(90deg, var(--border) 1px, transparent 1px);
    background-size: 20px 20px;
    opacity: 0.2;
    transform: rotateX(60deg) rotateZ(-45deg);
}}

/* --- Responsiveness --- */
@media (max-width: 968px) {{
    .hero-main {{
        grid-template-columns: 1fr;
        text-align: center;
        padding: 2rem;
    }}
    
    .text-content {{
        align-items: center;
    }}
    
    .subtitle {{ max-width: 100%; }}
    
    .cta-group {{
        align-items: center;
    }}
    
    .visual-content {{ display: none; }}
    
    .nav-links {{ display: none; }}
    
    .trust-bar {{
        flex-direction: column;
        justify-content: center;
        padding: 2rem;
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text[:20]}...</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="hero-container">
        
        <!-- Header -->
        <header class="header">
            <div class="logo">
                <svg class="logo-icon" viewBox="0 0 24 24"><path d="M12 2L2 22h20L12 2zm0 6l5.5 11h-11L12 8z"/></svg>
                <span>Rebel Base</span>
            </div>
            <nav class="nav-links">
                <a href="#ships">Our Ships</a>
                <a href="#mission">Mission</a>
                <a href="#donations">Donations</a>
            </nav>
            <button class="btn btn-ghost">Log In</button>
        </header>

        <!-- Main Hero -->
        <main class="hero-main">
            <div class="text-content">
                <h1 class="title">{title_text}</h1>
                <p class="subtitle">{body_text}</p>
                
                <div class="cta-group">
                    <button class="btn btn-primary">Join Now For Free</button>
                    
                    <!-- Social Proof Cluster -->
                    <div class="social-proof">
                        <div class="avatars">
                            <img src="https://i.pravatar.cc/100?img=11" alt="Member 1">
                            <img src="https://i.pravatar.cc/100?img=33" alt="Member 2">
                            <img src="https://i.pravatar.cc/100?img=47" alt="Member 3">
                            <img src="https://i.pravatar.cc/100?img=12" alt="Member 4">
                        </div>
                        <div class="social-text">
                            <strong>Obi Wan</strong> and 4,000 others<br>have already joined.
                        </div>
                    </div>
                </div>
            </div>

            <!-- Dynamic Right Visual -->
            <div class="visual-content">
                <div class="floating-graphic">
                    <div class="shape-grid"></div>
                    <div class="shape-polygon"></div>
                    <div class="shape-orb"></div>
                </div>
            </div>
        </main>

        <!-- Trust Bar -->
        <footer class="trust-bar">
            <div class="trust-label">As Seen On:</div>
            <div class="trust-logos">
                <span class="logo-fake">NBC</span>
                <span class="logo-fake">FOX</span>
                <span class="logo-fake">THE CW</span>
                <span class="logo-fake">ABC</span>
            </div>
        </footer>

    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    js = """// High-Converting Split Hero - Parallax Interaction
document.addEventListener('DOMContentLoaded', () => {
    const heroMain = document.querySelector('.hero-main');
    const graphic = document.querySelector('.floating-graphic');

    // Subtle parallax effect on the graphic relative to mouse position
    heroMain.addEventListener('mousemove', (e) => {
        if (!graphic) return;
        
        const rect = heroMain.getBoundingClientRect();
        
        // Calculate mouse position relative to the center of the container (-1 to 1)
        const x = ((e.clientX - rect.left) / rect.width - 0.5) * 2;
        const y = ((e.clientY - rect.top) / rect.height - 0.5) * 2;

        // Apply slight translation and 3D rotation
        const moveX = x * 30; // max 30px movement
        const moveY = y * 30;
        const rotateY = x * 10; // max 10 degrees rotation
        const rotateX = -y * 10;

        graphic.style.transform = `translate(${moveX}px, ${moveY}px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
    });

    // Reset transform when mouse leaves
    heroMain.addEventListener('mouseleave', () => {
        if (graphic) {
            graphic.style.transform = `translate(0px, 0px) rotateX(0deg) rotateY(0deg)`;
        }
    });
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

* **Accessibility (a11y)**:
  * The `h1` uses CSS `text-wrap: balance` to automatically prevent awkward typographic orphans and widow words on different screen sizes without manual `<br>` tags.
  * Contrast ratios are strictly maintained. The muted text (`#8a8d98` on `#0a0b10`) passes WCAG AA criteria for normal text (exceeds 4.5:1).
  * The fake placeholder logos use text instead of empty images for screen reader safety. In production, real SVG logos should include `aria-label` tags.
* **Performance**:
  * No heavy external libraries (like GSAP or Three.js) were required.
  * The parallax mousemove event is relatively lightweight, calculating transforms natively. For production sites with massive traffic, the `mousemove` listener could be throttled via `requestAnimationFrame`.
  * The starfield/vignette effect relies entirely on a CSS `radial-gradient` painted directly on the `body`, requiring near-zero GPU compositing compared to an actual particle canvas.