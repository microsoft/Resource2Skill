# Scroll-Pinned Morphing Product Showcase

## Analysis

An elegant and highly engaging scroll interaction pattern, this technique locks a primary visual element (like a product image) in the viewport while seamlessly morphing its properties (rotation, scale, position) to interact with new content blocks as they scroll past.

Here is the breakdown and reproducible code for the **Scroll-Pinned Morphing Product Showcase**.

### 1. High-level Design Pattern Extraction

> **Skill Name**: Scroll-Pinned Morphing Product Showcase

* **Core Visual Mechanism**: A central visual element (a product bottle in this case) is pinned to the center of the viewport upon scroll. As the user continues scrolling down, the background sections (hero, features, timeline) flow normally, while the pinned product uses a scrubbed timeline to morph its scale, rotation, and horizontal offset to dynamically interact with the new layouts appearing behind it. 
* **Why Use This Skill (Rationale)**: This creates an unbroken narrative thread. By keeping the product constantly in view and actively reacting to the scroll state, the user feels a continuous connection to the core subject. It transforms a standard, segmented landing page into a cohesive, cinematic storytelling experience.
* **Overall Applicability**: Perfect for high-end physical products (beverages, cosmetics, tech gadgets), storytelling brand pages, visual timelines, and "how-it's-made" interactive funnels.
* **Value Addition**: It drastically increases dwell time and scroll-depth. By physically moving the product aside to reveal text, it directs the user's eye exactly where the designer intends, achieving perfect harmony between visual aesthetic and information delivery.
* **Browser Compatibility**: Broadly compatible across modern browsers. Relies on GSAP (JavaScript) for fixed-position pinning and hardware-accelerated CSS transforms. `gsap.matchMedia()` handles responsive disabling for mobile views seamlessly.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **HTML Structure**: A sticky navigation header, followed by consecutive `100vh` sections (`hero`, `intro`, `timeline-1`, `timeline-2`). A separate, absolute-positioned wrapper holds the product graphic.
  - **Color Logic**: Warm, premium organic tones. A creamy background (`#f8f5eb`), deep rusty-red text/accents (`#8a2512`), and dark charcoal for secondary text (`#2c2c2c`).
  - **Typographic Hierarchy**: Premium serif headers (e.g., *Playfair Display*) paired with clean, utilitarian sans-serif body text (e.g., *Inter*).
  - **CSS Properties**: Uses `will-change: transform` to ensure the heavy scrub animations are GPU-accelerated. CSS gradients and inset box-shadows are used to give depth to the product.

* **Step B: Layout & Compositional Style**
  - **Flex Layout**: The sections use Flexbox to align text either left, right, or center depending on where the product will be positioned at that moment.
  - **Z-index Layering**: The sticky header has the highest z-index (`100`), the pinned product wrapper is placed just below it (`50`), and the background scrollable sections sit at the base level (`1`).

* **Step C: Interactive Behavior & Animations**
  - **Pinning (`pin: true`)**: GSAP ScrollTrigger removes the element from normal scroll flow, effectively making it `position: fixed` while the defined trigger area is in the viewport.
  - **Scrubbing (`scrub: true`)**: Binds the playback head of the animation directly to the user's scrollbar. If the user stops, the animation pauses. If they scroll up, it reverses.
  - **Sequential Timeline Triggers**: 
    1. Hero → Intro: Bottle scales down (`0.8`) and resets rotation to `0deg`.
    2. Intro → Timeline 1: Bottle shifts right (`x: 30vw`) and tilts right (`rotate: 10deg`) to reveal left-aligned text.
    3. Timeline 1 → Timeline 2: Bottle shifts left (`x: -25vw`) and tilts left (`rotate: -10deg`) to reveal right-aligned text.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Scroll Pinning & Scrubbing** | GSAP + ScrollTrigger | Native CSS cannot seamlessly string together complex, scrubbed timeline animations across multiple DOM sections while pinning an element. GSAP is the industry standard for this exact visual sequence. |
