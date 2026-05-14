import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_THEME_COLOR
from pptx.enum.text import PP_ALIGN

def create_slide(
    output_pptx_path: str = "network_diagram.pptx",
    **kwargs,
) -> str:
    """
    Creates a PPTX slide with an annotated network topology diagram.

    This function reproduces the visual style of explaining network segments
    by overlaying numbered labels on a clean, symbolic network map.

    Returns:
        str: The path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_slide_layout)

    # Define colors
    BG_COLOR = RGBColor(255, 255, 255)
    DEVICE_BLUE = RGBColor(79, 129, 189)
    END_DEVICE_GREY = RGBColor(128, 128, 128)
    LINE_COLOR = RGBColor(0, 0, 0)
    
    # Set background color
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = BG_COLOR

    # --- Device Definitions ---
    # {name: (shape_type, left, top, width, height, color, text)}
    devices = {
        'R1': (MSO_SHAPE.OVAL, Inches(2), Inches(1), Inches(1), Inches(1), DEVICE_BLUE, 'R1'),
        'R2': (MSO_SHAPE.OVAL, Inches(10), Inches(1), Inches(1), Inches(1), DEVICE_BLUE, 'R2'),
        'R3': (MSO_SHAPE.OVAL, Inches(3.5), Inches(3), Inches(1), Inches(1), DEVICE_BLUE, 'R3'),
        'R4': (MSO_SHAPE.OVAL, Inches(8.5), Inches(4), Inches(1), Inches(1), DEVICE_BLUE, 'R4'),
        'S1': (MSO_SHAPE.RECTANGLE, Inches(4.5), Inches(5.5), Inches(1), Inches(0.75), DEVICE_BLUE, 'S1'),
        'S2': (MSO_SHAPE.RECTANGLE, Inches(11), Inches(3), Inches(1), Inches(0.75), DEVICE_BLUE, 'S2'),
        'PC1': (MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(1.125), Inches(0.75), Inches(0.5), END_DEVICE_GREY, 'PC1'),
        'PC2': (MSO_SHAPE.RECTANGLE, Inches(12), Inches(1.125), Inches(0.75), Inches(0.5), END_DEVICE_GREY, 'PC2'),
        'PC3': (MSO_SHAPE.RECTANGLE, Inches(12), Inches(4.125), Inches(0.75), Inches(0.5), END_DEVICE_GREY, 'PC3'),
        'PC4': (MSO_SHAPE.RECTANGLE, Inches(2.5), Inches(6.5), Inches(0.75), Inches(0.5), END_DEVICE_GREY, 'PC4'),
        'PC5': (MSO_SHAPE.RECTANGLE, Inches(4.75), Inches(6.5), Inches(0.75), Inches(0.5), END_DEVICE_GREY, 'PC5'),
        'PC6': (MSO_SHAPE.RECTANGLE, Inches(7), Inches(6.5), Inches(0.75), Inches(0.5), END_DEVICE_GREY, 'PC6'),
    }

    device_shapes = {}
    for name, (shape_type, left, top, width, height, color, text) in devices.items():
        shape = slide.shapes.add_shape(shape_type, left, top, width, height)
        shape.text = text
        p = shape.text_frame.paragraphs[0]
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.alignment = PP_ALIGN.CENTER

        fill = shape.fill
        fill.solid()
        fill.fore_color.rgb = color
        
        line = shape.line
        line.fill.background() # No line
        
        device_shapes[name] = shape

    # --- Connection Definitions ---
    # (start_device, end_device)
    connections = [
        ('PC1', 'R1'), ('R1', 'R2'), ('PC2', 'R2'), ('R1', 'R3'),
        ('R2', 'R3'), ('R3', 'R4'), ('R2', 'S2'), ('R4', 'S2'),
        ('S2', 'PC3'), ('R3', 'S1'), ('R4', 'S1'), ('S1', 'PC4'),
        ('S1', 'PC5'), ('S1', 'PC6')
    ]

    for start_name, end_name in connections:
        start_shape = device_shapes[start_name]
        end_shape = device_shapes[end_name]
        connector = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, 0, 0, 0, 0)
        
        # Connect the shapes
        connector.begin_x = start_shape.left + start_shape.width // 2
        connector.begin_y = start_shape.top + start_shape.height // 2
        connector.end_x = end_shape.left + end_shape.width // 2
        connector.end_y = end_shape.top + end_shape.height // 2

        # Style connector line
        line = connector.line
        line.color.rgb = LINE_COLOR
        line.width = Pt(1.5)

    # --- Annotation Definitions ---
    # (number, left, top)
    annotations = [
        ('1', Inches(1.4), Inches(0.7)),
        ('2', Inches(6), Inches(0.7)),
        ('3', Inches(11.1), Inches(0.7)),
        ('4', Inches(2.9), Inches(2.2)),
        ('5', Inches(7), Inches(2.2)),
        ('6', Inches(11.2), Inches(2.2)),
        ('7', Inches(6.25), Inches(3.7)),
        ('8', Inches(3.5), Inches(4.7)),
    ]
    
    label_size = Inches(0.3)
    for num, left, top in annotations:
        textbox = slide.shapes.add_textbox(left, top, label_size, label_size)
        
        # Style textbox fill and line
        fill = textbox.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(255, 255, 255)
        line = textbox.line
        line.color.rgb = RGBColor(0, 0, 0)
        line.width = Pt(1)

        # Style text
        tf = textbox.text_frame
        tf.clear() # remove default paragraph
        p = tf.paragraphs[0]
        p.text = num
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = RGBColor(0, 0, 0)
        p.alignment = PP_ALIGN.CENTER
        tf.margin_bottom = 0
        tf.margin_top = 0
        tf.margin_left = 0
        tf.margin_right = 0

    prs.save(output_pptx_path)
    return output_pptx_path

# Example of how to run the function
if __name__ == '__main__':
    file_path = create_slide()
    print(f"Presentation saved to: {file_path}")
    # To open the file on Windows
    if os.name == 'nt':
        os.startfile(file_path)
