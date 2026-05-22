def create_slide(
    output_pptx_path: str,
    title_text: str = "色块封面制作大法",
    subtitle_text: str = "最简单的操作 | 最救急的技能 | 10秒做好一页PPT",
    speaker_text: str = "课程讲解：Jesse老师",
    primary_color: tuple = (23, 74, 124),   # Deep Blue
    secondary_color: tuple = (33, 115, 196) # Bright Blue
) -> str:
    """
    Create a PPTX file reproducing the "Off-Canvas Geometric Masking" visual effect.
    """
    import math
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN

    prs = Presentation()
    # Set to 16:9 widescreen
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # Helper function to remove shape borders
    def clear_border(shape):
        shape.line.fill.background()

    # === Layer 1: Off-Canvas Geometric Masking ===
    
    # We want two adjacent rectangles, rotated by 30 degrees.
    # To place them perfectly side-by-side after rotation, we calculate 
    # the shift of their center points along the rotated local X-axis.
    
    rotation_angle = 30 # degrees
    rect_width = Inches(3.0)
    rect_height = Inches(15.0) # Extra long to ensure it bleeds off the canvas
    
    # Center point for the first (Primary Color) rectangle
    cx1 = Inches(1.0)
    cy1 = Inches(7.5)
    
    # Calculate Center point for the second (Secondary Color) rectangle
    # Shifted exactly by 'rect_width' along the 30-degree tilted axis
    angle_rad = math.radians(rotation_angle)
    cx2 = cx1 + rect_width * math.cos(angle_rad)
    cy2 = cy1 + rect_width * math.sin(angle_rad)
    
    # Convert centers back to top-left coords (which python-pptx expects before rotation)
    left1 = cx1 - (rect_width / 2)
    top1 = cy1 - (rect_height / 2)
    
    left2 = cx2 - (rect_width / 2)
    top2 = cy2 - (rect_height / 2)

    # Add Primary Dark Blue Rectangle
    shape1 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left1, top1, rect_width, rect_height)
    shape1.rotation = rotation_angle
    shape1.fill.solid()
    shape1.fill.fore_color.rgb = RGBColor(*primary_color)
    clear_border(shape1)

    # Add Secondary Light Blue Rectangle
    shape2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left2, top2, rect_width, rect_height)
    shape2.rotation = rotation_angle
    shape2.fill.solid()
    shape2.fill.fore_color.rgb = RGBColor(*secondary_color)
    clear_border(shape2)


    # === Layer 2: Text & Content ===

    # Main Title
    title_box = slide.shapes.add_textbox(Inches(5.0), Inches(2.5), Inches(7.5), Inches(1.5))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.alignment = PP_ALIGN.RIGHT
    p.font.size = Pt(54)
    p.font.bold = True
    p.font.name = "Microsoft YaHei"
    p.font.color.rgb = RGBColor(40, 40, 40)

    # Subtitle
    sub_box = slide.shapes.add_textbox(Inches(5.0), Inches(4.0), Inches(7.5), Inches(0.8))
    tf_sub = sub_box.text_frame
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = subtitle_text
    p_sub.alignment = PP_ALIGN.RIGHT
    p_sub.font.size = Pt(18)
    p_sub.font.name = "Microsoft YaHei"
    p_sub.font.color.rgb = RGBColor(120, 120, 120)

    # Speaker Badge (Small rectangle acting as a label background)
    badge_width = Inches(2.5)
    badge_height = Inches(0.5)
    badge_left = Inches(10.0)
    badge_top = Inches(4.8)
    
    badge = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, badge_left, badge_top, badge_width, badge_height)
    badge.fill.solid()
    badge.fill.fore_color.rgb = RGBColor(*secondary_color)
    clear_border(badge)
    
    tf_badge = badge.text_frame
    tf_badge.vertical_anchor = MSO_SHAPE.RECTANGLE
    p_badge = tf_badge.paragraphs[0]
    p_badge.text = speaker_text
    p_badge.alignment = PP_ALIGN.CENTER
    p_badge.font.size = Pt(14)
    p_badge.font.name = "Microsoft YaHei"
    p_badge.font.color.rgb = RGBColor(255, 255, 255)

    prs.save(output_pptx_path)
    return output_pptx_path
