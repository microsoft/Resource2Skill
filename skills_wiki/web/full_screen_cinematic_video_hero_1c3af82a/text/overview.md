# Full-Screen Cinematic Video Hero

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Full-Screen Cinematic Video Hero

* **Core Visual Mechanism**: A continuous, muted video plays in the background behind the primary content. To ensure the foreground text remains legible regardless of the video's color variation, a semi-transparent dark overlay is applied between the video and the content. The layout relies on CSS absolute positioning to stretch the video and overlay, while Flexbox is used to perfectly center the main call-to-action in the foreground.

* **Why Use This Skill (Rationale)**: Background video immediately grabs attention and conveys complex emotional or contextual information much faster than static images or text. The overlay ensures that this dynamism doesn't compromise accessibility and text readability. It creates an immersive, "premium" feel that engages users the moment they land on the page.

* **Overall Applicability**: Ideal for the hero section (topmost section) of landing pages, SaaS product showcases, creative agency portfolios, or event websites where establishing a strong visual mood is critical.

* **Value Addition**: Compared to a static background color or image, a video hero adds motion, life, and narrative depth. It transforms a standard header into an engaging, television-like establishing shot for the website.

* **Browser Compatibility**: Broadly supported. HTML5 `<video>` elements, CSS `object-fit`, and CSS Flexbox are supported universally across all modern browsers (Chrome, Firefox, Safari, Edge). Autoplay requires the video to be `muted` on modern browsers to function correctly.


### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **HTML Structure**: Utilizes the semantic HTML5 `<video>` tag with specific attributes (`autoplay`, `loop`, `muted`, `playsinline`) to force it to act like an uninterruptible background rather than a standard media player.
  - **Color Logic**: The design relies on a dark-mode paradigm for the hero area. 
    - Text: Pure white `#ffffff`
    - Overlay: Semi-transparent black `rgba(0, 0, 0, 0.5)` to darken the video.
    - Button borders: White `#ffffff`.
  - **Typography**: Uses a geometric, highly legible sans-serif font (like Poppins or Inter). The main headline is massive (e.g., `95px` or `clamp()` equivalent) to act as a graphical element, with a high-contrast weight (bold/700).

