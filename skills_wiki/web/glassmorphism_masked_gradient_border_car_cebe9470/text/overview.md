# Glassmorphism Masked Gradient Border Card

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Glassmorphism Masked Gradient Border Card

* **Core Visual Mechanism**: This pattern solves the complex problem of combining translucent "frosted glass" elements (`backdrop-filter: blur()`) with vibrant, gradient borders. Standard CSS border images or simple background clips fail when the card background isn't solid. This technique uses a `z-index: -1` absolute pseudo-element to hold the border gradient, which is then hollowed out perfectly using a CSS `mask` and `mask-composite` operation. The result is a clean 1px glowing stroke around a blur-filtered surface.
* **Why Use This Skill (Rationale)**: Gradient borders provide premium, sci-fi, or highly polished aesthetic cues, drawing the eye to interactive panels or pricing tiers. When combined with glassmorphism, it allows ambient page backgrounds to dynamically interact with the card, creating depth and spatial hierarchy without feeling heavy.
* **Overall Applicability**: Ideal for SaaS dashboard widgets, pricing cards, Web3/crypto interfaces, high-end portfolio galleries, and "refer & earn" modal dialogs. 
* **Value Addition**: It elevates a flat, boring UI card into a tactile, floating object. It implies high value and interactivity.
* **Browser Compatibility**: `backdrop-filter` requires the `-webkit-` prefix for older Safari versions. The CSS `mask` trick utilizes `-webkit-mask-composite: xor` (for WebKit browsers) alongside the standard `mask-composite: exclude` (for Firefox/modern spec). This specific masking stack is robust and production-ready across all major modern browsers.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  * **Color Logic**: In dark mode, a deep space background (`#0f1117`) sits beneath a very faint white overlay (`rgba(255, 255, 255, 0.03)`). The border stroke fades from a vibrant accent color to a faint translucent rim (`rgba(255, 255, 255, 0.06)`). 
  * **Typographic Hierarchy**: High contrast sans-serif for primary values and titles (e.g., `1.25rem`, `600` weight), with muted, slightly tracked-out uppercase labels (`0.75rem`, `letter-spacing: 0.05em`) for secondary data. Monospace is used for codes/hashes.
  * **Key CSS Properties**: `backdrop-filter: blur()`, `mask`, `mask-composite`, `color-mix()`.

* **Step B: Layout & Compositional Style**
  * The card acts as the primary layout boundary with a fixed width/flex setup.
  * `padding: 32px` gives ample breathing room.
  * `border-radius: 24px` on the card is cleanly inherited by the pseudo-element border mask, preventing corner clipping artifacts.
  * Stacking contexts are rigidly controlled: `isolation: isolate` ensures the pseudo-element border stays bounded behind the card content but above the page background.

* **Step C: Interactive Behavior & Animations**
  * **Border Shimmer**: The border linear gradient is scaled to `200%` and continuously translated via `background-position` keyframes, creating an ambient glowing "scan" around the rim.
  * **Cursor Tracking**: A subtle radial glow inside the card tracks the user's cursor (`mousemove` event updating CSS custom properties), mixed seamlessly with the card's surface background.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Gradient Border** | CSS Pseudo-element + `mask-composite` | Allows the border to be a complex gradient without bleeding under a transparent card background. |
