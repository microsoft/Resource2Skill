def create_component(
    output_dir: str,
    title_text: str = "Timeline Nesting Choreography",
    body_text: str = "Click 'Play Sequence' to observe modular GSAP timelines reacting with overlaps, delays, and yoyo effects.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1000,
    height_px: int = 700,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the modular GSAP timeline choreography.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
        box_bg = "#f4f4f5"
        box_text = "#0d111c"
        grid_color = "rgba(255, 255, 255, 0.05)"
        panel_bg = "rgba(255, 255, 255, 0.03)"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        box_bg = "#1a1a2e"
        box_text = "#ffffff"
        grid_color = "rgba(0, 0, 0, 0.05)"
        panel_bg = "rgba(0, 0, 0, 0.03)"

    # === CSS ===
    css = f"""/* GSAP Nested Timeline — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --box-bg: {box_bg};
    --box-text: {box_text};
    --grid: {grid_color};
    --panel-bg: {panel_bg};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    /* Grid Background Pattern */
    background-image: 
        linear-gradient(var(--grid) 1px, transparent 1px),
        linear-gradient(90deg, var(--grid) 1px, transparent 1px);
    background-size: 40px 40px;
    background-position: center center;
}}

.app-container {{
    width: var(--width);
    height: var(--height);
    background: var(--panel-bg);
    backdrop-filter: blur(8px);
    border: 1px solid var(--grid);
    border-radius: 16px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    box-shadow: 0 24px 48px rgba(0,0,0,0.2);
}}

.header {{
    padding: 32px;
    border-bottom: 1px solid var(--grid);
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.header-text h1 {{
    font-size: 24px;
    font-weight: 600;
    margin-bottom: 8px;
}}

.header-text p {{
    font-size: 14px;
    opacity: 0.7;
    max-width: 600px;
}}

.controls button {{
    background: var(--accent);
    color: #fff;
    border: none;
    padding: 12px 24px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.2s ease, opacity 0.2s ease;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}}

.controls button:hover {{
    transform: translateY(-2px);
    opacity: 0.9;
}}

.controls button:active {{
    transform: translateY(0);
}}

.canvas {{
    flex: 1;
    padding: 64px;
    display: flex;
    flex-direction: column;
    gap: 32px;
    position: relative;
}}

.box {{
    width: 80px;
    height: 80px;
    background: var(--box-bg);
    color: var(--box-text);
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 32px;
    font-weight: 700;
    box-shadow: 0 8px 24px rgba(0,0,0,0.1);
    /* GSAP will animate transform */
    will-change: transform;
}}

/* Toast notification for completion */
.toast {{
    position: absolute;
    bottom: 32px;
    left: 50%;
    transform: translateX(-50%) translateY(20px);
    background: var(--text);
    color: var(--bg);
    padding: 12px 24px;
    border-radius: 30px;
    font-size: 14px;
    font-weight: 600;
    opacity: 0;
    pointer-events: none;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}}

.toast.show {{
    opacity: 1;
    transform: translateX(-50%) translateY(0);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-container">
        <div class="header">
            <div class="header-text">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
            </div>
            <div class="controls">
                <button id="play-btn">Play Sequence</button>
            </div>
        </div>
        
        <div class="canvas">
            <div class="box box-a">A</div>
            <div class="box box-b">B</div>
            <div class="box box-c">C</div>
            
            <div id="toast" class="toast">Animation Sequence Complete!</div>
        </div>
    </div>

    <!-- Load GSAP -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Modular GSAP Timeline Choreography

document.addEventListener('DOMContentLoaded', () => {
    
    // 1. Define modular timelines inside functions to keep them reusable
    
    function firstTimeline() {
        const tl = gsap.timeline({ defaults: { duration: 1, ease: "power1.inOut" } });
        // Box A rotates 180deg and moves right 300px
        tl.to(".box-a", { rotation: 180, x: 300 })
        // Then smoothly returns to origin
          .to(".box-a", { rotation: 0, x: 0 });
        return tl;
    }

    function secondTimeline() {
        const tl = gsap.timeline({ defaults: { duration: 1, ease: "power1.inOut" } });
        // Box B rotates inversely (-180deg) and moves right 300px
        tl.to(".box-b", { rotation: -180, x: 300 })
          .to(".box-b", { rotation: 0, x: 0 });
        return tl;
    }

    function thirdTimeline() {
        const tl = gsap.timeline({ defaults: { duration: 1, ease: "power1.inOut" } });
        // Box C mimics Box A
        tl.to(".box-c", { rotation: 180, x: 300 })
          .to(".box-c", { rotation: 0, x: 0 });
        return tl;
    }

    // Custom notification function instead of a blocking browser alert()
    function notifyComplete() {
        const toast = document.getElementById('toast');
        toast.classList.add('show');
        setTimeout(() => {
            toast.classList.remove('show');
        }, 2000);
    }

    // 2. Create the Master Timeline
    const mainTimeline = gsap.timeline({ 
        paused: true,          // Do not start until commanded
        repeat: 2,             // Play a total of 3 times (1 initial + 2 repeats)
        repeatDelay: 1,        // Pause for 1 second between loops
        yoyo: true,            // Play backwards on every other cycle
        onComplete: () => {
            notifyComplete();
            document.getElementById('play-btn').textContent = "Replay Sequence";
            document.getElementById('play-btn').disabled = false;
        }
    });

    // 3. Choreograph the modules using Timeline additions and position parameters
    mainTimeline
        .add(firstTimeline())
        // Start second timeline exactly 2 seconds AFTER the first timeline completes
        .add(secondTimeline(), "+=2")
        // Start third timeline exactly 1 second BEFORE the second timeline completes
        .add(thirdTimeline(), "-=1");

    // 4. Interactive Control
    const playBtn = document.getElementById('play-btn');
    
    playBtn.addEventListener('click', () => {
        // Prevent clicking while animating
        if (mainTimeline.isActive()) return;
        
        playBtn.disabled = true;
        playBtn.textContent = "Playing...";
        
        // Restart forces the animation from 0, useful for replays
        mainTimeline.restart();
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
