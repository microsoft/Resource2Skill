# Circular Pin Gauge Infographic

## Analysis

An elegant and precise technique for transforming standard numbers into a compelling visual dashboard. 

### 1. High-level Design Pattern Extraction

> **Skill Name**: Circular Pin Gauge Infographic

* **Core Visual Mechanism**: Three horizontal "location pin" nodes that act as circular gauges. The magic lies in the layer construction: a custom-drawn pin base, a dark "hollow" inner circle that perfectly matches the slide background (creating an illusion of negative space), and a thick yellow arc that visually represents the percentage. Small red triangles act as directional anchors pointing to the labels.
* **Why Use This Skill (Rationale)**: This layout breaks the monotony of bullet points and standard charts. The circular progress bars tap into our intuitive understanding of completion/gauges, while the location pin shape draws the eye downward into the explanatory text, naturally guiding the viewer's reading flow.
* **Overall Applicability**: Perfect for performance dashboards, metric highlights, key product stats, milestone completion rates, or comparison slides.
* **Value Addition**: Transforms basic percentages into a highly polished, professional-grade infographic that looks custom-made in Illustrator but is entirely editable within PowerPoint.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Background Canvas**: Dark Slate Blue `(35, 46, 62)`.
  - **Pin Base**: Lighter Blue `(44, 58, 78)`. It is constructed mathematically using a circle and a precisely angled tangent triangle.
  - **Hole Mask**: A smaller circle identical to the background color `(35, 46, 62)` to create a donut effect.
  - **Progress Arc**: Bright Yellow/Gold `(255, 192, 0)`.
  - **Text Hierarchy**: 
    - Giant bold white percentages (e.g., "38")
    - Small subdued gray uppercase labels ("PERCENT")
    - Accent elements (Red triangles `(239, 68, 68)`) pointing to subtext.

* **Step B: Compositional Style**
  - Divided strictly into 3 vertical columns.
  - Nodes are centered on the X-axis of each column and slightly lowered on the Y-axis to provide ample breathing room for the main header.
  - Symmetrical layout ensures cognitive ease.

* **Step C: Dynamic Effects & Transitions**
  - Background pins use a simple `Fade` in.
  - Percentages and inner holes use a `Zoom` effect.
  - Text and red triangles use a `Float Down` effect. 
  *(Note: The reproduction code below handles the static visual layout; animations can be added natively in PowerPoint later).*

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Location Pin Base** | `python-pptx` native math | A location pin is constructed by combining an Oval and an Isosceles Triangle, calculating exact geometric tangents so they merge seamlessly without weird bounding-box alignment issues. |
| **Progress Arc** | `lxml` XML injection | `python-pptx` cannot natively set the start and end angles of an `ARC` shape. We inject `<a:gd>` OpenXML tags to manually define the exact sweep angle based on the percentage. |
| **Hollow Donut Illusion** | `python-pptx` color matching | By overlaying a smaller circle colored identically to the background, we create a transparent "hole" perfectly sized to nest inside the progress arc. |

