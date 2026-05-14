# Persistent CSS Variable Theme Architecture (Dark/Light Mode)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Persistent CSS Variable Theme Architecture (Dark/Light Mode)

* **Core Visual Mechanism**: The defining mechanism of this pattern is the dynamic swapping of CSS Custom Properties (`--variables`) using a data-attribute toggle on the root HTML element, combined with JavaScript `localStorage`. Visually, this results in a seamless, animated transition across the entire user interface from a light aesthetic (light backgrounds, dark text, distinct shadows) to a dark aesthetic (dark backgrounds, light text, subdued/glow shadows), while preserving the user's preference across page reloads.
* **Why Use This Skill (Rationale)**: Implementing a dark mode is a fundamental modern web requirement. It drastically improves user experience by reducing eye strain in low-light environments, improving accessibility, and saving battery life on OLED screens. Architecturally, using CSS variables (rather than duplicating CSS classes or maintaining entirely separate stylesheets) is the most performant, maintainable, and scalable approach.
* **Overall Applicability**: Universal. This pattern is essential for SaaS dashboards, landing pages, blogs, portfolio websites, and web applications. Any site that users spend more than a few minutes reading or interacting with should implement this architecture.
* **Value Addition**: Transforms a static, one-dimensional webpage into a user-centric, adaptable interface. It demonstrates a high level of polish and consideration for the user's viewing environment.
* **Browser Compatibility**: Excellent. CSS Custom Properties (`var(--name)`) and `localStorage` are universally supported in all modern browsers (Chrome 49+, Firefox 31+, Safari 31+, Edge 15+).

*(Note: While the provided tutorial spends a significant amount of time manually swapping `<img>` `src` attributes via JavaScript to handle icon color changes, this extraction improves upon that pattern. The provided code utilizes inline SVGs and CSS variables for icons (`fill: var(--text-color)`), which is a much more robust, reusable, and less brittle industry best practice.)*

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **CSS Custom Properties**: The foundation is a `:root` pseudo-class containing baseline (light) colors, and a `[data-theme="dark"]` selector that redefines those exact same variables with dark equivalents.
  - **Color Logic**:
    - *Light Mode*: Background `#ffffff`, Surface `#f8f9fa`, Text `#1a1a2e`, Border `#e2e8f0`.
    - *Dark Mode*: Background `#0d111c`, Surface `#161b22`, Text `#f0f0f0`, Border `#30363d`.
  - **Typographic Hierarchy**: Relies on clean, modern sans-serif typography (`Inter` or system fonts) to ensure legibility in both high and low contrast states.
  - **CSS Transitions**: `transition: background-color 0.3s ease, color 0.3s ease;` applied to the `<body>` and surface elements ensures the switch isn't jarring.

* **Step B: Layout & Compositional Style**
  - The theme toggle is functionally independent of the layout, usually positioned in the top-right of a navigation bar.
  - The design utilizes "Surface" layers (cards, containers) that sit on top of the "Background" layer. In light mode, surfaces are often distinguished by subtle drop-shadows. In dark mode, shadows are typically removed or softened, and surfaces are distinguished by lighter background hex values compared to the deep background.

* **Step C: Interactive Behavior & Animations**
  - **Toggle Action**: A click event listener on a button triggers a JavaScript function.
  - **State Management**: JS checks the current theme, toggles it to the opposite state, applies the `data-theme` attribute to `document.documentElement` (the `<html>` tag), and crucially, writes this state to `localStorage`.
  - **Initialization (FOUC Prevention)**: To prevent a "Flash of Unstyled Content" (where the screen flashes white before turning dark), a synchronous script must run immediately in the `<head>` to check `localStorage` and apply the attribute before the `<body>` paints.
  - **Icon Animation**: The sun/moon icon typically features a subtle rotation or scale transform when clicked.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Global Theme Swapping | CSS Custom Properties (`:root` / `[data-theme]`) | Industry standard; allows changing the entire UI color palette by toggling a single DOM attribute. |
