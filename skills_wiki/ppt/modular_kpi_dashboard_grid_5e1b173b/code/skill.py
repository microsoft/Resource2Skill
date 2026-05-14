import collections.abc
from pptx import Presentation
from pptx.chart.data import ChartData, XyChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_THEME_COLOR

def create_slide(
    output_pptx_path: str,
    title_text: str = "BUSINESS PERFORMANCE DASHBOARD",
    kpi_data: dict = None,
    **kwargs,
) -> str:
    """
    Creates a PPTX slide with a modular KPI dashboard grid.

    Args:
        output_pptx_path: The path to save the generated PPTX file.
        title_text: The main title for the dashboard slide.
        kpi_data: A dictionary containing data for the KPI cards. 
                  If None, default sample data is used.

    Returns:
        The path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # --- Default Data ---
    if kpi_data is None:
        kpi_data = {
            "SALES GROWTH": {
                "type": "bar",
                "icon": "📈", # Unicode for chart increasing
                "categories": ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                "series": {
                    "Sales": [4500, 7000, 7200, 8500, 10200, 13500]
                }
            },
            "PRODUCT RANKING": {
                "type": "line",
                "icon": "⭐", # Unicode for star
                "categories": ['2021', '2022', '2023', '2024'],
                "series": {
                    "Product 1": [24000, 26000, 29000, 21000],
                    "Product 2": [18000, 22000, 27000, 31000],
                    "Product 3": [6000, 12000, 21000, 35000]
                }
            }
        }
    
    # --- Color Palette ---
    BG_COLOR = RGBColor(76, 58, 90) # Dark Purple
    TEXT_COLOR = RGBColor(255, 255, 255)
    CHART_LINE_COLOR = RGBColor(180, 180, 180)
    ACCENT_COLOR_1 = RGBColor(255, 215, 0) # Yellow
    ACCENT_COLOR_2 = RGBColor(0, 191, 255) # Cyan
    ACCENT_COLOR_3 = RGBColor(255, 105, 180) # Pink

    accent_colors = [ACCENT_COLOR_1, ACCENT_COLOR_2, ACCENT_COLOR_3]

    # === Layer 1: Background ===
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = BG_COLOR

    # === Layer 2: Main Title ===
    title_shape = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(12.33), Inches(0.75))
    title_tf = title_shape.text_frame
    p = title_tf.paragraphs[0]
    p.text = title_text
    p.font.name = 'Segoe UI Black'
    p.font.size = Pt(32)
    p.font.color.rgb = TEXT_COLOR

    # === Layer 3: KPI Cards ===
    card_positions = [
        {"left": Inches(0.5), "top": Inches(1.2), "width": Inches(6), "height": Inches(5.8)},
        {"left": Inches(6.83), "top": Inches(1.2), "width": Inches(6), "height": Inches(5.8)},
    ]

    for i, (kpi_title, data) in enumerate(kpi_data.items()):
        if i >= len(card_positions): break
        pos = card_positions[i]
        
        # --- Card Header ---
        header_box = slide.shapes.add_textbox(pos['left'], pos['top'], pos['width'], Inches(0.5))
        header_tf = header_box.text_frame
        p = header_tf.paragraphs[0]
        p.text = f"{data.get('icon', '')}  {kpi_title}"
        p.font.name = 'Segoe UI Semibold'
        p.font.size = Pt(18)
        p.font.color.rgb = TEXT_COLOR
        
        # --- Chart Creation ---
        chart_left = pos['left']
        chart_top = pos['top'] + Inches(0.6)
        chart_width = pos['width']
        chart_height = pos['height'] - Inches(0.6)

        if data['type'] == 'bar':
            chart_data = ChartData()
            chart_data.categories = data['categories']
            for series_name, values in data['series'].items():
                chart_data.add_series(series_name, values)
            
            x, y, cx, cy = chart_left, chart_top, chart_width, chart_height
            graphic_frame = slide.shapes.add_chart(
                XL_CHART_TYPE.COLUMN_CLUSTERED, x, y, cx, cy, chart_data
            )
            chart = graphic_frame.chart
            chart.has_legend = True
            chart.legend.position = XL_LEGEND_POSITION.BOTTOM
            chart.legend.include_in_layout = False
            chart.value_axis.has_major_gridlines = True

            # Style the chart
            plot = chart.plots[0]
            plot.has_data_labels = False
            
            # Bar color
            point = plot.series[0].points[0]
            fill = point.format.fill
            fill.solid()
            fill.fore_color.rgb = ACCENT_COLOR_1

        elif data['type'] == 'line':
            chart_data = XyChartData()
            
            for j, (series_name, values) in enumerate(data['series'].items()):
                series = chart_data.add_series(series_name)
                for k, cat in enumerate(data['categories']):
                    series.add_data_point(k+1, values[k]) # Use numeric categories for XY

            x, y, cx, cy = chart_left, chart_top, chart_width, chart_height
            graphic_frame = slide.shapes.add_chart(
                XL_CHART_TYPE.XY_SCATTER_LINES, x, y, cx, cy, chart_data
            )
            chart = graphic_frame.chart
            chart.has_legend = True
            chart.legend.position = XL_LEGEND_POSITION.BOTTOM
            chart.legend.include_in_layout = False
            
            # Style line colors
            for s_idx, series in enumerate(chart.series):
                line = series.format.line
                line.color.rgb = accent_colors[s_idx % len(accent_colors)]
                line.width = Pt(2.5)
            
            # Manually set category axis labels for XY chart
            category_axis = chart.category_axis
            category_axis.tick_labels.font.size = Pt(10)
            category_axis.tick_labels.font.color.rgb = TEXT_COLOR
            # This is a limitation workaround; python-pptx doesn't directly support text labels for XY axes.
            # Manual labeling in PPTX would be required for full effect.

        # --- General Chart Styling ---
        chart.chart_title.text_frame.text = "" # Remove chart title, we have a card title
        
        # Value Axis Style
        value_axis = chart.value_axis
        value_axis.tick_labels.font.color.rgb = TEXT_COLOR
        value_axis.format.line.color.rgb = CHART_LINE_COLOR
        value_axis.major_gridlines.format.line.color.rgb = CHART_LINE_COLOR
        
        # Category Axis Style
        category_axis = chart.category_axis
        category_axis.tick_labels.font.color.rgb = TEXT_COLOR
        category_axis.format.line.color.rgb = CHART_LINE_COLOR

        # Legend Style
        if chart.has_legend:
            chart.legend.font.color.rgb = TEXT_COLOR

    prs.save(output_pptx_path)
    return output_pptx_path

