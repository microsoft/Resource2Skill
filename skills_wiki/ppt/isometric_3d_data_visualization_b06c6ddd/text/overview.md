# Isometric 3D Data Visualization

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Isometric 3D Data Visualization

*   **Core Visual Mechanism**: This technique manually constructs isometric 3D objects (bars and platforms) using 2D geometric primitives (diamonds, parallelograms, and multi-point freeform polygons). By applying vertical gradient fills to the front faces and semi-transparent white overlays to the side faces, it simulates global illumination, specular highlights, and structural depth without relying on complex 3D rendering engines.
*   **Why Use This Skill (Rationale)**: Native PowerPoint 3D objects can sometimes look rigid or lack customizable lighting control per face. Constructing the 3D shapes manually gives you absolute control over the gradient stops and shadow opacities, resulting in a highly stylized, "glassmorphic" or "neon-tech" aesthetic that stands out.
*   **Overall Applicability**: Ideal for high-stakes business presentations, executive dashboards, or hero slides where presenting data (like a sales report or growth metric) needs to feel modern, spatial, and premium.
*   **Value Addition**: Transforms a standard, flat bar chart into an immersive spatial environment. The floating isometric panels and glowing data bars draw the eye naturally to the key metrics, creating a sense of scale and momentum.

### 2. Visual Breakdown

*   **Step A: Core Visual Elements**
    *   **Background**: Deep, glowing gradient canvas transitioning from dark navy (`#140A28`) to muted blue (`#0A1E3C`), accented by soft, blurred background waves.
    *   **Platform**: An isometric disc base acting as an anchor.
    *   **Data Bars**: Hexagonal prisms (diamond-based). The front-facing elements use vivid two-stop vertical gradients (e.g., Orange `#FFC107` to `#FF5722`, Cyan `#00BCD4` to `#0288D1`). The top faces are flat, light solid colors. The right side features a white overlay with 80% transparency to create a sharp geometric light reflection.
    *   **Text Hierarchy**: Large, floating percentage values in bold sans-serif directly above the bars, connected by thin vertical reference lines.

*   **Step B: Compositional Style**
    *   The composition centers around a virtual isometric ground plane. The data bars are aligned along a common horizontal baseline to mimic physical objects sitting side-by-side on a stage.
    *   A floating side-panel (injected with XML 3D rotation) balances the heavy visual weight of the bars and provides context ("Sales Report").

*   **Step C: Dynamic Effects & Transitions**
    *   Visually static in generation, but in a live slide, these bars are typically animated to "wipe" from bottom to top, simulating the bars growing to their respective data points.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
| :--- | :--- | :--- |
| **Deep Gradient & Glowing Waves** | `PIL/Pillow` | PowerPoint's native gradients are limited for abstract, blurred glowing organic shapes. PIL generates a perfect backdrop image. |
| **3D Isometric Bars** | `python-pptx` FreeformBuilder | Replicates the tutorial's exact manual diamond/rectangle construction method mathematically for pixel-perfect edge alignment. |
| **Gradient Fills & Transparencies** | `lxml` XML Injection | `python-pptx` cannot natively set gradient stops or inject alpha transparency onto shape fills. `lxml` safely alters the OpenXML elements. |
| **Isometric Context Panel** | `lxml` (a:scene3d) | Applying an `isometricLeftUp` camera rotation via XML onto a standard text box allows the text itself to skew naturally in 3D space. |

