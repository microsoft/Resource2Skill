# Pure CSS Parallax & Scroll-Revealing Cards

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Pure CSS Parallax & Scroll-Revealing Cards

* **Core Visual Mechanism**: This pattern leverages the modern **CSS Scroll-driven Animations API** to create a multi-layered scrolling effect. By declaring a named view timeline (`view-timeline-name`) on the card container, two concurrent animations are bound to the user's scroll position:
  1. **Entry/Exit Morph**: The cards scale down (to 80%) and fade out as they leave the viewport, and reverse this animation as they enter.
  2. **Internal Parallax**: An image wrapper inside the card (which is twice the height of the card) moves vertically in the opposite direction of the scroll. Because the card applies `overflow: clip`, this reveals different portions of the inner image, creating a deep parallax window effect.

* **Why Use This Skill (Rationale)**: Tying animations directly to scroll position (rather than time) creates a deeply physical, satisfying interactive experience. It makes the UI feel tactile. Moving the parallax logic entirely into CSS avoids the performance bottleneck (jank) typically associated with JavaScript `scroll` event listeners.

* **Overall Applicability**: Perfect for immersive landing pages, photography portfolios, product feature grids, and editorial content where visual storytelling is heavily reliant on imagery and depth.

* **Browser Compatibility**: This relies on **CSS Scroll-driven Animations Level 1** (`animation-timeline: view()`, `view-timeline-name`, and timeline ranges inside `@keyframes`). As of late 2023, this is fully supported in Chromium browsers (Chrome, Edge, Opera 115+). For Safari and Firefox, a polyfill is currently required (though not included in this pure CSS demonstration to highlight the native capability). In unsupported browsers, the cards gracefully degrade to static, visible grid items.


### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Cards (`.card`)**: 300px by 300px squares with `border-radius: 20px` and `overflow: clip`. They act as the subjects for the view timeline.
  - **Image Wrapper (`.card_image-wrapper`)**: A container set to `height: 600px` (double the card height). It provides the extra visual area needed to slide up and down without exposing empty space.
  - **Images (`.card_image`)**: Full width/height of the wrapper, using `object-fit: cover`.
  - **Color Logic**: A soft, subtle background gradient that contrasts well with rich, high-fidelity images.

* **Step B: Layout & Compositional Style**
  - Uses **CSS Grid** to create a rigid, 2-column structure with a `10px` gap (or `20px` for better breathing room).
  - The layout includes significant vertical whitespace (`100vh` spacer blocks) above and below the grid to ensure that the user can scroll entirely past the cards, allowing the `entry` and `exit` animation ranges to trigger fully.

