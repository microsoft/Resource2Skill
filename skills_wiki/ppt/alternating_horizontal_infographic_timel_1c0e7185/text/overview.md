# Alternating Horizontal Infographic Timeline

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Alternating Horizontal Infographic Timeline

* **Core Visual Mechanism**: The defining signature is a central, continuous horizontal track (the "timeline axis") with spaced milestone nodes. To maximize spatial efficiency and create visual rhythm, the content blocks (dates, titles, and descriptions) alternate above and below the central track. Vertical stem lines connect the floating content blocks back to their specific nodes on the axis.
* **Why Use This Skill (Rationale)**: Human eyes naturally scan left-to-right (in Western languages). A horizontal axis leverages this innate reading pattern. By alternating content up and down, the design prevents text overlapping, allowing for larger, more legible typography and longer descriptions than a single-sided layout could support. It balances the composition organically.
* **Overall Applicability**: Perfect for corporate histories, product roadmaps, project phase planning, and career journey slides. It works best when you have 4 to 6 distinct chronological milestones.
* **Value Addition**: Transforms a boring bulleted list of dates into a visual journey. The spatial arrangement implies forward momentum and structured progress, making the information feel organized, inevitable, and professionally planned.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **The Track**: A thick, muted horizontal line (e.g., light gray `(230, 230, 230, 255)`) spanning the slide.
  - **The Nodes**: Circular markers placed along the track. Usually designed as nested circles (a white outer circle with a colored inner dot) to create depth without relying on 3D effects.
  - **Connecting Stems**: Thin, often dashed or dotted lines linking the node to the text content.
  - **Color Logic**: A neutral background with a distinct accent color for each milestone to aid visual separation. For example: Cyan `(0, 191, 255)`, Teal `(32, 178, 170)`, Orange `(255, 165, 0)`.
  - **Text Hierarchy**: 
    1. **Date/Year**: Largest, boldest, uses the milestone's accent color.
    2. **Title**: Dark gray/black, bold, medium size.
    3. **Description**: Light gray, regular weight, smaller size.

* **Step B: Compositional Style**
  - **Spatial Feel**: The timeline axis sits exactly in the vertical center of the slide (or slightly lower if a large title is used). 
  - **Layout Principles**: Symmetry across the horizontal axis (alternating Top/Bottom). Even distribution across the vertical axis (equal spacing between nodes).
  - **Proportions**: Left/Right margins of ~10% canvas width. The timeline spans the middle 80%.

* **Step C: Dynamic Effects & Transitions**
  - **Transitions**: Typically uses a "Wipe" from left to right for the main track, followed by "Fade" or "Zoom" for the nodes and text in sequence. (These are native PPT animations).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Basic layout, timeline track, and nodes | `python-pptx` native shapes | Standard shapes (lines, ovals) are perfectly suited for this and allow the user to easily edit the nodes later. |
| Alternating text boxes and typography | `python-pptx` native text | Needs to remain editable text for standard presentation templates. |
| Connectors | `python-pptx` native connectors | Native lines allow us to create dashed stem lines cleanly. |

