# Origami Corner Infographic Tiles

## Analysis

Here is the extracted design skill, visual breakdown, and executable reproduction code.

### 1. High-level Design Pattern Extraction

> **Skill Name**: Origami Corner Infographic Tiles

* **Core Visual Mechanism**: The defining visual signature is the "folded paper" or "dog-ear" corner effect applied to a perfect square. This creates a skeuomorphic 3D illusion of a physical card whose corner has been folded forward. It relies on a 5-sided base polygon, a 3-sided fold triangle, and soft drop shadows to separate the layers.
* **Why Use This Skill (Rationale)**: Flat squares can look static and uninspired. Adding a folded corner provides tactile dimensionality and introduces a natural visual anchor point (the top-left corner), which is perfect for placing sequential numbers. It guides the reader's eye predictably through a step-by-step process.
* **Overall Applicability**: Ideal for process slides, feature highlights, core values, step-by-step instructions, or pricing tiers.
* **Value Addition**: Transforms standard bullet points or flat text boxes into premium, custom-designed graphic elements that imply attention to detail and professional polish.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  * **Shapes**: A modified square (with one corner cut off), a folding triangle, and an inner white rectangle.
  * **Color Logic**: Vibrant, saturated base colors contrasting with a clean white inner content area.
    * Green: `(112, 173, 71)`
    * Blue: `(68, 114, 196)`
    * Orange: `(237, 125, 49)`
    * Purple: `(112, 48, 160)`
    * Background: Very light grey/white radial gradient or solid light grey `(240, 240, 240)`.
  * **Text Hierarchy**:
    * **Step Number**: Large, bold, placed near the folded corner.
    * **Title**: Bold, uppercase, placed inside the white card.
    * **Body**: Smaller, regular weight, left-justified.

* **Step B: Compositional Style**
  * Layout: A symmetrical grid (2x2 or 2x3).
  * Spacing: Equal gutters between the squares, with the squares occupying roughly 70-80% of the total slide canvas to leave comfortable negative space.

* **Step C: Dynamic Effects & Transitions**
  * The video notes a "Fly In" animation from different corners. (Achievable natively in PowerPoint UI, though the static reproduction code will focus on the final layout state).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Cut Corner & Folded Triangle** | `python-pptx` FreeformBuilder | The video uses boolean operations (Intersect/Subtract) to create the shapes. `python-pptx` cannot do boolean shape operations, so we must calculate the vertices mathematically and draw the custom 5-sided and 3-sided polygons directly. |
| **Layering & Borders** | `python-pptx` native | Stacking the base shape, a white standard rectangle, and the fold triangle naturally mimics the tutorial's layering. |
| **Depth / Drop Shadows** | `lxml` XML injection | `python-pptx` lacks a native API for drop shadows. We must inject OpenXML (`<a:outerShdw>`) directly into the shapes to recreate the realistic depth between the paper and the fold. |

> **Feasibility Assessment**: 100%. By combining custom Freeform polygon math with OpenXML shadow injection, we can perfectly recreate the visual state of the origami tiles without needing external images or manual PPT tweaks.

#### 3b. Complete Reproduction Code

