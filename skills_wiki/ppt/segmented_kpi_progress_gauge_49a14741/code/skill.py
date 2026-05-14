import math
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

def create_kpi_dashboard_slide(output_pptx_path: str, kpi_data: list) -> str:
    """
    Creates a PPTX slide with a KPI dashboard featuring segmented progress gauges.

    Args:
        output_pptx_path (str): The path to save the generated PPTX file.
        kpi_data (list): A list of dictionaries, where each dictionary contains:
            'title': str (e.g., "SALES")
            'value': float (e.g., 72)
            'description': str
            'is_increase': bool (True for up/green, False for down/red)

    Returns:
        str: The path to the saved PPTX file.
    """

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # --- Helper function to get arc points ---
    def _get_arc_points(cx, cy, radius, start_angle_deg, end_angle_deg, num_points=10):
        points = []
        angle_step = (end_angle_deg - start_angle_deg) / (num_points - 1)
        for i in range(num_points):
            angle_deg = start_angle_deg + i * angle_step
            angle_rad = math.radians(angle_deg)
            x = cx + radius * math.cos(angle_rad)
            y = cy + radius * math.sin(angle_rad)
            points.append((x, y))
        return points

    # --- Helper function to create one KPI gauge ---
    def create_kpi_gauge(slide, cx_emu, cy_emu, value, title, description, is_increase=True):
        outer_radius = Inches(0.8)
        inner_radius = Inches(0.55)
        num_segments = 10
        segment_angle = 360 / num_segments
        segment_gap = 4 # degrees of gap

        # Colors
        color_increase = RGBColor(118, 184, 43)
        color_decrease = RGBColor(255, 0, 0)
        color_base = RGBColor(230, 230, 230)
        title_color = RGBColor(230, 83, 76)
        body_color = RGBColor(89, 89, 89)

        # Create 10 segments using Freeform shapes
        segments = []
        for i in range(num_segments):
            start_angle_deg = -90 + (i * segment_angle) + (segment_gap / 2)
            end_angle_deg = start_angle_deg + segment_angle - segment_gap

            outer_arc_points = _get_arc_points(cx_emu, cy_emu, outer_radius, start_angle_deg, end_angle_deg)
            inner_arc_points = _get_arc_points(cx_emu, cy_emu, inner_radius, start_angle_deg, end_angle_deg)
            
            path_points = [outer_arc_points[0]] + outer_arc_points + [inner_arc_points[-1]] + inner_arc_points[::-1]
            
            shape = slide.shapes.add_shape(MSO_SHAPE.FREEFORM, 0, 0, 0, 0) # Position and size are set by path
            freeform_builder = shape.freeform_builder
            freeform_builder.add_path(path_points, close=True)
            freeform_builder.close()

            shape.line.fill.background()
            segments.append(shape)

        # Color the segments
        num_to_color = int(round(value / 10.0))
        fill_color = color_increase if is_increase else color_decrease
        
        # Color filled segments
        if is_increase: # Clockwise
            for i in range(num_to_color):
                segments[i].fill.solid()
                segments[i].fill.fore_color.rgb = fill_color
        else: # Anti-clockwise
            for i in range(num_to_color):
                segments[-(i + 1)].fill.solid()
                segments[-(i + 1)].fill.fore_color.rgb = fill_color
                
        # Color unfilled segments
        for shape in segments:
            if not shape.fill.type:
                 shape.fill.solid()
                 shape.fill.fore_color.rgb = color_base
                 
        # Add central arrow
        arrow_size = Inches(0.4)
        arrow = slide.shapes.add_shape(
            MSO_SHAPE.ISOSCELES_TRIANGLE, 
            cx_emu - arrow_size / 2, cy_emu - arrow_size / 2, 
            arrow_size, arrow_size
        )
        arrow.fill.solid()
        arrow.fill.fore_color.rgb = fill_color
        arrow.line.fill.background()
        if not is_increase:
            arrow.rotation = 180
            
        # Add percentage text
        text_box = slide.shapes.add_textbox(cx_emu - Inches(0.75), cy_emu - Inches(0.3), Inches(1.5), Inches(0.6))
        tf = text_box.text_frame
        tf.clear()
        p = tf.paragraphs[0]
        p.text = f"{int(value)}%"
        p.font.name = 'Arial Black'
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = RGBColor(0, 0, 0)
        p.alignment = PP_ALIGN.CENTER
        tf.margin_bottom = 0
        tf.margin_top = 0
        tf.vertical_anchor = 'middle'
        
        # Add Title and Description
        title_box = slide.shapes.add_textbox(cx_emu + Inches(1.2), cy_emu - Inches(0.8), Inches(4), Inches(0.5))
        tf_title = title_box.text_frame
        tf_title.clear()
        p_title = tf_title.paragraphs[0]
        p_title.text = title.upper()
        try:
            p_title.font.name = 'Panton Black Caps' # Use specific font if available
        except:
            p_title.font.name = 'Arial Black' # Fallback font
        p_title.font.size = Pt(16)
        p_title.font.color.rgb = title_color
        
        desc_box = slide.shapes.add_textbox(cx_emu + Inches(1.2), cy_emu - Inches(0.5), Inches(7), Inches(1))
        tf_desc = desc_box.text_frame
        tf_desc.clear()
        p_desc = tf_desc.paragraphs[0]
        p_desc.text = description
        p_desc.font.name = 'Calibri'
        p_desc.font.size = Pt(12)
        p_desc.font.color.rgb = body_color

    # --- Main Slide Content ---
    
    # Add main slide title
    title_shape = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(12.33), Inches(1))
    tf = title_shape.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.text = "YOUR VERY OWN KPI DASHBOARD"
    p.alignment = PP_ALIGN.CENTER
    try:
        p.font.name = "Panton Black Caps"
    except:
        p.font.name = "Arial Black"
    p.font.size = Pt(24)
    p.font.color.rgb = RGBColor(230, 83, 76)

    # Create the KPI gauges based on input data
    start_y = Inches(1.7)
    y_increment = Inches(1.8)
    center_x = Inches(2.5)

    for i, data in enumerate(kpi_data):
        center_y = start_y + (i * y_increment)
        create_kpi_gauge(
            slide,
            cx_emu=int(center_x),
            cy_emu=int(center_y),
            value=data['value'],
            title=data['title'],
            description=data['description'],
            is_increase=data['is_increase']
        )

    prs.save(output_pptx_path)
    return output_pptx_path

# Example Usage:
if __name__ == '__main__':
    lorem_ipsum = "The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog."
    
    kpis = [
        {
            'title': "Sales",
            'value': 72,
            'description': f"Sales have increased by 72% due to the fact that {lorem_ipsum}",
            'is_increase': True
        },
        {
            'title': "Market Outreach",
            'value': 28,
            'description': f"Market outreach has decreased by 28% due to the fact that {lorem_ipsum}",
            'is_increase': False
        },
        {
            'title': "Customer Satisfaction",
            'value': 51,
            'description': f"Customer satisfaction increased by 51% due to the fact that {lorem_ipsum}",
            'is_increase': True
        }
    ]
    
    create_kpi_dashboard_slide("kpi_dashboard.pptx", kpis)
