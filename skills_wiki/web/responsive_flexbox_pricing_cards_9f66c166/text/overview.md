# Responsive Flexbox Pricing Cards

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Responsive Flexbox Pricing Cards

* **Core Visual Mechanism**: A clean, high-contrast, three-column card layout emphasizing conversion. The defining visual signature is the bold, colored block behind the price that spans the full width of the card, breaking up the white space. Custom pseudo-element bullets (checkmarks/arrows) reinforce the feature list, and ghost buttons invite interaction by filling with solid color on hover.
* **Why Use This Skill (Rationale)**: This pattern effectively compartmentalizes complex purchasing decisions. By aligning features horizontally and utilizing a distinct accent color for the price and CTA (Call to Action), the user's eye naturally flows from Tier -> Price -> Features -> Action. Flexbox ensures the cards stretch to equal heights, creating a neat, symmetrical grid regardless of feature list length.
* **Overall Applicability**: Perfect for SaaS product landing pages, subscription-based service sites, membership tiers, and agency pricing pages.
* **Value Addition**: Replaces a boring, hard-to-read HTML `<table>` with a mobile-first, digestible card format. The visual distinction of the price blocks makes the cost hierarchy immediately obvious.
* **Browser Compatibility**: Fully compatible with all modern browsers. Uses standard CSS Flexbox, pseudo-elements, and media queries. No bleeding-edge or experimental features used.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  * **Typography**: 'Poppins' (or similar geometric sans-serif). Strong hierarchy: Card titles are moderate (`22px`), Prices are massive (`2.5rem`), and feature text is standard (`16px`).
  * **Color Logic**:
    * Main Background: Dark gray (`#333333`) or light gray (`#f8f9fa`) depending on theme.
    * Card Background: White (`#ffffff`), creating a stark contrast against a dark page background.
    * Accent Color: Vibrant Green (`#93cb52`) used for price block backgrounds, checkmarks, and button hover states.
    * Text: Dark (`#333333`) inside the white cards to ensure readability.
  * **CSS Constructs**: Heavy reliance on `margin` and `padding` for breathing room. The price block achieves its full-bleed look inside a padded container by using negative horizontal margins or simply by not padding the parent container horizontally.

* **Step B: Layout & Compositional Style**
  * **Layout System**: CSS Flexbox (`display: flex`). The parent row centers the cards, and each card column uses `flex: 1` to distribute space equally.
  * **Spatial Feel**: Generous vertical padding (`2rem 0`). The cards use `gap` or `margin` to separate from one another (`1rem` or `2rem`).
  * **Alignment**: Card titles and prices are center-aligned (`text-align: center`), while the feature lists are left-aligned (`text-align: left`) with a left margin to keep them centered visually as a block.

* **Step C: Interactive Behavior & Animations**
  * **Hover Effects**: "Ghost" buttons (transparent with solid border) transition to solid backgrounds with white text on hover. Transition duration is `0.4s` for a smooth fill effect.
  * **Responsiveness**: At `768px`, the flex direction switches from `row` to `column`, stacking the cards vertically with a gap between them.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Card Layout & Stacking** | CSS Flexbox | Simplest and most robust way to ensure equal-height columns that collapse to rows on mobile. |
| **Custom List Bullets** | CSS `::before` pseudo-element | Avoids adding extra HTML spans or loading heavy icon fonts. Uses native unicode characters (`\2714` for checkmark). |
| **Hover Transitions** | CSS `transition: all 0.4s` | Hardware-accelerated, simple, and requires no JavaScript. |
| **Responsive Design** | CSS `@media` queries | Native approach to trigger the `flex-direction: column` shift at tablet breakpoints. |