> **Feasibility Assessment**: 100% reproducible. The static layout, typography, and shape geometries are fully supported by `python-pptx` natively. We don't need PIL or lxml because the flat, modern aesthetic of this specific timeline relies on clean vector geometry and typography rather than complex raster compositing or 3D effects.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "Our Journey to Success",
    body_text: str = "A brief overview of our major milestones and achievements over the past five years.",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the 'Alternating Horizontal Infographic Timeline' visual effect.
    """
    import pptx
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE

    # Initialize presentation (16:9)
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank layout
    slide_layout = prs.slide_layouts[6] 
    slide = prs.slides.add_slide(slide_layout)

    # Global dimensions
    canvas_w = 13.333
    canvas_h = 7.5
    track_y = 4.2  # Y position of the main horizontal track
    start_x = 1.5
    end_x = canvas_w - 1.5
    track_width = end_x - start_x

    # Colors
    color_bg = RGBColor(248, 249, 250)         # Off-white background
    color_text_dark = RGBColor(33, 37, 41)     # Dark slate for main text
    color_text_muted = RGBColor(108, 117, 125) # Gray for descriptions
    color_track = RGBColor(222, 226, 230)      # Light gray for track
    
    # Milestone specific colors (Cyan, Indigo, Orange, Green, Purple)
    ms_colors = [
        RGBColor(0, 191, 255),
        RGBColor(102, 16, 242),
        RGBColor(253, 126, 20),
        RGBColor(40, 167, 69),
        RGBColor(111, 66, 193)
    ]

    # Sample Data
    milestones = [
        {"date": "2021", "title": "Setting Sail", "desc": "Launched our new product line and entered a new market segment."},
        {"date": "2022", "title": "Full Steam Ahead", "desc": "Achieved record-breaking sales and opened a new office in New York."},
        {"date": "2023", "title": "Navigating Waters", "desc": "Successfully pivoted our business model towards recurring revenue."},
        {"date": "2024", "title": "Charting Course", "desc": "Set ambitious goals for the future and launched our AI platform."},
        {"date": "2025", "title": "Laying Foundation", "desc": "Secured $10M in Series A funding to build our core technology team."}
    ]

    # Set background color
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color_bg

    # --- Draw Header Title ---
    title_box = slide.shapes.add_textbox(Inches(start_x), Inches(0.5), Inches(8), Inches(1))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.bold = True
    p.font.size = Pt(36)
    p.font.color.rgb = color_text_dark

    sub_box = slide.shapes.add_textbox(Inches(start_x), Inches(1.1), Inches(8), Inches(0.5))
    tf_sub = sub_box.text_frame
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = body_text
    p_sub.font.size = Pt(16)
    p_sub.font.color.rgb = color_text_muted

    # --- Draw Main Horizontal Track ---
    track = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 
        Inches(start_x - 0.2), Inches(track_y - 0.05), Inches(track_width + 0.4), Inches(0.1)
    )
    track.fill.solid()
    track.fill.fore_color.rgb = color_track
    track.line.fill.background() # No border

    # --- Draw Milestones ---
    num_nodes = len(milestones)
    spacing = track_width / (num_nodes - 1) if num_nodes > 1 else 0

    node_radius = 0.15
    outer_radius = 0.25

    for i, ms in enumerate(milestones):
        x_center = start_x + (i * spacing)
        is_top = (i % 2 == 0) # Alternate layout
        
        node_color = ms_colors[i % len(ms_colors)]
        
        # Determine vertical placement logic
        stem_length = 1.0
        if is_top:
            stem_start_y = track_y - outer_radius
            stem_end_y = stem_start_y - stem_length
            box_y = stem_end_y - 1.5 # Text box grows down, so place it above stem
        else:
            stem_start_y = track_y + outer_radius
            stem_end_y = stem_start_y + stem_length
            box_y = stem_end_y + 0.1 # Text box starts below stem

        # Draw Vertical Stem (Dashed line)
        stem = slide.shapes.add_connector(
            1, # straight connector
            Inches(x_center), Inches(track_y), Inches(x_center), Inches(stem_end_y)
        )
        stem.line.solid()
        stem.line.fore_color.rgb = color_track
        stem.line.width = Pt(2)
        stem.line.dash_style = 2 # 2 is usually dashed/dotted in python-pptx

        # Draw Node (Outer Circle - White)
        outer_circle = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, 
            Inches(x_center - outer_radius), Inches(track_y - outer_radius), 
            Inches(outer_radius * 2), Inches(outer_radius * 2)
        )
        outer_circle.fill.solid()
        outer_circle.fill.fore_color.rgb = RGBColor(255, 255, 255)
        outer_circle.line.solid()
        outer_circle.line.fore_color.rgb = color_track
        outer_circle.line.width = Pt(2)

        # Draw Node (Inner Circle - Colored)
        inner_circle = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, 
            Inches(x_center - node_radius), Inches(track_y - node_radius), 
            Inches(node_radius * 2), Inches(node_radius * 2)
        )
        inner_circle.fill.solid()
        inner_circle.fill.fore_color.rgb = node_color
        inner_circle.line.fill.background()

        # Draw Content Box
        box_width = 2.0
        content_box = slide.shapes.add_textbox(
            Inches(x_center - (box_width / 2)), Inches(box_y), 
            Inches(box_width), Inches(1.5)
        )
        tf = content_box.text_frame
        tf.word_wrap = True
        
        # We need 3 paragraphs: Date, Title, Desc
        p_date = tf.paragraphs[0]
        p_date.text = ms["date"]
        p_date.alignment = PP_ALIGN.CENTER
        p_date.font.bold = True
        p_date.font.size = Pt(28)
        p_date.font.color.rgb = node_color

        p_title = tf.add_paragraph()
        p_title.text = ms["title"]
        p_title.alignment = PP_ALIGN.CENTER
        p_title.font.bold = True
        p_title.font.size = Pt(14)
        p_title.font.color.rgb = color_text_dark
        p_title.space_before = Pt(5)

        p_desc = tf.add_paragraph()
        p_desc.text = ms["desc"]
        p_desc.alignment = PP_ALIGN.CENTER
        p_desc.font.size = Pt(11)
        p_desc.font.color.rgb = color_text_muted
        p_desc.space_before = Pt(5)

    prs.save(output_pptx_path)
    return output_pptx_path
```