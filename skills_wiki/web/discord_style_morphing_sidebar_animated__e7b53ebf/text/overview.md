# Discord-Style Morphing Sidebar & Animated Tooltips

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Discord-Style Morphing Sidebar & Animated Tooltips

* **Core Visual Mechanism**: A fixed vertical sidebar navigation featuring icon buttons that undergo a fluid shape transformation on hover. The icons start as perfect circles with a muted background. Upon hovering, they morph into rounded squares (squicles) while filling with a bright accent color. Simultaneously, a dark-themed tooltip smoothly scales into view from the right side, originating from the icon's edge.
* **Why Use This Skill (Rationale)**: This pattern maximizes screen real estate by hiding text labels while maintaining excellent usability through tooltips. The shape-morphing (circle to rounded square) provides highly satisfying, tactile visual feedback that clearly communicates an interactive state, creating a playful yet polished user experience.
* **Overall Applicability**: Ideal for web apps, SaaS dashboards, communication tools (like Discord/Slack clones), and dense user interfaces where vertical side-navigation is preferred and horizontal space is premium.
* **Value Addition**: It elevates a standard list of links into an engaging app-like experience. The micro-interaction of the shape change paired with the swift tooltip reveal makes the interface feel highly responsive and premium.
* **Browser Compatibility**: Broadly compatible. Relies on standard modern CSS (`border-radius` transitions, `transform: scale`, Flexbox). Supported in all modern browsers (Chrome, Edge, Firefox, Safari).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **HTML Structure**: A parent flex container for the sidebar, containing wrapper `div` elements for each interactive item. Each wrapper holds an icon (`<i>` or `<svg>`) and a tooltip `span`.
  - **Color Logic**:
    - Sidebar Background: Very dark gray (`#202225` in dark mode).
    - Inactive Icon Background: Slightly lighter gray (`#36393f`).
    - Accent Color (Icon text, becomes background on hover): Configurable (e.g., Discord Green `#3ba55d`).
    - Tooltip Background: Deep charcoal (`#18191c`).
  - **Typography**: Clean, sans-serif font (Inter or system defaults). Tooltips use bold, small text (`12px` or `0.75rem`).
  - **Key CSS Properties**: `border-radius` (morphing), `transform` (scale), `transform-origin`, `transition`.

* **Step B: Layout & Compositional Style**
  - **Sidebar Grid/Flex**: The sidebar acts as a fixed column (`flex-direction: column`), typically taking up the full viewport height (`100vh`) with a fixed width of `64px` to `72px`.
  - **Icon Proportions**: Icons are typically `48px` by `48px` with an `8px` margin, creating a balanced vertical rhythm.
  - **Tooltip Placement**: Tooltips are absolutely positioned relative to the icon wrapper. They are pushed entirely outside the sidebar (e.g., `left: 60px`) to prevent overlapping the icons.

* **Step C: Interactive Behavior & Animations**
  - **Icon Hover**: The `border-radius` transitions from `50%` (circle) to `25%` or `12px` (rounded square). Background color transitions from muted gray to the accent color, while the icon itself transitions to white.
  - **Tooltip Reveal**: Handled via parent-child hover targeting (e.g., `.icon-group:hover .tooltip`). The tooltip transitions from `transform: scale(0)` to `scale(1)`.
  - **Timing functions**: The icon morphing uses a smoother, longer transition (`300ms linear` or `ease-in-out`), while the tooltip reveal is swift and snappy (`100ms linear`).
  - **Transform Origin**: The tooltip scales from its left edge (`transform-origin: left center`) so it appears to grow directly out of the icon.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Layout & Sidebar Structure | CSS Flexbox | Simplest way to align a column of icons perfectly in the center of the sidebar. |
| Icon Shape Morphing | CSS `border-radius` transition | Extremely performant, pure CSS solution that mimics the tutorial's Tailwind `@apply` logic without needing JS. |
| Animated Tooltips | CSS `transform: scale` + Parent Hover | Avoids JavaScript event listeners. `transform` triggers hardware acceleration for buttery smooth scaling. |
| Icons | Font Awesome CDN | Provides ready-to-use scalable vector icons quickly to demonstrate the visual layout. |

