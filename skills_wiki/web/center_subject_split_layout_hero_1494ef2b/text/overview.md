### 1. High-level Design Pattern Extraction

> **Skill Name**: Center-Subject Split-Layout Hero

* **Core Visual Mechanism**: This design relies on a layered dual-background approach combined with an asymmetrical, center-pushed Flexbox layout. A textured or patterned background sets the mood, while a cutout subject (like a portrait or product) is anchored to the bottom-center using CSS `background-image` stacking. Foreground text content is split into two distinct blocks (an introduction and secondary info/quotes) that are pushed outward from the center using relative positioning, framing the central subject in the negative space.
* **Why Use This Skill (Rationale)**: It breaks the standard left-to-right reading pattern, creating a highly engaging, theatrical, and personalized feel. Placing a human subject (or hero product) in the direct center immediately establishes a focal point and humanizes the page. Splitting the text ensures the subject isn't obscured while balancing the visual weight of the screen.
* **Overall Applicability**: Perfect for personal portfolios, striking SaaS hero sections, podcast landing pages, or author/speaker websites where a personal brand or specific hero product is the main selling point.
* **Value Addition**: Compared to a standard split 50/50 layout (text on left, image on right), this pattern feels much more integrated and modern. The background image stacking technique avoids complex absolute positioning of `<img>` tags and keeps the HTML semantics clean.
* **Browser Compatibility**: Excellent. Uses standard CSS Flexbox, multiple backgrounds, and `calc()`. Completely supported in all modern browsers (Chrome, Edge, Firefox, Safari).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Dual Background Stacking**: CSS allows multiple background images. They are stacked top-to-bottom. `background-image: url('subject.png'), url('pattern.png');` places the transparent subject *over* the repeating pattern.
  - **Color Logic**: A deep, saturated background (e.g., `#1A253A`) provides high contrast for white text (`#ffffff`). A vivid accent color (e.g., magenta `#c13584`) is used sparingly for buttons and structural borders to guide the eye.
  - **Typographic Hierarchy**: The main headline is massive, uppercase, and bold (`font-size: clamp(...)`, `text-transform: uppercase`, `font-weight: 700`). The secondary text uses a readable serif or clean sans-serif with reduced line length.

* **Step B: Layout & Compositional Style**
  - **Container**: `display: flex; justify-content: center; align-items: center; min-height: 100vh;` creates a full-screen stage.
  - **Content Shifting**: Instead of using margins or a complex grid, the tutorial uses a quick structural trick: `position: relative; right: 20vh;` for the left block and `left: 4vh;` for the right block. This visually pushes the text elements outward to make room for the central background image, with scaling tied to viewport height (`vh`).
  - **Border Accents**: The right-side quotes feature a thick left border (`border-left: 4px solid var(--accent)`) with padding, creating a distinct visual block that separates it from the central subject.

* **Step C: Interactive Behavior & Animations**
  - **Hover States**: The accent button features a basic background color shift or opacity change on hover.
  - **Static Elegance**: The primary strength of this component is its static composition rather than complex animation, relying on bold typography and spatial arrangement.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Layered Subject & Pattern** | CSS Multiple Backgrounds | Simplifies the DOM. Prevents the need for absolutely positioned `<img>` elements layered under text. |
