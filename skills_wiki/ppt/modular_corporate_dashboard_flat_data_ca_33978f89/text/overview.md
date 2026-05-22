# Modular Corporate Dashboard (Flat Data Cards)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Modular Corporate Dashboard (Flat Data Cards)

* **Core Visual Mechanism**: The core visual aesthetic relies on a structured, grid-based "card" layout with a strict and minimalist color palette. It uses clean white or light gray background areas overlaid with white bounding boxes (cards) to modularize information. A single strong accent color (corporate orange) is used surgically to draw attention to primary KPIs, progress indicators, chart data points, and active states, while neutral dark grays/blacks are used for typography.
* **Why Use This Skill (Rationale)**: This design pattern optimizes for cognitive ease. By breaking complex financial, sales, or operational data into distinct geometric "cards," it allows the audience to consume information in bite-sized, organized chunks. The strict adherence to a single accent color prevents visual fatigue and directs the eye immediately to the most important metrics or takeaways.
* **Overall Applicability**: Ideal for Business Reviews (QBRs), financial reports, sales pipeline updates, operational dashboards, and any data-heavy presentation requiring a clean, professional, and authoritative tone.
* **Value Addition**: Transforms a chaotic "data dump" slide into a structured dashboard. It elevates standard bullet points and native charts into a cohesive, software-like UI experience within PowerPoint.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**:
    - Canvas Background: Very light gray/off-white `(248, 248, 248, 255)`
    - Card Background: Pure White `(255, 255, 255, 255)`
    - Primary Accent (Corporate Orange): `(237, 125, 49, 255)`
    - Secondary Accent (Muted Sand/Orange): `(245, 180, 130, 255)`
    - Primary Text (Charcoal): `(64, 64, 64, 255)`
    - Secondary Text/Muted Elements (Medium Gray): `(166, 166, 166, 255)`
  - **Typography**: Clean Sans-Serif (Arial/Calibri style). Clear hierarchy: Slide titles are large and muted; Card headers are small and bold; KPI values are oversized and brightly colored.
  - **Shapes**: Sharp or slightly rounded rectangles. Thin borders `(220, 220, 220)` or very subtle drop shadows to lift cards off the background.

* **Step B: Compositional Style**
  - **Grid Layout**: Slides are divided into horizontal and vertical fractions (e.g., top 1/3 for high-level KPIs, bottom 2/3 for detailed tables/charts).
  - **Whitespace**: Generous padding inside cards (margins) to keep data legible.
  - **Proportions**: Top KPI cards usually occupy 20-25% of the slide height. Detailed content tables occupy ~60%.

* **Step C: Dynamic Effects & Transitions**
  - Flat and static by nature. Animations (if any) would be simple "Fade" or "Wipe" from left to right on the progress bars or charts. Achievable via native PowerPoint transitions, but the strength is in the static layout.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Card Layout & Typography** | `python-pptx` native | Precise control over shape dimensions, placement, and text styling for structural grids. |
| **Card Drop Shadows** | `lxml` XML injection | Native `python-pptx` API lacks shadow support. Direct OOXML injection is required to give cards the "UI Dashboard" floating effect. |
| **Custom KPI Progress Bars** | `python-pptx` native | Layering two rectangles (gray track + orange fill) creates pixel-perfect progress bars. |
| **Stylized Data Tables** | `python-pptx` + native cell formatting | Using the table API to strip default bloated styles and apply the exact solid fills (orange headers, white/gray alternating rows) seen in the tutorial. |