* **Step C: Interactive Behavior & Animations**
  - **Fade & Scale (Card)**: Bound to the card's intersection with the viewport.
    - `entry 0%`: `opacity: 0; transform: scale(0.8)`
    - `entry 100%` & `exit 0%`: `opacity: 1; transform: scale(1)`
    - `exit 100%`: `opacity: 0; transform: scale(0.8)`
  - **Parallax Translate (Image Wrapper)**: Bound to the same timeline.
    - `from`: `transform: translateY(-300px)` (Card bottom intersects viewport bottom)
    - `to`: `transform: translateY(0)` (Card top intersects viewport top)


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Scroll Tracking** | CSS `view-timeline-name` | Native CSS API. Maps an element's viewport intersection directly to an animation timeline, avoiding JS jank. |
| **Animation Bounds** | Timeline Ranges in `@keyframes` | Allows defining `entry` and `exit` states directly inside CSS keyframes, making the code incredibly clean and isolated. |
| **Parallax Effect** | Oversized inner wrapper + `translateY` | Translating a 600px tall wrapper inside a 300px clipped box is the mathematical core of the window-parallax effect. |
| **Card Generation** | JavaScript DOM | Used only to populate the grid with images to keep the HTML clean and self-contained for the demonstration. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Smooth Parallax Scrolling Cards",
    body_text: str = "Scroll down to see the native CSS parallax and fade effects in action.",
    color_scheme: str = "light",
    accent_color: str = "#000000",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Pure CSS Parallax Cards visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_gradient = "linear-gradient(135deg, #0d111c 0%, #1a1f2e 100%)"
        text_color = "#f0f0f0"
        surface_color = "#2a2f42"
    else:
        bg_gradient = "linear-gradient(135deg, #e6e9f0 0%, #eef1f5 100%)"
        text_color = "#1a1a2e"
        surface_color = "#ffffff"

    # === CSS ===
    css = f"""/* Pure CSS Parallax & Scroll-Revealing Cards */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-gradient: {bg_gradient};
    --text: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --max-width: {width_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg-gradient);
    color: var(--text);
    min-height: 100vh;
    overflow-x: hidden;
}}

.container {{
    width: 100%;
    max-width: var(--max-width);
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    align-items: center;
}}

/* Intro Hero Section */
.hero {{
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 0 20px;
}}

.title {{
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 1rem;
    letter-spacing: -0.02em;
}}

.body-text {{
    font-size: 1.1rem;
    opacity: 0.8;
    margin-bottom: 3rem;
}}

/* Scroll Indicator */
.scroll-indicator {{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
}}

.mouse {{
    width: 26px;
    height: 40px;
    border: 2px solid var(--text);
    border-radius: 13px;
    display: flex;
    justify-content: center;
}}

.mouse::before {{
    content: '';
    width: 4px;
    height: 8px;
    background: var(--text);
    border-radius: 2px;
    margin-top: 6px;
    animation: scroll-wheel 1.5s infinite ease-in-out;
}}

.arrow {{
    width: 8px;
    height: 8px;
    border-right: 2px solid var(--text);
    border-bottom: 2px solid var(--text);
    transform: rotate(45deg);
    animation: bounce 1.5s infinite ease-in-out;
}}

/* Card Grid Layout */
.cards {{
    display: grid;
    grid-template-columns: repeat(2, 300px);
    gap: 20px;
    padding: 10vh 20px;
}}

/* Core Visual Element: The Card */
.card {{
    width: 300px;
    height: 300px;
    border-radius: 20px;
    overflow: clip; /* Prefer clip over hidden for performance / scroll chaining */
    background: var(--surface);
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    
    /* CSS Scroll-Driven Animation Magic */
    view-timeline-name: --card;
    animation: fade-card linear forwards;
    animation-timeline: --card;
}}

/* Inner wrapper providing the parallax headroom */
.card_image-wrapper {{
    height: 600px; /* Double the height of the card */
    
    /* Inherits the named timeline from the parent .card */
    animation: move-image linear forwards;
    animation-timeline: --card;
}}

.card_image {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}}

/* Spacer to allow scrolling past the grid */
.footer-spacer {{
    height: 100vh;
    width: 100%;
}}

/* Animations */
@keyframes fade-card {{
    entry 0% {{
        opacity: 0;
        transform: scale(0.8);
    }}
    entry 100% {{
        opacity: 1;
        transform: scale(1);
    }}
    exit 0% {{
        opacity: 1;
        transform: scale(1);
    }}
    exit 100% {{
        opacity: 0;
        transform: scale(0.8);
    }}
}}

@keyframes move-image {{
    from {{
        transform: translateY(-300px);
    }}
    to {{
        transform: translateY(0);
    }}
}}

@keyframes scroll-wheel {{
    0% {{ transform: translateY(0); opacity: 1; }}
    100% {{ transform: translateY(12px); opacity: 0; }}
}}

@keyframes bounce {{
    0%, 100% {{ transform: translateY(0) rotate(45deg); }}
    50% {{ transform: translateY(4px) rotate(45deg); }}
}}

/* Responsive Fallback */
@media (max-width: 680px) {{
    .cards {{
        grid-template-columns: 300px;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <header class="hero">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
            <div class="scroll-indicator">
                <div class="mouse"></div>
                <div class="arrow"></div>
            </div>
        </header>
        
        <main class="cards" id="cards-container">
            <!-- Cards are injected via script.js -->
        </main>
        
        <div class="footer-spacer"></div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Generates the image cards dynamically to keep HTML clean.
// The actual scroll/parallax effect is handled entirely by CSS.

document.addEventListener('DOMContentLoaded', () => {{
    const cardsContainer = document.getElementById('cards-container');
    
    // High quality Unsplash images highlighting depth/parallax
    const images = [
        'https://images.unsplash.com/photo-1534447677768-be436bb09401?w=600&h=1200&fit=crop', // Moon
        'https://images.unsplash.com/photo-1505118380757-91f5f5632de0?w=600&h=1200&fit=crop', // Ocean
        'https://images.unsplash.com/photo-1518531933037-91b2f5f229cc?w=600&h=1200&fit=crop', // Abstract Leaves
        'https://images.unsplash.com/photo-1682687220742-aba13b6e50ba?w=600&h=1200&fit=crop', // Dunes
        'https://images.unsplash.com/photo-1562690868-60bbe7293e94?w=600&h=1200&fit=crop', // Rose
        'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=600&h=1200&fit=crop'  // Abstract Liquid
    ];

    images.forEach(src => {{
        // Create Card
        const card = document.createElement('div');
        card.className = 'card';
        
        // Create inner wrapper (this is what translates Y)
        const wrapper = document.createElement('div');
        wrapper.className = 'card_image-wrapper';
        
        // Create image
        const img = document.createElement('img');
        img.className = 'card_image';
        img.src = src;
        img.alt = 'Parallax image';
        img.loading = 'lazy';
        
        // Assemble
        wrapper.appendChild(img);
        card.appendChild(wrapper);
        cardsContainer.appendChild(card);
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