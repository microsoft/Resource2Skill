def create_component(
    output_dir: str,
    title_text: str = "HOME",
    body_text: str = "Click the navigation links to trigger the transition.",
    color_scheme: str = "dark",
    accent_color: str = "#ffffff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Cinematic Shutter Page Transition.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#111111"
        text_color = "#f4f4f5"
        shutter_color = accent_color if accent_color != "#ffffff" else "#f4f4f5"
    else:
        bg_color = "#f4f4f5"
        text_color = "#111111"
        shutter_color = accent_color if accent_color != "#ffffff" else "#111111"

    css = f"""/* Cinematic Shutter Transition */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --shutter: {shutter_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: #000;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.app-container {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    position: relative;
    overflow: hidden;
    background-color: var(--bg);
    color: var(--text);
    box-shadow: 0 20px 40px rgba(0,0,0,0.4);
}}

/* Navigation */
.nav {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    padding: 2.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 10;
}}

.logo {{
    color: var(--text);
    text-decoration: none;
    font-weight: 800;
    font-size: 1.25rem;
    letter-spacing: 0.05em;
}}

.nav-items {{
    display: flex;
    gap: 3rem;
}}

.nav-items a {{
    color: var(--text);
    text-decoration: none;
    font-family: 'IBM Plex Mono', monospace;
    text-transform: uppercase;
    font-size: 0.9rem;
    font-weight: 500;
    transition: opacity 0.2s;
}}

.nav-items a:hover {{
    opacity: 0.6;
}}

/* Content */
.content {{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    text-align: center;
}}

.title {{
    font-size: clamp(5rem, 12vw, 12rem);
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: -0.03em;
    line-height: 1;
}}

.body-text {{
    margin-top: 1.5rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1rem;
    opacity: 0.6;
}}

/* Transition Shutter Overlay */
.transition-container {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    z-index: 1000;
    pointer-events: none; /* Let clicks pass through when idle */
}}

.transition-row {{
    flex: 1;
    display: flex;
}}

.block {{
    flex: 1;
    background-color: var(--shutter);
    will-change: transform;
}}

/* Origin controls the scale direction */
.row-1 .block {{
    transform-origin: top;
}}

.row-2 .block {{
    transform-origin: bottom;
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cinematic Transition</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500&family=Inter:wght@400;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
    <!-- GSAP Core -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
</head>
<body>
    <div class="app-container">
        <nav class="nav">
            <a href="#" class="logo">LOGO</a>
            <div class="nav-items">
                <a href="#home">Home</a>
                <a href="#about">About</a>
                <a href="#contact">Contact</a>
            </div>
        </nav>
        
        <main class="content">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </main>

        <div class="transition-container">
            <div class="transition-row row-1">
                <div class="block"></div>
                <div class="block"></div>
                <div class="block"></div>
                <div class="block"></div>
                <div class="block"></div>
            </div>
            <div class="transition-row row-2">
                <div class="block"></div>
                <div class="block"></div>
                <div class="block"></div>
                <div class="block"></div>
                <div class="block"></div>
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Cinematic Shutter Page Transition Logic
document.addEventListener("DOMContentLoaded", () => {
    // Initial State: Shutters fully covering the screen
    gsap.set(".block", { scaleY: 1, visibility: "visible" });
    
    // Simulate initial page load reveal
    revealTransition();

    /**
     * Plays the opening animation (Shutters scaling away)
     */
    function revealTransition() {
        return new Promise(resolve => {
            const tl = gsap.timeline({ 
                onComplete: () => {
                    // Hide completely after animating to ensure no click-blocking artifacts
                    gsap.set(".block", { visibility: "hidden" });
                    resolve();
                }
            });
            
            // Top row collapses upward
            tl.to(".row-1 .block", {
                scaleY: 0,
                duration: 1,
                stagger: { each: 0.1, from: "center" },
                ease: "expo.inOut"
            }, 0)
            // Bottom row collapses downward
            .to(".row-2 .block", {
                scaleY: 0,
                duration: 1,
                stagger: { each: 0.1, from: "center" },
                ease: "expo.inOut"
            }, 0);
        });
    }

    /**
     * Plays the closing animation (Shutters covering the screen)
     */
    function animateTransition() {
        return new Promise(resolve => {
            gsap.set(".block", { visibility: "visible", scaleY: 0 });
            const tl = gsap.timeline({ onComplete: resolve });
            
            // Top row drops down, right to left
            tl.to(".row-1 .block", {
                scaleY: 1,
                duration: 1,
                stagger: { each: 0.1, from: "end" },
                ease: "expo.inOut"
            }, 0)
            // Bottom row grows up, left to right
            .to(".row-2 .block", {
                scaleY: 1,
                duration: 1,
                stagger: { each: 0.1, from: "start" },
                ease: "expo.inOut"
            }, 0);
        });
    }

    // Mockup Routing Logic
    let isAnimating = false;
    const links = document.querySelectorAll(".nav-items a");
    const title = document.querySelector(".title");

    links.forEach(link => {
        link.addEventListener("click", async (e) => {
            e.preventDefault();
            
            // Prevent multiple rapid clicks
            if (isAnimating) return;
            
            const targetText = e.target.textContent;
            
            // Do nothing if we are already on that "page"
            if (title.textContent.toUpperCase() === targetText.toUpperCase()) return;

            isAnimating = true;

            // 1. Play closing shutters
            await animateTransition();
            
            // 2. Load "New Page" content (Mocked via DOM manipulation)
            title.textContent = targetText.toUpperCase();
            
            // 3. Play opening shutters
            await revealTransition();
            
            isAnimating = false;
        });
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
