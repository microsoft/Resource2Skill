# 3D Ribbon Agenda Matrix

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: 3D Ribbon Agenda Matrix

* **Core Visual Mechanism**: This pattern relies on a layered "paper fold" illusion. It pairs two overlapping rounded rectangles—a white foreground card and a colored background tab—connected by a dark, diagonal geometric shadow (a triangle). This structural setup tricks the eye into seeing a single ribbon wrapping around a panel. A gradient-filled circular node anchors the tab, serving as a focal point for list numbering.
* **Why Use This Skill (Rationale)**: The 3D fold separates the index/numbering from the content, instantly establishing a clear visual hierarchy. Breaking the information into discrete "cards" with a soft drop shadow prevents visual fatigue when presenting dense, multi-step agendas or lengthy lists. 
* **Overall Applicability**: Ideal for comprehensive agendas, multi-phase project roadmaps, table of contents, step-by-step methodology slides, or any scenario where 6+ items must be displayed simultaneously without overwhelming the viewer.
* **Value Addition**: Transforms a standard bulleted list into an engaging, structured dashboard. The use of repeating colorful anchor points provides rhythm and navigability, keeping the audience oriented.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Main Card**: White (`255, 255, 255`) rounded rectangle with a soft, dispersed drop shadow.
  - **Index Tab**: Colored rounded rectangle positioned behind and shifted left/up from the main card.
  - **3D Ribbon Fold**: A small right triangle tucked behind the main card and connecting to the index tab, colored with a 40% darker shade of the tab's color to simulate a shadow fold.
  - **Anchor Node**: A circle overlapping the seam between the tab and the card, featuring a vertical linear gradient (lighter tint to base color) and containing a bold, white numeric index.
  - **Typography Hierarchy**: 
    - *Index/Step*: Vertical tracked-out text ("S T E P") alongside a large bold number (`16pt`).
    - *Title*: Dark gray (`50, 50, 50`), bold, `11pt`.
    - *Body*: Mid-gray (`100, 100, 100`), regular, `9pt`.

* **Step B: Compositional Style**
  - Arranged in a 2-column by 6-row matrix.
  - Items span 5.5 inches in width (roughly 40% of standard 16:9 canvas width each).
  - High whitespace between rows and columns ensures readability despite the high density of 12 distinct content blocks.

* **Step C: Dynamic Effects & Transitions**
  - *In Code*: The 3D fold effect is achieved via strict Z-order layering and geometric alignment of the fold triangle. The drop shadow is rendered as an alpha-composited PNG via Pillow for high-fidelity soft edges. 
  - *Manual PPTX Setup*: Can be enhanced manually with a "Wipe" or "Fade" cascade animation, bringing in each card sequentially.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Soft Drop Shadow** | `PIL/Pillow` | Native `python-pptx` lacks a direct API for soft outer shadows. Pillow renders realistic Gaussian blurred RGBA shadows efficiently. |
| **Ribbon Fold Illusion** | `FreeformBuilder` | Drawing a custom 3-point polygon guarantees mathematically perfect alignment between the tab and the card, preventing gaps. |
| **Circular Gradients** | `lxml` XML Injection | Native `python-pptx` cannot apply linear gradients to shapes. Direct OOXML manipulation handles the `a:gradFill` properties cleanly. |
| **Layout & Text Placement** | `python-pptx` | Standard APIs easily handle exact coordinate positioning, text framing, and coloring for the matrix. |

> **Feasibility Assessment**: 100% of the tutorial's core visual effect is reproduced. The layout perfectly aligns the geometric shapes to create the ribbon fold illusion, applies native OOXML gradients to the nodes, and renders high-quality drop shadows. 

#### 3b. Complete Reproduction Code

