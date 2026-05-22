# Numbered Feature Spotlight

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Numbered Feature Spotlight

*   **Core Visual Mechanism**: This design pattern uses clean, high-contrast blocks to present a numbered list. The core signature is a vibrant, colored square containing a large numeral, placed adjacent to a white, rounded rectangle that holds the descriptive text. A subtle drop shadow on the text block lifts it from the background, creating a sense of depth and focus.

*   **Why Use This Skill (Rationale)**: This technique works by creating a powerful visual hierarchy that is both aesthetically pleasing and highly functional. It transforms a simple list into a structured, easily scannable visual journey. The numbered blocks act as strong visual anchors, guiding the audience's attention sequentially, while the clean separation of number and text enhances readability and information retention.

*   **Overall Applicability**: This style is exceptionally versatile for corporate and educational presentations. It excels in scenarios such as:
    *   Presenting step-by-step processes or guides.
    *   Outlining key features or benefits of a product.
    *   Summarizing an agenda or key takeaways.
    *   Breaking down complex topics into digestible points.

*   **Value Addition**: Compared to a standard bulleted list, the Numbered Feature Spotlight adds a layer of professionalism and design intentionality. It feels more organized, modern, and engaging. The use of color and shadow directs focus far more effectively than simple text, making the information feel more significant and easier to process.

### 2. Visual Breakdown

*   **Step A: Core Visual Elements**
    *   **Background**: A solid, dark corporate blue serves as the foundation, providing high contrast for the lighter elements.
        *   Representative Color: Dark Navy/Indigo `(45, 45, 82, 255)`
    *   **Number Box**: A perfect square with a vibrant, attention-grabbing fill color.
        *   Representative Accent Color: Bright Orange `(247, 107, 28, 255)`
    *   **Text Bar**: A white, rounded rectangle that contains the main content. The rounded corners soften the otherwise geometric layout.
        *   Fill Color: White `(255, 255, 255, 255)`
    *   **Shadow**: A subtle, diffuse drop shadow applied to the Text Bar gives it a floating, three-dimensional quality.
    *   **Text Hierarchy**:
        *   **Number**: Large, bold, white, sans-serif font (e.g., Arial Black, Calibri Bold) centered within the Number Box.
        *   **Item Text**: Standard weight, dark gray or black sans-serif font (e.g., Calibri) vertically centered and left-aligned within the Text Bar.

*   **Step B: Compositional Style**
    *   **Alignment**: The Number Box and Text Bar are vertically aligned to their centers.
    *   **Spacing**: A small, consistent gap (approx. 2% of slide width) separates the Number Box from the Text Bar.
    *   **Layout**: The components are typically arranged in a vertical stack down the center or left side of the slide, with generous white space between each numbered item.

*   **Step C: Dynamic Effects & Transitions**
    *   The video shows simple "Appear" or "Fade" animations for each list item, which can be set manually in PowerPoint. The core static design is fully reproducible in code.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Dark blue background | `python-pptx` native | `slide.background.fill.solid()` is the direct and correct way to set a solid color background. |
| Numbered square & Text Bar | `python-pptx` native | Creating basic shapes (rectangle, rounded rectangle) and adding text are core functionalities. |
| **Drop Shadow on Text Bar** | **lxml XML injection** | **Crucial:** `python-pptx` lacks an API for shadow effects. Direct manipulation of the shape's `<p:spPr>` (Shape Properties) XML is the only way to programmatically add the shadow, which is essential for the "lifted" 3D look. |

> **Feasibility Assessment**: 100%. All key visual elements from the tutorial's list style (color, shapes, text, and the critical drop shadow) are reproducible with the combination of `python-pptx` and `lxml`.

#### 3b. Complete Reproduction Code

