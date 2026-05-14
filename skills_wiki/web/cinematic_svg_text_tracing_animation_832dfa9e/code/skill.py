def create_component(
    output_dir: str,
    title_text: str = "Lundev",
    body_text: str = "Experience the cinematic text tracing effect.",
    color_scheme: str = "dark",
    accent_color: str = "#00bfff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Cinematic SVG Text Tracing Animation.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#080c14"
        bg_gradient = "radial-gradient(circle at center, #1a233a 0%, #080c14 100%)"
        text_color = "#f0f0f0"
        body_color = "rgba(255, 255, 255, 0.7)"
    else:
        bg_color = "#f0f4f8"
        bg_gradient = "radial-gradient(circle at center, #ffffff 0%, #e1e5eb 100%)"
        text_color = "#111827"
        body_color = "rgba(17, 24, 39, 0.7)"

    # === CSS ===
    css = f"""/* Cinematic SVG Text Tracing Animation */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --bg-gradient: {bg_gradient};
    --text-color: {text_color};
    --body-color: {body_color};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Cinzel', 'Inter', system-ui, sans-serif;
    background: var(--bg-color);
    background-image: var(--bg-gradient);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.container {{
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    text-align: center;
}}

/* SVG Container Styling */
.svg-title-container {{
    width: 100%;
    max-width: 800px; /* Constrain width for optimal reading */
    height: 150px;
    margin-bottom: 2rem;
    display: flex;
    justify-content: center;
    align-items: center;
}}

/* The Core Text Animation Pattern */
.animated-text {{
    font-size: 85px; /* Sized relative to viewBox */
    font-weight: 700;
    letter-spacing: 5px;
    
    /* Crucial CSS for the effect */
    fill: transparent;
    stroke: var(--accent);
    stroke-width: 1.5px;
    
    /* 
       Dasharray must be larger than the longest character perimeter.
       1500px safely covers massive fonts. 
    */
    stroke-dasharray: 1500;
    stroke-dashoffset: 1500;
    
    /* Trigger the animation */
    animation: textTrace 4s cubic-bezier(0.4, 0.0, 0.2, 1) 1 forwards;
}}

@keyframes textTrace {{
    0% {{
        stroke-dashoffset: 1500;
        fill: transparent;
    }}
    80% {{
        stroke-dashoffset: 0;
        fill: transparent; /* Keep transparent until drawing finishes */
    }}
    100% {{
        stroke-dashoffset: 0;
        fill: var(--text-color);
    }}
}}

/* Support Elements */
.body-text {{
    font-family: 'Inter', system-ui, sans-serif;
    font-size: 1.25rem;
    color: var(--body-color);
    opacity: 0;
    transform: translateY(20px);
    /* Fade in after the title completes its drawing phase */
    animation: fadeUpReveal 1.5s ease-out 3.5s forwards;
}}

@keyframes fadeUpReveal {{
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

/* Responsive Scaling */
@media (max-width: 768px) {{
    .svg-title-container {{
        height: 100px;
    }}
    .animated-text {{
        font-size: 60px;
    }}
    .body-text {{
        font-size: 1rem;
    }}
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
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <!-- Cinzel provides a cinematic display font reminiscent of the video's elegant aesthetic -->
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Inter:wght@300;400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        
        <!-- SVG Canvas for the Tracing Effect -->
        <div class="svg-title-container">
            <!-- viewBox handles natural scaling -->
            <svg width="100%" height="100%" viewBox="0 0 800 150" preserveAspectRatio="xMidYMid meet">
                <!-- 
                     x="50%" y="50%" and text-anchor center ensures the text 
                     stays perfectly centered regardless of length 
                -->
                <text 
                    x="50%" 
                    y="55%" 
                    text-anchor="middle" 
                    dominant-baseline="middle" 
                    class="animated-text">
                    {title_text}
                </text>
            </svg>
        </div>

        <p class="body-text">{body_text}</p>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    # JS is used minimally here to offer dynamic recalculation of dasharray if text is exceptionally long, 
    # but the core CSS handles it out of the box. Added observer to replay animation on load robustly.
    js = f"""// Cinematic SVG Text Tracing Animation
document.addEventListener('DOMContentLoaded', () => {{
    const animatedText = document.querySelector('.animated-text');
    
    // Optional: Dynamic fallback to guarantee the dash array handles extremely large text 
    // without manual CSS tuning. By checking the computed text length, we can mathematically
    // ensure the stroke offset entirely covers the glyphs.
    if (animatedText) {{
        // getComputedTextLength returns width, multiplying it ensures we cover the perimeter
        const approxPerimeter = animatedText.getComputedTextLength() * 3; 
        
        // Only override if the text is abnormally huge compared to our CSS default (1500)
        if (approxPerimeter > 1500) {{
            animatedText.style.strokeDasharray = approxPerimeter;
            animatedText.style.strokeDashoffset = approxPerimeter;
            
            // Inject dynamic keyframes to use the new offset
            const styleSheet = document.styleSheets[0];
            const dynamicKeyframes = `
                @keyframes textTraceDynamic {{
                    0% {{ stroke-dashoffset: ${{approxPerimeter}}; fill: transparent; }}
                    80% {{ stroke-dashoffset: 0; fill: transparent; }}
                    100% {{ stroke-dashoffset: 0; fill: var(--text-color); }}
                }}
            `;
            styleSheet.insertRule(dynamicKeyframes, styleSheet.cssRules.length);
            animatedText.style.animation = 'textTraceDynamic 4s cubic-bezier(0.4, 0.0, 0.2, 1) 1 forwards';
        }}
    }}
}});
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
