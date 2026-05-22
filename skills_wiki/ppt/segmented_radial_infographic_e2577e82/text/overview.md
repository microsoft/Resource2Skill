# Segmented Radial Infographic

## Analysis

# Skill Strategy Document

### 1. High-level Design Pattern Extraction

> **Skill Name**: Segmented Radial Infographic

* **Core Visual Mechanism**: The defining visual signature is a segmented, 270-degree "arch" or "doughnut" chart functioning as a central focal point. The arc is procedurally divided into perfectly spaced geometric segments, each paired with radial connector lines that branch out horizontally to beautifully aligned text blocks. 
* **Why Use This Skill (Rationale)**: This layout leverages radial symmetry, which naturally draws the viewer's eye to the center (the core concept/hub) while systematically distributing supporting information around the perimeter. It effectively visually groups "parts of a whole" without resorting to a standard, overused pie chart or bulleted list. 
* **Overall Applicability**: Ideal for business strategy presentations, phase-by-phase roadmaps, core-value representations, or conceptual diagrams where multiple components revolve around a single central idea.
* **Value Addition**: Transforms a standard list of 3-5 items into a premium, custom-illustrated graphic. It brings a "consulting-firm" level of polish to the slide, making the information feel structured, interconnected, and highly professional.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Radial Segments**: Thick, curved vector shapes mimicking a doughnut chart but with a large open gap at the bottom (start angle ~135°, end angle ~405°).
  - **Color Logic**: A high-contrast corporate palette. Representative RGBA values:
    - Red: `(218, 56, 50, 255)`
    - Dark Navy: `(19, 41, 75, 255)`
    - Cyan/Blue: `(0, 114, 206, 255)`
    - Vibrant Yellow: `(255, 192, 0, 255)`
  - **Text Hierarchy**: 
    - Floating segment numbers inside the arcs (white, heavy bold, Pt 22).
    - Connecting node labels with bold colored titles (Pt 16) and grey explanatory body text (Pt 12).
    - A central graphic/icon anchored in the negative space.

* **Step B: Compositional Style**
  - **Spatial Feel**: Centered but slightly top-heavy due to the 90-degree opening at the bottom.
  - **Proportions**: 
    - The central radial graphic occupies the middle 40% of the canvas.
    - Text blocks are cleanly distributed in the left and right margins, consuming the remaining 60% of the width.
    - Connector lines strictly break out radially, then extend purely horizontally to ensure textual alignment remains perfectly clean and readable.

* **Step C: Dynamic Effects & Transitions**
  - *In-Video*: Elements fade and zoom in radially. 
  - *Achievable in Code*: We will focus on constructing the exact static, editable vector geometry.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Segmented Arc Geometry | `python-pptx` `FreeformBuilder` | The video relies on ungrouping SVG charts into editable shapes. We can natively bypass this by mathematically calculating the vertices of the arc segments and drawing true editable PPTX vector polygons. |
| Gap Effect between segments | `python-pptx` Line Formatting | Adding a thick white border to the freeform shapes flawlessly mimics the "gap" or "explosion" effect seen in the video without complex math. |
| Radial Layout & Connectors | `python-pptx` + Trigonometry | Calculating sine/cosine for mid-angles ensures perfectly positioned text numbers, connector lines, and text boxes. |

