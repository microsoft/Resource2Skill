### 1. High-level Design Pattern Extraction

> **Skill Name**: Responsive Sticky Navbar with Mobile Wrap-around Dropdown

* **Core Visual Mechanism**: A top-anchored navigation bar that utilizes CSS Flexbox to align branding and links horizontally on desktop. On mobile, the flex container wraps (`flex-wrap: wrap`), pushing the navigation links onto a new row that spans 100% of the width. This "wrap-around" row is toggled via JavaScript using a CSS-drawn hamburger icon, cleanly pushing the page content downwards when expanded.
* **Why Use This Skill (Rationale)**: This is one of the most robust and widely used patterns for navigation. By allowing the flex container to wrap instead of absolutely positioning a dropdown menu, the expanded menu stays within the document flow. This prevents the menu from accidentally obscuring important hero content, making it highly accessible and predictable across devices.
* **Overall Applicability**: Essential for almost any standard website, including SaaS landing pages, portfolios, corporate sites, and e-commerce platforms. The `position: sticky` property ensures the navigation remains accessible as the user scrolls through long content.
* **Value Addition**: Replaces static, hard-to-navigate headers with a responsive system that gracefully degrades based on viewport width, ensuring screen real estate is optimized for mobile users without sacrificing desktop functionality.
* **Browser Compatibility**: High. Uses standard CSS Grid/Flexbox, `position: sticky`, and basic Vanilla JavaScript class toggling. Supported in all modern browsers (Edge, Chrome, Safari, Firefox).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **HTML Structure**: Semantic `<nav>` container holding a logo `div`, a hamburger `div` (composed of three span "bars"), and an unordered list `<ul>` for links.
  - **Color Logic**: A distinct contrast between the navbar background and the page body. E.g., dark mode uses `#1a1a2e` for the navbar and `#0d111c` for the body, with a vibrant cyan accent (`#39ffde`) for the Call-to-Action (CTA) button. 
  - **Typographic Hierarchy**: Uppercase, medium-weight font (`500`) for navigation items to establish them as UI controls rather than reading text.
  - **CSS Properties**: `position: sticky`, `z-index: 1000` (for layering above content), and `border-radius` (for the pill-shaped CTA).

* **Step B: Layout & Compositional Style**
  - **Desktop Layout**: Flexbox with `justify-content: space-between` and `align-items: center` to push the logo to the left and links to the right. 
  - **Mobile Layout**: At `max-width: 768px`, the nav switches its inner items. The hamburger icon is revealed. The link list drops its horizontal flex display, takes `width: 100%`, and relies on the parent's `flex-wrap: wrap` to sit cleanly below the logo/hamburger row.
  - **Proportions**: Navbar minimum height is around `70px`. Links have generous hit areas (`padding: 10px 15px`).

* **Step C: Interactive Behavior & Animations**
  - **Hover States**: Links transition their text color to the accent color over `0.3s ease`. The CTA button reverses its color fill on hover.
  - **Mobile Toggle**: Clicking the hamburger toggles an `active` class on the link list, changing it from `display: none` to `display: flex`. The navbar height dynamically expands, pushing document content down.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Sticky Header | CSS `position: sticky` | Native, performant way to keep headers accessible on scroll without JavaScript math. |
