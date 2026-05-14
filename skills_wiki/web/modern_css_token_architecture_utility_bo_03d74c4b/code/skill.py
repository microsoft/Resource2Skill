def create_component(
    output_dir: str,
    title_text: str = "Design System Tokens",
    body_text: str = "This dashboard is built using the extracted CSS reset, custom properties, and utility class architecture.",
    color_scheme: str = "light",       
    accent_color: str = "hsl(12, 88%, 59%)", # The 'Bright Red' from the tutorial
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Modern CSS Token Architecture & Utility Boilerplate.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme based on inputs to simulate the token generation
    if color_scheme == "dark":
        bg_color = "hsl(228, 39%, 15%)"
        surface_color = "hsl(228, 39%, 23%)"
        text_primary = "hsl(0, 0%, 98%)"
        text_secondary = "hsl(227, 12%, 61%)"
    else:
        bg_color = "hsl(0, 0%, 98%)"
        surface_color = "hsl(0, 0%, 100%)"
        text_primary = "hsl(228, 39%, 23%)"
        text_secondary = "hsl(227, 12%, 61%)"

    # === CSS ===
    css = f"""/* 
  MODERN CSS ARCHITECTURE & RESET 
  Extracted from Frontend Mentor / Kevin Powell Tutorial
*/

/* --- CSS RESET --- */
*,
*::before,
*::after {{
  box-sizing: border-box;
}}

* {{
  margin: 0;
  padding: 0;
  font: inherit;
}}

ul[role='list'],
ol[role='list'] {{
  list-style: none;
}}

html:focus-within {{
  scroll-behavior: smooth;
}}

html,
body {{
  height: 100%;
}}

body {{
  text-rendering: optimizeSpeed;
  line-height: 1.5;
}}

a:not([class]) {{
  text-decoration-skip-ink: auto;
}}

img,
picture,
svg {{
  max-width: 100%;
  display: block;
}}

@media (prefers-reduced-motion: reduce) {{
  html:focus-within {{
    scroll-behavior: auto;
  }}
  *,
  *::before,
  *::after {{
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }}
}}

/* --- DESIGN TOKENS (CUSTOM PROPERTIES) --- */
:root {{
  /* Colors */
  --clr-accent-400: {accent_color};
  --clr-accent-300: hsl(12, 88%, 75%); /* Lighter variant */
  
  --clr-primary-400: {text_primary};
  --clr-neutral-900: {bg_color};
  --clr-neutral-100: {surface_color};
  --clr-text-muted: {text_secondary};

  /* Typography */
  --ff-primary: 'Be Vietnam Pro', sans-serif;
  --ff-body: var(--ff-primary);
  --ff-heading: var(--ff-primary);

  /* Font Weights */
  --fw-regular: 400;
  --fw-semi-bold: 500;
  --fw-bold: 700;

  /* Font Sizes (Fluid/Static Scale) */
  --fs-300: 0.8125rem; /* ~13px */
  --fs-400: 0.875rem;  /* ~14px */
  --fs-500: 0.9375rem; /* ~15px */
  --fs-600: 1.125rem;  /* ~18px */
  --fs-700: 1.875rem;  /* ~30px */
  --fs-800: 2.5rem;    /* ~40px */
  --fs-900: 3.5rem;    /* ~56px */
  
  /* Abstracted Typography Roles */
  --fs-body: var(--fs-400);
  --fs-nav: var(--fs-300);
  --fs-button: var(--fs-300);
  --fs-primary-heading: var(--fs-800);
  --fs-secondary-heading: var(--fs-700);
}}

/* Setup base body based on tokens */
body {{
  font-family: var(--ff-body);
  font-size: var(--fs-body);
  color: var(--clr-primary-400);
  background-color: var(--clr-neutral-900);
  display: flex;
  justify-content: center;
  align-items: center;
}}

.app-wrapper {{
  width: {width_px}px;
  height: {height_px}px;
  max-width: 100vw;
  max-height: 100vh;
  overflow-y: auto;
  background-color: var(--clr-neutral-100);
  box-shadow: 0 20px 40px rgba(0,0,0,0.1);
  padding: 3rem;
  border-radius: 1rem;
}}


/* --- UTILITY CLASSES --- */
.text-primary-400 {{ color: var(--clr-primary-400); }}
.text-accent-400 {{ color: var(--clr-accent-400); }}
.text-muted {{ color: var(--clr-text-muted); }}

.bg-primary-400 {{ background-color: var(--clr-primary-400); }}
.bg-accent-400 {{ background-color: var(--clr-accent-400); }}
.bg-neutral-900 {{ background-color: var(--clr-neutral-900); }}
.bg-neutral-100 {{ background-color: var(--clr-neutral-100); }}

.fw-regular {{ font-weight: var(--fw-regular); }}
.fw-semi-bold {{ font-weight: var(--fw-semi-bold); }}
.fw-bold {{ font-weight: var(--fw-bold); }}

.fs-primary-heading {{ font-size: var(--fs-primary-heading); line-height: 1.1; }}
.fs-secondary-heading {{ font-size: var(--fs-secondary-heading); line-height: 1.2; }}
.fs-300 {{ font-size: var(--fs-300); }}
.fs-400 {{ font-size: var(--fs-400); }}
.fs-500 {{ font-size: var(--fs-500); }}
.fs-600 {{ font-size: var(--fs-600); }}


/* --- COMPONENT STYLES (Built with utilities) --- */
.header {{
  margin-bottom: 3rem;
  border-bottom: 2px solid var(--clr-neutral-900);
  padding-bottom: 1.5rem;
}}

.grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}}

.card {{
  padding: 1.5rem;
  border-radius: 0.5rem;
  border: 1px solid var(--clr-text-muted);
  display: flex;
  flex-direction: column;
  gap: 1rem;
}}

.color-swatch {{
  height: 80px;
  border-radius: 0.25rem;
  display: flex;
  align-items: flex-end;
  padding: 0.5rem;
  font-size: var(--fs-300);
  font-weight: var(--fw-bold);
}}

/* Button built applying utility concepts */
.btn {{
  display: inline-flex;
  cursor: pointer;
  text-decoration: none;
  border: 0;
  border-radius: 100vw; /* Pill shape */
  padding: 0.75em 2em;
  font-family: var(--ff-primary);
  font-weight: var(--fw-bold);
  font-size: var(--fs-button);
  color: var(--clr-neutral-100);
  background-color: var(--clr-accent-400);
  transition: opacity 0.2s ease, transform 0.2s ease;
}}

.btn:hover, .btn:focus-visible {{
  opacity: 0.8;
  transform: translateY(-2px);
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
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="app-wrapper">
        <header class="header">
            <h1 class="fs-primary-heading fw-bold text-primary-400">{title_text}</h1>
            <p class="fs-500 text-muted" style="margin-top: 0.5rem;">{body_text}</p>
        </header>

        <div class="grid">
            <!-- Typography Module -->
            <div class="card bg-neutral-100">
                <h2 class="fs-secondary-heading fw-bold text-accent-400">Typography Scale</h2>
                <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                    <div class="fs-700 fw-bold">Heading 700</div>
                    <div class="fs-600 fw-semi-bold">Subheading 600</div>
                    <div class="fs-500 fw-regular">Large Body 500</div>
                    <div class="fs-400 fw-regular text-muted">Standard Body 400</div>
                    <div class="fs-300 fw-bold text-accent-400">Small Nav/Button 300</div>
                </div>
            </div>

            <!-- Color Palette Module -->
            <div class="card bg-neutral-100">
                <h2 class="fs-secondary-heading fw-bold text-primary-400">Color Palette</h2>
                <div class="grid" style="grid-template-columns: 1fr 1fr; gap: 0.5rem;">
                    <div class="color-swatch bg-accent-400" style="color: white;">Accent</div>
                    <div class="color-swatch bg-primary-400" style="color: white;">Primary</div>
                    <div class="color-swatch bg-neutral-900" style="color: white; border: 1px solid #ccc;">Neutral 900</div>
                    <div class="color-swatch bg-neutral-100 text-primary-400" style="border: 1px solid #ccc;">Neutral 100</div>
                </div>
            </div>

            <!-- UI Components Module -->
            <div class="card bg-neutral-100">
                <h2 class="fs-secondary-heading fw-bold text-primary-400">UI Composition</h2>
                <p class="text-muted fs-400">This card and button are built entirely by stacking utility classes on semantic HTML elements.</p>
                <div style="margin-top: auto; padding-top: 1rem;">
                    <button class="btn" id="interactive-btn">Interactive Button</button>
                </div>
            </div>
        </div>
    </main>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Architecture Demonstration
document.addEventListener('DOMContentLoaded', () => {{
    const btn = document.getElementById('interactive-btn');
    
    // Demonstrate interaction using CSS variables
    btn.addEventListener('click', () => {{
        const root = document.documentElement;
        
        // Randomly generate a new accent color to demonstrate token updating
        const hue = Math.floor(Math.random() * 360);
        const newAccent = `hsl(${{hue}}, 80%, 60%)`;
        
        // Updating the CSS variable updates all utility classes referencing it
        root.style.setProperty('--clr-accent-400', newAccent);
        
        btn.innerText = "Token Updated!";
        setTimeout(() => {{
            btn.innerText = "Interactive Button";
        }}, 1500);
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
