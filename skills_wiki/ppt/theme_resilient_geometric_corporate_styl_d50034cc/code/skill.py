import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

def create_slide(
    output_pptx_path: str,
    title_text: str = "Free Basic\nPresentation",
    subtitle_text: str = "Reimagined by Automated Design Agent",
    bg_color: tuple = (36, 54, 214),      # Royal Blue
    accent_color: tuple = (235, 52, 64),  # Bold Coral/Red
    text_color: tuple = (255, 255, 255),  # White
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the "Theme-Resilient Geometric Corporate" template style.
    Features robust text margins and edge-anchored vector shapes.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use a blank slide layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # === Layer 1: Background ===
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*bg_color)
    
    # === Layer 2: Geometric Accents ===
    
    # 2a. Right-side Vertical Stripes
    stripe_width = Inches(0.15)
    stripe_height = Inches(4.5)
    start_x = Inches(12.0)
    
    for i in range(3):
        stripe = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            start_x + (i * Inches(0.35)), Inches(0), stripe_width, stripe_height
        )
        stripe.fill.solid()
        stripe.fill.fore_color.rgb = RGBColor(*accent_color)
        stripe.line.fill.background() # Remove border
        
    # 2b. Bottom-Right Anchor Circle (Half visible)
    circle_size = Inches(2.5)
    anchor_circle = slide.shapes.add_shape(
        MSO_SHAPE.OVAL,
        Inches(11.5), Inches(6.25), circle_size, circle_size
    )
    anchor_circle.fill.solid()
    anchor_circle.fill.fore_color.rgb = RGBColor(*accent_color)
    anchor_circle.line.fill.background()
    
    # 2c. Left-side Concentric Rings
    # Using hollow circles (DONUT shapes) to create the line rings
    ring_center_x = Inches(-1.5)
    ring_center_y = Inches(3.0)
    
    for i in range(3):
        radius = Inches(3.5 + (i * 0.8))
        ring = slide.shapes.add_shape(
            MSO_SHAPE.DONUT,
            ring_center_x, ring_center_y, radius, radius
        )
        ring.fill.solid()
        # White rings with high transparency to mimic the video's subtle background pattern
        ring.fill.fore_color.rgb = RGBColor(255, 255, 255)
        # We adjust the donut hole to make the ring very thin
        ring.adjustments[0] = 0.98 
        ring.line.fill.background()
        
        # Approximate transparency by formatting XML directly or relying on thin lines
        # Here we use thin line to keep it clean natively if transparency isn't perfectly supported
        ring.line.color.rgb = RGBColor(255,255,255)
        ring.line.width = Pt(1)

    # === Layer 3: Text Boxes & Typography ===
    
    # Ensure standard margins as explicitly taught in the tutorial
    margin_left_right = Inches(0.1)
    margin_top_bottom = Inches(0.05)
    
    # Subtitle / Logo Placeholder (Top Left)
    logo_box = slide.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(4.0), Inches(0.5))
    tf_logo = logo_box.text_frame
    tf_logo.margin_left = margin_left_right
    tf_logo.margin_right = margin_left_right
    tf_logo.margin_top = margin_top_bottom
    tf_logo.margin_bottom = margin_top_bottom
    p_logo = tf_logo.paragraphs[0]
    p_logo.text = "❖ YOUR LOGO"
    p_logo.font.name = "Arial Black"
    p_logo.font.size = Pt(16)
    p_logo.font.color.rgb = RGBColor(*text_color)
    
    # Main Title (Center Left)
    title_box = slide.shapes.add_textbox(Inches(1.0), Inches(3.0), Inches(8.0), Inches(2.0))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = margin_left_right
    tf_title.margin_right = margin_left_right
    tf_title.margin_top = margin_top_bottom
    tf_title.margin_bottom = margin_top_bottom
    
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.name = "Arial Black"
    p_title.font.size = Pt(64)
    p_title.font.color.rgb = RGBColor(*text_color)
    p_title.line_spacing = 1.0
    
    # Presenter / Subtitle (Bottom Left)
    sub_box = slide.shapes.add_textbox(Inches(1.0), Inches(6.5), Inches(8.0), Inches(0.5))
    tf_sub = sub_box.text_frame
    tf_sub.margin_left = margin_left_right
    tf_sub.margin_right = margin_left_right
    tf_sub.margin_top = margin_top_bottom
    tf_sub.margin_bottom = margin_top_bottom
    
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = subtitle_text
    p_sub.font.name = "Arial"
    p_sub.font.size = Pt(18)
    p_sub.font.color.rgb = RGBColor(*text_color)

    # Save presentation
    prs.save(output_pptx_path)
    return output_pptx_path
