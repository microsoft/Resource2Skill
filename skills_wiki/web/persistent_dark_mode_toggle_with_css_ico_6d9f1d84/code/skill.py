def create_component(
    output_dir: str,
    title_text: str = "Some random website",
    body_text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quidem, beatae voluptates iure iste eveniet, molestias rerum dicta accusantium dolore libero laboriosam aspernatur!",
    color_scheme: str = "light",       # "dark" or "light" - dictates fallback if no localStorage is set
    accent_color: str = "#0071ff",     # CSS hex color for accent/buttons
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Persistent Dark Mode Toggle effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Note: color_scheme parameter dictates the *initial default* if local storage is empty.
    # The actual implementation relies entirely on CSS variables.
    default_state = "active" if color_scheme == "dark" else "null"

    # === CSS ===
    css = f"""/* Persistent Dark Mode Toggle */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

/* Light Mode Variables (Default) */
:root {{
    --base-color: #ffffff;
    --base-variant: #e8e9ed;
    --text-color: #111528;
    --secondary-text: #232738;
    --primary-color: #3a435d;
    --accent-color: {accent_color};
    --button-text: #ffffff;
}}

/* Dark Mode Variables (Applied via class) */
.darkmode {{
    --base-color: #070b1d;
    --base-variant: #101425;
    --text-color: #ffffff;
    --secondary-text: #a4a5b8;
    --primary-color: #e8e9ed;
    --accent-color: {accent_color};
    --button-text: #ffffff;
}}

body {{
    font-family: 'Poppins', -apple-system, sans-serif;
    background-color: var(--base-color);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    /* Added transition for a premium smooth color swap */
    transition: background-color 0.3s ease, color 0.3s ease;
}}

.container {{
    width: 100%;
    max-width: {width_px}px;
    padding: 40px;
}}

header {{
    margin-bottom: 30px;
}}

h1 {{
    font-size: 2.5rem;
    margin-bottom: 15px;
}}

p {{
    font-size: 1.1rem;
    line-height: 1.6;
    color: var(--secondary-text);
    margin-bottom: 30px;
    max-width: 600px;
}}

.cta-button {{
    background-color: var(--accent-color);
    color: var(--button-text);
    border: none;
    padding: 12px 24px;
    font-size: 1rem;
    font-weight: 600;
    border-radius: 6px;
    cursor: pointer;
    transition: opacity 0.2s;
}}

.cta-button:hover {{
    opacity: 0.9;
}}

/* === Theme Switch Button Styles === */
#theme-switch {{
    height: 50px;
    width: 50px;
    padding: 0;
    border-radius: 50%;
    background-color: var(--base-variant);
    border: none;
    display: flex;
    justify-content: center;
    align-items: center;
    position: fixed;
    top: 20px;
    right: 20px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}}

#theme-switch svg {{
    fill: var(--primary-color);
    transition: fill 0.3s ease;
}}

/* Icon Swapping Logic */
/* 1. Light Mode (Default): Hide the second child (Sun) */
#theme-switch svg:last-child {{
    display: none;
}}

/* 2. Dark Mode: Hide the first child (Moon), Show the second child (Sun) */
.darkmode #theme-switch svg:first-child {{
    display: none;
}}

.darkmode #theme-switch svg:last-child {{
    display: block;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dark Mode Toggle</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <!-- Floating Theme Switch -->
    <button id="theme-switch" aria-label="Toggle Dark Mode">
        <!-- Moon Icon (First Child) -->
        <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px">
            <path d="M0 0h24v24H0z" fill="none"/>
            <path d="M12 3c-4.97 0-9 4.03-9 9s4.03 9 9 9 9-4.03 9-9c0-.46-.04-.92-.1-1.36-.98 1.37-2.58 2.26-4.38 2.26-2.98 0-5.4-2.42-5.4-5.4 0-1.81.89-3.42 2.26-4.38C12.92 3.04 12.46 3 12 3zm0 16c-3.86 0-7-3.14-7-7s3.14-7 7-7c.19 0 .38.01.57.04-1.56 1.34-2.57 3.33-2.57 5.56 0 3.86 3.14 7 7 7 2.23 0 4.22-1.01 5.56-2.57-.42.23-.9.37-1.4.45-.63.1-1.28.12-1.92.05-3.03-.31-5.5-2.61-5.96-5.61-.25-1.63.1-3.21.94-4.52C16.89 5.86 18.66 4.67 20.73 4.1 19.34 3.42 17.75 3 16 3c-4.97 0-9 4.03-9 9s4.03 9 9 9c1.75 0 3.34-.42 4.73-1.1-.57-2.07-1.76-3.84-3.33-5.23C15.21 17.65 13.62 18.66 12 19z" fill="currentColor"/>
            <path d="M12 21c4.97 0 9-4.03 9-9 0-.46-.04-.92-.1-1.36-.98 1.37-2.58 2.26-4.38 2.26-2.98 0-5.4-2.42-5.4-5.4 0-1.81.89-3.42 2.26-4.38.19.03.38.04.57.04 3.86 0 7 3.14 7 7s-3.14 7-7 7-7-3.14-7-7 3.14-7 7-7z" opacity=".3"/>
        </svg>
        <!-- Sun Icon (Last Child) -->
        <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px">
            <path d="M0 0h24v24H0z" fill="none"/>
            <path d="M6.76 4.84l-1.8-1.79-1.41 1.41 1.79 1.79 1.42-1.41zM4 10.5H1v2h3v-2zm9-9.95h-2V3.5h2V.55zm7.45 3.91l-1.41-1.41-1.79 1.79 1.41 1.41 1.79-1.79zm-3.21 13.7l1.79 1.8 1.41-1.41-1.8-1.79-1.4 1.4zM20 10.5v2h3v-2h-3zm-8-5c-3.31 0-6 2.69-6 6s2.69 6 6 6 6-2.69 6-6-2.69-6-6-6zm-1 16.95h2V19.5h-2v2.95zm-7.45-3.91l1.41 1.41 1.79-1.8-1.41-1.41-1.79 1.8z"/>
        </svg>
    </button>

    <div class="container">
        <header>
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <button class="cta-button">GO PREMIUM</button>
        </header>
    </div>

    <script>
        // Provide the injected configuration
        const CONFIG_DEFAULT_STATE = "{default_state}";
    </script>
    <script src="script.js" defer></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Dark Mode Logic with LocalStorage persistence

document.addEventListener('DOMContentLoaded', () => {{
    // 1. Get current theme from local storage
    let darkmode = localStorage.getItem('darkmode');
    const themeSwitch = document.getElementById('theme-switch');

    // 2. Define enablement/disablement functions
    const enableDarkmode = () => {{
        document.body.classList.add('darkmode');
        localStorage.setItem('darkmode', 'active');
    }};

    const disableDarkmode = () => {{
        document.body.classList.remove('darkmode');
        localStorage.setItem('darkmode', 'null');
    }};

    // 3. Fallback logic: If local storage is entirely empty, use the python parameter default
    if (darkmode === null) {{
        darkmode = CONFIG_DEFAULT_STATE; 
    }}

    // 4. Initial load check
    if (darkmode === 'active') {{
        enableDarkmode();
    }}

    // 5. Button click listener
    themeSwitch.addEventListener('click', () => {{
        // Re-evaluate the local storage state inside the listener
        darkmode = localStorage.getItem('darkmode');

        if (darkmode !== 'active') {{
            enableDarkmode();
        }} else {{
            disableDarkmode();
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
