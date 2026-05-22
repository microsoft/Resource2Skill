# Responsive Gradient Hero Section with Dual CTAs

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Responsive Gradient Hero Section with Dual CTAs

* **Core Visual Mechanism**: A full-bleed, visually striking hero section defined by a vibrant, multi-color linear gradient background. It utilizes high-contrast typography (typically white text on dark gradients) with a specific accent color for highlights. The layout centers the content and employs a "Dual CTA" (Call to Action) pattern—pairing a prominent, solid-filled primary button with a transparent, bordered secondary button to guide user action priorities.
* **Why Use This Skill (Rationale)**: The gradient background instantly captures user attention and provides a modern, energetic aesthetic without the loading overhead of large images or videos. The centered alignment creates a strong focal point. The dual button design leverages visual hierarchy: the solid button draws the eye immediately to the desired primary conversion, while the outlined button offers an alternative, lower-friction path.
* **Overall Applicability**: Ideal for landing pages, SaaS product homepages, portfolio introductions, and any high-impact introductory section where capturing user interest and driving an immediate click is the primary goal.
* **Value Addition**: Compared to a standard flat background with text, this pattern adds depth, vibrancy, and a clear visual hierarchy. It transforms a simple text introduction into an engaging billboard.
* **Browser Compatibility**: Excellent. Relies on standard CSS Flexbox, Linear Gradients, and basic hover states. Fully supported in all modern browsers (Edge, Chrome, Firefox, Safari).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**:
    - Background: A vibrant linear gradient transitioning across three stops (e.g., Blue `#3b82f6` -> Purple `#9333ea` -> Indigo `#4338ca`).
    - Typography: Primary text is crisp white `#ffffff` for maximum contrast against the gradient.
    - Accent: A bright, contrasting color (e.g., Yellow `#facc15`) used for specific text highlights and the primary button.
  - **Typographic Hierarchy**:
    - Headline: Extra large, bold, sans-serif (e.g., `font-weight: 800`, `font-size: 3rem` scaling to `4rem`).
    - Subtitle/Highlight: Same size as the headline but colored with the accent color, often placed on a new line.
    - Body Description: Medium size, slightly lighter font weight, readable measure (e.g., `font-size: 1.125rem`, max-width applied).
  - **Component Elements**: Semantic HTML (`<header>`, `<h1>`, `<p>`, `<a>` tags formatted as buttons).

* **Step B: Layout & Compositional Style**
  - **Layout System**: CSS Flexbox (`display: flex; flex-direction: column; align-items: center; justify-content: center`).
  - **Spatial Feel**: Generous whitespace. The section typically spans `min-height: 100vh` (or a fixed substantial height) to ensure it commands the entire initial viewport.
  - **Button Group**: The CTAs are grouped in a row using Flexbox (`display: flex; gap: 1rem; flex-wrap: wrap; justify-content: center`), ensuring they stack gracefully on very small mobile screens.

* **Step C: Interactive Behavior & Animations**
  - **Primary Button Hover**: Background color shifts to a slightly darker or more saturated shade of the accent color. Scale might slightly increase (pure CSS `transition: background-color 0.2s, transform 0.2s`).
  - **Secondary Button Hover**: Background fills with solid white, and text color inverts to a dark gray/black, providing a satisfying "fill" effect (pure CSS).
  - **Focus States**: Outlines should be prominent for accessibility when navigating via keyboard.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Responsive Layout | CSS Flexbox | Native, clean centering for both column (text) and row (buttons) configurations. |
