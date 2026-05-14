# Developer-Centric Dark Mode Hero & Feature Grid

## Analysis

# Skill Strategy: Developer SaaS Dark Mode Hero

## 1. High-level Design Pattern Extraction

> **Skill Name**: Developer-Centric Dark Mode Hero & Feature Grid

* **Core Visual Mechanism**: High-contrast dark theme characterized by oversized, tightly-kerned typography (`letter-spacing: -0.05em`) and stark neon accents. The layout relies heavily on generous whitespace and massive font sizes rather than borders or background panels to establish visual hierarchy. It frequently employs technical visual metaphors, such as faux syntax-highlighted code windows, to immediately signal its target audience.
* **Why Use This Skill (Rationale)**: This aesthetic instantly communicates "modern developer tool" or "high-tech SaaS framework." Dark mode is naturally preferred by the developer demographic as it reduces eye strain. The use of vibrant, high-saturation accents (like neon green or cyan) against an almost-black background creates a focal point that draws immediate attention to primary Calls to Action (CTAs), driving conversions.
* **Overall Applicability**: Perfect for SaaS landing pages, API documentation portals, developer tools, Web3/crypto projects, and technical product marketing sites.
* **Value Addition**: Compared to standard landing pages, this pattern establishes immediate technical credibility. The "code window" graphic replaces generic illustrations, showing product value directly, while the tight, oversized typography conveys confidence and modernity.
* **Browser Compatibility**: Uses modern CSS Grid, Flexbox, and CSS Variables. Fully supported in all modern browsers (Chrome 80+, Safari 14+, Firefox 75+, Edge 80+).

## 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**: Dominant deep black/dark gray backgrounds (`#0a0a0a` or `#111827`), pure white primary headings (`#ffffff`), and muted gray secondary body text (`#a1a1aa` or `#9ca3af`). Accents are extremely vibrant (e.g., lime green `#a3e635` or emerald `#10b981`).
  - **Typographic Hierarchy**: Relies heavily on system sans-serif fonts (like *Inter* or *Rubik*). Headings are massive (`4rem` to `5rem`), heavy (`font-weight: 700` or `800`), with aggressively tight tracking (`letter-spacing: -0.04em`) and short line heights (`line-height: 1.1`). Body text is highly legible (`1.125rem`, `line-height: 1.6`).
  - **Component Details**: Input fields feature dark, subtle surface backgrounds (`#27272a`) to blend into the dark theme, paired with borderless, solid-color neon CTA buttons.

* **Step B: Layout & Compositional Style**
  - **Layout System**: Uses a fluid Flexbox navbar and a two-column CSS Grid for the Hero section on desktop (collapsing to a single column on mobile). The features section utilizes a standard 3-column CSS Grid (`grid-template-columns: repeat(auto-fit, minmax(300px, 1fr))`).
  - **Spatial Feel**: Content is heavily left-aligned in the hero, creating a strong reading edge. Padding is generous (`padding: 120px 0` for main sections) to let the large typography breathe.

* **Step C: Interactive Behavior & Animations**
  - **Interactions**: Buttons have subtle scaling and brightness transitions on hover.
  - **Animations**: Elements use a subtle, JavaScript-triggered Intersection Observer to fade and slide up into view as the user scrolls, creating a smooth, premium entrance.

## 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Responsive Layout Structure | CSS Grid & Flexbox | Clean, native responsive behavior without complex media queries. |
| Typography & Theming | CSS Custom Properties | Allows seamless injection of accent colors and dark/light mode toggles. |
| Code Window Graphic | Pure HTML/CSS | Recreates the macOS-style window and syntax highlighting natively without heavy images or external SVGs. |
| Reveal Animations | JS Intersection Observer | Performant native API for triggering CSS transitions when elements enter the viewport. |

