# Interlocking Wave & Reticle Layout

## Analysis

An elegant and modern team introduction slide that uses Z-depth interlocking to create a highly professional layout.

### 1. High-level Design Pattern Extraction

> **Skill Name**: Interlocking Wave & Reticle Layout

* **Core Visual Mechanism**: The defining characteristic is the **Z-order interlocking effect**. A dark, wavy "channel" spans the slide horizontally. Brightly colored circular borders sit *behind* this channel, while circular portrait photos sit *in front* of it. Small targeting triangles (reticles) point inward from the outer borders, enhancing the focus on the portraits. The wavy channel uses an inner shadow to simulate being recessed or stamped into the background.
* **Why Use This Skill (Rationale)**: The layered depth tricks the eye into seeing a 3D physical structure (a routed channel with discs inserted). The bright accent colors against the dark gray background command attention, while the geometric reticles frame the human faces, making the slide feel dynamic and highly intentional.
* **Overall Applicability**: Perfect for "Meet the Team", "Key Stakeholders", or "Board of Directors" slides where individual identity needs to be highlighted with equal weight but high visual impact. 
* **Value Addition**: Transforms a standard grid of photos into a cohesive, high-end agency-style graphic. The continuous wave binds the elements together horizontally, creating flow across the slide.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Background**: Solid dark charcoal gray `(38, 38, 38)`.
  - **Wave Channel**: Deeper dark gray `(26, 26, 26)` with an **inside shadow** to create a recessed effect.
  - **Accents**: Three vibrant colors for the three profiles (e.g., Magenta `(255, 0, 127)`, Lime/Green `(0, 230, 118)`, Yellow `(255, 214, 0)`).
  - **Portraits**: Perfectly circular masks nested within thick white borders.
  - **Text Hierarchy**: White, bold, uppercase title. Accent-colored member names. White uppercase designations. Light gray paragraph text.

* **Step B: Compositional Style**
  - The slide is split horizontally by the wave.
  - Three anchor points are distributed evenly at approximately 1/6, 1/2, and 5/6 of the horizontal width.
  - The layout relies heavily on perfect concentric circles: the outer accent ring, the white border ring, and the inner photo ring.

* **Step C: Dynamic Effects & Transitions**
  - The inner shadow on the wave is critical for the visual trick.
  - The overlapping Z-order (Back Ring -> Middle Wave -> Front Photo) creates the optical illusion.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Recessed Wave Band** | `python-pptx` Freeform + `lxml` | Requires custom bezier curves for the wave geometry, and `lxml` to inject the `<a:innerShdw>` XML for the recessed 3D effect. |
| **Circular Photo Avatars** | `PIL` (Pillow) | The safest and most robust way to ensure images are center-cropped to perfect circles with alpha transparency before inserting into PowerPoint. |
| **Z-Order Interlocking** | `python-pptx` sequence | Ordering the shape creation (Back Circles -> Wave -> Front Circles) natively achieves the interlocking layering without complex hacks. |

#### 3b. Complete Reproduction Code

