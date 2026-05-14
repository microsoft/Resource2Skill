def create_component(
    output_dir: str,
    title_text: str = "Shape Shifter",
    body_text: str = "Click to morph the SVG path seamlessly.",
    color_scheme: str = "dark",
    accent_color: str = "#8DC540",
    width_px: int = 1000,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Elastic SVG Morphing effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme definitions
    if color_scheme == "dark":
        bg_color = "#121212"
        card_bg = "#1e1e1e"
        text_color = "#f5f5f5"
        text_muted = "#a0a0a0"
        stroke_color = "#E5285D"
        button_bg = "rgba(255,255,255,0.1)"
        button_hover = "rgba(255,255,255,0.2)"
    else:
        bg_color = "#e5e7eb"
        card_bg = "#ffffff"
        text_color = "#111827"
        text_muted = "#6b7280"
        stroke_color = "#d01040"
        button_bg = "rgba(0,0,0,0.05)"
        button_hover = "rgba(0,0,0,0.1)"

    # Pre-calculated paths with identical node counts (10 points + Z)
    # This prevents the need for JS interpolation libraries
    path_square = "M 50,15 L 85,15 L 85,50 L 85,85 L 67.5,85 L 50,85 L 15,85 L 15,50 L 15,15 L 32.5,15 Z"
    path_star = "M 50,5 L 61,35 L 95,35 L 67,55 L 78,85 L 50,65 L 22,85 L 33,55 L 5,35 L 39,35 Z"

    css = f"""/* Elastic SVG Shape Morphing */
:root {{
    --bg-color: {bg_color};
    --card-bg: {card_bg};
    --text-primary: {text_color};
    --text-secondary: {text_muted};
    --accent: {accent_color};
    --stroke: {stroke_color};
    --btn-bg: {button_bg};
    --btn-hover: {button_hover};
}}

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
}}

.layout-wrapper {{
    width: {width_px}px;
    height: {height_px}px;
    display: flex;
    justify-content: center;
    align-items: center;
}}

.morph-card {{
    background: var(--card-bg);
    border-radius: 24px;
    padding: 60px 80px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 40px;
    text-align: center;
    transition: transform 0.3s ease;
}}

.svg-container {{
    width: 240px;
    height: 240px;
    filter: drop-shadow(0 10px 15px rgba(0,0,0,0.2));
}}

.morphing-shape {{
    /* Default state: Square */
    d: path("{path_square}");
    fill: var(--accent);
    stroke: var(--stroke);
    stroke-width: 2px;
    stroke-linejoin: round;
    /* The magic elastic bounce easing */
    transition: d 0.9s cubic-bezier(0.68, -0.6, 0.32, 1.6), 
                fill 0.9s ease;
}}

.morph-card.is-morphed .morphing-shape {{
    /* Morphed state: Star */
    d: path("{path_star}");
    fill: #FFD700; /* Shift color slightly for effect */
}}

.card-content h1 {{
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 12px;
    letter-spacing: -0.5px;
}}

.card-content p {{
    font-size: 16px;
    color: var(--text-secondary);
    margin-bottom: 30px;
}}

.toggle-btn {{
    appearance: none;
    background: var(--btn-bg);
    color: var(--text-primary);
    border: 1px solid rgba(255,255,255,0.1);
    padding: 14px 28px;
    border-radius: 99px;
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    outline: none;
}}

.toggle-btn:hover {{
    background: var(--btn-hover);
    transform: translateY(-2px);
}}

.toggle-btn:active {{
    transform: translateY(0);
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="layout-wrapper">
        <div class="morph-card" id="morphCard">
            
            <!-- SVG Container -->
            <div class="svg-container">
                <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                    <!-- The path uses CSS for its 'd' attribute transitions -->
                    <path class="morphing-shape"></path>
                </svg>
            </div>

            <!-- Content & Controls -->
            <div class="card-content">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
                <button class="toggle-btn" id="morphBtn">Trigger Morph</button>
            </div>

        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Elastic SVG Shape Morphing Interaction
document.addEventListener('DOMContentLoaded', () => {
    const morphBtn = document.getElementById('morphBtn');
    const morphCard = document.getElementById('morphCard');

    morphBtn.addEventListener('click', () => {
        // Toggling the class triggers the CSS path transition
        morphCard.classList.toggle('is-morphed');
        
        // Dynamic button text update
        if (morphCard.classList.contains('is-morphed')) {
            morphBtn.textContent = "Revert Shape";
        } else {
            morphBtn.textContent = "Trigger Morph";
        }
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
