# Symmetrical Node Flow Infographic (Stylized Barbell)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Symmetrical Node Flow Infographic (Stylized Barbell)

* **Core Visual Mechanism**: A stark, highly contrasted central focal point (a white circle) flanked by two symmetrical, teardrop-shaped nodes that visually anchor into the center. Semicircular arrows wrap the center, suggesting a continuous, cyclical relationship between the two lateral nodes. Depth is established through overlapping layers and subtle, straight-down drop shadows against a rich radial gradient background.
* **Why Use This Skill (Rationale)**: This layout inherently communicates balance, contrast, and relationship. It pulls the eye directly to the center (the core concept) while giving equal weight to two supporting pillars, options, or outcomes. The arrows prevent the design from feeling static by introducing a sense of flow.
* **Overall Applicability**: Ideal for comparison slides ("Option A vs. Option B"), bidirectional processes, cause-and-effect relationships, or introducing a core product with two main feature categories.
* **Value Addition**: Transforms a standard bulleted comparison into a premium, conceptual diagram. The custom-looking geometry (achieved via cleverly rotated teardrop shapes) gives the slide a bespoke, agency-level aesthetic that standard smart-art lacks.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Background**: Deep radial gradient focusing light behind the central circle. Center: Rich Purple `(89, 39, 138)`, Edge: Dark Indigo `(30, 10, 54)`.
  - **Side Nodes**: Custom "flared" shapes created natively using rotated Teardrop shapes. Color: Deep Purple `(69, 30, 107)`.
  - **Central Node**: Crisp white `(255, 255, 255)` circle acting as the visual anchor.
  - **Arrows**: Bright violet `(181, 107, 250)` arcs with triangular arrowheads wrapping the center.
  - **Typography**: Dark purple headings in the center for contrast; white/light gray text on the dark side nodes.

* **Step B: Compositional Style**
  - Perfect horizontal symmetry.
  - The central circle overlaps the points of the side teardrops, effortlessly creating a complex "filleted" structural look without requiring boolean shape operations.
  - Generous negative space around the horizontal axis to let the central diagram breathe.

* **Step C: Dynamic Effects & Transitions**
  - 3D layering achieved via exact z-order placement (Background -> Nodes -> Arrows -> Center Node).
  - LXML-injected drop shadows (blur 10pt, distance 3pt) applied to the solid shapes to lift them off the background.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Radial Gradient Background** | `PIL/Pillow` | `python-pptx` cannot reliably set high-quality radial gradients across all PPTX renderer versions. |
| **Complex Side Node Geometry** | `python-pptx` native | Rotating standard `MSO_SHAPE.TEARDROP` shapes perfectly replicates the video's custom boolean geometry while retaining vector scalability. |
| **Drop Shadows** | `lxml` XML injection | Native API lacks shadow controls; XML injection creates perfect, renderer-native outer shadows. |
| **Wrapping Arrows** | `lxml` XML injection | Setting precise start/end angles and adding arrowhead styles to `MSO_SHAPE.ARC` requires direct XML manipulation. |

#### 3b. Complete Reproduction Code

