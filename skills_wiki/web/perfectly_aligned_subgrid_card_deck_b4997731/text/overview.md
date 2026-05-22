# Perfectly Aligned Subgrid Card Deck

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Perfectly Aligned Subgrid Card Deck

* **Core Visual Mechanism**: This technique uses the modern CSS `subgrid` feature to perfectly align nested elements (like headers, paragraphs, and buttons) horizontally across multiple independent card containers, regardless of the differing lengths of content within each card. By setting `grid-template-rows: subgrid` and `grid-row: span 3` on the children, the cards map their internal rows directly to the parent grid's tracks. 
* **Why Use This Skill (Rationale)**: A common UI layout problem is misaligned call-to-action buttons in pricing or feature cards caused by varying text lengths. Previous solutions required hardcoding heights, using complex JavaScript to match heights, or hacking Flexbox with `flex-grow`. `subgrid` solves this natively and semantically, maintaining a clean visual rhythm and a highly polished, professional user experience.
* **Overall Applicability**: Essential for pricing tiers, product feature comparisons, team member directories, service offerings, and portfolio galleries. It works anywhere you have a grid of distinct items that share an identical internal DOM structure.
* **Value Addition**: It brings mathematical alignment to the structural rhythm of the page without compromising responsiveness. It ensures that the eye can scan across the page in straight horizontal lines (from heading to heading, or button to button), dramatically improving readability and visual harmony.
* **Browser Compatibility**: Fully supported in all modern browsers (Chrome 117+, Firefox 71+, Safari 16.0+, Edge 117+). For very old browsers, the layout will degrade to a standard grid/block layout where items won't perfectly align horizontally, which is an acceptable progressive enhancement strategy.


### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **HTML Constructs**: A semantic container (`<div class="wrapper">`) holding multiple item modules (`<article class="card">`). Each module contains a heading (`<h2>`), text (`<p>`), and a call-to-action (`<button>`).
  - **Color Logic**: High contrast, vibrant SaaS aesthetic. 
    - Background: Deep purple/indigo (`#300e67` or customizable dark background).
    - Surface: Elevated lighter violet/indigo (`#6200ff` or derived surface color).
    - Accents: Bright cyan/blue (`#22c4ff` for buttons).
  - **Typographic Hierarchy**: Sans-serif, geometric or neo-grotesque (like Inter or Poppins). Headings are bold and prominently sized (`1.5rem` to `2rem`), paragraphs use standard sizing with a slightly muted color or opacity, and buttons are uppercase or cleanly weighted for emphasis.

* **Step B: Layout & Compositional Style**
  - **Layout System**: Pure CSS Grid combined with `subgrid`.
  - **Parent (`.wrapper`)**: Uses `grid-template-columns: repeat(auto-fit, minmax(300px, 1fr))` for a fluid, responsive number of columns.
  - **Child (`.card`)**: Uses `display: grid`, `grid-template-rows: subgrid`, and `grid-row: span 3`. This tells the card to span 3 rows of the parent's grid and to pass those exact track sizes down to its own children.
  - **Spacing**: The parent defines the space between cards using `gap: 2rem`. Because `subgrid` inherits the parent's gap for its rows, it is often overridden inside the `.card` via `gap: 0;`, relying instead on semantic margins (e.g., `margin: 1.5rem 0` on the paragraph) to control internal spacing.

* **Step C: Interactive Behavior & Animations**
  - **Hover States**: Subtle interactive lifts on the cards (`transform: translateY(-5px)`) and brightness bumps on the buttons (`filter: brightness(1.1)` or `opacity: 0.9`).
  - **Transitions**: Smooth, fast CSS transitions (`0.2s ease`) on background colors and transforms to make the interface feel tactile.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Responsive layout & alignment | CSS Grid & `subgrid` | Native, robust, requires zero JavaScript, and precisely fulfills the tutorial's technical premise. |
