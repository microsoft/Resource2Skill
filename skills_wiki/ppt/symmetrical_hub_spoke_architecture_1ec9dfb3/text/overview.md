# Symmetrical Hub & Spoke Architecture

## Analysis

An analysis of the visual techniques in the video reveals a recurring and highly effective design pattern used repeatedly to illustrate systems, architectures, and integrations (specifically at 00:15, 00:20, and 00:30).

### 1. High-level Design Pattern Extraction

> **Skill Name**: Symmetrical Hub & Spoke Architecture

* **Core Visual Mechanism**: A prominent central core (the "Hub") flanked symmetrically by interconnected nodes (the "Spokes"). Connections are explicitly drawn with converging lines passing behind the elements. The layout utilizes distinct color blocking to separate the core system from peripheral modules.
* **Why Use This Skill (Rationale)**: This layout perfectly visualizes decentralized or modular systems relying on a central unified core (like an ERP, central database, or cloud infrastructure). Symmetrical layouts inherently convey stability, balance, and structural integrity—ideal psychological cues for system design and IT architecture presentations.
* **Overall Applicability**: Best used for system integration diagrams, API architectures, product ecosystem overviews, feature roadmaps, and centralized data flows.
* **Value Addition**: Unlike standard bullet points or messy flowcharts, this diagram forces complex information into an easily digestible, highly balanced visual hierarchy, immediately drawing the eye to the core concept before branching outward.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **The Hub**: A large, dark circular element anchored in the center `(e.g., Dark Slate RGB 44, 62, 80)`.
  - **Integration Ring**: A dashed circular border encompassing the hub, simulating continuous cyclic flow or a bounded integration zone.
  - **Floating Nodes**: Solid-colored circular icons `(e.g., Emerald Green RGB 39, 174, 96)` paired with text blocks.
  - **Typography**: Dark, bold titles for the nodes with right-alignment for the left hemisphere and left-alignment for the right hemisphere to maintain mirroring. 

* **Step B: Compositional Style**
  - Strict horizontal and vertical symmetry.
  - The canvas is divided into three vertical columns: Left nodes (width ~20%), Core Hub (width ~60% with blank space for connectors), Right nodes (width ~20%).
  - Text blocks maintain a consistent 0.35-inch offset from their respective node icons.

* **Step C: Dynamic Effects & Transitions**
  - Simulated depth using subtle XML-injected drop shadows on the floating elements, pulling them forward from the flat connector lines sitting in the background layer.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Architecture Layout** | `python-pptx` native | Flawless positioning of shapes (ovals, lines, text boxes) via exact coordinate math. |
