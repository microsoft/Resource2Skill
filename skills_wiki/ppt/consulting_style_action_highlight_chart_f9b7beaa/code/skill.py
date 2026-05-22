def create_slide(
    output_pptx_path: str,
    title_text: str = "Kwanzan Cherry became the best-selling species in 2023, driving overall growth.",
    subtitle_text: str = "Total tree sales by species (Units sold, 2020-2023)",
    highlight_index: int = 3, # Index of the data point to highlight
    accent_color: tuple = (0, 90, 160), # Deep Consulting Blue
    muted_color: tuple = (210, 210, 210), # Light Grey
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the 'Consulting-Style Action Highlight Chart'.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.chart.data import CategoryChartData
    from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION
    from pptx.enum.chart import XL_TICK_MARK

    # 1. Initialize Presentation and Slide
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # 2. Add Action Title (The Takeaway)
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(1.0))
    title_tf = title_box.text_frame
    title_tf.word_wrap = True
    p = title_tf.paragraphs[0]
    p.text = title_text
    p.font.name = "Arial" # Standard clean sans-serif
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0, 0, 0)
    p.alignment = PP_ALIGN.LEFT

    # 3. Add Subtitle / Unit Context
    sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(11.7), Inches(0.5))
    sub_tf = sub_box.text_frame
    p_sub = sub_tf.paragraphs[0]
    p_sub.text = subtitle_text
    p_sub.font.name = "Arial"
    p_sub.font.size = Pt(16)
    p_sub.font.italic = True
    p_sub.font.color.rgb = RGBColor(89, 89, 89)
    p_sub.alignment = PP_ALIGN.LEFT

    # 4. Prepare Data (Mock data representing a timeline or categories)
    chart_data = CategoryChartData()
    chart_data.categories = ['2020', '2021', '2022', '2023']
    # Adding a single series to represent the focal metric (e.g., Kwanzan Cherry sales)
    chart_data.add_series('Kwanzan Cherry Sales', (45, 51, 75, 103))

    # 5. Add Chart to Slide
    x, y, cx, cy = Inches(0.8), Inches(2.3), Inches(11.7), Inches(4.5)
    chart = slide.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_CLUSTERED, x, y, cx, cy, chart_data
    ).chart

    # 6. Apply Minimalist "Consulting" Styling to Chart
    chart.has_legend = False
    
    # Clean up Category Axis (X-axis)
    category_axis = chart.category_axis
    category_axis.format.line.color.rgb = RGBColor(150, 150, 150)
    category_axis.tick_labels.font.size = Pt(14)
    category_axis.tick_labels.font.name = "Arial"
    category_axis.tick_labels.font.color.rgb = RGBColor(89, 89, 89)
    category_axis.major_tick_mark = XL_TICK_MARK.NONE

    # Clean up Value Axis (Y-axis) - Remove lines and rely on data labels
    value_axis = chart.value_axis
    value_axis.has_major_gridlines = False
    value_axis.format.line.fill.background() # Hide axis line
    value_axis.tick_labels.font.size = Pt(12)
    value_axis.tick_labels.font.color.rgb = RGBColor(180, 180, 180) # Very light if visible
    value_axis.major_tick_mark = XL_TICK_MARK.NONE

    # 7. Apply Strategic Highlighting to the Series
    series = chart.series[0]
    series.has_data_labels = True
    
    # Iterate through points to color them individually
    for i, point in enumerate(series.points):
        # Set Data Label Font
        data_label = point.data_label
        data_label.font.size = Pt(16)
        data_label.font.name = "Arial"
        data_label.font.bold = True
        data_label.position = XL_LABEL_POSITION.OUTSIDE_END
        
        # Apply Highlight vs Muted Color
        fill = point.format.fill
        fill.solid()
        if i == highlight_index:
            fill.fore_color.rgb = RGBColor(*accent_color)
            data_label.font.color.rgb = RGBColor(*accent_color)
        else:
            fill.fore_color.rgb = RGBColor(*muted_color)
            data_label.font.color.rgb = RGBColor(120, 120, 120)

    # Save and return
    prs.save(output_pptx_path)
    return output_pptx_path

# Example execution:
# create_slide("consulting_highlight_chart.pptx")
