# Expandable Vertical-to-Horizontal Responsive Sidebar

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Expandable Vertical-to-Horizontal Responsive Sidebar

* **Core Visual Mechanism**: A sleek, dark-themed vertical navigation bar fixed to the side of the screen. By default, it displays only muted, grayscale icons. When hovered, the sidebar expands in width to reveal text labels, while the hovered icon illuminates with a vibrant, dual-tone accent color. On smaller screens, it seamlessly morphs into a fixed horizontal bottom navigation bar.
* **Why Use This Skill (Rationale)**: This pattern maximizes screen real estate for content by keeping navigation collapsed when not in use. The grayscale-to-color transition provides excellent interactive feedback and draws the user's eye naturally. The responsive shift to a bottom bar on mobile mimics native app ergonomics, making it highly touch-friendly.
* **Overall Applicability**: Dashboards, web apps, SaaS interfaces, and modern portfolio sites where content should be the primary focus, but deep navigation links need to remain accessible at all times.
* **Value Addition**: The use of CSS `filter` to manipulate SVG colors creates a highly polished duotone effect with minimal code. Container Queries (or Media Queries) ensure the component is entirely self-sufficient in adapting its layout.
* **Browser Compatibility**: Very high. Uses standard CSS Flexbox, Transitions, and Filters. The responsive logic uses CSS Container Queries (`@container`), which are supported in all modern browsers (Chrome 105+, Safari 16+, Firefox 110+).

---

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**: Uses a two-tier background system. A deep dark gray for the nav background (`#23232e`) and an even darker hue for hovered states (`#141418`). SVGs are injected with an explicitly vibrant `--accent` color, but are visually muted by default using CSS filters.
  - **Typographic Hierarchy**: Bold, uppercase, letter-spaced typography for the Logo/Brand, and clean, legible sans-serif for standard links. 
  - **CSS Drivers**: `filter: grayscale(100%) opacity(0.7)` handles the "inactive" state. The transition to `filter: grayscale(0%) opacity(1)` on hover creates the color pop.

* **Step B: Layout & Compositional Style**
  - **Layout System**: CSS Flexbox handles the internal item stacking. Desktop uses `flex-direction: column`, while mobile swaps to `flex-direction: row`.
  - **Whitespace Strategy**: Fixed 5rem width on desktop creates a comfortable gutter. Icons are given a strict `width` and `margin` so they remain perfectly centered regardless of the navbar's overall width.
  - **Alignment**: `margin-top: auto` is applied to the final item (the theme toggle) on desktop to push it securely to the bottom of the column.

* **Step C: Interactive Behavior & Animations**
  - **Hover Expansion**: The `.navbar` element transitions its `width` property over 200ms to smoothly slide open over the main content.
  - **Logo Rotation**: The double-arrow logo uses a CSS `transform: rotate(-180deg)` upon navbar hover to act as a visual "collapse/expand" indicator.
  - **JavaScript**: Kept strictly to functional enhancements, such as toggling a CSS class on the wrapper to flip the CSS variable theme palette.

