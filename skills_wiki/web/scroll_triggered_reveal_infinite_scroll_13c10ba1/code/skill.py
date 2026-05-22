def create_component(
    output_dir: str,
    title_text: str = "Infinite Scroll Feed",
    body_text: str = "Scroll down to reveal more cards. This demonstrates performant Intersection Observer mechanics.",
    color_scheme: str = "dark",        
    accent_color: str = "#00bfff",     
    width_px: int = 600,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Intersection Observer Card Reveal and Infinite Scroll.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
        surface_color = "rgba(255, 255, 255, 0.06)"
        border_color = "rgba(255, 255, 255, 0.1)"
        shadow = "0 8px 24px rgba(0, 0, 0, 0.3)"
    else:
        bg_color = "#f4f5f7"
        text_color = "#1a1a2e"
        surface_color = "#ffffff"
        border_color = "rgba(0, 0, 0, 0.08)"
        shadow = "0 8px 24px rgba(0, 0, 0, 0.05)"

    # === CSS ===
    css = f"""/* Scroll Reveal & Infinite Scroll Component */
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
    --shadow: {shadow};
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
}}

.app-wrapper {{
    width: var(--width);
    max-width: 100%;
    height: var(--height);
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 16px;
    box-shadow: var(--shadow);
    display: flex;
    flex-direction: column;
    overflow: hidden;
}}

.header {{
    padding: 24px;
    border-bottom: 1px solid var(--border);
    background: var(--surface);
    z-index: 10;
}}

.header h1 {{
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 8px;
}}

.header p {{
    font-size: 0.95rem;
    opacity: 0.8;
    line-height: 1.4;
}}

/* The scrollable container */
.card-container {{
    flex: 1;
    overflow-y: auto;
    padding: 24px;
    display: flex;
    flex-direction: column;
    gap: 16px;
}}

/* Smooth scrollbar */
.card-container::-webkit-scrollbar {{
    width: 8px;
}}
.card-container::-webkit-scrollbar-track {{
    background: transparent;
}}
.card-container::-webkit-scrollbar-thumb {{
    background: var(--border);
    border-radius: 4px;
}}

/* Card Elements */
.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    padding: 24px;
    border-radius: 12px;
    box-shadow: var(--shadow);
    border-left: 4px solid var(--accent);
    
    /* Reveal Animation defaults (Hidden State) */
    opacity: 0;
    transform: translateX(40px);
    transition: transform 0.4s cubic-bezier(0.2, 0.8, 0.2, 1), 
                opacity 0.4s ease;
}}

/* Visible State */
.card.show {{
    opacity: 1;
    transform: translateX(0);
}}

.card-title {{
    font-weight: 600;
    margin-bottom: 8px;
    color: var(--accent);
}}

.card-body {{
    font-size: 0.9rem;
    line-height: 1.5;
    opacity: 0.9;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-wrapper">
        <div class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </div>
        
        <div class="card-container" id="scrollContainer">
            <!-- Initial set of cards -->
            <div class="card"><div class="card-title">Card Item #1</div><div class="card-body">Initial loaded content block. Scroll to see the animation.</div></div>
            <div class="card"><div class="card-title">Card Item #2</div><div class="card-body">Initial loaded content block. Scroll to see the animation.</div></div>
            <div class="card"><div class="card-title">Card Item #3</div><div class="card-body">Initial loaded content block. Scroll to see the animation.</div></div>
            <div class="card"><div class="card-title">Card Item #4</div><div class="card-body">Initial loaded content block. Scroll to see the animation.</div></div>
            <div class="card"><div class="card-title">Card Item #5</div><div class="card-body">Initial loaded content block. Scroll to see the animation.</div></div>
            <div class="card"><div class="card-title">Card Item #6</div><div class="card-body">Initial loaded content block. Scroll to see the animation.</div></div>
            <div class="card"><div class="card-title">Card Item #7</div><div class="card-body">Initial loaded content block. Scroll to see the animation.</div></div>
            <div class="card"><div class="card-title">Card Item #8</div><div class="card-body">Initial loaded content block. Scroll to see the animation.</div></div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Intersection Observer Logic
document.addEventListener('DOMContentLoaded', () => {{
    const scrollContainer = document.getElementById('scrollContainer');
    
    // 1. Reveal Observer: Animates cards sliding in
    const revealObserver = new IntersectionObserver((entries, observer) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                // Add the 'show' class to trigger CSS transition
                entry.target.classList.add('show');
                
                // Stop observing once revealed so it doesn't animate out when scrolling back up
                observer.unobserve(entry.target);
            }}
        }});
    }}, {{
        root: scrollContainer, // Observe relative to our custom scrollable container
        threshold: 0.2         // Trigger when 20% of the card is visible
    }});

    // Attach reveal observer to initial cards
    document.querySelectorAll('.card').forEach(card => revealObserver.observe(card));

    // 2. Infinite Scroll Observer: Watches the LAST card to trigger loading more
    let cardCounter = 8; // Starting after our initial 8
    
    const infiniteScrollObserver = new IntersectionObserver((entries, observer) => {{
        const lastCard = entries[0];
        
        if (lastCard.isIntersecting) {{
            // Once we hit the last card, load new ones
            loadMoreCards();
            
            // Stop observing the OLD last card
            observer.unobserve(lastCard.target);
            
            // Observe the NEW last card we just created
            const newLastCard = scrollContainer.querySelector('.card:last-child');
            if (newLastCard) observer.observe(newLastCard);
        }}
    }}, {{
        root: scrollContainer,
        rootMargin: "50px", // Pre-fetch trigger: fires 50px before the element actually enters view
    }});

    // Start observing the initial last card
    infiniteScrollObserver.observe(document.querySelector('.card:last-child'));

    // Helper: Simulate fetching data and appending DOM nodes
    function loadMoreCards() {{
        // Add 5 new cards at a time
        for (let i = 0; i < 5; i++) {{
            cardCounter++;
            
            const newCard = document.createElement('div');
            newCard.classList.add('card');
            
            newCard.innerHTML = `
                <div class="card-title">Card Item #${{cardCounter}} (Lazy Loaded)</div>
                <div class="card-body">This card was dynamically appended to the DOM when you scrolled near the bottom.</div>
            `;
            
            // Add the new card to the DOM
            scrollContainer.appendChild(newCard);
            
            // Ensure the new card is hooked up to the Reveal Observer so it slides in
            revealObserver.observe(newCard);
        }}
    }}
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