| **Glassmorphism** | CSS `backdrop-filter` | Native GPU-accelerated blur for elements physically underneath the card. |
| **Interactive Glow** | JS Mouse Tracking + CSS `radial-gradient` | JavaScript captures coordinate offsets, feeding them to CSS variables for dynamic rendering without constant DOM repaints. |
| **Ambient Border Motion** | CSS `@keyframes` on `background-position` | Creates endless glowing motion purely on the GPU, avoiding JS overhead. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Refer and Earn",
    body_text: str = "Refer Friends, Earn Points and Fees",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#8b5cf6",     # Violet accent
    width_px: int = 1000,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Glassmorphism Masked Gradient Border effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#0f1117"
        text_color = "#f8fafc"
        text_muted = "#94a3b8"
        surface_color = "rgba(255, 255, 255, 0.03)"
        surface_inner = "rgba(0, 0, 0, 0.2)"
        glass_border_fade = "rgba(255, 255, 255, 0.06)"
        blob_opacity = "0.25"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        text_muted = "#64748b"
        surface_color = "rgba(255, 255, 255, 0.6)"
        surface_inner = "rgba(255, 255, 255, 0.8)"
        glass_border_fade = "rgba(0, 0, 0, 0.08)"
        blob_opacity = "0.15"

    # === CSS ===
    css = f"""/* Glassmorphism Masked Gradient Border Component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --surface: {surface_color};
    --surface-inner: {surface_inner};
    --border-fade: {glass_border_fade};
    --blob-opacity: {blob_opacity};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.container {{
    width: var(--width);
    height: var(--height);
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--bg);
    overflow: hidden;
}}

/* Ambient glowing blob in the background to emphasize the glass blur */
.ambient-blob {{
    position: absolute;
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, var(--accent) 0%, transparent 60%);
    filter: blur(60px);
    opacity: var(--blob-opacity);
    top: 50%;
    left: 40%;
    transform: translate(-50%, -50%);
    z-index: 0;
    pointer-events: none;
}}

/* --- Core Card Layout & Glassmorphism --- */
.card {{
    position: relative;
    width: min(100% - 48px, 420px);
    padding: 32px;
    border-radius: 24px;
    
    /* 1. Setup the transparent border to make physical room for the pseudo-element glow */
    border: 1px solid transparent;
    /* 2. Clip the card's background to the padding so it doesn't bleed into the border area */
    background-clip: padding-box;
    /* 3. Establish strict stacking context */
    isolation: isolate;

    /* Interactive hover glow combined with static surface */
    background-image: 
        radial-gradient(
            600px circle at var(--mouse-x, -1000px) var(--mouse-y, -1000px), 
            color-mix(in srgb, var(--accent) 15%, transparent),
            transparent 40%
        ),
        linear-gradient(var(--surface), var(--surface));
        
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    
    display: flex;
    flex-direction: column;
    gap: 28px;
    box-shadow: 0 12px 40px -12px rgba(0, 0, 0, 0.2);
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    z-index: 1;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 16px 50px -12px color-mix(in srgb, var(--accent) 30%, transparent);
}}

/* --- Masked Gradient Border --- */
@keyframes shimmer {{
    0% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}

.card::before {{
    content: "";
    position: absolute;
    /* Stretch over the transparent border */
    inset: -1px; 
    border-radius: inherit;
    /* The padding determines the border stroke width */
    padding: 1px; 
    
    background: linear-gradient(
        115deg, 
        var(--border-fade) 0%, 
        var(--accent) 50%, 
        var(--border-fade) 100%
    );
    background-size: 200% 100%;
    animation: shimmer 4s infinite linear;
    
    /* MASK MAGIC: Subtract content-box from border-box to leave only the 1px stroke */
    -webkit-mask: 
        linear-gradient(#fff 0 0) content-box, 
        linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    
    mask: 
        linear-gradient(#fff 0 0) content-box, 
        linear-gradient(#fff 0 0);
    mask-composite: exclude;
    
    z-index: -1;
    pointer-events: none;
}}

/* --- Inner Typography and Styling --- */
.card-header {{
    display: flex;
    flex-direction: column;
    gap: 6px;
}}
.title {{
    font-size: 1.25rem;
    font-weight: 600;
    letter-spacing: -0.02em;
    color: var(--text);
}}
.body-text {{
    font-size: 0.875rem;
    color: var(--text-muted);
    line-height: 1.5;
}}

.stats-row {{
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--border-fade);
}}
.stat-block {{
    display: flex;
    flex-direction: column;
    gap: 8px;
}}
.right-align {{
    align-items: flex-end;
}}
.stat-label {{
    font-size: 0.75rem;
    color: var(--text-muted);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}
.stat-value {{
    font-size: 1.125rem;
    font-weight: 500;
    color: var(--text);
}}
.code {{
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    background: var(--surface-inner);
    padding: 4px 10px;
    border-radius: 6px;
    letter-spacing: 0.05em;
    font-size: 0.875rem;
    border: 1px solid var(--border-fade);
}}

.rewards-pill {{
    background: var(--surface-inner);
    border-radius: 12px;
    padding: 16px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
    border: 1px solid var(--border-fade);
}}
.rewards-label {{
    font-size: 0.75rem;
    color: var(--text-muted);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}
.rewards-val {{
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--text);
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
    <div class="container">
        <!-- Abstract blur background to demonstrate glassmorphism -->
        <div class="ambient-blob"></div>
        
        <div class="card">
            <div class="card-header">
                <h2 class="title">{title_text}</h2>
                <p class="body-text">{body_text}</p>
            </div>
            
            <div class="stats-row">
                <div class="stat-block">
                    <span class="stat-label">Referral Code</span>
                    <span class="stat-value code">7D45564JK355</span>
                </div>
                <div class="stat-block right-align">
                    <span class="stat-label">Referred Users</span>
                    <span class="stat-value">4</span>
                </div>
            </div>
            
            <div class="rewards-pill">
                <span class="rewards-label">Rewards</span>
                <span class="rewards-val">20% Platform Fees + 10% Extra points</span>
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Interactive Mouse Tracking for Card Ambient Glow
document.addEventListener('DOMContentLoaded', () => {{
    const card = document.querySelector('.card');
    
    // Set initial position off-screen so the glow isn't visible until hover
    card.style.setProperty('--mouse-x', `-1000px`);
    card.style.setProperty('--mouse-y', `-1000px`);
    
    card.addEventListener('mousemove', (e) => {{
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        // Pass local cursor coordinates to CSS variables
        card.style.setProperty('--mouse-x', `${{x}}px`);
        card.style.setProperty('--mouse-y', `${{y}}px`);
    }});
    
    // Optional: Hide the cursor glow gracefully when leaving the card
    card.addEventListener('mouseleave', () => {{
        card.style.setProperty('--mouse-x', `-1000px`);
        card.style.setProperty('--mouse-y', `-1000px`);
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

* **Accessibility**: Contrast ratios are carefully considered. Standard muted text is set explicitly based on the chosen schema (`#94a3b8` on dark). The glowing effect relies heavily on aesthetics but doesn't override or hide critical functional text. To support users who prefer static UI elements, the shimmer animation can be disabled using a `@media (prefers-reduced-motion: reduce)` block to stop the `borderGlow` keyframes.
* **Performance**: The combination of `backdrop-filter` and `mask-composite` can be heavy on mobile GPUs if abused. Limiting the blur radius (kept at a balanced `20px`) prevents excessive repaints. The mouse-tracking effect applies coordinates to CSS variables modifying a lightweight radial gradient rather than relying on heavy DOM node repositioning or Canvas, maintaining a solid 60FPS.