This single function generates a complete PPTX slide with multiple numbered spotlight items.

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "Understanding Employee Spotlight",
    list_items: list = None,
    bg_color: tuple = (45, 45, 82),
    accent_color: tuple = (247, 107, 28),
    **kwargs,
) -> str:
    """
    Creates a PPTX slide with the 'Numbered Feature Spotlight' design.

    This style features clean, numbered blocks with drop shadows for a professional look.

    Args:
        output_pptx_path: Path to save the generated PPTX file.
        title_text: The main title for the slide.
        list_items: A list of strings, where each string is a point in the numbered list.
        bg_color: RGB tuple for the slide background.
        accent_color: RGB tuple for the numbered squares.
        **kwargs: Not used, for compatibility.

    Returns:
        The path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE
    from lxml import etree

    # Default list if none provided
    if list_items is None:
        list_items = [
            "Short text, video or written spotlight interview",
            "Podcast",
            "Blog",
            "Digital spotlight platform",
            "Events",
        ]

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: Background ===
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*bg_color)

    # === Layer 2: Title ===
    title_shape = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(12.33), Inches(1.0))
    title_tf = title_shape.text_frame
    p = title_tf.paragraphs[0]
    p.text = title_text
    p.font.name = "Calibri Light"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.LEFT

    # === Layer 3: Numbered List Items ===
    
    # Helper function to inject shadow XML
    def add_shadow_effect(shape):
        """Adds a standard outer drop shadow to a shape."""
        # XML for a soft, 40% transparent black shadow, offset down and right
        shadow_xml = f"""
            <a:effectLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
              <a:outerShdw blurRad="76200" dist="38100" dir="2700000" rotWithShape="0">
                <a:srgbClr val="000000">
                  <a:alpha val="40000"/>
                </a:srgbClr>
              </a:outerShdw>
            </a:effectLst>
        """
        # Get the shape's properties element
        spPr = shape.element.get_or_add_spPr()
        # Parse and append the shadow effect
        effect_lst = etree.fromstring(shadow_xml)
        spPr.append(effect_lst)


    # --- Loop to create list items ---
    start_top = Inches(1.75)
    item_height = Inches(0.8)
    item_spacing = Inches(0.2)
    
    for i, item_text in enumerate(list_items):
        current_top = start_top + i * (item_height + item_spacing)
        
        # Number Box (Square)
        num_box_size = Inches(0.8)
        num_box_left = Inches(1.5)
        num_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, num_box_left, current_top, num_box_size, num_box_size)
        num_box.fill.solid()
        num_box.fill.fore_color.rgb = RGBColor(*accent_color)
        num_box.line.fill.background()

        # Number Text
        num_tf = num_box.text_frame
        num_tf.vertical_anchor = 'middle'
        p_num = num_tf.paragraphs[0]
        p_num.text = f"{i+1:02d}" # Formats as 01, 02, etc.
        p_num.font.name = 'Arial Black'
        p_num.font.size = Pt(28)
        p_num.font.color.rgb = RGBColor(255, 255, 255)
        p_num.alignment = PP_ALIGN.CENTER

        # Text Bar (Rounded Rectangle)
        text_bar_left = num_box_left + num_box_size + Inches(0.2)
        text_bar_width = Inches(8)
        text_bar = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, text_bar_left, current_top, text_bar_width, item_height)
        text_bar.fill.solid()
        text_bar.fill.fore_color.rgb = RGBColor(255, 255, 255)
        text_bar.line.fill.background()
        
        # Apply shadow using lxml
        add_shadow_effect(text_bar)

        # Item Text
        item_tf = text_bar.text_frame
        item_tf.margin_left = Inches(0.2)
        item_tf.vertical_anchor = 'middle'
        p_item = item_tf.paragraphs[0]
        p_item.text = item_text
        p_item.font.name = 'Calibri'
        p_item.font.size = Pt(22)
        p_item.font.color.rgb = RGBColor(30, 30, 30)
        p_item.alignment = PP_ALIGN.LEFT

    prs.save(output_pptx_path)
    return output_pptx_path
```

#### 3c. Verification Checklist

- [x] Does the code import all required libraries? (`pptx`, `lxml`)
- [x] Does it handle the case where an image download fails (fallback)? (N/A - no image download)
- [x] Are all color values explicit RGB tuples? (Yes)
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect? (Yes, specifically the numbered list style.)
- [x] Would someone looking at the output say "yes, that's the same technique"? (Yes, the core elements are faithfully reproduced.)