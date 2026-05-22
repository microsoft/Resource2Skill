# Responsive Snap-Scroll Component Architecture

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Responsive Snap-Scroll Component Architecture

* **Core Visual Mechanism**: A full-container, immersive scrolling experience driven by CSS `scroll-snap-type`. Content is organized into bite-sized, screen-filling segments. The layout relies heavily on fluid typography (`clamp()`) and auto-wrapping flexbox grids (`flex: 1`, `min-width`) to completely eliminate the need for traditional `@media` query breakpoints. A centralized CSS variable system powers dynamic theming (e.g., a dark mode toggle).
* **Why Use This Skill (Rationale)**: Snap scrolling creates a highly controlled, presentation-like narrative flow, forcing the user's attention onto one distinct message or set of features at a time. The combination of fluid text and flexible cards ensures this high-control layout doesn't break on unpredictable screen sizes. CSS variables enable instant, performant theme switching without JavaScript style recalculations.
* **Overall Applicability**: Ideal for SaaS landing pages, interactive product showcases, tiered pricing sections, and high-impact portfolio pieces where controlling the user's reading pace is beneficial.
* **Browser Compatibility**: Fully supported in modern browsers (Edge 79+, Firefox 68+, Chrome 69+, Safari 13+). Uses standard CSS Grid/Flexbox, `clamp()`, and CSS Custom Properties.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**: Driven entirely by a `:root` variable dictionary based on `[data-theme]`.
    - Light: Background `#ffffff`, Surface `#f3f4f6`, Text `#111827`, Accent `user-defined`.
    - Dark: Background `#0f172a`, Surface `#1e293b`, Text `#f8fafc`, Accent `user-defined`.
  - **Typography**: Uses 'Inter' sans-serif. Sizes are governed by `clamp()` to interpolate smoothly between minimum and maximum bounds based on viewport width (e.g., `clamp(2.5rem, 5vw, 4.5rem)`).
  - **Icons**: Inline SVG paths colored via `fill: var(--text)` and transitioned to `var(--accent)` on hover, demonstrating interactive vector styling.

* **Step B: Layout & Compositional Style**
  - **Scroll Container**: `overflow-y: scroll`, `scroll-snap-type: y mandatory`, hiding the default scrollbar for a cleaner presentation aesthetic.
  - **Section Sizing**: Each child section is strictly `height: 100%` and `width: 100%` of the container, with `scroll-snap-align: start`.
  - **Flexible Grid**: The pricing cards use `display: flex; flex-wrap: wrap; gap: 30px`. Crucially, children use `flex: 1; min-width: 280px`. This algorithm forces cards into equal columns, automatically dropping to new rows if the container width falls below the minimum viable width for the cards, avoiding hard-coded breakpoints.

* **Step C: Interactive Behavior & Animations**
  - **Theme Toggle**: A fixed position button modifies a `data-theme` attribute on the root element. CSS variables cascade instantly, altering the entire component's color palette.
  - **Hover Micro-interactions**: Buttons and cards utilize `transform: scale(1.03) translateY(-5px)` coupled with `box-shadow` elevation, providing tactile feedback using GPU-accelerated CSS properties (`transition: transform 0.3s ease`).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Scroll Experience** | Pure CSS `scroll-snap` | Native API, hardware-accelerated, zero JavaScript jank or complex intersection observers required. |
