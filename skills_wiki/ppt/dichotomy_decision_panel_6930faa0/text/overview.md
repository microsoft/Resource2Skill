# Dichotomy Decision Panel

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Dichotomy Decision Panel

*   **Core Visual Mechanism**: This design pattern relies on a strong, binary visual division of the slide canvas. The space is split vertically into two distinct, high-contrast panels, typically green for "positive" (Pros, Advantages, Opportunities) and red for "negative" (Cons, Disadvantages, Risks). This chromatic and spatial separation is reinforced by large, universally understood icons like a checkmark (✓) and an 'X' (✗), allowing the audience to instantly grasp the slide's comparative purpose.

*   **Why Use This Skill (Rationale)**: The effectiveness of this style lies in its use of pre-attentive attributes. The brain processes the color and spatial split before reading any text, immediately establishing a "for vs. against" mental model. It leverages deeply ingrained cultural associations (green = go/good, red = stop/bad) to reduce cognitive load and make the presented information easily digestible. The rigid structure forces the presenter to be concise and balanced in their arguments.

*   **Overall Applicability**: This is a versatile and fundamental tool for any presentation focused on decision-making, evaluation, or comparison. It excels in scenarios such as:
    *   **Business Case Analysis**: Outlining the benefits vs. drawbacks of a new project.
    *   **Vendor/Software Evaluation**: Comparing two or more options side-by-side.
    *   **Strategy Meetings**: Debating the pros and cons of different strategic directions.
    *   **Risk Assessment**: Clearly separating opportunities from potential threats.

*   **Value Addition**: Compared to a simple bulleted list, the Dichotomy Decision Panel provides immediate clarity and visual impact. It transforms a potentially ambiguous list of points into a clear, structured argument, accelerating audience comprehension and facilitating faster, more informed decisions.

### 2. Visual Breakdown

*   **Step A: Core Visual Elements**
  - **Panels**: Two full-height rectangular panels, each occupying exactly 50% of the slide width.
  - **Icons**: Large, bold, single-color icons. A checkmark for the positive side, an 'X' for the negative side.
  - **Color Logic**:
    -   Positive Panel (Left): A solid, confident green. `(46, 179, 74)`
    -   Negative Panel (Right): A clear, cautionary red. `(217, 30, 24)`
    -   Text & Icons: High-contrast white for maximum readability. `(255, 255, 255)`
  - **Text Hierarchy**:
    -   **Header**: (e.g., "PROS", "CONS") - Large, all-caps, bold font (e.g., Arial Black, 44pt).
    -   **Body Text**: (Bullet points) - Standard sans-serif font (e.g., Arial, 20pt), with clear indentation.

*   **Step B: Compositional Style**
  - **Spatial Feel**: Symmetrical, balanced, and structured. The hard vertical line down the center creates a sense of opposition and balance.
  - **Layout Principles**: Each panel is a self-contained unit. The header and icon are vertically centered in the top third of the panel, while the body text is left-aligned and occupies the bottom two-thirds. Generous padding around the text is crucial to avoid a cramped look.
  - **Proportions**: The slide is divided 50/50 vertically. There are no overlapping elements.

*   **Step C: Dynamic Effects & Transitions**
  - This is primarily a static layout. Animations are not required for its core function.
  - If desired, a "Wipe" entrance animation (from center) could be manually applied in PowerPoint to reveal both panels simultaneously, reinforcing the central division. This is not reproducible in the code.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Split-screen colored panels | `python-pptx` native | Creating and coloring basic rectangle shapes is a core, efficient function of the library. |
| Titles and bullet points | `python-pptx` native | The library provides robust control over text box placement, text content, font properties, and paragraph alignment. |
| Checkmark and 'X' icons | `python-pptx` text box with Symbol Font | Using a text character from a symbol font (like Segoe UI Symbol) is far more reliable and scalable than trying to draw complex shapes with `FreeformBuilder` or importing images. It treats the icon as text, making it easy to color and resize. |

