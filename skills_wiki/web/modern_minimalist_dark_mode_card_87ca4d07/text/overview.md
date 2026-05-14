# Modern Minimalist Dark Mode Card

## Analysis

Here is a comprehensive extraction of the design principles and the code to reproduce the "Rise of the Dark Mode" UI component.

### 1. High-level Design Pattern Extraction

> **Skill Name**: Modern Minimalist Dark Mode Card

* **Core Visual Mechanism**: Deep elevation and muted color strategy. This component utilizes an off-black background (`#0d0e12`) and a slightly lighter surface (`#1a1c23`) to create spatial depth. Instead of heavy drop shadows (which fail in dark mode), it uses a 1px gradient border (`background-clip`) to simulate an edge-light, and a cursor-tracking ambient glow to provide interactive feedback.
* **Why Use This Skill (Rationale)**: True dark mode is not just "inverted white". Pure white text on pure black backgrounds creates "halation" (a fuzzy optical illusion that strains the eyes). High-saturation brand colors can also become aggressively bright in dark mode. By muting accent colors and relying on subtle border lighting, this pattern reduces eye strain while maintaining a premium, high-tech feel.
* **Overall Applicability**: SaaS dashboards, developer tools, premium portfolio showcases, pricing cards, and tech landing pages where extended reading comfort and a sleek aesthetic are paramount.
* **Value Addition**: Transforms a static "card" into an interactive, spatial object. The ambient glow gives a sense of dynamic lighting, making the UI feel responsive to the user's presence without requiring heavy 3D rendering.
* **Browser Compatibility**: Uses `color-mix()` to programmatically mute vivid colors (supported in Chrome 111+, Safari 16.4+, Firefox 113+). The gradient border technique relies on `background-clip`, which is widely supported.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**: Pure black is avoided. Background is `#0d0e12`, card surface is `#1a1c23`. Text avoids pure white (`#e4e5e9` primary, `#9aa0a6` secondary) to prevent halation.
  - **Muted Accents**: The primary accent color is slightly desaturated by mixing it with gray using CSS `color-mix()`. This aligns with the "Muted Colors" rule, ensuring the vivid accent doesn't overpower the dark interface.
  - **Typography**: Clean, sans-serif (`Inter`) with tight letter-spacing for headers (`-0.03em`) and comfortable line-height for body copy (`1.6`).

* **Step B: Layout & Compositional Style**
  - **Layout System**: CSS Flexbox for internal card alignment.
  - **Proportions**: Card is `420px` wide, with generous `40px` padding to emphasize minimalism and whitespace.
  - **Z-index Layering**: Background `0` -> Cursor Glow `1` -> Card Surface `10`. This stack creates physical depth.

* **Step C: Interactive Behavior & Animations**
  - **Hover Effects**: Buttons slightly shift up (`translateY(-1px)`) and increase brightness.
  - **JavaScript Interaction**: A subtle, large radial gradient follows the user's mouse cursor across the container. The coordinates are passed from JS to CSS custom properties (`--mouse-x`, `--mouse-y`) inside a `requestAnimationFrame` loop for silky smooth performance.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Edge-lighting border | CSS `background-clip` | Allows a gradient to act as a 1px border without extra DOM elements or SVG wrappers. |
