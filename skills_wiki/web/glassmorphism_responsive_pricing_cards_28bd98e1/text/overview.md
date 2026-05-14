# Glassmorphism Responsive Pricing Cards

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Glassmorphism Responsive Pricing Cards

* **Core Visual Mechanism**: The defining visual idea is the "frosted glass" aesthetic (Glassmorphism). This is achieved by combining a semi-transparent background color (`rgba`), a background blur effect (`backdrop-filter: blur()`), and a subtle, semi-transparent border to simulate a physical edge. When layered over a vibrant, complex, or photographic background, it creates a sense of depth and hierarchy without completely obscuring the underlying context.
* **Why Use This Skill (Rationale)**: Glassmorphism provides a modern, premium feel. It separates foreground content (pricing data) from background imagery gracefully, maintaining readability while keeping the design visually rich and integrated. The smooth hover transitions on the call-to-action buttons add tactile feedback.
* **Overall Applicability**: Highly applicable for SaaS pricing pages, feature comparison grids, subscription tier displays, or any dashboard widget where you want to present distinct blocks of information over a unified background image or gradient.
* **Browser Compatibility**: Requires modern browsers for `backdrop-filter` support. Fallbacks gracefully to a simple semi-transparent background in older browsers (like older versions of IE/Edge), though the blur effect will be missing. `-webkit-backdrop-filter` is required for Safari.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Containers**: Simple semantic HTML (`div`, `ul`, `li`, `h2`, `hr`, `a`).
  - **Color Logic (Dark Theme)**:
    - Card Background: `rgba(255, 255, 255, 0.1)` (10% white)
    - Card Border: `rgba(255, 255, 255, 0.2)` (20% white)
    - Text: `#ffffff`
    - Button Default: `rgba(21, 23, 24, 0.7)` (Dark gray/black translucent)
  - **Typographic Hierarchy**:
    - Uses a clean sans-serif (Roboto in the original, 'Inter' configured below).
    - Huge emphasis on the price (`96px`), standardizing titles (`36px`), and smaller detail text (`16px`).
  - **CSS Properties**: `backdrop-filter: blur(10px)` is the heavy lifter.

* **Step B: Layout & Compositional Style**
  - **Layout System**: CSS Grid is used for the main card container (`display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 4%;`). This ensures cards stretch and distribute evenly.
  - **Whitespace**: Generous padding (`50px` on desktop) inside the cards gives the content room to breathe, enhancing the premium feel.
  - **Responsiveness**: Media queries adapt the grid from 3 columns to 2 (`max-width: 1024px`), and then to 1 column (`max-width: 768px`), simultaneously scaling down internal padding and massive font sizes to prevent overflow.

* **Step C: Interactive Behavior & Animations**
  - **Hover Effects**: The Call-to-Action (CTA) button features a simple but effective background color transition (`transition: background 0.3s ease;`) to draw user focus.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Frosted glass overlay | CSS `backdrop-filter` | Native CSS feature, hardware-accelerated, perfect for this effect without needing canvas/JS. |
| Card Layout | CSS Grid | Simplest and most robust way to create equal-width, flexible columns that wrap easily on smaller screens. |
| Responsiveness | CSS Media Queries | Handles the layout shifts (3 -> 2 -> 1 columns) and typography scaling natively. |

