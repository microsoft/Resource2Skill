# Dark Mode Neon Glow Hero with Glassmorphism Header

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Dark Mode Neon Glow Hero with Glassmorphism Header

* **Core Visual Mechanism**: This design relies on a high-contrast "cyberpunk" or modern developer aesthetic. It combines a pitch-black/dark-grey background with a highly vibrant neon accent color (typically neon green or cyan). Depth is created using two primary techniques:
  1. **Glassmorphism**: A fixed top navigation bar with a semi-transparent background and `backdrop-filter: blur()` allows the background and scrolled content to faintly show through.
  2. **Layered Box Shadows (Neon Glow)**: Primary focal points (like the hero avatar and social buttons) have a baseline neon `box-shadow`. On hover, this shadow multiplies into layered, comma-separated values (e.g., `0 0 25px, 0 0 50px, 0 0 100px`) to create an intense, realistic blooming light effect.

* **Why Use This Skill (Rationale)**: The dark background forces the user's eye directly to the neon-accented elements, creating a clear, dominant visual hierarchy. The expanding glow on hover provides highly satisfying, tactile feedback that feels "electric" and responsive.

* **Overall Applicability**: Perfect for developer portfolios, SaaS product landing pages targeting technical users, Web3/crypto interfaces, and gaming websites.

* **Value Addition**: Transforms a standard two-column hero layout into a premium, interactive experience. The glass header maintains spatial context when scrolling, while the glowing hover states make the interface feel alive and polished.

* **Browser Compatibility**: Requires modern browsers. `backdrop-filter` requires Safari 9+, Chrome 76+, Edge 79+. Layered box shadows and CSS variables are universally supported in modern browsers. 


### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Colors**: Background `#000000` or `#080808`. Surface/Secondary background `#131313`. Text `#ffffff`. Accent (Neon) `#00ff51` (adjustable).
  - **Typography**: Clean geometric sans-serif (e.g., Poppins, Inter). High contrast in weights (font-weight 800 for names/logos, 500 for standard text).
  - **CSS Drivers**: 
    - Header: `background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(10px);`
    - Glow: `box-shadow: 0 0 25px var(--accent);`
    - Avatar masking: `border-radius: 50%;`

* **Step B: Layout & Compositional Style**
  - **Layout**: CSS Flexbox dominates here. The hero section is a flex container (`align-items: center`, `justify-content: space-between`).
  - **Spacing**: Uses generous horizontal padding (e.g., `padding: 10rem 12%`) to frame the content, preventing it from feeling cramped.
  - **Responsive Strategy**: At ~1024px, the layout flips to `flex-direction: column-reverse`, stacking the text below the glowing avatar, and swapping the inline nav links for a hamburger menu.

* **Step C: Interactive Behavior & Animations**
  - **Hover Scaling**: Interactive elements (social icons, avatar) scale up slightly (`transform: scale(1.05)`) or translate vertically (`transform: translateY(-5px)`).
  - **Hover Glowing**: The baseline `25px` blur spread transitions into a massive `100px` multi-layered spread.
  - **Timing**: Smooth transitions (`transition: 0.3s ease`) applied to `box-shadow`, `transform`, and `background-color`.
  - **JS Behavior**: A simple class toggle on the navbar and menu icon to handle mobile drop-down states.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Glassmorphism Header | CSS `backdrop-filter` | Native, performant way to blur elements behind a container. |