| **Responsive Logic** | `gsap.matchMedia()` | Automatically tears down complex ScrollTriggers on mobile (where they often cause UX jank) and replaces them with a simple fade-in. |
| **Product Visual** | Native CSS Shapes | To ensure the code runs immediately without external image dependency/CORS issues, the "bottle" is constructed entirely via CSS using gradients and box-shadows, creating a perfect, transparent, high-end placeholder. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Crimson Fermentation",
    body_text: str = "A journey began in a wooden barn nested among oak trees.",
    color_scheme: str = "light",
    accent_color: str = "#8a2512",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the GSAP Scroll-Pinned Morphing Product Showcase.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme colors
    if color_scheme == "dark":
        bg_color = "#1a1a1a"
        text_color = "#f8f5eb"
        surface_color = "#2c2c2c"
    else:
        bg_color = "#f8f5eb"
        text_color = "#2c2c2c"
        surface_color = "rgba(0,0,0,0.05)"

    # CSS - Root variables block
    css_root = f""":root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
}}
"""

    # CSS - Static rules block
    css_body = r"""
*, *::before, *::after {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Inter', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
    overflow-x: hidden;
    line-height: 1.6;
}

h1, h2, h3 {
    font-family: 'Playfair Display', serif;
    color: var(--accent);
    text-transform: uppercase;
}

header {
    position: sticky;
    top: 0;
    height: 60px;
    background: var(--bg);
    border-bottom: 1px solid var(--surface);
    display: flex;
    align-items: center;
    padding: 0 2rem;
    z-index: 100;
    font-weight: bold;
    letter-spacing: 2px;
}

/* Sections */
section {
    position: relative;
    min-height: 100vh;
    padding: 100px 10%;
    display: flex;
    align-items: center;
    border-bottom: 1px dashed var(--surface);
}

.hero {
    justify-content: center;
    text-align: center;
}

.hero h1 {
    font-size: clamp(3rem, 8vw, 7rem);
    z-index: 1;
    max-width: 900px;
    line-height: 1.1;
}

.section-intro .content { width: 45%; margin-right: auto; }
.timeline-1 { justify-content: flex-end; }
.timeline-1 .content { width: 45%; }
.timeline-2 { justify-content: flex-start; }
.timeline-2 .content { width: 45%; }

.content h2 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
}

.content p {
    font-size: 1.1rem;
    opacity: 0.8;
}

/* Product Wrapper & Element */
.bottle-wrapper {
    position: absolute;
    top: 15vh; /* Initial top offset, pinned here by GSAP */
    left: calc(50% - 60px); /* Centered based on bottle width (120/2) */
    width: 120px;
    height: 400px;
    z-index: 50;
    pointer-events: none; /* Let clicks pass through to sections below */
    will-change: transform;
}

.bottle-element {
    width: 100%;
    height: 100%;
    transform: rotate(20deg) scale(1.1); /* Default un-scrolled state */
    transform-origin: center center;
    will-change: transform;
}

/* Pure CSS stylized bottle for standalone reproduction */
.css-bottle {
    width: 100%;
    height: 100%;
    background: linear-gradient(to right, #8b3a13, #e27d32, #8b3a13);
    border-radius: 20px 20px 10px 10px;
    position: relative;
    box-shadow: inset -15px 0 25px rgba(0,0,0,0.6), 0 20px 40px rgba(0,0,0,0.4);
}

.css-bottle::before { /* Bottle Neck */
    content: '';
    position: absolute;
    bottom: 99%;
    left: 50%;
    transform: translateX(-50%);
    width: 36px;
    height: 120px;
    background: linear-gradient(to right, #8b3a13, #e27d32, #8b3a13);
    border-radius: 5px 5px 0 0;
    box-shadow: inset -8px 0 15px rgba(0,0,0,0.6);
}

.css-bottle::after { /* Bottle Cap */
    content: '';
    position: absolute;
    bottom: calc(100% + 115px);
    left: 50%;
    transform: translateX(-50%);
    width: 40px;
    height: 15px;
    background: #d4af37; /* Gold */
    border-radius: 3px;
    box-shadow: inset 0 -2px 5px rgba(0,0,0,0.3);
}

.bottle-label {
    position: absolute;
    top: 55%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 90%;
    height: 140px;
    background: #fffdf5;
    border-radius: 4px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: var(--accent);
    text-align: center;
    padding: 10px;
    box-shadow: inset 0 0 10px rgba(0,0,0,0.1);
    font-family: 'Playfair Display', serif;
}

.bottle-label span:first-child { font-size: 0.7rem; letter-spacing: 2px; }
.bottle-label span:last-child { font-size: 1.2rem; font-weight: bold; line-height: 1; margin-top: 5px; }

/* Responsive tweaks */
@media (max-width: 768px) {
    .section-intro .content, .timeline-1 .content, .timeline-2 .content {
        width: 100%;
        text-align: center;
    }
    .bottle-wrapper {
        position: relative;
        top: 0; left: 0;
        margin: 50px auto;
        opacity: 0; /* Fallback fade-in state */
    }
    .bottle-element { transform: rotate(0deg) scale(1); }
}
"""
    css = css_root + css_body

    # HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&family=Playfair+Display:wght@700;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
    
    <!-- GSAP & ScrollTrigger CDNs -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>
