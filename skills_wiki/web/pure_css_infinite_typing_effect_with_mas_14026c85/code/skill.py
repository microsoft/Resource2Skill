def create_component(
    output_dir: str,
    title_text: str = "I'm a",
    words_list: list = None,
    color_scheme: str = "dark",
    accent_color: str = "#ff7f50",
    width_px: int = 1000,
    height_px: int = 600,
    **kwargs,
) -> dict:
    import os

    # Default word list if none provided
    if not words_list:
        words_list = ["Youtuber", "Blogger", "Developer", "Designer", "Gamer"]

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#2f3542" # Muted dark slate
        text_color = "#ffffff"
    else:
        bg_color = "#f4f6f8"
        text_color = "#2d3436"

    # --- Core Algorithmic Keyframe Generation ---
    # To make this pure CSS effect parameterizable, we must dynamically calculate 
    # the exact percentages for the keyframes based on the number of words.
    n_words = len(words_list)
    cycle_pct = 100 / n_words
    duration = n_words * 4  # 4 seconds allocated per word

    # Dynamic step count based on the longest word ensures smooth typing chunks
    max_len = max([len(w) for w in words_list])
    steps_count = max(10, max_len + 2)

    width_0_pcts = []
    width_100_pcts = [0.0]
    content_keyframes = ""

    for i, word in enumerate(words_list):
        start = i * cycle_pct
        
        # Timeline logic for a single word cycle:
        # Phase 1: Hold empty (mask full width)
        # Phase 2: Type out (mask shrinks to 0)
        # Phase 3: Hold text (mask stays 0)
        # Phase 4: Delete back (mask grows to full width)
        
        width_100_pcts.append(start + cycle_pct * 0.25)
        width_0_pcts.append(start + cycle_pct * 0.50)
        width_0_pcts.append(start + cycle_pct * 0.75)
        width_100_pcts.append(start + cycle_pct)

        # Content swap happens exactly at the start of its cycle
        content_keyframes += f"    {start:g}% {{ content: '{word}'; }}\n"

    # Format percentage lists for CSS selectors
    width_100_pcts = sorted(list(set(width_100_pcts)))
    width_0_pcts = sorted(list(set(width_0_pcts)))
    w0_selectors = ", ".join([f"{p:g}%" for p in width_0_pcts])
    w100_selectors = ", ".join([f"{p:g}%" for p in width_100_pcts])

    # === CSS ===
    css = f"""/* Pure CSS Typing Effect */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --duration: {duration}s;
    --steps: {steps_count};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Montserrat', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.container {{
    width: var(--width);
    height: var(--height);
    display: flex;
    align-items: center;
    justify-content: center;
}}

.typing-wrapper {{
    font-size: 2.5rem;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
}}

.prefix {{
    margin-right: 12px;
}}

/* The parent span adapts to the width of its ::before content automatically */
.animated-text {{
    position: relative;
    display: inline-block;
}}

/* ::before holds the actual changing text */
.animated-text::before {{
    content: "{words_list[0]}"; 
    color: var(--accent);
    animation: words var(--duration) infinite;
}}

/* ::after acts as a mask block covering the text, shrinking/growing to simulate typing */
.animated-text::after {{
    content: "";
    position: absolute;
    right: -8px; /* Slight overhang for the cursor */
    top: 0;
    height: 100%;
    width: calc(100% + 8px);
    
    /* CRITICAL: Background must perfectly match the container background */
    background-color: var(--bg); 
    
    /* The left edge of the mask acts as the cursor */
    border-left: 3px solid var(--accent);
    
    animation:
        cursor 0.8s infinite,
        typing var(--duration) steps(var(--steps)) infinite;
}}

/* Blinking cursor animation */
@keyframes cursor {{
    0%, 100% {{ border-left-color: transparent; }}
    50% {{ border-left-color: var(--accent); }}
}}

/* Word swapping animation */
@keyframes words {{
{content_keyframes}
}}

/* Typing (mask width) animation */
@keyframes typing {{
    {w0_selectors} {{
        width: 0;
    }}
    {w100_selectors} {{
        width: calc(100% + 8px);
    }}
}}

/* Responsive Scaling */
@media (max-width: 768px) {{
    .typing-wrapper {{
        font-size: 1.8rem;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CSS Typing Animation</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="typing-wrapper">
            <span class="prefix">{title_text}</span>
            <span class="animated-text"></span>
        </div>
    </div>
</body>
</html>"""

    # === Write files ===
    files = []
    for fname, content in [("index.html", html), ("style.css", css)]:
        path = os.path.join(output_dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        files.append(path)

    return {
        "html": html,
        "css": css,
        "js": "", # No JavaScript required for this effect
        "files": files,
    }
