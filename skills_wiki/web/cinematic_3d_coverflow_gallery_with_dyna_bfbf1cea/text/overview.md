# Cinematic 3D Coverflow Gallery with Dynamic Displacement

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Cinematic 3D Coverflow Gallery with Dynamic Displacement

* **Core Visual Mechanism**: A horizontally scrolling track of image cards positioned in a 3D perspective space. As the user scrolls, the cards rotate dynamically to face the center, creating a cylindrical coverflow effect. When a card is clicked, it undergoes a smooth, spring-like scaling expansion while dynamically displacing all sibling cards outward to create a focused "stage" for the active content. The environment is grounded by a subtle floor reflection.
* **Why Use This Skill (Rationale)**: This pattern transforms a standard image list into an immersive, tactile experience. The smooth mathematical interpolation (`lerp`/damping) applied to scale, position, and rotation provides a premium, "heavy" physical feel. The dynamic sibling displacement solves the common UI problem of expanding elements overlapping their neighbors, doing so in a highly cinematic way.
* **Overall Applicability**: Ideal for photography portfolios, case study showcases, premium e-commerce product carousels, or any application where visual media is the primary focus and deserves a "gallery-like" presentation. 
* **Value Addition**: Compared to standard CSS scroll-snapping, this JS-driven approach allows for decoupled interaction states (scaling up while scrolling) and complex relationship mapping (pushing neighbors away based on a central active index). It bridges the gap between 2D web layout and 3D application design.
* **Browser Compatibility**: Requires modern browsers supporting ES6 JavaScript, CSS `transform-style: preserve-3d`, `perspective`, and `-webkit-box-reflect` (Chrome/Safari/Edge for reflections, degrades gracefully without them).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**: Deep atmospheric background (`#0d111c` fading to `#2a2a35`), stark white/light grey frames for the images to emulate physical photo paper, and an accent color (e.g., vibrant orange or cyan) for the focus border and active typography.
  - **Typography**: Clean sans-serif (Inter) overlaid as a fixed UI element rather than inside the scaling cards to prevent rendering artifacts.
  - **CSS Enhancements**: Images feature a default grayscale/high-contrast filter that transitions to full color on focus. A `-webkit-box-reflect` applies a faded mirror effect below the cards to anchor them in space.

* **Step B: Layout & Compositional Style**
  - **Virtual Grid**: The elements are absolutely positioned with `left: 50%` and `margin-left` offset to precisely control their center-points.
  - **Spatial Feel**: Cards have a base width of ~320px and a tight gap to encourage overlap during the 3D rotation. When focused, the card scales up by ~1.7x, and an extra ~80px of breathing room is dynamically injected into the gaps.

* **Step C: Interactive Behavior & Animations**
  - **Virtual Scrolling**: Native scrolling is decoupled. Wheel events and mouse drags accumulate into a `targetScrollX` variable.
  - **Continuous Interpolation**: A `requestAnimationFrame` loop constantly interpolates (`lerp`) current values towards target values for Position X, Z-index depth, Scale, and Y-Rotation.
  - **Dynamic Displacement Logic**: When an index is selected, the loop calculates a push distance based on the active scale multiplier and applies `-pushDist` to all items with a lower index, and `+pushDist` to all items with a higher index.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Smooth Movement & Scaling** | JS `requestAnimationFrame` + `lerp` | Provides the "damped spring" physics mentioned in the tutorial, allowing fluid interruption of animations. |
