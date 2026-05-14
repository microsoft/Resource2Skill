# Prismatic Green Geometric Layout

## Analysis

Here is the extracted design skill and reproduction code based on the provided PowerPoint tutorial.

### 1. High-level Design Pattern Extraction

> **Skill Name**: Prismatic Green Geometric Layout

* **Core Visual Mechanism**: The defining visual signature is a **faceted, low-poly (polygonal) geometric background** constructed from overlapping triangles and polygons in analogous shades of a single base color (in this case, energetic greens). This is paired with stark, flat white typography and strict geometric accents (hexagons, circles) to create a clean, structured look.
* **Why Use This Skill (Rationale)**: The faceted background implies complexity, analysis, and multifaceted solutions without creating visual clutter. The "low-poly" aesthetic bridges the gap between organic themes (enhanced by the green palette) and digital/technological precision. It prevents flat color backgrounds from feeling dull while keeping text highly legible.
* **Overall Applicability**: Ideal for corporate profiles, tech/data reporting, strategic planning (as indicated by the Chinese text "工作计划 / 汇报总结"), and environmental/sustainability tech companies.
* **Value Addition**: It elevates a standard corporate presentation into a modern, bespoke branded asset. The faceted background provides depth (a 2.5D feel) without relying on heavy shadows or gradients that can look dated.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**: Analogous green palette.
    - Deep base green: `RGBA(76, 168, 118, 255)`
    - Mid-tones: `RGBA(120, 204, 156, 255)`, `RGBA(94, 187, 137, 255)`
    - Highlights (Mint): `RGBA(154, 222, 178, 255)`
    - Typography: Pure White `RGBA(255, 255, 255, 255)` for prominent titles against dark areas; Dark Slate `RGBA(50, 70, 60, 255)` for readable body text against light areas.
  - **Shape Language**: Sharp angles in the background (polygons), juxtaposed with precise geometric content containers (hexagons, circles).
  - **Text Hierarchy**: Very high contrast. Massive, bold uppercase English titles ("POWERPOINT") anchored by much smaller, elegant localized subtitles.

* **Step B: Compositional Style**
  - **Spatial Feel**: Expansive and airy. The polygonal facets draw the eye across the canvas, typically radiating from a lighter central/top area to darker corners.
  - **Layout Proportions**: Content often uses a 1/3 to 2/3 split. Large empty spaces on one side are balanced by dense, icon-driven lists (e.g., stacked hexagons) on the other.

* **Step C: Dynamic Effects & Transitions**
  - The tutorial relies heavily on static visual impact, though these templates typically use smooth "Fade" or "Morph" transitions to make the geometric shapes feel like an ever-shifting kaleidoscope. (Our code will focus on generating the core static visual asset).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Faceted Polygonal Background** | PIL / Pillow | `python-pptx` cannot reliably draw native seamless background meshes. We use PIL to algorithmically draw a high-res custom low-poly background and insert it as an image layer. |
| **Hexagonal Geometric Nodes** | `python-pptx` native shapes | Native `MSO_SHAPE.HEXAGON` allows text to be natively embedded, edited, and perfectly aligned in the presentation. |
| **Typography & Layout** | `python-pptx` native | Provides standard text boxes, font formatting, and precise spatial distribution. |

> **Feasibility Assessment**: 95%. The code precisely replicates the unique faceted green background and the structured, geometric text layout. The only missing elements are the manual PowerPoint entrance animations, which are beyond static script generation.

#### 3b. Complete Reproduction Code

