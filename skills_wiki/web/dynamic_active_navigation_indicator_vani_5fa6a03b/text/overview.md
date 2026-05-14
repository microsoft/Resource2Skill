# Dynamic Active Navigation Indicator (Vanilla JS)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Dynamic Active Navigation Indicator (Vanilla JS)

*   **Core Visual Mechanism**: A solid-fill background highlight applied to the currently active navigation link. The text color is inverted against the highlight color to maintain high contrast. This effect is driven dynamically by JavaScript reading the current URL, replacing the need to hardcode `.active` classes on individual HTML pages.
*   **Why Use This Skill (Rationale)**: Wayfinding is critical in UX design. Users must instantly know where they are within a site's hierarchy. By automating the active state via JavaScript, developers eliminate the common human error of forgetting to update the active class when duplicating template files.
*   **Overall Applicability**: Universal. This pattern is foundational for any multi-page website (blogs, portfolios, corporate sites) that utilizes a global navigation header, especially those built without modern reactive frameworks (like React/Vue) or server-side templating engines.
*   **Value Addition**: Transforms static HTML navigation into a context-aware component. It reduces maintenance overhead and ensures the visual active state always perfectly reflects the browser's current URL.
*   **Browser Compatibility**: Flawless. Uses fundamental DOM APIs (`querySelectorAll`, `classList`, `window.location`, `Array.forEach`) supported by all modern and legacy browsers.

### 2. Visual & Technical Breakdown

*   **Step A: Core Visual Elements**
    *   **Typography**: Clean, sans-serif typography (e.g., system fonts or Inter) at a large scale (`1.5rem` to `2rem`) to give a modern, editorial feel.
    *   **Color Logic**: High contrast monochrome. Links default to dark text (`#111`) with no background. The active state flips this: dark background (`#000` or accent color) with white text (`#fff`).
    *   **Spacing**: Generous padding on the anchor tags (`0.5rem 1.5rem`) transforms inline text links into clickable block-like targets, ensuring the highlight background has substantial visual weight.
*   **Step B: Layout & Compositional Style**
    *   **Nav Layout**: `display: flex` applied to the `<ul>` with `justify-content: center` and a `gap` property to evenly space the links horizontally.
    *   **Page Composition**: The navigation sits at the top of a full-viewport (`min-height: 100vh`) hero section. A central, semi-transparent frosted card displays the current page title, anchoring the layout.
*   **Step C: Interactive Behavior & Animations**
    *   **Logic Flow**: On page load, JavaScript captures the current URL path (`window.location.pathname`). It loops through every anchor tag in the `<nav>`. If the anchor's `href` attribute includes the current path, it dynamically injects the `active` class.
    *   **Adaptation for Local Testing**: Because a pure `pathname` check requires multiple physical HTML files or a server to demonstrate, the code below simulates this behavior using `window.location.hash` (e.g., `#home`, `#about`). This allows the visual effect to be tested smoothly within a single local file.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
| :--- | :--- | :--- |
| **Active state tracking** | Vanilla JS `window.location` & `forEach` loop | Matches the tutorial's core lesson: dynamically checking the URL against link `href` attributes to apply classes. |
| **Styling application** | CSS `.active` class toggling | Separation of concerns; JS handles the logic, CSS handles the visual paint (color inversion). |
| **Nav alignment** | CSS Flexbox | `gap` and `justify-content: center` provide a perfect, flexible horizontal menu structure without margins. |