| User Persistence | JavaScript `localStorage` | Allows the browser to remember the user's choice indefinitely across tabs and sessions. |
| Smooth Transition | CSS `transition` on global elements | Provides a polished, native-feeling crossfade between light and dark palettes without JS animation libraries. |
| Icon Colors | Inline SVG + CSS `fill`/`stroke` | Vastly superior to the tutorial's method of swapping `.png` sources via JS; keeps icons crisp, perfectly color-matched to the theme, and reduces HTTP requests. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Frontend Developer",
    body_text: str = "Building responsive, accessible, and user-centric web applications with modern technologies.",
    color_scheme: str = "light",       # Default initial load state if no localStorage exists
    accent_color: str = "#3b82f6",     # Primary accent color (blue by default)
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Persistent CSS Variable Theme Architecture.
    Includes a realistic profile card layout to demonstrate the theme switching.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === CSS ===
    css = f"""/* Base & Theme Variables */
:root {{
    /* Light Mode Variables (Default) */
    --bg-color: #f8f9fa;
    --surface-color: #ffffff;
    --text-primary: #0f172a;
    --text-secondary: #64748b;
    --border-color: #e2e8f0;
    --accent-color: {accent_color};
    --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    --icon-hover-bg: #f1f5f9;
}}

/* Dark Mode Overrides */
[data-theme="dark"] {{
    --bg-color: #0f172a;
    --surface-color: #1e293b;
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --border-color: #334155;
    --shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5), 0 4px 6px -2px rgba(0, 0, 0, 0.3);
    --icon-hover-bg: #334155;
}}

/* Global Styles with Transitions */
*, *::before, *::after {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    /* Smooth transition for theme switching */
    transition: background-color 0.4s ease, color 0.4s ease;
}}

/* Navbar & Toggle Button */
.navbar {{
    position: absolute;
    top: 0;
    width: 100%;
    padding: 1.5rem 2rem;
    display: flex;
    justify-content: flex-end;
}}

.theme-toggle {{
    background: transparent;
    border: none;
    cursor: pointer;
    width: 44px;
    height: 44px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-primary);
    transition: background-color 0.2s ease, color 0.4s ease, transform 0.2s ease;
}}

.theme-toggle:hover {{
    background-color: var(--icon-hover-bg);
}}

.theme-toggle:active {{
    transform: scale(0.92);
}}

/* Icon swapping logic via CSS */
.theme-toggle .sun-icon {{ display: none; }}
.theme-toggle .moon-icon {{ display: block; }}

[data-theme="dark"] .theme-toggle .sun-icon {{ display: block; }}
[data-theme="dark"] .theme-toggle .moon-icon {{ display: none; }}

.theme-toggle svg {{
    width: 24px;
    height: 24px;
    fill: currentColor;
}}

/* Demo Profile Card */
.profile-card {{
    background-color: var(--surface-color);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 3rem 2rem;
    max-width: {width_px}px;
    width: 90%;
    text-align: center;
    box-shadow: var(--shadow);
    /* Surface transition */
    transition: background-color 0.4s ease, border-color 0.4s ease, box-shadow 0.4s ease;
}}

.avatar {{
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--accent-color), #8b5cf6);
    margin: 0 auto 1.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 3rem;
    font-weight: 700;
    box-shadow: 0 4px 14px rgba(59, 130, 246, 0.3);
}}

.title {{
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    letter-spacing: -0.025em;
}}

.subtitle {{
    font-size: 1.1rem;
    color: var(--accent-color);
    font-weight: 500;
    margin-bottom: 1.5rem;
}}

.description {{
    color: var(--text-secondary);
    line-height: 1.6;
    margin-bottom: 2rem;
    font-size: 1.05rem;
    transition: color 0.4s ease;
}}

.actions {{
    display: flex;
    gap: 1rem;
    justify-content: center;
}}

.btn {{
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    text-decoration: none;
    transition: all 0.2s ease;
    font-family: inherit;
}}

.btn-primary {{
    background-color: var(--accent-color);
    color: white;
    border: none;
}}

.btn-primary:hover {{
    filter: brightness(1.1);
    transform: translateY(-2px);
}}

.btn-outline {{
    background-color: transparent;
    color: var(--text-primary);
    border: 1px solid var(--border-color);
}}

.btn-outline:hover {{
    background-color: var(--icon-hover-bg);
}}
"""

    # === HTML ===
    # Note the inline script in <head> to prevent FOUC (Flash of Unstyled Content)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Theme Architecture Demo</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
    
    <!-- FOUC Prevention Script: Runs before CSS/DOM is fully parsed -->
    <script>
        (function() {{
            const savedTheme = localStorage.getItem('site-theme');
            // If saved theme exists, use it. Otherwise, fallback to OS preference, then default parameter.
            if (savedTheme) {{
                document.documentElement.setAttribute('data-theme', savedTheme);
            }} else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {{
                document.documentElement.setAttribute('data-theme', 'dark');
            }} else {{
                document.documentElement.setAttribute('data-theme', '{color_scheme}');
            }}
        }})();
    </script>
