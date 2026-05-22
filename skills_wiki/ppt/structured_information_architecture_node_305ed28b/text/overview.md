# Structured Information Architecture (Node-Based Hierarchy Diagram)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Structured Information Architecture (Node-Based Hierarchy Diagram)

*   **Core Visual Mechanism**: The defining visual idea is the transformation of linear, unstructured text (bullet points) into a spatial, node-based diagram. It uses geometric shapes (usually rounded rectangles or pills) connected by lines or spatial alignment to visually separate, group, and sequence information. 
*   **Why Use This Skill (Rationale)**: Human brains process visual geometry much faster than written text. By mapping logical relationships (parent-child, process steps, or categorizations) to spatial relationships (left-to-right, top-to-bottom, overlapping), you drastically reduce cognitive load. It prevents "death by PowerPoint" by chunking information into digestible visual blocks.
*   **Overall Applicability**: This is the ultimate "workhorse" skill for corporate presentations. It is perfect for Organization Charts (org-charts), feature breakdowns, process workflows, project roadmaps, and business model canvases.
*   **Value Addition**: It elevates a slide from a "reading document" to a "visual presentation." It immediately communicates professionalism, logical rigor, and clarity of thought.

### 2. Visual Breakdown

*   **Step A: Core Visual Elements**
    *   **Nodes (Shapes)**: Clean, flat geometric shapes, typically rectangles or rounded rectangles.
    *   **Connectors**: Thin, unobtrusive lines (straight or elbow) connecting parent nodes to child nodes.
    *   **Color Logic**: Hierarchical coloring. 
        *   Level 1 (Root): Dominant, dark color, e.g., Deep Navy `(32, 56, 100)`.
        *   Level 2 (Categories): Vibrant accent, e.g., Cyan `(0, 191, 255)` or Coral `(237, 125, 49)`.
        *   Level 3 (Details): Low-contrast or outlined, e.g., Light Gray `(242, 242, 242)` with dark text, or simple border-only shapes.
    *   **Text Hierarchy**: Large bold font for the root, medium for categories, and smaller regular font for details.

*   **Step B: Compositional Style**
    *   **Spatial Feel**: Orderly, balanced, and grid-aligned.
    *   **Layout Principles**: Progression is usually Left-to-Right (Process/Logic) or Top-to-Bottom (Command/Structure).
    *   **Proportions**: The diagram typically occupies 80% of the slide canvas, leaving a comfortable 10% margin on all sides.

*   **Step C: Dynamic Effects & Transitions**
    *   **Animation**: "Wipe" or "Fade" transitions revealing nodes level-by-level (e.g., Root appears, then Level 2 branches appear simultaneously, then Level 3). *Achieved via native PowerPoint animation settings.*

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
| :--- | :--- | :--- |
| **Node Layout & Text** | `python-pptx` native | For structured diagrams, text *must* remain editable. Native shapes with calculated X/Y coordinates perfectly replicate PowerPoint's auto-layout SmartArt. |
| **Connecting Lines** | `python-pptx` connectors | Using native connectors ensures that lines physically link the geometric centers of the shapes. |
| **Premium Polish (Shadows)** | lxml XML injection | Native `python-pptx` lacks API support for shape shadows. Injecting `<a:outerShdw>` gives the flat shapes the premium "floating card" look seen in modern SmartArt. |

