# Scroll-Driven Video Scrubber (Scrollytelling)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Scroll-Driven Video Scrubber (Scrollytelling)

* **Core Visual Mechanism**: Tying the `currentTime` of a sticky, full-screen background video directly to the user's vertical scroll progress. As the user scrolls down, the video plays forward; as they scroll up, it reverses. Content (text, cards) is layered on top, appearing at specific scroll depths to match the visual narrative of the video.
* **Why Use This Skill (Rationale)**: This technique creates a highly tactile, immersive experience. It hands temporal control over to the user, transforming passive video consumption into an active "scrollytelling" journey. It anchors the user's attention, making the content feel deliberate and high-end.
* **Overall Applicability**: Perfect for high-impact landing pages, product feature reveals (commonly seen on Apple product pages), storytelling editorials, and documentary-style web layouts.
* **Browser Compatibility**: Relies on CSS `position: sticky` and HTML5 `<video>`, which are universally supported in modern browsers. The GSAP ScrollTrigger library handles the complex scroll math. *Note: Smoothness is highly dependent on video encoding; videos must be encoded with frequent keyframes (ideally 30fps with a GOP size of 1) to prevent decoding lag while scrubbing.*

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Video Element**: An HTML5 `<video>` set to `object-fit: cover` to fill the viewport, heavily relying on `muted`, `playsinline`, and `preload="auto"` attributes.
  - **Color/Contrast**: A semi-transparent overlay (tint) is placed over the video to ensure the typography remains readable regardless of the video's underlying frame colors.
  - **Typography**: Bold, oversized headings (e.g., `clamp(3rem, 6vw, 6rem)`) using strong sans-serif fonts to command attention over the moving background.

* **Step B: Layout & Compositional Style**
  - **Scroll Track**: A parent container given an artificially tall height (e.g., `400vh`) to create a "scrollable zone."
  - **Sticky Container**: The video is wrapped in a container set to `position: sticky; top: 0; height: 100vh;`. This locks the video in place while the user scrolls through the `400vh` track.
  - **Z-Index Layering**: The video sits at `z-index: 0`, while the overlay text sections use `margin-top: -100vh` (or absolute positioning) and `z-index: 2` to overlap the sticky video naturally as the user scrolls.

* **Step C: Interactive Behavior & Animations**
  - A GSAP `ScrollTrigger` maps the scroll progress (`0` to `1`) of the track container to the video's `currentTime` (`0` to `duration`).
  - Smoothing (`scrub: 0.5`) is applied so the video doesn't abruptly stop when the user's mouse wheel clicks, but instead glides to the target frame.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Sticky Background** | CSS `position: sticky` | Native, performant way to pin an element to the viewport without complex JS recalculations. |
| **Scroll-to-Time Mapping** | JS (GSAP + ScrollTrigger) | Provides robust cross-browser scroll tracking and smooth tweening via the `scrub` property, avoiding manual `requestAnimationFrame` boilerplate. |
| **Foreground Content Layering** | CSS normal flow with negative margins | Allows multiple sections of text to naturally scroll up over the pinned video without absolute positioning calculations. |

