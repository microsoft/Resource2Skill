from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_THEME_COLOR
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN

def add_flowchart_shape(slide, shape_type, text, left, top, width, height):
    """Helper function to add a flowchart shape with standardized formatting."""
    shape = slide.shapes.add_shape(shape_type, left, top, width, height)
    
    # Shape Formatting
    fill = shape.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(255, 255, 255)
    
    line = shape.line
    line.color.rgb = RGBColor(68, 84, 106)
    line.width = Pt(1.5)
    
    # Text Formatting
    text_frame = shape.text_frame
    text_frame.text = text
    text_frame.margin_bottom = Inches(0.05)
    text_frame.margin_top = Inches(0.05)
    text_frame.margin_left = Inches(0.1)
    text_frame.margin_right = Inches(0.1)
    text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.font.name = 'Helvetica'
    p.font.size = Pt(14)
    p.font.color.rgb = RGBColor(0, 0, 0)
    
    return shape

def add_connector_arrow(slide, begin_shape, end_shape, begin_conn_site=2, end_conn_site=0):
    """Helper function to connect two shapes with an arrow."""
    connector = slide.shapes.add_connector(
        MSO_CONNECTOR.STRAIGHT, 
        begin_shape.connector_sites[begin_conn_site].position[0],
        begin_shape.connector_sites[begin_conn_site].position[1],
        end_shape.connector_sites[end_conn_site].position[0],
        end_shape.connector_sites[end_conn_site].position[1]
    )
    connector.line.color.rgb = RGBColor(68, 84, 106)
    connector.line.width = Pt(1.5)
    connector.line.end_arrowhead_style = 2  # Arrow style
    return connector

def create_flowchart_slide(
    output_pptx_path: str,
    title_text: str = "公司請假審批流程",
    **kwargs,
) -> str:
    """
    Creates a PPTX slide with a structured process flowchart,
    reproducing the leave application example from the tutorial.

    Returns: path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_slide_layout)

    # Add a title
    title_shape = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(12.33), Inches(0.5))
    title_tf = title_shape.text_frame
    p = title_tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.name = 'Helvetica'
    p.alignment = PP_ALIGN.CENTER

    # Define shape dimensions and positions
    proc_w, proc_h = Inches(2.0), Inches(1.0)
    dec_w, dec_h = Inches(2.5), Inches(1.5)
    term_w, term_h = Inches(1.5), Inches(0.75)
    
    center_x = prs.slide_width / 2

    # === Create Flowchart Elements ===
    # 1. Start
    start_shape = add_flowchart_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, "Start", center_x - term_w/2, Inches(1.0), term_w, term_h)
    
    # 2. Apply for Leave
    apply_shape = add_flowchart_shape(slide, MSO_SHAPE.RECTANGLE, "申請請假", center_x - proc_w/2, Inches(2.0), proc_w, proc_h)

    # 3. Decision: Check number of days
    decision_days = add_flowchart_shape(slide, MSO_SHAPE.DIAMOND, "判斷請假天數", center_x - dec_w/2, Inches(3.25), dec_w, dec_h)

    # 4a. Process: Department Manager Approval
    dept_approve = add_flowchart_shape(slide, MSO_SHAPE.RECTANGLE, "部門主管審批", center_x - dec_w - Inches(0.25), Inches(4.75), proc_w, proc_h)

    # 4b. Process: HR Approval
    hr_approve = add_flowchart_shape(slide, MSO_SHAPE.RECTANGLE, "HR人事審批", center_x + dec_w/2 + Inches(0.25), Inches(4.75), proc_w, proc_h)
    
    # 5. Decision: Approved?
    decision_final = add_flowchart_shape(slide, MSO_SHAPE.DIAMOND, "是否通過", center_x - dec_w/2, Inches(5.0), dec_w, dec_h)

    # 6. Process: Send Email
    send_email = add_flowchart_shape(slide, MSO_SHAPE.RECTANGLE, "發送Email通知", center_x - proc_w/2, Inches(6.25), proc_w, proc_h)
    
    # 7. End
    end_shape = add_flowchart_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, "End", center_x - term_w/2, Inches(7.5) - Inches(1.0), term_w, term_h)

    # === Connect the Shapes ===
    add_connector_arrow(slide, start_shape, apply_shape, 2, 0)
    add_connector_arrow(slide, apply_shape, decision_days, 2, 0)

    # Branching from first decision
    conn_to_dept = add_connector_arrow(slide, decision_days, dept_approve, 3, 0)
    slide.shapes.add_textbox(conn_to_dept.begin_x - Inches(0.5), conn_to_dept.begin_y, Inches(0.4), Inches(0.2)).text_frame.text = "< 5"
    
    conn_to_hr = add_connector_arrow(slide, decision_days, hr_approve, 1, 0)
    slide.shapes.add_textbox(conn_to_hr.begin_x + Inches(0.1), conn_to_hr.begin_y, Inches(0.4), Inches(0.2)).text_frame.text = ">= 6"

    # Merging to second decision (Manually create elbow connectors for aesthetics)
    # Connector from Dept to Final Decision
    connector1_part1 = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, dept_approve.left + proc_w/2, dept_approve.top + proc_h, dept_approve.left + proc_w/2, decision_final.top + dec_h/2)
    connector1_part2 = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, dept_approve.left + proc_w/2, decision_final.top + dec_h/2, decision_final.left, decision_final.top + dec_h/2)
    connector1_part2.line.end_arrowhead_style = 2
    
    # Connector from HR to Final Decision
    connector2_part1 = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, hr_approve.left + proc_w/2, hr_approve.top + proc_h, hr_approve.left + proc_w/2, decision_final.top + dec_h/2)
    connector2_part2 = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, hr_approve.left + proc_w/2, decision_final.top + dec_h/2, decision_final.left + dec_w, decision_final.top + dec_h/2)
    connector2_part2.line.end_arrowhead_style = 2
    
    # Final path
    add_connector_arrow(slide, decision_final, send_email, 2, 0)
    slide.shapes.add_textbox(send_email.left - Inches(0.5), send_email.top - Inches(0.4), Inches(0.4), Inches(0.2)).text_frame.text = "是"
    
    add_connector_arrow(slide, send_email, end_shape, 2, 0)

    prs.save(output_pptx_path)
    return output_pptx_path

# Example Usage:
# if __name__ == '__main__':
#     create_flowchart_slide("flowchart_example.pptx")

