import io
import math
import numpy as np
import matplotlib.pyplot as plt
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.drawing.line import LineFormat
from pptx.enum.chart import (
    XL_CHART_TYPE,
    XL_LEGEND_POSITION,
    XL_DATA_LABEL_POSITION,
    XL_TICK_MARK,
)
from pptx.enum.dml import MSO_THEME_COLOR, MSO_LINE_DASH_STYLE
from pptx.util import Inches, Pt, Emu


def create_gauge_chart(value, max_value=100, title=""):
    """
    Generates a gauge chart image using Matplotlib.
    The image is returned as a BytesIO object.
    """
    # Colors for the gauge arc
    colors = ["#00B0F0", "#92D050", "#FFC000", "#FF0000"] # Blue, Green, Yellow, Red
    values = [25, 25, 25, 25] # Four equal segments
    
    fig, ax = plt.subplots(figsize=(4, 2), subplot_kw={'projection': 'polar'})
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.spines['polar'].set_visible(False)
    ax.set_theta_zero_location('W')
    ax.set_theta_direction(-1)
    
    # Create the background arc
    for i in range(len(values)):
        ax.barh(1, np.deg2rad(sum(values[:i+1])*180/sum(values)), 
                left=np.deg2rad(sum(values[:i])*180/sum(values)), 
                color=colors[i], height=0.5, alpha=0.7)

    # Invisible bottom half
    ax.barh(1, np.deg2rad(180), left=np.deg2rad(180), color='white', height=0.5, alpha=0)
    
    # Needle
    angle = (1 - (value / max_value)) * 180
    ax.arrow(np.deg2rad(angle), 0, 0, 1, 
             width=0.02, head_width=0.0, head_length=0, 
             fc='white', ec='white', zorder=10)

    # Center circle
    ax.add_patch(plt.Circle((0, 0), 0.1, color='white', zorder=11))
    
    ax.set_rmax(1.2)
    ax.grid(False)
    
    # Render to a buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', transparent=True, bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    buf.seek(0)
    return buf