</head>
<body>
    <header>CRAFTEDGE</header>
    
    <div class="scroll-container">
        <section class="section hero" id="section-hero">
            <div class="bottle-wrapper">
                <div class="bottle-element">
                    <div class="css-bottle">
                        <div class="bottle-label">
                            <span>ARTISAN CRAFT</span>
                            <span>CRIMSON<br>RESERVE</span>
                        </div>
                    </div>
                </div>
            </div>
            <h1>{title_text}</h1>
        </section>

        <section class="section section-intro" id="section-intro">
            <div class="content">
                <h2>The Heritage Line</h2>
                <p>{body_text}</p>
                <p>Purified through time and intention, this reserve sets a new standard for smoothness and clarity.</p>
            </div>
        </section>

        <section class="section timeline-1" id="section-timeline-1">
            <div class="content">
                <h2>1984 First Batch</h2>
                <p>We brewed our first batch utilizing hand-milled barley and extreme patience nested deep within the valley.</p>
            </div>
        </section>

        <section class="section timeline-2" id="section-timeline-2">
            <div class="content">
                <h2>1989 The Fire Oak</h2>
                <p>A lightning storm sparked a fire that charred the oak barrels. From the ashes, we reclaimed our signature smoky finish.</p>
            </div>
        </section>
        
        <section class="section footer" style="min-height: 50vh; justify-content: center;">
            <div class="content" style="text-align: center;">
                <h2>Experience the Legacy</h2>
            </div>
        </section>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # JS
    js = r"""document.addEventListener('DOMContentLoaded', () => {
    gsap.registerPlugin(ScrollTrigger);

    // Reusable function to handle sequential pinning and scrub animation
    function pinAndAnimate({ trigger, endTrigger, pin, animations }) {
        // Offset 60px to account for the sticky header
        const tl = gsap.timeline({
            scrollTrigger: {
                trigger: trigger,
                start: "top top+=60", 
                endTrigger: endTrigger,
                end: "top top+=60",
                pin: pin,
                scrub: 1, // Add slight smoothing to the scrub
                pinSpacing: false, // Allows content below to flow up and under the pin
                invalidateOnRefresh: true
            }
        });

        // Add all passed animations to start simultaneously
        animations.forEach((anim) => {
            tl.to(anim.target, anim.vars, anim.position || 0);
        });
    }

    // Responsive Scroll logic
    let mm = gsap.matchMedia();

    // Desktop: Run full interactive scroll timelines
    mm.add("(min-width: 769px)", () => {
        
        // Setup initial state smoothly
        gsap.set(".bottle-wrapper", { x: 0 });

        // Sequence 1: Hero -> Intro (Settle into page)
        pinAndAnimate({
            trigger: "#section-hero",
            endTrigger: "#section-intro",
            pin: ".bottle-wrapper",
            animations: [
                { target: ".bottle-element", vars: { rotate: 0, scale: 0.8 } }
            ]
        });

        // Sequence 2: Intro -> Timeline 1 (Shift right, reveal left text)
        pinAndAnimate({
            trigger: "#section-intro",
            endTrigger: "#section-timeline-1",
            pin: ".bottle-wrapper",
            animations: [
                { target: ".bottle-element", vars: { rotate: 10, scale: 0.7 } },
                { target: ".bottle-wrapper", vars: { x: "25vw" } }
            ]
        });

        // Sequence 3: Timeline 1 -> Timeline 2 (Shift left, reveal right text)
        pinAndAnimate({
            trigger: "#section-timeline-1",
            endTrigger: "#section-timeline-2",
            pin: ".bottle-wrapper",
            animations: [
                { target: ".bottle-element", vars: { rotate: -10, scale: 0.7 } },
                { target: ".bottle-wrapper", vars: { x: "-25vw" } }
            ]
        });
        
        // Sequence 4: Timeline 2 -> Footer (Re-center)
        pinAndAnimate({
            trigger: "#section-timeline-2",
            endTrigger: ".footer",
            pin: ".bottle-wrapper",
            animations: [
                { target: ".bottle-element", vars: { rotate: 0, scale: 0.9 } },
                { target: ".bottle-wrapper", vars: { x: "0vw" } }
            ]
        });

    });

    // Mobile: Simplified fallback (Remove complex pinning, just fade in)
    mm.add("(max-width: 768px)", () => {
        gsap.to(".bottle-wrapper", {
            scrollTrigger: {
                trigger: "#section-hero",
                start: "top center",
            },
            opacity: 1,
            duration: 1.5,
            ease: "power2.out"
        });
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

* **Performance / GPU Acceleration**: The properties being animated (`x`, `rotate`, `scale`) are mapped entirely to CSS transforms. By declaring `will-change: transform;` in the CSS, we force the browser to composite the `.bottle-element` layer on the GPU, avoiding expensive layout repaints on every scroll tick.
* **Flow Separation (`pinSpacing: false`)**: The primary trick enabling this logic is setting `pinSpacing: false` on the ScrollTrigger. This isolates the pinned component visually without breaking the DOM dimensions, allowing the subsequent text blocks to scroll "underneath" the product smoothly.
* **MatchMedia Fallbacks**: Scroll-linked timeline scrubbing often creates terrible UX on smaller touch screens where native scroll-momentum behaves differently. The code uses `gsap.matchMedia()` to completely discard the scrub logic on mobile devices (`<768px`), collapsing the layout into standard block-flow and substituting it with a high-performance opacity fade-in.