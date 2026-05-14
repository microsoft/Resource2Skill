# Slanted Split-Screen Stat Comparison

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Slanted Split-Screen Stat Comparison

* **Core Visual Mechanism**: A high-contrast, diagonally divided layout designed to compare two opposing metrics (e.g., Dropped vs. Gained). It relies on a sharp, slanted central divider, dark-vs-light contextual backgrounds, large focal typography, and dashed circular progress/container rings.
* **Why Use This Skill (Rationale)**: The diagonal split creates a sense of dynamic tension and forward momentum, which is much more engaging than a standard vertical split. By assigning high contrast (dark vs. light) to opposing stats, the audience immediately intuitively grasps the comparison before even reading the numbers.
* **Overall Applicability**: Perfect for yearly reviews (losses vs. gains), A/B testing results, demographic splits, product comparisons, or highlighting the most critical opposing KPIs in a data dashboard. 
* **Value Addition**: Transforms standard, dry bulleted data points into an infographic-style visual anchor. It elevates simple percentages into a professional, modern story-driven slide.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Background**: Two-toned. The left is a deep, rich navy/teal `(20, 35, 45, 255)`, and the right is a clean, cool light grey/blue `(230, 235, 240, 255)`.
  - **Divider**: A bold, white slanted line bridging the two sides with a subtle drop shadow to create depth.
  - **Containers**: Large circular outlines with a dashed/segmented stroke. They serve to frame the numbers.
  - **Typography**: Huge, bold primary statistics (e.g., "26%", "74%") flanked by smaller, all-caps descriptors. Text colors contrast their respective backgrounds.
  - **Accents**: Cyan `(0, 191, 255, 255)` on the dark side, Bright Green `(46, 204, 113, 255)` on the light side.

* **Step B: Compositional Style**
  - **Layout**: Roughly a 50/50 split, but the slant (angling from top-right to bottom-left) breaks the symmetry.
  - **Alignment**: The text labels hug the central dividing line (Left text aligns right; Right text aligns left), pulling the viewer's eye toward the center of the slide.
  - **Proportions**: The circular data containers are massive, occupying about 40% of their respective halves, making the data the absolute hero of the slide.

* **Step C: Dynamic Effects & Transitions**
  - *In PowerPoint (Manual)*: The background panels wipe/stretch in. The circles "Zoom" in. The numbers "Fade" or "Zoom". The dashed rings feature a continuous "Spin" emphasis animation to make them look like active loading rings.
  - *In Code (Automated)*: We will generate the final visual state. (Automating complex PowerPoint timeline animations via code is limited, so we deliver the production-ready static assets and layout).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Diagonal Background & Shadowed Divider** | `PIL/Pillow` | Native python-pptx struggles with complex custom polygons, drop shadows on lines, and overlapping transparent geometric shapes. PIL generates a perfect, anti-aliased backdrop. |
| **Completely Transparent Rings** | `lxml` XML Injection | Standard `shape.fill.background()` reveals the *slide* background, not the PIL picture we inserted. We must inject `<a:noFill>` directly into the OpenXML to make the rings truly hollow. |
| **Editable Typography & Layout** | `python-pptx` Native | Text and data should remain editable by the end-user. Placing native text boxes over the PIL background achieves the best of both worlds. |