| Muted brand colors | CSS `color-mix()` | Programmatically dulls vivid colors for dark mode comfort without requiring the user to supply multiple hex codes. |
| Cursor-tracking glow | JavaScript + CSS Vars | Passing mouse coordinates to CSS vars (`--mouse-x`, `--mouse-y`) is highly performant and avoids direct DOM style repaints. |
| Anti-halation text | CSS Hex colors | Using `#e4e5e9` text on a `#1a1c23` surface naturally eliminates optical blur. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Level up your UI Game",
    body_text: str = "Organic life is chaotic. We impose order on the chaos. Bring structure to your interfaces with deliberate contrast, precise elevation, and purpose-driven colors.",
    color_scheme: str = "dark",        
    accent_color: str = "#00bfff",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Modern Minimalist Dark Mode Card visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)
    
    # Establish fallback body background to avoid flash of white
    body_bg = "#0d0e12" if color_scheme == "dark" else "#f3f4f6"

    # === CSS ===
    css = f"""/* Modern Minimalist Dark Mode Card */
:root {{
    --width: {width_px}px;
    --height: {height_px}px;
    --accent: {accent_color};
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: {body_bg};
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    overflow: hidden;
}}

.container {{
    width: var(--width);
    height: var(--height);
    background: var(--bg);
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    transition: background 0.3s ease;
}}

/* Theme Variable Architectures */
.theme-dark {{
    --bg: #0d0e12;
    --surface: #1a1c23;
    --text-primary: #e4e5e9; /* Off-white prevents halation */
    --text-secondary: #9aa0a6;
    --border: rgba(255, 255, 255, 0.08);
    --border-highlight: rgba(255, 255, 255, 0.25);
    /* Rule 7: Muted Colors. We mix the vivid accent with gray to soften it */
    --accent-display: color-mix(in srgb, var(--accent) 85%, #666);
    --primary-btn-text: #0d0e12;
}}

.theme-light {{
    --bg: #f3f4f6;
    --surface: #ffffff;
    --text-primary: #111827;
    --text-secondary: #4b5563;
    --border: rgba(0, 0, 0, 0.08);
    --border-highlight: rgba(0, 0, 0, 0.2);
    --accent-display: var(--accent);
    --primary-btn-text: #ffffff;
}}

/* Rule 6 & 9: Depth & Edge Lighting via Gradient Border */
.card {{
    position: relative;
    width: 420px;
    max-width: 90%;
    padding: 40px;
    background: linear-gradient(var(--surface), var(--surface)) padding-box,
                linear-gradient(145deg, var(--border-highlight) 0%, var(--border) 100%) border-box;
    border: 1px solid transparent;
    border-radius: 20px;
    z-index: 10;
    display: flex;
    flex-direction: column;
    gap: 20px;
    box-shadow: 0 24px 48px rgba(0, 0, 0, 0.4);
}}

/* Rule 4: Colors have a purpose (Semantic Badging) */
.card-badge {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 12px;
    border-radius: 99px;
    font-size: 0.85rem;
    font-weight: 600;
    /* Transparent muted background */
    background: color-mix(in srgb, var(--accent-display) 15%, transparent);
    color: var(--accent-display);
    border: 1px solid color-mix(in srgb, var(--accent-display) 25%, transparent);
    align-self: flex-start;
}}

.card-badge .dot {{
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--accent-display);
    box-shadow: 0 0 10px var(--accent-display);
}}

/* Rule 5: Readability Typography */
.title {{
    color: var(--text-primary);
    font-size: 1.75rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    line-height: 1.2;
}}

.body-text {{
    color: var(--text-secondary);
    font-size: 1.05rem;
    line-height: 1.6;
}}

/* Actions Hierarchy */
.action-group {{
    display: flex;
    gap: 12px;
    margin-top: 12px;
}}

.btn {{
    padding: 12px 20px;
    border-radius: 10px;
    font-weight: 600;
    font-size: 0.95rem;
    cursor: pointer;
    transition: all 0.2s ease;
    border: none;
    font-family: inherit;
    display: inline-flex;
    align-items: center;
    justify-content: center;
}}

.btn-primary {{
    background: var(--accent-display);
    color: var(--primary-btn-text);
}}

.btn-primary:hover {{
    filter: brightness(1.15);
    transform: translateY(-1px);
}}

.btn-secondary {{
    background: transparent;
    color: var(--text-primary);
    border: 1px solid var(--border);
}}

.btn-secondary:hover {{
    background: color-mix(in srgb, var(--text-primary) 5%, transparent);
    border-color: var(--border-highlight);
}}

/* Rule 8: Minimalism (Ambient Dynamic Glow) */
.glow-orb {{
    position: absolute;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, var(--accent-display) 0%, transparent 60%);
    opacity: 0.12;
    top: var(--mouse-y, 50%);
    left: var(--mouse-x, 50%);
    transform: translate(-50%, -50%);
    border-radius: 50%;
    z-index: 1;
    pointer-events: none;
    transition: opacity 0.3s ease;
}}

.container:hover .glow-orb {{
    opacity: 0.18;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container theme-{color_scheme}">
        <div class="glow-orb"></div>
        
        <div class="card">
            <div class="card-badge">
                <span class="dot"></span>
                <span class="badge-text">New Component</span>
            </div>
            
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
            
            <div class="action-group">
                <button class="btn btn-primary">Get Started</button>
                <button class="btn btn-secondary">Learn More</button>
            </div>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Mouse tracking for ambient glow effect
document.addEventListener('DOMContentLoaded', () => {{
    const container = document.querySelector('.container');
    let rafId = null;

    container.addEventListener('mousemove', (e) => {{
        const rect = container.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        // Use requestAnimationFrame to throttle CSS custom property updates
        if (rafId) cancelAnimationFrame(rafId);
        
        rafId = requestAnimationFrame(() => {{
            container.style.setProperty('--mouse-x', `${{x}}px`);
            container.style.setProperty('--mouse-y', `${{y}}px`);
        }});
    }});

    // Reset glow to center when mouse leaves the container
    container.addEventListener('mouseleave', () => {{
        if (rafId) cancelAnimationFrame(rafId);
        requestAnimationFrame(() => {{
            container.style.setProperty('--mouse-x', `50%`);
            container.style.setProperty('--mouse-y', `50%`);
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
  - The color palette is specifically designed to combat "halation" for users with astigmatism by restricting the use of pure `#000000` backgrounds and `#FFFFFF` text.
  - Buttons have a high contrast target state in both dark and light modes.
* **Performance**: 
  - The ambient cursor-tracking glow utilizes `requestAnimationFrame` to safely throttle the mouse events and applies coordinate changes to CSS variables (`--mouse-x`). The browser updates the gradient off the main rendering thread using these properties, avoiding expensive synchronous DOM mutations. 
  - The glow object relies strictly on `pointer-events: none` to prevent scroll-blocking or interfering with button clicks inside the card.