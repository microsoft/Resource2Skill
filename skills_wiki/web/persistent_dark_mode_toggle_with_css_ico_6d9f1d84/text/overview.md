# Persistent Dark Mode Toggle with CSS Icon Swapping

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Persistent Dark Mode Toggle with CSS Icon Swapping

* **Core Visual Mechanism**: A floating circular action button (FAB) that toggles a website's overall color palette between light and dark themes. The visual signature is the seamless transition of background/text colors combined with an immediate, JS-free swapping of the button's SVG icon (moon to sun) using CSS pseudo-class overriding. 
* **Why Use This Skill (Rationale)**: Allowing users to choose their preferred color scheme significantly improves accessibility and reduces eye strain in low-light environments. Persisting this choice via `localStorage` ensures a seamless, frustration-free experience across browser sessions.
* **Overall Applicability**: Universal. This pattern is fundamental for modern web applications, SaaS dashboards, blogs, portfolios, and content-heavy sites. 
* **Value Addition**: Transforms a static webpage into a responsive, user-aware interface. The CSS-only icon swap technique keeps the JavaScript payload extremely lightweight by avoiding expensive DOM node creation/destruction.
* **Browser Compatibility**: Excellent. Relies on standard CSS custom properties (variables), Flexbox, and `localStorage`, which are supported by all modern browsers (Chrome, Firefox, Safari, Edge).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**: Utilizes CSS Custom Properties (`:root`) to define a baseline color palette (e.g., `--base-color`, `--text-color`, `--accent-color`). A secondary `.darkmode` class redefines these exact variable names with inverse values. 
  - **Icons**: Inline SVG paths for a Moon (Dark Mode) and Sun (Light Mode).
  - **CSS Drivers**: 
    - `background-color` and `color` bound to variables.
    - `fill` attribute on SVGs bound to variables to match the text/accent color.

* **Step B: Layout & Compositional Style**
  - **Button Layout**: The toggle button is styled as a 50x50px perfect circle (`border-radius: 50%`) and uses `display: flex`, `justify-content: center`, `align-items: center` to perfectly center the active SVG icon.
  - **Positioning**: Uses `position: fixed` with `top: 20px` and `right: 20px` to keep the control persistently accessible regardless of scroll depth.
  - **Icon Stacking Trick**: Both SVGs are placed inside the button. The CSS dictates that the second icon (Sun) is hidden by default.

* **Step C: Interactive Behavior & Animations**
  - **CSS Icon Swap**: 
    - Light mode: `#theme-switch svg:last-child { display: none; }` (Hides Sun).
    - Dark mode: `.darkmode #theme-switch svg:first-child { display: none; }` (Hides Moon) and `.darkmode #theme-switch svg:last-child { display: block; }` (Shows Sun).
  - **JavaScript Logic**: 
    - On load: Checks `localStorage.getItem('darkmode')`. If it equals `"active"`, the `.darkmode` class is applied to `document.body`.
    - On click: Re-checks the state. If not active, it calls `enableDarkmode()` (adds class, sets `localStorage` to `"active"`). If active, calls `disableDarkmode()` (removes class, sets `localStorage` to `null`).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Theme variable switching** | CSS Variables + Cascade | `.darkmode` class trivially overwrites `:root` variables without touching individual elements. |
| **Icon swapping** | CSS `:first-child` / `:last-child` | Swaps visibility natively without requiring JavaScript to manipulate DOM nodes. |
| **State persistence** | JS `localStorage` | Browser's native key-value store, perfect for persisting lightweight user preferences across sessions. |
| **Smooth transition** | CSS `transition` | Added a smooth `0.3s ease` transition to `body` background and color for a more premium feel. |

