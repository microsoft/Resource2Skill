# Neon Dark-Mode System Architecture

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Neon Dark-Mode System Architecture

* **Core Visual Mechanism**: This pattern relies on a deep, near-black dark-mode canvas. Functional architectural components are represented by heavily rounded "pill" shapes filled with vibrant, neon-adjacent colors (cyan, mint green, vivid blue). The components are linked by precise, thin-line connectors. A signature touch is the use of subtle ambient "glows" (radial gradients) positioned behind core nodes to draw the eye and establish visual hierarchy without clutter.
* **Why Use This Skill (Rationale)**: High-contrast dark UI reduces eye strain and implies a modern, premium "developer" or "hacker" aesthetic. By using vibrant solid colors against dark gray, the functional layers of a system become immediately distinct. The pill shapes soften the rigidity typical of technical diagrams, making complex architectures feel approachable and streamlined.
* **Overall Applicability**: Ideal for system design diagrams, software architecture documentation, technical pitch decks (e.g., demonstrating SaaS infrastructure), and developer-focused training materials.
* **Value Addition**: Transforms a dry, chaotic engineering diagram into a sleek, cinematic infographic. The visual hierarchy effortlessly guides the audience's attention from data sources (Producers) through the core engine (Broker) out to destinations (Consumers).

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Background**: Deep slate/almost black `(20, 22, 25)`.
  - **Node Shapes**: MSO rounded rectangles with maximum roundness (pill shapes).
  - **Color Logic**:
    - Producers/Inputs: Vivid Blue `(41, 128, 185, 255)`
    - Core Engine/Broker: Neon Cyan `(0, 188, 212, 255)`
    - Consumers/Outputs: Mint Green `(39, 174, 96, 255)`
  - **Text Hierarchy**: 
    - Title: Large, bold, pure white `(255, 255, 255)`.
    - Node Titles: 14pt Arial, Bold, pure white.
    - Node Subtitles: 11pt Arial, Bold, light gray `(230, 230, 230)`.

* **Step B: Compositional Style**
  - **Spatial Feel**: A symmetrical, three-column layout (Left: Ingestion, Center: Processing, Right: Output).
  - **Proportions**: Nodes are wide enough to accommodate text comfortably (e.g., 2.5" wide by 0.8" high). The spacing between columns (approx. 2 inches) provides breathable whitespace for diagonal routing connectors, preventing visual congestion.

* **Step C: Dynamic Effects & Transitions**
  - Ambient glow under the central "Message Broker" node creates a focal point.
  - Connectors are drawn underneath the nodes so that lines neatly terminate precisely at the node boundaries.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Dark Background & Shapes** | `python-pptx` native | Standard library is highly efficient for exact positioning of text boxes and rounded rectangle nodes. |
| **Ambient Node Glow** | `PIL/Pillow` | `python-pptx` cannot natively render soft-blurred radial gradients. PIL is used to generate a transparent PNG overlay with heavy Gaussian blur to act as a backlight. |
| **Precise Arrowheads** | `lxml` XML injection | Relying on default connector behaviors in `python-pptx` often results in missing arrowheads or incorrect routing. Injecting `<a:tailEnd type="triangle"/>` directly into the DrawingML guarantees rendering. |

