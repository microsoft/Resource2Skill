# Themeable Portfolio Hero with Morphing Blob

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Themeable Portfolio Hero with Morphing Blob

* **Core Visual Mechanism**: This pattern relies on **CSS Custom Properties (variables)** attached to the `:root` and `body.dark-theme` selectors to manage global color states (backgrounds, text, borders). Visually, it features a stark, high-contrast layout paired with an organic, **keyframe-animated CSS blob** (`border-radius` manipulation) that serves as a dynamic backdrop for a featured image.
* **Why Use This Skill (Rationale)**: Implementing a dark/light mode toggle respects user system preferences and reduces eye strain, which is a hallmark of modern, considerate web design. The animated organic blob adds a layer of subtle, modern motion that breaks the rigidity of standard grid layouts, making the hero section feel alive and creative.
* **Overall Applicability**: Ideal for personal developer portfolios, creative agency landing pages, freelance resumes, or any site where a strong personal brand statement needs to be balanced with interactive polish.
* **Browser Compatibility**: Excellent. CSS variables, Flexbox, and `border-radius` animations are fully supported in all modern browsers (Edge, Chrome, Safari, Firefox).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**:
    - Light Theme (Default): Background `#ffffff`, Text `#1b1b1b`.
    - Dark Theme: Background `#1b1b1b`, Text `#ffffff`.
    - Accent Color: A vibrant, energetic hue (e.g., `#ff6401` orange) applied consistently to the logo mark, specific heading words, hover states, and the background blob.
  - **Typography**: Uses `Poppins` (Google Fonts) for a geometric, friendly, and highly legible sans-serif look. The main headline is heavily weighted (800) and uppercase (60px) to establish immediate hierarchy.
  - **Iconography**: FontAwesome icons are used for both social links and the theme toggle, ensuring scalable vector rendering.

* **Step B: Layout & Compositional Style**
  - **Layout System**: The entire container and navbar use **CSS Flexbox**. The hero section is split 50/50, with `flex: 1` assigned to both the text content (left) and image content (right).
  - **Alignment & Whitespace**: Vertical centering is achieved via `align-items: center` on the hero flex container. Generous padding prevents the content from hitting the browser edges.
  - **Z-index Layering**: The image section uses absolute positioning for the organic blob (`z-index: 1`) to place it strictly behind the relative-positioned featured image (`z-index: 2`).

* **Step C: Interactive Behavior & Animations**
  - **Theme Toggle**: JavaScript listens for clicks on the header button, toggling a `.dark-theme` class on the `<body>` tag. CSS variables automatically recalculate, and the `background-color` and `color` properties undergo a smooth `0.5s ease` transition.
  - **Blob Animation**: A pure CSS `@keyframes` animation continually shifts the multi-value `border-radius` of the accent background element over an 8-second cycle (`alternate`), creating a breathing, liquid effect.
  - **Hover States**: Links and social icons change to the accent color on hover. The "Download Resume" button inverts its colors, filling with the accent color and turning text white.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Theme Toggling** | CSS Custom Properties + JS | CSS variables allow instant global color updates simply by toggling a single class on the `<body>` tag via JavaScript. |
