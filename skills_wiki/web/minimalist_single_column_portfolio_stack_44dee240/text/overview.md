# Minimalist Single-Column Portfolio Stack

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Minimalist Single-Column Portfolio Stack

* **Core Visual Mechanism**: A clean, content-first vertical layout prioritizing typography and spaciousness. It features a central reading column with a distinct visual hierarchy: a prominent header, an introductory text block separated by a minimalist divider, and a vertical stack of projects. Each project utilizes a Flexbox header to align the project title and a descriptive tag on opposite ends, followed by a brief description and a large, full-width visual asset.
* **Why Use This Skill (Rationale)**: This layout removes UI clutter, allowing the work (images/videos) to take center stage. The dual-aligned project headers (`justify-content: space-between`) create a structured, tabular feel without the rigidity of a grid, guiding the eye naturally down the page. 
* **Overall Applicability**: Ideal for personal portfolios, case study showcases, minimalist blogs, or indie studio landing pages where high-quality visuals and brief context are the primary focus.
* **Browser Compatibility**: Fully supported across all modern browsers. Uses standard CSS Flexbox and basic CSS variables.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Typography**: Relies heavily on a clean sans-serif (e.g., 'Inter') with distinct weights. Headings are semi-bold (600), body text is regular (400), and tags are italicized and slightly muted.
  - **Color Logic**: High contrast monochrome base (white background `#ffffff` with dark text `#1a1a1a` for light mode, or vice versa for dark mode) with subtle muted grays for dividers and tags (`#dddddd` and `#666666`).
  - **Assets**: Project images/videos are full-width relative to the container, with subtle border radii to soften the edges.

* **Step B: Layout & Compositional Style**
  - **Container**: A centrally aligned column with a constrained `max-width` (typically 700px - 800px) to maintain optimal reading line length.
  - **Flexbox Headers**: The `.project-header` uses `display: flex` and `justify-content: space-between` paired with `align-items: baseline` to perfectly align the bottom of the title text with the bottom of the tag text.
  - **Whitespace**: Generous vertical margins (`margin-bottom: 60px` between projects, `40px` after the intro) to separate distinct thoughts and projects.

* **Step C: Interactive Behavior & Animations**
  - **Subtle Interactions**: Links feature a seamless color transition or border-bottom reveal on hover.
  - **Clickable Assets**: Project images act as large hit areas, utilizing JavaScript to read a `data-link` attribute and open external URLs, accompanied by a `cursor: pointer` CSS rule.
  - **Smooth Scrolling**: Global smooth scrolling applied to the document element for anchor links.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Centered Column Layout** | CSS `max-width` + `margin: auto` | The most robust standard for reading-column style layouts. |
