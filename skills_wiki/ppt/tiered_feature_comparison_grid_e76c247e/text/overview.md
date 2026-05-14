# Tiered Feature Comparison Grid

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Tiered Feature Comparison Grid

*   **Core Visual Mechanism**: A clean, structured multi-column grid that visually maps features to different product or service tiers. The design uses color-coded headers for each tier and simple, universally understood icons (checkmarks and crosses) for quick scannability. A prominent, vertically oriented "Features" bar on the left acts as a strong visual anchor for the rows, enhancing readability.

*   **Why Use This Skill (Rationale)**: This layout excels at presenting complex information in a digestible format. It leverages the human brain's natural ability to process grid-based data, allowing audiences to quickly compare offerings and identify the best option for their needs. The clear visual hierarchy and color coding reduce cognitive load, making the decision-making process easier.

*   **Overall Applicability**: This style is ideal for:
    *   Pricing pages for SaaS products or services.
    *   Product-to-product feature comparisons.
    *   Competitive analysis, comparing an "own" product against competitors.
    *   Internal presentations to decide on feature prioritization for different product tiers.

*   **Value Addition**: Compared to a simple bulleted list or a standard unformatted table, this design adds professionalism, clarity, and visual appeal. It guides the viewer's eye, highlights key differences, and makes the information feel organized and authoritative.

### 2. Visual Breakdown

*   **Step A: Core Visual Elements**
    - **Header Bar**: A top section containing company name and service type.
    - **Tier Columns**: Distinct columns for each product tier (e.g., "Basic", "Portfolio", "Business"). Each has a colored header.
    - **Feature Rows**: A list of features, with each feature name placed to the left of the main comparison table.
    - **Indicator Icons**: Green checkmarks (✓) and red crosses (✗) are used within the grid to indicate feature availability.
    - **Vertical Anchor**: A rotated, solid-color bar with the text "Features" on the far left.

    - **Color Logic**:
        - Background: White `(255, 255, 255, 255)`
        - Primary Accent (Headers, Vertical Bar): Dark Teal `(79, 129, 133, 255)`
        - Text on Accent: White `(255, 255, 255, 255)`
        - Main Text: Dark Gray `(64, 64, 64, 255)`
        - Checkmark Icon: Green `(0, 176, 80, 255)`
        - Cross Icon: Red `(255, 0, 0, 255)`
        - Table Borders: Light Gray `(217, 217, 217, 255)`

    - **Text Hierarchy**:
        - **Slide Title**: Large, bold, top-aligned.
        - **Tier Names**: Medium-sized, bold, white, centered in headers.
        - **Feature Names**: Regular weight, left-aligned.
        - **Icons**: Large font size for visibility.

*   **Step B: Compositional Style**
    - The layout is highly structured and symmetrical, following a clear grid.
    - The main table and its associated labels occupy approximately 80% of the slide width, creating a dominant and focused central element.
    - The vertical "Features" bar occupies the left ~5% of the slide, creating a strong vertical line that contrasts with the horizontal flow of the feature rows.
    - White space is used effectively to separate the header, the feature labels, and the main table, preventing a cluttered look.

*   **Step C: Dynamic Effects & Transitions**
    - The source video is static. For a live presentation, one could use a "Wipe" or "Fade" animation, revealing one feature row at a time to build the comparison step-by-step. These effects would need to be applied manually in PowerPoint but the static layout is fully reproducible via code.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect                  | Method                  | Why this method                                                                                                   |
| ------------------------------------- | ----------------------- | ----------------------------------------------------------------------------------------------------------------- |
| Overall layout and text boxes         | `python-pptx` native    | Ideal for placing and formatting standard shapes and text.                                                        |
| Tiered comparison grid                | `python-pptx` tables    | The `add_table` functionality is the most direct and robust way to create a structured, grid-based layout.      |
| Rotated "Features" bar                | `python-pptx` shapes    | A standard textbox shape can be filled, have its text formatted, and then be rotated to achieve the desired effect. |
| Checkmark and Cross icons             | Unicode characters      | Using text characters (✓, ✗) is simpler and more scalable than inserting multiple small image files.              |
| Color fills, borders, and font styles | `python-pptx` formatting | The library provides comprehensive APIs for controlling the visual properties of shapes, tables, and text.         |

