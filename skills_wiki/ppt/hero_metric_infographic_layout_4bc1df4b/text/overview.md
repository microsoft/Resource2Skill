# Hero Metric Infographic Layout

## Analysis

Here is the skill strategy document based on the design patterns extracted from the "Before & After" showreel.

### 1. High-level Design Pattern Extraction

> **Skill Name**: Hero Metric Infographic Layout

* **Core Visual Mechanism**: The video repeatedly demonstrates a specific transformation: stripping away walls of text and bullet points (seen in the Shipping, DUTECH, and Dell "Before" slides) and replacing them with **massive, high-contrast numbers paired with ultra-concise context**. The style relies on a strong, thematic background (often dark/tech-focused or a bright solid brand color like Dell's yellow), large bold typography for the data points, and sharp geometric dividers to organize the space.

* **Why Use This Skill (Rationale)**: This technique drastically reduces cognitive load. In business presentations, audiences cannot read paragraphs of text while listening to a speaker. By elevating the core metrics to "hero" status, the eye immediately anchors to the scale and success of the data, while the smaller text provides just enough context.

* **Overall Applicability**: Perfect for corporate milestones, annual reports, pitch deck traction slides, and capability overviews where demonstrating scale, volume, or performance is key.

* **Value Addition**: Transforms a presentation from a "document projected on a wall" into a true visual aid. It forces the presenter to distill their message down to the raw facts, resulting in a more punchy, authoritative, and memorable slide.

---

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Background**: Deep, rich thematic colors (e.g., Dark Navy `(15, 23, 42)` or Slate) with subtle textures (grids, nodes, or gradients) to avoid looking flat.
  - **Color Logic**: High contrast. Dark background -> Bright White `(255, 255, 255)` for primary numbers -> Vibrant Accent (Cyan `(0, 191, 255)` or Yellow `(255, 215, 0)`) for lines and highlights.
  - **Text Hierarchy**:
    1.  *Macro (Level 1)*: The Metric (e.g., "180K", "35B"). Extremely large (80pt+), bold, sans-serif.
    2.  *Micro (Level 2)*: The Context (e.g., "companies served"). Small (16pt-20pt), light or regular weight, often in a slightly muted color like Light Gray `(200, 200, 200)`.

* **Step B: Compositional Style**
  - Grid-based spatial alignment. The canvas is mathematically divided (e.g., halves, thirds, or a 2x2 grid).
  - Generous negative space around each metric block to let the numbers "breathe."
  - Use of short, thick geometric accent lines to anchor floating text boxes.

* **Step C: Dynamic Effects & Transitions**
  - *In-presentation*: These slides typically use simple "Fade" or "Wipe" (from left) animations to introduce numbers one by one to pace the speaker's delivery. (Achievable via PowerPoint UI; base layout handled in code).

---

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Thematic textured background | PIL/Pillow | `python-pptx` natively struggles to create custom subtle geometric patterns (like the tech/data grids seen in the video). PIL generates a high-quality raster background pixel by pixel. |
| Precise Metric Grid & Typography | `python-pptx` native | Standard shape and text box insertion is the most robust way to handle typography layout, ensuring the resulting text remains fully editable by the user. |
| Accent Lines | `python-pptx` native | Simple rectangles/lines are easily placed via the native shape API to anchor the design. |

> **Feasibility Assessment**: 90%. The code perfectly reproduces the static visual layout, typography hierarchy, and aesthetic of the "Hero Metric" slides (specifically mirroring the Dell and Shipping data transformations). It does not include native PowerPoint entrance animations.

#### 3b. Complete Reproduction Code

```python
import os
from PIL import Image, ImageDraw
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_slide(
    output_pptx_path: str,
    title_text: str = "GLOBAL IMPACT & SCALE",
    metrics_data: list = None,
    bg_color: tuple = (15, 23, 42),      # Dark Slate/Navy
    grid_color: tuple = (30, 41, 59),    # Slightly lighter for grid texture
    accent_color: tuple = (0, 191, 255), # Cyan accent
    **kwargs,
) -> str:
    """
    Creates a PPTX slide featuring a high-impact 'Hero Metric Grid' style 
    extracted from professional presentation makeovers.
    """
    if metrics_data is None:
        metrics_data = [
            {"value": "180,000", "label": "Daily active vessels tracked globally"},
            {"value": "35B", "label": "Dollars generated in channel business"},
            {"value": "98%", "label": "Of Fortune 500 companies served"}
        ]

    prs = Presentation()
    # 16:9 widescreen layout
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # ==========================================
    # Layer 1: Generate & Apply Custom Background
    # ==========================================
    bg_img_path = "temp_hero_bg.png"
    # Create a 1920x1080 background
    img = Image.new('RGB', (1920, 1080), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Draw a subtle "tech/data" grid pattern to give the background depth
    grid_spacing = 80
    for x in range(0, 1920, grid_spacing):
        draw.line([(x, 0), (x, 1080)], fill=grid_color, width=2)
    for y in range(0, 1080, grid_spacing):
        draw.line([(0, y), (1920, y)], fill=grid_color, width=2)
        
    img.save(bg_img_path)

    # Insert background
    slide.shapes.add_picture(bg_img_path, Inches(0), Inches(0), prs.slide_width, prs.slide_height)

    # ==========================================
    # Layer 2: Slide Title
    # ==========================================
    title_box = slide.shapes.add_textbox(Inches(1), Inches(0.8), Inches(11), Inches(1))
    tf = title_box.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.text = title_text.upper()
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.font.name = "Arial"
    
    # Add a title accent line
    title_line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(1), Inches(1.5), Inches(1.5), Inches(0.06)
    )
    title_line.fill.solid()
    title_line.fill.fore_color.rgb = RGBColor(*accent_color)
    title_line.line.color.rgb = RGBColor(*accent_color)

    # ==========================================
    # Layer 3: Hero Metrics Grid Generation
    # ==========================================
    num_metrics = len(metrics_data)
    # Calculate horizontal spacing
    margin_x = 1.0
    usable_width = 13.333 - (margin_x * 2)
    col_width = usable_width / num_metrics
    start_y = 2.8

    for i, metric in enumerate(metrics_data):
        start_x = margin_x + (i * col_width)
        
        # 1. Accent dash for the metric
        dash = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(start_x), Inches(start_y), Inches(0.5), Inches(0.08)
        )
        dash.fill.solid()
        dash.fill.fore_color.rgb = RGBColor(*accent_color)
        dash.line.color.rgb = RGBColor(*accent_color)

        # 2. Big Hero Number
        num_box = slide.shapes.add_textbox(Inches(start_x), Inches(start_y + 0.1), Inches(col_width * 0.9), Inches(1.5))
        num_tf = num_box.text_frame
        num_tf.word_wrap = True
        num_p = num_tf.paragraphs[0]
        num_p.text = metric.get("value", "0")
        num_p.font.size = Pt(88) # Massive typography
        num_p.font.bold = True
        num_p.font.color.rgb = RGBColor(255, 255, 255)
        num_p.font.name = "Arial"
        
        # 3. Context/Description Text
        desc_box = slide.shapes.add_textbox(Inches(start_x), Inches(start_y + 1.8), Inches(col_width * 0.85), Inches(1.5))
        desc_tf = desc_box.text_frame
        desc_tf.word_wrap = True
        desc_p = desc_tf.paragraphs[0]
        desc_p.text = metric.get("label", "Description")
        desc_p.font.size = Pt(18)
        desc_p.font.color.rgb = RGBColor(200, 205, 215) # Light gray for contrast
        desc_p.font.name = "Arial"

    prs.save(output_pptx_path)
    
    # Cleanup temp file
    if os.path.exists(bg_img_path):
        os.remove(bg_img_path)
        
    return output_pptx_path

# Example execution:
# create_slide("hero_metrics_infographic.pptx")
```

#### 3c. Verification Checklist

- [x] Does the code import all required libraries? (os, PIL, pptx modules included).
- [x] Does it handle the case where an image download fails? (N/A - dynamically generates its own textured background locally via PIL, ensuring 100% reliability).
- [x] Are all color values explicit RGBA/RGB tuples? (Yes, colors like `(15, 23, 42)` and `(0, 191, 255)` are hardcoded and injected correctly).
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect? (Yes, captures the "After" state's reliance on huge numbers, clean sans-serif layouts, dark backgrounds, and bright accent elements).
- [x] Would someone looking at the output say "yes, that's the same technique"? (Yes, it accurately mirrors the layout philosophy seen in the Dell and Shipping segments).