> **Feasibility Assessment**: 100% reproduction of the core mechanic. The code provides a robust, self-contained implementation of the Elementor/WordPress setup shown in the tutorial using pure HTML/CSS/JS.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "ORGANIC JUICE",
    body_text: str = "Scroll down to control time and explore the perfect blend.",
    color_scheme: str = "dark",
    accent_color: str = "#ff4757",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Scroll-Driven Video Scrubber effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0a0a0a"
        text_color = "#ffffff"
        tint_color = "rgba(0, 0, 0, 0.5)"
        section_bg = "#111111"
    else:
        bg_color = "#ffffff"
        text_color = "#0a0a0a"
        tint_color = "rgba(255, 255, 255, 0.4)"
        section_bg = "#f8f9fa"

    # === CSS ===
    css = f"""/* Scroll-Driven Video Scrubber */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --tint: {tint_color};
    --section-bg: {section_bg};
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
    overflow-x: hidden;
}}

/* Intro section just to show scroll context */
.intro-section {{
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--bg);
    padding: 2rem;
    text-align: center;
}}

.intro-section h1 {{
    font-size: clamp(2.5rem, 5vw, 5rem);
    text-transform: uppercase;
    letter-spacing: -0.03em;
    font-weight: 800;
}}

/* The main scroll track containing the video */
.scroll-track {{
    /* 400vh gives us 3 viewport heights worth of scrollable scrubbing space */
    height: 400vh; 
    position: relative;
    width: 100%;
}}

/* The sticky container locks the video to the viewport while inside the track */
.video-container {{
    position: sticky;
    top: 0;
    width: 100%;
    height: 100vh;
    overflow: hidden;
    z-index: 0;
}}

.scrub-video {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    /* Optional: scale slightly to prevent edge artifacts */
    transform: scale(1.02);
}}

.video-tint {{
    position: absolute;
    inset: 0;
    background: var(--tint);
    z-index: 1;
}}

/* Content layered on top of the video */
.content-overlay {{
    position: relative;
    z-index: 2;
    /* Pull the content up over the sticky container */
    margin-top: -100vh;
    pointer-events: none; /* Let clicks pass through if needed */
}}

.screen {{
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 2rem;
}}

.screen-content {{
    max-width: 800px;
    background: rgba(0, 0, 0, 0.01);
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
    padding: 3rem;
    border-radius: 24px;
    border: 1px solid rgba(255,255,255,0.1);
}}

.title {{
    font-size: clamp(3rem, 6vw, 6rem);
    text-transform: uppercase;
    letter-spacing: -0.02em;
    font-weight: 800;
    margin-bottom: 1rem;
    color: var(--text);
}}

.body-text {{
    font-size: clamp(1.1rem, 2vw, 1.5rem);
    line-height: 1.6;
    color: var(--text);
    opacity: 0.9;
}}

.highlight {{
    color: var(--accent);
}}

/* Normal content block below the track */
.normal-section {{
    min-height: 100vh;
    background: var(--section-bg);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    position: relative;
    z-index: 3;
    padding: 4rem 2rem;
    text-align: center;
}}

/* Graceful degradation for users who prefer reduced motion */
@media (prefers-reduced-motion: reduce) {{
    .scroll-track {{ height: auto; }}
    .video-container {{ position: relative; height: 60vh; }}
    .content-overlay {{ margin-top: 0; }}
    .screen {{ height: auto; padding: 4rem 2rem; }}
    .scrub-video {{ display: none; }} /* Fallback applied via JS or poster */
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <header class="intro-section">
        <div>
            <h1>Scroll Down</h1>
            <p style="opacity: 0.6; margin-top: 1rem;">Begin the experience</p>
        </div>
    </header>

    <main class="scroll-track">
        <div class="video-container">
            <!-- Using a widely available GSAP demo Codepen asset known for good keyframing -->
            <video class="scrub-video" 
                   src="https://assets.codepen.io/39255/output_960.mp4" 
                   muted 
                   playsinline 
                   preload="auto"></video>
            <div class="video-tint"></div>
        </div>
        
        <div class="content-overlay">
            <section class="screen">
                <div class="screen-content">
                    <h2 class="title">{title_text}</h2>
                    <p class="body-text">{body_text}</p>
                </div>
            </section>
            <section class="screen">
                <div class="screen-content">
                    <h2 class="title" style="font-size: clamp(2rem, 4vw, 4rem);">Perfectly <span class="highlight">Synced</span></h2>
                    <p class="body-text">The video is scrubbed forward and backward precisely to your scrollbar.</p>
                </div>
            </section>
            <section class="screen">
                <!-- Empty screen to let the user focus purely on the end of the video animation -->
            </section>
        </div>
    </main>

    <section class="normal-section">
        <h2 class="title" style="font-size: 3rem;">Normal Flow Resumes</h2>
        <p class="body-text" style="max-width: 600px; margin-top: 1rem;">
            Once the scroll track is completed, standard web flow takes over seamlessly.
        </p>
    </section>

    <!-- GSAP & ScrollTrigger CDNs -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Initialize Scroll-Driven Video Scrubber
document.addEventListener('DOMContentLoaded', () => {
    // Respect user motion preferences
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (prefersReducedMotion) return;

    gsap.registerPlugin(ScrollTrigger);
    
    const video = document.querySelector('.scrub-video');
    const track = document.querySelector('.scroll-track');

    // Function to set up the GSAP tween
    function setupScrub() {
        gsap.to(video, {
            // Animate the currentTime of the video to its total duration
            currentTime: video.duration || 1, 
            ease: "none",
            scrollTrigger: {
                trigger: track,
                start: "top top",     // When the top of track hits top of viewport
                end: "bottom bottom", // When bottom of track hits bottom of viewport
                scrub: 0.5,           // Slight smoothing for mouse wheel clicks
                // markers: true      // Uncomment for debugging
            }
        });
    }

    // We must ensure the browser has loaded the video metadata to know the duration
    if (video.readyState >= 1) { // HAVE_METADATA
        setupScrub();
    } else {
        video.addEventListener('loadedmetadata', setupScrub);
    }
    
    // Attempt to warm up the video decoder to prevent initial stuttering
    // Note: Autoplay policies might catch this, so we swallow the promise error
    video.play().then(() => {
        video.pause();
    }).catch((e) => {
        // Autoplay blocked, no action needed, scrubbing will still work
    });
});
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

* **Performance (Critical)**: Scrubbing an HTML5 `<video>` by continuously manipulating `currentTime` is computationally heavy. The browser has to decode specific frames rapidly. **The video file must be optimized for this:** it should have a high keyframe frequency (a GOP size of 1 means every frame is a keyframe) and a consistent framerate (e.g., 30fps). If the video lags in production, standard procedure is to extract the video into an image sequence and scrub through the images on a `<canvas>` instead.
* **Accessibility**: The interaction relies heavily on visual motion. The code includes a `@media (prefers-reduced-motion: reduce)` block in CSS and a `matchMedia` check in JavaScript. If a user has reduced motion enabled in their OS, the CSS flattens the sticky layout, and the JS skips the GSAP initialization entirely, providing a standard, static reading experience. 
* **Touch Devices**: `playsinline` is strictly required for iOS Safari; otherwise, it will attempt to open the video in the native fullscreen media player, breaking the design entirely. The `scrub: 0.5` property ensures the scrubber feels smooth and momentum-based even on varying touch/scroll wheel inputs.