> **Feasibility Assessment**: 100% — This code produces a fully native, perfectly editable, high-fidelity reproduction of the final infographic shown in the tutorial.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "Segmented Radial Infographic",
    body_text: str = "",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Segmented Radial Infographic visual effect.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
    from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
    import math

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Background ===
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(245, 245, 248)

    # === Slide Title ===
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(10), Inches(1))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = RGBColor(30, 30, 30)

    # === Geometry & Layout Configurations ===
    cx = int(prs.slide_width / 2)
    cy = int(prs.slide_height / 2 + Inches(0.4))
    r_out = Inches(2.2)
    r_in = Inches(1.3)
    
    # 4-Segment Palette and Alignment
    segments = [
        {"color": (218, 56, 50), "align": "right"}, # Red
        {"color": (19, 41, 75),  "align": "right"}, # Navy
        {"color": (0, 114, 206), "align": "left"},  # Blue
        {"color": (255, 192, 0), "align": "left"}   # Yellow
    ]

    # === Helper: Draw Arc Segment ===
    def add_arc_segment(slide_obj, cx_val, cy_val, radius_out, radius_in, start_deg, end_deg, color_rgb):
        steps = max(20, int((end_deg - start_deg) / 2))
        pts = []
        # Outer arc
        for i in range(steps + 1):
            ang = math.radians(start_deg + (end_deg - start_deg) * i / steps)
            pts.append((cx_val + radius_out * math.cos(ang), cy_val + radius_out * math.sin(ang)))
        # Inner arc (reversed)
        for i in range(steps, -1, -1):
            ang = math.radians(start_deg + (end_deg - start_deg) * i / steps)
            pts.append((cx_val + radius_in * math.cos(ang), cy_val + radius_in * math.sin(ang)))
            
        builder = slide_obj.shapes.build_freeform(pts[0][0], pts[0][1])
        builder.add_line_segments(pts[1:], close=True)
        shape = builder.convert_to_shape()
        
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(*color_rgb)
        # White border creates the visual "gap" between segments
        shape.line.color.rgb = RGBColor(245, 245, 248) # Match background
        shape.line.width = Pt(4)
        return shape

    # === Helper: Add Radial Labels & Connectors ===
    def add_radial_label(slide_obj, cx_val, cy_val, radius_out, radius_in, mid_deg, num, title, body, align_type, color_rgb):
        rad = math.radians(mid_deg)
        
        # 1. Floating Number inside the arc
        r_mid = (radius_out + radius_in) / 2 
        nx = cx_val + r_mid * math.cos(rad)
        ny = cy_val + r_mid * math.sin(rad)
        bs = Inches(0.6)
        nb = slide_obj.shapes.add_textbox(int(nx - bs/2), int(ny - bs/2), int(bs), int(bs))
        nb.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_num = nb.text_frame.paragraphs[0]
        p_num.text = f"0{num}"
        p_num.alignment = PP_ALIGN.CENTER
        p_num.font.size = Pt(22)
        p_num.font.bold = True
        p_num.font.color.rgb = RGBColor(255, 255, 255)
        
        # 2. Connector Line
        x_start = cx_val + radius_out * math.cos(rad)
        y_start = cy_val + radius_out * math.sin(rad)
        line_len = Inches(0.5)
        
        w = Inches(2.6)
        h = Inches(1.2)
        
        if align_type == 'right':
            x_end = x_start - line_len
            left = x_end - w
            text_align = PP_ALIGN.RIGHT
        else:
            x_end = x_start + line_len
            left = x_end
            text_align = PP_ALIGN.LEFT
            
        conn = slide_obj.shapes.add_connector(
            MSO_CONNECTOR.STRAIGHT, int(x_start), int(y_start), int(x_end), int(y_start)
        )
        conn.line.color.rgb = RGBColor(*color_rgb)
        conn.line.width = Pt(2)
        
        # 3. Text Box
        top = y_start - h / 2
        tb = slide_obj.shapes.add_textbox(int(left), int(top), int(w), int(h))
        tb.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
        
        p_title = tb.text_frame.paragraphs[0]
        p_title.text = title
        p_title.font.bold = True
        p_title.font.size = Pt(16)
        p_title.font.color.rgb = RGBColor(*color_rgb)
        p_title.alignment = text_align
        
        p_body = tb.text_frame.add_paragraph()
        p_body.text = body
        p_body.font.size = Pt(11)
        p_body.font.color.rgb = RGBColor(100, 100, 100)
        p_body.alignment = text_align

    # === Build Segments ===
    # Total span 270 degrees, starting at bottom-left (135) to bottom-right (405)
    start_angle = 135
    span = 270 / len(segments)
    
    for i, seg in enumerate(segments):
        end_angle = start_angle + span
        mid_angle = (start_angle + end_angle) / 2
        
        # Draw the vector pie segment
        add_arc_segment(slide, cx, cy, r_out, r_in, start_angle, end_angle, seg["color"])
        
        # Add the connected text elements
        add_radial_label(
            slide, cx, cy, r_out, r_in, mid_angle, i+1, 
            f"Phase 0{i+1} Heading", 
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore.", 
            seg["align"], seg["color"]
        )
        
        start_angle = end_angle

    # === Central Hub Graphic ===
    cr = r_in - Inches(0.1)
    center_circle = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, int(cx - cr), int(cy - cr), int(cr * 2), int(cr * 2)
    )
    center_circle.fill.solid()
    center_circle.fill.fore_color.rgb = RGBColor(25, 25, 35) # Dark contrasting hub
    center_circle.line.fill.background()
    
    ctb = slide.shapes.add_textbox(int(cx - cr), int(cy - cr), int(cr*2), int(cr*2))
    ctb.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    cp = ctb.text_frame.paragraphs[0]
    cp.text = "💡" # Represents the core idea
    cp.alignment = PP_ALIGN.CENTER
    cp.font.size = Pt(50)

    prs.save(output_pptx_path)
    return output_pptx_path
```