```python
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.oxml.xmlchemy import OxmlElement
from PIL import Image

def add_shadow(shape, blur_pt=10, dist_pt=3, angle_deg=90, alpha_pct=30):
    """Injects a native PowerPoint drop shadow using lxml."""
    spPr = shape.element.spPr
    effectLst = spPr.find(f'{{http://schemas.openxmlformats.org/drawingml/2006/main}}effectLst')
    if effectLst is None:
        effectLst = OxmlElement('a:effectLst')
        spPr.append(effectLst)
    
    outerShdw = OxmlElement('a:outerShdw')
    outerShdw.set('blurRad', str(int(blur_pt * 12700)))
    outerShdw.set('dist', str(int(dist_pt * 12700)))
    outerShdw.set('dir', str(int(angle_deg * 60000)))
    outerShdw.set('algn', 'ctr')
    
    srgbClr = OxmlElement('a:srgbClr')
    srgbClr.set('val', '000000')
    alpha = OxmlElement('a:alpha')
    alpha.set('val', str(int(alpha_pct * 1000)))
    srgbClr.append(alpha)
    outerShdw.append(srgbClr)

def remove_fill(shape):
    """Removes all fill elements from a shape to make it truly transparent."""
    spPr = shape.element.spPr
    for fill_el in spPr.xpath('./a:solidFill | ./a:gradFill | ./a:pattFill | ./a:blipFill | ./a:noFill'):
        spPr.remove(fill_el)
    noFill = OxmlElement('a:noFill')
    spPr.insert(0, noFill)

def set_arc_properties(shape, start_deg, end_deg):
    """Sets exact arc angles and appends a triangular arrowhead."""
    # Set Angles
    avLst = shape.element.xpath('.//a:avLst')
    if not avLst:
        avLst = OxmlElement('a:avLst')
        shape.element.spPr.insert(1, avLst)
    else:
        avLst = avLst[0]
        for gd in avLst.xpath('a:gd'):
            avLst.remove(gd)
            
    gd1 = OxmlElement('a:gd')
    gd1.set('name', 'adj1')
    gd1.set('fmla', f'val {int(start_deg * 60000)}')
    avLst.append(gd1)
    
    gd2 = OxmlElement('a:gd')
    gd2.set('name', 'adj2')
    gd2.set('fmla', f'val {int(end_deg * 60000)}')
    avLst.append(gd2)
    
    # Add Arrowhead to Tail (End of drawing path)
    ln = shape.element.spPr.ln
    if ln is not None:
        tail = OxmlElement('a:tailEnd')
        tail.set('type', 'triangle')
        tail.set('w', 'med')
        tail.set('len', 'med')
        ln.append(tail)

def create_radial_bg_pil(filepath):
    """Generates a high-quality radial gradient background image."""
    w, h = 320, 180  # Render small, scale up for speed and smooth blur
    img = Image.new('RGB', (w, h))
    pixels = img.load()
    cx, cy = w / 2, h / 2
    max_d = (cx**2 + cy**2)**0.5
    
    c_center = (89, 39, 138)
    c_edge = (30, 10, 54)
    
    for y in range(h):
        for x in range(w):
            d = ((x - cx)**2 + (y - cy)**2)**0.5
            ratio = min(d / max_d, 1.0)
            r = int(c_center[0] * (1 - ratio) + c_edge[0] * ratio)
            g = int(c_center[1] * (1 - ratio) + c_edge[1] * ratio)
            b = int(c_center[2] * (1 - ratio) + c_edge[2] * ratio)
            pixels[x, y] = (r, g, b)
            
    img = img.resize((1920, 1080), Image.Resampling.BICUBIC)
    img.save(filepath)

def add_formatted_text(slide, lines, left, top, width, height):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    
    for i, (text, size, bold, color) in enumerate(lines):
        p = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
        p.text = text
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(size)
        p.font.bold = bold
        p.font.color.rgb = RGBColor(*color)
    return txBox

def create_slide(output_pptx_path: str, **kwargs) -> str:
    """
    Create a PPTX file reproducing the Symmetrical Node Flow visual effect.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    cx, cy = 13.333 / 2, 7.5 / 2

    # === Layer 1: Radial Gradient Background ===
    bg_path = "temp_radial_bg.png"
    create_radial_bg_pil(bg_path)
    slide.shapes.add_picture(bg_path, 0, 0, prs.slide_width, prs.slide_height)
    os.remove(bg_path)

    node_color = RGBColor(69, 30, 107)
    
    # === Layer 2: Side Nodes (Using Rotated Teardrops) ===
    # Left Teardrop (Point rightwards towards center)
    left_node = slide.shapes.add_shape(
        MSO_SHAPE.TEARDROP, Inches(cx - 2.45), Inches(cy - 1.75), Inches(1.4), Inches(3.5)
    )
    left_node.rotation = 90
    left_node.fill.solid()
    left_node.fill.fore_color.rgb = node_color
    left_node.line.fill.background()
    add_shadow(left_node, blur_pt=8, dist_pt=2)

    # Right Teardrop (Point leftwards towards center)
    right_node = slide.shapes.add_shape(
        MSO_SHAPE.TEARDROP, Inches(cx + 1.05), Inches(cy - 1.75), Inches(1.4), Inches(3.5)
    )
    right_node.rotation = 270
    right_node.fill.solid()
    right_node.fill.fore_color.rgb = node_color
    right_node.line.fill.background()
    add_shadow(right_node, blur_pt=8, dist_pt=2)

    # === Layer 3: Central Anchor Circle ===
    center_circle = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, Inches(cx - 1.4), Inches(cy - 1.4), Inches(2.8), Inches(2.8)
    )
    center_circle.fill.solid()
    center_circle.fill.fore_color.rgb = RGBColor(255, 255, 255)
    center_circle.line.fill.background()
    add_shadow(center_circle, blur_pt=12, dist_pt=4, alpha_pct=40)

    # Decorative Inner Dashed Circle
    inner_dash = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, Inches(cx - 1.2), Inches(cy - 1.2), Inches(2.4), Inches(2.4)
    )
    remove_fill(inner_dash)
    inner_dash.line.color.rgb = RGBColor(220, 220, 220)
    inner_dash.line.width = Pt(1)
    inner_dash.line.dash_style = 4  # Dashed

    # === Layer 4: Cyclical Arrows ===
    arc_color = (181, 107, 250)
    
    # Top Arc
    top_arc = slide.shapes.add_shape(
        MSO_SHAPE.ARC, Inches(cx - 2.1), Inches(cy - 2.1), Inches(4.2), Inches(4.2)
    )
    remove_fill(top_arc)
    top_arc.line.color.rgb = RGBColor(*arc_color)
    top_arc.line.width = Pt(4)
    set_arc_properties(top_arc, start_deg=200, end_deg=340)
    
    # Bottom Arc
    bottom_arc = slide.shapes.add_shape(
        MSO_SHAPE.ARC, Inches(cx - 2.1), Inches(cy - 2.1), Inches(4.2), Inches(4.2)
    )
    remove_fill(bottom_arc)
    bottom_arc.line.color.rgb = RGBColor(*arc_color)
    bottom_arc.line.width = Pt(4)
    set_arc_properties(bottom_arc, start_deg=20, end_deg=160)

    # === Layer 5: Decorative End Caps & Typography ===
    # Left End Cap
    l_cap = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(cx - 3.75), Inches(cy - 0.25), Inches(0.5), Inches(0.5))
    l_cap.fill.solid()
    l_cap.fill.fore_color.rgb = node_color
    l_cap.line.color.rgb = RGBColor(255, 255, 255)
    l_cap.line.width = Pt(1.5)
    
    # Right End Cap
    r_cap = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(cx + 3.25), Inches(cy - 0.25), Inches(0.5), Inches(0.5))
    r_cap.fill.solid()
    r_cap.fill.fore_color.rgb = node_color
    r_cap.line.color.rgb = RGBColor(255, 255, 255)
    r_cap.line.width = Pt(1.5)

    # Texts
    add_formatted_text(slide, [
        ("OPTION", 12, True, (255, 255, 255)),
        ("This is sample text.\nYou can replace it.", 9, False, (200, 180, 220))
    ], Inches(cx - 3.4), Inches(cy - 0.8), Inches(2.0), Inches(1.0))

    add_formatted_text(slide, [
        ("OPTION", 12, True, (255, 255, 255)),
        ("This is sample text.\nYou can replace it.", 9, False, (200, 180, 220))
    ], Inches(cx + 1.4), Inches(cy - 0.8), Inches(2.0), Inches(1.0))

    add_formatted_text(slide, [
        ("INFOGRAPHIC", 16, True, (45, 10, 78)),
        ("Lorem ipsum dolor sit amet,\nconsectetur adipiscing elit.\nSed do eiusmod tempor.", 9, False, (100, 100, 100))
    ], Inches(cx - 1.0), Inches(cy - 0.6), Inches(2.0), Inches(1.2))

    prs.save(output_pptx_path)
    return output_pptx_path
```