> **Feasibility Assessment**: 95%. The combination of PIL for the atmosphere, exact 2D projection math for the bars, and XML injection for gradients and 3D skewing produces an incredibly faithful reproduction of the tutorial's aesthetic.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "SALES REPORT",
    body_text: str = "Q3 2024",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Isometric 3D Data Visualization effect.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN
    from pptx.oxml import parse_xml
    from PIL import Image, ImageDraw, ImageFilter
    import os

    # ---------------------------------------------------------
    # Helper: Apply Gradient Fill via XML
    # ---------------------------------------------------------
    def apply_gradient_fill(shape, colors_with_stops, angle=90, alpha=None):
        spPr = shape.element.spPr
        for elem in list(spPr):
            if elem.tag.endswith('Fill'):
                spPr.remove(elem)
                
        gsLst_xml = ""
        for color_hex, pos in colors_with_stops:
            alpha_tag = f'<a:alpha val="{int(alpha*100000)}"/>' if alpha is not None else ''
            gsLst_xml += f'<a:gs pos="{int(pos * 1000)}"><a:srgbClr val="{color_hex}">{alpha_tag}</a:srgbClr></a:gs>'
            
        gradFill_xml = f"""
        <a:gradFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
            <a:lin ang="{int(angle * 60000)}" scaled="1"/>
            <a:gsLst>{gsLst_xml}</a:gsLst>
        </a:gradFill>
        """
        gradFill = parse_xml(gradFill_xml)
        
        insert_idx = 0
        for i, child in enumerate(spPr):
            if child.tag.endswith('Geom'):
                insert_idx = i + 1
        spPr.insert(insert_idx, gradFill)

    # ---------------------------------------------------------
    # Initial Setup
    # ---------------------------------------------------------
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # ---------------------------------------------------------
    # Layer 1: Generate & Apply PIL Background
    # ---------------------------------------------------------
    bg_path = "isometric_bg_temp.png"
    width, height = 1920, 1080
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    # Dark linear gradient
    c1, c2 = (20, 10, 40), (10, 30, 60)
    for y in range(height):
        r = int(c1[0] + (c2[0] - c1[0]) * y / height)
        g = int(c1[1] + (c2[1] - c1[1]) * y / height)
        b = int(c1[2] + (c2[2] - c1[2]) * y / height)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
        
    # Glowing organic background waves
    glow = Image.new('RGBA', (width, height), (0,0,0,0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.polygon([(0, height), (width*0.4, height*0.6), (width, height*0.8), (width, height)], fill=(0, 200, 255, 40))
    gdraw.polygon([(width*0.2, height), (width*0.6, height*0.4), (width, height*0.5), (width, height)], fill=(255, 0, 255, 30))
    glow = glow.filter(ImageFilter.GaussianBlur(50))
    img.paste(glow, (0,0), glow)
    img.save(bg_path)
    
    slide.shapes.add_picture(bg_path, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # ---------------------------------------------------------
    # Layer 2: Draw the 3D Platform (Faux 3D disc)
    # ---------------------------------------------------------
    pcx, pcy = Inches(8.0), Inches(6.0)
    prx, pry = Inches(4.5), Inches(1.3)
    p_depth = Inches(0.4)
    
    bottom_oval = slide.shapes.add_shape(MSO_SHAPE.OVAL, pcx - prx, pcy - pry + p_depth, prx * 2, pry * 2)
    side_rect = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, pcx - prx, pcy, prx * 2, p_depth)
    top_oval = slide.shapes.add_shape(MSO_SHAPE.OVAL, pcx - prx, pcy - pry, prx * 2, pry * 2)
    
    for shp in [bottom_oval, side_rect, top_oval]:
        shp.line.fill.background()
        
    bottom_oval.fill.solid(); bottom_oval.fill.fore_color.rgb = RGBColor(18, 24, 88)
    side_rect.fill.solid(); side_rect.fill.fore_color.rgb = RGBColor(18, 24, 88)
    top_oval.fill.solid(); top_oval.fill.fore_color.rgb = RGBColor(26, 35, 126)

    # ---------------------------------------------------------
    # Layer 3: Isometric Context Panel (Left)
    # ---------------------------------------------------------
    panel = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(2.0), Inches(3.5), Inches(2.5))
    panel.line.fill.background()
    apply_gradient_fill(panel, [("FF00FF", 0.0), ("8A2BE2", 1.0)], angle=45, alpha=0.6)
    
    tf = panel.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = f"{title_text}\n{body_text}"
    p.font.name = "Arial"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    
    spPr = panel.element.spPr
    spPr.append(parse_xml("""
        <a:scene3d xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
            <a:camera prst="isometricLeftUp"/><a:lightRig rig="threePt" dir="t"/>
        </a:scene3d>
    """))
    spPr.append(parse_xml('<a:sp3d xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" prstMaterial="flat"/>'))

    # ---------------------------------------------------------
    # Layer 4: Isometric Bars
    # ---------------------------------------------------------
    def draw_bar(cx, cy, h, dx, dy, grad_hexes, top_hex, value_text):
        # 1. Main Front Body (Left + Right facing combined)
        ffb = slide.shapes.build_freeform()
        ffb.add_line_segments([
            (cx, cy - h - 2*dy), (cx + dx, cy - h - dy), (cx + dx, cy - dy),
            (cx, cy), (cx - dx, cy - dy), (cx - dx, cy - h - dy), (cx, cy - h - 2*dy)
        ])
        body = ffb.convert_to_shape()
        body.line.fill.background()
        apply_gradient_fill(body, [(grad_hexes[0], 0.0), (grad_hexes[1], 1.0)], angle=90)
        
        # 2. Right Highlight Overlay (intersected right half)
        ffb = slide.shapes.build_freeform()
        ffb.add_line_segments([
            (cx, cy - h), (cx + dx, cy - h - dy), (cx + dx, cy - dy), (cx, cy), (cx, cy - h)
        ])
        overlay = ffb.convert_to_shape()
        overlay.line.fill.background()
        overlay.fill.solid()
        overlay.fill.fore_color.rgb = RGBColor(255, 255, 255)
        # Inject Alpha for glass effect
        srgbClr = overlay.element.spPr.find(".//{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr")
        srgbClr.append(parse_xml('<a:alpha xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" val="20000"/>'))

        # 3. Top Diamond Face
        ffb = slide.shapes.build_freeform()
        ffb.add_line_segments([
            (cx, cy - h - 2*dy), (cx + dx, cy - h - dy), (cx, cy - h), (cx - dx, cy - h - dy), (cx, cy - h - 2*dy)
        ])
        top = ffb.convert_to_shape()
        top.line.fill.background()
        top.fill.solid()
        top.fill.fore_color.rgb = RGBColor.from_string(top_hex)

        # 4. Connecting Line & Floating Label
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx - Inches(0.01), cy - h - 2*dy - Inches(0.8), Inches(0.02), Inches(0.6))
        line.line.fill.background()
        line.fill.solid()
        line.fill.fore_color.rgb = RGBColor(255, 255, 255)
        srgbClr = line.element.spPr.find(".//{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr")
        srgbClr.append(parse_xml('<a:alpha xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" val="50000"/>'))
        
        txBox = slide.shapes.add_textbox(cx - Inches(0.75), cy - h - 2*dy - Inches(1.3), Inches(1.5), Inches(0.5))
        p = txBox.text_frame.paragraphs[0]
        p.text = value_text
        p.alignment = PP_ALIGN.CENTER
        p.font.name = "Arial"
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = RGBColor.from_string(top_hex)

    # Geometry Setup for standard 2:1 isometric ratio
    dx = Inches(0.65)
    dy = Inches(0.325)
    baseline_y = Inches(6.0)

    # Data & Color Palette
    bars_data = [
        {"x": Inches(5.5), "h": Inches(2.0), "val": "45%", "grad": ("FFC107", "FF5722"), "top": "FFD54F"},
        {"x": Inches(8.0), "h": Inches(3.2), "val": "65%", "grad": ("00BCD4", "0288D1"), "top": "4DD0E1"},
        {"x": Inches(10.5), "h": Inches(4.5), "val": "80%", "grad": ("E040FB", "7B1FA2"), "top": "EA80FC"},
    ]

    for data in bars_data:
        draw_bar(data["x"], baseline_y, data["h"], dx, dy, data["grad"], data["top"], data["val"])

    prs.save(output_pptx_path)
    
    if os.path.exists(bg_path):
        os.remove(bg_path)
        
    return output_pptx_path
```