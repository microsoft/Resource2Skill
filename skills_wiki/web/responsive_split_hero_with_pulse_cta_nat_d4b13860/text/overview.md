# Responsive Split Hero with Pulse CTA & Native Dialog Modal

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Responsive Split Hero with Pulse CTA & Native Dialog Modal

* **Core Visual Mechanism**: A modern, minimalist hero section featuring a 50/50 split layout (image alongside text) that stacks vertically on mobile devices. The focal point is a Call-To-Action (CTA) play button featuring a continuous, dual-ring "pulse" animation. Interacting with the CTA opens a native HTML5 `<dialog>` element serving as a video modal, complete with entry/exit fade animations and click-outside-to-close functionality.
* **Why Use This Skill (Rationale)**: The split layout provides an immediate, balanced presentation of identity (image) and value proposition (text). The continuous pulse animation acts as a strong visual cue, drawing the user's eye directly to the primary action without being overly aggressive. Using the native `<dialog>` element ensures proper stacking contexts, focus trapping, and accessibility out-of-the-box, replacing complex custom modal implementations.
* **Overall Applicability**: Ideal for personal portfolios, SaaS product introductions, agency landing pages, or any scenario where introductory text needs to be paired with a high-value video introduction or demo.
* **Browser Compatibility**: Excellent. The `<dialog>` element is now fully supported across all major modern browsers. CSS Grid and Flexbox are standard. The click-outside logic relies on `getBoundingClientRect`, which is universally supported.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  * **Typography**: Clean sans-serif ('Inter' or system UI). Large font sizes for headings (e.g., `3.3em`) with tight line-heights.
  * **Color Logic**: A high-contrast minimalist base (white/dark grey) accented by a single vibrant color (e.g., `#ff4444`). The accent color is used sparingly: for hover states, a decorative period at the end of the heading, the CTA button background, and its emitting pulse rings.
  * **Shapes**: Heavy use of perfect circles (`border-radius: 50%`) for the profile image and the play button to soften the overall rigid grid layout.

* **Step B: Layout & Compositional Style**
  * **Desktop**: CSS Grid is used to create a 2-column layout (`grid-template-columns: 1fr 1fr`) with vertical centering (`align-items: center`). Max-width containers keep content from spanning too wide on large screens.
  * **Mobile**: A media query (`@media (max-width: 880px)`) redefines the grid to a single column (`1fr`), centering the image above the text and adjusting font sizes. The navigation shifts to a hamburger menu.

* **Step C: Interactive Behavior & Animations**
  * **Pulse Animation**: Created using `::before` and `::after` pseudo-elements on the play button. They share a single `@keyframes` animation that scales them up and fades their opacity to 0, but they run with staggered delays to create a continuous ripple effect.
  * **Modal Lifecycle**: 
    * **Open**: Triggered by JS. Adds a `fadeIn` animation class, calls `modal.showModal()`, and starts video playback.
    * **Close**: Listens for clicks on the dialog. Compares click coordinates against the dialog's `getBoundingClientRect()`. If the click falls outside these bounds (meaning it hit the `::backdrop`), it applies a `fadeOut` animation. Crucially, it waits for the `animationend` event before actually calling `modal.close()` to ensure a smooth exit.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Responsive Hero Layout** | CSS Grid | Cleanest way to manage the 2-column to 1-column shift without complex wrapper divs. |
