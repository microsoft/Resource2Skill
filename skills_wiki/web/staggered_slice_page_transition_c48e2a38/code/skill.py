def create_component(
    output_dir: str,
    title_text: str = "Explore our Services",
    body_text: str = "An Ongoing Experience",
    color_scheme: str = "light",        
    accent_color: str = "#111111",     
    width_px: int = 1000,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Staggered Slice Page Transition.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
        card_bg = "#1a2235"
        alt_accent = "#ffffff"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        card_bg = "#ffffff"
        alt_accent = "#000000"

    # === CSS ===
    css = f"""/* Staggered Slice Page Transition — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --card-bg: {card_bg};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #000; /* Outer background */
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

/* Component constraints */
.wrapper {{
    width: var(--width);
    height: var(--height);
    background: var(--bg);
    color: var(--text);
    position: relative;
    overflow: hidden;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    border-radius: 8px;
}}

/* Transition Slice Overlay */
.transition {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 9999;
    display: flex;
    pointer-events: none;
    list-style: none;
}}

.transition li {{
    flex: 1;
    background: var(--accent);
    transform: scaleY(0);
    transform-origin: bottom left;
    will-change: transform;
}}

/* Page Layouts */
.page {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: none; /* Hidden by default */
    padding: 40px;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
}}

.page.active {{
    display: flex; /* Only active page is shown */
}}

.content-left {{
    flex: 1;
    padding-right: 40px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}}

h1 {{
    font-size: 3.5rem;
    line-height: 1.1;
    font-weight: 700;
    margin-bottom: 16px;
    letter-spacing: -0.03em;
}}

p {{
    font-size: 1.25rem;
    opacity: 0.8;
    margin-bottom: 40px;
}}

.btn {{
    align-self: flex-start;
    padding: 16px 32px;
    background: var(--card-bg);
    color: var(--text);
    border: 2px solid var(--text);
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    text-transform: uppercase;
    letter-spacing: 1px;
}}

.btn:hover {{
    background: var(--text);
    color: var(--bg);
}}

/* Image Reveal Element */
.image-wrapper {{
    width: 45%;
    height: 80%;
    position: relative;
    border-radius: 4px;
    overflow: hidden;
}}

.hero-image {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    /* Hidden state for animation */
    clip-path: polygon(0% 100%, 100% 100%, 100% 100%, 0% 100%);
    will-change: clip-path;
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
    <!-- GSAP Core -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
</head>
<body>

    <div class="wrapper">
        
        <!-- Slices Overlay -->
        <ul class="transition">
            <li></li><li></li><li></li><li></li><li></li>
        </ul>

        <!-- Virtual Page 1 -->
        <div id="home-page" class="page active">
            <div class="content-left">
                <h1>{body_text}</h1>
                <p>Welcome to our digital space. We craft seamless transitions.</p>
                <button class="btn" onclick="transitionTo('services-page')">Take me there</button>
            </div>
            <div class="image-wrapper">
                <!-- Initial image is visible without clip-path reset on first load -->
                <img class="hero-image" src="https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?auto=format&fit=crop&w=800&q=80" alt="Interior Architecture" style="clip-path: polygon(0% 0%, 100% 0%, 100% 100%, 0% 100%);">
            </div>
        </div>

        <!-- Virtual Page 2 -->
        <div id="services-page" class="page">
            <div class="content-left">
                <h1>{title_text}</h1>
                <p>Discover a new dimension of web interactivity.</p>
                <button class="btn" onclick="transitionTo('home-page')">Take me home</button>
            </div>
            <div class="image-wrapper">
                <img class="hero-image" src="https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=800&q=80" alt="Modern Living Space">
            </div>
        </div>

    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Staggered Slice Page Transition Logic
let isAnimating = false;

function transitionTo(targetPageId) {{
    // Prevent overlapping transitions
    if (isAnimating) return;
    isAnimating = true;

    // Create a GSAP Timeline
    const tl = gsap.timeline({{
        onComplete: () => {{
            isAnimating = false;
        }}
    }});

    // Phase 1: Slices slide UP to cover the screen
    tl.set('.transition li', {{ transformOrigin: "bottom left" }})
      .to('.transition li', {{
          duration: 0.5,
          scaleY: 1,
          stagger: 0.1,
          ease: "power2.inOut"
      }})
      
      // Phase 2: Swap the content while the screen is completely covered
      .call(() => {{
          // Hide all pages
          document.querySelectorAll('.page').forEach(page => {{
              page.classList.remove('active');
          }});
          
          // Show the target page
          document.getElementById(targetPageId).classList.add('active');

          // Reset the clip-path of the image on the newly active page so it can be animated in
          const newImg = document.querySelector('#' + targetPageId + ' .hero-image');
          if(newImg) {{
              gsap.set(newImg, {{ clipPath: "polygon(0% 100%, 100% 100%, 100% 100%, 0% 100%)" }});
          }}
      }})
      
      // Phase 3: Slices slide UP to reveal the new screen
      .set('.transition li', {{ transformOrigin: "top left" }})
      .to('.transition li', {{
          duration: 0.5,
          scaleY: 0,
          stagger: 0.1,
          ease: "power2.inOut",
          delay: 0.1
      }});

    // Phase 4: Secondary animations on the new page (Image Unfurl)
    const activeImg = document.querySelector('#' + targetPageId + ' .hero-image');
    if (activeImg) {{
        tl.to(activeImg, {{
            clipPath: "polygon(0% 0%, 100% 0%, 100% 100%, 0% 100%)",
            duration: 1.2,
            ease: "power3.out"
        }}, "-=0.4"); // Offset to start slightly before the slices finish leaving
    }}
}}
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
