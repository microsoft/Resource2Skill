# Swimlane Process Flowchart

## Analysis

An essential framework for mapping cross-functional business processes, visualizing both the sequence of events and the distinct responsibilities of different roles.

### 1. High-level Design Pattern Extraction

> **Skill Name**: Swimlane Process Flowchart

* **Core Visual Mechanism**: A grid-based layout where horizontal bands ("swimlanes") represent different departments, systems, or actors. Standard flowchart nodes (Start, Process, Decision, Database) are plotted on this coordinate system and connected by elbow arrows, explicitly mapping logical steps to their respective owners.
* **Why Use This Skill (Rationale)**: Traditional flowcharts show *what* happens and *when*, but struggle to show *who* does it. Swimlanes solve this by using spatial grouping to define responsibility. This visual separation instantly highlights hand-offs between teams, bottlenecks, and cross-departmental dependencies.
* **Overall Applicability**: Ideal for Standard Operating Procedures (SOPs), system architecture diagrams, business process re-engineering, and onboarding materials.
* **Value Addition**: Transforms a basic process map into an organizational diagnostic tool. The alternating background colors and strict horizontal alignment create a polished, "enterprise-grade" aesthetic that is easily readable even for complex workflows.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  * **Background Grid**: A vertical separator for headers and alternating light-fill horizontal bands to define lanes, replacing heavy table borders.
  * **Color Logic**:
    * **Primary Shapes**: Vibrant accent color (e.g., Deep Orange `(255, 140, 0)`) for high visibility of standard processes.
    * **Decisions**: White fill `(255, 255, 255)` with an accent-colored border to make the diamond shape stand out.
    * **Alternative/System Nodes**: Light grey `(245, 245, 245)` for databases or rejected paths, visually de-emphasizing them.
    * **Lanes**: Alternating white and ultra-light grey `(245, 245, 250)` for subtle reading guides.
  * **Text Hierarchy**: Large dark title -> Medium bold lane headers -> Small bold node labels -> Extra-small connector labels (Yes/No).

* **Step B: Compositional Style**
  * Left-aligned anchor column (approx. 15% of width) containing role headers.
  * Process flows strictly left-to-right to signify time/sequence, and up/down to signify cross-team hand-offs.
  * Uniform spacing (e.g., 0.8 to 1.0 inches between nodes) ensures the automated elbow connectors route cleanly without overlapping.

* **Step C: Dynamic Effects & Transitions**
  * Static display layout. The visual hierarchy relies purely on spatial positioning rather than animation.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Swimlane Grid & Nodes** | `python-pptx` native | Rectangles and native shapes (`MSO_SHAPE`) keep the flowchart fully text-editable in PPTX. |
| **Connector Arrowheads** | `lxml` XML injection | `python-pptx` cannot natively add arrowheads to connectors. Directly appending `<a:tailEnd type="triangle"/>` to the shape XML ensures standard flowchart styling. |
| **Routing Labels (Yes/No)** | Math & native TextBoxes | PPTX doesn't bind text to connectors natively; we calculate the midpoint of the connector's first segment and place a white-background textbox. |

