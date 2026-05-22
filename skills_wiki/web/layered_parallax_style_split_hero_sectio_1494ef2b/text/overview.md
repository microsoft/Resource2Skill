### 1. High-level Design Pattern Extraction

> **Skill Name**: Layered Parallax-Style Split Hero Section

* **Core Visual Mechanism**: This design utilizes a clever CSS trick: stacking multiple background images on a single container (`background-image: url(subject), url(pattern);`). By positioning a scalable subject (like a portrait or product) at `bottom center` with `no-repeat`, and layering it over a repeating geometric pattern, it creates an instant sense of depth and a parallax-like composition without any JavaScript. The content is then split symmetrically using Flexbox, framing the central subject.

* **Why Use This Skill (Rationale)**: Splitting the layout frames a central focal point perfectly, guiding the user's eye naturally from the bold headline on the left, to the central visual subject, and finally to secondary supporting text (like testimonials or features) on the right. The dual-background technique keeps the DOM extremely lightweight and ensures the subject scales fluidly with the viewport height.

* **Overall Applicability**: Ideal for personal portfolios, prominent product feature showcases, or bold SaaS landing page heroes where a single human element or flagship product needs to be flanked by strong value propositions.

* **Browser Compatibility**: Fully supported in all modern browsers. Multiple background images and Flexbox have been standard for many years.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Dual Background System**: The `.hero` container uses a comma-separated list for `background-image`. The first item sits on top (the portrait/silhouette), and the second sits at the bottom (the repeating geometric texture).
  - **Color Logic**: Dark, high-contrast theme. Deep blue/slate background (`#1A253A`), white typography (`#FFFFFF`), and a vibrant magenta/pink accent color (`#C13584` default, `#9E2F6E` on hover) used sparingly for calls-to-action and borders.
  - **Typographic Hierarchy**:
    - **H1**: Dominant, uppercase, extremely large (`clamp(40px, 6vw, 96px)`), tight line-height to make multiline statements punchy.
    - **Paragraphs**: Readable, airy (`18px` with `30px` line-height).
  - **Accent Borders**: The secondary content uses thick left-borders (`4px solid var(--accent)`) to visually tie it to the main call-to-action button on the opposite side.

* **Step B: Layout & Compositional Style**
  - **Layout System**: A full-width/height `flex` container. The content is wrapped in an inner container with `justify-content: space-between`, effectively pushing the main headline and the quotes to opposite edges, leaving the center clear for the background portrait.
  - **Spatial Feel**: Asymmetric balance. The large, heavy typography on the left is balanced by the offset, smaller typographic blocks (quotes) on the right.
  - **Staggered Flow**: The secondary quotes use a specific nth-child margin offset (`margin-left: 100px;`) to create a cascading, cascading editorial look rather than a rigid column.

* **Step C: Interactive Behavior & Animations**
  - Simple CSS transition on the primary Call to Action (CTA) button, changing background color on hover.
  - No JavaScript is strictly required for this core visual layout, keeping performance exceptionally high.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Layered Subject & Texture** | CSS Multiple `background-image` | The most elegant, DOM-light way to achieve this. Scales naturally with `vh` and `cover` sizes without requiring absolute positioning of `<img>` tags. |
| **Split Content Layout** | CSS Flexbox (`space-between`) | Safely pushes the text blocks to the sides of the central background subject, easily collapsing into a column on mobile. |
| **Staggered Quotes** | CSS `:nth-child(2)` | Allows targeted offsetting (`margin-left`) of specific paragraphs to create the editorial, cascading text effect seen in the tutorial. |
| **Self-Contained Graphics** | SVG Data URIs | Ensures the code runs immediately from a local HTML file without CORS issues or missing external image dependencies. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "WELCOME<br>TO MY FIRST<br>WEBSITE",
    body_text: str = "Nam interdum felis at felis placerat, sed varius massa ultricies. Integer quis nisi non dolor scelerisque efficitur at sed turpis.",
    color_scheme: str = "dark",
    accent_color: str = "#C13584",
    width_px: int = 1400,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Layered Split Hero Section.
    """
    import os
    import urllib.parse

    os.makedirs(output_dir, exist_ok=True)

    # Base64/Data URI SVGs to make the component completely self-contained
    # 1. Repeating geometric background pattern
    pattern_svg = '''<svg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg"><g fill="none" fill-rule="evenodd"><g fill="#ffffff" fill-opacity="0.03"><path d="M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z"/></g></g></svg>'''
    pattern_uri = "data:image/svg+xml," + urllib.parse.quote(pattern_svg)

    # 2. Central Portrait Silhouette
    portrait_svg = '''<svg width="500" height="700" viewBox="0 0 500 700" xmlns="http://www.w3.org/2000/svg"><path d="M250 100 C200 100 200 200 250 200 C300 200 300 100 250 100 Z M100 700 L100 400 C100 280 400 280 400 400 L400 700 Z" fill="#0d1424" opacity="0.95"/></svg>'''
    portrait_uri = "data:image/svg+xml," + urllib.parse.quote(portrait_svg)

    if color_scheme == "dark":
        bg_color = "#1A253A"
        text_color = "#FFFFFF"
    else:
        bg_color = "#E2E8F0"
        text_color = "#0F172A"
        # Invert SVGs for light mode
        pattern_svg = pattern_svg.replace('fill="#ffffff"', 'fill="#000000"')
        pattern_uri = "data:image/svg+xml," + urllib.parse.quote(pattern_svg)
        portrait_svg = portrait_svg.replace('fill="#0d1424"', 'fill="#94a3b8"')
        portrait_uri = "data:image/svg+xml," + urllib.parse.quote(portrait_svg)

    # Generating slightly darker accent for hover state
    # Simple hex manipulation logic for hover
    try:
        h = accent_color.lstrip('#')
        rgb = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
        hover_rgb = tuple(max(0, c - 40) for c in rgb)
        accent_hover = f"#{hover_rgb[0]:02x}{hover_rgb[1]:02x}{hover_rgb[2]:02x}"
    except:
        accent_hover = "#9E2F6E"

    css = f"""/* Split Layered Hero Component */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --accent-color: {accent_color};
    --accent-hover: {accent_hover};
    --hero-height: {height_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Roboto', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    line-height: 1.6;
    overflow-x: hidden;
}}