| **Responsive Grid** | Flexbox Auto-wrap | `flex: 1` + `min-width` handles infinite container sizes gracefully without rigid `@media` queries. |
| **Fluid Text** | CSS `clamp()` | Replaces the video's older `max()` technique with modern, bounded fluid typography scaling. |
| **Theme Switching** | CSS Variables + JS toggle | Most performant way to globally update colors; JS only toggles a single HTML attribute. |
| **Interactive Icons** | Inline SVG | Allows direct CSS inheritance (`fill: var(--color)`) without external HTTP requests. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Build Better Websites.",
    body_text: str = "Focus on design first. Use flexible systems, dynamic typography, and scalable architectures to create stunning, profitable web experiences without writing complex code.",
    color_scheme: str = "dark",
    accent_color: str = "#f66e3d",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Snap-Scroll Landing Page architecture.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === CSS ===
    css = f"""/* Responsive Snap-Scroll Component Architecture */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

/* Theme Variable Dictionary */
:root[data-theme="light"] {{
    --bg: #ffffff;
    --text: #111827;
    --surface: #f3f4f6;
    --shadow: rgba(0, 0, 0, 0.08);
    --border: #e5e7eb;
}}

:root[data-theme="dark"] {{
    --bg: #0f172a;
    --text: #f8fafc;
    --surface: #1e293b;
    --shadow: rgba(0, 0, 0, 0.4);
    --border: #334155;
}}

:root {{
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #000; /* Outer page backdrop */
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden; /* Prevents outer window scrolling */
}}

/* Main Component Wrapper */
.app-wrapper {{
    position: relative;
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    border-radius: 16px;
    overflow: hidden;
    background: var(--bg);
    color: var(--text);
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    transition: background 0.3s ease, color 0.3s ease;
}}

/* The Snap Scroll Container */
.snap-container {{
    width: 100%;
    height: 100%;
    overflow-y: scroll;
    scroll-snap-type: y mandatory;
    scroll-behavior: smooth;
    /* Hide scrollbar for immersive presentation */
    scrollbar-width: none; 
}}
.snap-container::-webkit-scrollbar {{
    display: none;
}}

/* Individual Sections */
.snap-section {{
    height: 100%;
    width: 100%;
    scroll-snap-align: start;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 5%;
    position: relative;
}}

/* Fluid Typography */
.hero-title {{
    font-size: clamp(2.5rem, 6vw, 5rem);
    line-height: 1.1;
    font-weight: 800;
    letter-spacing: -0.02em;
    text-align: center;
    margin-bottom: 1.5rem;
}}
.hero-body {{
    font-size: clamp(1rem, 2vw, 1.25rem);
    line-height: 1.6;
    text-align: center;
    max-width: 600px;
    opacity: 0.8;
    margin-bottom: 2.5rem;
}}
.section-title {{
    font-size: clamp(2rem, 4vw, 3rem);
    font-weight: 700;
    margin-bottom: 3rem;
    text-align: center;
}}

/* Buttons */
.btn {{
    background: var(--accent);
    color: #fff;
    border: none;
    padding: 1rem 2rem;
    font-size: 1.125rem;
    font-weight: 600;
    border-radius: 8px;
    cursor: pointer;
    transition: transform 0.2s ease, filter 0.2s ease;
    text-decoration: none;
}}
.btn:hover {{
    transform: scale(1.05);
    filter: brightness(1.1);
}}

/* Flexible Auto-wrapping Cards */
.cards-container {{
    display: flex;
    gap: 30px;
    flex-wrap: wrap;
    width: 100%;
    max-width: 1100px;
}}
.card {{
    flex: 1;
    min-width: 280px; /* Forces wrap if container is too narrow */
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 40px 30px;
    box-shadow: 0 10px 30px var(--shadow);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}}
.card:hover {{
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 20px 40px var(--shadow);
}}
.card-highlight {{
    border: 2px solid var(--accent);
    position: relative;
}}
.card-highlight::before {{
    content: "Most Popular";
    position: absolute;
    top: -14px;
    left: 50%;
    transform: translateX(-50%);
    background: var(--accent);
    color: #fff;
    padding: 4px 16px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 0.5px;
}}
.card h3 {{
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
}}
.card .price {{
    font-size: 2.5rem;
    font-weight: 800;
    color: var(--accent);
    margin-bottom: 1.5rem;
}}
.card .price span {{
    font-size: 1rem;
    color: var(--text);
    opacity: 0.6;
    font-weight: 500;
}}
.card ul {{
    list-style: none;
}}
.card li {{
    padding: 12px 0;
    border-top: 1px solid var(--border);
    font-size: 0.95rem;
    opacity: 0.9;
}}

/* Interactive SVG Row */
.icon-row {{
    display: flex;
    gap: 30px;
    margin-top: 2rem;
}}
.social-icon {{
    width: 36px;
    height: 36px;
    fill: var(--text);
    transition: fill 0.3s ease, transform 0.3s ease;
    cursor: pointer;
}}
.social-icon:hover {{
    fill: var(--accent);
    transform: scale(1.2) translateY(-4px);
}}

/* Theme Toggle Button */
.theme-btn {{
    position: absolute;
    top: 24px;
    right: 24px;
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: var(--surface);
    border: 1px solid var(--border);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 100;
    box-shadow: 0 4px 10px var(--shadow);
    transition: transform 0.2s ease, background 0.3s ease;
}}
.theme-btn:hover {{
    transform: scale(1.1) rotate(15deg);
}}
.theme-btn svg {{
    width: 20px;
    height: 20px;
    fill: var(--text);
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en" data-theme="{color_scheme}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Responsive Snap-Scroll Component</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <div class="app-wrapper">
        <!-- Floating Theme Toggle -->
        <button id="theme-toggle" class="theme-btn" aria-label="Toggle Theme">
            <svg viewBox="0 0 24 24"><path d="M12 3a9 9 0 1 0 9 9c0-.46-.04-.92-.1-1.36a5.389 5.389 0 0 1-4.4 2.26 5.403 5.403 0 0 1-3.14-9.8c-.44-.06-.9-.1-1.36-.1z"/></svg>
        </button>

        <div class="snap-container">
            
            <!-- Hero Section -->
            <section class="snap-section">
                <h1 class="hero-title">{title_text}</h1>
                <p class="hero-body">{body_text}</p>
                <a href="#pricing" class="btn">View Plans & Pricing</a>
            </section>

            <!-- Pricing / Cards Section -->
            <section id="pricing" class="snap-section">
                <h2 class="section-title">Flexible Plans</h2>
                <div class="cards-container">
                    <div class="card">
                        <h3>Basic</h3>
                        <p class="price">$7<span>/month</span></p>
                        <ul>
                            <li>Browse Destinations</li>
                            <li>Plan Trips</li>
                            <li>Basic Support</li>
                        </ul>
                    </div>
                    <div class="card card-highlight">
                        <h3>Standard</h3>
                        <p class="price">$12<span>/month</span></p>
                        <ul>
                            <li>Everything in Basic</li>
                            <li>Join Communities</li>
                            <li>Host Events</li>
                            <li>Priority Support</li>
                        </ul>
                    </div>
                    <div class="card">
                        <h3>Premium</h3>
                        <p class="price">$19<span>/month</span></p>
                        <ul>
                            <li>Everything in Standard</li>
                            <li>Receive Discounts</li>
                            <li>Direct Hotel Contacts</li>
                            <li>24/7 Dedicated Support</li>
                        </ul>
                    </div>
                </div>
            </section>

            <!-- Social/Footer Section -->
            <section class="snap-section">
                <h2 class="section-title">Connect With Us</h2>
                <p class="hero-body">Join our community across multiple platforms and stay updated.</p>
                
                <div class="icon-row">
                    <!-- Twitter / X -->
                    <svg viewBox="0 0 24 24" class="social-icon"><path d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z"/></svg>
                    <!-- GitHub -->
                    <svg viewBox="0 0 24 24" class="social-icon"><path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg>
                    <!-- LinkedIn -->
                    <svg viewBox="0 0 24 24" class="social-icon"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
                </div>
            </section>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Snap-Scroll & Theming Behavior
document.addEventListener('DOMContentLoaded', () => {{
    const themeToggleBtn = document.getElementById('theme-toggle');
    const htmlElement = document.documentElement;

    // Toggle CSS Variables dynamically by switching data attribute
    themeToggleBtn.addEventListener('click', () => {{
        const currentTheme = htmlElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        htmlElement.setAttribute('data-theme', newTheme);
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