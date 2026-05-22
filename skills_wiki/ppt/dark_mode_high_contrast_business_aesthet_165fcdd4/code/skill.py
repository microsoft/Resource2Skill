def create_slide(
    output_pptx_path: str = "dark_corporate_dashboard.pptx",
    title_text: str = "战略总览与分析 \nStrategic Overview",
    accent_color: tuple = (255, 204, 0),  # Cyber Yellow
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Dark Mode High-Contrast Business Aesthetic.
    Generates a premium dark gradient background, typographic title elements, 
    KPI cards, and a dark-mode styled bar chart.
    """
    import os
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.chart.data import CategoryChartData
    from pptx.enum.chart import XL_CHART_TYPE
    from pptx.enum.chart import XL_TICK_MARK, XL_TICK_LABEL_POSITION
    from PIL import Image, ImageDraw

    # Initialize Presentation (16:9)
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank layout
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    # ==========================================
    # Layer 1: Background Generation via PIL
    # ==========================================
    bg_path = "temp_dark_bg.png"
    width, height = int(13.333 * 100), int(7.5 * 100)
    bg_img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(bg_img)
    
    # Create a smooth vertical gradient from Dark Charcoal to Near Black
    color_top = (45, 45, 50)
    color_bottom = (10, 10, 12)
    for y in range(height):
        r = int(color_top[0] - (color_top[0] - color_bottom[0]) * (y / height))
        g = int(color_top[1] - (color_top[1] - color_bottom[1]) * (y / height))
        b = int(color_top[2] - (color_top[2] - color_bottom[2]) * (y / height))
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    bg_img.save(bg_path)
    slide.shapes.add_picture(bg_path, 0, 0, prs.slide_width, prs.slide_height)

    # ==========================================
    # Layer 2: Title and Aesthetic Accents
    # ==========================================
    # Title Text
    tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(8), Inches(1))
    tf = tx_box.text_frame
    
    p_main = tf.paragraphs[0]
    p_main.text = title_text.split('\n')[0]
    p_main.font.size = Pt(36)
    p_main.font.color.rgb = RGBColor(255, 255, 255)
    p_main.font.bold = True
    
    if "\n" in title_text:
        p_sub = tf.add_paragraph()
        p_sub.text = title_text.split('\n')[1]
        p_sub.font.size = Pt(18)
        p_sub.font.color.rgb = RGBColor(150, 150, 150)

    # Signature Yellow Accent Line (The "Corporate Template" stamp)
    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 
        Inches(0.8), Inches(1.8), 
        Inches(0.6), Inches(0.08)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = RGBColor(*accent_color)
    line.line.fill.background()

    # ==========================================
    # Layer 3: KPI Data Cards
    # ==========================================
    def create_kpi_card(slide, x, y, w, h, label, value, is_highlight=False):
        # Card Background
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(30, 30, 32)
        card.line.color.rgb = RGBColor(60, 60, 65)  # Subtle border
        card.line.width = Pt(1)
        
        # Value Text (Number)
        val_box = slide.shapes.add_textbox(x, y + Inches(0.2), w, Inches(1))
        val_tf = val_box.text_frame
        val_tf.text = value
        val_p = val_tf.paragraphs[0]
        val_p.alignment = PP_ALIGN.CENTER
        val_p.font.size = Pt(44)
        val_p.font.bold = True
        if is_highlight:
            val_p.font.color.rgb = RGBColor(*accent_color)
        else:
            val_p.font.color.rgb = RGBColor(255, 255, 255)

        # Label Text
        lbl_box = slide.shapes.add_textbox(x, y + Inches(1.1), w, Inches(0.5))
        lbl_tf = lbl_box.text_frame
        lbl_tf.text = label
        lbl_p = lbl_tf.paragraphs[0]
        lbl_p.alignment = PP_ALIGN.CENTER
        lbl_p.font.size = Pt(14)
        lbl_p.font.color.rgb = RGBColor(170, 170, 170)

    create_kpi_card(slide, Inches(0.8), Inches(2.5), Inches(3.5), Inches(2.0), "市场份额 (Market Share)", "56%", is_highlight=True)
    create_kpi_card(slide, Inches(0.8), Inches(4.8), Inches(3.5), Inches(2.0), "客户增长 (Client Growth)", "3,200", is_highlight=False)

    # ==========================================
    # Layer 4: Dark Mode Data Visualization
    # ==========================================
    chart_data = CategoryChartData()
    chart_data.categories = ['Q1', 'Q2', 'Q3', 'Q4', 'Next']
    chart_data.add_series('Base', (4.3, 2.5, 3.5, 2.8, 5.0))
    chart_data.add_series('Target', (2.4, 4.4, 1.8, 4.5, 2.0))

    x, y, cx, cy = Inches(4.8), Inches(2.5), Inches(7.8), Inches(4.3)
    chart = slide.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_CLUSTERED, x, y, cx, cy, chart_data
    ).chart

    # Dark Mode Chart Styling
    chart.has_legend = False
    
    # Series 1 (Base - Subdued Grey)
    series_1 = chart.series[0]
    series_1.format.fill.solid()
    series_1.format.fill.fore_color.rgb = RGBColor(80, 80, 85)
    
    # Series 2 (Target - Highlight Yellow)
    series_2 = chart.series[1]
    series_2.format.fill.solid()
    series_2.format.fill.fore_color.rgb = RGBColor(*accent_color)

    # Axis Styling
    category_axis = chart.category_axis
    category_axis.format.line.color.rgb = RGBColor(100, 100, 100)
    category_axis.tick_labels.font.color.rgb = RGBColor(170, 170, 170)
    category_axis.tick_labels.font.size = Pt(12)

    value_axis = chart.value_axis
    value_axis.has_major_gridlines = True
    value_axis.major_gridlines.format.line.color.rgb = RGBColor(50, 50, 55)
    value_axis.major_gridlines.format.line.dash_style = 1  # Solid
    value_axis.tick_labels.font.color.rgb = RGBColor(170, 170, 170)
    value_axis.tick_labels.font.size = Pt(12)

    # Add a subtle decorative frame/backdrop for the chart
    chart_bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x - Inches(0.2), y - Inches(0.2), cx + Inches(0.4), cy + Inches(0.4))
    chart_bg.fill.solid()
    chart_bg.fill.fore_color.rgb = RGBColor(25, 25, 28)
    chart_bg.line.fill.background() # No border
    
    # Send chart backdrop backward (requires manipulating z-order, but standard pptx adds it to top. 
    # To fix z-order natively in simple scripts, we add shapes in order. 
    # Since chart is already added, we will swap the XML nodes to push the background behind the chart)
    slide.shapes._spTree.insert(
        slide.shapes._spTree.index(chart.element), 
        chart_bg.element
    )

    # Save and clean up
    prs.save(output_pptx_path)
    if os.path.exists(bg_path):
        os.remove(bg_path)
        
    return output_pptx_path
