# Winding Serpentine Roadmap

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Winding Serpentine Roadmap

* **Core Visual Mechanism**: The defining visual signature is a continuous, thick, winding "S-curve" path that traverses the slide horizontally. It is styled to look like a physical road (dark asphalt base with a dashed white center line). Circular milestone nodes are placed sequentially along the curves, acting as anchors for alternating text descriptions.
* **Why Use This Skill (Rationale)**: The winding road is a universally understood metaphor for a journey, process, or timeline. The serpentine shape naturally guides the viewer's eye across the entire slide in a measured, sequential flow, preventing the visual fatigue often caused by dense, linear bullet points or rigid Gantt charts. Alternating text placement creates a balanced, harmonious composition.
* **Overall Applicability**: Ideal for strategic planning, product development timelines, project milestones, onboarding journeys, or any multi-step chronological narrative.
* **Value Addition**: Transforms a dry sequence of events into an engaging, story-driven visual. It elevates the perceived professionalism of the presentation by using vector-based custom pathing rather than standard smart-art blocks.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **The Road**: A custom geometric freeform path. Base layer is thick and dark `(50, 50, 50)`, overlaid with a thin, dashed white line `(255, 255, 255)` following the exact same coordinates.
  - **Milestone Nodes**: Pure white circular nodes `(255, 255, 255)` with a thick accent border (e.g., bright blue `(9, 132, 227)`), containing bold, centered step numbers.
  - **Connectors**: Subtle, dotted gray lines `(180, 180, 180)` linking nodes to their respective text boxes, ensuring clarity.
  - **Typography**: Clean hierarchy. Step titles match the accent color; body text is a muted dark gray `(100, 100, 100)`.

* **Step B: Compositional Style**
  - **Spatial Flow**: Left-to-Right, dropping down, Right-to-Left, dropping down, Left-to-Right. (A 3-tier 'Z' or 'S' shape).
  - **Alternating Balance**: Text boxes are explicitly placed either above or below the road depending on the segment, filling the negative space created by the curves without overlapping.

* **Step C: Dynamic Effects & Transitions**
  - The static composition is highly dynamic on its own due to the curves. In PowerPoint, this layout pairs perfectly with a "Wipe" animation (from left/right respectively for each segment) to reveal the road sequentially.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Serpentine Road Path** | `python-pptx` + Custom Math (`FreeformBuilder`) | Generating exact X/Y points using trigonometric functions allows us to draw perfectly smooth, editable vector curves directly in PPTX, bypassing the need for low-res images. |
| **Dashed Center Line** | `python-pptx` (Line formatting) | By duplicating the custom freeform path and applying `MSO_LINE.DASH`, we create a perfect road aesthetic natively. |
| **Drop Shadows & Clean Fills** | `lxml` XML injection | `python-pptx` struggles to apply `noFill` to freeform paths and lacks a native drop shadow API. XML injection precisely styles the nodes and cleans up the path backgrounds. |

> **Feasibility Assessment**: 100% reproducible. By calculating the mathematical points for the arcs and lines, we can generate a perfectly crisp, fully editable native PowerPoint shape that perfectly mimics the reference video's roadmap.

#### 3b. Complete Reproduction Code

