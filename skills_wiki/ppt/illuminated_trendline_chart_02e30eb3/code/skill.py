def create_slide(
    output_pptx_path: str,
    title_text: str = "Metaverse Market Potential",
    bg_image_url: str = "https://images.unsplash.com/photo-1534796636912-3b95b3ab5986?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2071&q=80",
    accent_color_start: tuple = (255, 220, 0),
    accent_color_end: tuple = (60, 179, 113),
    **kwargs,
) -> str:
    """
    Creates a PPTX slide with an "Illuminated Trendline Chart".

    This effect layers a line chart over a gradient-filled area chart,
    both using the same data, to create a visually rich data trend.

    Args:
        output_pptx_path: The path to save the generated .pptx file.
        title_text: The main title for the slide.
        bg_image_url: URL for a dark background image (e.g., space theme).
        accent_color_start: RGB tuple for the line color and top of the gradient.
        accent_color_end: RGB tuple for the bottom of the gradient.

    Returns:
        Path to the saved PPTX file.
    """
    import io
    import urllib.request
    from lxml import etree
    from pptx import Presentation
    from pptx.chart.data import ChartData, CategoryChartData
    from pptx.dml.color import RGBColor
    from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
    from pptx.util import Inches, Pt

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: Background ===
    try:
        with urllib.request.urlopen(bg_image_url) as url:
            f = io.BytesIO(url.read())
        slide.shapes.add_picture(f, 0, 0, width=prs.slide_width, height=prs.slide_height)
    except Exception:
        # Fallback to a solid dark background
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(10, 10, 40)

    # === Layer 2: Chart ===
    # --- Chart Data (based on the tutorial example) ---
    chart_data = CategoryChartData()
    chart_data.categories = [str(year) for year in range(2022, 2031)]
    # Series 1: The visible Line Chart
    chart_data.add_series('Market Size (Line)', (0.2, 0.288, 0.444, 0.661, 0.985, 1.469, 2.188, 3.268, 4.858))
    # Series 2: The gradient Area Chart (same data)
    chart_data.add_series('Market Size (Area)', (0.2, 0.288, 0.444, 0.661, 0.985, 1.469, 2.188, 3.268, 4.858))

    # --- Create the chart object ---
    x, y, cx, cy = Inches(0.5), Inches(1.5), Inches(12), Inches(5.5)
    graphic_frame = slide.shapes.add_chart(
        XL_CHART_TYPE.LINE, x, y, cx, cy, chart_data
    )
    chart = graphic_frame.chart
    chart.has_legend = False

    # --- Modify plots to create a Combination Chart ---
    # The first plot is the line chart, the second will be the area chart
    plot = chart.plots[0]
    plot.has_data_labels = False
    
    # Create an area chart plot element to add to the chart's XML
    # We will "steal" the second series from the line chart plot and move it here.
    chart_elm = chart._element
    plot_area_elm = chart_elm.plotArea
    
    # Create a new <c:areaChart> element
    area_chart_elm = etree.SubElement(plot_area_elm, '{http://schemas.openxmlformats.org/drawingml/2006/chart}areaChart')
    etree.SubElement(area_chart_elm, '{http://schemas.openxmlformats.org/drawingml/2006/chart}grouping', val="standard")

    # Move the second series definition from the line chart to the area chart
    line_chart_plot_elm = plot_area_elm.find('{http://schemas.openxmlformats.org/drawingml/2006/chart}lineChart')
    ser_to_move = line_chart_plot_elm.findall('{http://schemas.openxmlformats.org/drawingml/2006/chart}ser')[1]
    line_chart_plot_elm.remove(ser_to_move)
    area_chart_elm.append(ser_to_move)

    # Add axis IDs to the new area chart plot
    for ax_id_val in ['1', '2']: # Assuming standard axis IDs
        etree.SubElement(area_chart_elm, '{http://schemas.openxmlformats.org/drawingml/2006/chart}axId', val=ax_id_val)
    
    # --- Style the Line Series ---
    line_series = chart.series[0]
    line_series.format.line.color.rgb = RGBColor(*accent_color_start)
    line_series.format.line.width = Pt(3)
    line_series.smooth = True

    # --- Style the Area Series with Gradient Fill (lxml injection) ---
    area_series_elm = ser_to_move
    spPr_elm = area_series_elm.find('{http://schemas.openxmlformats.org/drawingml/2006/chart}spPr')
    if spPr_elm is None:
        spPr_elm = etree.SubElement(area_series_elm, '{http://schemas.openxmlformats.org/drawingml/2006/chart}spPr')

    # Remove default line on the area chart
    ln_elm = etree.SubElement(spPr_elm, '{http://schemas.openxmlformats.org/drawingml/2006/main}ln')
    etree.SubElement(ln_elm, '{http://schemas.openxmlformats.org/drawingml/2006/main}noFill')

    # Define the gradient fill
    grad_fill_elm = etree.SubElement(spPr_elm, '{http://schemas.openxmlformats.org/drawingml/2006/main}gradFill')
    gs_lst_elm = etree.SubElement(grad_fill_elm, '{http://schemas.openxmlformats.org/drawingml/2006/main}gsLst')
    
    # Gradient Stop 1 (Top)
    gs1 = etree.SubElement(gs_lst_elm, '{http://schemas.openxmlformats.org/drawingml/2006/main}gs', pos="0")
    srgb1 = etree.SubElement(gs1, '{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr', val="%02x%02x%02x" % accent_color_start)
    etree.SubElement(srgb1, '{http://schemas.openxmlformats.org/drawingml/2006/main}alpha', val="60000") # 60% opacity

    # Gradient Stop 2 (Bottom)
    gs2 = etree.SubElement(gs_lst_elm, '{http://schemas.openxmlformats.org/drawingml/2006/main}gs', pos="100000")
    srgb2 = etree.SubElement(gs2, '{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr', val="%02x%02x%02x" % accent_color_end)
    etree.SubElement(srgb2, '{http://schemas.openxmlformats.org/drawingml/2006/main}alpha', val="20000") # 20% opacity
    
    # Set gradient direction (top to bottom)
    lin_elm = etree.SubElement(grad_fill_elm, '{http://schemas.openxmlformats.org/drawingml/2006/main}lin', ang="9000000", scaled="1")

    # --- Format Axes ---
    category_axis = chart.category_axis
    category_axis.format.line.fill.background()
    category_axis.format.font.color.rgb = RGBColor(255, 255, 255)
    category_axis.format.font.size = Pt(12)
    category_axis.tick_labels.font.bold = False

    value_axis = chart.value_axis
    value_axis.format.line.fill.background()
    value_axis.has_major_gridlines = True
    value_axis.major_gridlines.format.line.color.rgb = RGBColor(255, 255, 255)
    value_axis.major_gridlines.format.line.dash_style = 'long_dash'
    value_axis.format.line.width = Pt(0.5)
    # Use lxml to set transparency for gridlines
    gridlns_spPr = value_axis.major_gridlines.format.line._get_or_add_ln().get_or_add_srgbClr()
    etree.SubElement(gridlns_spPr, '{http://schemas.openxmlformats.org/drawingml/2006/main}alpha', val="25000") # 25% opacity
    
    value_axis.format.font.color.rgb = RGBColor(255, 255, 255)
    value_axis.format.font.size = Pt(12)
    
    # --- Format Plot Area ---
    chart.plot_area.format.fill.background()

    # === Layer 3: Text & Content ===
    title_shape = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(10), Inches(1))
    title_shape.text_frame.text = title_text
    p = title_shape.text_frame.paragraphs[0]
    p.font.name = 'Segoe UI Light'
    p.font.size = Pt(36)
    p.font.color.rgb = RGBColor(255, 255, 255)

    prs.save(output_pptx_path)
    return output_pptx_path

