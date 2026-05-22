import os
import urllib.request
from io import BytesIO
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image, ImageFilter, ImageDraw

def create_slide(
    output_pptx_path: str,
    title_text: str = "Personal\nCV/RESUME",
    active_step_index: int = 1,  # 0 to 4
    content_title: str = "Work Experience",
    content_bullets: list = None,
    bg_keyword: str = "city,night,architecture",
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the Cinematic Horizontal Stepper layout.
    """
    if content_bullets is None:
        content_bullets = [
            "Senior Manager at WESTIN Group (2013.05 - 2014.05)",
            "Led cross-functional teams in luxury hospitality sector",
            "Product Manager at Tech Innovations (2014.05 - 2016.02)",
            "Spearheaded digital transformation initiatives"
        ]

    steps = ["Education", "Work", "Skills", "About", "Portfolio"]
    
    # 1. Setup Presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # Colors
    color_bg_tint = (20, 25, 32, 220) # RGBA Deep slate dark
    color_inactive_ui = RGBColor(100, 115, 130)
    color_active_ui = RGBColor(255, 255, 255)
    
    # === Layer 1: Background Generation via PIL ===
    bg_img_path = "temp_cinematic_bg.png"
    try:
        # Fetch image
        url = f"https://source.unsplash.com/random/1920x1080/?{bg_keyword}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            img = Image.open(BytesIO(response.read())).convert("RGBA")
    except Exception:
        # Fallback to dark gradient/solid if network fails
        img = Image.new("RGBA", (1920, 1080), (40, 45, 55, 255))
    
    # Apply Blur
    img = img.filter(ImageFilter.GaussianBlur(radius=15))
    
    # Apply Dark Overlay
    overlay = Image.new("RGBA", img.size, color_bg_tint)
    final_bg = Image.alpha_composite(img, overlay)
    final_bg.save(bg_img_path)
    
    # Insert Background
    slide.shapes.add_picture(bg_img_path, 0, 0, prs.slide_width, prs.slide_height)

    # === Layer 2: Top Header Area ===
    # Top Bar separator line
    top_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.2), Inches(13.333), Inches(0.02))
    top_line.fill.solid()
    top_line.fill.fore_color.rgb = color_inactive_ui
    top_line.line.fill.background()

    # Main Title
    tx_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(3), Inches(0.8))
    tf = tx_box.text_frame
    p = tf.add_paragraph()
    p.text = title_text
    p.font.size = Pt(18)
    p.font.color.rgb = color_active_ui
    p.font.bold = True

    # Global Traits (Top Right)
    traits = "Adaptability    |    Responsibility    |    Passion    |    Self-control"
    tx_box_traits = slide.shapes.add_textbox(Inches(5), Inches(0.5), Inches(8), Inches(0.5))
    tf_traits = tx_box_traits.text_frame
    p_traits = tf_traits.add_paragraph()
    p_traits.text = traits
    p_traits.font.size = Pt(14)
    p_traits.font.color.rgb = color_active_ui
    p_traits.alignment = PP_ALIGN.RIGHT

    # === Layer 3: The Stepper Navigation ===
    track_y = Inches(3.0)
    track_start_x = Inches(2.5)
    track_end_x = Inches(10.8)
    track_width = track_end_x - track_start_x
    
    # Main horizontal track line
    track_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, track_start_x, track_y, track_width, Inches(0.02))
    track_line.fill.solid()
    track_line.fill.fore_color.rgb = color_inactive_ui
    track_line.line.fill.background()

    # Draw Nodes
    num_steps = len(steps)
    step_spacing = track_width / (num_steps - 1)
    
    for i, step_name in enumerate(steps):
        is_active = (i == active_step_index)
        node_x = track_start_x + (i * step_spacing)
        
        # Node Circle
        radius = Inches(0.08) if not is_active else Inches(0.12)
        circle = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, 
            node_x - radius, 
            track_y - radius + Inches(0.01), 
            radius*2, 
            radius*2
        )
        circle.fill.solid()
        circle.fill.fore_color.rgb = color_active_ui if is_active else color_inactive_ui
        circle.line.fill.background()
        
        # Number above
        num_box = slide.shapes.add_textbox(node_x - Inches(0.5), track_y - Inches(0.8), Inches(1), Inches(0.5))
        p_num = num_box.text_frame.add_paragraph()
        p_num.text = str(i + 1)
        p_num.font.size = Pt(20)
        p_num.font.bold = True
        p_num.font.color.rgb = color_active_ui if is_active else color_inactive_ui
        p_num.alignment = PP_ALIGN.CENTER
        
        # Text below
        lbl_box = slide.shapes.add_textbox(node_x - Inches(0.75), track_y + Inches(0.2), Inches(1.5), Inches(0.5))
        p_lbl = lbl_box.text_frame.add_paragraph()
        p_lbl.text = step_name
        p_lbl.font.size = Pt(14)
        p_lbl.font.color.rgb = color_active_ui if is_active else color_inactive_ui
        p_lbl.alignment = PP_ALIGN.CENTER

        # Active State Vertical Drop Line
        if is_active:
            drop_length = Inches(1.2)
            drop_line = slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE, 
                node_x - Inches(0.01), 
                track_y, 
                Inches(0.02), 
                drop_length
            )
            drop_line.fill.solid()
            drop_line.fill.fore_color.rgb = color_active_ui
            drop_line.line.fill.background()
            
            # Tiny play/arrow icon at the end of the line
            arrow = slide.shapes.add_shape(
                MSO_SHAPE.ISOSCELES_TRIANGLE,
                node_x - Inches(0.08),
                track_y + drop_length,
                Inches(0.16),
                Inches(0.16)
            )
            arrow.rotation = 180
            arrow.fill.solid()
            arrow.fill.fore_color.rgb = color_active_ui
            arrow.line.fill.background()

    # === Layer 4: Content Area ===
    # We base the content position roughly under the active node, clamped to slide boundaries
    content_x = max(Inches(1.0), track_start_x + (active_step_index * step_spacing) - Inches(2.5))
    content_y = track_y + Inches(1.6)
    
    # Section Title
    title_box = slide.shapes.add_textbox(content_x, content_y, Inches(8), Inches(0.5))
    p_ct = title_box.text_frame.add_paragraph()
    p_ct.text = f"|  {content_title}  |"
    p_ct.font.size = Pt(16)
    p_ct.font.color.rgb = color_inactive_ui
    
    # Bullets
    body_box = slide.shapes.add_textbox(content_x + Inches(0.2), content_y + Inches(0.5), Inches(8), Inches(2.5))
    tf_body = body_box.text_frame
    for bullet in content_bullets:
        p_b = tf_body.add_paragraph()
        p_b.text = bullet
        p_b.font.size = Pt(14)
        p_b.font.color.rgb = color_active_ui
        p_b.level = 0
        p_b.space_after = Pt(10)

    prs.save(output_pptx_path)
    
    # Clean up temp file
    if os.path.exists(bg_img_path):
        os.remove(bg_img_path)
        
    return output_pptx_path