> **Feasibility Assessment**: 95%. This code accurately replicates the "Horizontal Hierarchy / Logic Tree" structural layout shown in the tutorial. By using an algorithmic layout calculation combined with XML shadow injection, it generates a highly professional, fully editable SmartArt-equivalent diagram.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "Hierarchical Logic Structure",
    body_text: str = "", # Unused in this layout, logic tree takes precedence
    bg_palette: str = "light", 
    accent_color: tuple = (0, 191, 255),  
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the [Structured Information Architecture] visual effect.
    Generates a Left-to-Right editable logic tree / hierarchy diagram.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
    from pptx.enum.text import PP_ALIGN
    from pptx.dml.color import RGBColor
    from lxml import etree

    # 1. Setup Presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout
    
    # Background - Light Grey/White
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(250, 250, 250)

    # 2. Add Title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.4), Inches(12.333), Inches(0.8))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = RGBColor(32, 56, 100) # Deep Navy

    # 3. Define the Structural Data (The Information to be Organized)
    hierarchy_data = {
        "Core Objective": {
            "Strategic Pillar A": ["Initiative 1", "Initiative 2"],
            "Strategic Pillar B": ["Initiative 3", "Initiative 4", "Initiative 5"],
            "Strategic Pillar C": ["Initiative 6"]
        }
    }

    # 4. Helper Function: Add Shadow via XML injection
    def apply_shadow(shape):
        spPr = shape.element.spPr
        effectLst = etree.SubElement(spPr, "{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst")
        outerShdw = etree.SubElement(effectLst, "{http://schemas.openxmlformats.org/drawingml/2006/main}outerShdw", 
                                     blurRad="50800", dist="38100", dir="2700000", algn="tl", rotWithShape="0")
        srgbClr = etree.SubElement(outerShdw, "{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr", val="000000")
        etree.SubElement(srgbClr, "{http://schemas.openxmlformats.org/drawingml/2006/main}alpha", val="15000") # 15% opacity

    # Helper Function: Create styled node
    def create_node(slide, x, y, w, h, text, level):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
        shape.line.fill.background() # No border
        
        # Color Logic based on level
        if level == 1:
            shape.fill.solid()
            shape.fill.fore_color.rgb = RGBColor(32, 56, 100) # Deep Navy
            font_color = RGBColor(255, 255, 255)
            font_size = Pt(20)
        elif level == 2:
            shape.fill.solid()
            shape.fill.fore_color.rgb = RGBColor(*accent_color) # Accent
            font_color = RGBColor(255, 255, 255)
            font_size = Pt(16)
        else: # Level 3
            shape.fill.solid()
            shape.fill.fore_color.rgb = RGBColor(255, 255, 255) # White
            shape.line.fill.solid()
            shape.line.fill.fore_color.rgb = RGBColor(200, 200, 200) # Soft border
            font_color = RGBColor(80, 80, 80)
            font_size = Pt(14)
            
        apply_shadow(shape)
        
        # Text formatting
        tf = shape.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
        p = tf.paragraphs[0]
        p.text = text
        p.alignment = PP_ALIGN.CENTER
        p.font.size = font_size
        p.font.bold = True if level < 3 else False
        p.font.color.rgb = font_color
        
        return shape

    # 5. Layout Calculation Engine
    # Canvas limits for the diagram
    start_x = Inches(1.0)
    end_x = Inches(12.333)
    start_y = Inches(1.5)
    end_y = Inches(6.5)
    
    node_w = Inches(2.2)
    node_h = Inches(0.6)
    
    # Calculate dimensions
    root_keys = list(hierarchy_data.keys())
    l1_text = root_keys[0]
    l2_dict = hierarchy_data[l1_text]
    l2_keys = list(l2_dict.keys())
    
    total_l3_items = sum([len(v) for v in l2_dict.values()])
    
    # Calculate Y positions to evenly distribute leaves (L3)
    available_height = end_y - start_y
    y_step = available_height / max(total_l3_items - 1, 1)
    
    # Draw L3 and L2, calculating L2 positions based on L3 children
    l3_shapes = []
    l2_shapes = []
    
    current_l3_index = 0
    
    for l2_idx, l2_text in enumerate(l2_keys):
        l3_items = l2_dict[l2_text]
        
        l2_child_shapes = []
        for l3_text in l3_items:
            # Draw L3
            x3 = start_x + (node_w * 2) + Inches(1.5) # Level 3 column
            y3 = start_y + (current_l3_index * y_step)
            s3 = create_node(slide, x3, y3, node_w, node_h, l3_text, 3)
            l2_child_shapes.append(s3)
            current_l3_index += 1
            
        # Draw L2 (centered vertically relative to its children)
        if l2_child_shapes:
            l2_y_center = sum([s.top for s in l2_child_shapes]) / len(l2_child_shapes)
        else:
            l2_y_center = start_y + (current_l3_index * y_step)
            
        x2 = start_x + node_w + Inches(0.75) # Level 2 column
        s2 = create_node(slide, x2, l2_y_center, node_w, node_h, l2_text, 2)
        l2_shapes.append(s2)
        
        # Connect L2 to L3
        for s3 in l2_child_shapes:
            connector = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, s2.left + s2.width, s2.top + s2.height/2, s3.left, s3.top + s3.height/2)
            connector.line.fill.solid()
            connector.line.fill.fore_color.rgb = RGBColor(180, 180, 180)

    # Draw Root (L1) (centered vertically relative to L2)
    if l2_shapes:
        l1_y_center = sum([s.top for s in l2_shapes]) / len(l2_shapes)
    else:
        l1_y_center = start_y + (available_height / 2)
        
    s1 = create_node(slide, start_x, l1_y_center, node_w, Inches(1.2), l1_text, 1) # Make root taller
    
    # Connect L1 to L2
    for s2 in l2_shapes:
        connector = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, s1.left + s1.width, s1.top + s1.height/2, s2.left, s2.top + s2.height/2)
        connector.line.fill.solid()
        connector.line.fill.fore_color.rgb = RGBColor(180, 180, 180)
        connector.line.width = Pt(1.5)

    prs.save(output_pptx_path)
    return output_pptx_path
```