def create_component(
    output_dir: str,
    title_text: str = "Intersection Observer Reveal",
    body_text: str = "Scroll down to see elements smoothly fade and slide into view.",
    color_scheme: str = "light",
    accent_color: str = "#957DAD",
    width_px: int = 800,
    height_px: int = 1000,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Scroll-Triggered Reveal visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Tutorial colors
    bg_color = "#E0BBE4" if color_scheme == "light" else "#1a1625"
    text_color = "#333333" if color_scheme == "light" else "#f0f0f0"
    card_bg = accent_color

    # === CSS ===
    css = f"""/* Scroll-Triggered Reveal — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --card-bg: {card_bg};
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    overflow-x: hidden;
}}

header {{
    height: 60vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 2rem;
}}

h1 {{
    font-size: 2.5rem;
    margin-bottom: 1rem;
}}

p {{
    font-size: 1.2rem;
    opacity: 0.8;
}}

.content-wrapper {{
    width: 100%;
    max-width: {width_px}px;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-bottom: 100px;
}}

/* --- Core Animation Logic --- */

/* Initial state (hidden and offset) */
.fade-in {{
    background: var(--card-bg);
    width: 100%;
    max-width: 400px;
    height: 300px;
    margin-bottom: 100px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-size: 2rem;
    font-weight: bold;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    
    /* Animation properties matching the tutorial */
    opacity: 0;
    transform: translateY(40%);
    transition: all 1s ease-out;
}}

/* Final state (visible and in position) */
.fade-in.active {{
    opacity: 1;
    transform: translateY(0);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </header>
    
    <div class="content-wrapper">
        <!-- These elements will be observed by JS -->
        <div class="fade-in">1</div>
        <div class="fade-in">2</div>
        <div class="fade-in">3</div>
        <div class="fade-in">4</div>
        <div class="fade-in">5</div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Scroll-Triggered Reveal Interaction
document.addEventListener('DOMContentLoaded', () => {{
    
    // Select all elements that need to be animated
    const elements = document.querySelectorAll('.fade-in');

    // Configure the observer
    const options = {{
        root: null,           // Use the viewport as the bounding box
        rootMargin: '0px',    // Explicitly set to 0px (note: '0' without units can cause errors here)
        threshold: 0.4        // Trigger when 40% of the element is visible
    }};

    // Create the observer callback function
    const cb = (entries, observer) => {{
        entries.forEach(entry => {{
            // Check if the element has crossed the threshold into view
            if (entry.isIntersecting) {{
                // Add the class that triggers the CSS transition
                entry.target.classList.add('active');
                
                // Optional enhancement: stop observing once it has animated in
                // to prevent it from animating out/in repeatedly if scrolling up and down.
                // observer.unobserve(entry.target); 
            }}
        }});
    }};

    // Instantiate the IntersectionObserver
    let observer = new IntersectionObserver(cb, options);

    // Register each element with the observer
    elements.forEach(el => {{
        observer.observe(el);
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
