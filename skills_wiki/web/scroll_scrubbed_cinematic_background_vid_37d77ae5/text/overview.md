# Scroll-Scrubbed Cinematic Background Video

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Scroll-Scrubbed Cinematic Background Video

*   **Core Visual Mechanism**: A full-screen, fixed-position background video whose playback is directly tied to the user's scroll position. Instead of playing automatically over time, the video acts as a timeline; scrolling down advances the video frames, and scrolling up rewinds them. The foreground UI elements (navigation, hero text) remain stationary (`position: fixed`) floating above the cinematic action.
*   **Why Use This Skill (Rationale)**: This technique creates a highly immersive, storytelling-driven user experience. It transfers control of the visual pacing to the user, making passive video consumption feel interactive. It is highly effective for product showcases where you want to emphasize different angles or states of a product as the user "progresses" through the page.
*   **Overall Applicability**: Ideal for high-end product landing pages (frequently used by companies like Apple), interactive documentaries, premium brand portfolios, and cinematic web experiences where visual spectacle is prioritized over dense text content.
*   **Value Addition**: Transforms a standard webpage into a timeline-based presentation. It adds a profound sense of depth, interactivity, and premium polish that static images or standard autoplaying background videos cannot achieve.
*   **Browser Compatibility**: Broadly supported in modern browsers. Relies on the HTML5 `<video>` element API (`currentTime` manipulation) and Intersection Observers (via GSAP). Smoothness heavily depends on the client's device performance and the specific encoding of the video file.

### 2. Visual & Technical Breakdown

*   **Step A: Core Visual Elements**
    *   **Background Video**: The foundational layer is a `<video>` element set to fill the screen (`width: 100vw; height: 100vh; object-fit: cover;`). It must have `muted` and `playsinline` attributes to allow programmatic playback control without user interaction policies blocking it.
    *   **Foreground UI**: Clean, bold typography floats above the video. The tutorial uses a minimalist, split-layout hero text ("Strawberry & Milk" on the left, "Milkshake Perfection" on the right).
    *   **Color Logic**: The video dictates the primary color palette. The UI text uses stark contrasting colors (e.g., `#ffffff` or very dark tones depending on the video brightness) to maintain legibility against the dynamic background.
    *   **CSS Properties**: `object-fit: cover` for the video, `position: fixed` for all visible elements, and a transparent layout overlay.

*   **Step B: Layout & Compositional Style**
    *   **The "Illusion" of Scrolling**: The actual visible content (video, header, hero text) is `position: fixed`. They do not move within the document flow.
    *   **The Scroll Spacer**: A hidden, empty `<div>` (e.g., `.scroll-spacer`) is given a massive height (e.g., `3000px` to `5000px`). This forces the browser to generate a scrollbar. The user is actually just scrolling down this empty space, while the fixed elements stay pinned to the viewport.
    *   **Z-index Layering**:
        *   `z-index: -1`: Video container
        *   `z-index: 10`: Hero text / Content
        *   `z-index: 20`: Header / Navigation

*   **Step C: Interactive Behavior & Animations**
    *   **Scroll-to-Video Sync**: JavaScript (using GSAP and ScrollTrigger) listens to the scroll position relative to the `.scroll-spacer`.
    *   It maps the scroll progress (0% to 100%) to the video's duration (0 seconds to `video.duration`).
    *   It continuously updates the `video.currentTime` property.
    *   `scrub: true` (or a numerical value like `scrub: 1` for smoothing) ensures the animation catches up to the scrollbar smoothly rather than jumping instantly, creating a fluid, easing effect.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
| :--- | :--- | :--- |
| **Video Playback Scrubbing** | GSAP ScrollTrigger + Video `currentTime` | Animating the `currentTime` property of a video element based on scroll progress is exactly what GSAP ScrollTrigger is built to optimize. It handles the requestAnimationFrame loop and scroll calculations automatically. |
| **Fullscreen Layout** | CSS Fixed Positioning | Using `position: fixed` keeps the video and UI pinned to the screen while allowing a hidden tall div to create the scrollable timeline. |
| **Media Scaling** | CSS `object-fit: cover` | Ensures the video covers the entire background without distorting its aspect ratio, regardless of the viewport dimensions. |

