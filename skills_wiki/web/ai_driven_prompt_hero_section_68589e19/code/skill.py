def create_component(
    output_dir: str,
    title_text: str = "What can I help you build?",
    body_text: str = "Start by describing your project or select a suggestion.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#8b5cf6",     # Vibrant purple/violet for AI feel
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the AI Prompt Hero Interface.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg = "#0e1116"
        text = "#f8fafc"
        text_muted = "#94a3b8"
        input_bg = "#1e293b"
        border = "#334155"
        chip_bg = "rgba(255, 255, 255, 0.03)"
        chip_hover = "rgba(255, 255, 255, 0.08)"
    else:
        bg = "#ffffff"
        text = "#0f172a"
        text_muted = "#64748b"
        input_bg = "#ffffff"
        border = "#e2e8f0"
        chip_bg = "#f8fafc"
        chip_hover = "#f1f5f9"

    # === CSS ===
    css = f"""/* AI Prompt Hero Interface — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg};
    --text: {text};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --input-bg: {input_bg};
    --border: {border};
    --chip-bg: {chip_bg};
    --chip-hover: {chip_hover};
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

.hero {{
    width: var(--width);
    height: var(--height);
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
}}

/* Ambient gradient glow behind the input */
.ambient-glow {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -40%);
    width: 600px;
    height: 400px;
    background: radial-gradient(circle, color-mix(in srgb, var(--accent) 15%, transparent) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
}}

.container {{
    position: relative;
    z-index: 1;
    width: 100%;
    max-width: 800px;
    padding: 0 24px;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
}}

h1 {{
    font-size: clamp(2.5rem, 5vw, 4rem);
    font-weight: 600;
    letter-spacing: -0.03em;
    margin-bottom: 1rem;
    line-height: 1.1;
}}

.subtitle {{
    font-size: 1.125rem;
    color: var(--text-muted);
    margin-bottom: 3rem;
    max-width: 600px;
}}

.prompt-container {{
    width: 100%;
    max-width: 720px;
}}

/* Input wrapper handles the shadow and focus states */
.input-wrapper {{
    position: relative;
    width: 100%;
    margin-bottom: 1.5rem;
    border-radius: 24px;
    background: var(--input-bg);
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.04), 0 1px 3px rgba(0,0,0,0.08);
    border: 1px solid var(--border);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}}

/* Elevated glowing state */
.input-wrapper:focus-within {{
    border-color: var(--accent);
    box-shadow: 
        0 0 0 4px color-mix(in srgb, var(--accent) 20%, transparent), 
        0 12px 32px color-mix(in srgb, var(--accent) 10%, transparent),
        0 4px 12px rgba(0, 0, 0, 0.1);
    transform: translateY(-2px);
}}

input {{
    width: 100%;
    height: 64px;
    padding: 0 64px 0 24px;
    border: none;
    background: transparent;
    color: var(--text);
    font-size: 1.125rem;
    font-family: inherit;
    outline: none;
}}

input::placeholder {{
    color: var(--text-muted);
    opacity: 0.8;
}}

#submit-btn {{
    position: absolute;
    right: 12px;
    top: 50%;
    transform: translateY(-50%);
    width: 40px;
    height: 40px;
    border-radius: 14px;
    background: var(--accent);
    color: white;
    border: none;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}}

#submit-btn:hover:not(:disabled) {{
    filter: brightness(1.1);
    transform: translateY(-50%) scale(1.05);
}}

#submit-btn:active:not(:disabled) {{
    transform: translateY(-50%) scale(0.95);
}}

#submit-btn:disabled {{
    opacity: 0.7;
    cursor: not-allowed;
}}

/* Suggestion Chips */
.suggestions {{
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    justify-content: center;
}}

.chip {{
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 18px;
    border-radius: 100px;
    border: 1px solid var(--border);
    background: var(--chip-bg);
    color: var(--text-muted);
    font-size: 0.9rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
}}

.chip svg {{
    opacity: 0.7;
}}

.chip:hover {{
    background: var(--chip-hover);
    color: var(--text);
    border-color: color-mix(in srgb, var(--text) 25%, transparent);
}}

/* Loading State Animations */
@keyframes shimmer {{
    0% {{ background-position: -1000px 0; }}
    100% {{ background-position: 1000px 0; }}
}}

@keyframes spin {{
    100% {{ transform: rotate(360deg); }}
}}

.hero.loading .input-wrapper {{
    background: linear-gradient(90deg, var(--input-bg) 0px, var(--chip-hover) 50%, var(--input-bg) 100%);
    background-size: 1000px 100%;
    animation: shimmer 2s infinite linear;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="hero" id="hero-container">
        <div class="ambient-glow"></div>
        <div class="container">
            <h1>{title_text}</h1>
            <p class="subtitle">{body_text}</p>
            
            <div class="prompt-container">
                <div class="input-wrapper">
                    <input type="text" id="ai-input" placeholder="Type a prompt or click a suggestion..." autocomplete="off">
                    <button id="submit-btn" aria-label="Generate">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                            <line x1="5" y1="12" x2="19" y2="12"></line>
                            <polyline points="12 5 19 12 12 19"></polyline>
                        </svg>
                    </button>
                </div>
                
                <div class="suggestions">
                    <button class="chip">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
                        Draft a welcome email
                    </button>
                    <button class="chip">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>
                        Analyze Q3 revenue data
                    </button>
                    <button class="chip">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg>
                        Generate hero image
                    </button>
                </div>
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// AI Prompt Hero Interface — Interactive Behavior
document.addEventListener('DOMContentLoaded', () => {{
    const input = document.getElementById('ai-input');
    const chips = document.querySelectorAll('.chip');
    const submitBtn = document.getElementById('submit-btn');
    const heroContainer = document.getElementById('hero-container');
    
    // Store original icon
    const originalIcon = submitBtn.innerHTML;
    // Loading icon (Spinner)
    const loadingIcon = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="animation: spin 1s linear infinite;"><path d="M21 12a9 9 0 1 1-6.219-8.56"></path></svg>`;

    let isTyping = false;

    // Handle chip clicks
    chips.forEach(chip => {{
        chip.addEventListener('click', () => {{
            if (isTyping) return;
            
            // Get text, ignoring SVG
            const text = chip.textContent.trim();
            
            isTyping = true;
            input.value = '';
            input.focus();
            
            let i = 0;
            const typeWriter = setInterval(() => {{
                input.value += text.charAt(i);
                i++;
                if (i >= text.length) {{
                    clearInterval(typeWriter);
                    isTyping = false;
                }}
            }}, 35); // Typing speed
        }});
    }});

    // Handle form submission simulation
    const simulateSubmit = () => {{
        if (!input.value.trim() || isTyping) return;
        
        // Enter loading state
        heroContainer.classList.add('loading');
        input.disabled = true;
        submitBtn.disabled = true;
        submitBtn.innerHTML = loadingIcon;
        
        // Simulate API response time
        setTimeout(() => {{
            heroContainer.classList.remove('loading');
            input.disabled = false;
            submitBtn.disabled = false;
            input.value = '';
            input.placeholder = "Prompt processed! What's next?";
            submitBtn.innerHTML = originalIcon;
            input.focus();
        }}, 2000);
    }};

    submitBtn.addEventListener('click', simulateSubmit);
    input.addEventListener('keydown', (e) => {{
        if (e.key === 'Enter') simulateSubmit();
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
