# Animated Duotone SVGs & Staggered Keyframe Sequences

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Animated Duotone SVGs & Staggered Keyframe Sequences

* **Core Visual Mechanism**: This pattern relies on combining inline `<svg>` markup with modern CSS features. By breaking an SVG into discrete `<g>` (groups) and `<path>` elements, it applies CSS variables (`var(--dark-color)`) for dynamic duotone theming. It uses CSS `transition` for interactive element swapping (e.g., sliding path elements on hover to create an infinite forward motion illusion) and `@keyframes` combined with inline variables (`style="--order: N"`) to create complex, perfectly staggered looping sequences.
* **Why Use This Skill (Rationale)**: SVGs are resolution-independent and lightweight. By offloading the animation and state logic entirely to CSS instead of relying on heavy JavaScript animation libraries or raster GIFs, the resulting components are extremely performant, easily themeable on the fly, and highly interactive. The staggered drop-in animation specifically directs the user's eye and adds a premium, polished feel to data visualization or UI mockups.
* **Overall Applicability**: Ideal for interactive buttons, feature highlights on SaaS landing pages, animated product mockups, loading sequences, and dynamic data dashboards.
* **Value Addition**: Transforms static vector graphics into engaging micro-interactions. The use of dynamic CSS variables allows a single SVG component to instantly adapt its color palette based on user interaction, state changes, or global themes (dark/light mode).
* **Browser Compatibility**: Fully supported in all modern browsers. Uses standard CSS Custom Properties, `calc()`, CSS Grid, and CSS Animations.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Inline SVGs**: Graphics are embedded directly in the HTML Document Object Model (DOM), giving CSS direct access to their inner paths and groups.
  - **Duotone Palette**: Controlled by global CSS variables on the `:root`:
    - `--dark-color` (e.g., primary accent `#00bfff`)
    - `--light-color` (e.g., secondary/pastel `#80e9ff`)
  - **Styling Hooks**: SVG groups `<g id="lightGroup">` and `<g id="darkGroup">` receive the `fill: var(--color)` instruction, automatically distributing the theme to child paths.

* **Step B: Layout & Compositional Style**
  - **Container Setup**: A responsive flexbox or grid layout acts as the presentation layer.
  - **ViewBox Coordinate System**: The SVGs utilize the `viewBox` attribute (e.g., `viewBox="0 0 100 100"`), meaning all internal CSS `translateX()` and `translateY()` values map directly to the vector coordinate space rather than screen pixels. This ensures the animation remains perfectly proportional regardless of the screen size.

* **Step C: Interactive Behavior & Animations**
  - **Hover Swapping (The Fast-Forward Effect)**: Uses `transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1)`. On hover, an invisible shape on the left translates into the center and fades in (`opacity: 1`), while the rightmost shape translates out and fades away (`opacity: 0`). This creates a continuous sliding illusion.
  - **Staggered Keyframes (The Phone Mockup)**:
    - Uses `@keyframes dropIn` manipulating `opacity` and `transform: translateY()`.
    - Every animated element receives an inline HTML variable: `style="--order: 1"`, `style="--order: 2"`, etc.
    - The CSS applies an offset delay via math: `animation-delay: calc(var(--order) * 200ms)`.
  - **JavaScript Theming**: A simple `onclick` event overrides the `--dark-color` and `--light-color` values on the root document, triggering a smooth, hardware-accelerated color transition across all SVGs.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Vector Rendering** | Inline HTML `<svg>` | Grants CSS and JS direct DOM access to specific graphic nodes (paths, groups), which isn't possible via `<img>` tags. |