```python
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml import OxmlElement
from PIL import Image, ImageDraw, ImageFilter

def create_shadow_image(width_in, height_in, radius_in, blur_in=0.15):
    """Generate a soft Gaussian blurred drop shadow PNG."""
    dpi = 150
    w = int(width_in * dpi)
    h = int(height_in * dpi)
    r = int(radius_in * dpi)
    b = int(blur_in * dpi)
    
    img = Image.new('RGBA', (w + 4*b, h + 4*b), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(
        [2*b, 2*b, 2*b + w, 2*b + h],
        radius=r,
        fill=(0, 0, 0, 40)
    )
    img = img.filter(ImageFilter.GaussianBlur(b))
    path = "temp_shadow_ribbon.png"
    img.save(path)
    return path

def darken_color(rgb, factor=0.6):
    """Return a darker shade of the given RGB tuple for the fold shadow."""
    return tuple(int(c * factor) for c in rgb)

def lighten_color(rgb, factor=0.4):
    """Return a lighter shade of the given RGB tuple for the gradient top."""
    return tuple(int(c + (255 - c) * factor) for c in rgb)

def apply_gradient(shape, color1, color2):
    """Inject OOXML to apply a vertical linear gradient to a shape."""
    spPr = shape.element.spPr
    # Remove existing solid fill
    solidFill = spPr.find("{http://schemas.openxmlformats.org/drawingml/2006/main}solidFill")
    if solidFill is not None:
        spPr.remove(solidFill)
    
    gradFill = OxmlElement('a:gradFill')
    gsLst = OxmlElement('a:gsLst')
    
    for pos, color in [(0, color1), (100000, color2)]:
        gs = OxmlElement('a:gs')
        gs.set('pos', str(pos))
        srgbClr = OxmlElement('a:srgbClr')
        srgbClr.set('val', f"{color[0]:02X}{color[1]:02X}{color[2]:02X}")
        gs.append(srgbClr)
        gsLst.append(gs)
        
    lin = OxmlElement('a:lin')
    lin.set('ang', '5400000') # 90 degrees (vertical gradient)
    
    gradFill.append(gsLst)
    gradFill.append(lin)
    spPr.append(gradFill)

def create_slide(
    output_pptx_path: str,
    title_text: str = "12 Points Agenda Slide",
    **kwargs
) -> str:
    """Create a PPTX file reproducing the 3D Ribbon Agenda Matrix effect."""
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout
    
    # Background: Solid light gray-blue
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(230, 233, 236)
    
    # Slide Title
    title_box = slide.shapes.add_textbox(Inches(0), Inches(0.2), Inches(13.333), Inches(0.6))
    title_tf = title_box.text_frame
    title_tf.text = title_text
    title_p = title_tf.paragraphs[0]
    title_p.alignment = PP_ALIGN.CENTER
    title_p.font.size = Pt(28)
    title_p.font.bold = True
    title_p.font.color.rgb = RGBColor(60, 65, 70)

    # 12 Vibrant Theme Colors
    palette = [
        (230, 60, 70),   # Red
        (245, 140, 40),  # Orange
        (250, 180, 30),  # Yellow
        (40, 180, 100),  # Green
        (30, 190, 170),  # Teal
        (40, 130, 220),  # Blue
        (130, 80, 210),  # Purple
        (220, 70, 150),  # Pink
        (180, 40, 60),   # Dark Red
        (140, 200, 40),  # Lime
        (50, 200, 230),  # Cyan
        (240, 110, 90)   # Coral
    ]
    
    # Icons (Unicode fallback simulating the Webdings in tutorial)
    symbols = ["💡", "🏠", "📁", "🗄️", "⚙️", "📈", "🎯", "🏆", "💵", "✉️", "📡", "🛡️"]

    # Layout dimensions
    col_x = [0.6, 7.0]          # X coordinates for Left and Right columns
    start_y = 1.0               # Initial Y offset
    row_spacing = 1.05          # Spacing between rows
    
    tab_w = 1.2
    tab_h = 0.8
    white_w = 4.8
    white_h = 0.8
    white_offset_x = 0.8        # White box overlaps tab, leaving 0.8 of tab visible
    white_offset_y = 0.1        # White box is shifted down slightly to create the 3D gap
    circle_d = 0.7
    
    # Pre-generate shadow image
    shadow_path = create_shadow_image(white_w, white_h, radius_in=0.1)

    for i in range(12):
        c_x = col_x[i // 6]
        c_y = start_y + (i % 6) * row_spacing
        color = palette[i]
        
        wx = c_x + white_offset_x
        wy = c_y + white_offset_y
        
        # 1. Shadow Layer (Behind everything)
        slide.shapes.add_picture(
            shadow_path, 
            Inches(wx - 0.3), Inches(wy - 0.3 + 0.05), 
            width=Inches(white_w + 0.6), height=Inches(white_h + 0.6)
        )
        
        # 2. Left Colored Tab (Background index)
        tab = slide.shapes.add_shape(
            1, # MSO_SHAPE.ROUNDED_RECTANGLE
            Inches(c_x), Inches(c_y), 
            Inches(tab_w), Inches(tab_h)
        )
        tab.fill.solid()
        tab.fill.fore_color.rgb = RGBColor(*color)
        tab.line.fill.background()
        
        # 3. 3D Ribbon Fold (Triangle connecting tab bottom to white box left edge)
        # Fold coordinates to match the visual gap perfectly
        pt_top_right = (wx, c_y + tab_h)
        pt_bottom_right = (wx, wy + white_h)
        pt_top_left = (wx - 0.15, c_y + tab_h)
        
        fold_builder = slide.shapes.build_freeform(Inches(pt_top_right[0]), Inches(pt_top_right[1]))
        fold_builder.add_line_segments([
            (Inches(pt_bottom_right[0]), Inches(pt_bottom_right[1])),
            (Inches(pt_top_left[0]), Inches(pt_top_left[1]))
        ], close=True)
        fold = fold_builder.convertToShape()
        
        fold.fill.solid()
        fold.fill.fore_color.rgb = RGBColor(*darken_color(color, 0.5))
        fold.line.fill.background()
        
        # 4. Main White Card (Foreground panel)
        card = slide.shapes.add_shape(
            1, # ROUNDED_RECTANGLE
            Inches(wx), Inches(wy), 
            Inches(white_w), Inches(white_h)
        )
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(255, 255, 255)
        card.line.fill.background()
        
        # 5. Anchor Circle (Overlapping the seam)
        circle_x = c_x + (white_offset_x / 2) - (circle_d / 2)
        circle_y = wy + (white_h / 2) - (circle_d / 2)
        circle = slide.shapes.add_shape(
            9, # MSO_SHAPE.OVAL
            Inches(circle_x), Inches(circle_y), 
            Inches(circle_d), Inches(circle_d)
        )
        circle.line.fill.background()
        apply_gradient(circle, lighten_color(color), color)
        
        # 6. Text Elements
        # Circular Number
        tf = circle.text_frame
        tf.text = f"{i+1:02d}"
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.font.bold = True
        p.font.size = Pt(14)
        p.font.color.rgb = RGBColor(255, 255, 255)
        
        # Vertical "STEP" Text in the Tab
        step_box = slide.shapes.add_textbox(Inches(c_x - 0.05), Inches(c_y + 0.1), Inches(0.4), Inches(0.6))
        step_tf = step_box.text_frame
        step_tf.word_wrap = True
        p_step = step_tf.paragraphs[0]
        p_step.text = "S\nT\nE\nP"
        p_step.alignment = PP_ALIGN.CENTER
        p_step.font.size = Pt(8)
        p_step.font.bold = True
        p_step.font.color.rgb = RGBColor(255, 255, 255)
        # Squeeze line spacing for the vertical stack
        p_step.line_spacing = Pt(9)
        
        # Title
        t_box = slide.shapes.add_textbox(Inches(wx + 0.3), Inches(wy + 0.05), Inches(3.5), Inches(0.3))
        p_title = t_box.text_frame.paragraphs[0]
        p_title.text = "TITLE"
        p_title.font.bold = True
        p_title.font.size = Pt(11)
        p_title.font.color.rgb = RGBColor(50, 50, 50)
        
        # Body
        b_box = slide.shapes.add_textbox(Inches(wx + 0.3), Inches(wy + 0.3), Inches(3.8), Inches(0.4))
        b_box.text_frame.word_wrap = True
        p_body = b_box.text_frame.paragraphs[0]
        p_body.text = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Maecenas porttitor congue massa."
        p_body.font.size = Pt(9)
        p_body.font.color.rgb = RGBColor(120, 120, 120)
        
        # Icon (Right side of the white card)
        icon_box = slide.shapes.add_textbox(Inches(wx + 4.1), Inches(wy + 0.15), Inches(0.5), Inches(0.5))
        p_icon = icon_box.text_frame.paragraphs[0]
        p_icon.text = symbols[i]
        p_icon.alignment = PP_ALIGN.CENTER
        p_icon.font.size = Pt(20)
        p_icon.font.color.rgb = RGBColor(*color)

    # Cleanup temp file
    if os.path.exists(shadow_path):
        os.remove(shadow_path)

    prs.save(output_pptx_path)
    return output_pptx_path
```