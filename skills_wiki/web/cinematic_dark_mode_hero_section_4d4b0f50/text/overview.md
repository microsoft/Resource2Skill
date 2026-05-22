### 1. High-level Design Pattern Extraction

> **Skill Name**: Cinematic Dark Mode Hero Section

* **Core Visual Mechanism**: A dramatic, full-viewport header designed to command attention. It leverages a dark, atmospheric background (often space or a dark gradient) paired with a high-contrast, heavily weighted sans-serif typographic hierarchy. A striking, transparent cutout subject image dominates the right side, creating a sense of depth and breaking the grid. The layout drives the user's eye in an F-pattern: Logo -> Nav -> Giant Headline -> Social Proof -> Primary CTA -> Foreground Visual.
* **Why Use This Skill (Rationale)**: This design maximizes emotional impact and credibility. The dark mode feels premium and cinematic. The large typography immediately communicates the value proposition, while the prominent "social proof" (avatars showing other users) and "authority logos" (As Seen On) at the bottom significantly lower the barrier to trust, encouraging conversions.
* **Overall Applicability**: Ideal for SaaS landing pages, gaming websites, movie/event promotions, and disruptive tech startups wanting a bold, rebellious, or epic brand positioning. 
* **Value Addition**: Transforms a standard informational header into a high-converting landing experience by systematically addressing user psychology: hook (headline), emotion (imagery), trust (avatars/logos), and action (high-contrast button).
* **Browser Compatibility**: Fully compatible with modern browsers using standard CSS Flexbox/Grid, CSS variables, and basic keyframe animations. No experimental APIs are required.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**: Dark atmospheric background `#0d111c` (or an image overlay). High contrast pure white text `#ffffff`. A highly aggressive accent color (e.g., Rebel Red `#e62b29`) for primary actions. Secondary text uses semi-transparent white `rgba(255, 255, 255, 0.6)`.
  - **Typographic Hierarchy**: Uses 'Inter' (or similar geometric sans-serif). Headlines are massive, tightly tracked (`letter-spacing: -1px`), and extra bold (`font-weight: 900`). Body copy is highly legible at `400` or `500` weight.
  - **Stylistic Signatures**:
    - "Ghost" buttons for secondary actions (transparent background, colored border).
    - Solid, heavy buttons for primary actions.
    - Overlapping circular avatars with border-strokes matching the background to create separation.

* **Step B: Layout & Compositional Style**
  - **Architecture**: A 3-tier vertical flex layout encompassing the `navbar`, the `main-content`, and the `footer-bar`.
  - **Main Content**: Split 50/50 using CSS Grid or Flexbox. The left column is text-heavy and left-aligned. The right column is a visual container where the foreground image is allowed to scale up and potentially overlap the top/bottom boundaries to create a 3D "pop-out" effect.
  - **Whitespace**: Generous padding on the horizontal edges (typically `4vw` to `8vw` depending on screen size) to frame the content elegantly.

* **Step C: Interactive Behavior & Animations**
  - **Hover Effects**: Buttons scale up slightly (`transform: translateY(-2px)`) with subtle box-shadows. 
  - **Atmospheric Motion**: The foreground image is given a very slow, continuous CSS `@keyframes` floating animation to make the scene feel alive without distracting from the copy.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Overall Layout** | CSS Flexbox & Grid | Provides robust, responsive structure for the 3-tier layout and the 50/50 content split without relying on JS. |
