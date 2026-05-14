# Corporate Geometric Split-Panel & Academic Formatting

## Analysis

# Strategy Document: Reusable Design Styles and Reproducible Implementation Code

## 1. High-level Design Pattern Extraction

> **Skill Name**: Corporate Geometric Split-Panel & Academic Formatting

* **Core Visual Mechanism**: The defining visual idea is the adaptation of strict academic formatting rules (like APA) into a visually engaging, professional slide layout using strong geometric color blocking. The core signature is the "Split-Panel" design: a bold, solid-colored geometric anchor (usually a vertical block on the left) that houses the primary slide heading in negative space (white text), juxtaposed against a clean, expansive white canvas on the right for heavily structured, hierarchical text (bullet points or hanging-indent citations).
* **Why Use This Skill (Rationale)**: Academic and highly technical presentations often suffer from "wall of text" syndrome. By introducing a massive, high-contrast geometric block, the slide immediately gains a strong structural grid. It guides the eye naturally from the high-contrast anchor (the topic) to the structured details. The strict adherence to typographic rules (consistent casing, hanging indents for references) establishes high credibility and readability.
* **Overall Applicability**: Ideal for academic defenses, corporate research reports, strategic management consulting decks, and any scenario where dense, structured information needs to be presented with authority and clarity without relying on decorative imagery.
* **Value Addition**: Transforms a basic, boring outline into a structured, branded document. It creates a clear visual boundary between the "metadata" (slide title) and the "data" (the bulleted fragments), reducing cognitive load while maintaining the strict formatting expected in academic/professional environments.

## 2. Visual Breakdown

* **Step A: Core Visual Elements**
  * **Color Logic**: High contrast is key. A dominant, dark corporate/academic color acts as the anchor.
    * Primary Anchor (Navy Blue): `RGBA(31, 73, 125, 255)`
    * Background (Crisp White): `RGBA(255, 255, 255, 255)`
    * Body Text (Deep Charcoal): `RGBA(60, 60, 60, 255)`
  * **Text Hierarchy**:
    * **Slide Titles**: Large, Sans-Serif, Sentence Case, placed within the colored anchor block (White text).
    * **Body Text**: Concise "idea fragments" (not full sentences unless quoting), bulleted, standard font size, strict consistency in casing.
    * **References**: Hanging indent formatting, smaller font size, single-spaced lines.

* **Step B: Compositional Style**
  * **Split-Panel Layout**: The canvas is distinctly divided. Approximately 25-30% of the horizontal space is consumed by the vertical anchor block. The remaining 70-75% is dedicated to content, ensuring generous left margin padding within the white space so text doesn't crowd the color block.
  * **Typographic Alignment**: Everything aligns to a strict invisible grid. Titles align to the top-left of the anchor block; bullet points align to a vertical axis just right of the anchor block.

* **Step C: Dynamic Effects & Transitions**
  * This style relies on static structural stability rather than dynamic motion. The "effect" is the crisp, sudden transition from one perfectly structured grid to the next. Fade transitions are recommended over complex wipes.

## 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Geometric Split-Panel Layout** | `python-pptx` native shapes | Native shape objects (`add_shape`) perfectly replicate the clean, vector-based color blocking seen in PowerPoint's "Design Ideas". |
| **Academic Text Hierarchy & Bullets** | `python-pptx` native text frames | Native API allows precise control over font size, color, bullet styling, and paragraph alignment needed for professional outlines. |
| **Hanging Indents (Reference Slide)** | `python-pptx` native paragraph format | The API provides direct access to `left_indent` and `first_line_indent`, which are required to programmatically create APA-style hanging indents. |

