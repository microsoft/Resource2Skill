import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image, ImageDraw
import tempfile

def create_slide(
    output_pptx_path: str,
    title_text: str = "Production Line 01 - Live Status",
    kpi_data: list = [
        {"label": "OEE", "value": 73, "color": (46, 204, 113)},
        {"label": "Quality", "value": 98, "color": (46, 204, 113)},
        {"label": "Availability", "value": 85, "color": (241, 196, 15)},
        {"label": "Performance", "value": 88, "color": (46, 204, 113)}
    ],
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing an Industrial SCADA/IIoT Dashboard layout.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank layout
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    # --- Helper Functions ---
    def set_shape_color(shape, fill_rgb, line_rgb=None):
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(*fill_rgb)
        if line_rgb:
            shape.line.color.rgb = RGBColor(*line_rgb)
            shape.line.width = Pt(1)
        else:
            shape.line.fill.background()

    def generate_donut_chart(percentage, color, filename):
        """Generates a transparent PNG donut chart ring using PIL"""
        size = 300
        thickness = 35
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Background track (dark grey)
        bbox = [10, 10, size-10, size-10]
        draw.arc(bbox, start=0, end=360, fill=(180, 180, 185, 255), width=thickness)
        
        # Progress track
        # PIL arc angles: 0 is 3 o'clock, sweeping clockwise. We want to start at top (270)
        start_angle = 270
        end_angle = 270 + (360 * (percentage / 100.0))
        draw.arc(bbox, start=start_angle, end=end_angle, fill=color + (255,), width=thickness)
        
        img.save(filename)
        return filename

    def add_text(slide, text, left, top, width, height, font_size, bold=False, color=(50, 50, 50), align=PP_ALIGN.CENTER):
        txBox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
        tf = txBox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = text
        p.alignment = align
        p.font.size = Pt(font_size)
        p.font.bold = bold
        p.font.color.rgb = RGBColor(*color)
        p.font.name = "Arial"
        return txBox

    # --- Colors ---
    bg_color = (235, 235, 240)
    panel_bg = (215, 215, 220)
    machine_grey = (100, 100, 105)
    conveyor_grey = (60, 60, 65)

    # --- Layer 1: Background & Zones ---
    # Main BG
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    set_shape_color(bg, bg_color)
    
    # Top KPI Panel Background
    kpi_panel = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.2), Inches(0.2), Inches(12.933), Inches(1.8))
    set_shape_color(kpi_panel, panel_bg)
    kpi_panel.adjustments[0] = 0.05
    
    # Middle Process Panel Background
    process_panel = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.2), Inches(2.2), Inches(12.933), Inches(3.2))
    set_shape_color(process_panel, panel_bg)
    process_panel.adjustments[0] = 0.02
    
    # Bottom Data Panel Background
    data_panel = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.2), Inches(5.6), Inches(12.933), Inches(1.7))
    set_shape_color(data_panel, panel_bg)
    data_panel.adjustments[0] = 0.05

    # Title
    add_text(slide, title_text, 0.4, 0.3, 3.0, 0.4, 14, bold=True, align=PP_ALIGN.LEFT)

    # --- Layer 2: KPI Widgets (Top Panel) ---
    temp_dir = tempfile.gettempdir()
    
    start_x = 0.5
    spacing = 1.8
    for i, kpi in enumerate(kpi_data):
        # Generate PIL Ring
        img_path = os.path.join(temp_dir, f"donut_{i}.png")
        generate_donut_chart(kpi["value"], kpi["color"], img_path)
        
        # Insert Ring
        ring = slide.shapes.add_picture(img_path, Inches(start_x + (i*spacing)), Inches(0.7), Inches(1.0), Inches(1.0))
        
        # Overlay Text
        add_text(slide, f"{kpi['value']}%", start_x + (i*spacing), 0.95, 1.0, 0.5, 18, bold=True)
        add_text(slide, kpi["label"], start_x + (i*spacing), 1.7, 1.0, 0.3, 10, bold=True)
        
        # Clean up temp image
        if os.path.exists(img_path):
            os.remove(img_path)

    # Add Digital Readout Target/Actual Widgets next to rings
    target_start = start_x + (len(kpi_data) * spacing) + 0.5
    for i, label in enumerate(["Production Actual", "Production Target"]):
        box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(target_start + (i*2.2)), Inches(0.7), Inches(1.8), Inches(1.0))
        set_shape_color(box, (50, 50, 55))
        add_text(slide, label, target_start + (i*2.2), 0.75, 1.8, 0.3, 10, color=(200, 200, 200))
        add_text(slide, str(89 if i==0 else 100), target_start + (i*2.2), 1.0, 1.8, 0.5, 28, bold=True, color=(255, 255, 255))

    # --- Layer 3: Process Schematic (Middle Panel) ---
    # Conveyor Belt
    belt = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(4.5), Inches(11.3), Inches(0.3))
    set_shape_color(belt, conveyor_grey)
    
    # Conveyor Rollers (Under belt)
    for i in range(15):
        roller = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(1.2 + (i*0.75)), Inches(4.8), Inches(0.2), Inches(0.2))
        set_shape_color(roller, machine_grey)

    # Machine Body Left
    machine_l = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(2.8), Inches(1.5), Inches(1.7))
    set_shape_color(machine_l, machine_grey, line_rgb=(70, 70, 75))
    # Control screen on machine
    screen = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(3.0), Inches(1.1), Inches(0.8))
    set_shape_color(screen, (20, 20, 30))
    add_text(slide, "SYS OK\n42 rpm", 1.2, 3.1, 1.1, 0.6, 10, color=(46, 204, 113))

    # Product Boxes on Conveyor
    box_positions = [3.5, 6.0, 9.5]
    for bx in box_positions:
        box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(bx), Inches(3.8), Inches(1.2), Inches(0.7))
        set_shape_color(box, (205, 170, 125), line_rgb=(139, 115, 85)) # Cardboard brown
        # Box label
        add_text(slide, "PN-748", bx, 4.0, 1.2, 0.3, 8)

    # Overhead Sensor/Arm
    arm_base = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.8), Inches(2.2), Inches(1.6), Inches(0.4))
    set_shape_color(arm_base, machine_grey)
    arm_drop = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.5), Inches(2.6), Inches(0.2), Inches(1.0))
    set_shape_color(arm_drop, machine_grey)
    sensor_head = slide.shapes.add_shape(MSO_SHAPE.CHEVRON, Inches(6.3), Inches(3.6), Inches(0.6), Inches(0.2))
    set_shape_color(sensor_head, (200, 50, 50)) # Red sensor

    # Value Display floating above sensor
    val_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.8), Inches(2.8), Inches(1.6), Inches(0.7))
    set_shape_color(val_box, (240, 240, 240), line_rgb=(150, 150, 150))
    add_text(slide, "52 m/sec\n25 °C", 5.8, 2.9, 1.6, 0.6, 12, bold=True)

    # Status LEDs (Red/Green Stack)
    for led_x in [3.0, 8.5]:
        pole = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(led_x), Inches(2.5), Inches(0.1), Inches(1.0))
        set_shape_color(pole, machine_grey)
        led_green = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(led_x - 0.1), Inches(2.3), Inches(0.3), Inches(0.3))
        set_shape_color(led_green, (46, 204, 113)) # Active green
        led_red = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(led_x - 0.1), Inches(2.0), Inches(0.3), Inches(0.3))
        set_shape_color(led_red, (100, 30, 30)) # Dimmed red

    # --- Layer 4: Data Table (Bottom Panel) ---
    add_text(slide, "System Tag Monitor", 0.4, 5.7, 3.0, 0.3, 11, bold=True, align=PP_ALIGN.LEFT)
    
    rows, cols = 4, 5
    table_shape = slide.shapes.add_table(rows, cols, Inches(0.4), Inches(6.0), Inches(12.5), Inches(1.1))
    table = table_shape.table

    # Set column widths
    col_widths = [Inches(2.5), Inches(2.5), Inches(2.5), Inches(2.5), Inches(2.5)]
    for i, width in enumerate(col_widths):
        table.columns[i].width = width

    # Define Data
    table_data = [
        ["Tag Name", "Value", "Function", "Min", "Max"],
        ["Selection 1 : eWON Tag", "True", "Toggle", "0", "1"],
        ["KPI 01 : Value", "73", "None", "0", "100"],
        ["Machine Speed : PLC_V1", "42", "Ramp", "0", "60"]
    ]

    # Populate Table and format
    for r in range(rows):
        for c in range(cols):
            cell = table.cell(r, c)
            cell.text = table_data[r][c]
            
            # Formatting text
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(10)
            p.font.name = "Arial"
            
            # Header formatting
            if r == 0:
                p.font.bold = True
                p.font.color.rgb = RGBColor(255, 255, 255)
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(100, 100, 105)
            else:
                p.font.color.rgb = RGBColor(50, 50, 50)
                cell.fill.solid()
                # Alternating row colors
                if r % 2 == 0:
                    cell.fill.fore_color.rgb = RGBColor(225, 225, 230)
                else:
                    cell.fill.fore_color.rgb = RGBColor(235, 235, 240)

    prs.save(output_pptx_path)
    return output_pptx_path