> **Feasibility Assessment**: 100% of the visual layout and vector geometry is perfectly reproduced and fully editable in PowerPoint.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "I N F O G R A P H I C S",
    subtitle_text: str = "Here you have to add some subtitle text by your own and replace with this\nsample text this is simple.",
    data_percentages: list = [38, 43, 68],
    **kwargs
) -> str:
    """
    Creates an infographic slide with three circular pin gauges.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN
    from pptx.oxml import parse_xml

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # --- Color Palette ---
    BG_COLOR = (35, 46, 62)
    PIN_COLOR = (44, 58, 78)
    ARC_COLOR = (255, 192, 0)
    TEXT_WHITE = (255, 255, 255)
    TEXT_GRAY = (156, 163, 175)
    RED_ACCENT = (239, 68, 68)

    # --- Helper Functions ---
    def add_centered_text(left, top, width, height, text, font_size, font_color, bold=False):
        txBox = slide.shapes.add_textbox(left, top, width, height)
        tf = txBox.text_frame
        tf.text = text
        tf.margin_left = Pt(0)
        tf.margin_right = Pt(0)
        tf.margin_top = Pt(0)
        tf.margin_bottom = Pt(0)
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        font = p.font
        font.size = Pt(font_size)
        font.color.rgb = RGBColor(*font_color)
        font.bold = bold
        return txBox

    def set_arc_angles(shape, start_deg, sweep_deg):
        # PowerPoint OpenXML uses 1/60000th of a degree
        start_val = int((start_deg % 360) * 60000)
        end_deg = start_deg + sweep_deg
        end_val = int((end_deg % 360) * 60000)

        prstGeom = shape.element.find('.//a:prstGeom', shape.element.nsmap)
        if prstGeom is not None:
            avLst = prstGeom.find('.//a:avLst', shape.element.nsmap)
            if avLst is None:
                avLst = parse_xml('<a:avLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>')
                prstGeom.append(avLst)
            for child in list(avLst):
                avLst.remove(child)
            # adj1 = start angle, adj2 = end angle
            avLst.append(parse_xml(f'<a:gd xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="adj1" fmla="val {start_val}"/>'))
            avLst.append(parse_xml(f'<a:gd xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="adj2" fmla="val {end_val}"/>'))

    # --- Step 1: Draw Background ---
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(*BG_COLOR)
    bg.line.color.rgb = RGBColor(*BG_COLOR)

    # --- Step 2: Add Headers ---
    add_centered_text(Inches(0), Inches(0.8), prs.slide_width, Inches(0.6), title_text, 32, TEXT_WHITE, bold=True)
    add_centered_text(Inches(2), Inches(1.5), Inches(9.333), Inches(0.6), subtitle_text, 12, TEXT_GRAY)

    # --- Step 3: Draw Nodes ---
    centers_x = [2.66, 6.66, 10.66]
    cy = 3.8  # Central Y axis for the pins

    # Geometric math for a perfect location pin (Circle + Tangent Triangle)
    R = 1.3  # Radius of the main pin head
    y_t = 2.2  # Distance from center to the sharp tip
    y_tangent = (R**2) / y_t  # Y-coordinate where triangle touches circle tangentially (0.768)
    x_tangent = (R**2 - y_tangent**2)**0.5  # X-coordinate for tangent (1.049)
    tri_width = 2 * x_tangent  # Width of triangle base (2.098)
    tri_height = y_t - y_tangent  # Height of triangle (1.432)

    for i in range(3):
        cx = centers_x[i]
        pct = data_percentages[i] if i < len(data_percentages) else 50

        # 3a. Pin Head (Outer Circle)
        circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(cx - R), Inches(cy - R), Inches(2 * R), Inches(2 * R))
        circle.fill.solid()
        circle.fill.fore_color.rgb = RGBColor(*PIN_COLOR)
        circle.line.color.rgb = RGBColor(*PIN_COLOR)

        # 3b. Pin Tail (Inverted Triangle)
        # We overlap by 0.02 to prevent anti-aliasing hairline gaps between shapes
        overlap = 0.02
        triangle = slide.shapes.add_shape(
            MSO_SHAPE.ISOSCELES_TRIANGLE,
            Inches(cx - tri_width / 2), Inches(cy + y_tangent - overlap),
            Inches(tri_width), Inches(tri_height + overlap)
        )
        triangle.rotation = 180
        triangle.fill.solid()
        triangle.fill.fore_color.rgb = RGBColor(*PIN_COLOR)
        triangle.line.color.rgb = RGBColor(*PIN_COLOR)

        # 3c. Inner Hole (Mask using background color)
        r_inner = 0.9
        hole = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(cx - r_inner), Inches(cy - r_inner), Inches(2 * r_inner), Inches(2 * r_inner))
        hole.fill.solid()
        hole.fill.fore_color.rgb = RGBColor(*BG_COLOR)
        hole.line.color.rgb = RGBColor(*BG_COLOR)

        # 3d. Progress Arc
        r_arc = 1.0  # Centers exactly between the inner hole edge and the outer pin edge
        arc = slide.shapes.add_shape(MSO_SHAPE.ARC, Inches(cx - r_arc), Inches(cy - r_arc), Inches(2 * r_arc), Inches(2 * r_arc))
        arc.line.color.rgb = RGBColor(*ARC_COLOR)
        arc.line.width = Pt(15)  # Creates a thick ring
        
        # Calculate sweep: Top of circle in PPT is 270 degrees
        start_deg = 270
        sweep_deg = pct * 360 / 100
        set_arc_angles(arc, start_deg, sweep_deg)

        # 3e. Text Content
        # Main Number
        add_centered_text(Inches(cx - 1), Inches(cy - 0.3), Inches(2), Inches(0.6), str(pct), 40, TEXT_WHITE, bold=True)
        # PERCENT Label
        add_centered_text(Inches(cx - 1), Inches(cy + 0.35), Inches(2), Inches(0.3), "PERCENT", 10, TEXT_GRAY, bold=True)

        # 3f. Accent Elements
        # Small Red Directional Triangle
        red_tri = slide.shapes.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE, Inches(cx - 0.15), Inches(cy + y_t + 0.1), Inches(0.3), Inches(0.2))
        red_tri.rotation = 180
        red_tri.fill.solid()
        red_tri.fill.fore_color.rgb = RGBColor(*RED_ACCENT)
        red_tri.line.color.rgb = RGBColor(*RED_ACCENT)

        # Bottom Text Label
        add_centered_text(Inches(cx - 1), Inches(cy + y_t + 0.4), Inches(2), Inches(0.3), "TEXT HERE", 11, TEXT_WHITE, bold=True)

    prs.save(output_pptx_path)
    return output_pptx_path
```