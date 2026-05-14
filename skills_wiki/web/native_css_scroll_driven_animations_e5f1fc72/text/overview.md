# Native CSS Scroll-Driven Animations

## Analysis

# Skill Strategy Document

### 1. High-level Design Pattern Extraction

> **Skill Name**: Native CSS Scroll-Driven Animations

* **Core Visual Mechanism**: Linking CSS keyframe animations directly to the scroll position of the page or the visibility of specific elements within the viewport, entirely without JavaScript. It utilizes the modern `animation-timeline`, `scroll-timeline`, and `view-timeline` CSS properties to create reading progress bars, scale-up image reveals, and slide-in list items as the user scrolls.
* **Why Use This Skill (Rationale)**: Scroll-linked animations create a dynamic and engaging narrative flow, drawing the user's eye to new content as it enters the screen. Historically, this required complex JavaScript intersection observers or heavy scroll event listeners, leading to performance jank. Native CSS scroll timelines move this computation to the browser's compositor thread, resulting in buttery-smooth animations that are much easier to author.
* **Overall Applicability**: Perfect for long-form articles, landing pages, product feature showcases, timeline designs, and portfolios where storytelling dictates that elements should animate into place as the user discovers them.
* **Value Addition**: It transforms a static block of text and images into an interactive experience. The top progress bar gives immediate contextual feedback on article length, while the entrance animations add a layer of polish and modernity to the layout.
* **Browser Compatibility**: **Important:** The `animation-timeline` suite is a modern CSS feature (broadly supported in Chrome/Edge 115+, Firefox 133+ or with flags, and currently lacking Safari support without feature flags). For production, it requires fallback strategies (e.g., using `@supports` to ensure elements aren't permanently hidden in unsupported browsers).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - A fixed progress bar at the top of the viewport.
  - Standard typography-driven article layout (`<h1>`, `<p>`, `<ul>`, `<li>`).
  - Inline images taking up significant viewport space.
  - **Color Logic**: Neutral background (e.g., `#f8f9fa` for light, `#0d111c` for dark) with a vibrant accent color (`#ff8400` in the tutorial, adaptable to `#00bfff`) for the progress bar and list item bullets.
  - **Key CSS Properties**: `animation-timeline`, `scroll-timeline-name`, `view-timeline-name`, `animation-range`, `transform: scale()`, `transform: translateX()`, `opacity`.

* **Step B: Layout & Compositional Style**
  - Single-column centered layout constrained by a `max-width` (e.g., `700px`) for optimal reading line length.
  - Ample vertical whitespace (`line-height: 2em`, `margin-bottom: 1.5em`) to ensure scrolling is required to see the effects.
  - The progress bar is taken out of normal flow using `position: fixed; top: 0; left: 0; width: 100%;`.

* **Step C: Interactive Behavior & Animations**
  - **Page Progress Bar**: Tied to the root scroll. `transform-origin: 0 50%` ensures it grows from left to right. Keyframes animate `transform: scaleX(0)` to `scaleX(1)`.
  - **Image Reveal**: Tied to the image's own view timeline. Keyframes animate `opacity: 0` -> `1` and `transform: scale(0)` -> `scale(1)`.
  - **List Item Slide-in**: Tied to each list item's view timeline. Keyframes animate `opacity: 0` -> `1` and `transform: translateX(-200px)` -> `translateX(0)`.
  - **Animation Range**: Uses ranges like `entry 25% cover 50%` meaning the animation begins when the element has crossed 25% into the viewport's entry zone, and finishes when it covers 50% of its total potential animation area.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Scroll Tracking | CSS `scroll-timeline` | Native browser implementation, zero JavaScript overhead, perfectly synced with the compositor thread. |
| Viewport Intersection | CSS `view-timeline` | Native replacement for `IntersectionObserver`, allows linking keyframes to element visibility percentage. |
| Entrance Transitions | CSS `@keyframes` | Standard, hardware-accelerated transforms and opacity changes. |
| Browser Fallback | CSS `@supports` | Ensures content remains visible and static on browsers (like Safari) that do not yet support scroll timelines. |

> **Feasibility Assessment**: 100%. The tutorial relies entirely on CSS features that can be fully reproduced in the provided code block. I have added `@supports` wrappers around the hiding logic to ensure the generated component works (i.e., degrades gracefully) in all browsers.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Scroll Animation Article",
    body_text: str = "Scroll down to see native CSS animations in action. No JavaScript is required for these effects.",
    color_scheme: str = "dark",
    accent_color: str = "#00bfff",
    width_px: int = 800,
    height_px: int = 1000,
    **kwargs,
) -> dict:
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#121212"
        text_color = "#e0e0e0"
        surface_color = "#1e1e1e"
    else:
        bg_color = "#ffffff"
        text_color = "#333333"
        surface_color = "#f5f5f5"

    css = f"""/* Native CSS Scroll Animations */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    line-height: 1.8;
}}

/* Set up the root scroll timeline for the progress bar */
html {{
    scroll-timeline-name: --page-scroll;
    scroll-timeline-axis: y;
}}

.progress-bar {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 6px;
    background-color: var(--accent);
    transform-origin: 0 50%;
    z-index: 100;
    /* Connect to the page scroll timeline */
    animation: progress-anim linear;
    animation-timeline: --page-scroll;
}}

@keyframes progress-anim {{
    from {{ transform: scaleX(0); }}
    to {{ transform: scaleX(1); }}
}}

main {{
    max-width: {width_px}px;
    margin: 0 auto;
    padding: 60px 20px 100vh 20px; /* Extra padding at bottom to allow scrolling */
}}

h1 {{
    font-size: 3rem;
    margin-bottom: 0.5em;
    color: var(--text);
}}

h2 {{
    font-size: 2rem;
    margin: 2em 0 1em;
    border-bottom: 2px solid var(--surface);
    padding-bottom: 0.5em;
}}

p {{
    font-size: 1.125rem;
    margin-bottom: 1.5em;
    color: var(--text);
    opacity: 0.9;
}}

.placeholder-text {{
    margin-bottom: 300px; /* Force scrolling space */
}}

.image-container {{
    width: 100%;
    height: 400px;
    background: var(--surface);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 40px 0;
    overflow: hidden;
    position: relative;
    border: 1px solid rgba(255, 255, 255, 0.1);
}}

.image-container::after {{
    content: 'Image Placeholder';
    color: var(--text);
    opacity: 0.5;
    font-size: 1.5rem;
    font-weight: 600;
}}

ul {{
    list-style: none;
    padding-left: 1rem;
}}

li {{
    font-size: 1.25rem;
    margin-bottom: 1rem;
    padding-left: 1.5rem;
    position: relative;
}}

li::before {{
    content: '•';
    color: var(--accent);
    font-weight: bold;
    font-size: 1.5rem;
    position: absolute;
    left: 0;
    top: -4px;
}}

/* === VIEW TIMELINE ANIMATIONS === */

/* Feature detection: Only apply starting hidden states if the browser supports view-timeline */
@supports (animation-timeline: view()) {{
    .reveal-img {{
        opacity: 0;
        view-timeline-name: --revealing-image;
        view-timeline-axis: y;
        animation: appear linear forwards;
        animation-timeline: --revealing-image;
        animation-range: entry 10% cover 40%;
    }}

    .slide-list li {{
        opacity: 0;
        /* Using the shorthand view() function instead of named timelines for the list items */
        animation: fadeLeft linear forwards;
        animation-timeline: view();
        animation-range: entry 10% cover 30%;
    }}
}}

@keyframes appear {{
    from {{
        opacity: 0;
        transform: scale(0.5);
    }}
    to {{
        opacity: 1;
        transform: scale(1);
    }}
}}

@keyframes fadeLeft {{
    from {{
        opacity: 0;
        transform: translateX(-100px);
    }}
    to {{
        opacity: 1;
        transform: translateX(0);
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="progress-bar"></div>

    <main>
        <h1>{title_text}</h1>
        <p><strong>Note:</strong> To see these effects, use Chrome/Edge 115+ or a compatible browser. In unsupported browsers, content will degrade gracefully and remain visible.</p>
        <p>{body_text}</p>
        
        <p class="placeholder-text">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
            <br><br>
            Keep scrolling down...
        </p>

        <h2>Scale Reveal Effect</h2>
        <p>This image container will scale up and fade in as it enters the viewport based on its own view timeline.</p>
        
        <div class="image-container reveal-img"></div>

        <p class="placeholder-text">
            Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Curabitur pretium tincidunt lacus. Nulla gravida orci a odio.
            <br><br>
            Keep scrolling down...
        </p>

        <h2>Sequential Slide Reveal</h2>
        <p>Each list item is linked to its own view timeline, causing them to slide in individually as they cross the threshold.</p>
        
        <ul class="slide-list">
            <li>First item sliding in from the left</li>
            <li>Second item follows as you scroll</li>
            <li>Third item appearing smoothly</li>
            <li>Fourth item completing the list</li>
            <li>Fifth item just to be sure</li>
        </ul>
        
        <p style="margin-top: 100px; text-align: center; opacity: 0.5;">End of Demo</p>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    js = """// No JavaScript required for these scroll animations!
// The effects are handled entirely by CSS animation-timeline properties.
console.log('Scroll animations initialized via CSS.');
"""

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

* **Accessibility**: Motion can cause issues for users with vestibular disorders. In a production environment, you must wrap these scroll animations in a `@media (prefers-reduced-motion: no-preference)` query. If the user prefers reduced motion, the CSS should fall back to the static state (opacity 1, scale 1) instantly.
* **Performance**: This is the most performant way to implement scroll animations. By using `animation-timeline`, the browser evaluates the scroll state and applies the transforms/opacity changes directly on the compositor thread. This avoids the main-thread layout thrashing commonly associated with JavaScript `window.addEventListener('scroll')` implementations.
* **Fallback Strategy**: The code utilizes `@supports (animation-timeline: view())` to ensure that browsers lacking support for this modern feature do not render invisible elements. If the feature is unsupported, the `opacity: 0` initial state is ignored, and the content appears statically as normal document flow.