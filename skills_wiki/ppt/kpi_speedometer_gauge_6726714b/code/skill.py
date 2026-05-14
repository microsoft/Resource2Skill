import math
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.dml import MSO_FILL
from lxml import etree
from pptx.oxml.ns import qn

def create_slide(
    output_pptx_path: str,
 техническое описание, please.
    percentage: float = 75.0,
    title_text: str = "Sales Performance Dashboard",
) -> str:
    """
    Creates a PowerPoint slide with a KPI speedometer gauge.

    Args:
        output_pptx_path (str): The path to save the generated PPTX file.
        percentage (float): The percentage value (0-100) to display on the gauge.
        title_text (str): The title for the slide.

    Returns:
        str: The path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(16)
    prs.slide_height = Inches(9)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: Background & Title ===
    background = slide.background
    background.fill.solid()
    background.fill.fore_color.rgb = RGBColor(240, 240, 240)

    title_shape = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(14), Inches(1))
    title_shape.text_frame.text = title_text
    title_shape.text_frame.paragraphs[0].font.size = Pt(36)
    title_shape.text_frame.paragraphs[0].font.bold = True
    title_shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(89, 89, 89)

    # === Layer 2: Gauge Panel and Face ===
    # Panel Background (Rounded Rectangle)
    panel_left = Inches(3)
    panel_top = Inches(1.5)
    panel_width = Inches(10)
    panel_height = Inches(5.5)
    
    panel = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, panel_left, panel_top, panel_width, panel_height
    )
    fill = panel.fill
    fill.gradient()
    fill.gradient_stops[0].color.rgb = RGBColor(47, 82, 122)
    fill.gradient_stops[1].color.rgb = RGBColor(28, 68, 119)
    panel.line.fill.background()

    # Gauge Arc
    gauge_size = Inches(8)
    arc = slide.shapes.add_shape(
        MSO_SHAPE.BLOCK_ARC,
        panel_left + Inches(1),
        panel_top + Inches(1),
        gauge_size,
        gauge_size,
    )
    # Adjust arc to be a 180-degree semicircle
    arc.adjustments[0] = 180000 # End angle (180 degrees)
    arc.adjustments[1] = 0     # Start angle (0 degrees)
    arc.adjustments[2] = 20000 # Thickness
    
    # Rotate the arc to be a lower semicircle
    arc_sp = arc.element
    arc_sp.spPr.xfrm.set('rot', str(int(90 * 60000))) # Rotate 90 degrees
    
    arc.fill.solid()
    arc.fill.fore_color.rgb = RGBColor(238, 236, 225)
    arc.line.fill.background()

    # Add Labels and Divider Lines
    gauge_center_x = panel_left + panel_width / 2
    gauge_center_y = panel_top + Inches(1) + gauge_size / 2
    radius = gauge_size / 2 - Inches(0.4)

    labels_data = {
        "0%": 180, "25%": 135, "50%": 90, "75%": 45, "100%": 0
    }

    for text, angle_deg in labels_data.items():
        angle_rad = math.radians(angle_deg)
        # Labels
        label_radius = radius + Inches(0.5)
        lx = gauge_center_x + label_radius * math.cos(angle_rad) - Inches(0.25)
        ly = gauge_center_y - label_radius * math.sin(angle_rad) - Inches(0.15)
        
        label_box = slide.shapes.add_textbox(lx, ly, Inches(0.5), Inches(0.3))
        p = label_box.text_frame.paragraphs[0]
        p.text = text
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.font.size = Pt(16)
        p.font.bold = True
        
        # Divider lines
        line_start_x = gauge_center_x + (radius - Inches(0.2)) * math.cos(angle_rad)
        line_start_y = gauge_center_y - (radius - Inches(0.2)) * math.sin(angle_rad)
        line_end_x = gauge_center_x + (radius + Inches(0.2)) * math.cos(angle_rad)
        line_end_y = gauge_center_y - (radius + Inches(0.2)) * math.sin(angle_rad)

        line = slide.shapes.add_connector(1, line_start_x, line_start_y, line_end_x, line_end_y) # 1 = Straight connector
        line.line.fill.solid()
        line.line.fill.fore_color.rgb = RGBColor(89, 89, 89)
        line.line.width = Pt(2)

    # === Layer 3: The Pointer ===
    pointer = slide.shapes.add_shape(
        MSO_SHAPE.ISOSCELES_TRIANGLE,
        gauge_center_x - Inches(0.1),
        panel_top,
        Inches(0.2),
        radius + Inches(0.1)
    )
    pointer.fill.solid()
    pointer.fill.fore_color.rgb = RGBColor(89, 89, 89)
    pointer.line.fill.background()

    # Calculate rotation. 0% = -90deg, 100% = +90deg
    # The default triangle shape points up (0 deg), so we adjust from there.
    # Total span is 180 degrees.
    clamped_percentage = max(0, min(100, percentage))
    rotation_degrees = (clamped_percentage / 100.0) * 180 - 90

    # Apply rotation using lxml
    sp = pointer.element
    spPr = sp.spPr
    xfrm = spPr.find(qn('a:xfrm'))
    if xfrm is None:
        xfrm = etree.SubElement(spPr, qn('a:xfrm'))
    xfrm.set('rot', str(int(rotation_degrees * 60000)))

    # Pivot Circle
    pivot_size = Inches(0.3)
    pivot = slide.shapes.add_shape(
        MSO_SHAPE.OVAL,
        gauge_center_x - pivot_size / 2,
        gauge_center_y - pivot_size / 2,
        pivot_size,
        pivot_size,
    )
    pivot.fill.solid()
    pivot.fill.fore_color.rgb = RGBColor(89, 89, 89)
    pivot.line.fill.background()
    
    prs.save(output_pptx_path)
    return output_pptx_path

# Example Usage:
# if __name__ == '__main__':
#     create_slide("kpi_gauge_dashboard.pptx", percentage=83, title_text="Q3 Project Completion")

