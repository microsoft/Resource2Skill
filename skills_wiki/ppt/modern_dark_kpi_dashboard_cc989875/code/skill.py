import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.chart.data import ChartData, CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_DATA_LABEL_POSITION
from pptx.dml.line import LineFormat
from pptx.enum.dml import MSO_LINE, MSO_THEME_COLOR

def create_hse_dashboard(output_pptx_path: str, report_date: str = "June 11, 2020"):
    """
    Creates a professional HSE (Health, Safety, and Environment) monthly dashboard
    slide in PowerPoint, populated with sample data.

    Args:
        output_pptx_path (str): The path to save the generated .pptx file.
        report_date (str): The date to display on the dashboard.

    Returns:
        str: The path to the saved .pptx file.
    """
    prs = Presentation()
    prs.slide_width = Inches(16)
    prs.slide_height = Inches(9)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # --- Color Palette ---
    COLOR_BG = RGBColor(23, 35, 56)
    COLOR_PANEL = RGBColor(36, 55, 88)
    COLOR_HEADER = RGBColor(255, 102, 0)
    COLOR_OUTLINE = RGBColor(238, 38, 103)
    COLOR_TEXT = RGBColor(255, 255, 255)
    COLOR_KPI = RGBColor(244, 142, 60)
    COLOR_GREEN = RGBColor(119, 218, 102)
    COLOR_RED = RGBColor(255, 0, 102)
    
    # --- Background and Header ---
    background = slide.background
    background.fill.solid()
    background.fill.fore_color.rgb = COLOR_BG

    header = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.8))
    header.fill.solid()
    header.fill.fore_color.rgb = COLOR_HEADER
    header.line.fill.background()

    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.1), Inches(15), Inches(0.6))
    p = title_box.text_frame.paragraphs[0]
    p.text = "HSE Monthly Dashboard"
    p.font.name = 'Oswald'; p.font.size = Pt(40); p.font.bold = True; p.font.color.rgb = COLOR_TEXT
    p.alignment = PP_ALIGN.CENTER

    # --- Panel Helper Function ---
    def add_panel(left, top, width, height):
        panel = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        panel.shadow.inherit = False
        panel.fill.solid()
        panel.fill.fore_color.rgb = COLOR_PANEL
        panel.line.color.rgb = COLOR_OUTLINE
        panel.line.width = Pt(1.5)
        return panel

    def add_title(left, top, width, text):
        title_box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(0.4))
        p = title_box.text_frame.paragraphs[0]
        p.text = text
        p.font.name = 'Oswald'; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = COLOR_TEXT
    
    def add_kpi(left, top, width, text):
        kpi_box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(0.4))
        p = kpi_box.text_frame.paragraphs[0]
        p.text = text
        p.font.name = 'Oswald'; p.font.size = Pt(24); p.font.bold = True; p.font.color.rgb = COLOR_KPI
        p.alignment = PP_ALIGN.RIGHT

    # --- Build Dashboard Layout ---
    # Col 1
    add_panel(0.5, 1.0, 4.8, 2.5) # Total Manpower
    add_panel(0.5, 5.9, 4.8, 2.5) # Safety Observations
    # Col 2 (Top)
    add_panel(5.6, 1.0, 4.8, 2.5) # Total Manhours
    # Col 2 (Middle)
    add_panel(0.5, 3.8, 9.9, 1.8) # Unsafe Acts/Conditions
    # Col 2 (Bottom)
    add_panel(5.6, 5.9, 4.8, 2.5) # Training Hours
    # Col 3
    add_panel(10.7, 1.0, 4.8, 2.5) # LTIF
    add_panel(10.7, 3.8, 4.8, 4.6) # Severity

    # --- Add Titles, Icons & KPIs ---
    add_title(1.0, 1.05, 3.0, "Total Manpower")
    add_kpi(3.8, 1.05, 1.2, "730")
    add_title(6.1, 1.05, 3.0, "Total Manhours")
    add_kpi(8.9, 1.05, 1.2, "234000")
    add_title(11.2, 1.05, 4.0, "Lost Time Injuries Frequency (LTIF)")
    add_title(1.0, 3.85, 4.0, "Unsafe Acts/Conditions")
    add_kpi(8.9, 3.85, 1.2, "445")
    add_title(1.0, 5.95, 4.0, "Safety Observations")
    add_kpi(6.3, 5.95, 1.2, "415")
    add_title(8.6, 5.95, 2.0, "Training Hours")
    add_kpi(9.6, 5.95, 1.0, "927")
    add_title(11.2, 3.85, 4.0, "Severity (S)")

    # Date
    date_panel = add_panel(0.5, 0.2, 2.0, 0.5)
    date_panel.fill.solid(); date_panel.fill.fore_color.rgb = COLOR_PANEL
    date_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.25), Inches(1.8), Inches(0.4))
    p = date_box.text_frame.paragraphs[0]; p.text = f"Date: {report_date}"; p.font.name='Oswald'; p.font.color.rgb = COLOR_TEXT
    
    # --- Add Charts ---

    # Manpower Bar Chart (Horizontal)
    chart_data = CategoryChartData()
    chart_data.categories = ['Company A', 'Company B', 'Company C']
    chart_data.add_series('', (100, 400, 230))
    chart = slide.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Inches(0.7), Inches(1.9), Inches(4.4), Inches(1.5), chart_data).chart
    chart.has_legend = False; chart.value_axis.visible = False; chart.chart_area.format.fill.background(); chart.plot_area.format.fill.background()
    chart.category_axis.tick_labels.font.color.rgb = COLOR_TEXT
    chart.plots[0].data_labels.show_value = True
    chart.plots[0].data_labels.font.color.rgb = COLOR_TEXT
    points = chart.series[0].points
    points[0].format.fill.solid(); points[0].format.fill.fore_color.rgb = RGBColor(204, 0, 204)
    points[1].format.fill.solid(); points[1].format.fill.fore_color.rgb = RGBColor(255, 0, 102)
    points[2].format.fill.solid(); points[2].format.fill.fore_color.rgb = RGBColor(244, 142, 60)

    # Manhours Area Chart
    chart_data = CategoryChartData()
    chart_data.categories = ['Company A', 'Company B', 'Company C']
    chart_data.add_series('', (45000, 120000, 69000))
    chart = slide.shapes.add_chart(XL_CHART_TYPE.AREA, Inches(5.8), Inches(1.6), Inches(4.4), Inches(1.8), chart_data).chart
    chart.has_legend = False; chart.value_axis.major_gridlines.format.line.fill.background(); chart.chart_area.format.fill.background(); chart.plot_area.format.fill.background()
    chart.value_axis.tick_labels.font.color.rgb = COLOR_TEXT; chart.category_axis.tick_labels.font.color.rgb = COLOR_TEXT
    chart.plots[0].data_labels.show_value = True; chart.plots[0].data_labels.position = XL_DATA_LABEL_POSITION.ABOVE; chart.plots[0].data_labels.font.color.rgb = COLOR_TEXT

    # Unsafe Acts - Positive/Negative Gauges
    p = slide.shapes.add_textbox(Inches(1.2), Inches(4.5), Inches(1.5), Inches(0.4)).text_frame.paragraphs[0]; p.text="Positive"; p.font.name='Oswald'; p.font.color.rgb = COLOR_TEXT; p.alignment=PP_ALIGN.CENTER
    chart_data = ChartData(); chart_data.add_series('', (150, 445-150))
    chart = slide.shapes.add_chart(XL_CHART_TYPE.DOUGHNUT_EXPLODED, Inches(1.3), Inches(4.7), Inches(1.2), Inches(1.2), chart_data).chart
    chart.has_legend = False; chart.chart_area.format.fill.background(); chart.plots[0].vary_by_categories = False; chart.plots[0].first_slice_angle = 270
    chart.series[0].points[0].format.fill.solid(); chart.series[0].points[0].format.fill.fore_color.rgb = COLOR_GREEN
    chart.series[0].points[1].format.fill.solid(); chart.series[0].points[1].format.fill.fore_color.rgb = RGBColor(60, 60, 60)
    p = slide.shapes.add_textbox(Inches(1.3), Inches(4.9), Inches(1.2), Inches(0.8)).text_frame.paragraphs[0]; p.text="150"; p.font.size=Pt(18);p.font.bold=True;p.font.color.rgb=COLOR_TEXT;p.alignment=PP_ALIGN.CENTER
    
    p = slide.shapes.add_textbox(Inches(7.7), Inches(4.5), Inches(1.5), Inches(0.4)).text_frame.paragraphs[0]; p.text="Negative"; p.font.name='Oswald'; p.font.color.rgb = COLOR_TEXT; p.alignment=PP_ALIGN.CENTER
    chart_data = ChartData(); chart_data.add_series('', (245, 445-245))
    chart = slide.shapes.add_chart(XL_CHART_TYPE.DOUGHNUT_EXPLODED, Inches(7.8), Inches(4.7), Inches(1.2), Inches(1.2), chart_data).chart
    chart.has_legend = False; chart.chart_area.format.fill.background(); chart.plots[0].vary_by_categories = False; chart.plots[0].first_slice_angle = 270
    chart.series[0].points[0].format.fill.solid(); chart.series[0].points[0].format.fill.fore_color.rgb = COLOR_RED
    chart.series[0].points[1].format.fill.solid(); chart.series[0].points[1].format.fill.fore_color.rgb = RGBColor(60, 60, 60)
    p = slide.shapes.add_textbox(Inches(7.8), Inches(4.9), Inches(1.2), Inches(0.8)).text_frame.paragraphs[0]; p.text="245"; p.font.size=Pt(18);p.font.bold=True;p.font.color.rgb=COLOR_TEXT;p.alignment=PP_ALIGN.CENTER

    # Safety Observations Chart
    chart_data = CategoryChartData()
    chart_data.categories = ['Work permit', 'Traffic', 'Scaffold', 'PPE', 'Power Tools', 'Manual handling', 'Lifting', 'Driving']
    chart_data.add_series('', (20, 40, 15, 90, 41, 7, 12, 13))
    chart = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.7), Inches(6.5), Inches(7.0), Inches(1.8), chart_data).chart
    chart.has_legend = False; chart.chart_area.format.fill.background(); chart.plot_area.format.fill.background()
    chart.value_axis.tick_labels.font.color.rgb = COLOR_TEXT
    chart.category_axis.tick_labels.font.color.rgb = COLOR_TEXT; chart.category_axis.tick_labels.font.size=Pt(8)
    chart.plots[0].data_labels.show_value = True; chart.plots[0].data_labels.font.color.rgb = COLOR_TEXT
    chart.value_axis.major_gridlines.format.line.fill.background()
    
    # Training Hours Bar Chart
    chart_data = CategoryChartData()
    chart_data.categories = ['Working At height', 'Work Permit', 'Confined Space', 'Lifting', 'Excavation', 'Welding and Cutting', 'Scaffolding']
    chart_data.add_series('', (140, 230, 110, 88, 90, 170, 99))
    chart = slide.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Inches(8.3), Inches(6.5), Inches(4.4), Inches(1.8), chart_data).chart
    chart.has_legend = False; chart.value_axis.visible = False; chart.chart_area.format.fill.background(); chart.plot_area.format.fill.background()
    chart.category_axis.tick_labels.font.color.rgb = COLOR_TEXT; chart.category_axis.tick_labels.font.size=Pt(8)
    chart.plots[0].data_labels.show_value = True; chart.plots[0].data_labels.font.color.rgb = COLOR_TEXT

    # LTIF Line Chart
    chart_data = CategoryChartData()
    chart_data.categories = ['2017', '2018', '2019', '2020']
    chart_data.add_series('', (0.2, 0.1, 0.3, 0.1))
    chart = slide.shapes.add_chart(XL_CHART_TYPE.LINE_MARKERS, Inches(10.9), Inches(1.6), Inches(4.4), Inches(1.8), chart_data).chart
    chart.has_legend = False; chart.value_axis.major_gridlines.format.line.fill.background(); chart.chart_area.format.fill.background(); chart.plot_area.format.fill.background()
    chart.value_axis.tick_labels.font.color.rgb = COLOR_TEXT; chart.category_axis.tick_labels.font.color.rgb = COLOR_TEXT
    chart.plots[0].data_labels.show_value = True; chart.plots[0].data_labels.font.color.rgb = COLOR_TEXT
    chart.series[0].format.line.color.rgb = RGBColor(255, 0, 102); chart.series[0].format.line.width = Pt(2.5)

    # Severity Line Chart
    chart_data = CategoryChartData()
    chart_data.categories = ['2017', '2018', '2019', '2020']
    chart_data.add_series('', (4, 2.5, 3.5, 2))
    chart = slide.shapes.add_chart(XL_CHART_TYPE.LINE_MARKERS_SMOOTHED, Inches(10.9), Inches(5.1), Inches(4.4), Inches(3.2), chart_data).chart
    chart.has_legend = False; chart.value_axis.major_gridlines.format.line.fill.background(); chart.chart_area.format.fill.background(); chart.plot_area.format.fill.background()
    chart.value_axis.tick_labels.font.color.rgb = COLOR_TEXT; chart.category_axis.tick_labels.font.color.rgb = COLOR_TEXT
    chart.plots[0].data_labels.show_value = True; chart.plots[0].data_labels.font.color.rgb = COLOR_TEXT
    chart.series[0].format.line.color.rgb = RGBColor(255, 20, 147); chart.series[0].format.line.width = Pt(2.5)
    
    prs.save(output_pptx_path)
    return output_pptx_path

# Example usage:
# if __name__ == '__main__':
#     file_path = "HSE_Dashboard.pptx"
#     create_hse_dashboard(file_path)
#     print(f"Dashboard saved to {file_path}")