| **Organic Background Shape** | CSS `border-radius` Animation | Using an 8-value border-radius animated via `@keyframes` creates fluid, blob-like shapes without needing complex SVG morphing or external image assets. |
| **Icons** | FontAwesome CDN | Provides a reliable, standardized set of vector icons for social media and the sun/moon toggle without cluttering the project with raw SVGs. |
| **Layout** | CSS Flexbox | Flexbox perfectly handles the horizontal distribution of the navbar and the 50/50 split of the hero content, easily wrapping to a column layout on mobile. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "I'M A <span class=\"accent\">PROGRAMMER</span>",
    body_text: str = "I'm a Self Taught Developer, Frontend Web Developer, and UI/UX enthusiast. Providing quality, interactive web experiences.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#ff6401",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Themeable Portfolio Hero visual effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Determine initial theme classes based on requested color_scheme
    body_class = "dark-theme" if color_scheme == "dark" else ""
    icon_class = "fa-sun" if color_scheme == "dark" else "fa-moon"

    # === CSS ===
    css = f"""/* Themeable Portfolio Hero Component */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
    
    /* Default Light Theme Variables */
    --bg: #ffffff;
    --text: #1b1b1b;
}}

/* Dark Theme Overrides */
body.dark-theme {{
    --bg: #1b1b1b;
    --text: #ffffff;
}}

body {{
    font-family: 'Poppins', sans-serif;
    background-color: var(--bg);
    color: var(--text);
    transition: background-color 0.4s ease, color 0.4s ease;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    overflow-x: hidden;
}}

.container {{
    width: var(--width);
    max-width: 100%;
    height: var(--height);
    min-height: 600px;
    padding: 0 5%;
    display: flex;
    flex-direction: column;
    position: relative;
    background-color: var(--bg);
    transition: background-color 0.4s ease;
}}

/* Navbar Styles */
.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 15vh;
    min-height: 80px;
}}

.logo {{
    font-size: 24px;
    font-weight: 800;
    color: var(--text);
    text-decoration: none;
    display: flex;
    align-items: center;
    gap: 10px;
    letter-spacing: 1px;
}}

.logo-icon {{
    width: 32px;
    height: 32px;
    background-color: var(--accent);
    clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
    display: inline-block;
}}

.nav-links {{
    display: flex;
    list-style: none;
    gap: 35px;
}}

.nav-links a {{
    text-decoration: none;
    color: var(--text);
    font-weight: 500;
    text-transform: uppercase;
    font-size: 14px;
    letter-spacing: 1px;
    transition: color 0.3s ease;
}}

.nav-links a:hover {{
    color: var(--accent);
}}

.theme-toggle {{
    background: none;
    border: none;
    color: var(--text);
    font-size: 22px;
    cursor: pointer;
    transition: color 0.3s ease, transform 0.3s ease;
}}

.theme-toggle:hover {{
    color: var(--accent);
    transform: scale(1.1);
}}

/* Hero Section Styles */
.hero {{
    display: flex;
    align-items: center;
    flex: 1;
    gap: 40px;
}}

.text-content {{
    flex: 1;
    padding-right: 20px;
}}

h1 {{
    font-size: clamp(40px, 5vw, 65px);
    font-weight: 800;
    text-transform: uppercase;
    line-height: 1.1;
    margin-bottom: 25px;
    letter-spacing: 2px;
}}

h1 .accent {{
    color: var(--accent);
}}

.body-text {{
    font-size: 16px;
    line-height: 1.7;
    margin-bottom: 40px;
    max-width: 500px;
    opacity: 0.9;
}}

.actions {{
    display: flex;
    align-items: center;
    gap: 30px;
    flex-wrap: wrap;
}}

.btn {{
    display: inline-block;
    padding: 14px 32px;
    background-color: transparent;
    color: var(--text);
    text-decoration: none;
    font-weight: 600;
    border: 2px solid var(--text);
    border-radius: 40px;
    text-transform: uppercase;
    font-size: 14px;
    letter-spacing: 1px;
    transition: all 0.3s ease;
}}

.btn:hover {{
    background-color: var(--accent);
    border-color: var(--accent);
    color: #ffffff;
}}

.social-links {{
    display: flex;
    gap: 20px;
}}

.social-links a {{
    color: var(--text);
    font-size: 22px;
    transition: color 0.3s ease, transform 0.3s ease;
}}

.social-links a:hover {{
    color: var(--accent);
    transform: translateY(-3px);
}}

/* Image & Organic Blob Styles */
.image-content {{
    flex: 1;
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
}}

.blob-background {{
    position: absolute;
    width: 80%;
    aspect-ratio: 1;
    max-width: 450px;
    background-color: var(--accent);
    /* Complex border radius creates the organic shape */
    border-radius: 40% 60% 70% 30% / 40% 50% 60% 50%;
    z-index: 1;
    animation: blobMorph 8s ease-in-out infinite alternate;
}}

@keyframes blobMorph {{
    0% {{ border-radius: 40% 60% 70% 30% / 40% 50% 60% 50%; }}
    100% {{ border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%; }}
}}

.profile-img {{
    position: relative;
    z-index: 2;
    width: 65%;
    max-width: 380px;
    height: auto;
    border-radius: 20px;
    box-shadow: 0 25px 50px rgba(0,0,0,0.25);
    object-fit: cover;
}}

/* Responsive Breakpoints */
@media (max-width: 900px) {{
    .hero {{
        flex-direction: column;
        text-align: center;
        padding-top: 30px;
        padding-bottom: 50px;
    }}
    .text-content {{
        padding-right: 0;
        margin-bottom: 40px;
        display: flex;
        flex-direction: column;
        align-items: center;
    }}
    .actions {{
        justify-content: center;
    }}
    .nav-links {{
        display: none; /* Collapsed for mobile simplicity */
    }}
    .blob-background {{
        width: 90%;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Themeable Portfolio Hero</title>
    <!-- FontAwesome for Vector Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body class="{body_class}">
    <div class="container">
        <!-- Navigation -->
        <nav class="navbar">
            <a href="#" class="logo">
                <span class="logo-icon"></span>
                DEV
            </a>
            <ul class="nav-links">
                <li><a href="#">Home</a></li>
                <li><a href="#">About</a></li>
                <li><a href="#">Portfolio</a></li>
                <li><a href="#">Services</a></li>
                <li><a href="#">Hire Me</a></li>
            </ul>
            <button id="theme-toggle" class="theme-toggle" aria-label="Toggle light and dark theme">
                <i class="fas {icon_class}"></i>
            </button>
        </nav>

        <!-- Main Hero Section -->
        <main class="hero">
            <div class="text-content">
                <h1>{title_text}</h1>
                <p class="body-text">{body_text}</p>
                <div class="actions">
                    <a href="#" class="btn">Download Resume</a>
                    <div class="social-links">
                        <a href="#" aria-label="GitHub"><i class="fab fa-github"></i></a>
                        <a href="#" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
                        <a href="#" aria-label="LinkedIn"><i class="fab fa-linkedin-in"></i></a>
                    </div>
                </div>
            </div>
            
            <div class="image-content">
                <!-- Morphing CSS shape -->
                <div class="blob-background"></div>
                <!-- Placeholder Image -->
                <img src="https://images.unsplash.com/photo-1560250097-0b93528c311a?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" alt="Profile picture" class="profile-img">
            </div>
        </main>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Theme Toggle Logic
document.addEventListener('DOMContentLoaded', () => {{
    const toggleBtn = document.getElementById('theme-toggle');
    const body = document.body;
    const icon = toggleBtn.querySelector('i');

    toggleBtn.addEventListener('click', () => {{
        // Toggle the class that maps to our CSS Variables
        body.classList.toggle('dark-theme');
        
        // Swap FontAwesome icons based on current theme state
        if(body.classList.contains('dark-theme')) {{
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
        }} else {{
            icon.classList.remove('fa-sun');
            icon.classList.add('fa-moon');
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