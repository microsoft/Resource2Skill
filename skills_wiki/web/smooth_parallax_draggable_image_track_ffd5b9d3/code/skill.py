def create_component(
    output_dir: str,
    title_text: str = "Drag to Explore",
    body_text: str = "Interactive parallax image track",
    color_scheme: str = "dark",
    accent_color: str = "#ffffff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Parallax Draggable Image Track visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#0a0a0a"
        text_color = "#ffffff"
        hint_color = "rgba(255, 255, 255, 0.5)"
    else:
        bg_color = "#f4f4f5"
        text_color = "#18181b"
        hint_color = "rgba(0, 0, 0, 0.5)"

    css = f"""/* Smooth Parallax Draggable Image Track */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --hint: {hint_color};
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
    /* Prevent pull-to-refresh on mobile */
    overscroll-behavior-y: none; 
}}

.app-wrapper {{
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    position: relative;
    overflow: hidden;
    background: var(--bg);
    box-shadow: 0 0 0 1px rgba(128,128,128,0.1);
}}

.header {{
    position: absolute;
    top: 40px;
    left: 40px;
    z-index: 10;
    pointer-events: none;
}}

.title {{
    font-size: 2rem;
    font-weight: 500;
    letter-spacing: -0.02em;
    margin-bottom: 8px;
}}

.body-text {{
    font-size: 1rem;
    color: var(--hint);
    font-weight: 400;
}}

#image-track {{
    display: flex;
    gap: 4vmin;
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(0%, -50%);
    /* Prevent text/image selection during drag */
    user-select: none;
    -webkit-user-select: none;
    touch-action: pan-y;
}}

.image {{
    width: 40vmin;
    height: 56vmin;
    min-width: 250px;
    min-height: 350px;
    object-fit: cover;
    object-position: 100% 50%;
    border-radius: 8px;
    pointer-events: none; /* Let the track handle drag events */
    box-shadow: 0 20px 40px rgba(0,0,0,0.3);
}}

/* Interactive cursor states */
.app-wrapper:active #image-track {{
    cursor: grabbing;
}}

#image-track {{
    cursor: grab;
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-wrapper" id="wrapper">
        <div class="header">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
        
        <div id="image-track" data-mouse-down-at="0" data-prev-percentage="0">
            <img class="image" src="https://images.unsplash.com/photo-1524781289445-e18c36281b31?q=80&w=1000&auto=format&fit=crop" draggable="false" alt="Gallery image 1" />
            <img class="image" src="https://images.unsplash.com/photo-1610194352361-4c81a6a8967e?q=80&w=1000&auto=format&fit=crop" draggable="false" alt="Gallery image 2" />
            <img class="image" src="https://images.unsplash.com/photo-1618202133208-280718d7bd3e?q=80&w=1000&auto=format&fit=crop" draggable="false" alt="Gallery image 3" />
            <img class="image" src="https://images.unsplash.com/photo-1495805442109-8b2138f6c41b?q=80&w=1000&auto=format&fit=crop" draggable="false" alt="Gallery image 4" />
            <img class="image" src="https://images.unsplash.com/photo-1548021682-27208e9e0e20?q=80&w=1000&auto=format&fit=crop" draggable="false" alt="Gallery image 5" />
            <img class="image" src="https://images.unsplash.com/photo-1496753480864-3e588e0269b3?q=80&w=1000&auto=format&fit=crop" draggable="false" alt="Gallery image 6" />
            <img class="image" src="https://images.unsplash.com/photo-1613346945084-35cccc812dd5?q=80&w=1000&auto=format&fit=crop" draggable="false" alt="Gallery image 7" />
            <img class="image" src="https://images.unsplash.com/photo-1516681100942-77d8e7f9dd97?q=80&w=1000&auto=format&fit=crop" draggable="false" alt="Gallery image 8" />
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""document.addEventListener('DOMContentLoaded', () => {{
    const track = document.getElementById("image-track");
    const wrapper = document.getElementById("wrapper");

    const handleOnDown = e => {{
        // Unified coordinate extraction for mouse and touch
        const clientX = e.type.includes('mouse') ? e.clientX : e.touches[0].clientX;
        track.dataset.mouseDownAt = clientX;
    }};

    const handleOnUp = () => {{
        track.dataset.mouseDownAt = "0";
        track.dataset.prevPercentage = track.dataset.percentage || "0";
    }};

    const handleOnMove = e => {{
        if(track.dataset.mouseDownAt === "0") return;

        const clientX = e.type.includes('mouse') ? e.clientX : e.touches[0].clientX;
        const mouseDelta = parseFloat(track.dataset.mouseDownAt) - clientX;
        
        // The distance required to slide the entire track (half the container width)
        const maxDelta = wrapper.clientWidth / 2;
        
        const percentage = (mouseDelta / maxDelta) * -100;
        const nextPercentageUnconstrained = parseFloat(track.dataset.prevPercentage) + percentage;
        
        // Clamp between 0% and -100%
        const nextPercentage = Math.max(Math.min(nextPercentageUnconstrained, 0), -100);
        
        track.dataset.percentage = nextPercentage;
        
        // Animate the track container moving horizontally
        track.animate({{
            transform: `translate(${{nextPercentage}}%, -50%)`
        }}, {{ duration: 1200, fill: "forwards" }});
        
        // Animate the object-position of each image for the counter-parallax effect
        for(const image of track.getElementsByClassName("image")) {{
            image.animate({{
                objectPosition: `${{100 + nextPercentage}}% center`
            }}, {{ duration: 1200, fill: "forwards" }});
        }}
    }};

    // Mouse Events
    wrapper.addEventListener("mousedown", handleOnDown);
    window.addEventListener("mouseup", handleOnUp);
    window.addEventListener("mousemove", handleOnMove);

    // Touch Events (mobile support)
    wrapper.addEventListener("touchstart", handleOnDown, {{ passive: true }});
    window.addEventListener("touchend", handleOnUp);
    window.addEventListener("touchmove", handleOnMove, {{ passive: true }});
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
