# Corporate Split-Pane Data Storytelling

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Corporate Split-Pane Data Storytelling

* **Core Visual Mechanism**: This pattern divides the slide vertically into two distinct zones (typically 60/40). The left pane features a highly stripped-down, focused data visualization (a horizontal bar chart with no axes or gridlines, using direct data labels). The primary subject (e.g., the US market) is highlighted in a bold, dark corporate color, while secondary subjects recede in a lighter tint. The right pane provides qualitative "Key Highlights" using custom-styled, colored square bullets to connect the data directly to actionable insights.

* **Why Use This Skill (Rationale)**: This is the gold standard for management consulting presentations (often called the "McKinsey/BCG style"). By stripping away "chart junk" (X-axis, gridlines, legends) and using direct labels, cognitive load is drastically reduced. The split-pane layout explicitly links *what the data says* with *why it matters* in a single eye-tracking motion from left to right.

* **Overall Applicability**: Ideal for executive summaries, financial reports, market share analysis, and business case pitch decks where qualitative takeaways are just as important as the raw numbers.

* **Value Addition**: Transforms a slide from a mere "data dump" into an "insight delivery mechanism." The strong use of color hierarchy (dark blue vs. light blue) immediately directs the viewer's attention to the most critical data point without them having to search for it.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Typography**: Clean, professional sans-serif (Arial, Calibri, or Helvetica). Strong hierarchy (Large title, medium headers, standard body).
  - **Colors**:
    - Dark Corporate Blue (Primary/Highlight): `(20, 35, 90)`
    - Light Ice Blue (Secondary Data): `(150, 180, 220)`
    - Text Gray (Body): `(80, 80, 80)`
  - **Chart Styling**: Horizontal bar chart. Axes removed. Gridlines removed. Data labels positioned `INSIDE_END` with bold, white text.
  - **Dividers**: 1.5pt thick dark blue horizontal lines separate the overarching title/subtitle from the column content.

* **Step B: Compositional Style**
  - **Grid System**: 2-column layout. Left column (Chart) occupies ~55-60% of the width. Right column (Highlights) occupies ~40% of the width.
  - **Margins**: Generous whitespace around the edges and a clear "gutter" between the left and right columns.

* **Step C: Dynamic Effects & Transitions**
  - This style relies entirely on static clarity rather than animation. It is designed to be printed as a leave-behind or read on a screen.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Layout & Text Hierarchy** | `python-pptx` native | Standard text box and paragraph management is robust and highly reproducible. |
| **Horizontal Separators** | `python-pptx` native shapes | Standard lines are easily configured via `MSO_SHAPE.LINE`. |
| **Data Visualization** | `python-pptx` native charts | Standard bar charts can be highly customized (removing axes, formatting specific data points) using native API properties. |
| **Custom Square Bullets** | Unicode + Text Runs | Instead of complex XML injection for bullet styling, using two text runs per paragraph (one for a colored Unicode square `■`, one for text) allows pixel-perfect color control. |