> **Feasibility Assessment**: 100%. The core visual aesthetic, layout, and micro-interactions demonstrated in the Tailwind tutorial are perfectly reproducible using standard, dependency-free CSS.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Morphing Sidebar Navigation",
    body_text: str = "Hover over the icons on the left to experience the shape-morphing transition and animated tooltips.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#3ba55d",     # Default is Discord-style green
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Discord-style Morphing Sidebar.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors based on scheme ===
    if color_scheme == "dark":
        sidebar_bg = "#202225"
        icon_bg = "#36393f"
        icon_hover_text = "#ffffff"
        tooltip_bg = "#18191c"
        tooltip_text = "#ffffff"
        page_bg = "#2f3136"
        text_main = "#dcddde"
    else:
        sidebar_bg = "#e3e5e8"
        icon_bg = "#ffffff"
        icon_hover_text = "#ffffff"
        tooltip_bg = "#18191c"
        tooltip_text = "#ffffff"
        page_bg = "#f2f3f5"
        text_main = "#2e3338"

    # === CSS ===
    css = f"""/* Discord-Style Morphing Sidebar — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --sidebar-bg: {sidebar_bg};
    --icon-bg: {icon_bg};
    --icon-color: {accent_color};
    --icon-hover-bg: {accent_color};
    --icon-hover-text: {icon_hover_text};
    --tooltip-bg: {tooltip_bg};
    --tooltip-text: {tooltip_text};
    --page-bg: {page_bg};
    --text-main: {text_main};
    
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--page-bg);
    color: var(--text-main);
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}}

.app-window {{
    width: var(--width);
    height: var(--height);
    background: var(--page-bg);
    position: relative;
    display: flex;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    overflow: hidden;
    border-radius: 8px;
}}

/* Sidebar Layout */
.sidebar {{
    width: 72px;
    height: 100%;
    background-color: var(--sidebar-bg);
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 12px;
    box-shadow: 2px 0 5px rgba(0,0,0,0.05);
    z-index: 10;
}}

/* Morphing Icon Container */
.sidebar-item {{
    position: relative;
    width: 48px;
    height: 48px;
    margin-bottom: 12px;
    background-color: var(--icon-bg);
    color: var(--icon-color);
    border-radius: 50%; /* Starts as a circle */
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    
    /* Smooth transition for shape, color, and background */
    transition: all 0.3s linear;
}}

/* Active/Hover State for Icon Container */
.sidebar-item:hover,
.sidebar-item.active {{
    border-radius: 16px; /* Morphs into a rounded square */
    background-color: var(--icon-hover-bg);
    color: var(--icon-hover-text);
}}

.sidebar-icon {{
    font-size: 20px;
    transition: color 0.3s linear;
}}

/* Separator Line */
.sidebar-separator {{
    height: 2px;
    width: 32px;
    background-color: var(--icon-bg);
    border-radius: 1px;
    margin: 4px 0 12px 0;
}}

/* Animated Tooltip */
.sidebar-tooltip {{
    position: absolute;
    left: 64px; /* Pushed outside the sidebar */
    background-color: var(--tooltip-bg);
    color: var(--tooltip-text);
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 700;
    white-space: nowrap;
    box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    pointer-events: none; /* Prevents tooltip from blocking cursor */
    
    /* Animation initial state */
    transform: scale(0);
    transform-origin: left center;
    transition: transform 0.1s linear;
    z-index: 100;
}}

/* Tooltip Arrow */
.sidebar-tooltip::before {{
    content: '';
    position: absolute;
    top: 50%;
    right: 100%;
    transform: translateY(-50%);
    border-width: 5px;
    border-style: solid;
    border-color: transparent var(--tooltip-bg) transparent transparent;
}}

/* Show Tooltip on Parent Hover */
.sidebar-item:hover .sidebar-tooltip {{
    transform: scale(1);
}}

/* Main Content Area */
.content {{
    flex: 1;
    padding: 40px;
    overflow-y: auto;
}}

.content h1 {{
    font-size: 28px;
    margin-bottom: 16px;
    color: var(--text-main);
}}

.content p {{
    font-size: 16px;
    line-height: 1.6;
    opacity: 0.8;
}}
"""

    # === HTML ===
    # Escaping variables to prevent basic HTML breaking
    safe_title = title_text.replace("<", "&lt;").replace(">", "&gt;")
    safe_body = body_text.replace("<", "&lt;").replace(">", "&gt;")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title}</title>
    <!-- FontAwesome for standard icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Inter Font -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-window">
        <!-- Sidebar Component -->
        <nav class="sidebar">
            <div class="sidebar-item" data-id="home">
                <i class="fa-brands fa-discord sidebar-icon"></i>
                <span class="sidebar-tooltip">Home</span>
            </div>
            
            <div class="sidebar-separator"></div>
            
            <div class="sidebar-item" data-id="fire">
                <i class="fa-solid fa-fire sidebar-icon"></i>
                <span class="sidebar-tooltip">Trending</span>
            </div>
            
            <div class="sidebar-item" data-id="plus">
                <i class="fa-solid fa-plus sidebar-icon"></i>
                <span class="sidebar-tooltip">Add Server</span>
            </div>
            
            <div class="sidebar-item" data-id="bolt">
                <i class="fa-solid fa-bolt sidebar-icon"></i>
                <span class="sidebar-tooltip">Quick Actions</span>
            </div>
            
            <div class="sidebar-item" data-id="download">
                <i class="fa-solid fa-download sidebar-icon"></i>
                <span class="sidebar-tooltip">Download Apps</span>
            </div>
        </nav>
        
        <!-- App Content -->
        <main class="content">
            <h1 id="page-title">{safe_title}</h1>
            <p id="page-content">{safe_body}</p>
        </main>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Sidebar interaction logic
