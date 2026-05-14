# Native Network Topology Schematics

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Native Network Topology Schematics

* **Core Visual Mechanism**: Representing physical or logical IT architectures using grid-aligned primitive shapes (clouds, cylinders, rounded rectangles) and routed orthogonal lines (elbow connectors). The design relies on spatial hierarchy, clear grouping, and high-contrast lines to dictate data flow and connectivity without relying on external image assets.
* **Why Use This Skill (Rationale)**: Complex IT infrastructures or logical workflows can overwhelm audiences when presented as text. By converting systems into standardized visual topologies, you reduce cognitive load. The orthogonal routing of lines creates a sense of order and precision.
* **Overall Applicability**: System architecture reviews, infrastructure deployment plans, database schemas, and technical educational presentations.
* **Value Addition**: While users often jump to external tools (like *draw.io* or *Creately* as shown in the tutorial) to build these diagrams, PowerPoint has a powerful, natively programmatic connector engine. Generating this directly in PPTX allows the audience to edit the nodes later without needing access to a third-party application.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Node Icons**: Standard primitive geometry repurposed as technical symbols (`CLOUD` for Internet, `OVAL` for Router, `CAN` for Server, `RECTANGLE` for Switch).
  - **Smart Connectors**: Elbow lines that automatically route around objects, capped with directional arrowheads.
  - **Color Logic**: 
    - Soft, distinct background fills for categorization: Server Blue `(240, 245, 250)`, Switch Green `(240, 255, 240)`, Router Red `(255, 240, 240)`.
    - Deep, saturated borders to anchor the shapes against a white background.
  - **Text Hierarchy**: Bold dark text for device names, followed by smaller, lighter text for technical details (e.g., IP addresses).

* **Step B: Compositional Style**
  - **Top-Down / Center-Out Hierarchy**: External networks (Cloud) at the top/corner, routing inward to core infrastructure (Routers/Switches), fanning out to edge devices (PCs/Laptops) at the bottom.
  - **Whitespace**: Generous spacing between nodes allows the elbow connectors to route cleanly without overlapping.

