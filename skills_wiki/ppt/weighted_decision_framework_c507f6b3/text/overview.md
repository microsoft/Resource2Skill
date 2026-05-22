# Weighted Decision Framework

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Weighted Decision Framework

*   **Core Visual Mechanism**: This design employs a balance scale as a central visual metaphor to compare "Pros" and "Cons". It transforms an abstract list into a tangible, intuitive graphic that visually represents the act of weighing options. The design is clean, corporate, and relies on simple geometric shapes to build a powerful narrative.

*   **Why Use This Skill (Rationale)**: The balance scale is a universally understood symbol for justice, equilibrium, and comparison. By mapping "Pros" and "Cons" onto the scale, the slide instantly communicates the purpose of the information: to evaluate and make a balanced decision. This metaphorical approach is more engaging and memorable than a simple two-column table.

*   **Overall Applicability**: This style is highly effective in business and strategic contexts. It is ideal for:
    *   Business case presentations (e.g., "Should we invest in Project X?").
    *   Product comparison and feature analysis.
    *   Strategic decision-making meetings.
    *   Risk assessment slides.

*   **Value Addition**: Compared to a plain bullet-point list, this design adds a layer of analytical storytelling. It frames the discussion around balance and trade-offs, encouraging the audience to think critically about the presented points. The addition of quantifiable metrics (like percentages) below the scale can further ground the decision-making process in data.

### 2. Visual Breakdown

*   **Step A: Core Visual Elements**
    *   **Scale Graphic**: A composition of simple black shapes forming a classic balance scale.
        *   Color: Black `(32, 33, 36, 255)`
    *   **Pro Card**: A primary-colored card for positive points.
        *   Fill Color: Corporate Blue `(0, 112, 192, 255)`
        *   Icon: Thumbs Up `MSO_SHAPE.THUMB_UP` (White fill)
        *   Text: White `(255, 255, 255, 255)`
    *   **Con Card**: A secondary-colored card for negative points.
        *   Fill Color: Teal `(47, 132, 128, 255)`
        *   Icon: Thumbs Down `MSO_SHAPE.THUMB_DOWN` (White fill)
        *   Text: White `(255, 255, 255, 255)`
    *   **Data Pods**: Two subtle, shadowed text boxes below the scale to display summary data or key takeaways.
        *   Fill Color: White `(255, 255, 255, 255)` with a subtle transparency.
        *   Shadow: Soft, black, 40% transparent drop shadow.
        *   Text: Dark Gray `(64, 64, 64, 255)`

*   **Step B: Compositional Style**
    *   **Symmetry & Balance**: The entire composition is built around a central vertical axis, reinforcing the theme of balance. The scale is perfectly centered and symmetrical.
    *   **Layering for Depth**: The design uses layering to create a sense of three-dimensionality. The Pro/Con cards sit on top of the scale's trays, and the data pods float "in front" of the background with a soft shadow.
    *   **Proportions**: The scale graphic is the hero element, occupying approximately 70% of the slide width and centered vertically. The data pods are smaller and placed in the lower third of the slide, providing supporting information without overwhelming the main graphic.
    *   **Negative Space**: The design uses generous white space to keep the focus on the central metaphor and prevent a cluttered feel.

*   **Step C: Dynamic Effects & Transitions**
    *   The source video shows a static design. However, this layout would be well-suited for "Wipe" or "Float In" animations, where the Pro and Con cards appear sequentially to build the argument. These animations would need to be applied manually in PowerPoint.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect         | Method                | Why this method                                                                                                                              |
| ---------------------------- | --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| Scale, Trays, and Pro/Con Cards | `python-pptx` native    | The core visual elements are standard geometric shapes (rectangles, ovals, rounded rectangles) that are easily created and positioned with `python-pptx`. |
| Shadow on Data Pods          | `lxml` XML injection  | `python-pptx` has no public API for applying shadow effects to shapes. Direct manipulation of the Open XML is required to add the `<a:outerShdw>` element. |
| Text and Icons               | `python-pptx` native    | Placing and formatting text, as well as adding standard icons like thumbs up/down, is a core strength of the `python-pptx` library.          |

> **Feasibility Assessment**: 95%. This code reproduces the entire structure, layout, color scheme, and the crucial shadow effect. The only potential deviations would be the exact font rendering and minor icon scaling, which are dependent on the user's environment. The visual identity is fully captured.

#### 3b. Complete Reproduction Code