/* Core Dual-Background Mechanism */
.hero-main {{
    width: 100vw;
    height: 100vh; /* Responsive fallback */
    min-height: var(--hero-height);
    background-color: var(--bg-color);
    /* Layer 1: Portrait (top), Layer 2: Geometric Pattern (bottom) */
    background-image: url('{portrait_uri}'), url('{pattern_uri}');
    background-size: 70vh, auto;
    background-position: bottom center, center;
    background-repeat: no-repeat, repeat;
    
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    padding-bottom: 8vh; /* Lift content slightly relative to bottom portrait */
}}

.content-wrapper {{
    width: 100%;
    max-width: {width_px}px;
    padding: 0 5vw;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 10; /* Ensure text sits above background layers */
}}

/* Left Column: Intro */
.main-intro {{
    max-width: 480px;
    flex-shrink: 1;
}}

.main-intro h1 {{
    font-size: clamp(48px, 6vw, 96px);
    line-height: 1.1;
    font-weight: 800;
    text-transform: uppercase;
    margin-bottom: 24px;
}}

.main-intro p {{
    font-size: 18px;
    line-height: 30px;
    margin-bottom: 30px;
    opacity: 0.9;
}}

.btn {{
    display: inline-block;
    background-color: var(--accent-color);
    color: #fff;
    padding: 12px 28px;
    text-decoration: none;
    font-weight: 600;
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 1px;
    transition: background-color 0.3s ease;
}}

.btn:hover {{
    background-color: var(--accent-hover);
}}

/* Right Column: Quotes */
.main-quotes {{
    max-width: 380px;
    flex-shrink: 1;
}}

.main-quotes .quote-block {{
    border-left: 4px solid var(--accent-color);
    padding-left: 20px;
    margin-bottom: 40px;
}}

/* Cascading offset for the second quote */
.main-quotes .quote-block:nth-child(2) {{
    margin-left: 80px;
}}

.main-quotes p.quote-text {{
    font-size: 18px;
    line-height: 30px;
    font-style: italic;
    margin-bottom: 8px;
}}

.main-quotes p.quote-author {{
    font-size: 16px;
    font-weight: 600;
    color: var(--accent-color);
}}

/* Responsive Design */
@media (max-width: 1024px) {{
    .hero-main {{
        background-position: bottom right -10vw, center;
        background-size: 50vh, auto;
    }}
    .content-wrapper {{
        flex-direction: column;
        justify-content: center;
        gap: 60px;
    }}
    .main-intro, .main-quotes {{
        max-width: 600px;
        background: rgba(26, 37, 58, 0.7); /* Enhance readability over portrait */
        padding: 20px;
        border-radius: 8px;
        backdrop-filter: blur(4px);
    }}
    .main-quotes .quote-block:nth-child(2) {{
        margin-left: 20px;
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Split Layered Hero</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,400;0,600;0,800;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <main class="hero-main">
        <div class="content-wrapper">
            
            <!-- Left Side: Main Introduction -->
            <section class="main-intro">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
                <a href="#" class="btn">My Work</a>
            </section>

            <!-- Right Side: Secondary Content (Quotes) -->
            <section class="main-quotes">
                <div class="quote-block">
                    <p class="quote-text">"The more that you read, the more things you will know. The more that you learn, the more places you'll go."</p>
                    <p class="quote-author">- Dr. Seuss</p>
                </div>
                <div class="quote-block">
                    <p class="quote-text">"For the best return on your money, pour your purse into your head."</p>
                    <p class="quote-author">- Benjamin Franklin</p>
                </div>
            </section>

        </div>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    js = """// Interactive behavior
document.addEventListener('DOMContentLoaded', () => {
    // Parallax effect enhancement on mousemove for deeper immersion
    const hero = document.querySelector('.hero-main');
    
    hero.addEventListener('mousemove', (e) => {
        const x = (e.clientX / window.innerWidth - 0.5) * 20;
        const y = (e.clientY / window.innerHeight - 0.5) * 20;
        
        // Shift background position slightly based on mouse
        // Keeps portrait anchored at bottom, shifts center horizontally slightly
        hero.style.backgroundPosition = `calc(50% + ${x}px) bottom, calc(50% + ${x * 0.5}px) calc(50% + ${y * 0.5}px)`;
    });

    hero.addEventListener('mouseleave', () => {
        hero.style.backgroundPosition = `bottom center, center`;
    });
});
"""

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