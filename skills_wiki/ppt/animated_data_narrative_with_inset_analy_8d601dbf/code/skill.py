from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_DATA_LABEL_POSITION, XL_LEGEND_POSITION
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_THEME_COLOR

def create_slide(
    output_pptx_path: str,
    title_text: str = "Annual Publications & Country Contributions", # Not used in chart, for file naming
    **kwargs,
) -> str:
    """
    Creates a PPTX slide with an animated data narrative structure.
    
    This function generates a slide with a primary column chart and an inset bar chart,
    styled with varied colors per bar. The final animation steps must be applied manually
    in PowerPoint.

    Returns: path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Data for the Charts ===
    column_chart_data = {
        'categories': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021],
        'values': [3, 6, 2, 12, 14, 24, 26, 29, 47, 70, 71, 17]
    }
    
    bar_chart_data = {
        'categories': ['Saudi Arabia', 'Spain', 'England', 'USA', 'China'],
        'values': [16, 17, 18, 60, 166]
    }

    # === 1. Create and Format the Primary Column Chart ===
    chart_data_col = CategoryChartData()
    chart_data_col.categories = column_chart_data['categories']
    chart_data_col.add_series('Publications', column_chart_data['values'])

    x, y, cx, cy = Inches(1), Inches(1), Inches(11.33), Inches(6)
    graphic_frame_col = slide.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_CLUSTERED, x, y, cx, cy, chart_data_col
    )
    chart_col = graphic_frame_col.chart

    # --- Styling the Column Chart ---
    plot_col = chart_col.plots[0]
    plot_col.vary_by_category = True  # Key step for multi-colored bars
    plot_col.has_data_labels = True
    data_labels_col = plot_col.data_labels
    data_labels_col.position = XL_DATA_LABEL_POSITION.OUTSIDE_END
    data_labels_col.font.size = Pt(12)

    # --- Axis Formatting ---
    category_axis_col = chart_col.category_axis
    category_axis_col.has_title = True
    category_axis_col.axis_title.text_frame.text = "Year"
    category_axis_col.axis_title.text_frame.paragraphs[0].font.size = Pt(16)
    category_axis_col.tick_labels.font.size = Pt(12)

    value_axis_col = chart_col.value_axis
    value_axis_col.has_title = True
    value_axis_col.axis_title.text_frame.text = "Number of publications"
    value_axis_col.axis_title.text_frame.paragraphs[0].font.size = Pt(16)
    value_axis_col.tick_labels.font.size = Pt(12)
    value_axis_col.has_major_gridlines = False

    # --- General Chart Cleanup ---
    chart_col.has_legend = False
    chart_col.has_title = False
    
    # Remove chart border
    chart_col.chart_area.format.line.fill.background()


    # === 2. Create and Format the Inset Bar Chart ===
    chart_data_bar = CategoryChartData()
    chart_data_bar.categories = bar_chart_data['categories']
    chart_data_bar.add_series('Publications', bar_chart_data['values'])

    x, y, cx, cy = Inches(0.5), Inches(0.5), Inches(5), Inches(3.5)
    graphic_frame_bar = slide.shapes.add_chart(
        XL_CHART_TYPE.BAR_CLUSTERED, x, y, cx, cy, chart_data_bar
    )
    chart_bar = graphic_frame_bar.chart

    # --- Styling the Bar Chart ---
    plot_bar = chart_bar.plots[0]
    plot_bar.vary_by_category = True # Key step for multi-colored bars
    plot_bar.has_data_labels = True
    data_labels_bar = plot_bar.data_labels
    data_labels_bar.position = XL_DATA_LABEL_POSITION.OUTSIDE_END
    data_labels_bar.font.size = Pt(14)
    data_labels_bar.font.bold = True

    # --- Axis Formatting for minimalist look ---
    category_axis_bar = chart_bar.category_axis
    category_axis_bar.tick_labels.font.size = Pt(14)
    category_axis_bar.format.line.fill.background() # Remove axis line

    value_axis_bar = chart_bar.value_axis
    value_axis_bar.has_title = True
    value_axis_bar.axis_title.text_frame.text = "Publications"
    value_axis_bar.axis_title.text_frame.paragraphs[0].font.size = Pt(14)
    value_axis_bar.tick_labels.font.size = Pt(12)
    value_axis_bar.format.line.fill.background() # Remove axis line
    value_axis_bar.has_major_gridlines = False
    
    # Set y-axis categories in reverse order to match video (China at bottom)
    category_axis_bar.reverse_order = True

    # --- General Chart Cleanup ---
    chart_bar.has_legend = False
    chart_bar.has_title = False
    chart_bar.chart_area.format.line.fill.background() # Remove chart border
    chart_bar.plot_area.format.fill.background() # Make plot area transparent
    
    
    prs.save(output_pptx_path)
    return output_pptx_path