*Feasibility Assessment*: 100%. The visual effect demonstrated in the tutorial can be completely and perfectly reproduced using standard HTML and CSS, packaged with a small JS script for interactivity.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Choose Your Plan",
    body_text: str = "Simple, transparent pricing for everyone.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#93cb52",     # Default green from the tutorial
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Pricing Table visual effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme handling (Note: Cards are always white to match tutorial contrast style)
    if color_scheme == "dark":
        bg_color = "#333333"
        header_text_color = "#ffffff"
        card_shadow = "none"
    else:
        bg_color = "#f4f7f6"
        header_text_color = "#333333"
        card_shadow = "0 10px 30px rgba(0,0,0,0.08)"

    # === CSS ===
    css = f"""/* Responsive Pricing Table */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap');

*, *::before, *::after {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

:root {{
    --bg-main: {bg_color};
    --header-text: {header_text_color};
    --accent: {accent_color};
    --card-bg: #ffffff;
    --card-text: #333333;
}}

body {{
    font-family: 'Poppins', sans-serif;
    background: var(--bg-main);
    color: var(--header-text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

.page-header {{
    text-align: center;
    margin-bottom: 3rem;
}}

.page-header h1 {{
    font-size: 2.5rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}}

.page-header p {{
    font-size: 1.1rem;
    font-weight: 300;
    opacity: 0.8;
}}

.container {{
    width: 100%;
    max-width: {width_px}px;
    margin: 0 auto;
}}

.tbl_row {{
    display: flex;
    justify-content: center;
    align-items: stretch;
    gap: 2rem;
}}

.tbl_col {{
    flex: 1;
    background: var(--card-bg);
    color: var(--card-text);
    border-radius: 8px;
    text-align: center;
    padding: 2.5rem 0;
    box-shadow: {card_shadow};
    overflow: hidden;
    transition: transform 0.3s ease;
}}

.tbl_col:hover {{
    transform: translateY(-5px);
}}

/* Card Title */
.tbl_col > p {{
    font-size: 22px;
    font-weight: 500;
    letter-spacing: 1px;
    text-transform: uppercase;
}}

/* Price Block */
.tbl_col h3 {{
    font-size: 3rem;
    margin: 20px 0 40px;
    font-weight: 600;
    background: var(--accent);
    color: #ffffff;
    padding: 25px 0;
}}

.tbl_col h3 span {{
    font-size: 1.2rem;
    font-weight: 400;
    opacity: 0.9;
}}

/* Feature List */
.tbl_col ul {{
    text-align: left;
    margin: 0 auto;
    width: max-content;
    list-style: none;
    margin-bottom: 40px;
}}

.tbl_col ul li {{
    margin: 1.2rem 0;
    font-size: 15px;
    font-weight: 400;
    position: relative;
    padding-left: 25px;
}}

/* Custom Bullet (Checkmark) */
.tbl_col ul li::before {{
    content: "\\2714"; /* Unicode Checkmark */
    color: var(--accent);
    position: absolute;
    left: 0;
    font-size: 16px;
    font-weight: bold;
}}

/* Button */
.tbl_col button {{
    width: 75%;
    border: 2px solid var(--accent);
    background: transparent;
    color: var(--card-text);
    padding: 14px 0;
    border-radius: 5px;
    font-size: 16px;
    font-weight: 500;
    font-family: inherit;
    cursor: pointer;
    transition: all 0.4s ease;
}}

.tbl_col button:hover {{
    background: var(--accent);
    color: #ffffff;
}}

/* Responsive Breakpoint */
@media (max-width: 850px) {{
    .tbl_row {{
        flex-direction: column;
        align-items: center;
    }}
    
    .tbl_col {{
        width: 100%;
        max-width: 450px;
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
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="page-header">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </div>

    <div class="container">
        <div class="tbl_row">
            <!-- Card 1 -->
            <div class="tbl_col">
                <p>Basic</p>
                <h3>$2.95 <span>/ Month</span></h3>
                <ul>
                    <li>Top Features</li>
                    <li>1 Website</li>
                    <li>10 GB SSD Storage</li>
                    <li>Custom Themes</li>
                    <li>24/7 Customer Support</li>
                    <li>Free Domain 1 Year</li>
                </ul>
                <button class="select-btn" data-plan="Basic">Select Now</button>
            </div>

            <!-- Card 2 -->
            <div class="tbl_col">
                <p>Plus</p>
                <h3>$5.45 <span>/ Month</span></h3>
                <ul>
                    <li>Top Features</li>
                    <li>Unlimited Websites</li>
                    <li>20 GB SSD Storage</li>
                    <li>Custom Themes</li>
                    <li>24/7 Customer Support</li>
                    <li>Free Domain 1 Year</li>
                </ul>
                <button class="select-btn" data-plan="Plus">Select Now</button>
            </div>

            <!-- Card 3 -->
            <div class="tbl_col">
                <p>Choice Plus</p>
                <h3>$13.95 <span>/ Month</span></h3>
                <ul>
                    <li>Top Features</li>
                    <li>Unlimited Websites</li>
                    <li>40 GB SSD Storage</li>
                    <li>Custom Themes</li>
                    <li>24/7 Customer Support</li>
                    <li>Free Domain 1 Year</li>
                </ul>
                <button class="select-btn" data-plan="Choice Plus">Select Now</button>
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Pricing Table Interactions
document.addEventListener('DOMContentLoaded', () => {{
    const buttons = document.querySelectorAll('.select-btn');

    buttons.forEach(button => {{
        button.addEventListener('click', (e) => {{
            const planName = e.target.getAttribute('data-plan');
            
            // Visual feedback
            const originalText = e.target.innerText;
            e.target.innerText = 'Processing...';
            e.target.style.opacity = '0.8';
            
            // Simulate action
            setTimeout(() => {{
                alert(`You have selected the ${{planName}} plan!`);
                e.target.innerText = originalText;
                e.target.style.opacity = '1';
            }}, 400);
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

#### 3c. Verification Checklist

- [x] Does the code produce valid HTML5 that passes basic validation?
- [x] Does `index.html` work when opened directly in a browser (`file://` protocol)?
- [x] Are all color values explicit hex or rgba?
- [x] Are all external resources loaded from CDN URLs? (Google Fonts Poppins included)
- [x] Does the component respect the `width_px` parameters via `max-width`?
- [x] Does `color_scheme="dark"` produce a dark theme and `"light"` a light theme?
- [x] Does `accent_color` propagate to all accent elements (price background, borders, bullets, hover states)?
- [x] Does the JavaScript run without console errors?
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect?

### 4. Accessibility & Performance Notes

* **Accessibility**:
  * The contrast ratio between the white card background (`#ffffff`) and the dark text (`#333333`) is well above the WCAG AA minimum.
  * *Improvement applied*: Added `button` elements instead of standard `div`s for the "Select Now" elements. Buttons are naturally focusable and can be triggered via the Keyboard (`Enter` / `Space`), making the pricing table immediately keyboard accessible.
  * If the accent color is changed to a very light color, ensure the price text inside the `h3` is altered to dark text to maintain contrast. Currently, white text on the green accent `#93cb52` borders on low contrast (WCAG warns about light green + white), but accurately reproduces the tutorial's aesthetic.
* **Performance**:
  * **Exceptional**: This layout relies purely on CSS Flexbox and pseudo-elements. There are no images, no heavy SVGs, and no complex JS calculations. Rendering is incredibly fast.
  * Transitions are limited to `transform` and `background/color`, ensuring no reflow/repaint jank during interactions.