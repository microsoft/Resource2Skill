import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_DATA_LABEL_POSITION
from pptx.chart.data import ChartData, CategoryChartData

def create_pizza_dashboard_slide(
    output_pptx_path: str,
    title_text: str = "PIZZA SALES PERFORMANCE",
    **kwargs,
) -> str:
    """
    Creates a PPTX slide reproducing the static visual style of an Excel-based
    Pizza Sales Performance dashboard.

    Note: The interactivity of Excel Slicers and Timelines cannot be reproduced.
    This function generates a static visual representation.

    Returns: path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(16)
    prs.slide_height = Inches(9)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Background and Theme Colors ===
    bg_color = RGBColor(255, 255, 255)
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = bg_color

    header_color = RGBColor(140, 0, 0) # Dark Red
    slicer_bg_color = RGBColor(248, 203, 173) # Light Red/Pink
    slicer_header_color = RGBColor(192, 80, 77) # Medium Red
    
    # Chart colors
    c_red = RGBColor(192, 0, 0)
    c_orange = RGBColor(237, 125, 49)
    c_yellow = RGBColor(255, 192, 0)
    c_green = RGBColor(112, 173, 71)

    # === Layer 1: Header ===
    header_shape = slide.shapes.add_shape(1, Inches(0), Inches(0), prs.slide_width, Inches(1.0))
    header_shape.fill.solid()
    header_shape.fill.fore_color.rgb = header_color
    header_shape.line.fill.background()

    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(10), Inches(0.6))
    title_p = title_box.text_frame.paragraphs[0]
    title_p.text = title_text
    title_p.font.name = 'Century Gothic'
    title_p.font.bold = True
    title_p.font.size = Pt(32)
    title_p.font.color.rgb = RGBColor(255, 255, 255)

    # === Layer 2: KPI Scorecards ===
    kpi_data = {
        "Total Revenue": "$817,860",
        "Total Order": "21,350",
        "Average Order Value (AOV)": "$38.31"
    }
    kpi_width = Inches(3.0)
    kpi_height = Inches(1.0)
    start_left = Inches(3.8)
    for i, (label, value) in enumerate(kpi_data.items()):
        left = start_left + Inches(i * 3.5)
        shape = slide.shapes.add_shape(1, left, Inches(1.2), kpi_width, kpi_height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(255, 255, 255)
        shape.line.color.rgb = RGBColor(200, 200, 200)
        
        # Label
        lbl_box = slide.shapes.add_textbox(left, Inches(1.25), kpi_width, Inches(0.4))
        lbl_p = lbl_box.text_frame.paragraphs[0]
        lbl_p.text = label
        lbl_p.font.name = 'Century Gothic'
        lbl_p.font.size = Pt(12)
        lbl_p.alignment = 1  # Center

        # Value
        val_box = slide.shapes.add_textbox(left, Inches(1.6), kpi_width, Inches(0.5))
        val_p = val_box.text_frame.paragraphs[0]
        val_p.text = value
        val_p.font.name = 'Century Gothic'
        val_p.font.bold = True
        val_p.font.size = Pt(24)
        val_p.alignment = 1  # Center

    # === Layer 3: Slicer Placeholders (Non-functional) ===
    slicer_data = {
        "pizza_category": ["Chicken", "Classic", "Supreme", "Veggie"],
        "pizza_size": ["S", "M", "L", "XL", "XXL"],
        "pizza_name": ["The Barbecue C...", "The Big Meat P...", "The Brie Carre P...", "The Calabrese P..."]
    }
    slicer_top = Inches(2.5)
    for category, items in slicer_data.items():
        slicer_height = Inches(0.5 + len(items) * 0.35)
        header = slide.shapes.add_shape(1, Inches(0.3), slicer_top, Inches(3), Inches(0.4))
        header.fill.solid()
        header.fill.fore_color.rgb = slicer_header_color
        header.line.fill.background()
        
        # Slicer Header Text
        header_text_box = slide.shapes.add_textbox(Inches(0.35), slicer_top, Inches(2.9), Inches(0.4))
        header_p = header_text_box.text_frame.paragraphs[0]
        header_p.text = category.replace("_", " ").title()
        header_p.font.color.rgb = RGBColor(255, 255, 255)
        header_p.font.bold = True
        header_p.font.size = Pt(11)

        # Slicer Items
        for i, item in enumerate(items):
            item_top = slicer_top + Inches(0.4 + i * 0.35)
            item_shape = slide.shapes.add_shape(1, Inches(0.3), item_top, Inches(3), Inches(0.35))
            item_shape.fill.solid()
            item_shape.fill.fore_color.rgb = slicer_bg_color
            item_shape.line.color.rgb = slicer_header_color
            
            item_text_box = slide.shapes.add_textbox(Inches(0.35), item_top - Inches(0.05), Inches(2.9), Inches(0.35))
            item_p = item_text_box.text_frame.paragraphs[0]
            item_p.text = item
            item_p.font.size = Pt(10)
        
        slicer_top += slicer_height + Inches(0.2)

    # === Layer 4: Charts ===

    # --- Chart 1: Quantity by Pizza Category (Pie Chart) ---
    chart_data = CategoryChartData()
    chart_data.categories = ['Chicken', 'Classic', 'Supreme', 'Veggie']
    chart_data.add_series('Quantity', (22, 30, 24, 24))
    
    x, y, cx, cy = Inches(3.8), Inches(2.5), Inches(4.5), Inches(3)
    graphic_frame = slide.shapes.add_chart(XL_CHART_TYPE.PIE, x, y, cx, cy, chart_data)
    chart = graphic_frame.chart
    chart.has_title = True
    chart.chart_title.text_frame.text = "Quantity of Pizza Category"
    chart.plots[0].has_data_labels = True
    data_labels = chart.plots[0].data_labels
    data_labels.show_percentage = True
    data_labels.show_category_name = True
    data_labels.font.size = Pt(11)

    # --- Chart 2: Top 10 Pizza by Quantity (Bar Chart) ---
    chart_data = CategoryChartData()
    chart_data.categories = ['Classic Deluxe', 'Barbecue Chicken', 'Hawaiian', 'Pepperoni', 'Thai Chicken']
    chart_data.add_series('Quantity', (2453, 2432, 2422, 2418, 2371))
    
    x, y, cx, cy = Inches(8.8), Inches(2.5), Inches(6.8), Inches(3)
    graphic_frame = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, x, y, cx, cy, chart_data)
    chart = graphic_frame.chart
    chart.has_title = True
    chart.chart_title.text_frame.text = "Top 10 Pizza by Quantity"
    chart.value_axis.has_major_gridlines = False
    chart.has_legend = False
    
    # --- Chart 3: Revenue Trend per Month (Line Chart) ---
    chart_data = CategoryChartData()
    chart_data.categories = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    chart_data.add_series('Revenue', (69, 65, 70, 68, 71, 68, 72, 68, 64, 64, 70, 64))
    
    x, y, cx, cy = Inches(3.8), Inches(5.8), Inches(5), Inches(3)
    graphic_frame = slide.shapes.add_chart(XL_CHART_TYPE.LINE, x, y, cx, cy, chart_data)
    chart = graphic_frame.chart
    chart.has_title = True
    chart.chart_title.text_frame.text = "Revenue Trend per Month"
    chart.has_legend = False
    plot = chart.plots[0]
    series = plot.series[0]
    series.smooth = False
    line = series.format.line
    line.color.rgb = header_color
    line.width = Pt(2.5)

    # --- Chart 4: Revenue by Pizza Category (Stacked Bar) ---
    chart_data = CategoryChartData()
    chart_data.categories = ['Chicken', 'Classic', 'Supreme', 'Veggie']
    chart_data.add_series('Size L', (94, 66, 94, 104))
    chart_data.add_series('Size M', (60, 66, 47, 67))
    chart_data.add_series('Size S', (41, 47, 32, 22))

    x, y, cx, cy = Inches(9.2), Inches(5.8), Inches(6.4), Inches(3)
    graphic_frame = slide.shapes.add_chart(XL_CHART_TYPE.BAR_STACKED, x, y, cx, cy, chart_data)
    chart = graphic_frame.chart
    chart.has_title = True
    chart.chart_title.text_frame.text = "Revenue by Pizza Category"
    chart.has_legend = True
    chart.legend.position = XL_LEGEND_POSITION.RIGHT
    chart.legend.include_in_layout = False
    
    prs.save(output_pptx_path)
    return output_pptx_path

