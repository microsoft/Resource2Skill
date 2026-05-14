# Animated Geometric Alternating Timeline

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Animated Geometric Alternating Timeline

* **Core Visual Mechanism**: A central horizontal axis serves as the backbone of a chronological timeline. Nodes are represented by nested geometric shapes (a solid inner dot, a thick hollow circle, and an outer rotating arc). Branching lines alternate top-to-bottom to connect the timeline nodes to their corresponding text elements. Each node utilizes a specific accent color, creating a cohesive yet vibrant progression.
* **Why Use This Skill (Rationale)**: The alternating top/bottom layout prevents text collision, allowing for a dense but clean display of chronological data. The overlapping geometric shapes (inner circle + hollow circle + arc) create a technical, polished look that resembles an intricate dial or lens mechanism. Z-order masking (using a background-colored fill on the hollow circle to hide the lines behind it) keeps the center pristine without complex math.
* **Overall Applicability**: Ideal for corporate milestones, project roadmaps, product launch history, and company history overviews. 
* **Value Addition**: Transforms a basic bulleted list of dates into a visually engaging, easy-to-read narrative structure that guides the viewer's eye sequentially.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Main Axis**: A 1.5pt solid horizontal line (light gray).
  - **Nodes**: Built in three layers to create a "technical" feel:
    1. Outer arc (2pt, matching accent color, rotated stylistically).
    2. Middle hollow circle (2.5pt border, filled with the exact color of the slide background to mask underlying lines).
    3. Inner solid dot (matching accent color).
  - **Color Logic**: A light off-white background `(245, 245, 245)` with a 5-color repeating sequential palette (e.g., Cyan, Orange, Pink, Blue, Green).
  - **Text Hierarchy**: 
    - Title: Large, centered at the top, dark gray.
    - Year/Date: Large (28pt), colored to match the node, positioned at the end of the branch.
    - Body text: Small (10pt), light gray, placed adjacent to the year.

* **Step B: Compositional Style**
  - Timeline occupies the middle horizontal split (`Y = 50%`).
  - Nodes are distributed evenly across the horizontal plane with a 1.5-inch margin on either side.
  - Branches alternate: Index 0 (Up), Index 1 (Down), Index 2 (Up), etc.

* **Step C: Dynamic Effects & Transitions**
  - *Tutorial Implementation*: PowerPoint native animations (Wipe left-to-right for lines, Zoom for circles, Float In for text). 
  - *Code Constraints*: While the static composition is 100% reproducible via `python-pptx`, the sequential entry animations must be configured inside PowerPoint post-generation.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Geometric Nodes (Circles/Arcs)** | `python-pptx` native | PowerPoint's native `MSO_SHAPE.OVAL` and `MSO_SHAPE.ARC` are perfect for crisp vector rendering. |
| **Connecting Lines** | `python-pptx` native | `MSO_CONNECTOR.STRAIGHT` handles the precise mathematical alignment. |
| **Line Masking Trick** | `python-pptx` Z-order | By drawing the lines first, then drawing the middle circle with a solid fill matching the slide background, we get a clean "cutout" effect over the timeline axis natively without complex math. |