* **Step C: Dynamic Effects & Transitions**
  - Static diagrammatic layout. Shadows are subtly applied via XML injection to lift the nodes off the canvas, giving them a modern "app-like" flat-design feel (similar to *Creately's* aesthetic).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Nodes & Base Layout** | `python-pptx` standard shapes | Native auto-shapes (Clouds, Cans, Rectangles) are perfectly suited for diagram nodes. |
| **Routing Lines** | `python-pptx` Connectors | The `add_connector()` and `begin_connect()` APIs allow lines to dynamically anchor to shapes, mimicking draw.io's core feature. |
| **Directional Arrowheads** | `lxml` XML Injection | `python-pptx` does not expose an API to add arrowheads to connectors. We must inject the `<a:tailEnd>` element directly into the line XML. |
| **Drop Shadows** | `lxml` XML Injection | Adding an `<a:outerShdw>` element gives the diagram a polished, modern SaaS aesthetic not easily triggered via the base API. |

> **Feasibility Assessment**: 100% reproduction of the diagramming logic demonstrated in the tutorial, accomplished entirely within PowerPoint's native rendering engine.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "Network Infrastructure Topology",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing an auto-routed Network Topology Schema.
    
    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
    from pptx.enum.text import PP_ALIGN
    from pptx.dml.color import RGBColor
    from lxml import etree

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use a blank slide layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Title & Subtitle ===
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12.333), Inches(0.8))
    tf = title_box.text_frame
    tf.text = title_text
    p = tf.paragraphs[0]
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = RGBColor(30, 41, 59)

    p2 = tf.add_paragraph()
    p2.text = "Generated Logical Architecture Diagram"
    p2.font.size = Pt(14)
    p2.font.color.rgb = RGBColor(100, 116, 139)

    # === Helper: XML Shadow Injection ===
    def add_shadow(shape):
        spPr = shape.element.spPr
        ns = '{http://schemas.openxmlformats.org/drawingml/2006/main}'
        
        # Skip if shadow already exists
        if spPr.find(ns + 'effectLst') is not None:
            return

        effectLst = etree.Element(ns + 'effectLst')
        outerShdw = etree.SubElement(effectLst, ns + 'outerShdw', blurRad="50000", dist="35000", dir="2700000", algn="tl")
        srgbClr = etree.SubElement(outerShdw, ns + 'srgbClr', val="000000")
        etree.SubElement(srgbClr, ns + 'alpha', val="12000") # 12% opacity
        
        # Schema strictly requires effectLst before scene3d, sp3d, or extLst
        insert_idx = len(spPr)
        for i, child in enumerate(spPr):
            if child.tag in [ns+'scene3d', ns+'sp3d', ns+'extLst']:
                insert_idx = i
                break
        spPr.insert(insert_idx, effectLst)

    # === Helper: XML Arrowhead Injection ===
    def add_arrowhead(connector_shape):
        line_pr = connector_shape.element.spPr.ln
        if line_pr is None:
            return
        
        ns = '{http://schemas.openxmlformats.org/drawingml/2006/main}'
        tailEnd = etree.Element(ns + 'tailEnd', type="triangle", w="med", len="med")
        
        # Schema requires tailEnd before extLst
        insert_idx = len(line_pr)
        for i, child in enumerate(line_pr):
            if child.tag == ns + 'extLst':
                insert_idx = i
                break
        line_pr.insert(insert_idx, tailEnd)

    # === Node Configuration Data ===
    nodes_config = {
        "cloud":  {"type": MSO_SHAPE.CLOUD, "x": 8.5, "y": 1.2, "w": 2.2, "h": 1.4, "text": "Internet\n(WAN)", "fill": (255,255,255), "line": (150,150,150)},
        "router": {"type": MSO_SHAPE.OVAL, "x": 6.0, "y": 2.5, "w": 1.6, "h": 1.0, "text": "Router\n10.0.0.1", "fill": (255,240,240), "line": (200,80,80)},
        "server": {"type": MSO_SHAPE.CAN, "x": 2.0, "y": 4.0, "w": 1.3, "h": 1.6, "text": "DB Server\n10.0.0.5", "fill": (240,245,250), "line": (40,100,200)},
        "switch": {"type": MSO_SHAPE.RECTANGLE, "x": 4.5, "y": 4.4, "w": 4.5, "h": 0.8, "text": "Main Switch", "fill": (240,255,240), "line": (80,200,80)},
        "pc1":    {"type": MSO_SHAPE.ROUNDED_RECTANGLE, "x": 3.0, "y": 6.2, "w": 1.5, "h": 1.0, "text": "PC 1\n.101", "fill": (250,250,250), "line": (100,100,100)},
        "pc2":    {"type": MSO_SHAPE.ROUNDED_RECTANGLE, "x": 6.0, "y": 6.2, "w": 1.5, "h": 1.0, "text": "Laptop\n.102", "fill": (250,250,250), "line": (100,100,100)},
        "pc3":    {"type": MSO_SHAPE.ROUNDED_RECTANGLE, "x": 9.0, "y": 6.2, "w": 1.5, "h": 1.0, "text": "PC 2\n.103", "fill": (250,250,250), "line": (100,100,100)},
    }

    # === Render Nodes ===
    nodes = {}
    for name, cfg in nodes_config.items():
        shape = slide.shapes.add_shape(
            cfg["type"], Inches(cfg["x"]), Inches(cfg["y"]), Inches(cfg["w"]), Inches(cfg["h"])
        )
        
        # Style Fill & Line
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(*cfg["fill"])
        shape.line.color.rgb = RGBColor(*cfg["line"])
        shape.line.width = Pt(1.5)
        
        add_shadow(shape)
        
        # Format Text Hierarchy
        lines = cfg["text"].split('\n')
        tf = shape.text_frame
        tf.word_wrap = False
        
        p = tf.paragraphs[0]
        p.text = lines[0]
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = RGBColor(40, 40, 40)
        p.alignment = PP_ALIGN.CENTER
        
        if len(lines) > 1:
            p2 = tf.add_paragraph()
            p2.text = lines[1]
            p2.font.size = Pt(10)
            p2.font.bold = False
            p2.font.color.rgb = RGBColor(80, 80, 80)
            p2.alignment = PP_ALIGN.CENTER

        nodes[name] = shape

    # === Render Smart Connectors ===
    # Format: (SourceNode, SourceSiteIndex, DestNode, DestSiteIndex)
    # Site Indices typically map to: 0=Top, 1=Right, 2=Bottom, 3=Left
    connections = [
        ("cloud", 3, "router", 0),  # Cloud Left -> Router Top
        ("router", 2, "switch", 0), # Router Bottom -> Switch Top
        ("server", 1, "switch", 3), # Server Right -> Switch Left
        ("switch", 2, "pc1", 0),    # Switch Bottom -> PC1 Top
        ("switch", 2, "pc2", 0),    # Switch Bottom -> PC2 Top
        ("switch", 2, "pc3", 0),    # Switch Bottom -> PC3 Top
    ]

    for src, s_idx, dst, d_idx in connections:
        # Create an elbow connector (coordinates act as dummy defaults until connected)
        conn = slide.shapes.add_connector(MSO_CONNECTOR.ELBOW, 0, 0, 100, 100)
        
        # Anchor the ends to the shapes dynamically
        conn.begin_connect(nodes[src], s_idx)
        conn.end_connect(nodes[dst], d_idx)
        
        # Style the line
        conn.line.color.rgb = RGBColor(120, 120, 120)
        conn.line.width = Pt(1.5)
        
        # Inject the directional arrowhead
        add_arrowhead(conn)

    prs.save(output_pptx_path)
    return output_pptx_path
```