def create_slide(
    output_pptx_path: str,
    title_text: str = "Last Years Product Sales",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Icon-Anchored Flat Ribbon Chart effect.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.chart import XL_CHART_TYPE, XL_TICK_MARK, XL_LABEL_POSITION
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN
    from pptx.chart.data import CategoryChartData

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Set background color to light gray/off-white
    bg_color = RGBColor(245, 245, 245)
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = bg_color

    # --- 1. Draw the Ribbon Title ---
    ribbon_y = Inches(0.8)
    ribbon_x = Inches(3.5)
    ribbon_w = Inches(6.333)
    ribbon_h = Inches(0.6)
    
    ribbon_color = RGBColor(112, 128, 144)
    ribbon_dark = RGBColor(80, 95, 110)

    # Left tail (pointing outwards/left) - using a chevron rotated or simply a pentagon
    left_tail = slide.shapes.add_shape(
        MSO_SHAPE.CHEVRON, ribbon_x - Inches(0.4), ribbon_y + Inches(0.2), Inches(0.6), Inches(0.4)
    )
    left_tail.rotation = 180
    left_tail.fill.solid()
    left_tail.fill.fore_color.rgb = ribbon_dark
    left_tail.line.fill.background()

    # Right tail (pointing outwards/right)
    right_tail = slide.shapes.add_shape(
        MSO_SHAPE.CHEVRON, ribbon_x + ribbon_w - Inches(0.2), ribbon_y + Inches(0.2), Inches(0.6), Inches(0.4)
    )
    right_tail.fill.solid()
    right_tail.fill.fore_color.rgb = ribbon_dark
    right_tail.line.fill.background()

    # Main Ribbon Rectangle (Front)
    ribbon_main = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, ribbon_x, ribbon_y, ribbon_w, ribbon_h
    )
    ribbon_main.fill.solid()
    ribbon_main.fill.fore_color.rgb = ribbon_color
    ribbon_main.line.fill.background()
    
    # Ribbon Text
    tf = ribbon_main.text_frame
    tf.text = title_text
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    tf.paragraphs[0].font.size = Pt(20)
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)

    # --- 2. Create the Data Chart ---
    categories = ["iPhone", "iPod", "Mac", "iPad", "Services"]
    # Unicode equivalents for icons
    icons = ["📱", "🎵", "💻", "🖥️", "☁️"]
    values = [1478, 381, 2640, 2280, 3715]
    
    # Palette matching the tutorial
    palette = [
        RGBColor(0, 191, 255),   # Cyan
        RGBColor(255, 180, 0),   # Yellow
        RGBColor(126, 211, 33),  # Green
        RGBColor(186, 85, 211),  # Purple
        RGBColor(74, 144, 226)   # Blue
    ]

    chart_data = CategoryChartData()
    chart_data.categories = categories
    chart_data.add_series("Sales", values)

    chart_x, chart_y = Inches(1.5), Inches(2.2)
    chart_cx, chart_cy = Inches(10.333), Inches(3.5)

    chart = slide.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_CLUSTERED, chart_x, chart_y, chart_cx, chart_cy, chart_data
    ).chart

    # Format Chart
    chart.has_legend = False
    chart.has_title = False
    
    # Format Y-Axis (Hide it completely)
    value_axis = chart.value_axis
    value_axis.has_major_gridlines = True
    value_axis.major_gridlines.format.line.color.rgb = RGBColor(220, 220, 220)
    value_axis.major_tick_mark = XL_TICK_MARK.NONE
    value_axis.minor_tick_mark = XL_TICK_MARK.NONE
    value_axis.tick_labels.font.size = Pt(1) # effectively hidden
    value_axis.tick_labels.font.color.rgb = bg_color
    value_axis.format.line.fill.background()

    # Format X-Axis (Hide labels, we will draw icons)
    category_axis = chart.category_axis
    category_axis.major_tick_mark = XL_TICK_MARK.NONE
    category_axis.tick_labels.font.size = Pt(1)
    category_axis.tick_labels.font.color.rgb = bg_color
    category_axis.format.line.color.rgb = RGBColor(200, 200, 200)

    # Format Data Series (Colors and Labels)
    series = chart.series[0]
    series.has_data_labels = True
    series.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
    series.data_labels.font.size = Pt(12)
    series.data_labels.font.bold = True
    series.data_labels.font.color.rgb = RGBColor(80, 80, 80)

    # Apply individual colors to bars
    for idx, point in enumerate(series.points):
        fill = point.format.fill
        fill.solid()
        fill.fore_color.rgb = palette[idx % len(palette)]
        # Remove border
        point.format.line.fill.background()

    # --- 3. Draw Icon Badges below X-Axis ---
    # Heuristic for calculating X positions of the columns
    # Plot area width is slightly smaller than chart width.
    plot_width = chart_cx - Inches(0.5) 
    start_x = chart_x + Inches(0.25)
    
    badge_radius = Inches(0.3)
    y_badge = chart_y + chart_cy + Inches(0.1)

    for idx, (cat, icon_text, color) in enumerate(zip(categories, icons, palette)):
        # Center X for this category
        center_x = start_x + (plot_width * (idx + 0.5) / len(categories))
        
        # 3a. Draw colored circle
        circle = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, 
            center_x - badge_radius, 
            y_badge, 
            badge_radius * 2, 
            badge_radius * 2
        )
        circle.fill.solid()
        circle.fill.fore_color.rgb = color
        circle.line.fill.background()

        # 3b. Add Icon (Unicode)
        tf_icon = circle.text_frame
        tf_icon.text = icon_text
        tf_icon.paragraphs[0].alignment = PP_ALIGN.CENTER
        tf_icon.paragraphs[0].font.size = Pt(24)

        # 3c. Add Category Label Text Box below badge
        label_box = slide.shapes.add_textbox(
            center_x - Inches(0.75), 
            y_badge + badge_radius * 2 + Inches(0.1), 
            Inches(1.5), 
            Inches(0.4)
        )
        tf_label = label_box.text_frame
        tf_label.text = cat
        tf_label.paragraphs[0].alignment = PP_ALIGN.CENTER
        tf_label.paragraphs[0].font.size = Pt(14)
        tf_label.paragraphs[0].font.bold = True
        tf_label.paragraphs[0].font.color.rgb = RGBColor(80, 80, 80)

    prs.save(output_pptx_path)
    return output_pptx_path