> **Feasibility Assessment**: 100% reproducible. The code perfectly generates the dark-mode aesthetic, the custom PIL-based ambient glow, and precise node-to-node routing.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "Event-Driven Architecture",
    body_text: str = "Decoupling services using scalable message brokers",
    bg_color: tuple = (20, 22, 25),
    accent_color: tuple = (0, 188, 212),
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Neon Dark-Mode System Architecture visual effect.
    """
    import os
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
    from pptx.enum.text import PP_ALIGN
    from lxml import etree
    import PIL.Image as Image
    import PIL.ImageDraw as ImageDraw
    import PIL.ImageFilter as ImageFilter

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use a blank slide layout
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    # === Layer 1: Solid Dark Background ===
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(*bg_color)
    bg.line.fill.background()

    # === Text: Titles ===
    title_box = slide.shapes.add_textbox(0, Inches(0.4), prs.slide_width, Inches(1.0))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.alignment = PP_ALIGN.CENTER
    p.font.name = "Arial"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    
    if body_text:
        p2 = tf.add_paragraph()
        p2.text = body_text
        p2.alignment = PP_ALIGN.CENTER
        p2.font.name = "Arial"
        p2.font.size = Pt(16)
        p2.font.color.rgb = RGBColor(180, 180, 180)

    # === Layout Coordinates ===
    w, h = 2.5, 0.8
    y_top, y_mid, y_bot = 2.2, 4.0, 5.8
    x_left, x_mid, x_right = 1.0, 5.4, 9.8

    producer_color = (41, 128, 185)  # Vivid Blue
    broker_color = accent_color      # Neon Cyan
    consumer_color = (39, 174, 96)   # Mint Green

    # === Layer 2: Ambient Glow (PIL) ===
    # Generate a heavily blurred radial gradient to place behind the central broker
    glow_path = "temp_ambient_glow.png"
    glow_size_px = 600
    img = Image.new("RGBA", (glow_size_px, glow_size_px), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    center = glow_size_px // 2
    radius = 150
    draw.ellipse(
        (center - radius, center - radius, center + radius, center + radius),
        fill=(broker_color[0], broker_color[1], broker_color[2], 140)
    )
    blurred_img = img.filter(ImageFilter.GaussianBlur(80))
    blurred_img.save(glow_path)

    glow_size_in = 6.25 # 600px at 96dpi
    glow_x = Inches(x_mid + w/2) - Inches(glow_size_in/2)
    glow_y = Inches(y_mid + h/2) - Inches(glow_size_in/2)
    slide.shapes.add_picture(glow_path, glow_x, glow_y, width=Inches(glow_size_in), height=Inches(glow_size_in))

    # === Helper: Draw Nodes ===
    def draw_node(slide, text, x, y, width, height, bg_rgb):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(width), Inches(height))
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(*bg_rgb)
        shape.line.fill.solid()
        shape.line.color.rgb = RGBColor(*bg_rgb)
        
        # Maximize roundness for pill effect
        if len(shape.adjustments) > 0:
            shape.adjustments[0] = 0.5
            
        tf = shape.text_frame
        tf.word_wrap = True
        lines = text.split("\n")
        
        for i, line in enumerate(lines):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.text = line
            p.alignment = PP_ALIGN.CENTER
            p.font.name = "Arial"
            p.font.bold = True
            
            if i == 0:
                p.font.size = Pt(14)
                p.font.color.rgb = RGBColor(255, 255, 255)
            else:
                p.font.size = Pt(11)
                p.font.color.rgb = RGBColor(230, 230, 230)
        return shape

    # === Helper: Draw Connectors with lxml arrowheads ===
    def add_arrow(slide, start_x, start_y, end_x, end_y):
        cxn = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(start_x), Inches(start_y), Inches(end_x), Inches(end_y))
        cxn.line.color.rgb = RGBColor(120, 130, 140)
        cxn.line.width = Pt(1.5)
        
        # XML Injection for arrowhead
        nsmap = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
        spPr = cxn.element.spPr
        ln = spPr.find('a:ln', namespaces=nsmap)
        if ln is not None:
            existing_tail = ln.find('a:tailEnd', namespaces=nsmap)
            if existing_tail is not None:
                ln.remove(existing_tail)
            etree.SubElement(ln, '{http://schemas.openxmlformats.org/drawingml/2006/main}tailEnd', type="triangle", w="med", len="med")

    # === Layer 3: Connectors ===
    # Draw these BEFORE nodes so the lines rest underneath the node shapes
    y_positions = [y_top, y_mid, y_bot]
    
    # Left to Center connections
    for y in y_positions:
        add_arrow(slide, x_left + w, y + h/2, x_mid, y_mid + h/2)
        
    # Center to Right connections
    for y in y_positions:
        add_arrow(slide, x_mid + w, y_mid + h/2, x_right, y + h/2)

    # === Layer 4: Nodes ===
    # Left Column: Producers
    for i, y in enumerate(y_positions):
        draw_node(slide, f"Event Producer {i+1}", x_left, y, w, h, producer_color)
        
    # Center Column: Broker
    draw_node(slide, "Message Broker\n(Kafka / RabbitMQ)", x_mid, y_mid, w, h, broker_color)
    
    # Right Column: Consumers
    for i, y in enumerate(y_positions):
        draw_node(slide, f"Event Consumer {i+1}", x_right, y, w, h, consumer_color)

    # Save and cleanup
    prs.save(output_pptx_path)
    if os.path.exists(glow_path):
        os.remove(glow_path)
        
    return output_pptx_path
```