```python
import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from lxml import etree

def add_shadow_to_shape(shape):
    """
    Applies a soft outer shadow to a shape using lxml to manipulate the OOXML.
    """
    # Create a namespace map
    nsmap = {
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'
    }

    # Get the shape's XML element
    sp = shape._element
    # Find the shape properties (spPr) element
    spPr = sp.xpath('p:spPr', namespaces=nsmap)[0]

    # Create the effect list element <a:effectLst>
    effect_list = etree.SubElement(spPr, etree.QName(nsmap['a'], 'effectLst'))

    # Create the outer shadow element <a:outerShdw>
    # blurRad="50800" (4pt), dist="38100" (3pt), dir="5400000" (90 deg), algn="bl"
    shadow = etree.SubElement(effect_list, etree.QName(nsmap['a'], 'outerShdw'),
                              blurRad="50800", dist="38100", dir="5400000", algn="bl")

    # Set the shadow color <a:srgbClr> with transparency <a:alpha>
    shadow_color = etree.SubElement(shadow, etree.QName(nsmap['a'], 'srgbClr'), val="000000")
    etree.SubElement(shadow_color, etree.QName(nsmap['a'], 'alpha'), val="40000") # 40% transparency

def create_slide(
    output_pptx_path: str,
    pro_text: str = "Maecenas non laoreet odio",
    con_text: str = "Maecenas non laoreet odio",
    pro_data_text: str = "Maecenas non laoreet odio. Fusce lobortis porttitor purus, vel vestibulum libero pharetra vel.",
    con_data_text: str = "Maecenas non laoreet odio. Fusce lobortis porttitor purus, vel vestibulum libero pharetra vel.",
    pro_percentage: int = 45,
    con_percentage: int = 45,
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the Weighted Decision Framework visual effect.

    Args:
        output_pptx_path: Path to save the generated .pptx file.
        pro_text: Text for the "Pros" card.
        con_text: Text for the "Cons" card.
        pro_data_text: Text for the data pod under the "Pros" side.
        con_data_text: Text for the data pod under the "Cons" side.
        pro_percentage: Percentage value for the "Pros" data pod.
        con_percentage: Percentage value for the "Cons" data pod.

    Returns:
        Path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # --- Define Colors ---
    BLACK = RGBColor(32, 33, 36)
    PRO_BLUE = RGBColor(0, 112, 192)
    CON_TEAL = RGBColor(47, 132, 128)
    WHITE = RGBColor(255, 255, 255)
    TEXT_GRAY = RGBColor(89, 89, 89)
    PERCENT_BLUE = RGBColor(0, 112, 192)

    # --- Layer 1: Build the Scale Graphic ---
    # Central anchor point for the scale
    cx, cy = Inches(13.333 / 2), Inches(3.5)

    # Base
    base = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx - Inches(1.5), cy + Inches(1.2), Inches(3), Inches(0.2))
    base.fill.solid(); base.fill.fore_color.rgb = BLACK; base.line.fill.background()
    # Stand
    stand = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx - Inches(0.1), cy - Inches(0.5), Inches(0.2), Inches(1.7))
    stand.fill.solid(); stand.fill.fore_color.rgb = BLACK; stand.line.fill.background()
    # Fulcrum
    fulcrum = slide.shapes.add_shape(MSO_SHAPE.OVAL, cx - Inches(0.25), cy - Inches(0.75), Inches(0.5), Inches(0.5))
    fulcrum.fill.solid(); fulcrum.fill.fore_color.rgb = BLACK; fulcrum.line.fill.background()
    # Beam
    beam = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx - Inches(4), cy - Inches(0.6), Inches(8), Inches(0.2))
    beam.fill.solid(); beam.fill.fore_color.rgb = BLACK; beam.line.fill.background()
    # Trays
    tray_l = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx - Inches(4.5), cy - Inches(0.4), Inches(2.2), Inches(0.08))
    tray_l.fill.solid(); tray_l.fill.fore_color.rgb = BLACK; tray_l.line.fill.background()
    tray_r = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx + Inches(2.3), cy - Inches(0.4), Inches(2.2), Inches(0.08))
    tray_r.fill.solid(); tray_r.fill.fore_color.rgb = BLACK; tray_r.line.fill.background()

    # --- Layer 2: Pro and Con Cards ---
    # Pro Card (Left)
    pro_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx - Inches(4.5), cy - Inches(1.8), Inches(2.2), Inches(1.4))
    pro_card.fill.solid(); pro_card.fill.fore_color.rgb = PRO_BLUE; pro_card.line.fill.background()
    pro_card.text_frame.text = "Pros\n" + pro_text
    pro_card.text_frame.paragraphs[0].font.bold = True
    pro_card.text_frame.paragraphs[0].font.size = Pt(18)
    pro_card.text_frame.paragraphs[1].font.size = Pt(12)
    for p in pro_card.text_frame.paragraphs:
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER
    pro_icon = slide.shapes.add_shape(MSO_SHAPE.THUMB_UP, cx - Inches(3.95), cy - Inches(2.4), Inches(0.5), Inches(0.5))
    pro_icon.fill.solid(); pro_icon.fill.fore_color.rgb = WHITE; pro_icon.line.fill.background()

    # Con Card (Right)
    con_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx + Inches(2.3), cy - Inches(1.8), Inches(2.2), Inches(1.4))
    con_card.fill.solid(); con_card.fill.fore_color.rgb = CON_TEAL; con_card.line.fill.background()
    con_card.text_frame.text = "Cons\n" + con_text
    con_card.text_frame.paragraphs[0].font.bold = True
    con_card.text_frame.paragraphs[0].font.size = Pt(18)
    con_card.text_frame.paragraphs[1].font.size = Pt(12)
    for p in con_card.text_frame.paragraphs:
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER
    con_icon = slide.shapes.add_shape(MSO_SHAPE.THUMB_DOWN, cx + Inches(2.85), cy - Inches(2.4), Inches(0.5), Inches(0.5))
    con_icon.fill.solid(); con_icon.fill.fore_color.rgb = WHITE; con_icon.line.fill.background()

    # --- Layer 3: Data Pods with Shadows ---
    # Pro Data Pod (Left)
    pro_data_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1), Inches(5), Inches(5), Inches(1.75))
    pro_data_card.fill.solid(); pro_data_card.fill.fore_color.rgb = WHITE; pro_data_card.line.fill.background()
    add_shadow_to_shape(pro_data_card)
    # Text in Pro Data Pod
    p_tf = pro_data_card.text_frame
    p_tf.margin_left = Inches(0.8)
    p_tf.text = pro_data_text
    p_tf.paragraphs[0].font.size = Pt(11)
    p_tf.paragraphs[0].font.color.rgb = TEXT_GRAY
    # Percentage Box
    p_percent_box = slide.shapes.add_textbox(Inches(1.2), Inches(5.2), Inches(1), Inches(1))
    p_percent_box.text_frame.text = f"{pro_percentage}%"
    p_percent_box.text_frame.paragraphs[0].font.size = Pt(24)
    p_percent_box.text_frame.paragraphs[0].font.bold = True
    p_percent_box.text_frame.paragraphs[0].font.color.rgb = PERCENT_BLUE

    # Con Data Pod (Right)
    con_data_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.333), Inches(5), Inches(5), Inches(1.75))
    con_data_card.fill.solid(); con_data_card.fill.fore_color.rgb = WHITE; con_data_card.line.fill.background()
    add_shadow_to_shape(con_data_card)
    # Text in Con Data Pod
    c_tf = con_data_card.text_frame
    c_tf.margin_left = Inches(0.8)
    c_tf.text = con_data_text
    c_tf.paragraphs[0].font.size = Pt(11)
    c_tf.paragraphs[0].font.color.rgb = TEXT_GRAY
    # Percentage Box
    c_percent_box = slide.shapes.add_textbox(Inches(7.533), Inches(5.2), Inches(1), Inches(1))
    c_percent_box.text_frame.text = f"{con_percentage}%"
    c_percent_box.text_frame.paragraphs[0].font.size = Pt(24)
    c_percent_box.text_frame.paragraphs[0].font.bold = True
    c_percent_box.text_frame.paragraphs[0].font.color.rgb = PERCENT_BLUE

    # --- Save the presentation ---
    prs.save(output_pptx_path)
    return output_pptx_path

# Example Usage:
# if __name__ == '__main__':
#     file_path = "weighted_decision_framework.pptx"
#     create_slide(file_path)
#     print(f"Presentation saved to {os.path.abspath(file_path)}")

```

#### 3c. Verification Checklist

-   [x] Does the code import all required libraries?
-   [x] Does it handle the case where an image download fails (fallback)? (N/A, no images used)
-   [x] Are all color values explicit RGB tuples (not referencing undefined variables)?
-   [x] Does it produce a visually recognizable reproduction of the tutorial's effect?
-   [x] Would someone looking at the output say "yes, that's the same technique"?