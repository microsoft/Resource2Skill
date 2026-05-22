# Duotone Brand-Aligned Overlay

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Duotone Brand-Aligned Overlay

* **Core Visual Mechanism**: This design pattern involves desaturating (grayscaling) a photographic background and applying a full-bleed or partial semi-transparent color overlay. This technique suppresses visual noise from the photo while imposing a strong, brand-specific color tint (a pseudo-duotone effect).
* **Why Use This Skill (Rationale)**: Photographs often contain busy textures and competing colors that make text illegible. By neutralizing the photo's original color palette and placing a transparent shape on top, you achieve high text contrast while retaining the emotional context and texture of the imagery. 
* **Overall Applicability**: This technique is highly effective for Title slides, KPI/Metric highlight slides (like the one demonstrated), quote slides, and section transitions. It is especially useful when creating a unified presentation deck out of disparate stock photos.
* **Value Addition**: Transforms chaotic stock imagery into polished, brand-compliant assets. It immediately establishes a modern, editorial visual hierarchy where data/text is the undisputed focal point.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Background**: Edge-to-edge photographic image converted to 0% saturation (grayscale).
  - **Color Mask**: A vector rectangle spanning the canvas, filled with a brand color (e.g., Slate Navy `RGBA(44, 76, 104, 178)`) with ~30% transparency. 
  - **Typography Hierarchy**: Stark white text for maximum contrast. Broken into microcopy (small, normal weight) and macro-metrics (oversized, heavy weight).

* **Step B: Compositional Style**
  - **Left-Aligned Gravity**: Content is anchored to the left margin (approx. 10% of canvas width), giving the composition a structured, modern editorial layout. 
  - **Proportional Scaling**: The focal metric ("9%") is scaled roughly 400% larger than the supporting microcopy ("Only", "gets recycled"), occupying almost a third of the vertical canvas.

* **Step C: Dynamic Effects & Transitions**
  - **Animation**: Best paired with a subtle "Fade" transition for the background, and a "Wipe" (from left) or "Fade" for the text elements to emphasize the left-to-right reading pattern.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Grayscale Image Recoloring** | `PIL (Pillow)` | `python-pptx` cannot natively desaturate/recolor picture layers. PIL perfectly replicates PowerPoint's "0% Saturation" picture format option. |
| **Shape Transparency** | `lxml` XML Injection | `python-pptx` does not expose an API for shape transparency. Direct OOXML manipulation creates a native, editable PowerPoint shape overlay. |
| **Text Layout & Hierarchy** | `python-pptx` native | Standard placement of text boxes with distinct font formatting achieves the desired typographic contrast. |

> **Feasibility Assessment**: 100% reproducible. The code directly outputs the final aesthetic shown in the tutorial, complete with native PowerPoint shape editability for the transparent overlay. 

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "9%",
    body_text: str = "Only\ngets recycled",
    bg_palette: str = "environment",
    accent_color: tuple = (44, 76, 104),  # Slate Navy Blue
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Duotone Brand Overlay visual effect.
    """
    import os
    import urllib.request
    from PIL import Image
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.oxml.ns import qn
    from lxml import etree

    # Initialize presentation (16:9 format)
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

    # === Layer 1: Background Image (Grayscale processing via PIL) ===
    bg_path = "temp_bg_gray.jpg"
    try:
        # Fetch placeholder image
        url = f"https://picsum.photos/seed/{bg_palette}/1920/1080"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            with open("temp_raw_bg.jpg", "wb") as f:
                f.write(response.read())
        
        # Process image with Pillow
        img = Image.open("temp_raw_bg.jpg")
        
        # Crop exactly to 16:9 to prevent distortion
        target_aspect = 16 / 9
        w, h = img.size
        aspect = w / h
        if aspect > target_aspect:
            new_w = int(h * target_aspect)
            left = (w - new_w) / 2
            img = img.crop((left, 0, left + new_w, h))
        elif aspect < target_aspect:
            new_h = int(w / target_aspect)
            top = (h - new_h) / 2
            img = img.crop((0, top, w, top + new_h))
            
        # Desaturate (Convert to Grayscale)
        img = img.convert('L')
        img.save(bg_path)
    except Exception as e:
        # Fallback if download fails
        img = Image.new('L', (1920, 1080), color=100)
        img.save(bg_path)

    # Insert background
    slide.shapes.add_picture(bg_path, 0, 0, prs.slide_width, prs.slide_height)

    # === Layer 2: Transparent Brand Color Overlay (lxml XML injection) ===
    overlay = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
    )
    overlay.fill.solid()
    overlay.fill.fore_color.rgb = RGBColor(*accent_color)
    overlay.line.fill.background()  # Remove outline

    # Inject alpha transparency natively into OOXML (70% opaque = 30% transparent)
    spPr = overlay.element
    srgbClr = spPr.find('.//a:srgbClr', namespaces={'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'})
    if srgbClr is not None:
        alpha = etree.SubElement(srgbClr, qn('a:alpha'))
        alpha.set('val', '70000')  # PPTX expects 100000 base for opacity

    # === Layer 3: Typography ===
    body_parts = body_text.split('\n')
    top_text = body_parts[0] if len(body_parts) > 0 else ""
    bottom_text = body_parts[1] if len(body_parts) > 1 else ""

    left_margin = Inches(1.0)

    # Microcopy: Top
    if top_text:
        txBox1 = slide.shapes.add_textbox(left_margin, Inches(1.8), Inches(5), Inches(1))
        tf1 = txBox1.text_frame
        tf1.margin_left = 0
        p1 = tf1.paragraphs[0]
        p1.text = top_text
        p1.font.size = Pt(36)
        p1.font.name = 'Arial'
        p1.font.color.rgb = RGBColor(255, 255, 255)

    # Macro-metric: Center Huge
    txBox2 = slide.shapes.add_textbox(left_margin, Inches(2.2), Inches(8), Inches(2.5))
    tf2 = txBox2.text_frame
    tf2.margin_left = 0
    p2 = tf2.paragraphs[0]
    p2.text = title_text
    p2.font.size = Pt(160)
    p2.font.bold = True
    p2.font.name = 'Arial'
    p2.font.color.rgb = RGBColor(255, 255, 255)

    # Microcopy: Bottom
    if bottom_text:
        txBox3 = slide.shapes.add_textbox(left_margin, Inches(4.7), Inches(8), Inches(1))
        tf3 = txBox3.text_frame
        tf3.margin_left = 0
        p3 = tf3.paragraphs[0]
        p3.text = bottom_text
        p3.font.size = Pt(36)
        p3.font.bold = True
        p3.font.name = 'Arial'
        p3.font.color.rgb = RGBColor(255, 255, 255)

    # Save and clean up
    prs.save(output_pptx_path)
    for tmp in ["temp_raw_bg.jpg", bg_path]:
        if os.path.exists(tmp):
            os.remove(tmp)
            
    return output_pptx_path
```

#### 3c. Verification Checklist
- [x] Does the code import all required libraries? (Yes, `PIL`, `urllib`, `lxml`, `pptx` handled)
- [x] Does it handle the case where an image download fails (fallback)? (Yes, PIL generates a gray base)
- [x] Are all color values explicit RGBA tuples? (Yes, Slate Navy and White explicitly declared)
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect? (Yes, implements the highest-contrast method 3 shown in the video)
- [x] Would someone looking at the output say "yes, that's the same technique"? (Yes, features the desaturation, precise transparent tint, and massive metric typography layout)