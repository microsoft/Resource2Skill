def create_component(
    output_dir: str,
    title_text: str = "Find your perfect home today",
    body_text: str = "Explore our exclusive listings of beautiful properties. Your dream home is just a click away, backed by our team of expert real estate agents ready to assist you every step of the way.",
    color_scheme: str = "dark",        # "dark" overlays dark gradient + white text, "light" overlays white gradient + dark text
    accent_color: str = "#0d6efd",     # Standard blue accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Hero Section with Image Overlay and Parallax.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)
    
    # Custom background image option
    bg_image_url = kwargs.get("bg_image_url", "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1920&q=80")

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        # Dark overlay, white text (as seen in the tutorial)
        overlay_color = "rgba(0, 0, 0, 0.6)"
        text_color = "#ffffff"
        body_text_color = "#e0e0e0"
    else:
        # Light overlay, dark text (inverse adaptation)
        overlay_color = "rgba(255, 255, 255, 0.85)"
        text_color = "#1a1a1a"
        body_text_color = "#333333"

    # === CSS ===
    css = f"""/* Hero Section Component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --accent: {accent_color};
    --overlay: {overlay_color};
    --text-primary: {text_color};
    --text-secondary: {body_text_color};
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    /* Wrapper styling to showcase the component within requested dimensions */
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    background-color: #f0f0f0; 
}}

/* Bounding box for the isolated component */
.component-wrapper {{
    width: {width_px}px;
    height: {height_px}px;
    max-width: 100%;
    overflow-y: auto; /* Allow scrolling within the component to see parallax if height > viewport */
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    position: relative;
}}

/* --- Core Hero Styles --- */
.hero {{
    /* Combine gradient overlay and image */
    background-image: linear-gradient(var(--overlay), var(--overlay)), url('{bg_image_url}');
    background-position: center;
    background-repeat: no-repeat;
    background-size: cover;
    /* Parallax effect relative to the viewport */
    background-attachment: fixed; 
    
    /* Spacious padding as per tutorial */
    padding: 120px 5%;
    min-height: 100%; /* Fill wrapper height */
    display: flex;
    align-items: center;
}}

.container {{
    max-width: 1100px;
    margin-left: auto;
    margin-right: auto;
    width: 100%;
}}

.hero h1 {{
    font-size: 62px;
    line-height: 68px;
    color: var(--text-primary);
    margin-bottom: 18px;
    font-weight: 700;
}}

.hero p {{
    font-size: 28px;
    line-height: 36px;
    color: var(--text-secondary);
    margin-bottom: 40px;
    max-width: 900px;
}}

/* --- Action Buttons --- */
.action-btns {{
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
}}

.action-btns a {{
    text-decoration: none;
    color: #ffffff;
    background-color: var(--accent);
    padding: 12px 28px;
    border-radius: 8px;
    font-size: 18px;
    font-weight: 500;
    transition: background-color 0.2s ease, transform 0.1s ease;
}}

.action-btns a.secondary {{
    background-color: transparent;
    border: 2px solid var(--text-primary);
    color: var(--text-primary);
}}

.action-btns a:hover {{
    filter: brightness(1.1);
    transform: translateY(-2px);
}}

/* Responsive Typography */
@media (max-width: 768px) {{
    .hero {{
        padding: 80px 5%;
    }}
    .hero h1 {{
        font-size: 42px;
        line-height: 50px;
    }}
    .hero p {{
        font-size: 20px;
        line-height: 30px;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hero Section Component</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="component-wrapper">
        <!-- Core Hero Section -->
        <section class="hero">
            <div class="container">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
                
                <div class="action-btns">
                    <a href="#" class="primary">Explore properties</a>
                    <a href="#" class="secondary">Get in touch</a>
                </div>
            </div>
        </section>
        
        <!-- Extra content to demonstrate parallax scrolling within the wrapper -->
        <div style="height: 600px; background: white; padding: 60px 5%; color: #333;">
            <div class="container">
                <h2 style="font-size: 36px; margin-bottom: 20px;">Scroll up and down</h2>
                <p style="font-size: 18px; line-height: 1.6; color: #555;">Notice how the hero background image remains fixed in place (parallax effect) while this content and the hero text scrolls normally over it. This is achieved using the <code>background-attachment: fixed</code> CSS property.</p>
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// No JavaScript is required for this core CSS layout pattern.
document.addEventListener('DOMContentLoaded', () => {
    console.log("Hero section loaded.");
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
