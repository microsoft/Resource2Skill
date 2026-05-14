# Chevron-Tabular Graphic List

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Chevron-Tabular Graphic List

* **Core Visual Mechanism**: This pattern replaces a standard, boring grid table with a sequence of styled, modular rows. The defining signature is the **overlapping two-tone chevron (pentagon) header** on the left of each row. It creates a sense of forward momentum, pointing directly into the contiguous grey data blocks. The data columns themselves are borderless, separated only by razor-thin white gaps, creating a clean "ribbon" or "bar" aesthetic. Floating "pill" shapes act as column headers, detaching them from the rigid structure of a standard table header.
* **Why Use This Skill (Rationale)**: Standard PowerPoint tables often feel dry, cramped, and visually heavy due to gridlines. This approach uses Gestalt principles of continuity and enclosure to group data by row without needing lines. The chevron shape naturally guides the eye from the category/product name across to the specific data points, improving readability and visual flow.
* **Overall Applicability**: Ideal for product feature comparisons, pricing structures, step-by-step specifications, or any structured data list where you want the slide to feel like a modern UI dashboard rather than a spreadsheet.
* **Value Addition**: Transforms tabular data into a highly visual, branded asset. The use of discrete colored blocks makes each item feel distinct and important, while the strictly aligned right-hand columns maintain mathematical readability.


### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Row Anchor**: A two-tone left header. A dark square block containing a white icon sits flush against a brighter pentagon (chevron) containing the title. 
  - **Data Cells**: Borderless rectangles. 
  - **Color Logic**: 
    - Row Accents: Vibrant flat UI colors. e.g., Blue `(52, 152, 219)`, Red `(231, 76, 60)`, Orange `(243, 156, 18)`.
    - Middle Cell: Soft Grey `(235, 235, 235)`.
    - Right Cell: Lighter Grey `(245, 245, 245)`.
    - Column Headers: Dark Charcoal `(80, 80, 80)` for high contrast.
  - **Text Hierarchy**: 
    - Slide Title: Large (28pt), Bold, Dark Grey.
    - Row Titles: White, Bold, 12pt.
    - Descriptions: Medium Grey, regular weight, 11pt.
    - Values/Prices: Dark Grey, Bold, 12pt.

* **Step B: Compositional Style**
  - The list is centrally balanced. Total width is ~10 inches on a 13.33-inch canvas.
  - **Crucial Overlap**: The colored chevron points *into* and physically overlaps the left edge of the grey middle rectangle. This eliminates awkward gaps and unifies the shape.
  - **Thin Separators**: A micro-gap (0.05 inches) between the middle and right data cells allows the white slide background to peek through, creating a crisp, non-obtrusive vertical divider.

* **Step C: Dynamic Effects & Transitions**
  - In the tutorial, these rows animate via a "Wipe" from left to right, emphasizing the forward-pointing nature of the chevron.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Overall Layout & Shapes** | `python-pptx` native | The effect relies entirely on clean, flat vector geometry. Native shapes ensure the slide remains 100% editable for text, colors, and resizing. |
| **Two-tone Chevron Header** | `python-pptx` shape stacking | By precisely layering a dark `RECTANGLE` over the flat left edge of a bright `PENTAGON`, we achieve the two-tone icon/title block seen in the video without needing complex custom polygons. |
| **Seamless Block Connection** | `python-pptx` z-ordering | Drawing the grey data block *first*, and then rendering the colored pentagon slightly over its left edge, ensures the chevron tip perfectly merges into the data row. |

