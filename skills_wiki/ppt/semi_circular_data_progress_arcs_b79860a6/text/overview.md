# Semi-Circular Data Progress Arcs

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Semi-Circular Data Progress Arcs

* **Core Visual Mechanism**: Clean, sleek half-circle (semi-circular) progress rings arranged horizontally in a grid. Each ring consists of a soft grey background track and a vibrantly colored overlay arc that represents a specific percentage. The percentage and thematic text below each arc share its exact color, creating immediate visual grouping.
* **Why Use This Skill (Rationale)**: This technique translates abstract numerical data into immediate spatial comparisons. Utilizing a *half-donut* instead of a full donut chart conserves vertical screen space, leaving ample room below for titles, metrics, and explanatory text without feeling cluttered.
* **Overall Applicability**: Perfect for executive summaries, KPI dashboards, demographic splits, and portfolio highlights where ~4 key metrics need to be presented side-by-side. 
* **Value Addition**: Transforms a basic bulleted list of metrics or a standard, heavy bar chart into a lightweight, scannable, and highly professional infographic dashboard.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Progress Arcs**: Composed of two layers. A base track `(235, 235, 235, 255)` and a primary fill color. The ends of the arcs are flat, not rounded.
  - **Color Logic**: Utilizes a vibrant, distinct 4-color Material palette against a stark white background:
    - Segment 1: Pink/Magenta `(233, 30, 99, 255)`
    - Segment 2: Teal/Cyan `(0, 150, 136, 255)`
    - Segment 3: Light Green `(139, 195, 74, 255)`
    - Segment 4: Indigo/Blue `(63, 81, 181, 255)`
  - **Text Hierarchy**: 
    1. Overall Title: Spaced out, bold, uppercase (e.g., "P E R C E N T A G E S").
    2. Data Point: Large, bold, dynamically colored percentage (e.g., "60%").
    3. Segment Title: Medium, bold, matching color.
    4. Description text: Small, regular weight, muted grey `(158, 158, 158)`.

* **Step B: Compositional Style**
  - **Layout Principles**: A rigid, symmetrical 4-column horizontal layout. 
  - **Spacing**: The arcs are evenly distributed across the 13.33" width slide. Centers are mathematically placed at approximately ~2.16", ~5.16", ~8.16", and ~11.16" to ensure perfect symmetry and whitespace margins.

* **Step C: Dynamic Effects & Transitions**
  - *Tutorial animation*: The colored arcs use a "Spin" animation with custom degree amounts to "fill up", while the text below uses a delayed "Zoom" entrance. (Note: Our code generates the static, fully-realized visual).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Semi-circular Progress Arcs** | `PIL/Pillow` | Native `python-pptx` does not support drawing precise, variable-degree donut slices or thick arcs programmatically. We use PIL to mathematically draw smooth, antialiased thick arcs and insert them as transparent PNGs. |
| **Text Layout & Formatting** | `python-pptx` native | `python-pptx` perfectly handles precise coordinate placement, font styling, and word wrapping for the labels and descriptions. |

