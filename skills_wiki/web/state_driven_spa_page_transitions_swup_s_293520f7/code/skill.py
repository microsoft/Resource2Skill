def create_component(
    output_dir: str,
    title_text: str = "Smooth Transitions",
    body_text: str = "Click the navigation links above to see the page transition effect without a hard browser reload. This mimics modern SPA routing.",
    color_scheme: str = "dark",
    accent_color: str = "#00bfff",
    width_px: int = 1000,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the SPA Page Transition visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
        surface_color = "#161b26"
        border_color = "rgba(255, 255, 255, 0.08)"
    else:
        bg_color = "#e9ecef"
        text_color = "#1a1a2e"
        surface_color = "#ffffff"
        border_color = "rgba(0, 0, 0, 0.08)"

    # === CSS ===
    css = f"""/* Smooth SPA Transitions */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --border: {border_color};
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.app-container {{
    width: {width_px}px;
    height: {height_px}px;
    background: var(--surface);
    border-radius: 12px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    border: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    overflow: hidden;
}}

/* -- Header & Nav -- */
header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem 2.5rem;
    border-bottom: 1px solid var(--border);
}}

.logo {{
    font-weight: 700;
    font-size: 1.25rem;
    letter-spacing: -0.5px;
}}

.logo span {{
    color: var(--accent);
}}

nav {{
    display: flex;
    gap: 2rem;
}}

nav a {{
    color: var(--text);
    text-decoration: none;
    font-weight: 500;
    font-size: 0.95rem;
    opacity: 0.7;
    transition: opacity 0.2s, color 0.2s;
}}

nav a:hover {{
    opacity: 1;
}}

nav a.active {{
    opacity: 1;
    color: var(--accent);
}}

/* -- Main Content Area -- */
main {{
    padding: 3rem 2.5rem;
    flex: 1;
    display: flex;
    flex-direction: column;
}}

.title {{
    font-size: 2.5rem;
    margin-bottom: 1rem;
    font-weight: 600;
    letter-spacing: -1px;
}}

.body-text {{
    font-size: 1.1rem;
    line-height: 1.6;
    opacity: 0.8;
    max-width: 600px;
}}

.btn {{
    align-self: flex-start;
    margin-top: 2rem;
    padding: 0.8rem 1.5rem;
    background: var(--accent);
    color: #fff;
    border: none;
    border-radius: 6px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}}

/* =========================================
   CORE SKILL: TRANSITION LIFECYCLE HOOKS
   ========================================= */

/* Default State (Entered / Idle) */
.transition-fade {{
    transition: all 500ms cubic-bezier(0.4, 0, 0.2, 1);
    opacity: 1;
    transform: translateX(0);
}}

/* Entry State (Animating IN from the right) */
html.is-animating .transition-fade {{
    opacity: 0;
    transform: translateX(40px);
}}

/* Exit State (Animating OUT to the left) */
html.is-animating.is-leaving .transition-fade {{
    opacity: 0;
    transform: translateX(-40px);
}}


/* Alternate element-specific animation (Swipe) */
.transition-swipe {{
    transition: all 500ms cubic-bezier(0.4, 0, 0.2, 1);
    opacity: 1;
    transform: translateY(0);
}}

html.is-animating .transition-swipe {{
    opacity: 0;
    transform: translateY(40px); /* Enters from bottom */
}}

html.is-animating.is-leaving .transition-swipe {{
    opacity: 0;
    transform: translateY(-40px); /* Leaves to top */
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-container">
        <header>
            <div class="logo">SPA<span>Motion</span></div>
            <nav>
                <a href="#" data-target="home" class="active">Home</a>
                <a href="#" data-target="pricing">Pricing</a>
                <a href="#" data-target="about">About</a>
            </nav>
        </header>
        
        <!-- The container that gets swapped and animated -->
        <main id="swup">
            <div class="transition-fade">
                <h1 class="title">{title_text}</h1>
                <p class="body-text">{body_text}</p>
            </div>
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Virtual Pages Data (Simulating server HTML responses)
const pages = {{
    'home': `
        <div class="transition-fade">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
    `,
    'pricing': `
        <div class="transition-fade">
            <h1 class="title">Flexible Pricing</h1>
            <p class="body-text">We offer multiple tiers for different needs. Notice how this text fades and slides in smoothly.</p>
        </div>
        <button class="btn transition-swipe">Purchase Now</button>
    `,
    'about': `
        <div class="transition-fade">
            <h1 class="title">About This Effect</h1>
            <p class="body-text">This simulates the Swup.js lifecycle. Elements are assigned lifecycle classes (is-animating, is-leaving) to trigger CSS-based entry and exit states.</p>
        </div>
    `
}};

document.addEventListener('DOMContentLoaded', () => {{
    const navLinks = document.querySelectorAll('nav a');
    const mainContainer = document.getElementById('swup');
    let isNavigating = false;

    navLinks.forEach(link => {{
        link.addEventListener('click', (e) => {{
            e.preventDefault();
            if (isNavigating) return; // Prevent spam clicking

            const target = e.target.getAttribute('data-target');
            if (!pages[target]) return;

            isNavigating = true;

            // Update Nav Active State
            navLinks.forEach(l => l.classList.remove('active'));
            e.target.classList.add('active');

            const html = document.documentElement;
            
            // 1. Start Leave Animation
            html.classList.add('is-animating', 'is-leaving');
            
            // 2. Wait for exit transition to complete (500ms matches CSS)
            setTimeout(() => {{
                
                // 3. Swap the DOM content
                mainContainer.innerHTML = pages[target];
                
                // 4. Remove 'is-leaving' to prep elements in their Entry start state
                html.classList.remove('is-leaving');
                
                // 5. Force a reflow so the browser registers the start state
                requestAnimationFrame(() => {{
                    requestAnimationFrame(() => {{
                        
                        // 6. Remove 'is-animating' to trigger the Entry transition
                        html.classList.remove('is-animating');
                        
                        // Unlock routing after entry finishes
                        setTimeout(() => {{
                            isNavigating = false;
                        }}, 500);

                    }});
                }});

            }}, 500); 
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
