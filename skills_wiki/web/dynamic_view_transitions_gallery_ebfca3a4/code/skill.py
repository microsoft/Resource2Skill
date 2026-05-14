def create_component(
    output_dir: str,
    title_text: str = "Cinematic View Transitions",
    body_text: str = "Click any poster to trigger the native morphing animation.",
    color_scheme: str = "dark",
    accent_color: str = "#0ea5e9",
    width_px: int = 1000,
    height_px: int = 700,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Dynamic View Transitions Gallery.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_color = "#f8fafc"
        text_muted = "#94a3b8"
        surface_color = "#1e293b"
        hover_color = "#334155"
        app_bg = "#000000"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        text_muted = "#64748b"
        surface_color = "#e2e8f0"
        hover_color = "#cbd5e1"
        app_bg = "#cbd5e1"

    css = f"""/* Dynamic View Transitions Gallery */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --surface: {surface_color};
    --hover: {hover_color};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: {app_bg};
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

.container {{
    width: var(--width);
    height: var(--height);
    max-width: 100%;
    max-height: 100vh;
    background: var(--bg);
    color: var(--text);
    border-radius: 24px;
    box-shadow: 0 24px 48px rgba(0, 0, 0, 0.4);
    overflow-y: auto;
    overflow-x: hidden;
    position: relative;
    padding: 2.5rem;
}}

/* -- Utility -- */
[hidden] {{
    display: none !important;
}}

/* -- Gallery View -- */
.header {{
    margin-bottom: 2.5rem;
}}
.header h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    margin-bottom: 0.5rem;
}}
.header p {{
    color: var(--text-muted);
    font-size: 1.1rem;
}}

.grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 2rem;
}}

.card {{
    background: var(--surface);
    border-radius: 16px;
    padding: 12px;
    cursor: pointer;
    transition: transform 0.25s ease, background 0.25s ease;
    display: flex;
    flex-direction: column;
    gap: 12px;
}}
.card:hover {{
    transform: translateY(-6px);
    background: var(--hover);
}}

.poster {{
    width: 100%;
    aspect-ratio: 2 / 3;
    object-fit: cover;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}}

.card-title {{
    font-size: 1.1rem;
    font-weight: 600;
    line-height: 1.3;
    width: max-content;
    max-width: 100%;
}}

/* -- Detail View -- */
.back-btn {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: var(--surface);
    color: var(--text);
    border: none;
    padding: 0.6rem 1.2rem;
    border-radius: 30px;
    cursor: pointer;
    margin-bottom: 1.5rem;
    font-size: 0.95rem;
    font-weight: 500;
    transition: background 0.2s, color 0.2s;
}}
.back-btn:hover {{
    background: var(--accent);
    color: #fff;
}}

.hero-container {{
    margin-bottom: 2rem;
}}

.hero-image {{
    width: 100%;
    aspect-ratio: 21 / 9;
    object-fit: cover;
    border-radius: 16px;
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.25);
    display: block;
}}

.hero-title {{
    font-size: 3rem;
    font-weight: 800;
    margin-top: 1.5rem;
    margin-bottom: 1rem;
    letter-spacing: -0.02em;
    width: max-content;
    max-width: 100%;
}}

.hero-desc {{
    font-size: 1.15rem;
    line-height: 1.7;
    color: var(--text-muted);
    max-width: 800px;
    /* Only assigned name here to trigger enter/exit animations */
    view-transition-name: active-desc;
}}

/* =========================================
   View Transitions API Styles
   ========================================= */

/* 1. Global curve for the active morphing elements */
::view-transition-group(active-poster),
::view-transition-group(active-title) {{
    animation-duration: 0.6s;
    animation-timing-function: cubic-bezier(0.22, 1, 0.36, 1);
}}

/* Layering logic */
::view-transition-group(active-poster) {{ z-index: 10; }}
::view-transition-group(active-title) {{ z-index: 20; }}

/* 2. Aspect Ratio Fix: 
   Force the rasterized snapshots to cover the animating bounding box 
   instead of squishing/stretching. */
::view-transition-old(active-poster),
::view-transition-new(active-poster) {{
    height: 100%;
    width: 100%;
    object-fit: cover;
    border-radius: 12px;
    overflow: clip;
}}

/* 3. Text Sizing Fix:
   Prevent text wrapping weirdly during the scale interpolation */
::view-transition-old(active-title),
::view-transition-new(active-title) {{
    width: auto;
    height: auto;
}}

/* 4. Asymmetric Entrance/Exit for the Description Text */
::view-transition-new(active-desc) {{
    animation: slide-up-fade 0.5s ease-out forwards;
    /* Delay slightly to let the image establish its shape */
    animation-delay: 0.1s;
    opacity: 0;
}}

::view-transition-old(active-desc) {{
    animation: fade-out 0.2s ease-in forwards;
}}

@keyframes slide-up-fade {{
    from {{ opacity: 0; transform: translateY(20px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

@keyframes fade-out {{
    to {{ opacity: 0; }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        
        <!-- Gallery View -->
        <div id="gallery" class="view">
            <div class="header">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
            </div>
            <div class="grid" id="grid">
                <!-- Injected via JS -->
            </div>
        </div>

        <!-- Detail View -->
        <div id="detail" class="view" hidden>
            <button class="back-btn" id="back-btn">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M19 12H5M12 19l-7-7 7-7"/>
                </svg>
                Back to Gallery
            </button>
            <div class="hero-container">
                <img class="hero-image" id="hero-img" src="" alt="">
                <h1 class="hero-title" id="hero-title"></h1>
            </div>
            <p class="hero-desc" id="hero-desc"></p>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Dynamic View Transitions Gallery Logic

const items = [
    {{
        id: 1,
        title: "Dune Landscape",
        desc: "A vast and unforgiving desert world where survival is a daily struggle. The sands hold ancient secrets and immense power for those brave enough to seek it.",
        img: "https://images.unsplash.com/photo-1542401886-65d6c61db217?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80"
    }},
    {{
        id: 2,
        title: "Cybernetic City",
        desc: "A sprawling metropolis bathed in neon. The streets pulse with life, technology, and the shadows of a corporate-run dystopia.",
        img: "https://images.unsplash.com/photo-1605810230434-7631ac76ec81?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80"
    }},
    {{
        id: 3,
        title: "Interstellar Journey",
        desc: "Pushing the boundaries of human exploration. A visual spectacle of wormholes, distant galaxies, and the isolation of deep space.",
        img: "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80"
    }},
    {{
        id: 4,
        title: "The Final Stand",
        desc: "An epic conclusion to a legendary saga. Heroes rise, alliances fall, and the fate of the universe hangs by a thread.",
        img: "https://images.unsplash.com/photo-1478479405421-ce83c92fb3ba?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80"
    }}
];

let currentId = null;

function init() {{
    const grid = document.getElementById('grid');
    items.forEach(item => {{
        const card = document.createElement('div');
        card.className = 'card';
        card.dataset.id = item.id;
        card.innerHTML = `
            <img class="poster" src="${{item.img}}" alt="${{item.title}}">
            <div class="card-title">${{item.title}}</div>
        `;
        card.addEventListener('click', () => goToDetail(item.id));
        grid.appendChild(card);
    }});

    document.getElementById('back-btn').addEventListener('click', goBack);
}}

function goToDetail(id) {{
    const card = document.querySelector(`.card[data-id="${{id}}"]`);
    const cardImg = card.querySelector('.poster');
    const cardTitle = card.querySelector('.card-title');
    
    const detailImg = document.getElementById('hero-img');
    const detailTitle = document.getElementById('hero-title');
    
    // 1. Tag the outgoing elements specifically before transition
    cardImg.style.viewTransitionName = 'active-poster';
    cardTitle.style.viewTransitionName = 'active-title';
    
    // Fallback for browsers without View Transitions support
    if (!document.startViewTransition) {{
        performSwitch(id);
        return;
    }}
    
    // 2. Start the transition
    const transition = document.startViewTransition(() => {{
        performSwitch(id);
        
        // 3. Tag the incoming elements inside the transition callback
        // The browser captures the new state immediately after this callback finishes.
        detailImg.style.viewTransitionName = 'active-poster';
        detailTitle.style.viewTransitionName = 'active-title';
    }});
    
    // 4. Cleanup inline styles after the animation completes
    transition.finished.finally(() => {{
        cardImg.style.viewTransitionName = '';
        cardTitle.style.viewTransitionName = '';
    }});
}}

function goBack() {{
    const card = document.querySelector(`.card[data-id="${{currentId}}"]`);
    const cardImg = card.querySelector('.poster');
    const cardTitle = card.querySelector('.card-title');
    
    const detailImg = document.getElementById('hero-img');
    const detailTitle = document.getElementById('hero-title');
    
    // Tag outgoing elements (we are moving away from detail)
    detailImg.style.viewTransitionName = 'active-poster';
    detailTitle.style.viewTransitionName = 'active-title';
    
    if (!document.startViewTransition) {{
        performSwitchBack();
        return;
    }}
    
    const transition = document.startViewTransition(() => {{
        performSwitchBack();
        // Tag incoming elements (back to the specific card in the gallery)
        cardImg.style.viewTransitionName = 'active-poster';
        cardTitle.style.viewTransitionName = 'active-title';
    }});
    
    transition.finished.finally(() => {{
        detailImg.style.viewTransitionName = '';
        detailTitle.style.viewTransitionName = '';
        cardImg.style.viewTransitionName = '';
        cardTitle.style.viewTransitionName = '';
    }});
}}

function performSwitch(id) {{
    const item = items.find(i => i.id === id);
    const detailImg = document.getElementById('hero-img');
    const detailTitle = document.getElementById('hero-title');
    const detailDesc = document.getElementById('hero-desc');
    
    detailImg.src = item.img;
    detailTitle.textContent = item.title;
    detailDesc.textContent = item.desc;
    
    document.getElementById('gallery').hidden = true;
    document.getElementById('detail').hidden = false;
    currentId = id;
    
    // Scroll container to top
    document.querySelector('.container').scrollTo(0, 0);
}}

function performSwitchBack() {{
    document.getElementById('detail').hidden = true;
    document.getElementById('gallery').hidden = false;
    currentId = null;
}}

document.addEventListener('DOMContentLoaded', init);
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
