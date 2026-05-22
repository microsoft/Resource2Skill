### 1. High-level Design Pattern Extraction

> **Skill Name**: Responsive Glassmorphism Navigation Bar

* **Core Visual Mechanism**: A modern, translucent navigation menu that utilizes `backdrop-filter: blur()` over a semi-transparent background to create a frosted-glass effect. On mobile devices, it functions as a fixed, slide-out drawer (sliding in from the right). On larger screens, it seamlessly transforms into a horizontal, inline navigation bar, integrating perfectly with the surrounding layout while maintaining its glass-like aesthetic.
* **Why Use This Skill (Rationale)**: This pattern solves the universal problem of mobile-to-desktop navigation scaling without relying on heavy JavaScript libraries. The "glassmorphism" aesthetic allows vibrant background imagery (like space themes, large hero images, or gradients) to bleed through the UI, establishing depth and visual hierarchy without completely obscuring the background context.
* **Overall Applicability**: Perfect for modern landing pages, portfolio sites, SaaS marketing sites, and high-fidelity promotional websites (especially those featuring full-screen photography, 3D elements, or rich background textures).
* **Value Addition**: Compared to a standard solid-color navbar, this technique makes the UI feel lightweight and premium. It relies purely on CSS for its fluid motion (`transform: translateX`) and visual rendering (`backdrop-filter`), ensuring high frame rates and a polished user experience.
* **Browser Compatibility**: `backdrop-filter` is broadly supported in modern browsers, but older versions of Safari may require the `-webkit-backdrop-filter` prefix. CSS Flexbox, CSS Custom Properties (variables), and `clamp()` are fully supported across all modern browsers.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Glass Effect**: Achieved using a highly transparent background color (e.g., `hsl(0 0% 100% / 0.05)`) combined with `backdrop-filter: blur(1rem)`.
  - **Typography**: Clean, uppercase sans-serif text with significant tracking (`letter-spacing`). The tutorial highlights the use of numbers (`00`, `01`) with bold weights (`700`) next to regular weight text to create structural rhythm.
  - **Accessibility Nodes**: Use of `.sr-only` (screen-reader only) classes to hide text visually but keep it available for assistive technologies (e.g., hiding the word "Menu" on the hamburger button, or hiding the decorative `00` numbers from screen readers using `aria-hidden="true"`).

* **Step B: Layout & Compositional Style**
  - **Mobile State**: Uses `position: fixed; inset: 0 0 0 30%;` to anchor the menu to the top, right, and bottom, covering the right 70% of the screen. Flexbox is set to `flex-direction: column` to stack the links.
  - **Desktop State**: A media query (`@media (min-width: 35em)`) switches the nav to a horizontal layout (`flex-direction: row`), resets the positioning, and turns off the hamburger toggle button.
  - **Dynamic Padding**: Uses `clamp()` (e.g., `padding-inline: clamp(3rem, 5vw, 10rem)`) to gracefully scale the horizontal padding of the navbar between tablet and desktop sizes without needing rigid breakpoints.

* **Step C: Interactive Behavior & Animations**
  - **Slide Animation**: The mobile menu hides off-screen using `transform: translateX(100%)`. When the toggle button is clicked, JS updates a data attribute (`data-visible="true"`), which triggers CSS to apply `transform: translateX(0%)`.
  - **Transition**: `transition: transform 350ms ease-out;` ensures the drawer slides in smoothly.
  - **JS Role**: JavaScript is kept to an absolute minimum. It solely listens for a click on the mobile toggle button, toggles the `data-visible` attribute on the `<nav>`, and updates the `aria-expanded` state on the button itself.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Frosted Glass Background** | CSS `backdrop-filter` | Provides native, real-time hardware-accelerated blurring of whatever is behind the element. |