---

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Responsive Layout Swap | CSS Flexbox + Container Queries | Allows the sidebar to shift from a column (side) to a row (bottom) dynamically based on the component's assigned dimensions, rather than the whole browser window. |
| Grayscale to Color Pop | CSS `filter` | Easily mutes vibrantly colored SVGs without needing complex path color management, then reveals the true color on hover. |
| Duotone Icons | Inline SVGs + Opacity | Replicates premium duotone icon sets by applying the accent color to both SVG paths, but reducing the `opacity` of the secondary path. |
| Hover Expansion | CSS `transition: width` | Pure CSS solution that handles the smooth sliding effect when the user targets the navigation bar. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "CSS Is Cool",
    body_text: str = "I'm baby kale chips affogato ennui lumbersexual, williamsburg paleo quinoa iceland normcore turmeric. Kitsch coloring book retro, seitan schlitz tattooed biodiesel vexillologist neutra. Synth mumblecore deep v, umami selfies normcore gluten-free snackwave.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#ff7eee",     # CSS hex color for accent
    width_px: int = 1000,
    height_px: int = 700,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Expandable Responsive Sidebar visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Calculate theme variables and fallback alt theme
    if color_scheme == "dark":
        theme_css = f"""
    --nav-bg: #23232e;
    --nav-bg-hover: #141418;
    --text-muted: #b6b6b6;
    --text-active: #ececec;
    --content-bg: #0d111c;
    --content-text: #f0f0f0;"""
        alt_theme_css = f"""
    --nav-bg: #ffffff;
    --nav-bg-hover: #f3f4f6;
    --text-muted: #6b7280;
    --text-active: #111827;
    --content-bg: #f8f9fa;
    --content-text: #1a1a2e;"""
    else:
        theme_css = f"""
    --nav-bg: #ffffff;
    --nav-bg-hover: #f3f4f6;
    --text-muted: #6b7280;
    --text-active: #111827;
    --content-bg: #f8f9fa;
    --content-text: #1a1a2e;"""
        alt_theme_css = f"""
    --nav-bg: #23232e;
    --nav-bg-hover: #141418;
    --text-muted: #b6b6b6;
    --text-active: #ececec;
    --content-bg: #0d111c;
    --content-text: #f0f0f0;"""

    css = f"""/* Expandable Vertical-to-Horizontal Responsive Sidebar */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    background: #111; /* External page background */
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Open Sans', system-ui, sans-serif;
}}

/* Component Wrapper Container */
.component-wrapper {{
    width: {width_px}px;
    height: {height_px}px;
    max-width: 100vw;
    max-height: 100vh;
    position: relative;
    overflow: hidden;
    border-radius: 12px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.5);
    background: var(--content-bg);
    color: var(--content-text);
    container-type: inline-size;
    container-name: viewport;
    display: flex;
    flex-direction: row;

    /* Theme Variables */
{theme_css}
    --accent: {accent_color};
    --transition-color: 600ms ease;
    --transition-layout: 200ms ease;
}}

/* Alt Theme Toggled via JS */
.component-wrapper.alt-theme {{
{alt_theme_css}
}}

/* -- Sidebar Navigation -- */
.navbar {{
    position: absolute;
    top: 0;
    left: 0;
    width: 5rem;
    height: 100%;
    background: var(--nav-bg);
    transition: width var(--transition-layout);
    z-index: 100;
    overflow-x: hidden;
    overflow-y: auto;
    border-right: 1px solid rgba(0,0,0,0.1);
}}

/* Hide standard scrollbar for the sleek sidebar */
.navbar::-webkit-scrollbar {{
    display: none;
}}

.navbar:hover {{
    width: 16rem;
}}

.navbar-nav {{
    list-style: none;
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100%;
}}

.nav-item {{
    width: 100%;
}}

.nav-item:last-child {{
    margin-top: auto;
}}

/* -- Links and Icons -- */
.nav-link {{
    display: flex;
    align-items: center;
    height: 5rem;
    color: var(--text-muted);
    text-decoration: none;
    filter: grayscale(100%) opacity(0.7);
    transition: var(--transition-color);
}}

.nav-link:hover, .nav-link:focus-visible {{
    filter: grayscale(0%) opacity(1);
    background: var(--nav-bg-hover);
    color: var(--text-active);
    outline: none;
}}

.nav-link svg {{
    min-width: 2rem;
    width: 2rem;
    margin: 0 1.5rem;
}}

/* Duotone Technique */
svg .primary {{
    fill: var(--accent);
    transition: fill var(--transition-color);
}}

svg .secondary {{
    fill: var(--accent);
    opacity: 0.4;
    transition: fill var(--transition-color);
}}

.link-text {{
    display: none;
    margin-left: 1rem;
    white-space: nowrap;
    font-weight: 600;
    font-size: 1.1rem;
    letter-spacing: 0.05ch;
}}

.navbar:hover .link-text {{
    display: block;
}}

/* -- Logo Specific Styling -- */
.logo {{
    font-weight: bold;
    text-transform: uppercase;
    margin-bottom: 1rem;
    text-align: center;
    background: var(--nav-bg-hover);
    font-size: 1.5rem;
    letter-spacing: 0.3ch;
    width: 100%;
}}

.logo .nav-link {{
    color: var(--text-active);
    filter: none; /* Logo is vibrant by default */
}}

.logo svg {{
    transform: rotate(0deg);
    transition: transform var(--transition-layout);
}}

.navbar:hover .logo svg {{
    transform: rotate(-180deg);
}}

/* -- Main Content Area -- */
.content {{
    height: 100%;
    overflow-y: auto;
    margin-left: 5rem; /* Matches collapsed sidebar width */
    padding: 3rem;
    transition: background var(--transition-layout), color var(--transition-layout);
}}

/* Custom Scrollbar for Content */
.content::-webkit-scrollbar {{
    width: 0.4rem;
}}
.content::-webkit-scrollbar-track {{
    background: var(--content-bg);
}}
.content::-webkit-scrollbar-thumb {{
    background: var(--accent);
    border-radius: 4px;
}}

.content h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 1.5rem;
}}

.content p {{
    font-size: 1.1rem;
    line-height: 1.8;
    margin-bottom: 1.5rem;
    opacity: 0.85;
}}

/* -- Responsive Mobile Swap via Container Queries -- */
@container viewport (max-width: 600px) {{
    .navbar {{
        top: auto;
        bottom: 0;
        width: 100%;
        height: 5rem;
        border-right: none;
        border-top: 1px solid rgba(0,0,0,0.1);
    }}

    .navbar:hover {{
        width: 100%; /* Disable width expansion */
    }}

    .content {{
        margin-left: 0;
        margin-bottom: 5rem;
        padding: 2rem 1.5rem;
    }}

    .navbar-nav {{
        flex-direction: row;
        justify-content: center;
    }}

    .nav-item:last-child {{
        margin-top: 0;
    }}

    .logo {{
        display: none;
    }}

    .nav-link {{
        justify-content: center;
    }}

    .nav-link svg {{
        margin: 0 1rem;
    }}

    .navbar:hover .link-text {{
        display: none; /* Keep text hidden on mobile */
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    
    <div class="component-wrapper">
        
        <nav class="navbar">
            <ul class="navbar-nav">
                
                <li class="logo">
                    <a href="#" class="nav-link">
                        <span class="link-text logo-text">Fireship</span>
                        <svg viewBox="0 0 24 24" aria-hidden="true">
                            <path class="secondary" d="M11 17l5-5-5-5-2 2 3 3-3 3z"/>
                            <path class="primary" d="M5 17l5-5-5-5-2 2 3 3-3 3z"/>
                        </svg>
                    </a>
                </li>

                <li class="nav-item">
                    <a href="#" class="nav-link">
                        <svg viewBox="0 0 24 24" aria-hidden="true">
                            <path class="primary" d="M12 3L2 12h3v8h14v-8h3L12 3z"/>
                            <path class="secondary" d="M10 20v-6h4v6h-4z"/>
                        </svg>
                        <span class="link-text">Home</span>
                    </a>
                </li>

                <li class="nav-item">
                    <a href="#" class="nav-link">
                        <svg viewBox="0 0 24 24" aria-hidden="true">
                            <circle class="primary" cx="12" cy="7" r="5"/>
                            <path class="secondary" d="M4 21c0-4 4-7 8-7s8 3 8 7v1H4v-1z"/>
                        </svg>
                        <span class="link-text">Profile</span>
                    </a>
                </li>

                <li class="nav-item">
                    <a href="#" class="nav-link">
                        <svg viewBox="0 0 24 24" aria-hidden="true">
                            <path class="primary" d="M12 2L8 6v4h8V6l-4-4z"/>
                            <path class="secondary" d="M8 10v6l-4 4v2h16v-2l-4-4v-6H8z"/>
                        </svg>
                        <span class="link-text">Projects</span>
                    </a>
                </li>

                <li class="nav-item" id="themeToggleBtn">
                    <a href="#" class="nav-link">
                        <svg viewBox="0 0 24 24" aria-hidden="true">
                            <path class="primary" d="M12 3c-4.97 0-9 4.03-9 9s4.03 9 9 9 9-4.03 9-9c0-.46-.04-.92-.1-1.36-.98 1.37-2.58 2.26-4.4 2.26-2.98 0-5.4-2.42-5.4-5.4 0-1.81.89-3.42 2.26-4.4C12.92 3.04 12.46 3 12 3z"/>
                        </svg>
                        <span class="link-text">Theme</span>
                    </a>
                </li>

            </ul>
        </nav>

        <main class="content">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <p>Sartorial kogi taxidermy, kickstarter synth yr irony ennui everyday carry retro helvetica stumptown cloud bread squid echo park. Etsy cloud bread sartorial quinoa tacos beard mumblecore shaman tumblr pop-up. Twee retro fingerstache af helvetica pabst 8-bit leggings taiyaki portland ramps tbh tumblr vinyl.</p>
            <p>Neutra humblebrag bushwick portland subway tile plaid, offal scenester flexitarian cliche squid small batch palo santo. Palo santo meh adaptogen +1 3 wolf moon, listicle brunch ethical fanny pack everyday carry fam. Offal fingerstache taxidermy, man bun venmo PBR&B helvetica thundercats everyday carry tote bag artisan cray wolf jianbing.</p>
            <p>Taxidermy thundercats whatever austin, VHS helvetica ethical, dreamcatcher enamel pin YOLO shabby chic locavore man bun crucifix pabst chillwave pop-up vegan. Air plant mlkshk ethical echo park turmeric, whatever crucifix godard scenester locavore pork belly yuccie vape. +1 gochujang put a bird on it, pork belly whatever selfies vaporware occupy banh mi normcore VHS.</p>
            <p>Cornhole normcore hashtag tilde. Hell of yr try-hard DIY raw denim banjo, enamel pin irony polaroid copper mug tofu. Dreamcatcher lomo literally 90's before they sold out, 3 wolf moon banh mi seitan chambray cliche offal tote bag occupy pug.</p>
        </main>

    </div>

    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Expandable Responsive Sidebar Interactive Logic
document.addEventListener('DOMContentLoaded', () => {{
    const themeToggleBtn = document.getElementById('themeToggleBtn');
    const wrapper = document.querySelector('.component-wrapper');

    // Toggle Alternative Color Theme
    themeToggleBtn.addEventListener('click', (e) => {{
        e.preventDefault();
        wrapper.classList.toggle('alt-theme');
    }});
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
```

### 4. Accessibility & Performance Notes

* **Accessibility**: 
  - The SVGs are marked with `aria-hidden="true"` because their adjacent `.link-text` elements provide the necessary semantic labeling for screen readers. 
  - Standard focus states (`:focus-visible`) have been hooked into the same stylistic pipeline as the `:hover` states to ensure the navigation bar behaves predictably and remains navigable when using a keyboard interface.
* **Performance**: 
  - CSS filters (`grayscale(100%)`) on SVGs are hardware accelerated in modern browsers and cost very little to paint, making the color pop highly performant.
  - **Note on Layout Paint Costs**: Animating the `width` property (as done in `.navbar`) theoretically triggers layout reflow calculations during the transition. For extremely complex DOMs, this might drop frames. For a standard layout menu, it is completely acceptable. A higher-performance (but structurally more complex) alternative would involve utilizing `transform: translateX()` coupled with absolute positioned overflow containment.