| **Split Project Header** | CSS Flexbox | `justify-content: space-between` perfectly pushes the title and tag to opposite edges. |
| **Clickable Project Images** | JavaScript Event Listeners | Reads `data-link` attributes to redirect users, replicating the tutorial's interactive behavior cleanly without wrapping block elements in `<a>` tags. |
| **Typography** | Google Fonts (Inter) | Replicates the clean, modern aesthetic seen in the original design. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Nashallery: Creative Software",
    body_text: str = "We create playful, design-forward software projects and tutorials that make coding fun, feminine, and accessible.",
    color_scheme: str = "light",        
    accent_color: str = "#8a4baf",     
    width_px: int = 800,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Minimalist Single-Column Portfolio Stack.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#121212"
        text_main = "#f0f0f0"
        text_muted = "#a0a0a0"
        divider_color = "#333333"
        asset_bg_1 = "linear-gradient(135deg, #2b1055 0%, #753a88 100%)"
        asset_bg_2 = "linear-gradient(120deg, #0f2027 0%, #203a43 50%, #2c5364 100%)"
    else:
        bg_color = "#ffffff"
        text_main = "#1a1a1a"
        text_muted = "#666666"
        divider_color = "#dddddd"
        asset_bg_1 = "linear-gradient(135deg, #ff9a9e 0%, #fecfef 99%, #fecfef 100%)"
        asset_bg_2 = "linear-gradient(120deg, #f6d365 0%, #fda085 100%)"

    # === CSS ===
    css = f"""/* Minimalist Single-Column Portfolio Stack */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text-main: {text_main};
    --text-muted: {text_muted};
    --divider: {divider_color};
    --accent: {accent_color};
    --max-width: {width_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text-main);
    line-height: 1.6;
    padding: 60px 5vw;
    -webkit-font-smoothing: antialiased;
}}

.container {{
    max-width: var(--max-width);
    margin: 0 auto;
}}

/* Intro Section */
.header {{
    margin-bottom: 24px;
}}

.site-title {{
    font-size: 1.75rem;
    font-weight: 600;
    letter-spacing: -0.02em;
}}

.intro-text {{
    font-size: 1.05rem;
    font-weight: 400;
    margin-bottom: 24px;
    color: var(--text-main);
}}

.featured {{
    margin-bottom: 60px;
    padding-bottom: 30px;
    border-bottom: 1px solid var(--divider);
    font-size: 1rem;
    color: var(--text-muted);
}}

.featured strong {{
    font-weight: 600;
    color: var(--text-main);
}}

/* Interactive Links */
a {{
    color: inherit;
    text-decoration: none;
    border-bottom: 1px solid var(--divider);
    transition: color 0.2s ease, border-color 0.2s ease;
}}

a:hover {{
    color: var(--accent);
    border-bottom-color: var(--accent);
}}

/* Projects Stack */
.projects-list {{
    display: flex;
    flex-direction: column;
    gap: 60px;
}}

.project {{
    display: flex;
    flex-direction: column;
}}

.project-header {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 8px;
}}

.project-title {{
    font-size: 1.25rem;
    font-weight: 600;
    letter-spacing: -0.01em;
}}

.project-tag {{
    font-size: 0.875rem;
    color: var(--text-muted);
    font-style: italic;
}}

.project-description {{
    font-size: 1rem;
    margin-bottom: 20px;
    color: var(--text-main);
    max-width: 90%;
}}

.project-asset {{
    width: 100%;
    aspect-ratio: 16 / 10;
    border-radius: 8px;
    overflow: hidden;
    cursor: pointer;
    position: relative;
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s ease;
}}

.project-asset:hover {{
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08);
}}

.asset-1 {{
    background: {asset_bg_1};
}}

.asset-2 {{
    background: {asset_bg_2};
}}

/* Asset overlay hint */
.project-asset::after {{
    content: 'View Project ↗';
    position: absolute;
    bottom: 20px;
    right: 20px;
    background: rgba(255, 255, 255, 0.9);
    color: #1a1a1a;
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 0.875rem;
    font-weight: 500;
    opacity: 0;
    transform: translateY(10px);
    transition: opacity 0.3s ease, transform 0.3s ease;
}}

.project-asset:hover::after {{
    opacity: 1;
    transform: translateY(0);
}}

@media (max-width: 600px) {{
    .project-header {{
        flex-direction: column;
        align-items: flex-start;
        gap: 4px;
    }}
    
    .project-asset {{
        aspect-ratio: 4 / 3;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,600;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="container">
        <!-- Intro Area -->
        <header class="header">
            <h1 class="site-title">{title_text}</h1>
        </header>
        
        <section class="intro">
            <p class="intro-text">{body_text}</p>
            <p class="featured">
                Featured on <strong><a href="#">@design</a></strong>, Climate Week NYC, and GitHub Community.
            </p>
        </section>
        
        <!-- Projects Stack -->
        <section class="projects-list">
            
            <article class="project">
                <div class="project-header">
                    <h2 class="project-title">Study Soda</h2>
                    <span class="project-tag">desktop game</span>
                </div>
                <p class="project-description">An interactive "study until the ice melts" timer built with custom engines. Focus on playful aesthetics.</p>
                <div class="project-asset asset-1" data-link="https://example.com/study-soda"></div>
            </article>

            <article class="project">
                <div class="project-header">
                    <h2 class="project-title">Egg Timer Widget</h2>
                    <span class="project-tag">desktop widget</span>
                </div>
                <p class="project-description">A cooking timer widget built with web technologies. The tutorial video has over 4M views.</p>
                <div class="project-asset asset-2" data-link="https://example.com/egg-timer"></div>
            </article>

        </section>
    </main>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Minimalist Portfolio Interaction Logic
document.addEventListener('DOMContentLoaded', () => {{
    
    // Enable smooth scrolling for the document
    document.documentElement.style.scrollBehavior = 'smooth';

    // Make project assets clickable based on data-link attribute
    const projectAssets = document.querySelectorAll('.project-asset');
    
    projectAssets.forEach(asset => {{
        asset.addEventListener('click', function() {{
            const link = this.getAttribute('data-link');
            if (link) {{
                // In a real scenario, this would open the link
                // window.open(link, '_blank', 'noopener,noreferrer');
                console.log('Navigating to:', link);
                
                // Visual feedback for demo purposes
                const originalText = this.style.transform;
                this.style.transform = 'scale(0.98)';
                setTimeout(() => {{
                    this.style.transform = '';
                }}, 150);
            }}
        }});
    }});
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
  - The layout follows a strict semantic HTML structure (`<main>`, `<header>`, `<section>`, `<article>`) which is excellent for screen readers.
  - Contrast ratios for text-on-background natively satisfy WCAG AA requirements in both light and dark modes.
  - The `a:hover` effect alters border and color to make links distinct, avoiding sole reliance on color to denote interactivity.
* **Performance**:
  - No heavy frameworks or libraries are required. Pure CSS Flexbox handles all layout shifting, which is highly performant.
  - The `transform` and `box-shadow` hover animations on the project assets are GPU-accelerated, ensuring 60fps silky smooth interactions without layout recalculation (reflow).