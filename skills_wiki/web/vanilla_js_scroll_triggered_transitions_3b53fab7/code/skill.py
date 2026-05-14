def create_component(
    output_dir: str,
    title_text: str = "Scroll Reveal Magic",
    body_text: str = "Buy my product",
    color_scheme: str = "dark",
    accent_color: str = "#00bfff",
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Vanilla JS Animate On Scroll effect.
    """
    import os
    import html

    os.makedirs(output_dir, exist_ok=True)
    
    # Escape user inputs
    safe_title = html.escape(title_text)
    safe_body = html.escape(body_text)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#131316"
        text_color = "#ffffff"
        surface_color = "rgba(255, 255, 255, 0.08)"
        border_color = "rgba(255, 255, 255, 0.15)"
    else:
        bg_color = "#ffffff"
        text_color = "#131316"
        surface_color = "rgba(0, 0, 0, 0.05)"
        border_color = "rgba(0, 0, 0, 0.1)"

    # === CSS ===
    css = f"""/* Vanilla JS Scroll-Triggered Transitions */
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
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Poppins', system-ui, -apple-system, sans-serif;
    background: #000; /* Darker backdrop for the component frame */
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

/* The isolated scrollable component */
.scroll-container {{
    width: var(--width);
    height: var(--height);
    background: var(--bg);
    overflow-y: scroll;
    overflow-x: hidden; /* Prevent horizontal scrollbar from translate */
    scroll-behavior: smooth;
    position: relative;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    border-radius: 12px;
}}

/* Hide scrollbar for a cleaner look */
.scroll-container::-webkit-scrollbar {{
    width: 8px;
}}
.scroll-container::-webkit-scrollbar-track {{
    background: var(--bg);
}}
.scroll-container::-webkit-scrollbar-thumb {{
    background: var(--border);
    border-radius: 4px;
}}

section {{
    display: grid;
    place-items: center;
    align-content: center;
    min-height: 100%; /* Relative to the scroll-container's height */
    padding: 2rem;
    text-align: center;
}}

h1 {{
    font-size: 3rem;
    margin-bottom: 1rem;
}}

h2 {{
    font-size: 2.5rem;
    margin-bottom: 1rem;
}}

p {{
    font-size: 1.1rem;
    line-height: 1.6;
    max-width: 600px;
    opacity: 0.8;
}}

/* --- THE CORE ANIMATION CLASSES --- */

.hidden {{
    opacity: 0;
    filter: blur(5px);
    transform: translateX(-100%);
    transition: all 1s ease-out;
}}

.show {{
    opacity: 1;
    filter: blur(0);
    transform: translateX(0);
}}

/* Staggered Card Layout */
.stagger-group {{
    display: flex;
    gap: 1.5rem;
    margin-top: 2rem;
    flex-wrap: wrap;
    justify-content: center;
}}

.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    padding: 2rem;
    border-radius: 16px;
    font-size: 3rem;
    width: 120px;
    height: 120px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: transform 0.2s, background 0.2s;
}}

.card:hover {{
    transform: scale(1.05) translateY(-5px);
    border-color: var(--accent);
}}

/* Apply Staggered Delays for children */
/* Using specific delays to match the video's list staggering effect */
.stagger-group .hidden:nth-child(1) {{ transition-delay: 100ms; }}
.stagger-group .hidden:nth-child(2) {{ transition-delay: 200ms; }}
.stagger-group .hidden:nth-child(3) {{ transition-delay: 300ms; }}
.stagger-group .hidden:nth-child(4) {{ transition-delay: 400ms; }}

/* --- ACCESSIBILITY --- */
/* The polite way to handle animations for users who prefer reduced motion */
@media(prefers-reduced-motion) {{
    .hidden {{
        transition: none;
    }}
}}
"""

    # === HTML ===
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="scroll-container">
        
        <!-- Section 1: Hero (Static, visible immediately) -->
        <section class="hero">
            <h1>Hi Mom!</h1>
            <p>Scroll down to see the Intersection Observer magic in action.</p>
            <svg style="width:24px; height:24px; margin-top:2rem; animation: bounce 2s infinite;" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 5v14M19 12l-7 7-7-7"/>
            </svg>
            <style>
                @keyframes bounce {{
                    0%, 20%, 50%, 80%, 100% {{transform: translateY(0);}}
                    40% {{transform: translateY(-20px);}}
                    60% {{transform: translateY(-10px);}}
                }}
            </style>
        </section>

        <!-- Section 2: Standard Slide-in Reveal -->
        <section>
            <div class="hidden">
                <h2 style="color: var(--accent);">{safe_body}</h2>
                <p>The things you own end up owning you. It's only after you lose everything that you're free to do anything.</p>
            </div>
        </section>

        <!-- Section 3: Staggered Child Element Reveal -->
        <section>
            <h2 class="hidden">It's really good</h2>
            <div class="stagger-group">
                <div class="card hidden logo">🤓</div>
                <div class="card hidden logo">👩🏽‍🦱</div>
                <div class="card hidden logo">👴🏻</div>
                <div class="card hidden logo">👵🏼</div>
            </div>
        </section>
        
        <!-- Section 4: Outro -->
        <section>
            <h2 class="hidden" style="color: var(--accent);">{safe_title} Complete</h2>
            <p class="hidden" style="transition-delay: 200ms;">Keep scrolling up and down to replay the animations.</p>
        </section>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Intersection Observer Logic
document.addEventListener('DOMContentLoaded', () => {{
    // 1. Identify the scrolling viewport. 
    // In a full webpage, this is usually 'null' (the browser window).
    // Because we are building a constrained UI component, we observe relative to our custom scroll container.
    const scrollContainer = document.querySelector('.scroll-container');

    // 2. Create the observer
    const observer = new IntersectionObserver((entries) => {{
        entries.forEach((entry) => {{
            // Log entry state to console (optional, good for debugging)
            // console.log(entry.target, entry.isIntersecting);
            
            if (entry.isIntersecting) {{
                // Add the 'show' class to trigger CSS transition
                entry.target.classList.add('show');
            }} else {{
                // Remove the class when scrolled out of view so it animates again next time
                entry.target.classList.remove('show');
            }}
        }});
    }}, {{
        root: scrollContainer,
        // Trigger when 10% of the element is visible
        threshold: 0.1 
    }});

    // 3. Grab all elements that need to be animated
    const hiddenElements = document.querySelectorAll('.hidden');
    
    // 4. Tell the observer to watch each one
    hiddenElements.forEach((el) => observer.observe(el));
}});
"""

    # Write files
    files = []
    for fname, content in [("index.html", html_content), ("style.css", css), ("script.js", js)]:
        path = os.path.join(output_dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        files.append(path)

    return {
        "html": html_content,
        "css": css,
        "js": js,
        "files": files,
    }
