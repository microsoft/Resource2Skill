# Glassmorphism Card with Masked Gradient Border

## Analysis

# Agent_Skill_Distiller Report

### 1. High-level Design Pattern Extraction

> **Skill Name**: Glassmorphism Card with Masked Gradient Border

* **Core Visual Mechanism**: The core aesthetic relies on combining `backdrop-filter: blur()` with a semi-transparent surface color to create a frosted-glass pane. To give this pane a premium, continuous gradient border without ruining the transparency of the inner card, a CSS masking trick is utilized. A pseudo-element is strictly sized to the card, given a gradient background, and then a CSS `mask` is applied using the XOR composition (`exclude` / `subtract`) of the `padding-box` and `border-box` to perfectly "cookie-cut" the center out, leaving only a flawless gradient outline.
* **Why Use This Skill (Rationale)**: Applying a gradient to a `border` in CSS usually requires `border-image`, which fundamentally breaks `border-radius`. The standard workaround is to nest an inner div with a solid background to cover the center of the gradient—but this destroys the transparency required for true glassmorphism. This masking technique is the definitive solution, preserving both rounded corners and internal transparency, creating depth, reflection, and premium "physical" lighting cues in the UI.
* **Overall Applicability**: Perfect for modern dark-mode interfaces, Web3 landing pages, premium SaaS pricing tiers, AI tool dashboards, and interactive portfolio cards. 
* **Value Addition**: It elevates a flat, boring UI into a layered, tactile environment. The gradient border acts as a rim light, simulating how light catches the physical edge of a glass plane, making the component pop against complex, dynamic backgrounds.
* **Browser Compatibility**: Fully supported in modern browsers. `backdrop-filter` requires the `-webkit-` prefix for older Safari. The CSS mask composition uses `-webkit-mask-composite: xor` (for Safari/older Chrome) and standard `mask-composite: exclude` for Firefox and modern Chromium.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Glass Pane**: `background: rgba(255, 255, 255, 0.03)` combined with `backdrop-filter: blur(16px)`.
  - **Rim Light (Border)**: Linear gradient transitioning from a highly visible translucent white (`rgba(255,255,255,0.3)`) at the top to a faint outline (`rgba(255,255,255,0.05)`) at the bottom, simulating a top-down light source.
  - **Internal Glow**: A subtle `radial-gradient` positioned at the bottom-center (`circle at 50% 150%`) to create an ambient base glow reflecting off the "floor".
  - **Masking Mechanism**: `-webkit-mask-composite: xor;` intersecting a `padding-box` mask and a `border-box` mask.

* **Step B: Layout & Compositional Style**
  - Uses `position: relative` on the main card to act as a containing block.
  - The `::before` pseudo-element uses `position: absolute; inset: 0; z-index: -1;` to overlay exactly over the card footprint.
  - Card content utilizes Flexbox (`display: flex; flex-direction: column; gap: 16px;`) for a clean, structural typographic hierarchy.

* **Step C: Interactive Behavior & Animations**
  - Pure CSS hover states to slightly scale the card (`transform: translateY(-4px)`) and intensify the border glow, adding a tactile, floaty responsiveness.
  - Smooth transitions applied to transform, box-shadow, and pseudo-element opacities (`transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1)`).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Frosted Glass Surface | CSS `backdrop-filter` + `rgba()` | Native hardware-accelerated blur that interacts with the background directly. |
