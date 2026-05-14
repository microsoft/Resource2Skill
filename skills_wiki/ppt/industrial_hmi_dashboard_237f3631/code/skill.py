def create_slide(
    output_pptx_path: str,
    title_text: str = "Factory Operations Dashboard",
    bg_palette: str = "industrial",  # This parameter is for theme consistency but not used for image search
    accent_color: tuple = (105, 190, 40),  # RGB for 'Good' status
    **kwargs,
) -> str:
    """
    Creates a PPTX slide with an Industrial HMI Dashboard for a production line.

    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.dml import MSO_FILL
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
    from pptx.shapes.freeform import FreeformBuilder

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Define color palette based on the video
    BG_COLOR = RGBColor(230, 230, 230)
    DARK_GRAY = RGBColor(89, 89, 89)
    MID_GRAY = RGBColor(166, 166, 166)
    LIGHT_GRAY = RGBColor(217, 217, 217)
    GREEN_STATUS = RGBColor(accent_color[0], accent_color[1], accent_color[2])
    RED_STATUS = RGBColor(255, 0, 0)
    BLUE_PRODUCT = RGBColor(68, 114, 196)
    WHITE_TEXT = RGBColor(255, 255, 255)
    BLACK_TEXT = RGBColor(0, 0, 0)

    # === Layer 1: Background ===
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = BG_COLOR
    
    # Helper to add text easily
    def add_text(shape, text, size=12, bold=False, color=BLACK_TEXT, align=PP_ALIGN.CENTER):
        text_frame = shape.text_frame
        text_frame.clear()
        p = text_frame.paragraphs[0]
        p.text = text
        p.font.size = Pt(size)
        p.font.bold = bold
        p.font.color.rgb = color
        p.alignment = align
        text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
        text_frame.margin_bottom = 0
        text_frame.margin_top = 0
        text_frame.margin_left = 0
        text_frame.margin_right = 0
        return shape

    # === Layer 2: KPI Dashboard (Top) ===
    def draw_kpi_gauge(left, top, title, value_str):
        gauge = slide.shapes.add_shape(MSO_SHAPE.DONUT, Inches(left), Inches(top), Inches(0.9), Inches(0.9))
        gauge.fill.solid()
        gauge.fill.fore_color.rgb = GREEN_STATUS
        gauge.line.fill.background()
        gauge.adjustments[0] = 0.75 # Make ring thinner
        
        add_text(gauge, value_str, size=16, bold=True, color=WHITE_TEXT)
        
        label = slide.shapes.add_textbox(Inches(left-0.05), Inches(top+0.9), Inches(1), Inches(0.3))
        add_text(label, title, size=10, color=DARK_GRAY)

    def draw_kpi_box(left, top, title, value_str, sub_label):
        box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(1.8), Inches(1.1))
        box.fill.solid()
        box.fill.fore_color.rgb = DARK_GRAY
        box.line.fill.background()
        
        title_shape = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(1.8), Inches(0.3))
        add_text(title_shape, title, size=10, color=WHITE_TEXT)

        value_shape = slide.shapes.add_textbox(Inches(left), Inches(top+0.2), Inches(1.8), Inches(0.7))
        add_text(value_shape, value_str, size=32, bold=True, color=WHITE_TEXT)

        sub_label_shape = slide.shapes.add_textbox(Inches(left), Inches(top+0.8), Inches(1.8), Inches(0.3))
        add_text(sub_label_shape, sub_label, size=9, color=LIGHT_GRAY)

    draw_kpi_gauge(1.0, 0.3, "OEE", "27%")
    draw_kpi_gauge(2.5, 0.3, "Quality", "30%")
    draw_kpi_gauge(4.0, 0.3, "Availability", "4%")
    draw_kpi_gauge(5.5, 0.3, "Operation", "32%")
    
    draw_kpi_box(7.5, 0.2, "Production", "71", "Actual")
    draw_kpi_box(9.5, 0.2, "Production", "48", "Target")
    draw_kpi_box(11.5, 0.2, "Production", "31", "Average")

    # === Layer 3: Production Line ===
    # Conveyor Belt
    conveyor_y = Inches(4.5)
    conveyor_height = Inches(0.5)
    conveyor = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), conveyor_y, Inches(12.33), conveyor_height)
    conveyor.fill.solid()
    conveyor.fill.fore_color.rgb = DARK_GRAY
    conveyor.line.fill.background()

    for i in range(18):
        roller = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.8 + i*0.65), conveyor_y + Inches(0.15), Inches(0.2), Inches(0.2))
        roller.fill.solid()
        roller.fill.fore_color.rgb = MID_GRAY
        roller.line.fill.background()
    
    # Machinery
    machine_1 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.5), Inches(3.5), Inches(2.0), Inches(1.0))
    machine_1.fill.solid(); machine_1.fill.fore_color.rgb = MID_GRAY; machine_1.line.fill.background()
    machine_2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4.0), Inches(3.8), Inches(1.5), Inches(0.7))
    machine_2.fill.solid(); machine_2.fill.fore_color.rgb = MID_GRAY; machine_2.line.fill.background()
    
    # Products
    for i in range(3):
        bottle = slide.shapes.add_shape(MSO_SHAPE.CAN, Inches(1.8 + i*0.5), Inches(4.0), Inches(0.3), Inches(0.5))
        bottle.fill.solid(); bottle.fill.fore_color.rgb = BLUE_PRODUCT; bottle.line.fill.background()
        
    box_1 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.5), Inches(3.8), Inches(1.0), Inches(0.7))
    box_1.fill.solid(); box_1.fill.fore_color.rgb = RGBColor(210, 180, 140); box_1.line.color.rgb = DARK_GRAY

    # Gantry Robot Arm
    gripper_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(9.8), Inches(3.8), Inches(1.0), Inches(0.7))
    gripper_box.fill.solid(); gripper_box.fill.fore_color.rgb = RGBColor(210, 180, 140); gripper_box.line.color.rgb = DARK_GRAY

    freeform = FreeformBuilder(Inches(10.2), Inches(2.5), Emu(0), Emu(0))
    freeform.add_line_segments([(Inches(10.2), Inches(3.8)), (Inches(10.3), Inches(3.8)), (Inches(10.3), Inches(2.5))])
    freeform.close()
    gantry_gripper = freeform.convert_to_shape(slide.shapes)
    gantry_gripper.fill.solid(); gantry_gripper.fill.fore_color.rgb = DARK_GRAY; gantry_gripper.line.fill.background()
    
    gantry_rail = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(9.0), Inches(2.3), Inches(2.5), Inches(0.2))
    gantry_rail.fill.solid(); gantry_rail.fill.fore_color.rgb = DARK_GRAY; gantry_rail.line.fill.background()

    # Status Light Tower
    def draw_status_light_tower(left):
        pole = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(2.0), Inches(0.1), Inches(2.5))
        pole.fill.solid(); pole.fill.fore_color.rgb = DARK_GRAY; pole.line.fill.background()
        light_on = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(left-0.1), Inches(2.0), Inches(0.3), Inches(0.3))
        light_on.fill.solid(); light_on.fill.fore_color.rgb = GREEN_STATUS; light_on.line.fill.background()
        
    draw_status_light_tower(0.8)
    draw_status_light_tower(12.4)

    # === Layer 4: Control Panel (Bottom) ===
    def draw_button(left, text, color, text_color):
        button = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(5.8), Inches(1.2), Inches(0.5))
        button.fill.solid(); button.fill.fore_color.rgb = color; button.line.fill.background()
        add_text(button, text, size=11, bold=True, color=text_color)
    
    draw_button(8.5, "START", GREEN_STATUS, WHITE_TEXT)
    draw_button(10.0, "STOP", RED_STATUS, WHITE_TEXT)
    
    prs.save(output_pptx_path)
    return output_pptx_path
