# Accent-Banded Pricing Cards

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Accent-Banded Pricing Cards

* **Core Visual Mechanism**: A dark-themed, 3-column layout built with CSS Flexbox. The design relies on high contrast—using a deep background (`#191a1f`) combined with slightly lighter card surfaces (`#24272e`) to create subtle depth. The hallmark of the style is the bold, solid-fill "banner" across the upper-middle of each card that highlights the price and contract duration using a vivid accent color (e.g., `#fd3c4d`), instantly drawing the eye.
* **Why Use This Skill (Rationale)**: Pricing tables are critical conversion elements. By utilizing a dark mode aesthetic, the bright red (or any primary accent) creates a strong focal point exactly where the user needs to look (the price). The repetitive card structure reinforces comparison, while Flexbox handles responsive wrapping naturally across devices.
* **Overall Applicability**: SaaS pricing pages, gym/membership subscription tiers, service packages, and landing page conversion sections.
* **Value Addition**: It translates a standard unordered list of features into a scannable, visually prioritized decision matrix. The added hover lift and shadow interactions provide a tactile "clickable" feel that encourages interaction.
* **Browser Compatibility**: Excellent. Relies on standard CSS Flexbox and variables. Supported on all modern browsers (Chrome 21+, Firefox 28+, Safari 6.1+).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Containers**: A wrapper section containing a Flexbox grid of cards (`div` elements). 
  - **Color Logic (Dark Theme)**: 
    - App Background: `#191a1f`
    - Card Background: `#24272e`
    - Accent Banner/Buttons: `#fd3c4d`
    - Text: `#ffffff`
  - **Typographic Hierarchy**: Sans-serif (`Inter` or `Arial`), capitalized headings (`text-transform: uppercase`), heavy weights for the price and titles (`700`), and standard weights for feature lists.
  - **Visual Anchors**: The checkmarks (`&#10003;`) colored in the accent hue tie the list visually to the main banner and button.

* **Step B: Layout & Compositional Style**
  - **Grid/Layout**: `display: flex` with `flex-wrap: wrap` and `justify-content: center`.
  - **Card Proportions**: Each card utilizes `flex: 1 1 300px` (or similar constraints like `max-width: 350px`) to ensure they stay uniformly sized and wrap gracefully when the viewport shrinks below ~900px.
  - **Spacing**: Generous padding inside the cards (`25px` or `30px`) creates breathability. A horizontal line separator (styled div with reduced opacity) organizes the space between the header and features.

* **Step C: Interactive Behavior & Animations**
  - **Hover Effects**: The cards physically elevate (`transform: translateY(-10px)`) and cast a wider, darker shadow on hover (`box-shadow`), providing immediate tactile feedback. 
  - **Buttons**: The CTA buttons scale up slightly (`transform: scale(1.05)`) and brighten on hover.
  - **On-load**: A staggered sequential fade-in via JavaScript adds polish when the pricing section enters the viewport.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Responsive Grid** | CSS Flexbox | `flex-wrap: wrap` with a `flex-basis` creates a perfectly fluid layout without explicit media queries. |
