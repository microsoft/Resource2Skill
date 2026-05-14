def create_slide(
    output_pptx_path: str,
    title_text: str = "Customers rated cleanliness highest and educational lowest.",
    chart_data: dict = None,
    accent_color: tuple = (29, 112, 184),
    **kwargs,
) -> str:
    """
    Creates a PowerPoint slide with a clean, decluttered, action-titled bar chart.

    Args:
        output_pptx_path: The path to save the generated PPTX file.
        title_text: The main insight or title for the slide.
        chart_data: A dictionary of data for the chart, e.g., {'Category A': 90, 'Category B': 75}.
                    If None, default survey data is used.
        accent_color: An RGB tuple for the chart bars and title.

    Returns:
        The path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.chart.data import ChartData
    from pptx.enum.chart import XL_CHART_TYPE, XL_DATA_LABEL_POSITION
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor

    # Use default data if none is provided
    if chart_data is None:
        chart_data = {
            "Cleanliness": 90,
            "Safety": 90,
            "Welcoming": 88,
            "Accessibility": 88,
            "Value for Cost": 78,
            "Overall Experience": 74,
            "Easy to Navigate": 69,
            "Educational": 67,
        }

    # Sort the data by value, descending.
    # The chart object populates from the bottom up, so to have the largest
    # bar on top, we need to sort the data ascendingly.
    sorted_items = sorted(chart_data.items(), key=lambda item: item[1])
    sorted_categories = [item[0] for item in sorted_items]
    sorted_values = [item[1] / 100.0 for item in sorted_items] # Convert to percentages for chart data

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: Background (White) ===
    # Default is white, no action needed.

    # === Layer 2: Chart ===
    chart_data_obj = ChartData()
    chart_data_obj.categories = sorted_categories
    chart_data_obj.add_series('Survey Data', sorted_values)

    x, y, cx, cy = Inches(1), Inches(1.5), Inches(11.33), Inches(5.5)
    chart = slide.shapes.add_chart(
        XL_CHART_TYPE.BAR_CLUSTERED, x, y, cx, cy, chart_data_obj
    ).chart

    # --- Declutter Chart ---
    chart.has_legend = False
    chart.has_title = False

    # Remove value axis (X-axis for horizontal bar chart)
    value_axis = chart.value_axis
    value_axis.visible = False
    if value_axis.has_major_gridlines:
        value_axis.major_gridlines.format.line.fill.background()

    # Remove category axis line (Y-axis line)
    category_axis = chart.category_axis
    category_axis.format.line.fill.background()

    # --- Style Chart Elements ---
    plot = chart.plots[0]
    plot.gap_width = 30  # Make bars thicker

    # Style bars
    series = chart.series[0]
    fill = series.format.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*accent_color)
    series.format.line.fill.background() # No border on bars

    # Add and style data labels
    plot.has_data_labels = True
    data_labels = plot.data_labels
    data_labels.position = XL_DATA_LABEL_POSITION.INSIDE_END
    data_labels.number_format = '0"%"' # Display as integer percentage
    data_labels.font.size = Pt(16)
    data_labels.font.color.rgb = RGBColor(255, 255, 255)
    data_labels.font.bold = True
    try:
        data_labels.font.name = 'Arial Nova Cond'
    except KeyError:
        data_labels.font.name = 'Arial Narrow'


    # Style category labels (Y-axis)
    category_axis.tick_labels.font.size = Pt(18)
    category_axis.tick_labels.font.bold = True
    category_axis.tick_labels.font.color.rgb = RGBColor(51, 51, 51)
    try:
        category_axis.tick_labels.font.name = 'Arial Nova Cond'
    except KeyError:
        category_axis.tick_labels.font.name = 'Arial Narrow'

    # === Layer 3: Action Title ===
    title_shape = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(11.33), Inches(1.0))
    text_frame = title_shape.text_frame
    p = text_frame.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = RGBColor(*accent_color)
    try:
        p.font.name = 'Arial Nova Cond'
    except KeyError:
        p.font.name = 'Arial Narrow'


    prs.save(output_pptx_path)
    return output_pptx_path
