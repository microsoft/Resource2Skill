# Programmatic Linear Flowchart (SmartArt Alternative)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Programmatic Linear Flowchart (SmartArt Alternative)

* **Core Visual Mechanism**: The defining visual idea is the **sequential logical progression** represented through geometric nodes connected by directional arrows. It relies on perfect mathematical alignment, uniform spacing, and contrasting colors between the focal data nodes and the transitional connectors.
* **Why Use This Skill (Rationale)**: Human cognition processes linear sequences best when they are visually mapped out spatially (left-to-right or top-to-bottom). Replacing a bulleted list with a flowchart forces the viewer to understand the dependency and chronology of the steps.
* **Overall Applicability**: Ideal for process documentation, project milestones, chronological timelines, algorithmic logic, operational procedures, or any "Step 1 -> Step 2 -> Step 3" scenario.
* **Value Addition**: Transforms dense text into an intuitive, easily digestible visual map. Bypasses the rigidity of built-in SmartArt by programmatically generating a clean, customizable manual flowchart layout.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Nodes**: Rounded rectangles containing the core step text.
    - Typical Color: Professional Blue `(31, 73, 125, 255)`.
    - Styling: Flat solid fill, no border, subtle drop shadow to lift them off the canvas.
  - **Connectors**: Block arrows pointing to the next node.
    - Typical Color: Neutral Gray `(165, 165, 165, 255)` to ensure they do not compete with the nodes for attention.
  - **Text Hierarchy**: White, bold sans-serif text `(255, 255, 255, 255)` vertically and horizontally centered within the nodes.
* **Step B: Compositional Style**
  - Linear horizontal progression centered exactly in the middle of the slide canvas.
  - Mathematically calculated equal spacing: The gap between nodes is proportional to the width of the node (e.g., gap is 40% of the node width).
  - Dynamic scaling: Node width adjusts automatically based on the number of steps provided to ensure the entire flowchart fits nicely within a 12-inch safe zone.
* **Step C: Dynamic Effects & Transitions**
  - Statically, it presents the whole process. In PowerPoint, these elements are typically animated using a "Wipe (From Left)" effect, revealing one node and arrow pair at a time.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Perfect alignment & spacing | Math + `python-pptx` | Programmatic calculation is far superior to manual dragging for ensuring pixel-perfect spacing and alignment across arbitrary list lengths. |
| Shapes and text layout | `python-pptx` native | `ROUNDED_RECTANGLE` and `RIGHT_ARROW` shapes natively handle text wrapping and crisp vector rendering. |
| Subtle Drop Shadow | `lxml` XML injection | Native `python-pptx` cannot apply shadow effects to shapes. Modifying the `a:spPr` element directly achieves that "SmartArt" professional polish. |

> **Feasibility Assessment**: 100%. The visual style of a clean, evenly spaced flowchart is fully reproducible. Furthermore, by calculating dynamic widths based on the length of the input list, the programmatic version is more robust than a static template.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "Process Flowchart",
    steps: list = ["Initiation", "Planning", "Execution", "Closure"],
    node_color: tuple = (31, 73, 125),   # Deep Blue
    text_color: tuple = (255, 255, 255), # White
    arrow_color: tuple = (165, 165, 165) # Gray
) -> str:
    """
    Create a PPTX file reproducing a clean, linearly aligned horizontal flowchart.
    
    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.oxml.xmlchemy import OxmlElement

    # Helper function to add a subtle drop shadow to shapes via XML injection
    def add_shadow(shape):
        spPr = shape.element.spPr
        
        # Create effectLst element
        effectLst = OxmlElement('a:effectLst')
        
        # Create outerShdw element
        outerShdw = OxmlElement('a:outerShdw')
        outerShdw.set('blurRad', '50800')   # Blur radius
        outerShdw.set('dist', '38100')      # Distance
        outerShdw.set('dir', '2700000')     # Direction (90 degrees / down)
        outerShdw.set('algn', 'tl')
        
        # Set shadow color and transparency
        srgbClr = OxmlElement('a:srgbClr')
        srgbClr.set('val', '000000')
        alpha = OxmlElement('a:alpha')
        alpha.set('val', '30000') # 30% opacity
        
        srgbClr.append(alpha)
        outerShdw.append(srgbClr)
        effectLst.append(outerShdw)
        
        # Append effectLst to shape properties
        spPr.append(effectLst)

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # --- 1. Add Title ---
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(12.333), Inches(1.0))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0, 0, 0)
    p.alignment = PP_ALIGN.CENTER

    # --- 2. Calculate Dynamic Layout ---
    num_steps = len(steps)
    if num_steps == 0:
        prs.save(output_pptx_path)
        return output_pptx_path

    # We use a maximum of 12 inches for the width to keep margins
    available_width = 12.0
    
    # Calculate node width dynamically so it fits, cap max size at 2.5 inches
    # Assume gap is 40% of the node width
    node_w_val = min(2.5, available_width / (num_steps + (num_steps - 1) * 0.4))
    gap_val = node_w_val * 0.4
    
    total_width = num_steps * node_w_val + (num_steps - 1) * gap_val
    
    # Center the entire flowchart block horizontally and vertically
    start_x = (13.333 - total_width) / 2
    center_y = 4.2  # slightly below exact center to account for title
    
    node_h_inch = Inches(1.2)
    node_w_inch = Inches(node_w_val)
    gap_inch = Inches(gap_val)

    # --- 3. Render Nodes and Connectors ---
    for i, step_text in enumerate(steps):
        x = Inches(start_x) + i * (node_w_inch + gap_inch)
        y = Inches(center_y) - node_h_inch / 2

        # A. Draw Data Node
        shape = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            x, y, node_w_inch, node_h_inch
        )
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(*node_color)
        shape.line.fill.background() # Removes border
        
        # Apply XML drop shadow for depth
        add_shadow(shape)

        # Add step text
        text_frame = shape.text_frame
        text_frame.word_wrap = True
        p = text_frame.paragraphs[0]
        p.text = step_text
        p.font.size = Pt(18)
        p.font.color.rgb = RGBColor(*text_color)
        p.font.bold = True
        p.alignment = PP_ALIGN.CENTER
        
        # Vertical centering (lxml trick)
        shape.text_frame.vertical_anchor = 3 # middle

        # B. Draw Connecting Arrow (if not the last node)
        if i < num_steps - 1:
            arrow_w = gap_inch * 0.8 # slightly shorter than the gap to provide margin
            arrow_x = x + node_w_inch + (gap_inch * 0.1)
            arrow_h = Inches(0.35)
            arrow_y = Inches(center_y) - arrow_h / 2

            arrow = slide.shapes.add_shape(
                MSO_SHAPE.RIGHT_ARROW,
                arrow_x, arrow_y, arrow_w, arrow_h
            )
            arrow.fill.solid()
            arrow.fill.fore_color.rgb = RGBColor(*arrow_color)
            arrow.line.fill.background() # Removes border
            
            # Subtler shadow for the arrow
            add_shadow(arrow)

    prs.save(output_pptx_path)
    return output_pptx_path
```