| **Sibling Displacement** | JS state index calculation | CSS cannot easily push distant siblings outward dynamically based on a clicked index. |
| **3D Coverflow Curve** | CSS `rotateY` driven by JS | Maps the element's distance from the screen center to a rotation angle, simulating a 3D curved track without needing WebGL/Three.js. |
| **Floor Reflection** | CSS `-webkit-box-reflect` | A single line of CSS achieves a realistic floor mirror effect without duplicating DOM nodes or using canvas. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Cinematic Gallery",
    body_text: str = "Scroll or drag to explore. Click an image to focus.",
    color_scheme: str = "dark",
    accent_color: str = "#ff5500",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Cinematic 3D Coverflow Gallery.
    """
    import os
    import json

    os.makedirs(output_dir, exist_ok=True)

    # Theme colors
    if color_scheme == "dark":
        bg_color_center = "#2a2a35"
        bg_color_edge = "#0d111c"
        text_color = "#f0f0f0"
        card_bg = "#ffffff"
    else:
        bg_color_center = "#ffffff"
        bg_color_edge = "#e0e5ec"
        text_color = "#1a1a2e"
        card_bg = "#ffffff"

    # Helper for transparent accent
    def hex_to_rgba(hex_code, alpha):
        h = hex_code.lstrip('#')
        if len(h) == 3: h = ''.join(c + c for c in h)
        r, g, b = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
        return f"rgba({r}, {g}, {b}, {alpha})"

    accent_transparent = hex_to_rgba(accent_color, 0.4)

    # Gallery Data
    images_data = [
        {"title": "Neon Echoes", "desc": "Cyberpunk aesthetics in modern Tokyo.", "url": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"},
        {"title": "Concrete Brutalism", "desc": "Raw structural forms and shadows.", "url": "https://images.unsplash.com/photo-1513694203232-719a280e022f?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"},
        {"title": "Minimal Horizons", "desc": "Clean lines against open skies.", "url": "https://images.unsplash.com/photo-1505843513577-22bb7d21e455?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"},
        {"title": "Glass Canyons", "desc": "Reflections in the corporate district.", "url": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"},
        {"title": "Abstract Geometry", "desc": "Finding patterns in architecture.", "url": "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"},
        {"title": "Urban Monoliths", "desc": "The weight of the modern city.", "url": "https://images.unsplash.com/photo-1497366216548-37526070297c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"},
        {"title": "Twilight Grid", "desc": "When the city lights begin to glow.", "url": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"}
    ]

    items_html = ""
    for i, item in enumerate(images_data):
        items_html += f"""
            <div class="gallery-item" data-index="{i}">
                <div class="gallery-item-inner">
                    <img src="{item['url']}" alt="{item['title']}">
                </div>
            </div>
        """

    # === CSS ===
    css = f"""/* Cinematic 3D Coverflow Gallery */
:root {{
    --bg-center: {bg_color_center};
    --bg-edge: {bg_color_edge};
    --text: {text_color};
    --accent: {accent_color};
    --accent-trans: {accent_transparent};
    --card-bg: {card_bg};
    --width: {width_px}px;
    --height: {height_px}px;
}}

* {{ margin: 0; padding: 0; box-sizing: border-box; }}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: radial-gradient(circle at 50% 30%, var(--bg-center) 0%, var(--bg-edge) 100%);
    color: var(--text);
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    user-select: none;
}}

.app-wrapper {{
    width: var(--width);
    height: var(--height);
    position: relative;
    overflow: hidden;
    border-radius: 12px;
    box-shadow: 0 40px 100px rgba(0,0,0,0.5);
}}

/* UI Overlay */
.ui-overlay {{
    position: absolute;
    bottom: 50px;
    left: 60px;
    z-index: 1000;
    pointer-events: none;
}}
.ui-title {{
    font-size: 3rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    margin-bottom: 8px;
    transition: color 0.4s ease;
}}
.ui-desc {{
    font-size: 1.1rem;
    font-weight: 300;
    opacity: 0.7;
}}

/* Gallery Infrastructure */
.gallery-container {{
    position: absolute;
    inset: 0;
    cursor: grab;
    perspective: 1500px;
}}
.gallery-container:active {{ cursor: grabbing; }}

.gallery-track {{
    position: absolute;
    top: 50%;
    left: 50%; /* Origin is exactly center screen */
    width: 0;
    height: 0;
    transform-style: preserve-3d;
}}