| **Dark Atmospheric Look** | CSS Background Blend Modes | Using a dark color over an image with `background-blend-mode: multiply` or a pseudo-element overlay easily achieves the cinematic backdrop. |
| **Foreground Pop-out** | CSS Absolute Positioning & Transform | Allows the main subject image to break out of the standard document flow, scale up, and float dynamically. |
| **Ambient Animation** | CSS `@keyframes` | A subtle floating effect on the main image adds life, hardware-accelerated by the browser. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "It's your universe,<br>it's time to save it",
    body_text: str = "The Rebel alliance is fighting to get rid of the evil empire. Join the resistance to create a better future for your children.",
    color_scheme: str = "dark",
    accent_color: str = "#e62b29",
    width_px: int = 1280,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Cinematic Dark Mode Hero Section.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Base theme colors
    bg_color = "#05070a" # Deep space black/blue
    text_color = "#ffffff"
    muted_text = "rgba(255, 255, 255, 0.65)"
    border_color = "rgba(255, 255, 255, 0.15)"

    # CSS
    css = f"""/* Cinematic Hero Section */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;900&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {muted_text};
    --accent: {accent_color};
    --border: {border_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: #000;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

/* Preview Wrapper restricts size to requested dimensions */
.hero-wrapper {{
    width: var(--width);
    height: var(--height);
    background-color: var(--bg);
    /* Simulated starfield background */
    background-image: 
        radial-gradient(circle at 15% 50%, rgba(255, 255, 255, 0.08) 0%, transparent 50%),
        radial-gradient(circle at 85% 30%, rgba(230, 43, 41, 0.05) 0%, transparent 50%);
    color: var(--text);
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    box-shadow: 0 24px 48px rgba(0,0,0,0.5);
}}

/* --- Navigation --- */
.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 24px 48px;
    z-index: 10;
}}

.logo {{
    display: flex;
    align-items: center;
    gap: 12px;
    font-weight: 700;
    font-size: 1.25rem;
    letter-spacing: -0.5px;
}}

.nav-links {{
    display: flex;
    gap: 32px;
    list-style: none;
}}

.nav-links a {{
    color: var(--text-muted);
    text-decoration: none;
    font-weight: 500;
    font-size: 0.9rem;
    transition: color 0.2s ease;
}}

.nav-links a:hover {{
    color: var(--text);
}}

.btn-ghost {{
    border: 2px solid var(--accent);
    background: transparent;
    color: var(--text);
    padding: 10px 24px;
    font-weight: 700;
    text-transform: uppercase;
    font-size: 0.85rem;
    cursor: pointer;
    transition: all 0.2s ease;
}}

.btn-ghost:hover {{
    background: var(--accent);
}}

/* --- Main Content --- */
.hero-main {{
    flex: 1;
    display: grid;
    grid-template-columns: 1fr 1fr;
    padding: 0 48px;
    align-items: center;
    z-index: 5;
}}

.hero-text {{
    display: flex;
    flex-direction: column;
    gap: 24px;
    max-width: 540px;
}}

.headline {{
    font-size: clamp(3rem, 4vw, 4.5rem);
    font-weight: 900;
    line-height: 1.05;
    letter-spacing: -1.5px;
}}

.sub-headline {{
    font-size: 1.1rem;
    color: var(--text-muted);
    line-height: 1.6;
}}

.btn-primary {{
    align-self: flex-start;
    background: var(--accent);
    color: #fff;
    border: none;
    padding: 18px 36px;
    font-weight: 900;
    font-size: 1rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    cursor: pointer;
    box-shadow: 0 4px 14px rgba(230, 43, 41, 0.4);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    margin-top: 8px;
}}

.btn-primary:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(230, 43, 41, 0.6);
}}

/* Social Proof */
.social-proof {{
    display: flex;
    align-items: center;
    gap: 16px;
    margin-top: 16px;
}}

.avatars {{
    display: flex;
}}

.avatar {{
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: 2px solid var(--bg);
    background-color: #333;
    background-size: cover;
    background-position: center;
    margin-left: -12px;
}}

.avatar:first-child {{
    margin-left: 0;
}}

.social-text {{
    font-size: 0.85rem;
    color: var(--text-muted);
    font-weight: 500;
}}

/* --- Visual Foreground --- */
.hero-visual {{
    position: relative;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}}

/* Placeholder for a dramatic cut-out image */
.visual-subject {{
    width: 120%;
    max-width: 800px;
    position: absolute;
    right: -10%;
    filter: drop-shadow(-20px 20px 30px rgba(0,0,0,0.8));
    animation: float 6s ease-in-out infinite;
}}

@keyframes float {{
    0%, 100% {{ transform: translateY(0) rotate(-2deg); }}
    50% {{ transform: translateY(-20px) rotate(1deg); }}
}}

/* --- Footer Logos --- */
.hero-footer {{
    display: flex;
    align-items: center;
    gap: 24px;
    padding: 24px 48px;
    border-top: 1px solid var(--border);
    z-index: 10;
}}

.as-seen {{
    font-size: 0.8rem;
    text-transform: uppercase;
    font-weight: 700;
    color: var(--text-muted);
    letter-spacing: 1px;
}}

.brand-logos {{
    display: flex;
    gap: 32px;
}}

.brand-logo {{
    height: 24px;
    opacity: 0.4;
    filter: grayscale(100%) brightness(200%);
    transition: opacity 0.3s ease;
}}

.brand-logo:hover {{
    opacity: 0.8;
}}
"""

    # HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cinematic Hero Section</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="hero-wrapper">
        
        <!-- Navbar -->
        <nav class="navbar">
            <div class="logo">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="var(--accent)">
                    <path d="M12 2L1 21h22L12 2zm0 3.99L19.53 19H4.47L12 5.99z"/>
                </svg>
                REBEL ALLIANCE
            </div>
            <ul class="nav-links">
                <li><a href="#">Our Ships</a></li>
                <li><a href="#">Mission</a></li>
                <li><a href="#">Donations</a></li>
            </ul>
            <button class="btn-ghost">Join Now</button>
        </nav>

        <!-- Main Content -->
        <main class="hero-main">
            <div class="hero-text">
                <h1 class="headline">{title_text}</h1>
                <p class="sub-headline">{body_text}</p>
                <button class="btn-primary">Join Now For Free</button>
                
                <div class="social-proof">
                    <div class="avatars">
                        <div class="avatar" style="background-image: url('https://i.pravatar.cc/100?img=11')"></div>
                        <div class="avatar" style="background-image: url('https://i.pravatar.cc/100?img=32')"></div>
                        <div class="avatar" style="background-image: url('https://i.pravatar.cc/100?img=33')"></div>
                        <div class="avatar" style="background-image: url('https://i.pravatar.cc/100?img=68')"></div>
                    </div>
                    <span class="social-text">Obi Wan and 4,000 others have already joined</span>
                </div>
            </div>

            <div class="hero-visual">
                <!-- Using a high-quality transparent PNG placeholder from an open API to simulate the cutout effect -->
                <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/150.png" alt="Hero Subject" class="visual-subject" style="filter: grayscale(100%) contrast(150%) brightness(80%) drop-shadow(-20px 20px 30px rgba(0,0,0,0.8));">
            </div>
        </main>

        <!-- Footer / Authority Logos -->
        <footer class="hero-footer">
            <span class="as-seen">As Seen On:</span>
            <div class="brand-logos">
                <!-- Placeholder SVG logos -->
                <svg class="brand-logo" viewBox="0 0 100 30" fill="currentColor"><text x="0" y="20" font-weight="900" font-size="24">FORBES</text></svg>
                <svg class="brand-logo" viewBox="0 0 100 30" fill="currentColor"><text x="0" y="20" font-weight="900" font-size="24">WIRED</text></svg>
                <svg class="brand-logo" viewBox="0 0 100 30" fill="currentColor"><text x="0" y="20" font-weight="900" font-size="24">CNBC</text></svg>
            </div>
        </footer>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # JavaScript
    js = """// Cinematic Hero Section
document.addEventListener('DOMContentLoaded', () => {
    // Optional: Add simple parallax effect to the hero visual on mousemove
    const visual = document.querySelector('.visual-subject');
    const wrapper = document.querySelector('.hero-wrapper');

    wrapper.addEventListener('mousemove', (e) => {
        const x = (window.innerWidth - e.pageX * 2) / 90;
        const y = (window.innerHeight - e.pageY * 2) / 90;
        
        // Combine mouse parallax with the CSS floating animation
        visual.style.transform = `translateX(${x}px) translateY(${y}px) rotate(-2deg)`;
    });

    wrapper.addEventListener('mouseleave', () => {
        visual.style.transform = `translateX(0) translateY(0) rotate(-2deg)`;
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
  - Contrast ratios for the primary text (`#ffffff` on `#05070a`) easily pass WCAG AAA standards. Muted text (`rgba(255,255,255,0.65)`) also maintains a strong enough ratio against pure black backgrounds.
  - Action buttons (`<button>`) are semantic. Anchor tags (`<a>`) are used for navigation. 
  - To improve screen reader experience, the decorative floating image should have an empty `alt=""` attribute if it is purely aesthetic, though an alt tag is provided in the code assuming it is contextual (e.g., "X-Wing Fighter").
* **Performance**:
  - The floating animation utilizes `transform: translateY()`, which is isolated to the GPU and does not trigger document repaints, ensuring a smooth 60fps framerate.
  - If deploying to production, the transparent PNG cutout should be compressed (e.g., WebP format) as large alpha-channel images can carry significant file size weight.