> **Feasibility Assessment**: 100%. The provided code perfectly replicates the visual toggle, the CSS-based icon swapping mechanism, and the JS localStorage persistence demonstrated in the tutorial.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Some random website",
    body_text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quidem, beatae voluptates iure iste eveniet, molestias rerum dicta accusantium dolore libero laboriosam aspernatur!",
    color_scheme: str = "light",       # "dark" or "light" - dictates fallback if no localStorage is set
    accent_color: str = "#0071ff",     # CSS hex color for accent/buttons
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Persistent Dark Mode Toggle effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Note: color_scheme parameter dictates the *initial default* if local storage is empty.
    # The actual implementation relies entirely on CSS variables.
    default_state = "active" if color_scheme == "dark" else "null"

    # === CSS ===
    css = f"""/* Persistent Dark Mode Toggle */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

/* Light Mode Variables (Default) */
:root {{
    --base-color: #ffffff;
    --base-variant: #e8e9ed;
    --text-color: #111528;
    --secondary-text: #232738;
    --primary-color: #3a435d;
    --accent-color: {accent_color};
    --button-text: #ffffff;
}}

/* Dark Mode Variables (Applied via class) */
.darkmode {{
    --base-color: #070b1d;
    --base-variant: #101425;
    --text-color: #ffffff;
    --secondary-text: #a4a5b8;
    --primary-color: #e8e9ed;
    --accent-color: {accent_color};
    --button-text: #ffffff;
}}

body {{
    font-family: 'Poppins', -apple-system, sans-serif;
    background-color: var(--base-color);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    /* Added transition for a premium smooth color swap */
    transition: background-color 0.3s ease, color 0.3s ease;
}}

.container {{
    width: 100%;
    max-width: {width_px}px;
    padding: 40px;
}}

header {{
    margin-bottom: 30px;
}}

h1 {{
    font-size: 2.5rem;
    margin-bottom: 15px;
}}

p {{
    font-size: 1.1rem;
    line-height: 1.6;
    color: var(--secondary-text);
    margin-bottom: 30px;
    max-width: 600px;
}}

.cta-button {{
    background-color: var(--accent-color);
    color: var(--button-text);
    border: none;
    padding: 12px 24px;
    font-size: 1rem;
    font-weight: 600;
    border-radius: 6px;
    cursor: pointer;
    transition: opacity 0.2s;
}}

.cta-button:hover {{
    opacity: 0.9;
}}

/* === Theme Switch Button Styles === */
#theme-switch {{
    height: 50px;
    width: 50px;
    padding: 0;
    border-radius: 50%;
    background-color: var(--base-variant);
    border: none;
    display: flex;
    justify-content: center;
    align-items: center;
    position: fixed;
    top: 20px;
    right: 20px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}}

#theme-switch svg {{
    fill: var(--primary-color);
    transition: fill 0.3s ease;
}}

/* Icon Swapping Logic */
/* 1. Light Mode (Default): Hide the second child (Sun) */
#theme-switch svg:last-child {{
    display: none;
}}

/* 2. Dark Mode: Hide the first child (Moon), Show the second child (Sun) */
.darkmode #theme-switch svg:first-child {{
    display: none;
}}

.darkmode #theme-switch svg:last-child {{
    display: block;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dark Mode Toggle</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <!-- Floating Theme Switch -->
    <button id="theme-switch" aria-label="Toggle Dark Mode">
        <!-- Moon Icon (First Child) -->
        <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px">
            <path d="M0 0h24v24H0z" fill="none"/>
            <path d="M12 3c-4.97 0-9 4.03-9 9s4.03 9 9 9 9-4.03 9-9c0-.46-.04-.92-.1-1.36-.98 1.37-2.58 2.26-4.38 2.26-2.98 0-5.4-2.42-5.4-5.4 0-1.81.89-3.42 2.26-4.38C12.92 3.04 12.46 3 12 3zm0 16c-3.86 0-7-3.14-7-7s3.14-7 7-7c.19 0 .38.01.57.04-1.56 1.34-2.57 3.33-2.57 5.56 0 3.86 3.14 7 7 7 2.23 0 4.22-1.01 5.56-2.57-.42.23-.9.37-1.4.45-.63.1-1.28.12-1.92.05-3.03-.31-5.5-2.61-5.96-5.61-.25-1.63.1-3.21.94-4.52C16.89 5.86 18.66 4.67 20.73 4.1 19.34 3.42 17.75 3 16 3c-4.97 0-9 4.03-9 9s4.03 9 9 9c1.75 0 3.34-.42 4.73-1.1-.57-2.07-1.76-3.84-3.33-5.23C15.21 17.65 13.62 18.66 12 19z" fill="currentColor"/>
            <path d="M12 21c4.97 0 9-4.03 9-9 0-.46-.04-.92-.1-1.36-.98 1.37-2.58 2.26-4.38 2.26-2.98 0-5.4-2.42-5.4-5.4 0-1.81.89-3.42 2.26-4.38.19.03.38.04.57.04 3.86 0 7 3.14 7 7s-3.14 7-7 7-7-3.14-7-7 3.14-7 7-7z" opacity=".3"/>
        </svg>
        <!-- Sun Icon (Last Child) -->
        <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px">
            <path d="M0 0h24v24H0z" fill="none"/>
            <path d="M6.76 4.84l-1.8-1.79-1.41 1.41 1.79 1.79 1.42-1.41zM4 10.5H1v2h3v-2zm9-9.95h-2V3.5h2V.55zm7.45 3.91l-1.41-1.41-1.79 1.79 1.41 1.41 1.79-1.79zm-3.21 13.7l1.79 1.8 1.41-1.41-1.8-1.79-1.4 1.4zM20 10.5v2h3v-2h-3zm-8-5c-3.31 0-6 2.69-6 6s2.69 6 6 6 6-2.69 6-6-2.69-6-6-6zm-1 16.95h2V19.5h-2v2.95zm-7.45-3.91l1.41 1.41 1.79-1.8-1.41-1.41-1.79 1.8z"/>
        </svg>
    </button>

    <div class="container">
        <header>
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <button class="cta-button">GO PREMIUM</button>
        </header>
    </div>

    <script>
        // Provide the injected configuration
        const CONFIG_DEFAULT_STATE = "{default_state}";
    </script>
    <script src="script.js" defer></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Dark Mode Logic with LocalStorage persistence

document.addEventListener('DOMContentLoaded', () => {{
    // 1. Get current theme from local storage
    let darkmode = localStorage.getItem('darkmode');
    const themeSwitch = document.getElementById('theme-switch');

    // 2. Define enablement/disablement functions
    const enableDarkmode = () => {{
        document.body.classList.add('darkmode');
        localStorage.setItem('darkmode', 'active');
    }};

    const disableDarkmode = () => {{
        document.body.classList.remove('darkmode');
        localStorage.setItem('darkmode', 'null');
    }};

    // 3. Fallback logic: If local storage is entirely empty, use the python parameter default
    if (darkmode === null) {{
        darkmode = CONFIG_DEFAULT_STATE; 
    }}

    // 4. Initial load check
    if (darkmode === 'active') {{
        enableDarkmode();
    }}

    // 5. Button click listener
    themeSwitch.addEventListener('click', () => {{
        // Re-evaluate the local storage state inside the listener
        darkmode = localStorage.getItem('darkmode');

        if (darkmode !== 'active') {{
            enableDarkmode();
        }} else {{
            disableDarkmode();
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

### 4. Accessibility & Performance Notes

* **Accessibility**:
  - The toggle button includes an `aria-label="Toggle Dark Mode"` to ensure screen readers can identify the un-labeled icon button.
  - Using high-contrast color shifts (`#070b1d` background vs `#ffffff` text) ensures WCAG AA compliance.
  - Relying on SVG icon swaps visually communicates state immediately, bypassing reliance purely on color.
* **Performance**:
  - **No DOM Thrashing**: The technique of keeping both SVGs in the DOM and toggling them via CSS (`display: none` vs `display: block`) avoids the performance penalty of using JS to destroy and recreate DOM nodes or rewrite SVG attributes.
  - The JS script is loaded with `defer` to prevent render-blocking the HTML parser.
  - `transition` properties are limited to colors and opacities which are relatively cheap to compute compared to layout-altering CSS.