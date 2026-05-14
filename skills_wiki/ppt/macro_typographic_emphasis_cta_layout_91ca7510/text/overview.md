# Macro Typographic Emphasis & CTA Layout

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Macro Typographic Emphasis & CTA Layout

* **Core Visual Mechanism**: This style relies on **extreme typographic scale contrast** combined with a stark, minimal color palette. It uses a soft radial gradient background to push focus entirely to the center text. The visual anchor is a single massive, boldly colored keyword surrounded by smaller neutral text, followed by strong, flat geometric Call-To-Action (CTA) shapes (like downward arrows) that drive viewer attention toward a final instruction or link.
* **Why Use This Skill (Rationale)**: The enormous size of the focal word acts as a psychological hook, immediately anchoring the viewer's attention. Eliminating cluttered background visuals and using flat directional shapes (arrows) creates a clear, undeniable flow of information from the key message down to the desired action.
* **Overall Applicability**: Ideal for Title Slides, Section Transitions, and Ending/Conclusion slides where you want to leave a lasting impression or drive audience engagement (e.g., "Follow Us", "Q&A", "Download Here").
* **Value Addition**: It replaces tired, bulleted "Thank You" slides with an authoritative, modern, and high-impact visual that treats a presentation like a premium billboard or landing page.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  * **Color Logic**:
    * **Background**: Soft, subtle radial gradient from White `(248, 249, 250)` at the center to Light Grey `(222, 226, 230)` at the edges.
    * **Primary Accent**: A strong corporate hue, such as Deep Blue `(30, 90, 150)`.
    * **Neutral Text**: Dark Charcoal `(80, 80, 80)` and Medium Grey `(100, 100, 100)`.
  * **Text Hierarchy**:
    * *Pre-text*: Small/Medium, all-caps, bold, medium grey (e.g., "HOW TO").
    * *Hero word*: Massive (130pt+), all-caps, bold, accent color (e.g., "END").
    * *Post-text*: Medium, all-caps, bold, dark grey (e.g., "A PRESENTATION").

* **Step B: Compositional Style**
  * Perfect center-axis alignment.
  * The typographic block dominates the top 60% of the canvas.
  * Two prominent CTA shapes (arrows) flank the bottom layout symmetrically, pointing toward a central URL or contact detail at the bottom edge.

* **Step C: Dynamic Effects & Transitions**
  * Easily enhanced with a simple "Fade" transition or a "Zoom" animation on the hero word. (PowerPoint manual setup).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Soft Radial Background** | `lxml` XML Injection | Injecting `<a:gradFill>` directly into a shape creates a flawless native PowerPoint gradient that is lightweight, resolution-independent, and doesn't rely on downloading external PIL images. |
| **Massive Typography** | `python-pptx` native | Standard text frames with tightened `line_spacing` (0.85) and contrasting font sizes perfectly recreate the title card aesthetic. |
| **CTA Arrows** | `python-pptx` shapes | Native `MSO_SHAPE.DOWN_ARROW` provides the crisp, flat vector geometry needed for the end-screen call-to-actions. |