> **Feasibility Assessment**: 90%. The code produces an incredibly faithful reproduction of the visual style, layout, and colors. The only element excluded is the continuous "Spin" animation, which must be applied manually in the PowerPoint Animation Pane if desired.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    stat_left: str = "26%",
    label_left: str = "DROPPED THIS\nYEAR",
    stat_right: str = "74%",
    label_right: str = "GAINED THIS\nYEAR",
    color_left_bg: tuple = (20, 35, 45),
    color_right_bg: tuple = (230, 235, 240),
    color_left_accent: tuple = (0, 191, 255),
    color_right_accent: tuple = (46, 204, 113),
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the 'Slanted Split-Screen Stat Comparison' layout.
    """
    import os
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN, MSO_VERTICAL_ANCHOR
    from pptx.enum.dml import MSO_LINE_DASH_STYLE
    from pptx.oxml import OxmlElement
    from PIL import Image, ImageDraw, ImageFilter

    # --- Setup Presentation ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank layout
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    # --- HELPER: XML Injection for True Transparency ---
    def make_shape_transparent(shape):
        """Forces a shape to have absolutely no fill, allowing background pictures to show through."""
        spPr = shape.element.spPr
        # Remove any existing fill tags
        for child in list(spPr):
            if child.tag.endswith('Fill'):
                spPr.remove(child)
        # Inject standard OpenXML noFill tag
        noFill = OxmlElement('a:noFill')
        spPr.insert(0, noFill)

    # --- Layer 1: PIL Background Generation ---
    W, H = 1920, 1080
    bg_img = Image.new('RGBA', (W, H), color_right_bg + (255,))
    draw = ImageDraw.Draw(bg_img, 'RGBA')

    # Calculate diagonal split (leaning right, meaning top-center is further right than bottom-center)
    top_split_x = int(W * 0.55)
    bot_split_x = int(W * 0.45)

    # Left Dark Polygon
    left_poly = [(0, 0), (top_split_x, 0), (bot_split_x, H), (0, H)]
    draw.polygon(left_poly, fill=color_left_bg + (255,))

    # Add geometric flair to left side (subtle lighter overlapping triangles)
    draw.polygon([(0, H * 0.4), (W * 0.3, H), (0, H)], fill=(30, 80, 100, 120))
    draw.polygon([(W * 0.1, 0), (W * 0.5, 0), (W * 0.3, H * 0.5)], fill=(0, 150, 200, 30))

    # Add geometric flair to right side (subtle white geometric frames)
    draw.rectangle([W * 0.7, H * 0.2, W * 0.8, H * 0.4], outline=(255, 255, 255, 180), width=6)
    draw.rectangle([W * 0.85, H * 0.6, W * 0.95, H * 0.8], outline=(200, 210, 220, 180), width=6)

    # Slanted divider with drop shadow
    thickness = 35
    # Draw Shadow
    shadow_poly = [
        (top_split_x - thickness + 15, 0),
        (top_split_x + thickness + 15, 0),
        (bot_split_x + thickness + 15, H),
        (bot_split_x - thickness + 15, H)
    ]
    # Create a separate layer for the shadow to blur it
    shadow_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow_layer)
    shadow_draw.polygon(shadow_poly, fill=(0, 0, 0, 80))
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(15))
    bg_img = Image.alpha_composite(bg_img, shadow_layer)

    # Draw White Divider Line
    div_poly = [
        (top_split_x - thickness, 0),
        (top_split_x + thickness, 0),
        (bot_split_x + thickness, H),
        (bot_split_x - thickness, H)
    ]
    draw = ImageDraw.Draw(bg_img, 'RGBA') # get draw handle again after composite
    draw.polygon(div_poly, fill=(255, 255, 255, 255))
    
    # Save and insert background
    bg_path = "temp_split_bg.png"
    bg_img.save(bg_path)
    slide.shapes.add_picture(bg_path, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # --- Layer 2: PPTX Shapes & Typography ---
    
    # --- LEFT SIDE (Dark) ---
    # 1. Left Ring
    left_ring = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(1.2), Inches(2.25), Inches(3.0), Inches(3.0))
    make_shape_transparent(left_ring)
    left_ring.line.color.rgb = RGBColor(*color_left_accent)
    left_ring.line.width = Pt(8)
    left_ring.line.dash_style = MSO_LINE_DASH_STYLE.DASH

    # 2. Left Number
    left_num = slide.shapes.add_textbox(Inches(1.2), Inches(2.25), Inches(3.0), Inches(3.0))
    left_num.text_frame.clear()
    p1 = left_num.text_frame.paragraphs[0]
    p1.text = stat_left
    p1.alignment = PP_ALIGN.CENTER
    p1.font.size = Pt(66)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(255, 255, 255)
    p1.font.name = "Arial"
    left_num.text_frame.vertical_anchor = MSO_VERTICAL_ANCHOR.MIDDLE

    # 3. Left Label
    left_lbl = slide.shapes.add_textbox(Inches(4.4), Inches(2.9), Inches(1.8), Inches(1.5))
    left_lbl.text_frame.clear()
    p2 = left_lbl.text_frame.paragraphs[0]
    p2.text = label_left
    p2.alignment = PP_ALIGN.RIGHT
    p2.font.size = Pt(20)
    p2.font.color.rgb = RGBColor(200, 210, 220)
    p2.font.name = "Arial"

    # --- RIGHT SIDE (Light) ---
    # 1. Right Ring
    right_ring = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(9.1), Inches(2.25), Inches(3.0), Inches(3.0))
    make_shape_transparent(right_ring)
    right_ring.line.color.rgb = RGBColor(*color_right_accent)
    right_ring.line.width = Pt(8)
    right_ring.line.dash_style = MSO_LINE_DASH_STYLE.DASH

    # 2. Right Number
    right_num = slide.shapes.add_textbox(Inches(9.1), Inches(2.25), Inches(3.0), Inches(3.0))
    right_num.text_frame.clear()
    p3 = right_num.text_frame.paragraphs[0]
    p3.text = stat_right
    p3.alignment = PP_ALIGN.CENTER
    p3.font.size = Pt(66)
    p3.font.bold = True
    p3.font.color.rgb = RGBColor(30, 40, 50)
    p3.font.name = "Arial"
    right_num.text_frame.vertical_anchor = MSO_VERTICAL_ANCHOR.MIDDLE

    # 3. Right Label
    right_lbl = slide.shapes.add_textbox(Inches(7.1), Inches(2.9), Inches(1.8), Inches(1.5))
    right_lbl.text_frame.clear()
    p4 = right_lbl.text_frame.paragraphs[0]
    p4.text = label_right
    p4.alignment = PP_ALIGN.LEFT
    p4.font.size = Pt(20)
    p4.font.color.rgb = RGBColor(100, 110, 120)
    p4.font.name = "Arial"

    # Save presentation
    prs.save(output_pptx_path)
    
    # Cleanup temp file
    if os.path.exists(bg_path):
        os.remove(bg_path)

    return output_pptx_path
```