> **Feasibility Assessment**: 100% reproduction of the static visual layout. Animations and slide transitions from the tutorial are not implemented in the Python code, as `python-pptx` does not expose robust timeline animation sequence APIs.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "T I M E L I N E   S L I D E",
    timeline_data: list = None,
    bg_color: tuple = (245, 245, 245),
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Animated Geometric Alternating Timeline effect.
    
    :param output_pptx_path: Path to save the PPTX file
    :param title_text: Text for the top title
    :param timeline_data: List of dicts containing 'year', 'desc', and 'color' (RGB tuple). 
    :param bg_color: RGB tuple for the slide background
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
    from pptx.enum.text import PP_ALIGN

    # Default data if none provided
    if not timeline_data:
        timeline_data = [
            {"year": "2013", "desc": "YOU NEED TO ADD\nYOUR OWN BULLET POINTS", "color": (52, 152, 219)},   # Cyan
            {"year": "2014", "desc": "YOU NEED TO ADD\nYOUR OWN BULLET POINTS", "color": (230, 126, 34)},   # Orange
            {"year": "2015", "desc": "YOU NEED TO ADD\nYOUR OWN BULLET POINTS", "color": (231, 76, 60)},    # Pink/Red
            {"year": "2016", "desc": "YOU NEED TO ADD\nYOUR OWN BULLET POINTS", "color": (41, 128, 185)},   # Dark Blue
            {"year": "2017", "desc": "YOU NEED TO ADD\nYOUR OWN BULLET POINTS", "color": (39, 174, 96)},    # Green
        ]

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Set Background ===
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*bg_color)

    # === Calculations ===
    margin = Inches(1.5)
    usable_width = prs.slide_width - (margin * 2)
    # Avoid division by zero if there's only 1 point
    spacing = usable_width / (len(timeline_data) - 1) if len(timeline_data) > 1 else 0
    center_y = prs.slide_height / 2

    # === Layer 1: Connectors (Drawn first so nodes sit on top) ===
    
    # 1a. Main Horizontal Axis
    axis = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, 0, center_y, prs.slide_width, center_y)
    axis.line.color.rgb = RGBColor(200, 200, 200)
    axis.line.width = Pt(1.5)

    # 1b. Vertical Branch Lines
    branch_len = Inches(1.2)
    for i, pt in enumerate(timeline_data):
        cx = margin + (i * spacing)
        # Alternate directions: -1 for UP, 1 for DOWN
        dir_y = -1 if i % 2 == 0 else 1
        end_y = center_y + (dir_y * branch_len)
        
        branch = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, cx, center_y, cx, end_y)
        branch.line.color.rgb = RGBColor(200, 200, 200)
        branch.line.width = Pt(1.5)

    # === Layer 2: Geometric Nodes (Overlays the lines natively) ===
    
    for i, pt in enumerate(timeline_data):
        cx = margin + (i * spacing)
        color = pt["color"]

        # Outer Arc Shape
        arc_r = Inches(0.35)
        arc = slide.shapes.add_shape(MSO_SHAPE.ARC, cx - arc_r, center_y - arc_r, arc_r * 2, arc_r * 2)
        arc.line.color.rgb = RGBColor(*color)
        arc.line.width = Pt(2.0)
        arc.rotation = 45 if i % 2 == 0 else -135 # stylistic rotation

        # Middle Hollow Circle (Masking trick: Fill matches slide BG to hide lines passing through)
        hc_r = Inches(0.2)
        hc = slide.shapes.add_shape(MSO_SHAPE.OVAL, cx - hc_r, center_y - hc_r, hc_r * 2, hc_r * 2)
        hc.fill.solid()
        hc.fill.fore_color.rgb = RGBColor(*bg_color) 
        hc.line.color.rgb = RGBColor(*color)
        hc.line.width = Pt(2.5)

        # Inner Solid Dot
        ic_r = Inches(0.08)
        ic = slide.shapes.add_shape(MSO_SHAPE.OVAL, cx - ic_r, center_y - ic_r, ic_r * 2, ic_r * 2)
        ic.fill.solid()
        ic.fill.fore_color.rgb = RGBColor(*color)
        ic.line.color.rgb = RGBColor(*color) # Remove default border line

    # === Layer 3: Text Content ===
    
    # 3a. Node Texts (Year & Description)
    tw, th = Inches(2.0), Inches(0.5)
    d_th = Inches(0.6)
    
    for i, pt in enumerate(timeline_data):
        cx = margin + (i * spacing)
        dir_y = -1 if i % 2 == 0 else 1
        end_y = center_y + (dir_y * branch_len)
        color = pt["color"]
        tx = cx - (tw / 2)

        # Calculate Y positions based on direction to keep text at the end of the line
        if dir_y == -1: # Upwards
            year_y = end_y - th
            desc_y = year_y - d_th
        else:           # Downwards
            year_y = end_y
            desc_y = year_y + th

        # Year Box
        tb = slide.shapes.add_textbox(tx, year_y, tw, th)
        p = tb.text_frame.paragraphs[0]
        p.text = pt["year"]
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(28)
        p.font.name = "Century Gothic"
        p.font.color.rgb = RGBColor(*color)

        # Description Box
        dtb = slide.shapes.add_textbox(tx, desc_y, tw, d_th)
        dp = dtb.text_frame.paragraphs[0]
        dp.text = pt["desc"]
        dp.alignment = PP_ALIGN.CENTER
        dp.font.size = Pt(10)
        dp.font.name = "Century Gothic"
        dp.font.color.rgb = RGBColor(150, 150, 150)

    # 3b. Main Title
    title_w, title_h = Inches(6), Inches(0.6)
    title_x = (prs.slide_width - title_w) / 2
    title_y = Inches(0.4)
    
    title_box = slide.shapes.add_textbox(title_x, title_y, title_w, title_h)
    tp = title_box.text_frame.paragraphs[0]
    tp.text = title_text
    tp.alignment = PP_ALIGN.CENTER
    tp.font.size = Pt(24)
    tp.font.name = "Century Gothic"
    tp.font.color.rgb = RGBColor(120, 120, 120)

    # 3c. Title Header Dots (Mini legend)
    dot_spacing = Inches(0.2)
    start_x = (prs.slide_width - (dot_spacing * (len(timeline_data) - 1))) / 2
    dot_y = title_y + Inches(0.6)
    dot_r = Inches(0.06)

    for i, pt in enumerate(timeline_data):
        dx = start_x + (i * dot_spacing)
        dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, dx - dot_r, dot_y - dot_r, dot_r * 2, dot_r * 2)
        dot.fill.solid()
        dot.fill.fore_color.rgb = RGBColor(*pt["color"])
        dot.line.color.rgb = RGBColor(*pt["color"])

    prs.save(output_pptx_path)
    return output_pptx_path
```