def create_component(
    output_dir: str,
    title_text: str = "Design System Tokens",
    body_text: str = "This component demonstrates a robust CSS variable architecture, modern reset, and utility-class-driven layout derived from professional frontend practices.",
    color_scheme: str = "dark",
    accent_color: str = "hsl(12, 88%, 59%)",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Creates a web component demonstrating the Scalable CSS Token Architecture.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Dynamic Theme Configuration based on Python inputs
    if color_scheme == "dark":
        neutral_900 = "hsl(228, 39%, 23%)"
        neutral_100 = "hsl(0, 0%, 100%)"
        bg_color = "var(--clr-neutral-900)"
        text_color = "var(--clr-neutral-100)"
        card_bg = "hsl(233, 12%, 13%)"
    else:
        neutral_900 = "hsl(233, 12%, 13%)"
        neutral_100 = "hsl(0, 0%, 100%)"
        bg_color = "var(--clr-neutral-100)"
        text_color = "var(--clr-neutral-900)"
        card_bg = "hsl(0, 0%, 98%)"

    css = f"""/* ==========================================================================
   1. MODERN CSS RESET
   ========================================================================== */
*, *::before, *::after {{
    box-sizing: border-box;
}}

* {{
    margin: 0;
    padding: 0;
    font: inherit;
}}

html:focus-within {{
    scroll-behavior: smooth;
}}

html, body {{
    height: 100%;
}}

body {{
    text-rendering: optimizeSpeed;
    line-height: 1.5;
}}

img, picture, svg {{
    max-width: 100%;
    display: block;
}}

/* Remove list styles on ul, ol elements with a list role */
ul[role='list'], ol[role='list'] {{
    list-style: none;
}}

/* Accessibility: Remove all animations, transitions and smooth scroll for people that prefer not to see them */
@media (prefers-reduced-motion: reduce) {{
  html:focus-within {{
   scroll-behavior: auto;
  }}
  *, *::before, *::after {{
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }}
}}

/* ==========================================================================
   2. CSS DESIGN TOKENS (VARIABLES)
   ========================================================================== */
:root {{
    /* Colors */
    --clr-accent-400: {accent_color};
    --clr-primary-400: hsl(228, 39%, 23%);
    --clr-neutral-900: {neutral_900};
    --clr-neutral-100: {neutral_100};
    --clr-card-bg: {card_bg};

    /* Typography Hierarchy Setup */
    --ff-primary: 'Inter', sans-serif;
    --ff-body: var(--ff-primary);
    --ff-heading: var(--ff-primary);

    --fw-regular: 400;
    --fw-semi-bold: 500;
    --fw-bold: 700;

    /* Responsive Font Sizes (Mobile First) */
    --fs-400: 0.875rem;     /* 14px */
    --fs-500: 1rem;         /* 16px */
    --fs-600: 1.5rem;       /* 24px */
    --fs-700: 2rem;         /* 32px */
    
    /* Mapping semantic sizes to scales */
    --fs-body: var(--fs-400);
    --fs-primary-heading: var(--fs-700);
    --fs-secondary-heading: var(--fs-600);
    --fs-button: var(--fs-500);
}}

/* Scale up font sizes at larger viewports (Desktop) */
@media (min-width: 50em) {{
    :root {{
        --fs-body: var(--fs-500);
        --fs-primary-heading: var(--fs-700);
        --fs-secondary-heading: var(--fs-600);
        --fs-button: var(--fs-400);
        
        /* The actual scale shifts up */
        --fs-400: 1rem;       /* 16px */
        --fs-500: 1.125rem;   /* 18px */
        --fs-600: 2rem;       /* 32px */
        --fs-700: 3.5rem;     /* 56px */
    }}
}}

/* ==========================================================================
   3. UTILITY CLASSES
   ========================================================================== */
/* Typography */
.ff-primary {{ font-family: var(--ff-primary); }}
.ff-body {{ font-family: var(--ff-body); }}
.ff-heading {{ font-family: var(--ff-heading); }}

.fw-regular {{ font-weight: var(--fw-regular); }}
.fw-semi-bold {{ font-weight: var(--fw-semi-bold); }}
.fw-bold {{ font-weight: var(--fw-bold); }}

.fs-primary-heading {{ font-size: var(--fs-primary-heading); line-height: 1.1; }}
.fs-secondary-heading {{ font-size: var(--fs-secondary-heading); line-height: 1.2; }}
.fs-body {{ font-size: var(--fs-body); }}

/* Colors */
.text-primary-400 {{ color: var(--clr-primary-400); }}
.text-accent-400 {{ color: var(--clr-accent-400); }}
.text-neutral-100 {{ color: var(--clr-neutral-100); }}
.text-neutral-900 {{ color: var(--clr-neutral-900); }}

.bg-primary-400 {{ background-color: var(--clr-primary-400); }}
.bg-accent-400 {{ background-color: var(--clr-accent-400); }}
.bg-neutral-100 {{ background-color: var(--clr-neutral-100); }}
.bg-neutral-900 {{ background-color: var(--clr-neutral-900); }}

/* Layout */
.container {{
    max-width: {width_px}px;
    min-height: {height_px}px;
    margin: 0 auto;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
}}

.grid-flow {{
    display: grid;
    gap: 2rem;
}}

.card {{
    background-color: var(--clr-card-bg);
    padding: 2rem;
    border-radius: 0.5rem;
    border-left: 6px solid var(--clr-accent-400);
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}}

/* General Page Styling */
body {{
    background-color: {bg_color};
    color: {text_color};
    font-family: var(--ff-body);
    font-size: var(--fs-body);
    font-weight: var(--fw-regular);
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <!-- Importing System Font -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="container">
        
        <div class="grid-flow card">
            <div>
                <p class="text-accent-400 fw-bold">DESIGN SYSTEM ARCHITECTURE</p>
                <h1 class="fs-primary-heading fw-bold ff-heading">{title_text}</h1>
            </div>
            
            <p class="fs-body fw-regular">{body_text}</p>
            
            <div>
                <h2 class="fs-secondary-heading fw-semi-bold">Typography Scaling Demo</h2>
                <ul role="list" class="grid-flow" style="gap: 1rem; margin-top: 1rem;">
                    <li class="fs-400"><strong>Level 400:</strong> Responsive base text element.</li>
                    <li class="fs-500"><strong>Level 500:</strong> Slightly larger emphasis text.</li>
                    <li class="fs-600 fw-semi-bold">Level 600: Secondary Headings</li>
                </ul>
            </div>

            <div style="display: flex; gap: 1rem; margin-top: 1rem;">
                <button class="bg-accent-400 text-neutral-100 fw-bold" style="border:none; padding: 0.75rem 1.5rem; border-radius: 100vmax; cursor: pointer;">
                    Primary Action
                </button>
                <button class="bg-neutral-900 text-neutral-100 fw-bold" style="border:none; padding: 0.75rem 1.5rem; border-radius: 100vmax; cursor: pointer;">
                    Secondary Action
                </button>
            </div>
        </div>

    </main>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// No JavaScript required for this purely CSS-driven architecture pattern.
// The fluid typography is handled via CSS custom properties and media queries.
console.log('Design tokens initialized correctly.');
"""

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