</head>
<body>
    <nav class="navbar">
        <button id="theme-toggle" class="theme-toggle" aria-label="Toggle dark mode">
            <!-- Moon Icon (shows in Light mode) -->
            <svg class="moon-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
            </svg>
            <!-- Sun Icon (shows in Dark mode) -->
            <svg class="sun-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="5"></circle>
                <line x1="12" y1="1" x2="12" y2="3"></line>
                <line x1="12" y1="21" x2="12" y2="23"></line>
                <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
                <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
                <line x1="1" y1="12" x2="3" y2="12"></line>
                <line x1="21" y1="12" x2="23" y2="12"></line>
                <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
                <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
            </svg>
        </button>
    </nav>

    <main class="profile-card">
        <div class="avatar">JD</div>
        <h1 class="title">John Doe</h1>
        <h2 class="subtitle">{title_text}</h2>
        <p class="description">{body_text}</p>
        
        <div class="actions">
            <button class="btn btn-primary">Download CV</button>
            <button class="btn btn-outline">Contact Info</button>
        </div>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Script for handling interactive behavior after DOM loads
document.addEventListener('DOMContentLoaded', () => {{
    const themeToggleBtn = document.getElementById('theme-toggle');
    const htmlElement = document.documentElement;

    themeToggleBtn.addEventListener('click', () => {{
        // Determine current theme
        const currentTheme = htmlElement.getAttribute('data-theme');
        
        // Toggle logic
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        // Apply new theme to DOM
        htmlElement.setAttribute('data-theme', newTheme);
        
        // Persist user preference to localStorage
        localStorage.setItem('site-theme', newTheme);
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

* **Accessibility (A11y)**:
  - **Aria-Label**: The theme toggle button contains an `aria-label="Toggle dark mode"` attribute because it only relies on visual SVGs. This ensures screen readers announce the button's purpose correctly.
  - **Color Contrast**: The defined dark and light mode variable palettes ensure high text-to-background contrast ratios (WCAG AA compliant).
  - **System Preferences**: The inline script includes a check for `window.matchMedia('(prefers-color-scheme: dark)')`. This ensures that if a user visits the site for the first time, it naturally respects their Operating System's dark/light mode settings before falling back to the parameter default.
* **Performance**:
  - **FOUC Prevention**: The most critical performance detail in dark mode implementation is preventing the Flash of Unstyled Content. The script placed synchronously in the `<head>` checks `localStorage` and applies the `data-theme` attribute *before* the browser renders the CSS Object Model (CSSOM). 
  - **CSS Transitions**: Applying transitions to `background-color` and `color` is highly performant. Using CSS variables dynamically repaints the affected layers efficiently without heavy JavaScript DOM manipulation overhead.
  - **SVG vs PNG**: By utilizing inline SVGs styled via `fill: currentColor;` and controlled by CSS `display: block/none`, we completely eliminate the need for extra HTTP image requests, which makes the implementation significantly faster and more resilient than swapping `.png` sources via JS.