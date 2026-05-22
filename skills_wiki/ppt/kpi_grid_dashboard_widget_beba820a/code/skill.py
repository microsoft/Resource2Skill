import collections.abc
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

def create_slide(
    output_pptx_path: str,
    widget_title: str = "Status: Top Five Employees",
    accent_color_rgb: tuple = (47, 85, 151),
    **kwargs,
) -> str:
    """
    Creates a PPTX slide with a KPI Grid Dashboard Widget.

    This function reproduces the "Top Five Employees" performance widget
    showcased in the "Dashboard Beyond Charts" tutorial.

    Args:
        output_pptx_path: The path to save the generated .pptx file.
        widget_title: The title to display on the widget.
        accent_color_rgb: The RGB tuple for the widget's header bar.

    Returns:
        The path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_slide_layout)

    # === Layer 1: Slide Background ===
    background = slide.background
    background.fill.solid()
    background.fill.fore_color.rgb = RGBColor(0, 0, 0)

    # === Sample Data (as seen in the tutorial) ===
    employee_data = [
        {'name': 'Andrew', 'status': 'good', 'monthly_sales': [1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1], 'sales_target': 23719},
        {'name': 'Janet', 'status': 'good', 'monthly_sales':  [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0], 'sales_target': 19172},
        {'name': 'Laura', 'status': 'warning', 'monthly_sales': [0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0], 'sales_target': 15112},
        {'name': 'Margaret', 'status': 'bad', 'monthly_sales':  [1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1], 'sales_target': 31997},
        {'name': 'Nancy', 'status': 'good', 'monthly_sales':  [1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1], 'sales_target': 27765},
    ]

    # === Color Palette ===
    COLOR_WHITE = RGBColor(255, 255, 255)
    COLOR_ACCENT = RGBColor.from_rgb(*accent_color_rgb)
    COLOR_GRID_FILL = RGBColor(146, 208, 80)
    COLOR_TARGET_BAR = RGBColor(237, 125, 49)
    STATUS_COLORS = {
        'good': RGBColor(0, 176, 80),
        'warning': RGBColor(255, 192, 0),
        'bad': RGBColor(255, 0, 0)
    }

    # === Widget Dimensions & Positioning ===
    WIDGET_X, WIDGET_Y = Inches(1), Inches(1.5)
    WIDGET_WIDTH, WIDGET_HEIGHT = Inches(11.33), Inches(4.5)

    # === Layer 2: Widget Container & Header ===
    # Main container
    container = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, WIDGET_X, WIDGET_Y, WIDGET_WIDTH, WIDGET_HEIGHT)
    container.fill.solid()
    container.fill.fore_color.rgb = RGBColor(31, 31, 31)
    container.line.fill.solid()
    container.line.fill.fore_color.rgb = RGBColor(128, 128, 128)
    
    # Header Bar
    header_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, WIDGET_X, WIDGET_Y, WIDGET_WIDTH, Inches(0.1))
    header_bar.fill.solid()
    header_bar.fill.fore_color.rgb = COLOR_ACCENT
    header_bar.line.fill.none()
    
    # Widget Title
    title_box = slide.shapes.add_textbox(WIDGET_X + Inches(0.2), WIDGET_Y + Inches(0.2), Inches(5), Inches(0.5))
    p = title_box.text_frame.paragraphs[0]
    p.text = widget_title
    p.font.name = 'Calibri'
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE

    # === Layer 3: Column Headers ===
    HEADER_Y = WIDGET_Y + Inches(0.8)
    headers = {
        "Status": Inches(0.3),
        "Top Five Employees": Inches(1.1),
        "Monthly total sales revenue": Inches(3.5),
        "Sales Target": Inches(8.5)
    }
    for text, x_offset in headers.items():
        tb = slide.shapes.add_textbox(WIDGET_X + x_offset, HEADER_Y, Inches(3), Inches(0.3))
        p = tb.text_frame.paragraphs[0]
        p.text = text
        p.font.name = 'Calibri'
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_WHITE

    # === Layer 4: Employee Data Rows ===
    START_Y = HEADER_Y + Inches(0.5)
    ROW_HEIGHT = Inches(0.6)
    
    for i, employee in enumerate(employee_data):
        current_y = START_Y + (i * ROW_HEIGHT)

        # Column 1: Status Circle
        status_shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, WIDGET_X + Inches(0.4), current_y, Inches(0.25), Inches(0.25))
        status_shape.fill.solid()
        status_shape.fill.fore_color.rgb = STATUS_COLORS.get(employee['status'], RGBColor(128, 128, 128))
        status_shape.line.fill.none()

        # Column 2: Employee Name
        name_tb = slide.shapes.add_textbox(WIDGET_X + headers["Top Five Employees"], current_y - Inches(0.1), Inches(2), Inches(0.5))
        p = name_tb.text_frame.paragraphs[0]
        p.text = employee['name']
        p.font.name = 'Calibri'
        p.font.size = Pt(14)
        p.font.color.rgb = COLOR_WHITE
    
        # Column 3: Monthly Sales Grid
        GRID_START_X = WIDGET_X + headers["Monthly total sales revenue"]
        CELL_SIZE = Inches(0.2)
        CELL_SPACING = Inches(0.05)
        for month_idx, sales_achieved in enumerate(employee['monthly_sales']):
            cell_x = GRID_START_X + (month_idx * (CELL_SIZE + CELL_SPACING))
            
            # Background cell
            bg_cell = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, cell_x, current_y, CELL_SIZE, CELL_SIZE)
            bg_cell.fill.solid()
            bg_cell.fill.fore_color.rgb = COLOR_WHITE
            bg_cell.line.fill.solid()
            bg_cell.line.fill.fore_color.rgb = RGBColor(200, 200, 200)

            # Foreground fill if sales target met
            if sales_achieved:
                fill_cell = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, cell_x, current_y, CELL_SIZE, CELL_SIZE)
                fill_cell.fill.solid()
                fill_cell.fill.fore_color.rgb = COLOR_GRID_FILL
                fill_cell.line.fill.none()
    
        # Column 4: Sales Target Bar
        TARGET_START_X = WIDGET_X + headers["Sales Target"]
        target_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, TARGET_START_X, current_y, Inches(1.5), Inches(0.3))
        target_bar.fill.solid()
        target_bar.fill.fore_color.rgb = COLOR_TARGET_BAR
        target_bar.line.fill.none()
        
        # Sales Target Text
        target_text_box = slide.shapes.add_textbox(TARGET_START_X, current_y - Inches(0.05), Inches(1.5), Inches(0.4))
        p = target_text_box.text_frame.paragraphs[0]
        p.text = f"{employee['sales_target']:,}" # Format with commas
        p.font.name = 'Calibri'
        p.font.bold = True
        p.font.size = Pt(14)
        p.font.color.rgb = COLOR_WHITE
        p.alignment = 1 # Center alignment

    prs.save(output_pptx_path)
    return output_pptx_path