*Feasibility Assessment*: 100%. This code beautifully merges the massive typographic title card (0:18) and the closing screen (0:21) into a single, highly reusable layout.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    pre_title: str = "HOW TO",
    main_title: str = "END",
    post_title: str = "A PRESENTATION",
    cta_1: str = "FOLLOW US\nCLICK HERE",
    cta_2: str = "MORE INFO\nCLICK HERE",
    url_text: str = "www.expertacademy.be",
    accent_color: tuple = (30, 90, 150),
    **kwargs
) -> str:
    """
    Create a PPTX file reproducing the "Macro Typographic & CTA" visual effect.
    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.dml.color import RGBColor
    from pptx.oxml import parse_xml

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

    # === Layer 1: Radial Gradient Background (via lxml injection) ===
    bg_rect = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg_rect.line.fill.background()
    spPr = bg_rect._element.spPr

    # Remove default solid fill if present
    for child in list(spPr):
        if child.tag.endswith('Fill'):
            spPr.remove(child)

    # Inject native PowerPoint radial gradient (center white, edges light grey)
    grad_xml = """
    <a:gradFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" rotWithShape="1">
        <a:gsLst>
            <a:gs pos="0"><a:srgbClr val="FFFFFF"/></a:gs>
            <a:gs pos="100000"><a:srgbClr val="DCE0E5"/></a:gs>
        </a:gsLst>
        <a:path path="rect">
            <a:fillToRect l="50000" t="50000" r="50000" b="50000"/>
        </a:path>
    </a:gradFill>
    """
    spPr.insert(0, parse_xml(grad_xml))

    # === Layer 2: Massive Typographic Block ===
    # Top 60% of the slide
    tb = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(11.333), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True

    # Pre-title
    p1 = tf.paragraphs[0]
    p1.alignment = PP_ALIGN.CENTER
    p1.line_spacing = 0.85
    run1 = p1.add_run()
    run1.text = pre_title + "\n"
    run1.font.size = Pt(54)
    run1.font.bold = True
    run1.font.name = "Arial"
    run1.font.color.rgb = RGBColor(110, 110, 110)

    # Main Hero Title
    p2 = tf.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    p2.line_spacing = 0.85
    run2 = p2.add_run()
    run2.text = main_title + "\n"
    run2.font.size = Pt(140)
    run2.font.bold = True
    run2.font.name = "Arial"
    run2.font.color.rgb = RGBColor(*accent_color)

    # Post-title
    p3 = tf.add_paragraph()
    p3.alignment = PP_ALIGN.CENTER
    p3.line_spacing = 0.85
    run3 = p3.add_run()
    run3.text = post_title
    run3.font.size = Pt(44)
    run3.font.bold = True
    run3.font.name = "Arial"
    run3.font.color.rgb = RGBColor(70, 70, 70)

    # === Layer 3: Call-To-Action (CTA) Geometry ===
    arrow_width = Inches(1.8)
    arrow_height = Inches(2.2)
    arrow_y = Inches(4.8)

    # Left CTA Arrow
    x_left = Inches(2.8)
    arrow1 = slide.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, x_left, arrow_y, arrow_width, arrow_height)
    arrow1.fill.solid()
    arrow1.fill.fore_color.rgb = RGBColor(*accent_color)
    arrow1.line.color.rgb = RGBColor(*accent_color)  # Hide outline
    arrow1.text_frame.text = cta_1
    for paragraph in arrow1.text_frame.paragraphs:
        paragraph.alignment = PP_ALIGN.CENTER
        for run in paragraph.runs:
            run.font.size = Pt(13)
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)

    # Right CTA Arrow
    x_right = prs.slide_width - Inches(2.8) - arrow_width
    arrow2 = slide.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, x_right, arrow_y, arrow_width, arrow_height)
    arrow2.fill.solid()
    arrow2.fill.fore_color.rgb = RGBColor(*accent_color)
    arrow2.line.color.rgb = RGBColor(*accent_color)
    arrow2.text_frame.text = cta_2
    for paragraph in arrow2.text_frame.paragraphs:
        paragraph.alignment = PP_ALIGN.CENTER
        for run in paragraph.runs:
            run.font.size = Pt(13)
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)

    # Central CTA Link / URL Text
    url_box = slide.shapes.add_textbox(Inches(4.5), Inches(5.6), Inches(4.333), Inches(0.8))
    url_p = url_box.text_frame.paragraphs[0]
    url_p.alignment = PP_ALIGN.CENTER
    url_run = url_p.add_run()
    url_run.text = url_text
    url_run.font.size = Pt(22)
    url_run.font.bold = True
    url_run.font.color.rgb = RGBColor(*accent_color)
    url_run.font.underline = True

    # Save and return
    prs.save(output_pptx_path)
    return output_pptx_path
```