| Gradient Outline | CSS `mask` & `mask-composite` | Allows a gradient border while keeping the center transparent and preserving `border-radius`. |
| Internal Lighting | CSS `radial-gradient` | Easily mimics ambient lighting and reflections without needing external image assets. |
| Dynamic Opacity Colors | CSS `color-mix()` | Robustly mixes the user's hex `accent_color` with transparency directly in CSS. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Ask anything",
    body_text: str = "Trying to wrap your head around a new topic? Looking for specific recommendations? We'll help you decode it.",
    color_scheme: str = "dark",        
    accent_color: str = "#8a2be2",     
    width_px: int = 420,
    height_px: int = 280,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Glassmorphism Card with Masked Gradient Border effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        page_bg = "#0d1117"
        card_bg = "rgba(255, 255, 255, 0.02)"
        border_light = "rgba(255, 255, 255, 0.3)"
        border_dark = "rgba(255, 255, 255, 0.05)"
        text_color = "#f0f6fc"
        text_muted = "#8b949e"
        icon_bg = "rgba(255, 255, 255, 0.05)"
        icon_border = "rgba(255, 255, 255, 0.1)"
    else:
        page_bg = "#f3f4f6"
        card_bg = "rgba(255, 255, 255, 0.4)"
        border_light = "rgba(255, 255, 255, 0.8)"
        border_dark = "rgba(255, 255, 255, 0.2)"
        text_color = "#111827"
        text_muted = "#4b5563"
        icon_bg = "rgba(255, 255, 255, 0.5)"
        icon_border = "rgba(255, 255, 255, 0.4)"

    # === CSS ===
    css = f"""/* Glassmorphism Card with Masked Gradient Border */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --page-bg: {page_bg};
    --card-bg: {card_bg};
    --text-color: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --border-light: {border_light};
    --border-dark: {border_dark};
    --icon-bg: {icon_bg};
    --icon-border: {icon_border};
    
    /* Using color-mix to create dynamic translucent variations of the accent color */
    --accent-glow: color-mix(in srgb, var(--accent) 30%, transparent);
    --orb-1: color-mix(in srgb, var(--accent) 25%, transparent);
    --orb-2: color-mix(in srgb, #4169e1 20%, transparent);
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--page-bg);
    /* Abstract background to show off the glass blur effect */
    background-image: 
        radial-gradient(circle at 15% 20%, var(--orb-1) 0%, transparent 40%),
        radial-gradient(circle at 85% 80%, var(--orb-2) 0%, transparent 40%);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    padding: 2rem;
}}

.card {{
    width: {width_px}px;
    max-width: 100%;
    min-height: {height_px}px;
    position: relative;
    border-radius: 20px;
    padding: 32px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    
    /* True Glass Background */
    background: 
        radial-gradient(circle at 50% 150%, var(--accent-glow), transparent 60%),
        var(--card-bg);
    
    /* The Blur */
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    
    /* Ambient Shadow */
    box-shadow: 0 12px 32px 0 rgba(0, 0, 0, 0.2);
    
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s ease;
    cursor: pointer;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 16px 40px 0 rgba(0, 0, 0, 0.3), 0 0 40px 0 var(--accent-glow);
}}

/* THE MASKED GRADIENT BORDER TRICK */
.card::before {{
    content: "";
    position: absolute;
    inset: 0; /* Cover the whole card */
    border-radius: inherit; /* Match card radius exactly */
    z-index: -1;
    pointer-events: none;
    
    /* Set border width using a transparent border */
    border: 1px solid transparent; 
    
    /* The actual gradient that will act as the border */
    background: linear-gradient(180deg, var(--border-light), var(--border-dark)) border-box;
    
    /* The Masking logic to cut out the center */
    -webkit-mask: 
        linear-gradient(#fff 0 0) padding-box, 
        linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    
    /* Standard CSS Masking */
    mask: 
        linear-gradient(#fff 0 0) padding-box, 
        linear-gradient(#fff 0 0);
    mask-composite: exclude;
    
    transition: opacity 0.3s ease;
}}

.card:hover::before {{
    background: linear-gradient(180deg, var(--accent), var(--border-dark)) border-box;
    opacity: 1;
}}

/* Inner Content Styling */
.card-icon {{
    width: 48px;
    height: 48px;
    border-radius: 12px;
    background: var(--icon-bg);
    border: 1px solid var(--icon-border);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 8px;
    color: var(--accent);
}}

.card-title {{
    font-size: 1.5rem;
    font-weight: 600;
    letter-spacing: -0.02em;
    line-height: 1.2;
}}

.card-body {{
    font-size: 0.95rem;
    line-height: 1.6;
    color: var(--text-muted);
}}

.card-button {{
    align-self: flex-start;
    margin-top: auto;
    background: transparent;
    border: none;
    color: var(--accent);
    font-weight: 600;
    font-size: 0.95rem;
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    transition: opacity 0.2s ease;
}}

.card-button:hover {{
    opacity: 0.7;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="card">
        <div class="card-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
            </svg>
        </div>
        <h2 class="card-title">{title_text}</h2>
        <p class="card-body">{body_text}</p>
        <button class="card-button">
            Learn more
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="5" y1="12" x2="19" y2="12"></line>
                <polyline points="12 5 19 12 12 19"></polyline>
            </svg>
        </button>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Pure CSS is handling the visual complexity (masks, blurs, and hover states).
// Minimal JS included to handle potential data interactions.
document.addEventListener('DOMContentLoaded', () => {{
    const card = document.querySelector('.card');
    const button = document.querySelector('.card-button');
    
    button.addEventListener('click', (e) => {{
        e.stopPropagation(); // Prevent card click event if button is clicked
        console.log('Action initiated');
    }});

    card.addEventListener('click', () => {{
        console.log('Card clicked');
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
  - Contrast ratios have been maintained via the color derivation system, ensuring `text_muted` does not drop below readability thresholds in dark or light mode.
  - The card uses semantic HTML tags (`h2`, `p`, `button`) ensuring screen readers parse the structural hierarchy correctly.
* **Performance**: 
  - `backdrop-filter` triggers a separate render pass in the browser and heavily relies on the GPU. Using it on massive elements or deeply nesting multiple blurred elements can cause scroll jank. It is safely isolated to a single layer here.
  - `mask` and `-webkit-mask` composite operations are highly optimized native methods, functioning far more efficiently than using arbitrary SVGs or JS calculations to fake a gradient border outline.