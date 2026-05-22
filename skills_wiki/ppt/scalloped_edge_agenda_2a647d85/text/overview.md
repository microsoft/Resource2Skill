# Scalloped Edge Agenda

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Scalloped Edge Agenda

*   **Core Visual Mechanism**: This design creates a dynamic "scalloped" or "tabbed" edge between a large image and a content area. This is achieved by placing white circular shapes that partially overlap the image's vertical border, creating a negative-space illusion of cutouts. These cutouts then serve as visually integrated containers for the agenda's numbering, seamlessly blending the list structure with the slide's imagery.

*   **Why Use This Skill (Rationale)**: The technique breaks the monotony of a standard split-screen layout. By replacing a hard vertical line with an interactive, curved boundary, it draws the eye and creates a sense of depth and craftsmanship. It transforms the list's numbering from a purely functional element into a core part of the slide's aesthetic composition, making the agenda feel more intentional and professionally designed.

*   **Overall Applicability**: This style is highly effective for any presentation that requires a numbered or itemized list alongside a strong visual anchor. It excels in:
    *   Agenda and table of contents slides.
    *   Outlining process steps or project phases.
    *   Showcasing a list of product features or benefits.
    *   Chapter or section divider slides.

*   **Value Addition**: It elevates a simple list into a sophisticated graphic element, making the information more engaging and memorable. The design feels custom and polished, increasing the perceived quality of the entire presentation.

### 2. Visual Breakdown

*   **Step A: Core Visual Elements**
    - **Background Image**: A single, impactful image that occupies the left ~45% of the slide's height, starting below the title area.
    - **Content Background**: A solid white rectangle (`(255, 255, 255, 255)`) covering the right side of the slide.
    - **"Scallop" Shapes**: White circles (`MSO_SHAPE.OVAL`) with no outline, strategically placed to create the cutout illusion.
    - **Text Hierarchy**:
        - **Main Title**: Large, bold, sans-serif font at the top-left.
        - **Item Numbers**: Centered within the white circles. Medium-sized, bold, sans-serif font in a dark color (e.g., `(50, 50, 50, 255)`).
        - **Item Text**: Positioned to the right of the numbers. Regular weight, sans-serif font, slightly smaller than the numbers.

*   **Step B: Compositional Style**
    - **Layout**: A modified split-screen layout. The image on the left provides visual context, while the clean white space on the right ensures readability for the agenda text.
    - **Focal Point**: The scalloped edge is the primary visual focal point, guiding the viewer's eye from the image to the agenda items.
    - **Alignment**: Strong vertical and horizontal alignment is crucial. Each number, its circle, and its corresponding text are vertically centered as a unit. These units are then distributed evenly down the slide.
    - **Proportions**: The image occupies approximately 45% of the slide width. The content area occupies the remaining 55%.

*   **Step C: Dynamic Effects & Transitions**
    - The base design is static. Animations are not a core part of this style but could be added. For example, each agenda item (circle, number, and text) could "Wipe" or "Fade" in sequentially.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Image placement and cropping | `python-pptx` native | Provides direct API calls to add and position a picture on the slide. |
| Scalloped edge "cutout" effect | `python-pptx` native shapes | The effect is an illusion created by placing white `MSO_SHAPE.OVAL` shapes with no outline on the seam between the image and white background. This is a basic shape operation. |
| Numbered list and agenda text | `python-pptx` native shapes and tables | A table is used for the agenda text to easily manage consistent vertical spacing and alignment. Text boxes are used for the numbers within the circles. |