> **Feasibility Assessment**: 100%. The visual effect is based on strong typography, color, and layout principles, all of which are fully controllable via the `python-pptx` library. No complex image manipulation or XML injection is needed.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    pro_title: str = "PROS",
    con_title: str = "CONS",
    pro_points: list = ["Clarity and focus", "Saves significant time", "Aids quick decision-making"],
    con_points: list = ["Can look generic", "Risk of oversimplification", "May hide weak thinking"],
    pro_color_rgb: tuple = (46, 179, 74),
    con_color_rgb: tuple = (217, 30, 24),
    font_color_rgb: tuple = (255, 255, 255),
    **kwargs,
) -> str:
    """
    Creates a PPTX slide with a classic Pros and Cons dichotomy decision panel.

    Args:
        output_pptx_path (str): The path to save the generated PPTX file.
        pro_title (str): The title for the positive (left) panel.
        con_title (str): The title for the negative (right) panel.
        pro_points (list): A list of strings for the positive panel's bullet points.
        con_points (list): A list of strings for the negative panel's bullet points.
        pro_color_rgb (tuple): The RGB background color for the positive panel.
        con_color_rgb (tuple): The RGB background color for the negative panel.
        font_color_rgb (tuple): The RGB color for all text and icons.

    Returns:
        str: The path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN

    prs = Presentation()
    prs.slide_width = Inches(13.333)  # 16:9 aspect ratio
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

    # Define common dimensions
    slide_width = prs.slide_width
    slide_height = prs.slide_height
    panel_width = slide_width / 2

    # === Layer 1: Background Panels ===

    # Pro Panel (Left, Green)
    pro_panel = slide.shapes.add_shape(1, 0, 0, panel_width, slide_height)  # 1 is autoshape for rectangle
    pro_panel.fill.solid()
    pro_panel.fill.fore_color.rgb = RGBColor(*pro_color_rgb)
    pro_panel.line.fill.background()

    # Con Panel (Right, Red)
    con_panel = slide.shapes.add_shape(1, panel_width, 0, panel_width, slide_height)
    con_panel.fill.solid()
    con_panel.fill.fore_color.rgb = RGBColor(*con_color_rgb)
    con_panel.line.fill.background()

    # === Layer 2: Text and Icons ===

    # --- Pro Side Elements ---
    # Pro Title
    pro_title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), panel_width - Inches(1), Inches(1.0))
    tf_pro_title = pro_title_box.text_frame
    tf_pro_title.text = pro_title
    p_pro_title = tf_pro_title.paragraphs[0]
    p_pro_title.font.name = 'Arial Black'
    p_pro_title.font.size = Pt(44)
    p_pro_title.font.bold = True
    p_pro_title.font.color.rgb = RGBColor(*font_color_rgb)
    p_pro_title.alignment = PP_ALIGN.CENTER
    
    # Pro Icon (Checkmark)
    pro_icon_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), panel_width - Inches(1), Inches(1.5))
    tf_pro_icon = pro_icon_box.text_frame
    tf_pro_icon.text = "\u2714" # Unicode for Heavy Check Mark
    p_pro_icon = tf_pro_icon.paragraphs[0]
    p_pro_icon.font.name = 'Segoe UI Symbol'
    p_pro_icon.font.size = Pt(80)
    p_pro_icon.font.color.rgb = RGBColor(*font_color_rgb)
    p_pro_icon.alignment = PP_ALIGN.CENTER
    
    # Pro Bullet Points
    pro_points_box = slide.shapes.add_textbox(Inches(0.75), Inches(3.0), panel_width - Inches(1.5), Inches(4.0))
    tf_pro_points = pro_points_box.text_frame
    tf_pro_points.clear() # clear the default paragraph
    for point in pro_points:
        p = tf_pro_points.add_paragraph()
        p.text = point
        p.font.name = 'Arial'
        p.font.size = Pt(22)
        p.font.color.rgb = RGBColor(*font_color_rgb)
        p.level = 0
    tf_pro_points.margin_left = Inches(0.25)
    
    # --- Con Side Elements ---
    # Con Title
    con_title_box = slide.shapes.add_textbox(panel_width + Inches(0.5), Inches(0.5), panel_width - Inches(1), Inches(1.0))
    tf_con_title = con_title_box.text_frame
    tf_con_title.text = con_title
    p_con_title = tf_con_title.paragraphs[0]
    p_con_title.font.name = 'Arial Black'
    p_con_title.font.size = Pt(44)
    p_con_title.font.bold = True
    p_con_title.font.color.rgb = RGBColor(*font_color_rgb)
    p_con_title.alignment = PP_ALIGN.CENTER

    # Con Icon (X Mark)
    con_icon_box = slide.shapes.add_textbox(panel_width + Inches(0.5), Inches(1.5), panel_width - Inches(1), Inches(1.5))
    tf_con_icon = con_icon_box.text_frame
    tf_con_icon.text = "\u2718" # Unicode for Heavy Ballot X
    p_con_icon = tf_con_icon.paragraphs[0]
    p_con_icon.font.name = 'Segoe UI Symbol'
    p_con_icon.font.size = Pt(80)
    p_con_icon.font.color.rgb = RGBColor(*font_color_rgb)
    p_con_icon.alignment = PP_ALIGN.CENTER

    # Con Bullet Points
    con_points_box = slide.shapes.add_textbox(panel_width + Inches(0.75), Inches(3.0), panel_width - Inches(1.5), Inches(4.0))
    tf_con_points = con_points_box.text_frame
    tf_con_points.clear()
    for point in con_points:
        p = tf_con_points.add_paragraph()
        p.text = point
        p.font.name = 'Arial'
        p.font.size = Pt(22)
        p.font.color.rgb = RGBColor(*font_color_rgb)
        p.level = 0
    tf_con_points.margin_left = Inches(0.25)

    prs.save(output_pptx_path)
    return output_pptx_path

# Example Usage:
# create_slide("dichotomy_decision_panel.pptx")
```

#### 3c. Verification Checklist

- [x] Does the code import all required libraries?
- [x] Does it handle the case where an image download fails (fallback)? (N/A, no images used)
- [x] Are all color values explicit RGB tuples (not referencing undefined variables)?
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect?
- [x] Would someone looking at the output say "yes, that's the same technique"?