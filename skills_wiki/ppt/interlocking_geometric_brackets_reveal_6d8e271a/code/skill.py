def create_slide(
    output_pptx_path: str,
    title_text: str = "WELCOME",
    left_color: tuple = (237, 125, 49),   # Orange
    right_color: tuple = (38, 38, 38),    # Dark Gray
    bg_color: tuple = (248, 249, 250),    # Off-White
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the "Interlocking Geometric Brackets" visual effect.
    
    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    
    # Initialize presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout
    
    # 1. Set Background
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*bg_color)
    
    # --- Geometric Polygon Math ---
    # We construct the custom polygon for the Left Bracket using pure math
    # to ensure perfect 45-degree parallel angles and exact thickness.
    cx, cy = 13.333 / 2, 7.5 / 2  # Slide Center
    
    W = 1.8       # Width of the top angled slash
    H = 4.2       # Total height of the outer vertical edge
    T = 0.7       # Thickness of the shape strokes
    T_diag = T * 1.4142 # Diagonal extension required to maintain thickness T at 45 degrees
    
    # Points defining the left bracket (origin at top-right of the angled slash)
    # Winding path: Outer top-right -> Outer slant -> Outer vertical -> Bottom flat -> Inner vertical -> Inner slant -> Top flat
    pts = [
        (W, 0),                  
        (0, W),                  
        (0, H),                  
        (T, H),                  
        (T, W + T_diag - T),     
        (W + T_diag, 0)          
    ]
    
    # Define origin placement for the Left Bracket
    origin_x = cx - 5.0  # Pushed left to create a gap for the text
    origin_y = cy - (H / 2)
    
    # Calculate global coordinates for Left Bracket
    left_pts = [(origin_x + x, origin_y + y) for x, y in pts]
    
    # Calculate global coordinates for Right Bracket (180-degree mathematical mirror)
    right_pts = [(cx + (cx - px), cy + (cy - py)) for px, py in left_pts]
    
    def draw_polygon(slide, points_array, color):
        """Helper to draw a custom vector polygon using FreeformBuilder."""
        start_pt = points_array[0]
        ff_builder = slide.shapes.build_freeform(Inches(start_pt[0]), Inches(start_pt[1]))
        
        # Add remaining segments and close the shape
        ff_builder.add_line_segments([(Inches(x), Inches(y)) for x, y in points_array[1:]], close=True)
        shape = ff_builder.convert_to_shape()
        
        # Style the shape
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(*color)
        shape.line.fill.solid()
        shape.line.color.rgb = RGBColor(*color) # Match line to fill to avoid ghost borders
        shape.line.width = Pt(0)
        return shape

    # 2. Draw Left Bracket
    draw_polygon(slide, left_pts, left_color)
    
    # 3. Draw Right Bracket
    draw_polygon(slide, right_pts, right_color)
    
    # 4. Add Central Title Text
    tw, th = Inches(8.0), Inches(2.0)
    tx, ty = Inches(cx) - tw/2, Inches(cy) - th/2
    tb = slide.shapes.add_textbox(tx, ty, tw, th)
    tf = tb.text_frame
    tf.word_wrap = False
    
    # Configure Text
    p = tf.paragraphs[0]
    p.text = title_text.upper()
    p.alignment = PP_ALIGN.CENTER
    
    font = p.runs[0].font
    font.name = "Arial Black"
    font.size = Pt(65)
    font.bold = True
    font.color.rgb = RGBColor(0, 0, 0)
    
    # Save the presentation
    prs.save(output_pptx_path)
    return output_pptx_path
