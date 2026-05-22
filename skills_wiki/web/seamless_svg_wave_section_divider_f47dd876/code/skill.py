def create_component(
    output_dir: str,
    title_text: str = "Web Dev Simplified",
    body_text: str = "Exclusive Course Discounts. Be the first to know when my Learn React Today course drops!",
    color_scheme: str = "dark",        # "dark" or "light" (affects the top section)
    accent_color: str = "#00AAFF",     # Maps to the bottom section background
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Seamless SVG Wave Section Divider.
    """
    import os
    import urllib.parse

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors based on the tutorial's aesthetic ===
    if color_scheme == "dark":
        top_bg = "#005681" # Deep Blue from the tutorial
        top_text = "#FFFFFF"
    else:
        top_bg = "#F8F9FA"
        top_text = "#333333"

    bottom_bg = accent_color # Light blue from the tutorial
    bottom_text = "#FFFFFF"

    # Define the SVG wave. This is a top-hanging wave that visually extends from the top section.
    # The 'fill' must perfectly match the top_bg to create the seamless illusion.
    raw_svg = f"""<svg viewBox="0 0 1440 120" xmlns="http://www.w3.org/2000/svg"><path fill="{top_bg}" d="M0,64L80,69.3C160,75,320,85,480,80C640,75,800,53,960,48C1120,43,1280,53,1360,58.7L1440,64L1440,0L1360,0C1280,0,1120,0,960,0C800,0,640,0,480,0C320,0,160,0,80,0L0,0Z"></path></svg>"""
    
    # URL encode the SVG so it can be used safely in CSS background-image
    encoded_svg = urllib.parse.quote(raw_svg)
    svg_data_uri = f"data:image/svg+xml;charset=utf-8,{encoded_svg}"

    # === CSS ===
    css = f"""/* Seamless SVG Wave Section Divider */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --top-bg: {top_bg};
    --top-text: {top_text};
    --bottom-bg: {bottom_bg};
    --bottom-text: {bottom_text};
    --content-max-width: 1000px;
}}

body {{
    font-family: 'Nunito', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: var(--bottom-bg); /* Body inherits bottom color for smooth scrolling */
    min-height: 100vh;
    overflow-x: hidden;
}}

/* -- Top Section (Hero) -- */
.dark-header {{
    background-color: var(--top-bg);
    color: var(--top-text);
    padding: 60px 20px 20px 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    position: relative;
    z-index: 2; /* Keep above the wave */
}}

.content-wrapper {{
    max-width: var(--content-max-width);
    margin: 0 auto;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 20px;
}}

.brand-name {{
    font-size: 1.5rem;
    font-weight: 800;
    letter-spacing: 1px;
}}

.title {{
    font-size: 3.5rem;
    font-weight: 900;
    line-height: 1.1;
    margin-top: 10px;
}}

.sub-title {{
    font-size: 1.25rem;
    font-weight: 400;
    max-width: 600px;
    opacity: 0.9;
}}

/* -- The Wave Divider -- */
.dark-header-divider {{
    background-image: url('{svg_data_uri}');
    background-repeat: no-repeat;
    background-position: bottom;
    background-size: cover;
    height: 120px; /* Base height for the wave */
    width: 100vw;
    
    /* THE CRITICAL TRICK: Pull the wave up slightly to eliminate sub-pixel rendering gaps */
    margin-top: -5px; 
    
    position: relative;
    z-index: 1; /* Sit neatly under the main header content */
}}

/* -- Bottom Section (Form & Content) -- */
.light-section {{
    background-color: var(--bottom-bg);
    color: var(--bottom-text);
    padding: 0 20px 80px 20px;
    display: flex;
    justify-content: center;
}}

/* -- Email Form Styles -- */
.email-form {{
    display: flex;
    width: 100%;
    max-width: 650px;
    gap: 15px;
    margin-top: 20px;
}}

.email-form input {{
    flex-grow: 1;
    padding: 18px 24px;
    border-radius: 50px; /* Pill shape */
    border: 2px solid transparent;
    font-size: 1.1rem;
    font-family: inherit;
    outline: none;
    transition: background-color 0.3s ease, border-color 0.3s ease;
}}

.email-form input:focus {{
    background-color: #f0f8ff;
    border-color: rgba(0, 0, 0, 0.1);
}}

.email-form button {{
    padding: 18px 40px;
    border-radius: 50px; /* Pill shape */
    background-color: #222222;
    color: #FFFFFF;
    border: 2px solid #222222;
    font-size: 1.1rem;
    font-weight: 700;
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.1s ease;
    font-family: inherit;
}}

.email-form button:hover {{
    background-color: #000000;
    border-color: #000000;
}}

.email-form button:active {{
    transform: scale(0.98);
}}

/* Responsive Adjustments */
@media (max-width: 768px) {{
    .title {{ font-size: 2.5rem; }}
    .sub-title {{ font-size: 1rem; }}
    
    /* Stack the form on mobile */
    .email-form {{
        flex-direction: column;
    }}
    .email-form button {{
        width: 100%;
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
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;800;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <!-- Top Dark Section -->
    <header class="dark-header">
        <div class="content-wrapper">
            <div class="brand-name">&#123;WDS&#125;</div>
            <h1 class="title">{title_text}</h1>
            <p class="sub-title">{body_text}</p>
        </div>
    </header>

    <!-- The Seamless SVG Wave -->
    <div class="dark-header-divider" aria-hidden="true"></div>

    <!-- Bottom Light Section -->
    <main class="light-section">
        <div class="content-wrapper">
            <form class="email-form" id="signup-form">
                <input type="email" placeholder="Enter Your Email" required aria-label="Email Address">
                <button type="submit">Join Now!</button>
            </form>
        </div>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Form interaction logic
document.addEventListener('DOMContentLoaded', () => {{
    const form = document.getElementById('signup-form');
    
    if(form) {{
        form.addEventListener('submit', (e) => {{
            e.preventDefault();
            const btn = form.querySelector('button');
            const originalText = btn.innerText;
            
            // Provide immediate user feedback
            btn.innerText = "Submitting...";
            btn.style.backgroundColor = "#4caf50";
            btn.style.borderColor = "#4caf50";
            
            // Simulate network request
            setTimeout(() => {{
                btn.innerText = "Joined!";
                form.querySelector('input').value = '';
                
                // Reset after a delay
                setTimeout(() => {{
                    btn.innerText = originalText;
                    btn.style.backgroundColor = "";
                    btn.style.borderColor = "";
                }}, 3000);
            }}, 1500);
        }});
    }}
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
