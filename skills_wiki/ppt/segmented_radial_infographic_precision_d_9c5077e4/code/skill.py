def create_slide(
    output_pptx_path: str,
    title_text: str = "Core Architecture",
    body_text: str = "A precisely engineered 14-point cycle.",
    segments: int = 14,
    gap_degrees: float = 3.5,
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Segmented Radial Infographic visual effect.
    """
    import math
    import io
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from PIL import Image, ImageDraw, ImageFilter
    
    # Initialize Presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide_layout = prs.slide_layouts[6] # Blank layout
    slide = prs.slides.add_slide(slide_layout)

    # Theme Colors
    bg_color = (18, 22, 28)
    color_palette = [
        (0, 191, 255, 255),   # Cyan
        (255, 140, 0, 255),   # Orange
        (0, 250, 154, 255),   # Medium Spring Green
        (147, 112, 219, 255)  # Medium Purple
    ]

    # Set Background
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*bg_color)

    # === Layer 1: PIL Generation of the Segmented Donut ===
    # Using high resolution for anti-aliasing
    img_size = 1200
    canvas = Image.new('RGBA', (img_size, img_size), (0, 0, 0, 0))
    shadow_canvas = Image.new('RGBA', (img_size, img_size), (0, 0, 0, 0))
    
    draw = ImageDraw.Draw(canvas)
    shadow_draw = ImageDraw.Draw(shadow_canvas)
    
    # Graphic constraints
    ring_thickness = 140
    margin = 100
    bbox = [margin, margin, img_size - margin, img_size - margin]
    
    # Calculate sweep of each segment
    sweep_angle = 360 / segments
    
    for i in range(segments):
        # Calculate angles, incorporating the boolean "gap" equivalent to the tutorial's line
        start_angle = (i * sweep_angle) + (gap_degrees / 2)
        end_angle = ((i + 1) * sweep_angle) - (gap_degrees / 2)
        
        # Select alternating color
        color = color_palette[i % len(color_palette)]
        
        # Draw shadow arc (black, slightly offset)
        shadow_draw.arc(bbox, start_angle, end_angle, fill=(0, 0, 0, 150), width=ring_thickness)
        
        # Draw main segment arc
        draw.arc(bbox, start_angle, end_angle, fill=color, width=ring_thickness)

    # Blur the shadow layer
    shadow_canvas = shadow_canvas.filter(ImageFilter.GaussianBlur(15))
    
    # Composite main graphics over shadow
    final_img = Image.alpha_composite(shadow_canvas, canvas)
    
    # Save to in-memory stream
    img_stream = io.BytesIO()
    final_img.save(img_stream, format='PNG')
    img_stream.seek(0)

    # === Layer 2: Insert into PPTX ===
    # Place graphic on the right side
    graphic_size = Inches(6.5)
    pic_left = Inches(6.0)
    pic_top = Inches(0.5)
    slide.shapes.add_picture(img_stream, pic_left, pic_top, graphic_size, graphic_size)

    # === Layer 3: PPTX Text Elements ===
    # Title Text (Left Panel)
    tx_box = slide.shapes.add_textbox(Inches(1.0), Inches(2.5), Inches(4.5), Inches(1.5))
    tf = tx_box.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = title_text.upper()
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.font.name = "Arial"
    
    p2 = tf.add_paragraph()
    p2.text = body_text
    p2.font.size = Pt(18)
    p2.font.color.rgb = RGBColor(180, 180, 190)
    p2.font.name = "Arial"

    # Central Callout inside the Donut
    center_box = slide.shapes.add_textbox(Inches(7.75), Inches(3.25), Inches(3.0), Inches(1.0))
    center_tf = center_box.text_frame
    center_p = center_tf.paragraphs[0]
    center_p.text = str(segments)
    center_p.font.size = Pt(64)
    center_p.font.bold = True
    center_p.font.color.rgb = RGBColor(255, 255, 255)
    center_p.alignment = 2 # center alignment
    
    center_p2 = center_tf.add_paragraph()
    center_p2.text = "MODULES"
    center_p2.font.size = Pt(16)
    center_p2.font.bold = True
    center_p2.font.color.rgb = RGBColor(*color_palette[0][:3])
    center_p2.alignment = 2 # center alignment

    # Save Presentation
    prs.save(output_pptx_path)
    return output_pptx_path
