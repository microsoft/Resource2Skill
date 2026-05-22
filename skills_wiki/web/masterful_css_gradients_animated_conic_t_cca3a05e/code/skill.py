def create_component(
    output_dir: str,
    title_text: str = "Mastering CSS Gradients",
    body_text: str = "Discover the power of linear, radial, and conic gradients to build stunning, lightweight UI components.",
    color_scheme: str = "dark",
    accent_color: str = "#ff007f",
    width_px: int = 1200,
    height_px: int = 900,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing various CSS Gradient techniques.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme definitions
    if color_scheme == "dark":
        bg_color = "#0a0a0f"
        card_bg = "#15151e"
        text_primary = "#ffffff"
        text_secondary = "#a0a0b0"
    else:
        bg_color = "#f4f4f9"
        card_bg = "#ffffff"
        text_primary = "#111118"
        text_secondary = "#555566"

    # HTML Content
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Space+Grotesk:wght@700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="animated-bg"></div>
    
    <div class="container">
        <header class="header">
            <h1 class="gradient-text">{title_text}</h1>
            <p class="subtitle">{body_text}</p>
        </header>

        <div class="grid">
            <!-- 1. Linear & Repeating -->
            <div class="card">
                <h3>Linear & Repeating</h3>
                <div class="demo-box repeating-linear"></div>
            </div>

            <!-- 2. Radial Gradient -->
            <div class="card">
                <h3>Radial Gradient</h3>
                <div class="demo-box radial-box"></div>
            </div>

            <!-- 3. Conic Gradient -->
            <div class="card">
                <h3>Conic Gradient</h3>
                <div class="demo-box conic-box"></div>
            </div>

            <!-- 4. Gradient Image Overlay -->
            <div class="card">
                <h3>Gradient Overlay</h3>
                <div class="demo-box overlay-box">
                    <span class="overlay-text">Beautiful Contrast</span>
                </div>
            </div>
        </div>

        <div class="cta-section">
            <button class="gradient-border-btn">
                <span class="btn-content">Hover Me - Gradient Border</span>
            </button>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # CSS Content
    css = f"""/* CSS Gradients Showcase */
:root {{
    --bg-color: {bg_color};
    --card-bg: {card_bg};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --accent: {accent_color};
    --container-width: {width_px}px;
    --container-height: {height_px}px;
}}

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Inter', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    overflow-x: hidden;
}}

/* === 1. Animated Gradient Background === */
.animated-bg {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: -1;
    /* Large animated linear gradient */
    background: linear-gradient(-45deg, #ff007f, #7928ca, #0070f3, #00dfd8);
    background-size: 400% 400%;
    animation: gradientShift 15s ease infinite;
    opacity: 0.15; /* Kept subtle to not overpower the content */
}}

@keyframes gradientShift {{
    0% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}

/* Layout */
.container {{
    width: 100%;
    max-width: var(--container-width);
    padding: 40px;
    display: flex;
    flex-direction: column;
    gap: 48px;
}}

.header {{
    text-align: center;
}}

/* === 2. Gradient Text === */
.gradient-text {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 4.5rem;
    font-weight: 800;
    margin-bottom: 16px;
    
    /* The core gradient text trick */
    background: linear-gradient(to right, #00dfd8, #0070f3, #7928ca, #ff007f);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    
    /* Optional: Animate the text gradient too */
    background-size: 300% 300%;
    animation: gradientShift 8s ease infinite;
}}

.subtitle {{
    font-size: 1.25rem;
    color: var(--text-secondary);
    max-width: 600px;
    margin: 0 auto;
    line-height: 1.6;
}}

.grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 24px;
}}

.card {{
    background: var(--card-bg);
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    display: flex;
    flex-direction: column;
    gap: 16px;
}}

.card h3 {{
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 1px;
}}

.demo-box {{
    width: 100%;
    height: 180px;
    border-radius: 12px;
}}

/* === 3. Repeating Linear Gradient === */
.repeating-linear {{
    background: repeating-linear-gradient(
        45deg,
        #ff007f,
        #ff007f 10px,
        #7928ca 10px,
        #7928ca 20px
    );
}}

/* === 4. Radial Gradient === */
.radial-box {{
    background: radial-gradient(
        circle at top right,
        #00dfd8 0%,
        #0070f3 50%,
        #0a0a0f 100%
    );
}}

/* === 5. Conic Gradient === */
.conic-box {{
    background: conic-gradient(
        from 0deg at 50% 50%,
        #ff007f, #7928ca, #0070f3, #00dfd8, #ff007f
    );
}}

/* === 6. Gradient Overlay on Image === */
.overlay-box {{
    position: relative;
    display: flex;
    align-items: flex-end;
    padding: 20px;
    
    /* Chaining linear-gradient and url() */
    background: 
        linear-gradient(to top, rgba(0,0,0,0.9) 0%, rgba(0,0,0,0.1) 100%),
        url('https://picsum.photos/400/300?random=1');
    background-size: cover;
    background-position: center;
}}

.overlay-text {{
    color: #ffffff;
    font-weight: 600;
    font-size: 1.1rem;
}}

/* === 7. Gradient Border Button === */
.cta-section {{
    display: flex;
    justify-content: center;
    margin-top: 20px;
}}

.gradient-border-btn {{
    position: relative;
    appearance: none;
    background: var(--card-bg);
    border: none;
    border-radius: 50px; /* Highly rounded */
    padding: 20px 40px;
    cursor: pointer;
    z-index: 1; /* Keep text above pseudo-element */
    outline: none;
    transition: transform 0.2s ease;
}}

.btn-content {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--text-primary);
}}

/* The pseudo-element forms the gradient border */
.gradient-border-btn::after {{
    content: '';
    position: absolute;
    /* Extends outside the button by 3px to form a 3px border */
    inset: -3px; 
    z-index: -1; /* Pushes it behind the main button background */
    border-radius: inherit; /* Copies the 50px border radius perfectly */
    background: linear-gradient(to right, #ff007f, #00dfd8);
    background-size: 200% 200%;
    transition: filter 0.3s ease, background-position 0.3s ease;
}}

.gradient-border-btn:hover {{
    transform: translateY(-2px);
}}

.gradient-border-btn:hover::after {{
    /* Animate gradient position and add a glowing blur on hover */
    background-position: 100% 50%;
    filter: drop-shadow(0 0 15px rgba(255, 0, 127, 0.5));
}}
"""

    # JS Content
    js = f"""// CSS Gradients Interactive Behavior
document.addEventListener('DOMContentLoaded', () => {{
    // The core techniques are pure CSS. 
    // This script adds a subtle mouse-tracking rotation to the conic gradient
    // to demonstrate blending JS state with CSS variables for dynamic gradients.

    const conicBox = document.querySelector('.conic-box');
    
    if(conicBox) {{
        conicBox.addEventListener('mousemove', (e) => {{
            const rect = conicBox.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            
            // Calculate angle based on mouse position relative to center
            let angle = Math.atan2(y, x) * (180 / Math.PI) + 90;
            
            // Apply the dynamic angle via inline style
            conicBox.style.background = `conic-gradient(from ${{angle}}deg at 50% 50%, #ff007f, #7928ca, #0070f3, #00dfd8, #ff007f)`;
        }});

        // Reset on mouse leave
        conicBox.addEventListener('mouseleave', () => {{
            conicBox.style.background = ''; // Reverts to stylesheet default
        }});
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