| **Hover Animations** | CSS `transition` | GPU-accelerated and simple; moving specific paths using `translateX` and `opacity` handles the interactive visual swapping perfectly. |
| **Staggered Sequence** | `@keyframes` + `calc()` | Using inline CSS variables (`--order`) allows a single `@keyframes` rule to stagger an infinite amount of elements without needing bloated CSS classes (`.delay-1`, `.delay-2`). |
| **Dynamic Colors** | CSS Variables + JS Event | Updating root custom properties via JavaScript instantly propagates new colors to the SVGs, maintaining the duotone look flawlessly. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Animated Vector Graphics",
    body_text: str = "Combining inline SVGs with CSS variables and keyframes.",
    color_scheme: str = "dark",
    accent_color: str = "#635bff",
    width_px: int = 1000,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Duotone SVGs & Staggered Keyframes visual effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme definitions
    if color_scheme == "dark":
        bg_color = "#0a0c10"
        card_bg = "#161b22"
        text_color = "#f0f6fc"
        surface_color = "#21262d"
        light_accent = "#80e9ff"
    else:
        bg_color = "#f6f8fa"
        card_bg = "#ffffff"
        text_color = "#24292f"
        surface_color = "#e1e4e8"
        light_accent = "#80e9ff"

    # === CSS ===
    css = f"""/* Duotone SVG & Staggered Keyframes */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --card-bg: {card_bg};
    --text: {text_color};
    --surface: {surface_color};
    
    /* Duotone Theming Variables */
    --dark-color: {accent_color};
    --light-color: {light_accent};
    
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow-x: hidden;
    transition: background-color 0.4s ease;
}}

.header {{
    text-align: center;
    margin-bottom: 3rem;
}}

.header h1 {{
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}}

.header p {{
    color: var(--text);
    opacity: 0.7;
}}

.layout-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 2rem;
    width: 100%;
    max-width: var(--width);
    padding: 0 2rem;
}}

.card {{
    background: var(--card-bg);
    border: 1px solid var(--surface);
    border-radius: 1.5rem;
    padding: 2.5rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    box-shadow: 0 20px 40px rgba(0,0,0,0.05);
    min-height: 400px;
}}

.card h3 {{
    font-size: 1.25rem;
    margin-bottom: 0.5rem;
}}

.card p {{
    font-size: 0.9rem;
    opacity: 0.7;
    margin-bottom: 2rem;
}}

.demo-area {{
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
}}

/* =========================================
   Interactive Fast-Forward Icon 
   ========================================= */
#ff-icon {{
    cursor: pointer;
    overflow: visible; /* Prevents clipping during transforms */
}}

/* Animate color fills and path transforms smoothly */
#ff-icon path, #ff-icon g {{
    transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}}

/* Apply Duotone Colors */
#lightGroup {{ fill: var(--light-color); }}
#darkGroup {{ fill: var(--dark-color); }}

/* Initial State: dark2 is pushed to the left and hidden */
#dark2 {{
    transform: translateX(-20px);
    opacity: 0;
}}

/* Hover State: Shift elements to simulate infinite progression */
#ff-icon:hover #light1 {{
    transform: translateX(20px);
}}
#ff-icon:hover #dark1 {{
    transform: translateX(20px);
    opacity: 0;
}}
#ff-icon:hover #dark2 {{
    transform: translateX(20px);
    opacity: 1;
}}

/* =========================================
   Staggered Phone Sequence
   ========================================= */
   
/* 1. Skeleton Text Fade Up */
@keyframes fadeInUp {{
    from {{ opacity: 0; transform: translateY(15px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

#skeletonGroup rect {{
    opacity: 0;
    animation: fadeInUp 1.2s ease forwards;
}}

/* 2. Staggered Drop In Loop */
@keyframes dropIn {{
    0%, 10% {{ opacity: 0; transform: translateY(-30px); }}
    20%, 80% {{ opacity: 1; transform: translateY(0); }}
    90%, 100% {{ opacity: 0; transform: translateY(0); }}
}}

.stagger-item {{
    opacity: 0;
    /* Infinite loop with dynamic delay */
    animation: dropIn 6s cubic-bezier(0.34, 1.56, 0.64, 1) infinite forwards;
    animation-delay: calc(var(--order) * 150ms);
}}

/* SVG inner fills for dynamic theme matching */
.card-shell {{ fill: var(--card-bg); stroke: var(--surface); }}
.skeleton-bar {{ fill: var(--surface); }}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="header">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </div>

    <div class="layout-grid">
        <!-- Interactive Icon Demo -->
        <div class="card">
            <h3>Interactive Duotone</h3>
            <p>Hover to trigger internal path transitions. Click to randomize the CSS root variables.</p>
            <div class="demo-area">
                <!-- Inline SVG Fast Forward Icon -->
                <svg viewBox="0 0 100 100" width="140" height="140" id="ff-icon">
                    <g id="lightGroup">
                        <path id="light1" d="M30,20 L70,50 L30,80 Z" opacity="0.6"/>
                    </g>
                    <g id="darkGroup">
                        <!-- Placed exactly 20 units offset from each other -->
                        <path id="dark1" d="M50,20 L90,50 L50,80 Z"/>
                        <path id="dark2" d="M10,20 L50,50 L10,80 Z"/>
                    </g>
                </svg>
            </div>
        </div>

        <!-- Staggered Sequence Demo -->
        <div class="card">
            <h3>Staggered Keyframes</h3>
            <p>Infinite loop powered by standard CSS <code>@keyframes</code> and inline <code>--order</code> variables.</p>
            <div class="demo-area">
                <!-- Inline SVG Phone Mockup -->
                <svg viewBox="0 0 200 300" width="180" height="270">
                    <!-- Phone Body -->
                    <rect x="10" y="10" width="180" height="280" rx="20" class="card-shell" stroke-width="4"/>
                    <rect x="70" y="20" width="60" height="6" rx="3" class="skeleton-bar"/>
                    
                    <!-- One-time Fade In -->
                    <g id="skeletonGroup">
                        <rect x="30" y="50" width="140" height="24" rx="12" class="skeleton-bar"/>
                        <rect x="30" y="85" width="90" height="12" rx="6" class="skeleton-bar"/>
                    </g>
                    
                    <!-- Looping Staggered Items -->
                    <g class="stagger-item" style="--order: 1">
                        <rect x="30" y="120" width="60" height="60" rx="10" class="skeleton-bar"/>
                        <circle cx="60" cy="150" r="14" fill="var(--dark-color)"/>
                    </g>
                    <g class="stagger-item" style="--order: 2">
                        <rect x="110" y="120" width="60" height="60" rx="10" class="skeleton-bar"/>
                        <circle cx="140" cy="150" r="14" fill="var(--light-color)"/>
                    </g>
                    <g class="stagger-item" style="--order: 3">
                        <rect x="30" y="195" width="60" height="60" rx="10" class="skeleton-bar"/>
                        <circle cx="60" cy="225" r="14" fill="var(--dark-color)"/>
                    </g>
                    <g class="stagger-item" style="--order: 4">
                        <rect x="110" y="195" width="60" height="60" rx="10" class="skeleton-bar"/>
                        <circle cx="140" cy="225" r="14" fill="var(--light-color)"/>
                    </g>
                </svg>
            </div>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Interactive Duotone SVG - JS Logic
document.addEventListener('DOMContentLoaded', () => {
    const icon = document.getElementById('ff-icon');
    
    // Aesthetic duotone palettes
    const palettes = [
        ['#635bff', '#80e9ff'], // Stripe Purple / Cyan
        ['#ff4500', '#ffd700'], // OrangeRed / Gold
        ['#00e599', '#00d4ff'], // Emerald / Light Blue
        ['#e11d48', '#fbcfe8'], // Rose / Light Pink
        ['#8a2be2', '#ff69b4'], // BlueViolet / HotPink
        ['#10b981', '#a7f3d0']  // Tailwind Green
    ];
    
    let currentPaletteIndex = 0;

    icon.addEventListener('click', () => {
        // Increment and wrap around
        currentPaletteIndex = (currentPaletteIndex + 1) % palettes.length;
        
        // Destructure the chosen palette
        const [darkColor, lightColor] = palettes[currentPaletteIndex];
        
        // Push changes to the CSS Root
        document.documentElement.style.setProperty('--dark-color', darkColor);
        document.documentElement.style.setProperty('--light-color', lightColor);
    });
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
  - Since the graphic serves an illustrative or interactive purpose, the `<svg>` elements ideally should contain `<title>` tags internally or an `aria-label` attribute if utilized as a real functional button.
  - Users with vestibular disorders may experience discomfort with looping animations. Consider adding a `@media (prefers-reduced-motion: reduce)` block in the CSS to set `.stagger-item { animation: none; opacity: 1; }` and disable the hover path transforms.
* **Performance**: 
  - **High Performance**: SVGs manipulated entirely via CSS `transform` and `opacity` are incredibly cheap for the browser to render, heavily utilizing hardware acceleration without triggering expensive DOM layouts or repaints.
  - Leveraging `calc()` with CSS variables removes the need to loop through nodes in JavaScript to assign inline delays or maintain complex animation state logic, shifting the heavy lifting exclusively to the CSS rendering engine.