* **Step B: Layout & Compositional Style**
  - **Spatial Feel**: Centered, balanced, and expansive. The content occupies the middle of the screen, leaving the edges free to showcase the video.
  - **Z-Index Layering**: 
    1. Base layer (`z-index: 0`): The Video, stretched to fill the container.
    2. Middle layer (`z-index: 1`): The overlay `div` with the `rgba` background.
    3. Top layer (`z-index: 2`): The content container holding the text and button.
  - **Positioning**: The container uses `position: relative` with `100vh` height. The video and overlay use `position: absolute`, `top: 0`, `left: 0`, `width: 100%`, `height: 100%`. To ensure the video covers the area without distortion, `object-fit: cover` is used (a modern, robust alternative to the tutorial's media-query approach).

* **Step C: Interactive Behavior & Animations**
  - **Button Hover**: The hollow "ghost" button transitions on hover. The transparent background fills with a solid color, and the text color inverts. 
  - **Timing**: A smooth `transition: 0.3s ease` is applied to the button's background and text color to make the interaction feel polished.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Background Video | HTML5 `<video>` tag | Native, performant way to play media without external libraries. Attributes handle looping and muting. |
| Video Sizing | CSS `object-fit: cover` | Modern standard for making media completely fill a container while preserving aspect ratio, avoiding complex media queries. |
| Content Centering | CSS Flexbox | `justify-content: center` and `align-items: center` perfectly align the content block horizontally and vertically. |
| Dimming Overlay | CSS absolutely positioned `div` | A separate layer with `background: rgba()` ensures the dimming effect applies cleanly over the video without affecting the stacking context of the text. |

> **Feasibility Assessment**: 100% reproduction. The code below perfectly recreates the cinematic video background, the text overlay, and the interactive ghost button using modern, robust CSS standards.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Explore More",
    body_text: str = "Discover the future of interactive learning.",
    color_scheme: str = "dark",        # "dark" (dark overlay/white text) or "light" (light overlay/dark text)
    accent_color: str = "#ffffff",     # Button hover background color
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Cinematic Video Hero visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors based on the requested scheme ===
    if color_scheme == "dark":
        text_color = "#ffffff"
        overlay_color = "rgba(0, 0, 0, 0.5)"
        btn_hover_text = "#000000" if accent_color.lower() in ["#ffffff", "white"] else "#ffffff"
    else:
        text_color = "#1a1a2e"
        overlay_color = "rgba(255, 255, 255, 0.65)"
        btn_hover_text = "#ffffff" if accent_color.lower() in ["#000000", "black"] else "#ffffff"

    # === CSS ===
    css = f"""/* Cinematic Video Hero — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --text-color: {text_color};
    --overlay-color: {overlay_color};
    --accent-color: {accent_color};
    --btn-hover-text: {btn_hover_text};
    
    /* Variables for embedding context, though the hero usually spans viewport */
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Poppins', system-ui, -apple-system, sans-serif;
    /* Center the component in the viewer */
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    background: #111;
}}

/* The main component container */
.video-hero {{
    position: relative;
    width: var(--width);
    max-width: 100%;
    height: var(--height);
    max-height: 100vh;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    border-radius: 8px; /* Optional: Looks good if not full-screen */
    box-shadow: 0 20px 40px rgba(0,0,0,0.4);
}}

/* The background video */
.video-hero__media {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    z-index: 0;
}}

/* The color overlay to ensure text readability */
.video-hero__overlay {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: var(--overlay-color);
    z-index: 1;
}}

/* The foreground content */
.video-hero__content {{
    position: relative;
    z-index: 2;
    padding: 2rem;
    color: var(--text-color);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.5rem;
}}

.video-hero__title {{
    /* Using clamp for responsive typography */
    font-size: clamp(3rem, 8vw, 6rem);
    font-weight: 700;
    line-height: 1.1;
    letter-spacing: -0.02em;
    margin-bottom: 0.5rem;
}}

.video-hero__body {{
    font-size: clamp(1rem, 2vw, 1.25rem);
    font-weight: 400;
    max-width: 600px;
    opacity: 0.9;
    margin-bottom: 1rem;
}}

/* The call to action button */
.video-hero__btn {{
    display: inline-block;
    padding: 15px 35px;
    font-size: 1.25rem;
    font-weight: 500;
    color: var(--text-color);
    text-decoration: none;
    background: transparent;
    border: 2px solid var(--text-color);
    border-radius: 50px;
    cursor: pointer;
    transition: all 0.3s ease;
}}

.video-hero__btn:hover,
.video-hero__btn:focus {{
    background-color: var(--accent-color);
    color: var(--btn-hover-text);
    border-color: var(--accent-color);
    outline: none;
    transform: translateY(-2px);
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    
    <section class="video-hero">
        <!-- Sample video from an open source test bucket -->
        <video class="video-hero__media" autoplay loop muted playsinline poster="https://storage.googleapis.com/gtv-videos-bucket/sample/images/ForBiggerBlazes.jpg">
            <source src="https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4" type="video/mp4">
            Your browser does not support the video tag.
        </video>
        
        <div class="video-hero__overlay"></div>
        
        <div class="video-hero__content">
            <h1 class="video-hero__title">{title_text}</h1>
            <p class="video-hero__body">{body_text}</p>
            <a href="#" class="video-hero__btn">Start Learning</a>
        </div>
    </section>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Cinematic Video Hero — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const video = document.querySelector('.video-hero__media');
    
    // Fallback: Ensure video plays even if browser policies block initial autoplay
    // Sometimes browsers require interaction even if muted, though usually muted bypasses this.
    const attemptPlay = () => {{
        video.play().catch(error => {{
            console.log("Autoplay prevented. Waiting for interaction.", error);
            // Optionally show a play button here if autoplay completely fails
        }});
    }};
    
    attemptPlay();
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

### 4. Accessibility & Performance Notes

* **Accessibility**:
  - The video must have the `muted` attribute; otherwise, modern browsers will block it from autoplaying, breaking the intended visual effect.
  - The `rgba` overlay layer is crucial for maintaining contrast ratios. Ensure the opacity is high enough (e.g., `0.5` or higher on dark mode) so the white text passes WCAG AA guidelines against whatever is playing in the video.
  - Ideally, for users with vestibular disorders, checking for `@media (prefers-reduced-motion: reduce)` in CSS to display a static background image instead of the video is best practice, though this requires configuring a static fallback image path.
* **Performance**:
  - Background videos are heavy. It is highly recommended to compress the video heavily (using lower bitrates, 720p or 1080p maximum, removing audio tracks entirely from the file itself rather than just muting via HTML).
  - Use the `poster` attribute on the `<video>` tag. This loads a static image instantly while the video buffers, preventing an ugly blank space during page load. The generated code includes a sample poster.