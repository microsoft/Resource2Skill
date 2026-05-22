### 1. High-level Design Pattern Extraction

> **Skill Name**: High-Converting Authority Hero Section

* **Core Visual Mechanism**: A cinematic, two-column hero layout that blends atmospheric background lighting with a softly masked featured image. It relies heavily on layered social proof (user avatars and media logos) and a high-contrast Call-To-Action (CTA) to drive immediate conversions. 
* **Why Use This Skill (Rationale)**: This layout is structurally engineered for conversion psychology. It moves the user logically through a sequence: Value Proposition (Headline) → Elaboration (Subheadline) → Frictionless Action ("Join for free") → Peer Validation (4,000 others) → Institutional Authority (Media Logos). Visually, the soft radial masking of the hero image integrates it seamlessly into the background, avoiding the "boxed" feel of traditional stock photos and making the page feel like a premium, custom-designed experience.
* **Overall Applicability**: SaaS landing pages, community recruitment pages, course sales pages, and any hero section where building immediate trust and driving a single primary action is the goal.
* **Value Addition**: Transforms a standard text-and-image header into a high-trust conversion engine. The atmospheric glow and parallax hover effects add a layer of modern polish that signals quality to the user.
* **Browser Compatibility**: Fully supported in modern browsers. Uses `backdrop-filter` for the navigation bar, `mask-image` for the edge-faded hero image, and CSS Grid for layout. (Note: `-webkit-mask-image` is included for full WebKit/Blink support).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**: Utilizes a deep background (e.g., `#0B0E14` for dark mode) offset by a vibrant, blurred atmospheric light source generated via CSS `filter: blur(150px)` tied to the `accent_color`. Text uses high-contrast primary text (`#FFFFFF`) and mid-contrast muted text (`rgba(255, 255, 255, 0.65)`).
  - **Typographic Hierarchy**: Driven by the `Inter` font. The headline is massive (`3.5rem`), bold (`800`), and tightly tracked (`letter-spacing: -0.02em`) to command attention. The subheadline provides comfortable reading (`1.125rem`, `line-height: 1.6`).
  - **Visual Anchors**: The primary CTA button is a solid block of the accent color, while overlapping circular avatars create a recognizable "community" cluster pattern.

* **Step B: Layout & Compositional Style**
  - **Layout System**: The main container uses CSS Grid (`grid-template-columns: 1.2fr 1fr`) to distribute visual weight. The text column is slightly wider to accommodate longer headlines without awkward wrapping.
  - **Z-Index Layering**: 
    1. Base background color
    2. Atmospheric blurred glow (`z-index: 0`)
    3. Grid content and floating image (`z-index: 1`)
    4. Sticky glassmorphism navigation bar (`z-index: 100`)

* **Step C: Interactive Behavior & Animations**
  - **Entrance**: The text elements cascade into view using a `slideUpFade` keyframe animation with staggered delays (`0.1s`, `0.2s`, etc.), guiding the eye down the page.
  - **Continuous Motion**: The hero image features a subtle, continuous CSS `@keyframes` float animation (moving `15px` up and down over 6 seconds) to make the space feel alive.
  - **Cursor Interaction**: JavaScript tracks mouse movement to apply a slight parallax translation to the hero image wrapper, creating 3D depth relative to the mouse position.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Layout & Spacing** | CSS Grid & Flexbox | Cleanest way to handle the two-column split and internal stacking of the text column without manual math. |
