def create_component(
    output_dir: str,
    title_text: str = "Live Analog Clock",
    body_text: str = "Pure CSS animation synchronized to your local time.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#e63946",     # CSS hex color for accent (strap, sec hand)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Pure CSS Analog Clock visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#0f111a"
        text_color = "#f8f9fa"
        clock_bg = "#1e2233"
        clock_border = "#2a2f45"
        hand_color = "#ffffff"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        clock_bg = "#ffffff"
        clock_border = "#1a1a2e"
        hand_color = "#1a1a2e"

    # === CSS ===
    css = f"""/* Pure CSS Analog Clock — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --clock-bg: {clock_bg};
    --clock-border: {clock_border};
    --hand-color: {hand_color};
    --width: {width_px}px;
    --height: {height_px}px;
    
    /* Responsive clock sizing */
    --clock-size: 280px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.container {{
    width: var(--width);
    height: var(--height);
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
}}

.header {{
    margin-bottom: 80px;
    z-index: 10;
}}

.title {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 12px;
    letter-spacing: -0.02em;
}}

.body-text {{
    font-size: 1.1rem;
    opacity: 0.7;
    font-weight: 300;
}}

/* Clock Container */
.clock-wrapper {{
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
}}

/* Red Strap/Handle */
.clock-strap {{
    width: 60px;
    height: 120px;
    background-color: var(--accent);
    border-radius: 8px 8px 0 0;
    margin-bottom: -40px; /* Pulls clock face up over the strap */
    z-index: 1;
    box-shadow: inset 0 0 10px rgba(0,0,0,0.2);
}}

/* Clock Face */
.clock-face {{
    width: var(--clock-size);
    height: var(--clock-size);
    background-color: var(--clock-bg);
    border: 12px solid var(--clock-border);
    border-radius: 50%;
    position: relative;
    z-index: 2;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2), inset 0 0 20px rgba(0,0,0,0.05);
}}

/* Center Dot */
.center-dot {{
    width: 18px;
    height: 18px;
    background-color: var(--accent);
    border-radius: 50%;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 10;
    border: 3px solid var(--clock-bg);
    box-shadow: 0 2px 4px rgba(0,0,0,0.3);
}}

/* Base style for all hands */
.hand {{
    position: absolute;
    bottom: 50%;
    left: 50%;
    transform-origin: bottom center;
    border-radius: 10px 10px 0 0;
    /* Use margin-left to center horizontally to leave 'transform' free for rotation */
}}

/* Specific Hands */
.hour-hand {{
    width: 8px;
    height: 30%;
    background-color: var(--hand-color);
    margin-left: -4px;
    z-index: 5;
    animation: rotate 43200s linear infinite; /* 12 hours */
}}

.min-hand {{
    width: 6px;
    height: 40%;
    background-color: var(--hand-color);
    margin-left: -3px;
    z-index: 6;
    animation: rotate 3600s linear infinite; /* 60 minutes */
}}

.sec-hand {{
    width: 3px;
    height: 45%;
    background-color: var(--accent);
    margin-left: -1.5px;
    z-index: 7;
    animation: rotate 60s linear infinite; /* 60 seconds */
    /* Add a slight tail dropping below the center point */
    transform-origin: center calc(100% - 15px);
    bottom: calc(50% - 15px);
    height: calc(45% + 15px);
}}

/* Animation Keyframes */
@keyframes rotate {{
    100% {{ transform: rotate(360deg); }}
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>

        <div class="clock-wrapper">
            <div class="clock-strap"></div>
            <div class="clock-face" role="img" aria-label="Analog clock showing current time">
                <div class="center-dot"></div>
                <div class="hand hour-hand" id="hour"></div>
                <div class="hand min-hand" id="min"></div>
                <div class="hand sec-hand" id="sec"></div>
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Pure CSS Analog Clock — Real-time Synchronization
document.addEventListener('DOMContentLoaded', () => {{
    const secHand = document.getElementById('sec');
    const minHand = document.getElementById('min');
    const hourHand = document.getElementById('hour');

    function syncClock() {{
        const now = new Date();
        const seconds = now.getSeconds();
        const minutes = now.getMinutes();
        const hours = now.getHours();

        // We use a negative animation-delay. 
        // This tells the CSS animation to start as if it had already been running for X seconds.
        // It immediately snaps to the correct angle without needing JavaScript to update styles every frame.
        
        const secDelay = -seconds;
        const minDelay = -(minutes * 60 + seconds);
        const hourDelay = -((hours % 12) * 3600 + minutes * 60 + seconds);

        secHand.style.animationDelay = `${{secDelay}}s`;
        minHand.style.animationDelay = `${{minDelay}}s`;
        hourHand.style.animationDelay = `${{hourDelay}}s`;
    }}

    // Sync on load
    syncClock();
    
    // Optional: Resync when user returns to the tab to correct any browser background-throttling drift
    document.addEventListener("visibilitychange", () => {{
        if (!document.hidden) {{
            // Temporarily disable animation to reset cleanly
            secHand.style.animation = 'none';
            minHand.style.animation = 'none';
            hourHand.style.animation = 'none';
            
            // Trigger reflow
            void secHand.offsetWidth;
            
            // Re-enable and sync
            secHand.style.animation = '';
            minHand.style.animation = '';
            hourHand.style.animation = '';
            syncClock();
        }}
    }});
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