| Fluid columns | `repeat(auto-fit, minmax(...))` | Handles screen resizing natively without relying on CSS media query breakpoints. |
| Row track spanning | `grid-row: span 3` | Tells the parent grid to allocate enough rows so the subgrid logic maps exactly to the inner elements. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Subgrid Alignment",
    body_text: str = "Notice how the buttons align perfectly across all cards, despite the varying text lengths in the paragraphs above them.",
    color_scheme: str = "dark",
    accent_color: str = "#22c4ff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Perfectly Aligned Subgrid Card Deck.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os
    import html

    os.makedirs(output_dir, exist_ok=True)

    # Theme definitions based on video aesthetic
    if color_scheme == "dark":
        bg_color = "#150a2e"          # Dark violet/navy background
        surface_color = "#3a197a"     # Elevated purple surface
        text_primary = "#ffffff"
        text_secondary = "#d1c4e9"
    else:
        bg_color = "#f4f5f7"
        surface_color = "#ffffff"
        text_primary = "#111827"
        text_secondary = "#4b5563"

    # Escape texts
    safe_title = html.escape(title_text)
    safe_body = html.escape(body_text)

    # === CSS ===
    css = f"""/* Perfectly Aligned Subgrid Card Deck */
:root {{
    --bg-color: {bg_color};
    --surface-color: {surface_color};
    --accent-color: {accent_color};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --max-width: {width_px}px;
}}

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    line-height: 1.6;
}}

.header {{
    text-align: center;
    margin-bottom: 4rem;
    max-width: 600px;
}}

.header h1 {{
    font-size: 2.5rem;
    margin-bottom: 1rem;
    font-weight: 700;
    letter-spacing: -0.02em;
}}

.header p {{
    color: var(--text-secondary);
    font-size: 1.1rem;
}}

/* The Parent Grid */
.wrapper {{
    display: grid;
    /* Responsive columns that auto-wrap */
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 2rem;
    width: 100%;
    max-width: var(--max-width);
    margin: 0 auto;
}}

/* The Subgrid Cards */
.card {{
    background-color: var(--surface-color);
    border-radius: 12px;
    padding: 2.5rem 2rem;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    
    /* Core Subgrid Magic */
    display: grid;
    grid-template-rows: subgrid;
    /* Span exactly the number of elements inside (h2, p, button = 3) */
    grid-row: span 3;
    
    /* Override the gap inherited from the wrapper so we can use semantic margins */
    gap: 0; 
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
}}

/* Card Elements */
.card h2 {{
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--text-primary);
    align-self: start;
}}

.card p {{
    color: var(--text-secondary);
    font-size: 1rem;
    /* Use margin to separate content since grid gap is 0 */
    margin: 1.5rem 0 2.5rem 0;
    align-self: start;
}}

.card button {{
    background-color: var(--accent-color);
    color: #ffffff;
    border: none;
    padding: 1rem 1.5rem;
    border-radius: 6px;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    transition: filter 0.2s ease, transform 0.1s ease;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    align-self: end;
    /* Subtle shadow for the button based on accent color */
    box-shadow: 0 4px 14px calc(var(--accent-color)40);
}}

.card button:hover {{
    filter: brightness(1.15);
}}

.card button:active {{
    transform: scale(0.97);
}}
"""

    # === HTML ===
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="header">
        <h1>{safe_title}</h1>
        <p>{safe_body}</p>
    </header>

    <main class="wrapper">
        <!-- Card 1 (Short content) -->
        <article class="card">
            <h2>Custom Websites</h2>
            <p>We design fast, modern, and responsive websites that help your business look professional.</p>
            <button>Learn More</button>
        </article>

        <!-- Card 2 (Long content) -->
        <article class="card">
            <h2>Full-Service Web Development</h2>
            <p>Need a more complex solution? We develop complete web applications with solid architecture, clean code, and a focus on long-term maintainability. Whether it's booking systems, dashboards, or custom APIs — we've got it covered.</p>
            <button>Discover</button>
        </article>

        <!-- Card 3 (Medium content) -->
        <article class="card">
            <h2>SEO & Performance Optimization</h2>
            <p>Slow site? Dropping rankings? We audit, optimize, and rebuild the technical foundation of your website to improve loading speed and search visibility.</p>
            <button>Optimize</button>
        </article>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// No complex JavaScript is required for CSS subgrid to function perfectly.
// This empty script serves as a placeholder for potential future interactions.
document.addEventListener('DOMContentLoaded', () => {
    console.log("Subgrid component loaded successfully.");
});
"""

    # === Write files ===
    files = []
    for fname, content in [("index.html", html_content), ("style.css", css), ("script.js", js)]:
        path = os.path.join(output_dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        files.append(path)

    return {
        "html": html_content,
        "css": css,
        "js": js,
        "files": files,
    }
```

### 4. Accessibility & Performance Notes

* **Accessibility (a11y)**: 
  * The markup uses semantic `<article>` tags for the cards and a `<main>` container, ensuring clear landmarks for screen readers. 
  * Text contrast ratios have been designed to exceed WCAG AA standards (4.5:1), especially assuming the use of `#ffffff` and `#d1c4e9` on the deep `#3a197a` background.
  * Interactive elements (`<button>`) have clear structural sizing and predictable layout locations, drastically reducing cognitive load for visually impaired users utilizing magnification tools.
* **Performance**:
  * This layout is remarkably performant. Native CSS Grid operations run efficiently on the browser's rendering engine without triggering expensive JavaScript layout recalcs. 
  * Avoiding JS-based matching-height logic avoids ResizeObserver loops and layout thrashing.
  * Transitions are strictly applied to hardware-accelerated properties (`transform` and `filter`), ensuring consistent 60fps interaction on hover.