| **Atmospheric Glow** | CSS `filter: blur()` | A massive blur on an absolutely positioned div creates a dynamic, resolution-independent lighting effect that matches the accent color. |
| **Image Blending** | CSS `mask-image: radial-gradient()` | Fades the edges of the hero image into transparency, replicating the Photoshop composition technique shown in the tutorial natively in the browser. |
| **Parallax Interaction** | Vanilla JavaScript | A simple `mousemove` event listener calculates offsets to push the image opposite the cursor, adding premium interactivity. |
| **Logos & Avatars** | Inline SVGs & Pravatar API | Ensures the social proof sections render immediately and look authentic without requiring local static assets. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "It's your universe, it's time to save it",
    body_text: str = "The Rebel alliance is fighting to get rid of the evil empire. Join the resistance to create a better future for your children.",
    color_scheme: str = "dark",
    accent_color: str = "#E63946",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the High-Converting Authority Hero Section.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0B0E14"
        text_main = "#FFFFFF"
        text_muted = "rgba(255, 255, 255, 0.65)"
        nav_bg = "rgba(11, 14, 20, 0.75)"
        border_color = "rgba(255, 255, 255, 0.15)"
        # Dark text on light accent colors for button legibility
        btn_text = "#0B0E14" if accent_color.lower() in ["#00bfff", "#fff", "white", "#0ff", "cyan", "yellow", "#00ffff"] else "#FFFFFF"
        hero_img_url = "https://images.unsplash.com/photo-1614730321146-b6fa6a46bcb4?auto=format&fit=crop&w=800&q=80"
    else:
        bg_color = "#FFFFFF"
        text_main = "#111827"
        text_muted = "#4B5563"
        nav_bg = "rgba(255, 255, 255, 0.85)"
        border_color = "rgba(0, 0, 0, 0.1)"
        btn_text = "#FFFFFF" if accent_color.lower() not in ["#fff", "white", "#ffff00", "yellow"] else "#111827"
        hero_img_url = "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=800&q=80"

    # === CSS ===
    css = f"""/* High-Converting Authority Hero Section */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;800&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text-main: {text_main};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --btn-text: {btn_text};
    --nav-bg: {nav_bg};
    --border-color: {border_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #050505; /* Outer canvas background */
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-main);
}}

.viewport-container {{
    width: var(--width);
    height: var(--height);
    background-color: var(--bg);
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    box-shadow: 0 24px 80px rgba(0, 0, 0, 0.4);
}}

/* Atmospheric Light Glow */
.viewport-container::before {{
    content: '';
    position: absolute;
    top: 50%;
    right: 5%;
    width: 500px;
    height: 500px;
    background: var(--accent);
    filter: blur(160px);
    opacity: 0.15;
    transform: translateY(-50%);
    pointer-events: none;
    z-index: 0;
}}

/* Navbar */
.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 24px 48px;
    background: var(--nav-bg);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--border-color);
    position: relative;
    z-index: 100;
}}

.logo {{
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: 800;
    font-size: 1.25rem;
    letter-spacing: -0.02em;
}}

.nav-links {{
    display: flex;
    gap: 32px;
    list-style: none;
}}

.nav-links a {{
    text-decoration: none;
    color: var(--text-main);
    font-weight: 500;
    font-size: 0.95rem;
    transition: color 0.2s;
}}

.nav-links a:hover {{
    color: var(--accent);
}}

.btn-outline {{
    border: 2px solid var(--border-color);
    padding: 10px 24px;
    border-radius: 6px;
    text-decoration: none;
    color: var(--text-main);
    font-weight: 600;
    font-size: 0.9rem;
    transition: all 0.2s ease;
}}

.btn-outline:hover {{
    border-color: var(--text-main);
}}

/* Hero Layout */
.hero-section {{
    flex: 1;
    display: grid;
    grid-template-columns: 1.2fr 1fr;
    gap: 40px;
    padding: 0 64px;
    align-items: center;
    position: relative;
    z-index: 1;
}}

/* Text Content Column */
.text-column {{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}}

.headline {{
    font-size: clamp(2.5rem, 4vw, 4rem);
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -0.03em;
    margin-bottom: 24px;
}}

.subheadline {{
    font-size: clamp(1rem, 1.5vw, 1.125rem);
    line-height: 1.6;
    color: var(--text-muted);
    max-width: 90%;
    margin-bottom: 32px;
}}

/* CTA Area */
.cta-group {{
    margin-bottom: 24px;
}}

.btn-primary {{
    background-color: var(--accent);
    color: var(--btn-text);
    padding: 18px 36px;
    border-radius: 6px;
    text-decoration: none;
    font-weight: 700;
    font-size: 1rem;
    letter-spacing: 0.02em;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    box-shadow: 0 4px 14px color-mix(in srgb, var(--accent) 40%, transparent);
}}

.btn-primary:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 24px color-mix(in srgb, var(--accent) 60%, transparent);
}}

/* Social Proof - Users */
.social-proof-users {{
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 48px;
}}

.avatars {{
    display: flex;
}}

.avatars img {{
    width: 36px;
    height: 36px;
    border-radius: 50%;
    border: 3px solid var(--bg);
    margin-left: -12px;
    object-fit: cover;
}}

.avatars img:first-child {{
    margin-left: 0;
}}

.proof-text {{
    font-size: 0.875rem;
    color: var(--text-muted);
    line-height: 1.4;
}}

.proof-text strong {{
    color: var(--text-main);
    font-weight: 600;
}}

/* Social Proof - Media */
.social-proof-media {{
    width: 100%;
    border-top: 1px solid var(--border-color);
    padding-top: 24px;
}}

.media-label {{
    display: block;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-muted);
    margin-bottom: 16px;
    font-weight: 600;
}}

.logos-row {{
    display: flex;
    gap: 32px;
    align-items: center;
    opacity: 0.5;
    filter: grayscale(100%);
    transition: opacity 0.3s;
}}

.logos-row:hover {{
    opacity: 0.9;
}}

.logos-row svg {{
    height: 24px;
    width: auto;
    fill: var(--text-main);
}}

/* Image Column */
.image-column {{
    width: 100%;
    height: 600px;
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
}}

.hero-image-parallax {{
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    transition: transform 0.1s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}}

.hero-image {{
    max-width: 110%;
    max-height: 110%;
    object-fit: contain;
    /* Softly blends the edges of the image into the background */
    mask-image: radial-gradient(circle at center, black 40%, transparent 80%);
    -webkit-mask-image: radial-gradient(circle at center, black 40%, transparent 80%);
    animation: float 6s ease-in-out infinite;
}}

/* Animations */
@keyframes float {{
    0%, 100% {{ transform: translateY(0); }}
    50% {{ transform: translateY(-16px); }}
}}

@keyframes slideUpFade {{
    from {{ opacity: 0; transform: translateY(20px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

.text-column > * {{
    opacity: 0;
    animation: slideUpFade 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}}

.text-column > *:nth-child(1) {{ animation-delay: 0.1s; }}
.text-column > *:nth-child(2) {{ animation-delay: 0.2s; }}
.text-column > *:nth-child(3) {{ animation-delay: 0.3s; }}
.text-column > *:nth-child(4) {{ animation-delay: 0.4s; }}
.text-column > *:nth-child(5) {{ animation-delay: 0.5s; }}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>High-Converting Hero</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="viewport-container">
        
        <!-- Navigation -->
        <header class="navbar">
            <div class="logo">
                <svg viewBox="0 0 24 24" width="28" height="28" fill="var(--accent)">
                    <path d="M12 2L1 21h22L12 2zm0 3.99L19.53 19H4.47L12 5.99z"/>
                </svg>
                Alliance
            </div>
            <ul class="nav-links">
                <li><a href="#">Initiatives</a></li>
                <li><a href="#">Manifesto</a></li>
                <li><a href="#">Support</a></li>
            </ul>
            <a href="#" class="btn-outline">Sign In</a>
        </header>

        <!-- Main Hero Area -->
        <main class="hero-section">
            
            <!-- Content -->
            <div class="text-column">
                <h1 class="headline">{title_text}</h1>
                <p class="subheadline">{body_text}</p>
                
                <div class="cta-group">
                    <a href="#" class="btn-primary">JOIN NOW FOR FREE</a>
                </div>

                <div class="social-proof-users">
                    <div class="avatars">
                        <img src="https://i.pravatar.cc/100?img=11" alt="User 1">
                        <img src="https://i.pravatar.cc/100?img=32" alt="User 2">
                        <img src="https://i.pravatar.cc/100?img=68" alt="User 3">
                        <img src="https://i.pravatar.cc/100?img=47" alt="User 4">
                    </div>
                    <div class="proof-text">
                        <strong>Obi Wan</strong> and 4,000 others have already joined
                    </div>
                </div>

                <div class="social-proof-media">
                    <span class="media-label">As seen on</span>
                    <div class="logos-row">
                        <!-- NBC-style text logo -->
                        <svg viewBox="0 0 80 30" width="60" height="24" fill="currentColor">
                            <text x="0" y="24" font-family="Arial, sans-serif" font-weight="900" font-size="28" letter-spacing="-2">NBC</text>
                        </svg>
                        <!-- FOX-style text logo -->
                        <svg viewBox="0 0 70 30" width="50" height="24" fill="currentColor">
                            <text x="0" y="24" font-family="Arial, sans-serif" font-weight="900" font-size="28" letter-spacing="1">FOX</text>
                        </svg>
                        <!-- CW-style text logo -->
                        <svg viewBox="0 0 100 30" width="75" height="24" fill="currentColor">
                            <text x="0" y="24" font-family="Arial, sans-serif" font-weight="bold" font-size="26">The CW</text>
                        </svg>
                    </div>
                </div>
            </div>

            <!-- Visuals -->
            <div class="image-column">
                <div class="hero-image-parallax">
                    <img src="{hero_img_url}" class="hero-image" alt="Cinematic Hero Visual">
                </div>
            </div>

        </main>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// High-Converting Authority Hero Section - Interactive Behavior

document.addEventListener('DOMContentLoaded', () => {{
    const container = document.querySelector('.viewport-container');
    const parallaxTarget = document.querySelector('.hero-image-parallax');

    // Subtle parallax effect on mouse movement to create depth
    container.addEventListener('mousemove', (e) => {{
        // Calculate offset based on cursor position relative to container center
        const rect = container.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        
        // Division factor limits how far the image moves (higher = less movement)
        const xAxis = (centerX - e.clientX) / 35;
        const yAxis = (centerY - e.clientY) / 35;
        
        // Apply transform
        parallaxTarget.style.transform = `translate(${{xAxis}}px, ${{yAxis}}px)`;
    }});

    // Reset smoothly when mouse leaves the container
    container.addEventListener('mouseleave', () => {{
        parallaxTarget.style.transform = `translate(0px, 0px)`;
    }});
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