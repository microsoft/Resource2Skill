import collections.abc
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_TICK_MARK, XL_LEGEND_POSITION
from pptx.chart.data import ChartData
from pptx.enum.shapes import MSO_SHAPE

def create_slide(
    output_pptx_path: str,
    title_text: str = "Quarterly Business Review",
    accent_color: tuple = (255, 106, 0),  # Default: Alibaba Orange, as seen in the tutorial
    **kwargs,
) -> str:
    """
    Creates a PPTX slide based on the "Systematic Color Palette Development" principle,
    specifically the "LOGO-based/Monochromatic with Neutrals" method.

    This method uses a primary accent color combined with black, white, and gray to create
    a clean, professional, and branded visual style.

    Returns: path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(16)
    prs.slide_height = Inches(9)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

    # === Define the Color Palette based on the principle ===
    # This is the core of the skill: a limited, structured palette.
    ACCENT_RGB = RGBColor(accent_color[0], accent_color[1], accent_color[2])
    WHITE_RGB = RGBColor(255, 255, 255)
    DARK_TEXT_RGB = RGBColor(40, 40, 40)
    LIGHT_GRAY_RGB = RGBColor(240, 240, 240)
    
    # Set a solid white background for maximum clarity
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = WHITE_RGB

    # === Layer 1: Title & Structure ===
    title_shape = slide.shapes.add_textbox(Inches(0.75), Inches(0.5), Inches(14.5), Inches(1))
    title_tf = title_shape.text_frame
    p = title_tf.paragraphs[0]
    p.text = title_text
    p.font.name = 'Segoe UI'
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = DARK_TEXT_RGB

    # Add a decorative line using the accent color
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.75), Inches(1.3), Inches(4), Inches(0.08))
    line.fill.solid()
    line.fill.fore_color.rgb = ACCENT_RGB
    line.line.fill.solid()
    line.line.fill.fore_color.rgb = ACCENT_RGB

    # === Layer 2: Content (Applying the Color Scheme) ===

    # --- Bar Chart ---
    chart_data = ChartData()
    chart_data.categories = ['East Region', 'West Region', 'Midwest']
    chart_data.add_series('Q1 Sales (M)', (19.2, 21.4, 16.7))

    x, y, cx, cy = Inches(0.75), Inches(2), Inches(8), Inches(5.5)
    chart = slide.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_CLUSTERED, x, y, cx, cy, chart_data
    ).chart

    chart.has_legend = False
    chart.font.name = 'Segoe UI'
    chart.font.size = Pt(12)
    chart.font.color.rgb = DARK_TEXT_RGB
    chart.chart_title.text_frame.text = 'Regional Performance'
    
    # Style the chart using the palette
    value_axis = chart.value_axis
    value_axis.tick_labels.font.color.rgb = DARK_TEXT_RGB
    value_axis.has_major_gridlines = True
    value_axis.major_gridlines.format.line.color.rgb = LIGHT_GRAY_RGB

    category_axis = chart.category_axis
    category_axis.tick_labels.font.color.rgb = DARK_TEXT_RGB
    category_axis.format.line.fill.background() # No axis line

    # Apply the accent color to the data series
    plot = chart.plots[0]
    plot.has_data_labels = True
    data_labels = plot.data_labels
    data_labels.font.size = Pt(12)
    data_labels.font.color.rgb = DARK_TEXT_RGB

    series = plot.series[0]
    series.format.fill.solid()
    series.format.fill.fore_color.rgb = ACCENT_RGB
    
    # --- KPI Boxes ---
    kpi_data = {
        "Total Revenue": "$4.2M",
        "New Customers": "1,200",
        "Growth": "+15%"
    }
    
    start_x = Inches(9.5)
    start_y = Inches(2)
    box_width = Inches(5.75)
    box_height = Inches(1.5)
    gap = Inches(0.5)

    for i, (metric, value) in enumerate(kpi_data.items()):
        y_pos = start_y + i * (box_height + gap)
        
        # Light gray background box for subtle separation
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, start_x, y_pos, box_width, box_height)
        shape.adjustments[0] = 0.1 # Corner radius
        shape.fill.solid()
        shape.fill.fore_color.rgb = LIGHT_GRAY_RGB
        shape.line.fill.background() # No outline

        tf = shape.text_frame
        tf.margin_left = Inches(0.3)
        tf.margin_right = Inches(0.3)
        
        # Metric Name (Dark Text)
        p1 = tf.paragraphs[0]
        p1.text = metric
        p1.font.name = 'Segoe UI Light'
        p1.font.size = Pt(18)
        p1.font.color.rgb = DARK_TEXT_RGB
        
        # Metric Value (Accent Color)
        p2 = tf.add_paragraph()
        p2.text = value
        p2.font.name = 'Segoe UI'
        p2.font.size = Pt(32)
        p2.font.bold = True
        p2.font.color.rgb = ACCENT_RGB

    prs.save(output_pptx_path)
    return output_pptx_path