> **Feasibility Assessment**: 95%. The code accurately reproduces the core modular dashboard style, exact color palette, typography hierarchy, UI card shadows, progress bars, and custom-styled tables seen across the slides in the provided deck.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "Sales Review: Current Sales Pipeline",
    bg_palette: str = "corporate", 
    accent_color: tuple = (237, 125, 49),  # Corporate Orange
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Modular Corporate Dashboard visual effect.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.oxml.xmlchemy import OxmlElement
    import copy

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank layout
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)

    # Core Colors
    ACCENT_COLOR = RGBColor(*accent_color)
    BG_COLOR = RGBColor(248, 248, 248)
    CARD_BG = RGBColor(255, 255, 255)
    TEXT_DARK = RGBColor(64, 64, 64)
    TEXT_LIGHT = RGBColor(150, 150, 150)
    BORDER_COLOR = RGBColor(230, 230, 230)

    # --- Helper: Apply Shadow via lxml ---
    def apply_subtle_shadow(shape):
        spPr = shape.element.spPr
        effectLst = OxmlElement('a:effectLst')
        outerShdw = OxmlElement('a:outerShdw')
        outerShdw.set('blurRad', '300000') # 3pt blur
        outerShdw.set('dist', '200000')    # 2pt distance
        outerShdw.set('dir', '5400000')    # 90 degrees (down)
        outerShdw.set('algn', 'tl')
        outerShdw.set('rotWithShape', '0')
        
        srgbClr = OxmlElement('a:srgbClr')
        srgbClr.set('val', '000000')
        alpha = OxmlElement('a:alpha')
        alpha.set('val', '10000') # 10% opacity
        srgbClr.append(alpha)
        
        outerShdw.append(srgbClr)
        effectLst.append(outerShdw)
        spPr.append(effectLst)

    # --- Layer 1: Background ---
    bg_shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
    )
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = BG_COLOR
    bg_shape.line.fill.background()

    # --- Header Area ---
    # Top orange accent line
    top_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(0), Inches(12.333), Inches(0.08))
    top_line.fill.solid()
    top_line.fill.fore_color.rgb = ACCENT_COLOR
    top_line.line.fill.background()

    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(10), Inches(0.8))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = TEXT_DARK
    p.font.name = "Arial"

    # --- Layer 2: KPI Cards (Top Grid) ---
    kpi_data = [
        {"title": "Total Revenue", "val": "$44.2M", "prog": 0.8, "prog_label": "+5.3%"},
        {"title": "EBITDA Margin", "val": "18.5%", "prog": 0.6, "prog_label": "+1.8%"},
        {"title": "Active Partners", "val": "102", "prog": 0.9, "prog_label": "On Track"},
        {"title": "Key Markets", "val": "13", "prog": 0.4, "prog_label": "Needs Review"}
    ]

    card_width = Inches(2.9)
    card_height = Inches(1.6)
    start_x = Inches(0.5)
    start_y = Inches(1.2)
    spacing_x = Inches(0.24)

    for i, data in enumerate(kpi_data):
        x = start_x + i * (card_width + spacing_x)
        
        # Card Background
        card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, start_y, card_width, card_height)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = BORDER_COLOR
        card.line.width = Pt(1)
        apply_subtle_shadow(card)

        # Card Title
        tx_title = slide.shapes.add_textbox(x + Inches(0.1), start_y + Inches(0.1), card_width - Inches(0.2), Inches(0.3))
        p_title = tx_title.text_frame.paragraphs[0]
        p_title.text = data["title"]
        p_title.font.size = Pt(12)
        p_title.font.color.rgb = TEXT_LIGHT
        p_title.font.name = "Arial"

        # KPI Value
        tx_val = slide.shapes.add_textbox(x + Inches(0.1), start_y + Inches(0.4), card_width - Inches(0.2), Inches(0.6))
        p_val = tx_val.text_frame.paragraphs[0]
        p_val.text = data["val"]
        p_val.font.size = Pt(28)
        p_val.font.bold = True
        p_val.font.color.rgb = ACCENT_COLOR
        p_val.font.name = "Arial"

        # Progress Bar Track
        bar_x = x + Inches(0.2)
        bar_y = start_y + Inches(1.15)
        bar_w = Inches(1.8)
        bar_h = Inches(0.08)
        
        track = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, bar_x, bar_y, bar_w, bar_h)
        track.fill.solid()
        track.fill.fore_color.rgb = BORDER_COLOR
        track.line.fill.background()

        # Progress Bar Fill
        fill = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, bar_x, bar_y, bar_w * data["prog"], bar_h)
        fill.fill.solid()
        fill.fill.fore_color.rgb = ACCENT_COLOR
        fill.line.fill.background()

        # Progress Label
        tx_prog = slide.shapes.add_textbox(bar_x + bar_w + Inches(0.05), bar_y - Inches(0.12), Inches(0.8), Inches(0.3))
        p_prog = tx_prog.text_frame.paragraphs[0]
        p_prog.text = data["prog_label"]
        p_prog.font.size = Pt(9)
        p_prog.font.color.rgb = TEXT_DARK
        p_prog.font.name = "Arial"

    # --- Layer 3: Main Content Area (Table Widget) ---
    # A large card containing a styled data table
    table_y = Inches(3.2)
    table_w = Inches(12.333)
    table_h = Inches(3.8)
    
    table_card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), table_y, table_w, table_h)
    table_card.fill.solid()
    table_card.fill.fore_color.rgb = CARD_BG
    table_card.line.color.rgb = BORDER_COLOR
    apply_subtle_shadow(table_card)

    # Table Title
    tx_tbl_title = slide.shapes.add_textbox(Inches(0.7), table_y + Inches(0.2), Inches(5), Inches(0.4))
    p_tbl_title = tx_tbl_title.text_frame.paragraphs[0]
    p_tbl_title.text = "Revenue Gap Analysis & Projections"
    p_tbl_title.font.size = Pt(14)
    p_tbl_title.font.bold = True
    p_tbl_title.font.color.rgb = TEXT_DARK
    p_tbl_title.font.name = "Arial"

    # Add Table
    rows, cols = 6, 6
    tbl_shape = slide.shapes.add_table(rows, cols, Inches(0.7), table_y + Inches(0.7), table_w - Inches(0.4), table_h - Inches(1.0))
    table = tbl_shape.table

    headers = ["Region / Function", "Total Revenue", "Target", "% vs Target", "Expected Revenues", "Actual Target"]
    row_data = [
        ["Overall", "19,500", "20,000", "97.5%", "13,800", "20,000"],
        ["Product Line 1", "4,300", "4,500", "95.5%", "2,300", "4,300"],
        ["Product Line 2", "2,400", "2,400", "100.0%", "4,400", "2,400"],
        ["Product Line 3", "3,800", "4,000", "95.0%", "2,300", "3,800"],
        ["Product Line 4", "4,200", "4,500", "93.3%", "3,000", "4,200"]
    ]

    # Style Table Cells
    for row_idx in range(rows):
        for col_idx in range(cols):
            cell = table.cell(row_idx, col_idx)
            # Remove default margins for cleaner look
            cell.margin_top = Pt(5)
            cell.margin_bottom = Pt(5)
            cell.margin_left = Pt(10)
            cell.margin_right = Pt(10)
            
            # Fill logic
            if row_idx == 0:
                # Header row
                cell.fill.solid()
                cell.fill.fore_color.rgb = ACCENT_COLOR
                text = headers[col_idx]
                font_color = CARD_BG
                is_bold = True
            else:
                # Data rows (alternating)
                cell.fill.solid()
                if row_idx % 2 == 0:
                    cell.fill.fore_color.rgb = RGBColor(245, 245, 245) # Light Gray stripe
                else:
                    cell.fill.fore_color.rgb = CARD_BG
                
                text = row_data[row_idx-1][col_idx]
                font_color = TEXT_DARK
                is_bold = (col_idx == 0) # Bold the first column

            # Insert Text
            tf = cell.text_frame
            tf.clear() # Clear default paragraph
            p = tf.paragraphs[0]
            p.text = text
            p.alignment = PP_ALIGN.CENTER if col_idx > 0 else PP_ALIGN.LEFT
            p.font.name = "Arial"
            p.font.size = Pt(11)
            p.font.color.rgb = font_color
            p.font.bold = is_bold

    prs.save(output_pptx_path)
    return output_pptx_path
```