> **Feasibility Assessment**: 100% reproduction. By combining native shapes with OpenXML manipulation for arrowheads, we create a fully-featured, editable flowchart matching the tutorial's output.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "Cross-Functional Swimlane Flowchart",
    body_text: str = "",
    bg_palette: str = "business", 
    accent_color: tuple = (255, 140, 0),  # Deep Orange
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Swimlane Flowchart visual effect.
    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
    from pptx.enum.text import PP_ALIGN
    from pptx.dml.color import RGBColor
    from pptx.oxml.ns import qn
    from pptx.oxml import parse_xml

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Colors
    c_accent = RGBColor(*accent_color)
    c_white = RGBColor(255, 255, 255)
    c_dark_txt = RGBColor(60, 60, 60)
    c_border = RGBColor(160, 160, 160)
    c_lane_alt = RGBColor(245, 245, 250)

    # === Layer 1: Title ===
    title = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(10), Inches(0.6))
    title.text = title_text
    p = title.text_frame.paragraphs[0]
    p.font.size = Pt(28)
    p.font.color.rgb = c_dark_txt
    p.font.bold = True

    # === Layer 2: Swimlane Grid ===
    lanes = ["Customer", "Sales Team", "Operations", "System / DB"]
    y_start = 1.0
    lane_h = 1.5

    for i, name in enumerate(lanes):
        y = y_start + i * lane_h
        
        # Alternating background fill
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(y), Inches(12.3), Inches(lane_h))
        bg.line.fill.background()
        bg.fill.solid()
        bg.fill.fore_color.rgb = c_lane_alt if i % 2 == 0 else c_white

        # Thin top divider line
        line = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(0.5), Inches(y), Inches(12.8), Inches(y))
        line.line.color.rgb = RGBColor(220, 220, 225)
        
        # Lane Header Text
        tb = slide.shapes.add_textbox(Inches(0.5), Inches(y + 0.5), Inches(1.35), Inches(0.5))
        tb.text = name
        tp = tb.text_frame.paragraphs[0]
        tp.font.bold = True
        tp.font.size = Pt(11)
        tp.font.color.rgb = RGBColor(100, 100, 100)
        tp.alignment = PP_ALIGN.RIGHT

    # Bottom border line
    line = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(0.5), Inches(y_start + 4*lane_h), Inches(12.8), Inches(y_start + 4*lane_h))
    line.line.color.rgb = RGBColor(220, 220, 225)

    # Vertical Header Separator
    vline = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(2.0), Inches(y_start), Inches(2.0), Inches(y_start + 4*lane_h))
    vline.line.color.rgb = RGBColor(220, 220, 225)


    # === Layer 3: Flowchart Nodes ===
    def add_node(shape_type, text, lane_idx, x_inch, w_inch=1.2, h_inch=0.6, fill=None, outline=None, font_clr=c_white):
        # Calculate Y center based on lane index (1-based)
        y_center = y_start + (lane_idx - 0.5) * lane_h
        y_inch = y_center - (h_inch / 2)
        
        shape = slide.shapes.add_shape(shape_type, Inches(x_inch), Inches(y_inch), Inches(w_inch), Inches(h_inch))
        shape.text = text
        
        # Style Shape
        shape.fill.solid()
        if fill: shape.fill.fore_color.rgb = fill
        if outline: 
            shape.line.color.rgb = outline
            shape.line.width = Pt(1.5)
        else: shape.line.fill.background()
            
        # Style Text
        shape.text_frame.word_wrap = True
        shape.text_frame.margin_left = Pt(2)
        shape.text_frame.margin_right = Pt(2)
        for paragraph in shape.text_frame.paragraphs:
            paragraph.alignment = PP_ALIGN.CENTER
            for run in paragraph.runs:
                run.font.size = Pt(9) if shape_type == MSO_SHAPE.FLOWCHART_DECISION else Pt(10)
                run.font.bold = True
                run.font.color.rgb = font_clr
        return shape

    # Instantiate the process steps
    n1 = add_node(MSO_SHAPE.FLOWCHART_TERMINAL, "Start", 1, 2.5, fill=c_accent)
    n2 = add_node(MSO_SHAPE.ROUNDED_RECTANGLE, "Receive\nOrder", 2, 4.5, fill=c_accent)
    n3 = add_node(MSO_SHAPE.FLOWCHART_DECISION, "Valid?", 2, 6.5, w_inch=1.1, h_inch=0.9, fill=c_white, outline=c_accent, font_clr=c_dark_txt)
    n4 = add_node(MSO_SHAPE.ROUNDED_RECTANGLE, "Reject\nOrder", 3, 6.5, fill=RGBColor(210, 210, 210), font_clr=c_dark_txt)
    n5 = add_node(MSO_SHAPE.ROUNDED_RECTANGLE, "Process\nFulfillment", 2, 8.5, fill=c_accent)
    n6 = add_node(MSO_SHAPE.CAN, "Database", 4, 8.5, fill=c_white, outline=c_border, font_clr=c_dark_txt)
    n7 = add_node(MSO_SHAPE.FLOWCHART_TERMINAL, "End", 1, 11.0, fill=c_accent)


    # === Layer 4: Connectors & Logic ===
    def inject_arrowhead(connector):
        """XML hack to add an arrowhead to a pptx connector."""
        spPr = connector.element.spPr
        ln = spPr.find(qn('a:ln'))
        if ln is None:
            ln = parse_xml(r'<a:ln xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>')
            spPr.append(ln)
        tailEnd = ln.find(qn('a:tailEnd'))
        if tailEnd is None:
            tailEnd = parse_xml(r'<a:tailEnd xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" type="triangle"/>')
            ln.append(tailEnd)
        else:
            tailEnd.set('type', 'triangle')

    def connect(s1, site1, s2, site2, text=None):
        # site mapping (approx): 0=Top, 1=Right, 2=Bottom, 3=Left
        connector = slide.shapes.add_connector(MSO_CONNECTOR.ELBOW, Inches(0), Inches(0), Inches(1), Inches(1))
        connector.begin_connect(s1, site1)
        connector.end_connect(s2, site2)
        connector.line.color.rgb = c_border
        connector.line.width = Pt(1.5)
        inject_arrowhead(connector)
        
        # Add labels for Decision routes
        if text:
            # Estimate label placement
            if site1 == 1: # Moving Right
                mx, my = (s1.left + s1.width + s2.left) / 2, s1.top + (s1.height/2)
            elif site1 == 2: # Moving Down
                mx, my = s1.left + (s1.width/2), (s1.top + s1.height + s2.top) / 2
            else:
                mx, my = (s1.left + s2.left)/2, (s1.top + s2.top)/2
                
            tb = slide.shapes.add_textbox(mx - Inches(0.25), my - Inches(0.2), Inches(0.5), Inches(0.4))
            tb.text = text
            tb.fill.solid()
            tb.fill.fore_color.rgb = c_white # opaque background overlays the line perfectly
            tb.text_frame.margin_left = tb.text_frame.margin_right = Pt(0)
            tb.text_frame.margin_top = tb.text_frame.margin_bottom = Pt(0)
            
            p = tb.text_frame.paragraphs[0]
            p.font.size = Pt(10)
            p.font.bold = True
            p.font.color.rgb = c_dark_txt
            p.alignment = PP_ALIGN.CENTER

    # Route the Flow
    connect(n1, 2, n2, 3)          # Start (Bottom) to Receive (Left)
    connect(n2, 1, n3, 3)          # Receive (Right) to Decision (Left)
    connect(n3, 2, n4, 0, "No")    # Decision (Bottom) to Reject (Top)
    connect(n3, 1, n5, 3, "Yes")   # Decision (Right) to Process (Left)
    connect(n5, 2, n6, 0)          # Process (Bottom) to DB (Top)
    connect(n5, 1, n7, 3)          # Process (Right) to End (Left)

    prs.save(output_pptx_path)
    return output_pptx_path
```