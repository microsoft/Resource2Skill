def create_component(
    output_dir: str,
    title_text: str = "Viewport Dynamics",
    body_text: str = "Scroll down to explore performant, intersection-triggered animations and seamless infinite scrolling.",
    color_scheme: str = "dark",
    accent_color: str = "#8b5cf6",
    width_px: int = 1000,
    height_px: int = 800,
    **kwargs,
) -> dict:
    import os

    os.makedirs(output_dir, exist_ok=True)
    
    # Safe escaping for HTML inputs
    title_safe = title_text.replace('<', '&lt;').replace('>', '&gt;')
    body_safe = body_text.replace('<', '&lt;').replace('>', '&gt;')

    # Theme definitions
    if color_scheme == "dark":
        bg_color = "#09090b"
        surface_color = "#18181b"
        border_color = "#27272a"
        text_color = "#fafafa"
        muted_text = "#a1a1aa"
    else:
        bg_color = "#ffffff"
        surface_color = "#f4f4f5"
        border_color = "#e4e4e7"
        text_color = "#09090b"
        muted_text = "#71717a"

    css = f"""/* Viewport Dynamics — Generated Component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --surface: {surface_color};
    --border: {border_color};
    --text: {text_color};
    --muted: {muted_text};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #111; /* Dark backdrop for the embedded window */
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

/* The scrollable component window */
.viewport-container {{
    width: var(--width);
    height: var(--height);
    background: var(--bg);
    color: var(--text);
    overflow-y: auto;
    overflow-x: hidden;
    position: relative;
    box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5);
    border-radius: 12px;
    scroll-behavior: smooth;
}}

/* Sections Layout */
section {{
    padding: 100px 40px;
    max-width: 800px;
    margin: 0 auto;
}}

.hero {{
    height: 80vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    border-bottom: 1px solid var(--border);
}}

.hero h1 {{
    font-size: 3.5rem;
    font-weight: 800;
    letter-spacing: -0.05em;
    margin-bottom: 1rem;
    background: linear-gradient(135deg, var(--text), var(--accent));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

.hero p {{
    font-size: 1.25rem;
    color: var(--muted);
    max-width: 600px;
    line-height: 1.6;
}}

.scroll-indicator {{
    margin-top: 40px;
    animation: bounce 2s infinite;
    color: var(--accent);
}}

@keyframes bounce {{
    0%, 20%, 50%, 80%, 100% {{ transform: translateY(0); }}
    40% {{ transform: translateY(-20px); }}
    60% {{ transform: translateY(-10px); }}
}}

/* --- Core Reveal Animation Styles --- */
.observe-me {{
    opacity: 0;
    transition: opacity 0.8s cubic-bezier(0.16, 1, 0.3, 1), 
                transform 0.8s cubic-bezier(0.16, 1, 0.3, 1);
    will-change: opacity, transform;
}}

.slide-up {{ transform: translateY(60px); }}
.slide-left {{ transform: translateX(-60px); }}
.slide-right {{ transform: translateX(60px); }}

.observe-me.show {{
    opacity: 1;
    transform: translate(0);
}}

/* Grid Gallery */
.gallery-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 24px;
    margin-top: 40px;
}}

.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    height: 200px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    color: var(--muted);
    position: relative;
    overflow: hidden;
}}

.card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(45deg, transparent, rgba(255,255,255,0.03), transparent);
    transform: translateX(-100%);
    transition: transform 0.6s ease;
}}

.card:hover::before {{
    transform: translateX(100%);
}}

/* Infinite Scroll List */
.list-section h2 {{
    margin-bottom: 24px;
    font-size: 2rem;
}}

.infinite-list {{
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 16px;
}}

.list-item {{
    background: var(--surface);
    padding: 20px 24px;
    border-radius: 8px;
    border-left: 4px solid var(--accent);
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: 500;
}}

.badge {{
    background: var(--bg);
    color: var(--accent);
    padding: 4px 10px;
    border-radius: 99px;
    font-size: 0.8rem;
    border: 1px solid var(--border);
}}

.loading-spinner {{
    text-align: center;
    padding: 40px;
    color: var(--muted);
    font-size: 0.9rem;
    opacity: 0.5;
}}

@media (prefers-reduced-motion: reduce) {{
    .observe-me {{
        transition: none !important;
        transform: none !important;
        opacity: 1 !important;
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_safe}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="viewport-container" id="scroll-root">
        
        <section class="hero">
            <h1>{title_safe}</h1>
            <p>{body_safe}</p>
            <div class="scroll-indicator">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14M19 12l-7 7-7-7"/></svg>
            </div>
        </section>

        <section class="gallery-section">
            <h2 class="observe-me slide-up">Dynamic Grid Reveal</h2>
            <div class="gallery-grid">
                <div class="card observe-me slide-left">Grid Item 1</div>
                <div class="card observe-me slide-up">Grid Item 2</div>
                <div class="card observe-me slide-right">Grid Item 3</div>
                <div class="card observe-me slide-left" style="transition-delay: 100ms">Grid Item 4</div>
                <div class="card observe-me slide-up" style="transition-delay: 200ms">Grid Item 5</div>
                <div class="card observe-me slide-right" style="transition-delay: 300ms">Grid Item 6</div>
            </div>
        </section>

        <section class="list-section">
            <h2 class="observe-me slide-up">Infinite Data Stream</h2>
            <ul class="infinite-list" id="infinite-list">
                <!-- Initial items populated via JS to share the same logic -->
            </ul>
            <div class="loading-spinner">Scroll down to load more...</div>
        </section>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Viewport Dynamics — Intersection Observer implementation
document.addEventListener('DOMContentLoaded', () => {{
    
    // The container acts as our scrollable viewport
    const rootContainer = document.getElementById('scroll-root');

    // 1. SCROLL REVEAL OBSERVER
    // Checks when elements enter 15% of the viewport and triggers their CSS transition
    const revealOptions = {{
        root: rootContainer,
        threshold: 0.15,
        rootMargin: "0px"
    }};

    const revealObserver = new IntersectionObserver((entries, observer) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                entry.target.classList.add('show');
                
                // Optional: Stop observing once revealed so it doesn't animate out and back in
                // observer.unobserve(entry.target); 
            }} else {{
                // Remove class when out of view so it animates again next time
                entry.target.classList.remove('show');
            }}
        }});
    }}, revealOptions);

    // Attach observer to all statically defined elements with 'observe-me'
    document.querySelectorAll('.observe-me').forEach(el => revealObserver.observe(el));


    // 2. INFINITE SCROLL OBSERVER
    const listContainer = document.getElementById('infinite-list');
    let currentItemCount = 0;
    
    // Options for infinite scroll: trigger 100px BEFORE the element hits the screen
    const infiniteOptions = {{
        root: rootContainer,
        rootMargin: "100px", 
        threshold: 0
    }};

    // Function to generate new DOM nodes
    const appendNewItems = (count) => {{
        const fragment = document.createDocumentFragment();
        
        for (let i = 0; i < count; i++) {{
            currentItemCount++;
            const li = document.createElement('li');
            li.className = 'list-item observe-me slide-up'; // Inherit reveal animations!
            li.innerHTML = `
                <span>Log Record #00${{currentItemCount}}</span>
                <span class="badge">Loaded</span>
            `;
            fragment.appendChild(li);
            
            // Critical: tell our first observer to watch these new dynamically created elements
            revealObserver.observe(li);
        }}
        
        listContainer.appendChild(fragment);
    }};

    const infiniteObserver = new IntersectionObserver((entries) => {{
        const lastItem = entries[0];
        
        if (lastItem.isIntersecting) {{
            // 1. Unobserve the current last item so we don't trigger recursively
            infiniteObserver.unobserve(lastItem.target);
            
            // 2. Append new items (simulate network fetch)
            setTimeout(() => {{
                appendNewItems(5);
                
                // 3. Re-target the observer to the newly appended last child
                const newLastItem = listContainer.querySelector('.list-item:last-child');
                if (newLastItem) {{
                    infiniteObserver.observe(newLastItem);
                }}
            }}, 400); // Artificial delay to simulate network load feel
        }}
    }}, infiniteOptions);

    // Initialize the list with starting items
    appendNewItems(8);
    
    // Start observing the last item of the newly generated batch
    const initialLastItem = listContainer.querySelector('.list-item:last-child');
    if (initialLastItem) {{
        infiniteObserver.observe(initialLastItem);
    }}
}});
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
