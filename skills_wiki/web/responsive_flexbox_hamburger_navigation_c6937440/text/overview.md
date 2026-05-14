### 1. High-level Design Pattern Extraction

> **Skill Name**: Responsive Flexbox Hamburger Navigation

* **Core Visual Mechanism**: A top-level horizontal navigation bar built with Flexbox that gracefully degrades on smaller viewports. When the screen width drops below a specific breakpoint, the horizontal links collapse into a vertical list (`display: none`), and a minimalist CSS-only "hamburger" icon (`span` elements) appears. Clicking the icon triggers JavaScript to toggle an `.active` class, switching the vertical list back to `display: flex`.
* **Why Use This Skill (Rationale)**: This is the fundamental pattern for modern web navigation. It solves the problem of limited horizontal space on mobile devices, ensuring links remain accessible without breaking the page layout or forcing horizontal scrolling.
* **Overall Applicability**: Essential for nearly every multi-page website, web application, or portfolio. It provides a universal, expected user experience for mobile navigation.
* **Value Addition**: Transforms a rigid, broken header into an adaptive interface. The use of absolute positioning for the hamburger button ensures the structural flexbox flow isn't interrupted during the mobile transition.
* **Browser Compatibility**: Excellent. Relies on standard CSS Flexbox, standard Media Queries (`@media`), and basic DOM manipulation. Works universally across all modern desktop and mobile browsers.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **HTML Structure**: A `<nav>` wrapping a brand `<div>`, an `<a>` toggle button containing three `<span class="bar">` elements, and a `<div>` wrapping a `<ul>` of links.
  - **Color Logic**: High contrast. Typically a dark background (e.g., `#333333`) with white text (`#ffffff`), and a slightly lighter shade for hover states (e.g., `#555555`). 
  - **Typography**: Clean, sans-serif fonts. The brand title is emphasized with a larger size (`1.5rem`) and bold weight.
  - **CSS Constructs**: `display: flex` heavily drives the layout. 

* **Step B: Layout & Compositional Style**
  - **Desktop Layout**: The `.navbar` uses `justify-content: space-between` to push the brand to the left and links to the right. `align-items: center` centers them vertically. Links are laid out horizontally using an inner flex container on the `<ul>`.
  - **Mobile Layout**: At `< 600px`, the `.navbar` switches to `flex-direction: column; align-items: flex-start;`. The links container switches to `width: 100%` and `flex-direction: column`, centering the text for easy tapping.
  - **Toggle Button**: Positioned absolutely (`top: 0.75rem; right: 1rem;`) so it sits neatly in the corner regardless of the column flex flow of the main navbar underneath it. The three horizontal bars are spaced perfectly using `flex-direction: column` and `justify-content: space-between`.

* **Step C: Interactive Behavior & Animations**
  - **Hover**: Background color transitions on the anchor tags to provide clear feedback.
  - **Toggle**: Vanilla JavaScript listens for a click on the hamburger button and calls `.classList.toggle('active')` on the links container. In CSS, the `.active` class overrides `display: none` with `display: flex`.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Responsive Layout | CSS Flexbox & Media Queries | Native, highly performant way to switch between horizontal and vertical stacking based on viewport width. |
| Hamburger Icon | CSS Spans inside Flexbox | Extremely lightweight; avoids the need to load external SVGs or icon fonts. `justify-content: space-between` perfectly spaces the bars. |
| Toggle Logic | Vanilla JS `classList.toggle()` | Simplest, dependency-free way to toggle state classes without needing a heavy framework. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Brand Name",
    body_text: str = "Resize the browser window to see the responsive hamburger menu in action.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#555555",     # Background color on hover
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Flexbox Hamburger Navigation.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        nav_bg = "#333333"
        nav_text = "#ffffff"
        page_bg = "#f4f4f4"
        page_text = "#111111"
        hover_bg = accent_color if accent_color else "#555555"
    else:
        nav_bg = "#f8f9fa"
        nav_text = "#333333"
        page_bg = "#ffffff"
        page_text = "#111111"
        hover_bg = accent_color if accent_color else "#e2e6ea"

    # === CSS ===
    css = f"""/* Responsive Navbar Styles */
*, *::before, *::after {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    padding: 0;
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: {page_bg};
    color: {page_text};
    /* Simulating requested dimensions for demonstration context */
    min-width: 320px;
}}

/* Navbar Container */
.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: {nav_bg};
    color: {nav_text};
}}

.brand-title {{
    font-size: 1.5rem;
    margin: 0.5rem;
    font-weight: bold;
}}

/* Desktop Links */
.navbar-links ul {{
    margin: 0;
    padding: 0;
    display: flex;
}}

.navbar-links li {{
    list-style: none;
}}

.navbar-links li a {{
    text-decoration: none;
    color: {nav_text};
    padding: 1rem;
    display: block;
    transition: background-color 0.2s ease;
}}

.navbar-links li a:hover {{
    background-color: {hover_bg};
}}

/* Mobile Toggle Button (Hidden on Desktop) */
.toggle-button {{
    position: absolute;
    top: 0.75rem;
    right: 1rem;
    display: none;
    flex-direction: column;
    justify-content: space-between;
    width: 30px;
    height: 21px;
}}

.toggle-button .bar {{
    height: 3px;
    width: 100%;
    background-color: {nav_text};
    border-radius: 10px;
}}

/* Responsive Breakpoint */
@media (max-width: 600px) {{
    .toggle-button {{
        display: flex;
    }}

    .navbar-links {{
        display: none;
        width: 100%;
    }}

    .navbar {{
        flex-direction: column;
        align-items: flex-start;
    }}

    .navbar-links ul {{
        width: 100%;
        flex-direction: column;
    }}

    .navbar-links li {{
        text-align: center;
    }}

    .navbar-links li a {{
        padding: 0.5rem 1rem;
    }}

    /* Class added via JavaScript */
    .navbar-links.active {{
        display: flex;
    }}
}}

/* Page Content */
.content {{
    padding: 2rem;
    max-width: 800px;
    margin: 0 auto;
    text-align: center;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text} Navigation</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <nav class="navbar">
        <div class="brand-title">{title_text}</div>
        
        <!-- Hamburger Button -->
        <a href="#" class="toggle-button" aria-label="Toggle navigation">
            <span class="bar"></span>
            <span class="bar"></span>
            <span class="bar"></span>
        </a>
        
        <!-- Navigation Links -->
        <div class="navbar-links">
            <ul>
                <li><a href="#">Home</a></li>
                <li><a href="#">About</a></li>
                <li><a href="#">Services</a></li>
                <li><a href="#">Contact</a></li>
            </ul>
        </div>
    </nav>
    
    <main class="content">
        <h1>Welcome to {title_text}</h1>
        <p>{body_text}</p>
    </main>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Responsive Navbar Toggle Logic
document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.querySelector('.toggle-button');
    const navbarLinks = document.querySelector('.navbar-links');

    toggleButton.addEventListener('click', (e) => {
        e.preventDefault(); // Prevent page jump on '#' link
        navbarLinks.classList.toggle('active');
    });
});
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
  - The toggle button includes an `aria-label="Toggle navigation"` attribute so screen readers announce its purpose, rather than ignoring empty `span` tags.
  - The `e.preventDefault()` in JS ensures clicking the empty `#` anchor link does not aggressively snap the scrollbar to the top of the page, maintaining user context.
* **Performance**:
  - Extremely optimal. Pure CSS handles all the layout shifting based on viewport dimensions.
  - Javascript is restricted strictly to applying a single class string to an element, avoiding any layout thrashing or repetitive event-listener overhead associated with tracking screen resizes via JS.