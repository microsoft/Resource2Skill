def create_neon_glow_dashboard(
    output_pptx_path: str,
    company_name: str = "XX Company",
    dashboard_title: str = "Sales Dashboard",
    **kwargs,
) -> str:
    """
    Creates a single-slide PPTX file reproducing the Neon Glow Data Dashboard style.

    Args:
        output_pptx_path: The path to save the generated PPTX file.
        company_name: The name of the company for the title.
        dashboard_title: The main title of the dashboard.

    Returns:
        The path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt, Emu
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE, MSO_AUTO_SHAPE_TYPE
    from pptx.enum.dml import MSO_THEME_COLOR
    from PIL import Image, ImageDraw
    import io
    import math
    from lxml import etree
    
    # --- Helper Functions ---
    def create_radial_gradient_bg(width_px, height_px):
        """Generates a dark radial gradient background image."""
        img = Image.new('RGB', (width_px, height_px))
        draw = ImageDraw.Draw(img)
        
        center_x, center_y = width_px / 2, height_px / 2
        max_radius = math.sqrt(center_x**2 + center_y**2)
        
        c1 = (43, 27, 86) # Dark Purple
        c2 = (11, 4, 39)  # Near-Black Indigo

        for y in range(height_px):
            for x in range(width_px):
                distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                ratio = distance / max_radius
                
                r = int(c1[0] * (1 - ratio) + c2[0] * ratio)
                g = int(c1[1] * (1 - ratio) + c2[1] * ratio)
                b = int(c1[2] * (1 - ratio) + c2[2] * ratio)
                
                draw.point((x, y), fill=(r, g, b))
        
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        return img_byte_arr

    def create_sparkline_area(width_px, height_px, data_points, color):
        """Generates a transparent sparkline area chart image."""
        img = Image.new('RGBA', (width_px, height_px), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        min_val, max_val = min(data_points), max(data_points)
        range_val = max_val - min_val if max_val > min_val else 1
        
        # Normalize points
        normalized_points = []
        for i, dp in enumerate(data_points):
            x = (i / (len(data_points) - 1)) * width_px
            y = height_px - ((dp - min_val) / range_val) * (height_px * 0.8) - (height_px * 0.1) # Add padding
            normalized_points.append((x, y))

        # Create polygon for filled area
        polygon_points = normalized_points.copy()
        polygon_points.append((width_px, height_px))
        polygon_points.append((0, height_px))

        draw.polygon(polygon_points, fill=color)

        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        return img_byte_arr

    def add_text_glow(run, color_hex="FDD550", size_pt=6, alpha_percent=50):
        """Adds a glow effect to a text run using lxml."""
        _r = run._r
        rPr = _r.get_or_add_rPr()
        effect_lst = rPr.get_or_add_effectLst()
        
        outer_shadow = etree.SubElement(effect_lst, "{http://schemas.openxmlformats.org/drawingml/2006/main}outerShw")
        outer_shadow.set("blurRad", str(Emu(Pt(size_pt))))
        outer_shadow.set("dist", "0")
        outer_shadow.set("dir", "0")
        outer_shadow.set("algn", "ctr")
        
        srgb_clr = etree.SubElement(outer_shadow, "{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr")
        srgb_clr.set("val", color_hex)
        
        alpha = etree.SubElement(srgb_clr, "{http://schemas.openxmlformats.org/drawingml/2006/main}alpha")
        alpha.set("val", str(alpha_percent * 1000))

    # --- Presentation Setup ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # --- Layer 1: Background ---
    bg_img = create_radial_gradient_bg(int(prs.slide_width.emu / 9525), int(prs.slide_height.emu / 9525))
    slide.shapes.add_picture(bg_img, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # --- Layer 2: Main Layout Elements (Sidebar & Header) ---
    # Sidebar
    sidebar = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE, Inches(0), Inches(0), Inches(2.2), prs.slide_height)
    sidebar.fill.solid()
    sidebar.fill.fore_color.rgb = RGBColor(27, 27, 63) # #1B1B3F
    sidebar.line.fill.background()

    # Header
    title_box = slide.shapes.add_textbox(Inches(2.5), Inches(0.2), Inches(10.5), Inches(0.8))
    p = title_box.text_frame.paragraphs[0]
    p.text = f"{company_name} {dashboard_title}"
    p.font.name = 'Segoe UI Semibold'
    p.font.size = Pt(24)
    p.font.color.rgb = RGBColor(255, 255, 255)

    # --- Layer 3: Navigation Items ---
    nav_items = ["Overall", "Period Analysis", "Product Analysis", "Region Analysis", "Returns Analysis", "Performance", "Customer Analysis"]
    home_icon_shape = slide.shapes.add_freeform_shape(
        Inches(0.4), Inches(0.4),
        [
            (Inches(0.25), Inches(0)), (Inches(0.5), Inches(0.25)), (Inches(0.4), Inches(0.25)),
            (Inches(0.4), Inches(0.5)), (Inches(0.1), Inches(0.5)), (Inches(0.1), Inches(0.25)),
            (Inches(0), Inches(0.25)), (Inches(0.25), Inches(0))
        ]
    )
    home_icon_shape.fill.solid()
    home_icon_shape.fill.fore_color.rgb = RGBColor(70, 200, 210)
    home_icon_shape.line.fill.background()

    for i, item in enumerate(nav_items):
        y_pos = Inches(1.5 + i * 0.7)
        nav_box = slide.shapes.add_textbox(Inches(0.4), y_pos, Inches(1.6), Inches(0.5))
        p = nav_box.text_frame.paragraphs[0]
        p.text = item
        p.font.name = 'Segoe UI'
        p.font.size = Pt(14)
        if i == 0: # Active item
            p.font.bold = True
            p.font.color.rgb = RGBColor(70, 200, 210) # Cyan
        else:
            p.font.color.rgb = RGBColor(255, 255, 255)

    # --- Layer 4: KPI Cards ---
    kpi_data = [
        {"title": "SALES TOTAL", "value": "1,009", "unit": "M", "comp_label": "vs PY", "comp_val": "718", "growth": "40.5%", "chart_data": [10, 20, 15, 30, 25, 45, 40]},
        {"title": "PROFIT TOTAL", "value": "130", "unit": "M", "comp_label": "vs PY", "comp_val": "115", "growth": "13.2%", "chart_data": [5, 8, 6, 12, 10, 15, 14]},
        {"title": "ORDERS TOTAL", "value": "6,297", "unit": "", "comp_label": "vs PY", "comp_val": "4,418", "growth": "42.5%", "chart_data": [30, 50, 40, 80, 70, 100, 95]},
        {"title": "SALES VOLUME", "value": "6,297", "unit": "units", "comp_label": "vs PY", "comp_val": "4,418", "growth": "42.5%", "chart_data": [30, 50, 40, 80, 70, 100, 95]},
        {"title": "GROSS MARGIN", "value": "12.9", "unit": "%", "comp_label": "vs PY", "comp_val": "16.0", "growth": "-3.1%", "chart_data": [20, 18, 19, 15, 16, 13, 12]},
        {"title": "TOTAL CUSTOMERS", "value": "680", "unit": "", "comp_label": "vs PY", "comp_val": "647", "growth": "5.1%", "chart_data": [10, 12, 15, 14, 18, 22, 25]},
    ]

    grid_cols, grid_rows = 3, 2
    card_width, card_height = Inches(3.5), Inches(2.8)
    start_x, start_y = Inches(2.5), Inches(1.2)
    gap_x, gap_y = Inches(0.2), Inches(0.3)

    for i, data in enumerate(kpi_data):
        row = i // grid_cols
        col = i % grid_cols
        x = start_x + col * (card_width + gap_x)
        y = start_y + row * (card_height + gap_y)

        # Card background
        card = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE, x, y, card_width, card_height)
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(27, 27, 63)
        card.line.solid()
        card.line.color.rgb = RGBColor(70, 200, 210)
        card.line.width = Pt(0.5)

        # Card Title
        tb = slide.shapes.add_textbox(x + Inches(0.2), y + Inches(0.2), card_width - Inches(0.4), Inches(0.4))
        p = tb.text_frame.paragraphs[0]
        p.text = data["title"]
        p.font.name = 'Segoe UI Semibold'; p.font.size = Pt(12); p.font.color.rgb = RGBColor(200, 200, 200)

        # KPI Value with Glow
        tb_val = slide.shapes.add_textbox(x + Inches(0.2), y + Inches(0.6), card_width - Inches(1), Inches(1.2))
        p_val = tb_val.text_frame.paragraphs[0]
        run_val = p_val.add_run()
        run_val.text = data["value"]
        run_val.font.name = 'Segoe UI Black'; run_val.font.size = Pt(44)
        run_val.font.color.rgb = RGBColor(253, 221, 80)
        add_text_glow(run_val, color_hex="FDD550", size_pt=12, alpha_percent=80)
        
        if data["unit"]:
            run_unit = p_val.add_run()
            run_unit.text = f' {data["unit"]}'
            run_unit.font.name = 'Segoe UI Semibold'; run_unit.font.size = Pt(16)
            run_unit.font.color.rgb = RGBColor(253, 221, 80)

        # Comparison metrics
        tb_comp = slide.shapes.add_textbox(x + Inches(0.2), y + Inches(1.8), card_width - Inches(0.4), Inches(0.4))
        p_comp = tb_comp.text_frame.paragraphs[0]
        p_comp.text = f'{data["comp_label"]}: {data["comp_val"]}    Growth: {data["growth"]}'
        p_comp.font.name = 'Segoe UI'; p_comp.font.size = Pt(10); p_comp.font.color.rgb = RGBColor(220, 220, 220)

        # Sparkline
        spark_img = create_sparkline_area(300, 100, data["chart_data"], (70, 200, 210, 255))
        slide.shapes.add_picture(spark_img, x + Inches(0.2), y + Inches(2.1), height=Inches(0.5), width=card_width - Inches(0.4))

    prs.save(output_pptx_path)
    return output_pptx_path

# Example Usage:
# create_neon_glow_dashboard("Neon_Glow_Dashboard.pptx")