> **Feasibility Assessment**: 100%. The visual style is rooted in strict typographic alignment and clean vector geometry, which `python-pptx` handles natively with perfect fidelity. The code below generates a 3-slide mini-deck demonstrating the Title, Split-Panel Content, and Reference slide layouts taught in the tutorial.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "Strategic Management Consultants",
    author_text: str = "Chelsea Seburn\nDepartment of Business: John F. Kennedy University\nSTM 252: Strategic Management\nDr. Keith Wade\nFebruary 5, 2021",
    accent_color: tuple = (31, 73, 125),  # Corporate Navy Blue
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the 'Corporate Geometric Split-Panel & Academic Formatting' visual effect.
    Generates a 3-slide deck demonstrating Title, Content, and Reference formatting.
    
    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE

    prs = Presentation()
    # Widescreen 16:9
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Define Theme Colors
    color_accent = RGBColor(*accent_color)
    color_text_dark = RGBColor(60, 60, 60)
    color_text_light = RGBColor(255, 255, 255)
    font_name = "Calibri"

    # ==========================================
    # SLIDE 1: Title Slide (Centered Academic)
    # ==========================================
    slide_layout_blank = prs.slide_layouts[6]
    slide_title = prs.slides.add_slide(slide_layout_blank)

    # Decorative Top Banner
    top_banner = slide_title.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 
        Inches(0), Inches(0), Inches(13.333), Inches(0.5)
    )
    top_banner.fill.solid()
    top_banner.fill.fore_color.rgb = color_accent
    top_banner.line.fill.background()

    # Title Text
    title_box = slide_title.shapes.add_textbox(Inches(1), Inches(1.5), Inches(11.333), Inches(1.5))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.name = font_name
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = color_text_dark
    p.alignment = PP_ALIGN.CENTER

    # Author/Meta Text
    meta_box = slide_title.shapes.add_textbox(Inches(2), Inches(3.5), Inches(9.333), Inches(3))
    tf_meta = meta_box.text_frame
    tf_meta.word_wrap = True
    
    for line in author_text.split('\n'):
        p = tf_meta.add_paragraph()
        p.text = line
        p.font.name = font_name
        p.font.size = Pt(20)
        p.font.color.rgb = color_text_dark
        p.alignment = PP_ALIGN.CENTER
        p.space_after = Pt(12)

    # ==========================================
    # SLIDE 2: Body Slide (Geometric Split-Panel)
    # ==========================================
    slide_body = prs.slides.add_slide(slide_layout_blank)

    # Left Anchor Panel (30% width)
    left_panel = slide_body.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 
        Inches(0), Inches(0), Inches(4), Inches(7.5)
    )
    left_panel.fill.solid()
    left_panel.fill.fore_color.rgb = color_accent
    left_panel.line.fill.background()

    # Heading inside Anchor Panel
    head_box = slide_body.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(3), Inches(3))
    tf_head = head_box.text_frame
    tf_head.word_wrap = True
    p = tf_head.paragraphs[0]
    p.text = "Company History"
    p.font.name = font_name
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = color_text_light
    p.alignment = PP_ALIGN.LEFT

    # Content Area (Right 70%)
    content_box = slide_body.shapes.add_textbox(Inches(4.5), Inches(0.5), Inches(8.333), Inches(6.5))
    tf_content = content_box.text_frame
    tf_content.word_wrap = True
    
    bullets = [
        "Founded by Jeff Bezos in 1995",
        "Started as an online bookstore",
        "Year one reached 1,000,000 in sales",
        "Current market value is extremely high",
        "Largest global e-commerce company",
        "Offers a wide variety of products and services"
    ]
    
    for item in bullets:
        p = tf_content.add_paragraph()
        p.text = item
        p.font.name = font_name
        p.font.size = Pt(24)
        p.font.color.rgb = color_text_dark
        p.level = 0
        p.space_after = Pt(24) # Generous spacing for readability

    # ==========================================
    # SLIDE 3: Reference Slide (Hanging Indent)
    # ==========================================
    slide_ref = prs.slides.add_slide(slide_layout_blank)

    # Simple Top Accent Line for continuity
    ref_line = slide_ref.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 
        Inches(0), Inches(0), Inches(13.333), Inches(0.2)
    )
    ref_line.fill.solid()
    ref_line.fill.fore_color.rgb = color_accent
    ref_line.line.fill.background()

    # Reference Heading
    ref_head_box = slide_ref.shapes.add_textbox(Inches(1), Inches(0.5), Inches(11.333), Inches(1))
    tf_ref_head = ref_head_box.text_frame
    p = tf_ref_head.paragraphs[0]
    p.text = "References"
    p.font.name = font_name
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = color_text_dark
    p.alignment = PP_ALIGN.CENTER

    # Reference List with Hanging Indents
    ref_box = slide_ref.shapes.add_textbox(Inches(1), Inches(1.5), Inches(11.333), Inches(5.5))
    tf_ref = ref_box.text_frame
    tf_ref.word_wrap = True
    
    references = [
        "Cuofano et al., (2019, March 20). Amazon Mission Statement and Vision Statement In A Nutshell. FourWeekMBA. https://fourweekmba.com/amazon-vision-statement-mission-statement/",
        "Farfan, B. (2019, November 20). Amazon's Mission Statement. The balance everyday. https://www.thebalanceeveryday.com/amazon-mission-statement-4068548",
        "Feiner, Lauren. (2019, January 7). Amazon is the most valuable public company in the world after passing Microsoft. CNBC. https://www.cnbc.com/2019/01/07/amazon-passes-microsoft-market-value-becomes-largest.html"
    ]
    
    for ref in references:
        p = tf_ref.add_paragraph()
        p.text = ref
        p.font.name = font_name
        p.font.size = Pt(16)
        p.font.color.rgb = color_text_dark
        p.space_after = Pt(14)
        
        # *** CORE MECHANISM: APA Hanging Indent Formula ***
        pf = p.paragraph_format
        pf.left_indent = Inches(0.5)
        pf.first_line_indent = Inches(-0.5)

    prs.save(output_pptx_path)
    return output_pptx_path
```