> **Feasibility Assessment**: 100%. The core mechanism is perfectly reproducible using vanilla HTML/CSS and GSAP. *Note: For the absolute best performance in production, the video file itself must be specifically encoded with frequent keyframes (I-frames) to prevent browser decoding lag when seeking rapidly.*

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Cinematic Flow",
    body_text: str = "Scroll down to control time.",
    color_scheme: str = "dark",
    accent_color: str = "#ff2a5f",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Scroll-Scrubbed Cinematic Background Video effect.
    Uses GSAP ScrollTrigger to tie video playback to scroll position.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        text_color = "#ffffff"
        ui_bg = "rgba(0, 0, 0, 0.3)"
    else:
        text_color = "#111111"
        ui_bg = "rgba(255, 255, 255, 0.4)"

    # Using a reliable public domain sample video suitable for demonstrating the effect
    video_url = "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4"

    css = f"""/* Scroll-Scrubbed Background Video */
:root {{
    --text-color: {text_color};
    --accent: {accent_color};
    --ui-bg: {ui_bg};
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body, html {{
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    background-color: #000;
    color: var(--text-color);
    /* Prevent horizontal scrolling */
    overflow-x: hidden; 
}}

/* The hidden spacer that creates the scrollable area */
.scroll-spacer {{
    /* The height determines how long the user has to scroll to finish the video */
    height: 400vh; 
    width: 100%;
    position: absolute;
    top: 0;
    left: 0;
    z-index: 0;
}}

/* Fixed container holding all visual elements */
.fixed-viewport {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: 1;
    overflow: hidden;
}}

/* The video itself */
.bg-video {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    z-index: -1;
    /* Optional: add a slight dimming filter if needed for text contrast */
    filter: brightness(0.8);
}}

/* UI Overlay styling */
header {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    padding: 2rem 4rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 10;
}}

.logo {{
    font-size: 1.5rem;
    font-weight: bold;
    letter-spacing: 2px;
}}

nav ul {{
    list-style: none;
    display: flex;
    gap: 2rem;
}}

nav a {{
    color: var(--text-color);
    text-decoration: none;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    transition: color 0.3s ease;
}}

nav a:hover {{
    color: var(--accent);
}}

.hero {{
    position: absolute;
    top: 50%;
    left: 0;
    width: 100%;
    transform: translateY(-50%);
    display: flex;
    justify-content: space-between;
    padding: 0 5vw;
    z-index: 10;
    pointer-events: none; /* Let clicks pass through to video if needed */
}}

.hero-left, .hero-right {{
    width: 45%;
}}

.hero-right {{
    text-align: right;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    justify-content: center;
}}

h1 {{
    font-size: clamp(3rem, 6vw, 6rem);
    line-height: 1.1;
    font-weight: 800;
    margin-bottom: 1rem;
}}

p {{
    font-size: clamp(1rem, 1.5vw, 1.5rem);
    font-weight: 400;
    opacity: 0.9;
    max-width: 400px;
}}

.scroll-indicator {{
    position: absolute;
    bottom: 3rem;
    left: 4rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    z-index: 10;
}}

.scroll-text {{
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 4px;
    writing-mode: vertical-rl;
    transform: rotate(180deg);
    opacity: 0.7;
}}

.scroll-line {{
    width: 1px;
    height: 60px;
    background-color: var(--text-color);
    opacity: 0.5;
}}

/* Loader for when video is buffering metadata */
.loader {{
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 1.2rem;
    letter-spacing: 2px;
    z-index: 100;
    color: var(--text-color);
    transition: opacity 0.5s ease;
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <!-- Loading state indicator -->
    <div class="loader" id="loader">Loading Video...</div>

    <!-- The tall element that creates scrollable space -->
    <div class="scroll-spacer"></div>

    <!-- The fixed viewport holding the UI and Video -->
    <div class="fixed-viewport">
        <!-- Video element: muted and playsinline are critical for programmatic control -->
        <video 
            id="bg-video" 
            class="bg-video" 
            src="{video_url}" 
            muted 
            playsinline 
            preload="auto"
        ></video>

        <header>
            <div class="logo">BRAND</div>
            <nav>
                <ul>
                    <li><a href="#">Home</a></li>
                    <li><a href="#">Showcase</a></li>
                    <li><a href="#">Specs</a></li>
                    <li><a href="#">Buy</a></li>
                </ul>
            </nav>
        </header>

        <section class="hero">
            <div class="hero-left">
                <h1>{title_text}</h1>
            </div>
            <div class="hero-right">
                <p>{body_text}</p>
            </div>
        </section>

        <div class="scroll-indicator">
            <div class="scroll-line"></div>
            <div class="scroll-text">SCROLL</div>
        </div>
    </div>

    <!-- GSAP Core -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <!-- GSAP ScrollTrigger -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Register GSAP Plugin
gsap.registerPlugin(ScrollTrigger);

document.addEventListener('DOMContentLoaded', () => {{
    const video = document.getElementById('bg-video');
    const loader = document.getElementById('loader');

    // It is crucial to wait for the video metadata to load so we know its duration
    video.addEventListener('loadedmetadata', () => {{
        
        // Hide loader once video is ready
        loader.style.opacity = '0';
        setTimeout(() => loader.style.display = 'none', 500);

        // Map scroll position to video time
        gsap.to(video, {{
            currentTime: video.duration, // Animate from 0 to full duration
            ease: "none",                // Linear progression, tied strictly to scroll
            scrollTrigger: {{
                trigger: ".scroll-spacer", // The element determining scroll length
                start: "top top",          // Start animation when top of spacer hits top of viewport
                end: "bottom bottom",      // End animation when bottom of spacer hits bottom of viewport
                scrub: 1,                  // Smooth scrubbing effect (1 second lag)
                markers: false             // Set to true for debugging
            }}
        }});
    }});

    // Fallback: If video is cached, loadedmetadata might have already fired before the event listener was attached
    if (video.readyState >= 1) {{
        // Manually dispatch event to trigger setup
        video.dispatchEvent(new Event('loadedmetadata'));
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

*   **Accessibility (a11y)**:
    *   **Motion Sensitivity**: This effect creates intense, full-screen movement tied to user scrolling, which can trigger vestibular disorders. A robust implementation must include a `@media (prefers-reduced-motion: reduce)` media query or JS check to disable the GSAP ScrollTrigger and allow the video to simply play normally or fall back to a static image.
    *   **Contrast**: Because the background changes constantly, text contrast is unpredictable. Using a semi-transparent dark overlay (`filter: brightness(0.8)` or a CSS gradient over the video) helps ensure the text remains readable regardless of what frame the video is on.
*   **Performance (Crucial)**:
    *   **Video Encoding matters more than code here.** Standard MP4 videos (H.264) compress data by saving a full image (Keyframe/I-frame) every few seconds, and for the frames in between, they only save the *changes* (P-frames/B-frames). When a user scrolls rapidly, GSAP asks the browser to jump to random times in the video. If that time lands on a P-frame, the browser must find the previous Keyframe and rapidly decode all intermediate frames to calculate the current image. This causes severe lag, CPU spikes, and "janky" scrubbing.
    *   **The Fix**: For production, the video should be transcoded to have a **Keyframe every 1 frame** (All-Intra encoding). This drastically increases file size, so it must be balanced with heavy compression and reduced resolution (e.g., 720p or aggressive bitrate limiting).
    *   **Mobile Execution**: Mobile browsers often throttle programmatic video playback to save battery. Ensure the video element explicitly includes `muted` and `playsinline` attributes, or iOS Safari will refuse to scrub it and will try to open it in the native fullscreen player.