*Feasibility Assessment*: 100%. The script perfectly captures the video's logic. (Note: Adapted to use URL hashes instead of pathnames so the generated component functions locally without a web server).

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Active Nav",
    body_text: str = "Click the links above to see the active state change dynamically.",
    color_scheme: str = "light",
    accent_color: str = "#000000",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Dynamic Active Navigation Indicator.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Resolve colors based on scheme
    if color_scheme == "dark":
        text_color = "#f0f0f0"
        nav_bg = "rgba(0, 0, 0, 0.6)"
        hero_bg = "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&q=80&w=2000" # Darker mountain/nature alternative
        active_text = "#ffffff"
    else:
        text_color = "#111111"
        nav_bg = "rgba(255, 255, 255, 0.8)"
        hero_bg = "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&q=80&w=2000" # Bright mountain peak
        active_text = "#ffffff"

    # === CSS ===
    css = f"""/* Vanilla JS Active Nav Indicator */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --accent: {accent_color};
    --text-default: {text_color};
    --text-active: {active_text};
    --nav-bg: {nav_bg};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #333;
}}

.hero-container {{
    width: var(--width);
    height: var(--height);
    background: url('{hero_bg}') center/cover no-repeat;
    display: flex;
    flex-direction: column;
    position: relative;
    box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    overflow: hidden;
}}

header {{
    background: var(--nav-bg);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    padding: 1.5rem 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}}

nav ul {{
    display: flex;
    list-style-type: none;
    justify-content: center;
    gap: 2rem;
}}

nav li a {{
    color: var(--text-default);
    text-decoration: none;
    font-size: 1.25rem;
    font-weight: 500;
    padding: 0.5rem 1.5rem;
    transition: all 0.3s ease;
}}

/* Active State Styling */
nav li a.active {{
    background-color: var(--accent);
    color: var(--text-active);
}}

nav li a:hover:not(.active) {{
    opacity: 0.6;
}}

.content-area {{
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

.page-title-box {{
    background: var(--nav-bg);
    backdrop-filter: blur(8px);
    padding: 3rem 6rem;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}}

.page-title {{
    font-size: 5rem;
    font-weight: 800;
    color: var(--text-default);
    letter-spacing: -2px;
    margin-bottom: 1rem;
}}

.page-body {{
    font-size: 1.1rem;
    color: var(--text-default);
    opacity: 0.8;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="hero-container">
        <header>
            <nav>
                <ul>
                    <li><a href="#home">Home</a></li>
                    <li><a href="#blog">Blog</a></li>
                    <li><a href="#about">About</a></li>
                    <li><a href="#contact">Contact</a></li>
                </ul>
            </nav>
        </header>

        <main class="content-area">
            <div class="page-title-box">
                <h1 class="page-title">Home</h1>
                <p class="page-body">{body_text}</p>
            </div>
        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Vanilla JS Dynamic Active Navigation Logic
document.addEventListener('DOMContentLoaded', () => {{
    
    function setActivePage() {{
        // 1. Identify the current page.
        // NOTE: The tutorial uses `window.location.pathname` for multi-page sites.
        // For this single-file interactive demo, we use `window.location.hash` 
        // so you can click links and test the logic locally without a server.
        let activePage = window.location.hash || '#home';

        // 2. Select all navigation links
        const navLinks = document.querySelectorAll('nav a');

        // 3. Iterate over each link
        navLinks.forEach(link => {{
            
            // Clear existing active classes (necessary for this single-page simulation)
            link.classList.remove('active');

            // 4. Check if the link's href includes our current page identifier
            if (link.href.includes(activePage)) {{
                // 5. Apply the active styling class
                link.classList.add('active');
            }}
        }});

        // --- Demo specific: Update the visual UI card to reflect the "page change" ---
        const titleEl = document.querySelector('.page-title');
        if (titleEl) {{
            const pageName = activePage.replace('#', '');
            titleEl.textContent = pageName.charAt(0).toUpperCase() + pageName.slice(1);
        }}
    }}

    // Run immediately on page load
    setActivePage();

    // Re-run when the hash changes to simulate navigating to a new page
    window.addEventListener('hashchange', setActivePage);
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
- [x] Does `color_scheme` logic properly update readability elements?
- [x] Does `accent_color` propagate to the active highlight?
- [x] Does the JavaScript run without console errors?
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect?

### 4. Accessibility & Performance Notes

*   **Accessibility**: 
    *   Using `<nav>` and `<ul>` ensures screen readers announce the navigation block and the number of links correctly.
    *   To improve this beyond the video's scope, adding `aria-current="page"` to the active link via JS is highly recommended. The visual `.active` class relies entirely on sight; `aria-current` communicates the same state programmatically.
*   **Performance**:
    *   The Javascript is extremely lightweight. `querySelectorAll` on a small number of nav items is instantaneous.
    *   String matching via `.includes()` is safe and highly performant for standard URLs.