def create_dashboard_slide(
    output_pptx_path: str,
    accent_color_1: tuple = (0, 176, 240),  # Blue
    accent_color_2: tuple = (255, 192, 0),  # Orange/Gold
    **kwargs,
) -> str:
    """
    Creates a PPTX file with a single slide reproducing the Project Management Dashboard.

    Returns: the path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(16)
    prs.slide_height = Inches(9)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # --- Slide Background ---
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = RGBColor(45, 48, 51)
    
    # Helper to add panel backgrounds
    def add_panel(left, top, width, height):
        panel = slide.shapes.add_shape(1, left, top, width, height)
        panel.fill.solid()
        panel.fill.fore_color.rgb = RGBColor(56, 61, 65)
        panel.line.fill.background()
        return panel

    # --- Layout Panels ---
    panel_kpi1 = add_panel(Inches(0.5), Inches(0.5), Inches(2.5), Inches(1.5))
    panel_kpi2 = add_panel(Inches(0.5), Inches(2.25), Inches(2.5), Inches(1.5))
    panel_budget = add_panel(Inches(3.25), Inches(0.5), Inches(3.5), Inches(3.25))
    panel_workload = add_panel(Inches(7.0), Inches(0.5), Inches(4.25), Inches(3.25))
    panel_satisfaction = add_panel(Inches(11.5), Inches(0.5), Inches(4.0), Inches(3.25))
    panel_gantt = add_panel(Inches(0.5), Inches(4.0), Inches(15.0), Inches(4.5))
    
    # --- KPI Cards ---
    def add_kpi(panel_left, panel_top, panel_width, title, value):
        # Title
        tb_title = slide.shapes.add_textbox(panel_left, panel_top + Inches(0.2), panel_width, Inches(0.5))
        p_title = tb_title.text_frame.paragraphs[0]
        p_title.text = title
        p_title.font.color.rgb = RGBColor(240, 240, 240)
        p_title.font.size = Pt(14)
        p_title.font.bold = True
        
        # Value
        tb_val = slide.shapes.add_textbox(panel_left, panel_top + Inches(0.5), panel_width, Inches(1.0))
        p_val = tb_val.text_frame.paragraphs[0]
        p_val.text = str(value)
        p_val.font.color.rgb = RGBColor(0, 176, 240)
        p_val.font.size = Pt(44)
        p_val.font.bold = True

    add_kpi(Inches(0.5), Inches(0.5), Inches(2.5), "總專案數", "10")
    add_kpi(Inches(0.5), Inches(2.25), Inches(2.5), "已完成數", "4")
    
    # --- Chart 1: Budget Donut Chart ---
    chart_data = CategoryChartData()
    chart_data.categories = ['已支出預算', '剩餘預算']
    chart_data.add_series('Budget', (71, 29))
    
    chart = slide.shapes.add_chart(
        XL_CHART_TYPE.DOUGHNUT, Inches(3.5), Inches(0.75), Inches(3.0), Inches(2.75), chart_data
    ).chart
    
    chart.has_legend = False
    chart.plot_area.format.fill.background()
    chart.chart_title.text_frame.text = '已支出預算'
    chart.chart_title.text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
    
    plot = chart.plots[0]
    plot.has_data_labels = True
    plot.data_labels.font.color.rgb = RGBColor(255, 255, 255)
    plot.data_labels.number_format = '0"%"'
    
    point = plot.series[0].points[0]
    point.format.fill.solid()
    point.format.fill.fore_color.rgb = RGBColor(*accent_color_1)
    
    point = plot.series[0].points[1]
    point.format.fill.solid()
    point.format.fill.fore_color.rgb = RGBColor(89, 89, 89)

    # --- Chart 2: Workload Bar Chart ---
    chart_data = CategoryChartData()
    chart_data.categories = ['小玉', '小明', '小強', '小美', '阿杰']
    chart_data.add_series('已完成', (10, 13, 8, 5, 12))
    chart_data.add_series('總天數', (3, 5, 6, 4, 4)) # Remaining days
    
    chart = slide.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_STACKED, Inches(7.25), Inches(0.75), Inches(3.75), Inches(2.75), chart_data
    ).chart

    chart.has_legend = True
    chart.legend.position = XL_LEGEND_POSITION.TOP
    chart.legend.font.color.rgb = RGBColor(255, 255, 255)
    chart.chart_title.text_frame.text = "個人工作量"
    chart.chart_title.text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
    
    chart.value_axis.has_major_gridlines = False
    chart.value_axis.visible = False
    
    chart.category_axis.format.font.color.rgb = RGBColor(255, 255, 255)
    chart.category_axis.format.line.fill.background()
    
    plot = chart.plots[0]
    plot.series_overlap = 100
    plot.gap_width = 150
    plot.has_data_labels = True
    plot.data_labels.position = XL_DATA_LABEL_POSITION.OUTSIDE_END
    plot.data_labels.font.color.rgb = RGBColor(255, 255, 255)

    # Style completed series
    plot.series[0].format.fill.solid()
    plot.series[0].format.fill.fore_color.rgb = RGBColor(*accent_color_1)
    
    # Style total series (make it an outline)
    plot.series[1].format.fill.background()
    line = plot.series[1].format.line
    line.color.rgb = RGBColor(150, 150, 150)
    line.width = Pt(1.5)
    
    # --- Chart 3: Satisfaction Gauge ---
    gauge_image_stream = create_gauge_chart(88)
    slide.shapes.add_picture(gauge_image_stream, Inches(11.75), Inches(1.25), width=Inches(3.5))
    tb_sat_title = slide.shapes.add_textbox(Inches(11.5), Inches(0.75), Inches(4.0), Inches(0.5))
    tb_sat_title.text_frame.paragraphs[0].text = "客戶滿意度"
    tb_sat_title.text_frame.paragraphs[0].font.color.rgb = RGBColor(255,255,255)

    # --- Chart 4: Gantt Chart ---
    chart_data = CategoryChartData()
    chart_data.categories = ['專案 Z', '專案 Y', '專案 X', '專案 G', '專案 F', '專案 E', '專案 D', '專案 C', '專案 B', '專案 A']
    
    start_dates_as_num = [44399, 44404, 44403, 44396, 44398, 44388, 44385, 44384, 44383, 44378]
    durations = [4, 5, 7, 9, 5, 12, 6, 9, 8, 5]

    chart_data.add_series('Start Date', start_dates_as_num)
    chart_data.add_series('Duration', durations)
    
    chart = slide.shapes.add_chart(
        XL_CHART_TYPE.BAR_STACKED, Inches(0.75), Inches(4.25), Inches(14.5), Inches(4.0), chart_data
    ).chart

    chart.has_legend = False
    chart.plot_area.format.fill.background()
    chart.has_title = False
    
    # Style axes
    category_axis = chart.category_axis
    category_axis.format.font.color.rgb = RGBColor(255, 255, 255)
    category_axis.format.line.fill.background()
    
    value_axis = chart.value_axis
    value_axis.has_major_gridlines = True
    value_axis.major_gridlines.format.line.color.rgb = RGBColor(89, 89, 89)
    value_axis.major_gridlines.format.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    value_axis.format.font.color.rgb = RGBColor(255, 255, 255)
    value_axis.format.line.fill.background()
    value_axis.minimum_scale = float(min(start_dates_as_num))
    value_axis.number_format = 'm/d' # Date format
    
    # Make the 'Start Date' series invisible
    plot = chart.plots[0]
    plot.series[0].format.fill.background()
    
    # Style the 'Duration' series
    plot.series[1].format.fill.solid()
    plot.series[1].format.fill.fore_color.rgb = RGBColor(*accent_color_2)
    
    prs.save(output_pptx_path)
    return output_pptx_path

