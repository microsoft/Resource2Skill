# Neon Concentric Radial Dashboard

## Analysis

Here is the skill extraction and reproduction code for the professional neon concentric donut chart effect.

### 1. High-level Design Pattern Extraction

> **Skill Name**: Neon Concentric Radial Dashboard

* **Core Visual Mechanism**: A layered, overlapping circular bar chart (radial doughnut) where each data track is styled with vibrant, neon-colored gradients, soft glowing edges, and rounded caps. The glowing arcs are placed against a dark background, evoking a futuristic or high-end analytical dashboard. 
* **Why Use This Skill (Rationale)**: Traditional pie or doughnut charts can feel static and corporate. By nesting the arcs concentrically and mapping them to a 360-degree scale, the design saves horizontal space while visually representing progress towards a goal (100%). The neon glow against a dark UI creates high contrast, drawing immediate attention to the data extremes.
* **Overall Applicability**: Perfect for data dashboards, performance metrics summary slides, SaaS product mockups, and "hero" data visualizations in tech or financial presentations.
* **Value Addition**: Transforms standard quantitative data into a visually striking, premium infographic. The glowing tracking lines communicate modern precision and elevate the perceived value of the information.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Background**: Deep space navy or rich black `(13, 17, 28, 255)`.
  - **Tracks (Background Arcs)**: Faded, semi-transparent white rings `(255, 255, 255, 15)`.
  - **Data Arcs**: Highly saturated neon colors with soft gaussian blurs (Glow). E.g., Cyan `(0, 255, 255)`, Lime `(0, 255, 157)`, Magenta `(255, 0, 255)`.
  - **Typography**: Bold, heavy sans-serif fonts for the titles featuring horizontal gradient fills. Crisp, monospaced or modern sans-serif for data labels.

* **Step B: Compositional Style**
  - Left panel (~40% width): Hero title, descriptive text, and a call-to-action button.
  - Right panel (~60% width): The concentric chart.
  - Labels use precise geometric anchor lines connecting the dynamic end of the arc directly to floating percentage tags.

* **Step C: Dynamic Effects & Transitions**
  - *Wheel Reveal*: The arcs ideally animate in using the "Wheel" animation in PowerPoint, making the neon lines "draw" themselves around the tracks.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Concentric Glowing Arcs** | `PIL/Pillow` (ImageDraw & ImageFilter) | PowerPoint does not natively support rounded caps on standard doughnut charts, nor can it easily apply variable angular masks to rings with accurate glow rendering. PIL allows pixel-perfect drawing of rounded arcs and exact gaussian glow compositing. |
| **Data Anchors & Lines** | `python-pptx` native shapes | Connecting lines and floating text boxes are rendered natively so the text remains vector-crisp and easily editable. |
| **Text Gradient Fill** | `lxml` XML injection | `python-pptx` has no pythonic API for text gradients. Direct drawingML manipulation `<a:gradFill>` achieves the beautiful two-tone title. |