| **Card Depth** | CSS `box-shadow` & Backgrounds | Using distinct background hex codes creates surface separation; shadows add physical depth. |
| **Icons** | HTML Entity `&#10003;` | Lightweight, native checkmarks avoiding external icon library dependencies. |
| **Entrance Animation** | JS `setTimeout` | Simple, effective way to stagger the appearance of the 3 cards sequentially. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "PRICING FOR YOU",
    body_text: str = "Choose the plan that best fits your goals.",
    color_scheme: str = "dark",
    accent_color: str = "#fd3c4d",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 'Accent-Banded Pricing Cards' visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme colors configuration
    if color_scheme == "dark":
        bg_color = "#191a1f"
        card_bg = "#24272e"
        text_color = "#ffffff"
        text_muted = "rgba(255, 255, 255, 0.7)"
        shadow_base = "rgba(0, 0, 0, 0.2)"
        shadow_hover = "rgba(0, 0, 0, 0.4)"
    else:
        bg_color = "#f0f2f5"
        card_bg = "#ffffff"
        text_color = "#1a1a2e"
        text_muted = "rgba(0, 0, 0, 0.6)"
        shadow_base = "rgba(0, 0, 0, 0.05)"
        shadow_hover = "rgba(0, 0, 0, 0.15)"

    # Format title to highlight the first word
    words = title_text.split()
    if len(words) > 0:
        first_word = words[0]
        rest_of_title = " ".join(words[1:])
        formatted_title = f"<span>{first_word}</span> {rest_of_title}"
    else:
        formatted_title = f"<span>{title_text}</span>"

    # Static data for cards
    plans = [
        {
            "name": "Beginner Plan",
            "price": "$50",
            "contract": "1 Month Contract",
            "features": ["Classes 2 Weeks", "Open Gym Monday-Friday", "Yoga Relax classes", "Free drinking package"]
        },
        {
            "name": "Advanced Plan",
            "price": "$150",
            "contract": "6 Month Contract",
            "features": ["Classes 6 Weeks", "Open Gym Monday-Friday", "Yoga Relax classes", "Free drinking package"]
        },
        {
            "name": "Pro Plan",
            "price": "$250",
            "contract": "12 Month Contract",
            "features": ["Classes 9 Weeks", "Open Gym Monday-Friday", "Yoga Relax classes", "Free drinking package"]
        }
    ]

    cards_html = ""
    for plan in plans:
        features_html = "".join([f"<li><span class=\"check\">&#10003;</span> {f}</li>" for f in plan['features']])
        cards_html += f"""
            <div class="pricing-card">
                <h4>{plan['name']}</h4>
                <div class="head">
                    <h3>{plan['price']}</h3>
                    <p>{plan['contract']}</p>
                </div>
                <div class="line"></div>
                <ul class="feature">
                    {features_html}
                </ul>
                <div class="btn-container">
                    <a href="#" class="btn">Get Started</a>
                </div>
            </div>
        """

    # === CSS ===
    css = f"""/* Accent-Banded Pricing Cards — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-main: {bg_color};
    --bg-card: {card_bg};
    --text-main: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --shadow-base: {shadow_base};
    --shadow-hover: {shadow_hover};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-main);
    color: var(--text-main);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow-x: hidden;
}}

.pricing-section {{
    width: 100%;
    max-width: var(--width);
    padding: 60px 20px;
}}

.header-container {{
    text-align: center;
    margin-bottom: 50px;
}}

.pricing-title {{
    font-size: 2.2rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 10px;
}}

.pricing-title span {{
    color: var(--accent);
}}

.pricing-subtitle {{
    color: var(--text-muted);
    font-size: 1.1rem;
}}

.pricing-table {{
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 30px;
    max-width: 1100px;
    margin: 0 auto;
}}

.pricing-card {{
    background-color: var(--bg-card);
    flex: 1 1 300px;
    max-width: 340px;
    text-align: center;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 10px 30px var(--shadow-base);
    
    /* Animation defaults */
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 0.6s ease, transform 0.6s cubic-bezier(0.2, 0.8, 0.2, 1);
}}

/* JS Triggers this class */
.pricing-card.visible {{
    opacity: 1;
    transform: translateY(0);
}}

.pricing-card.visible:hover {{
    transform: translateY(-10px);
    box-shadow: 0 15px 40px var(--shadow-hover);
    /* Transition specifically for the hover state, maintaining opacity */
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}}

.pricing-card h4 {{
    color: var(--text-main);
    text-transform: uppercase;
    padding: 25px 0;
    font-size: 1.1rem;
    letter-spacing: 1px;
}}

.pricing-card .head {{
    background-color: var(--accent);
    color: #ffffff; /* Always white text on accent backgrounds */
    padding: 20px 0;
}}

.pricing-card .head h3 {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 5px;
}}

.pricing-card .head p {{
    font-size: 0.95rem;
    font-weight: 500;
    opacity: 0.95;
}}

.pricing-card .line {{
    background-color: var(--accent);
    width: 70%;
    height: 2px;
    margin: 25px auto;
    opacity: 0.4;
}}

.pricing-card ul {{
    list-style: none;
    padding: 0 20px;
    margin-bottom: 25px;
}}

.pricing-card li {{
    color: var(--text-main);
    margin-bottom: 15px;
    font-size: 0.95rem;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
}}

.pricing-card li .check {{
    color: var(--accent);
    font-weight: bold;
    font-size: 1.1rem;
}}

.pricing-card .btn-container {{
    padding: 0 20px 30px;
}}

.pricing-card .btn {{
    display: inline-block;
    background-color: var(--accent);
    color: #ffffff;
    text-decoration: none;
    width: 85%;
    padding: 14px 0;
    border-radius: 30px;
    text-transform: uppercase;
    font-weight: 600;
    font-size: 0.9rem;
    letter-spacing: 1px;
    transition: background-color 0.3s ease, transform 0.2s ease;
}}

.pricing-card .btn:hover {{
    filter: brightness(1.15);
    transform: scale(1.05);
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
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <section class="pricing-section">
        <div class="header-container">
            <h2 class="pricing-title">{formatted_title}</h2>
            <p class="pricing-subtitle">{body_text}</p>
        </div>
        
        <div class="pricing-table">
{cards_html}
        </div>
    </section>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Accent-Banded Pricing Cards — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const cards = document.querySelectorAll('.pricing-card');
    
    // Sequential fade-in and slide-up animation on load
    cards.forEach((card, index) => {{
        setTimeout(() => {{
            card.classList.add('visible');
        }}, 150 * (index + 1)); // Stagger by 150ms
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
  - Structural hierarchy uses `h2`, `h3`, and `h4` correctly. 
  - Standard HTML checkmark entities `&#10003;` are used instead of icon fonts. To make it strictly screen-reader friendly, `aria-hidden="true"` could be appended to the checkmark spans, though visually they are understandable.
  - Color contrast on the `accent` bands utilizes explicit `#ffffff` text regardless of the theme to ensure it remains legible against vivid accent colors (like red/blue).
* **Performance**: 
  - The design relies exclusively on GPU-accelerated CSS properties (`transform` and `opacity`) for hover and entrance animations.
  - Uses CSS Flexbox, guaranteeing no Javascript layout thrashing or window resize listener bottlenecks.
  - The entrance animation uses a low-impact initialization `setTimeout` routine that triggers existing CSS transitions.