```python
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from lxml import etree

def apply_drop_shadow(shape, blur_pt=10, distance_pt=3, angle_deg=45, alpha_pct=40):
    """
    Injects an OpenXML outer shadow effect into a python-pptx shape.
    """
    spPr = shape.element.spPr
    effectLst = spPr.find("{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst")
    if effectLst is None:
        effectLst = etree.SubElement(spPr, "{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst")
    
    outerShdw = etree.SubElement(effectLst, "{http://schemas.openxmlformats.org/drawingml/2006/main}outerShdw")
    outerShdw.set("blurRad", str(int(blur_pt * 12700)))
    outerShdw.set("dist", str(int(distance_pt * 12700)))
    outerShdw.set("dir", str(int(angle_deg * 60000)))
    outerShdw.set("algn", "tl")
    outerShdw.set("rotWithShape", "0")
    
    srgbClr = etree.SubElement(outerShdw, "{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr")
    srgbClr.set("val", "000000") # Black shadow
    alpha = etree.SubElement(srgbClr, "{http://schemas.openxmlformats.org/drawingml/2006/main}alpha")
    alpha.set("val", str(int(alpha_pct * 1000)))

def draw_origami_tile(slide, x, y, size, fold_size, color_rgb, number_text, title_text, body_text):
    """
    Draws a single origami folded square tile at the given coordinates.
    """
    # 1. Calculate Vertices for the base shape (Square with top-left corner cut off)
    # Start top-center-ish, go clockwise
    base_vertices = [
        (x + fold_size, y),          # Top edge, start after fold
        (x + size, y),               # Top right
        (x + size, y + size),        # Bottom right
        (x, y + size),               # Bottom left
        (x, y + fold_size)           # Left edge, start after fold
    ]
    
    # Draw Base Shape
    freeform_builder = slide.shapes.build_freeform(base_vertices[0][0], base_vertices[0][1])
    for v in base_vertices[1:]:
        freeform_builder.add_line_segments([v], close=False)
    base_shape = freeform_builder.convert_to_shape()
    base_shape.fill.solid()
    base_shape.fill.fore_color.rgb = RGBColor(*color_rgb)
    base_shape.line.fill.background() # No outline
    apply_drop_shadow(base_shape, blur_pt=12, distance_pt=4, angle_deg=90, alpha_pct=25)

    # 2. Draw Inner White Rectangle
    # Leaves a colored border showing on all sides
    border = Inches(0.15)
    inner_x = x + border
    inner_y = y + fold_size + border # Push down to avoid fold area
    inner_w = size - (border * 2)
    inner_h = size - fold_size - (border * 2)
    
    inner_rect = slide.shapes.add_shape(
        1, # msoShapeRectangle
        inner_x, inner_y, inner_w, inner_h
    )
    inner_rect.fill.solid()
    inner_rect.fill.fore_color.rgb = RGBColor(255, 255, 255)
    inner_rect.line.fill.background()
    apply_drop_shadow(inner_rect, blur_pt=8, distance_pt=2, angle_deg=45, alpha_pct=15)

    # 3. Calculate Vertices for the Fold Triangle
    # The corner that folds down
    fold_vertices = [
        (x, y + fold_size),          # Bottom left point of fold
        (x + fold_size, y),          # Top right point of fold
        (x + fold_size, y + fold_size) # Inner point of fold (pointing down/right)
    ]
    
    # Draw Fold Shape
    fold_builder = slide.shapes.build_freeform(fold_vertices[0][0], fold_vertices[0][1])
    for v in fold_vertices[1:]:
        fold_builder.add_line_segments([v], close=False)
    fold_shape = fold_builder.convert_to_shape()
    fold_shape.fill.solid()
    # Make fold slightly darker than base color for 3D effect
    dark_factor = 0.85
    fold_color = RGBColor(int(color_rgb[0]*dark_factor), int(color_rgb[1]*dark_factor), int(color_rgb[2]*dark_factor))
    fold_shape.fill.fore_color.rgb = fold_color
    fold_shape.line.fill.background()
    apply_drop_shadow(fold_shape, blur_pt=6, distance_pt=3, angle_deg=45, alpha_pct=35)

    # 4. Add Step Number
    num_box = slide.shapes.add_textbox(x + fold_size + Inches(0.1), y - Inches(0.1), Inches(1), Inches(0.5))
    num_frame = num_box.text_frame
    num_frame.text = number_text
    num_p = num_frame.paragraphs[0]
    num_p.font.name = "Arial"
    num_p.font.size = Pt(28)
    num_p.font.bold = True
    num_p.font.color.rgb = RGBColor(255, 255, 255)

    # 5. Add Title
    title_box = slide.shapes.add_textbox(inner_x + Inches(0.1), inner_y + Inches(0.1), inner_w - Inches(0.2), Inches(0.4))
    title_frame = title_box.text_frame
    title_frame.text = title_text
    t_p = title_frame.paragraphs[0]
    t_p.font.name = "Arial"
    t_p.font.size = Pt(16)
    t_p.font.bold = True
    t_p.font.color.rgb = RGBColor(50, 50, 50)
    t_p.alignment = PP_ALIGN.CENTER

    # 6. Add Body Text
    body_box = slide.shapes.add_textbox(inner_x + Inches(0.1), inner_y + Inches(0.6), inner_w - Inches(0.2), inner_h - Inches(0.7))
    body_frame = body_box.text_frame
    body_frame.word_wrap = True
    body_frame.text = body_text
    b_p = body_frame.paragraphs[0]
    b_p.font.name = "Arial"
    b_p.font.size = Pt(11)
    b_p.font.color.rgb = RGBColor(100, 100, 100)
    b_p.alignment = PP_ALIGN.LEFT


def create_slide(
    output_pptx_path: str,
    title_text: str = "4 Step Origami Process",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Origami Corner Infographic Tiles effect.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # === Layer 1: Background ===
    # Set a light gray background
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(240, 242, 245)

    # === Layer 2: Visual Effect (The Tiles) ===
    # Tile definitions
    tile_size = Inches(3.2)
    fold_size = Inches(0.9)
    
    # Colors mimicking the tutorial
    colors = [
        (112, 173, 71),   # Green
        (68, 114, 196),   # Blue
        (237, 125, 49),   # Orange
        (112, 48, 160)    # Purple
    ]
    
    dummy_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas porttitor congue massa. Fusce posuere, magna sed pulvinar ultricies."

    # Grid logic (2x2 layout centered)
    start_x = (prs.slide_width - (tile_size * 2) - Inches(0.5)) / 2
    start_y = (prs.slide_height - (tile_size * 2) - Inches(0.5)) / 2

    positions = [
        (start_x, start_y),
        (start_x + tile_size + Inches(0.5), start_y),
        (start_x, start_y + tile_size + Inches(0.5)),
        (start_x + tile_size + Inches(0.5), start_y + tile_size + Inches(0.5))
    ]

    for i in range(4):
        draw_origami_tile(
            slide=slide,
            x=positions[i][0],
            y=positions[i][1],
            size=tile_size,
            fold_size=fold_size,
            color_rgb=colors[i],
            number_text=f"0{i+1}",
            title_text="STEP TITLE",
            body_text=dummy_text
        )

    # Optional Title at the very top
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), prs.slide_width - Inches(1), Inches(0.6))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.name = "Arial"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = RGBColor(80, 80, 80)
    p.alignment = PP_ALIGN.CENTER

    prs.save(output_pptx_path)
    return output_pptx_path

# Example execution:
# create_slide("origami_tiles.pptx")
```