| **Outward Content Shift** | Flexbox + `position: relative` | Accurately reproduces the tutorial's specific layout technique to frame the central space. |
| **Self-Contained Assets** | SVG Data URIs | Ensures the code works perfectly offline and instantly without external image dependencies, generating a pattern and a silhouette portrait entirely in CSS. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Welcome to my<br>first website",
    body_text: str = "Nam interdum felis at felis placerat, sed varius massa ultricies. Integer quis nisl non dolor scelerisque efficitur.",
    color_scheme: str = "dark",
    accent_color: str = "#c13584",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Center-Subject Split-Layout Hero.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors and SVG assets based on color_scheme ===
    if color_scheme == "dark":
        bg_color = "#1A253A"
        text_color = "#ffffff"
        text_muted = "rgba(255, 255, 255, 0.7)"
        # Darker silhouette for dark theme
        silhouette_color = "%230d1421" 
        pattern_color = "%23ffffff"
        pattern_opacity = "0.03"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        text_muted = "rgba(15, 23, 42, 0.7)"
        # Lighter silhouette for light theme
        silhouette_color = "%23e2e8f0" 
        pattern_color = "%23000000"
        pattern_opacity = "0.03"

    # SVG Pattern Data URI
    svg_pattern = f"data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M20 20.5V18H0v-2h20v-2H0v-2h20v-2H0V8h20V6H0V4h20V2H0V0h22v20h2V0h2v20h2V0h2v20h2V0h2v20h2V0h2v20h2v2H20v-1.5zM0 20h2v20H0V20zm4 0h2v20H4V20zm4 0h2v20H8V20zm4 0h2v20h-2V20zm4 0h2v20h-2V20zm4 4h20v2H20v-2zm0 4h20v2H20v-2zm0 4h20v2H20v-2zm0 4h20v2H20v-2z' fill='{pattern_color}' fill-opacity='{pattern_opacity}' fill-rule='evenodd'/%3E%3C/svg%3E"
    
    # SVG Portrait Silhouette Data URI
    svg_portrait = f"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 500'%3E%3Cpath d='M200 50c-40 0-70 30-70 70s30 70 70 70 70-30 70-70-30-70-70-70zm-90 160c-40 0-80 20-80 60v230h340v-230c0-40-40-60-80-60H110z' fill='{silhouette_color}'/%3E%3C/svg%3E"

    # === CSS ===
    css = f"""/* Center-Subject Split-Layout Hero — generated component */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --text-muted: {text_muted};
    --accent-color: {accent_color};
    --container-width: {width_px}px;
    --container-height: {height_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Roboto', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
}}

/* Main Hero Container */
.hero-main {{
    width: 100%;
    min-height: var(--container-height);
    /* Dual Backgrounds: Portrait on top, Pattern on bottom */
    background-image: 
        url("{svg_portrait}"),
        url("{svg_pattern}");
    background-position: bottom center, center;
    background-repeat: no-repeat, repeat;
    background-size: min(70vh, 500px), auto;
    
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
}}

/* Left Column: Intro */
.main-intro {{
    position: relative;
    right: 15vw; /* Pushes content left from center */
    max-width: 400px;
    z-index: 10;
}}

.main-intro h1 {{
    font-size: clamp(2rem, 5vw, 4.5rem);
    line-height: 1.1;
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}}

.main-intro p {{
    font-size: 1rem;
    line-height: 1.6;
    color: var(--text-muted);
    margin-bottom: 2rem;
}}

.btn {{
    display: inline-block;
    background-color: var(--accent-color);
    color: #ffffff; /* Always white text on accent button */
    padding: 12px 24px;
    text-decoration: none;
    text-transform: uppercase;
    font-weight: 700;
    font-size: 0.9rem;
    letter-spacing: 1px;
    transition: filter 0.3s ease;
}}

.btn:hover {{
    filter: brightness(1.2);
}}

/* Right Column: Quotes */
.main-quotes {{
    position: relative;
    left: 10vw; /* Pushes content right from center */
    max-width: 350px;
    z-index: 10;
}}

.quote-block {{
    border-left: 4px solid var(--accent-color);
    padding-left: 1.5rem;
    margin-bottom: 2.5rem;
}}

.quote-block p.quote-text {{
    font-size: 1rem;
    line-height: 1.6;
    font-style: italic;
    margin-bottom: 0.5rem;
}}

.quote-block p.quote-author {{
    font-size: 0.9rem;
    font-weight: 700;
    color: var(--text-muted);
}}

/* Responsive Fallback */
@media (max-width: 900px) {{
    .hero-main {{
        flex-direction: column;
        justify-content: flex-start;
        padding: 4rem 2rem;
        background-position: bottom center, center;
        background-size: min(40vh, 300px), auto;
    }}
    
    .main-intro, .main-quotes {{
        position: static;
        right: auto;
        left: auto;
        max-width: 100%;
        text-align: center;
        margin-bottom: 3rem;
    }}
    
    .quote-block {{
        text-align: left;
        margin: 0 auto 2rem auto;
        max-width: 400px;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hero Layout Component</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="hero-main">
        <div class="main-intro">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <a href="#" class="btn">My Work</a>
        </div>
        
        <div class="main-quotes">
            <div class="quote-block">
                <p class="quote-text">"The more that you read, the more things you will know. The more that you learn, the more places you'll go."</p>
                <p class="quote-author">- Dr. Seuss</p>
            </div>
            <div class="quote-block">
                <p class="quote-text">"For the best return on your money, pour your purse into your head."</p>
                <p class="quote-author">- Benjamin Franklin</p>
            </div>
        </div>
    </main>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Center-Subject Split-Layout Hero
// Interaction logic can be added here (e.g., parallax effects on scroll)
document.addEventListener('DOMContentLoaded', () => {
    console.log("Hero component loaded successfully.");
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
```

### 4. Accessibility & Performance Notes

* **Accessibility**: 
  - Using dual backgrounds for the main decorative portrait is semantically safe since the background image is purely decorative in this context. However, if the portrait represents a specific person critical to the context, an `aria-label` or visually hidden text `<span>` inside the main container describing the person would improve screen reader context.
  - Color contrast meets WCAG guidelines when using the default light text on the dark `#1A253A` background.
* **Performance**:
  - The use of inline SVG Data URIs for both the background pattern and the portrait silhouette ensures **zero HTTP requests** for assets, resulting in instantaneous rendering.
  - Relying on Flexbox layout shifts (`right`/`left`) is performant, but utilizing `@media` queries (as provided in the reproduction code) is strictly necessary. Pushing layout nodes with `vw` or `vh` units creates horizontal overflow issues on mobile screens if the flex items are forced to wrap naturally. The media query cleanly resets the relative positioning to `static` on smaller screens.