> **Feasibility Assessment**: 100%. The visual effect from the tutorial is entirely achievable using pure HTML and CSS. JavaScript is not strictly required for the core visual rendering, making it highly performant.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Choose Your Plan",
    body_text: str = "Select the perfect plan for your needs. Upgrade or downgrade at any time.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Glassmorphism Pricing Cards visual effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Configure theme variables based on color_scheme
    if color_scheme == "dark":
        text_color = "#ffffff"
        text_muted = "rgba(255, 255, 255, 0.7)"
        bg_image = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=2564&auto=format&fit=crop"
        card_bg = "rgba(255, 255, 255, 0.05)"
        card_border = "rgba(255, 255, 255, 0.15)"
        btn_bg = "rgba(0, 0, 0, 0.5)"
        btn_text = "#ffffff"
        btn_hover_text = "#ffffff"
    else:
        text_color = "#1a1a2e"
        text_muted = "rgba(26, 26, 46, 0.7)"
        bg_image = "https://images.unsplash.com/photo-1550684848-fac1c5b4e853?q=80&w=2670&auto=format&fit=crop"
        card_bg = "rgba(255, 255, 255, 0.3)"
        card_border = "rgba(255, 255, 255, 0.5)"
        btn_bg = "rgba(255, 255, 255, 0.6)"
        btn_text = "#1a1a2e"
        btn_hover_text = "#ffffff"

    # === CSS ===
    css = f"""/* Glassmorphism Pricing Cards — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --text-main: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --card-bg: {card_bg};
    --card-border: {card_border};
    --btn-bg: {btn_bg};
    --btn-text: {btn_text};
    --btn-hover-text: {btn_hover_text};
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    color: var(--text-main);
    background-image: url('{bg_image}');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    background-repeat: no-repeat;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px 20px;
}}

.header {{
    text-align: center;
    margin-bottom: 60px;
    max-width: 800px;
    /* Apply a subtle text shadow to ensure readability over complex backgrounds */
    text-shadow: 0 2px 10px rgba(0,0,0,0.2);
}}

.header h1 {{
    font-size: clamp(2.5rem, 5vw, 3.5rem);
    font-weight: 700;
    margin-bottom: 16px;
}}

.header p {{
    font-size: 1.1rem;
    color: var(--text-muted);
    line-height: 1.6;
}}

.container {{
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
}}

.grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 30px;
    align-items: stretch;
}}

.card {{
    background: var(--card-bg);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--card-border);
    border-radius: 24px;
    padding: 40px 30px;
    display: flex;
    flex-direction: column;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}}

.card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 30px 60px rgba(0, 0, 0, 0.15);
}}

.card_title {{
    font-size: 1.5rem;
    font-weight: 500;
    margin-bottom: 15px;
    letter-spacing: 0.5px;
}}

.pricing {{
    font-size: 4.5rem;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 5px;
}}

.pricing .small {{
    font-size: 1rem;
    font-weight: 400;
    color: var(--text-muted);
}}

.savings {{
    font-size: 0.9rem;
    color: var(--accent);
    font-weight: 600;
}}

hr {{
    border: 0;
    height: 1px;
    background: var(--card-border);
    margin: 30px 0;
}}

.features {{
    list-style: none;
    margin-bottom: 40px;
    flex-grow: 1; /* Pushes button to bottom */
}}

.features li {{
    padding: 8px 0;
    font-size: 0.95rem;
    display: flex;
    align-items: center;
    color: var(--text-muted);
}}

.features li::before {{
    content: "✓";
    color: var(--accent);
    font-weight: bold;
    margin-right: 12px;
}}

.cta_btn {{
    display: block;
    width: 100%;
    text-align: center;
    background: var(--btn-bg);
    color: var(--btn-text);
    padding: 16px 0;
    border-radius: 50px;
    text-decoration: none;
    font-weight: 600;
    letter-spacing: 1px;
    transition: all 0.3s ease;
    border: 1px solid transparent;
}}

.cta_btn:hover {{
    background: var(--accent);
    color: var(--btn-hover-text);
    border-color: var(--accent);
    box-shadow: 0 10px 20px rgba(0,0,0,0.2);
}}

/* Responsive Design */
@media screen and (max-width: 1024px) {{
    .grid {{
        grid-template-columns: repeat(2, 1fr);
    }}
}}

@media screen and (max-width: 768px) {{
    .grid {{
        grid-template-columns: 1fr;
        max-width: 450px;
        margin: 0 auto;
    }}
    .pricing {{
        font-size: 3.5rem;
    }}
    .card {{
        padding: 30px 20px;
    }}
}}
"""

    # === HTML ===
    # Using python string escaping for the title and body text
    import html as html_lib
    safe_title = html_lib.escape(title_text)
    safe_body = html_lib.escape(body_text)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    
    <div class="header">
        <h1>{safe_title}</h1>
        <p>{safe_body}</p>
    </div>

    <div class="container">
        <div class="grid">
            
            <!-- Card 1 -->
            <div class="card">
                <h2 class="card_title">Student</h2>
                <div class="pricing">$10<span class="small">/mo</span></div>
                <div class="savings">Save $5 monthly</div>
                <hr>
                <ul class="features">
                    <li>1 User Account</li>
                    <li>Unlimited listening</li>
                    <li>Standard audio quality</li>
                    <li>Ad-supported</li>
                </ul>
                <a href="#" class="cta_btn">Get Student</a>
            </div>

            <!-- Card 2 -->
            <div class="card" style="border-color: var(--accent); box-shadow: 0 0 20px rgba(0,191,255,0.1);">
                <h2 class="card_title">Personal</h2>
                <div class="pricing">$29<span class="small">/mo</span></div>
                <div class="savings">Most popular</div>
                <hr>
                <ul class="features">
                    <li>1 User Account</li>
                    <li>Unlimited listening</li>
                    <li>High audio quality</li>
                    <li>Ad-free experience</li>
                    <li>Offline mode</li>
                </ul>
                <a href="#" class="cta_btn" style="background: var(--accent); color: var(--btn-hover-text);">Get Personal</a>
            </div>

            <!-- Card 3 -->
            <div class="card">
                <h2 class="card_title">Family</h2>
                <div class="pricing">$60<span class="small">/mo</span></div>
                <div class="savings">Save $25 monthly</div>
                <hr>
                <ul class="features">
                    <li>Up to 6 User Accounts</li>
                    <li>Unlimited listening</li>
                    <li>High audio quality</li>
                    <li>Ad-free experience</li>
                    <li>Offline mode</li>
                    <li>Family mix playlist</li>
                </ul>
                <a href="#" class="cta_btn">Get Family</a>
            </div>

        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Glassmorphism Pricing Cards — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    // Optional: Add a subtle 3D tilt effect on mouse move for extra flair
    const cards = document.querySelectorAll('.card');
    
    cards.forEach(card => {{
        card.addEventListener('mousemove', (e) => {{
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = ((y - centerY) / centerY) * -5;
            const rotateY = ((x - centerX) / centerX) * 5;
            
            card.style.transform = `perspective(1000px) rotateX(${{rotateX}}deg) rotateY(${{rotateY}}deg) translateY(-5px)`;
        }});
        
        card.addEventListener('mouseleave', () => {{
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateY(0)';
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
  - Text contrast against photographic backgrounds can be unpredictable. To mitigate this, a subtle text-shadow is applied to the main header, and the glass cards use sufficiently opaque colors (`0.15` to `0.3` alpha) to ensure internal text remains legible.
  - The feature list uses standard semantic `<ul>` and `<li>` elements rather than just line breaks.
  - Custom list bullets are added via CSS `::before` pseudo-elements, which screen readers generally ignore (treating it as presentation), preventing them from reading out "check mark" repeatedly.
* **Performance**:
  - `backdrop-filter: blur()` is notoriously performance-intensive on lower-end devices. However, modern browsers offload this to the GPU. To maintain smooth scrolling, we limit the blur radius to `16px` and apply it to relatively constrained geometric bounds (the cards).
  - The background image is set to `fixed` attachment to prevent it from repainting during scroll, which helps maintain 60fps when paired with backdrop filters.
  - The subtle 3D tilt script added to JS uses basic math and updates `transform` properties, which are cheap to animate as they don't trigger layout reflows.