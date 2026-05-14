# Data Analytics Dashboard Grid

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Data Analytics Dashboard Grid

*   **Core Visual Mechanism**: The defining visual idea is the "Card UI" pattern typical of web-based CRM and analytics dashboards. Data is segmented into uniform, distinct rectangular containers (cards) arranged in a rigid grid. The visual hierarchy prioritizes high-level summary metrics (KPIs) using easily scannable charts like Doughnuts (for part-to-whole ratios) and Horizontal Bars (for rankings).
*   **Why Use This Skill (Rationale)**: This layout reduces cognitive load when presenting dense data. By enclosing distinct metrics within light-bordered cards, the eye is guided through the information in a predictable pattern. Doughnut charts quickly communicate distribution, while horizontal bar charts are excellent for reading long categorical labels (like names or company titles) alongside rankings.
*   **Overall Applicability**: Ideal for business reporting, sales performance reviews, marketing campaign readouts, project status summaries, and any presentation attempting to summarize quantitative data into an executive-level "snapshot."
*   **Value Addition**: Transforms standard slide layouts into a professional, application-like interface. It implies real-time, data-driven insights and brings a modern Software-as-a-Service (SaaS) aesthetic to static PowerPoint presentations.

### 2. Visual Breakdown

*   **Step A: Core Visual Elements**
    *   **Containers**: White rectangular cards with a subtle light gray border `(220, 220, 220, 255)` on a slightly off-white or light gray background `(245, 245, 245, 255)`.
    *   **Chart Types**:
        *   Doughnut charts showing 3-part distributions.
        *   Horizontal bar charts showing "Top 5" rankings.
    *   **Color Logic**:
        *   Categorical Donut Colors: Green `(76, 175, 80, 255)`, Blue `(33, 150, 243, 255)`, Red `(244, 67, 54, 255)`.
        *   Highlight Bar Color: Orange `(255, 152, 0, 255)`.
        *   Text: Dark Charcoal `(50, 50, 50, 255)` for primary titles, medium gray for axes.
    *   **Text Hierarchy**: Panel titles at the top-left or top-center of each card, bold and moderately sized. Axis labels and data points are secondary and smaller.

*   **Step B: Compositional Style**
    *   **Grid Structure**: A clear 3-column layout. The video shows two primary rows of data cards.
    *   **Proportions**: Cards are relatively uniform. The top row (donuts) occupies roughly the top 50% of the slide's active area, and the bottom row (bars) occupies the remaining space. Margins between cards are consistent (gutter space).

*   **Step C: Dynamic Effects & Transitions**
    *   The source material is a scrolling web page, so there are no native slide transitions. In PowerPoint, this static, flat-design layout is best served without complex animations, perhaps using a simple "Fade" transition between slides to mimic changing dashboard tabs.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
| :--- | :--- | :--- |
| **Grid Layout & Cards** | `python-pptx` native | Standard PowerPoint shapes (`RECTANGLE`) are perfect for drawing UI cards and positioning them mathematically. |
| **Doughnut Charts** | `python-pptx` native | Native `XL_CHART_TYPE.DOUGHNUT` allows for data-driven, editable charts directly in the PPTX. We can loop through points to set the specific Green/Blue/Red colors. |
| **Horizontal Bar Charts** | `python-pptx` native | Native `XL_CHART_TYPE.BAR_CLUSTERED` produces horizontal bars. We can override the series fill color to match the orange accent from the video. |

