import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN

def create_slide(
    output_pptx_path: str,
    main_title: str = "技术部员工技能培训",
    intro_text: str = "员工培训是指一定组织为开展业务及培育人才的需要，采用各种方式对员工进行有目的、有计划的培养和训练的管理活动。公开课、内训、等均为常见的员工培训企业培训形式。",
    columns_data: list = None,
    header_color: tuple = (23, 60, 136), # Corporate Blue
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the "High-Contrast Header & Horizontal Grid" layout.
    """
    if columns_data is None:
        columns_data = [
            {"title": "提取技术法", "body": "通过现代教学技术（如投影仪、DVD、录像机等工具），对员工进行培训。"},
            {"title": "案例研讨法", "body": "通过向培训对象提供有关背景材料，让其寻找合适的解决方法。这一方式比较客观、实际。"},
            {"title": "角色扮演法", "body": "培训对象在设定情境中扮演某种角色，利用这一角色的身份来处理各种问题。"},
            {"title": "阶梯培训法", "body": "根据不同层级和职位的员工定制不同的培训计划，逐步提升专业技能和管理能力。"}
        ]

    # Initialize presentation (16:9)
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank slide layout
    blank_slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_slide_layout)

    # ==========================================
    # Layer 1: Top Header Block (The "Container")
    # ==========================================
    header_height = Inches(2.6)
    bg_shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 
        0, 0, prs.slide_width, header_height
    )
    # Style the background block
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = RGBColor(*header_color)
    bg_shape.line.fill.background() # Remove border

    # ==========================================
    # Layer 2: Header Text (Macro Information)
    # ==========================================
    # Main Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.8))
    tf = title_box.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.text = main_title
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)

    # Intro Paragraph
    intro_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.2), Inches(11.7), Inches(1.0))
    tf_intro = intro_box.text_frame
    tf_intro.word_wrap = True
    p_intro = tf_intro.paragraphs[0]
    p_intro.text = intro_text
    p_intro.font.size = Pt(16)
    p_intro.font.color.rgb = RGBColor(230, 230, 230) # Light gray for readability
    p_intro.line_spacing = 1.3

    # ==========================================
    # Layer 3: The Horizontal Grid (Micro Details)
    # ==========================================
    margin_x = Inches(0.8)
    margin_y = Inches(3.2) # Start slightly below the header block
    gap = Inches(0.4)
    
    num_cols = len(columns_data)
    # Calculate exact width for each column to fit perfectly within margins
    usable_width = prs.slide_width - (2 * margin_x)
    col_width = (usable_width - (gap * (num_cols - 1))) / num_cols
    
    for idx, col in enumerate(columns_data):
        current_x = margin_x + (idx * (col_width + gap))
        
        # 1. Column Title
        title_box = slide.shapes.add_textbox(current_x, margin_y, col_width, Inches(0.5))
        tf_col = title_box.text_frame
        p_col = tf_col.paragraphs[0]
        p_col.text = col["title"]
        p_col.font.size = Pt(20)
        p_col.font.bold = True
        p_col.font.color.rgb = RGBColor(*header_color) # Tie back to header color
        
        # 2. Serial Number (e.g., "PART 01")
        part_box = slide.shapes.add_textbox(current_x, margin_y - Inches(0.1), col_width, Inches(0.4))
        tf_part = part_box.text_frame
        p_part = tf_part.paragraphs[0]
        p_part.alignment = PP_ALIGN.RIGHT
        p_part.text = f"PART {idx+1:02d}"
        p_part.font.size = Pt(12)
        p_part.font.bold = True
        p_part.font.color.rgb = RGBColor(180, 180, 180) # Subtle gray
        
        # 3. Divider Line
        line_y = margin_y + Inches(0.6)
        line = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, current_x, line_y, current_x + col_width, line_y)
        line.line.color.rgb = RGBColor(200, 200, 200) # Light gray line
        line.line.width = Pt(1.5)
        
        # 4. Body Text
        body_box = slide.shapes.add_textbox(current_x, line_y + Inches(0.1), col_width, Inches(2.5))
        tf_body = body_box.text_frame
        tf_body.word_wrap = True
        p_body = tf_body.paragraphs[0]
        p_body.text = col["body"]
        p_body.font.size = Pt(14)
        p_body.font.color.rgb = RGBColor(80, 80, 80) # Charcoal text
        p_body.line_spacing = 1.3

    # Save the file
    prs.save(output_pptx_path)
    return output_pptx_path

# Example execution:
# create_slide("optimized_efficiency_layout.pptx")