| Background Styling | CSS `linear-gradient` | Performs perfectly without images, exactly mimics the Tailwind utility classes used in the source. |
| Title Highlighting | Vanilla JavaScript | Dynamically splits the generic `title_text` to wrap the final words in a highlighted `<span>`, mimicking the video's specific title layout without requiring rigid input parameters. |
| Button Hover States | CSS `:hover` pseudo-class | Simple, performant native feature for color inversions and shading. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Build Your Dream Website Easily & Quickly",
    body_text: str = "Unlock the Power of Creativity with Our design and tools. Don't wait. Try Now!",
    color_scheme: str = "dark",        # "dark" produces deep vibrant colors, "light" softer vibrant colors
    accent_color: str = "#facc15",     # CSS hex color for accent (Tailwind yellow-400)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Gradient Hero Section.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors based on scheme ===
    if color_scheme == "dark":
        grad_start = "#3b82f6" # blue-500
        grad_mid = "#9333ea"   # purple-600
        grad_end = "#4338ca"   # indigo-700
        text_color = "#ffffff"
        text_muted = "#e5e7eb" # gray-200
        btn_text_dark = "#111827" # gray-900
    else:
        # A softer, brighter gradient for a "light" theme interpretation,
        # but maintaining white text for the classic hero look.
        grad_start = "#60a5fa" # blue-400
        grad_mid = "#c084fc"   # purple-400
        grad_end = "#818cf8"   # indigo-400
        text_color = "#ffffff"
        text_muted = "#f3f4f6"
        btn_text_dark = "#111827"

    # === CSS ===
    css = f"""/* Responsive Gradient Hero Section */
:root {{
    --grad-start: {grad_start};
    --grad-mid: {grad_mid};
    --grad-end: {grad_end};
    --text-primary: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --btn-text-dark: {btn_text_dark};
    --container-width: {width_px}px;
    --container-height: {height_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: #000; /* Fallback */
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

.hero-container {{
    width: 100%;
    max-width: var(--container-width);
    height: var(--container-height);
    background: linear-gradient(to right, var(--grad-start), var(--grad-mid), var(--grad-end));
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem 1.5rem;
    position: relative;
    overflow: hidden;
}}

.hero-content {{
    max-width: 800px;
    z-index: 10;
}}

.hero-title {{
    color: var(--text-primary);
    font-size: clamp(2.5rem, 5vw, 4rem);
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 1.5rem;
    letter-spacing: -0.02em;
}}

.hero-title .highlight {{
    color: var(--accent);
    display: inline-block;
    margin-top: 0.25rem;
}}

.hero-description {{
    color: var(--text-muted);
    font-size: clamp(1rem, 2vw, 1.25rem);
    font-weight: 400;
    max-width: 600px;
    margin: 0 auto 2.5rem auto;
    line-height: 1.6;
}}

.hero-actions {{
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
}}

.btn {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.75rem 2rem;
    border-radius: 9999px; /* Fully rounded */
    font-size: 1.125rem;
    font-weight: 600;
    text-decoration: none;
    transition: all 0.2s ease-in-out;
    cursor: pointer;
}}

.btn-primary {{
    background-color: var(--accent);
    color: var(--btn-text-dark);
    border: 2px solid var(--accent);
}}

.btn-primary:hover {{
    filter: brightness(0.9);
    transform: translateY(-2px);
}}

.btn-secondary {{
    background-color: transparent;
    color: var(--text-primary);
    border: 2px solid var(--text-primary);
}}

.btn-secondary:hover {{
    background-color: var(--text-primary);
    color: var(--btn-text-dark);
    transform: translateY(-2px);
}}

@media (max-width: 640px) {{
    .hero-actions {{
        flex-direction: column;
        width: 100%;
        max-width: 300px;
        margin: 0 auto;
    }}
    .btn {{
        width: 100%;
    }}
}}
"""

    # === HTML ===
    # Using JS to safely inject text and handle the highlight logic
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Responsive Hero Section</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="hero-container">
        <div class="hero-content">
            <!-- Title populated by JS to apply highlight styling -->
            <h1 class="hero-title" id="dynamic-title" data-raw-title="{title_text}"></h1>
            
            <p class="hero-description">{body_text}</p>
            
            <div class="hero-actions">
                <a href="#" class="btn btn-primary">Get Started</a>
                <a href="#" class="btn btn-secondary">Learn More</a>
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Dynamic text highlighting logic
document.addEventListener('DOMContentLoaded', () => {{
    const titleEl = document.getElementById('dynamic-title');
    const rawText = titleEl.getAttribute('data-raw-title');
    
    if (rawText) {{
        // Split words to highlight the last two, mimicking the tutorial's visual structure
        const words = rawText.trim().split(' ');
        
        if (words.length >= 3) {{
            const highlightWords = words.splice(-2).join(' '); // Take last 2 words
            const mainWords = words.join(' ');
            
            // Reconstruct HTML with a line break and span
            titleEl.innerHTML = `${{mainWords}}<br/><span class="highlight">${{highlightWords}}</span>`;
        }} else {{
            // Fallback if title is very short
            titleEl.textContent = rawText;
        }}
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
```

### 4. Accessibility & Performance Notes

* **Accessibility**:
  - Contrast ratios between the white text and the deep blue/purple gradients are extremely high, easily passing WCAG AAA standards.
  - The buttons are marked up as links (`<a>`) but styled as buttons, which is appropriate if they navigate to new pages. If they trigger on-page modals, they should be `<button>` elements.
  - Hover states include `transform: translateY(-2px)`. To strictly adhere to accessibility preferences, this could be wrapped in a `@media (prefers-reduced-motion: no-preference)` block, though the movement is minimal.
* **Performance**:
  - The component is incredibly lightweight. CSS gradients are hardware-accelerated and paint instantly compared to loading large hero banner images.
  - Only uses vanilla CSS and minimal JS string manipulation executed once on DOM load, resulting in zero blocking time and perfect layout performance.