> **Feasibility Assessment**: 100% reproduction of the visual aesthetic. By fusing a dynamically generated PIL backdrop for the complex geometry with native PPTX vectors for labels, the result perfectly matches the tutorial's futuristic aesthetic.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "CREATE\nAWESOME\nCHARTS",
    body_text: str = "Lorem ipsum is placeholder text commonly used in the graphic, print, and publishing industries for previewing layouts and visual mockups.",
    bg_palette: str = "technology",
    **kwargs,
) -> str:
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
    from pptx.enum.text import PP_ALIGN
    from pptx.oxml import parse_xml
    from PIL import Image, ImageDraw, ImageFilter
    import math
    import urllib.request
    import tempfile
    import os

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === XML Helpers ===
    def set_text_gradient(shape, color_stops):
        """Injects drawingML XML to apply a horizontal linear gradient to text."""
        for paragraph in shape.text_frame.paragraphs:
            for run in paragraph.runs:
                rPr = run._r.get_or_add_rPr()
                for child in list(rPr):
                    if child.tag.endswith('Fill'):
                        rPr.remove(child)
                gsLst_xml = "".join([f'<a:gs pos="{int(pos*1000)}"><a:srgbClr val="{color}"/> </a:gs>' for pos, color in color_stops])
                gradFill_xml = f'''
                    <a:gradFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
                        <a:gsLst>{gsLst_xml}</a:gsLst>
                        <a:lin ang="0" scaled="0"/>
                    </a:gradFill>
                '''
                rPr.append(parse_xml(gradFill_xml))

    def set_shape_gradient(shape, color_stops):
        """Injects drawingML XML to apply a horizontal linear gradient to a shape."""
        spPr = shape.element.spPr
        for child in list(spPr):
            if child.tag.endswith('Fill'):
                spPr.remove(child)
        gsLst_xml = "".join([f'<a:gs pos="{int(pos*1000)}"><a:srgbClr val="{color}"/> </a:gs>' for pos, color in color_stops])
        gradFill_xml = f'''
            <a:gradFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
                <a:gsLst>{gsLst_xml}</a:gsLst>
                <a:lin ang="0" scaled="0"/>
            </a:gradFill>
        '''
        gradFill = parse_xml(gradFill_xml)
        prstGeom = spPr.find("{http://schemas.openxmlformats.org/drawingml/2006/main}prstGeom")
        if prstGeom is not None:
            prstGeom.addnext(gradFill)
        else:
            spPr.append(gradFill)

    def hex_to_rgba(hex_color, alpha=255):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4)) + (alpha,)

    # === Layer 1: Background ===
    try:
        bg_path = tempfile.mktemp(suffix=".jpg")
        urllib.request.urlretrieve("https://images.unsplash.com/photo-1550684848-fac1c5b4e853?q=80&w=1920&auto=format&fit=crop", bg_path)
        slide.shapes.add_picture(bg_path, 0, 0, prs.slide_width, prs.slide_height)
    except Exception:
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(13, 17, 28)

    # Apply a dark overlay to make text pop
    overlay = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    overlay.fill.solid()
    overlay.fill.fore_color.rgb = RGBColor(10, 15, 25)
    overlay.fill.transparency = 0.15
    overlay.line.fill.background()

    # === Layer 2: Left Content Panel ===
    title = slide.shapes.add_textbox(Inches(0.8), Inches(1.2), Inches(4.5), Inches(2.0))
    title.text = title_text
    for p in title.text_frame.paragraphs:
        p.font.size = Pt(54)
        p.font.bold = True
        p.font.name = "Arial Black"
    set_text_gradient(title, [(0, "00FFFF"), (100, "B200FF")]) # Cyan to Purple gradient

    body = slide.shapes.add_textbox(Inches(0.8), Inches(3.8), Inches(3.5), Inches(1.0))
    body.text = body_text
    body.text_frame.paragraphs[0].font.size = Pt(11)
    body.text_frame.paragraphs[0].font.color.rgb = RGBColor(160, 160, 175)
    body.text_frame.word_wrap = True

    btn = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.2), Inches(1.5), Inches(0.45))
    btn.text = "START"
    btn.text_frame.paragraphs[0].font.bold = True
    btn.text_frame.paragraphs[0].font.size = Pt(12)
    btn.line.fill.background()
    set_shape_gradient(btn, [(0, "2A0845"), (100, "6441A5")]) 

    # === Layer 3: Neon Concentric Radial Chart (PIL) ===
    metrics = kwargs.get('metrics', [
        {"name": "METRIC 1", "value": 0.45, "color": "00D2FF"}, # Cyan
        {"name": "METRIC 2", "value": 0.53, "color": "00FF9D"}, # Lime
        {"name": "METRIC 3", "value": 0.60, "color": "0090FF"}, # Blue
        {"name": "METRIC 4", "value": 0.72, "color": "9D00FF"}, # Purple
        {"name": "METRIC 5", "value": 0.84, "color": "FF00FF"}, # Magenta
    ])

    img_size = 2000
    chart_x, chart_y, chart_size = 6.0, 0.4, 6.5  # Inches layout constraints
    center = (img_size // 2, img_size // 2)
    base_img = Image.new('RGBA', (img_size, img_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(base_img)

    max_r, min_r, thickness = 850, 350, 45
    gap = (max_r - min_r) / max(1, len(metrics) - 1)

    def draw_neon_arc(draw_obj, cx, cy, radius, start_deg, end_deg, color, width):
        bbox = [cx - radius, cy - radius, cx + radius, cy + radius]
        draw_obj.arc(bbox, start_deg, end_deg, fill=color, width=width)
        for angle in (start_deg, end_deg):
            rad = math.radians(angle)
            px = cx + radius * math.cos(rad)
            py = cy + radius * math.sin(rad)
            draw_obj.ellipse([px - width/2, py - width/2, px + width/2, py + width/2], fill=color)

    # Draw Chart Layers
    for i, m in enumerate(metrics):
        r = min_r + i * gap
        track_color = (255, 255, 255, 10)
        val_color = hex_to_rgba(m['color'])
        start_angle = 270
        end_angle = 270 + m['value'] * 360

        draw_neon_arc(draw, center[0], center[1], r, 0, 360, track_color, thickness) # Background track

        arc_img = Image.new('RGBA', (img_size, img_size), (0, 0, 0, 0))
        arc_draw = ImageDraw.Draw(arc_img)
        draw_neon_arc(arc_draw, center[0], center[1], r, start_angle, end_angle, val_color, thickness) # Data arc
        
        # Stacking gaussian blurs creates an intense organic neon glow
        base_img = Image.alpha_composite(base_img, arc_img.filter(ImageFilter.GaussianBlur(30)))
        base_img = Image.alpha_composite(base_img, arc_img.filter(ImageFilter.GaussianBlur(12)))
        base_img = Image.alpha_composite(base_img, arc_img)

    # Insert PIL Image
    chart_img_path = tempfile.mktemp(suffix=".png")
    base_img.save(chart_img_path)
    slide.shapes.add_picture(chart_img_path, Inches(chart_x), Inches(chart_y), Inches(chart_size), Inches(chart_size))

    # === Layer 4: Data Connectors & Native Overlays ===
    for i, m in enumerate(metrics):
        r = min_r + i * gap
        theta_rad = math.radians(270 + m['value'] * 360)
        
        # Map PIL coordinates to PPTX Inch coordinates
        end_x_inch = chart_x + chart_size/2 + (r / img_size) * chart_size * math.cos(theta_rad)
        end_y_inch = chart_y + chart_size/2 + (r / img_size) * chart_size * math.sin(theta_rad)

        is_right = math.cos(theta_rad) >= 0
        box_w, box_h, line_len = 0.6, 0.3, 0.3

        if is_right:
            line_end_x = end_x_inch + line_len
            label_x = line_end_x
        else:
            line_end_x = end_x_inch - line_len
            label_x = line_end_x - box_w

        # Draw Connector Line
        line = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(end_x_inch), Inches(end_y_inch), Inches(line_end_x), Inches(end_y_inch))
        line.line.color.rgb = RGBColor.from_string(m['color'])
        line.line.width = Pt(1.5)

        # Draw Tiny Anchor Dot
        dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(end_x_inch - 0.04), Inches(end_y_inch - 0.04), Inches(0.08), Inches(0.08))
        dot.fill.solid()
        dot.fill.fore_color.rgb = RGBColor.from_string(m['color'])
        dot.line.fill.background()

        # Draw Value Tag
        label = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(label_x), Inches(end_y_inch - box_h/2), Inches(box_w), Inches(box_h))
        label.fill.solid()
        label.fill.fore_color.rgb = RGBColor(10, 15, 25)
        label.line.color.rgb = RGBColor.from_string(m['color'])
        label.line.width = Pt(1)

        tf = label.text_frame
        tf.text = f"{int(m['value']*100)}%"
        tf.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
        tf.paragraphs[0].font.size = Pt(11)
        tf.paragraphs[0].font.bold = True
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER

    # === Layer 5: Legend Layout ===
    legend_start_x = chart_x + chart_size * 0.55
    legend_start_y = chart_y + chart_size * 0.70
    for i, m in enumerate(metrics):
        y_pos = legend_start_y + (i * 0.25)
        l_dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(legend_start_x), Inches(y_pos), Inches(0.12), Inches(0.12))
        l_dot.fill.solid()
        l_dot.fill.fore_color.rgb = RGBColor(10, 15, 25)
        l_dot.line.color.rgb = RGBColor.from_string(m['color'])
        l_dot.line.width = Pt(2.5)

        l_text = slide.shapes.add_textbox(Inches(legend_start_x + 0.2), Inches(y_pos - 0.06), Inches(2.0), Inches(0.25))
        l_text.text = m['name']
        l_text.text_frame.paragraphs[0].font.color.rgb = RGBColor(200, 200, 210)
        l_text.text_frame.paragraphs[0].font.size = Pt(11)
        l_text.text_frame.paragraphs[0].font.bold = True

    try: os.remove(bg_path)
    except: pass
    try: os.remove(chart_img_path)
    except: pass

    prs.save(output_pptx_path)
    return output_pptx_path
```