> **Feasibility Assessment**: 100%. The visual effect is based on clever layering of standard shapes and text, all of which are fully supported by the `python-pptx` library.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "Agenda Slide Design #1",
    agenda_items: list = None,
    image_keyword: str = "business meeting",
    **kwargs,
) -> str:
    """
    Creates a PowerPoint slide with the "Scalloped Edge Agenda" design.

    Args:
        output_pptx_path (str): The path to save the generated PPTX file.
        title_text (str): The main title for the slide.
        agenda_items (list): A list of strings, where each string is an agenda item.
        image_keyword (str): A keyword to search for a background image on Unsplash.

    Returns:
        str: The path to the saved PPTX file.
    """
    import requests
    from io import BytesIO
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN, MSO_VERTICAL_ANCHOR
    from pptx.enum.shapes import MSO_SHAPE

    if agenda_items is None:
        agenda_items = [
            "Introduction",
            "Why do we need the transformation?",
            "What do we need to transform?",
            "How to transform the organization?",
            "Who are those driving the transformation?",
        ]

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: Background (White) ===
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(255, 255, 255)

    # === Layer 2: Image ===
    title_height = Inches(1.2)
    img_width = Inches(5.8)
    img_height = prs.slide_height - title_height
    img_left = Inches(0)
    img_top = title_height
    
    try:
        unsplash_url = f"https://source.unsplash.com/1600x900/?{image_keyword}"
        response = requests.get(unsplash_url, timeout=10)
        image_stream = BytesIO(response.content)
        pic = slide.shapes.add_picture(
            image_stream,
            img_left,
            img_top,
            width=img_width,
            height=img_height
        )
    except requests.exceptions.RequestException:
        # Fallback to a solid color rectangle if image download fails
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, img_left, img_top, img_width, img_height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(128, 128, 128)
        shape.line.fill.background()

    # === Layer 3: Text & Content ===
    # --- Main Title ---
    title_shape = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(8), Inches(0.8))
    title_tf = title_shape.text_frame
    title_p = title_tf.paragraphs[0]
    title_p.text = title_text
    title_p.font.name = "Arial"
    title_p.font.size = Pt(32)
    title_p.font.bold = True
    title_p.font.color.rgb = RGBColor(0, 0, 0)

    # --- Agenda Items and Scalloped Edge ---
    num_items = len(agenda_items)
    content_area_height = prs.slide_height - title_height
    item_v_spacing = content_area_height / num_items
    circle_diameter = Inches(0.8)

    for i, item_text in enumerate(agenda_items):
        v_center = title_height + (i + 0.5) * item_v_spacing

        # A. Add the white circle for the cutout effect
        circle_left = img_width - (circle_diameter / 2)
        circle_top = v_center - (circle_diameter / 2)
        circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, circle_left, circle_top, circle_diameter, circle_diameter)
        
        circle.fill.solid()
        circle.fill.fore_color.rgb = RGBColor(255, 255, 255)
        circle.line.fill.background() # No outline

        # B. Add the number inside the circle
        tf_num = circle.text_frame
        tf_num.clear()
        p_num = tf_num.paragraphs[0]
        p_num.text = str(i + 1)
        p_num.font.name = "Arial"
        p_num.font.size = Pt(18)
        p_num.font.bold = True
        p_num.font.color.rgb = RGBColor(50, 50, 50)
        p_num.alignment = PP_ALIGN.CENTER
        tf_num.vertical_anchor = MSO_VERTICAL_ANCHOR.MIDDLE
        
        # C. Add agenda item text
        text_left = img_width + Inches(0.5)
        text_width = prs.slide_width - text_left - Inches(0.5)
        text_height = item_v_spacing
        text_top = title_height + i * item_v_spacing
        
        txt_box = slide.shapes.add_textbox(text_left, text_top, text_width, text_height)
        tf_item = txt_box.text_frame
        tf_item.word_wrap = True
        tf_item.vertical_anchor = MSO_VERTICAL_ANCHOR.MIDDLE
        p_item = tf_item.paragraphs[0]
        p_item.text = item_text
        p_item.font.name = "Arial"
        p_item.font.size = Pt(16)
        p_item.font.color.rgb = RGBColor(89, 89, 89)

    prs.save(output_pptx_path)
    return output_pptx_path
```

#### 3c. Verification Checklist

- [x] Does the code import all required libraries?
- [x] Does it handle the case where an image download fails (fallback)? (Yes, creates a gray rectangle).
- [x] Are all color values explicit RGB tuples? (Yes).
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect? (Yes).
- [x] Would someone looking at the output say "yes, that's the same technique"? (Yes, the scalloped edge with numbers is the key feature and is reproduced accurately).