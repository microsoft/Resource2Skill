import os

def create_component(
    output_dir: str,
    title_text: str = "Responsive Grid Layouts",
    body_text: str = "Explore the power of CSS Grid for dynamic and flexible web design. From auto-wrapping product lists to complex bento grids and layered stacking effects, master modern layout techniques.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#6a0dad",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800, # Note: height_px is used for the overall body/container, but specific sections have their own heights/min-heights.
    **kwargs,
) -> dict:
    """
    Create a web component reproducing various CSS Grid layout effects from the tutorial.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#1a1a2e"
        text_color = "#f0f0f0"
        surface_color = "rgba(255, 255, 255, 0.08)"
        card_bg_color = "#282844"
        card_text_color = "#f0f0f0"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        surface_color = "rgba(0, 0, 0, 0.05)"
        card_bg_color = "#ffffff"
        card_text_color = "#333333"
    
    # === CSS ===
    css = f"""
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --card-bg: {card_bg_color};
    --card-text: {card_text_color};
    --container-width: {width_px}px;
    --container-height: {height_px}px;
    --gap: 1.5rem;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: var(--gap);
    line-height: 1.6;
}}

h1, h2, h3 {{
    color: var(--accent);
    margin-bottom: 0.5em;
    text-align: center;
}}

p {{
    margin-bottom: 1em;
}}

.main-content {{
    width: min(100%, var(--container-width));
}}

.section {{
    width: 100%; /* Sections fill the main-content width */
    margin-bottom: 4rem;
    padding: var(--gap);
    border-radius: 8px;
    background: var(--surface);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}}

/* --- Auto-Wrapping Product Grid --- */
.product-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); /* Auto-fit, responsive columns */
    gap: var(--gap);
    justify-content: center; /* Center items horizontally if there's extra space */
    padding: var(--gap) 0;
}}

.product-item {{
    background: var(--card-bg);
    color: var(--card-text);
    padding: 1.5rem;
    border-radius: 8px;
    text-align: center;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
}}

.product-item img {{
    max-width: 100%;
    height: auto; /* Maintain aspect ratio */
    border-radius: 4px;
    margin-bottom: 1rem;
}}

.product-item h3 {{
    font-size: 1.2rem;
    color: var(--accent);
    margin-bottom: 0.5rem;
}}

.product-item p {{
    font-size: 0.9rem;
    color: var(--card-text);
    margin-bottom: 1rem;
}}

.product-item .price {{
    font-weight: bold;
    color: var(--accent);
    font-size: 1.1rem;
}}

/* --- Bento Grid (Grid Template Areas) --- */
.bento-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr; /* 4 equal columns */
    grid-template-rows: 150px 150px; /* 2 fixed-height rows */
    gap: var(--gap);
    padding: var(--gap);
}}

.bento-item {{
    background: var(--card-bg);
    color: var(--card-text);
    padding: 1rem;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 1.5rem;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}}

