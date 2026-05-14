# Geometric Split-Screen Gradient Overlay

## Analysis

Here is the extracted skill strategy based on your provided video tutorial.

### 1. High-level Design Pattern Extraction

> **Skill Name**: Geometric Split-Screen Gradient Overlay

* **Core Visual Mechanism**: A full-bleed background photograph is visually bisected by a semi-transparent, colored geometric overlay (diagonal, stepped, or vertical). A stark white boundary line separates the "tinted" zone from the "raw" photographic zone. This creates a high-contrast, dual-tone aesthetic over which central typography is anchored.
* **Why Use This Skill (Rationale)**: The split-screen approach injects instant visual tension and cinematic framing into static imagery. It naturally leads the eye along the dividing geometry right into the center of the slide where the text resides. The tinted half provides a guaranteed high-contrast background area to ensure typography remains legible regardless of the underlying photo.
* **Overall Applicability**: Perfect for high-impact title slides, portfolio hero sections, transition markers, and dramatic concluding "Thank You" slides.
* **Value Addition**: Transforms standard stock photography into bespoke, branded graphic assets. It feels much more premium and highly produced than a simple full-slide image with a text box.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Background**: Full-bleed photograph (preferably expansive landscapes or distinct portraits).
  - **Overlay Mask**: A sharp polygon filling exactly one side of the layout. Colored with a semi-transparent dark or vibrant tint (e.g., `(20, 30, 50, 160)` or `(255, 100, 150, 120)`).
  - **Boundary Line**: A thick, crisp border (e.g., `(255, 255, 255, 255)`, 8px width) mapping the exact contour of the split.
  - **Typography Block**: A transparent geometric box featuring a bold white border matching the split line weight, framing stark, widely-spaced uppercase typography.

* **Step B: Compositional Style**
  - The canvas feels evenly split, maintaining a 50/50 or 60/40 visual weight distribution.
  - Text is strictly center-aligned on both X and Y axes, floating above the split to physically bridge the raw and tinted zones.
  - Wide letter spacing (~15pt) is applied to uppercase text to give it a cinematic, monumental scale.

* **Step C: Dynamic Effects & Transitions**
  - In motion, these elements often slide in laterally or cross-fade. However, the static layout itself provides an intrinsic "before/after" dynamic frozen in time. 

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Geometric Split Overlay & Line** | `PIL/Pillow` | Native `python-pptx` freeform shapes can be difficult to align perfectly to edges and lack clean corner joint handling for stepped lines. Drawing an RGBA mask with PIL guarantees pixel-perfect geometry and smooth, continuous boundary lines. |
| **Transparent Outline Text Box** | `lxml` XML injection | Native `python-pptx` lacks a direct API to set `<a:noFill/>` reliably without risking inheritance issues. Modifying the XML directly guarantees a perfectly transparent framing box. |
| **Typography Shadow & Spacing** | `lxml` XML injection | Wide letter spacing and crisp drop shadows are hallmarks of this style but are inaccessible via standard API wrappers. Injecting `a:spc` and `a:outerShdw` unlocks this premium typography tier. |

> **Feasibility Assessment**: 100% of the static visual aesthetic is perfectly reproduced. The Python function dynamically renders the precise shapes (including the complex "stepped" variation) directly onto the image canvas.

#### 3b. Complete Reproduction Code

