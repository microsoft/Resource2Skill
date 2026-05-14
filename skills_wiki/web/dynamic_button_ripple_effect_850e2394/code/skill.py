def create_component(
    output_dir: str,
    title_text: str = "Interactive Button Ripples",
    body_text: str = "Click the buttons below to see the precise, coordinate-based ripple effect.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Dynamic Button Ripple Effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#040d15"
        text_color = "#ffffff"
        btn_text = "#ffffff"
        ripple_color = "rgba(255, 255, 255, 0.6)"
    else:
        bg_color = "#f0f4f8"
        text_color = "#1a202c"
        btn_text = "#ffffff"
        ripple_color = "rgba(255, 255, 255, 0.8)"

    # === CSS ===
    css = f"""/* Dynamic Button Ripple Effect — generated component */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --btn-text: {btn_text};
    --ripple-color: {ripple_color};
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}}

.container {{
    width: {width_px}px;
    height: {height_px}px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
}}

.header {{
    margin-bottom: 3rem;
}}

.header h1 {{
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 1rem;
    letter-spacing: -0.5px;
}}

.header p {{
    font-size: 1rem;
    opacity: 0.8;
    max-width: 500px;
    line-height: 1.5;
}}

.button-group {{
    display: flex;
    gap: 2rem;
    flex-wrap: wrap;
    justify-content: center;
}}

/* -- Core Button Styling -- */
.ripple-btn {{
    position: relative;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 18px 48px;
    font-size: 18px;
    font-weight: 600;
    color: var(--btn-text);
    text-decoration: none;
    text-transform: uppercase;
    letter-spacing: 2px;
    border-radius: 40px;
    border: none;
    cursor: pointer;
    overflow: hidden; /* Crucial: Keeps ripple inside bounds */
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    /* Prevent text selection on rapid clicks */
    user-select: none; 
    -webkit-tap-highlight-color: transparent;
}}

.ripple-btn:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.3);
}}

.ripple-btn:active {{
    transform: translateY(1px);
}}

/* Ensure text stays above the ripple */
.ripple-btn span.btn-text {{
    position: relative;
    z-index: 10;
}}

/* Gradient Variations */
.ripple-btn.cyan {{
    background: linear-gradient(90deg, #0162c8, #55e7fc);
}}

.ripple-btn.purple {{
    background: linear-gradient(90deg, #755bea, #ff72c0);
}}

/* -- The Ripple Element -- */
.ripple-btn .ripple-effect {{
    position: absolute;
    background: var(--ripple-color);
    border-radius: 50%;
    transform: translate(-50%, -50%);
    pointer-events: none; /* Ignore clicks so button underneath registers */
    animation: animateRipple 0.8s linear forwards;
}}

/* Ripple Animation Keyframes */
@keyframes animateRipple {{
    0% {{
        width: 0px;
        height: 0px;
        opacity: 0.5;
    }}
    100% {{
        width: 600px; /* Large enough to cover wide buttons */
        height: 600px;
        opacity: 0;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </div>
        
        <div class="button-group">
            <a href="#" class="ripple-btn cyan">
                <span class="btn-text">Button</span>
            </a>
            <button class="ripple-btn purple">
                <span class="btn-text">Button</span>
            </button>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Dynamic Ripple Effect Logic
document.addEventListener('DOMContentLoaded', () => {{
    const buttons = document.querySelectorAll('.ripple-btn');

    buttons.forEach(button => {{
        button.addEventListener('click', function(e) {{
            // Use getBoundingClientRect for robust positioning even if layout changes
            const rect = this.getBoundingClientRect();
            
            // Calculate exact click coordinates inside the button
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            // Create the ripple span element
            const ripple = document.createElement('span');
            ripple.classList.add('ripple-effect');
            
            // Set position based on click coordinates
            ripple.style.left = `${{x}}px`;
            ripple.style.top = `${{y}}px`;

            // Append to the button
            this.appendChild(ripple);

            // Cleanup: remove the span after animation completes (800ms matches CSS duration)
            setTimeout(() => {{
                ripple.remove();
            }}, 800);
        }});
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