> **Feasibility Assessment**: 95%. The layout, chart types, and color schemes are reproduced using native editable PowerPoint objects. The exact pixel-perfect HTML/CSS rendering (like specific shadow CSS or exact HTML font rendering) varies slightly in PowerPoint, but the overall "Dashboard Card" aesthetic is fully captured and remains fully editable for the user.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "PERFORMANCE DASHBOARD",
    body_text: str = "",
    bg_palette: str = "light",
    accent_color: tuple = (33, 150, 243),
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Data Analytics Dashboard Grid visual effect.
    Returns: path to the saved PPTX file.
    """
    import os
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.dml.color import RGBColor
    from pptx.chart.data import CategoryChartData
    from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
    from pptx.enum.text import PP_ALIGN

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use a blank layout
    blank_slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_slide_layout)

    # === Layer 1: Background ===
    # Subtle off-white background to make white cards pop
    bg = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
    )
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(245, 246, 248) # Light gray/blue tint
    bg.line.fill.background() # No line

    # Header Ribbon
    header = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.8)
    )
    header.fill.solid()
    header.fill.fore_color.rgb = RGBColor(13, 71, 161) # Dark Blue UI header
    header.line.fill.background()
    
    # Title Text
    tx_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.15), Inches(5), Inches(0.5))
    tf = tx_box.text_frame
    p = tf.add_paragraph()
    p.text = title_text
    p.font.size = Pt(24)
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.font.bold = True

    # Color Palette for Charts based on the video
    color_green = RGBColor(76, 175, 80)
    color_blue = RGBColor(33, 150, 243)
    color_red = RGBColor(244, 67, 54)
    color_orange = RGBColor(255, 152, 0)
    
    # Card Border Color
    border_color = RGBColor(220, 220, 220)

    # Grid Configuration
    card_width = Inches(4.0)
    margin_x = Inches(0.4)
    gap_x = Inches(0.26)
    x_positions = [
        margin_x, 
        margin_x + card_width + gap_x, 
        margin_x + (card_width * 2) + (gap_x * 2)
    ]
    
    # --- ROW 1: Doughnut Charts ---
    y_row1 = Inches(1.1)
    height_row1 = Inches(3.2)
    titles_r1 = ["Current Year To Date Snapshot", "Current Quarter To Date Snapshot", "Current Month To Date Snapshot"]
    
    for i, x in enumerate(x_positions):
        # 1. Draw Card Background
        card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y_row1, card_width, height_row1)
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(255, 255, 255)
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
        
        # 2. Add Card Title
        tx_box = slide.shapes.add_textbox(x, y_row1 + Inches(0.1), card_width, Inches(0.4))
        tf = tx_box.text_frame
        p = tf.paragraphs[0]
        p.text = titles_r1[i]
        p.font.size = Pt(14)
        p.font.color.rgb = RGBColor(80, 80, 80)
        p.alignment = PP_ALIGN.CENTER
        
        # 3. Add Doughnut Chart
        chart_data = CategoryChartData()
        chart_data.categories = ['Sales', 'Pipeline', 'Lost']
        # Slight data variations for realism
        data_variations = [(32, 37, 31), (30, 40, 30), (45, 25, 30)]
        chart_data.add_series('Series 1', data_variations[i])
        
        chart_x = x + Inches(0.2)
        chart_y = y_row1 + Inches(0.5)
        chart_w = card_width - Inches(0.4)
        chart_h = height_row1 - Inches(0.6)
        
        chart_shape = slide.shapes.add_chart(
            XL_CHART_TYPE.DOUGHNUT, chart_x, chart_y, chart_w, chart_h, chart_data
        )
        chart = chart_shape.chart
        
        # Chart formatting
        chart.has_legend = True
        chart.legend.position = XL_LEGEND_POSITION.BOTTOM
        chart.legend.font.size = Pt(10)
        
        # Color the points to match the video (Green, Blue, Red)
        series = chart.series[0]
        try:
            points = series.points
            points[0].format.fill.solid()
            points[0].format.fill.fore_color.rgb = color_green
            points[1].format.fill.solid()
            points[1].format.fill.fore_color.rgb = color_blue
            points[2].format.fill.solid()
            points[2].format.fill.fore_color.rgb = color_red
        except Exception:
            pass # Fallback to default colors if points array isn't accessible

    # --- ROW 2: Horizontal Bar Charts ---
    y_row2 = Inches(4.5)
    height_row2 = Inches(2.7)
    titles_r2 = ["Top 5 Monthly Salesmen", "Top 5 Monthly Accounts", "Top 5 Hot Leads"]
    
    for i, x in enumerate(x_positions):
        # 1. Draw Card Background
        card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y_row2, card_width, height_row2)
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(255, 255, 255)
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
        
        # 2. Add Card Title
        tx_box = slide.shapes.add_textbox(x + Inches(0.1), y_row2 + Inches(0.1), card_width - Inches(0.2), Inches(0.4))
        tf = tx_box.text_frame
        p = tf.paragraphs[0]
        p.text = titles_r2[i]
        p.font.size = Pt(14)
        p.font.color.rgb = RGBColor(80, 80, 80)
        
        # 3. Add Horizontal Bar Chart
        chart_data = CategoryChartData()
        chart_data.categories = ['Sample 5', 'Sample 4', 'Sample 3', 'Sample 2', 'Sample 1']
        
        # Simulate decaying bar lengths
        bars_data = [(0.5, 1.2, 1.8, 2.5, 3.0), (0.2, 0.5, 0.8, 1.5, 2.0), (0.1, 0.3, 0.6, 1.2, 1.9)]
        chart_data.add_series('Value', bars_data[i])
        
        chart_x = x + Inches(0.1)
        chart_y = y_row2 + Inches(0.5)
        chart_w = card_width - Inches(0.2)
        chart_h = height_row2 - Inches(0.6)
        
        chart_shape = slide.shapes.add_chart(
            XL_CHART_TYPE.BAR_CLUSTERED, chart_x, chart_y, chart_w, chart_h, chart_data
        )
        chart = chart_shape.chart
        
        # Formatting specific to the video's flat bar charts
        chart.has_legend = False
        chart.value_axis.has_major_gridlines = True
        chart.value_axis.major_gridlines.format.line.color.rgb = RGBColor(230, 230, 230)
        
        # Set all bars to the Orange accent color
        series = chart.series[0]
        series.format.fill.solid()
        series.format.fill.fore_color.rgb = color_orange
        series.gap_width = 150 # Make bars thinner

    prs.save(output_pptx_path)
    return output_pptx_path
```