/* Gallery Items */
.gallery-item {{
    position: absolute;
    top: -200px; /* Half of height */
    left: 0;
    margin-left: -150px; /* Half of width to perfectly center */
    width: 300px;
    height: 400px;
    background: var(--card-bg);
    padding: 10px;
    box-shadow: 0 15px 35px rgba(0,0,0,0.3);
    will-change: transform;
    cursor: pointer;
    border: 2px solid transparent;
    transition: border-color 0.4s ease, box-shadow 0.4s ease;
    transform-style: preserve-3d;
    -webkit-box-reflect: below 8px linear-gradient(to bottom, rgba(0,0,0,0) 60%, rgba(0,0,0,0.3) 100%);
}}

.gallery-item:hover {{
    border-color: rgba(255, 255, 255, 0.3);
}}

.gallery-item.is-selected {{
    border-color: var(--accent);
    box-shadow: 0 40px 80px rgba(0,0,0,0.6), 0 0 50px var(--accent-trans);
}}

.gallery-item-inner {{
    width: 100%;
    height: 100%;
    overflow: hidden;
    background: #000;
}}

.gallery-item img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    pointer-events: none;
    transition: filter 0.6s ease, transform 0.6s ease;
    filter: grayscale(60%) contrast(120%) brightness(0.8);
    transform: scale(1.05); /* Slight zoom out room */
}}

.gallery-item.is-selected img {{
    filter: grayscale(0%) contrast(100%) brightness(1);
    transform: scale(1);
}}