```python
import math
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN
from pptx.oxml import parse_xml
from lxml import etree

def create_slide(
    output_pptx_path: str,
    title_text: str = "Strategic Roadmap",
    body_text: str = "A clear path to achieving our key milestones.",
    bg_palette: str = "white",
    accent_color: tuple = (9, 132, 227),  # Bright Blue
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Winding Serpentine Roadmap effect.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # --- Helper Functions ---
    def get_arc_points(cx, cy, r, start_theta, end_theta, steps=30):
        """Generate (x,y) tuples for an arc using trigonometry."""
        points = []
        step = (end_theta - start_theta) / steps
        for i in range(steps + 1):
            theta = start_theta + i * step
            px = cx + r * math.cos(theta)
            py = cy + r * math.sin(theta)
            points.append((px, py))
        return points

    def force_no_fill(shape):
        """Injects XML to ensure a freeform line has absolutely no background fill."""
        spPr = shape.element.spPr
        for child in list(spPr):
            if child.tag.endswith('Fill'):
                spPr.remove(child)
        no_fill = parse_xml(r'<a:noFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>')
        ln = spPr.find('{http://schemas.openxmlformats.org/drawingml/2006/main}ln')
        if ln is not None:
            ln.addprevious(no_fill)
        else:
            spPr.append(no_fill)

    def add_shadow(shape):
        """Injects XML to add a subtle drop shadow to nodes."""
        spPr = shape.element.spPr
        effectLst = parse_xml(
            '<a:effectLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
            '<a:outerShdw blurRad="38100" dist="38100" dir="2700000" algn="tl" rotWithShape="0">'
            '<a:srgbClr val="000000"><a:alpha val="30000"/></a:srgbClr>'
            '</a:outerShdw>'
            '</a:effectLst>'
        )
        spPr.append(effectLst)

    # --- 1. Background Setup ---
    # Solid light background for clean contrast
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(248, 249, 250)
    bg.line.fill.background()

    # Title Text
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(8), Inches(1))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = RGBColor(45, 52, 54)
    
    p2 = tf.add_paragraph()
    p2.text = body_text
    p2.font.size = Pt(16)
    p2.font.color.rgb = RGBColor(100, 100, 100)

    # --- 2. Calculate Road Coordinates ---
    points = []
    # Segment 1: Top straight line (L to R)
    points.append((Inches(1.0), Inches(2.5)))
    points.append((Inches(10.5), Inches(2.5)))
    
    # Segment 2: Right turn semi-circle
    # Center X = 10.5, Center Y = 3.5, Radius = 1.0. Angles: -90 deg to +90 deg
    arc1 = get_arc_points(Inches(10.5), Inches(3.5), Inches(1.0), -0.5*math.pi, 0.5*math.pi)
    points.extend(arc1[1:]) 
    
    # Segment 3: Middle straight line (R to L)
    points.append((Inches(2.5), Inches(4.5)))
    
    # Segment 4: Left turn semi-circle
    # Center X = 2.5, Center Y = 5.5, Radius = 1.0. Angles: 270 deg to 90 deg (moving backwards)
    arc2 = get_arc_points(Inches(2.5), Inches(5.5), Inches(1.0), 1.5*math.pi, 0.5*math.pi)
    points.extend(arc2[1:])
    
    # Segment 5: Bottom straight line (L to R)
    points.append((Inches(12.5), Inches(6.5)))

    # --- 3. Draw The Road ---
    # Base dark road
    builder_base = slide.shapes.build_freeform(points[0][0], points[0][1])
    builder_base.add_line_segments(points[1:])
    road_base = builder_base.convert_to_shape()
    force_no_fill(road_base)
    road_base.line.width = Pt(45)
    road_base.line.color.rgb = RGBColor(50, 50, 50) # Dark Asphalt
    
    # Dashed center line
    builder_dash = slide.shapes.build_freeform(points[0][0], points[0][1])
    builder_dash.add_line_segments(points[1:])
    road_dash = builder_dash.convert_to_shape()
    force_no_fill(road_dash)
    road_dash.line.width = Pt(3)
    road_dash.line.color.rgb = RGBColor(255, 255, 255)
    from pptx.enum.shapes import MSO_LINE
    road_dash.line.dash_style = MSO_LINE.DASH

    # --- 4. Define and Draw Nodes & Content ---
    nodes_config = [
        {"id": "01", "x": Inches(3.0), "y": Inches(2.5), "pos": "top"},
        {"id": "02", "x": Inches(8.5), "y": Inches(2.5), "pos": "bottom"},
        {"id": "03", "x": Inches(8.5), "y": Inches(4.5), "pos": "top"}, # Hit first going left
        {"id": "04", "x": Inches(4.5), "y": Inches(4.5), "pos": "bottom"},
        {"id": "05", "x": Inches(7.5), "y": Inches(6.5), "pos": "top"},
    ]

    for node in nodes_config:
        nx, ny = node['x'], node['y']
        r = Inches(0.35)
        
        # Determine text placement and connector coordinates
        tw, th = Inches(2.4), Inches(1.2)
        tx = nx - tw/2
        
        if node['pos'] == 'top':
            ty = ny - Inches(0.6) - th
            cx_start, cy_start = nx, ny - r
            cx_end, cy_end = nx, ty + th
        else:
            ty = ny + Inches(0.6)
            cx_start, cy_start = nx, ny + r
            cx_end, cy_end = nx, ty

        # Draw Connector Line
        conn = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, cx_start, cy_start, cx_end, cy_end)
        conn.line.color.rgb = RGBColor(150, 150, 150)
        conn.line.width = Pt(1.5)
        conn.line.dash_style = MSO_LINE.ROUND_DOT

        # Draw Text Box
        tb = slide.shapes.add_textbox(tx, ty, tw, th)
        tf_tb = tb.text_frame
        
        p_title = tf_tb.paragraphs[0]
        p_title.text = f"Phase {node['id']}"
        p_title.font.bold = True
        p_title.font.size = Pt(14)
        p_title.font.color.rgb = RGBColor(*accent_color)
        if node['pos'] == 'top':
            p_title.alignment = PP_ALIGN.CENTER
        else:
            p_title.alignment = PP_ALIGN.CENTER
            
        p_desc = tf_tb.add_paragraph()
        p_desc.text = "Add sub-text here to describe the specific goals of this step."
        p_desc.font.size = Pt(11)
        p_desc.font.color.rgb = RGBColor(100, 100, 100)
        p_desc.alignment = PP_ALIGN.CENTER

        # Draw Node Circle (drawn last so it sits on top of connectors)
        circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, nx - r, ny - r, r*2, r*2)
        circle.fill.solid()
        circle.fill.fore_color.rgb = RGBColor(255, 255, 255)
        circle.line.color.rgb = RGBColor(*accent_color)
        circle.line.width = Pt(4)
        add_shadow(circle)

        # Number inside Node
        # Text alignment inside circles in pptx can be finicky, a perfectly placed textbox is more robust
        num_box = slide.shapes.add_textbox(nx - r, ny - r + Inches(0.05), r*2, r*2) # slight Y adjustment for visual center
        tf_num = num_box.text_frame
        tf_num.text = node['id']
        p_num = tf_num.paragraphs[0]
        p_num.alignment = PP_ALIGN.CENTER
        p_num.font.size = Pt(14)
        p_num.font.bold = True
        p_num.font.color.rgb = RGBColor(*accent_color)
        
        # Zero out margins to ensure centering
        tf_num.margin_left = 0
        tf_num.margin_right = 0
        tf_num.margin_top = 0
        tf_num.margin_bottom = 0

    prs.save(output_pptx_path)
    return output_pptx_path
```