> **Feasibility Assessment**: 100%. The chosen design is a classic table-based layout that relies on fundamental shapes, text, and table elements. All aspects of this visual style are fully reproducible using the `python-pptx` library.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "Product capability comparison for photo and videos editing website",
    company_name: str = "ABC Pvt. Ltd.",
    service_name: str = "Photo & Videos editing website",
    tiers: list = None,
    features: list = None,
    **kwargs,
) -> str:
    """
    Creates a PowerPoint slide with a tiered feature comparison grid.

    Args:
        output_pptx_path (str): The path to save the generated PPTX file.
        title_text (str): The main title of the slide.
        company_name (str): The name of the company.
        service_name (str): The name of the service being compared.
        tiers (list): A list of tier names (e.g., ["Basic", "Portfolio", "Business"]).
        features (list): A list of dictionaries, where each dict contains a "name"
                         and a "values" list of booleans corresponding to the tiers.

    Returns:
        str: The path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
    from pptx.enum.shapes import MSO_SHAPE

    # --- Default Data if not provided ---
    if tiers is None:
        tiers = ["Basic", "Portfolio", "Business"]
    if features is None:
        features = [
            {"name": "Customizable website", "values": [True, True, True]},
            {"name": "Unlimited photos and videos upload", "values": [True, True, True]},
            {"name": "Responsive design", "values": [True, True, True]},
            {"name": "Free mobile app to edit", "values": [True, True, True]},
            {"name": "Fully hosted, unlimited traffic", "values": [False, True, True]},
            {"name": "Ads and spam", "values": [True, True, True]},
            {"name": "Share on the go", "values": [False, False, True]},
            {"name": "Add text here", "values": [False, False, True]},
            {"name": "Add text here", "values": [False, False, True]},
        ]

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # --- Color Palette ---
    ACCENT_COLOR = RGBColor(79, 129, 133)
    WHITE_COLOR = RGBColor(255, 255, 255)
    DARK_GRAY_COLOR = RGBColor(64, 64, 64)
    GREEN_CHECK_COLOR = RGBColor(0, 176, 80)
    RED_CROSS_COLOR = RGBColor(255, 0, 0)
    LIGHT_GRAY_BORDER = RGBColor(217, 217, 217)

    # === Slide Title ===
    title_shape = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(12), Inches(0.5))
    title_shape.text_frame.text = title_text
    p = title_shape.text_frame.paragraphs[0]
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = DARK_GRAY_COLOR

    # === Top Info Bar ===
    company_box = slide.shapes.add_textbox(Inches(2.8), Inches(1.2), Inches(2), Inches(0.3))
    company_box.text_frame.text = f"Company Name: {company_name}"
    company_box.text_frame.paragraphs[0].font.size = Pt(10)

    service_box = slide.shapes.add_textbox(Inches(6.5), Inches(1.2), Inches(3), Inches(0.3))
    service_box.text_frame.text = f"Services: {service_name}"
    service_box.text_frame.paragraphs[0].font.size = Pt(10)

    # === Vertical "Features" Bar ===
    features_bar = slide.shapes.add_textbox(Inches(0.5), Inches(2.5), Inches(4), Inches(0.5))
    features_bar.rotation = 270
    features_bar.text_frame.text = "Features"
    features_bar.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    features_bar.text_frame.paragraphs[0].font.color.rgb = WHITE_COLOR
    features_bar.text_frame.paragraphs[0].font.bold = True
    features_bar.text_frame.paragraphs[0].font.size = Pt(18)
    features_bar.fill.solid()
    features_bar.fill.fore_color.rgb = ACCENT_COLOR
    features_bar.line.fill.background()

    # === Feature Name Text Boxes ===
    feature_y_start = Inches(2.5)
    feature_row_height = Inches(0.45)
    for i, feature in enumerate(features):
        y_pos = feature_y_start + (i * feature_row_height)
        tx_box = slide.shapes.add_textbox(Inches(1.2), y_pos, Inches(3.5), feature_row_height)
        tx_box.text_frame.text = feature["name"]
        tx_box.text_frame.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE
        p = tx_box.text_frame.paragraphs[0]
        p.font.size = Pt(12)
        p.font.color.rgb = DARK_GRAY_COLOR
        p.alignment = PP_ALIGN.LEFT
        tx_box.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE

    # === Comparison Table ===
    table_cols = len(tiers)
    table_rows = len(features) + 1
    table_left = Inches(4.8)
    table_top = Inches(2.0)
    table_width = Inches(8)
    table_height = Inches(0.5) + (len(features) * feature_row_height)

    table_shape = slide.shapes.add_table(table_rows, table_cols, table_left, table_top, table_width, table_height)
    table = table_shape.table
    
    # --- Set Column Widths ---
    for i in range(table_cols):
        table.columns[i].width = int(table_width / table_cols)

    # --- Format Table Header ---
    for i, tier_name in enumerate(tiers):
        cell = table.cell(0, i)
        cell.text = tier_name
        cell.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
        cell.text_frame.paragraphs[0].font.bold = True
        cell.text_frame.paragraphs[0].font.size = Pt(16)
        cell.text_frame.paragraphs[0].font.color.rgb = WHITE_COLOR
        cell.fill.solid()
        cell.fill.fore_color.rgb = ACCENT_COLOR
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE

    # --- Populate Table Body ---
    for row_idx, feature in enumerate(features, start=1):
        for col_idx, value in enumerate(feature["values"]):
            cell = table.cell(row_idx, col_idx)
            paragraph = cell.text_frame.paragraphs[0]
            if value:
                paragraph.text = "✓"
                paragraph.font.color.rgb = GREEN_CHECK_COLOR
            else:
                paragraph.text = "✗"
                paragraph.font.color.rgb = RED_CROSS_COLOR
            paragraph.font.name = "Segoe UI Symbol" # A font that reliably renders these symbols
            paragraph.font.size = Pt(24)
            paragraph.font.bold = True
            paragraph.alignment = PP_ALIGN.CENTER
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    
    # --- Apply Borders to all cells ---
    for r in range(table_rows):
        for c in range(table_cols):
            cell = table.cell(r, c)
            for border_part in ['top', 'bottom', 'left', 'right']:
                border = getattr(cell, f'border_{border_part}')
                border.fill.solid()
                border.fill.fore_color.rgb = LIGHT_GRAY_BORDER
                border.width = Pt(1)

    prs.save(output_pptx_path)
    return output_pptx_path

```

#### 3c. Verification Checklist

- [x] Does the code import all required libraries?
- [x] Does it handle the case where an image download fails (fallback)? (N/A for this design)
- [x] Are all color values explicit RGB tuples (not referencing undefined variables)?
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect?
- [x] Would someone looking at the output say "yes, that's the same technique"?