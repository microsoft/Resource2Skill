def create_slide(
    output_pptx_path: str,
    title_text: str = "多 元 化 创 新 发 展",
    subtitle_text: str = "UNORTHODOX DIVERSIFIED INNOVATION",
    bg_color: tuple = (9, 13, 26),        # Very dark blue
    start_color: tuple = (0, 255, 220),   # Bright Cyan (Inner core)
    end_color: tuple = (25, 45, 90),      # Muted Deep Blue (Outer edges)
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the "Spiraling Abstract Wireframe Tween" visual effect.
    
    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN
    
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank slide

    # === Helper: Linear Interpolation (Lerp) ===
    def lerp(v0, v1, t):
        return v0 + (v1 - v0) * t

    def lerp_color(c0, c1, t):
        return tuple(int(lerp(c0[i], c1[i], t)) for i in range(3))

    # === Layer 1: Solid Dark Background ===
    bg_shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
    )
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = RGBColor(*bg_color)
    bg_shape.line.fill.background() # No line

    # === Layer 2: Tweened Spiraling Wireframe (The Core Effect) ===
    # Define start state (Small, bright, left-center)
    start_w, start_h = Inches(1.0), Inches(1.0)
    start_x, start_y = Inches(3.0), Inches(3.25)
    start_rot = 0
    
    # Define end state (Massive, muted, off-center right)
    end_w, end_h = Inches(18.0), Inches(18.0)
    end_x, end_y = Inches(10.0), Inches(3.75)
    end_rot = 135 # Rotate by 135 degrees over the tween
    
    steps = 45 # Number of intermediate shapes

    # Generate the tweened shapes
    for i in range(steps + 1):
        t = i / steps
        # Apply easing function (ease-in-out) for more organic spacing
        # t_eased = t * t * (3 - 2 * t) 
        # Using a slight ease-in to bunch shapes near the center
        t_eased = t ** 1.5 
        
        cur_w = lerp(start_w, end_w, t_eased)
        cur_h = lerp(start_h, end_h, t_eased)
        
        # Note: PPT requires Top/Left coordinates, so we calculate Center X/Y first, 
        # then offset by half width/height to keep the tween paths anchored properly.
        cur_cx = lerp(start_x, end_x, t_eased)
        cur_cy = lerp(start_y, end_y, t_eased)
        cur_left = cur_cx - (cur_w / 2)
        cur_top = cur_cy - (cur_h / 2)
        
        cur_rot = lerp(start_rot, end_rot, t_eased)
        cur_color = lerp_color(start_color, end_color, t_eased)
        
        # Add the shape
        shape = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, cur_left, cur_top, cur_w, cur_h
        )
        
        # Style the shape: No Fill, Solid Interpolated Line
        shape.fill.background()
        shape.line.color.rgb = RGBColor(*cur_color)
        shape.line.width = Pt(1.25)
        shape.rotation = cur_rot
        
        # Adjust rounded corner radius (optional, PPT XML hack normally, but standard works well enough)
        # By default, python-pptx sets a reasonable rounding radius.

    # === Layer 3: Overlay Text ===
    # Main Title
    title_box = slide.shapes.add_textbox(Inches(1.0), Inches(3.0), Inches(6.0), Inches(1.0))
    tf = title_box.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255) # White
    p.font.name = "Microsoft YaHei"
    
    # Subtitle
    sub_box = slide.shapes.add_textbox(Inches(1.0), Inches(3.8), Inches(6.0), Inches(0.5))
    tf_sub = sub_box.text_frame
    tf_sub.clear()
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = subtitle_text
    p_sub.font.size = Pt(14)
    p_sub.font.color.rgb = RGBColor(150, 160, 180) # Light grey-blue
    p_sub.font.letter_spacing = Pt(3) # Increase tracking for modern look
    p_sub.font.name = "Arial"

    # Brand / Corner Tag
    tag_box = slide.shapes.add_textbox(Inches(1.0), Inches(1.0), Inches(3.0), Inches(0.5))
    p_tag = tag_box.text_frame.paragraphs[0]
    p_tag.text = "旁门左道PPT"
    p_tag.font.size = Pt(16)
    p_tag.font.bold = True
    p_tag.font.color.rgb = RGBColor(*start_color) # Use the Cyan accent

    prs.save(output_pptx_path)
    return output_pptx_path