> **Feasibility Assessment**: **100%** visual reproduction of the final slide state. The exact layout, colors, geometry, and typographic hierarchy are fully reproduced. (PowerPoint custom animations must be added manually in the UI if desired).

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "PERCENTAGES",
    subtitle_text: str = "This is a demo text you may write a brief text here to explain the title or if you think you do\nnot need this you may consider deleting the text box.",
    segments: list = None,
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the 'Semi-Circular Data Progress Arcs' visual effect.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from PIL import Image, ImageDraw
    import io

    # Default segment data mapping the tutorial's exact numbers and color palette
    if segments is None:
        segments = [
            {"pct": 60, "color": (233, 30, 99), "title": "GRAPHIC DESIGN", "desc": "Here You Should Add\nSome Brief Text to Explain\nMain Title"},
            {"pct": 70, "color": (0, 150, 136), "title": "WEB DESIGN", "desc": "Here You Should Add\nSome Brief Text to Explain\nMain Title"},
            {"pct": 50, "color": (139, 195, 74), "title": "VIDEO EDITING", "desc": "Here You Should Add\nSome Brief Text to Explain\nMain Title"},
            {"pct": 90, "color": (63, 81, 181), "title": "UX DESIGN", "desc": "Here You Should Add\nSome Brief Text to Explain\nMain Title"},
        ]

    # Initialize presentation (16:9 standard)
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

    # Helper: Text Box Generator
    def add_formatted_text(left, top, width, height, text, font_size, font_color, is_bold=False):
        txBox = slide.shapes.add_textbox(left, top, width, height)
        tf = txBox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        run = p.add_run()
        run.text = text
        run.font.size = Pt(font_size)
        run.font.bold = is_bold
        run.font.name = "Century Gothic"
        run.font.color.rgb = font_color
        return txBox

    # Helper: PIL Arc Generator for smooth high-res progress rings
    def get_arc_stream(pct, color):
        scale = 4  # Render large for antialiasing
        base_size = 400
        size = base_size * scale
        thickness = 40 * scale
        
        img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        bbox = [thickness/2, thickness/2, size - thickness/2, size - thickness/2]
        
        # Draw background track (180 to 360 sweeps the top half)
        draw.arc(bbox, 180, 360, fill=(235, 235, 235, 255), width=thickness)
        
        # Draw percentage fill
        fill_end = 180 + (pct / 100.0) * 180
        draw.arc(bbox, 180, fill_end, fill=color + (255,), width=thickness)
        
        # Crop to the exact semi-circle bounding area
        crop_bottom = int(size/2 + thickness/2 + 2 * scale)
        img = img.crop((0, 0, size, crop_bottom))
        
        # Downscale for crisp anti-aliased edges
        img = img.resize((base_size, int(crop_bottom/scale)), Image.Resampling.LANCZOS)
        
        img_stream = io.BytesIO()
        img.save(img_stream, format='PNG')
        img_stream.seek(0)
        return img_stream

    # --- Layer 1: Global Titles ---
    # Convert "PERCENTAGES" to spaced out string "P  E  R  C  E  N  T  A  G  E  S"
    title_spaced = "  ".join(list(title_text.replace(" ", "")))
    add_formatted_text(Inches(2.0), Inches(0.6), Inches(9.33), Inches(0.8), 
                       title_spaced, 36, RGBColor(160, 160, 160), is_bold=True)
    
    add_formatted_text(Inches(2.0), Inches(1.4), Inches(9.33), Inches(0.8), 
                       subtitle_text, 12, RGBColor(158, 158, 158), is_bold=False)

    # --- Layer 2: Dashboard Grid Assembly ---
    num_items = len(segments)
    # Distribute centers evenly across the canvas
    centers = [2.166 + (i * 3.0) for i in range(num_items)]

    for i, seg in enumerate(segments):
        center_x = centers[i]
        seg_color = RGBColor(*seg['color'])
        
        # Insert PIL Progress Arc
        arc_stream = get_arc_stream(seg['pct'], seg['color'])
        arc_width = 2.4
        slide.shapes.add_picture(arc_stream, Inches(center_x - arc_width/2), Inches(3.0), width=Inches(arc_width))
        
        # Insert Percentage Text
        add_formatted_text(Inches(center_x - 1.0), Inches(4.4), Inches(2.0), Inches(0.6),
                           f"{seg['pct']}%", 32, seg_color, is_bold=True)
        
        # Insert Title Text
        add_formatted_text(Inches(center_x - 1.0), Inches(5.1), Inches(2.0), Inches(0.4),
                           seg['title'], 14, seg_color, is_bold=True)
        
        # Insert Description Text
        add_formatted_text(Inches(center_x - 1.2), Inches(5.4), Inches(2.4), Inches(1.0),
                           seg['desc'], 11, RGBColor(158, 158, 158), is_bold=False)

    prs.save(output_pptx_path)
    return output_pptx_path
```