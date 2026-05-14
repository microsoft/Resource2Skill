# Asymmetric Split-Panel Pricing Table

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Asymmetric Split-Panel Pricing Table

* **Core Visual Mechanism**: This pattern relies on a highly contrasting, two-pane asymmetric split layout (typically 35% / 65% on desktop). The smaller, visually heavy side acts as an emotional anchor, featuring a vibrant, color-tinted full-bleed background image overlaid with a human-centric testimonial. The larger side provides a clean, high-contrast, distraction-free "functional" zone for the actual pricing cards and conversion buttons.
* **Why Use This Skill (Rationale)**: By physically separating the *emotional* appeal (testimonial and rich imagery) from the *logical* decision-making process (pricing tiers and feature lists), it reduces cognitive load. The user feels the brand identity on the left, but reads the data clearly on the right. 
* **Overall Applicability**: Ideal for SaaS pricing pages, high-ticket e-commerce subscription checkouts, and premium service landing pages where building trust (via testimonials) is just as important as feature comparison.
* **Value Addition**: Transforms a standard, boring grid of pricing cards into a cohesive storytelling element. The responsive pivot—from a vertical stack on mobile to a horizontal split on desktop—keeps the emotional anchor visible without pushing the pricing data out of the viewport.
* **Browser Compatibility**: Excellent. Relies on standard CSS Flexbox, `mix-blend-mode` for image tinting, and `calc()` for sizing. Supported in all modern browsers (Chrome 88+, Safari 14+, Firefox 85+).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**: A dominant accent color creates a translucent overlay on the image pane using `mix-blend-mode: multiply` to preserve image texture while enforcing brand color. The pricing side relies on strict monochrome contrast (e.g., `#ffffff` background with `#1a1a2e` text) to maximize legibility.
  - **Typographic Hierarchy**: Uses a clean, geometric sans-serif (e.g., *Jost* or *Inter*). The price itself is visually dominant (`~2.5rem`, bold), establishing immediate visual hierarchy. Features are lighter and smaller.
  - **CSS Constructs**: `background-image` combined with absolute pseudo-elements (`::before`) for overlays. `box-shadow` provides elevation to the cards, pulling them off the flat canvas.

* **Step B: Layout & Compositional Style**
  - **Layout System**: A mobile-first CSS Flexbox architecture.
    - Mobile: `flex-direction: column`. The hero anchor sits at the top.
    - Desktop (`> 768px`): `flex-direction: row`. The container splits `flex: 0 0 35%` and `flex: 1` (65%).
    - Desktop Large (`> 1000px`): The inner pricing cards pivot from a single column to a side-by-side flex layout.
  - **Spatial Feel**: Generous padding (`2rem` to `3rem`) within the cards and around the container prevents the dense feature lists from feeling claustrophobic.

* **Step C: Interactive Behavior & Animations**
  - **Hover States**: The Call-to-Action buttons feature a subtle brightness shift and vertical lift (`transform: translateY(-2px)`) on hover, driven by a `0.3s ease` transition.
  - **Selection Logic (JS)**: Clicking a card elevates it and paints its border with the accent color, giving the user immediate visual feedback on their chosen tier.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Responsive Split Layout | CSS Flexbox | Native, clean transitions between column and row layouts across 3 distinct breakpoints. |