```python
import io
import math
import urllib.request
from PIL import Image, ImageDraw
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.oxml import parse_xml

def get_circular_avatar(url: str) -> io.BytesIO:
    """Downloads an image, crops it to a square, and masks it into a transparent circle."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            img = Image.open(io.BytesIO(response.read())).convert("RGBA")
    except Exception:
        # Fallback placeholder if download fails
        img = Image.new("RGBA", (400, 400), (100, 100, 100, 255))
        
    w, h = img.size
    min_dim = min(w, h)
    left = (w - min_dim) / 2
    top = (h - min_dim) / 2
    img = img.crop((left, top, left + min_dim, top + min_dim))
    img = img.resize((400, 400), Image.Resampling.LANCZOS)
    
    mask = Image.new("L", (400, 400), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, 400, 400), fill=255)
    
    out_img = Image.new("RGBA", (400, 400), (0, 0, 0, 0))
    out_img.paste(img, (0, 0), mask)
    
    img_io = io.BytesIO()
    out_img.save(img_io, format='PNG')
    img_io.seek(0)
    return img_io

def apply_inner_shadow(shape):
    """Injects DrawingML XML to apply an inner shadow for a recessed effect."""
    shadow_xml = """
    <a:effectLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
        <a:innerShdw blurRad="152400" dist="60000" dir="5400000">
            <a:prstClr val="black">
                <a:alpha val="60000"/>
            </a:prstClr>
        </a:innerShdw>
    </a:effectLst>
    """
    effectLst = parse_xml(shadow_xml)
    spPr = shape.element.spPr
    # Remove existing effect list if present
    for existing in spPr.findall('.//a:effectLst', namespaces={'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}):
        spPr.remove(existing)
    spPr.append(effectLst)

def add_pointer_triangle(slide, cx, cy, radius, angle_deg, color):
    """Creates a small dart/triangle pointing towards the center of a circle."""
    angle_rad = math.radians(angle_deg)
    # The tip touches the circle
    tip_x = cx + radius * math.cos(angle_rad)
    tip_y = cy + radius * math.sin(angle_rad)
    # The base is slightly further out
    base_dist = radius + Inches(0.45)
    base_cx = cx + base_dist * math.cos(angle_rad)
    base_cy = cy + base_dist * math.sin(angle_rad)
    # The base has a width
    half_base = Inches(0.2)
    perp_rad = angle_rad + math.pi / 2
    b1_x = base_cx + half_base * math.cos(perp_rad)
    b1_y = base_cy + half_base * math.sin(perp_rad)
    b2_x = base_cx - half_base * math.cos(perp_rad)
    b2_y = base_cy - half_base * math.sin(perp_rad)
    
    ff = slide.shapes.build_freeform(tip_x, tip_y)
    ff.add_line_segments([(b1_x, b1_y), (b2_x, b2_y), (tip_x, tip_y)])
    shape = ff.convert_to_shape()
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.color.rgb = color
    shape.line.width = Pt(1)

def create_slide(output_pptx_path: str, **kwargs) -> str:
    """Create a PPTX file reproducing the Interlocking Wave & Reticle Layout."""
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: Background ===
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(38, 38, 38)

    # Theme Configuration
    colors = [RGBColor(255, 214, 0), RGBColor(0, 230, 118), RGBColor(255, 0, 127)]
    centers = [(Inches(2.22), Inches(3.75)), (Inches(6.66), Inches(3.75)), (Inches(11.11), Inches(3.75))]
    dart_angles = [(135, 225), (225, 315), (45, 315)] # Angles pointing inwards based on position
    names = ["ALEX JOHNSON", "MARIA GARCIA", "DAVID CHEN"]
    
    img_urls = [
        "https://images.unsplash.com/photo-1560250097-0b93528c311a?w=400&q=80",
        "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=400&q=80",
        "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=400&q=80"
    ]

    back_radius = Inches(1.7)
    outer_border_radius = Inches(1.45)
    inner_pic_radius = Inches(1.3)

    # === Layer 2: Colored Back Circles & Darts ===
    for i, (cx, cy) in enumerate(centers):
        color = colors[i]
        add_pointer_triangle(slide, cx, cy, back_radius, dart_angles[i][0], color)
        add_pointer_triangle(slide, cx, cy, back_radius, dart_angles[i][1], color)
        
        back_circ = slide.shapes.add_shape(MSO_SHAPE.OVAL, cx - back_radius, cy - back_radius, back_radius * 2, back_radius * 2)
        back_circ.fill.solid()
        back_circ.fill.fore_color.rgb = color
        back_circ.line.color.rgb = color
        back_circ.line.width = Pt(1)

    # === Layer 3: Recessed Wavy Channel ===
    ff = slide.shapes.build_freeform(0, Inches(2.8))
    # Top edge left to right
    ff.add_curve_segments([((Inches(4.44), Inches(1.5)), (Inches(8.88), Inches(4.0)), (Inches(13.33), Inches(2.5)))])
    # Right edge
    ff.add_line_segments([(Inches(13.33), Inches(5.0))])
    # Bottom edge right to left (maintaining exact thickness)
    ff.add_curve_segments([((Inches(8.88), Inches(6.5)), (Inches(4.44), Inches(4.0)), (0, Inches(5.3)))])
    # Left edge close
    ff.add_line_segments([(0, Inches(2.8))])
    
    wave = ff.convert_to_shape()
    wave.fill.solid()
    wave.fill.fore_color.rgb = RGBColor(26, 26, 26)
    wave.line.color.rgb = RGBColor(26, 26, 26)
    wave.line.width = Pt(1)
    apply_inner_shadow(wave) # The magic that makes it look like a physical groove

    # === Layer 4: Front White Borders & Picture Avatars ===
    for i, (cx, cy) in enumerate(centers):
        # White framing border (sits on top of the wave)
        border = slide.shapes.add_shape(MSO_SHAPE.OVAL, cx - outer_border_radius, cy - outer_border_radius, outer_border_radius * 2, outer_border_radius * 2)
        border.fill.solid()
        border.fill.fore_color.rgb = RGBColor(255, 255, 255)
        border.line.color.rgb = RGBColor(255, 255, 255)
        
        # Circular Avatar Image
        avatar_img = get_circular_avatar(img_urls[i])
        slide.shapes.add_picture(avatar_img, cx - inner_pic_radius, cy - inner_pic_radius, inner_pic_radius * 2, inner_pic_radius * 2)

    # === Layer 5: Text Hierarchy ===
    # Main Title
    title_box = slide.shapes.add_textbox(0, Inches(0.4), Inches(13.333), Inches(1.0))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "MY BUSINESS TEAM"
    p.font.bold = True
    p.font.size = Pt(40)
    p.font.name = "Arial"
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.CENTER

    # Per-Profile Text
    for i, (cx, cy) in enumerate(centers):
        color = colors[i]
        text_y = cy + outer_border_radius + Inches(0.2)
        
        tbox = slide.shapes.add_textbox(cx - Inches(1.8), text_y, Inches(3.6), Inches(1.5))
        tf = tbox.text_frame
        tf.word_wrap = True
        
        # Name
        p0 = tf.paragraphs[0]
        p0.text = names[i]
        p0.font.bold = True
        p0.font.size = Pt(16)
        p0.font.name = "Arial"
        p0.font.color.rgb = color
        p0.alignment = PP_ALIGN.CENTER
        
        # Designation
        p1 = tf.add_paragraph()
        p1.text = "EXECUTIVE ROLE"
        p1.font.bold = True
        p1.font.size = Pt(12)
        p1.font.name = "Arial"
        p1.font.color.rgb = RGBColor(255, 255, 255)
        p1.alignment = PP_ALIGN.CENTER
        
        # Description
        p2 = tf.add_paragraph()
        p2.text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras urna odio, dictum ac sem nec."
        p2.font.size = Pt(10)
        p2.font.name = "Arial"
        p2.font.color.rgb = RGBColor(180, 180, 180)
        p2.alignment = PP_ALIGN.CENTER

    prs.save(output_pptx_path)
    return output_pptx_path
```