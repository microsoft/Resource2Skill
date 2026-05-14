# Scroll-Spy Navigation Bar

## Analysis

Here is the extraction of the web component design pattern and the reproducible code based on the tutorial.

### 1. High-level Design Pattern Extraction

> **Skill Name**: Scroll-Spy Navigation Bar

* **Core Visual Mechanism**: A fixed/sticky navigation header combined with "scroll spy" logic. As the user scrolls down the page, the navigation links dynamically highlight (changing color) to indicate which content section is currently visible in the viewport. 
* **Why Use This Skill (Rationale)**: This pattern creates strong spatial awareness for the user. In long-form pages, it acts as a real-time progress indicator and a map, helping users understand where they are within the document hierarchy without needing to scroll back up.
* **Overall Applicability**: Perfect for single-page applications (SPAs), product landing pages, portfolios, and long-form articles where content is divided into distinct, full-screen vertical sections.
* **Value Addition**: Transforms static anchor links into an interactive, state-aware UI element. It bridges the gap between layout and navigation, making long scrolling pages feel structured and intentional rather than overwhelming.
* **Browser Compatibility**: Broadly supported. The logic relies on standard DOM properties (`scrollTop`, `offsetTop`, `offsetHeight`) and the styling uses flexbox and sticky positioning, which are universally supported in modern browsers.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**: A high-contrast aesthetic. Dark themes utilize deep charcoal backgrounds (e.g., `#1f242d`, `#323946`) paired with stark white text and a vivid neon accent color (e.g., Cyan `#0ef`) exclusively used to denote active states and hover interactions.
  - **Typography**: Uses 'Poppins' (or similar geometric sans-serif). The logo and active links are bolded (`font-weight: 600`), while default links are medium (`500`). Section headers are massive (`100px`, `700` weight) to dominate the viewport.
  - **CSS Properties**: The heavy lifting is done by `position: sticky` (for the header), `:nth-of-type(even)` for alternating section backgrounds, and smooth `color` transitions.

* **Step B: Layout & Compositional Style**
  - **Header Alignment**: Flexbox with `justify-content: space-between` pushes the logo to the left and navigation links to the right. 
  - **Section Scale**: Each `<section>` is forced to at least `100vh` (or 100% of the container height), centering its content vertically and horizontally using Flexbox. This creates a "presentation slide" rhythm.

* **Step C: Interactive Behavior & Animations**
  - **Scroll Spying**: A JavaScript event listener tracks the scroll position. It compares the current scroll `top` against the `offsetTop` and `offsetHeight` boundaries of each section. When the viewport crosses a boundary, it updates the `.active` CSS class on the corresponding navigation link.
  - **Smooth Scrolling**: Clicking a nav link triggers a smooth transition down the page, calculating the destination offset minus the height of the sticky header so the content isn't obscured.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Sticky Navigation** | CSS `position: sticky` | Keeps the header visible without taking it entirely out of the document flow, making offset calculations cleaner than absolute fixed positioning. |