| Image Color Tinting | `mix-blend-mode` + pseudo-element | Allows the Python script to inject *any* HEX accent color over a photo without requiring pre-edited RGBA values. |
| Component Styling | CSS Variables (`--var`) | Ensures seamless theming (Light/Dark modes and Accent swapping) directly from the function parameters. |
| Plan Selection Interaction | Vanilla JavaScript | Simple event listeners to apply an "active" state, highlighting the user's choice. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Choose your plan",
    body_text: str = "Let's deliver your groceries to your house every month.",
    color_scheme: str = "light",       # "dark" or "light"
    accent_color: str = "#d32f2f",     # CSS hex color for accent (e.g., Strawberry Red)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 'Asymmetric Split-Panel Pricing Table' visual effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        panel_bg = "#0d111c"
        card_bg = "#1a1f33"
        text_primary = "#ffffff"
        text_muted = "#9ca3af"
        shadow_color = "rgba(0, 0, 0, 0.4)"
        border_color = "#2d3748"
    else:
        panel_bg = "#f9fafb"
        card_bg = "#ffffff"
        text_primary = "#111827"
        text_muted = "#4b5563"
        shadow_color = "rgba(0, 0, 0, 0.08)"
        border_color = "#e5e7eb"

    # === CSS ===
    css = f"""/* Asymmetric Split-Panel Pricing Table — generated component */
@import url('https://fonts.googleapis.com/css2?family=Jost:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --accent: {accent_color};
    --panel-bg: {panel_bg};
    --card-bg: {card_bg};
    --text-primary: {text_primary};
    --text-muted: {text_muted};
    --shadow: {shadow_color};
    --border: {border_color};
    
    --comp-width: {width_px}px;
    --comp-height: {height_px}px;
}}

body {{
    font-family: 'Jost', sans-serif;
    background-color: #e2e8f0; /* Neutral canvas for preview */
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

.pricing-wrapper {{
    display: flex;
    flex-direction: column;
    width: 100%;
    max-width: var(--comp-width);
    min-height: var(--comp-height);
    background-color: var(--panel-bg);
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}}

/* Left Panel: Emotional Anchor */
.hero-panel {{
    position: relative;
    padding: 4rem 2rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    background-image: url('https://images.unsplash.com/photo-1516684732162-798a0062be99?auto=format&fit=crop&w=1000&q=80');
    background-size: cover;
    background-position: center;
    color: #ffffff;
    min-height: 350px;
}}

.hero-panel::before {{
    content: '';
    position: absolute;
    inset: 0;
    background-color: var(--accent);
    mix-blend-mode: multiply;
    opacity: 0.85;
    z-index: 1;
}}

.hero-content {{
    position: relative;
    z-index: 2;
    max-width: 320px;
}}

.avatar {{
    width: 80px;
    height: 80px;
    border-radius: 50%;
    border: 3px solid rgba(255, 255, 255, 0.4);
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
}}

.testimonial {{
    font-size: 1.1rem;
    font-style: italic;
    line-height: 1.6;
    margin-bottom: 1rem;
    opacity: 0.95;
}}

.author {{
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    font-size: 0.85rem;
}}

/* Right Panel: Functional UI */
.pricing-panel {{
    padding: 3rem 2rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    flex: 1;
}}

.pricing-header {{
    text-align: center;
    margin-bottom: 3rem;
}}

.pricing-header h2 {{
    font-size: 2.5rem;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
    font-weight: 600;
}}

.pricing-header p {{
    color: var(--text-muted);
    font-size: 1.1rem;
}}

.cards-container {{
    display: flex;
    flex-direction: column;
    gap: 2rem;
    width: 100%;
    max-width: 800px;
}}

.pricing-card {{
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 2.5rem 2rem;
    text-align: center;
    box-shadow: 0 10px 25px var(--shadow);
    transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
    display: flex;
    flex-direction: column;
    position: relative;
    overflow: hidden;
    cursor: pointer;
}}

.pricing-card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 20px 40px var(--shadow);
}}

.pricing-card.active {{
    border-color: var(--accent);
    box-shadow: 0 0 0 2px var(--accent), 0 20px 40px var(--shadow);
}}

.card-icon {{
    width: 64px;
    height: 64px;
    margin: 0 auto 1.5rem;
    color: var(--text-primary);
}}

.card-title {{
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
}}

.card-price {{
    font-size: 3rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.25rem;
}}

.card-price span {{
    font-size: 1rem;
    font-weight: 400;
    color: var(--text-muted);
}}

.card-features {{
    list-style: none;
    margin: 2rem 0;
    flex: 1;
}}

.card-features li {{
    color: var(--text-muted);
    margin-bottom: 0.75rem;
    font-size: 0.95rem;
}}

.card-features li.highlight {{
    color: var(--accent);
    font-weight: 600;
    text-transform: uppercase;
    font-size: 0.85rem;
    letter-spacing: 0.5px;
    margin-top: 1.5rem;
}}

.btn {{
    background-color: var(--accent);
    color: #ffffff;
    border: none;
    padding: 1rem;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: filter 0.2s ease;
    font-family: inherit;
    width: 100%;
}}

.btn:hover {{
    filter: brightness(1.15);
}}

/* Breakpoints */
@media (min-width: 768px) {{
    .pricing-wrapper {{
        flex-direction: row;
    }}
    .hero-panel {{
        flex: 0 0 35%;
        padding: 4rem;
    }}
    .pricing-panel {{
        flex: 1;
        padding: 4rem;
    }}
}}

@media (min-width: 1024px) {{
    .cards-container {{
        flex-direction: row;
        align-items: stretch;
    }}
    .pricing-card {{
        flex: 1;
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
    <div class="pricing-wrapper">
        
        <!-- Emotion / Trust Panel -->
        <div class="hero-panel">
            <div class="hero-content">
                <img src="https://i.pravatar.cc/150?img=68" alt="User Avatar" class="avatar">
                <p class="testimonial">"Lorem ipsum dolor sit amet consectetur adipisicing elit. A officia sunt quia, Eaque laborum veritatis eius consectetur asperiores eos, accusantium illum provident."</p>
                <span class="author">John Doe</span>
            </div>
        </div>

        <!-- Functional / Data Panel -->
        <div class="pricing-panel">
            <div class="pricing-header">
                <h2>{title_text}</h2>
                <p>{body_text}</p>
            </div>

            <div class="cards-container">
                
                <!-- Card 1 -->
                <div class="pricing-card" data-plan="discounted">
                    <!-- Inline SVG Shopping Bag -->
                    <svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
                        <line x1="3" y1="6" x2="21" y2="6"></line>
                        <path d="M16 10a4 4 0 0 1-8 0"></path>
                    </svg>
                    <h3 class="card-title">Discounted monthly</h3>
                    <div class="card-price">$65<span>/mo</span></div>
                    
                    <ul class="card-features">
                        <li>Bag will include:</li>
                        <li>Fresh fruits</li>
                        <li>Fresh vegetables</li>
                        <li>Fresh proteins of your choice</li>
                        <li>Canned tomatoes</li>
                        <li>Whole wheat pasta</li>
                        <li class="highlight">Discounted Shipping</li>
                    </ul>
                    
                    <button class="btn">Choose this plan</button>
                </div>

                <!-- Card 2 -->
                <div class="pricing-card active" data-plan="free">
                    <!-- Inline SVG Tote Bag -->
                    <svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                        <rect x="4" y="6" width="16" height="16" rx="2" ry="2"></rect>
                        <path d="M8 6V4a4 4 0 0 1 8 0v2"></path>
                        <path d="M12 11v4"></path>
                    </svg>
                    <h3 class="card-title">Free monthly delivery</h3>
                    <div class="card-price">$105<span>/mo</span></div>
                    
                    <ul class="card-features">
                        <li>Bag will include:</li>
                        <li>Fresh fruits</li>
                        <li>Fresh vegetables</li>
                        <li>Fresh proteins of your choice</li>
                        <li>Canned tomatoes</li>
                        <li>Whole wheat pasta</li>
                        <li class="highlight">Free Shipping</li>
                    </ul>
                    
                    <button class="btn">Choose this plan</button>
                </div>

            </div>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Asymmetric Split-Panel Pricing Table — Interactive Behavior
document.addEventListener('DOMContentLoaded', () => {{
    const pricingCards = document.querySelectorAll('.pricing-card');

    pricingCards.forEach(card => {{
        // Add click listener to select a specific plan
        card.addEventListener('click', () => {{
            // Remove active class from all cards
            pricingCards.forEach(c => c.classList.remove('active'));
            
            // Add active class to clicked card
            card.classList.add('active');
            
            // Optional: You could dispatch a custom event here for framework integrations
            const planName = card.getAttribute('data-plan');
            console.log(`User selected the ${{planName}} plan.`);
        }});
        
        // Prevent button click from bubbling up multiple times if needed
        const btn = card.querySelector('.btn');
        if(btn) {{
            btn.addEventListener('click', (e) => {{
                e.stopPropagation(); // Stop parent card click
                // Set this card as active anyway
                pricingCards.forEach(c => c.classList.remove('active'));
                card.classList.add('active');
                
                alert("Plan selected! (Demo interaction)");
            }});
        }}
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
  - Structural HTML elements (`<ul>`, `<li>`, `<h2>`, `<h3>`) correctly format the document hierarchy.
  - Form controls (`<button>`) are used for actions rather than styled divs.
  - Color blending (`mix-blend-mode: multiply`) ensures the white text on the emotional anchor panel maintains a high WCAG contrast ratio, regardless of the underlying image's brightness, because the accent color establishes a dark baseline.
* **Performance**:
  - The layout relies purely on the browser's native CSS Flexbox rendering. There are no expensive JS layout recalculations.
  - The `mix-blend-mode` property is hardware-accelerated on modern browsers.
  - Hover animations target `transform` and `box-shadow` which do not trigger costly layout reflows (unlike animating `padding` or `margin`).