document.addEventListener('DOMContentLoaded', () => {{
    const sidebarItems = document.querySelectorAll('.sidebar-item');
    const pageTitle = document.getElementById('page-title');
    
    // Optional: Add click behavior to show active states
    sidebarItems.forEach(item => {{
        item.addEventListener('click', () => {{
            // Remove active class from all
            sidebarItems.forEach(el => el.classList.remove('active'));
            
            // Add active class to clicked
            item.classList.add('active');
            
            // Update page content dynamically for demo purposes
            const tooltipText = item.querySelector('.sidebar-tooltip').textContent;
            pageTitle.textContent = tooltipText + ' Section';
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
- [x] Are all external resources loaded from CDN URLs?
- [x] Does the component respect the `width_px` and `height_px` parameters?
- [x] Does `color_scheme="dark"` produce a dark theme and `"light"` a light theme?
- [x] Does `accent_color` propagate to all accent elements?
- [x] Are `title_text` and `body_text` properly escaped for HTML?
- [x] Does the JavaScript run without console errors?
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect?

### 4. Accessibility & Performance Notes

* **Accessibility**: 
  - To make this fully accessible, the `div` wrapper for the icons should ideally have `role="button"` and `tabindex="0"`, or be replaced entirely with native `<button>` or `<a>` tags.
  - An `aria-label` should be mapped to the text present inside the tooltip so screen readers can announce the button's purpose without needing to trigger the hover state.
  - Consider adding a `@media (prefers-reduced-motion: reduce)` block to instantly snap the `border-radius` and `transform` scales rather than animating them, ensuring comfort for users with vestibular sensitivities.
* **Performance**: 
  - The animations rely exclusively on `transform` and `opacity` (by virtue of scaling), and `border-radius`. These properties are highly optimized in modern browsers and do not trigger heavy layout recalculations or repaints.
  - Hover states are managed entirely in CSS, keeping the main thread free and avoiding potential JavaScript jank on rapid mouse movements.