| **Section Layout** | CSS Flexbox & `min-height` | `min-height: 100%` ensures each section dominates the view, while flexbox perfectly centers the typography. |
| **Active State Tracking** | JavaScript Scroll Event | Accurately reproduces the tutorial's logic, checking if the current scroll position falls between the top and bottom boundaries of an element. |
| **Smooth Anchoring** | JS `scrollTo()` | Prevents native anchor links from shifting the entire browser window, keeping the effect perfectly constrained inside the reusable component widget. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "ActiveLink.",
    body_text: str = "Welcome to our responsive single-page platform. Scroll down to explore our services and portfolio.",
    color_scheme: str = "dark",
    accent_color: str = "#00efff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Scroll-Spy Navigation Bar effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#1f242d"
        alt_bg_color = "#323946"
        header_bg = "#11141a"
        text_color = "#ffffff"
        nav_text = "#ffffff"
    else:
        bg_color = "#f0f2f5"
        alt_bg_color = "#e4e6eb"
        header_bg = "#ffffff"
        text_color = "#1a1a1a"
        nav_text = "#333333"

    # === CSS ===
    css = f"""/* Scroll-Spy Navigation Component */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --alt-bg: {alt_bg_color};
    --header-bg: {header_bg};
    --text: {text_color};
    --nav-text: {nav_text};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Poppins', sans-serif;
    background: #000;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

/* Constrained container for reproducible isolation */
.scroll-container {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    overflow-y: auto;
    overflow-x: hidden;
    position: relative;
    background: var(--bg);
    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
}}

/* Sticky Header */
header {{
    position: sticky;
    top: 0;
    left: 0;
    width: 100%;
    padding: 25px 8%;
    background: var(--header-bg);
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 100;
}}

.logo {{
    font-size: 28px;
    color: var(--nav-text);
    text-decoration: none;
    font-weight: 700;
    letter-spacing: -0.5px;
}}

.nav-links a {{
    font-size: 18px;
    color: var(--nav-text);
    text-decoration: none;
    font-weight: 500;
    margin-left: 35px;
    transition: color 0.3s ease;
}}

.nav-links a:hover,
.nav-links a.active {{
    color: var(--accent);
}}

/* Full-height Content Sections */
section {{
    min-height: var(--height);
    display: flex;
    justify-content: center;
    align-items: center;
    background: var(--bg);
    padding: 100px 8%;
}}

section:nth-of-type(even) {{
    background: var(--alt-bg);
}}

.section-content {{
    text-align: center;
    max-width: 800px;
}}

section h2 {{
    font-size: clamp(60px, 8vw, 100px);
    font-weight: 700;
    color: var(--text);
    margin-bottom: 20px;
}}

section p {{
    font-size: 18px;
    line-height: 1.6;
    color: var(--text);
    opacity: 0.8;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text} Navigation</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <div class="scroll-container">
        <header>
            <a href="#home" class="logo">{title_text}</a>
            <nav class="nav-links">
                <a href="#home" class="active">Home</a>
                <a href="#about">About</a>
                <a href="#services">Services</a>
                <a href="#portfolio">Portfolio</a>
                <a href="#contact">Contact</a>
            </nav>
        </header>

        <section id="home">
            <div class="section-content">
                <h2>Home</h2>
                <p>{body_text}</p>
            </div>
        </section>
        
        <section id="about">
            <div class="section-content">
                <h2>About</h2>
            </div>
        </section>
        
        <section id="services">
            <div class="section-content">
                <h2>Services</h2>
            </div>
        </section>
        
        <section id="portfolio">
            <div class="section-content">
                <h2>Portfolio</h2>
            </div>
        </section>
        
        <section id="contact">
            <div class="section-content">
                <h2>Contact</h2>
            </div>
        </section>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""document.addEventListener('DOMContentLoaded', () => {{
    const container = document.querySelector('.scroll-container');
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('.nav-links a');
    const header = document.querySelector('header');

    // 1. Hande clicks for smooth scrolling inside the constrained container
    navLinks.forEach(link => {{
        link.addEventListener('click', (e) => {{
            e.preventDefault();
            const targetId = link.getAttribute('href').substring(1);
            const targetSection = document.getElementById(targetId);
            
            if (targetSection) {{
                const headerHeight = header.offsetHeight;
                container.scrollTo({{
                    // Subtract header height so content isn't hidden under the sticky nav
                    top: targetSection.offsetTop - headerHeight,
                    behavior: 'smooth'
                }});
            }}
        }});
    }});

    // 2. Scroll Spy Logic
    container.addEventListener('scroll', () => {{
        let top = container.scrollTop;
        const headerHeight = header.offsetHeight;
        
        sections.forEach(sec => {{
            // Calculate effective position relative to scroll container
            let offset = sec.offsetTop - headerHeight - 150; // 150px buffer to trigger slightly early
            let height = sec.offsetHeight;
            let id = sec.getAttribute('id');

            // Check if current scroll position is within the bounds of this section
            if (top >= offset && top < offset + height) {{
                
                // Clear active state from all links
                navLinks.forEach(link => {{
                    link.classList.remove('active');
                }});
                
                // Add active state to corresponding link
                let activeLink = document.querySelector(`.nav-links a[href="#${{id}}"]`);
                if (activeLink) {{
                    activeLink.classList.add('active');
                }}
            }}
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

* **Accessibility (a11y)**: 
  * Currently, the active link relies purely on a CSS class (`.active`) which changes the visual color. For screen readers to understand which page is currently active, the JavaScript should ideally toggle the `aria-current="page"` attribute on the active link rather than just updating the class.
  * Contrast ratios in the dark theme (`#00efff` cyan on `#11141a` dark grey) pass WCAG AA standards, providing excellent visibility.
* **Performance**: 
  * The code attaches an un-throttled event listener directly to the `scroll` event. This means the callback fires hundreds of times per second while scrolling, triggering a DOM query (`querySelectorAll`) each time. 
  * **Optimization Path**: While this implementation stays strictly faithful to the visual tutorial's extraction logic, in a production environment, this event should either be wrapped in a simple `debounce`/`throttle` function, or entirely replaced by the modern `IntersectionObserver` API, which offloads the boundary calculations to the browser's native rendering engine.