| **Pulse Animation** | CSS `@keyframes` + Pseudo-elements | Highly performant, requires no JS, keeps markup clean (only one button element needed). |
| **Video Modal** | Native HTML `<dialog>` | Provides top-layer z-indexing, backdrop styling, and focus management natively. |
| **Click-Outside Close** | JS Bounding Box Check | The standard, most reliable way to detect clicks on a native dialog's backdrop. |
| **Icons** | Font Awesome CDN | Quick, scalable vector icons for the play button and mobile menu. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "The Portfolio of Emily Grace",
    body_text: str = "I'm Emily Grace, a passionate logo designer dedicated to crafting visual symbols that tell stories, capture hearts, and make lasting impressions.",
    color_scheme: str = "light",
    accent_color: str = "#ff4444",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme colors
    if color_scheme == "dark":
        bg_color = "#121212"
        text_color = "#ffffff"
        text_muted = "#a0a0a0"
        nav_hover = "#ffffff"
    else:
        bg_color = "#ffffff"
        text_color = "#000000"
        text_muted = "#5d5d5d"
        nav_hover = "#000000"
        
    # Generate a slightly lighter version of the accent color for the pulse effect
    pulse_color = accent_color + "99" # Adding hex transparency

    css = f"""/* Base Reset */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-primary: {text_color};
    --text-secondary: {text_muted};
    --accent: {accent_color};
    --pulse-color: {pulse_color};
    --nav-hover: {nav_hover};
    font-family: 'Inter', system-ui, sans-serif;
}}

body {{
    background-color: var(--bg-color);
    color: var(--text-primary);
    line-height: 1.6;
    overflow-x: hidden;
}}

.container {{
    max-width: 1100px;
    margin: 0 auto;
    padding: 0 2em;
}}

/* Navbar */
header {{
    padding-top: 2em;
}}

.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    z-index: 10;
}}

.navbar .brand {{
    font-size: 1.3em;
    font-weight: 700;
    text-decoration: none;
    color: var(--text-primary);
}}

.navbar .menu {{
    display: flex;
    gap: 2em;
}}

.navbar a {{
    text-decoration: none;
    color: var(--text-primary);
    transition: color 0.3s ease;
    font-weight: 500;
}}

.navbar a:hover {{
    color: var(--accent);
}}

.nav-btn {{
    display: none;
    background: none;
    border: none;
    font-size: 1.5em;
    cursor: pointer;
    color: var(--text-primary);
}}

/* Hero Section */
.hero {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    align-items: center;
    min-height: calc(100vh - 100px);
    gap: 4em;
}}

.profile-img {{
    width: 100%;
    max-width: 450px;
    aspect-ratio: 1/1;
    border-radius: 50%;
    object-fit: cover;
    background-color: #fcebeb; /* Fallback placeholder color matching tutorial theme */
    justify-self: center;
}}

.hero-details h1 {{
    font-size: clamp(2.5rem, 5vw, 3.5rem);
    font-weight: 700;
    line-height: 1.1;
    margin-bottom: 0.5em;
}}

.hero-details h1 span {{
    color: var(--accent);
}}

.hero-details p {{
    color: var(--text-secondary);
    font-size: 1.1rem;
    margin-bottom: 2em;
    max-width: 90%;
}}

/* Video CTA & Pulse Button */
.video-cta {{
    display: flex;
    align-items: center;
    gap: 1.5em;
}}

.video-btn {{
    position: relative;
    width: 60px;
    height: 60px;
    background-color: var(--accent);
    border: none;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    color: #fff;
    font-size: 1.2rem;
    cursor: pointer;
    z-index: 1;
    padding-left: 4px; /* visually center play icon */
}}

.video-btn::before,
.video-btn::after {{
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 100%;
    height: 100%;
    background-color: var(--pulse-color);
    border-radius: 50%;
    z-index: -1;
    animation: pulse 2s ease-out infinite;
}}

.video-btn::after {{
    animation-delay: 1s;
}}

@keyframes pulse {{
    0% {{ transform: translate(-50%, -50%) scale(1); opacity: 0.8; }}
    100% {{ transform: translate(-50%, -50%) scale(1.8); opacity: 0; }}
}}

.video-cta span {{
    font-weight: 600;
    font-size: 1.1rem;
}}

/* Native Dialog Modal */
.modal {{
    margin: auto;
    width: 90%;
    max-width: 900px;
    border: none;
    border-radius: 12px;
    background: transparent;
    overflow: hidden;
    box-shadow: 0 20px 40px rgba(0,0,0,0.3);
}}

.modal::backdrop {{
    background: rgba(0, 0, 0, 0.85);
    backdrop-filter: blur(4px);
}}

.modal video {{
    width: 100%;
    display: block;
    border-radius: 12px;
}}

/* Modal Animations */
.modal[open] {{
    animation: fadeIn 0.4s ease-out forwards;
}}

.modal.closing {{
    animation: fadeOut 0.4s ease-out forwards;
}}

@keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(20px); scale: 0.95; }}
    to {{ opacity: 1; transform: translateY(0); scale: 1; }}
}}

@keyframes fadeOut {{
    from {{ opacity: 1; transform: translateY(0); scale: 1; }}
    to {{ opacity: 0; transform: translateY(20px); scale: 0.95; }}
}}

/* Responsive Design */
@media (max-width: 880px) {{
    .hero {{
        grid-template-columns: 1fr;
        text-align: center;
        padding-top: 3em;
        gap: 2em;
    }}
    
    .hero-details p {{
        margin: 0 auto 2em auto;
    }}

    .video-cta {{
        justify-content: center;
    }}

    .nav-btn {{
        display: block;
    }}

    .navbar .menu {{
        display: none;
        position: absolute;
        top: 100%;
        left: 0;
        width: 100%;
        background: var(--bg-color);
        flex-direction: column;
        padding: 2em;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }}

    .navbar .menu.active {{
        display: flex;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    
    <header>
        <div class="container navbar">
            <a href="#" class="brand">Emily Grace</a>
            <div class="menu">
                <a href="#">About</a>
                <a href="#">Portfolio</a>
                <a href="#">Contact</a>
            </div>
            <button class="nav-btn"><i class="fas fa-bars"></i></button>
        </div>
    </header>

    <main class="container hero">
        <!-- Using a placeholder image with the appropriate aspect ratio -->
        <img src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&q=80&w=800" alt="Profile" class="profile-img">
        
        <div class="hero-details">
            <h1>The Portfolio of<br>{title_text.split()[-2]} {title_text.split()[-1]}<span>.</span></h1>
            <p>{body_text}</p>
            
            <div class="video-cta">
                <button class="video-btn" aria-label="Play video"><i class="fas fa-play"></i></button>
                <span>Watch Video</span>
            </div>
        </div>
    </main>

    <!-- Native HTML Dialog -->
    <dialog class="modal">
        <!-- Using a placeholder open-source video -->
        <video controls>
            <source src="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/TearsOfSteel.mp4" type="video/mp4">
            Your browser does not support the video tag.
        </video>
    </dialog>

    <script src="script.js"></script>
</body>
</html>"""

    js = f"""document.addEventListener('DOMContentLoaded', () => {{
    
    // --- Mobile Menu Toggle ---
    const navBtn = document.querySelector('.nav-btn');
    const menu = document.querySelector('.menu');

    navBtn.addEventListener('click', () => {{
        menu.classList.toggle('active');
        const icon = navBtn.querySelector('i');
        if(menu.classList.contains('active')) {{
            icon.classList.remove('fa-bars');
            icon.classList.add('fa-times');
        }} else {{
            icon.classList.remove('fa-times');
            icon.classList.add('fa-bars');
        }}
    }});

    // --- Modal Logic ---
    const openBtn = document.querySelector('.video-btn');
    const modal = document.querySelector('.modal');
    const video = document.querySelector('.modal video');

    // Open Modal
    openBtn.addEventListener('click', () => {{
        modal.showModal();
        video.play().catch(e => console.log("Autoplay prevented:", e));
    }});

    // Close Modal when clicking on backdrop
    modal.addEventListener('click', (e) => {{
        // Get bounds of the dialog
        const dialogDimensions = modal.getBoundingClientRect();
        
        // Check if click was outside the dialog bounds
        if (
            e.clientX < dialogDimensions.left ||
            e.clientX > dialogDimensions.right ||
            e.clientY < dialogDimensions.top ||
            e.clientY > dialogDimensions.bottom
        ) {{
            closeModal();
        }}
    }});

    // Function to handle close with animation
    function closeModal() {{
        modal.classList.add('closing');
        video.pause();
        
        // Wait for animation to finish before actually closing
        modal.addEventListener('animationend', function handler() {{
            modal.classList.remove('closing');
            modal.close();
            modal.removeEventListener('animationend', handler);
        }});
    }}
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

* **Accessibility (`<dialog>`)**: Utilizing the native `<dialog>` element guarantees excellent accessibility without extra effort. It automatically traps focus inside the modal when open, correctly hides background content from screen readers (`aria-hidden="true"` behavior), and responds to the `Escape` key to close natively.
* **Animation Performance**: The pulse animation uses `transform: scale()` instead of animating `width` and `height` as seen in some older tutorials. This is crucial because `transform` triggers hardware acceleration (GPU) and avoids expensive browser layout recalculations (reflows) on every frame of the infinite animation, saving battery and ensuring a smooth 60fps effect.
* **Semantic Button**: The play button includes an `aria-label="Play video"` to ensure screen reader users understand the icon-only button's purpose.