/* Decorative close hint */
.close-hint {{
    position: absolute;
    top: 40px;
    right: 40px;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: rgba(255,255,255,0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.3s ease;
    z-index: 1000;
    backdrop-filter: blur(4px);
}}
.close-hint::before, .close-hint::after {{
    content: '';
    position: absolute;
    width: 16px;
    height: 2px;
    background: #fff;
}}
.close-hint::before {{ transform: rotate(45deg); }}
.close-hint::after {{ transform: rotate(-45deg); }}
.has-selection .close-hint {{ opacity: 1; pointer-events: auto; }}
.close-hint:hover {{ background: var(--accent); }}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-wrapper">
        <div class="ui-overlay">
            <h1 class="ui-title" id="ui-title">{title_text}</h1>
            <p class="ui-desc" id="ui-desc">{body_text}</p>
        </div>
        
        <div class="close-hint" id="close-btn"></div>

        <div class="gallery-container" id="container">
            <div class="gallery-track" id="track">
                {items_html}
            </div>
        </div>
    </div>

    <script>
        const galleryData = {json.dumps(images_data)};
        const defaultTitle = "{title_text}";
        const defaultDesc = "{body_text}";
    </script>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""document.addEventListener('DOMContentLoaded', () => {{
    const container = document.getElementById('container');
    const items = Array.from(document.querySelectorAll('.gallery-item'));
    const uiTitle = document.getElementById('ui-title');
    const uiDesc = document.getElementById('ui-desc');
    const closeBtn = document.getElementById('close-btn');
    const appWrapper = document.querySelector('.app-wrapper');

    // Layout configuration
    const itemWidth = 300;
    const gap = 30;
    const scaleActive = 1.7;
    const scaleInactive = 0.85;
    const extraPush = 80; // Distance to push siblings away
    const lerpSpeed = 0.07;
    
    let scrollX = 0;
    let targetScrollX = 0;
    let selectedIndex = -1;

    // Initialize state objects for interpolation
    const itemState = items.map((el, i) => ({{
        el,
        baseX: i * (itemWidth + gap),
        currentX: i * (itemWidth + gap),
        currentScale: 1,
        currentRotation: 0,
        currentZ: 0
    }}));

    const maxScroll = itemState[itemState.length - 1].baseX;

    // --- Interaction Logic ---
    let isDragging = false;
    let startX = 0;
    let startScrollX = 0;
    let dragged = false;

    container.addEventListener('mousedown', (e) => {{
        isDragging = true;
        dragged = false;
        startX = e.clientX;
        startScrollX = targetScrollX;
    }});

    window.addEventListener('mousemove', (e) => {{
        if (!isDragging) return;
        const delta = startX - e.clientX;
        if (Math.abs(delta) > 5) dragged = true; // threshold to differentiate click vs drag
        targetScrollX = startScrollX + delta * 1.5;
    }});

    window.addEventListener('mouseup', () => {{
        isDragging = false;
    }});

    // Trackpad / Mouse wheel support
    container.addEventListener('wheel', (e) => {{
        targetScrollX += (e.deltaY + e.deltaX) * 0.8;
    }}, {{ passive: true }});

    // Handle Clicks
    items.forEach((item, i) => {{
        item.el.addEventListener('click', (e) => {{
            e.stopPropagation(); // Prevent container click
            if (dragged) return; // Don't trigger if user was panning

            if (selectedIndex === i) {{
                deselect();
            }} else {{
                selectedIndex = i;
                targetScrollX = itemState[i].baseX; // Center the item
                updateUI();
            }}
        }});
    }});

    // Click background to deselect
    container.addEventListener('click', (e) => {{
        if (e.target === container || e.target.classList.contains('gallery-track')) {{
            if (!dragged) deselect();
        }}
    }});

    closeBtn.addEventListener('click', deselect);

    function deselect() {{
        selectedIndex = -1;
        updateUI();
    }}

    function updateUI() {{
        items.forEach((el, j) => {{
            if (j === selectedIndex) el.el.classList.add('is-selected');
            else el.el.classList.remove('is-selected');
        }});

        if (selectedIndex === -1) {{
            uiTitle.textContent = defaultTitle;
            uiDesc.textContent = defaultDesc;
            uiTitle.style.color = "var(--text)";
            appWrapper.classList.remove('has-selection');
        }} else {{
            const data = galleryData[selectedIndex];
            uiTitle.textContent = data.title;
            uiDesc.textContent = data.desc;
            uiTitle.style.color = "var(--accent)";
            appWrapper.classList.add('has-selection');
        }}
    }}

    // --- Animation Loop ---
    function lerp(start, end, t) {{
        return start * (1 - t) + end * t;
    }}

    function animate() {{
        // Elastic bounds clamping when not dragging
        if (!isDragging && selectedIndex === -1) {{
            if (targetScrollX < 0) targetScrollX = lerp(targetScrollX, 0, 0.1);
            if (targetScrollX > maxScroll) targetScrollX = lerp(targetScrollX, maxScroll, 0.1);
        }}

        scrollX = lerp(scrollX, targetScrollX, lerpSpeed);

        itemState.forEach((item, i) => {{
            let targetScale = 1;
            let displacement = 0;
            let targetZ = 0;

            if (selectedIndex !== -1) {{
                if (i === selectedIndex) {{
                    targetScale = scaleActive;
                    targetZ = 50; // Pop forward
                }} else {{
                    targetScale = scaleInactive;
                    // Calculate exact distance required to clear the expanded item plus extra padding
                    const pushDist = (itemWidth * scaleActive)/2 + (itemWidth * scaleInactive)/2 - itemWidth + extraPush;
                    if (i < selectedIndex) displacement = -pushDist;
                    if (i > selectedIndex) displacement = pushDist;
                    targetZ = -50; // Push inactive slightly back
                }}
            }}

            const targetX = item.baseX + displacement - scrollX;
            
            // Calculate 3D rotation based on distance from center (simulates curved cylinder)
            const maxRotation = 25;
            let targetRotation = selectedIndex === -1 ? targetX * 0.03 : (selectedIndex === i ? 0 : targetX * 0.015);
            targetRotation = Math.max(-maxRotation, Math.min(maxRotation, targetRotation));

            // Interpolate values
            item.currentX = lerp(item.currentX, targetX, lerpSpeed);
            item.currentScale = lerp(item.currentScale, targetScale, lerpSpeed);
            item.currentRotation = lerp(item.currentRotation, targetRotation, lerpSpeed);
            item.currentZ = lerp(item.currentZ, targetZ, lerpSpeed);

            // Apply transforms
            item.el.style.transform = `
                translate3d(${{item.currentX}}px, 0, ${{item.currentZ}}px) 
                scale(${{item.currentScale}}) 
                rotateY(${{item.currentRotation}}deg)
            `;
        }});

        requestAnimationFrame(animate);
    }}

    // Start loop
    animate();
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