| **Mobile Menu Slide** | CSS `transform: translateX` + `transition` | GPU-accelerated property; prevents layout thrashing (reflows) during animation. |
| **State Management** | Vanilla JS + Data Attributes | A lightweight click listener that toggles a `data-visible` attribute is much cleaner than toggling inline styles or massive class lists. |
| **Icons (Menu/Close)** | Inline SVG | Ensures the component is perfectly self-contained without relying on external image files as seen in the original tutorial. |
| **Dynamic Spacing** | CSS `clamp()` | Reduces the number of media queries needed by allowing padding to scale fluidly with viewport width. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "SPACE TOURISM",
    body_text: str = "Explore the universe with our new frosted-glass navigation bar.",
    color_scheme: str = "dark",
    accent_color: str = "#d0d6f9",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Glassmorphism Navbar.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Base theme configurations
    if color_scheme == "dark":
        text_col = "#ffffff"
        nav_bg = "rgba(255, 255, 255, 0.05)"
        page_bg = "radial-gradient(circle at bottom right, #0b0d17, #15192b, #05060b)"
    else:
        text_col = "#0b0d17"
        nav_bg = "rgba(0, 0, 0, 0.05)"
        page_bg = "radial-gradient(circle at bottom right, #ffffff, #d0d6f9, #f0f0f0)"

    css = f"""/* Responsive Glassmorphism Navigation */
:root {{
    --clr-text: {text_col};
    --clr-accent: {accent_color};
    --clr-nav-bg: {nav_bg};
    --nav-blur: 1.5rem;
    --transition-speed: 350ms;
}}

/* Resets */
*, *::before, *::after {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Inter', sans-serif;
    color: var(--clr-text);
    background: {page_bg};
    min-height: 100vh;
    overflow-x: hidden;
    line-height: 1.5;
}}

/* Decorative background elements to show off the glass blur */
body::before, body::after {{
    content: '';
    position: absolute;
    border-radius: 50%;
    z-index: -1;
}}
body::before {{
    width: 300px;
    height: 300px;
    background: linear-gradient(45deg, #ff00cc, #3333ff);
    top: 10%;
    left: 15%;
    filter: blur(80px);
    opacity: 0.5;
}}
body::after {{
    width: 400px;
    height: 400px;
    background: linear-gradient(45deg, #00ffff, #00ffcc);
    bottom: 20%;
    right: 5%;
    filter: blur(100px);
    opacity: 0.4;
}}

/* Utility Classes */
.flex {{ display: flex; gap: var(--gap, 1rem); }}
.sr-only {{
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}}

/* --- Header & Layout --- */
.primary-header {{
    justify-content: space-between;
    align-items: center;
    padding-top: 1.5rem;
    padding-left: clamp(1.5rem, 5vw, 3.5rem);
}}

.logo svg {{
    fill: var(--clr-text);
    width: 48px;
    height: 48px;
}}

/* --- Mobile Nav Toggle Button --- */
.mobile-nav-toggle {{
    display: none; /* Hidden on desktop */
    background: transparent;
    border: 0;
    cursor: pointer;
    position: absolute;
    z-index: 9999;
    right: 1.5rem;
    top: 2rem;
    width: 2rem;
    aspect-ratio: 1;
}}

.mobile-nav-toggle svg {{
    width: 100%;
    height: 100%;
    fill: var(--clr-text);
    transition: opacity 250ms ease-in-out;
}}

/* Toggle SVG visibility based on aria-expanded */
.mobile-nav-toggle .icon-close {{ display: none; }}
.mobile-nav-toggle[aria-expanded="true"] .icon-hamburger {{ display: none; }}
.mobile-nav-toggle[aria-expanded="true"] .icon-close {{ display: block; }}


/* --- Primary Navigation --- */
.primary-navigation {{
    list-style: none;
    margin: 0;
    background: var(--clr-nav-bg);
    backdrop-filter: blur(var(--nav-blur));
    -webkit-backdrop-filter: blur(var(--nav-blur));
}}

.primary-navigation a {{
    text-decoration: none;
    color: var(--clr-text);
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 0.9rem;
    font-weight: 400;
    display: block;
    padding: 0.5rem 0;
    border-bottom: 2px solid transparent;
    transition: border-color 0.2s ease;
}}

.primary-navigation a:hover,
.primary-navigation a:focus {{
    border-bottom-color: var(--clr-accent);
}}

.primary-navigation span[aria-hidden="true"] {{
    font-weight: 700;
    margin-right: 0.5em;
}}

/* --- Mobile Styles --- */
@media (max-width: 35em) {{
    .primary-navigation {{
        --gap: 2rem;
        position: fixed;
        inset: 0 0 0 30%; /* Top, Right, Bottom, Left. Covers right 70% */
        flex-direction: column;
        padding: min(30vh, 10rem) 2rem;
        z-index: 1000;
        
        /* Animation setup */
        transform: translateX(100%);
        transition: transform var(--transition-speed) ease-out;
    }}
    
    /* Open State */
    .primary-navigation[data-visible="true"] {{
        transform: translateX(0%);
    }}

    .mobile-nav-toggle {{
        display: block;
    }}
}}

/* --- Desktop/Tablet Styles --- */
@media (min-width: 35em) {{
    .primary-navigation {{
        --gap: clamp(1.5rem, 5vw, 3rem);
        padding-block: 2rem;
        padding-inline: clamp(3rem, 7vw, 10rem);
    }}
    
    /* Hide the numbers on medium screens for space, show on large */
    @media (min-width: 35em) and (max-width: 55em) {{
        .primary-navigation span[aria-hidden="true"] {{
            display: none;
        }}
    }}
}}

/* Demo Content Page Styles */
main {{
    padding: 4rem clamp(1.5rem, 5vw, 3.5rem);
    max-width: 800px;
}}
h1 {{
    font-size: clamp(2.5rem, 8vw, 5rem);
    text-transform: uppercase;
    letter-spacing: 4px;
    margin-bottom: 1rem;
}}
p {{
    font-size: 1.1rem;
    color: var(--clr-accent);
    max-width: 60ch;
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <header class="primary-header flex">
        <div class="logo">
            <!-- Simulated Logo SVG -->
            <svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
                <circle cx="24" cy="24" r="24" fill="currentColor"/>
                <path d="M24 0c0 13.255-10.745 24-24 24 13.255 0 24 10.745 24 24 0-13.255 10.745-24 24-24-13.255 0-24-10.745-24-24z" fill="var(--clr-accent)"/>
            </svg>
        </div>

        <button class="mobile-nav-toggle" aria-controls="primary-navigation" aria-expanded="false">
            <span class="sr-only">Menu</span>
            <!-- Hamburger Icon -->
            <svg class="icon-hamburger" viewBox="0 0 24 21" xmlns="http://www.w3.org/2000/svg">
                <g fill="currentColor" fill-rule="evenodd">
                    <path d="M0 0h24v3H0zM0 9h24v3H0zM0 18h24v3H0z"/>
                </g>
            </svg>
            <!-- Close (X) Icon -->
            <svg class="icon-close" viewBox="0 0 20 21" xmlns="http://www.w3.org/2000/svg">
                <g fill="currentColor" fill-rule="evenodd">
                    <path d="M2.575.954l16.97 16.97-2.12 2.122L.455 3.076z"/>
                    <path d="M.454 17.925L17.424.955l2.122 2.12-16.97 16.97z"/>
                </g>
            </svg>
        </button>

        <nav>
            <ul id="primary-navigation" class="primary-navigation flex" data-visible="false">
                <li>
                    <a href="#"><span aria-hidden="true">00</span>Home</a>
                </li>
                <li>
                    <a href="#"><span aria-hidden="true">01</span>Destination</a>
                </li>
                <li>
                    <a href="#"><span aria-hidden="true">02</span>Crew</a>
                </li>
                <li>
                    <a href="#"><span aria-hidden="true">03</span>Technology</a>
                </li>
            </ul>
        </nav>
    </header>

    <main>
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Responsive Navbar Interaction Logic
document.addEventListener('DOMContentLoaded', () => {{
    const nav = document.querySelector('.primary-navigation');
    const navToggle = document.querySelector('.mobile-nav-toggle');

    if (!nav || !navToggle) return;

    navToggle.addEventListener('click', () => {{
        // Read current state
        const visibility = nav.getAttribute('data-visible');
        
        // Toggle logic
        if (visibility === "false") {{
            nav.setAttribute('data-visible', "true");
            navToggle.setAttribute('aria-expanded', "true");
        }} else {{
            nav.setAttribute('data-visible', "false");
            navToggle.setAttribute('aria-expanded', "false");
        }}
    }});
}});
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

* **Accessibility (a11y)**:
  * **`aria-expanded`**: Vital for screen readers. It tells the user whether the menu connected to the button is currently open or closed. The JavaScript dynamically toggles this state.
  * **`aria-controls`**: Connects the toggle button to the `<ul id="primary-navigation">`. This programmatic link informs assistive technologies what element the button dictates.
  * **`.sr-only`**: Used on the button text. Buttons containing only icons fail accessibility checks; the hidden text provides context to screen readers without breaking the visual design.
  * **`aria-hidden="true"`**: Applied to the decorative numbers (`00`, `01`). This stops screen readers from confusingly reading out "Zero Zero Home, Zero One Destination."
* **Performance**:
  * The sliding drawer animation targets the `transform: translateX` property. Transforming elements does not trigger DOM layout reflows or repaints, meaning the animation is handled by the GPU, ensuring a silky smooth 60fps experience even on lower-end mobile devices.
  * `backdrop-filter: blur()` can be computationally expensive on very old devices or extremely large surface areas. By confining it solely to the `<ul class="primary-navigation">`, performance impact is heavily mitigated compared to blurring entire page wrappers. Additionally, the fallback `-webkit-` prefix guarantees it functions gracefully on iOS devices.