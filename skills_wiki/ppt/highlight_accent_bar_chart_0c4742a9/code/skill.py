from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_LEGEND_POSITION
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_THEME_COLOR
import os

def create_slide(
    output_pptx_path: str,
    chart_data: list,
    title_text: str = "2016年各品牌手机访问量占比",
    subtitle_text: str = "单位：百分比",
    source_text: str = "*数据来源：国双数据中心",
    base_color: tuple = (176, 196, 222), # Light Steel Blue
    accent_color: tuple = (252, 175, 120), # Light Orange
    highlight_index: int = -1,
    **kwargs
) -> str:
    """
    Creates a PPTX slide with a 'Highlight Accent Bar Chart'.

    Args:
        output_pptx_path (str): The path to save the generated PPTX file.
        chart_data (list): A list of tuples, where each tuple is (category_name, value).
                           Example: [('Brand A', 0.25), ('Brand B', 0.45)]
        title_text (str): The main title of the chart.
        subtitle_text (str): The subtitle (e.g., units).
        source_text (str): The data source footnote.
        base_color (tuple): RGB tuple for the standard bars.
        accent_color (tuple): RGB tuple for the highlighted bar.
        highlight_index (int): The index of the data point to highlight. Defaults to the last item.

    Returns:
        str: The path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide_layout = prs.slide_layouts[6]  # Blank layout
    slide = prs.slides.add_slide(slide_layout)
    
    # --- Chart Data Preparation ---
    chart_data_obj = CategoryChartData()
    chart_data_obj.categories = [item[0] for item in chart_data]
    chart_data_obj.add_series('Series 1', [item[1] for item in chart_data])

    # --- Chart Placement and Creation ---
    x, y, cx, cy = Inches(1.5), Inches(1.5), Inches(10), Inches(5)
    graphic_frame = slide.shapes.add_chart(
        XL_CHART_TYPE.CLUSTERED_COLUMN, x, y, cx, cy, chart_data_obj
    )
    chart = graphic_frame.chart

    # --- Chart Styling ---
    chart.has_legend = False
    
    # Value Axis (Y-axis)
    value_axis = chart.value_axis
    value_axis.has_major_gridlines = True
    value_axis.major_gridlines.format.line.solid()
    value_axis.major_gridlines.format.line.color.rgb = RGBColor(220, 220, 220)
    value_axis.major_gridlines.format.line.width = Pt(1)
    value_axis.tick_labels.font.size = Pt(10)
    value_axis.tick_labels.font.color.rgb = RGBColor(89, 89, 89)
    value_axis.format.line.fill.background() # Hide axis line
    value_axis.number_format = '0"%"' # Format as percentage

    # Category Axis (X-axis)
    category_axis = chart.category_axis
    category_axis.tick_labels.font.size = Pt(11)
    category_axis.tick_labels.font.color.rgb = RGBColor(89, 89, 89)
    category_axis.format.line.fill.background() # Hide axis line

    # --- Series and Point Formatting (The Core Effect) ---
    plot = chart.plots[0]
    plot.has_data_labels = True
    data_labels = plot.data_labels
    data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
    data_labels.font.size = Pt(10)
    data_labels.font.color.rgb = RGBColor(89, 89, 89)
    data_labels.number_format = '0.00"%"'

    series = plot.series[0]
    
    # Set the base color for the entire series first
    series.format.fill.solid()
    series.format.fill.fore_color.rgb = RGBColor(*base_color)

    # Now, override the color for the highlighted point
    if highlight_index < 0:
        highlight_index += len(chart_data)
        
    if 0 <= highlight_index < len(chart_data):
        point_to_highlight = series.points[highlight_index]
        point_to_highlight.format.fill.solid()
        point_to_highlight.format.fill.fore_color.rgb = RGBColor(*accent_color)

    # --- Add Title and other Text Elements ---
    title_shape = slide.shapes.add_textbox(Inches(1.5), Inches(0.5), Inches(10), Inches(0.5))
    title_shape.text_frame.text = title_text
    title_p = title_shape.text_frame.paragraphs[0]
    title_p.font.size = Pt(24)
    title_p.font.bold = True
    title_p.font.color.rgb = RGBColor(89, 89, 89)

    subtitle_shape = slide.shapes.add_textbox(Inches(1.5), Inches(1.0), Inches(10), Inches(0.5))
    subtitle_shape.text_frame.text = subtitle_text
    subtitle_p = subtitle_shape.text_frame.paragraphs[0]
    subtitle_p.font.size = Pt(14)
    subtitle_p.font.color.rgb = RGBColor(128, 128, 128)

    source_shape = slide.shapes.add_textbox(Inches(9), Inches(6.6), Inches(4), Inches(0.5))
    source_shape.text_frame.text = source_text
    source_p = source_shape.text_frame.paragraphs[0]
    source_p.font.size = Pt(10)
    source_p.font.italic = True
    source_p.font.color.rgb = RGBColor(150, 150, 150)

    prs.save(output_pptx_path)
    return output_pptx_path

# Example Usage based on the video tutorial
if __name__ == '__main__':
    video_data = [
        ("联想", 0.066),
        ("OPPO", 0.067),
        ("Vivo", 0.075),
        ("小米", 0.083),
        ("三星", 0.116),
        ("华为", 0.165),
        ("苹果", 0.279),
    ]
    
    output_file = "highlight_accent_chart.pptx"
    create_slide(output_file, chart_data=video_data, highlight_index=-1) # Highlight the last item (Apple)
    
    print(f"Presentation saved to {os.path.abspath(output_file)}")
