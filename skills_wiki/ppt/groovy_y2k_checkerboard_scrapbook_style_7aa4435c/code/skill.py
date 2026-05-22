import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from PIL import Image, ImageDraw

def create_slide(
    output_pptx_path: str,
    title_text: str = "GROUP\nPROJECT",
    subtitle_text: str = "Presented by: Group 2",
    **kwargs
) -> str:
    """
    Creates a PPTX file reproducing the Groovy Y2K Checkerboard Scrapbook Style.
    """
    
    # --- Theme Colors (RGBA / RGB) ---
    C_PASTEL_BLUE = (189, 212, 231)
    C_MID_BLUE    = (141, 176, 211)
    C_NAVY_DARK   = (43, 62, 98)
    C_OFF_WHITE   = (242, 245, 235)
    
    # Presentation Setup (16:9)
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide_layout = prs.slide_layouts[6] # Blank slide
    slide = prs.slides.add_slide(slide_layout)

    # ==========================================
    # Layer 1: Background Generation (PIL)
    # ==========================================
    bg_path = "temp_checkerboard_bg.png"
    width, height = 1920, 1080
    square_size = 135
    
    bg_img = Image.new('RGB', (width, height), C_PASTEL_BLUE)
    draw = ImageDraw.Draw(bg_img)
    
    for y in range(0, height, square_size):
        for x in range(0, width, square_size):
            # Alternating pattern
            if (x // square_size + y // square_size) % 2 == 1:
                draw.rectangle([x, y, x + square_size, y + square_size], fill=C_MID_BLUE)
                
    bg_img.save(bg_path)
    
    # Insert Background
    slide.shapes.add_picture(bg_path, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # ==========================================
    # Layer 2: Decorative Abstract Shapes (PIL)
    # ==========================================
    decor_path = "temp_retro_rings.png"
    decor_size = 400
    ring_img = Image.new('RGBA', (decor_size, decor_size), (255, 255, 255, 0))
    r_draw = ImageDraw.Draw(ring_img)
    
    # Draw concentric quarter circles (retro vibe)
    center = (0, decor_size)
    r_draw.pieslice([-100, decor_size-300, 300, decor_size+300], 270, 360, fill=C_NAVY_DARK)
    r_draw.pieslice([-60, decor_size-260, 260, decor_size+260], 270, 360, fill=C_PASTEL_BLUE)
    r_draw.pieslice([-20, decor_size-220, 220, decor_size+220], 270, 360, fill=C_NAVY_DARK)
    r_draw.pieslice([20, decor_size-180, 180, decor_size+180], 270, 360, fill=C_MID_BLUE)
    
    ring_img.save(decor_path)
    
    # Insert decor in corners
    # Bottom Left
    slide.shapes.add_picture(decor_path, Inches(0), Inches(4.5), width=Inches(3), height=Inches(3))
    # Top Right (Rotated)
    pic2 = slide.shapes.add_picture(decor_path, Inches(10.333), Inches(0), width=Inches(3), height=Inches(3))
    pic2.rotation = 180

    # ==========================================
    # Layer 3: Main Central UI Box
    # ==========================================
    box_width = Inches(8.5)
    box_height = Inches(4.5)
    box_left = (prs.slide_width - box_width) / 2
    box_top = (prs.slide_height - box_height) / 2

    # Outer border/shadow box (Navy)
    shadow_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, box_left + Inches(0.08), box_top + Inches(0.08), box_width, box_height)
    shadow_box.fill.solid()
    shadow_box.fill.fore_color.rgb = RGBColor(*C_NAVY_DARK)
    shadow_box.line.color.rgb = RGBColor(*C_NAVY_DARK)
    shadow_box.adjustments[0] = 0.25 # Roundness

    # Inner main box (Mid Blue to match the template's central pill)
    main_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, box_left, box_top, box_width, box_height)
    main_box.fill.solid()
    main_box.fill.fore_color.rgb = RGBColor(*C_MID_BLUE)
    main_box.line.color.rgb = RGBColor(*C_NAVY_DARK)
    main_box.line.width = Pt(4)
    main_box.adjustments[0] = 0.25 # Roundness

    # Inner dotted/dashed border (A common scrapbook trope seen in the template)
    inner_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, box_left + Inches(0.2), box_top + Inches(0.2), box_width - Inches(0.4), box_height - Inches(0.4))
    inner_box.fill.background() # transparent
    inner_box.line.color.rgb = RGBColor(*C_PASTEL_BLUE)
    inner_box.line.width = Pt(3)
    inner_box.adjustments[0] = 0.22

    # ==========================================
    # Layer 4: Typography with Hard "Sticker" Shadows
    # ==========================================
    
    def add_hard_shadow_text(slide, text, left, top, width, height, font_size, primary_color, shadow_color):
        """Helper to create the retro offset text shadow effect"""
        # 1. Background Shadow Text
        shadow_tb = slide.shapes.add_textbox(left + Inches(0.06), top + Inches(0.06), width, height)
        shadow_p = shadow_tb.text_frame.add_paragraph()
        shadow_p.text = text
        shadow_p.alignment = PP_ALIGN.CENTER
        shadow_p.font.size = Pt(font_size)
        shadow_p.font.name = "Arial Black" # Closest standard thick font
        shadow_p.font.color.rgb = RGBColor(*shadow_color)
        
        # 2. Foreground Main Text
        main_tb = slide.shapes.add_textbox(left, top, width, height)
        main_p = main_tb.text_frame.add_paragraph()
        main_p.text = text
        main_p.alignment = PP_ALIGN.CENTER
        main_p.font.size = Pt(font_size)
        main_p.font.name = "Arial Black"
        main_p.font.color.rgb = RGBColor(*primary_color)

    # Title Text (Centered in the box)
    title_top = box_top + Inches(0.5)
    add_hard_shadow_text(
        slide, title_text, 
        left=box_left, top=title_top, 
        width=box_width, height=Inches(2), 
        font_size=72, 
        primary_color=C_OFF_WHITE, 
        shadow_color=C_NAVY_DARK
    )

    # Subtitle Text (Below title)
    sub_tb = slide.shapes.add_textbox(box_left, box_top + Inches(3.2), box_width, Inches(1))
    sub_p = sub_tb.text_frame.add_paragraph()
    sub_p.text = subtitle_text
    sub_p.alignment = PP_ALIGN.CENTER
    sub_p.font.size = Pt(24)
    sub_p.font.name = "Century Gothic" # Clean sans to contrast the bold title
    sub_p.font.color.rgb = RGBColor(*C_NAVY_DARK)

    # ==========================================
    # Cleanup & Save
    # ==========================================
    prs.save(output_pptx_path)
    
    # Clean up temp files
    if os.path.exists(bg_path):
        os.remove(bg_path)
    if os.path.exists(decor_path):
        os.remove(decor_path)
        
    return output_pptx_path

# Example execution if run standalone:
# create_slide("groovy_y2k_checkerboard.pptx")
