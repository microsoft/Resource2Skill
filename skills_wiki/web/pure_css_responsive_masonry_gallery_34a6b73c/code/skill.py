def create_component(
    output_dir: str,
    title_text: str = "Image Title",
    body_text: str = "Lorem ipsum dolor sit amet consectetur adipisicing elit. Dicta odio iste magnam obcaecati ipsa veniam. Deleniti exercitationem alias ullam quia!",
    color_scheme: str = "light",        # "dark" or "light"
    accent_color: str = "deeppink",     # CSS hex/color for accent
    width_px: int = 1200,               # Default viewport size context
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Pure CSS Masonry Gallery visual effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#11141a"
        card_bg = "#1e2430"
        title_color = "#f0f0f0"
        text_color = "#a0a5b0"
        shadow = "rgba(0,0,0,0.6)"
        border_color = "rgba(255,255,255,0.1)"
        icon_color = "#ccc"
    else:
        bg_color = "#dddddd"
        card_bg = "#ffffff"
        title_color = "#555555"
        text_color = "#999999"
        shadow = "rgba(0,0,0,0.3)"
        border_color = "rgba(0,0,0,0.1)"
        icon_color = "#333333"

    # === HTML Generation ===
    # Using real placeholder images with different aspect ratios to demonstrate the masonry packing.
    images = [
        ("https://images.unsplash.com/photo-1524504388940-b1c1722653e1?auto=format&fit=crop&w=400&q=80", "Portrait of a woman"),
        ("https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=400&q=80", "Portrait close up"),
        ("https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=400&q=80", "Man looking away"),
        ("https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=400&q=80", "Smiling woman"),
        ("https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=400&q=80", "Woman with camera"),
        ("https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?auto=format&fit=crop&w=400&q=80", "Fashion portrait"),
        ("https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=400&q=80", "Man in forest")
    ]
    
    boxes_html = ""
    for i, (img_url, alt_text) in enumerate(images, 1):
        boxes_html += f"""
        <div class="box">
            <img src="{img_url}" alt="{alt_text}" loading="lazy">
            <div class="info">
                <h3><span>{i:02d}.</span> {title_text} Here</h3>
                <p>{body_text}</p>
                <div class="share">
                    <a href="#" class="fab fa-facebook-f" aria-label="Facebook"></a>
                    <a href="#" class="fab fa-twitter" aria-label="Twitter"></a>
                    <a href="#" class="fab fa-instagram" aria-label="Instagram"></a>
                    <a href="#" class="fab fa-linkedin-in" aria-label="LinkedIn"></a>
                </div>
            </div>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CSS Masonry Gallery</title>
    <!-- Font Awesome CDN for Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <!-- Gallery Container -->
    <div class="gallery">
{boxes_html}
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === CSS Generation ===
    css = f"""/* Pure CSS Masonry Gallery Component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    transition: all .2s linear;
}}

body {{
    font-family: Arial, Helvetica, sans-serif;
    background-color: {bg_color};
    min-height: 100vh;
}}

/* Core Masonry Setup */
.gallery {{
    background: {bg_color};
    padding: 40px 8%;
    /* Create columns */
    column-count: 3;
    column-gap: 20px;
}}

.gallery .box {{
    background: {card_bg};
    padding: 15px;
    margin-bottom: 20px; /* Provides vertical spacing between masonry items */
    box-shadow: 0 3px 5px {shadow};
    /* CRUCIAL: Prevents card from splitting across columns */
    break-inside: avoid;
    /* Fallback for older browsers */
    display: inline-block;
    width: 100%;
}}

.gallery .box img {{
    width: 100%;
    border-radius: 2px;
    object-fit: cover;
    display: block; /* Removes baseline gap */
}}

.gallery .box .info h3 {{
    font-size: 20px;
    padding: 15px 0 10px 0;
    color: {title_color};
}}

.gallery .box .info h3 span {{
    color: {accent_color};
}}

.gallery .box .info p {{
    font-size: 14px;
    color: {text_color};
    line-height: 1.5;
}}

/* Footer Share Section */
.gallery .box .info .share {{
    margin-top: 15px;
    padding-top: 15px;
    border-top: 1px solid {border_color};
}}

.gallery .box .info .share a {{
    font-size: 20px;
    color: {icon_color};
    margin-right: 15px;
    text-decoration: none;
}}

.gallery .box .info .share a:hover {{
    color: {accent_color};
}}

/* Responsive Breakpoints */
@media (max-width: 991px) {{
    .gallery {{
        column-count: 2;
    }}
}}

@media (max-width: 650px) {{
    .gallery {{
        column-count: 1;
        padding: 20px;
    }}
}}
"""

    # === JavaScript ===
    # No JS required for layout; providing empty setup for consistency.
    js = f"""// CSS Multi-column layout handles masonry natively.
// No JavaScript logic required for this component.
console.log("Masonry layout loaded successfully.");
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