```python
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from PIL import Image, ImageDraw

def create_slide(
    output_pptx_path: str,
    title_text: str = "POWERPOINT",
    subtitle_text: str = "工作计划 / 汇报总结 / 年中总结 / 述职报告等",
    **kwargs,
) -> str:
    """
    Creates a PowerPoint slide reproducing the 'Prismatic Green Geometric' style.
    Generates a custom low-poly background via PIL and lays out hexagonal content nodes.
    
    Returns: path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # === Layer 1: Generate & Apply Prismatic Background (PIL) ===
    bg_path = "temp_prismatic_bg.png"
    width, height = 1920, 1080
    img = Image.new("RGBA", (width, height), (142, 201, 146, 255))
    draw = ImageDraw.Draw(img)

    # Define polygons to simulate a 3D faceted low-poly surface
    polygons = [
        # (Coordinates list), (R, G, B)
        ([(0,0), (1200,0), (800, 600), (0, 800)], (154, 222, 178)),
        ([(0,800), (800, 600), (550, 1080), (0, 1080)], (94, 187, 137)),
        ([(1200,0), (1920,0), (1920, 500), (1450, 350)], (175, 235, 195)),
        ([(800, 600), (1200, 0), (1450, 350), (1600, 1080), (550, 1080)], (120, 204, 156)),
        ([(1450, 350), (1920, 500), (1920, 1080), (1600, 1080)], (76, 168, 118)),
        ([(400, 400), (800, 600), (550, 1080), (200, 900)], (105, 195, 145)), # Extra overlay facet
    ]

    for coords, color in polygons:
        draw.polygon(coords, fill=color)
    
    img.save(bg_path)
    
    # Insert background
    slide.shapes.add_picture(bg_path, 0, 0, prs.slide_width, prs.slide_height)

    # === Layer 2: Main Title & Subtitle Typography ===
    title_box = slide.shapes.add_textbox(Inches(1.0), Inches(2.5), Inches(6.0), Inches(1.5))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.name = "Arial Black"
    p.font.size = Pt(64)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    
    sub_box = slide.shapes.add_textbox(Inches(1.1), Inches(3.6), Inches(6.0), Inches(0.5))
    tf_sub = sub_box.text_frame
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = subtitle_text
    p_sub.font.name = "Microsoft YaHei"
    p_sub.font.size = Pt(16)
    p_sub.font.color.rgb = RGBColor(255, 255, 255)

    # === Layer 3: Geometric Content Nodes (Hexagons) ===
    # Creates a 3-item list on the right side using hexagonal nodes
    content_items = [
        "Focus on professional PPT template development and corporate visual design.",
        "Provide customized solutions for internal logic and data visualization.",
        "Committed to enhancing the communication value of every slide presentation."
    ]
    
    start_y = Inches(2.0)
    spacing = Inches(1.5)
    
    for i, text in enumerate(content_items):
        y_pos = start_y + (i * spacing)
        
        # Add Hexagon Node
        hex_shape = slide.shapes.add_shape(MSO_SHAPE.HEXAGON, Inches(7.5), y_pos, Inches(1.0), Inches(1.0))
        hex_shape.fill.solid()
        hex_shape.fill.fore_color.rgb = RGBColor(255, 255, 255) # White Hexagon
        hex_shape.line.fill.background() # No line
        
        # Number inside hexagon
        hex_tf = hex_shape.text_frame
        hex_p = hex_tf.paragraphs[0]
        hex_p.text = str(i + 1)
        hex_p.alignment = PP_ALIGN.CENTER
        hex_p.font.name = "Arial"
        hex_p.font.size = Pt(24)
        hex_p.font.bold = True
        hex_p.font.color.rgb = RGBColor(94, 187, 137) # Green text matching background
        
        # Add body text next to hexagon
        body_box = slide.shapes.add_textbox(Inches(8.7), y_pos + Inches(0.1), Inches(3.8), Inches(0.8))
        body_tf = body_box.text_frame
        body_tf.word_wrap = True
        body_p = body_tf.paragraphs[0]
        body_p.text = text
        body_p.font.name = "Microsoft YaHei"
        body_p.font.size = Pt(14)
        body_p.font.color.rgb = RGBColor(255, 255, 255)

    # Save and cleanup
    prs.save(output_pptx_path)
    if os.path.exists(bg_path):
        os.remove(bg_path)
        
    return output_pptx_path
```