> **Feasibility Assessment**: 100% reproduction of the core layout, typographic styling, and color logic seen in the reference material.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "The platform for local-first software.",
    body_text: str = "Don't write real-time APIs. Move your database to the browser. Keep local data in sync effortlessly.",
    color_scheme: str = "dark",        
    accent_color: str = "#22c55e",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Developer-Centric Dark Mode Hero.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0a0a0a"
        text_primary = "#ffffff"
        text_secondary = "#a1a1aa"
        surface_bg = "#18181b"
        border_color = "#27272a"
        code_bg = "#1e1e1e"
        btn_text = "#050505"
    else:
        bg_color = "#ffffff"
        text_primary = "#09090b"
        text_secondary = "#52525b"
        surface_bg = "#f4f4f5"
        border_color = "#e4e4e7"
        code_bg = "#1e1e1e" # Code windows usually stay dark
        btn_text = "#ffffff"

    # === CSS ===
    css = f"""/* Developer SaaS Hero Component */
:root {{
    --bg-color: {bg_color};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --surface-bg: {surface_bg};
    --border-color: {border_color};
    --accent-color: {accent_color};
    --code-bg: {code_bg};
    --btn-text: {btn_text};
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-primary);
    line-height: 1.5;
    -webkit-font-smoothing: antialiased;
    overflow-x: hidden;
}}

/* Layout Container */
.container {{
    max-width: 1280px;
    margin: 0 auto;
    padding: 0 24px;
}}

/* Navbar */
.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 24px 0;
}}

.logo {{
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    display: flex;
    align-items: center;
    gap: 8px;
}}

.logo-icon {{
    width: 24px;
    height: 24px;
    background-color: var(--accent-color);
    border-radius: 6px;
}}

.nav-links {{
    display: none;
    gap: 32px;
}}

@media (min-width: 768px) {{
    .nav-links {{ display: flex; }}
}}

.nav-links a {{
    color: var(--text-secondary);
    text-decoration: none;
    font-size: 0.95rem;
    font-weight: 500;
    transition: color 0.2s ease;
}}

.nav-links a:hover {{
    color: var(--text-primary);
}}

/* Buttons */
.btn {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 12px 24px;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.95rem;
    text-decoration: none;
    cursor: pointer;
    transition: all 0.2s ease;
    border: none;
}}

.btn-accent {{
    background-color: var(--accent-color);
    color: var(--btn-text);
}}

.btn-accent:hover {{
    filter: brightness(1.1);
    transform: translateY(-1px);
}}

.btn-outline {{
    background-color: transparent;
    color: var(--text-primary);
    border: 1px solid var(--border-color);
}}

.btn-outline:hover {{
    background-color: var(--surface-bg);
}}

/* Hero Section */
.hero {{
    display: grid;
    grid-template-columns: 1fr;
    gap: 64px;
    padding: 80px 0;
    align-items: center;
}}

@media (min-width: 1024px) {{
    .hero {{
        grid-template-columns: 1fr 1fr;
        padding: 120px 0;
    }}
}}

.hero-content h1 {{
    font-size: clamp(3rem, 6vw, 5rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.04em;
    margin-bottom: 24px;
}}

.hero-content p {{
    font-size: clamp(1.125rem, 2vw, 1.25rem);
    color: var(--text-secondary);
    margin-bottom: 40px;
    max-width: 540px;
}}

.email-form {{
    display: flex;
    flex-direction: column;
    gap: 12px;
    max-width: 480px;
}}

@media (min-width: 480px) {{
    .email-form {{
        flex-direction: row;
    }}
}}

.email-form input {{
    flex: 1;
    background-color: var(--surface-bg);
    border: 1px solid var(--border-color);
    color: var(--text-primary);
    padding: 14px 16px;
    border-radius: 8px;
    font-size: 1rem;
    font-family: inherit;
    outline: none;
    transition: border-color 0.2s ease;
}}

.email-form input:focus {{
    border-color: var(--accent-color);
}}

/* Code Window Graphic */
.code-window {{
    background-color: var(--code-bg);
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    overflow: hidden;
    color: #e5e5e5;
    font-family: 'Fira Code', monospace;
    font-size: 0.9rem;
    line-height: 1.6;
}}

.window-header {{
    display: flex;
    gap: 8px;
    padding: 16px;
    background-color: rgba(255, 255, 255, 0.03);
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}}

.dot {{
    width: 12px;
    height: 12px;
    border-radius: 50%;
}}

.dot.red {{ background-color: #ff5f56; }}
.dot.yellow {{ background-color: #ffbd2e; }}
.dot.green {{ background-color: #27c93f; }}

.window-body {{
    padding: 24px;
    overflow-x: auto;
}}

.kw {{ color: #ff7b72; }} /* Keyword */
.fn {{ color: #d2a8ff; }} /* Function */
.st {{ color: #a5d6ff; }} /* String */
.co {{ color: #8b949e; }} /* Comment */
.vr {{ color: #79c0ff; }} /* Variable */

/* Features Section */
.features {{
    padding: 80px 0;
    border-top: 1px solid var(--border-color);
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 48px;
}}

.feature-icon {{
    width: 48px;
    height: 48px;
    border-radius: 12px;
    background-color: var(--surface-bg);
    border: 1px solid var(--border-color);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 24px;
    color: var(--accent-color);
}}

.feature h3 {{
    font-size: 1.25rem;
    font-weight: 700;
    margin-bottom: 12px;
    letter-spacing: -0.02em;
}}

.feature p {{
    color: var(--text-secondary);
    font-size: 1rem;
}}

/* Reveal Animation Classes */
.reveal {{
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 0.8s ease-out, transform 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}}

.reveal.visible {{
    opacity: 1;
    transform: translateY(0);
}}

.delay-1 {{ transition-delay: 0.1s; }}
.delay-2 {{ transition-delay: 0.2s; }}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Fira+Code&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <header class="navbar reveal">
            <div class="logo">
                <div class="logo-icon"></div>
                homebase
            </div>
            <nav class="nav-links">
                <a href="#">Documentation</a>
                <a href="#">Pricing</a>
                <a href="#">Resources</a>
                <a href="#">Blog</a>
            </nav>
            <a href="#" class="btn btn-outline">Sign In</a>
        </header>

        <main>
            <section class="hero">
                <div class="hero-content">
                    <h1 class="reveal delay-1">{title_text}</h1>
                    <p class="reveal delay-2">{body_text}</p>
                    <form class="email-form reveal delay-2" onsubmit="event.preventDefault();">
                        <input type="email" placeholder="Your email address" required>
                        <button type="submit" class="btn btn-accent">Get early access</button>
                    </form>
                </div>
                
                <div class="hero-graphic reveal delay-2">
                    <div class="code-window">
                        <div class="window-header">
                            <span class="dot red"></span>
                            <span class="dot yellow"></span>
                            <span class="dot green"></span>
                        </div>
                        <div class="window-body">
<pre><code><span class="kw">import</span> {{ useCurrentUser, useQuery }} <span class="kw">from</span> <span class="st">'homebase-react'</span>

<span class="kw">const</span> <span class="fn">Todos</span> = ({{ project }}) => {{
  <span class="kw">const</span> [currentUser] = <span class="fn">useCurrentUser</span>()
  <span class="kw">const</span> [todos, errors, syncing] = <span class="fn">useQuery</span>({{
    $find: <span class="st">'todo'</span>,
    $where: {{
      project: project.id,
      isArchived: <span class="kw">false</span>
    }}
  }})

  <span class="kw">if</span> (errors) <span class="kw">return</span> &lt;Error /&gt;
  
  <span class="co">// Data syncs automatically</span>
  <span class="kw">return</span> (
    &lt;div&gt;{{todos.map(t => &lt;Todo key={{t.id}} data={{t}}/&gt;)}}&lt;/div&gt;
  )
}}</code></pre>
                        </div>
                    </div>
                </div>
            </section>

            <section class="features">
                <div class="feature reveal">
                    <div class="feature-icon">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>
                    </div>
                    <h3>Faster than an API</h3>
                    <p>Changes are pushed to all clients in real-time. Local data is fast, read and write it instantly. Cache it forever.</p>
                </div>
                <div class="feature reveal delay-1">
                    <div class="feature-icon">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>
                    </div>
                    <h3>Easy to use</h3>
                    <p>Develop with a local database that's as capable as cloud DBs. Cut out your API and manage data flows effortlessly.</p>
                </div>
                <div class="feature reveal delay-2">
                    <div class="feature-icon">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
                    </div>
                    <h3>More Collaborative</h3>
                    <p>When the database is responsible for resolving conflicts you don't have to solve realtime collaboration manually.</p>
                </div>
            </section>
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Intersection Observer for scroll-triggered reveal animations
document.addEventListener('DOMContentLoaded', () => {{
    const revealElements = document.querySelectorAll('.reveal');

    const revealObserver = new IntersectionObserver((entries, observer) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                entry.target.classList.add('visible');
                // Optional: Stop observing once revealed
                observer.unobserve(entry.target);
            }}
        }});
    }}, {{
        root: null,
        threshold: 0.1, // Trigger when 10% of the element is visible
        rootMargin: "0px 0px -50px 0px"
    }});

    revealElements.forEach(el => {{
        revealObserver.observe(el);
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

## 4. Accessibility & Performance Notes

* **Accessibility**: 
  - Structural HTML5 tags (`<header>`, `<nav>`, `<main>`, `<section>`) are used to establish a clear document outline.
  - The contrast ratio between the primary text (`#ffffff`) and the dark background (`#0a0a0a`) far exceeds WCAG AAA standards. 
  - Form inputs include visual focus states (`border-color` change) to assist keyboard navigators.
  - SVG icons inside the features section use standard stroke styling without relying on external icon fonts, preventing text-scaling issues.
* **Performance**: 
  - The scroll-reveal effect utilizes the native `IntersectionObserver` API, which is non-blocking and highly performant compared to binding functions directly to the `scroll` event.
  - CSS animations use `opacity` and `transform`, which are hardware-accelerated properties, preventing main-thread layout thrashing.
  - No heavy frameworks or libraries are included; the implementation relies strictly on vanilla CSS and JavaScript, resulting in a near-instant Time to Interactive (TTI).