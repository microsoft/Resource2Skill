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
