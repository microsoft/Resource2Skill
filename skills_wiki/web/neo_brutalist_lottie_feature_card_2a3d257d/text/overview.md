# Neo-Brutalist Lottie Feature Card

## Analysis

# High-level Design Pattern Extraction

> **Skill Name**: Neo-Brutalist Lottie Feature Card

* **Core Visual Mechanism**: Integrating a lightweight, highly scalable JSON-based vector animation using the `<lottie-player>` web component. The animation is housed within a "Neo-Brutalist" card layout characterized by stark high-contrast borders, solid offset drop shadows, and vivid colors, directly mimicking the Figma project style seen in the tutorial.
* **Why Use This Skill (Rationale)**: Lottie animations add a high-quality, 60fps layer of "delight" and motion to user interfaces without the massive payload constraints of video or GIFs. Combining this motion with Neo-Brutalist styling creates a highly engaging, modern, and playful user experience that commands immediate visual attention. 
* **Overall Applicability**: This pattern shines in feature announcements, pricing tiers, onboarding flows, success messages, and empty states where motion can provide context or reward user interaction.
* **Value Addition**: Compared to static imagery, this component breathes life into the UI. It provides continuous passive engagement (via looping) and can be wired to respond dynamically to user interactions (like speeding up on hover).
* **Browser Compatibility**: Fully supported in all modern browsers. The Lottie player utilizes the Canvas or SVG API under the hood, and the Neo-Brutalist styling relies on standard CSS properties (`box-shadow`, `flexbox`).

# Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Lottie Player**: A custom web component `<lottie-player>` injected via the official LottieFiles CDN.
  - **HTML Structure**: Semantic use of an `<article>` for the card, with strict separation between the visual header (housing the animation) and the content body.
  - **Color Logic**: High contrast is mandatory. The light scheme uses a warm beige background (`#F4EFE6`), stark black borders (`#000000`), a pale pink container for the Lottie (`#FFC5C5`), and a vivid accent color.
  - **Typographic Hierarchy**: `Space Grotesk` (Google Fonts) provides the bold, geometric look essential for brutalist titles and buttons. `Inter` handles the body copy for maximum legibility. 
  - **CSS Properties**: Hard `box-shadow` values without blur (e.g., `8px 8px 0px #000`) and thick `border: 4px solid #000`.

* **Step B: Layout & Compositional Style**
  - **Card System**: CSS Flexbox column layout. 
  - **Compartmentalization**: A thick internal border separates the animation wrapper from the text content area, reinforcing the "raw structural" look of Neo-Brutalism.
  - **Proportions**: The card is constrained to a max-width (e.g., `400px`), with generous padding (`2rem` inside containers) to allow the bold typography to breathe.

* **Step C: Interactive Behavior & Animations**
  - **Lottie Playback**: The vector animation is set to `loop` and `autoplay` natively.
  - **CSS Hover State**: Hovering the card triggers a hardware-accelerated translation (`transform: translate(-4px, -4px)`) and expands the solid box-shadow, simulating a physical 3D button press.
  - **JS Interaction API**: JavaScript targets the Lottie player to increase animation playback speed (`player.setSpeed(1.5)`) on hover, and reset the timeline (`player.seek(0)`) on click, creating a tight feedback loop between DOM events and the animation engine.

# Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Vector Animation Engine** | `<lottie-player>` CDN script | The industry standard for parsing and rendering Lottie JSON files in the browser; GPU-accelerated and vastly smaller than GIFs/videos. |
| **Animation Interaction** | LottiePlayer JS API | Exposes simple methods (`setSpeed()`, `seek()`) to map user hover/click events directly to the animation timeline. |
| **Neo-Brutalist Layout** | Pure CSS (Box-shadow, Borders) | Native CSS achieves the exact hard-edged, bold aesthetic from the video's Figma file without relying on complex SVGs. |
| **Typography** | Google Fonts CDN | Injects `Space Grotesk` and `Inter` to perfectly emulate the raw, structural typographic feel of brutalism. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Explore your new skills",
    body_text: str = "New skills diversify your job options and help you to keep up with the fast-changing world.",
    color_scheme: str = "light",        # "dark" or "light"
    accent_color: str = "#6C5CE7",     # CSS hex color for the call-to-action
    width_px: int = 420,
    height_px: int = 700,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Neo-Brutalist Lottie Feature Card.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#121212"
        text_color = "#ffffff"
        border_color = "#ffffff"
        card_bg = "#1e1e1e"
        lottie_bg = "#2a2a2a"
        btn_text = "#000000"
    else:
        bg_color = "#F4EFE6"
        text_color = "#000000"
        border_color = "#000000"
        card_bg = "#FFFBF2"
        lottie_bg = "#FFC5C5"
        btn_text = "#ffffff"

    # Using the exact animation URL generated in the video tutorial
    # If the file is inaccessible, the player fails gracefully.
    lottie_url = "https://lottie.host/48bfaa2f-8364-4384-9964-b508431398ae/6rZxAJjQ89.json"

    # === CSS ===
    css = f"""/* Neo-Brutalist Lottie Feature Card */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --border-color: {border_color};
    --card-bg: {card_bg};
    --lottie-bg: {lottie_bg};
    --btn-text: {btn_text};
    --width: {width_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    overflow-x: hidden;
}}

.card {{
    width: 100%;
    max-width: var(--width);
    background: var(--card-bg);
    border: 4px solid var(--border-color);
    border-radius: 16px;
    box-shadow: 8px 8px 0px var(--border-color);
    overflow: hidden;
    display: flex;
    flex-direction: column;
    /* Spring-like transition for brutalist interaction */
    transition: transform 0.2s cubic-bezier(0.25, 1, 0.5, 1), box-shadow 0.2s cubic-bezier(0.25, 1, 0.5, 1);
}}

.card:hover {{
    transform: translate(-4px, -4px);
    box-shadow: 12px 12px 0px var(--border-color);
}}

.lottie-container {{
    background: var(--lottie-bg);
    border-bottom: 4px solid var(--border-color);
    padding: 2rem;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
}}

lottie-player {{
    width: 100%;
    height: 240px;
    transition: transform 0.3s ease;
}}

.card:hover lottie-player {{
    transform: scale(1.05);
}}

.card-content {{
    padding: 2.5rem 2rem;
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
}}

.title {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.25rem;
    line-height: 1.1;
    font-weight: 700;
    letter-spacing: -0.02em;
}}

.body-text {{
    font-size: 1.05rem;
    line-height: 1.6;
    font-weight: 500;
    opacity: 0.9;
}}

.btn {{
    background: var(--accent);
    color: var(--btn-text);
    border: 4px solid var(--border-color);
    border-radius: 8px;
    padding: 1rem 1.5rem;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 1.15rem;
    box-shadow: 4px 4px 0px var(--border-color);
    cursor: pointer;
    transition: all 0.15s ease;
    align-self: flex-start;
    margin-top: 0.5rem;
}}

.btn:hover {{
    transform: translate(-2px, -2px);
    box-shadow: 6px 6px 0px var(--border-color);
    background: var(--text);
    color: var(--bg);
}}

.btn:active {{
    transform: translate(4px, 4px);
    box-shadow: 0px 0px 0px var(--border-color);
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Neo-Brutalist Lottie Feature Card</title>
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@600;700&family=Inter:wght@400;500&display=swap" rel="stylesheet">
    
    <!-- Custom CSS -->
    <link rel="stylesheet" href="style.css">
    
    <!-- Lottie Player Web Component -->
    <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
</head>
<body>

    <article class="card">
        <header class="lottie-container">
            <!-- 
               If the tutorial's exact URL expires, the player fails gracefully. 
               Feel free to swap the src attribute with any valid Lottie JSON.
            -->
            <lottie-player 
                src="{lottie_url}" 
                background="transparent" 
                speed="1" 
                loop 
                autoplay>
            </lottie-player>
        </header>
        <div class="card-content">
            <h2 class="title">{title_text}</h2>
            <p class="body-text">{body_text}</p>
            <button class="btn">Start Learning</button>
        </div>
    </article>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Lottie Interaction Logic
document.addEventListener('DOMContentLoaded', () => {{
    const card = document.querySelector('.card');
    const player = document.querySelector('lottie-player');
    const btn = document.querySelector('.btn');

    // Make the animation react dynamically to user interaction
    card.addEventListener('mouseenter', () => {{
        // Speed up animation to reward hover intent
        if(player && typeof player.setSpeed === 'function') {{
            player.setSpeed(1.5);
        }}
    }});

    card.addEventListener('mouseleave', () => {{
        // Return to passive speed
        if(player && typeof player.setSpeed === 'function') {{
            player.setSpeed(1.0);
        }}
    }});
    
    // Wire the Call-to-Action to reset/restart the animation timeline
    btn.addEventListener('click', (e) => {{
        if(player && typeof player.seek === 'function' && typeof player.play === 'function') {{
            player.seek(0);
            player.play();
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

# Accessibility & Performance Notes

* **Accessibility**: 
  - The animation functions as a visual enhancement; it is contained within a `<header>` to establish document structure.
  - The Lottie player operates without breaking keyboard navigation, and the button uses standard focusable DOM interactions.
  - To be strictly WCAG compliant, you might consider dynamically pausing the `<lottie-player>` if `window.matchMedia('(prefers-reduced-motion: reduce)').matches` is true.
* **Performance**: 
  - Using Lottie JSON format combined with the web component is immensely more performant than using an animated GIF or video (file sizes are routinely 80%+ smaller).
  - The hover transitions use GPU-accelerated CSS properties (`transform`) rather than expensive layout changes.
  - The Lottie player loads via CDN. For production environments, it is recommended to self-host the script or ensure appropriate caching headers are set.