> **Feasibility Assessment**: 95%. The code reproduces the layout, the exact chart formatting (including the specific color highlighting of the top bar), the typography hierarchy, and the custom colored bullets. The only element omitted is manually placing country flag images next to the chart labels, as chart coordinate mapping is not natively exposed in `python-pptx`.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "The US market is the most significant accounting for over\n30% of total revenue in 2021",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the "Corporate Split-Pane Data Storytelling" visual effect.
    """
    import os
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.chart import XL_CHART_TYPE, XL_DATA_LABEL_POSITION
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.chart.data import CategoryChartData

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank slide layout

    # --- Color Palette ---
    dark_blue = RGBColor(20, 35, 90)
    light_blue = RGBColor(142, 175, 225)
    text_gray = RGBColor(80, 80, 80)
    white = RGBColor(255, 255, 255)

    # --- 1. Slide Main Title ---
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.4), Inches(12.333), Inches(1.0))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.add_paragraph()
    p.text = title_text
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = text_gray

    # --- 2. Column Headers ---
    # Left Header (Chart)
    left_header = slide.shapes.add_textbox(Inches(0.5), Inches(1.8), Inches(7.0), Inches(0.5))
    lh_tf = left_header.text_frame
    lh_p = lh_tf.add_paragraph()
    lh_p.text = "Top 6 Countries by Revenue in $ millions"
    lh_p.font.size = Pt(16)
    lh_p.font.bold = True
    lh_p.font.color.rgb = text_gray
    lh_p.alignment = PP_ALIGN.CENTER

    # Right Header (Highlights)
    right_header = slide.shapes.add_textbox(Inches(8.0), Inches(1.8), Inches(4.833), Inches(0.5))
    rh_tf = right_header.text_frame
    rh_p = rh_tf.add_paragraph()
    rh_p.text = "Key Highlights"
    rh_p.font.size = Pt(16)
    rh_p.font.bold = True
    rh_p.font.color.rgb = text_gray
    rh_p.alignment = PP_ALIGN.CENTER

    # --- 3. Divider Lines ---
    # Left Line
    left_line = slide.shapes.add_shape(MSO_SHAPE.LINE, Inches(0.5), Inches(2.3), Inches(7.5), Inches(2.3))
    left_line.line.color.rgb = dark_blue
    left_line.line.width = Pt(1.5)

    # Right Line
    right_line = slide.shapes.add_shape(MSO_SHAPE.LINE, Inches(8.0), Inches(2.3), Inches(12.833), Inches(2.3))
    right_line.line.color.rgb = dark_blue
    right_line.line.width = Pt(1.5)

    # --- 4. Left Pane: Focused Horizontal Bar Chart ---
    # Data is ordered bottom-to-top so the highest value appears at the top of the bar chart
    categories = ['Brazil', 'Japan', 'Canada', 'United Kingdom', 'Mexico', 'United States']
    values = [5401, 5428, 7358, 7589, 8556, 13010]

    chart_data = CategoryChartData()
    chart_data.categories = categories
    chart_data.add_series('Revenue', values)

    # Position: x, y, width, height
    chart_shape = slide.shapes.add_chart(
        XL_CHART_TYPE.BAR_CLUSTERED, 
        Inches(0.5), Inches(2.5), 
        Inches(7.0), Inches(4.5), 
        chart_data
    )
    chart = chart_shape.chart

    # Strip Chart Junk
    chart.has_legend = False
    
    # Format X-Axis (Value Axis)
    val_axis = chart.value_axis
    val_axis.visible = False
    val_axis.has_major_gridlines = False

    # Format Y-Axis (Category Axis)
    cat_axis = chart.category_axis
    cat_axis.has_major_gridlines = False
    cat_axis.tick_labels.font.size = Pt(14)
    cat_axis.tick_labels.font.color.rgb = text_gray

    # Format Series (Bars, Data Labels, specific point colors)
    series = chart.series[0]
    series.has_data_labels = True
    
    # Set inside end positioning for labels
    try:
        series.data_labels.position = XL_DATA_LABEL_POSITION.INSIDE_END
    except AttributeError:
        pass # Handle potential version differences in python-pptx safely

    for dl in series.data_labels:
        dl.font.size = Pt(12)
        dl.font.bold = True
        dl.font.color.rgb = white

    # Color specific bars (Highlighting the top one)
    # The last point in the series array corresponds to 'United States' because of bottom-to-top rendering
    for idx, point in enumerate(series.points):
        fill = point.format.fill
        fill.solid()
        if idx == len(values) - 1: # The highlighted key subject
            fill.fore_color.rgb = dark_blue
        else: # The secondary subjects
            fill.fore_color.rgb = light_blue

    # --- 5. Right Pane: Key Highlights with Custom Colored Bullets ---
    highlights = [
        "The United States sparkling soft drinks market has seen 12% growth YoY from 2012-2021.",
        "Beverage regulations in the European Union slashed EU growth expectations to less than 1.5% in 2022.",
        "Coca-Cola has solidified its position as market leader in the United States despite intense competition."
    ]

    highlights_box = slide.shapes.add_textbox(Inches(8.0), Inches(2.5), Inches(4.833), Inches(4.0))
    h_tf = highlights_box.text_frame
    h_tf.word_wrap = True

    for text in highlights:
        p = h_tf.add_paragraph()
        p.space_after = Pt(24) # Generous spacing between bullets
        p.line_spacing = 1.2
        
        # We use separate text runs to perfectly color the square bullet differently from the text
        # Run 1: The custom bullet
        bullet_run = p.add_run()
        bullet_run.text = "■  "
        bullet_run.font.size = Pt(12)
        bullet_run.font.color.rgb = dark_blue
        
        # Run 2: The content text
        text_run = p.add_run()
        text_run.text = text
        text_run.font.size = Pt(14)
        text_run.font.color.rgb = text_gray

    # Save presentation
    prs.save(output_pptx_path)
    return output_pptx_path
```