.bento-item-1 {{ grid-area: box1; background: {accent_color}; color: #fff; }}
.bento-item-2 {{ grid-area: box2; }}
.bento-item-3 {{ grid-area: box3; background: {accent_color}; color: #fff; }}
.bento-item-4 {{ grid-area: box4; }}
.bento-item-5 {{ grid-area: box5; }}

/* Desktop Layout */
.bento-grid {{
    grid-template-areas:
        "box1 box1 box2 box3"
        "box4 box5 box5 box3";
}}

/* Tablet Layout (example: max-width 768px, ~48em) */
@media (max-width: 48em) {{
    .bento-grid {{
        grid-template-columns: 1fr 1fr 1fr; /* 3 columns */
        grid-template-rows: repeat(3, 120px);
        grid-template-areas:
            "box1 box1 box2"
            "box1 box1 box3"
            "box4 box5 box5";
    }}
}}

/* Mobile Layout (example: max-width 480px, ~30em) */
@media (max-width: 30em) {{
    .bento-grid {{
        grid-template-columns: 1fr; /* Single column */
        grid-template-rows: repeat(5, 100px);
        grid-template-areas:
            "box1"
            "box2"
            "box3"
            "box4"
            "box5";
    }}
    .bento-item {{
        font-size: 1.2rem;
    }}
}}

/* --- Grid Stacking (Header Background Video) --- */
.header-stack {{
    height: 60vh;
    min-height: 400px;
    width: 100%;
    display: grid;
    grid-template-areas: "stack"; /* All children go into this single area */
    place-items: center; /* Center content vertically and horizontally */
    border-radius: 8px;
    overflow: hidden; /* Clip video/image outside rounded corners */
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
    margin-bottom: 4rem;
}}

.header-stack video {{
    grid-area: stack; /* Place video in the 'stack' area */
    width: 100%;
    height: 100%;
    object-fit: cover; /* Cover the entire grid area */
    z-index: 1; /* Below content */
    opacity: 0.6; /* Slightly transparent */
}}

.header-stack .content-overlay {{
    grid-area: stack; /* Place content in the same 'stack' area */
    z-index: 2; /* Above video */
    text-align: center;
    max-width: 70%;
    padding: 2rem;
    background: rgba(0, 0, 0, 0.4); /* Semi-transparent background for readability */
    border-radius: 8px;
}}

.header-stack .content-overlay h2 {{
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
    color: #fff;
    text-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
}}

.header-stack .content-overlay p {{
    font-size: 1.1rem;
    margin-bottom: 1.5rem;
    color: #e0e0e0;
}}

.header-stack .content-overlay button {{
    background-color: var(--accent);
    color: white;
    padding: 0.8rem 1.8rem;
    border: none;
    border-radius: 30px;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.3s ease;
}}

.header-stack .content-overlay button:hover {{
    background-color: color-mix(in srgb, var(--accent) 80%, black);
}}

@media (max-width: 600px) {{
    .header-stack .content-overlay h2 {{
        font-size: 1.8rem;
    }}
    .header-stack .content-overlay p {{
        font-size: 0.9rem;
    }}
    .header-stack .content-overlay {{
        max-width: 90%;
        padding: 1.5rem;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="main-content">
        <h1>{title_text}</h1>
        <p style="text-align: center; max-width: 800px; margin: 0 auto 2rem auto;">{body_text}</p>

        <!-- Section 1: Auto-Wrapping Product Grid -->
        <div class="section">
            <h2>Auto-Wrapping Product Gallery</h2>
            <p style="text-align: center; margin-bottom: 2rem;">Products automatically adjust their column count based on screen width.</p>
            <div class="product-grid">
                <div class="product-item">
                    <img src="https://picsum.photos/id/237/300/200" alt="Product Image 1">
                    <h3>Ergonomic Mouse</h3>
                    <p>Designed for comfort and precision. A must-have for professionals.</p>
                    <span class="price">$29.99</span>
                </div>
                <div class="product-item">
                    <img src="https://picsum.photos/id/238/300/200" alt="Product Image 2">
                    <h3>Mechanical Keyboard</h3>
                    <p>Tactile switches for a satisfying typing experience.</p>
                    <span class="price">$49.99</span>
                </div>
                <div class="product-item">
                    <img src="https://picsum.photos/id/239/300/200" alt="Product Image 3">
                    <h3>Noise-Cancelling Headphones</h3>
                    <p>Immerse yourself in pure audio, block out distractions.</p>
                    <span class="price">$19.99</span>
                </div>
                <div class="product-item">
                    <img src="https://picsum.photos/id/240/300/200" alt="Product Image 4">
                    <h3>Smart Fitness Tracker</h3>
                    <p>Monitor your health and achieve your fitness goals.</p>
                    <span class="price">$79.99</span>
                </div>
                <div class="product-item">
                    <img src="https://picsum.photos/id/241/300/200" alt="Product Image 5">
                    <h3>Portable SSD</h3>
                    <p>Blazing fast storage on the go. Secure your data.</p>
                    <span class="price">$34.50</span>
                </div>
                <div class="product-item">
                    <img src="https://picsum.photos/id/242/300/200" alt="Product Image 6">
                    <h3>Webcam 4K HD</h3>
                    <p>Crystal clear video calls and streaming. Look your best.</p>
                    <span class="price">$62.00</span>
                </div>
                <div class="product-item">
                    <img src="https://picsum.photos/id/243/300/200" alt="Product Image 7">
                    <h3>Gaming Monitor</h3>
                    <p>High refresh rate, stunning visuals. Elevate your gameplay.</p>
                    <span class="price">$12.99</span>
                </div>
                <div class="product-item">
                    <img src="https://picsum.photos/id/244/300/200" alt="Product Image 8">
                    <h3>Wireless Charger</h3>
                    <p>Fast, convenient charging for all your compatible devices.</p>
                    <span class="price">$89.99</span>
                </div>
            </div>
        </div>

        <!-- Section 2: Bento Grid -->
        <div class="section">
            <h2>Bento Grid Layout (Media Queries)</h2>
            <p style="text-align: center; margin-bottom: 2rem;">Complex grid areas redefine layout responsively via CSS Media Queries.</p>
            <div class="bento-grid">
                <div class="bento-item bento-item-1">Feature Spotlight</div>
                <div class="bento-item bento-item-2">Quick Access</div>
                <div class="bento-item bento-item-3">Analytics View</div>
                <div class="bento-item bento-item-4">Latest News</div>
                <div class="bento-item bento-item-5">User Profile</div>
            </div>
        </div>

        <!-- Section 3: Stacked Header with Background Video -->
        <div class="header-stack">
            <video autoplay loop muted playsinline>
                <source src="https://cdn.pixabay.com/video/2022/10/24/136737-761405101_large.mp4" type="video/mp4">
                Your browser does not support the video tag.
            </video>
            <div class="content-overlay">
                <h2>Immersive Header Experience</h2>
                <p>Combine video backgrounds with overlay content using Grid Stacking for dynamic and engaging hero sections.</p>
                <button>Discover More</button>
            </div>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript (Placeholder, not strictly needed for these CSS examples) ===
    js = """
document.addEventListener('DOMContentLoaded', () => {
    // No specific JavaScript needed for these CSS Grid examples
    console.log('CSS Grid examples loaded.');
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
