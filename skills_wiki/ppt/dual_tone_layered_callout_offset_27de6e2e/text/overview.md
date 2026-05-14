# Dual-Tone Layered Callout Offset

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Dual-Tone Layered Callout Offset

* **Core Visual Mechanism**: This pattern utilizes two identical geometric shapes (specifically, rectangular speech bubbles/callouts). They are stacked directly on top of each other with a slight diagonal offset. The bottom layer uses a darker, heavier tone combined with a soft drop shadow to ground the element, while the top layer uses a lighter, softer tint of the same hue to hold the primary text. 
* **Why Use This Skill (Rationale)**: By overlapping solid shapes with contrasting brightness and an offset, it simulates a 3D "stack" or "sticker" effect without relying on complex gradients or 3D rotations. It draws immediate focal attention to the text, making it pop off a plain background with a satisfying, tactile feel (similar to "Neo-Brutalism" but softened by the drop shadow).
* **Overall Applicability**: Ideal for highlight quotes, key takeaways, alert messages, tooltips, or critical tips on clean, minimalist slides. 
* **Value Addition**: Transforms a standard, flat text box into a prominent, engaging visual card. It breaks the grid and adds depth while maintaining extremely clean vectors.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Shape Type**: Rectangular wedge callouts (speech bubbles).
  - **Color Logic**: Monochromatic scaling. 
    - Base Slide: White `(255, 255, 255, 255)`
    - Back Layer (Shadow): Dark Burgundy/Red `(105, 25, 45, 255)`
    - Front Layer (Content): Soft Rose/Pink `(215, 150, 160, 255)`
    - Content Text: Dark grey/black for high contrast `(50, 20, 25, 255)`
  - **Text Hierarchy**: Centered bold title at the top of the slide, medium paragraph text inside the callout, and a smaller, secondary descriptive text below the graphic.

* **Step B: Compositional Style**
  - **Proportions**: The callout shape occupies approximately 50% of the slide's total width and 40% of its height, placed dead center.
  - **Offset**: The bottom layer is offset roughly 0.25 inches to the bottom right relative to the top layer.
  - **Borders**: No visible outlines; borders perfectly match the fill color to keep edges clean.

* **Step C: Dynamic Effects & Transitions**
  - The static 3D depth is achieved exclusively through layer positioning, high/low contrast overlapping, and XML-injected drop shadows. (No motion animation is strictly required to sell this effect).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Editable Callout Shapes | `python-pptx` native | Using `MSO_SHAPE.WEDGE_RECT_CALLOUT` allows the text to remain fully editable natively in PowerPoint. |
| Drop Shadow | `lxml` XML injection | `python-pptx` lacks a native API for drop shadows. We inject `<a:effectLst>` directly into the shape properties to create the authentic PowerPoint shadow. |
| Border Removal | `python-pptx` native | Native shape line color assignment matching the fill color seamlessly eliminates default borders. |

> **Feasibility Assessment**: 100%. The code precisely replicates the visual offset, color tinting, shape geometry, and editable text fields demonstrated in the tutorial.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "Title Here",
    body_text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit,\nsed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    bg_color: tuple = (255, 255, 255),
    shadow_color: tuple = (105, 25, 45),  # Dark Burgundy
    front_color: tuple = (215, 150, 160), # Soft Rose/Pink
    text_color: tuple = (50, 20, 25),     # Dark font color
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the "Dual-Tone Layered Callout Offset" visual effect.
    
    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN
    from pptx.dml.color import RGBColor
    from pptx.oxml import parse_xml

    # Initialize presentation and blank slide
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide_layout = prs.slide_layouts[6]  # 6 is usually a blank slide layout
    slide = prs.slides.add_slide(slide_layout)

    # Set background color
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*bg_color)

    # === Layer 1: Top Title ===
    title_box = slide.shapes.add_textbox(Inches(2), Inches(0.8), Inches(9.333), Inches(1))
    tf_title = title_box.text_frame
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.alignment = PP_ALIGN.CENTER
    run_title = p_title.runs[0]
    run_title.font.size = Pt(40)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(50, 50, 50)

    # Base coordinates & dimensions for the callout
    w = Inches(6.0)
    h = Inches(3.2)
    base_left = Inches(3.66)
    base_top = Inches(2.2)
    offset = Inches(0.25)

    # === Layer 2: Shadowed Back Callout ===
    # Placed with offset (bottom-right)
    back_shape = slide.shapes.add_shape(
        MSO_SHAPE.WEDGE_RECT_CALLOUT,
        base_left + offset, base_top + offset, w, h
    )
    back_shape.fill.solid()
    back_shape.fill.fore_color.rgb = RGBColor(*shadow_color)
    back_shape.line.fill.solid()
    back_shape.line.color.rgb = RGBColor(*shadow_color) # Hide border

    # Inject exact drop shadow using lxml
    shadow_xml = """
    <a:effectLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
        <a:outerShdw blurRad="50000" dist="40000" dir="2700000" algn="tl" rotWithShape="0">
            <a:srgbClr val="000000">
                <a:alpha val="40000"/>
            </a:srgbClr>
        </a:outerShdw>
    </a:effectLst>
    """
    back_shape.element.spPr.append(parse_xml(shadow_xml))

    # === Layer 3: Front Content Callout ===
    # Placed at true base coordinates
    front_shape = slide.shapes.add_shape(
        MSO_SHAPE.WEDGE_RECT_CALLOUT,
        base_left, base_top, w, h
    )
    front_shape.fill.solid()
    front_shape.fill.fore_color.rgb = RGBColor(*front_color)
    front_shape.line.fill.solid()
    front_shape.line.color.rgb = RGBColor(*front_color) # Hide border

    # Add and format text inside the front callout
    tf_front = front_shape.text_frame
    tf_front.word_wrap = True
    tf_front.margin_left = Inches(0.4)
    tf_front.margin_right = Inches(0.4)
    tf_front.margin_top = Inches(0.6)
    tf_front.margin_bottom = Inches(0.6)

    p_front = tf_front.paragraphs[0]
    p_front.text = body_text
    p_front.alignment = PP_ALIGN.LEFT
    run_front = p_front.runs[0]
    run_front.font.size = Pt(20)
    run_front.font.color.rgb = RGBColor(*text_color)

    # === Layer 4: Lower Supplementary Text ===
    footer_box = slide.shapes.add_textbox(Inches(2.66), Inches(6.0), Inches(8), Inches(1))
    tf_foot = footer_box.text_frame
    tf_foot.word_wrap = True
    p_foot = tf_foot.paragraphs[0]
    p_foot.text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 2
    p_foot.alignment = PP_ALIGN.CENTER
    p_foot.font.size = Pt(14)
    p_foot.font.color.rgb = RGBColor(100, 100, 100)

    # Save presentation
    prs.save(output_pptx_path)
    return output_pptx_path
```