| Desktop & Mobile Layout | CSS Flexbox | `flex-wrap` allows the mobile menu to naturally drop to a new line within the navbar container, simplifying layout logic. |
| Mobile Toggle | Vanilla JS + CSS Class | Toggling an `.active` class avoids the "resize bug" caused by manipulating inline `style.display` directly via JavaScript. |
| Hamburger Icon | CSS Divs | Drawing lines with CSS `div`s is lightweight and allows for easy future animations (like transforming into an 'X'). |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "BrandName",
    body_text: str = "Scroll down to see the navigation bar remain sticky at the top of the viewport. Resize the window below 768px to see the responsive hamburger menu in action.",
    color_scheme: str = "dark",
    accent_color: str = "#39ffde",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Sticky Navbar visual effect.
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        nav_bg = "#1a1a2e"
        nav_text = "#f0f0f0"
        page_bg = "#0d111c"
        page_text = "#a0a0b0"
        border_color = "rgba(255, 255, 255, 0.1)"
        hover_bg = "rgba(255, 255, 255, 0.05)"
    else:
        nav_bg = "#ffffff"
        nav_text = "#111111"
        page_bg = "#f4f4f9"
        page_text = "#444444"
        border_color = "rgba(0, 0, 0, 0.1)"
        hover_bg = "rgba(0, 0, 0, 0.03)"

    css = f"""/* Responsive Sticky Navbar */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --width: {width_px}px;
    --height: {height_px}px;
    --nav-bg: {nav_bg};
    --nav-text: {nav_text};
    --nav-accent: {accent_color};
    --page-bg: {page_bg};
    --page-text: {page_text};
    --border-color: {border_color};
    --hover-bg: {hover_bg};
}}

body {{
    background: #000;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
}}

/* Device viewport container to enforce specified dimensions */
.device-container {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    background: var(--page-bg);
    overflow-y: auto;
    position: relative;
    color: var(--page-text);
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
}}

/* Scrollbar styling for device container */
.device-container::-webkit-scrollbar {{ width: 8px; }}
.device-container::-webkit-scrollbar-track {{ background: var(--page-bg); }}
.device-container::-webkit-scrollbar-thumb {{ background: var(--border-color); border-radius: 4px; }}

/* Navigation Bar Core */
.navbar {{
    position: sticky;
    top: 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap; /* Crucial for mobile row-wrapping */
    padding: 0 40px;
    background-color: var(--nav-bg);
    color: var(--nav-text);
    min-height: 70px;
    z-index: 1000;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
}}

/* Branding / Logo */
.logo {{
    display: flex;
    align-items: center;
    gap: 12px;
}}

.logo svg {{
    width: 28px;
    height: 28px;
    fill: var(--nav-text);
}}

.logo h3 {{
    font-size: 1.25rem;
    font-weight: 700;
    letter-spacing: -0.5px;
}}

/* Desktop Links */
.nav-links {{
    display: flex;
    align-items: center;
    list-style: none;
    gap: 10px;
}}

.nav-links li a {{
    color: var(--nav-text);
    text-decoration: none;
    padding: 10px 15px;
    display: block;
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    transition: color 0.2s ease, background-color 0.2s ease;
    border-radius: 4px;
}}

.nav-links li a:hover:not(.nav-cta-button) {{
    color: var(--nav-accent);
    background-color: var(--hover-bg);
}}

/* CTA Button Specifics */
.nav-cta-button {{
    margin-left: 10px;
    border: 2px solid var(--nav-accent);
    border-radius: 50px;
    padding: 10px 24px !important;
}}

.nav-links li a.nav-cta-button:hover {{
    background-color: var(--nav-accent);
    color: var(--nav-bg);
}}

/* Hamburger Icon (Hidden on Desktop) */
.hamburger {{
    display: none;
    flex-direction: column;
    cursor: pointer;
    gap: 5px;
    padding: 5px;
}}

.hamburger .bar {{
    width: 26px;
    height: 3px;
    background-color: var(--nav-text);
    border-radius: 2px;
    transition: all 0.3s ease;
}}

/* Page Content Formatting */
.content {{
    padding: 60px 40px;
    max-width: 800px;
    margin: 0 auto;
}}

.content h1 {{
    color: var(--nav-text);
    font-size: 2.5rem;
    margin-bottom: 20px;
}}

.content p {{
    font-size: 1.1rem;
    line-height: 1.6;
}}

.dummy-scroll-space {{
    height: 150vh;
    background: linear-gradient(to bottom, transparent, var(--border-color));
    margin-top: 40px;
    border-radius: 8px;
}}

/* === Mobile Responsive Layout === */
@media (max-width: 768px) {{
    .navbar {{
        padding: 15px 20px;
    }}

    .hamburger {{
        display: flex;
    }}

    .nav-links {{
        display: none; /* Hidden by default */
        width: 100%;   /* Forces wrap to new line */
        flex-direction: column;
        margin-top: 15px;
        padding-top: 10px;
        border-top: 1px solid var(--border-color);
        gap: 0;
    }}

    .nav-links.active {{
        display: flex; /* Toggled by JS */
    }}

    .nav-links li {{
        width: 100%;
    }}

    .nav-links li a {{
        padding: 16px 0;
        text-align: center;
        border-radius: 0;
        border-bottom: 1px solid var(--border-color);
    }}

    .nav-links li:last-child a {{
        border-bottom: none;
    }}

    .nav-cta-button {{
        margin: 20px auto 10px auto;
        display: inline-block;
        width: max-content;
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text} - Responsive Navbar</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="device-container">
        
        <nav class="navbar">
            <div class="logo">
                <svg viewBox="0 0 24 24">
                    <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
                </svg>
                <h3>{title_text}</h3>
            </div>
            
            <div class="hamburger">
                <div class="bar"></div>
                <div class="bar"></div>
                <div class="bar"></div>
            </div>
            
            <ul class="nav-links">
                <li><a href="#home">Home</a></li>
                <li><a href="#about">About</a></li>
                <li><a href="#cases">Cases</a></li>
                <li><a href="#services">Services</a></li>
                <li><a class="nav-cta-button" href="#contact">Contact</a></li>
            </ul>
        </nav>

        <main class="content">
            <h1>Welcome to {title_text}</h1>
            <p>{body_text}</p>
            <div class="dummy-scroll-space"></div>
        </main>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Responsive Navbar Interaction
document.addEventListener('DOMContentLoaded', () => {{
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    // Toggle menu open/close on mobile
    hamburger.addEventListener('click', () => {{
        navLinks.classList.toggle('active');
        
        // Optional: Animate hamburger bars to 'X' (not required but good UX)
        // You would add CSS for .hamburger.active .bar to handle the transforms
    }});

    // Close menu when a link is clicked (good UX practice)
    const links = document.querySelectorAll('.nav-links li a');
    links.forEach(link => {{
        link.addEventListener('click', () => {{
            navLinks.classList.remove('active');
        }});
    }});
}});
"""

    # Write files
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
  - Using a native `<nav>` and `<ul>` semantic tags ensures screen readers identify this area as primary navigation. 
  - To make the hamburger icon fully accessible, `aria-expanded="false"` should technically be added to the `.hamburger` element and updated via JS, alongside an `aria-label="Toggle navigation"`. (The code focuses heavily on the visual reproduction to keep JS slim, but this is best practice).
  - High contrast colors are used, and focus states natively cascade into the hover rules.
* **Performance**: 
  - Extracted logic utilizes CSS class toggling (`.classList.toggle('active')`) instead of inline `style.display` modification. This prevents a common resizing bug where mobile styling lingers if the browser is resized back to desktop dimensions, eliminating the need for expensive window `resize` event listeners. 
  - `position: sticky` is GPU-accelerated and completely avoids the performance jank associated with JavaScript scroll-listener sticky headers.