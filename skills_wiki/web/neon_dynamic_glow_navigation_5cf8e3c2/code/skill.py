def create_component(
    output_dir: str,
    title_text: str = "Neon Glowing Navigation",
    body_text: str = "Hover over the icons or use the keyboard to navigate.",
    color_scheme: str = "dark",
    accent_color: str = "#00f3ff",
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Neon Dynamic Glow Navigation visual effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme definitions
    if color_scheme == "dark":
        bg_color = "#12141c"
        nav_bg = "#222635"
        text_color = "#ffffff"
        text_muted = "rgba(255, 255, 255, 0.4)"
        icon_active_color = "#ffffff"
    else:
        bg_color = "#eef1f6"
        nav_bg = "#ffffff"
        text_color = "#1a1a2e"
        text_muted = "rgba(0, 0, 0, 0.3)"
        icon_active_color = "#1a1a2e"

    # Define the neon color palette for the icons
    palette = [
        accent_color,
        "#ff00c8", # Neon Pink
        "#00d1ff", # Bright Blue
        "#ffa100", # Neon Orange
        "#ff0051"  # Magenta Red
    ]

    # === CSS ===
    css = f"""/* Neon Glowing Navigation - generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --nav-bg: {nav_bg};
    --text: {text_color};
    --text-muted: {text_muted};
    --icon-active: {icon_active_color};
    --width: {width_px}px;
    --height: {height_px}px;
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

.container {{
    max-width: var(--width);
    min-height: var(--height);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 60px;
    padding: 2rem;
}}

.header {{
    text-align: center;
}}

.title {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    letter-spacing: -0.03em;
}}

.body-text {{
    font-size: 1.1rem;
    color: var(--text-muted);
    max-width: 500px;
    line-height: 1.5;
}}

/* Navigation Container */
.navbar-container {{
    background: var(--nav-bg);
    border-radius: 24px;
    padding: 0 16px;
    box-shadow: 
        0 20px 40px rgba(0, 0, 0, 0.15), 
        inset 0 1px 3px rgba(255, 255, 255, 0.05);
    position: relative;
}}

.nav-list {{
    display: flex;
    list-style: none;
    position: relative;
    gap: 8px;
}}

/* Individual Nav Items */
.nav-item {{
    width: 72px;
    height: 72px;
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 2; /* Sits above the glowing indicator */
    cursor: pointer;
    color: var(--text-muted);
    font-size: 1.6rem;
    transition: color 0.3s ease, text-shadow 0.3s ease;
    outline: none;
}}

.nav-item:hover, 
.nav-item.active,
.nav-item:focus-visible {{
    color: var(--icon-active);
    /* Internal glow on the icon itself */
    text-shadow: 0 0 15px var(--clr), 0 0 30px var(--clr);
}}

/* The glowing indicator that slides behind the active item */
.indicator {{
    position: absolute;
    top: -8px; /* Protrude slightly above the navbar */
    left: 0;
    width: 72px;
    height: 60px;
    background-color: var(--clr);
    border-radius: 14px;
    z-index: 1; /* Sits behind the icons */
    opacity: 0;
    
    /* 
       The inset shadow with negative Y (-30px) draws a shadow from the bottom up.
       Using the navbar background color perfectly masks the neon block, 
       creating a smooth, animatable gradient fade-out effect.
    */
    box-shadow: 
        0 -6px 20px var(--clr), 
        inset 0 -30px 25px var(--nav-bg);
        
    /* Smooth, bouncy transition for position and color snapping */
    transition: 
        transform 0.4s cubic-bezier(0.5, 1.2, 0.4, 1), 
        background-color 0.4s ease, 
        box-shadow 0.4s ease,
        width 0.4s ease,
        opacity 0.3s ease;
        
    will-change: transform, background-color, box-shadow;
}}

/* Visibility toggles */
.nav-list:hover .indicator,
.nav-list:focus-within .indicator,
.indicator.has-active {{
    opacity: 0.9;
}}

/* Bright white glowing top edge of the indicator */
.indicator::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 15%;
    width: 70%;
    height: 4px;
    background: #ffffff;
    border-radius: 4px;
    box-shadow: 0 0 12px #ffffff;
}}

/* Subtle pulse animation on the active indicator */
@keyframes pulseGlow {{
    0% {{ filter: brightness(1); }}
    50% {{ filter: brightness(1.15); }}
    100% {{ filter: brightness(1); }}
}}

.indicator.has-active {{
    animation: pulseGlow 2s infinite ease-in-out;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <!-- FontAwesome for Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
        
        <nav class="navbar-container" aria-label="Main Navigation">
            <ul class="nav-list" role="tablist">
                <div class="indicator" aria-hidden="true"></div>
                
                <!-- Nav Items containing dynamic CSS variables for colors -->
                <li class="nav-item" role="tab" aria-selected="false" tabindex="0" aria-label="Home" style="--clr: {palette[0]};">
                    <i class="fas fa-home"></i>
                </li>
                <li class="nav-item" role="tab" aria-selected="false" tabindex="0" aria-label="Profile" style="--clr: {palette[1]};">
                    <i class="fas fa-user"></i>
                </li>
                <li class="nav-item" role="tab" aria-selected="false" tabindex="0" aria-label="Create" style="--clr: {palette[2]};">
                    <i class="fas fa-plus"></i>
                </li>
                <li class="nav-item" role="tab" aria-selected="false" tabindex="0" aria-label="Settings" style="--clr: {palette[3]};">
                    <i class="fas fa-cog"></i>
                </li>
                <li class="nav-item" role="tab" aria-selected="false" tabindex="0" aria-label="Messages" style="--clr: {palette[4]};">
                    <i class="fas fa-comment"></i>
                </li>
            </ul>
        </nav>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Neon Glowing Navigation - interactive behavior

document.addEventListener('DOMContentLoaded', () => {{
    const items = document.querySelectorAll('.nav-item');
    const indicator = document.querySelector('.indicator');

    // Function to calculate geometry and update the glowing indicator
    function setActive(activeItem) {{
        // Reset all items
        items.forEach(item => {{
            item.classList.remove('active');
            item.setAttribute('aria-selected', 'false');
        }});
        
        // Set current item
        activeItem.classList.add('active');
        activeItem.setAttribute('aria-selected', 'true');
        
        // Calculate position and width relative to the ul.nav-list container
        const left = activeItem.offsetLeft;
        const width = activeItem.offsetWidth;
        const clr = activeItem.style.getPropertyValue('--clr').trim();
        
        // Update indicator styles via DOM transform and Custom Properties
        indicator.style.transform = `translateX(${{left}}px)`;
        indicator.style.width = `${{width}}px`;
        indicator.style.setProperty('--clr', clr);
        indicator.classList.add('has-active');
    }}

    // Bind event listeners to all navigation items
    items.forEach(item => {{
        // Pointer hover interaction
        item.addEventListener('mouseenter', () => setActive(item));
        
        // Keyboard focus interaction (Accessibility)
        item.addEventListener('focus', () => setActive(item));
        
        // Keyboard selection execution (Space/Enter)
        item.addEventListener('keydown', (e) => {{
            if (e.key === 'Enter' || e.key === ' ') {{
                e.preventDefault();
                setActive(item);
            }}
        }});
    }});

    // Initialize the first item as active on load.
    // Use a small timeout to ensure the browser has finished rendering layout 
    // geometries (offsetLeft) before performing the calculation.
    setTimeout(() => {{
        if (items.length > 0) {{
            setActive(items[0]);
            
            // Re-calculate on window resize to keep the indicator perfectly aligned
            window.addEventListener('resize', () => {{
                const currentActive = document.querySelector('.nav-item.active') || items[0];
                setActive(currentActive);
            }});
        }}
    }}, 50);
}});
"""

    # Write files to disk
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