```python
import os
import io
import tempfile
import urllib.request
from PIL import Image, ImageDraw
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml import OxmlElement

def create_slide(
    output_pptx_path: str,
    title_text: str = "THANK YOU",
    overlay_style: str = "diagonal",  # Choose from: 'diagonal', 'stepped', 'vertical'
    bg_image_url: str = "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?q=80&w=1920&h=1080&fit=crop",
    overlay_color: tuple = (20, 30, 50, 160),  # Deep navy tint
    line_color: tuple = (255, 255, 255, 255),  # Pure white
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the "Geometric Split-Screen Gradient Overlay" effect.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # blank layout

    # 1. Fetch Background Image (with solid color fallback)
    try:
        req = urllib.request.Request(bg_image_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            bg_image = Image.open(io.BytesIO(response.read())).convert("RGBA")
            bg_image = bg_image.resize((1920, 1080))
    except Exception:
        bg_image = Image.new("RGBA", (1920, 1080), (50, 50, 60, 255))

    # 2. Generate Geometric Overlay Mask using PIL
    overlay = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    line_width = 8

    if overlay_style == "vertical":
        draw.rectangle([0, 0, 960, 1080], fill=overlay_color)
        draw.line([(960, 0), (960, 1080)], fill=line_color, width=line_width)
        
    elif overlay_style == "stepped":
        points = [(0, 0), (800, 0), (800, 350), (1200, 350), (1200, 750), (1920, 750), (1920, 1080), (0, 1080)]
        draw.polygon(points, fill=overlay_color)
        # Draw contiguous boundary line using curve joints for crisp corners
        boundary = [(800, 0), (800, 350), (1200, 350), (1200, 750), (1920, 750)]
        draw.line(boundary, fill=line_color, width=line_width, joint="curve")
        
    else:  # 'diagonal' (Default)
        draw.polygon([(0, 0), (0, 1080), (1920, 1080)], fill=overlay_color)
        draw.line([(0, 0), (1920, 1080)], fill=line_color, width=line_width)

    # 3. Save and Insert Images with exact z-ordering
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_bg:
        bg_image.save(tmp_bg.name)
        bg_path = tmp_bg.name

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_overlay:
        overlay.save(tmp_overlay.name)
        overlay_path = tmp_overlay.name

    slide.shapes.add_picture(bg_path, 0, 0, width=prs.slide_width, height=prs.slide_height)
    slide.shapes.add_picture(overlay_path, 0, 0, width=prs.slide_width, height=prs.slide_height)

    os.unlink(bg_path)
    os.unlink(overlay_path)

    # 4. Add Central Framed Typography (Transparent Box + White Outline)
    left = Inches(3.166)
    top = Inches(2.75)
    width = Inches(7.0)
    height = Inches(2.0)

    rect = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    
    # Safely inject <a:noFill> right before <a:ln> to make the shape transparent
    spPr = rect._element.spPr
    fill_idx = -1
    for i, child in enumerate(list(spPr)):
        if 'Fill' in child.tag:
            fill_idx = i
            spPr.remove(child)
            
    noFill = OxmlElement('a:noFill')
    if fill_idx != -1:
        spPr.insert(fill_idx, noFill)
    else:
        for i, child in enumerate(list(spPr)):
            if child.tag.endswith('ln'):
                spPr.insert(i, noFill)
                break
        else:
            spPr.append(noFill)

    # Outline settings
    rect.line.color.rgb = RGBColor(line_color[0], line_color[1], line_color[2])
    rect.line.width = Pt(4)

    # Text Block Configuration
    tf = rect.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.text = title_text.upper()
    p.alignment = PP_ALIGN.CENTER

    font = p.font
    font.name = 'Arial'
    font.size = Pt(64)
    font.bold = True
    font.color.rgb = RGBColor(255, 255, 255)

    # Typography Enhancements: Letter Spacing and Drop Shadow via XML
    rPr = font._element
    rPr.set('spc', '1500')  # 15pt wide cinematic letter spacing

    effectLst = OxmlElement('a:effectLst')
    outerShdw = OxmlElement('a:outerShdw')
    outerShdw.set('blurRad', '30000')  # 3pt blur
    outerShdw.set('dist', '30000')     # 3pt distance
    outerShdw.set('dir', '2700000')    # 45-degree angle
    srgbClr = OxmlElement('a:srgbClr')
    srgbClr.set('val', '000000')
    alpha = OxmlElement('a:alpha')
    alpha.set('val', '60000')          # 60% shadow opacity
    srgbClr.append(alpha)
    outerShdw.append(srgbClr)
    effectLst.append(outerShdw)
    rPr.append(effectLst)

    prs.save(output_pptx_path)
    return output_pptx_path
```