import pandas as pd
from pptx import Presentation
from pptx.chart.data import ChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_TICK_MARK, XL_LEGEND_POSITION, XL_DATA_LABEL_POSITION
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_THEME_COLOR
from pptx.enum.shapes import MSO_SHAPE

def create_slide(
    output_pptx_path: str,
    title_text: str = "Company Performance",
    **kwargs,
) -> str:
    """
    Creates a PPTX slide that visually reproduces the layout of the Dynamic KPI Slicer Dashboard.
    Note: The slicer is a static visual representation and is not interactive.

    Returns: path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === 1. Data Simulation (using pandas to mimic Power Pivot) ===
    # In a real scenario, this data would come from a database or file.
    data = {
        'Company Name': ['Bold Night', 'Urban Right', 'Meta Creations', 'Lucas Basics', 'Pina Lina'] * 4,
        'Product': ['T-Shirt', 'Shorts', 'Case', 'Basics', 'Crop Top'] * 4,
        'Quantity': [800, 700, 300, 400, 200, 850, 690, 330, 310, 240, 850, 690, 315, 265, 250, 850, 690, 315, 265, 250],
        'OrderID': range(20)
    }
    df = pd.DataFrame(data)

    # --- KPI Calculations ---
    # a. Quantity Sold (The one we will display)
    quantity_sold = df.groupby('Company Name')['Quantity'].sum().sort_values(ascending=False)

    # b. Product Count (For reference)
    product_count = df.groupby('Company Name')['Product'].nunique().sort_values(ascending=False)

    # c. Number of Orders (For reference)
    num_orders = df.groupby('Company Name')['OrderID'].count().sort_values(ascending=False)
    
    # We'll use 'quantity_sold' for our static chart
    kpi_data = quantity_sold

    # === 2. Create and Format the Chart ===
    chart_data = ChartData()
    chart_data.categories = kpi_data.index
    chart_data.add_series('KPI', kpi_data.values)

    x, y, cx, cy = Inches(1.5), Inches(2.0), Inches(10), Inches(4.5)
    chart = slide.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_CLUSTERED, x, y, cx, cy, chart_data
    ).chart

    chart.has_legend = False
    
    # Category Axis Formatting
    category_axis = chart.category_axis
    category_axis.major_tick_mark = XL_TICK_MARK.NONE
    category_axis.tick_labels.font.size = Pt(12)
    category_axis.tick_labels.font.bold = True
    
    # Value Axis Formatting (Remove it)
    value_axis = chart.value_axis
    value_axis.has_major_gridlines = False
    value_axis.visible = False

    # Plot Area Formatting
    plot = chart.plots[0]
    plot.has_data_labels = True
    data_labels = plot.data_labels
    data_labels.position = XL_DATA_LABEL_POSITION.OUTSIDE_END
    data_labels.font.size = Pt(11)
    data_labels.number_format = '#,##0'

    # Series Color
    series = chart.series[0]
    series.format.fill.solid()
    series.format.fill.fore_color.rgb = RGBColor(128, 128, 128) # Medium Gray

    # === 3. Create Static Slicer Visuals ===
    slicer_labels = ["Number of Orders", "Product Count", "Quantity Sold"]
    button_width = Inches(2.5)
    button_height = Inches(0.5)
    start_x = Inches(2.9)
    start_y = Inches(1.0)
    
    for i, label in enumerate(slicer_labels):
        x_pos = start_x + (i * (button_width + Inches(0.1)))
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x_pos, start_y, button_width, button_height)
        
        shape.text = label
        text_frame = shape.text_frame
        p = text_frame.paragraphs[0]
        p.font.size = Pt(14)
        p.font.color.rgb = RGBColor(0,0,0)
        p.alignment = 1  # Center alignment
        
        fill = shape.fill
        fill.solid()
        # Highlight the selected KPI
        if label == "Quantity Sold":
            fill.fore_color.rgb = RGBColor(255, 192, 0) # Yellow accent
        else:
            fill.fore_color.rgb = RGBColor(240, 240, 240) # Light Gray

        line = shape.line
        line.fill.solid()
        line.fill.fore_color.rgb = RGBColor(200, 200, 200)

    prs.save(output_pptx_path)
    return output_pptx_path