> **Feasibility Assessment**: 100% — The static visual design from the tutorial can be perfectly reproduced using native PowerPoint shapes.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "LIST OF PRODUCTS",
    subtitle_text: str = "MENTION YOUR SLIDE SUBTITLE HERE TO PROVIDE ADDITIONAL CONTEXT",
    items_data: list = None,
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the "Chevron-Tabular Graphic List" visual effect.
    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
    from pptx.dml.color import RGBColor

    # Initialize presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # Ensure pure white background for crisp gaps
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = RGBColor(255, 255, 255)

    # === Layer 1: Titles ===
    title_box = slide.shapes.add_textbox(Inches(0), Inches(0.5), Inches(13.333), Inches(0.8))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.alignment = PP_ALIGN.CENTER
    p.font.bold = True
    p.font.size = Pt(28)
    p.font.color.rgb = RGBColor(60, 60, 60)

    sub_box = slide.shapes.add_textbox(Inches(0), Inches(1.2), Inches(13.333), Inches(0.4))
    tf_sub = sub_box.text_frame
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = subtitle_text
    p_sub.alignment = PP_ALIGN.CENTER
    p_sub.font.size = Pt(12)
    p_sub.font.color.rgb = RGBColor(140, 140, 140)

    # === Layer 2: Column Headers (Pill Shapes) ===
    def add_pill_header(x, y, w, h, text):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
        shape.adjustments[0] = 0.5  # Max roundness creates the pill effect
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(80, 80, 80)
        shape.line.fill.solid()
        shape.line.fill.fore_color.rgb = RGBColor(80, 80, 80)
        
        tf = shape.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.text = text
        p.alignment = PP_ALIGN.CENTER
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = RGBColor(255, 255, 255)

    # Headers aligned with the data columns below
    add_pill_header(4.0, 2.3, 5.3, 0.4, "DESCRIPTION")
    add_pill_header(9.35, 2.3, 2.0, 0.4, "PRICING")

    # === Layer 3: Data Rows ===
    if items_data is None:
        items_data = [
            {"title": "PRODUCT 01", "color": (52, 152, 219), "dark_color": (41, 128, 185), "desc": "Lorem ipsum dolor sit amet werent consectetur adipiscing elit sed doe.", "price": "$ 36", "icon": "❖"},
            {"title": "PRODUCT 02", "color": (231, 76, 60), "dark_color": (192, 57, 43), "desc": "Lorem ipsum dolor sit amet werent consectetur adipiscing elit sed doe.", "price": "$ 42", "icon": "⚙"},
            {"title": "PRODUCT 03", "color": (243, 156, 18), "dark_color": (211, 84, 0), "desc": "Lorem ipsum dolor sit amet werent consectetur adipiscing elit sed doe.", "price": "$ 89", "icon": "⛶"},
            {"title": "PRODUCT 04", "color": (46, 204, 113), "dark_color": (39, 174, 96), "desc": "Lorem ipsum dolor sit amet werent consectetur adipiscing elit sed doe.", "price": "$ 63", "icon": "★"},
        ]

    y_start = 3.0
    row_h = 0.75
    gap = 0.15

    for i, item in enumerate(items_data):
        y = y_start + i * (row_h + gap)

        # 1. Middle Cell (Description) - Drawn first so it sits under the chevron tip
        mid_color = RGBColor(235, 235, 235)
        mid_rect = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(3.7), Inches(y), Inches(5.6), Inches(row_h))
        mid_rect.fill.solid()
        mid_rect.fill.fore_color.rgb = mid_color
        mid_rect.line.fill.solid()
        mid_rect.line.fill.fore_color.rgb = mid_color
        
        tf_mid = mid_rect.text_frame
        tf_mid.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf_mid.margin_left = Inches(0.4) # Indent text to avoid the overlapping chevron tip
        tf_mid.margin_right = Inches(0.2)
        p_mid = tf_mid.paragraphs[0]
        p_mid.text = item["desc"]
        p_mid.font.size = Pt(11)
        p_mid.font.color.rgb = RGBColor(85, 85, 85)

        # 2. Right Cell (Pricing)
        right_color = RGBColor(245, 245, 245)
        right_rect = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(9.35), Inches(y), Inches(2.0), Inches(row_h))
        right_rect.fill.solid()
        right_rect.fill.fore_color.rgb = right_color
        right_rect.line.fill.solid()
        right_rect.line.fill.fore_color.rgb = right_color

        tf_r = right_rect.text_frame
        tf_r.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_r = tf_r.paragraphs[0]
        p_r.text = item["price"]
        p_r.alignment = PP_ALIGN.CENTER
        p_r.font.bold = True
        p_r.font.size = Pt(12)
        p_r.font.color.rgb = RGBColor(50, 50, 50)

        # 3. Left Pentagon (Chevron Row Header) - Overlaps middle cell by 0.3 inches
        main_color = RGBColor(*item["color"])
        pent = slide.shapes.add_shape(MSO_SHAPE.PENTAGON, Inches(1.2), Inches(y), Inches(2.8), Inches(row_h))
        pent.fill.solid()
        pent.fill.fore_color.rgb = main_color
        pent.line.fill.solid()
        pent.line.fill.fore_color.rgb = main_color
        pent.text_frame.clear() # Clear default text to handle layering manually

        # 4. Icon Box (Dark square masking the flat left edge of the pentagon)
        dark_color = RGBColor(*item["dark_color"])
        icon_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(y), Inches(0.75), Inches(row_h))
        icon_box.fill.solid()
        icon_box.fill.fore_color.rgb = dark_color
        icon_box.line.fill.solid()
        icon_box.line.fill.fore_color.rgb = dark_color

        tf_icon = icon_box.text_frame
        tf_icon.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_icon = tf_icon.paragraphs[0]
        p_icon.text = item["icon"]
        p_icon.alignment = PP_ALIGN.CENTER
        p_icon.font.size = Pt(18)
        p_icon.font.color.rgb = RGBColor(255, 255, 255)

        # 5. Title Text Box (Floats securely over the main body of the pentagon)
        title_box = slide.shapes.add_textbox(Inches(1.95), Inches(y), Inches(1.8), Inches(row_h))
        tf_t = title_box.text_frame
        tf_t.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf_t.margin_left = Inches(0.1)
        tf_t.margin_right = 0
        tf_t.margin_top = 0
        tf_t.margin_bottom = 0
        
        p_t = tf_t.paragraphs[0]
        p_t.text = item["title"]
        p_t.alignment = PP_ALIGN.LEFT
        p_t.font.bold = True
        p_t.font.size = Pt(12)
        p_t.font.color.rgb = RGBColor(255, 255, 255)

    prs.save(output_pptx_path)
    return output_pptx_path
```