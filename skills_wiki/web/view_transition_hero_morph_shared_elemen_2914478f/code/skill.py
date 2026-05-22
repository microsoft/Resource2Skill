def create_component(
    output_dir: str,
    title_text: str = "Music Library",
    body_text: str = "Recently Played",
    color_scheme: str = "dark",
    accent_color: str = "#00bfff",
    width_px: int = 1000,
    height_px: int = 800,
    **kwargs,
) -> dict:
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
        surface_color = "rgba(255, 255, 255, 0.05)"
        surface_hover = "rgba(255, 255, 255, 0.09)"
    else:
        bg_color = "#f9fafb"
        text_color = "#111827"
        surface_color = "rgba(0, 0, 0, 0.04)"
        surface_hover = "rgba(0, 0, 0, 0.08)"

    css = f"""/* View Transition Hero Morph */
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
    --surface-hover: {surface_hover};
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #000;
    color: var(--text);
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    padding: 2rem;
}}

.app-container {{
    width: 100%;
    max-width: {width_px}px;
    height: {height_px}px;
    background: var(--bg);
    border-radius: 16px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    overflow-y: auto;
    position: relative;
}}

/* Hide scrollbar for sleek app feel */
.app-container::-webkit-scrollbar {{ display: none; }}

header {{
    padding: 2rem 2rem 1rem 2rem;
    position: sticky;
    top: 0;
    background: rgba(var(--bg), 0.8);
    backdrop-filter: blur(12px);
    z-index: 10;
}}

header h1 {{ font-size: 1.5rem; font-weight: 600; margin-bottom: 0.25rem; }}
header p {{ font-size: 0.9rem; opacity: 0.6; }}

/* --- Grid View --- */
.view-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1.5rem;
    padding: 1rem 2rem 3rem 2rem;
}}

.card {{
    background: var(--surface);
    border-radius: 12px;
    padding: 1rem;
    cursor: pointer;
    transition: transform 0.2s ease, background 0.2s ease;
}}

.card:hover {{
    transform: translateY(-4px);
    background: var(--surface-hover);
}}

.card img {{
    width: 100%;
    aspect-ratio: 1;
    border-radius: 8px;
    object-fit: cover;
    margin-bottom: 1rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}}

.card h3 {{ font-size: 1rem; font-weight: 600; margin-bottom: 0.25rem; }}
.card p {{ font-size: 0.85rem; opacity: 0.7; }}

/* --- Detail View --- */
.view-detail {{
    padding: 2rem;
}}

.btn-back {{
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: transparent;
    border: none;
    color: var(--text);
    font-size: 1rem;
    cursor: pointer;
    padding: 0.5rem 0;
    margin-bottom: 2rem;
    opacity: 0.7;
    transition: opacity 0.2s;
}}
.btn-back:hover {{ opacity: 1; }}

.detail-content {{
    display: flex;
    flex-direction: column;
    gap: 2rem;
}}

@media (min-width: 768px) {{
    .detail-content {{
        flex-direction: row;
        gap: 4rem;
    }}
}}

.detail-album-cover {{
    width: clamp(250px, 40vw, 350px);
    aspect-ratio: 1;
    border-radius: 12px;
    object-fit: cover;
    box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    flex-shrink: 0;
    /* MAGIC PROPERTY: This binds the detail image to the transition */
    view-transition-name: hero;
}}

.tracklist {{ flex: 1; }}
.title-large {{ font-size: clamp(2rem, 4vw, 3rem); font-weight: 700; line-height: 1.1; margin-bottom: 0.5rem; }}
.artist-large {{ font-size: 1.25rem; opacity: 0.7; margin-bottom: 2rem; }}

.controls {{
    display: flex;
    gap: 1rem;
    margin-bottom: 2.5rem;
}}

.btn-play {{
    background: var(--accent);
    color: #fff;
    border: none;
    padding: 0.75rem 2rem;
    border-radius: 2rem;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    box-shadow: 0 8px 16px rgba(0, 191, 255, 0.3);
    transition: transform 0.1s;
}}
.btn-play:active {{ transform: scale(0.95); }}

.btn-shuffle {{
    background: var(--surface);
    color: var(--text);
    border: none;
    padding: 0.75rem 2rem;
    border-radius: 2rem;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
}}

.song-list {{ list-style: none; }}
.song-list li {{
    display: grid;
    grid-template-columns: 32px 1fr auto;
    padding: 1rem 0;
    border-bottom: 1px solid var(--surface);
    opacity: 0.7;
    font-size: 0.95rem;
    transition: opacity 0.2s;
    cursor: default;
}}
.song-list li:hover {{ opacity: 1; }}

/* --- View Transition Customization --- */
::view-transition-old(hero),
::view-transition-new(hero) {{
    /* Custom elastic morph timing */
    animation-duration: 0.5s;
    animation-timing-function: cubic-bezier(0.25, 1, 0.5, 1);
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-container" id="app-scroll-container">
        
        <!-- GRID VIEW -->
        <main class="view-grid" id="view-grid">
            <header style="grid-column: 1 / -1; background: transparent; padding: 0 0 1rem 0; position: static; backdrop-filter: none;">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
            </header>
            
            <div class="card">
                <img src="https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?auto=format&fit=crop&w=600&q=80" alt="Neon Nights">
                <div class="card-info">
                    <h3>Neon Nights</h3>
                    <p>Synthwave</p>
                </div>
            </div>
            
            <div class="card">
                <img src="https://images.unsplash.com/photo-1493225457124-a1a2a5f5f92e?auto=format&fit=crop&w=600&q=80" alt="Analog Warmth">
                <div class="card-info">
                    <h3>Analog Warmth</h3>
                    <p>Vinyl Collections</p>
                </div>
            </div>
            
            <div class="card">
                <img src="https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=600&q=80" alt="Live at The Apollo">
                <div class="card-info">
                    <h3>Live at The Apollo</h3>
                    <p>Concert Series</p>
                </div>
            </div>
            
            <div class="card">
                <img src="https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=600&q=80" alt="Club Mix 2024">
                <div class="card-info">
                    <h3>Club Mix 2024</h3>
                    <p>DJ Essentails</p>
                </div>
            </div>
            
            <div class="card">
                <img src="https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=600&q=80" alt="Studio Sessions">
                <div class="card-info">
                    <h3>Studio Sessions</h3>
                    <p>Acoustic Covers</p>
                </div>
            </div>
            
            <div class="card">
                <img src="https://images.unsplash.com/photo-1459749411175-04bf5292ceea?auto=format&fit=crop&w=600&q=80" alt="Classical Keys">
                <div class="card-info">
                    <h3>Classical Keys</h3>
                    <p>Piano Masterpieces</p>
                </div>
            </div>
        </main>
        
        <!-- DETAIL VIEW -->
        <main class="view-detail" id="view-detail" style="display: none;">
            <button id="btn-back" class="btn-back">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
                Library
            </button>
            <div class="detail-content">
                <img src="" id="detail-img" class="detail-album-cover">
                <div class="tracklist">
                    <h2 id="detail-title" class="title-large">Album Title</h2>
                    <p id="detail-artist" class="artist-large">Artist</p>
                    <div class="controls">
                        <button class="btn-play">Play</button>
                        <button class="btn-shuffle">Shuffle</button>
                    </div>
                    <ol class="song-list">
                        <li><span>1</span> <span>Intro / Overture</span> <span>2:15</span></li>
                        <li><span>2</span> <span>The Main Event</span> <span>4:05</span></li>
                        <li><span>3</span> <span>Interlude (Echoes)</span> <span>1:30</span></li>
                        <li><span>4</span> <span>Midnight Drive</span> <span>3:43</span></li>
                        <li><span>5</span> <span>Fade to Black</span> <span>5:12</span></li>
                    </ol>
                </div>
            </div>
        </main>
        
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""document.addEventListener('DOMContentLoaded', () => {{
    const gridView = document.getElementById('view-grid');
    const detailView = document.getElementById('view-detail');
    const detailImg = document.getElementById('detail-img');
    const detailTitle = document.getElementById('detail-title');
    const detailArtist = document.getElementById('detail-artist');
    const scrollContainer = document.getElementById('app-scroll-container');
    
    let activeCardImg = null;
    let savedScrollPosition = 0;

    // Helper to abstract the View Transition API with a fallback
    function transitionTo(callback) {{
        if (!document.startViewTransition) {{
            // Fallback for Safari < 18 or Firefox
            callback();
            return;
        }}
        // Trigger native view transition
        return document.startViewTransition(callback);
    }}

    // Handle clicking a card
    document.querySelectorAll('.card').forEach(card => {{
        card.addEventListener('click', () => {{
            const img = card.querySelector('img');
            const title = card.querySelector('h3').innerText;
            const artist = card.querySelector('p').innerText;
            
            // 1. Tag the clicked image dynamically so it becomes the source of the morph
            activeCardImg = img;
            activeCardImg.style.viewTransitionName = 'hero';
            
            savedScrollPosition = scrollContainer.scrollTop;

            transitionTo(() => {{
                // 2. DOM Updates (Old state -> New state)
                gridView.style.display = 'none';
                detailView.style.display = 'block';
                
                // Populate new data
                detailImg.src = activeCardImg.src;
                detailTitle.innerText = title;
                detailArtist.innerText = artist;
                
                // Reset scroll for the new view
                scrollContainer.scrollTop = 0;
                
                // Note: detailImg statically has 'view-transition-name: hero' in CSS, 
                // so the browser automatically interpolates from activeCardImg to detailImg.
            }});
        }});
    }});

    // Handle clicking the back button
    document.getElementById('btn-back').addEventListener('click', () => {{
        const transition = transitionTo(() => {{
            // Restore Grid
            detailView.style.display = 'none';
            gridView.style.display = 'grid';
            
            // Restore scroll position so user doesn't lose their place
            scrollContainer.scrollTop = savedScrollPosition;
        }});

        if (transition) {{
            // 3. Clean up the dynamic tag after the reverse animation finishes
            transition.finished.then(() => {{
                if (activeCardImg) {{
                    activeCardImg.style.viewTransitionName = '';
                    activeCardImg = null;
                }}
            }});
        }} else {{
            // Fallback cleanup
            if (activeCardImg) activeCardImg.style.viewTransitionName = '';
            activeCardImg = null;
        }}
    }});
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