| Neon Glow Effects | CSS `box-shadow` (layered) | Chaining multiple shadows creates a realistic light bloom without Canvas/WebGL. |
| Hero Layout | CSS Flexbox | Easily handles vertical centering and swapping to column-layout on mobile. |
| Mobile Menu Toggle | JavaScript (DOM) | Simplest way to toggle CSS classes for opening/closing the mobile nav. |
| Icons | BoxIcons CDN | Lightweight, consistent iconography matching the tutorial's aesthetic. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Hi, It's Developer",
    body_text: str = "I'm a passionate frontend developer specializing in creating interactive, glowing web experiences.",
    color_scheme: str = "dark",        
    accent_color: str = "#00ff51",     # Cyberpunk neon green
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Neon Glow Hero & Glass Header effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Force dark scheme mapping for best neon contrast, but allow slight variations
    if color_scheme == "light":
        bg_color = "#f0f0f0"
        second_bg = "#ffffff"
        text_color = "#080808"
        glass_bg = "rgba(255, 255, 255, 0.4)"
        btn_text = "#ffffff"
    else:
        bg_color = "#080808"
        second_bg = "#131313"
        text_color = "#ffffff"
        glass_bg = "rgba(0, 0, 0, 0.3)"
        btn_text = "#000000"

    # === CSS ===
    css = f"""@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;800&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    text-decoration: none;
    outline: none;
}}

:root {{
    --bg-color: {bg_color};
    --second-bg-color: {second_bg};
    --text-color: {text_color};
    --main-color: {accent_color};
    --btn-text: {btn_text};
}}

/* Preview container to simulate browser window for the agent */
.preview-window {{
    width: {width_px}px;
    height: {height_px}px;
    max-width: 100%;
    margin: 0 auto;
    position: relative;
    overflow-y: auto;
    overflow-x: hidden;
    background: var(--bg-color);
    color: var(--text-color);
    font-family: 'Poppins', sans-serif;
    scroll-behavior: smooth;
    border: 1px solid #333;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}}

/* Header / Glassmorphism */
.header {{
    position: sticky;
    top: 0;
    left: 0;
    width: 100%;
    padding: 2rem 8%;
    background: {glass_bg};
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 100;
}}

.logo {{
    font-size: 2rem;
    color: var(--text-color);
    font-weight: 800;
    cursor: pointer;
    transition: 0.3s ease;
}}

.logo span {{
    color: var(--main-color);
}}

.logo:hover {{
    transform: scale(1.05);
}}

.navbar a {{
    font-size: 1rem;
    color: var(--text-color);
    margin-left: 3rem;
    font-weight: 500;
    transition: 0.3s ease;
    border-bottom: 3px solid transparent;
    padding-bottom: 4px;
}}

.navbar a:hover, .navbar a.active {{
    color: var(--main-color);
    border-bottom: 3px solid var(--main-color);
}}

#menu-icon {{
    font-size: 2.5rem;
    color: var(--main-color);
    display: none;
    cursor: pointer;
}}

/* Hero Section */
.home {{
    min-height: calc(100% - 80px); /* Adjusting for header */
    padding: 4rem 8%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 4rem;
}}

.home-content {{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    max-width: 600px;
}}

.home-content h1 {{
    font-size: clamp(2.5rem, 5vw, 4.5rem);
    font-weight: 800;
    line-height: 1.2;
}}

.home-content h1 span {{
    color: var(--main-color);
}}

.home-content h3 {{
    font-size: clamp(1.5rem, 3vw, 2.2rem);
    font-weight: 600;
    color: var(--main-color);
    margin-top: 0.5rem;
}}

.home-content p {{
    font-size: 1rem;
    margin: 1.5rem 0 2rem;
    line-height: 1.6;
    color: var(--text-color);
    opacity: 0.9;
}}

/* Glowing Social Icons */
.social-icons {{
    display: flex;
    gap: 1rem;
    margin-bottom: 2.5rem;
}}

.social-icons a {{
    display: inline-flex;
    justify-content: center;
    align-items: center;
    width: 45px;
    height: 45px;
    background: transparent;
    border: 2px solid var(--main-color);
    border-radius: 50%;
    font-size: 1.5rem;
    color: var(--main-color);
    transition: 0.3s ease;
}}

.social-icons a:hover {{
    background: var(--main-color);
    color: var(--btn-text);
    box-shadow: 0 0 25px var(--main-color);
    transform: translateY(-5px);
}}

/* Buttons */
.btn-group {{
    display: flex;
    gap: 1.5rem;
}}

.btn {{
    display: inline-block;
    padding: 0.8rem 2.2rem;
    background: var(--main-color);
    color: var(--btn-text);
    border: 2px solid var(--main-color);
    border-radius: 3rem;
    font-weight: 600;
    letter-spacing: 1px;
    transition: 0.3s ease;
    box-shadow: 0 0 15px var(--main-color);
}}

.btn:hover {{
    box-shadow: 0 0 25px var(--main-color), 0 0 50px var(--main-color);
    transform: scale(1.05);
}}

.btn.transparent {{
    background: transparent;
    color: var(--main-color);
    box-shadow: none;
}}

.btn.transparent:hover {{
    background: var(--main-color);
    color: var(--btn-text);
    box-shadow: 0 0 25px var(--main-color);
}}

/* Glowing Avatar Image */
.home-img img {{
    width: 100%;
    max-width: 400px;
    aspect-ratio: 1/1;
    object-fit: cover;
    border-radius: 50%;
    box-shadow: 0 0 25px var(--main-color);
    transition: 0.4s ease-in-out;
    border: 4px solid var(--second-bg-color);
}}

.home-img img:hover {{
    box-shadow: 0 0 25px var(--main-color),
                0 0 50px var(--main-color),
                0 0 100px var(--main-color);
    transform: scale(1.02);
}}

/* Responsive Breakpoints */
@media (max-width: 900px) {{
    #menu-icon {{
        display: block;
    }}
    
    .navbar {{
        position: absolute;
        top: 100%;
        right: 0;
        width: 50%;
        padding: 1rem 3rem;
        background: var(--bg-color);
        backdrop-filter: blur(10px);
        border-left: 2px solid var(--main-color);
        border-bottom: 2px solid var(--main-color);
        border-bottom-left-radius: 2rem;
        display: none;
        flex-direction: column;
    }}

    .navbar.active {{
        display: flex;
    }}

    .navbar a {{
        display: block;
        font-size: 1.2rem;
        margin: 1.5rem 0;
        text-align: center;
    }}

    .home {{
        flex-direction: column-reverse;
        text-align: center;
        justify-content: center;
        padding-top: 2rem;
    }}

    .home-content {{
        align-items: center;
    }}

    .home-img img {{
        max-width: 300px;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Neon Portfolio Hero</title>
    <!-- BoxIcons for easy icons -->
    <link href='https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css' rel='stylesheet'>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    
    <!-- Wrapper to simulate standard browser view for agent testing -->
    <div class="preview-window">
        
        <!-- Header / Navbar -->
        <header class="header">
            <a href="#" class="logo">Dev<span>Folio</span></a>
            
            <i class='bx bx-menu' id="menu-icon"></i>
            
            <nav class="navbar">
                <a href="#" class="active">Home</a>
                <a href="#">About</a>
                <a href="#">Services</a>
                <a href="#">Portfolio</a>
                <a href="#">Contact</a>
            </nav>
        </header>

        <!-- Hero Section -->
        <section class="home">
            <div class="home-content">
                <h1>{title_text}</h1>
                <h3>A <span>Creative Problem Solver</span></h3>
                <p>{body_text}</p>
                
                <div class="social-icons">
                    <a href="#"><i class='bx bxl-github'></i></a>
                    <a href="#"><i class='bx bxl-linkedin'></i></a>
                    <a href="#"><i class='bx bxl-twitter'></i></a>
                    <a href="#"><i class='bx bxl-discord'></i></a>
                </div>

                <div class="btn-group">
                    <a href="#" class="btn">Hire Me</a>
                    <a href="#" class="btn transparent">View Work</a>
                </div>
            </div>

            <div class="home-img">
                <!-- Using a placeholder API to get a moody tech image -->
                <img src="https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=600&q=80" alt="Developer Profile">
            </div>
        </section>

    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Neon Glow Portfolio - Interactive Behavior

document.addEventListener('DOMContentLoaded', () => {{
    const menuIcon = document.querySelector('#menu-icon');
    const navbar = document.querySelector('.navbar');

    // Toggle Mobile Menu
    menuIcon.addEventListener('click', () => {{
        // Toggle the active class on the navbar to show/hide it
        navbar.classList.toggle('active');
        
        // Swap the box-icon from menu to X
        if(navbar.classList.contains('active')) {{
            menuIcon.classList.remove('bx-menu');
            menuIcon.classList.add('bx-x');
        }} else {{
            menuIcon.classList.remove('bx-x');
            menuIcon.classList.add('bx-menu');
        }}
    }});

    // Close menu when clicking a nav link (useful for mobile)
    const navLinks = document.querySelectorAll('.navbar a');
    navLinks.forEach(link => {{
        link.addEventListener('click', () => {{
            navbar.classList.remove('active');
            menuIcon.classList.remove('bx-x');
            menuIcon.classList.add('bx-menu');
            
            // Handle active state indicator
            navLinks.forEach(nav => nav.classList.remove('active'));
            link.classList.add('active');
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
- [x] Are all external resources loaded from CDN URLs (BoxIcons, Google Fonts)?
- [x] Does the component respect the `width_px` and `height_px` parameters (via the `.preview-window` wrapper)?
- [x] Does the JS execute without errors and successfully toggle the mobile menu?
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect (Glass header + multiple nested glowing box-shadows on hover)?


### 4. Accessibility & Performance Notes

* **Accessibility (a11y)**: 
  - *Color Contrast*: In neon/dark mode designs, ensuring the accent color passes WCAG AA contrast ratio against the dark background is critical. The script maps dark text to the filled button to ensure text readability over bright neon backgrounds.
  - *Focus States*: Currently, the CSS uses `:hover` states extensively. For production a11y, `:focus-visible` should be appended to all `:hover` selectors so keyboard navigators experience the same glow feedback.
  - *Aria labels*: Icon-only buttons (like the social media links) should technically have `aria-label="GitHub"` for screen readers.

* **Performance**: 
  - Heavy use of `box-shadow` (especially layering 3 shadows with 100px spreads) and `backdrop-filter: blur()` forces the browser to heavily utilize the GPU. 
  - *Mitigation*: The `transition` properties are limited to `0.3s`. If running on severely constrained mobile devices, adding `will-change: box-shadow, transform` to the `.btn` and `.home-img img` classes can prompt the browser to create separate composite layers, reducing repaint jank.