| **Connecting Lines** | `python-pptx` Connectors | Built-in connector shapes inherently suit architectural network lines. |
| **Depth / Shadows** | `lxml` XML injection | Native `python-pptx` lacks drop shadow APIs; XML injection is required to add professional `outerShdw` depth to the core and nodes. |

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "System Integration Architecture",
    theme_color: tuple = (39, 174, 96),  # Emerald Green
    dark_accent: tuple = (44, 62, 80),   # Dark Slate
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the 'Symmetrical Hub & Spoke Architecture' effect.
    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
    from pptx.enum.dml import MSO_LINE_DASH_STYLE
    from lxml import etree

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Helper function for XML drop shadow
    def add_shadow(shape, blur="150000", dist="50000", alpha="30000"):
        spPr = shape.element.spPr
        effectLst = etree.SubElement(spPr, '{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst')
        outerShdw = etree.SubElement(effectLst, '{http://schemas.openxmlformats.org/drawingml/2006/main}outerShdw')
        outerShdw.set('blurRad', blur)
        outerShdw.set('dist', dist)
        outerShdw.set('dir', '2700000') # Drop shadow angled downwards
        srgbClr = etree.SubElement(outerShdw, '{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr')
        srgbClr.set('val', '000000') # Black shadow
        alpha_node = etree.SubElement(srgbClr, '{http://schemas.openxmlformats.org/drawingml/2006/main}alpha')
        alpha_node.set('val', alpha) 

    # --- Layer 0: Decorative Background Accent ---
    light_bg = tuple(min(255, int(c + (255 - c) * 0.92)) for c in theme_color)
    bg_accent = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(-3), Inches(-4), Inches(9), Inches(9))
    bg_accent.fill.solid()
    bg_accent.fill.fore_color.rgb = RGBColor(*light_bg)
    bg_accent.line.fill.background()

    # --- Slide Title ---
    title_shape = slide.shapes.add_textbox(Inches(0.5), Inches(0.4), Inches(12.333), Inches(0.8))
    tf = title_shape.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = RGBColor(51, 51, 51)
    
    # Data structure for the layout
    nodes = [
        {"title": "Feature Implementation", "body": "Seamlessly integrate new capabilities into the ecosystem.", "icon": "⚙️"},
        {"title": "Platform Customization", "body": "Adapt and configure to meet specific business needs.", "icon": "🎨"},
        {"title": "Data Harmonization", "body": "Unify data from diverse domains for a single source of truth.", "icon": "📊"},
        {"title": "Third-Party Integration", "body": "Connect external products via standardized APIs.", "icon": "📦"},
        {"title": "Application Ecosystem", "body": "Manage interconnected applications smoothly and securely.", "icon": "📱"},
        {"title": "Hybrid Cloud Hosting", "body": "Deploy across private, public, and on-premise environments.", "icon": "☁️"},
    ]

    Y_centers = [2.2, 4.0, 5.8]
    hub_y_center = 4.0
    hub_x_center = 6.666
    
    # --- Layer 1: Connectors ---
    # Drawn first so they sit naturally beneath the hubs and nodes
    for i in range(6):
        y_center = Y_centers[i % 3]
        x_start = 4.2 if i < 3 else 9.133
        
        conn = slide.shapes.add_connector(
            MSO_CONNECTOR.STRAIGHT,
            Inches(x_start), Inches(y_center),
            Inches(hub_x_center), Inches(hub_y_center)
        )
        conn.line.width = Pt(2)
        conn.line.color.rgb = RGBColor(210, 215, 211)

    # --- Layer 2: Core Hub Architecture ---
    # Integration Ring
    ring_size = 3.4
    ring = slide.shapes.add_shape(
        MSO_SHAPE.OVAL,
        Inches(hub_x_center - ring_size/2), Inches(hub_y_center - ring_size/2), 
        Inches(ring_size), Inches(ring_size)
    )
    ring.fill.background()
    ring.line.color.rgb = RGBColor(*theme_color)
    ring.line.width = Pt(2.5)
    ring.line.dash_style = MSO_LINE_DASH_STYLE.DASH

    # Solid Central Hub
    hub_size = 2.4
    hub = slide.shapes.add_shape(
        MSO_SHAPE.OVAL,
        Inches(hub_x_center - hub_size/2), Inches(hub_y_center - hub_size/2), 
        Inches(hub_size), Inches(hub_size)
    )
    hub.fill.solid()
    hub.fill.fore_color.rgb = RGBColor(*dark_accent)
    hub.line.fill.background()
    add_shadow(hub, blur="200000", dist="60000") # Enhanced shadow
    
    # Hub Text Label
    htf = hub.text_frame
    htf.text = "🔄\nCore\nSystem"
    htf.paragraphs[0].font.size = Pt(24)
    for p in htf.paragraphs:
        p.alignment = PP_ALIGN.CENTER
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.font.bold = True

    # --- Layer 3: Flanking Nodes ---
    for i, node in enumerate(nodes):
        is_left = i < 3
        y_center = Y_centers[i % 3]
        
        # Adjust layout directionality based on hemisphere
        if is_left:
            x_icon = 4.2
            x_text = 0.8
        else:
            x_icon = 9.133
            x_text = 9.833
            
        # Floating Icon Node
        icon_size = 0.7
        icon_shape = slide.shapes.add_shape(
            MSO_SHAPE.OVAL,
            Inches(x_icon - icon_size/2), Inches(y_center - icon_size/2), 
            Inches(icon_size), Inches(icon_size)
        )
        icon_shape.fill.solid()
        icon_shape.fill.fore_color.rgb = RGBColor(*theme_color)
        icon_shape.line.fill.background()
        add_shadow(icon_shape, blur="80000", dist="30000", alpha="25000")
        
        # Emoji Icon Setup
        itf = icon_shape.text_frame
        itf.text = node["icon"]
        itf.paragraphs[0].font.size = Pt(16)
        itf.paragraphs[0].alignment = PP_ALIGN.CENTER
        icon_shape.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
        
        # Accompanying Text Box
        text_box = slide.shapes.add_textbox(
            Inches(x_text), Inches(y_center - 0.45), 
            Inches(3.0), Inches(1.0)
        )
        tf = text_box.text_frame
        tf.word_wrap = True
        
        p_title = tf.paragraphs[0]
        p_title.text = node["title"]
        p_title.font.bold = True
        p_title.font.size = Pt(12)
        p_title.font.color.rgb = RGBColor(*dark_accent)
        
        p_body = tf.add_paragraph()
        p_body.text = node["body"]
        p_body.font.size = Pt(10)
        p_body.font.color.rgb = RGBColor(110, 110, 110)
        
        # Mirrored Alignment Logic
        if is_left:
            p_title.alignment = PP_ALIGN.RIGHT
            p_body.alignment = PP_ALIGN.RIGHT
        else:
            p_title.alignment = PP_ALIGN.LEFT
            p_body.alignment = PP_ALIGN.LEFT

    prs.save(output_pptx_path)
    return output_pptx_path
```